"""Buổi đo Before/After: phân ca theo tài khoản, thứ tự làm, khóa kết quả, ẩn đáp án và xuất CSV."""
import csv

import pytest
import yaml
from fastapi.testclient import TestClient

from src import app as app_mod
from src import do_luong, luu_tru, xuat_ket_qua

MK = "mat-khau-gia"


def ca(id_):
    return {"id": id_, "ten": f"Tên lộ đáp án {id_}", "benh_nhan": {"tuoi_thang": 24}, "sinh_hieu": {"nhiet_do": 39},
            "icd": ["J18.9"], "phieu_kham": "Sốt 2 ngày", "chi_dinh": [
                {"ma": "23.0228.1483", "ten": "Định lượng CRP", "dap_an": "tich"},
                {"ma": "23.0130.1549", "ten": "Định lượng Pro-calcitonin [Máu]", "dap_an": "khong_tich"}]}


BO = {"bo": {"A": [ca("DO-A1"), ca("DO-A2")], "B": [ca("DO-B1"), ca("DO-B2")]}}


@pytest.fixture(autouse=True)
def moi_truong(tmp_path, monkeypatch):
    p = tmp_path / "bo-ca.yaml"
    p.write_text(yaml.safe_dump(BO, allow_unicode=True), encoding="utf-8")
    monkeypatch.setattr(do_luong, "BO_CA_PATH", p)
    monkeypatch.setenv("MAT_KHAU_CHUNG", MK)
    monkeypatch.setenv("KHOA_PHIEN", "k" * 40)
    monkeypatch.setitem(app_mod.state, "kho", luu_tru.KhoFile(tmp_path / "ca.yaml", tmp_path / "log.jsonl"))
    monkeypatch.setitem(app_mod.state, "check", lambda luot, rules, a1: {"dong": []})
    monkeypatch.setitem(app_mod.state, "rules", type("R", (), {"phien_ban_rule": "fake"})())
    monkeypatch.setitem(app_mod.state, "a1_mode", "off")
    monkeypatch.setitem(app_mod.state, "a1", None)
    monkeypatch.setitem(app_mod.state, "lq", None)


def bs(tk="bs01"):
    c = TestClient(app_mod.app, base_url="http://127.0.0.1")
    assert c.post("/dang-nhap", json={"tai_khoan": tk, "mat_khau": MK, "cam_ket": True}).status_code == 200
    return c


def dong(chon=("tich", "khong_tich")):
    return [{"ma": g["ma"], "ten": g["ten"], "bac_si_chon": x} for g, x in zip(ca("x")["chi_dinh"], chon)]


def luu(c, ca_id, kiem_tra_id=None, d=None):
    return c.post(f"/do-luong/{ca_id}", json={"kiem_tra_id": kiem_tra_id, "dong": dong() if d is None else d})


def luot(ca_id):
    return {"luot_kham": "LK-" + ca_id, "benh_nhan": {"tuoi_thang": 24}, "icd": [], "sinh_hieu": {}, "phieu_kham": "Sốt",
            "chi_dinh": [{"ma": None, "ten": "CRP"}]}


@pytest.mark.parametrize("tk,thu_tu", [
    ("bs01", [("DO-A1", "tu_tra"), ("DO-A2", "tu_tra"), ("DO-B1", "cong_cu"), ("DO-B2", "cong_cu")]),
    ("bs03", [("DO-A1", "tu_tra"), ("DO-A2", "tu_tra"), ("DO-B1", "cong_cu"), ("DO-B2", "cong_cu")]),
    ("bs02", [("DO-B1", "tu_tra"), ("DO-B2", "tu_tra"), ("DO-A1", "cong_cu"), ("DO-A2", "cong_cu")]),
    ("bs04", [("DO-B1", "tu_tra"), ("DO-B2", "tu_tra"), ("DO-A1", "cong_cu"), ("DO-A2", "cong_cu")]),
])
def test_phan_ca_dao_bo_va_tu_tra_truoc(tk, thu_tu):
    assert [(m["ca"]["id"], m["che_do"]) for m in do_luong.lich(tk)] == thu_tu
    assert [m["thu_tu"] for m in do_luong.lich(tk)] == [1, 2, 3, 4]


