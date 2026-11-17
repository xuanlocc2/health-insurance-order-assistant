"""Bất biến của engine (spec 09: nguyên tắc 2–3, mục 5–6), kiểm ngẫu nhiên có seed trên tests/fixtures/rules.

Mỗi lượt khám ngẫu nhiên chạy với: A1 im lặng (mọi vế chua_thay), A1 ngẫu nhiên (đạt / chưa thấy / số bừa / lỗi /
sai dạng / raise), A1 "đồng ý hết" (mọi vế dat, số nào cũng vượt ngưỡng) và a1=None. Lỗi in kèm số thứ tự lượt để chạy lại.
"""
import copy
import random
from collections import Counter
from pathlib import Path

from src.engine import DU_CAN_CU, KHONG_TRA, PHU_HOP, XEM_LAI, check
from src.rules import load_rules

RULES = load_rules(Path(__file__).parent / "fixtures" / "rules")
SO_LUOT = 2000
CRP, PCT = "23.0228.1483", "23.0130.1549"
O_GOI_Y = {PHU_HOP: ("tich", False), DU_CAN_CU: ("tich", True), XEM_LAI: (None, False), KHONG_TRA: ("trong", False)}


# ---------- sinh lượt khám ----------

def _chi_dinh(rnd):
    e = rnd.choice(RULES.danh_muc)
    kieu = rnd.randrange(6)
    if kieu == 0:
        return {"ma": None, "ten": rnd.choice(["Siêu âm tim cản âm", "Định lượng IgE đặc hiệu", "Dịch vụ lạ"])}
    if kieu == 1:
        return {"ma": None, "ten": "  " + e["ten"].upper().replace(" ", "  ")}   # tên, khác hoa thường và khoảng trắng
    if kieu == 2 and e.get("bi_danh"):
        return {"ma": None, "ten": rnd.choice(e["bi_danh"])}
    return {"ma": e.get("ma"), "ten": e["ten"]}


def luot_ngau_nhien(rnd):
    chon, co = rnd.choice, lambda p: rnd.random() < p  # noqa: E731
    bn = chon([{}, {"tuoi_ngay": chon([0, 5, 28, 29, 30, 50, 400])},
               {"tuoi_thang": chon([0, 1, 2, 11, 12, 30, 59, 60, 191, 192, 300])},
               {"tuoi_thang": rnd.randrange(0, 250)}])
    the = chon([None, {}, {"han_den": None, "muc_huong": 80}, {"han_den": "2026-11-11", "muc_huong": 80},
                {"han_den": "2026-11-12", "muc_huong": 100}, {"han_den": "2027-12-31", "muc_huong": 100},
                {"han_den": "2027-12-31", "muc_huong": 100}, {"han_den": "2027-12-31", "muc_huong": 100}])
    if the is not None or co(0.5):
        bn["the"] = the
    sinh_hieu = {}
    for truong, gia_tri in (("nhiet_do", [35.5, 36, 36.1, 37, 38.2, 38.3, 39.5]),
                            ("mach", [80, 150, 190]), ("nhip_tho", [20, 39, 40, 49, 50, 59, 60, 70])):
        if co(0.75):
            sinh_hieu[truong] = chon([None, *gia_tri, *gia_tri])
    lich_su = [{"ma": chon([PCT, PCT, CRP]), "ngay_cach": chon([0, 0.5, 1, 1.5, 2, 3, None]),
                "ket_qua": chon([None, 0.2, 1.0, 1.01, 5]), "tham_chieu_tren": chon([None, 0.5, 0.05])}
               for _ in range(chon([0, 0, 1, 2]))]
    cds = [_chi_dinh(rnd) for _ in range(rnd.randrange(1, 7))]
    if co(0.3):
        cds.append(dict(chon(cds)))                                                # dòng trùng
    luot = {"luot_kham": "LK", "ngay_kham": "2026-11-12", "benh_nhan": bn,
            "icd": rnd.sample(["J18.9", "P36.9", "p36", "I21.0", "M30.3", "L51.1", "J06.9", ""], rnd.randrange(0, 4)),
            "sinh_hieu": sinh_hieu, "phieu_kham": "Ran ẩm đáy phổi phải. NT 45 l/p.", "lich_su": lich_su, "chi_dinh": cds}
    if co(0.05):
        del luot["ngay_kham"]
    return luot


# ---------- A1 giả ----------

