"""Nơi lưu ca tự tạo, log xác nhận và câu trả lời AI đã nhớ.
Có DATABASE_URL thì lưu ở Neon (bản host: Vercel không ghi được file), không có thì lưu file (máy cá nhân, test).
Tạo bảng trên Neon một lần: python -m src.luu_tru"""
import hashlib
import json
import os
import threading
from datetime import datetime, timezone
from pathlib import Path

import yaml

from src import log

TAI_KHOAN_TAM = "chung"  # ca và log ghi trước khi có đăng nhập
MAX_NHO_FILE = 5000

BANG = """
CREATE TABLE IF NOT EXISTS ca_tu_tao (
    tai_khoan text NOT NULL,
    id text NOT NULL,
    du_lieu jsonb NOT NULL,
    tao_luc timestamptz NOT NULL DEFAULT now(),
    sua_luc timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (tai_khoan, id)
);
CREATE TABLE IF NOT EXISTS xac_nhan (
    id bigserial PRIMARY KEY,
    tai_khoan text NOT NULL,
    luot_kham text,
    kiem_tra_id text,
    ghi_luc timestamptz NOT NULL DEFAULT now(),
    dong jsonb NOT NULL
);
CREATE TABLE IF NOT EXISTS nho_a1 (
    khoa text PRIMARY KEY,
    gia_tri jsonb NOT NULL,
    tao_luc timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS luot_ai (
    tai_khoan text NOT NULL,
    ngay date NOT NULL,
    so integer NOT NULL,
    PRIMARY KEY (tai_khoan, ngay)
);
CREATE TABLE IF NOT EXISTS ket_qua_do (
    tai_khoan text NOT NULL,
    ca_id text NOT NULL,
    du_lieu jsonb NOT NULL,
    luu_luc timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (tai_khoan, ca_id)
);
"""


def _bay_gio():
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def bam_khoa(khoa):
    """Khóa nhớ gồm cả phiếu khám: chỉ lưu mã băm để khóa ngắn và không lặp lại nội dung phiếu."""
    return hashlib.sha256(json.dumps(list(khoa), ensure_ascii=False).encode("utf-8")).hexdigest()


def _dumps(x):
    # Postgres không nhận ký tự NUL trong jsonb
    return json.dumps(x, ensure_ascii=False, default=str).replace("\\u0000", "")


