"""Eval độ đúng của hệ thống so với nhãn nhóm tự viết (không phải độ đồng thuận với bác sĩ).

    python eval/run_eval.py                                   # stub, data/test-cases/*.yaml
    python eval/run_eval.py --a1 stub --lan 2 --cases "data/test-cases/*.yaml" "data/eval/*.yaml"
    python eval/run_eval.py --a1 live --lan 3 --yes           # tốn tiền OpenAI

Ba phần: nạp ca (mặc định của bộ test áp ở đây, không ở engine) → chạy engine, ghi bản ghi
(row / clause / so / call / he) → tính chỉ số bằng hàm thuần, xuất .md + .json.
Phần chỉ số không import engine, để test được khi engine còn đang viết (eval/test_report.py).
"""
import argparse
import glob
import json
import math
import os
import sys
import time
from collections import Counter, defaultdict
from datetime import date, datetime
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

PHU_HOP = "Phù hợp quy tắc BHYT"
DU_CAN_CU = "Đủ căn cứ · bác sĩ xác nhận"
XEM_LAI = "Cần xem lại"
KHONG_TRA = "Không được chi trả"
THU_TU = [PHU_HOP, DU_CAN_CU, XEM_LAI, KHONG_TRA]  # thuận lợi nhất → kém nhất
HANG = {s: i for i, s in enumerate(THU_TU)}
INPUT_KEYS = ("luot_kham", "ngay_kham", "benh_nhan", "icd", "sinh_hieu", "phieu_kham", "lich_su", "chi_dinh")
LOI_TRICH = "trich_dan_"  # tiền tố ghi chú của verify (khong_khop, cat_phu_dinh): không phải lỗi gọi A1


# ---------- nạp ca ----------

def load_cases(patterns):
    out = []
    for pat in patterns:
        p = Path(pat) if Path(pat).is_absolute() else ROOT / pat
        files = sorted(glob.glob(str(p)))
        if not files:
            print(f"! không có file khớp {pat}", file=sys.stderr)
        for f in files:
            for c in yaml.safe_load(Path(f).read_text(encoding="utf-8")) or []:
                out.append({**c, "_file": Path(f).name})
    return out


def mac_dinh(case):
    """Đầu vào engine (spec mục 4) + mặc định của bộ test (test-cases/README.md). Engine không có mặc định."""
    luot = {k: case[k] for k in INPUT_KEYS if k in case}
    luot.setdefault("ngay_kham", date(2026, 11, 12))
    luot.setdefault("luot_kham", "LK-" + str(case["id"]))
    bn = luot["benh_nhan"] = dict(luot.get("benh_nhan") or {})
    if "the" not in bn:
        thang = bn["tuoi_thang"] if bn.get("tuoi_thang") is not None else (bn.get("tuoi_ngay") or 0) / 30.44
        bn["the"] = {"han_den": date(2027, 12, 31), "muc_huong": 100 if thang < 72 else 80}
    return luot


def _ds(x):
    return [] if x is None else [x] if isinstance(x, str) else list(x)


def so_ky_vong(case):
    """{truong: gia_tri | None}; None = không được trích. Ưu tiên a1_ky_vong_so_lieu, rồi a1_gia_lap.so_lieu.
    Nhận cả dạng list [{truong, gia_tri}] lẫn dict {truong: gia_tri}. Không có nhãn → None."""
    src = case.get("a1_ky_vong_so_lieu")
    if src is None:
        src = (case.get("a1_gia_lap") or {}).get("so_lieu")
    if src is None:
        return None
    if isinstance(src, dict):
        return {k: (v.get("gia_tri") if isinstance(v, dict) else v) for k, v in src.items()}
    return {s["truong"]: s.get("gia_tri") for s in src}


def so_trong_ok(case):
    """Trường có chap_nhan_trong: true (a1-kho.yaml): A1 bỏ trống cũng tính đúng, trả số khác vẫn sai."""
    src = case.get("a1_ky_vong_so_lieu")
    return {s["truong"] for s in src if s.get("chap_nhan_trong")} if isinstance(src, list) else set()


# ---------- bản ghi (thuần, từ kết quả engine đã chạy) ----------

