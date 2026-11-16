# 10 — Giả định đang dùng

**Cập nhật:** 14/11/2026 · **Liên quan:** [06 điểm mơ hồ](06-diem-mo-ho-bac-si-duyet.md) · [09 spec](09-spec.md) · [nguồn rule](../data/rules/NGUON.md) · [audit rule](../data/rules/AUDIT.md)

Mục đích: ghi một chỗ mọi điều hệ thống **đang coi là đúng** dù văn bản không nói rõ hoặc chưa có dữ liệu của Vinmec. Đọc file này để biết một kết quả trên màn hình dựa vào giả định nào, và muốn bỏ giả định thì sửa ở đâu.

- **docs/06 (M-xx)** là câu hỏi gửi bác sĩ. **File này (GD-xx)** là câu trả lời tạm mà hệ đang chạy theo.
- Kết luận nào dựa vào giả định thì câu lý do có hậu tố "(cách hiểu tạm M-xx, chưa được bác sĩ duyệt)". Bảng dưới ghi mã M-xx tương ứng để tra ngược.
- Khi bác sĩ hoặc viện trả lời: sửa dữ liệu theo cột "Gỡ giả định", đổi `nguon` sang `bac_si_duyet` nếu giữ nguyên giá trị, rồi ghi ngày chốt vào đây.

## 1. Giả định về Vinmec

| Mã | Giả định | Ảnh hưởng | Gỡ giả định | M-xx |
|---|---|---|---|---|
| GD-01 | Vinmec đã đăng ký kỹ thuật chung **"Virus test nhanh"** (24.108, mã giá 24.0108.1720) và **"Vi khuẩn test nhanh"** (24.2, mã giá 24.0002.1720), và thu test nhanh RSV, Adenovirus (mã virus) và liên cầu nhóm A (mã vi khuẩn) theo hai mã này | 3 dịch vụ ra **Phù hợp quy tắc BHYT**, ô BHYT tích sẵn, lý do có hậu tố M-13 | `danh-muc.yaml`: 3 dòng đổi `bhyt: co` về `xac_minh`, bỏ `ma_chung` → ra Cần xem lại. Sửa 4 ca: DEMO-01, DEMO-02, R1-01, R1-02 | M-13 |
| GD-03 | Mã dịch vụ và giá lấy theo bảng giá BV Nhi TW (QĐ 3500), không phải mã nội bộ Vinmec. Chưa có file Excel BHYT của viện | Tra danh mục theo mã QĐ 3500 hoặc theo tên/bí danh | Khi có Excel của viện: thêm lớp ghi đè (PRD mục 9) | M-13 |
| GD-04 | Biến thể kỹ thuật theo máy: CTM laser (22.121), PT/APTT bán tự động, máu lắng tự động, Mycoplasma theo một trong hai mã giá. Canxi ion hóa đo trực tiếp | Các dòng này ra Phù hợp | Sửa mã trong `danh-muc.yaml` khi biết máy thật | M-12, M-13 |
| GD-05 | Ngoại trú Nhi Vinmec có làm siêu âm tim cản âm (nên rule Doppler có ý nghĩa) | Doppler cùng phiếu với siêu âm tim cản âm → Không được chi trả | Viện không làm: bỏ rule Doppler trong `dieu-kien.yaml` | M-11 |
| GD-06 | Eform/VIS có ô sinh hiệu riêng nhưng hay để trống; ICD có thể chưa nhập ở lần tích 1 | Ô trống thì A1 trích số từ phiếu khám; thiếu ICD → "chưa đủ dữ liệu" | Quan sát tại khoa | M-17, M-18 |

**Vì sao GD-01 hợp lý.** Không có "danh mục BHYT" riêng: theo TT 35/2016 Điều 1, BHYT chi trả mọi kỹ thuật trong danh mục kỹ thuật (nay là PL01 TT 23/2024), trừ Danh mục 3. PL01 không có dòng tên riêng "test nhanh RSV / Adenovirus / liên cầu A", nhưng có dòng chung "Virus test nhanh" (STT 17689, tr. 551) và "Vi khuẩn test nhanh" (STT 17583, tr. 547); cả hai có giá 261.000đ trong QĐ 3500 (tr. 452) và không nằm trong DM3.

**Rủi ro của GD-01.** (1) Viện không đăng ký hai mã chung → xuất toán. (2) RSV và Adenovirus cùng lượt dùng chung mã 24.0108.1720; BHXH có thể coi là trùng. Hệ **không** cảnh báo trường hợp này vì hai dòng khác tên. Câu 12 trong [phiếu hỏi bác sĩ](08-phieu-hoi-bac-si.md) sẽ chốt.

