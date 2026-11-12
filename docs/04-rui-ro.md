# 04 — Rủi ro và câu hỏi mở

**Rủi ro lớn nhất: thời điểm nhập mã ICD.** Nếu ICD thường được nhập *sau* khi tích BHYT, phần lớn rule R3 không chạy được đúng lúc.

| Rủi ro | Ảnh hưởng | Cách xử lý |
|---|---|---|
| ICD chưa có lúc bác sĩ tích BHYT | R3 không chạy; A1 thành bắt buộc | Quan sát ngay tuần 1 thứ tự thao tác thật |
| Bảng dịch vụ ↔ ICD hợp lệ không có sẵn | Phải tự dựng, dễ thiếu/sai | Chỉ dựng từ căn cứ thành văn; điểm mơ hồ gửi bác sĩ duyệt ([06](06-diem-mo-ho-bac-si-duyet.md)); ghi nguồn từng dòng |
| Không có danh sách xuất toán thật | Không đo được hiệu quả thật | Bộ test tự dựng + ca kể lại; ghi rõ giới hạn |
| Quy định BHYT thay đổi (Luật BHYT sửa đổi 2024, thông tư danh mục mới) | Rule lỗi thời | Mỗi rule ghi văn bản căn cứ + ngày hiệu lực; xác nhận văn bản đang hiệu lực |
| Bác sĩ tin mù quáng vào công cụ | Trách nhiệm bị đẩy sang công cụ | Bác sĩ luôn bấm xác nhận; có trạng thái "Cần xem lại" thay vì ép kết luận |
| Tiếp cận dữ liệu bệnh nhân | Chậm tiến độ (TC-13 vẫn chờ phê duyệt) | MVP chỉ dùng dữ liệu giả + danh mục công khai |
| A1 gửi phiếu khám ra LLM bên ngoài | Lộ dữ liệu bệnh nhân khi triển khai thật | Demo dùng dữ liệu giả; triển khai thật chỉ dùng model viện cho phép |
| A1 báo "chưa thấy" quá nhiều | Bác sĩ phiền, bỏ qua cảnh báo | Đo tỉ lệ trên bộ test; chỉ chạy A1 cho vế văn xuôi của điều kiện thành văn |
| A1 bịa đoạn trích | Bác sĩ tin căn cứ không có thật | Code kiểm tra trích dẫn khớp nguyên văn phiếu khám; không khớp → "chưa thấy" |

## Câu hỏi mở

Câu hỏi về diễn giải điều kiện chi trả: xem [06-diem-mo-ho-bac-si-duyet.md](06-diem-mo-ho-bac-si-duyet.md).

- [ ] Mã ICD được nhập trước hay sau khi tích BHYT?
- [ ] Ai gửi hồ sơ lên BHXH và ai báo xuất toán cho bác sĩ?
- [ ] Bác sĩ tích BHYT trên Eform hay VIS? (không chặn MVP)
- [ ] Có lấy được 1–3 ca xuất toán thật qua lời kể, kèm dịch vụ và lý do không?
- [ ] Danh mục dịch vụ BHYT viện đã đăng ký nằm ở đâu, ai giữ?
- [ ] Số "~3 phút/đơn" (TC-09, thuốc) có đúng với xét nghiệm/CĐHA ở Nhi không?