def ban_ghi(case, pairs, visit, lan):
    """pairs = [(thu_tu, dòng ky_vong)] (tests.stub_a1.gan_thu_tu). visit = kết quả chay_luot.
    → (rows, clauses, so) cho một lần chạy một ca."""
    ca, bay_ca = case["id"], _ds(case.get("bay"))
    rows, clauses = [], []
    for tt, kv in pairs:
        d = visit["dong"].get(tt)
        rows.append({"ca": ca, "file": case.get("_file"), "lan": lan, "thu_tu": tt,
                     "ten": kv.get("ten") or kv.get("ma") or (d or {}).get("ten"),
                     "ky_vong": kv.get("trang_thai"), "got": d and d["trang_thai"],
                     "chi_rule": visit.get("chi_rule", {}).get(tt), "bay": bay_ca})
        cl = {v.get("id"): v for v in (d or {}).get("checklist") or []}
        for v in kv.get("ve") or []:
            if not v.get("id"):
                continue
            g = cl.get(v["id"]) or {}
            ai = v.get("kiem_bang") == "ai"
            got, trich, nguon = g.get("ket_qua"), g.get("trich_dan"), "engine"
            them = g.get("trich_them") or []
            a1v = (visit.get("a1_ve") or {}).get(f"{tt}:{v['id']}")
            if ai and a1v and kv.get("trang_thai") is None:  # bộ chỉ đo A1 (a1-kho): chấm câu trả lời A1 sau verify
                got, trich, nguon = a1v.get("ket_qua"), a1v.get("trich_dan"), "a1"
                them = a1v.get("trich_them") or []
            chap = _ds(v.get("trich_dan")) + _ds(v.get("trich_dan_khac"))
            clauses.append({"ca": ca, "lan": lan, "thu_tu": tt, "id": v["id"], "nhanh": g.get("nhanh"),
                            "ai": ai, "ky_vong": v.get("ket_qua"), "got": got, "nguon_got": nguon, "trich": trich,
                            "sai_cho": bool(ai and got == "dat" and v.get("ket_qua") == "dat" and chap
                                            and not any(giao(t, c) for t in [trich, *them] for c in chap)),
                            "bay": _ds(v.get("bay")) or bay_ca})
    so = []
    ky = so_ky_vong(case)
    if ky is not None:
        got, hoi, tok = visit.get("so_lieu") or {}, set(visit.get("so_hoi") or []), so_trong_ok(case)
        for tr in sorted(set(ky) | set(got) | hoi):
            so.append({"ca": ca, "lan": lan, "truong": tr, "ky_vong": ky.get(tr), "got": got.get(tr),
                       "hoi": tr in hoi, "trong_ok": tr in tok, "bay": bay_ca})
    return rows, clauses, so


def giao(a, b, toi_thieu=5):
    """Hai trích dẫn giao nhau: có chuỗi con chung ≥ toi_thieu ký tự (hoặc bằng cả đoạn ngắn hơn)."""
    # ponytail: ngưỡng ký tự thô, có thể khớp nhầm qua từ chung ngắn; cần chặt hơn thì so theo vị trí trong phiếu khám
    from difflib import SequenceMatcher
    a, b = (" ".join(x.split()).casefold() if isinstance(x, str) else "" for x in (a, b))
    if not a or not b:
        return False
    m = SequenceMatcher(None, a, b, autojunk=False).find_longest_match(0, len(a), 0, len(b))
    return m.size >= min(toi_thieu, len(a), len(b))


def dem_trich(raw, res):
    """(số trích dẫn trong đầu ra thô của A1, số bị src.a1.verify loại). raw = JSON model, res = sau verify.
    Đếm: trich_dan của vế dat, trich_lien_quan, trich_dan của so_lieu. Thuần, không phụ thuộc hàm nội bộ của src.a1."""
    def dem(x, tho):
        ve = [v for v in (x or {}).get("ve") or [] if isinstance(v, dict)]
        sl = [z for z in (x or {}).get("so_lieu") or [] if isinstance(z, dict)]
        return (sum(v.get("ket_qua") == "dat" and v.get("trich_dan") is not None for v in ve)
                + sum(len(v.get("trich_lien_quan") or []) for v in ve)
                + (len(sl) if tho else len({z.get("truong") for z in sl})))
    n = dem(raw, True)
    return n, max(0, n - dem(res, False))


# ---------- chỉ số (thuần) ----------

def phan_vi(xs, p):
    """Nearest-rank."""
    if not xs:
        return None
    s = sorted(xs)
    return s[max(0, math.ceil(p / 100 * len(s)) - 1)]


def m_dong(rows):
    """Chỉ tính dòng có nhãn trang_thai (bộ a1-kho không có → khong_nhan)."""
    khong_nhan = sum(r["ky_vong"] is None for r in rows)
    rows = [r for r in rows if r["ky_vong"] is not None]
    cm = Counter((r["ky_vong"], r["got"]) for r in rows)
    over = [r for r in rows if r["got"] in HANG and r["ky_vong"] in HANG and HANG[r["got"]] < HANG[r["ky_vong"]]]
    under = [r for r in rows if r["got"] in HANG and r["ky_vong"] in HANG and HANG[r["got"]] > HANG[r["ky_vong"]]]
    dung = sum(r["got"] == r["ky_vong"] for r in rows)
    return {"n": len(rows), "khong_nhan": khong_nhan, "dung": dung, "ty_le_dung": dung / len(rows) if rows else None,
            "qua_thuan_loi": len(over), "kem_thuan_loi": len(under),
            "khong_co_dong": sum(r["got"] is None for r in rows),
            "ma_tran": {f"{k}|{g}": n for (k, g), n in cm.items()},
            "ds_qua_thuan_loi": [_r(r) for r in over], "ds_kem_thuan_loi": [_r(r) for r in under]}


