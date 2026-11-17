"""API demo BHYT (spec mục 11b). Chạy: uvicorn src.app:app --host 127.0.0.1 --port 8000"""
import functools
import importlib
import json
import os
import uuid
from concurrent.futures import ThreadPoolExecutor
from contextlib import asynccontextmanager
from datetime import date, datetime, timezone
from pathlib import Path

import yaml
from fastapi import Body, FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse
from starlette.middleware.trustedhost import TrustedHostMiddleware

from src import log

ROOT = Path(__file__).resolve().parent.parent
RULES_DIR = ROOT / "data" / "rules"
LOG_PATH = ROOT / "logs" / "xac-nhan.jsonl"
CASES_PATH = ROOT / "data" / "test-cases" / "demo.yaml"
# mặc định của app mô phỏng (engine không có mặc định; test-cases/README.md)
NGAY_KHAM = "2026-11-12"
MAX_CHI_DINH, MAX_PHIEU = 50, 20000  # chặn body bất thường trước khi gửi A1
LY_DO = ("nguoi_nha_yeu_cau", "loai_tru_theo_doi", "khong_dong_y", "khac")
F13 = ("thu_tu", "ma", "ten", "trang_thai", "o_bhyt_goi_y", "bac_si_chon", "checklist", "can_cu", "phien_ban_rule")
DAU_VAO = ("tuoi", "the", "icd", "sinh_hieu", "lich_su_da_dung")

# test gán trực tiếp các khóa này
state = {"rules": None, "check": None, "a1": None, "a1_mode": "off", "model": None, "reasoning_effort": None,
         "lq": None}


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
    print(f"[bhyt] a1_mode={mode} model={model} reasoning_effort={effort} rules={rules.phien_ban_rule[:10]}")
    yield


app = FastAPI(title="Trợ lý BHYT (demo)", lifespan=lifespan)
# chỉ nhận Host cục bộ: chặn DNS rebinding (trang lạ gọi /check tốn khóa OpenAI, hoặc ghi log giả)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["127.0.0.1", "localhost"])


@app.exception_handler(RequestValidationError)
async def _bad_body(_req: Request, _exc):
    return JSONResponse({"detail": "Dữ liệu gửi lên phải là một đối tượng JSON."}, status_code=422)


def _plain(x):
    return json.loads(json.dumps(x, default=str, ensure_ascii=False))  # date của YAML → chuỗi


def _demo_cases():
    raw = yaml.safe_load(CASES_PATH.read_text(encoding="utf-8")) or []
    out = []
    for c in raw:
        c = _plain(c)
        bn = c.setdefault("benh_nhan", {})
        if "the" not in bn:
            thang = bn["tuoi_thang"] if bn.get("tuoi_thang") is not None else (bn.get("tuoi_ngay") or 0) / 30.44
            bn["the"] = {"han_den": "2026-12-31", "muc_huong": 100 if thang < 72 else 80}
        c.setdefault("luot_kham", "LK-" + c["id"])
        c.setdefault("ngay_kham", NGAY_KHAM)
        c.setdefault("lich_su", [])
        out.append(c)
    return out


def _fail(msg):
    raise HTTPException(422, msg)


def _num(x):
    return x is None or (isinstance(x, (int, float)) and not isinstance(x, bool))


def _ngay(x):
    if x is None:
        return True
    try:
        date.fromisoformat(x)
        return True
    except (TypeError, ValueError):
        return False


def _validate_luot(b):
    """Kiểu dữ liệu ở biên tin cậy, để engine không 500 vì body lạ. Thiếu khóa vẫn được (engine → Cần xem lại)."""
    if not isinstance(b.get("luot_kham"), str) or not b["luot_kham"]:
        _fail("Thiếu 'luot_kham' (chuỗi).")
    cd = b.get("chi_dinh")
    if not isinstance(cd, list) or not cd or len(cd) > MAX_CHI_DINH:
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
                and all(_num(r.get(k)) for k in ("ngay_cach", "ket_qua", "tham_chieu_tren"))):
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


# ponytail: dict trong bộ nhớ, xóa sạch khi đầy; đủ cho demo một máy. Nhiều người dùng → LRU/Redis theo lượt khám.
_NHO = {}


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
        loi = None
        if any(kv(q) not in _NHO for q in cau) or any(ks(s) not in _NHO for s in so):
            if not doc_ai:
                loi = "chua_doc"
            else:
                res = a1(req) or {}
                loi = res.get("loi")
                if str(loi or "").startswith("a1_"):  # gọi hỏng: không nhớ, lần bấm sau gọi lại
                    return res
                if len(_NHO) > 5000:
                    _NHO.clear()
                tl = {v["khoa"]: v for v in res.get("ve") or []}
                for q in cau:
                    if q["khoa"] in tl:
                        _NHO[kv(q)] = tl[q["khoa"]]
                co = {s["truong"]: s for s in res.get("so_lieu") or []}
                for s in so:
                    _NHO[ks(s)] = co.get(s["truong"])
        ve = [{**_NHO[kv(q)], "khoa": q["khoa"]} if kv(q) in _NHO else
              {"khoa": q["khoa"], "ket_qua": "chua_thay", "trich_dan": None, "trich_them": [], "trich_lien_quan": [], "chua_doc": True}
              for q in cau]
        return {"ve": ve, "so_lieu": [_NHO[ks(s)] for s in so if _NHO.get(ks(s))], "loi": loi}
    return f


@app.post("/check")
def check(body: dict = Body(...)):  # def → chạy trong threadpool, A1 chặn tới 8 s không treo server
    _validate_luot(body)
    doc_ai = body.get("doc_ai") is not False  # false = rule tự chạy lại sau khi sửa chỉ định/ICD, không gọi A1
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
def confirm(body: dict = Body(...)):
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
    log.append(rows, LOG_PATH)
    return {"ghi": len(rows)}


@app.get("/cases")
def cases():
    return [{k: v for k, v in c.items() if k not in ("ky_vong", "he_chi_rule", "a1_gia_lap")} for c in _demo_cases()]


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
