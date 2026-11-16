"""A1 giả lập cho A1_MODE=stub (spec 09 mục 7, 11b): sinh kết quả từ ky_vong + a1_gia_lap.so_lieu của ca test.

- Câu hỏi khóa "{thu_tu}:{id_ve}" → dòng ky_vong của thu_tu đó → vế cùng id: dat → dat (kèm trich_dan), khác → chua_thay.
- Dòng ky_vong không liệt kê vế nào: dat nếu trang_thai là "Cần xem lại · đủ căn cứ" (vd R4-01, DEMO-01/02), ngược lại chua_thay.
- so_lieu: chỉ trả các trường engine hỏi.
"""
from src.engine import DU_CAN_CU, chuan_hoa


def gan_thu_tu(case):
    """[(thu_tu, dòng ky_vong)]: theo thu_tu nếu có, không thì dòng chỉ định đầu tiên chưa gán khớp ma (hoặc tên)."""
    cds, dung, out = case.get("chi_dinh") or [], set(), []
    for kv in case.get("ky_vong") or []:
        tt = kv.get("thu_tu") or next(
            i for i, cd in enumerate(cds, 1) if i not in dung and (
                cd.get("ma") == kv["ma"] if kv.get("ma") else chuan_hoa(cd.get("ten")) == chuan_hoa(kv.get("ten"))))
        dung.add(tt)
        out.append((tt, kv))
    return out


def make_stub(case):
    ky = dict(gan_thu_tu(case))
    so = (case.get("a1_gia_lap") or {}).get("so_lieu") or []

    def a1(req):
        ve = []
        for q in req.get("cau_hoi") or []:
            tt, vid = q["khoa"].split(":", 1)
            kv = ky.get(int(tt)) or {}
            v = next((v for v in kv.get("ve") or [] if v.get("id") == vid), None)
            if v is not None:
                dat, trich, lq = v.get("ket_qua") == "dat", v.get("trich_dan"), v.get("trich_lien_quan") or []
            else:
                dat, trich, lq = not kv.get("ve") and kv.get("trang_thai") == DU_CAN_CU, kv.get("trich_dan"), []
            ve.append({"khoa": q["khoa"], "ket_qua": "dat" if dat else "chua_thay",
                       "trich_dan": trich if dat else None, "trich_lien_quan": lq})
        muon = {s["truong"] for s in req.get("so_lieu") or []}
        return {"ve": ve, "so_lieu": [s for s in so if s["truong"] in muon], "loi": None}

    return a1
