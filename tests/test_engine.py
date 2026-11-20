"""Unit test engine (spec 09 mục 4–6, 11). Rules: tests/fixtures/rules (ổn định, không phụ thuộc data/rules)."""
import copy
from pathlib import Path
from types import SimpleNamespace

import pytest

from src.engine import (DU_CAN_CU, KHONG_TRA, PHU_HOP, XEM_LAI, check, gop_dieu_kien, gop_hoac, gop_loai_tru,
                        gop_nhanh)
from src.rules import load_rules

FIX = Path(__file__).parent / "fixtures" / "rules"
CRP, PCT, DOP, CTM = "23.0228.1483", "23.0130.1549", "18.0052.0004", "22.0121.1369"
THE = {"han_den": "2027-12-31", "muc_huong": 100}


@pytest.fixture(scope="module")
def rules():
    return load_rules(FIX)


def kq(ket_qua, nguon="nhap"):
    return {"ket_qua": ket_qua, "nguon": nguon, "bang_chung": "", "trich_dan": None, "trich_lien_quan": []}


def luot(chi_dinh, **kw):
    bn = kw.pop("benh_nhan", {"tuoi_thang": 24})
    bn.setdefault("the", THE)
    return {"luot_kham": "LK", "ngay_kham": "2026-11-12", "benh_nhan": bn, "icd": ["J18.9"],
            "sinh_hieu": {"nhiet_do": 38.8, "mach": 150, "nhip_tho": 46}, "phieu_kham": "Ran ẩm đáy phổi phải.",
            "lich_su": [], "chi_dinh": [{"ma": m, "ten": m} if isinstance(m, str) else m for m in chi_dinh], **kw}


class Stub:
    """A1 giả: ve = {id_ve: (ket_qua, trich_dan)}, so = {truong: gia_tri}. Ghi lại các lần gọi."""

    def __init__(self, ve=None, so=None):
        self.ve, self.so, self.calls = ve or {}, so or {}, []

    def __call__(self, req):
        self.calls.append(req)
        ve = [{"khoa": q["khoa"], "ket_qua": self.ve[q["khoa"].split(":")[1]][0],
               "trich_dan": self.ve[q["khoa"].split(":")[1]][1], "trich_lien_quan": []}
              for q in req["cau_hoi"] if q["khoa"].split(":")[1] in self.ve]
        so = [{"truong": s["truong"], "gia_tri": self.so[s["truong"]], "trich_dan": f"{s['truong']} {self.so[s['truong']]}"}
              for s in req["so_lieu"] if s["truong"] in self.so]
        return {"ve": ve, "so_lieu": so, "loi": None}


def row(res, i=1):
    return res["dong"][i - 1]


def ve(d, vid):
    return next(v for v in d["checklist"] if v["id"] == vid)


# ---------- bảng gộp mục 6 ----------

@pytest.mark.parametrize("states, ky", [
    ([], XEM_LAI),                               # không có nhánh áp dụng
    (["dat_rule"], PHU_HOP),
    (["dat_rule", "truot"], PHU_HOP),
    (["dat_rule", "dat_ai"], PHU_HOP),
    (["dat_rule", "chua_ro"], PHU_HOP),
    (["dat_ai"], DU_CAN_CU),
    (["dat_ai", "truot"], DU_CAN_CU),
    (["dat_ai", "chua_ro"], DU_CAN_CU),
    (["truot"], KHONG_TRA),
    (["truot", "truot", "truot"], KHONG_TRA),
    (["truot", "chua_ro"], XEM_LAI),
    (["chua_ro"], XEM_LAI),
])
def test_gop_dieu_kien(states, ky):
    assert gop_dieu_kien(states) == ky


@pytest.mark.parametrize("ves, ky", [
    ([kq("dat"), kq("dat")], "dat_rule"),
    ([kq("dat"), kq("dat", "a1")], "dat_ai"),
    ([kq("dat"), kq("khong_dat")], "truot"),
    ([kq("khong_dat"), kq("chua_thay", None)], "truot"),
    ([kq("dat"), kq("chua_thay", None)], "chua_ro"),
    ([kq("dat"), kq("chua_du_du_lieu", None)], "chua_ro"),
    ([], "chua_ro"),                             # nhánh rỗng không bao giờ đạt
])
def test_gop_nhanh(ves, ky):
    assert gop_nhanh(ves) == ky


