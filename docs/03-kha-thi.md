# 03 — Cách chứng minh tính khả thi

Mục tiêu 5 tuần: chứng minh ba điều — vấn đề có thật, làm được về kỹ thuật, chạy được trên dữ liệu đủ thật. Không phải đạt hiệu năng cao.

## 1. Vấn đề có thật — khảo sát bác sĩ + bấm giờ

Phiếu ẩn danh, hỏi theo khoảng, không hỏi số tiền:

1. Trung bình mỗi lượt khám, anh/chị chỉ định bao nhiêu dòng xét nghiệm/CĐHA?
2. Tích BHYT cho một lượt khám mất bao lâu? (< 30 giây / 30 giây–1 phút / 1–3 phút / > 3 phút)
3. Anh/chị tự tin mình tích đúng ở mức nào? (1–5)
4. Khi không chắc, anh/chị làm gì? (theo trí nhớ / hỏi đồng nghiệp / tra văn bản / bỏ không tích)
5. Anh/chị đã từng bị xuất toán phải bù chưa? (chưa / 1 lần / nhiều lần)
6. Khi bị xuất toán, anh/chị có biết rõ mình sai ở dòng nào và vì sao không?
7. Nếu có cảnh báo ngay lúc tích, anh/chị có dùng không?

Kết hợp bấm giờ trực tiếp 5–10 lượt khám để đối chiếu câu 2 (thời gian tự khai thường lệch).

Kết quả khảo sát → lưu vào `../research/` (ví dụ `ket-qua-khao-sat.md`).

## 2. Làm được về kỹ thuật — bảng phủ rule

Với 50 dịch vụ trong danh sách chốt, phân loại theo mẫu (lưu ở `../data/danh-muc/`):

| Dịch vụ | Có trong danh mục BHYT | Điều kiện chi trả | Kiểm tra được bằng rule? | Dữ liệu cần, có sẵn lúc chỉ định không |
|---|---|---|---|---|
| | | | | |

Kết quả mong đợi: *"X% dịch vụ kiểm tra được hoàn toàn bằng rule, Y% cần đọc phiếu khám, Z% không kiểm tra được."*

## 3. Chạy được — bộ test "đủ thật" + demo

- **Thật:** danh mục dịch vụ, mã ICD, rule từ thông tư, cấu trúc lượt khám (từ quan sát).
- **Giả:** thông tin bệnh nhân, nội dung phiếu khám (viết theo mẫu thường gặp).
- 50–100 ca (lưu ở `../data/test-cases/`). Mỗi rule có ca đúng và ca sai, cộng ca biên: thiếu ICD, ICD chung chung, xét nghiệm lặp.
- Dựng lại các ca xuất toán từ lời kể bác sĩ (dịch vụ gì, lý do gì — không cần số tiền). Công cụ phải bắt được.
- Nhờ 1 bác sĩ gán nhãn ~30 ca để đo mức đồng thuận công cụ ↔ bác sĩ.
- **Đo riêng A1 theo từng vế** (không chỉ theo dòng): tỉ lệ vế đúng (dat / chua_thay / loai_tru), tỉ lệ trích dẫn qua kiểm tra nguyên văn, kết quả trên nhóm ca có câu phủ định.
- **So với hệ chỉ dùng rule:** mỗi ca ghi `he_chi_rule` (xem [a1-seed.yaml](../data/test-cases/a1-seed.yaml)). Đếm số ca hệ chỉ rule báo "Phù hợp" nhưng hồ sơ thiếu căn cứ — đây là con số chứng minh giá trị của A1.
- Demo: màn hình mô phỏng sidebar cạnh danh sách chỉ định, chạy trên bộ test.

Báo cáo cuối ghi rõ: kết quả đo trên dữ liệu mô phỏng; đánh giá trên danh sách xuất toán thật là bước tiếp theo nếu triển khai.
