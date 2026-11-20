"""API demo BHYT (spec mục 11b). Chạy: uvicorn src.app:app --host 127.0.0.1 --port 8000"""
import functools
import importlib
import json
import math
import os
import re
import uuid
from concurrent.futures import ThreadPoolExecutor
from contextlib import asynccontextmanager
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import yaml
from fastapi import Body, FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
from starlette.middleware.trustedhost import TrustedHostMiddleware

from src import auth, do_luong, luu_tru
from src.luu_tru import TAI_KHOAN_TAM

ROOT = Path(__file__).resolve().parent.parent
RULES_DIR = ROOT / "data" / "rules"
LOG_PATH = ROOT / "logs" / "xac-nhan.jsonl"
CASES_PATH = ROOT / "data" / "test-cases" / "demo.yaml"
# ca bác sĩ tự tạo trên màn hình; để ngoài test-cases/ để eval không quét phải (ca này không có nhãn)
TU_TAO_PATH = ROOT / "data" / "ca-tu-tao.yaml"
TU_TAO_ID = re.compile(r"^TU-[A-Z0-9]{1,20}$")
# mặc định của app mô phỏng (engine không có mặc định; test-cases/README.md)
NGAY_KHAM = "2026-11-12"
MAX_CHI_DINH, MAX_PHIEU = 50, 20000  # chặn body bất thường trước khi gửi A1
GIOI_HAN_AI_NGAY = 50  # lượt bấm "Kiểm tra BHYT" của mỗi tài khoản mỗi ngày, để khóa OpenAI không bị dùng quá mức
GIO_VN = timezone(timedelta(hours=7))
LY_DO = ("nguoi_nha_yeu_cau", "loai_tru_theo_doi", "khong_dong_y", "khac")
F13 = ("thu_tu", "ma", "ten", "trang_thai", "o_bhyt_goi_y", "bac_si_chon", "checklist", "can_cu", "phien_ban_rule")
DAU_VAO = ("tuoi", "the", "icd", "sinh_hieu", "lich_su_da_dung")
PHIEU_O = ("ly_do", "benh_su", "tien_su", "kham", "chan_doan", "xu_tri")  # các ô của trang Phiếu khám ngoại trú
LICH_SU_KHOA = ("ma", "ten", "ngay_cach", "ket_qua", "tham_chieu_tren", "don_vi")
TRUONG_CA_DO = ("id", "benh_nhan", "sinh_hieu", "icd", "phieu_kham", "phieu_o", "lich_su", "ngay_kham")  # trường ca đo được gửi cho bác sĩ

# test gán trực tiếp các khóa này
state = {"rules": None, "check": None, "a1": None, "a1_mode": "off", "model": None, "reasoning_effort": None,
         "lq": None, "kho": luu_tru.KhoFile(TU_TAO_PATH, LOG_PATH)}


def load_env(path=ROOT / ".env"):
    """KEY=value; biến môi trường đã có thắng .env; KEY= (trống) bị bỏ qua. utf-8-sig: Notepad hay ghi BOM."""
    if not Path(path).exists():
        return
    for line in Path(path).read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            v = v.strip().strip("\"'")
            if v:
                os.environ.setdefault(k.strip(), v)


@asynccontextmanager
async def lifespan(_app):
    load_env()
    state["kho"] = luu_tru.tao_kho(TU_TAO_PATH, LOG_PATH)
    rules = importlib.import_module("src.rules").load_rules(RULES_DIR)
    state["rules"] = rules
    state["check"] = importlib.import_module("src.engine").check
    key, model = os.environ.get("OPENAI_API_KEY"), os.environ.get("OPENAI_MODEL") or None
    effort = os.environ.get("A1_REASONING_EFFORT") or None
    mode = (os.environ.get("A1_MODE") or ("live" if key else "off")).strip().lower()
    if mode not in ("live", "stub", "off") or (mode == "live" and not (key and model)):
        mode = "off"  # thiếu khóa/model hoặc giá trị lạ: không gọi được → mọi vế AI chưa thấy
    state.update(a1_mode=mode, model=model, reasoning_effort=effort, a1=None, lq=None)
    if mode == "live":
        khoang = (rules.tham_so or {}).get("khoang_hop_le")
        if isinstance(khoang, dict) and "gia_tri" in khoang:
            khoang = khoang["gia_tri"]
        state["a1"] = importlib.import_module("src.a1").make_live(
            model, float(os.environ.get("A1_TIMEOUT_S") or 8), khoang,
            **({"reasoning_effort": effort} if effort else {}))  # chỉ truyền khi có đặt: make_live cũ không nhận tham số này
        if (os.environ.get("LQ_MODE") or "off").strip().lower() == "live":  # A3 tắt mặc định (docs/02)
            state["lq"] = importlib.import_module("src.a1").make_lien_quan(
                model, float(os.environ.get("A1_TIMEOUT_S") or 8), effort)
    print(f"[bhyt] a1_mode={mode} model={model} reasoning_effort={effort} rules={rules.phien_ban_rule[:10]} "
          f"kho={type(state['kho']).__name__}")
    yield


