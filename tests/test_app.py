import json

import pytest
from fastapi.testclient import TestClient

from src import app as app_mod

LUOT = {"luot_kham": "LK-T", "benh_nhan": {"tuoi_thang": 24}, "icd": [],
        "sinh_hieu": {}, "phieu_kham": "Ho", "chi_dinh": [{"ma": None, "ten": "CRP"}]}
DAU_VAO = {"tuoi": {"tuoi_thang": 24}, "the": None, "icd": [], "sinh_hieu": {}, "lich_su_da_dung": []}
F13 = {"thoi_gian", "luot_kham", "kiem_tra_id", "thu_tu", "ma", "ten", "trang_thai", "o_bhyt_goi_y",
       "bac_si_chon", "ly_do_bac_si", "checklist", "can_cu", "phien_ban_rule", "dau_vao"}


def dong(thu_tu=1, trang_thai="Phù hợp quy tắc BHYT", goi_y="tich", chon="tich", **kw):
    return {"thu_tu": thu_tu, "ma": "m", "ten": f"d{thu_tu}", "trang_thai": trang_thai, "o_bhyt_goi_y": goi_y,
            "bac_si_chon": chon, "ly_do_bac_si": None, "checklist": [], "can_cu": [], "phien_ban_rule": "v", **kw}


def confirm_body(*rows, **kw):
    return {"luot_kham": "LK-T", "dau_vao": DAU_VAO, "dong": list(rows), **kw}


@pytest.fixture
def client(tmp_path, monkeypatch):
    calls = []

    def fake_check(luot, rules, a1):
        calls.append((luot, rules, a1))
        return {"phien_ban_rule": "fake", "a1": {"goi": False, "loi": "a1_tat", "ms": 0},
                "dong": [{"thu_tu": 1, "ten": r["ten"], "trang_thai": "Cần xem lại"} for r in luot["chi_dinh"]]}

    monkeypatch.setattr(app_mod, "LOG_PATH", tmp_path / "x" / "log.jsonl")
    monkeypatch.setitem(app_mod.state, "check", fake_check)
    monkeypatch.setitem(app_mod.state, "rules", type("R", (), {"phien_ban_rule": "fake"})())
    monkeypatch.setitem(app_mod.state, "a1_mode", "off")
    monkeypatch.setitem(app_mod.state, "a1", None)
    monkeypatch.setitem(app_mod.state, "model", None)
    monkeypatch.setitem(app_mod.state, "reasoning_effort", None)
    monkeypatch.setitem(app_mod.state, "lq", None)
    # không dùng "with": bỏ qua lifespan (rules/engine thật có thể chưa có)
    c = TestClient(app_mod.app, base_url="http://127.0.0.1")
    c.calls = calls
    return c


def logged():
    return [json.loads(x) for x in app_mod.LOG_PATH.read_text(encoding="utf-8").splitlines()]


def test_health(client):
    assert client.get("/health").json() == {"phien_ban_rule": "fake", "a1_mode": "off", "model": None,
                                            "reasoning_effort": None}


def test_foreign_host_rejected(client):
    # chống DNS rebinding: trang lạ trỏ tên miền về 127.0.0.1 không gọi được /check (tốn khóa OpenAI) hay ghi log
    assert client.post("/check", json=LUOT, headers={"host": "evil.example"}).status_code == 400


def test_cases_strip_and_defaults(client):
    cs = client.get("/cases").json()
    assert len(cs) >= 8
    assert all(not {"ky_vong", "he_chi_rule", "a1_gia_lap"} & c.keys() for c in cs)
    assert all(c["luot_kham"] and c["ngay_kham"] and c["benh_nhan"]["the"] for c in cs)


def test_danh_muc(client, monkeypatch):
    r = type("R", (), {"danh_muc": [{"ma": "23.0228.1483", "ten": "Định lượng CRP", "bi_danh": ["CRP"], "bhyt": "co"}]})()
    monkeypatch.setitem(app_mod.state, "rules", r)
    assert client.get("/danh-muc").json() == [{"ma": "23.0228.1483", "ten": "Định lượng CRP", "bi_danh": ["CRP"]}]


def test_icd(client):
    ds = client.get("/icd").json()
    assert len(ds) > 15000 and {"ma": "J18.9", "ten": "Viêm phổi, không xác định"} in ds


def test_gia_dinh(client):
    g = client.get("/gia-dinh").json()
    assert len(g) >= 20 and g[0]["ma"] == "M-01" and all(x["cach_hieu"] and "**" not in x["tra_loi"] for x in g)


def test_check_passthrough(client):
    j = client.post("/check", json=LUOT).json()
    assert j["phien_ban_rule"] == "fake" and j["dong"][0]["ten"] == "CRP"
    assert client.calls[0][0]["luot_kham"] == "LK-T"


