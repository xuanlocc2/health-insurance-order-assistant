# AUDIT — kiểm tra độc lập dữ liệu quy tắc (2026-11-14)

Phạm vi: `danh-muc.yaml`, `dieu-kien.yaml`, `tham-so.yaml`, `NGUON.md`, đối chiếu với `docs/09-spec.md` mục 1–8 và `docs/06-diem-mo-ho-bac-si-duyet.md`.

Cách làm:

- Trích lại văn bản từ PDF gốc (không dùng bản trích của lượt trước): Phụ lục TT 39/2024 (22 trang, có lớp chữ), VBHN 17 (52 trang, đọc trên ảnh trang ở những chỗ OCR sai), PL01 TT 23/2024 (624 trang), QĐ 3500 (475 trang), TT 25/2026, PL ICD-10 TT 06/2026.
- Chạy engine thật (`src/engine.py`, `check()`) trên 13 lượt khám dựng riêng để xem dữ liệu hiện tại cho ra kết luận gì.
- Chạy `tests/` (bỏ `tests/test_app.py` vì sandbox chặn ghi file, không liên quan dữ liệu): bộ quy tắc hiện tại cho **4 failed, 160 passed**.

Số trang ghi dưới đây là số trang PDF. "PL TT39" = `2024_TT-39-2024-TT-BYT_phu-luc-DM1-DM2.pdf`.

Lưu ý: thêm file này vào `data/rules/` làm đổi `phien_ban_rule` (sha1 tính trên mọi file trong thư mục).

## 1. Bảng phát hiện

Mức: **blocker** = có thể ra "Không được chi trả" sai, hoặc trái nguyên văn; **major** = sai nhãn nguồn, thiếu mệnh đề phạm vi, mâu thuẫn tài liệu, ca thử sai; **minor** = không đổi kết luận.