class A1:
    """kieu: im_lang | dong_y | phan_doi (vế nào cũng khong_dat, số nào cũng trong giới hạn bình thường) |
    ngau_nhien (theo seed). Đếm số lần gọi."""

    def __init__(self, kieu, seed=0):
        self.kieu, self.seed, self.calls = kieu, seed, []

    def __call__(self, req):
        self.calls.append(req)
        rnd = random.Random(self.seed)
        if self.kieu == "im_lang":
            return {"ve": [{"khoa": q["khoa"], "ket_qua": "chua_thay", "trich_dan": None, "trich_lien_quan": []}
                           for q in req["cau_hoi"]], "so_lieu": [], "loi": None}
        if self.kieu in ("dong_y", "phan_doi"):
            kq, so = ("dat", {"nhiet_do": 39.9}) if self.kieu == "dong_y" else ("khong_dat", {"nhiet_do": 37, "nhip_tho": 20})
            return {"ve": [{"khoa": q["khoa"], "ket_qua": kq, "trich_dan": "Ran ẩm", "trich_lien_quan": []}
                           for q in req["cau_hoi"]], "loi": None,
                    "so_lieu": [{"truong": s["truong"], "gia_tri": so.get(s["truong"], 119), "trich_dan": "x"}
                                for s in req["so_lieu"]]}
        r = rnd.random()
        if r < 0.05:
            raise TimeoutError
        if r < 0.10:
            return {"ve": [], "so_lieu": [], "loi": "a1_json_loi"}
        if r < 0.13:
            return rnd.choice([None, [], {"ve": [{"sai": 1}]}, {"ve": "x"}, {"so_lieu": [{"gia_tri": 1}]}])
        ve = [{"khoa": q["khoa"], "ket_qua": rnd.choice(["dat", "dat", "chua_thay", "khong_dat", None]),
               "trich_dan": rnd.choice(["Ran ẩm", None]), "trich_lien_quan": rnd.choice([[], ["Mẹ đang viêm họng"]])}
              for q in req["cau_hoi"] if rnd.random() < 0.9]
        so = [{"truong": s["truong"], "trich_dan": "x",
               "gia_tri": rnd.choice([rnd.uniform(0, 200), 20, 36, 37, 37, 38.3, 40, 60, None, "39", True, float("nan"), float("inf")])}
              for s in req["so_lieu"] if rnd.random() < 0.9]
        so.append({"truong": "nhiet_do", "gia_tri": 41, "trich_dan": "không ai hỏi"})  # số không được hỏi phải bị bỏ
        ve.append({"khoa": "1:V3", "ket_qua": "dat", "trich_dan": "không ai hỏi"})     # vế không được hỏi cũng vậy
        return {"ve": ve, "so_lieu": so, "loi": None}


def _bo_ms(res):
    return {**res, "a1": {**res["a1"], "ms": 0}}


def _tt(res):
    return [d["trang_thai"] for d in res["dong"]]


# ---------- bất biến trên một kết quả ----------

def kiem_ket_qua(luot, res, a1, nhan):
    assert a1 is None or len(a1.calls) <= 1, f"{nhan}: A1 bị gọi {len(a1.calls)} lần"                     # (e)
    if a1 is not None and a1.calls:
        khoa = [q["khoa"] for q in a1.calls[0]["cau_hoi"]]
        assert len(khoa) == len(set(khoa)), f"{nhan}: khóa lặp {khoa}"
        assert all(1 <= int(k.split(":")[0]) <= len(luot["chi_dinh"]) for k in khoa), f"{nhan}: {khoa}"
        assert a1.calls[0]["cau_hoi"] or a1.calls[0]["so_lieu"], f"{nhan}: gọi A1 khi không có gì để hỏi"
    assert [d["thu_tu"] for d in res["dong"]] == list(range(1, len(luot["chi_dinh"]) + 1)), nhan
    for d in res["dong"]:
        n = f"{nhan} dòng {d['thu_tu']} {d['ten']!r} ({d['trang_thai']}; {d['ly_do']})"
        assert (d["o_bhyt_goi_y"], d["to_mau"]) == O_GOI_Y[d["trang_thai"]], n
        assert d["ma_ly_do"] != "loi_quy_tac" and d["phien_ban_rule"] == RULES.phien_ban_rule, n
        assert all("trich" in c for c in d["can_cu"]), n
        assert d["trang_thai"] == PHU_HOP or d["ly_do"], n                         # không phù hợp thì phải có lý do
        for v in d["checklist"]:
            assert not (v["ket_qua"] == "khong_dat" and v["nguon_ket_qua"] != "nhap"), f"{n}: vế {v['id']} không đạt từ AI"
            assert v["ket_qua"] != "dat" or v["nguon_ket_qua"] in ("nhap", "a1"), f"{n}: vế {v['id']} đạt không rõ nguồn"
        nhanh = {}
        for v in d["checklist"]:
            nhanh.setdefault(v["nhanh"], []).append(v)
        loai_tru = nhanh.pop("loai_tru", [])
        dat = [vs for vs in nhanh.values() if all(v["ket_qua"] == "dat" for v in vs)]
        if d["trang_thai"] == PHU_HOP and d["checklist"]:                                                   # (a)
            assert any(all(v["nguon_ket_qua"] == "nhap" for v in vs) for vs in dat), f"{n}: không nhánh nào đạt hoàn toàn từ nhap"
            assert not (loai_tru and all(v["ket_qua"] == "dat" for v in loai_tru)), f"{n}: loại trừ đủ vế mà vẫn Phù hợp"
        if d["trang_thai"] == DU_CAN_CU:
            assert dat and any(v["nguon_ket_qua"] == "a1" for vs in dat for v in vs), f"{n}: đủ căn cứ mà không có vế AI"
        if d["trang_thai"] in (PHU_HOP, DU_CAN_CU):                                # R2: thẻ còn hạn, có ngày khám
            the = (luot["benh_nhan"].get("the") or {})
            assert the.get("han_den") and the["han_den"] >= luot.get("ngay_kham", "~"), f"{n}: thẻ {the}"