def test_bs05_khong_co_lich_do():
    assert bs("bs05").get("/do-luong").json() == {"co_phan_cong": False, "tong": 0, "da_xong": 0, "hien_tai": None}


def test_chua_co_file_bo_ca_thi_khong_co_buoi_do(tmp_path, monkeypatch):
    monkeypatch.setattr(do_luong, "BO_CA_PATH", tmp_path / "chua-co.yaml")
    assert bs("bs01").get("/do-luong").json()["co_phan_cong"] is False


def test_chi_tra_ca_hien_tai_va_khong_lo_dap_an():
    r = bs("bs01").get("/do-luong")
    j = r.json()
    assert j["co_phan_cong"] is True and j["tong"] == 4 and j["da_xong"] == 0
    h = j["hien_tai"]
    assert h["id"] == "DO-A1" and h["che_do"] == "tu_tra" and h["thu_tu"] == 1 and h["luot_kham"] == "LK-DO-A1"
    assert h["ten"] == "Ca đo 1" and h["benh_nhan"]["the"] and h["lich_su"] == []
    assert "dap_an" not in r.text and "Tên lộ đáp án" not in r.text and "DO-A2" not in r.text and "DO-B1" not in r.text


def test_ca_do_khong_nam_trong_danh_sach_ca_thuong():
    assert not any(c["id"].startswith("DO-") for c in bs("bs01").get("/cases").json())


def test_lam_het_theo_thu_tu_roi_hoan_thanh():
    c = bs("bs01")
    assert luu(c, "DO-A1").json()["hien_tai"]["id"] == "DO-A2"
    assert luu(c, "DO-A2").json()["hien_tai"]["che_do"] == "cong_cu"
    assert luu(c, "DO-B1", "kt1").json()["da_xong"] == 3
    j = luu(c, "DO-B2", "kt2").json()
    assert j["hien_tai"] is None and j["da_xong"] == 4


def test_ket_qua_da_luu_bi_khoa():
    c = bs("bs01")
    assert luu(c, "DO-A1").status_code == 200
    r = luu(c, "DO-A1", d=dong(("khong_tich", "tich")))
    assert r.status_code == 409 and isinstance(r.json()["detail"], str)
    ket = app_mod.state["kho"].doc_ket_qua_do("bs01")
    assert len(ket) == 1 and ket[0]["dong"][0]["bac_si_chon"] == "tich"


def test_khong_duoc_lam_vuot_thu_tu():
    assert luu(bs("bs01"), "DO-A2").status_code == 409
    assert luu(bs("bs01"), "DO-B1", "kt").status_code == 409


def test_tai_khoan_khac_khong_anh_huong_nhau():
    a, b = bs("bs01"), bs("bs03")
    assert luu(a, "DO-A1").status_code == 200
    assert b.get("/do-luong").json()["hien_tai"]["id"] == "DO-A1"
    assert bs("bs05").post("/do-luong/DO-A1", json={"dong": dong()}).status_code == 409


@pytest.mark.parametrize("d", [[], dong()[:1], dong() + dong()[:1], "x", [1, 2], [{"ten": "Khác", "bac_si_chon": "tich"}, dong()[1]],
                               dong(("co", "khong_tich"))])
def test_dong_sai_bi_tu_choi_va_khong_khoa_ca(d):
    c = bs("bs01")
    assert luu(c, "DO-A1", d=d).status_code == 422
    assert luu(c, "DO-A1").status_code == 200


def test_luot_dung_cong_cu_phai_da_kiem_tra():
    c = bs("bs01")
    luu(c, "DO-A1"), luu(c, "DO-A2")
    assert luu(c, "DO-B1").status_code == 422
    assert luu(c, "DO-B1", "kt1").status_code == 200