| id | File / mục | Mức | Bằng chứng | Sửa đề nghị |
|---|---|---|---|---|
| B-1 | `dieu-kien.yaml` CRP `23.0228.1483`, vế C1 (dòng 81) và D1 (dòng 87) | blocker — **đã có quyết định xử lý** | PL TT39 tr. 9, STT 7 (TT35: 11): "c) Bệnh mạch vành, nhồi máu cơ tim; d) Viêm da nhiễm độc, các bệnh tự miễn." Văn bản không nêu mã ICD nào. YAML dùng hai danh sách tự dựng (`I20`–`I25`; `M30.3, M08, M32, D69.0, L51`) theo kiểu `icd_trong` không có `neu_khong_khop`, nên ICD ngoài danh sách cho `khong_dat`. Chạy engine: trẻ 37,0°C với ICD M33.0 (viêm đa cơ và da, PL ICD tr. 582), D69.3 (tr. 212), L27.0 (tr. 493), K75.4 (viêm gan tự miễn, tr. 480) đều ra **"Không được chi trả"**; M30.3 ra "Phù hợp". `docs/06` M-07 lại ghi cách hiểu tạm là "Chưa áp dụng nhánh d cho đến khi có danh sách ICD". `NGUON.md` mục 3 điểm 2 đã nêu rủi ro này nhưng dữ liệu không giảm rủi ro. | Theo quyết định ngày 14/11: danh sách ICD tự dựng không khớp thì trả `chua_du_du_lieu`, không bao giờ `khong_dat`. ICD khớp vẫn `dat`. Hệ quả cần làm cùng lúc: (1) CRP ở trẻ > 28 ngày không còn ra "Không được chi trả" được nữa, đúng với văn bản vì nhánh c, d là danh sách mở; (2) 4 ca thử đang kỳ vọng "Không được chi trả" phải đổi sang "Cần xem lại": CRP-02, CRP-09, CRP-16, DEMO-03 (tôi đã thử bản `neu_khong_khop: ai_doc` cho C1/D1: đúng 4 ca này đổi kết luận; chưa thử bản `chua_du_du_lieu` vì engine chưa có); (3) sửa `docs/06` M-07 và `NGUON.md` mục 3 điểm 2 cho khớp. |
| B-2 | `dieu-kien.yaml` PCT `23.0130.1549`, `tan_suat.toi_thieu_gio: 24` (dòng 146–151) | blocker — **chưa có quyết định** | PL TT39 tr. 9–10, cột "Tỷ lệ, mức giá thanh toán": "Khi sử dụng xét nghiệm Procalcitonin để theo dõi tình trạng nhiễm trùng nặng và đáp ứng điều trị theo quy định tại khoản 1 Mục này: + Thanh toán tối đa 01 lần/mỗi 24 giờ đối với người bệnh sốc nhiễm trùng; + Thanh toán tối đa 01 lần/mỗi 48 giờ đối với người bệnh nhiễm trùng nặng;". Hai giới hạn bị ràng bởi mệnh đề phạm vi. "nhiễm trùng nặng" là chữ của điểm a (người lớn); điểm b trẻ em dùng "nhiễm trùng huyết" và "suy đa tạng". "khoản 1 Mục này" không tra được trong kho (không có TT 50/2017). Số 24 và 48 có trong văn bản, nhưng việc áp cho mọi lượt PCT của trẻ là tự dựng (`nguon: tu_dung`, M-10). Chạy engine: PCT lặp trong ngày (`ngay_cach: 0`), hồ sơ có ghi nhiễm trùng huyết, ra **"Không được chi trả"**, lý do "Đã làm cách 0 giờ; giới hạn 48 giờ (cách hiểu tạm M-10…)". `docs/06` M-10 chỉ tạm ghi "48 giờ", không có mốc từ chối 24 giờ. | Đổi `toi_thieu_gio: 24` thành `0`. Khoảng [0, 48) giờ vẫn ra "Cần xem lại"; không ca thử nào đổi; `check_rules.py` vẫn OK (đã chạy trên bản sao). Đây là cùng nguyên tắc với B-1: giá trị áp ngoài phạm vi văn bản không được sinh "Không được chi trả". Kèm M-2 (chép thêm mệnh đề phạm vi vào `trich`). |
| M-1 | `dieu-kien.yaml` CRP, vế V1 (dòng 36–43): `nguon: van_ban`, `diem_mo_ho: M-03` | major | Ngưỡng "≤ 36°C hoặc ≥ 38,3°C" đúng nguyên văn (PL TT39 tr. 9). Nhưng với CRP theo dõi, kết luận phụ thuộc M-05 ("Phải thỏa lại"), trong khi văn bản mở đầu bằng "Chẩn đoán, theo dõi một trong các trường hợp sau đây:" (tr. 8). Ca CRP-16 (36,9°C sau 3 ngày kháng sinh, CRP trước 48 mg/L) hiện ra "Không được chi trả". M-05 chỉ nằm trong danh sách đầu mục nên hậu tố lý do không nhắc tới (quan sát: "cách hiểu tạm M-03, M-07, M-01, M-06"). | Sau B-1 ca này thành "Cần xem lại". Vẫn nên ghi `diem_mo_ho: [M-03, M-05]` trên V1 (engine nhận danh sách) để lý do nêu đúng điểm mơ hồ. |
| M-2 | `dieu-kien.yaml` PCT, `tan_suat.trich` và `loai_tru.trich` (dòng 146–163) | major | Hai `trich` bắt đầu từ "+ Thanh toán tối đa…" và "+ Không thanh toán…", bỏ mệnh đề phạm vi đứng ngay trước: "Khi sử dụng xét nghiệm Procalcitonin để theo dõi tình trạng nhiễm trùng nặng và đáp ứng điều trị theo quy định tại khoản 1 Mục này:" (PL TT39 tr. 9). Phần chép thì đúng từng chữ, nhưng bỏ mệnh đề này làm người đọc tưởng giới hạn áp vô điều kiện. `loai_tru`, X1, X2 không gắn `nguon: tu_dung` hay `diem_mo_ho`, dù việc áp loại trừ cho trẻ em, câu hỏi X1 và cách lấy kết quả lần trước đều là cách hiểu (chỉ `@pct_tham_chieu` kéo M-10 vào gián tiếp). Không tự sinh "Không được chi trả" (X1 là `ai_doc`). | Chép mệnh đề phạm vi vào đầu cả hai `trich`. Thêm `nguon: tu_dung, diem_mo_ho: M-10` cho `loai_tru`. |
| M-3 | `dieu-kien.yaml` Doppler `18.0052.0004` vế D1 và Điện tim `02.0085.1778` vế E1 (`khong_cung_luot`); `danh-muc.yaml` dòng #48 | major (hướng an toàn) | Nguyên văn đúng: PL TT39 tr. 22, STT 48 (TT35: 109) "Không thanh toán khi thực hiện dịch vụ kỹ thuật Siêu âm tim có cản âm khi chỉ định thực hiện cùng một thời điểm."; tr. 21, STT 47 (TT35: 104) "Không thanh toán thêm dịch vụ kỹ thuật Điện tâm đồ trong cùng thời điểm lập trình máy tạo nhịp tim." Ba chỗ tự dựng dẫn tới "Không được chi trả" (đã chạy engine, cả hai rule): (1) "cùng (một) thời điểm" = cùng lượt chỉ định; (2) danh sách tên/mã đối ứng: PL01 không có kỹ thuật tên "Siêu âm tim có cản âm" (chỉ có 2.115 "Siêu âm tim cản âm" tr. 22, 2.444 tr. 31, 18.51 "Siêu âm tim, mạch máu có cản âm" tr. 455) và không có "Điện tâm đồ" (chỉ có "Điện tim thường" 2.85 tr. 21, 21.14 tr. 496); (3) tên DM2 "Siêu âm Doppler tim" khớp từng chữ với PL01 2.113 "Siêu âm doppler tim" (QĐ 3500 `02.0113.0004`, tr. 4), không phải 18.52 "Siêu âm doppler tim, van tim" mà rule đang gắn. Dòng #48 trong `danh-muc.yaml` có bí danh "Siêu âm Doppler tim" nhưng **không có `nguon: tu_dung`**; `NGUON.md` dòng 225 tự nhận "Coi hai tên là một dịch vụ là cách hiểu của nhóm". `docs/06` M-11 chỉ nói về Doppler, không phủ "Điện tâm đồ = Điện tim thường". | Rủi ro thấp vì engine chỉ so trong cùng một phiếu chỉ định, sát với "chỉ định thực hiện cùng một thời điểm". Tối thiểu: thêm `nguon: tu_dung, diem_mo_ho: M-11` và `ghi_chu` nêu 2.113 / `02.0113.0004` cho dòng #48; mở rộng M-11 trong `docs/06` sang rule Điện tim. Cần nhóm quyết định: nếu áp nguyên tắc của B-1 cho mọi giá trị tự dựng thì hai rule này phải hạ xuống "Cần xem lại" (ca DOP-02 đổi kỳ vọng). |
| M-4 | `data/test-cases/`: DEMO-01, DEMO-02, R1-01, R1-02 (không phải dữ liệu quy tắc) | major | 4 ca đang đỏ. Ca thử kỳ vọng "Không được chi trả" cho test nhanh RSV, Adenovirus, liên cầu nhóm A; dữ liệu để `xac_minh` nên ra "Cần xem lại". Kết quả tra độc lập: PL01 không có kỹ thuật test nhanh gọi đích danh RSV, Adenovirus hay liên cầu A (chỉ có "RSV Real-time PCR" 24.253, "RSV Ab miễn dịch bán tự động" 24.252 tr. 558; "Adenovirus Real-time PCR" 24.232 tr. 557; "Streptococcus pyogenes ASO" 24.94 tr. 551). Nhưng PL01 có kỹ thuật chung "Virus test nhanh" 24.108 (tr. 551) và "Vi khuẩn test nhanh" 24.2 (tr. 547), cả hai có giá trong QĐ 3500 tr. 452 (`24.0108.1720`, `24.0002.1720`, 261.000). Vì vậy không thể khẳng định "không có trong danh mục"; `xac_minh` là trạng thái bảo vệ được. | Giữ `xac_minh`. Sửa 4 kỳ vọng thành "Cần xem lại". Không chuyển các dòng này sang `khong_thay`. Câu hỏi cho bác sĩ / phòng BHYT: viện có thanh toán test nhanh RSV, Adenovirus, liên cầu A dưới mã 24.108 / 24.2 không. |
| M-5 | `docs/06-diem-mo-ho-bac-si-duyet.md` M-07, M-10, M-11 | major | M-07 mâu thuẫn với YAML (xem B-1). Trích dẫn PCT trong `docs/06` thiếu mệnh đề phạm vi (xem M-2). M-11 không phủ rule Điện tim (xem M-3). Câu trẻ em của CRP trong văn bản in "ô nhiễm trùng" (PL TT39 tr. 9; `nguyen_van` trong YAML giữ đúng lỗi in này), `docs/06` viết "ổ". | Sửa `docs/06` cho khớp văn bản và khớp YAML sau khi xử lý B-1, B-2. |
| m-1 | `dieu-kien.yaml` PCT, quan hệ giữa N1 và N2 | minor | Văn bản điểm b trẻ em là hai gạch đầu dòng, không có chữ "hoặc" (PL TT39 tr. 9). "01 trong 02 tiêu chuẩn" mà `NGUON.md` viện dẫn thuộc điểm a (người lớn). Ghi chú 2 về cách đọc nằm sau DM2 (VBHN 17 tr. 51). Đọc là OR là hướng an toàn (dễ đạt hơn). | Ghi rõ trong `NGUON.md` rằng OR giữa hai gạch là cách hiểu. |
| m-2 | `dieu-kien.yaml` CRP, `a_nguoi_lon` không mã hóa | minor | Trẻ 10 tuổi, 38,1°C, mạch 130, nhịp thở 30, nghi nhiễm trùng: đạt 3/4 tiêu chuẩn điểm a ("- Nhiệt độ cơ thể < 36°c hoặc > 38°C; - Nhịp tim nhanh > 90 lần/phút; - Nhịp thở > 22 lần/phút…", PL TT39 tr. 8) nhưng hiện ra "Không được chi trả" vì trẻ em chỉ xét câu "Đối với trẻ em". Hậu tố có M-01. `NGUON.md` mục 3 điểm 1 đã nêu. | Sau B-1 thành "Cần xem lại". Thêm nhãn `tu_dung` / M-01 ngay tại `a_nguoi_lon`. |
| m-3 | `dieu-kien.yaml` CRP, vế V2 | minor | Văn bản: "nhịp tim hoặc nhịp thở thay đổi quá giới hạn sinh lý theo tuổi" (tr. 9). YAML chỉ mã hóa chiều "nhanh" (≥ ngưỡng); chiều chậm không xét. V2 và `a_tre_em.ap_dung` không ghi `nguon` trực tiếp (lấy qua tham số). Thiếu bảng nhịp tim thì ra `chua_du_du_lieu`, không gây từ chối. | Ghi chú giới hạn này trong `NGUON.md`. |
| m-4 | `danh-muc.yaml`, chú thích đầu file | minor | Ghi "50 dịch vụ" nhưng có 55 dòng (STT 4, 32, 35, 41 tách nhiều dòng). | Sửa chú thích: 50 mục, 55 dòng. |
| m-5 | `danh-muc.yaml` dòng #1 (CTM), #4 (PT/APTT), #32 (Mycoplasma), máu lắng | minor | Chọn biến thể kỹ thuật (CTM laser 22.121 thay vì 22.122; PT/APTT "bán tự động"; Mycoplasma hai mã giá; máu lắng tự động) và bí danh là giả định về máy của viện, không có trong văn bản. Dòng #4, #32 chỉ có `diem_mo_ho: M-13`, không có `nguon: tu_dung`. Không đổi kết luận (đều `co`). | Thêm `nguon: tu_dung` cho các dòng chọn biến thể. |
| m-6 | `data/test-cases/pct.yaml`, `doppler-khac.yaml`, `README.md` | minor | Chú thích cũ: "DM1 mục 8" (đúng là STT 8, TT35 mục 12), "DM2 mục 48" (STT 48, TT35 mục 109), "Mã siêu âm tim cản âm chưa tra" (đã có: `02.0115.0005`, `02.0444.0005`, `18.0051.0005`). | Sửa chú thích. |
| m-7 | `NGUON.md` mục 4 điểm 2 | minor | "khoản 1 Mục này" (PL TT39 tr. 9) không giải được bằng tài liệu trong kho; cần TT 50/2017 hoặc bản TT 35/2016 đã sửa đổi đầy đủ. `NGUON.md` đã nêu. | Bổ sung văn bản vào `data/van-ban/` hoặc giữ nguyên ghi chú. |

