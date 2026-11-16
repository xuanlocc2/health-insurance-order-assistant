"""Engine: một lượt khám → trạng thái từng dòng (spec 09 mục 4–6, 8). Hàm thuần: không I/O, không mạng.

Giá trị nghiệp vụ chỉ lấy từ Rules (src/rules.py). R2 (thẻ) viết thẳng ở đây theo spec.
"""
import math
import operator
import time
import unicodedata
from datetime import date, datetime

PHU_HOP = "Phù hợp quy tắc BHYT"
DU_CAN_CU = "Cần xem lại · đủ căn cứ"
XEM_LAI = "Cần xem lại"
KHONG_TRA = "Không được chi trả"
NANG = {PHU_HOP: 0, DU_CAN_CU: 1, XEM_LAI: 2, KHONG_TRA: 3}

NGAY_MOI_THANG = 30.44  # spec mục 4
OPS = {"<=": operator.le, "<": operator.lt, ">=": operator.ge, ">": operator.gt, "==": operator.eq}
KY_HIEU = {"<=": "≤", ">=": "≥"}
NHAN = {"nhiet_do": "nhiệt độ", "mach": "mạch", "nhip_tho": "nhịp thở"}  # nhãn hiển thị
LOI_QUY_TAC = (XEM_LAI, "loi_quy_tac", "Quy tắc của dịch vụ này chưa đọc được")
# nhắc mức lượt khám, không đổi trạng thái dòng: lần tích 1 chỉ định trước khi có chẩn đoán là bình thường (DEMO-01)
_QD4750 = "QĐ 4750/QĐ-BYT (sửa đổi QĐ 130/QĐ-BYT), phụ lục bảng chỉ tiêu XML"
THIEU_CHAN_DOAN = {
    "ma": "thieu_chan_doan",
    "noi_dung": "Chưa có chẩn đoán chính (mã ICD-10). Khi đề nghị thanh toán, mỗi chỉ định được hiểu là để điều trị bệnh chính.",
    "can_cu": [
        {"van_ban": _QD4750, "phu_luc": "Bảng 1, trường 26 MA_BENH_CHINH", "trang": 12,
         "trich": "Ghi mã bệnh chính theo mã ICD-10 do Bộ trưởng Bộ Y tế ban hành"},
        {"van_ban": _QD4750, "phu_luc": "Bảng 3, trường 35 MA_BENH", "trang": 41,
         "trich": "Trường hợp không có thông tin ở trường này thì được hiểu là DVKT được chỉ định để điều trị "
                  "bệnh chính (MA_BENH_CHINH)."}]}


def chuan_hoa(s):
    return " ".join(unicodedata.normalize("NFC", s or "").split()).lower()


def dinh_danh(d):
    return d.get("ma") or chuan_hoa(d.get("ten"))


def _so(x):
    return f"{x:g}".replace(".", ",")


def _ngay(x):
    """date | datetime | chuỗi ISO (có hoặc không có giờ) → date; không đọc được → None."""
    if isinstance(x, datetime):
        return x.date()
    if isinstance(x, date):
        return x
    try:
        return datetime.fromisoformat(str(x)).date()
    except ValueError:
        return None


def _la_so(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)


def _kq(ket_qua, nguon=None, bang_chung="", trich_dan=None, trich_lien_quan=()):
    return {"ket_qua": ket_qua, "nguon": nguon, "bang_chung": bang_chung,
            "trich_dan": trich_dan, "trich_lien_quan": list(trich_lien_quan)}


# ---------- gộp trạng thái (mục 6) ----------

def gop_hoac(cons):
    dat = [c for c in cons if c["ket_qua"] == "dat"]
    if dat:
        return next((c for c in dat if c["nguon"] == "nhap"), dat[0])
    bc = "; ".join(dict.fromkeys(c["bang_chung"] for c in cons if c["bang_chung"]))
    dua = [x for c in cons for x in c.get("dua", [])]  # không đạt / chưa rõ: phụ thuộc mọi vế con
    if cons and all(c["ket_qua"] == "khong_dat" for c in cons):
        return {**_kq("khong_dat", "nhap", bc), "dua": dua}
    return {**_kq("chua_du_du_lieu", "a1" if any(c["nguon"] == "a1" for c in cons) else None, bc), "dua": dua}


