# 02 — Giải pháp

Với mỗi dòng đã chỉ định, công cụ trả về một trạng thái kèm lý do, đặt ngay cạnh ô tích BHYT của bác sĩ.

## Người dùng và phạm vi

Người dùng duy nhất của MVP: bác sĩ khám ngoại trú Trung tâm Nhi, tại thời điểm tích BHYT cho các dòng đã chỉ định.

**Trong phạm vi**
- Xét nghiệm, CĐHA, dịch vụ kỹ thuật được chỉ định trong lượt khám ngoại trú
- 50 dịch vụ chỉ định nhiều nhất ([danh sách chốt](../data/danh-muc/nhi-ngoai-tru-de-xuat.md))
- Kiểm tra thông tin thẻ liên quan đến mức hưởng (trẻ dưới 6 tuổi, thẻ hết hạn)

**Ngoài phạm vi MVP**
- Thuốc
- Phẫu thuật/thủ thuật, nội trú, ngày giường
- Tích hợp thật vào Eform/VIS
- Hậu kiểm sau khi gửi hồ sơ

**Không bao giờ làm** (ranh giới cứng, kể cả sau MVP)
- Không chẩn đoán, không gợi ý hoặc đổi mã ICD
- Không gợi ý thêm chỉ định để được BHYT chi trả nhiều hơn
- Không tự tích thay bác sĩ — điền sẵn được, bác sĩ phải bấm xác nhận
- Không sửa hoặc sinh nội dung vào hồ sơ bệnh án
- Không đánh giá chỉ định đúng hay sai về chuyên môn, không gợi ý xét nghiệm liên quan

Lý do: công cụ BHYT mà gợi ý chỉ định hay mã bệnh sẽ bị xem là tối ưu thanh toán, và can thiệp vào quyết định chuyên môn.

**Ranh giới khi kiểm tra chẩn đoán (R3):** công cụ chỉ hỏi "hồ sơ đã đủ căn cứ để **thanh toán BHYT** cho dòng này chưa", không hỏi "có nên chỉ định không". Câu chữ là "Hồ sơ chưa có chẩn đoán làm căn cứ thanh toán BHYT", không bao giờ là "chỉ định chưa hợp lý". Bác sĩ xử lý bằng cách bổ sung chẩn đoán đúng thực tế hoặc bỏ tích BHYT; việc chỉ định vẫn giữ nguyên. Chỉ cảnh báo khi có căn cứ thành văn; không có AI tự phán "có vẻ không liên quan".

## Luồng xử lý mỗi dòng

```
Dòng chỉ định → Rule R1–R4 ─┬─ kết luận được → Phù hợp quy tắc / Không được chi trả ─┐
                            ├─ thiếu dữ liệu (vd vế cần ICD mà chưa nhập) → Cần xem lại ─┤
                            └─ điều kiện có vế văn xuôi                       │
                                 → AI A1 đọc phiếu khám → Cần xem lại (· đủ căn cứ) ┤
                                                                            ▼
                                                     Bác sĩ xác nhận → Lưu lịch sử
```

**Mỗi lần tích chạy cùng một luồng** *(chốt 12/11/2026)*: lần 1 (trước khi làm) và lần 2 (sau khi có kết quả) đều chạy mọi kiểm tra trên dữ liệu đang có. Vế nào thiếu dữ liệu (vd cần ICD mà chưa nhập) ghi "chưa đủ dữ liệu" → dòng đó "Cần xem lại". Không chia rule theo lần tích, vì nhiều vế (vd CRP trẻ em: sinh hiệu + phiếu khám) đã kiểm được ngay từ lần 1.

**R2 trong MVP** chỉ gồm: thẻ hết hạn và hiển thị mức hưởng (vd trẻ < 6 tuổi 100%). Không làm tuyến/cấp chuyên môn.

