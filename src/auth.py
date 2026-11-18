"""Đăng nhập cho đợt thử: 5 tài khoản bs01–bs05 dùng chung MAT_KHAU_CHUNG, phiên lưu trong cookie có chữ ký.
Thiếu MAT_KHAU_CHUNG hoặc KHOA_PHIEN thì không ai đăng nhập được: cấu hình sai không được làm lộ app."""
import hashlib
import hmac
import os
import time

TAI_KHOAN = ("bs01", "bs02", "bs03", "bs04", "bs05")
COOKIE = "phien"
THOI_HAN_S = 12 * 3600  # đủ một ngày làm việc


def da_cau_hinh():
    return bool(os.environ.get("MAT_KHAU_CHUNG") and os.environ.get("KHOA_PHIEN"))


def _bang(a, b):
    return hmac.compare_digest(a.encode("utf-8"), b.encode("utf-8"))


def dung_mat_khau(tai_khoan, mat_khau):
    return da_cau_hinh() and tai_khoan in TAI_KHOAN and isinstance(mat_khau, str) \
        and _bang(mat_khau, os.environ["MAT_KHAU_CHUNG"])


def _ky(noi_dung):
    return hmac.new(os.environ["KHOA_PHIEN"].encode("utf-8"), noi_dung.encode("utf-8"), hashlib.sha256).hexdigest()


def tao_phien(tai_khoan):
    noi_dung = f"{tai_khoan}.{int(time.time()) + THOI_HAN_S}"
    return f"{noi_dung}.{_ky(noi_dung)}"


def doc_phien(token):
    """Trả tên tài khoản nếu phiên hợp lệ và còn hạn, ngược lại trả None."""
    if not token or not da_cau_hinh():
        return None
    phan = token.split(".")
    if len(phan) != 3:
        return None
    tai_khoan, het_han, chu_ky = phan
    if not _bang(chu_ky, _ky(f"{tai_khoan}.{het_han}")) or tai_khoan not in TAI_KHOAN:
        return None
    return tai_khoan if het_han.isdigit() and int(het_han) > time.time() else None
