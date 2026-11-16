# Nguồn của từng quy tắc và giá trị

File này là sổ kiểm chứng cho `danh-muc.yaml`, `dieu-kien.yaml`, `tham-so.yaml`. Mỗi quy tắc và mỗi giá trị đều ghi: lấy từ file nào, trang PDF nào, câu nguyên văn, có phải đọc sửa trên ảnh trang không, và phần nào là cách hiểu tự dựng.

Quy ước:

- **Trang** là số trang của file PDF (không phải số trang in). Riêng QĐ 3500, chữ in "Page N" ứng với trang PDF N+1.
- **Nguyên văn** chép đúng chữ, kể cả lỗi in của bản gốc. Chỉ gộp các dòng bị ngắt thành dấu cách.
- **Đọc sửa trên ảnh** nghĩa là lớp chữ của file là OCR có lỗi, câu trích đã được đọc lại trên ảnh trang.
- Mọi file nằm dưới `data/van-ban/`.

## 1. Văn bản đã dùng

| Ký hiệu | File | Lớp chữ | Dùng để |
|---|---|---|---|
| PL01 | `01-dvkt-va-co-so-phap-ly/2024_TT-23-2024-TT-BYT_phu-luc-01_danh-muc-ky-thuat.pdf` | Chữ thật | Tên và mã kỹ thuật (R1) |
| TT 39 PL | `01-dvkt-va-co-so-phap-ly/2024_TT-39-2024-TT-BYT_phu-luc-danh-muc-1-2_dieu-kien-thanh-toan.pdf` | Chữ thật | Điều kiện thanh toán đã sửa đổi (R3) |
| TT 39 | `01-dvkt-va-co-so-phap-ly/2024_TT-39-2024-TT-BYT_sua-doi-TT35-2016.pdf` | Chữ thật | Định nghĩa "một lượt khám bệnh, chữa bệnh" |
| VBHN 17 | `01-dvkt-va-co-so-phap-ly/2024_VBHN-17-2024-BYT_hop-nhat-TT35-2016-DVKT-BHYT.pdf` | OCR, có lỗi | Toàn bộ Danh mục 1, 2, 3 và Điều 4 của TT 35/2016 |
| TT 25/2026 | `01-dvkt-va-co-so-phap-ly/2026_TT-25-2026-TT-BYT_sua-doi-TT23-2024-va-TT32-2023.pdf` | Chữ thật | Hiệu lực của mã kỹ thuật PL01 |
| QĐ 3500 | `04-mau-gia-bv-nhi-tw/2024_QD-3500-QD-BYT_dieu-chinh-gia-PL1-PL3-QD3467.pdf` | Chữ thật | Đối chiếu mã đầy đủ XX.YYYY.ZZZZ và ghi chú giá |
| TT 06/2026 PL | `02-ma-dung-chung-chan-doan-xml/2026_TT-06-2026-TT-BYT_PL-danh-muc-ma-benh-ICD10.pdf` | Chữ thật | Tên các mã ICD-10 trong danh sách tự dựng |
| QĐ 4750 PL | `02-ma-dung-chung-chan-doan-xml/2023_QD-4750-QD-BYT_PL-bang-chi-tieu-XML.pdf` | Chữ thật | Trường hạn thẻ (mục 7) |
| TT 01/2025 | `01-dvkt-va-co-so-phap-ly/2025_TT-01-2025-TT-BYT_huong-dan-Luat-BHYT.pdf` | Chữ thật | Tìm căn cứ về hạn thẻ (mục 7) |

Hai điểm cần biết khi đọc mã:

- **QĐ 3500 là bảng giá của BV Nhi Trung ương, không phải của Vinmec.** Ở đây chỉ dùng để biết mã đầy đủ và ghi chú giá. Vinmec có làm dịch vụ đó không và thu theo mã nào thì chưa biết (M-13).
- TT 25/2026, trang 4, Điều 3, nguyên văn: "Số thứ tự kỹ thuật theo từng chương của Thông tư số 43/2013/TT-BYT và Thông tư số 21/2017/TT-BYT được liệt kê tại cột 2 Phụ lục số 01 của Thông tư này được tiếp tục sử dụng làm mã kỹ thuật của kỹ thuật tương ứng tại Phụ lục số 01 (trừ các kỹ thuật có mã “BS_...”)." Cũng tại Điều 3: PL01 "được thực hiện đến hết ngày 31 tháng 12 năm 2027". Vì vậy các dòng chỉ có mã `BS_...` để `xac_minh`.

**Số thứ tự.** Phụ lục TT 39 có hai cột số: "STT" (đánh lại từ 1 trong phụ lục) và "STT theo TT 35". Tài liệu của dự án (docs/06, ca thử) gọi "DM1 mục 7, mục 8, DM2 mục 48" là theo cột STT của phụ lục TT 39. Trong TT 35 và VBHN 17, ba mục đó là **11, 12 và 109**. `dieu-kien.yaml` ghi cả hai (`stt`, `stt_tt35`).

## 2. Danh mục (R1): `danh-muc.yaml`

### 2.1. Cách tra

Mỗi dịch vụ được tra theo bốn bước:

1. **PL01**: tìm đúng mã kỹ thuật ở cột 2, chép tên. Tên trong `ten` là tên của PL01, không phải tên trong danh sách đề xuất.
2. **QĐ 3500**: tìm đúng mã đầy đủ, ghi trang.
3. **Danh mục 1 (15 mục) và Danh mục 2 (109 mục)** của TT 35/2016: đọc tuần tự toàn bộ trong VBHN 17 (Danh mục 1: trang 20–30; Danh mục 2: trang 31–51) và toàn bộ phụ lục TT 39 (22 trang), không chỉ tìm theo từ khóa. Mục nào có tên gần với một dịch vụ trong danh sách thì ghi lại ở bảng 2.3.
4. **Danh mục 3** (tạm thời chưa thanh toán): VBHN 17 trang 52, đọc trên ảnh trang. TT 39 không sửa Danh mục 3.

