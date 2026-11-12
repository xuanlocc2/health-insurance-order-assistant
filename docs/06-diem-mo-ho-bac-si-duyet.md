# 06 — Điểm mơ hồ cần bác sĩ duyệt trước khi xây rule

**Trạng thái:** bản nháp 11/11/2026, chưa gửi bác sĩ.
**Vì sao cần:** văn bản BHYT viết bằng ngôn ngữ lâm sàng tự do. Nhiều chỗ phải diễn giải mới thành rule được. Nhóm không tự diễn giải; mỗi điểm dưới đây có **cách hiểu tạm** để làm mock, rule chỉ chốt sau khi bác sĩ trả lời.

Căn cứ trích nguyên văn từ phụ lục TT 39/2024 ([file gốc](../data/van-ban/01-dvkt-va-co-so-phap-ly/)) và VBHN 17/VBHN-BYT. Ca minh họa ở [a1-seed.yaml](../data/test-cases/a1-seed.yaml).

**Cách trả lời:** ghi vào cột "Bác sĩ trả lời". Không chắc thì ghi `?` — rule sẽ để "Cần xem lại" ở điểm đó.

## A. CRP (Danh mục 1, mục 7)

> *"Chẩn đoán, theo dõi một trong các trường hợp sau đây: a) Nghi ngờ có ổ nhiễm trùng, có ít nhất 02 trong 04 tiêu chuẩn sau [người lớn]… Đối với trẻ em: Khi nghi ngờ có ổ nhiễm trùng, có nhiệt độ cơ thể ≤ 36°C hoặc ≥ 38,3°C và có nhịp tim hoặc nhịp thở thay đổi quá giới hạn sinh lý theo tuổi. b) Nhiễm trùng sơ sinh; c) Bệnh mạch vành, nhồi máu cơ tim; d) Viêm da nhiễm độc, các bệnh tự miễn."*

| Mã | Câu hỏi | Vì sao mơ hồ | Cách hiểu tạm | Bác sĩ trả lời |
|---|---|---|---|---|
| M-01 | "Trẻ em" tính đến bao nhiêu tuổi? | Văn bản không định nghĩa. Quyết định áp nhánh trẻ em hay nhánh người lớn (2/4 tiêu chuẩn) | Dưới 16 tuổi (Luật Trẻ em) | |
| M-02 | "Giới hạn sinh lý theo tuổi" theo bảng nào, cho cả nhịp tim và nhịp thở? | Văn bản không dẫn bảng | Nhịp thở: ngưỡng WHO (< 2 tháng ≥ 60; 2–11 tháng ≥ 50; 1–5 tuổi ≥ 40). Nhịp tim: **chưa có** | |
| M-03 | Nhiệt độ tính lúc đo tại phòng khám, hay tính cả sốt theo lời kể (đã uống hạ sốt trước khi đến)? | Trẻ hay được hạ sốt ở nhà, đo tại viện 37,5°C | Chỉ tính nhiệt độ đo được và ghi trong hồ sơ | |
| M-04 | "Nghi ngờ có ổ nhiễm trùng": sốt chưa rõ nguồn (nhất là trẻ < 3 tháng) có tính không? Ghi thế nào là đủ? | Ca sốt chưa rõ nguồn rất hay làm CRP | Phải ghi được một ổ hoặc dấu hiệu nghi ngờ cụ thể | |
| M-05 | CRP làm lại để "theo dõi" có phải thỏa lại điều kiện tại thời điểm làm lại không? | Văn bản ghi "chẩn đoán, theo dõi" nhưng điều kiện mô tả lúc chẩn đoán | Phải thỏa lại | |
| M-06 | Nhánh b "Nhiễm trùng sơ sinh": sơ sinh là ≤ 28 ngày? Có cần kèm tiêu chí sinh hiệu không? | Nhánh b đứng riêng, không ghi ngưỡng | ≤ 28 ngày; không cần sinh hiệu | |
| M-07 | Nhánh d "các bệnh tự miễn": ở Nhi gồm bệnh nào? (vd Kawasaki, viêm khớp thiếu niên, lupus, Henoch-Schönlein…) | Không có danh sách | Chưa áp dụng nhánh d cho đến khi có danh sách ICD | |

## B. Procalcitonin (Danh mục 1, mục 8)

> *"b) Đối với trẻ em: Chẩn đoán và theo dõi các trường hợp nhiễm trùng huyết; Theo dõi và tiên lượng suy đa tạng khi có rối loạn chức năng từ 2 cơ quan trở lên."* Tỷ lệ: *"tối đa 01 lần/mỗi 24 giờ đối với người bệnh sốc nhiễm trùng; tối đa 01 lần/mỗi 48 giờ đối với người bệnh nhiễm trùng nặng; không thanh toán đối với các trường hợp đã có bằng chứng chứng minh: hết dấu hiệu chỉ định và Procalcitonin ≤ 02 lần giá trị tham chiếu."*