def test_check_luu_y_ho_so_chi_dong_danh_muc(client, monkeypatch):
    nhan = []

    def lq(req):
        nhan.append(req)
        return {1: {"ket_qua": "chua_thay_ly_do", "trich_dan": None}, 2: {"ket_qua": "chua_thay_ly_do", "trich_dan": None}}

    def fake_check(luot, rules, a1):
        return {"dong": [{"thu_tu": 1, "ma_ly_do": "danh_muc", "trang_thai": "Phù hợp quy tắc BHYT", "o_bhyt_goi_y": "tich"},
                         {"thu_tu": 2, "ma_ly_do": "dieu_kien_dat", "trang_thai": "Đủ căn cứ", "o_bhyt_goi_y": "tich"}]}
    monkeypatch.setitem(app_mod.state, "check", fake_check)
    monkeypatch.setitem(app_mod.state, "lq", lq)
    monkeypatch.setitem(app_mod.state, "a1_mode", "live")
    body = {**LUOT, "icd": ["J18.9"], "chi_dinh": [{"ma": None, "ten": "PT"}, {"ma": None, "ten": "CRP"}]}
    d = client.post("/check", json=body).json()["dong"]
    assert d[0]["luu_y_ho_so"] == {"ket_qua": "chua_thay_ly_do", "trich_dan": None}
    assert d[0]["trang_thai"] == "Phù hợp quy tắc BHYT" and d[0]["o_bhyt_goi_y"] == "tich"  # chỉ là lưu ý
    assert d[1]["luu_y_ho_so"] is None  # dòng có điều kiện: đã có quy tắc, không thêm lưu ý AI
    assert nhan == [{"dich_vu": ["PT", "CRP"], "phieu_kham": "Ho",
                     "icd": [{"ma": "J18.9", "ten": "Viêm phổi, không xác định"}]}]


@pytest.mark.parametrize("bad", [
    {}, {**LUOT, "chi_dinh": []}, {**LUOT, "chi_dinh": [{"ma": "x"}]},
    {**LUOT, "icd": "J18"}, {**LUOT, "icd": [1]},
    {**LUOT, "chi_dinh": [{"ma": ["x"], "ten": "CRP"}]},
    {**LUOT, "ngay_kham": "12/11/2026"},
    {**LUOT, "benh_nhan": {"tuoi_thang": "24"}},
    {**LUOT, "benh_nhan": {"tuoi_thang": 24, "the": {"han_den": "hôm qua"}}},
    {**LUOT, "sinh_hieu": {"nhiet_do": "38,5"}},
    {**LUOT, "lich_su": [{"ma": "x", "ngay_cach": "1"}]},
    {**LUOT, "chi_dinh": [{"ma": None, "ten": "CRP"}] * 51},
])
def test_check_bad_body_422(client, bad):
    r = client.post("/check", json=bad)
    assert r.status_code == 422 and isinstance(r.json()["detail"], str)
    assert not client.calls


def test_check_not_object_422(client):
    assert client.post("/check", json=[1]).status_code == 422


def test_confirm_writes_jsonl_with_all_f13_fields(client):
    body = confirm_body(*[dong(i) for i in (1, 2, 3)])
    assert client.post("/confirm", json=body).json() == {"ghi": 3}
    assert client.post("/confirm", json=body).json() == {"ghi": 3}  # chỉ ghi thêm
    rows = logged()
    assert len(rows) == 6
    assert all(F13 <= r.keys() for r in rows)
    assert rows[0]["luot_kham"] == "LK-T" and rows[0]["thu_tu"] == 1 and rows[0]["dau_vao"] == DAU_VAO


def test_confirm_row_cannot_override_server_fields(client):
    row = dong(1, thoi_gian="1999-01-01", luot_kham="LK-GIA", kiem_tra_id="gia", dau_vao={})
    client.post("/confirm", json=confirm_body(row))
    r = logged()[0]
    assert r["thoi_gian"] != "1999-01-01" and r["luot_kham"] == "LK-T" and r["kiem_tra_id"] is None
    assert r["dau_vao"] == DAU_VAO


@pytest.mark.parametrize("row,expect", [
    # F-12: bỏ tích dòng gợi ý "tich" → cần lý do; không có thì vẫn ghi (không chặn), loai = null
    (dong(1, chon="khong_tich"), {"loai": None, "ghi_chu": None}),
    # tích dòng Không được chi trả → cần lý do
    (dong(1, "Không được chi trả", "trong", "tich"), {"loai": None, "ghi_chu": None}),
    (dong(1, "Không được chi trả", "trong", "tich", ly_do_bac_si={"loai": "nguoi_nha_yeu_cau"}),
     {"loai": "nguoi_nha_yeu_cau", "ghi_chu": None}),
    # Cần xem lại (gợi ý null): chọn gì cũng không cần lý do
    (dong(1, "Cần xem lại", None, "tich"), None),
    (dong(1, "Cần xem lại", None, "khong_tich"), None),
    # giữ đúng gợi ý → không cần lý do
    (dong(1), None),
    (dong(1, "Không được chi trả", "trong", "khong_tich"), None),
])
def test_confirm_ly_do_bac_si_rules(client, row, expect):
    assert client.post("/confirm", json=confirm_body(row)).status_code == 200
    assert logged()[0]["ly_do_bac_si"] == expect