def _r(r):
    return {k: r[k] for k in ("ca", "lan", "thu_tu", "ten", "ky_vong", "got") if k in r}


def _ve_stats(cs):
    sc = [c for c in cs if c.get("sai_cho")]
    dung = sum(c["got"] == c["ky_vong"] and not c.get("sai_cho") for c in cs)
    fd = [c for c in cs if c["ai"] and c["got"] == "dat" and c["ky_vong"] != "dat"]
    md = [c for c in cs if c["ai"] and c["ky_vong"] == "dat" and c["got"] != "dat"]
    return {"n": len(cs), "dung": dung, "ty_le_dung": dung / len(cs) if cs else None,
            "dat_sai": len(fd), "bo_sot_dat": len(md), "dat_sai_cho": len(sc), "_fd": fd, "_md": md, "_sc": sc}


def m_ve(clauses):
    tat_ca, ai = _ve_stats(clauses), _ve_stats([c for c in clauses if c["ai"]])
    rule = _ve_stats([c for c in clauses if not c["ai"]])
    by = defaultdict(list)
    for c in clauses:
        for t in c.get("bay") or []:
            by[t].append(c)
    cl = lambda s: {k: v for k, v in s.items() if not k.startswith("_")}  # noqa: E731
    ve = lambda c: {k: c.get(k) for k in ("ca", "lan", "thu_tu", "id", "nhanh", "ky_vong", "got", "trich", "bay")}  # noqa: E731
    return {"tat_ca": cl(tat_ca), "rule": cl(rule), "ai": cl(ai),
            "ds_dat_sai": [ve(c) for c in ai["_fd"]], "ds_bo_sot_dat": [ve(c) for c in ai["_md"]],
            "ds_dat_sai_cho": [ve(c) for c in ai["_sc"]],
            "theo_bay": {t: cl(_ve_stats(cs)) for t, cs in sorted(by.items())}}


def _bang(a, b):
    return a is None and b is None or a is not None and b is not None and abs(float(a) - float(b)) < 1e-9


def m_so(so):
    """dung (gồm đúng là không trích), sai_gia_tri, bo_sot, trich_thua; trường engine không hỏi → khong_hoi (không tính)."""
    loai = Counter()
    ds = []
    for s in so:
        if not s["hoi"]:
            k = "khong_hoi"
        elif _bang(s["ky_vong"], s["got"]) or s["got"] is None and s.get("trong_ok"):
            k = "dung"
        elif s["got"] is None:
            k = "bo_sot"
        elif s["ky_vong"] is None:
            k = "trich_thua"
        else:
            k = "sai_gia_tri"
        loai[k] += 1
        if k not in ("dung", "khong_hoi"):
            ds.append({**{x: s[x] for x in ("ca", "lan", "truong", "ky_vong", "got")}, "loai": k})
    n = sum(v for k, v in loai.items() if k != "khong_hoi")
    return {"n": n, **{k: loai[k] for k in ("dung", "sai_gia_tri", "bo_sot", "trich_thua", "khong_hoi")},
            "ty_le_dung": loai["dung"] / n if n else None, "ds_sai": ds}


def m_trich(calls):
    cs = [c for c in calls if c["goi"] and c.get("trich") is not None]
    tong, bo = sum(c["trich"] for c in cs), sum(c["trich_bo"] for c in cs)
    return {"so_lan_goi": len(cs), "trich_dan": tong, "bi_bo": bo,
            "bi_bo_moi_lan_goi": bo / len(cs) if cs else None,
            "lan_goi_co_loi_trich": sum((c.get("loi") or "").startswith(LOI_TRICH) for c in calls if c["goi"]),
            "ds": [{"ca": c["ca"], "lan": c["lan"], "bi_bo": c["trich_bo"]} for c in cs if c["trich_bo"]]}


