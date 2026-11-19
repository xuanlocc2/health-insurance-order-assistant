"""Buổi đo Before/After: mỗi bác sĩ làm 2 bộ ca, một bộ tự tra trước, một bộ dùng công cụ sau.
Ca đo và đáp án nằm ở data/do-luong/bo-ca.yaml; đáp án chỉ dùng để chấm khi xuất kết quả, không gửi xuống trình duyệt.
Cách đo giải thích cho bác sĩ: E:/VinMec/00_Dieu_Phoi/CACH_DO_BEFORE_AFTER.md"""
import functools
from pathlib import Path

import yaml

BO_CA_PATH = Path(__file__).resolve().parent.parent / "data" / "do-luong" / "bo-ca.yaml"
# tài khoản: (bộ tự tra, bộ dùng công cụ). bs05 là BS Trung duyệt đáp án, không tính vào số đo.
PHAN_CONG = {"bs01": ("A", "B"), "bs02": ("B", "A"), "bs03": ("A", "B"), "bs04": ("B", "A")}


@functools.lru_cache(maxsize=4)
def _doc(path, _sua_luc):
    return (yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}).get("bo") or {}


def bo_ca():
    return _doc(BO_CA_PATH, BO_CA_PATH.stat().st_mtime_ns) if BO_CA_PATH.exists() else {}


def lich(tai_khoan):
    """Thứ tự làm của một tài khoản: hết lượt tự tra rồi mới đến lượt dùng công cụ."""
    if tai_khoan not in PHAN_CONG:
        return []
    bo = bo_ca()
    tu_tra, cong_cu = PHAN_CONG[tai_khoan]
    muc = [(b, c, "tu_tra") for b in [tu_tra] for c in bo.get(b) or []] + \
        [(b, c, "cong_cu") for b in [cong_cu] for c in bo.get(b) or []]
    return [{"bo": b, "ca": c, "che_do": che_do, "thu_tu": i} for i, (b, c, che_do) in enumerate(muc, 1)]


def la_luot_do(luot_kham):
    return any("LK-" + c["id"] == luot_kham for ds in bo_ca().values() for c in ds or [])


def dap_an(ca_id):
    """Đáp án theo tên dịch vụ của một ca đo."""
    for ds in bo_ca().values():
        for c in ds or []:
            if c["id"] == ca_id:
                return {d["ten"]: d.get("dap_an") for d in c["chi_dinh"]}
    return {}