def test_gop_hoac():
    assert gop_hoac([kq("khong_dat"), kq("dat")])["ket_qua"] == "dat"
    assert gop_hoac([kq("dat", "a1"), kq("dat")])["nguon"] == "nhap"
    assert gop_hoac([kq("khong_dat"), kq("khong_dat")])["ket_qua"] == "khong_dat"
    assert gop_hoac([kq("khong_dat"), kq("chua_du_du_lieu", None)])["ket_qua"] == "chua_du_du_lieu"


@pytest.mark.parametrize("ves, ky", [
    ([kq("dat"), kq("dat")], KHONG_TRA),         # mọi vế dat từ nhap
    ([kq("dat", "a1"), kq("dat")], XEM_LAI),     # có vế từ a1
    ([kq("dat", "a1"), kq("khong_dat")], None),  # có vế khác dat → không áp dụng
    ([kq("dat"), kq("chua_du_du_lieu", None)], None),
    ([kq("chua_thay", None)], None),
    ([], None),
])
def test_gop_loai_tru(ves, ky):
    assert gop_loai_tru(ves) == ky


# ---------- end-to-end qua check() ----------

def test_crp_du_can_cu_va_mot_lan_a1(rules):
    a1 = Stub(ve={"V3": ("dat", "Ran ẩm đáy phổi phải")})
    res = check(luot([CRP, CTM, PCT]), rules, a1)
    assert len(a1.calls) == 1 and res["a1"]["goi"]
    khoa = [q["khoa"] for q in a1.calls[0]["cau_hoi"]]
    assert khoa == ["1:V3", "3:N1", "3:N2", "3:X1"]
    d = row(res)
    assert d["trang_thai"] == DU_CAN_CU and d["o_bhyt_goi_y"] == "tich" and d["to_mau"]
    assert ve(d, "V3")["trich_dan"] == "Ran ẩm đáy phổi phải" and ve(d, "V3")["nguon_ket_qua"] == "a1"
    assert row(res, 2)["trang_thai"] == PHU_HOP and row(res, 2)["o_bhyt_goi_y"] == "tich"
    assert d["can_cu"][0]["trich"].startswith("Chẩn đoán") and d["phien_ban_rule"] == rules.phien_ban_rule


def test_moi_nhanh_khong_dat_tu_nhap_khong_goi_a1(rules):
    a1 = Stub()
    res = check(luot([CRP], sinh_hieu={"nhiet_do": 38.2, "mach": 135, "nhip_tho": 46}, icd=["J06.9"]), rules, a1)
    assert a1.calls == [] and not res["a1"]["goi"]
    d = row(res)
    assert d["trang_thai"] == KHONG_TRA and d["o_bhyt_goi_y"] == "trong" and d["ma_ly_do"] == "ve_khong_dat"
    assert "38,2" in d["ly_do"]


def test_so_a1_khong_dat_bi_ha(rules):
    a1 = Stub(ve={"V3": ("dat", "x")}, so={"nhiet_do": 37.5, "nhip_tho": 45})
    res = check(luot([CRP], sinh_hieu={"nhiet_do": None, "mach": None, "nhip_tho": None}), rules, a1)
    assert {s["truong"] for s in a1.calls[0]["so_lieu"]} == {"nhiet_do", "nhip_tho"}  # mạch: chưa có ngưỡng → không hỏi
    d = row(res)
    assert ve(d, "V1")["ket_qua"] == "chua_du_du_lieu" and ve(d, "V1")["nguon_ket_qua"] == "a1"
    assert ve(d, "V2")["ket_qua"] == "dat" and ve(d, "V2")["nguon_ket_qua"] == "a1"
    assert d["trang_thai"] == XEM_LAI


def test_so_a1_dat_chi_toi_du_can_cu(rules):
    a1 = Stub(ve={"V3": ("dat", "x")}, so={"nhiet_do": 38.8, "nhip_tho": 45})
    d = row(check(luot([CRP], sinh_hieu={}), rules, a1))
    assert d["trang_thai"] == DU_CAN_CU  # AI không đưa tới Phù hợp, kể cả qua số


def test_ai_doc_toi_da_chua_thay(rules):
    a1 = Stub(ve={"N2": ("dat", "Lơ mơ")})
    d = row(check(luot([PCT]), rules, a1))
    assert ve(d, "N2")["ket_qua"] == "chua_thay" and ve(d, "N2")["trich_dan"] == "Lơ mơ"
    assert d["trang_thai"] == XEM_LAI