class KhoFile:
    """Một tiến trình trên một máy: ca ghi YAML, log ghi JSONL, câu trả lời AI nhớ trong bộ nhớ."""

    def __init__(self, tu_tao_path, log_path):
        self.tu_tao_path, self.log_path = Path(tu_tao_path), Path(log_path)
        self._khoa = threading.Lock()
        self._nho = {}
        self._luot = {}

    def _doc_ca(self):
        return yaml.safe_load(self.tu_tao_path.read_text(encoding="utf-8")) or [] if self.tu_tao_path.exists() else []

    def _ghi_ca(self, ds):
        tmp = self.tu_tao_path.with_suffix(".tmp")
        tmp.write_text(yaml.safe_dump(ds, allow_unicode=True, sort_keys=False), encoding="utf-8")
        tmp.replace(self.tu_tao_path)  # ghi đè nguyên khối: hỏng giữa chừng không làm mất file cũ

    @staticmethod
    def _cua(c, tai_khoan):
        return c.get("tai_khoan", TAI_KHOAN_TAM) == tai_khoan

    def ds_ca(self, tai_khoan):
        return [{k: v for k, v in c.items() if k != "tai_khoan"} for c in self._doc_ca() if self._cua(c, tai_khoan)]

    def luu_ca(self, tai_khoan, ca):
        with self._khoa:
            ds = self._doc_ca()
            la_no = lambda c: self._cua(c, tai_khoan) and c.get("id") == ca["id"]
            cu = next((c for c in ds if la_no(c)), None)
            now = _bay_gio()
            moi = {**ca, "tai_khoan": tai_khoan, "tao_luc": (cu or {}).get("tao_luc") or now, "sua_luc": now}
            self._ghi_ca(ds + [moi] if cu is None else [moi if la_no(c) else c for c in ds])

    def xoa_ca(self, tai_khoan, ca_id):
        with self._khoa:
            ds = self._doc_ca()
            con = [c for c in ds if not (self._cua(c, tai_khoan) and c.get("id") == ca_id)]
            if len(con) == len(ds):
                return False
            self._ghi_ca(con)
            return True

    def ghi_xac_nhan(self, tai_khoan, rows):
        log.append([{**r, "tai_khoan": tai_khoan} for r in rows], self.log_path)

    def doc_xac_nhan(self, tai_khoan):
        if not self.log_path.exists():
            return []
        rows = [json.loads(x) for x in self.log_path.read_text(encoding="utf-8").splitlines()]
        return [r for r in rows if r.get("tai_khoan") == tai_khoan]

    def doc_nho(self, khoa):
        return {k: self._nho[k] for k in khoa if k in self._nho}

    def ghi_nho(self, moi):
        if len(self._nho) > MAX_NHO_FILE:
            self._nho.clear()
        self._nho.update(moi)

    def tang_luot_ai(self, tai_khoan, ngay):
        with self._khoa:
            self._luot[tai_khoan, ngay] = self._luot.get((tai_khoan, ngay), 0) + 1
            return self._luot[tai_khoan, ngay]

    def luu_ket_qua_do(self, tai_khoan, ket):
        """Mỗi ca chỉ lưu một lần: đã có thì trả False và giữ nguyên kết quả cũ."""
        with self._khoa:
            if any(k["ca_id"] == ket["ca_id"] for k in self.doc_ket_qua_do(tai_khoan)):
                return False
            log.append([{**ket, "tai_khoan": tai_khoan, "luu_luc": _bay_gio()}], self.log_path.with_name("ket-qua-do.jsonl"))
            return True

    def doc_ket_qua_do(self, tai_khoan=None):
        p = self.log_path.with_name("ket-qua-do.jsonl")
        rows = [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines()] if p.exists() else []
        return [r for r in rows if tai_khoan is None or r["tai_khoan"] == tai_khoan]


