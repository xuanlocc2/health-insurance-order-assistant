# 07 — PRD: Trợ lý tích BHYT cho bác sĩ Nhi (MVP)

**Trạng thái:** nháp 12/11/2026 · **Phạm vi thời gian:** demo cuối tuần 5 · **Chi tiết thiết kế:** [02-giai-phap.md](02-giai-phap.md) · **Spec kỹ thuật:** viết sau PRD

## 1. Vấn đề

Bác sĩ tự tích BHYT cho từng dòng xét nghiệm/CĐHA, không có công cụ hỗ trợ. Tích sai thì 3–6 tháng sau bị xuất toán và bác sĩ phải bù tiền; bỏ sót thì bệnh nhân mất quyền lợi. Chi tiết: [01-bai-toan.md](01-bai-toan.md).

## 2. Người dùng và thời điểm

- **Người dùng duy nhất:** bác sĩ khám ngoại trú Trung tâm Nhi (gồm phòng khám Ngoại Nhi).
- **Thời điểm:** lúc tích BHYT cho các dòng đã chỉ định, ở cả hai lần: lần 1 trước khi làm và lần 2 sau khi có kết quả.
- **Việc người dùng cần làm xong:** tích đúng từng dòng, và giữ được căn cứ để giải trình nếu bị hỏi lại.

## 3. Mục tiêu MVP

Chứng minh tính khả thi, không đặt mục tiêu hiệu năng:
1. Vấn đề có thật (khảo sát và bấm giờ).
2. Kiểm tra được bằng rule và AI trên 50 dịch vụ (bảng phủ rule).
3. Chạy đúng trên bộ test đủ thật, và bắt được những ca mà hệ chỉ dùng rule bỏ sót.

## 4. Phạm vi

| Trong MVP | Ngoài MVP | Không bao giờ làm |
|---|---|---|
| 50 dịch vụ XN/CĐHA/TDCN ([danh sách](../data/danh-muc/nhi-ngoai-tru-de-xuat.md)) | Thuốc, PT/TT, nội trú | Chẩn đoán, gợi ý hoặc đổi mã ICD |
| Điều kiện riêng của 3 dịch vụ: CRP, Procalcitonin, Doppler tim | Tích hợp thật Eform/VIS, mapping mã nội bộ | Gợi ý thêm chỉ định để được chi trả |
| Thẻ: hết hạn, mức hưởng trẻ < 6 tuổi | Tuyến, giấy chuyển | Tự tích thay bác sĩ |
| Màn hình mô phỏng, dữ liệu giả | Phân quyền xem log | Đánh giá chỉ định đúng/sai chuyên môn |
| | AI biên dịch luật, học từ xuất toán, gói giải trình | Sinh hoặc sửa nội dung bệnh án |

## 5. Yêu cầu chức năng

**Must** (thiếu thì không demo được)

