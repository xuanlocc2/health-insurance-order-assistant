"""Nạp quy tắc từ data/rules/ (spec 09 mục 1–3, 11b).

Rules (SimpleNamespace):
  .danh_muc        [ {ma, ten, bi_danh[], bhyt, ...} ]
  .dieu_kien       { ma: {...} }   "@tham_so" đã giải; dict nào dùng tham số có thêm "_tham_so": {khóa: [tên]}
  .tham_so         { ten: {...} }  nguyên bản tham-so.yaml (giữ nguon / diem_mo_ho)
  .phien_ban_rule  sha1 cả thư mục
"""
import hashlib
from pathlib import Path
from types import SimpleNamespace as Rules

import yaml

from src.engine import chi_muc


def load_rules(dir="data/rules") -> Rules:
    p = Path(dir)
    doc = {ten: yaml.safe_load((p / f"{ten}.yaml").read_text(encoding="utf-8")) or {}
           for ten in ("danh-muc", "dieu-kien", "tham-so")}
    tham_so = doc["tham-so"]
    h = hashlib.sha1()
    for f in sorted(x for x in p.rglob("*") if x.is_file()):
        h.update(f.relative_to(p).as_posix().encode())
        h.update(f.read_bytes())
    dm = _danh_sach(doc["danh-muc"])
    return Rules(danh_muc=dm,
                 chi_muc=chi_muc(dm),  # tra mã/tên O(1): danh mục cả viện vài nghìn dòng
                 dieu_kien=_giai(doc["dieu-kien"], tham_so, []),
                 tham_so=tham_so,
                 phien_ban_rule=h.hexdigest())


def _danh_sach(d):
    """danh-muc.yaml: danh sách, hoặc một khóa bọc danh sách (vd dich_vu: [...])."""
    if isinstance(d, dict):
        lists = [v for v in d.values() if isinstance(v, list)]
        if len(lists) != 1:
            raise ValueError("danh-muc.yaml: cần một danh sách dịch vụ")
        d = lists[0]
    return d


def _giai(o, tham_so, refs):
    """Thay "@ten" bằng giá trị tham số; ghi tên tham số theo khóa vào "_tham_so" của dict gần nhất."""
    if isinstance(o, str) and o.startswith("@"):
        ten = o[1:]
        if ten not in tham_so:
            raise ValueError(f"Tham số không tồn tại: {o}")
        refs.append(ten)
        v = tham_so[ten]
        if isinstance(v, dict):
            v = v["gia_tri"] if "gia_tri" in v else v.get("bang", v)
        return v
    if isinstance(o, list):
        return [_giai(x, tham_so, refs) for x in o]
    if isinstance(o, dict):
        d, mine = {}, {}
        for k, v in o.items():
            d[k] = _giai(v, tham_so, mine.setdefault(k, []))
        if any(mine.values()):
            d["_tham_so"] = {k: v for k, v in mine.items() if v}
        return d
    return o