def gop_nhanh(ves):
    """VÀ: truot | dat_rule | dat_ai | chua_ro."""
    if any(v["ket_qua"] == "khong_dat" for v in ves):
        return "truot"
    if ves and all(v["ket_qua"] == "dat" for v in ves):
        return "dat_rule" if all(v["nguon"] == "nhap" for v in ves) else "dat_ai"
    return "chua_ro"


def gop_dieu_kien(states):
    """HOẶC trên các nhánh áp dụng (nhánh chưa rõ tuổi tính là chua_ro)."""
    if not states:
        return XEM_LAI
    if "dat_rule" in states:
        return PHU_HOP
    if "dat_ai" in states:
        return DU_CAN_CU
    if all(s == "truot" for s in states):
        return KHONG_TRA
    return XEM_LAI


def gop_loai_tru(ves):
    """Chỉ áp dụng khi mọi vế dat. None = không áp dụng."""
    if ves and all(v["ket_qua"] == "dat" for v in ves):
        return KHONG_TRA if all(v["nguon"] == "nhap" for v in ves) else XEM_LAI
    return None


# ---------- tuổi, áp dụng nhánh ----------

def tuoi(bn):
    if bn.get("tuoi_ngay") is not None:
        return bn["tuoi_ngay"], math.floor(bn["tuoi_ngay"] / NGAY_MOI_THANG)
    return None, bn.get("tuoi_thang")


def ap_dung(ad, tuoi_ngay, tuoi_thang):
    """True / False / None (chưa đủ dữ liệu). Khoảng nửa mở [tu, den); den null = không chặn trên."""
    kq = True
    for k, v in (ad or {}).items():
        if k in ("nguon", "diem_mo_ho", "_tham_so"):
            continue
        r = None
        if k in ("tuoi_thang", "tuoi_ngay"):
            tu, den = v[0], math.inf if v[1] is None else v[1]
            if k == "tuoi_thang":
                r = None if tuoi_thang is None else tu <= tuoi_thang < den
            elif tuoi_ngay is not None:
                r = tu <= tuoi_ngay < den
            elif tuoi_thang is not None:  # chỉ có tháng: tuổi ngày nằm trong [m, m+1) tháng
                lo, hi = tuoi_thang * NGAY_MOI_THANG, (tuoi_thang + 1) * NGAY_MOI_THANG
                r = False if hi <= tu or lo >= den else (True if tu <= lo and hi <= den else None)
        if r is False:
            return False
        if r is None:
            kq = None
    return kq


# ---------- kiểm tra một vế ----------

def _la_ai(ve):
    return (ve.get("kiem") or {}).get("loai") == "ai_doc"


def _so_lieu(truong, kiem, ctx):
    """(giá trị, nguồn, trích dẫn). Ô trống → nhờ A1 (pha 1 ghi nhu cầu, pha 2 đọc kết quả)."""
    v = ctx["sinh_hieu"].get(truong)
    if v is not None:
        return v, "nhap", None
    if ctx["so"] is None:
        ctx["can"].append(("so", truong, kiem.get("don_vi")))
        return None, None, None
    s = ctx["so"].get(truong)
    return (s["gia_tri"], "a1", s.get("trich_dan")) if s else (None, None, None)


def _so_sanh(truong, v, nguon, trich, op, nguong):
    nhan = NHAN.get(truong, truong)
    goc = f"A1 trích '{trich}' → " if nguon == "a1" else ""
    if OPS[op](v, nguong):
        return _kq("dat", nguon, f"{goc}{nhan} {_so(v)} {KY_HIEU.get(op, op)} {_so(nguong)}", trich)
    return _kq("khong_dat", nguon, f"{goc}{nhan} {_so(v)}", trich)


def _doc_ai(kiem, ve, ctx):
    if ctx["mode"] == "chi_rule":
        return _kq("chua_du_du_lieu", None, "Hệ chỉ-rule không đọc phiếu khám")
    khoa = f"{ctx['thu_tu']}:{ve.get('id')}"
    if ctx["ai"] is None:  # pha 1
        ctx["can"].append(("ve", khoa, ve.get("mo_ta"), kiem.get("cau_hoi")))
        return _kq("chua_thay", None, "Chờ A1")
    if khoa not in ctx["hoi"]:
        return _kq("chua_du_du_lieu", None, "Không hỏi A1 (nhánh đã trượt hoặc dòng đã có kết luận)")
    tl = ctx["ai"].get(khoa) or {}
    lq = tl.get("trich_lien_quan") or []
    if tl.get("ket_qua") != "dat":
        return _kq("chua_thay", None, "Phiếu khám chưa thấy nội dung tương ứng", None, lq)
    if kiem.get("toi_da") == "chua_thay":
        return _kq("chua_thay", None, "A1 chỉ trích dấu hiệu, không tự kết luận vế này", tl.get("trich_dan"), lq)
    return _kq("dat", "a1", "A1 đọc phiếu khám", tl.get("trich_dan"), lq)