def test_a1_none_o_full_la_a1_tat(rules):
    res = check(luot([CRP]), rules, None)
    assert res["a1"] == {"goi": False, "loi": "a1_tat", "ms": 0}
    assert ve(row(res), "V3")["ket_qua"] == "chua_thay" and row(res)["trang_thai"] == XEM_LAI


def test_a1_raise_khong_chan(rules):
    def hong(req):
        raise TimeoutError
    res = check(luot([CRP]), rules, hong)
    assert res["a1"]["loi"] == "a1_loi_TimeoutError" and row(res)["trang_thai"] == XEM_LAI


# ---------- loại trừ: nhap vs a1 ----------

def _pct_lich_su(ket_qua, ngay_cach=3):
    return [{"ma": PCT, "ngay_cach": ngay_cach, "ket_qua": ket_qua, "tham_chieu_tren": 0.5}]


def test_loai_tru_co_a1_chi_can_xem_lai(rules):
    a1 = Stub(ve={"N1": ("dat", "Theo dõi nhiễm trùng huyết"), "X1": ("dat", "Hết sốt")})
    d = row(check(luot([PCT], lich_su=_pct_lich_su(0.4)), rules, a1))
    assert ve(d, "X1")["ket_qua"] == "dat" and ve(d, "X2")["ket_qua"] == "dat"
    assert d["trang_thai"] == XEM_LAI and d["ma_ly_do"] == "loai_tru"


def test_loai_tru_khong_ap_dung_khi_mot_ve_khong_dat(rules):
    a1 = Stub(ve={"N1": ("dat", "x"), "X1": ("dat", "y")})
    d = row(check(luot([PCT], lich_su=_pct_lich_su(2.5)), rules, a1))
    assert ve(d, "X2")["ket_qua"] == "khong_dat" and d["trang_thai"] == DU_CAN_CU


def test_loai_tru_toan_nhap_khong_tra(rules):
    r = copy.deepcopy(rules)
    r.dieu_kien[PCT]["loai_tru"]["ve"][0] = {
        "id": "X1", "mo_ta": "Nhiệt độ < 37,5", "kiem": {"loai": "so_sanh", "truong": "nhiet_do", "toan_tu": "<", "gia_tri": 37.5}}
    a1 = Stub(ve={"N1": ("dat", "x")})
    d = row(check(luot([PCT], sinh_hieu={"nhiet_do": 36.8}, lich_su=_pct_lich_su(0.4)), r, a1))
    assert d["trang_thai"] == KHONG_TRA and d["ma_ly_do"] == "loai_tru"
    assert a1.calls == []  # loại trừ đã đủ từ nhap: AI không đổi được kết luận → không hỏi


# ---------- tần suất ----------

@pytest.mark.parametrize("ngay_cach, ky, ly_do", [
    (0, KHONG_TRA, "Đã làm cách 0 giờ; giới hạn 48 giờ (cách hiểu tạm M-10, chưa được bác sĩ duyệt)"),
    (1, XEM_LAI, "Đã làm cách 24 giờ; giới hạn 48 giờ (cách hiểu tạm M-10, chưa được bác sĩ duyệt)"),
    (2, DU_CAN_CU, None),                        # 48 giờ: hết giới hạn
])
def test_tan_suat(rules, ngay_cach, ky, ly_do):
    a1 = Stub(ve={"N1": ("dat", "x")})
    d = row(check(luot([PCT], lich_su=_pct_lich_su(3.2, ngay_cach)), rules, a1))
    assert d["trang_thai"] == ky
    if ly_do:
        assert d["ly_do"] == ly_do and d["ma_ly_do"] == "tan_suat"


def test_tan_suat_duoi_24h_khong_hoi_a1(rules):
    a1 = Stub()
    check(luot([PCT], lich_su=_pct_lich_su(3.2, 0)), rules, a1)
    assert a1.calls == []


# ---------- R4 ----------

def test_r4_hai_dong_ma_null_khac_ten(rules):
    d = check(luot([{"ma": None, "ten": "Test nhanh RSV"}, {"ma": None, "ten": "Định lượng Kẽm"}]), rules, None)["dong"]
    assert [x["ma_ly_do"] for x in d] == ["khong_thay", "xac_minh"]