Dòng `ma: null` (chưa có mã) chỉ tra bước 1 và 2, nên `da_tra` chỉ có `PL01, QD3500`.

### 2.2. Bảng 55 dòng

Bảng này sinh từ `danh-muc.yaml`. Cột "DM1/2/3" ghi kết quả bước 3 và 4.

| # | Mã | Tên (PL01) | PL01: mã kỹ thuật, STT, trang | QĐ 3500: trang | DM1/2/3 | `bhyt` |
|---|---|---|---|---|---|---|
| 1 | 22.0121.1369 | Tổng phân tích tế bào máu ngoại vi (bằng máy đếm laser) | 22.121, STT 16556, tr. 508 | 418 | Không có (có mục tên gần, xem 2.3) | `co` |
| 2 | 22.0143.1303 | Máu lắng (bằng máy tự động) | 22.143, STT 16578, tr. 509 | 413 | Không có | `co` |
| 3 | 22.0135.1313 | Xét nghiệm hồng cầu lưới (bằng máy đếm laser) | 22.135, STT 16570, tr. 508 | 414 | Không có | `co` |
| 4 | 22.0002.1352 | Thời gian prothrombin (PT: Prothrombin Time), (Các tên khác: TQ; Tỷ lệ Prothrombin) bằng máy bán tự động | 22.2, STT 16437, tr. 502 | 417 | Không có | `co` |
| 4 | 22.0006.1354 | Thời gian thromboplastin một phần hoạt hóa (APTT: Activated Partial Thromboplastin Time) (tên khác: TCK) bằng máy bán tự động | 22.6, STT 16441, tr. 502 | 418 | Không có | `co` |
| 5 | 23.0228.1483 | Định lượng CRP (C-Reactive Protein) | 23.228, STT 17434, tr. 543 | 430 | DM1 mục 11 (TT 39 PL STT 7) | `dieu_kien` |
| 6 | 23.0130.1549 | Định lượng Pro-calcitonin [Máu] | 23.130, STT 17336, tr. 541 | 435 | DM1 mục 12 (TT 39 PL STT 8) | `dieu_kien` |
| 7 | 23.0075.1494 | Định lượng Glucose [Máu] | 23.75, STT 17281, tr. 540 | 431 | Không có | `co` |
| 8 | 23.0166.1494 | Định lượng Urê máu [Máu] | 23.166, STT 17372, tr. 542 | 431 | Không có | `co` |
| 9 | 23.0051.1494 | Định lượng Creatinin (máu) | 23.51, STT 17257, tr. 539 | 431 | Không có | `co` |
| 10 | 23.0020.1493 | Đo hoạt độ AST (GOT) [Máu] | 23.20, STT 17226, tr. 538 | 431 | Không có | `co` |
| 11 | 23.0019.1493 | Đo hoạt độ ALT (GPT) [Máu] | 23.19, STT 17225, tr. 538 | 431 | Không có | `co` |
| 12 | 23.0058.1487 | Điện giải đồ (Na, K, Cl) [Máu] | 23.58, STT 17264, tr. 539 | 430 | Không có | `co` |
| 13 | 23.0029.1473 | Định lượng Canxi toàn phần [Máu] | 23.29, STT 17235, tr. 538 | 429 | Không có | `co` |
| 14 | 23.0030.1472 | Định lượng Canxi ion hóa [Máu] | 23.30, STT 17236, tr. 538 | 429 | Không có | `co` |
| 15 | 23.0143.1503 | Định lượng Sắt [Máu] | 23.143, STT 17349, tr. 541 | 432 | Không có | `co` |
| 16 | 23.0063.1514 | Định lượng Ferritin [Máu] | 23.63, STT 17269, tr. 539 | 433 | Không có | `co` |
| 17 | 23.0027.1493 | Định lượng Bilirubin toàn phần [Máu] | 23.27, STT 17233, tr. 538 | 430 | Không có | `co` |
| 18 | 23.0025.1493 | Định lượng Bilirubin trực tiếp [Máu] | 23.25, STT 17231, tr. 538 | 430 | Không có | `co` |
| 19 | 23.0007.1494 | Định lượng Albumin [Máu] | 23.7, STT 17213, tr. 538 | 431 | Không có | `co` |
| 20 | 23.0055.1489 | Định lượng 25OH Vitamin D (D3) [Máu] | 23.55, STT 17261, tr. 539 | 430 | Không có | `co` |
| 21 | — | Định lượng Kẽm *(tên đề xuất)* | ứng viên BS_23.318 “Định lượng kẽm”, tr. 545; ứng viên 23.249 “Xác định các yếu tố vi lượng (đồng, kẽm)”, tr. 544 | Không có tên riêng | Chưa tra (chưa có mã) | `xac_minh` |
| 22 | 23.0093.1527 | Định lượng IgE (Immunoglobuline E) [Máu] | 23.93, STT 17299, tr. 540 | 434 | Không có | `co` |
| 23 | 23.0162.1570 | Định lượng TSH (Thyroid Stimulating hormone) [Máu] | 23.162, STT 17368, tr. 542 | 437 | Không có | `co` |
| 24 | 23.0069.1561 | Định lượng FT4 (Free Thyroxine) [Máu] | 23.69, STT 17275, tr. 539 | 436 | Không có | `co` |
| 25 | 24.0243.1671 | Influenza virus A, B test nhanh | 24.243, STT 17824, tr. 557 | 443 | Không có | `co` |
| 26 | — | Test nhanh RSV *(tên đề xuất)* | ứng viên 24.108 “Virus test nhanh”, tr. 551; ứng viên 24.252 “RSV Ab miễn dịch bán tự động”, tr. 558; ứng viên 24.253 “RSV Real-time PCR”, tr. 558 | Không có tên riêng | Chưa tra (chưa có mã) | `xac_minh` |
| 27 | — | Test nhanh SARS-CoV-2 (Ag) *(tên đề xuất)* | ứng viên BS_24.374 “Xét nghiệm SARS-CoV-2 Ag test nhanh”, tr. 563 | Không có tên riêng | Chưa tra (chưa có mã) | `xac_minh` |
| 28 | — | Test nhanh Adenovirus *(tên đề xuất)* | ứng viên 24.108 “Virus test nhanh”, tr. 551; ứng viên 24.232 “Adenovirus Real-time PCR”, tr. 557 | Không có tên riêng | Chưa tra (chưa có mã) | `xac_minh` |
| 29 | — | Test nhanh liên cầu nhóm A *(tên đề xuất)* | ứng viên 24.2 “Vi khuẩn test nhanh”, tr. 547; ứng viên 24.94 “Streptococcus pyogenes ASO”, tr. 551 | Không có tên riêng | Chưa tra (chưa có mã) | `xac_minh` |
| 30 | 24.0183.1637 | Dengue virus NS1Ag test nhanh | 24.183, STT 17764, tr. 555 | 441 | Không có | `co` |
| 31 | 24.0187.1637 | Dengue virus IgM/IgG test nhanh | 24.187, STT 17768, tr. 555 | 441 | Không có | `co` |
| 32 | 24.0082.1689 | Mycoplasma pneumoniae Ab miễn dịch bán tự động | 24.82, STT 17663, tr. 550 | 445 | Không có | `co` |
| 32 | 24.0082.1690 | Mycoplasma pneumoniae Ab miễn dịch bán tự động | 24.82, STT 17663, tr. 550 | 446 | Không có | `co` |
| 33 | 24.0249.1697 | Rotavirus test nhanh | 24.249, STT 17830, tr. 558 | 446 | Không có | `co` |
| 34 | — | PCR đa tác nhân hô hấp *(tên đề xuất)* | ứng viên BS_24.377 “Vi sinh vật định danh PCR đa tác nhân (cho trên 3 tác nhân t”, tr. 563; ứng viên BS_24.370 “Vi sinh vật nhiễm khuẩn hô hấp Real - time PCR đa mồi”, tr. 563 | Không có tên riêng | Chưa tra (chưa có mã) | `xac_minh` |
| 35 | 24.0263.1665 | Hồng cầu, bạch cầu trong phân soi tươi | 24.263, STT 17844, tr. 558 | 443 | Không có | `co` |
| 35 | 24.0267.1674 | Trứng giun, sán soi tươi | 24.267, STT 17848, tr. 558 | 444 | Không có | `co` |
| 35 | 24.0265.1674 | Đơn bào đường ruột soi tươi | 24.265, STT 17846, tr. 558 | 443 | Không có | `co` |
| 36 | 24.0005.1716 | Vi khuẩn nuôi cấy, định danh và kháng thuốc hệ thống tự động | 24.5, STT 17586, tr. 547 | 448 | Không có (có mục tên gần, xem 2.3) | `co` |
| 37 | 23.0206.1596 | Tổng phân tích nước tiểu (Bằng máy tự động) | 23.206, STT 17412, tr. 543 | 438 | Không có | `co` |
| 38 | 18.0119.0028 | Chụp X-quang ngực thẳng | 18.119, STT 15103, tr. 456 | 9 | Không có | `co` |
| 39 | 18.0125.0028 | Chụp X-quang bụng không chuẩn bị thẳng hoặc nghiêng | 18.125, STT 15109, tr. 456 | 7 | Không có | `co` |
| 40 | 18.0107.0028 | Chụp X-quang xương cổ tay thẳng, nghiêng hoặc chếch | 18.107, STT 15091, tr. 456 | 10 | Không có | `co` |
| 41 | 18.0106.0028 | Chụp X-quang xương cẳng tay thẳng nghiêng | 18.106, STT 15090, tr. 456 | 10 | Không có | `co` |
| 41 | 18.0114.0028 | Chụp X-quang xương cẳng chân thẳng nghiêng | 18.114, STT 15098, tr. 456 | 10 | Không có | `co` |
| 42 | 18.0015.0001 | Siêu âm ổ bụng (gan mật, tụy, lách, thận, bàng quang) | 18.15, STT 14999, tr. 454 | 3 | Không có | `co` |
| 43 | 18.0001.0001 | Siêu âm tuyến giáp | 18.1, STT 14985, tr. 454 | 4 | Không có | `co` |
| 44 | 18.0004.0001 | Siêu âm hạch vùng cổ | 18.4, STT 14988, tr. 454 | 3 | Không có | `co` |
| 45 | 18.0057.0001 | Siêu âm tinh hoàn hai bên | 18.57, STT 15041, tr. 455 | 4 | Không có | `co` |
| 46 | 18.0043.0001 | Siêu âm khớp (gối, háng, khuỷu, cổ tay….) | 18.43, STT 15027, tr. 455 | 3 | Không có (có mục tên gần, xem 2.3) | `co` |
| 47 | 18.0007.0001 | Siêu âm qua thóp | 18.7, STT 14991, tr. 454 | 4 | Không có | `co` |
| 48 | 18.0052.0004 | Siêu âm doppler tim, van tim | 18.52, STT 15036, tr. 455 | 5 | DM2 mục 109 (TT 39 PL STT 48) | `dieu_kien` |
| 49 | 02.0085.1778 | Điện tim thường | 2.85, STT 487, tr. 21 | 459 | DM2 mục 104 nhắc tới (TT 39 PL STT 47) | `dieu_kien` |
| 50 | 02.0024.1791 | Đo chức năng hô hấp | 2.24, STT 426, tr. 19 | 460 | Không có (có mục tên gần, xem 2.3) | `co` |

### 2.3. Các mục có tên gần nhưng không phải

Đây là các mục trong Danh mục 1, 2 dễ bị nhầm với dịch vụ trong danh sách. Tất cả đọc trên ảnh trang VBHN 17 (đọc sửa trên ảnh).

| Dịch vụ trong danh sách | Mục gần (STT theo TT 35) | Vì sao không phải |
|---|---|---|
| Tổng phân tích tế bào máu ngoại vi (bằng máy đếm laser), 22.121 | DM1 mục 8, trang 26: "Tổng phân tích tế bào máu ngoại vi bằng hệ thống tự động hoàn toàn (có nhuộm tiêu bản tự động)" | Là kỹ thuật khác (22.122) |
| Đo chức năng hô hấp, 2.24 | DM2 mục 11, trang 33: "Đo biến đổi thể tích toàn thân - Body Plethysmography"; DM2 mục 9: đo đa ký hô hấp | Là kỹ thuật khác |
| Vi khuẩn nuôi cấy, định danh và kháng thuốc hệ thống tự động, 24.5 | DM2 mục 89 và 95 | Là dịch vụ vi sinh khác |
| Siêu âm khớp, 18.43 | DM2 mục 13 | Là thủ thuật tiêm khớp dưới hướng dẫn siêu âm |
| Các dòng siêu âm (42–47) | DM2 mục 52 (phụ lục TT 39 STT 23, trang 16): "Siêu âm doppler mạch máu", nguyên văn "Thanh toán 01 lần không phân biệt bên phải hoặc trái đối với hệ thống mạch máu đối xứng." | Là siêu âm doppler mạch máu, không có trong danh sách 50 |

Danh mục 3 (VBHN 17 trang 52, đọc sửa trên ảnh) gồm 16 mục: HIV genotype giải trình tự gene; HBV genotype giải trình tự gene; Điều trị bằng bùn; Điều trị bằng nước khoáng; Luyện tập dưỡng sinh; ANA 17 profile test; Helicobacter pylori giải trình tự gene; Chlamydia giải trình tự gene; Neisseria gonorrhoeae kháng thuốc giải trình tự gene; Vibrio cholerae giải trình tự gene; Vi khuẩn kháng thuốc giải trình tự gene; Rubella virus giải trình tự gene; Influenza virus A, B giải trình tự gene; HPV genotype giải trình tự gene; Enterovirus genotype giải trình tự gene; EV71 genotype giải trình tự gene. Không mục nào thuộc danh sách 50. Dòng "Influenza virus A, B test nhanh" (24.243) là test nhanh, khác "Influenza virus A, B giải trình tự gene".

### 2.4. Trạng thái đã đổi so với danh sách sơ bộ

Danh sách sơ bộ là `data/danh-muc/nhi-ngoai-tru-de-xuat.md`.

**a) Test nhanh RSV, Test nhanh Adenovirus, Test nhanh liên cầu nhóm A: "Không thấy" → `xac_minh`.**

