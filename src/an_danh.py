"""Ẩn thông tin định danh trong phiếu khám trước khi gửi ra ngoài (OpenAI). Chạy trên máy chủ của app.

Thay bằng nhãn: tên người ([TÊN]), số điện thoại ([SĐT]), số thẻ BHYT ([SỐ THẺ]), mã bệnh nhân / số giấy tờ
([MÃ], [SỐ]), email, ngày sinh, địa chỉ có nhãn. KHÔNG đụng số liệu lâm sàng: nhiệt độ, mạch, xét nghiệm,
ngày khám, mã ICD, mã dịch vụ (A1 trích số và trích dẫn từ đây; tests/test_an_danh.py giữ chiều này).

ponytail: lọc theo mẫu nên không bắt được mọi cách viết (tên viết thường, địa chỉ không có nhãn). Đây là lớp
giảm rủi ro, không thay cho việc IT/pháp chế duyệt trước khi dùng dữ liệu thật; bản chắc chắn là LLM chạy trong viện.
"""
import re

# họ phổ biến: cụm ≥ 2 từ viết hoa bắt đầu bằng họ = họ tên người (hoặc địa danh, xóa cũng không sao)
HO = set("Nguyễn Trần Lê Phạm Hoàng Huỳnh Phan Vũ Võ Đặng Bùi Đỗ Hồ Ngô Dương Lý Đinh Đào Trịnh Mai Lương Lâm Tạ "
         "Hà Cao Vương Chu Kiều Tô Quách Đoàn Trương Thái Tôn Phùng Từ Lưu Châu Nghiêm Lại Khúc Kim Thân Triệu Doãn "
         "Hứa Quan Giang Âu Tăng Thạch Mạc Tống Diệp Lục Viên Lã Bạch Đàm Ninh Phí Nông Khổng Ông Mã Bế Hầu Lò Đồng "
         "Vi Đường Văn".split()) - {"Văn"}
# từ xưng hô / nhãn đứng ngay trước tên: "bé An", "mẹ là chị Lan", "Tên: Khôi"
XUNG = set("bé cháu em chị anh ông bà cô chú bác dì mợ mẹ bố ba má tên".split())

_DIA_CHI = re.compile(r"(?i)\b(địa chỉ|đ/c|đc(?=\s*:)|trú tại|thường trú|tạm trú)(\s*:?\s*)[^\n.;]+")
_NGAY_SINH = re.compile(r"(?i)\b(ngày sinh|sinh ngày|dob)(\s*:?\s*)\d{1,2}[/.-]\d{1,2}[/.-]\d{2,4}")
_MA = re.compile(r"(?i)\b(pid|mrn|mã\s*(?:bn|bệnh\s*nhân|hồ\s*sơ|y\s*tế|bhxh|bhyt|thẻ)|"
                 r"số\s*(?:hồ\s*sơ|thẻ|bhxh|bhyt|cccd|cmnd|định\s*danh)|cccd|cmnd)(\s*[:#]?\s*)[A-Za-z]*\d[\w-]*")
_EMAIL = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
_THE = re.compile(r"(?<!\w)[A-Za-z]{2}(?:[ .-]?\d){13}(?!\d)")  # thẻ BHYT: 2 chữ + 13 số, vd TE1010123456789
_SDT = re.compile(r"(?<![\w+])(?:\+84[ .-]?|84[ .-]?|0)\d{2,4}(?:[ .-]?\d{2,4}){1,3}(?!\w)")
_DAI = re.compile(r"(?<![\w.,])\d{9,}(?!\w|[.,]\d)")  # CCCD/CMND/BHXH: dãy ≥ 9 số liền, số lâm sàng không dài vậy
_TU = re.compile(r"[^\W\d_]+")


def _sdt(m):
    """Số VN: 0 + 9 số, hoặc 84 + 9 số; số sau tiền tố là đầu số di động/cố định (2,3,5,7,8,9).
    Khớp dài hơn (vd SĐT rồi tới "12 giờ") thì chỉ xóa phần SĐT."""
    s, d = m[0], re.sub(r"\D", "", m[0])
    can = 11 if d.startswith("84") else 10
    if len(d) < can or d[can - 9] not in "235789":
        return s
    n = 0
    for i, ch in enumerate(s):
        n += ch.isdigit()
        if n == can:
            return "[SĐT]" + s[i + 1:] if i + 1 == len(s) or not s[i + 1].isdigit() else s
    return s


def _hoa(w):  # viết hoa kiểu tên riêng ("An", "Đức", "B"); bỏ chữ viết tắt toàn hoa ("CRP", "TD")
    return w[0].isupper() and (len(w) == 1 or not w[1:].isupper())


def _ten(s):
    tu, xoa, i = list(_TU.finditer(s)), [], 0
    while i < len(tu):
        j = i
        while j < len(tu) and _hoa(tu[j][0]) and (j == i or s[tu[j - 1].end():tu[j].start()] == " "):
            j += 1
        if j == i:
            i += 1
            continue
        cum = tu[i:j]
        if cum[0][0].lower() in XUNG and len(cum) > 1:  # "Bé Minh Anh" đầu câu: bỏ từ xưng hô ra
            cum = cum[1:]
        elif not (len(cum) > 1 and cum[0][0] in HO):
            truoc = tu[i - 1] if i else None
            if not (truoc and truoc[0].lower() in XUNG and re.fullmatch(r"\s*:?\s*", s[truoc.end():tu[i].start()])):
                cum = []
        if cum:
            xoa.append((cum[0].start(), cum[-1].end()))
        i = j
    for a, b in reversed(xoa):
        s = s[:a] + "[TÊN]" + s[b:]
    return s


def an_danh(s):
    if not isinstance(s, str):
        return s
    s = _DIA_CHI.sub(r"\1\2[ĐỊA CHỈ]", s)
    s = _NGAY_SINH.sub(r"\1\2[NGÀY SINH]", s)
    s = _MA.sub(r"\1\2[MÃ]", s)
    s = _EMAIL.sub("[EMAIL]", s)
    s = _THE.sub("[SỐ THẺ]", s)
    s = _SDT.sub(_sdt, s)
    s = _DAI.sub("[SỐ]", s)
    return _ten(s)
