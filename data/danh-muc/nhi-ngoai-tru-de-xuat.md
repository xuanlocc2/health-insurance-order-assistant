# Danh sách đề xuất: 50 dịch vụ hay chỉ định ở Nhi ngoại trú

**Trạng thái:** chốt làm danh sách MVP (11/11/2026). Bác sĩ chưa duyệt, góp ý thì bổ sung sau. Đã tra sơ bộ mã, giá và điều kiện BHYT. MVP dùng thẳng mã/tên chuẩn ở đây, không làm mapping mã nội bộ Vinmec.
**Phạm vi:** khám Nhi ngoại trú (gồm phòng khám Ngoại Nhi). Chỉ có xét nghiệm, CĐHA và thăm dò chức năng. Không có thuốc, không có PT/TT.

**Nhờ bác sĩ:**
1. Điền cột **Giữ?**: `C` (giữ), `B` (bỏ) hoặc `?` (không chắc).
2. Thêm dịch vụ hay chỉ định nhưng còn thiếu ở cuối bảng.
3. Nếu biết dịch vụ nào **hay bị xuất toán hoặc bị hỏi lại**, ghi vào cột Ghi chú.

## Cách đọc các cột tra cứu

- **Mã tương đương:** lấy từ bảng giá BV Nhi Trung ương ([QĐ 3500/QĐ-BYT](../van-ban/04-mau-gia-bv-nhi-tw/), điều chỉnh Phụ lục III của QĐ 3467). Dạng `XX.YYYY.ZZZZ`, trong đó `XX.YYYY` là mã kỹ thuật (cột 2 PL01 TT 23/2024) và `ZZZZ` là mã giá.
  - Vinmec dùng mã kỹ thuật giống hệt, vì đây là mã chuẩn quốc gia. Giá thì khác, vì mỗi bệnh viện có quyết định giá riêng.
- **Giá:** giá BV Nhi TW năm 2024, chỉ để tham khảo. Không phải giá Vinmec, và có thể đã được điều chỉnh sau 11/2024.
- **BHYT (sơ bộ):**
  - **Có**: có trong danh mục kỹ thuật PL01, không thuộc Danh mục 3 (BHYT chưa thanh toán), và không có điều kiện riêng.
  - **Điều kiện**: có điều kiện trong Danh mục 1/2 của TT 35/2016 (sửa bởi TT 39/2024).
  - **Không thấy**: không tìm thấy trong danh mục kỹ thuật. Khả năng cao là BHYT không trả.
  - **Xác minh**: chưa kết luận được.
- Kết quả tra là sơ bộ. Danh mục 1/2 được rà bằng từ khóa trên văn bản hợp nhất [VBHN 17/VBHN-BYT](../van-ban/01-dvkt-va-co-so-phap-ly/) (bản OCR có lỗi chữ), nên cần đọc lại bản gốc trước khi đưa vào rule.

## Xét nghiệm huyết học

| # | Dịch vụ | Tình huống hay gặp | Mã tương đương | Giá (Nhi TW) | BHYT (sơ bộ) | Giữ? | Ghi chú |
|---|---|---|---|---|---|---|---|
| 1 | Tổng phân tích tế bào máu ngoại vi (máy đếm laser) | Sốt, nhiễm trùng, thiếu máu | 22.0121.1369 | 49.700 | Có | | |
| 2 | Máu lắng (máy tự động) | Viêm, sốt kéo dài | 22.0143.1303 | 37.300 | Có | | |
| 3 | Xét nghiệm hồng cầu lưới (máy đếm laser) | Thiếu máu | 22.0135.1313 | 43.500 | Có | | |
| 4 | Đông máu cơ bản: PT + APTT | Chảy máu, bầm tím, trước thủ thuật | PT 22.0002.1352; APTT 22.0006.1354 | 68.400; 43.500 | Có | | PT có nhiều biến thể theo loại máy, cần chọn đúng mã |

## Xét nghiệm sinh hóa và miễn dịch máu

