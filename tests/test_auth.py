"""Đăng nhập, tách dữ liệu theo tài khoản và giới hạn lượt gọi AI."""
import pytest
from fastapi.testclient import TestClient

from src import app as app_mod
from src import auth, luu_tru

MK = "mat-khau-gia"
LUOT = {"luot_kham": "LK-T", "benh_nhan": {"tuoi_thang": 24}, "icd": [], "sinh_hieu": {}, "phieu_kham": "Ho",
        "chi_dinh": [{"ma": None, "ten": "CRP"}]}
CA = {"ten": "Ca giả", "benh_nhan": {"tuoi_thang": 24}, "chi_dinh": [], "phieu_kham": ""}


def khach():
    return TestClient(app_mod.app, base_url="http://127.0.0.1", follow_redirects=False)


def dang_nhap(tk="bs01", mk=MK, cam_ket=True, c=None):
    c = c or khach()
    c.dn = c.post("/dang-nhap", json={"tai_khoan": tk, "mat_khau": mk, "cam_ket": cam_ket})
    return c


@pytest.fixture(autouse=True)
def moi_truong(tmp_path, monkeypatch):
    monkeypatch.setenv("MAT_KHAU_CHUNG", MK)
    monkeypatch.setenv("KHOA_PHIEN", "k" * 40)
    monkeypatch.setitem(app_mod.state, "kho", luu_tru.KhoFile(tmp_path / "ca.yaml", tmp_path / "log.jsonl"))
    monkeypatch.setitem(app_mod.state, "check", lambda luot, rules, a1: {"dong": []})
    monkeypatch.setitem(app_mod.state, "rules", type("R", (), {"phien_ban_rule": "fake"})())
    monkeypatch.setitem(app_mod.state, "a1_mode", "off")
    monkeypatch.setitem(app_mod.state, "a1", None)
    monkeypatch.setitem(app_mod.state, "lq", None)


@pytest.mark.parametrize("cach,duong", [("get", "/cases"), ("get", "/health"), ("get", "/icd"), ("get", "/danh-muc"),
                                        ("get", "/gia-dinh"), ("get", "/toi"), ("post", "/check"), ("post", "/confirm"),
                                        ("put", "/cases/TU-A1"), ("delete", "/cases/TU-A1"), ("post", "/dang-xuat")])
def test_chua_dang_nhap_bi_chan_moi_api(cach, duong):
    r = getattr(khach(), cach)(duong)
    assert r.status_code == 401 and isinstance(r.json()["detail"], str)


def test_trang_chinh_chuyen_ve_dang_nhap():
    r = khach().get("/")
    assert r.status_code == 303 and r.headers["location"] == "/dang-nhap"


def test_trang_dang_nhap_mo_duoc_va_co_cam_ket():
    r = khach().get("/dang-nhap")
    assert r.status_code == 200 and "dữ liệu giả" in r.text and 'type="password"' in r.text


def test_trang_dang_nhap_bat_buoc_chon_tai_khoan():
    """Không chọn sẵn tài khoản đo (bs01): người duyệt quên đổi sang bs05 sẽ lỡ vào màn đo."""
    t = khach().get("/dang-nhap").text
    assert '<select id="tk" autocomplete="username" required>' in t
    assert '<option value="" selected disabled>' in t and "<option selected>bs0" not in t


def test_dang_nhap_dung_vao_duoc_app():
    c = dang_nhap("bs03")
    assert c.dn.status_code == 200 and c.dn.json() == {"tai_khoan": "bs03"}
    cookie = c.dn.headers["set-cookie"].lower()
    assert "httponly" in cookie and "samesite=lax" in cookie and "max-age=" in cookie
    assert c.get("/toi").json() == {"tai_khoan": "bs03"}
    assert c.get("/").status_code == 200
    assert c.get("/dang-nhap").status_code == 303  # đã đăng nhập thì vào thẳng app


def test_cookie_chi_secure_khi_chay_https():
    c = khach()
    r = c.post("/dang-nhap", json={"tai_khoan": "bs01", "mat_khau": MK, "cam_ket": True},
               headers={"x-forwarded-proto": "https"})
    assert "secure" in r.headers["set-cookie"].lower()
    assert "secure" not in dang_nhap().dn.headers["set-cookie"].lower()


@pytest.mark.parametrize("tk,mk,ma", [("bs01", "sai", 401), ("bs99", MK, 401), ("", MK, 401), ("bs01", None, 401),
                                      ("bs01", "mật khẩu sai", 401), (None, MK, 401)])
def test_dang_nhap_sai_bi_tu_choi(tk, mk, ma):
    c = dang_nhap(tk, mk)
    assert c.dn.status_code == ma and "set-cookie" not in c.dn.headers
    assert c.get("/cases").status_code == 401


@pytest.mark.parametrize("cam_ket", [False, None, "true", 1])
def test_phai_tick_cam_ket(cam_ket):
    c = dang_nhap(cam_ket=cam_ket)
    assert c.dn.status_code == 422 and "set-cookie" not in c.dn.headers