@pytest.mark.parametrize("body", [
    confirm_body(dong(1, chon="?")),
    confirm_body({k: v for k, v in dong(1).items() if k != "checklist"}),          # thiếu trường F-13
    confirm_body(dong(1, chon="khong_tich", ly_do_bac_si={"loai": "tuy_y"})),       # lý do ngoài danh sách
    confirm_body(dong(1, o_bhyt_goi_y="co")),
    confirm_body(dong(1), dau_vao={"tuoi": 1}),                                     # dau_vao thiếu khóa §9
    confirm_body(dong(1), kiem_tra_id=1),
    confirm_body(),
])
def test_confirm_bad_422(client, body):
    r = client.post("/confirm", json=body)
    assert r.status_code == 422 and isinstance(r.json()["detail"], str)
    assert not app_mod.LOG_PATH.exists()


def test_stub_a1_follows_subset_of_chi_dinh(monkeypatch):
    # bác sĩ bỏ dòng 1 của DEMO-01 → CRP thành thu_tu 1; stub phải vẫn trả lời đúng dòng CRP
    monkeypatch.setitem(app_mod.state, "a1_mode", "stub")
    case = next(c for c in app_mod._demo_cases() if c["id"] == "DEMO-01")
    luot = {**case, "chi_dinh": case["chi_dinh"][1:]}
    a1 = app_mod._a1_for(luot)
    res = a1({"phieu_kham": case["phieu_kham"], "cau_hoi": [{"khoa": "1:V3", "mo_ta": "", "cau_hoi": ""}],
              "so_lieu": []})
    assert res["ve"] == [{"khoa": "1:V3", "ket_qua": "dat", "trich_dan": "Phổi ran ẩm nhỏ hạt đáy phổi phải",
                          "trich_them": [], "trich_lien_quan": []}]


def test_load_env_bom_and_no_override(tmp_path, monkeypatch):
    p = tmp_path / ".env"
    p.write_text("﻿OPENAI_API_KEY=sk-test\nA1_MODE=stub\nOPENAI_MODEL=\n", encoding="utf-8")
    for k in ("OPENAI_API_KEY", "OPENAI_MODEL"):
        monkeypatch.delenv(k, raising=False)
    monkeypatch.setenv("A1_MODE", "off")
    app_mod.load_env(p)
    import os
    assert os.environ["OPENAI_API_KEY"] == "sk-test"
    assert os.environ["A1_MODE"] == "off"  # biến môi trường thắng .env
    assert "OPENAI_MODEL" not in os.environ


def test_index(client):
    r = client.get("/")
    assert r.status_code == 200 and "Kiểm tra BHYT" in r.text


def test_a1_nho_chi_goi_khi_bam_va_khong_goi_lai(client):
    goi = []

    def a1(req):
        goi.append(1)
        return {"ve": [{"khoa": q["khoa"], "ket_qua": "dat", "trich_dan": "Ho", "trich_lien_quan": []}
                       for q in req["cau_hoi"]], "so_lieu": [], "loi": None}

    def req(tt, pk="Ho  sốt"):
        return {"phieu_kham": pk, "cau_hoi": [{"khoa": f"{tt}:V1", "mo_ta": "m", "cau_hoi": "c"}],
                "so_lieu": [{"truong": "mach", "don_vi": None}]}

    app_mod._NHO.clear()
    r = app_mod._a1_nho(a1, False)(req(1))  # rule tự chạy lại: không gọi A1, báo chưa đọc
    assert not goi and r["loi"] == "chua_doc" and r["ve"][0]["chua_doc"]
    r = app_mod._a1_nho(a1, True)(req(1))  # bấm Kiểm tra BHYT
    assert len(goi) == 1 and r["ve"][0]["ket_qua"] == "dat" and r["loi"] is None
    r = app_mod._a1_nho(a1, False)(req(2, "Ho sốt"))  # xóa dòng phía trên (đổi thu_tu), phiếu như cũ: dùng lại
    assert len(goi) == 1 and r["ve"][0]["khoa"] == "2:V1" and r["ve"][0]["ket_qua"] == "dat" and r["loi"] is None
    hong = app_mod._a1_nho(lambda q: {"ve": [], "so_lieu": [], "loi": "a1_loi_Timeout"}, True)
    n = len(app_mod._NHO)
    assert hong(req(1, "khác"))["loi"] == "a1_loi_Timeout" and len(app_mod._NHO) == n  # gọi hỏng thì không nhớ
    assert isinstance(client.post("/check", json=LUOT).json()["kiem_tra_id"], str)
    app_mod._NHO.clear()
