"""Trích mã + tên tiếng Việt từ PL danh mục mã bệnh ICD-10 (TT 06/2026/TT-BYT) ra icd10.tsv.
Chạy một lần: python data/danh-muc/trich_icd10.py   (cần pdfplumber; ~1271 trang)"""
import re
import sys
from pathlib import Path

import pdfplumber

ROOT = Path(__file__).resolve().parents[2]
PDF = ROOT / "data/van-ban/02-ma-dung-chung-chan-doan-xml/2026_TT-06-2026-TT-BYT_PL-danh-muc-ma-benh-ICD10.pdf"
OUT = Path(__file__).with_name("icd10.tsv")
MA = re.compile(r"[A-Z]\d{2}(\.\d{1,2})?\+?\*?")  # cột 17: mã bệnh; cột 21: tên bệnh (tiếng Việt)


def main():
    seen, rows = set(), []
    with pdfplumber.open(PDF) as pdf:
        for i, page in enumerate(pdf.pages):
            for t in page.extract_tables():
                for r in t:
                    if len(r) < 22 or not (r[0] or "").strip().isdigit():
                        continue
                    ma, ten = (r[17] or "").strip(), " ".join((r[21] or "").split())
                    if MA.fullmatch(ma) and ten and ma not in seen:
                        seen.add(ma)
                        rows.append(f"{ma}\t{ten}")
            if i % 100 == 0:
                print(i, len(rows), file=sys.stderr, flush=True)
    OUT.write_text("ma\tten\n" + "\n".join(rows) + "\n", encoding="utf-8")
    print(len(rows), "mã →", OUT)


if __name__ == "__main__":
    main()