def kiem_tra(k, ve, ctx):
    loai = k.get("loai")
    if loai == "so_sanh":
        v, nguon, trich = _so_lieu(k["truong"], k, ctx)
        if v is None:
            return _kq("chua_du_du_lieu", None, f"{NHAN.get(k['truong'], k['truong'])}: trống")
        return _so_sanh(k["truong"], v, nguon, trich, k["toan_tu"], k["gia_tri"])
    if loai == "nguong_theo_tuoi":
        nhan, thang = NHAN.get(k["truong"], k["truong"]), ctx["tuoi_thang"]
        dong = None if thang is None else next(
            (d for d in k.get("bang") or [] if d["tu"] <= thang < (math.inf if d["den"] is None else d["den"])), None)
        if dong is None:
            return _kq("chua_du_du_lieu", None, f"{nhan}: chưa có ngưỡng cho tuổi này")
        v, nguon, trich = _so_lieu(k["truong"], k, ctx)
        if v is None:
            return _kq("chua_du_du_lieu", None, f"{nhan}: trống")
        return _so_sanh(k["truong"], v, nguon, trich, ">=", dong["nguong"])
    if loai == "icd_trong":
        icd = [c.strip().upper() for c in ctx["icd"] if c]
        khop = [c for c in icd if any(c.startswith(p.upper()) for p in k["ds"])]
        if khop:
            return _kq("dat", "nhap", f"ICD {', '.join(khop)}")
        if k.get("neu_khong_khop") == "ai_doc":  # cả khi chưa có ICD (xem báo cáo: CRP-13)
            return _doc_ai(k, ve, ctx)
        if not icd:
            return _kq("chua_du_du_lieu", None, "Chưa có ICD")
        return _kq("khong_dat", "nhap", f"ICD {', '.join(icd)}")
    if loai == "ai_doc":
        return _doc_ai(k, ve, ctx)
    if loai == "lich_su_so_sanh":
        recs = sorted((r for r in ctx["lich_su"] if r.get("ma") == k["ma"]),
                      key=lambda r: math.inf if r.get("ngay_cach") is None else r["ngay_cach"])
        if not recs or recs[0].get("ket_qua") is None:
            return _kq("chua_du_du_lieu", None, "Chưa có kết quả lần trước")
        r = recs[0]
        ref = r["tham_chieu_tren"] if r.get("tham_chieu_tren") is not None else k.get("tham_chieu")
        if ref is None:
            return _kq("chua_du_du_lieu", None, "Chưa có giá trị tham chiếu")
        nguong = k.get("he_so", 1) * ref
        ok = OPS[k["toan_tu"]](r["ket_qua"], nguong)
        kq = _kq("dat" if ok else "khong_dat", "nhap",
                 f"lần trước {_so(r['ket_qua'])} {'' if ok else 'không '}{KY_HIEU.get(k['toan_tu'], k['toan_tu'])} {_so(nguong)}")
        if r.get("tham_chieu_tren") is not None:  # tham chiếu của bản ghi → không phụ thuộc tham số tham_chieu
            kq["dua"] = [{**k, "_tham_so": {a: b for a, b in (k.get("_tham_so") or {}).items() if a != "tham_chieu"}}]
        return kq
    if loai == "khong_cung_luot":
        ds = {chuan_hoa(x) for x in k["ma_hoac_bi_danh"]} | set(k["ma_hoac_bi_danh"])
        trung = [cd.get("ten") or cd.get("ma") for i, cd in enumerate(ctx["chi_dinh"], 1)
                 if i != ctx["thu_tu"] and (cd.get("ma") in ds or chuan_hoa(cd.get("ten")) in ds)]
        if trung:
            return _kq("khong_dat", "nhap", f"có '{trung[0]}' trong cùng lượt")
        return _kq("dat", "nhap", "không có trong cùng lượt")
    return _kq("chua_du_du_lieu", None, "Vế chưa mã hóa được")