@pytest.mark.parametrize("thieu", ["MAT_KHAU_CHUNG", "KHOA_PHIEN"])
def test_thieu_cau_hinh_thi_khoa_app(monkeypatch, thieu):
    co = dang_nhap().cookies.get(auth.COOKIE)
    monkeypatch.delenv(thieu)
    c = dang_nhap()
    assert c.dn.status_code == 503 and "set-cookie" not in c.dn.headers
    if thieu == "KHOA_PHIEN":
        k = khach()
        k.cookies.set(auth.COOKIE, co)
        assert k.get("/cases").status_code == 401


@pytest.mark.parametrize("sua", [lambda t: t[:-1] + ("0" if t[-1] != "0" else "1"),
                                 lambda t: t.replace("bs01", "bs02", 1), lambda t: "bs01.9999999999.abc", lambda t: "rác",
                                 lambda t: "bs99." + t.split(".", 1)[1], lambda t: "bs01.xx." + t.rsplit(".", 1)[1]])
def test_phien_bi_sua_khong_dung_duoc(sua):
    t = auth.tao_phien("bs01")
    assert auth.doc_phien(t) == "bs01" and auth.doc_phien(sua(t)) is None


def test_phien_het_han(monkeypatch):
    t = auth.tao_phien("bs01")
    now = auth.time.time()
    monkeypatch.setattr(auth.time, "time", lambda: now + auth.THOI_HAN_S + 1)
    assert auth.doc_phien(t) is None


def test_dang_xuat():
    c = dang_nhap()
    assert c.post("/dang-xuat").status_code == 200
    assert c.get("/cases").status_code == 401


def test_host_la_van_bi_chan_truoc_dang_nhap():
    assert khach().get("/cases", headers={"host": "evil.example"}).status_code == 400


def test_ca_tu_tao_rieng_tung_tai_khoan_ca_mau_dung_chung():
    a, b = dang_nhap("bs01"), dang_nhap("bs02")
    assert a.put("/cases/TU-A1", json=CA).status_code == 200
    ids = lambda c: {x["id"] for x in c.get("/cases").json()}
    assert "TU-A1" in ids(a) and "TU-A1" not in ids(b)
    assert "DEMO-01" in ids(a) and "DEMO-01" in ids(b)
    assert b.delete("/cases/TU-A1").status_code == 404  # không xóa được ca của người khác
    assert "TU-A1" in ids(a)


def test_log_xac_nhan_ghi_dung_tai_khoan():
    c = dang_nhap("bs04")
    dong = {"thu_tu": 1, "ma": "m", "ten": "d", "trang_thai": "Cần xem lại", "o_bhyt_goi_y": None, "bac_si_chon": "tich",
            "checklist": [], "can_cu": [], "phien_ban_rule": "v"}
    body = {"luot_kham": "LK-T", "dau_vao": {k: None for k in app_mod.DAU_VAO}, "dong": [dong]}
    assert c.post("/confirm", json=body).status_code == 200
    kho = app_mod.state["kho"]
    assert len(kho.doc_xac_nhan("bs04")) == 1 and kho.doc_xac_nhan("bs01") == []


def test_gioi_han_luot_ai_moi_ngay(monkeypatch):
    monkeypatch.setattr(app_mod, "GIOI_HAN_AI_NGAY", 2)
    monkeypatch.setattr(app_mod, "_hom_nay", lambda: "2026-11-23")
    a = dang_nhap("bs01")
    assert [a.post("/check", json=LUOT).status_code for _ in range(2)] == [200, 200]
    r = a.post("/check", json=LUOT)
    assert r.status_code == 429 and "2 lượt" in r.json()["detail"]
    assert a.post("/check", json={**LUOT, "doc_ai": False}).status_code == 200  # chạy lại quy tắc không tốn lượt AI
    assert dang_nhap("bs02").post("/check", json=LUOT).status_code == 200       # tài khoản khác không bị ảnh hưởng
    monkeypatch.setattr(app_mod, "_hom_nay", lambda: "2026-11-24")
    assert a.post("/check", json=LUOT).status_code == 200                       # sang ngày mới được tính lại


def test_body_sai_khong_tinh_luot(monkeypatch):
    monkeypatch.setattr(app_mod, "GIOI_HAN_AI_NGAY", 1)
    a = dang_nhap()
    assert a.post("/check", json={}).status_code == 422
    assert a.post("/check", json=LUOT).status_code == 200


def test_ngay_tinh_theo_gio_viet_nam(monkeypatch):
    class GioGia(app_mod.datetime):
        @classmethod
        def now(cls, tz=None):
            return app_mod.datetime(2026, 11, 22, 18, 0, tzinfo=app_mod.timezone.utc).astimezone(tz)
    monkeypatch.setattr(app_mod, "datetime", GioGia)
    assert app_mod._hom_nay() == "2026-11-23"  # 18h UTC là 1h sáng hôm sau ở Việt Nam