- PL01 không có tên riêng cho ba test này. Tìm trong toàn bộ PL01: tên có "RSV" chỉ gồm 24.252 "RSV Ab miễn dịch bán tự động" và 24.253 "RSV Real-time PCR" (trang 558); tên có "Adenovirus" chỉ gồm 24.232 "Adenovirus Real-time PCR" (trang 557); tên có "Streptococcus" chỉ gồm 24.94 "Streptococcus pyogenes ASO" (trang 551).
- Nhưng PL01 có hai tên chung: mã 24.108 "Virus test nhanh" (STT 17689, trang 551) và mã 24.2 "Vi khuẩn test nhanh" (STT 17583, trang 547). QĐ 3500 trang 452 có giá cho cả hai: "24.0108.1720 Virus test nhanh" và "24.0002.1720 Vi khuẩn test nhanh" (261.000).
- Vì vậy không đủ căn cứ để nói ba test này "không có trong danh mục". Cũng chưa đủ căn cứ để nói chúng được xếp vào tên chung. Để `xac_minh` → công cụ trả "Cần xem lại". Cần hỏi Vinmec: có làm không, và đang ánh xạ vào mã nào.
- Hệ quả: bốn ca thử DEMO-01, DEMO-02, R1-01, R1-02 đang kỳ vọng "Không được chi trả" cho ba test này sẽ không đạt. Nếu nhóm quyết định giữ cách hiểu cũ thì đổi `bhyt: xac_minh` thành `bhyt: khong_thay` ở ba dòng đó.