**Màn hình demo:** trang giả lập HIS gồm thông tin bệnh nhân + thẻ, sinh hiệu (ô riêng), ICD (có thể trống), phiếu khám văn bản, danh sách chỉ định, sidebar trạng thái. Bác sĩ chọn ca từ bộ mock, không nhập tay. Công nghệ: rule YAML, engine Python, giao diện web đơn giản.

**Đầu vào:** tuổi (tháng), danh sách dịch vụ đã chỉ định, mã ICD (nếu đã nhập), sinh hiệu (nhiệt độ, mạch, nhịp thở — có thể trống), thông tin thẻ BHYT, nội dung phiếu khám (nếu có), lịch sử chỉ định và kết quả xét nghiệm trước của bệnh nhân.

**Đầu ra cho từng dòng**

| Trạng thái | Nghĩa | Bác sĩ làm gì |
|---|---|---|
| Phù hợp quy tắc BHYT | Qua hết các rule; không phải cam kết BHXH sẽ trả | Tích BHYT |
| Không được chi trả | Vi phạm ít nhất một rule, có lý do và căn cứ | Không tích, hoặc tự kiểm tra lại |
| Cần xem lại · đủ căn cứ | Mọi vế điều kiện đều có căn cứ, nhưng ít nhất một vế do A1 đọc từ phiếu khám (AI không được dẫn tới "Phù hợp") | Đọc lướt đoạn trích rồi xác nhận |
| Cần xem lại | Rule không kết luận được, hoặc có vế chưa thấy căn cứ / rơi vào điều khoản loại trừ; có trích dẫn nếu tìm thấy | Tự quyết định |

**Trải nghiệm bác sĩ**
- Sidebar cạnh danh sách chỉ định, mỗi dòng một trạng thái và một câu lý do; bấm vào để xem căn cứ.
- Công cụ điền sẵn dấu tích theo trạng thái; bác sĩ bấm xác nhận hoặc sửa *(chốt 12/11/2026)*:

  | Trạng thái | Ô BHYT |
  |---|---|
  | Phù hợp quy tắc BHYT | Tích sẵn |
  | Cần xem lại · đủ căn cứ | Tích sẵn, tô màu để bác sĩ đọc lướt đoạn trích (nhãn này sinh ra để bác sĩ đỡ việc) |
  | Cần xem lại | Để trống, bác sĩ tự chọn |
  | Không được chi trả | Để trống |
- Không có nút hay gợi ý kiểu "thêm chỉ định để được chi trả".
- **Lý do khi bỏ qua cảnh báo hoặc bỏ tích:** bác sĩ chọn nhanh một lý do — "Người nhà yêu cầu → chuyển tự túc" / "Loại trừ, theo dõi nghi ngờ (ghi 1 dòng)" / "Khác (ghi 1 dòng)". Không chặn, không phán xét; lý do được lưu vào lịch sử để giải trình và làm số liệu khảo sát (tỉ lệ dòng thiếu căn cứ do người nhà yêu cầu so với chỉ định loại trừ).
- **Lịch sử:** mỗi lần xác nhận lưu lại trạng thái, lý do, căn cứ và lựa chọn của bác sĩ → khi bị xuất toán tra lại được ngay. *(Ý mới từ phần slide Lợi ích, chưa có trong báo cáo Claude Docs.)*
  - Chỉ ghi thêm, không sửa/xóa. Mỗi lần tích (lần 1, lần 2) là một bản ghi riêng.
  - Chép nguyên văn căn cứ và phiên bản rule vào bản ghi (rule sẽ đổi, log thì không).
  - Ảnh chụp đầu vào tối thiểu: ICD, sinh hiệu rule đã dùng, đoạn trích A1. Không chép cả phiếu khám.
  - Khóa nối: mã lượt khám + mã dịch vụ, để ghép thẳng với danh sách xuất toán.
  - Không phải bệnh án; căn cứ pháp lý khi giải trình vẫn là bệnh án.
  - MVP: file JSONL, không phân quyền xem. Phân quyền để viện quyết khi triển khai thật.