| # | Dịch vụ | Tình huống hay gặp | Mã tương đương | Giá (Nhi TW) | BHYT (sơ bộ) | Giữ? | Ghi chú |
|---|---|---|---|---|---|---|---|
| 5 | Định lượng CRP | Sốt, phân biệt vi khuẩn/virus | 23.0228.1483 | 56.100 | **Điều kiện** (DM1 mục 7) | | **Ca thử chính.** Với trẻ em: nghi ổ nhiễm trùng, nhiệt độ ≤ 36°C hoặc ≥ 38,3°C, **và** nhịp tim hoặc nhịp thở vượt giới hạn sinh lý theo tuổi. Sốt 38°C với mạch bình thường thì không đạt |
| 6 | Định lượng Procalcitonin | Sốt, nghi nhiễm khuẩn nặng | 23.0130.1549 | 414.700 | **Điều kiện** (DM1 mục 8) | | **Ca thử.** Với trẻ em: chỉ khi nhiễm trùng huyết, hoặc suy ≥ 2 cơ quan. Ngoại trú hiếm khi đạt. Có giới hạn tần suất (24 giờ/48 giờ) |
| 7 | Định lượng Glucose [Máu] | Mệt, nôn, theo dõi đường huyết | 23.0075.1494 | 22.400 | Có | | |
| 8 | Định lượng Urê máu | Mất nước, bệnh thận | 23.0166.1494 | 22.400 | Có | | |
| 9 | Định lượng Creatinin (máu) | Mất nước, bệnh thận | 23.0051.1494 | 22.400 | Có | | |
| 10 | Đo hoạt độ AST (GOT) | Men gan, sốt virus | 23.0020.1493 | 22.400 | Có | | |
| 11 | Đo hoạt độ ALT (GPT) | Men gan, sốt virus | 23.0019.1493 | 22.400 | Có | | |
| 12 | Điện giải đồ (Na, K, Cl) | Tiêu chảy, nôn, mất nước | 23.0058.1487 | 30.200 | Có | | |
| 13 | Định lượng Canxi toàn phần | Còi xương, co giật | 23.0029.1473 | 13.400 | Có | | |
| 14 | Định lượng Canxi ion hóa | Còi xương, co giật | 23.0030.1472 | 16.800 | Có | | Quyết định giá ghi: "Chỉ thanh toán khi định lượng trực tiếp" |
| 15 | Định lượng Sắt [Máu] | Thiếu máu thiếu sắt | 23.0143.1503 | 33.600 | Có | | |
| 16 | Định lượng Ferritin | Thiếu máu thiếu sắt | 23.0063.1514 | 84.100 | Có | | |
| 17 | Định lượng Bilirubin toàn phần | Vàng da sơ sinh | 23.0027.1493 | 22.400 | Có | | |
| 18 | Định lượng Bilirubin trực tiếp | Vàng da sơ sinh, ứ mật | 23.0025.1493 | 22.400 | Có | | |
| 19 | Định lượng Albumin | Suy dinh dưỡng, phù | 23.0007.1494 | 22.400 | Có | | |
| 20 | Định lượng 25OH Vitamin D (D3) | Còi xương, chậm lớn | 23.0055.1489 | 302.500 | Có | | Nhóm đoán là ca thử, nhưng tra ra **không có điều kiện riêng** |
| 21 | Định lượng Kẽm | Biếng ăn, chậm lớn | BS_23.317 hoặc 23.249 ("yếu tố vi lượng đồng, kẽm") | Nhi TW không định giá | **Xác minh** | | Mã BS_ có quy định riêng theo TT 25/2026 |
| 22 | Định lượng IgE toàn phần | Dị ứng, chàm, hen | 23.0093.1527 | 67.300 | Có | | IgE **đặc hiệu** là dịch vụ khác, giá 589.200/dị nguyên |
| 23 | Định lượng TSH | Chậm lớn, bướu cổ | 23.0162.1570 | 61.700 | Có | | |
| 24 | Định lượng FT4 | Chậm lớn, bướu cổ | 23.0069.1561 | 67.300 | Có | | |

## Vi sinh và test nhanh

| # | Dịch vụ | Tình huống hay gặp | Mã tương đương | Giá (Nhi TW) | BHYT (sơ bộ) | Giữ? | Ghi chú |
|---|---|---|---|---|---|---|---|
| 25 | Influenza virus A, B test nhanh | Sốt, ho mùa cúm | 24.0243.1671 | 185.700 | Có | | |
| 26 | Test nhanh RSV | Viêm tiểu phế quản trẻ nhỏ | — | — | **Không thấy** | | PL01 chỉ có RSV Ab (24.0252) và RSV Real-time PCR (24.0253) |
| 27 | Test nhanh SARS-CoV-2 (Ag) | Sốt, ho | Có tên trong PL01 nhưng cột 2 không có mã | — | **Xác minh** | | |
| 28 | Test nhanh Adenovirus | Sốt cao, viêm kết mạc, viêm họng | — | — | **Không thấy** | | PL01 chỉ có Adenovirus Real-time PCR (24.0232) |
| 29 | Test nhanh liên cầu nhóm A | Viêm họng | — | — | **Không thấy** | | PL01 chỉ có ASO (24.0095) |
| 30 | Dengue virus NS1Ag test nhanh | Sốt cấp ≤ 5 ngày | 24.0183.1637 | 142.500 | Có | | |
| 31 | Dengue virus IgM/IgG test nhanh | Sốt > 5 ngày | 24.0187.1637 | 142.500 | Có | | |
| 32 | Mycoplasma pneumoniae Ab (miễn dịch bán tự động) | Ho kéo dài, viêm phổi không điển hình | 24.0082 (mã giá 1689 hoặc 1690) | 273.000 / 182.700 | Có | | Có 2 mức giá, chưa rõ mức nào là IgM. Hỏi lab Vinmec |
| 33 | Rotavirus test nhanh | Tiêu chảy cấp | 24.0249.1697 | 194.700 | Có | | |
| 34 | PCR đa tác nhân hô hấp | Viêm phổi, sốt kéo dài | Có tên "Vi sinh vật định danh PCR đa tác nhân" nhưng cột 2 không có mã | Nhi TW không định giá | **Xác minh** | | |
| 35 | Soi phân: HC, BC soi tươi + trứng giun sán + đơn bào | Tiêu chảy, phân máu | 24.0263.1665; 24.0267.1674; 24.0265.1674 | 41.700; 45.500; 45.500 | Có | | Ba dịch vụ riêng |
| 36 | Vi khuẩn nuôi cấy, định danh, kháng thuốc (tự động) – nước tiểu | Nghi nhiễm khuẩn tiết niệu | 24.0005.1716 | 325.200 | Có | | |
| 37 | Tổng phân tích nước tiểu (máy tự động) | Sốt không rõ nguồn, tiết niệu | 23.0206.1596 | 28.600 | Có | | |