Không tìm thấy khẳng định sai trong `NGUON.md`: mọi số trang, số STT và câu trích tôi kiểm đều đúng. Vấn đề của `NGUON.md` là nêu rủi ro (B-1, M-3) mà dữ liệu không xử lý.

## 2. Hướng an toàn — tổng hợp

Đường ra "Không được chi trả" hiện có trong dữ liệu, và căn cứ của từng đường:

| Đường | Căn cứ | Đánh giá |
|---|---|---|
| R1 `khong_thay` | Không có dòng nào `khong_thay` (45 `co`, 4 `dieu_kien`, 6 `xac_minh`) | Không thể xảy ra. Đúng. |
| CRP: mọi nhánh trượt | C1, D1 trượt do danh sách ICD tự dựng | B-1. Sau quyết định 14/11: hết. |
| PCT: lặp dưới 24 giờ | Mốc 24 giờ áp ngoài phạm vi văn bản | B-2. Còn mở. |
| Doppler / Điện tim: cùng phiếu có dịch vụ đối ứng | Nguyên văn có câu "Không thanh toán…", nhưng "cùng thời điểm" và danh sách đối ứng là tự dựng (M-11) | M-3. Gần với chữ văn bản; cần nhóm quyết định. |

## 3. Đã kiểm và đúng