def m_on_dinh(rows, clauses):
    def flips(recs, key):
        g = defaultdict(list)
        for r in recs:
            g[key(r)].append(r["got"])
        nhom = {k: v for k, v in g.items() if len(v) >= 2}
        lat = {k: v for k, v in nhom.items() if len(set(v)) > 1}
        return {"n": len(nhom), "lat": len(lat), "ty_le_lat": len(lat) / len(nhom) if nhom else None,
                "ds": [{"khoa": "/".join(map(str, k)), "gia_tri": v} for k, v in lat.items()]}
    return {"dong": flips(rows, lambda r: (r["ca"], r["thu_tu"])),
            "ve": flips(clauses, lambda c: (c["ca"], c["thu_tu"], c["id"]))}


def m_ops(calls, gia_vao=None, gia_ra=None):
    goi = [c for c in calls if c["goi"]]
    loi = [c for c in goi if c.get("loi") and not c["loi"].startswith(LOI_TRICH)]
    het_gio = [c for c in loi if "timeout" in c["loi"].lower()]
    ms = [c["ms"] for c in calls]
    a1ms = [c["a1_ms"] for c in goi]
    tin = [c["tok_vao"] for c in goi if c.get("tok_vao") is not None]
    tout = [c["tok_ra"] for c in goi if c.get("tok_ra") is not None]
    chi_phi = None
    if tin and gia_vao is not None and gia_ra is not None:
        chi_phi = sum(tin) / 1e6 * gia_vao + sum(tout) / 1e6 * gia_ra
    return {"luot": len(calls), "goi_a1": len(goi), "loi": len(loi), "het_gio": len(het_gio),
            "ty_le_loi": len(loi) / len(goi) if goi else None,
            "ty_le_het_gio": len(het_gio) / len(goi) if goi else None,
            "loai_loi": dict(Counter(c["loi"] for c in loi)),
            "check_ms_p50": phan_vi(ms, 50), "check_ms_p95": phan_vi(ms, 95), "check_ms_max": max(ms) if ms else None,
            "a1_ms_p50": phan_vi(a1ms, 50), "a1_ms_p95": phan_vi(a1ms, 95),
            "token_vao": sum(tin) if tin else None, "token_ra": sum(tout) if tout else None,
            "lan_goi_co_usage": len(tin), "chi_phi_usd": chi_phi}


def m_chi_rule(rows, he):
    """A1 value: dòng hệ chỉ-rule báo Phù hợp nhưng nhãn kém thuận lợi hơn; 'bắt được' = hệ đầy đủ không quá thuận lợi."""
    r1 = [r for r in rows if r["lan"] == 1 and r.get("chi_rule") is not None and r["ky_vong"] is not None]
    mo = [r for r in r1 if r["chi_rule"] == PHU_HOP and HANG.get(r["ky_vong"], 0) > 0]
    bat = [r for r in mo if r["got"] in HANG and HANG[r["got"]] >= HANG[r["ky_vong"]]]
    khop = [h for h in he if h["got"] == h["nhan"]]
    return {"n_dong": len(r1), "chi_rule_dung": sum(r["chi_rule"] == r["ky_vong"] for r in r1),
            "chi_rule_qua_thuan_loi": len(mo), "he_day_du_bat_duoc": len(bat),
            "ds_a1_gia_tri": [{**_r(r), "chi_rule": r["chi_rule"]} for r in bat],
            "ds_a1_bo_lo": [{**_r(r), "chi_rule": r["chi_rule"]} for r in mo if r not in bat],
            "nhan_he_chi_rule": {"n": len(he), "khop": len(khop),
                                 "ds_lech": [h for h in he if h["got"] != h["nhan"]]}}


def tinh(rec, gia_vao=None, gia_ra=None):
    return {"dong": m_dong(rec["rows"]), "ve": m_ve(rec["clauses"]), "so": m_so(rec["so"]),
            "trich": m_trich(rec["calls"]), "on_dinh": m_on_dinh(rec["rows"], rec["clauses"]),
            "ops": m_ops(rec["calls"], gia_vao, gia_ra), "chi_rule": m_chi_rule(rec["rows"], rec["he"])}


# ---------- báo cáo ----------

def _pct(x):
    return "—" if x is None else f"{100 * x:.1f}%"


def _bang_md(head, rows):
    out = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    out += ["| " + " | ".join("—" if c is None else str(c) for c in r) + " |" for r in rows]
    return "\n".join(out)


