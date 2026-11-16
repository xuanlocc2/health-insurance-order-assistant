"""Unit test các hàm chỉ số của run_eval.py trên dữ liệu tổng hợp (không cần engine / rules)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_eval as E  # noqa: E402

P, D, X, K = E.THU_TU


def row(ky, got, ca="C1", lan=1, tt=1, chi_rule=None):
    return {"ca": ca, "lan": lan, "thu_tu": tt, "ten": "dv", "ky_vong": ky, "got": got, "chi_rule": chi_rule, "bay": []}


def ve(ky, got, ai=True, bay=(), ca="C1", lan=1, vid="V1"):
    return {"ca": ca, "lan": lan, "thu_tu": 1, "id": vid, "nhanh": None, "ai": ai, "ky_vong": ky, "got": got, "bay": list(bay)}


def so(ky, got, hoi=True, trong_ok=False, truong="nhiet_do"):
    return {"ca": "C1", "lan": 1, "truong": truong, "ky_vong": ky, "got": got, "hoi": hoi, "trong_ok": trong_ok, "bay": []}


def call(goi=True, loi=None, ms=100, a1_ms=80, trich=None, trich_bo=None, tok=(None, None), ca="C1", lan=1):
    return {"ca": ca, "lan": lan, "ms": ms, "goi": goi, "loi": loi, "a1_ms": a1_ms,
            "tok_vao": tok[0], "tok_ra": tok[1], "trich": trich, "trich_bo": trich_bo}


def test_m_dong_confusion_va_qua_thuan_loi():
    m = E.m_dong([row(P, P), row(X, P, ca="C2"), row(K, D, ca="C3"), row(P, X, ca="C4"),
                  row(X, None, ca="C5"), row(None, P, ca="KHO")])
    assert (m["n"], m["khong_nhan"], m["dung"]) == (5, 1, 1)
    assert m["qua_thuan_loi"] == 2 and {r["ca"] for r in m["ds_qua_thuan_loi"]} == {"C2", "C3"}
    assert m["kem_thuan_loi"] == 1 and m["khong_co_dong"] == 1
    assert m["ma_tran"][f"{X}|{P}"] == 1 and sum(m["ma_tran"].values()) == 5


def test_m_dong_rong():
    m = E.m_dong([row(None, P)])
    assert m["n"] == 0 and m["ty_le_dung"] is None and m["qua_thuan_loi"] == 0


def test_m_ve_dat_sai_bo_sot_theo_bay():
    m = E.m_ve([ve("chua_thay", "dat", bay=["phu_dinh"]),              # AI đạt sai
                ve("dat", "chua_thay", bay=["phu_dinh", "viet_tat"]),  # AI bỏ sót
                ve("dat", "dat", bay=["viet_tat"]),
                ve("khong_dat", "dat", ai=False),                      # vế rule sai: không tính là AI đạt sai
                ve("dat", None)])                                      # engine không có vế → bỏ sót
    assert m["ai"]["dat_sai"] == 1 and m["ai"]["bo_sot_dat"] == 2 and m["ai"]["n"] == 4
    assert m["rule"]["n"] == 1 and m["tat_ca"]["dung"] == 1
    assert len(m["ds_dat_sai"]) == 1 and m["ds_dat_sai"][0]["ky_vong"] == "chua_thay"
    assert m["theo_bay"]["phu_dinh"] == {"n": 2, "dung": 0, "ty_le_dung": 0.0, "dat_sai": 1, "bo_sot_dat": 1, "dat_sai_cho": 0}
    assert m["theo_bay"]["viet_tat"]["dung"] == 1


def test_m_so():
    m = E.m_so([so(38.6, 38.6), so(38.6, 38.5), so(132, None), so(None, 40), so(None, None),
                so(36, None, hoi=False), so(39.5, None, trong_ok=True), so(39.5, 39.0, trong_ok=True)])
    assert (m["dung"], m["sai_gia_tri"], m["bo_sot"], m["trich_thua"], m["khong_hoi"]) == (3, 2, 1, 1, 1)
    assert m["n"] == 7 and len(m["ds_sai"]) == 4


def test_so_ky_vong_va_trong_ok():
    c = {"a1_ky_vong_so_lieu": [{"truong": "mach", "gia_tri": 132}, {"truong": "nhiet_do", "gia_tri": 39.5, "chap_nhan_trong": True}],
         "a1_gia_lap": {"so_lieu": [{"truong": "mach", "gia_tri": 1}]}}
    assert E.so_ky_vong(c) == {"mach": 132, "nhiet_do": 39.5} and E.so_trong_ok(c) == {"nhiet_do"}
    assert E.so_ky_vong({"a1_gia_lap": {"so_lieu": [{"truong": "mach", "gia_tri": 1}]}}) == {"mach": 1}
    assert E.so_ky_vong({"a1_ky_vong_so_lieu": []}) == {} and E.so_ky_vong({}) is None


def test_m_trich():
    m = E.m_trich([call(trich=3, trich_bo=1, loi=E.LOI_TRICH), call(trich=2, trich_bo=0, lan=2),
                   call(goi=False), call(loi="a1_loi_APITimeoutError")])
    assert (m["so_lan_goi"], m["trich_dan"], m["bi_bo"], m["lan_goi_co_loi_trich"]) == (2, 5, 1, 1)
    assert m["ds"] == [{"ca": "C1", "lan": 1, "bi_bo": 1}]


def test_m_on_dinh():
    m = E.m_on_dinh([row(P, P, lan=1), row(P, X, lan=2), row(X, X, ca="C2", lan=1), row(X, X, ca="C2", lan=2),
                     row(X, X, ca="C3")],  # 1 lần: không tính
                    [ve("dat", "dat", lan=1), ve("dat", "chua_thay", lan=2)])
    assert (m["dong"]["n"], m["dong"]["lat"]) == (2, 1) and m["dong"]["ds"][0]["khoa"] == "C1/1"
    assert (m["ve"]["n"], m["ve"]["lat"]) == (1, 1)


def test_m_ops():
    calls = [call(ms=i * 100, a1_ms=i * 10, tok=(1000, 100)) for i in range(1, 19)]
    calls += [call(ms=9000, loi="a1_loi_APITimeoutError"), call(ms=50, loi=E.LOI_TRICH), call(goi=False, loi="a1_tat", ms=1)]
    m = E.m_ops(calls, gia_vao=2.0, gia_ra=10.0)
    assert (m["luot"], m["goi_a1"], m["loi"], m["het_gio"]) == (21, 20, 1, 1)  # LOI_TRICH không phải lỗi gọi
    assert m["ty_le_loi"] == 0.05 and m["check_ms_max"] == 9000 and m["check_ms_p95"] == 1800
    assert (m["token_vao"], m["token_ra"], m["lan_goi_co_usage"]) == (18000, 1800, 18)
    assert abs(m["chi_phi_usd"] - (0.018 * 2 + 0.0018 * 10)) < 1e-12
    assert E.m_ops(calls)["chi_phi_usd"] is None


def test_phan_vi():
    assert E.phan_vi([], 50) is None and E.phan_vi([5], 95) == 5
    assert E.phan_vi(list(range(1, 101)), 50) == 50 and E.phan_vi(list(range(1, 101)), 95) == 95


def test_m_chi_rule_gia_tri_a1():
    rows = [row(X, X, ca="A", chi_rule=P),         # chỉ-rule quá thuận lợi, hệ đầy đủ bắt được
            row(X, P, ca="B", chi_rule=P),         # A1 bỏ lọt
            row(P, P, ca="C", chi_rule=P),
            row(X, X, ca="A", lan=2, chi_rule=P),  # chỉ tính lần 1
            row(None, P, ca="KHO", chi_rule=P)]    # không nhãn
    m = E.m_chi_rule(rows, [{"ca": "A", "nhan": P, "got": P}, {"ca": "B", "nhan": X, "got": P}])
    assert (m["n_dong"], m["chi_rule_dung"], m["chi_rule_qua_thuan_loi"], m["he_day_du_bat_duoc"]) == (3, 1, 2, 1)
    assert [r["ca"] for r in m["ds_a1_gia_tri"]] == ["A"] and [r["ca"] for r in m["ds_a1_bo_lo"]] == ["B"]
    assert m["nhan_he_chi_rule"]["khop"] == 1 and m["nhan_he_chi_rule"]["ds_lech"][0]["ca"] == "B"


def test_mac_dinh():
    luot = E.mac_dinh({"id": "X", "benh_nhan": {"tuoi_thang": 30}, "ky_vong": [], "bay": ["a"]})
    assert luot["benh_nhan"]["the"]["muc_huong"] == 100 and luot["lan_tich"] == 2 and "ky_vong" not in luot
    assert E.mac_dinh({"id": "Y", "benh_nhan": {"tuoi_thang": 96}})["benh_nhan"]["the"]["muc_huong"] == 80


def test_ban_ghi_va_render():
    case = {"id": "C1", "bay": ["phu_dinh"], "a1_ky_vong_so_lieu": [{"truong": "mach", "gia_tri": 132}]}
    pairs = [(1, {"ma": "m", "ve": [{"id": "V3", "kiem_bang": "ai", "ket_qua": "chua_thay"}, {"mo_ta": "không id"}]}),
             (2, {"ten": "x", "trang_thai": X})]
    visit = {"dong": {1: {"trang_thai": P, "ten": "CRP", "checklist": [{"id": "V3", "ket_qua": "dat", "nhanh": "a"}]}},
             "chi_rule": {1: P, 2: P}, "so_lieu": {"mach": 132.0, "nhiet_do": 39.0}, "so_hoi": ["mach", "nhiet_do"]}
    rows, cl, sl = E.ban_ghi(case, pairs, visit, 1)
    assert [(r["ky_vong"], r["got"]) for r in rows] == [(None, P), (X, None)]
    assert len(cl) == 1 and cl[0]["ai"] and cl[0]["got"] == "dat" and cl[0]["bay"] == ["phu_dinh"]
    assert {s["truong"]: (s["ky_vong"], s["got"]) for s in sl} == {"mach": (132, 132.0), "nhiet_do": (None, 39.0)}
    rec = {"rows": rows, "clauses": cl, "so": sl, "calls": [call(trich=1, trich_bo=0)], "he": []}
    s = E.tinh(rec)
    assert s["ve"]["ai"]["dat_sai"] == 1 and s["so"]["trich_thua"] == 1 and s["dong"]["khong_co_dong"] == 1
    md = E.render_md(s, {"a1": "stub", "lan": 1, "so_ca": 1, "cases": ["x"], "phien_ban_rule": "abc"})
    assert "CHƯA ĐẠT" in md and "(không có dòng)" in md and "## 7." in md
    empty = E.tinh({"rows": [], "clauses": [], "so": [], "calls": [], "he": []})
    assert "## 1." in E.render_md(empty, {})


def test_giao():
    assert E.giao("Phổi  hết ran", "phổi hết ran nổ") and E.giao("họng đỏ", "Khám: họng đỏ, amidan mủ")
    assert not E.giao("mẹ bị viêm họng", "tai P chảy mủ") and not E.giao(None, "x") and not E.giao("", "x")


def test_a1_kho_schema():
    """Bộ a1-kho: không trang_thai → chấm câu trả lời A1; dat phải giao trich_dan / trich_dan_khac; [] = không được trích."""
    case = {"id": "KHO-X", "bay": ["nguoi_khac"], "a1_ky_vong_so_lieu": []}
    kv = {"ma": "m", "ve": [
        {"id": "V3", "kiem_bang": "ai", "ket_qua": "dat", "trich_dan": "tai P chảy mủ vàng", "trich_dan_khac": ["CĐ: viêm tai giữa"]},
        {"id": "N1", "kiem_bang": "ai", "ket_qua": "dat", "trich_dan": "TD NTH"},
        {"id": "X1", "kiem_bang": "ai", "ket_qua": "dat", "trich_dan": "hết sốt 3 ngày"},
        {"id": "N2", "kiem_bang": "ai", "ket_qua": "chua_thay"}]}
    visit = {"dong": {1: {"trang_thai": E.XEM_LAI, "checklist": [
                {"id": "V3", "ket_qua": "chua_du_du_lieu", "nhanh": "a"}, {"id": "N2", "ket_qua": "chua_thay", "nhanh": "b"}]}},
             "a1_ve": {"1:V3": {"khoa": "1:V3", "ket_qua": "dat", "trich_dan": "viêm tai giữa"},        # giao trich_dan_khac
                       "1:N1": {"khoa": "1:N1", "ket_qua": "dat", "trich_dan": "mẹ đang sốt cao"},      # đoạn bẫy
                       "1:X1": {"khoa": "1:X1", "ket_qua": "chua_thay", "trich_dan": None}},
             "so_lieu": {"mach": 120.0}, "so_hoi": ["mach", "nhiet_do"]}
    rows, cl, sl = E.ban_ghi(case, [(1, kv)], visit, 1)
    by = {c["id"]: c for c in cl}
    assert (by["V3"]["got"], by["V3"]["nguon_got"], by["V3"]["sai_cho"]) == ("dat", "a1", False)  # không lấy chua_du_du_lieu của engine
    assert by["N1"]["sai_cho"] and not by["X1"]["sai_cho"] and by["N2"]["nguon_got"] == "engine"
    s = E.tinh({"rows": rows, "clauses": cl, "so": sl, "calls": [], "he": []})
    assert s["dong"]["n"] == 0 and s["dong"]["khong_nhan"] == 1 and s["dong"]["qua_thuan_loi"] == 0
    ai = s["ve"]["ai"]
    assert (ai["n"], ai["dung"], ai["dat_sai"], ai["bo_sot_dat"], ai["dat_sai_cho"]) == (4, 2, 0, 1, 1)
    assert [c["id"] for c in s["ve"]["ds_dat_sai_cho"]] == ["N1"] and s["ve"]["theo_bay"]["nguoi_khac"]["dat_sai_cho"] == 1
    assert (s["so"]["trich_thua"], s["so"]["dung"], s["so"]["n"]) == (1, 1, 2)  # mach trích thừa, nhiet_do đúng là bỏ trống
    assert "trích sai chỗ" in E.render_md(s, {})


def test_engine_label_khong_dung_a1_ve():
    """Ca data/test-cases (có trang_thai): vế chấm theo checklist của engine."""
    kv = {"ma": "m", "trang_thai": E.XEM_LAI, "ve": [{"id": "N2", "kiem_bang": "ai", "ket_qua": "chua_du_du_lieu"}]}
    visit = {"dong": {1: {"trang_thai": E.XEM_LAI, "checklist": [{"id": "N2", "ket_qua": "chua_du_du_lieu"}]}},
             "a1_ve": {"1:N2": {"khoa": "1:N2", "ket_qua": "dat", "trich_dan": "x"}}}
    _, cl, _ = E.ban_ghi({"id": "C"}, [(1, kv)], visit, 1)
    assert cl[0]["got"] == "chua_du_du_lieu" and cl[0]["nguon_got"] == "engine"


def test_dem_trich():
    raw = {"ve": [{"ket_qua": "dat", "trich_dan": "a", "trich_lien_quan": ["b", "c"]},
                  {"ket_qua": "dat", "trich_dan": "bịa"}, {"ket_qua": "chua_thay", "trich_dan": None}],
           "so_lieu": [{"truong": "mach", "gia_tri": 1, "trich_dan": "x"}, {"truong": "nhiet_do", "gia_tri": 2, "trich_dan": "y"}]}
    res = {"ve": [{"ket_qua": "dat", "trich_dan": "a", "trich_lien_quan": ["b"]}, {"ket_qua": "chua_thay", "trich_dan": None}],
           "so_lieu": [{"truong": "mach", "gia_tri": 1.0, "trich_dan": "x"}]}
    assert E.dem_trich(raw, res) == (6, 3) and E.dem_trich(raw, raw) == (6, 0) and E.dem_trich(None, {}) == (0, 0)


def test_loi_trich_khong_phai_loi_goi():
    m = E.m_ops([call(loi="trich_dan_cat_phu_dinh"), call(loi="trich_dan_khong_khop"), call(loi="a1_json_loi")])
    assert m["loi"] == 1 and m["loai_loi"] == {"a1_json_loi": 1}
    assert E.m_trich([call(loi="trich_dan_cat_phu_dinh", trich=1, trich_bo=1)])["lan_goi_co_loi_trich"] == 1
