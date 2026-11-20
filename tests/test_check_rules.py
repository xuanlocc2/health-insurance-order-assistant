"""check_rules.py chạy trong pytest. Engine gặp chỗ rule lạ (gõ sai loại kiểm, khóa lạ) chỉ lặng lẽ trả Cần xem lại,
nên lỗi dữ liệu rule phải bị chặn ở đây, trước khi lên app. Quan trọng khi danh mục và điều kiện tăng lên."""
import copy
import importlib.util
from pathlib import Path

import pytest
import yaml

DIR = Path(__file__).resolve().parent.parent / "data" / "rules"
_spec = importlib.util.spec_from_file_location("check_rules", DIR / "check_rules.py")
cr = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cr)
GOC = {t: yaml.safe_load((DIR / f"{t}.yaml").read_text(encoding="utf-8")) for t in ("danh-muc", "dieu-kien", "tham-so")}
CRP = "23.0228.1483"


def kiem(sua=None):
    d = copy.deepcopy(GOC)
    if sua:
        sua(d)
    cr.kiem(d["danh-muc"]["dich_vu"], d["dieu-kien"], d["tham-so"])


def _v1(d):  # CRP nhánh trẻ em, vế nhiệt độ: hoac gồm 2 so_sanh
    return d["dieu-kien"][CRP]["nhanh"][0]["ve"][0]["hoac"][0]


def test_du_lieu_that_hop_le():
    cr.main()


@pytest.mark.parametrize("sua", [
    lambda d: _v1(d).update(loai="so_sanhh"),                                   # gõ sai loại kiểm
    lambda d: _v1(d).update(truong="nhiet"),                                    # trường sinh hiệu lạ
    lambda d: _v1(d).update(toan_tu="=>"),                                      # toán tử lạ
    lambda d: _v1(d).pop("gia_tri"),                                            # thiếu ngưỡng
    lambda d: d["dieu-kien"][CRP]["nhanh"][0]["ap_dung"].update(tuoi_nam=[0, 16]),  # khóa áp dụng lạ
    lambda d: next(e for e in d["danh-muc"]["dich_vu"] if e["bhyt"] == "xac_minh")
    .setdefault("bi_danh", []).append("CTM"),                                   # tên trùng dòng khác kết luận
], ids=["loai", "truong", "toan_tu", "thieu_khoa", "ap_dung", "trung_ten"])
def test_du_lieu_hong_bi_chan(sua):
    with pytest.raises(AssertionError):
        kiem(sua)