def render_md(s, meta):
    d, v, so, tr, od, op, cr = (s[k] for k in ("dong", "ve", "so", "trich", "on_dinh", "ops", "chi_rule"))
    ok = lambda b: "ĐẠT" if b else "**CHƯA ĐẠT**"  # noqa: E731
    p95 = op["check_ms_p95"]
    L = [f"# Eval hệ thống — {meta.get('thoi_gian', '')}", "",
         f"A1: `{meta.get('a1')}`{' (' + str(meta.get('model')) + ')' if meta.get('model') else ''} · "
         f"lần lặp: {meta.get('lan')} · ca: {meta.get('so_ca')} · rules: `{meta.get('phien_ban_rule', '')[:12]}` · "
         f"file ca: {', '.join(meta.get('cases', []))}", "",
         "## Tóm tắt", "",
         _bang_md(["Chỉ số", "Giá trị", "Mục tiêu"], [
             ["Dòng QUÁ THUẬN LỢI (got thuận lợi hơn nhãn)", d["qua_thuan_loi"], f"0 — {ok(d['qua_thuan_loi'] == 0)}"],
             ["Dòng kém thuận lợi", d["kem_thuan_loi"], ""],
             ["Khớp trạng thái dòng", f"{d['dung']}/{d['n']} ({_pct(d['ty_le_dung'])})", ""],
             ["Vế AI đạt sai (got dat, nhãn ≠ dat)", v["ai"]["dat_sai"], f"0 — {ok(v['ai']['dat_sai'] == 0)}"],
             ["Vế AI bỏ sót đạt", v["ai"]["bo_sot_dat"], ""],
             ["Vế AI đạt nhưng trích sai chỗ (không giao trich_dan / trich_dan_khac)", v["ai"]["dat_sai_cho"], ""],
             ["Khớp ket_qua vế (mọi vế có id)", f"{v['tat_ca']['dung']}/{v['tat_ca']['n']} ({_pct(v['tat_ca']['ty_le_dung'])})", ""],
             ["Trích số khớp", f"{so['dung']}/{so['n']} ({_pct(so['ty_le_dung'])})", ""],
             ["Trích dẫn A1 bị loại / lần gọi", f"{tr['bi_bo']}/{tr['trich_dan']} ({tr['bi_bo_moi_lan_goi'] if tr['bi_bo_moi_lan_goi'] is None else round(tr['bi_bo_moi_lan_goi'], 2)})", ""],
             ["Lật trạng thái dòng qua các lần", f"{od['dong']['lat']}/{od['dong']['n']} ({_pct(od['dong']['ty_le_lat'])})", ""],
             ["A1 lỗi / hết giờ", f"{op['loi']} / {op['het_gio']} trên {op['goi_a1']} lần gọi", ""],
             ["engine.check p50 / p95 (ms)", f"{op['check_ms_p50']} / {p95}", f"p95 < 10000 — {ok(p95 is not None and p95 < 10000)}"],
             ["Hệ chỉ-rule báo Phù hợp sai → hệ đầy đủ bắt được", f"{cr['he_day_du_bat_duoc']}/{cr['chi_rule_qua_thuan_loi']}", ""],
         ]), ""]

    L += ["## 1. Trạng thái dòng", "", "Hàng = nhãn, cột = hệ thống trả."
          + (f" Bỏ qua {d['khong_nhan']} dòng không có nhãn `trang_thai`." if d["khong_nhan"] else ""), ""]
    cols = THU_TU + ([None] if d["khong_co_dong"] else [])
    L.append(_bang_md(["nhãn \\ got"] + [c or "(không có dòng)" for c in cols],
                      [[k] + [d["ma_tran"].get(f"{k}|{g}", 0) for g in cols] for k in THU_TU]))
    for ten, ds in (("Quá thuận lợi", d["ds_qua_thuan_loi"]), ("Kém thuận lợi", d["ds_kem_thuan_loi"])):
        L += ["", f"**{ten}** ({len(ds)})", ""]
        if ds:
            L.append(_bang_md(["ca", "lần", "dòng", "dịch vụ", "nhãn", "got"],
                              [[r["ca"], r["lan"], r["thu_tu"], r["ten"], r["ky_vong"], r["got"]] for r in ds]))

    L += ["", "## 2. Vế điều kiện", "",
          _bang_md(["nhóm", "n", "khớp", "đạt sai", "bỏ sót đạt", "đạt sai chỗ"],
                   [[k, v[k]["n"], _pct(v[k]["ty_le_dung"])] + ([v[k]["dat_sai"], v[k]["bo_sot_dat"], v[k]["dat_sai_cho"]] if k != "rule" else ["", "", ""])
                    for k in ("tat_ca", "rule", "ai")]
                   + [[f"bẫy: {t}", x["n"], _pct(x["ty_le_dung"]), x["dat_sai"], x["bo_sot_dat"], x["dat_sai_cho"]] for t, x in v["theo_bay"].items()])]
    for ten, ds in (("Vế AI đạt sai", v["ds_dat_sai"]), ("Vế AI bỏ sót đạt", v["ds_bo_sot_dat"]),
                    ("Vế AI đạt nhưng trích sai chỗ", v["ds_dat_sai_cho"])):
        L += ["", f"**{ten}** ({len(ds)})", ""]
        if ds:
            L.append(_bang_md(["ca", "lần", "dòng", "vế", "nhánh", "nhãn", "got", "trích dẫn", "bẫy"],
                              [[c["ca"], c["lan"], c["thu_tu"], c["id"], c["nhanh"], c["ky_vong"], c["got"], c["trich"], ", ".join(c["bay"])] for c in ds]))

    L += ["", "## 3. Trích số", "",
          f"Khớp {so['dung']}, sai giá trị {so['sai_gia_tri']}, bỏ sót {so['bo_sot']}, trích thừa {so['trich_thua']}, "
          f"engine không hỏi {so['khong_hoi']} (không tính).", ""]
    if so["ds_sai"]:
        L.append(_bang_md(["ca", "lần", "trường", "nhãn", "got", "loại"],
                          [[x["ca"], x["lan"], x["truong"], x["ky_vong"], x["got"], x["loai"]] for x in so["ds_sai"]]))

    L += ["", "## 4. Trích dẫn bị loại khi kiểm tra", "",
          f"{tr['bi_bo']} trên {tr['trich_dan']} trích dẫn, {tr['so_lan_goi']} lần gọi; "
          f"lần gọi có `loi: {LOI_TRICH}*`: {tr['lan_goi_co_loi_trich']}.", ""]
    if tr["ds"]:
        L.append(_bang_md(["ca", "lần", "bị loại"], [[x["ca"], x["lan"], x["bi_bo"]] for x in tr["ds"]]))

    L += ["", "## 5. Độ ổn định qua các lần lặp", ""]
    if meta.get("lan", 1) < 2:
        L.append("Chỉ chạy 1 lần (`--lan ≥ 2` để đo).")
    else:
        L.append(f"Dòng lật: {od['dong']['lat']}/{od['dong']['n']} ({_pct(od['dong']['ty_le_lat'])}) · "
                 f"vế lật: {od['ve']['lat']}/{od['ve']['n']} ({_pct(od['ve']['ty_le_lat'])})")
        ds = od["dong"]["ds"] + od["ve"]["ds"]
        if ds:
            L += ["", _bang_md(["khóa", "giá trị qua các lần"], [[x["khoa"], " → ".join(map(str, x["gia_tri"]))] for x in ds])]

    L += ["", "## 6. Vận hành", "",
          _bang_md(["", "giá trị"], [
              ["lượt × lần", op["luot"]], ["lần gọi A1", op["goi_a1"]],
              ["lỗi A1", f"{op['loi']} ({_pct(op['ty_le_loi'])}) {op['loai_loi'] or ''}"],
              ["hết giờ", f"{op['het_gio']} ({_pct(op['ty_le_het_gio'])})"],
              ["engine.check p50 / p95 / max (ms)", f"{op['check_ms_p50']} / {op['check_ms_p95']} / {op['check_ms_max']}"],
              ["A1 p50 / p95 (ms)", f"{op['a1_ms_p50']} / {op['a1_ms_p95']}"],
              ["token vào / ra", f"{op['token_vao']} / {op['token_ra']} ({op['lan_goi_co_usage']} lần gọi có usage)"],
              ["chi phí ước tính (USD)", "—" if op["chi_phi_usd"] is None else f"{op['chi_phi_usd']:.4f}"],
          ])]

    L += ["", "## 7. Hệ chỉ-rule và giá trị của A1", "",
          f"Hệ chỉ-rule (máy sinh, mode=chi_rule) khớp nhãn dòng: {cr['chi_rule_dung']}/{cr['n_dong']}. "
          f"Báo Phù hợp nhưng nhãn kém thuận lợi hơn: {cr['chi_rule_qua_thuan_loi']}, hệ đầy đủ bắt được {cr['he_day_du_bat_duoc']}.",
          f"Nhãn `he_chi_rule` của ca khớp máy sinh: {cr['nhan_he_chi_rule']['khop']}/{cr['nhan_he_chi_rule']['n']}.", ""]
    for ten, ds in (("A1 có giá trị", cr["ds_a1_gia_tri"]), ("A1 bỏ lọt", cr["ds_a1_bo_lo"])):
        if ds:
            L += [f"**{ten}** ({len(ds)})", "",
                  _bang_md(["ca", "dòng", "dịch vụ", "nhãn", "chỉ-rule", "đầy đủ"],
                           [[r["ca"], r["thu_tu"], r["ten"], r["ky_vong"], r["chi_rule"], r["got"]] for r in ds]), ""]
    if cr["nhan_he_chi_rule"]["ds_lech"]:
        L += ["**Nhãn `he_chi_rule` lệch máy sinh**", "",
              _bang_md(["ca", "nhãn", "máy sinh"], [[h["ca"], h["nhan"], h["got"]] for h in cr["nhan_he_chi_rule"]["ds_lech"]]), ""]
    if meta.get("ghi_chu"):
        L += ["## Ghi chú", ""] + [f"- {x}" for x in meta["ghi_chu"]]
    return "\n".join(L) + "\n"