| Mã | Câu hỏi | Vì sao mơ hồ | Cách hiểu tạm | Bác sĩ trả lời |
|---|---|---|---|---|
| M-08 | "Nhiễm trùng huyết": cần chẩn đoán xác định, hay nghi ngờ là đủ? Ngoại trú Nhi có ca nào đạt không? | "Chẩn đoán" có thể hiểu là đang đi tìm chẩn đoán | Nghi ngờ phải ghi rõ trong hồ sơ | |
| M-09 | "Rối loạn chức năng" mỗi cơ quan ở trẻ dựa theo tiêu chí nào (vd pSOFA)? | Không dẫn tiêu chí | Chưa có, A1 chỉ trích dấu hiệu, không đếm cơ quan | |
| M-10 | "Giá trị tham chiếu" PCT của lab Vinmec là bao nhiêu? Giới hạn 24 giờ/48 giờ có áp cho ngoại trú không? | Phụ thuộc lab; điều khoản viết cho bệnh nặng | Tạm 0,5 ng/mL; 48 giờ | |

## C. Dịch vụ khác trong danh sách 50

| Mã | Câu hỏi | Vì sao mơ hồ | Cách hiểu tạm | Bác sĩ trả lời |
|---|---|---|---|---|
| M-11 | Doppler tim (DM2 mục 48: *"không thanh toán khi thực hiện… Siêu âm tim có cản âm khi chỉ định thực hiện cùng một thời điểm"*): "cùng một thời điểm" là cùng lượt khám hay cùng ngày? Nhi Vinmec có làm siêu âm tim cản âm không? | Không định nghĩa "thời điểm" | Cùng lượt khám; nếu viện không làm siêu âm cản âm thì bỏ rule | |
| M-12 | Canxi ion hóa (*"chỉ thanh toán khi định lượng trực tiếp"*), và nguyên tắc chung *"dịch vụ có kết quả được tính toán từ kết quả của dịch vụ khác"* không được thanh toán: máy Vinmec đo trực tiếp hay tính? Còn chỉ số nào khác là tính toán (vd bilirubin gián tiếp)? | Phụ thuộc máy xét nghiệm | Đo trực tiếp | |
| M-13 | Các dịch vụ không thấy trong danh mục hoặc chưa xác minh: test nhanh RSV, Adenovirus, liên cầu nhóm A; Kẽm; test nhanh SARS-CoV-2; PCR đa tác nhân; Mycoplasma (2 mã giá); PT (nhiều mã theo máy). Vinmec có làm không, đang thu thế nào? | Tra theo bảng giá BV Nhi TW, không phải của Vinmec | "Không thấy" → Không được chi trả; "Xác minh" → Cần xem lại | |

## D. Chỗ văn bản không nói gì

Theo ranh giới đã chốt, tool chỉ cảnh báo khi có căn cứ thành văn. Các câu dưới đây hỏi kinh nghiệm thực tế để quyết định có đưa vào lớp ghi đè của viện hay không.

| Mã | Câu hỏi | Ảnh hưởng | Cách hiểu tạm | Bác sĩ trả lời |
|---|---|---|---|---|
| M-14 | Dịch vụ **không có điều kiện riêng** nhưng thực tế vẫn hay bị cắt vì "không phù hợp chẩn đoán" là dịch vụ nào, với chẩn đoán nào? | Không có căn cứ thành văn thì tool không cảnh báo | Không cảnh báo | |
| M-15 | Văn bản không quy định khoảng cách làm lại cho CTM, CRP… Thực tế BHXH cắt nếu làm lại sau bao lâu? | Quyết định R4 bắt gì | R4 chỉ bắt trùng trong cùng lượt khám | |
| M-16 | ICD chỉ là triệu chứng (R10.4 đau bụng, R50.9 sốt…) kèm dịch vụ không có điều kiện (vd siêu âm bụng): có hay bị cắt không? | Quyết định A1 có cần chạy cho nhóm này | Không cảnh báo, A1 không chạy → "Phù hợp quy tắc BHYT" (chốt 12/11). Hay bị cắt thì bổ sung vào lớp ghi đè | |

## E. Quy trình và dữ liệu

| Mã | Câu hỏi | Ảnh hưởng | Cách hiểu tạm | Bác sĩ trả lời |
|---|---|---|---|---|
| M-17 | Nhiệt độ, mạch, nhịp thở có ô riêng trên Eform/VIS không, hay chỉ ghi trong phiếu khám? | Rule đọc được trực tiếp hay phải nhờ A1 trích | Có ô riêng nhưng hay để trống (mock có cả hai kiểu) | |
| M-18 | ICD nhập trước hay sau mỗi lần tích BHYT? (trùng câu hỏi mở ở [04-rui-ro.md](04-rui-ro.md)) | Bao nhiêu dòng "chưa đủ dữ liệu" ở lần 1 | Mỗi lần tích chạy mọi kiểm tra; vế cần ICD mà chưa có → "chưa đủ dữ liệu" (chốt 12/11) | |