def test_luot_tu_tra_khong_goi_duoc_cong_cu():
    c = bs("bs01")
    for doc_ai in (True, False):
        r = c.post("/check", json={**luot("DO-A1"), "doc_ai": doc_ai})
        assert r.status_code == 403 and isinstance(r.json()["detail"], str)


def test_khong_xem_truoc_goi_y_ca_chua_den_luot():
    assert bs("bs01").post("/check", json=luot("DO-B1")).status_code == 403
    assert bs("bs05").post("/check", json=luot("DO-A1")).status_code == 403


def test_luot_dung_cong_cu_goi_duoc_kiem_tra_va_khoa_sau_khi_luu():
    c = bs("bs01")
    luu(c, "DO-A1"), luu(c, "DO-A2")
    assert c.post("/check", json=luot("DO-B1")).status_code == 200
    luu(c, "DO-B1", "kt1")
    assert c.post("/check", json=luot("DO-B1")).status_code == 403


def test_ca_thuong_van_kiem_tra_binh_thuong():
    assert bs("bs01").post("/check", json=luot("DEMO-01")).status_code == 200


def test_xuat_csv_cham_dung_sai_theo_dap_an(tmp_path):
    c = bs("bs01")
    luu(c, "DO-A1")
    luu(c, "DO-A2", d=dong(("khong_tich", "tich")))
    goi_y = [{**d, "trang_thai": "Cần xem lại", "o_bhyt_goi_y": None} for d in dong()]
    luu(c, "DO-B1", "kt1", d=goi_y)
    rows = xuat_ket_qua.tao_dong(app_mod.state["kho"].doc_ket_qua_do())
    assert len(rows) == 6
    assert [r["dung"] for r in rows] == ["dung", "dung", "sai", "sai", "dung", "dung"]
    r = rows[4]
    assert (r["tai_khoan"], r["thu_tu_lam"], r["bo"], r["che_do"], r["ca_id"]) == ("bs01", 3, "B", "cong_cu", "DO-B1")
    assert r["dap_an"] == "tich" and r["trang_thai_cong_cu"] == "Cần xem lại" and r["kiem_tra_id"] == "kt1"
    assert xuat_ket_qua.tom_tat(rows) == [
        {"tai_khoan": "bs01", "che_do": "tu_tra", "so_ca": 2, "so_dong": 4, "so_dong_sai": 2},
        {"tai_khoan": "bs01", "che_do": "cong_cu", "so_ca": 1, "so_dong": 2, "so_dong_sai": 0}]
    p = xuat_ket_qua.ghi_csv(rows, tmp_path / "kq.csv")
    assert p.read_bytes().startswith(b"\xef\xbb\xbf")  # Excel đọc đúng tiếng Việt
    with p.open(encoding="utf-8-sig", newline="") as f:
        doc = list(csv.DictReader(f))
    assert len(doc) == 6 and doc[0]["ten"] == "Định lượng CRP"


def test_chua_co_dap_an_thi_khong_cham(tmp_path, monkeypatch):
    bo = {"bo": {"A": [{**ca("DO-A1"), "chi_dinh": [{"ma": "m", "ten": "Định lượng CRP"}]}], "B": [ca("DO-B1")]}}
    p = tmp_path / "bo2.yaml"
    p.write_text(yaml.safe_dump(bo, allow_unicode=True), encoding="utf-8")
    monkeypatch.setattr(do_luong, "BO_CA_PATH", p)
    c = bs("bs01")
    assert luu(c, "DO-A1", d=[{"ma": "m", "ten": "Định lượng CRP", "bac_si_chon": "tich"}]).status_code == 200
    r = xuat_ket_qua.tao_dong(app_mod.state["kho"].doc_ket_qua_do())[0]
    assert r["dap_an"] == "" and r["dung"] == ""