def danh_gia_ve(ve, ctx):
    """Kết quả một vế; "dua" = các phần quy tắc mà kết quả thật sự dựa vào (cho hậu tố "cách hiểu tạm")."""
    if "hoac" in ve:
        kq = gop_hoac([_ha({"dua": [k], **kiem_tra(k, ve, ctx)}) for k in ve["hoac"]])
    elif ve.get("kiem"):
        kq = _ha({"dua": [ve["kiem"]], **kiem_tra(ve["kiem"], ve, ctx)})
    else:
        kq = _kq("chua_du_du_lieu", None, "Vế chưa mã hóa được")
    return {**kq, "dua": [_nong(ve), *kq.get("dua", [])]}


def _ha(kq):
    """Kết quả khong_dat có nguồn a1 bị hạ thành chua_du_du_lieu (mục 6)."""
    if kq["ket_qua"] == "khong_dat" and kq["nguon"] == "a1":
        return {**kq, "ket_qua": "chua_du_du_lieu", "bang_chung": kq["bang_chung"] + " (số do A1 trích, không dùng để kết luận không đạt)"}
    return kq


# ---------- nguồn quy tắc, hậu tố "cách hiểu tạm" ----------

def _meta(obj, tham_so):
    """(tập nguon, mã M-xx của phần tạm). Phần tạm = nguon tu_dung hoặc có diem_mo_ho, trừ bac_si_duyet."""
    nguon, ma = set(), []

    def walk(o):
        if isinstance(o, dict):
            if o.get("nguon"):
                nguon.add(o["nguon"])
            if o.get("nguon") != "bac_si_duyet" and (o.get("nguon") == "tu_dung" or o.get("diem_mo_ho")):
                nguon.add("_tam")
                dm = o.get("diem_mo_ho") or []
                for c in [dm] if isinstance(dm, str) else dm:
                    if c not in ma:
                        ma.append(c)
            for tens in (o.get("_tham_so") or {}).values():
                for ten in tens:
                    walk(tham_so.get(ten))
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)

    walk(obj)
    return nguon, ma


def _nong(o):
    """Nhãn nguồn của riêng dict này, không đi vào các phần con."""
    return {k: o[k] for k in ("nguon", "diem_mo_ho") if k in (o or {})}


def _dua(ves):
    return [x for _, k in ves for x in k["dua"]]


def _hau_to(objs, tham_so):
    nguon, ma = set(), []
    for o in objs:
        n, m = _meta(o, tham_so)
        nguon |= n
        ma += [c for c in m if c not in ma]
    if "_tam" not in nguon:
        return ""
    return f" (cách hiểu tạm {', '.join(ma)}, chưa được bác sĩ duyệt)" if ma else " (cách hiểu tạm, chưa được bác sĩ duyệt)"


# ---------- R3 ----------

def danh_gia_dk(dk, ctx):
    """→ (nhánh [{nhanh, ad, state, ves:[(ve, kq)]}], loại trừ [(ve, kq)], trạng thái loại trừ, câu hỏi)."""
    ds, can = [], []
    for nh in dk.get("nhanh") or []:
        ad = ap_dung(nh.get("ap_dung"), ctx["tuoi_ngay"], ctx["tuoi_thang"])
        if ad is False:
            continue
        ves = nh.get("ve") or []
        if ctx["mode"] == "chi_rule" and any(not _la_ai(v) for v in ves):
            ves = [v for v in ves if not _la_ai(v)]  # mục 6: nhánh có vế rule thì bỏ qua vế ai_doc
        ctx["can"] = []
        kq = [(v, danh_gia_ve(v, ctx)) for v in ves]
        state = gop_nhanh([k for _, k in kq]) if ad else "chua_ro"
        if ad and state != "truot":
            can += ctx["can"]
        ds.append({"nhanh": nh, "ad": ad, "state": state, "ves": kq})
    lt = dk.get("loai_tru") or {}
    ctx["can"] = []
    lt_kq = [(v, danh_gia_ve(v, ctx)) for v in lt.get("ve") or []]
    if any(n["ad"] and n["state"] != "truot" for n in ds):
        can += ctx["can"]
    return ds, lt_kq, gop_loai_tru([k for _, k in lt_kq]), can