# ---------- chạy engine ----------

def _bat_openai(sink):
    """Bọc OpenAI trong src.a1 (không sửa file) để giữ response thô: usage + nội dung trước verify."""
    import src.a1 as a1mod
    real = a1mod.OpenAI

    def factory(*a, **k):
        c = real(*a, **k)
        create = c.chat.completions.create

        def cap(*a2, **k2):
            r = create(*a2, **k2)
            sink.append(r)
            return r
        c.chat.completions.create = cap
        return c
    a1mod.OpenAI = factory


def chay_luot(luot, rules, check, a1fn, resp_sink):
    """Một lượt, mode=full. → visit dict (dong theo thu_tu, so_lieu A1 trả, thời gian, usage, trích dẫn)."""
    cap = {}

    def wrap(req):
        cap["req"] = req
        cap["res"] = a1fn(req)
        return cap["res"]
    resp_sink.clear()
    t0 = time.perf_counter()
    out = check(luot, rules, wrap if a1fn else None)
    ms = int((time.perf_counter() - t0) * 1000)
    info = out.get("a1") or {}
    visit = {"dong": {d["thu_tu"]: d for d in out["dong"]}, "ms": ms, "a1": info,
             "so_hoi": [s["truong"] for s in (cap.get("req") or {}).get("so_lieu") or []],
             "so_lieu": {s["truong"]: s.get("gia_tri") for s in (cap.get("res") or {}).get("so_lieu") or []},
             "a1_ve": {x["khoa"]: x for x in (cap.get("res") or {}).get("ve") or [] if isinstance(x, dict) and "khoa" in x},
             "tok_vao": None, "tok_ra": None, "trich": None, "trich_bo": None}
    raw = cap.get("res")
    if resp_sink:  # live: đếm trên đầu ra thô của model
        r = resp_sink[-1]
        u = getattr(r, "usage", None)
        if u is not None:
            visit["tok_vao"], visit["tok_ra"] = u.prompt_tokens, u.completion_tokens
        try:
            raw = json.loads(r.choices[0].message.content)
        except Exception:
            raw = None
    if "res" in cap and raw is not None:
        visit["trich"], visit["trich_bo"] = dem_trich(raw, cap["res"])
    return visit


