"""Xuất kết quả buổi đo ra CSV mở được bằng Excel và in bảng tóm tắt.
Chạy sau mỗi buổi đo: python -m src.xuat_ket_qua (file nằm trong logs/, không commit)."""
import csv
import sys
from datetime import datetime
from pathlib import Path

from src import do_luong, luu_tru

COT = ("tai_khoan", "thu_tu_lam", "bo", "che_do", "ca_id", "ma", "ten", "bac_si_chon", "dap_an", "dung",
       "goi_y_cong_cu", "trang_thai_cong_cu", "kiem_tra_id", "luu_luc")
ROOT = Path(__file__).resolve().parent.parent


def tao_dong(ket_qua):
    """Mỗi dịch vụ một dòng. Chưa có đáp án thì để trống cột chấm, không tự coi là đúng hay sai."""
    rows = []
    for k in sorted(ket_qua, key=lambda x: (x["tai_khoan"], x["thu_tu"])):
        da = do_luong.dap_an(k["ca_id"])
        for d in k["dong"]:
            dung = da.get(d["ten"])
            rows.append({"tai_khoan": k["tai_khoan"], "thu_tu_lam": k["thu_tu"], "bo": k["bo"], "che_do": k["che_do"],
                         "ca_id": k["ca_id"], "ma": d.get("ma"), "ten": d["ten"], "bac_si_chon": d["bac_si_chon"],
                         "dap_an": dung or "", "dung": ("dung" if d["bac_si_chon"] == dung else "sai") if dung else "",
                         "goi_y_cong_cu": d.get("o_bhyt_goi_y") or "", "trang_thai_cong_cu": d.get("trang_thai") or "",
                         "kiem_tra_id": k.get("kiem_tra_id") or "", "luu_luc": k.get("luu_luc") or ""})
    return rows


def tom_tat(rows):
    nhom = {}
    for r in rows:
        n = nhom.setdefault((r["tai_khoan"], r["che_do"]), {"ca": set(), "so_dong": 0, "so_dong_sai": 0})
        n["ca"].add(r["ca_id"])
        n["so_dong"] += 1
        n["so_dong_sai"] += r["dung"] == "sai"
    return [{"tai_khoan": tk, "che_do": cd, "so_ca": len(n["ca"]), "so_dong": n["so_dong"], "so_dong_sai": n["so_dong_sai"]}
            for (tk, cd), n in nhom.items()]


def ghi_csv(rows, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as f:  # có BOM để Excel đọc đúng tiếng Việt
        w = csv.DictWriter(f, fieldnames=COT)
        w.writeheader()
        w.writerows(rows)
    return path


if __name__ == "__main__":
    from src.app import LOG_PATH, TU_TAO_PATH, load_env
    sys.stdout.reconfigure(encoding="utf-8")
    load_env()
    dong = tao_dong(luu_tru.tao_kho(TU_TAO_PATH, LOG_PATH).doc_ket_qua_do())
    file = ghi_csv(dong, ROOT / "logs" / f"ket-qua-do-{datetime.now():%Y%m%d-%H%M%S}.csv")
    for t in tom_tat(dong):
        print(f"{t['tai_khoan']} | {t['che_do']:8} | {t['so_ca']} ca | {t['so_dong']} dòng | {t['so_dong_sai']} dòng sai")
    print(f"Đã ghi {len(dong)} dòng vào {file}")