def _ly_do_r3(dk, ds, lt_kq, lt_state, tt_dk):
    """(trạng thái, mã lý do, câu, các phần quy tắc mà kết luận dựa vào)."""
    tt = max(tt_dk, lt_state or PHU_HOP, key=NANG.get)
    moi_ap_dung = [n.get("ap_dung") for n in dk.get("nhanh") or []]
    if lt_state and NANG[lt_state] >= NANG[tt_dk]:
        return tt, "loai_tru", f"Có thể thuộc điều khoản không thanh toán: {dk['loai_tru'].get('mo_ta', '')}", \
            [_nong(dk["loai_tru"]), *_dua(lt_kq)]
    if not ds:
        return tt, "khong_nhanh", "Không có nhánh điều kiện áp dụng cho tuổi này", moi_ap_dung
    if tt_dk in (PHU_HOP, DU_CAN_CU):
        n = next(n for n in ds if n["state"] == ("dat_rule" if tt_dk == PHU_HOP else "dat_ai"))
        if tt_dk == PHU_HOP:
            cau = "Đạt điều kiện: " + "; ".join(v.get("mo_ta", "") for v, _ in n["ves"])
        else:
            cau = "Đạt điều kiện, có vế do AI đọc phiếu khám: " + "; ".join(
                v.get("mo_ta", "") for v, k in n["ves"] if k["nguon"] == "a1")
        return tt, "dat" if tt_dk == PHU_HOP else "dat_ai", cau, \
            [_nong(n["nhanh"]), n["nhanh"].get("ap_dung"), *_dua(n["ves"])]
    if tt_dk == KHONG_TRA:
        hong = [(v, k) for n in ds for v, k in n["ves"] if k["ket_qua"] == "khong_dat"]
        # mỗi nhánh nêu vế trượt đầu tiên; các nhánh ICD gộp thành một vế câu (bác sĩ thấy đủ vì sao, kể cả nhánh tự dựng)
        dau = [next((v, k) for v, k in n["ves"] if k["ket_qua"] == "khong_dat") for n in ds]
        icd = [(v, k) for v, k in dau if (v.get("kiem") or {}).get("loai") == "icd_trong"]
        phan = [f"{v.get('mo_ta', '')}: {k['bang_chung']} chưa đạt" for v, k in dau if (v, k) not in icd]
        if icd:
            phan.append(f"{icd[0][1]['bang_chung']} không thuộc nhóm " + ", ".join(f"'{v.get('mo_ta', '')}'" for v, _ in icd))
        return tt, "ve_khong_dat", "; ".join(phan), _dua(hong) + moi_ap_dung
    # Cần xem lại: vế đầu tiên chưa đạt của nhánh còn sống đầu tiên
    for n in ds:
        if n["state"] == "truot":
            continue
        if not n["ad"]:
            return tt, "ve_chua_du", "Chưa đủ dữ liệu cho vế 'độ tuổi áp dụng nhánh'", [n["nhanh"].get("ap_dung")]
        for v, k in n["ves"]:
            if k["ket_qua"] == "chua_thay":
                return tt, "ve_chua_thay", f"Điều kiện có vế '{v.get('mo_ta', '')}'; phiếu khám chưa thấy nội dung tương ứng", k["dua"]
            if k["ket_qua"] != "dat":
                return tt, "ve_chua_du", f"Chưa đủ dữ liệu cho vế '{v.get('mo_ta', '')}'", k["dua"]
    return tt, "ve_chua_du", "Chưa đủ dữ liệu", []


def _checklist(ds, lt_kq, ts):
    out = []
    for nhanh, ves in [(n["nhanh"].get("id"), n["ves"]) for n in ds] + [("loai_tru", lt_kq)]:
        for v, k in ves:
            nguon, ma = _meta(v, ts)
            out.append({"nhanh": nhanh, "id": v.get("id"), "mo_ta": v.get("mo_ta"), "ket_qua": k["ket_qua"],
                        "nguon_ket_qua": k["nguon"], "bang_chung": k["bang_chung"], "trich_dan": k["trich_dan"],
                        "trich_lien_quan": k["trich_lien_quan"],
                        "nguon_quy_tac": "tu_dung" if "tu_dung" in nguon else
                        "bac_si_duyet" if "bac_si_duyet" in nguon else "van_ban",
                        "diem_mo_ho": ma})
    return out


# ---------- R1, R2 ----------

def tra_danh_muc(cd, danh_muc):
    if cd.get("ma"):
        e = next((e for e in danh_muc if e.get("ma") == cd["ma"]), None)
        if e:
            return e
    ten = chuan_hoa(cd.get("ten"))
    return next((e for e in danh_muc if ten and ten in
                 {chuan_hoa(x) for x in [e.get("ten"), *(e.get("bi_danh") or [])]}), None) if ten else None