app = FastAPI(title="Trợ lý BHYT (demo)", lifespan=lifespan)


@app.middleware("http")
async def _bat_dang_nhap(request: Request, call_next):
    """Mọi đường dẫn đều cần đăng nhập, trừ trang đăng nhập."""
    if request.url.path == "/dang-nhap":
        return await call_next(request)
    tai_khoan = auth.doc_phien(request.cookies.get(auth.COOKIE))
    if tai_khoan is None:
        if request.url.path == "/":
            return RedirectResponse("/dang-nhap", status_code=303)
        return JSONResponse({"detail": "Cần đăng nhập."}, status_code=401)
    request.state.tai_khoan = tai_khoan
    return await call_next(request)


# chỉ nhận Host đã khai báo: chặn DNS rebinding (trang lạ gọi /check tốn khóa OpenAI, hoặc ghi log giả).
# Thêm sau cùng để chạy trước đăng nhập. Bản host khai báo tên miền trong ALLOWED_HOSTS (cách nhau bằng dấu phẩy).
app.add_middleware(TrustedHostMiddleware, allowed_hosts=[
    "127.0.0.1", "localhost", *(h.strip() for h in os.environ.get("ALLOWED_HOSTS", "").split(",") if h.strip())])


@app.exception_handler(RequestValidationError)
async def _bad_body(_req: Request, _exc):
    return JSONResponse({"detail": "Dữ liệu gửi lên phải là một đối tượng JSON."}, status_code=422)


@app.get("/dang-nhap")
def trang_dang_nhap(request: Request):
    if auth.doc_phien(request.cookies.get(auth.COOKIE)):
        return RedirectResponse("/", status_code=303)
    return FileResponse(ROOT / "web" / "dang-nhap.html")


@app.post("/dang-nhap")
def dang_nhap(request: Request, body: dict = Body(...)):
    if not auth.da_cau_hinh():
        raise HTTPException(503, "Hệ thống chưa được cấu hình đăng nhập.")
    if body.get("cam_ket") is not True:
        _fail("Cần xác nhận chỉ nhập dữ liệu giả.")
    tai_khoan = body.get("tai_khoan")
    if not auth.dung_mat_khau(tai_khoan, body.get("mat_khau")):
        raise HTTPException(401, "Sai tài khoản hoặc mật khẩu.")
    res = JSONResponse({"tai_khoan": tai_khoan})
    res.set_cookie(auth.COOKIE, auth.tao_phien(tai_khoan), max_age=auth.THOI_HAN_S, httponly=True, samesite="lax",
                   secure=request.headers.get("x-forwarded-proto", request.url.scheme) == "https")
    return res


@app.post("/dang-xuat")
def dang_xuat():
    res = JSONResponse({"dang_xuat": True})
    res.delete_cookie(auth.COOKIE)
    return res


@app.get("/toi")
def toi(request: Request):
    return {"tai_khoan": request.state.tai_khoan}


def _hom_nay():
    return datetime.now(GIO_VN).date().isoformat()


def _plain(x):
    return json.loads(json.dumps(x, default=str, ensure_ascii=False))  # date của YAML → chuỗi


def _demo_cases(tai_khoan=TAI_KHOAN_TAM):
    raw = (yaml.safe_load(CASES_PATH.read_text(encoding="utf-8")) or []) + \
        [{**c, "tu_tao": True} for c in state["kho"].ds_ca(tai_khoan)]
    return [_chuan_hoa_ca(c) for c in raw]