**b) Điện tim thường (02.0085.1778): "Có" → `dieu_kien`.**

- Phụ lục TT 39, Danh mục 2, STT 47 (STT theo TT 35: 104), trang 21, dòng "Lập trình máy tạo nhịp tim", nguyên văn: "Không thanh toán thêm dịch vụ kỹ thuật Điện tâm đồ trong cùng thời điểm lập trình máy tạo nhịp tim." Đối chiếu VBHN 17 trang 50.
- Điều kiện này đứng ở dòng của dịch vụ khác, nhưng tác động vào việc thanh toán điện tâm đồ. Rule chỉ có một vế (E1): không làm cùng lượt khám với "Lập trình máy tạo nhịp tim" (PL01 mã 2.100, trang 21; QĐ 3500 02.0100.0069, trang 85).
- Tự dựng: coi "Điện tâm đồ" là "Điện tim thường"; coi "cùng thời điểm" là cùng lượt khám (M-19). Ở Nhi ngoại trú gần như không gặp, nên mọi ca thường vẫn ra "Phù hợp". Muốn bỏ: đổi lại `bhyt: co` và xóa mục `02.0085.1778` trong `dieu-kien.yaml`.

**c) Sửa mã so với danh sách sơ bộ (không đổi trạng thái).**

- Kẽm: PL01 ghi "Định lượng kẽm" ở mã BS_23.318 (trang 545). BS_23.317 là "Định lượng đồng".
- Test nhanh SARS-CoV-2: PL01 có mã BS_24.374 "Xét nghiệm SARS-CoV-2 Ag test nhanh" (trang 563).
- PCR đa tác nhân hô hấp: PL01 có BS_24.377 và BS_24.370 (trang 563).
- ASO: mã kỹ thuật là 24.94, không phải 24.95.
- Siêu âm tim cản âm (không thuộc danh sách 50, dùng trong rule Doppler tim): PL01 2.115 "Siêu âm tim cản âm" (trang 22), 2.444 "Siêu âm tim cản âm cấp cứu tại giường" (trang 31), 18.51 "Siêu âm tim, mạch máu có cản âm" (trang 455); QĐ 3500 trang 5: 02.0115.0005, 02.0444.0005, 18.0051.0005.