class KhoNeon:
    """Mỗi lượt mở một kết nối ngắn qua connection pooling của Neon, hợp với hàm serverless."""

    def __init__(self, dsn):
        self.dsn = dsn

    def _ket_noi(self):
        import psycopg  # chỉ cần khi có DATABASE_URL
        # prepare_threshold=None: connection pooling của Neon không giữ prepared statement giữa các lượt
        return psycopg.connect(self.dsn, prepare_threshold=None, connect_timeout=15)

    @staticmethod
    def _json(x):
        from psycopg.types.json import Jsonb
        return Jsonb(x, dumps=_dumps)

    def tao_bang(self):
        with self._ket_noi() as c:
            for lenh in (x.strip() for x in BANG.split(";")):
                if lenh:
                    c.execute(lenh)

    def ds_ca(self, tai_khoan):
        with self._ket_noi() as c:
            rows = c.execute("SELECT du_lieu, tao_luc, sua_luc FROM ca_tu_tao WHERE tai_khoan = %s ORDER BY tao_luc, id",
                             (tai_khoan,)).fetchall()
        return [{**d, "tao_luc": t.isoformat(timespec="seconds"), "sua_luc": s.isoformat(timespec="seconds")}
                for d, t, s in rows]

    def luu_ca(self, tai_khoan, ca):
        with self._ket_noi() as c:
            c.execute("""INSERT INTO ca_tu_tao (tai_khoan, id, du_lieu) VALUES (%s, %s, %s)
                         ON CONFLICT (tai_khoan, id) DO UPDATE SET du_lieu = excluded.du_lieu, sua_luc = now()""",
                      (tai_khoan, ca["id"], self._json(ca)))

    def xoa_ca(self, tai_khoan, ca_id):
        with self._ket_noi() as c:
            return c.execute("DELETE FROM ca_tu_tao WHERE tai_khoan = %s AND id = %s", (tai_khoan, ca_id)).rowcount > 0

    def ghi_xac_nhan(self, tai_khoan, rows):
        if not rows:
            return
        cho = ", ".join(["(%s, %s, %s, %s)"] * len(rows))
        gia_tri = [x for r in rows for x in (tai_khoan, r.get("luot_kham"), r.get("kiem_tra_id"),
                                             self._json({**r, "tai_khoan": tai_khoan}))]
        with self._ket_noi() as c:
            c.execute(f"INSERT INTO xac_nhan (tai_khoan, luot_kham, kiem_tra_id, dong) VALUES {cho}", gia_tri)

    def doc_xac_nhan(self, tai_khoan):
        with self._ket_noi() as c:
            return [r[0] for r in c.execute("SELECT dong FROM xac_nhan WHERE tai_khoan = %s ORDER BY id",
                                            (tai_khoan,)).fetchall()]

    def doc_nho(self, khoa):
        if not khoa:
            return {}
        bam = {bam_khoa(k): k for k in khoa}
        with self._ket_noi() as c:
            rows = c.execute("SELECT khoa, gia_tri FROM nho_a1 WHERE khoa = ANY(%s)", (list(bam),)).fetchall()
        return {bam[k]: v for k, v in rows}

    def ghi_nho(self, moi):
        if not moi:
            return
        dong = {bam_khoa(k): v for k, v in moi.items()}
        cho = ", ".join(["(%s, %s)"] * len(dong))
        gia_tri = [x for k, v in dong.items() for x in (k, self._json(v))]
        with self._ket_noi() as c:
            c.execute(f"""INSERT INTO nho_a1 (khoa, gia_tri) VALUES {cho}
                          ON CONFLICT (khoa) DO UPDATE SET gia_tri = excluded.gia_tri""", gia_tri)

    def tang_luot_ai(self, tai_khoan, ngay):
        with self._ket_noi() as c:
            return c.execute("""INSERT INTO luot_ai (tai_khoan, ngay, so) VALUES (%s, %s::date, 1)
                                ON CONFLICT (tai_khoan, ngay) DO UPDATE SET so = luot_ai.so + 1
                                RETURNING so""", (tai_khoan, ngay)).fetchone()[0]

    def luu_ket_qua_do(self, tai_khoan, ket):
        """Mỗi ca chỉ lưu một lần: đã có thì trả False và giữ nguyên kết quả cũ."""
        with self._ket_noi() as c:
            return c.execute("""INSERT INTO ket_qua_do (tai_khoan, ca_id, du_lieu) VALUES (%s, %s, %s)
                                ON CONFLICT (tai_khoan, ca_id) DO NOTHING""",
                             (tai_khoan, ket["ca_id"], self._json(ket))).rowcount > 0

    def doc_ket_qua_do(self, tai_khoan=None):
        with self._ket_noi() as c:
            rows = c.execute("""SELECT tai_khoan, du_lieu, luu_luc FROM ket_qua_do
                                WHERE %(tk)s::text IS NULL OR tai_khoan = %(tk)s ORDER BY tai_khoan, luu_luc""",
                             {"tk": tai_khoan}).fetchall()
        return [{**d, "tai_khoan": tk, "luu_luc": t.isoformat(timespec="seconds")} for tk, d, t in rows]


def tao_kho(tu_tao_path, log_path):
    dsn = os.environ.get("DATABASE_URL")
    return KhoNeon(dsn) if dsn else KhoFile(tu_tao_path, log_path)


if __name__ == "__main__":
    from src.app import load_env
    load_env()
    KhoNeon(os.environ["DATABASE_URL"]).tao_bang()
    print("Đã tạo bảng: ca_tu_tao, xac_nhan, nho_a1, luot_ai, ket_qua_do")