def _chuan_hoa_ca(c):
    c = _plain(c)
    bn = c.setdefault("benh_nhan", {})
    if "the" not in bn:
        thang = bn["tuoi_thang"] if bn.get("tuoi_thang") is not None else (bn.get("tuoi_ngay") or 0) / 30.44
        bn["the"] = {"han_den": "2026-12-31", "muc_huong": 100 if thang < 72 else 80}
    c.setdefault("luot_kham", "LK-" + c["id"])
    c.setdefault("ngay_kham", NGAY_KHAM)
    c.setdefault("lich_su", [])
    return c


def _fail(msg):
    raise HTTPException(422, msg)


def _num(x):
    # json của Python nhận NaN/Infinity: phải chặn, NaN làm mọi phép so sánh sai → vế trượt
    return x is None or (isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x))


def _ngay(x):
    if x is None:
        return True
    try:
        date.fromisoformat(x)
        return True
    except (TypeError, ValueError):
        return False


def _validate_luot(b, cho_rong=False):
    """Kiểu dữ liệu ở biên tin cậy, để engine không 500 vì body lạ. Thiếu khóa vẫn được (engine → Cần xem lại).
    cho_rong: ca tự tạo được lưu khi chưa có chỉ định nào."""
    if not isinstance(b.get("luot_kham"), str) or not b["luot_kham"]:
        _fail("Thiếu 'luot_kham' (chuỗi).")
    cd = b.get("chi_dinh")
    if not isinstance(cd, list) or (not cd and not cho_rong) or len(cd) > MAX_CHI_DINH:
        _fail(f"'chi_dinh' cần danh sách 1–{MAX_CHI_DINH} chỉ định.")
    for i, r in enumerate(cd, 1):
        if not isinstance(r, dict) or not isinstance(r.get("ten"), str) or not r["ten"].strip() \
                or not isinstance(r.get("ma"), (str, type(None))):
            _fail(f"Chỉ định thứ {i} thiếu 'ten' hoặc 'ma' không phải chuỗi.")
    if not isinstance(b.get("phieu_kham", ""), str) or len(b.get("phieu_kham") or "") > MAX_PHIEU:
        _fail(f"'phieu_kham' phải là chuỗi ≤ {MAX_PHIEU} ký tự.")
    if not _ngay(b.get("ngay_kham")):
        _fail("'ngay_kham' phải có dạng YYYY-MM-DD.")
    for k, t in (("benh_nhan", dict), ("sinh_hieu", dict), ("icd", list), ("lich_su", list)):
        if k in b and not isinstance(b[k], t):
            _fail(f"'{k}' sai kiểu dữ liệu.")
    bn = b.get("benh_nhan") or {}
    if not (_num(bn.get("tuoi_ngay")) and _num(bn.get("tuoi_thang"))):
        _fail("Tuổi phải là số.")
    the = bn.get("the")
    if the is not None and not (isinstance(the, dict) and _ngay(the.get("han_den")) and _num(the.get("muc_huong"))):
        _fail("'the' cần {han_den: YYYY-MM-DD, muc_huong: số}.")
    if not all(_num(v) for v in (b.get("sinh_hieu") or {}).values()):
        _fail("Sinh hiệu phải là số (dấu chấm thập phân).")
    if not all(isinstance(x, str) for x in b.get("icd") or []):
        _fail("'icd' là danh sách mã chuỗi.")
    for r in b.get("lich_su") or []:
        if not (isinstance(r, dict) and isinstance(r.get("ma"), (str, type(None)))
                and all(_num(r.get(k)) for k in ("ngay_cach", "ket_qua", "tham_chieu_tren"))
                and (r.get("ngay_cach") or 0) >= 0):  # âm = làm "trong tương lai" → tần suất < 24 giờ sai
            _fail("'lich_su' sai kiểu dữ liệu.")