- `nguyen_van` / `trich` của cả 4 rule khớp từng chữ với PL TT39 tr. 8–10, 21, 22, kể cả lỗi in của nguồn ("36°c", "ô nhiễm trùng"). Số STT và số mục TT35 đúng (7/11, 8/12, 47/104, 48/109). Trang đối chiếu VBHN 17 đúng (tr. 27, 27–28, 50, 51; đọc trên ảnh trang).
- Cấu trúc CRP: bốn điểm a, b, c, d là OR ("một trong các trường hợp sau đây"); câu trẻ em là AND ba vế ("nghi ngờ có ô nhiễm trùng, có nhiệt độ… và có nhịp tim hoặc nhịp thở…"). Mã hóa đúng. Ngưỡng nhiệt độ trẻ em "≤ 36°C hoặc ≥ 38,3°C" là số của văn bản.
- Cấu trúc PCT trẻ em: hai gạch đầu dòng; loại trừ cần đủ hai điều kiện ("hết dấu hiệu chỉ định và Procalcitonin ≤ 02 lần giá trị tham chiếu"). Mã hóa đúng (trừ m-1).
- Danh mục: cả 55 dòng khớp PL01 (STT, mã, tên từng chữ, trang) và QĐ 3500 (mã đầy đủ nằm trên trang ghi trong `trang`). Kiểm toàn bộ, không lấy mẫu.
- DM3 (VBHN 17 tr. 52): đúng 16 mục, không mục nào trùng dịch vụ trong danh mục.
- Đọc tuần tự toàn bộ DM1 (15 mục) và DM2 (109 mục; VBHN 17 tr. 31–51 trên ảnh trang, cộng 22 trang PL TT39): không dòng `co` nào có điều kiện trong DM1/DM2. Các tên gần giống mà `NGUON.md` đã loại (DM1 mục 8; DM2 mục 9, 11, 13, 52, 89, 95) đều loại đúng.
- 6 dòng `xac_minh` (Kẽm, RSV, SARS-CoV-2 Ag, Adenovirus, liên cầu A, PCR đa tác nhân): các kỹ thuật ứng viên có trong PL01 đúng như `NGUON.md` ghi; không sót kỹ thuật test nhanh đích danh nào. "Xét nghiệm SARS-CoV-2 Ag test nhanh" có trong PL01 (tr. 563) nhưng không có giá trong QĐ 3500. Dòng #14 Canxi ion hóa: ghi chú QĐ 3500 tr. 429 "Chỉ thanh toán khi định lượng trực tiếp." đúng, gắn `tu_dung` M-12 đúng.
- `tham-so.yaml`: mọi giá trị đều `nguon: tu_dung` kèm mã M đúng (`tre_em_den_thang` 192 tháng / M-01; `nhip_tho_nhanh` 60/50/40 theo [0,2), [2,12), [12,60) tháng / M-02; `nhip_tim_nhanh` bảng rỗng / M-02; `pct_tham_chieu` 0,5 ng/mL / M-10). Khoảng nửa mở, không chồng, không hở; đơn vị đúng. `tuoi_ngay: [0, 29)` = 0–28 ngày, khớp M-06.
- Mã ICD trong các danh sách tồn tại với đúng tên trong PL ICD-10 TT 06/2026 (P36 tr. 810; I20–I25 tr. 399–402; M30.3, M32 tr. 581; M08 tr. 536; D69.0 tr. 212; L51 tr. 496). Mã thì đúng; việc chọn danh sách mới là phần tự dựng (B-1).
- Các trích dẫn khác trong `NGUON.md`: TT 39 thân văn bản tr. 1 (khoản 7 Điều 4); VBHN 17 tr. 6 (khoản 4, 6 Điều 4) và tr. 51 (Ghi chú 1, 2); TT 25/2026 tr. 4; ghi chú QĐ 3500 tr. 429, 430 và ghi chú X-quang "Áp dụng cho 01 vị trí"; PL TT39 tr. 15 STT 19 "Siêu âm tim cản âm".