### 2.5. Các dòng `co` có ghi chú

| Dòng | Ghi chú | Nguồn |
|---|---|---|
| Canxi ion hóa 23.0030.1472 | Ghi chú giá, nguyên văn: "Chỉ thanh toán khi định lượng trực tiếp." Tạm coi máy Vinmec đo trực tiếp nên để `co` (`nguon: tu_dung`, M-12). | QĐ 3500 trang 429. Ghi chú này nằm trong bảng giá BV Nhi TW. Căn cứ chung: điểm b khoản 4 Điều 4 TT 35/2016 (mục 6 dưới đây). |
| Bilirubin toàn phần 23.0027.1493 | Ghi chú giá, nguyên văn: "Không thanh toán đối với các xét nghiệm Bilirubin gián tiếp; Tỷ lệ A/G là những xét nghiệm có thể ngoại suy được." Danh sách 50 không có Bilirubin gián tiếp nên không thành rule. | QĐ 3500 trang 430 |
| Điện giải đồ 23.0058.1487 | Ghi chú giá: "Áp dụng cho cả trường hợp cho kết quả nhiều hơn 3 chỉ số" | QĐ 3500 trang 430 |
| X-quang (mã giá 0028) | Ghi chú giá: "Áp dụng cho 01 vị trí" | QĐ 3500 trang 7–10 |
| PT 22.0002.1352, APTT 22.0006.1354 | Mã trong danh sách là biến thể "bằng máy bán tự động". QĐ 3500 trang 417 còn 22.0001.1352 cùng mã giá. Chưa biết Vinmec dùng mã nào (M-13). | PL01 trang 502 |
| Mycoplasma 24.0082.1689 và 24.0082.1690 | Cùng mã kỹ thuật 24.82, hai mã giá (273.000 và 182.700), cùng tên. Chưa rõ khác nhau ở đâu (M-13). | QĐ 3500 trang 445, 446 |

## 3. CRP: `dieu-kien.yaml` → `23.0228.1483`

**Nguồn.** Phụ lục TT 39, Danh mục 1, STT 7 (STT theo TT 35: 11), trang 8–9. Tên dịch vụ trong văn bản: "Định lượng CRP/CRP hs [Máu]". Đã so với ảnh trang, không sửa chữ nào. Đối chiếu VBHN 17 trang 27.

**Nguyên văn cột "Điều kiện thanh toán":**

> Chẩn đoán, theo dõi một trong các trường hợp sau đây: a) Nghi ngờ có ổ nhiễm trùng, có ít nhất 02 trong 04 tiêu chuẩn sau: - Nhiệt độ cơ thể < 36°c hoặc > 38°C; - Nhịp tim nhanh > 90 lần/phút; - Nhịp thở > 22 lần/phút hoặc PaCO2 <32 mmHg; - Bạch cầu máu >12G/L, hoặc < 4G/L hoặc > 10% bạch cầu non. Đối với trẻ em: Khi nghi ngờ có ô nhiễm trùng, có nhiệt độ cơ thể ≤ 36°C hoặc ≥ 38,3°C và có nhịp tim hoặc nhịp thở thay đổi quá giới hạn sinh lý theo tuổi. b) Nhiễm trùng sơ sinh; c) Bệnh mạch vành, nhồi máu cơ tim; d) Viêm da nhiễm độc, các bệnh tự miễn.

Cột "Tỷ lệ, mức giá thanh toán": "Thanh toán bằng giá DVKT".

Bản in chính thức ghi "36°c" và "ô nhiễm trùng" (ở câu trẻ em). Hai chỗ này giữ nguyên trong `nguyen_van`. Phần `mo_ta` hiển thị cho bác sĩ viết "ổ nhiễm trùng".

| Phần trong rule | Giá trị | Nguồn | Cách hiểu |
|---|---|---|---|
| Nhánh `a_tre_em`, áp cho [0, 192) tháng | 192 tháng | **Tự dựng, M-01** | Văn bản chỉ ghi "Đối với trẻ em", không định nghĩa. Tạm lấy dưới 16 tuổi. |
| V1 | ≤ 36 hoặc ≥ 38,3 °C | **Văn bản**: "có nhiệt độ cơ thể ≤ 36°C hoặc ≥ 38,3°C" | Chỉ tính nhiệt độ đo được, không tính sốt theo lời kể (M-03). |
| V2 | Bảng `@nhip_tho_nhanh`, `@nhip_tim_nhanh` | Câu chữ từ văn bản: "có nhịp tim hoặc nhịp thở thay đổi quá giới hạn sinh lý theo tuổi". **Ngưỡng tự dựng, M-02** | Văn bản không dẫn bảng nào. Xem mục 5. |
| V3 | AI đọc phiếu khám | Văn bản: "Khi nghi ngờ có ô nhiễm trùng" | Phải ghi được một ổ hoặc dấu hiệu cụ thể (M-04). Câu hỏi cho AI chỉ hỏi phiếu khám có ghi hay không. |
| Nhánh `a_nguoi_lon`, áp cho từ 192 tháng | Chưa mã hóa | Văn bản: điểm a) với 02 trong 04 tiêu chuẩn. **Việc trẻ em không xét điểm a) là tự dựng, M-01** (nhãn đặt ngay tại nhánh trong YAML) | Ngoài phạm vi Nhi. Vế không có phép kiểm → "Cần xem lại". |
| Nhánh `b_so_sinh`, áp cho [0, 29) ngày | 0–28 ngày tuổi | Văn bản: "b) Nhiễm trùng sơ sinh;". **Mốc 28 ngày tự dựng, M-06** | Không cần kèm sinh hiệu (M-06). |
| B1 | ICD `P36`, không khớp thì AI đọc | **Tự dựng, M-06** | P36 = "Nhiễm khuẩn hệ thống ở trẻ sơ sinh" (TT 06/2026 PL, trang 810). Văn bản không nêu mã ICD. |
| C1 | ICD `I20`–`I25` | Văn bản: "c) Bệnh mạch vành, nhồi máu cơ tim;". **Danh sách mã tự dựng, M-07** | I20–I25 = nhóm "Ischaemic heart diseases" (TT 06/2026 PL, trang 399–402). |
| D1 | ICD L27, L51, L53.0, M05, M06, M08, M09, M30–M35, D69.0, D69.3, D59.1, L10, L12, L93, K75.4, E06.3, G70.0 (danh sách mở rộng 14/11, docs/10 GD-02) | Văn bản: "d) Viêm da nhiễm độc, các bệnh tự miễn.". **Danh sách mã tự dựng, M-07** | TT 06/2026 PL: M30.3 Kawasaki (trang 581), M08 viêm khớp thiếu niên (trang 536), M32 lupus ban đỏ hệ thống (trang 581), D69.0 ban xuất huyết dị ứng (trang 212), L51 hồng ban đa dạng, gồm L51.2 hoại tử thượng bì nhiễm độc (trang 496). Bản 5 mã đầu tiên lấy theo docs/09-spec.md mục 2; các mã thêm 14/11 chưa đối chiếu số trang PL ICD. |