def test_r4_ma_null_cung_ten_chuan_hoa(rules):
    d = check(luot([{"ma": None, "ten": "Tổng phân tích  tế bào máu ngoại vi"},
                    {"ma": None, "ten": "tổng phân tích tế bào máu ngoại vi "}]), rules, None)["dong"]
    assert d[0]["trang_thai"] == PHU_HOP and d[1]["ma_ly_do"] == "trung_dong" and d[1]["trang_thai"] == XEM_LAI


def test_r4_trung_ma(rules):
    d = check(luot([CTM, CTM]), rules, None)["dong"]
    assert d[0]["trang_thai"] == PHU_HOP and d[1]["trang_thai"] == XEM_LAI and d[1]["ma_ly_do"] == "trung_dong"


# ---------- tuổi ----------

def _so_sinh(bn, icd=("P36.9",)):
    return luot([CRP], benh_nhan=bn, icd=list(icd), sinh_hieu={"nhiet_do": 37.2, "mach": 160, "nhip_tho": 58})


@pytest.mark.parametrize("bn, ky", [
    ({"tuoi_ngay": 0}, PHU_HOP),
    ({"tuoi_ngay": 28}, PHU_HOP),                # [0, 29) ngày
    ({"tuoi_ngay": 29}, KHONG_TRA),              # nhánh b không áp dụng; a trượt (37,2), c, d trượt
    ({"tuoi_thang": 0}, XEM_LAI),                # chỉ có tháng = 0 → nhánh b chưa đủ dữ liệu
    ({"tuoi_thang": 1}, KHONG_TRA),              # tháng ≥ 1 → nhánh b không áp dụng
    ({}, XEM_LAI),                               # không có tuổi → nhánh có ap_dung chưa đủ dữ liệu
])
def test_tuoi_nhanh_so_sinh(rules, bn, ky):
    assert row(check(_so_sinh(bn), rules, None))["trang_thai"] == ky


def test_tuoi_ngay_quy_ra_thang(rules):
    # 50 ngày → 1 tháng → băng [0, 2) ngưỡng 60: nhịp thở 56 không đạt
    d = row(check(luot([CRP], benh_nhan={"tuoi_ngay": 50}, sinh_hieu={"nhiet_do": 38.6, "nhip_tho": 56}), rules, None))
    assert "nhịp thở 56" in ve(d, "V2")["bang_chung"]
    d = row(check(luot([CRP], benh_nhan={"tuoi_thang": 2}, sinh_hieu={"nhiet_do": 38.6, "nhip_tho": 56}), rules, None))
    assert ve(d, "V2")["ket_qua"] == "dat"


def test_khong_co_nhanh_ap_dung(rules):
    r = copy.deepcopy(rules)
    r.dieu_kien[CRP]["nhanh"] = [r.dieu_kien[CRP]["nhanh"][0]]  # chỉ nhánh trẻ em
    d = row(check(luot([CRP], benh_nhan={"tuoi_thang": 194}), r, Stub()))
    assert d["trang_thai"] == XEM_LAI and d["ma_ly_do"] == "khong_nhanh"


def test_nhanh_nguoi_lon_chua_ma_hoa_khong_ket_luan(rules):
    d = row(check(luot([CRP], benh_nhan={"tuoi_thang": 194}), rules, Stub()))
    assert d["trang_thai"] == XEM_LAI


# ---------- R1, R2 ----------

@pytest.mark.parametrize("cd, ky, ma_ly_do", [
    ({"ma": None, "ten": "Test nhanh RSV"}, KHONG_TRA, "khong_thay"),
    ({"ma": None, "ten": "Kẽm"}, XEM_LAI, "xac_minh"),              # khớp bí danh
    ({"ma": None, "ten": "Định lượng IgE đặc hiệu"}, XEM_LAI, "chua_tra"),
    ({"ma": "99.0000.0001", "ten": "x"}, XEM_LAI, "chua_co_dieu_kien"),
])
def test_r1(rules, cd, ky, ma_ly_do):
    d = row(check(luot([cd]), rules, None))
    assert (d["trang_thai"], d["ma_ly_do"]) == (ky, ma_ly_do)


def test_r1_khong_thay_co_hau_to_tu_dung(rules):
    assert row(check(luot([{"ma": None, "ten": "Test nhanh RSV"}]), rules, None))["ly_do"].endswith(
        "(cách hiểu tạm M-13, chưa được bác sĩ duyệt)")


