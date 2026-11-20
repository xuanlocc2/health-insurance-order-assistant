"""Kiểm tra nhanh 3 file rule. Chạy: python data/rules/check_rules.py (từ thư mục gốc repo hoặc bất kỳ đâu)."""
import sys
import unicodedata
from pathlib import Path

import yaml

HERE = Path(__file__).parent
CASES = HERE.parent / "test-cases"
BHYT = {"co", "dieu_kien", "khong_thay", "xac_minh"}
NGUON = {"van_ban", "tu_dung", "bac_si_duyet"}
# Loại kiểm engine hiểu (src/engine.py kiem_tra) → khóa bắt buộc. Thêm loại mới ở engine thì thêm ở đây.
KIEM = {"so_sanh": ("truong", "toan_tu", "gia_tri"), "nguong_theo_tuoi": ("truong", "bang"), "icd_trong": ("ds",),
        "ai_doc": ("cau_hoi",), "lich_su_so_sanh": ("ma", "toan_tu"), "khong_cung_luot": ("ma_hoac_bi_danh",)}
TRUONG = {"nhiet_do", "mach", "nhip_tho"}  # sinh hiệu engine đọc (NHAN trong engine)
TOAN_TU = {"<=", "<", ">=", ">", "=="}
AP_DUNG = {"tuoi_thang", "tuoi_ngay", "nguon", "diem_mo_ho"}


def load(p):
    return yaml.safe_load(p.read_text(encoding="utf-8"))


def chuan(s):  # giống src/engine.py: NFC, gộp khoảng trắng, chữ thường
    return " ".join(unicodedata.normalize("NFC", s or "").split()).lower()


def walk(x):
    yield x
    for c in x.values() if isinstance(x, dict) else x if isinstance(x, list) else ():
        yield from walk(c)