Ba điểm cần bác sĩ và nhóm biết:

1. **Điểm a) không ghi "đối với người lớn".** Văn bản đặt câu "Đối với trẻ em" ngay sau bốn tiêu chuẩn của điểm a). Rule hiểu là trẻ em dùng câu riêng, người từ 16 tuổi dùng 02/04 tiêu chuẩn. Đây là cách hiểu, không phải câu chữ.
2. **Nhánh d (M-07).** Chốt 14/11 (docs/10 GD-02): giữ cách chấm theo ICD như giám định viên, mở rộng danh sách, lý do nêu rõ cả phần ICD. Rủi ro còn lại: trẻ có bệnh tự miễn nằm ngoài danh sách, không sốt, sẽ bị trả "Không được chi trả" dù văn bản có thể cho thanh toán. Cần bác sĩ duyệt danh sách trước khi dùng thật.
3. **"Theo dõi" (M-05).** Văn bản ghi "Chẩn đoán, theo dõi". Rule yêu cầu thỏa lại điều kiện ở mỗi lần làm. Không có giá trị riêng nào cho việc này.
4. **V2 chỉ xét chiều "nhanh".** Văn bản ghi "thay đổi quá giới hạn sinh lý theo tuổi", tức gồm cả nhanh và chậm. Rule chỉ mã hóa nhịp tim, nhịp thở cao hơn ngưỡng; nhịp chậm không xét. Thiếu bảng nhịp tim thì vế ra "chưa đủ dữ liệu", không gây từ chối (AUDIT m-3).

## 4. Procalcitonin: `dieu-kien.yaml` → `23.0130.1549`

**Nguồn.** Phụ lục TT 39, Danh mục 1, STT 8 (STT theo TT 35: 12), trang 9–10. Tên trong văn bản: "Định lượng Pro-calcitonin [Máu]". Đã so với ảnh trang, không sửa chữ nào. Đối chiếu VBHN 17 trang 27–28.

**Nguyên văn cột "Điều kiện thanh toán":**

> a) Chẩn đoán và theo dõi tình trạng nhiễm trùng nặng khi đáp ứng 01 trong 02 tiêu chuẩn sau đây: - Điểm suy đa tạng (SOFA) ≥ 2; - Nghi ngờ có ổ nhiễm trùng và có 2 trong 3 tiêu chuẩn: Nhịp thở ≥ 22 lần/phút; Huyết áp tâm thu ≤ 100 mmHg; Glasgow <15 điểm. b) Đối với trẻ em: - Chẩn đoán và theo dõi các trường hợp nhiễm trùng huyết; - Theo dõi và tiên lượng suy đa tạng khi có rối loạn chức năng từ 2 cơ quan trở lên.

**Nguyên văn cột "Tỷ lệ, mức giá thanh toán":**

> Thanh toán bằng giá DVKT. Khi sử dụng xét nghiệm Procalcitonin để theo dõi tình trạng nhiễm trùng nặng và đáp ứng điều trị theo quy định tại khoản 1 Mục này: + Thanh toán tối đa 01 lần/mỗi 24 giờ đối với người bệnh sốc nhiễm trùng; + Thanh toán tối đa 01 lần/mỗi 48 giờ đối với người bệnh nhiễm trùng nặng; + Không thanh toán đối với các trường hợp đã có bằng chứng chứng minh: hết dấu hiệu chỉ định và Procalcitonin ≤ 02 lần giá trị tham chiếu.

`nguyen_van` trong YAML gộp hai cột, có nhãn `[Cột …]` do nhóm thêm để phân biệt. Hai nhãn đó không phải chữ của văn bản.

| Phần trong rule | Giá trị | Nguồn | Cách hiểu |
|---|---|---|---|
| Nhánh `n1`, `n2` áp cho [0, 192) tháng | 192 tháng | **Tự dựng, M-01** | Như CRP. |
| N1 | AI đọc phiếu khám | Văn bản: "Chẩn đoán và theo dõi các trường hợp nhiễm trùng huyết" | Nghi ngờ phải ghi rõ trong hồ sơ (M-08). |
| N2 | AI đọc, tối đa "chưa thấy" | Văn bản: "khi có rối loạn chức năng từ 2 cơ quan trở lên" | Văn bản không dẫn tiêu chí cho từng cơ quan. AI chỉ trích dấu hiệu, không đếm cơ quan, nên vế này không bao giờ tự đạt (M-09). |
| Nhánh `a_nguoi_lon` | Chưa mã hóa | Văn bản: điểm a) | Ngoài phạm vi Nhi → "Cần xem lại". |
| `tan_suat.toi_thieu_gio` | 24 | Số 24 có trong văn bản. **Cách áp tự dựng, M-20** | Dưới 24 giờ kể từ lần trước → "Không được chi trả". |
| `tan_suat.nen_gio` | 48 | Số 48 có trong văn bản. **Cách áp tự dựng, M-20** | Từ 24 đến dưới 48 giờ → "Cần xem lại". |
| X1 | AI đọc phiếu khám | Văn bản: "hết dấu hiệu chỉ định" | Câu hỏi chỉ hỏi phiếu khám có ghi dấu hiệu đã hết hay không. |
| X2 | PCT lần trước ≤ 2 × `@pct_tham_chieu` | Hệ số 2: văn bản ("≤ 02 lần giá trị tham chiếu"). **Giá trị tham chiếu tự dựng, M-10** | Xem mục 5. |