**Kiến trúc:** lõi xử lý độc lập với hệ thống bệnh viện — nhận dữ liệu lượt khám, trả trạng thái từng dòng. MVP dùng màn hình mô phỏng; sau này gắn vào Eform hay VIS chỉ cần thay lớp giao diện.

## Ví dụ minh họa (dữ liệu giả)

Lấy từ [a1-seed.yaml](../data/test-cases/a1-seed.yaml) (chi tiết từng vế ở đó).

| Ca | Chỉ định | Trạng thái | Lý do | Ô BHYT |
|---|---|---|---|---|
| A1-02 · 3 tuổi, sốt 39,2°C, amidan có mủ | CRP | Cần xem lại · đủ căn cứ | Sinh hiệu đạt (rule); "nghi ổ nhiễm trùng" có trích dẫn "Amidan 2 bên sưng to, có mủ trắng" (A1) | Tích sẵn, tô màu |
| A1-01 · 4 tháng, sốt sau tiêm | CRP | Cần xem lại | Sinh hiệu đạt, nhưng phiếu khám chưa thấy ổ nhiễm trùng ("sau tiêm vắc xin 6 trong 1", "không ho", "phổi không ran"). Hệ chỉ rule sẽ báo Phù hợp | Để trống |
| (minh họa R4) | CRP chỉ định 2 lần trong cùng lượt khám | Cần xem lại | Trùng trong cùng lượt khám; văn bản không có điều khoản nên không kết luận Không được chi trả (M-15) | Để trống |
| (minh họa) | Siêu âm ổ bụng, ICD R10.4 | Phù hợp quy tắc BHYT | Có trong danh mục, không có điều kiện riêng (M-16) | Tích sẵn |

## Phạm vi Rule-based và AI

BHYT là bài toán chữ ở cả hai đầu: quy định là văn xuôi, hồ sơ cũng là văn xuôi. Rule xử lý phần có cấu trúc ở giữa; **AI làm mọi chỗ cần đọc hiểu, rule giữ quyền kết luận**. AI không bao giờ tự kết luận một dòng là "Phù hợp quy tắc BHYT" — AI sai thì dòng đó thành "Cần xem lại", không bao giờ thành "Phù hợp".

**Nguyên tắc phân vai**
- Kiểm tra được bằng mã/trường có cấu trúc → rule. Rule rẻ, giải thích được, không ảo giác.
- Câu trả lời nằm trong văn bản tự do → AI.
- Mọi đầu ra AI kèm trích dẫn đoạn nguồn; code kiểm tra trích dẫn khớp nguyên văn. Không chắc → "Cần xem lại".

**Rule**

| Mã | Kiểm tra | Dữ liệu cần | Vì sao là rule |
|---|---|---|---|
| R1 | Dịch vụ có trong danh mục BHYT viện đã đăng ký | MVP: dùng thẳng mã/tên chuẩn (mã tương đương TT 23/2024), giả định tên nội bộ không lệch nhiều; mapping mã nội bộ Vinmec để sau khi tích hợp thật | Tra bảng |
| R2 | Thẻ còn hạn; hiển thị mức hưởng (trẻ < 6 tuổi) | Thông tin thẻ | Trường có cấu trúc |
| R3 | Các vế có cấu trúc (tuổi, sinh hiệu, ICD) của điều kiện thành văn; chỉ cho dịch vụ có điều kiện riêng (MVP: CRP, PCT, Doppler) | Checklist nhánh → vế → loại trừ ([spec](09-spec.md)) | So khớp mã/ngưỡng; chỉ dựng từ căn cứ thành văn: TT 35/2016 sđ TT 39/2024, file Excel BHYT của viện, lịch sử xuất toán. Không có bảng ICD ↔ dịch vụ chung (M-14, M-16) |
| R4 | Trùng trong cùng lượt (→ Cần xem lại) hoặc vượt tần suất thành văn (PCT) | Lịch sử chỉ định | So ngày |

**AI trong MVP**