def kiem(dm, dk, ts):
    """Cấu trúc 3 file rule (chưa gồm ca thử). Sai → AssertionError. tests/test_check_rules.py gọi hàm này."""
    def giai(v):  # "@ten" → giá trị trong tham-so.yaml
        if isinstance(v, str) and v.startswith("@"):
            t = ts.get(v[1:])
            assert isinstance(t, dict) and ("gia_tri" in t or "bang" in t), f"tham chiếu {v} không có trong tham-so.yaml"
            return t["gia_tri"] if "gia_tri" in t else t["bang"]
        return v

    def khoang(tu, den, o):  # nửa mở [tu, den); den None = không chặn trên
        tu, den = giai(tu), giai(den)
        assert isinstance(tu, (int, float)) and (den is None or tu < den), f"khoảng sai ở {o}: [{tu}, {den})"

    # danh mục
    ma = [e["ma"] for e in dm if e.get("ma")]
    assert len(ma) == len(set(ma)), "mã trùng trong danh-muc.yaml"
    for e in dm:
        assert e.get("ten") and e.get("bhyt") in BHYT, f"dòng danh mục thiếu ten/bhyt: {e}"
        if e["bhyt"] in ("co", "dieu_kien"):
            assert (e.get("ma") or e.get("ma_chung")) and e.get("can_cu"), f"{e['ten']}: co/dieu_kien phải có ma (hoặc ma_chung) và can_cu"
    theo_ten = {}
    for e in dm:
        for t in {chuan(x) for x in [e["ten"], *(e.get("bi_danh") or [])]}:
            theo_ten.setdefault(t, []).append(e)
    for t, ds in theo_ten.items():  # cùng quy tắc với engine.tra_danh_muc (nhap_nhang)
        assert len(ds) == 1 or (len({e["bhyt"] for e in ds}) == 1 and ds[0]["bhyt"] != "dieu_kien"), \
            f"tên '{t}' khớp {len(ds)} dòng danh mục khác kết luận: chỉ định theo tên sẽ ra Cần xem lại"
    co_dk = {e["ma"] for e in dm if e["bhyt"] == "dieu_kien"}
    assert co_dk == set(dk), f"dieu_kien lệch giữa 2 file: {co_dk ^ set(dk)}"

    # điều kiện
    for m, d in dk.items():
        assert d.get("nguyen_van") and d.get("can_cu") and d.get("nhanh"), f"{m}: thiếu nguyen_van/can_cu/nhanh"
        ve = [v for n in d["nhanh"] for v in n["ve"]] + (d.get("loai_tru") or {}).get("ve", [])
        ids = [v["id"] for v in ve]
        assert len(ids) == len(set(ids)) and all(v.get("mo_ta") for v in ve), f"{m}: id vế trùng hoặc thiếu mo_ta"
        for v in ve:  # vế không có kiem/hoac = "chưa mã hóa" (engine → Cần xem lại), được phép
            for k in [v["kiem"]] if v.get("kiem") else v.get("hoac") or []:
                thieu = [f for f in KIEM.get(k.get("loai"), ()) if f not in k]
                assert k.get("loai") in KIEM and not thieu, f"{m}/{v['id']}: loại kiểm lạ hoặc thiếu {thieu}: {k}"
                assert k.get("truong", "nhiet_do") in TRUONG, f"{m}/{v['id']}: trường sinh hiệu lạ: {k['truong']}"
                assert k.get("toan_tu", "<") in TOAN_TU, f"{m}/{v['id']}: toán tử lạ: {k['toan_tu']}"
                assert k.get("neu_khong_khop") in (None, "ai_doc") and \
                    (k.get("neu_khong_khop") != "ai_doc" or k.get("cau_hoi")), f"{m}/{v['id']}: neu_khong_khop sai"
        for n in d["nhanh"]:
            assert set(n.get("ap_dung") or {}) <= AP_DUNG, f"{m}/{n['id']}: khóa ap_dung lạ: {n['ap_dung']}"
            for k, v in (n.get("ap_dung") or {}).items():
                if k in ("tuoi_thang", "tuoi_ngay"):
                    khoang(v[0], v[1], f"{m}/{n['id']}")
        if "tan_suat" in d:
            khoang(d["tan_suat"]["toi_thieu_gio"], d["tan_suat"]["nen_gio"] + 1, f"{m}/tan_suat")

    # tham số
    for ten, t in ts.items():
        rows = t.get("bang") or [] if isinstance(t, dict) else []
        for r in rows:
            khoang(r["tu"], r["den"], f"tham-so/{ten}")
        assert all(a["den"] <= b["tu"] for a, b in zip(rows, rows[1:])), f"tham-so/{ten}: các khoảng chồng nhau"

    # toàn bộ: @ref, nguon, tu_dung → diem_mo_ho
    for x in walk([dm, dk, ts]):
        giai(x)
        if isinstance(x, dict) and "nguon" in x:
            assert x["nguon"] in NGUON, f"nguon lạ: {x['nguon']}"
            assert x["nguon"] != "tu_dung" or x.get("diem_mo_ho"), f"tu_dung thiếu diem_mo_ho: {x}"



def main():
    sys.stdout.reconfigure(encoding="utf-8")  # console Windows không in được tiếng Việt theo mặc định
    dm = load(HERE / "danh-muc.yaml")["dich_vu"]
    dk = load(HERE / "dieu-kien.yaml")
    ts = load(HERE / "tham-so.yaml")
    kiem(dm, dk, ts)
    ma = {e["ma"] for e in dm if e.get("ma")}

    # ca thử: mọi chỉ định phải tra được, trừ dòng ca thử chủ ý để ngoài danh sách
    ten = {chuan(t) for e in dm for t in [e["ten"], *(e.get("bi_danh") or [])]}
    n = 0
    for f in sorted(CASES.glob("*.yaml")):
        for ca in load(f) or []:
            if not isinstance(ca, dict):
                continue
            ngoai = {k.get("ma") or chuan(k.get("ten")) for k in ca.get("ky_vong") or [] if "Ngoài danh sách" in (k.get("ly_do") or "")}
            for c in ca.get("chi_dinh") or []:
                thay = c.get("ma") in ma or chuan(c.get("ten")) in ten
                la_ngoai = (c.get("ma") or chuan(c.get("ten"))) in ngoai
                assert thay != la_ngoai, f"{f.name} {ca.get('id')}: {c} {'không được tra thấy' if thay else 'không tra được trong danh-muc.yaml'}"
                n += 1
    print(f"OK: {len(dm)} dòng danh mục, {len(dk)} dịch vụ có điều kiện, {len(ts)} tham số, {n} chỉ định trong ca thử")


if __name__ == "__main__":
    main()