## 2. Giả định khi đọc văn bản

### GD-02. CRP nhánh c và d: danh sách ICD tự dựng (cách C, chốt 14/11/2026)

**Văn bản** (TT 39/2024 PL, DM1 STT 7, tr. 9): "c) Bệnh mạch vành, nhồi máu cơ tim; d) Viêm da nhiễm độc, các bệnh tự miễn." Không nêu mã ICD, không liệt kê bệnh.

**Hệ đang làm:**
- Nhánh c: ICD bắt đầu bằng I20–I25 thì đạt.
- Nhánh d: ICD bắt đầu bằng một mã trong danh sách sau thì đạt (so theo tiền tố, vd `M08` khớp `M08.0`):

| Nhóm | Mã |
|---|---|
| Viêm da nhiễm độc | L27, L51 (gồm Stevens-Johnson, TEN), L53.0 |
| Tự miễn: khớp, mô liên kết, mạch máu | M05, M06, M08, M09, M30 (gồm Kawasaki M30.3), M31, M32, M33, M34, M35 |
| Tự miễn: máu, da, cơ quan | D69.0 (Henoch-Schönlein), D69.3 (ITP), D59.1, L10, L12, L93, K75.4, E06.3, G70.0 |
| **Chưa đưa vào**, chờ bác sĩ | E10 (đái tháo đường typ 1), K50/K51 (viêm ruột), L40 (vảy nến), G35 (xơ cứng rải rác) |

- Có ICD mà không khớp danh sách → vế trượt. Nếu nhánh a và b cũng trượt → **Không được chi trả**, ô BHYT để trống.
- Chưa có ICD → "chưa đủ dữ liệu" → Cần xem lại.

**Câu lý do nêu đủ hai phần**, để bác sĩ thấy kết luận dựa vào danh sách tự dựng:

> Nhiệt độ ≤ 36°C hoặc ≥ 38,3°C: nhiệt độ 37,2 chưa đạt; ICD R10.4 không thuộc nhóm 'Bệnh mạch vành, nhồi máu cơ tim', 'Viêm da nhiễm độc, các bệnh tự miễn' (cách hiểu tạm M-03, M-05, M-07, …, chưa được bác sĩ duyệt)

**Vì sao chọn cách này.** Giám định viên BHXH cũng xét nhánh d qua mã ICD trên hồ sơ, nên "không có mã bệnh tự miễn → nhánh d không đạt" gần với cách chấm thật. Danh sách rộng hơn bản 5 mã cũ để giảm báo sai ở trẻ có bệnh tự miễn.

**Rủi ro.** Trẻ có bệnh tự miễn ngoài danh sách, không sốt, sẽ bị báo Không được chi trả. Vì ô BHYT của "Cần xem lại" cũng để trống, khác biệt với bác sĩ chủ yếu là nhãn và việc phải chọn lý do khi vẫn tích.

**Gỡ giả định.** `dieu-kien.yaml` vế D1 (và C1): sửa `ds`. Nếu muốn CRP không bao giờ ra Không được chi trả từ danh sách này: thêm `neu_khong_khop: ai_doc` cho C1, D1 (engine đã hỗ trợ); 4 ca CRP-02, CRP-09, CRP-16, DEMO-03 đổi sang Cần xem lại.

### Các giả định đọc văn bản khác