| Mã | Việc | Khi nào chạy | Đầu ra | Vì sao rule không làm được |
|---|---|---|---|---|
| A1 | **Đọc hồ sơ như giám định viên:** đối chiếu từng vế văn xuôi của điều kiện chi trả thành văn (vd CRP: "nghi ổ nhiễm trùng") với phiếu khám. Dịch vụ không có điều kiện riêng thì A1 không chạy, kể cả khi ICD chỉ là triệu chứng (M-16) | Mỗi lần tích, khi điều kiện có vế văn xuôi | Checklist từng vế: ✅ kèm trích dẫn nguyên văn / ⚠️ "chưa thấy trong phiếu khám". Mọi vế ✅ → "Cần xem lại · đủ căn cứ"; còn ⚠️ → "Cần xem lại". Không đánh giá lý do đủ hay không | ~83% tiền bị cắt (2018–2022) đến từ người đọc hồ sơ; từ khóa không xử lý được phủ định ("không sốt") và viết tắt |
| A3 | *Đã cân nhắc và loại (16/11/2026), xem bên dưới.* Lưu ý hồ sơ do AI tự đánh giá | — | — | — |
| A2 | *Đã bỏ (11/11/2026).* Hỏi đáp tự do (chatbot) rủi ro cao, khó kiểm soát và đánh giá | — | — | — |

**Dịch vụ lạc đề với hồ sơ (vd PT, APTT cho trẻ ho sốt) — cách xử lý (chốt 16/11/2026)**

Đã thử A3: AI tự xem hồ sơ có nêu lý do cho từng chỉ định không, gắn nhãn "Hồ sơ chưa nêu lý do chỉ định". **Loại**, vì:
1. Phá nguyên tắc "chỉ cảnh báo khi có căn cứ thành văn"; với Hội đồng chuyên môn đó là hệ thống hỗ trợ quyết định lâm sàng, không còn là công cụ BHYT.
2. Log "hệ thống đã cảnh báo, bác sĩ vẫn chỉ định" thành bằng chứng bất lợi cho chính bác sĩ khi bị xuất toán.
3. Thiệt hại lệch: AI bỏ sót thì không mất gì; AI báo nhầm thì trẻ có thể mất một xét nghiệm cần.
4. Khuyến khích ghi một câu mẫu cho tắt nhãn: dẫn dắt, trái nguyên tắc CDI.
5. Không đo được nếu không có bác sĩ gán nhãn từng cặp (ca, dịch vụ), tức là quay lại dựng chuẩn chuyên môn (M-14).

Thay bằng hai thay đổi không cần AI phán xét:
- **Câu chữ:** dòng chỉ khớp danh mục (không có điều kiện riêng) hiển thị "Có trong danh mục BHYT", không ghi "Phù hợp". Trạng thái lưu trong log giữ nguyên. Chữ "Phù hợp quy tắc BHYT" chỉ còn ở dòng đã qua kiểm tra điều kiện.
- **Nhắc thiếu chẩn đoán chính** ở mức lượt khám, không đổi trạng thái dòng, vì lần tích 1 chỉ định trước khi có chẩn đoán là bình thường. Căn cứ: QĐ 4750/QĐ-BYT, phụ lục bảng chỉ tiêu XML, Bảng 1 trường 26 `MA_BENH_CHINH` (tr. 12) và Bảng 3 trường 35 `MA_BENH` (tr. 41): "Trường hợp không có thông tin ở trường này thì được hiểu là DVKT được chỉ định để điều trị bệnh chính (MA_BENH_CHINH)."

Code A3 giữ lại sau công tắc `LQ_MODE=live` (mặc định tắt) để đo khi có dữ liệu thật; không bật cho người dùng.

**Nút "Vì sao?" trên mỗi dòng:** không dùng LLM — mẫu câu + nguyên văn căn cứ lấy từ YAML của rule. Chắc chắn đúng, không bịa được.

**Ranh giới cho A1 (nguyên tắc CDI — Clinical Documentation Integrity):** câu nhắc không dẫn dắt. Được nói "Điều kiện có vế X; phiếu khám chưa thấy nội dung tương ứng". Không được nói "Hãy ghi Y để được thanh toán".