@pytest.mark.parametrize("the, ky", [
    (None, XEM_LAI),
    ({"han_den": "2026-11-11", "muc_huong": 80}, KHONG_TRA),
    ({"han_den": "2026-11-12", "muc_huong": 80}, PHU_HOP),
])
def test_r2(rules, the, ky):
    d = row(check(luot([CTM], benh_nhan={"tuoi_thang": 84, "the": the}), rules, None))
    assert d["trang_thai"] == ky


def test_r2_het_han_ly_do_va_khong_hoi_a1(rules):
    a1 = Stub()
    d = row(check(luot([CRP], benh_nhan={"tuoi_thang": 24, "the": {"han_den": "2026-11-11"}}), rules, a1))
    assert d["ly_do"] == "Thẻ BHYT hết hạn 11/11/2026" and a1.calls == []


def test_thieu_ngay_kham_can_xem_lai(rules):
    l = luot([CTM])
    del l["ngay_kham"]
    assert row(check(l, rules, None))["trang_thai"] == XEM_LAI


# ---------- Doppler, chỉ-rule ----------

def test_doppler_cung_luot(rules):
    d = check(luot([DOP, {"ma": None, "ten": "Siêu âm tim  cản âm"}]), rules, None)["dong"]
    assert d[0]["trang_thai"] == KHONG_TRA and d[1]["trang_thai"] == XEM_LAI
    assert row(check(luot([DOP]), rules, None))["trang_thai"] == PHU_HOP


def test_chi_rule_bo_qua_ve_ai_trong_nhanh_co_ve_rule(rules):
    res = check(luot([CRP, PCT]), rules, Stub(), mode="chi_rule")
    assert not res["a1"]["goi"]
    assert row(res)["trang_thai"] == PHU_HOP          # V1, V2 rule đạt; V3 bỏ qua
    assert row(res, 2)["trang_thai"] == XEM_LAI       # nhánh toàn vế AI → chưa đủ dữ liệu


def test_ve_chua_ma_hoa_khong_bao_gio_dat():
    r = SimpleNamespace(danh_muc=[{"ma": "X", "ten": "X", "bhyt": "dieu_kien"}], tham_so={}, phien_ban_rule="t",
                        dieu_kien={"X": {"nhanh": [{"id": "n", "ve": [{"id": "Z", "mo_ta": "chưa mã hóa"}]}]}})
    assert row(check(luot(["X"]), r, None))["trang_thai"] == XEM_LAI


# ---------- hậu tố "cách hiểu tạm": chỉ kể giá trị tu_dung thật sự dùng ----------

XQ, CANXI = "18.0119.0028", "23.0030.1472"
HAU_TO = "(cách hiểu tạm {}, chưa được bác sĩ duyệt)"


def test_hau_to_loai_tru_khong_ke_tham_chieu_khong_dung(rules):
    a1 = Stub(ve={"N1": ("dat", "x"), "X1": ("dat", "Hết sốt")})
    d = row(check(luot([PCT], lich_su=_pct_lich_su(0.4)), rules, a1))  # dùng tham_chieu_tren của bản ghi
    assert d["ma_ly_do"] == "loai_tru" and "cách hiểu tạm" not in d["ly_do"]
    ls = [{"ma": PCT, "ngay_cach": 3, "ket_qua": 0.4}]                 # không có → dùng @pct_tham_chieu (M-10)
    d = row(check(luot([PCT], lich_su=ls), rules, a1))
    assert d["ma_ly_do"] == "loai_tru" and d["ly_do"].endswith(HAU_TO.format("M-10"))


def _rules_hoac():
    ve = {"id": "H", "mo_ta": "sốt hoặc mạch nhanh", "hoac": [
        {"loai": "so_sanh", "truong": "nhiet_do", "toan_tu": ">=", "gia_tri": 38, "nguon": "tu_dung", "diem_mo_ho": "M-91"},
        {"loai": "so_sanh", "truong": "mach", "toan_tu": ">=", "gia_tri": 100, "nguon": "tu_dung", "diem_mo_ho": "M-92"}]}
    return SimpleNamespace(danh_muc=[{"ma": "X", "ten": "X", "bhyt": "dieu_kien"}], tham_so={}, phien_ban_rule="t",
                           dieu_kien={"X": {"nhanh": [{"id": "n", "ve": [ve]}]}})


