"""Ẩn thông tin định danh trong phiếu khám trước khi gửi OpenAI. Hai chiều đều phải đúng:
xóa được tên/SĐT/số thẻ/giấy tờ/email/ngày sinh/địa chỉ, và KHÔNG đụng số liệu lâm sàng (A1 trích số từ đây)."""
import glob

import pytest
import yaml

from src.an_danh import an_danh

LAM_SANG = ("Sốt 3 ngày, nhiệt độ 38,5°C lúc 08:30 ngày 12/11/2026, đo lại 38.5. Mạch 150 l/p, nhịp thở 46 l/p, "
            "SpO2 97%, HA 90/60. CRP 25 mg/L, PCT 0.5 ng/mL, WBC 15.2 G/L, Hb 112 g/L, TC 350 G/L. "
            "Ran ẩm đáy phổi phải. TD viêm phổi J18.9, chưa loại trừ Kawasaki M30.3. Chỉ định 02.0085.1778, "
            "23.0228.1483. Bé tỉnh, Họng đỏ, Amidan sưng. Cân nặng 12,5 kg, chiều cao 85 cm. Ngày 05.11.2026 sốt "
            "39 40 38, PCT 0.5 0.6 0.7 0.8 0.9. Lý do khám: ho. Cao huyết áp: không. Dương tính cúm A. "
            "Mẹ cho uống Hapacol 150 mg. Tiền sử: sinh mổ 38 tuần, 3,2 kg. Anh trai bị cúm. BHYT 100%.")


def test_khong_dong_noi_dung_lam_sang():
    assert an_danh(LAM_SANG) == LAM_SANG


def test_khong_dong_phieu_kham_mau():
    # phiếu khám trong ca thử/eval là dữ liệu giả không có định danh: ẩn danh không được đổi kết quả eval
    for f in glob.glob("data/test-cases/*.yaml") + glob.glob("data/eval/*.yaml"):
        for ca in yaml.safe_load(open(f, encoding="utf-8")) or []:
            pk = ca.get("phieu_kham") if isinstance(ca, dict) else None
            if isinstance(pk, str):
                assert an_danh(pk) == pk, f"{f} {ca.get('id')}: {an_danh(pk)}"


@pytest.mark.parametrize("goc, mat", [
    ("SĐT mẹ 0912 345 678.", "0912 345 678"),
    ("ĐT: 0912.345.678", "0912.345.678"),
    ("gọi +84 912 345 678 khi cần", "912 345 678"),
    ("liên hệ 0912345678", "0912345678"),
    ("bố 091 234 5678", "091 234 5678"),
    ("CCCD 001203004567", "001203004567"),
    ("Thẻ TE1010123456789 còn hạn", "TE1010123456789"),
    ("Thẻ TE 1 01 0123456789", "0123456789"),
    ("email me.be@gmail.com", "me.be@gmail.com"),
    ("Họ tên: Nguyễn Văn An, 2 tuổi", "Nguyễn Văn An"),
    ("Họ tên: Lê Thị B", "Lê Thị B"),
    ("Bé Minh Anh 2 tuổi, sốt", "Minh Anh"),
    ("mẹ là chị Lan đưa đi khám", "Lan"),
    ("Tên: Khôi", "Khôi"),
    ("sinh ngày 03/04/2024", "03/04/2024"),
    ("Ngày sinh: 3-4-2024", "3-4-2024"),
    ("PID: VM123456", "VM123456"),
    ("mã BN 21345678", "21345678"),
    ("Địa chỉ: 458 Minh Khai, Hai Bà Trưng. Sốt 2 ngày", "458 Minh Khai"),
])
def test_xoa_thong_tin_dinh_danh(goc, mat):
    ra = an_danh(goc)
    assert mat not in ra and "[" in ra, ra


def test_giu_phan_lam_sang_quanh_cho_bi_xoa():
    ra = an_danh("Địa chỉ: 458 Minh Khai. Sốt 38,5°C, SĐT mẹ 0912345678, ran ẩm phổi phải")
    assert "Sốt 38,5°C" in ra and "ran ẩm phổi phải" in ra