## 4. Trạng thái xử lý (14/11)

Phần này ghi việc đã làm sau đợt kiểm. Bảng phát hiện ở mục 1 giữ nguyên.

| id | Trạng thái |
|---|---|
| B-1 | Đã chốt cách C: mở rộng danh sách ICD của nhánh d, ICD không khớp vẫn cho "Không được chi trả", lý do nêu rõ phần ICD (`docs/10` GD-02). |
| B-2 | Chưa chốt, tạm giữ `toi_thieu_gio: 24`. Phạm vi giới hạn tần suất tách thành điểm mơ hồ mới M-20 trong `docs/06`; `tan_suat` và `loai_tru` trong YAML nay gắn M-20. |
| M-1 | Xong: V1 gắn `diem_mo_ho: [M-03, M-05]`. |
| M-2 | Xong: hai `trich` có mệnh đề phạm vi; `loai_tru` gắn `nguon: tu_dung`, `diem_mo_ho: [M-10, M-20]`. |
| M-3 | Chưa chốt, tạm giữ "Không được chi trả" khi cùng phiếu. Rule Điện tim nay gắn điểm mơ hồ riêng M-19 ("Điện tâm đồ" = "Điện tim thường"); M-11 ghi rõ chỉ phủ Doppler. |
| M-4 | Thay bằng giả định GD-01 (`docs/10`): ba test nhanh coi như thu theo mã chung "Virus/Vi khuẩn test nhanh" → Phù hợp. |
| M-5 | Xong: `docs/06` sửa M-07, chép đủ mệnh đề phạm vi PCT, tách M-10 / M-20, M-11 nêu chỉ phủ Doppler, thêm M-19, ghi chú lỗi in "ô nhiễm trùng". |
| m-1 | Xong: `NGUON.md` mục 4 điểm 4 ghi rõ đọc N1 hoặc N2 là cách hiểu. |
| m-2 | Xong: nhánh CRP `a_nguoi_lon` gắn `nguon: tu_dung, diem_mo_ho: M-01` (phần tự dựng là "trẻ em chỉ xét câu trẻ em"; mốc < 16 tuổi đã được bác sĩ duyệt); `NGUON.md` mục 3 cập nhật dòng tương ứng. |
| m-3 | Xong: `NGUON.md` mục 3 điểm 4 ghi V2 chỉ xét chiều "nhanh". |
| m-4 | Xong: chú thích đầu `danh-muc.yaml` ghi 50 mục, 55 dòng. |
| m-5 | Xong: gắn `nguon: tu_dung, diem_mo_ho: M-13` cho CTM (#1), máu lắng (#2), PT và APTT (#4, hai dòng), Mycoplasma (#32, hai dòng). Kết luận vẫn Phù hợp, lý do thêm hậu tố "cách hiểu tạm". |
| m-6 | Xong: sửa chú thích `pct.yaml`, `doppler-khac.yaml`, `README.md` của ca thử. |
| m-7 | Giữ ghi chú, kho chưa có TT 50/2017; `NGUON.md` mục 4 điểm 2 nêu văn bản cần bổ sung. |