| Mã | Yêu cầu |
|---|---|
| F-01 | Với mỗi dòng chỉ định, trả về một trong 4 trạng thái kèm một câu lý do: Phù hợp quy tắc BHYT / Cần xem lại · đủ căn cứ / Cần xem lại / Không được chi trả |
| F-02 | Mỗi lần tích chạy mọi kiểm tra trên dữ liệu đang có. Vế thiếu dữ liệu ghi "chưa đủ dữ liệu", dòng đó ra Cần xem lại |
| F-03 | R1: dịch vụ không có trong danh mục BHYT → Không được chi trả; chưa xác minh → Cần xem lại |
| F-04 | R2: thẻ hết hạn → Không được chi trả; hiển thị mức hưởng |
| F-05 | R3: kiểm tra từng vế điều kiện có cấu trúc (tuổi, sinh hiệu theo ngưỡng tuổi, ICD) của 3 dịch vụ có điều kiện. Chỉ dùng căn cứ thành văn |
| F-06 | R4: dịch vụ trùng trong cùng lượt khám → Cần xem lại (văn bản không có điều khoản nên không kết luận Không được chi trả). PCT làm lại < 24 giờ → Không được chi trả; 24–48 giờ → Cần xem lại |
| F-07 | A1: với vế văn xuôi, đọc phiếu khám và trả ✅ kèm trích dẫn nguyên văn, ⚠️ "chưa thấy", hoặc "rơi vào điều khoản loại trừ". A1 cũng trích số liệu nằm trong chữ để rule so ngưỡng |
| F-08 | Code kiểm tra trích dẫn của A1 khớp nguyên văn phiếu khám; không khớp thì vế đó thành "chưa thấy" |
| F-09 | AI không bao giờ đưa một dòng tới "Phù hợp quy tắc BHYT", và không tự gây "Không được chi trả", kể cả qua số liệu AI trích từ phiếu khám. Thiếu dữ liệu hoặc không có nhánh điều kiện áp dụng → Cần xem lại |
| F-10 | Điền sẵn ô BHYT: Phù hợp và Cần xem lại · đủ căn cứ → tích sẵn (dòng đủ căn cứ tô màu đoạn trích); hai trạng thái còn lại → để trống. Bác sĩ phải bấm xác nhận |
| F-11 | Nút "Vì sao?": mẫu câu + nguyên văn căn cứ và checklist từng vế. Không dùng LLM |
| F-12 | Khi bỏ tích dòng được tích sẵn, hoặc tích dòng Không được chi trả, bác sĩ chọn nhanh một lý do: Người nhà yêu cầu → tự túc / Loại trừ, theo dõi nghi ngờ / Khác. Dòng Cần xem lại chọn gì cũng không cần lý do. Không chặn |
| F-13 | Lịch sử chỉ ghi thêm (JSONL): mỗi lần xác nhận lưu trạng thái, lựa chọn, lý do, căn cứ nguyên văn, phiên bản rule, đoạn trích A1. Khóa = mã lượt khám + mã dịch vụ |
| F-14 | Màn hình mô phỏng: chọn ca từ bộ mock, gồm thông tin thẻ, sinh hiệu, ICD (có thể trống), phiếu khám, danh sách chỉ định, sidebar trạng thái |

**Should** (có thì tốt, cắt đầu tiên nếu trễ)
- S-01: chạy hàng loạt bộ test và xuất bảng so sánh với nhãn kỳ vọng và với hệ chỉ rule.
- S-02: xem lại lịch sử của một lượt khám trên màn hình.

**Won't (MVP):** chatbot hỏi đáp, tích hợp hệ thống thật, chỉnh rule qua giao diện.

## 6. Yêu cầu phi chức năng

- Chỉ dữ liệu giả; không đưa dữ liệu bệnh nhân thật ra LLM bên ngoài.
- Một lượt khám (≤ 10 dòng) trả kết quả trong khoảng < 10 giây *(đề xuất, đo lại khi có A1)*.
- Mỗi rule ghi văn bản căn cứ và ngày hiệu lực. Câu chữ theo nguyên tắc CDI: chỉ nói "chưa thấy", không bao giờ nói "hãy ghi Y".

## 7. Tiêu chí nghiệm thu

Ca lấy từ [a1-seed.yaml](../data/test-cases/a1-seed.yaml); các ca còn lại sẽ bổ sung vào bộ test.