| Mã | Giả định | Ảnh hưởng | M-xx |
|---|---|---|---|
| GD-07 | "Trẻ em" = dưới 16 tuổi (192 tháng): **bác sĩ chốt 14/11**. Phần còn tạm: trẻ em chỉ xét câu "Đối với trẻ em", không xét 02/04 tiêu chuẩn của điểm a | Trẻ 10 tuổi đạt tiêu chuẩn người lớn nhưng chưa đạt câu trẻ em vẫn có thể ra Không được chi trả | M-01 |
| GD-08 | "Quá giới hạn sinh lý theo tuổi": nhịp thở nhanh theo WHO (< 2 tháng ≥ 60; 2–11 tháng ≥ 50; 1–5 tuổi ≥ 40). Nhịp tim theo **thang Úc** (bác sĩ chốt 14/11); bảng cụ thể nhóm chọn là RACGP "Sick child assessment" (vượt cận trên khoảng bình thường): 0–1 tuổi ≥ 161; 1–2 tuổi ≥ 151; 2–5 tuổi ≥ 141; 5–6 tuổi ≥ 121 lần/phút. Chỉ xét chiều nhanh | Mạch nhanh giờ có thể làm vế nhịp tim/thở đạt. Từ 6 tuổi chưa có ngưỡng nhịp tim, từ 5 tuổi chưa có ngưỡng nhịp thở → "chưa đủ dữ liệu". Cần xác nhận bảng RACGP đúng là "thang Úc" bác sĩ dùng, và lấy bảng cho trẻ ≥ 6 tuổi (RCH Melbourne) | M-02 |
| GD-09 | Chỉ tính nhiệt độ đo được và ghi trong hồ sơ, không tính sốt theo lời kể | Trẻ đã hạ sốt ở nhà, đo 37,5°C → vế nhiệt độ trượt | M-03 |
| GD-10 | "Nghi ngờ ổ nhiễm trùng" phải ghi được một ổ hoặc dấu hiệu cụ thể; sốt chưa rõ nguồn chưa đủ | A1 trả "chưa thấy" → Cần xem lại | M-04 |
| GD-11 | CRP làm lại để theo dõi phải thỏa lại điều kiện tại lần làm lại | CRP theo dõi khi hết sốt có thể ra Không được chi trả | M-05 |
| GD-12 | Sơ sinh = 0–28 ngày; nhánh b không cần sinh hiệu; ICD P36 thì đạt, không có thì AI đọc phiếu | | M-06 |
| GD-13 | PCT: "nhiễm trùng huyết" nghi ngờ là đủ nếu ghi rõ; hai gạch đầu dòng của điểm b trẻ em là HOẶC; A1 không tự đếm số cơ quan rối loạn | | M-08, M-09 |
| GD-14 | PCT: giá trị tham chiếu 0,5 ng/mL; giới hạn 24 giờ / 48 giờ và điều khoản loại trừ áp cho mọi lượt PCT của trẻ, dù văn bản viết cho "theo dõi tình trạng nhiễm trùng nặng" | PCT làm lại < 24 giờ → Không được chi trả; 24–48 giờ → Cần xem lại | M-10, M-20 |
| GD-15 | Doppler tim / Điện tim: "cùng một thời điểm" = cùng phiếu chỉ định trong lượt khám. "Siêu âm Doppler tim" của DM2 = dòng 18.52 trong danh mục; "Điện tâm đồ" = "Điện tim thường" | Có dịch vụ đối ứng cùng phiếu → Không được chi trả | M-11, M-19 |
| GD-16 | Dịch vụ không có điều kiện riêng thì không cảnh báo dù ICD chỉ là triệu chứng | Siêu âm bụng + R10.4 → Phù hợp, A1 không chạy | M-14, M-16 |
| GD-17 | Trùng dịch vụ trong cùng lượt → Cần xem lại (văn bản không có điều khoản). Không xét làm lại giữa các lượt (trừ PCT) | | M-15 |
| GD-18 | Thẻ hết hạn trước ngày khám → Không được chi trả. Chưa tìm được câu văn bản nói thẳng (NGUON.md mục 7) | Mọi dòng của lượt khám ra Không được chi trả | — |

## 3. Giả định về hệ thống

- Chỉ dùng dữ liệu giả. Dữ liệu bệnh viện (dù đã ẩn danh) chỉ gửi lên OpenAI sau khi IT/pháp chế đồng ý.
- AI không bao giờ đưa một dòng tới "Phù hợp quy tắc BHYT", và số do AI trích từ phiếu khám không gây "Không được chi trả".
- Tra danh mục: theo mã trước, rồi theo tên hoặc bí danh sau khi chuẩn hóa. Dịch vụ không tra được → Cần xem lại.

## 4. Chưa chốt: tạm giữ bản hiện tại, chờ duyệt sau (quyết định 14/11)

| Việc | Hiện tại | Đề xuất của audit 14/11 |
|---|---|---|
| GD-14, PCT < 24 giờ | Không được chi trả | Đổi `toi_thieu_gio: 24` → `0`, nên mọi lần làm lại < 48 giờ ra Cần xem lại, vì giới hạn viết cho "theo dõi nhiễm trùng nặng" chứ không cho mọi lượt (AUDIT B-2) |
| GD-15, Doppler / Điện tim | Không được chi trả | Giữ (sát chữ "chỉ định cùng một thời điểm"), hoặc hạ xuống Cần xem lại nếu áp nguyên tắc "giá trị tự dựng không gây từ chối" (AUDIT M-3) |

Hệ quả của GD-01 với bộ test: không còn dòng nào trong danh mục ở trạng thái `khong_thay`, nên R1 hiện không có ca "Không được chi trả". AC-06 trong PRD đã đổi theo.