Ba điểm cần bác sĩ và nhóm biết:

1. **Phạm vi của giới hạn 24/48 giờ.** Văn bản chỉ áp ba gạch đầu dòng "+" cho trường hợp "theo dõi tình trạng nhiễm trùng nặng và đáp ứng điều trị theo quy định tại khoản 1 Mục này". 24 giờ là cho "người bệnh sốc nhiễm trùng", 48 giờ là cho "người bệnh nhiễm trùng nặng". Rule áp chung cho mọi lần làm lại ở trẻ em, không phân biệt hai nhóm. Đây là cách hiểu tự dựng (M-20). Câu trích trong docs/06 đã chép đủ mệnh đề phạm vi (14/11).
2. **"khoản 1 Mục này" không rõ trỏ vào đâu.** Cột điều kiện đánh a), b), không có "khoản 1". Giữ nguyên chữ, không suy diễn. Muốn giải được cần TT 50/2017/TT-BYT hoặc bản TT 35/2016 đã sửa đổi đầy đủ; kho `data/van-ban/` chưa có, nên giữ ghi chú này (AUDIT m-7).
3. **Điểm a) không ghi "đối với người lớn".** Như CRP: rule hiểu trẻ em chỉ dùng điểm b).
4. **N1 hoặc N2 là cách hiểu.** Điểm b) trẻ em là hai gạch đầu dòng, không có chữ "hoặc". Cụm "01 trong 02 tiêu chuẩn" thuộc điểm a) người lớn, không thuộc điểm b). Rule đọc hai gạch là "một trong hai" dựa vào Ghi chú 2 cuối Danh mục 2 (VBHN 17 trang 51, xem mục 6). Đây là cách hiểu, theo hướng an toàn (dễ đạt hơn) (AUDIT m-1).

## 5. Siêu âm Doppler tim, Điện tim, và tham số

### Siêu âm Doppler tim: `18.0052.0004`

- Nguồn: phụ lục TT 39, Danh mục 2, STT 48 (STT theo TT 35: 109), trang 22. Tên trong văn bản: "Siêu âm Doppler tim". Đã so với ảnh trang, không sửa chữ nào. Đối chiếu VBHN 17 trang 51 (đọc sửa trên ảnh).
- Nguyên văn: "Không thanh toán khi thực hiện dịch vụ kỹ thuật Siêu âm tim có cản âm khi chỉ định thực hiện cùng một thời điểm."
- Tên dịch vụ trong danh sách là "Siêu âm doppler tim, van tim" (PL01 mã 18.52). Coi hai tên là một dịch vụ là cách hiểu của nhóm.
- Vế D1 (`khong_cung_luot`): **tự dựng, M-11**. "Cùng một thời điểm" hiểu là cùng lượt khám. Danh sách tên và mã siêu âm tim cản âm lấy từ PL01 và QĐ 3500 (mục 2.4c).
- Liên quan: TT 39, trang 1, khoản 1 Điều 1 bổ sung khoản 7 Điều 4 TT 35, nguyên văn: "7. Một lượt khám bệnh, chữa bệnh được xác định là một lần khám ngoại trú hoặc một đợt điều trị (điều trị ngoại trú hoặc điều trị ban ngày hoặc điều trị nội trú). Số ngày của một lượt khám bệnh, chữa bệnh do người hành nghề quyết định dựa trên tình trạng bệnh của người bệnh." Câu này định nghĩa "lượt", không định nghĩa "thời điểm".
- Điều kiện riêng của "Siêu âm tim cản âm" (phụ lục TT 39, Danh mục 2, STT 19, STT theo TT 35: 47, trang 15) không mã hóa vì dịch vụ này ngoài danh sách 50.

### Điện tim thường: `02.0085.1778`

Xem mục 2.4b.

### `tham-so.yaml`

Không giá trị nào trong file này có trong văn bản BHYT.

| Tham số | Giá trị | Nguồn | Ghi chú |
|---|---|---|---|
| `tre_em_den_thang` | 192 (dưới 16 tuổi) | **Bác sĩ duyệt** 14/11/2026, M-01 | Trùng mốc Luật Trẻ em (luật không có trong `data/van-ban/`). |
| `nhip_tho_nhanh` | < 2 tháng: ≥ 60; 2 đến dưới 12 tháng: ≥ 50; 12 đến dưới 60 tháng: ≥ 40 | Tự dựng, M-02 | docs/06 dẫn ngưỡng thở nhanh của WHO. Tài liệu WHO không có trong `data/van-ban/` nên chưa đối chiếu. Từ 60 tháng trở lên chưa có ngưỡng. |
| `nhip_tim_nhanh` | 0–1 tuổi ≥ 161; 1–2 tuổi ≥ 151; 2–5 tuổi ≥ 141; 5–6 tuổi ≥ 121 lần/phút; từ 72 tháng: chưa có | Bác sĩ chọn "thang Úc" (14/11); bảng cụ thể tự chọn, M-02 | RACGP, *Sick child assessment*, trang 1, bảng "Normal ranges for respiratory and heart rates" (0–1: 110–160; 1–2: 100–150; 2–3, 3–4, 4–5: 95–140; 5–6: 80–120). Ngưỡng = cận trên + 1; trang 2 ghi định nghĩa nhịp nhanh của APLS cùng mốc (< 12 tháng > 160; 12–24 tháng > 150; 2–5 tuổi > 140). Nguồn: https://gplearning.racgp.org.au/Content/gplearning/ALM/SickChild/Sick_child_assessment.pdf (tải 14/11/2026, lưu tại `05-tham-chieu-lam-sang/RACGP_sick-child-assessment_nhip-tho-nhip-tim.pdf`). |
| `pct_tham_chieu` | 0,5 ng/mL | Tự dựng, M-10 | Giá trị tạm. Phải thay bằng giá trị tham chiếu của lab Vinmec. |
| `khoang_hop_le` | Nhiệt độ 34–43; mạch 40–250; nhịp thở 10–120 | Chốt kỹ thuật (docs/09-spec.md mục 3) | Không phải quy tắc BHYT. Dùng để loại số AI trích nhầm. |

