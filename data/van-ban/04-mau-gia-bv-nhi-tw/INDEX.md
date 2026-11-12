# 04 – Bảng giá mẫu: Bệnh viện Nhi Trung ương

Dùng làm **danh mục mẫu cho Nhi**, vì Vinmec không công khai danh mục DVKT BHYT (xem [research/vinmec-danh-muc-cong-khai.md](../../../research/vinmec-danh-muc-cong-khai.md)). Đây không phải giá Vinmec.

| Số hiệu | Nội dung | Ban hành / hiệu lực | Tình trạng 11/2026 | File | Nguồn |
|---|---|---|---|---|---|
| QĐ 3467/QĐ-BYT | Giá DV KCB tại BV Nhi TW: PL I khám, PL II giường, PL III DVKT + xét nghiệm, PL IV vô cảm gây tê. Gồm cả dịch vụ BHYT và dịch vụ không thuộc BHYT | 15/11/2024, từ ngày ký | PL I và PL III đã được thay bởi QĐ 3500. Chưa kiểm tra có quyết định giá nào mới hơn (2025–2026) hay không | `2024_QD-3467-QD-BYT_gia-KCB-BV-Nhi-TW.pdf` (772 tr., ký số) | benhviennhitrunguong.gov.vn (CT, website bệnh viện) |
| QĐ 3500/QĐ-BYT | Điều chỉnh giá PL I và PL III của QĐ 3467 (thay cả phụ lục) | 19/11/2024, từ ngày ký | Bảng PL III dùng để tra mã, giá | `2024_QD-3500-QD-BYT_dieu-chinh-gia-PL1-PL3-QD3467.pdf` (475 tr., ký số) | benhviennhitrunguong.gov.vn (CT) |

**Cấu trúc PL III:** STT | Mã tương đương (`XX.YYYY.ZZZZ`) | Tên kỹ thuật theo TT 23/2024 | Tên dịch vụ được duyệt giá | Mức giá | Ghi chú.

**Lưu ý khi trích:** PDF có watermark chữ ký số nằm chéo, làm lẫn chữ khi dùng `pdftotext`. Nên trích bằng PyMuPDF và bỏ các dòng có `dir` không nằm ngang. Tên dài bị xuống dòng, tên nằm ở dòng ngay trên dòng chứa mã.