def _stub_for(case, luot):
    """Stub khóa câu hỏi theo thu_tu của ca đầy đủ; bác sĩ có thể chỉ gửi một phần chỉ định → đổi khóa qua lại."""
    stub = importlib.import_module("tests.stub_a1").make_stub(case)
    goc, dung = {}, set()
    for i, cd in enumerate(luot["chi_dinh"], 1):
        j = next((j for j, x in enumerate(case.get("chi_dinh") or [], 1) if j not in dung
                  and ((x.get("ma") and x.get("ma") == cd.get("ma")) or x.get("ten") == cd.get("ten"))), None)
        if j:
            dung.add(j)
            goc[str(i)] = str(j)
    ve_lai = {v: k for k, v in goc.items()}

    def doi(khoa, bang):
        tt, vid = khoa.split(":", 1)
        return f"{bang.get(tt, '0')}:{vid}"  # '0' = dòng không có trong ca → stub trả chua_thay

    def a1(req):
        res = stub({**req, "cau_hoi": [{**q, "khoa": doi(q["khoa"], goc)} for q in req.get("cau_hoi") or []]})
        hoi = [q["khoa"] for q in req.get("cau_hoi") or []]
        ve = [{**v, "khoa": hoi[i] if doi(v["khoa"], ve_lai) == "0:" + v["khoa"].split(":", 1)[1] else doi(v["khoa"], ve_lai)}
              for i, v in enumerate(res.get("ve") or [])]
        return {**res, "ve": ve}
    return a1


def _a1_for(luot):
    if state["a1_mode"] != "stub":
        return state["a1"]
    # stub sinh từ ky_vong của ca demo; chỉ import tests/ ở chế độ stub
    for c in yaml.safe_load(CASES_PATH.read_text(encoding="utf-8")) or []:
        if (c.get("luot_kham") or "LK-" + c["id"]) == luot["luot_kham"]:
            try:
                return _stub_for(c, luot)
            except ImportError:
                return None
    return None


def _a1_nho(a1, doc_ai):
    """Nhớ câu trả lời A1 theo (phiếu khám, nội dung câu hỏi): thêm/xóa chỉ định hay ICD không gọi lại A1.
    doc_ai=False (rule tự chạy lại): chỉ dùng câu đã nhớ; câu chưa có → chua_thay + loi 'chua_doc'."""
    if a1 is None:
        return None

    def f(req):
        pk = " ".join((req.get("phieu_kham") or "").split())
        cau, so = req.get("cau_hoi") or [], req.get("so_lieu") or []
        kv = lambda q: (pk, "ve", q.get("mo_ta"), q.get("cau_hoi"))
        ks = lambda s: (pk, "so", s["truong"])
        nho = state["kho"].doc_nho([kv(q) for q in cau] + [ks(s) for s in so])
        loi = None
        if any(kv(q) not in nho for q in cau) or any(ks(s) not in nho for s in so):
            if not doc_ai:
                loi = "chua_doc"
            else:
                res = a1(req) or {}
                loi = res.get("loi")
                if str(loi or "").startswith("a1_"):  # gọi hỏng: không nhớ, lần bấm sau gọi lại
                    return res
                tl = {v["khoa"]: v for v in res.get("ve") or []}
                co = {s["truong"]: s for s in res.get("so_lieu") or []}
                moi = {**{kv(q): tl[q["khoa"]] for q in cau if q["khoa"] in tl},
                       **{ks(s): co.get(s["truong"]) for s in so}}
                state["kho"].ghi_nho(moi)
                nho = {**nho, **moi}
        ve = [{**nho[kv(q)], "khoa": q["khoa"]} if kv(q) in nho else
              {"khoa": q["khoa"], "ket_qua": "chua_thay", "trich_dan": None, "trich_them": [], "trich_lien_quan": [], "chua_doc": True}
              for q in cau]
        return {"ve": ve, "so_lieu": [nho[ks(s)] for s in so if nho.get(ks(s))], "loi": loi}
    return f