def _r2(luot):
    the = (luot.get("benh_nhan") or {}).get("the")
    if not the:
        return XEM_LAI, "the_thieu", "Chưa có thông tin thẻ BHYT"
    if the.get("han_den") is None:
        return XEM_LAI, "the_thieu", "Chưa có thông tin thẻ BHYT"
    han, ngay = _ngay(the["han_den"]), _ngay(luot.get("ngay_kham"))
    if han is None:
        return XEM_LAI, "the_thieu", "Chưa có thông tin thẻ BHYT"
    if ngay is None:
        return XEM_LAI, "thieu_ngay_kham", "Chưa có ngày khám"
    if han < ngay:
        return KHONG_TRA, "the_het_han", f"Thẻ BHYT hết hạn {han:%d/%m/%Y}"
    return None


def _r1(e, dk, ts):
    if e is None:
        return XEM_LAI, "chua_tra", "Ngoài danh sách đã tra"
    bhyt = e.get("bhyt")
    if bhyt == "khong_thay":
        return KHONG_TRA, "khong_thay", "Không tìm thấy trong danh mục kỹ thuật đã tra" + _hau_to([e], ts)
    if bhyt == "dieu_kien" and dk is None:
        return XEM_LAI, "chua_co_dieu_kien", "Có điều kiện thanh toán nhưng chưa có quy tắc"
    if bhyt not in ("co", "dieu_kien"):
        return XEM_LAI, "xac_minh", "Có trong danh mục kỹ thuật nhưng chưa tìm thấy giá BHYT tương ứng, cần kiểm tra với bảng giá của viện" + _hau_to([e], ts)
    return None


def _can_cu(dk, e):
    """Căn cứ của điều kiện (trích = nguyên văn điều kiện) nếu có, không thì của dòng danh mục. Luôn có khóa "trich"."""
    if dk and dk.get("can_cu"):
        return [{"trich": dk.get("nguyen_van"), **c} for c in dk["can_cu"]]
    return [{"trich": None, **c} for c in (e or {}).get("can_cu") or []]


# ---------- lượt khám ----------