def kiem_luot(i):
    rnd = random.Random(i)
    luot = luot_ngau_nhien(rnd)
    goc = copy.deepcopy(luot)
    nhan = f"lượt {i}"

    im = A1("im_lang")
    nen = check(luot, RULES, im)
    kiem_ket_qua(luot, nen, im, nhan + " (A1 im lặng)")
    khong_a1 = check(luot, RULES, None)
    kiem_ket_qua(luot, khong_a1, None, nhan + " (a1=None)")
    assert _tt(khong_a1) == _tt(nen), f"{nhan}: a1=None khác A1 im lặng"
    assert khong_a1["a1"]["loi"] == ("a1_tat" if im.calls else None), nhan

    thay = _tt(nen)
    for kieu in ("ngau_nhien", "dong_y", "phan_doi"):
        a1 = A1(kieu, seed=i)
        res = check(luot, RULES, a1)
        thay += _tt(res)
        kiem_ket_qua(luot, res, a1, f"{nhan} (A1 {kieu})")
        assert len(a1.calls) == len(im.calls), f"{nhan}: câu trả lời A1 làm đổi số lần gọi"
        for d, d0 in zip(res["dong"], nen["dong"]):                                                         # (b)
            n = f"{nhan} (A1 {kieu}) dòng {d['thu_tu']} {d['ten']!r}: {d0['trang_thai']} → {d['trang_thai']} ({d['ly_do']})"
            assert d["trang_thai"] != PHU_HOP or d0["trang_thai"] == PHU_HOP, n + " — AI đưa tới Phù hợp"
            assert (d["trang_thai"] == KHONG_TRA) == (d0["trang_thai"] == KHONG_TRA), n + " — AI đổi Không được chi trả"
        assert _bo_ms(check(luot, RULES, A1(kieu, seed=i))) == _bo_ms(res), f"{nhan}: A1 {kieu} không tất định"   # (d)

    chi_rule = A1("dong_y")
    res = check(luot, RULES, chi_rule, mode="chi_rule")
    assert not chi_rule.calls and DU_CAN_CU not in _tt(res), f"{nhan}: chi_rule gọi A1 hoặc có đủ căn cứ"

    # (c) thiếu dữ liệu đầu vào → dịch vụ có điều kiện đọc dữ liệu đó không bao giờ Phù hợp, kể cả khi A1 đồng ý hết
    trong = {**luot, "sinh_hieu": {}, "icd": [], "lich_su": [], "benh_nhan": {"the": luot["benh_nhan"].get("the")}}
    co_tuoi = {**trong, "benh_nhan": luot["benh_nhan"]}                               # còn tuổi, thiếu phần còn lại
    for d in [*check(trong, RULES, A1("dong_y"))["dong"], *check(co_tuoi, RULES, A1("dong_y"))["dong"],
              *check(co_tuoi, RULES, None)["dong"]]:
        assert not (d["trang_thai"] == PHU_HOP and d["ma"] in (CRP, PCT)), f"{nhan}: thiếu dữ liệu mà {d['ten']!r} Phù hợp"
        for v in d["checklist"] if d["ma"] in (CRP, PCT) else ():                     # không có gì nhập thì không vế nào đạt từ nhap
            assert not (v["ket_qua"] == "dat" and v["nguon_ket_qua"] == "nhap"), f"{nhan}: thiếu dữ liệu mà vế {v['id']} đạt từ nhap"
    for thieu in ({**luot, "benh_nhan": {k: v for k, v in luot["benh_nhan"].items() if k != "the"}},
                  {k: v for k, v in luot.items() if k != "ngay_kham"}):
        tt = _tt(check(thieu, RULES, A1("dong_y")))
        assert PHU_HOP not in tt and DU_CAN_CU not in tt, f"{nhan}: thiếu thẻ / ngày khám mà vẫn gợi ý tích"

    assert luot == goc, f"{nhan}: engine sửa dữ liệu đầu vào"
    return thay


def test_bat_bien_ngau_nhien():
    dem = Counter()
    for i in range(SO_LUOT):
        dem.update(kiem_luot(i))
    assert all(dem[t] >= 50 for t in O_GOI_Y), f"bộ sinh lệch, không phủ đủ trạng thái: {dem}"