## 6. Quy định chung có liên quan

Tất cả từ VBHN 17 (đọc sửa trên ảnh).

- Trang 6, khoản 4 Điều 4 TT 35/2016: "4. Quỹ bảo hiểm y tế và người bệnh không thanh toán chi phí dịch vụ kỹ thuật y tế trong các trường hợp sau đây: a) Dịch vụ kỹ thuật y tế thuộc quy trình chuyên môn của một dịch vụ kỹ thuật y tế khác mà chi phí của dịch vụ kỹ thuật đó đã được tính trong cơ cấu giá của dịch vụ kỹ thuật y tế khác đó; b) Dịch vụ kỹ thuật y tế có kết quả được tính toán từ kết quả của dịch vụ kỹ thuật y tế khác hoặc có kết quả từ việc thực hiện dịch vụ kỹ thuật y tế khác." Đây là căn cứ chung cho M-12.
- Trang 6, khoản 6 Điều 4: "6. Quỹ bảo hiểm y tế tạm thời chưa thanh toán đối với dịch vụ kỹ thuật y tế quy định tại Danh mục 3 ban hành kèm theo Thông tư này."
- Trang 51, cuối Danh mục 2: "Ghi chú: 1. Đối với dịch vụ kỹ thuật có quy định nhiều điều kiện thanh toán có số thứ tự 1, 2, 3... tại Cột 3, quỹ bảo hiểm y tế thanh toán khi dịch vụ kỹ thuật đáp ứng tất cả các điều kiện; 2. Đối với dịch vụ kỹ thuật có quy định nhiều điều kiện thanh toán có gạch đầu dòng (-) hoặc a), b), c)... tại Cột 3, quỹ bảo hiểm y tế thanh toán khi dịch vụ kỹ thuật đáp ứng một trong các điều kiện đó." Ghi chú này chỉ đứng sau Danh mục 2. Phụ lục TT 39 không có phần ghi chú. Với CRP và PCT (Danh mục 1), cách đọc a), b), c), d) là "một trong" dựa vào chính câu chữ của mục ("một trong các trường hợp sau đây", "01 trong 02 tiêu chuẩn").

## 7. R2 thẻ BHYT

Câu hỏi: có câu nào bằng văn bản nói "thẻ hết hạn thì không được thanh toán" không?

**Kết quả: trong các file hiện có, không tìm thấy câu nào nói thẳng như vậy.**

| Văn bản | Tìm thấy gì |
|---|---|
| QĐ 4750 PL, trang 3, Bảng 1, chỉ tiêu 10 và 11 | "GT_THE_TU … Ghi thời điểm thẻ BHYT bắt đầu có giá trị sử dụng, gồm 08 ký tự…" và "GT_THE_DEN … Ghi thời điểm thẻ BHYT hết giá trị sử dụng, gồm 08 ký tự, bao gồm: 04 ký tự năm + 02 ký tự tháng + 02 ký tự ngày." Đây là định nghĩa trường dữ liệu, không phải quy tắc thanh toán. |
| TT 01/2025 | Chỉ có một ô trong mẫu phiếu chuyển cơ sở khám bệnh, chữa bệnh: "- Thời hạn sử dụng của thẻ bảo hiểm y tế đến ngày….. tháng……. năm……….". |
| VBHN 17 và TT 39 | Không có câu nào về hạn thẻ. Điểm a khoản 1 Điều 4 dẫn sang các Điều 21, 22, 31 của Luật BHYT (phần này mới đọc qua lớp OCR, chưa đọc lại trên ảnh). |
| Luật BHYT, NĐ 188/2025 | Không có trong `data/van-ban/`. Chưa kiểm được. |
| TT 12/2026/TT-BTC (`02-…/2026_TT-12-2026-TT-BTC_giam-dinh-thanh-quyet-toan-BHYT.pdf`) | File là ảnh quét, không có lớp chữ. Chưa tìm trong file này. |

Hệ quả: R2 hiện dựa trên hai trường dữ liệu `GT_THE_TU`, `GT_THE_DEN` và cách hiểu thông thường. Chưa có câu trích bằng văn bản để hiển thị làm căn cứ. Muốn có căn cứ, cần bổ sung Luật BHYT (hợp nhất) và NĐ 188/2025 vào `data/van-ban/`, và OCR TT 12/2026/TT-BTC.

## 8. Chưa kiểm chứng được

- Vinmec có làm và có đăng ký từng dịch vụ hay không, và thu theo mã nào: không có dữ liệu của Vinmec. Mọi mã đầy đủ lấy theo bảng giá BV Nhi TW.
- Ba test nhanh (RSV, Adenovirus, liên cầu nhóm A) có được xếp vào "Virus test nhanh" / "Vi khuẩn test nhanh" hay không. Tạm giả định là có (docs/10 GD-01), `danh-muc.yaml` để `co` với `ma_chung`.
- Hai mã giá Mycoplasma (1689, 1690) khác nhau ở đâu; PT và APTT dùng biến thể máy nào.
- Câu chữ của Luật Trẻ em (M-01) và bảng ngưỡng WHO (M-02): không có file nguồn trong repo.
- R2: xem mục 7.
- TT 35/2016 bản gốc và TT 13/2020 có trong repo nhưng không dùng làm nguồn trích. Nội dung hiện hành lấy theo VBHN 17 và phụ lục TT 39.
