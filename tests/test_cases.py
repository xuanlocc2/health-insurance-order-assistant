"""Chạy mọi ca data/test-cases/*.yaml ở A1_MODE=stub (spec 09 mục 11).

So trang_thai từng dòng (khóa thu_tu), ket_qua của vế có id, muc_huong nếu ca ghi, và he_chi_rule (mode="chi_rule").
Rules: data/rules/ (đổi bằng biến môi trường RULES_DIR, vd tests/fixtures/rules khi phát triển).
"""
import os
from datetime import date
from pathlib import Path

import pytest
import yaml

from src.engine import DU_CAN_CU, KHONG_TRA, PHU_HOP, XEM_LAI, check
from src.rules import load_rules
from tests.stub_a1 import gan_thu_tu, make_stub

ROOT = Path(__file__).resolve().parent.parent
RULES_DIR = Path(os.environ.get("RULES_DIR") or ROOT / "data" / "rules")
FILES = ("danh-muc.yaml", "dieu-kien.yaml", "tham-so.yaml")

# Ca mâu thuẫn spec ↔ kỳ vọng: id → lý do (xfail strict, để biết khi được sửa)
XFAIL = {}

CASES = [c for f in sorted((ROOT / "data" / "test-cases").glob("*.yaml"))
         for c in yaml.safe_load(f.read_text(encoding="utf-8")) or []]


@pytest.fixture(scope="module")
def rules():
    missing = [f for f in FILES if not (RULES_DIR / f).exists()]
    if missing:
        pytest.skip(f"Chưa có {', '.join(missing)} trong {RULES_DIR}")
    return load_rules(RULES_DIR)


def mac_dinh(case):
    """Mặc định của bộ test (test-cases/README.md) — chỉ áp ở đây, engine không có mặc định."""
    luot = {k: v for k, v in case.items()
            if k not in ("id", "ten", "muc_dich", "ky_vong", "he_chi_rule", "diem_mo_ho", "a1_gia_lap")}
    luot.setdefault("ngay_kham", date(2026, 11, 12))
    luot.setdefault("luot_kham", "LK-" + case["id"])
    bn = luot["benh_nhan"] = dict(luot.get("benh_nhan") or {})
    if "the" not in bn:
        thang = bn["tuoi_thang"] if bn.get("tuoi_thang") is not None else (bn.get("tuoi_ngay") or 0) / 30.44
        bn["the"] = {"han_den": date(2027, 12, 31), "muc_huong": 100 if thang < 72 else 80}
    return luot


def _ca(c):
    return pytest.param(c, id=c["id"], marks=[pytest.mark.xfail(reason=XFAIL[c["id"]], strict=True)]
                        if c["id"] in XFAIL else [])


@pytest.mark.parametrize("case", [_ca(c) for c in CASES])
def test_ca(case, rules):
    luot = mac_dinh(case)
    dong = {d["thu_tu"]: d for d in check(luot, rules, make_stub(case))["dong"]}
    loi = [f"dòng {d['thu_tu']} {d['ten']}: quy tắc không đọc được (loi_quy_tac)"  # lưới an toàn của engine che lỗi schema
           for d in dong.values() if d["ma_ly_do"] == "loi_quy_tac"]
    for tt, kv in gan_thu_tu(case):
        d = dong[tt]
        if d["trang_thai"] != kv["trang_thai"]:
            loi.append(f"dòng {tt} {d['ten']}: {d['trang_thai']!r} ≠ kỳ vọng {kv['trang_thai']!r} (lý do: {d['ly_do']})")
        vs = {v["id"]: v for v in d["checklist"]}
        for v in kv.get("ve") or []:
            got = vs.get(v["id"], {}).get("ket_qua")
            if got != v["ket_qua"]:
                loi.append(f"dòng {tt} vế {v['id']}: {got!r} ≠ kỳ vọng {v['ket_qua']!r}")
        if "muc_huong" in kv and d["muc_huong"] != kv["muc_huong"]:
            loi.append(f"dòng {tt}: muc_huong {d['muc_huong']} ≠ {kv['muc_huong']}")
    if case.get("he_chi_rule"):
        ky = case["he_chi_rule"].split(" (")[0].strip()
        chi = check(luot, rules, None, mode="chi_rule")["dong"]
        tt0 = gan_thu_tu(case)[0][0]  # ca có he_chi_rule chỉ có một dòng kỳ vọng
        got = next(d for d in chi if d["thu_tu"] == tt0)["trang_thai"]
        if got != ky:
            loi.append(f"he_chi_rule: {got!r} ≠ kỳ vọng {ky!r}")
    assert not loi, "\n".join(loi)


def test_danh_muc_r1(rules):
    """Vòng lặp R1 qua danh mục: cột bhyt → trạng thái (dịch vụ không có điều kiện)."""
    ky = {"co": PHU_HOP, "khong_thay": KHONG_TRA, "xac_minh": XEM_LAI}
    the = {"han_den": "2027-12-31", "muc_huong": 100}
    for e in rules.danh_muc:
        if e.get("bhyt") == "dieu_kien" or e.get("ma") in rules.dieu_kien:
            continue
        luot = {"ngay_kham": "2026-11-12", "benh_nhan": {"tuoi_thang": 24, "the": the},
                "chi_dinh": [{"ma": e.get("ma"), "ten": e["ten"]}]}
        d = check(luot, rules, None)["dong"][0]
        assert d["trang_thai"] == ky.get(e.get("bhyt"), XEM_LAI), e
        assert d["trang_thai"] != DU_CAN_CU