@app.post("/check")
def check(request: Request, body: dict = Body(...)):  # def → chạy trong threadpool, A1 chặn tới 8 s không treo server
    _validate_luot(body)
    doc_ai = body.get("doc_ai") is not False  # false = rule tự chạy lại sau khi sửa chỉ định/ICD, không gọi A1
    if do_luong.la_luot_do(body["luot_kham"]):  # lượt tự tra và ca chưa đến lượt không được xem gợi ý của công cụ
        muc = _muc_do_hien_tai(request.state.tai_khoan)
        if not muc or "LK-" + muc["ca"]["id"] != body["luot_kham"] or muc["che_do"] != "cong_cu":
            raise HTTPException(403, "Ca đo này chưa được dùng công cụ kiểm tra.")
    if doc_ai and state["kho"].tang_luot_ai(request.state.tai_khoan, _hom_nay()) > GIOI_HAN_AI_NGAY:
        raise HTTPException(429, f"Tài khoản đã dùng hết {GIOI_HAN_AI_NGAY} lượt Kiểm tra BHYT hôm nay. Vui lòng thử lại vào ngày mai.")
    res = _check(body, doc_ai)
    # mã lần kiểm tra: /confirm ghi lại để biết bác sĩ xác nhận trên kết quả nào
    res["kiem_tra_id"] = uuid.uuid4().hex[:12]
    return res


def _check(body, doc_ai):
    lq = state["lq"] if state["a1_mode"] == "live" and doc_ai else None
    if lq is None:
        return state["check"](body, state["rules"], _a1_nho(_a1_for(body), doc_ai))
    ten = {e["ma"]: e["ten"] for e in icd()}
    req = {"dich_vu": [c["ten"] for c in body["chi_dinh"]], "phieu_kham": body.get("phieu_kham") or "",
           "icd": [{"ma": m, "ten": ten.get(m)} for m in body.get("icd") or []]}
    with ThreadPoolExecutor(1) as ex:  # chạy song song với A1 trong check: không cộng dồn thời gian chờ
        fut = ex.submit(lq, req)
        res = state["check"](body, state["rules"], _a1_nho(_a1_for(body), doc_ai))
        luu_y = fut.result()
    for d in res.get("dong") or []:
        # chỉ dòng "Phù hợp" thuần theo danh mục; không đổi trạng thái hay ô gợi ý (gợi ý AI, không phải quy tắc)
        d["luu_y_ho_so"] = luu_y.get(d.get("thu_tu")) if d.get("ma_ly_do") == "danh_muc" else None
    return res


def _ly_do(d):
    """F-12 / spec §9: cần lý do khi bỏ tích dòng gợi ý 'tich', hoặc tích dòng Không được chi trả.
    Không chặn: thiếu thì ghi {loai: null}. Dòng không cần lý do vẫn giữ lý do hợp lệ nếu có."""
    can = (d["o_bhyt_goi_y"] == "tich" and d["bac_si_chon"] == "khong_tich") or \
          (d["trang_thai"] == "Không được chi trả" and d["bac_si_chon"] == "tich")
    ly = d.get("ly_do_bac_si")
    if ly is None:
        return {"loai": None, "ghi_chu": None} if can else None
    if not isinstance(ly, dict) or ly.get("loai") not in (*LY_DO, None) \
            or not isinstance(ly.get("ghi_chu"), (str, type(None))):
        return False
    return {"loai": ly.get("loai"), "ghi_chu": ly.get("ghi_chu")}


@app.post("/confirm")
def confirm(request: Request, body: dict = Body(...)):
    if not isinstance(body.get("luot_kham"), str) or not body["luot_kham"]:
        _fail("Thiếu 'luot_kham' (chuỗi).")
    if not isinstance(body.get("kiem_tra_id"), (str, type(None))):
        _fail("'kiem_tra_id' phải là chuỗi.")
    dv = body.get("dau_vao")
    if not isinstance(dv, dict) or not all(k in dv for k in DAU_VAO):
        _fail(f"'dau_vao' cần các khóa: {', '.join(DAU_VAO)}.")
    dong = body.get("dong")
    if not isinstance(dong, list) or not dong:
        _fail("Thiếu 'dong': cần danh sách ít nhất một dòng.")
    now = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")
    rows = []
    for i, d in enumerate(dong, 1):
        if not isinstance(d, dict) or not all(k in d for k in F13):
            _fail(f"Dòng {i} thiếu trường log: cần {', '.join(F13)}.")
        if d["bac_si_chon"] not in ("tich", "khong_tich") or d["o_bhyt_goi_y"] not in ("tich", "trong", None) \
                or not isinstance(d["thu_tu"], int):
            _fail(f"Dòng {i}: 'thu_tu' số nguyên, 'bac_si_chon' tich | khong_tich, 'o_bhyt_goi_y' tich | trong | null.")
        ly = _ly_do(d)
        if ly is False:
            _fail(f"Dòng {i}: 'ly_do_bac_si.loai' phải là {' | '.join(LY_DO)}.")
        # trường của server đặt sau cùng: dòng gửi lên không ghi đè được thời gian, khóa lượt khám, đầu vào
        rows.append({**d, "ly_do_bac_si": ly, "thoi_gian": now, "luot_kham": body["luot_kham"],
                     "kiem_tra_id": body.get("kiem_tra_id"), "dau_vao": dv})
    state["kho"].ghi_xac_nhan(request.state.tai_khoan, rows)
    return {"ghi": len(rows)}