| Mã | Ca | Kết quả mong đợi |
|---|---|---|
| AC-01 | A1-01: CRP, 4 tháng, sốt sau tiêm | Cần xem lại, ô trống; vế "ổ nhiễm trùng" = chưa thấy, có trích các câu phủ định |
| AC-02 | A1-02: CRP, amidan có mủ | Cần xem lại · đủ căn cứ, tích sẵn, đoạn trích khớp nguyên văn |
| AC-03 | A1-03: ô nhịp thở trống, "thở nhanh 58 l/p" trong phiếu | A1 trích 58, rule kết luận đạt (≥ 50) |
| AC-04 | A1-04: PCT ngoại trú, trẻ tỉnh | Cần xem lại, cả hai nhánh = chưa thấy |
| AC-05 | A1-05: PCT tái khám, hết sốt | Cần xem lại (không phải Không được chi trả), có đánh dấu điều khoản loại trừ |
| AC-06 | Test nhanh RSV | Phù hợp quy tắc BHYT, hậu tố "cách hiểu tạm M-13" (giả định GD-01: thu theo mã chung "Virus test nhanh", [10](10-gia-dinh.md)) |
| AC-07 | Siêu âm ổ bụng + ICD R10.4 | Phù hợp quy tắc BHYT, A1 không chạy |
| AC-08 | CRP chỉ định 2 lần cùng lượt | Dòng thứ hai: Cần xem lại, lý do "trùng dòng" (R4) |
| AC-09 | Thẻ hết hạn | Mọi dòng: Không được chi trả (R2) |
| AC-10 | CRP, không có sinh hiệu ở ô riêng lẫn trong phiếu | Cần xem lại, vế sinh hiệu = chưa đủ dữ liệu |
| AC-11 | Trích dẫn A1 bị sửa một chữ | Vế đó thành chưa thấy |
| AC-12 | Bác sĩ bỏ tích dòng Phù hợp | Bắt chọn lý do; log có đủ trường F-13 |
| AC-13 | CRP, ô nhiệt độ trống, phiếu ghi "T° 37,5" | Cần xem lại (số do AI trích không được gây Không được chi trả) |
| AC-14 | Kết luận dựa trên cách hiểu tạm (vd PCT-04) | Lý do có hậu tố "cách hiểu tạm M-xx, chưa được bác sĩ duyệt" |

## 8. Chỉ số thành công (đo tuần 5)

| Chỉ số | Cách đo | Mục tiêu |
|---|---|---|
| Thời gian và mức tự tin khi tích BHYT | Khảo sát 7 câu + bấm giờ 5–10 lượt ([03](03-kha-thi.md)) | Có số liệu |
| Tỉ lệ phủ rule | X% rule hoàn toàn / Y% cần A1 / Z% không kiểm được | Có bảng |
| Đúng trên bộ test | 50–100 ca, theo dòng và theo từng vế | Báo cáo theo rule |
| Đồng thuận với bác sĩ | ~30 ca bác sĩ gán nhãn | Báo cáo |
| **An toàn** | Số dòng công cụ báo "Phù hợp" nhưng bác sĩ gán là thiếu căn cứ | 0 |
| An toàn (dòng tích sẵn có AI) | Số dòng "Cần xem lại · đủ căn cứ" nhưng bác sĩ gán là thiếu căn cứ | Báo cáo; cao thì đổi dòng này sang để trống |
| Giá trị của A1 | Số ca hệ chỉ rule báo Phù hợp nhưng hồ sơ thiếu căn cứ, A1 bắt được | Báo cáo (ca chính để demo) |
| Trích dẫn | Tỉ lệ trích dẫn A1 qua kiểm tra nguyên văn | Báo cáo; trích dẫn bịa không bao giờ hiện ra |

## 9. Phụ thuộc và giả định

| Phụ thuộc | Ảnh hưởng nếu chưa có | Phương án tạm |
|---|---|---|
| Bác sĩ trả lời [phiếu hỏi](08-phieu-hoi-bac-si.md) (danh sách 50, M-xx, cách điền sẵn) | Ngưỡng và rule CRP/PCT chưa chốt | Dùng cách hiểu tạm, ghi `nguon: tu_dung` |
| ICD nhập trước hay sau khi tích | Nhiều dòng "chưa đủ dữ liệu" ở lần 1 | F-02 xử lý cả hai trường hợp; quan sát tại khoa |
| File Excel BHYT của viện | Thiếu lớp ghi đè | Chỉ dùng TT 35/2016 sđ TT 39/2024 |
| Ca xuất toán kể lại | Demo thiếu ca thật | Mở đầu demo bằng ca A1-01 |

## 10. Mốc

| Tuần | Đầu ra |
|---|---|
| 2 (hiện tại) | PRD, phiếu hỏi bác sĩ, checklist vế CRP/PCT/Doppler, bộ mock bắt đầu |
| 3 | Spec (schema nhánh → vế → loại trừ), rule R1–R4, bộ test 50–100 ca |
| 4 | A1 + kiểm tra trích dẫn, màn hình mô phỏng, log, bác sĩ gán nhãn ~30 ca |
| 5 | Đo chỉ số mục 8, báo cáo, demo |

Chi tiết từng việc: [05-ke-hoach.md](05-ke-hoach.md).