def check(luot, rules, a1, mode="full"):
    ts, cds = rules.tham_so, luot.get("chi_dinh") or []
    tuoi_ngay, tuoi_thang = tuoi(luot.get("benh_nhan") or {})
    base = {"mode": mode, "tuoi_ngay": tuoi_ngay, "tuoi_thang": tuoi_thang, "icd": luot.get("icd") or [],
            "sinh_hieu": luot.get("sinh_hieu") or {}, "lich_su": luot.get("lich_su") or [], "chi_dinh": cds}
    r2 = _r2(luot)
    the = (luot.get("benh_nhan") or {}).get("the") or {}
    da_thay, dong = set(), []

    # pha 1: bước 1–5c cho mọi dòng, gom câu hỏi
    for tt, cd in enumerate(cds, 1):
        e = tra_danh_muc(cd, rules.danh_muc)
        dk = rules.dieu_kien.get(e.get("ma")) if e and e.get("ma") else None
        buoc = [b for b in (r2, _r1(e, dk, ts)) if b]
        dd = {dinh_danh(cd)} | ({id(e)} if e else set())  # cùng mã/tên, hoặc cùng một dòng danh mục (mã ↔ bí danh)
        if dd & da_thay:
            buoc.append((XEM_LAI, "trung_dong", "Trùng dịch vụ trong cùng lượt khám"))
        da_thay |= dd
        can = []
        try:
            if dk and dk.get("tan_suat"):
                f = dk["tan_suat"]
                cach = [r["ngay_cach"] for r in base["lich_su"] if r.get("ma") == e["ma"] and r.get("ngay_cach") is not None]
                if cach:
                    gio = min(cach) * 24
                    cau = f"Đã làm cách {_so(gio)} giờ; giới hạn {_so(f['nen_gio'])} giờ" + _hau_to([f], ts)
                    if gio < f["toi_thieu_gio"]:
                        buoc.append((KHONG_TRA, "tan_suat", cau))
                    elif gio < f["nen_gio"]:
                        buoc.append((XEM_LAI, "tan_suat", cau))
            if dk:
                ctx = {**base, "thu_tu": tt, "ai": None, "so": None, "hoi": set(), "can": []}
                _, _, lt_state, can = danh_gia_dk(dk, ctx)
                if lt_state == KHONG_TRA or any(b[0] == KHONG_TRA for b in buoc):
                    can = []  # đã Không được chi trả từ dữ liệu nhập: AI không đổi được kết luận
        except Exception:  # quy tắc không đọc được → Cần xem lại (nguyên tắc 2), không chặn các dòng khác
            buoc.append(LOI_QUY_TAC)
            dk, can = None, []
        dong.append({"tt": tt, "cd": cd, "e": e, "dk": dk, "buoc": buoc, "can": can})

    # một lần A1 cho cả lượt
    cau_hoi = {}  # mỗi khóa hỏi một lần (giữ câu đầu)
    for c in (c for d in dong for c in d["can"] if c[0] == "ve"):
        cau_hoi.setdefault(c[1], {"khoa": c[1], "mo_ta": c[2], "cau_hoi": c[3]})
    cau_hoi = list(cau_hoi.values())
    so_lieu = list({c[1]: {"truong": c[1], "don_vi": c[2]} for d in dong for c in d["can"] if c[0] == "so"}.values())
    info, ai, so = {"goi": False, "loi": None, "ms": 0}, {}, {}
    if mode == "full" and (cau_hoi or so_lieu):
        if a1 is None:
            info["loi"] = "a1_tat"
        else:
            t0 = time.perf_counter()
            muon = {s["truong"] for s in so_lieu}
            try:
                res = a1({"phieu_kham": luot.get("phieu_kham") or "", "cau_hoi": cau_hoi, "so_lieu": so_lieu}) or {}
                loi = res.get("loi")
                ai = {v["khoa"]: v for v in res.get("ve") or []}
                so = {s["truong"]: s for s in res.get("so_lieu") or [] if s["truong"] in muon and _la_so(s.get("gia_tri"))}
            except Exception as ex:  # hợp đồng: A1Fn không raise, trả đúng dạng; phòng hờ để không chặn bác sĩ
                ai, so, loi = {}, {}, f"a1_loi_{type(ex).__name__}"
            info = {"goi": True, "loi": loi, "ms": int((time.perf_counter() - t0) * 1000)}
    hoi = {q["khoa"] for q in cau_hoi}

    # pha 2: điền kết quả A1, gộp
    out = []
    for d in dong:
        buoc, checklist = list(d["buoc"]), []
        e = d["e"] or {}
        if d["dk"]:
            try:
                ctx = {**base, "thu_tu": d["tt"], "ai": ai, "so": so, "hoi": hoi, "can": []}
                ds, lt_kq, lt_state, _ = danh_gia_dk(d["dk"], ctx)
                tt, ma, cau, dua = _ly_do_r3(d["dk"], ds, lt_kq, lt_state, gop_dieu_kien([n["state"] for n in ds]))
                buoc.append((tt, ma, cau + _hau_to([*dua, _nong(e)], ts)))
                checklist = _checklist(ds, lt_kq, ts)
            except Exception:  # như pha 1
                buoc.append(LOI_QUY_TAC)
        elif not buoc:  # Phù hợp chỉ theo danh mục
            buoc.append((PHU_HOP, "danh_muc", "Có trong danh mục BHYT, không có điều kiện thanh toán riêng"
                         + _hau_to([_nong(e)], ts)))
        tt, ma_ly_do, ly_do = max(buoc, key=lambda b: NANG[b[0]]) if buoc else (PHU_HOP, None, None)
        out.append({"thu_tu": d["tt"], "ma": d["cd"].get("ma") or e.get("ma"), "ten": d["cd"].get("ten") or e.get("ten"),
                    "trang_thai": tt,
                    "o_bhyt_goi_y": "tich" if tt in (PHU_HOP, DU_CAN_CU) else "trong" if tt == KHONG_TRA else None,
                    "to_mau": tt == DU_CAN_CU,
                    "ly_do": ly_do, "ma_ly_do": ma_ly_do, "muc_huong": the.get("muc_huong"),
                    "checklist": checklist, "can_cu": _can_cu(d["dk"], d["e"]),
                    "phien_ban_rule": rules.phien_ban_rule})
    return {"phien_ban_rule": rules.phien_ban_rule, "a1": info, "dong": out,
            "nhac": [] if base["icd"] else [THIEU_CHAN_DOAN]}