def _muc_do_hien_tai(tai_khoan):
    """Ca đầu tiên chưa lưu trong lịch của tài khoản; làm lần lượt, không nhảy cóc."""
    da_luu = {k["ca_id"] for k in state["kho"].doc_ket_qua_do(tai_khoan)}
    return next((m for m in do_luong.lich(tai_khoan) if m["ca"]["id"] not in da_luu), None)


def _trang_thai_do(tai_khoan):
    lich = do_luong.lich(tai_khoan)
    if not lich:
        return {"co_phan_cong": False, "tong": 0, "da_xong": 0, "hien_tai": None}
    muc = _muc_do_hien_tai(tai_khoan)
    hien_tai = None
    if muc:  # chỉ gửi ca đang làm, đúng các trường cần để khám; tên ca, mã ca gốc, đáp án và ghi chú không đi xuống trình duyệt
        goc = muc["ca"]
        ca = _chuan_hoa_ca({**{k: goc[k] for k in TRUONG_CA_DO if k in goc}, "ten": f"Ca đo {muc['thu_tu']}",
                            "chi_dinh": [{"ma": d.get("ma"), "ten": d["ten"]} for d in goc["chi_dinh"]]})
        hien_tai = {**ca, "che_do": muc["che_do"], "thu_tu": muc["thu_tu"]}
    return {"co_phan_cong": True, "tong": len(lich), "da_xong": muc["thu_tu"] - 1 if muc else len(lich), "hien_tai": hien_tai}


@app.get("/do-luong")
def trang_thai_do(request: Request):
    return _trang_thai_do(request.state.tai_khoan)


@app.post("/do-luong/{ca_id}")
def luu_ket_qua_do(request: Request, ca_id: str, body: dict = Body(...)):
    tai_khoan = request.state.tai_khoan
    muc = _muc_do_hien_tai(tai_khoan)
    if not muc or muc["ca"]["id"] != ca_id:
        raise HTTPException(409, "Ca này đã lưu hoặc chưa đến lượt.")
    dong, goc = body.get("dong"), muc["ca"]["chi_dinh"]
    if not isinstance(dong, list) or len(dong) != len(goc) or not all(
            isinstance(d, dict) and d.get("ten") == g["ten"] and d.get("bac_si_chon") in ("tich", "khong_tich")
            for d, g in zip(dong, goc)):
        _fail("Kết quả không khớp danh sách chỉ định của ca đo.")
    kiem_tra_id = body.get("kiem_tra_id")
    if muc["che_do"] == "cong_cu" and not (isinstance(kiem_tra_id, str) and kiem_tra_id):
        _fail("Cần bấm Kiểm tra BHYT trước khi lưu ca này.")
    ket = {"ca_id": ca_id, "bo": muc["bo"], "che_do": muc["che_do"], "thu_tu": muc["thu_tu"],
           "kiem_tra_id": kiem_tra_id if muc["che_do"] == "cong_cu" else None,
           "dong": [{k: d.get(k) for k in ("ma", "ten", "bac_si_chon", "trang_thai", "o_bhyt_goi_y")} for d in dong]}
    if not state["kho"].luu_ket_qua_do(tai_khoan, ket):
        raise HTTPException(409, "Ca này đã lưu hoặc chưa đến lượt.")
    return _trang_thai_do(tai_khoan)


@app.get("/cases")
def cases(request: Request):
    return [{k: v for k, v in c.items() if k not in ("ky_vong", "he_chi_rule", "a1_gia_lap")}
            for c in _demo_cases(request.state.tai_khoan)]