def chay(cases, rules, a1_mode, lan, live_fn=None, resp_sink=None):
    from src.engine import check
    from tests.stub_a1 import gan_thu_tu, make_stub
    rec = {"rows": [], "clauses": [], "so": [], "calls": [], "he": []}
    sink = resp_sink if resp_sink is not None else []
    for case in cases:
        luot = mac_dinh(case)
        pairs = gan_thu_tu(case)
        chi = {d["thu_tu"]: d["trang_thai"] for d in check(luot, rules, None, mode="chi_rule")["dong"]}
        if case.get("he_chi_rule") and pairs:
            rec["he"].append({"ca": case["id"], "nhan": case["he_chi_rule"].split(" (")[0].strip(),
                              "got": chi.get(pairs[0][0])})
        for i in range(1, lan + 1):
            # stub: bộ a1-kho không có a1_gia_lap → lấy số từ a1_ky_vong_so_lieu
            gl = case.get("a1_gia_lap") or {"so_lieu": [s for s in _ds(case.get("a1_ky_vong_so_lieu")) if isinstance(s, dict)]}
            fn = make_stub({**case, "a1_gia_lap": gl}) if a1_mode == "stub" else live_fn
            v = chay_luot(luot, rules, check, fn, sink)
            v["chi_rule"] = chi
            rows, cl, so = ban_ghi(case, pairs, v, i)
            rec["rows"] += rows
            rec["clauses"] += cl
            rec["so"] += so
            rec["calls"].append({"ca": case["id"], "lan": i, "ms": v["ms"], "goi": bool(v["a1"].get("goi")),
                                 "loi": v["a1"].get("loi"), "a1_ms": v["a1"].get("ms", 0),
                                 "tok_vao": v["tok_vao"], "tok_ra": v["tok_ra"],
                                 "trich": v["trich"], "trich_bo": v["trich_bo"]})
        print(f"  {case['id']}", file=sys.stderr)
    return rec


