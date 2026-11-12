# 01 — Bài toán

Bác sĩ đang phải làm việc của một nhân viên BHYT mà không có công cụ hỗ trợ, và chịu tiền khi làm sai.

## Quy trình hiện tại

1. Bác sĩ khám và chỉ định xét nghiệm/CĐHA/dịch vụ.
2. Với các dòng đã chỉ định, bác sĩ tự tích từng dòng được BHYT chi trả (tính năng mới trên Eform hoặc VIS — chưa xác nhận hệ thống nào, không ảnh hưởng thiết kế).
3. Hồ sơ được gửi lên BHXH.
4. Sau 1–2 quý, BHXH thông báo xuất toán các dòng không hợp lệ. Bác sĩ đã chỉ định phải bù tiền.

## Nỗi đau

- **Tích sai theo hai chiều.** Tích nhầm là được chi trả → bị xuất toán, bác sĩ bù. Bỏ sót dòng được chi trả → bệnh nhân mất quyền lợi.
- **Phản hồi trễ 3–6 tháng.** Khi biết bị xuất toán, bác sĩ không còn nhớ ca bệnh và dễ lặp lại cùng một lỗi nhiều tháng.
- **Không có chỗ dựa.** Viện không có phòng BHYT/KHTH, không có phần mềm kiểm tra BHYT. Bác sĩ tích theo trí nhớ.

## Bằng chứng đã thu thập

| Nguồn | Ghi nhận | Loại |
|---|---|---|
| TC-03 Trung tâm Nhi (nhóm mình) | Bác sĩ không thể vừa xử lý chuyên môn vừa nhớ quy định BHYT; sai thì bác sĩ bù hoặc bệnh nhân mất quyền lợi. **Đã xác nhận: bác sĩ từng phải bù tiền xuất toán.** Xuất toán về 1–2 quý một lần. | Phỏng vấn |
| TC-09 Nội Ung bướu | Hệ thống không gợi ý mục nào BHYT chi trả; bác sĩ dò từng mục, **~3 phút/đơn** (đo trên **thuốc**, không phải xét nghiệm). | Nhóm khác đo |
| TC-16 TMH | Bác sĩ không biết mục nào được bảo hiểm chi trả khi kê đơn (cần hỏi lại là BHYT hay bảo hiểm tư nhân). | Nhóm khác ghi nhận |

Ba nhóm độc lập cùng ghi nhận một điểm nghẽn ở khâu chỉ định. **Chưa có số đo thời gian riêng cho xét nghiệm/CĐHA ở Nhi** — việc cần đo tuần 1.

Chi tiết: [../research/insight-cac-nhom.md](../research/insight-cac-nhom.md), [../research/khao-sat-nhi.md](../research/khao-sat-nhi.md).

## Ý tưởng đã thay đổi thế nào

Ý tưởng bắt đầu là công cụ hậu kiểm cho nhân viên BHYT ([../research/y-tuong-ban-dau.md](../research/y-tuong-ban-dau.md)), rồi chuyển thành công cụ cho bác sĩ ở khâu chỉ định, vì tại viện không có người dùng cho bản đầu tiên.

| Quyết định | Lý do |
|---|---|
| Bỏ hướng *BHYT Evidence & Audit Copilot* (cho nhân viên BHYT, hậu kiểm) | Viện không có phòng BHYT/KHTH và không có phần mềm xử lý BHYT → không có người dùng |
| Chuyển sang hỗ trợ bác sĩ lúc tích BHYT | Đây là nơi duy nhất việc kiểm tra BHYT đang diễn ra, và là nơi duy nhất sửa được lỗi trước khi gửi |
| Không làm thuốc trong MVP | Thu hẹp phạm vi; tập trung xét nghiệm, CĐHA, dịch vụ |
| Không làm phẫu thuật/thủ thuật | Ngoại Nhi tại Times City chỉ là phòng khám ngoại trú, ca mổ đi qua đơn vị khác |
| Không phụ thuộc Eform hay VIS | Chưa chắc hệ thống nào, hệ thống nội bộ khó tích hợp → lõi xử lý độc lập, giao diện gắn sau |
| Đánh giá trên dữ liệu tự dựng, không dùng danh sách xuất toán thật | Danh sách xuất toán liên quan tiền bạc, khó xin; mục tiêu là khả thi, không phải hiệu năng |
| Làm độc lập, không phối hợp nhóm khác | TC-01 và TC-09 cũng chạm BHYT nhưng nhóm chọn đi riêng |