@app.put("/cases/{ca_id}")
def luu_ca(request: Request, ca_id: str, body: dict = Body(...)):
    """Tạo mới hoặc cập nhật một ca tự tạo. Ca mẫu trong demo.yaml không sửa được."""
    if not TU_TAO_ID.match(ca_id):
        _fail("Chỉ lưu được ca tự tạo (mã dạng TU-…).")
    ten = body.get("ten")
    if not isinstance(ten, str) or not ten.strip() or len(ten) > 200:
        _fail("Ca cần có tên (1–200 ký tự).")
    lich_su, phieu_o = [] if body.get("lich_su") is None else body["lich_su"], body.get("phieu_o")
    if not isinstance(lich_su, list) or not all(isinstance(r, dict) and isinstance(r.get("ten"), (str, type(None)))
                                                and isinstance(r.get("don_vi"), (str, type(None))) for r in lich_su):
        _fail("'lich_su' sai kiểu dữ liệu.")
    if phieu_o is not None and not (isinstance(phieu_o, dict) and set(phieu_o) <= set(PHIEU_O)
                                    and all(isinstance(v, str) for v in phieu_o.values())
                                    and sum(map(len, phieu_o.values())) <= MAX_PHIEU):
        _fail("'phieu_o' sai kiểu dữ liệu.")
    ca = {"id": ca_id, "ten": ten.strip(), "ngay_kham": body.get("ngay_kham") or NGAY_KHAM,
          "benh_nhan": body.get("benh_nhan") or {},
          "sinh_hieu": body.get("sinh_hieu") or {}, "icd": body.get("icd") or [],
          "chi_dinh": [{"ma": r.get("ma"), "ten": r.get("ten")} for r in body.get("chi_dinh") or [] if isinstance(r, dict)],
          "lich_su": [{k: r[k] for k in LICH_SU_KHOA if k in r} for r in lich_su],
          "phieu_kham": body.get("phieu_kham") or "", "phieu_o": phieu_o}
    _validate_luot({**ca, "luot_kham": "LK-" + ca_id}, cho_rong=True)
    state["kho"].luu_ca(request.state.tai_khoan, ca)
    return {"luu": ca_id}


@app.delete("/cases/{ca_id}")
def xoa_ca(request: Request, ca_id: str):
    if not state["kho"].xoa_ca(request.state.tai_khoan, ca_id):
        raise HTTPException(404, "Không có ca tự tạo này.")
    return {"xoa": ca_id}


@app.get("/danh-muc")
def danh_muc():
    """Gợi ý cho ô thêm chỉ định khi bác sĩ tự nhập; tra cứu BHYT thật vẫn do engine làm ở /check."""
    return [{"ma": e.get("ma"), "ten": e["ten"], "bi_danh": e.get("bi_danh") or []}
            for e in getattr(state["rules"], "danh_muc", None) or []]


@app.get("/icd")
@functools.lru_cache(maxsize=1)
def icd():
    """Danh mục ICD-10 tiếng Việt (TT 06/2026), trích sẵn bằng data/danh-muc/trich_icd10.py; thiếu file → rỗng."""
    p = ROOT / "data/danh-muc/icd10.tsv"
    if not p.exists():
        return []
    return [dict(zip(("ma", "ten"), x.split("\t", 1))) for x in p.read_text(encoding="utf-8").splitlines()[1:] if "\t" in x]


@app.get("/gia-dinh")
def gia_dinh():
    """Điểm mơ hồ M-xx cho bảng "Giả định" trên màn hình, đọc thẳng bảng trong docs/06 (nguồn duy nhất)."""
    p = ROOT / "docs/06-diem-mo-ho-bac-si-duyet.md"
    if not p.exists():
        return []
    rows = [[c.strip().replace("**", "") for c in x.split("|")[1:-1]]
            for x in p.read_text(encoding="utf-8").splitlines() if x.startswith("| M-")]
    return [{"ma": r[0], "cau_hoi": r[1], "cach_hieu": r[3], "tra_loi": r[4]} for r in rows if len(r) >= 5]


@app.get("/health")
def health():
    return {"phien_ban_rule": getattr(state["rules"], "phien_ban_rule", None), "a1_mode": state["a1_mode"],
            "model": state["model"], "reasoning_effort": state["reasoning_effort"]}


@app.get("/")
def index():
    return FileResponse(ROOT / "web" / "index.html")