def uoc_tinh_goi(cases, rules):
    """Số lượt sẽ gọi A1 (chạy engine với A1 giả rỗng)."""
    from src.engine import check
    nop = lambda req: {"ve": [], "so_lieu": [], "loi": None}  # noqa: E731
    return sum(bool(check(mac_dinh(c), rules, nop)["a1"].get("goi")) for c in cases)


def _f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--a1", choices=("stub", "live"), default="stub")
    ap.add_argument("--lan", type=int, default=1, help="số lần lặp mỗi ca (đo độ ổn định khi ≥ 2)")
    ap.add_argument("--cases", nargs="+", default=["data/test-cases/*.yaml"])
    ap.add_argument("--rules", default="data/rules")
    ap.add_argument("--out", help="đường dẫn .md (kèm .json cùng tên); mặc định eval/reports/<thời gian>.md")
    ap.add_argument("--yes", action="store_true", help="đồng ý gọi OpenAI thật (live)")
    a = ap.parse_args(argv)
    for f in (sys.stdout, sys.stderr):  # console Windows cp1252
        if hasattr(f, "reconfigure"):
            f.reconfigure(encoding="utf-8")
    if a.lan < 1:
        ap.error("--lan phải ≥ 1")

    from src.rules import load_rules
    rules_dir = Path(a.rules) if Path(a.rules).is_absolute() else ROOT / a.rules
    thieu = [f for f in ("danh-muc.yaml", "dieu-kien.yaml", "tham-so.yaml") if not (rules_dir / f).exists()]
    if thieu:
        sys.exit(f"Chưa có {', '.join(thieu)} trong {rules_dir}")
    rules = load_rules(rules_dir)
    cases = load_cases(a.cases)
    if not cases:
        sys.exit("Không có ca nào.")
    meta = {"thoi_gian": datetime.now().strftime("%Y-%m-%d %H:%M"), "a1": a.a1, "lan": a.lan, "so_ca": len(cases),
            "cases": a.cases, "phien_ban_rule": rules.phien_ban_rule, "ghi_chu": []}

    live_fn, sink = None, []
    if a.a1 == "live":
        from src.app import load_env
        load_env()
        model, key = os.environ.get("OPENAI_MODEL"), os.environ.get("OPENAI_API_KEY")
        if not model or not key:
            sys.exit("Cần OPENAI_API_KEY và OPENAI_MODEL (env hoặc .env).")
        n = uoc_tinh_goi(cases, rules) * a.lan
        print(f"Ước tính {n} lần gọi OpenAI (model {model}, effort {os.environ.get('A1_REASONING_EFFORT') or 'mặc định'}, "
              f"{len(cases)} ca × {a.lan} lần, "
              f"timeout {os.environ.get('A1_TIMEOUT_S') or 8}s).", file=sys.stderr)
        if not a.yes:
            sys.exit("Thêm --yes để chạy thật.")
        from src.a1 import make_live
        _bat_openai(sink)
        ts = rules.tham_so if isinstance(rules.tham_so, dict) else {}
        effort = os.environ.get("A1_REASONING_EFFORT") or None
        khoang = ts.get("khoang_hop_le")
        if isinstance(khoang, dict) and "gia_tri" in khoang:  # như src/app.py
            khoang = khoang["gia_tri"]
        live_fn = make_live(model, float(os.environ.get("A1_TIMEOUT_S") or 8), khoang,
                            **({"reasoning_effort": effort} if effort else {}))
        meta["model"] = model + (f", reasoning_effort={effort}" if effort else "")
    else:
        meta["ghi_chu"].append("Stub: vế AI và số liệu sinh từ chính nhãn (ky_vong, a1_gia_lap) — đo engine, không đo LLM.")

    gia_vao, gia_ra = _f(os.environ.get("EVAL_PRICE_IN_PER_1M")), _f(os.environ.get("EVAL_PRICE_OUT_PER_1M"))
    if a.a1 == "live" and gia_vao is None:
        meta["ghi_chu"].append("Chưa đặt EVAL_PRICE_IN_PER_1M / EVAL_PRICE_OUT_PER_1M (USD / 1M token) nên không tính chi phí.")

    rec = chay(cases, rules, a.a1, a.lan, live_fn, sink)
    s = tinh(rec, gia_vao, gia_ra)

    out = Path(a.out) if a.out else ROOT / "eval" / "reports" / (datetime.now().strftime("%Y%m%d-%H%M%S") + ".md")
    out.parent.mkdir(parents=True, exist_ok=True)
    md = render_md(s, meta)
    out.write_text(md, encoding="utf-8")
    out.with_suffix(".json").write_text(
        json.dumps({"meta": meta, "chi_so": s, "ban_ghi": rec}, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    print(md.split("## 1.")[0])
    print(f"→ {out}  (+ .json)")
    return s


if __name__ == "__main__":
    main()