## Chẩn đoán hình ảnh và thăm dò chức năng

**Áp dụng chung cho X-quang và siêu âm:** BHXH giới hạn số ca thanh toán đủ giá theo số máy và giờ làm của bệnh viện (TT 39/2024, Điều 4d khoản 6). Đây là quyết toán ở cấp bệnh viện, không phải lỗi ở từng chỉ định, nên không đưa vào rule lúc bác sĩ chỉ định.

| # | Dịch vụ | Tình huống hay gặp | Mã tương đương | Giá (Nhi TW) | BHYT (sơ bộ) | Giữ? | Ghi chú |
|---|---|---|---|---|---|---|---|
| 38 | Chụp X-quang ngực thẳng (số hóa 1 phim) | Viêm phổi, ho kéo dài | 18.0119.0028 | 73.300 | Có | | |
| 39 | Chụp X-quang bụng không chuẩn bị (số hóa 1 phim) | Đau bụng, nghi tắc ruột | 18.0125.0028 | 73.300 | Có | | |
| 40 | Chụp X-quang xương cổ tay (tuổi xương) | Chậm lớn, dậy thì sớm | 18.0107.0028 | 73.300 | Có | | |
| 41 | Chụp X-quang xương chi (cẳng tay / cẳng chân…) | Chấn thương (Ngoại Nhi) | 18.0106.0028; 18.0114.0028… | 73.300 | Có | | Mỗi vị trí một mã |
| 42 | Siêu âm ổ bụng (gan mật, tụy, lách, thận, bàng quang) | Đau bụng, lồng ruột, ruột thừa | 18.0015.0001 | 58.600 | Có | | |
| 43 | Siêu âm tuyến giáp | Bướu cổ | 18.0001.0001 | 58.600 | Có | | |
| 44 | Siêu âm hạch vùng cổ | Hạch cổ to | 18.0004.0001 | 58.600 | Có | | |
| 45 | Siêu âm tinh hoàn hai bên | Tinh hoàn ẩn, tràn dịch (Ngoại Nhi) | 18.0057.0001 | 58.600 | Có | | |
| 46 | Siêu âm khớp (gối, háng, khuỷu, cổ tay…) | Sàng lọc loạn sản khớp háng | 18.0043.0001 | 58.600 | Có | | |
| 47 | Siêu âm qua thóp | Sơ sinh, trẻ nhỏ | 18.0007.0001 | 58.600 | Có | | |
| 48 | Siêu âm doppler tim, van tim | Tiếng thổi tim | 18.0052.0004 | 252.300 | **Điều kiện** (DM2 mục 48) | | Không thanh toán nếu làm cùng thời điểm với siêu âm tim cản âm |
| 49 | Điện tim thường | Đau ngực, hồi hộp, ngất | 02.0085.1778 | 39.900 | Có | | |
| 50 | Đo chức năng hô hấp | Hen, ho kéo dài (trẻ lớn) | 02.0024.1791 | 144.300 | Có | | Điều kiện trong DM2 là của đo thể tích toàn thân (plethysmography), không áp dụng cho dịch vụ này |

## Tóm tắt cho bộ test

- **Có điều kiện (rule R3 phải xử lý):** CRP, Procalcitonin, Doppler tim. CRP là ca quan trọng nhất vì Nhi chỉ định rất nhiều, và điều kiện cho trẻ em cần sinh hiệu (nhiệt độ, mạch, nhịp thở). Sinh hiệu có sẵn trong phiếu khám.
- **Không thấy trong danh mục (rule R1 phải bắt):** test nhanh RSV, Adenovirus, liên cầu nhóm A.
- **Cần xác minh:** Kẽm, test nhanh SARS-CoV-2, PCR đa tác nhân, mã giá Mycoplasma.
- **Đoán sai:** Vitamin D và IgE toàn phần được nhóm đoán là ca thử, nhưng tra ra không có điều kiện riêng.

## Bác sĩ bổ sung

| # | Dịch vụ | Tình huống hay gặp | Giữ? | Ghi chú |
|---|---|---|---|---|
| | | | | |