def test_hau_to_hoac_chi_ke_ve_con_dat():
    d = row(check(luot(["X"], sinh_hieu={"nhiet_do": 39, "mach": 80}), _rules_hoac(), None))
    assert d["trang_thai"] == PHU_HOP and d["ly_do"].endswith(HAU_TO.format("M-91"))
    d = row(check(luot(["X"], sinh_hieu={"nhiet_do": 37, "mach": 80}), _rules_hoac(), None))
    assert d["trang_thai"] == KHONG_TRA and d["ly_do"].endswith(HAU_TO.format("M-91, M-92"))  # trượt vì cả hai


def test_phu_hop_theo_danh_muc_tu_dung_co_hau_to(rules):
    d = check(luot([CANXI, CTM]), rules, None)["dong"]
    assert d[0]["trang_thai"] == PHU_HOP and d[0]["ly_do"].endswith(HAU_TO.format("M-12"))
    assert d[1]["trang_thai"] == PHU_HOP and d[1]["ly_do"] == "Có trong danh mục BHYT, không có điều kiện thanh toán riêng"


# ---------- chống vỡ: A1 trả sai dạng, quy tắc hỏng, ngày sai dạng ----------

@pytest.mark.parametrize("tra", [
    {"ve": [{"sai": 1}], "so_lieu": []},
    {"ve": "x", "so_lieu": [{"gia_tri": 1}]},
    ["khong phai dict"],
])
def test_a1_tra_sai_dang_khong_vo(rules, tra):
    res = check(luot([CRP]), rules, lambda req: tra)
    assert res["a1"]["goi"] and res["a1"]["loi"].startswith("a1_loi_") and row(res)["trang_thai"] == XEM_LAI


@pytest.mark.parametrize("gia_tri", ["39", True, float("nan"), float("inf")])
def test_so_a1_khong_phai_so_bi_bo(rules, gia_tri):
    a1 = lambda req: {"ve": [{"khoa": "1:V3", "ket_qua": "dat", "trich_dan": "x"}], "loi": None,  # noqa: E731
                      "so_lieu": [{"truong": "nhiet_do", "gia_tri": gia_tri, "trich_dan": "x"}]}
    d = row(check(luot([CRP], sinh_hieu={"nhip_tho": 46}), rules, a1))
    assert ve(d, "V1")["ket_qua"] == "chua_du_du_lieu" and d["trang_thai"] == XEM_LAI


def test_quy_tac_hong_chi_dong_do_can_xem_lai(rules):
    r = copy.deepcopy(rules)
    del r.dieu_kien[CRP]["nhanh"][0]["ve"][0]["hoac"][0]["gia_tri"]
    d = check(luot([CRP, CTM]), r, Stub())["dong"]
    assert (d[0]["trang_thai"], d[0]["ma_ly_do"]) == (XEM_LAI, "loi_quy_tac") and d[1]["trang_thai"] == PHU_HOP


def test_khoa_cau_hoi_khong_lap():
    ai = {"loai": "ai_doc", "cau_hoi": "?"}
    r = SimpleNamespace(danh_muc=[{"ma": "X", "ten": "X", "bhyt": "dieu_kien"}], tham_so={}, phien_ban_rule="t",
                        dieu_kien={"X": {"nhanh": [{"id": "n", "ve": [{"id": "Z", "mo_ta": "z", "hoac": [ai, ai]}]}]}})
    a1 = Stub()
    check(luot(["X"]), r, a1)
    assert [q["khoa"] for q in a1.calls[0]["cau_hoi"]] == ["1:Z"]


@pytest.mark.parametrize("ngay_kham, han_den, ky", [
    ("2026-11-12T08:30:00", "2026-11-12", PHU_HOP),   # có giờ: vẫn so theo ngày
    ("2026-11-12T08:30:00", "2026-11-11T23:59:59", KHONG_TRA),
    ("hôm nay", "2027-12-31", XEM_LAI),               # không đọc được → không kết luận
    ("2026-11-12", "31/12/2027", XEM_LAI),
])
def test_ngay_co_gio_hoac_sai_dang(rules, ngay_kham, han_den, ky):
    l = luot([CTM], benh_nhan={"tuoi_thang": 24, "the": {"han_den": han_den, "muc_huong": 100}}, ngay_kham=ngay_kham)
    assert row(check(l, rules, None))["trang_thai"] == ky


