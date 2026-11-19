"""Hợp đồng chung của nơi lưu trữ: file (máy cá nhân, test) và Neon (bản host) phải cư xử giống nhau.
Mặc định chỉ chạy với file. Chạy cả Neon thật: NEON_TEST=1 pytest tests/test_luu_tru.py (tự dọn dữ liệu thử)."""
import os
import uuid

import pytest

from src import app as app_mod
from src import luu_tru


@pytest.fixture(params=["file", "neon"])
def kho(request, tmp_path, monkeypatch):
    if request.param == "file":
        yield luu_tru.KhoFile(tmp_path / "ca.yaml", tmp_path / "logs" / "xac-nhan.jsonl")
        return
    if os.environ.get("NEON_TEST") != "1":
        pytest.skip("chỉ chạy với NEON_TEST=1")
    monkeypatch.delenv("DATABASE_URL", raising=False)
    app_mod.load_env()
    k = luu_tru.KhoNeon(os.environ["DATABASE_URL"])
    k.tao_bang()
    k.da_tao = []
    yield k
    nho = [luu_tru.bam_khoa((t, "ve", "mô tả", str(i))) for t in k.da_tao for i in range(3)]
    with k._ket_noi() as c:
        c.execute("DELETE FROM ca_tu_tao WHERE tai_khoan = ANY(%s)", (k.da_tao,))
        c.execute("DELETE FROM xac_nhan WHERE tai_khoan = ANY(%s)", (k.da_tao,))
        c.execute("DELETE FROM nho_a1 WHERE khoa = ANY(%s)", (nho,))
        c.execute("DELETE FROM luot_ai WHERE tai_khoan = ANY(%s)", (k.da_tao,))
        c.execute("DELETE FROM ket_qua_do WHERE tai_khoan = ANY(%s)", (k.da_tao,))


@pytest.fixture
def tk(kho):
    ten = ["thu-" + uuid.uuid4().hex[:10], "thu-" + uuid.uuid4().hex[:10]]
    if hasattr(kho, "da_tao"):
        kho.da_tao.extend(ten)
    return ten


def ca(id_="TU-A1", ten="Ca giả"):
    return {"id": id_, "ten": ten, "benh_nhan": {"tuoi_thang": 24}, "phieu_kham": "Sốt 2 ngày", "phieu_o": None}


def test_ca_tu_tao_tach_rieng_theo_tai_khoan(kho, tk):
    a, b = tk
    kho.luu_ca(a, ca(ten="Ca của A"))
    assert [c["ten"] for c in kho.ds_ca(a)] == ["Ca của A"]
    assert kho.ds_ca(b) == []
    kho.luu_ca(b, ca(ten="Ca của B"))  # cùng mã ca ở tài khoản khác không đè nhau
    assert [c["ten"] for c in kho.ds_ca(a)] == ["Ca của A"]
    assert [c["ten"] for c in kho.ds_ca(b)] == ["Ca của B"]
    assert kho.xoa_ca(a, "TU-A1") is True
    assert kho.ds_ca(a) == [] and len(kho.ds_ca(b)) == 1


def test_sua_ca_giu_thoi_diem_tao(kho, tk):
    a = tk[0]
    kho.luu_ca(a, ca())
    tao = kho.ds_ca(a)[0]["tao_luc"]
    kho.luu_ca(a, ca(ten="Tên mới"))
    ds = kho.ds_ca(a)
    assert len(ds) == 1 and ds[0]["ten"] == "Tên mới" and ds[0]["tao_luc"] == tao and ds[0]["sua_luc"] >= tao
    assert ds[0]["benh_nhan"] == {"tuoi_thang": 24} and ds[0]["phieu_o"] is None


def test_xoa_ca_khong_co_tra_false(kho, tk):
    assert kho.xoa_ca(tk[0], "TU-KHONG") is False


def test_xac_nhan_ghi_them_va_gan_tai_khoan(kho, tk):
    a, b = tk
    kho.ghi_xac_nhan(a, [{"luot_kham": "LK-1", "kiem_tra_id": "x1", "thu_tu": 1, "ten": "Định lượng CRP"},
                         {"luot_kham": "LK-1", "kiem_tra_id": "x1", "thu_tu": 2, "ten": "CTM"}])
    kho.ghi_xac_nhan(a, [{"luot_kham": "LK-2", "kiem_tra_id": None, "thu_tu": 1, "ten": "PCT"}])
    kho.ghi_xac_nhan(b, [{"luot_kham": "LK-3", "kiem_tra_id": None, "thu_tu": 1, "ten": "Khác"}])
    r = kho.doc_xac_nhan(a)
    assert [x["ten"] for x in r] == ["Định lượng CRP", "CTM", "PCT"] and {x["tai_khoan"] for x in r} == {a}


def test_nho_ai_doc_ghi_va_giu_gia_tri_rong(kho, tk):
    k1, k2, k3 = [(tk[0], "ve", "mô tả", str(i)) for i in range(3)]
    assert kho.doc_nho([k1, k2]) == {}
    kho.ghi_nho({k1: {"ket_qua": "dat", "trich_dan": "Sốt 39 độ"}, k2: None})
    assert kho.doc_nho([k1, k2, k3]) == {k1: {"ket_qua": "dat", "trich_dan": "Sốt 39 độ"}, k2: None}
    kho.ghi_nho({k1: {"ket_qua": "chua_thay"}})
    assert kho.doc_nho([k1])[k1] == {"ket_qua": "chua_thay"}
    assert kho.doc_nho([]) == {}
    kho.ghi_nho({})


def test_dem_luot_ai_theo_tai_khoan_va_ngay(kho, tk):
    a, b = tk
    assert [kho.tang_luot_ai(a, "2026-11-23") for _ in range(3)] == [1, 2, 3]
    assert kho.tang_luot_ai(b, "2026-11-23") == 1
    assert kho.tang_luot_ai(a, "2026-11-24") == 1


def test_ket_qua_do_chi_luu_mot_lan_moi_ca(kho, tk):
    a, b = tk
    ket = {"ca_id": "DO-A1", "bo": "A", "che_do": "tu_tra", "thu_tu": 1, "kiem_tra_id": None,
           "dong": [{"ma": "m", "ten": "Định lượng CRP", "bac_si_chon": "tich"}]}
    assert kho.luu_ket_qua_do(a, ket) is True
    assert kho.luu_ket_qua_do(a, {**ket, "dong": []}) is False  # kết quả đã lưu không bị ghi đè
    assert kho.luu_ket_qua_do(b, ket) is True                   # tài khoản khác làm cùng ca vẫn lưu được
    r = kho.doc_ket_qua_do(a)
    assert len(r) == 1 and r[0]["dong"][0]["ten"] == "Định lượng CRP" and r[0]["tai_khoan"] == a and r[0]["luu_luc"]
    assert {x["tai_khoan"] for x in kho.doc_ket_qua_do() if x["tai_khoan"] in tk} == {a, b}


def test_chon_kho_theo_database_url(tmp_path, monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "")
    assert isinstance(luu_tru.tao_kho(tmp_path / "c.yaml", tmp_path / "l.jsonl"), luu_tru.KhoFile)
    monkeypatch.setenv("DATABASE_URL", "postgresql://gia:gia@localhost/gia")
    assert isinstance(luu_tru.tao_kho(tmp_path / "c.yaml", tmp_path / "l.jsonl"), luu_tru.KhoNeon)