Checklist từng vế cho các dịch vụ có điều kiện trong MVP (CRP, Procalcitonin, Doppler tim) do nhóm dựng tay từ văn bản, bác sĩ duyệt.

**Nhập nhằng: chốt phần văn bản, AI đọc phần hồ sơ, học dần từ thực tế (chốt 14/11/2026)**

| Loại nhập nhằng | Số lượng | Cách xử lý |
|---|---|---|
| Nghĩa câu chữ trong văn bản (vd "trẻ em" là bao nhiêu tuổi, ngưỡng nhịp nhanh, PCT làm lại < 24h) | Hữu hạn, khoảng 20 điểm ([06](06-diem-mo-ho-bac-si-duyet.md) M-01…M-20) | Bác sĩ chốt một lần → thành rule, áp cho mọi ca |
| Cách bác sĩ ghi phiếu (vd "TD viêm tai", "chưa loại trừ NKH", "ở nhà sốt 39 độ") | Vô hạn, không liệt kê hết | A1 đọc và đoán, kèm trích nguyên văn → bác sĩ xem lại |

- Không cố viết rule cho từng cách ghi phiếu. 45 ca khó ([a1-kho.yaml](../data/eval/a1-kho.yaml)) là bộ đề để **đo** A1 sai bao nhiêu và sai kiểu gì, không phải danh sách để phủ hết.
- AI đoán sai không được làm dòng thành "Phù hợp": cao nhất là "Cần xem lại · đủ căn cứ"; không chắc → "chưa thấy". Chỉ số chặn: số dòng báo thuận lợi hơn kỳ vọng = 0.
- Rủi ro chính là bác sĩ đồng ý theo quán tính (automation bias) → luôn hiện câu trích để nhìn là kiểm được.
- **Học dần từ thực tế:** log ghi lần bác sĩ không đồng ý với A1 và lý do. Cách ghi nào lặp lại nhiều thì mới đưa thành nguyên tắc (hỏi bác sĩ chốt) hoặc thêm vào bộ ca thử. Về sau ghép với danh sách xuất toán (vòng học bên dưới).

**Hướng mở rộng (đề xuất riêng, ngoài MVP): vòng học của từng viện**
- **Biên dịch luật thành rule:** AI đọc điều kiện văn xuôi (~56 dịch vụ trong TT 35/39, file Excel của viện) → đề xuất checklist từng vế + YAML kèm căn cứ, người duyệt.
- **Học từ xuất toán:** AI đọc lý do xuất toán của BHXH, ghép với log → đề xuất rule cho lớp overrides.
- **Cảnh báo dịch vụ lạc đề có căn cứ:** chỉ cảnh báo cặp (dịch vụ, nhóm chẩn đoán) mà BHXH đã từng xuất toán tại chính viện với lý do "chỉ định không phù hợp chẩn đoán", trích đúng biên bản đó. Khác A3 (đã loại): có căn cứ thành văn, không do AI phán xét. Cần dữ liệu xuất toán của viện.
- **Gói giải trình:** gom log + checklist + trích dẫn thành bản nháp giải trình khi bị xuất toán.
- **Mapping tên dịch vụ nội bộ → mã chuẩn** khi tích hợp thật.

Vendor có rule chung; vòng này cho mỗi viện rule riêng, tự cải thiện từ chính lịch sử xuất toán.

## Lợi ích

| Bên | Lợi ích |
|---|---|
| Bác sĩ | Bớt thời gian tích BHYT; không phải học/nhớ quy định; có lịch sử tra lại khi bị xuất toán; ít phải tự bù tiền |
| Bệnh nhân | Không bị bỏ sót quyền lợi BHYT; được giải thích rõ dịch vụ nào được chi trả, vì sao |
| Bệnh viện | Ít bị xuất toán, hồ sơ chính xác hơn; biết lỗi hay gặp để đào tạo, sửa quy trình; có lưu vết khi BHXH hỏi lại |