# ---------- R4 qua danh mục, can_cu ----------

def test_r4_ma_va_bi_danh_cung_dich_vu(rules):
    d = check(luot([CTM, {"ma": None, "ten": "ctm"}]), rules, None)["dong"]
    assert d[0]["trang_thai"] == PHU_HOP and d[1]["ma_ly_do"] == "trung_dong"


def test_can_cu_luon_co_trich(rules):
    d = check(luot([XQ, CRP]), rules, None)["dong"]
    assert d[0]["can_cu"] == [{"trich": None, "van_ban": "TT 23/2024", "phu_luc": "PL01"}]
    assert d[1]["can_cu"][0]["trich"].startswith("Chẩn đoán") and d[1]["can_cu"][0]["stt"] == 7
    r = copy.deepcopy(rules)
    r.dieu_kien[CRP]["can_cu"][0]["trich"] = "riêng"                  # trích riêng của căn cứ được giữ
    assert row(check(luot([CRP]), r, None))["can_cu"][0]["trich"] == "riêng"


def test_nhac_thieu_chan_doan_khong_doi_trang_thai(rules):
    co, khong = check(luot([CTM]), rules, None), check(luot([CTM], icd=[]), rules, None)
    assert co["nhac"] == [] and [n["ma"] for n in khong["nhac"]] == ["thieu_chan_doan"]
    assert khong["dong"][0]["trang_thai"] == co["dong"][0]["trang_thai"] == PHU_HOP  # chưa ICD lúc chỉ định là bình thường
    assert all(c["van_ban"].startswith("QĐ 4750") and c["trich"] for c in khong["nhac"][0]["can_cu"])


# ---------- dữ liệu nhập lệch dạng, danh mục lớn ----------

def test_icd_khong_dau_cham_van_khop(rules):
    # HIS có thể gửi "D690" thay cho "D69.0": khác định dạng không được thành Không được chi trả
    d = row(check(luot([CRP], icd=["d690"], sinh_hieu={}), rules, None))
    assert ve(d, "D1")["ket_qua"] == "dat" and d["trang_thai"] == PHU_HOP


@pytest.mark.parametrize("gia_tri", [385, float("nan"), float("inf")])
def test_sinh_hieu_nhap_ngoai_khoang_khong_lam_can_cu(rules, gia_tri):
    # 385 = gõ nhầm 38,5 → không được làm vế đạt; NaN → không được làm vế trượt (thành Không được chi trả)
    a1 = Stub(ve={"V3": ("dat", "Ran ẩm đáy phổi phải.")})
    d = row(check(luot([CRP], sinh_hieu={"nhiet_do": gia_tri, "mach": 150, "nhip_tho": 46}), rules, a1))
    v1 = ve(d, "V1")
    assert v1["ket_qua"] == "chua_du_du_lieu" and "ngoài khoảng hợp lệ" in v1["bang_chung"]
    assert d["trang_thai"] == XEM_LAI
    assert not any(s["truong"] == "nhiet_do" for c in a1.calls for s in c["so_lieu"])  # bác sĩ sửa số, không nhờ AI


def test_ten_khop_nhieu_dong_danh_muc():
    def r(bhyt_b):
        return SimpleNamespace(danh_muc=[{"ma": "A", "ten": "Xét nghiệm X", "bhyt": "co"},
                                         {"ma": "B", "ten": "Xét nghiệm X máy 2", "bi_danh": ["Xét nghiệm X"], "bhyt": bhyt_b}],
                               tham_so={}, phien_ban_rule="t", dieu_kien={})
    ten = {"ma": None, "ten": "Xét nghiệm X"}
    d = row(check(luot([ten]), r("xac_minh"), None))   # khác kết luận: không được lặng lẽ chọn dòng đầu
    assert (d["trang_thai"], d["ma_ly_do"]) == (XEM_LAI, "nhap_nhang")
    assert row(check(luot([{"ma": "A", "ten": "Xét nghiệm X"}]), r("xac_minh"), None))["trang_thai"] == PHU_HOP  # có mã
    assert row(check(luot([ten]), r("co"), None))["trang_thai"] == PHU_HOP  # cùng kết luận (vd Mycoplasma 2 mã giá)
