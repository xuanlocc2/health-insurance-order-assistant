# data/eval — bộ đánh giá KHÓ cho A1

`a1-kho.yaml`: 45 ca (KHO-01 … KHO-45) để đo A1 (LLM đọc phiếu khám, `src/a1.py`).
Khác `data/test-cases/` (đo cả engine): bộ này chỉ đo đầu ra của A1 và không được pytest nạp.

**Lưu ý quan trọng: nhãn do nhóm tự viết theo spec (docs/09) và các diễn giải tạm ở docs/06,
CHƯA được bác sĩ duyệt. Phiếu khám do nhóm soạn (mô phỏng cách ghi của bác sĩ), không phải dữ liệu thật.**

## Mục đích

Lỗi nguy hiểm nhất của A1 là `dat` SAI (và số sinh hiệu SAI): engine chỉ dùng `dat` từ A1,
nên `dat` sai dẫn thẳng tới gợi ý "đủ điều kiện" sai. Bộ này dồn bẫy vào đúng hướng đó:
phủ định, người khác trong nhà, tiền sử/lần khám trước, số của đại lượng khác, chữ viết tắt,
không dấu, sai chính tả, nghi ngờ nước đôi, chèn lệnh (prompt injection) trong phiếu.

Chỉ số chính: **tỉ lệ `dat` sai** (trên 40 vế mong đợi `chua_thay`) và **tỉ lệ số sai**
(trên 43 trường phải bỏ trống + giá trị khác mong đợi). Chỉ số phụ: bỏ sót `dat`, bỏ sót số.

## Cách chạy (gợi ý cho runner)

- Hỏi A1 đúng các vế liệt kê trong `ky_vong[].ve` (đều `kiem_bang: ai`), khoá `"{thu_tu}:{id}"`,
  câu hỏi lấy từ `dieu-kien.yaml` (V3, B1 cho CRP; N1, N2, X1 cho PCT).
- Hỏi số cho mọi trường `null` trong `sinh_hieu` (`nhiet_do`, `mach`, `nhip_tho`).
- So sánh sau khi qua `verify()`.
- Vế `dat`: đúng khi A1 trả `dat` VÀ trích dẫn giao với `trich_dan` hoặc một mục trong
  `trich_dan_khac`. `dat` nhưng trích vào đoạn bẫy = sai.
- Số: trường có trong `a1_ky_vong_so_lieu` phải đúng `gia_tri`; trường được hỏi mà không
  có trong danh sách = A1 KHÔNG được trả.

## Trường thêm so với data/test-cases

| Trường | Ý nghĩa |
|---|---|
| `bay` | Danh sách nhãn bẫy của ca (bảng dưới). |
| `a1_ky_vong_so_lieu` | `[{truong, gia_tri}]` số A1 phải trích từ phiếu; `[]` = không có số hợp lệ nào. |
| `chap_nhan_trong` | (trong `a1_ky_vong_so_lieu`) `true` = trả rỗng cũng chấp nhận; giá trị khác vẫn là sai. Dùng cho "39độ5", "38°5". |
| `trich_dan_khac` | Các đoạn bằng chứng khác cũng chấp nhận (đều là chuỗi con nguyên văn). |
| `ly_giai` | Một dòng giải thích nhãn. Bắt buộc khi có `diem_mo_ho`. |
| `diem_mo_ho` | Mã M-xx ở docs/06 mà nhãn phụ thuộc; `chua_co_ma` = mơ hồ chưa có trong docs/06. |

`ky_vong` chỉ có vế AI, không có `trang_thai`/`he_chi_rule`. N2 chỉ gắn nhãn ở ca chắc chắn
`chua_thay` (M-09: engine luôn chặn trần N2).

## Thống kê

- 45 ca; 22 ca (49%) có ít nhất một vế `dat`.
- 63 vế AI: 23 `dat` (37%), 40 `chua_thay`.
  V3 18/21, B1 1/1, N1 3/10, N2 0/7, X1 1/1 (dat/chua_thay).
- 101 trường số được hỏi: 58 phải trích, 43 phải bỏ trống; 18 ca phải trả `so_lieu` rỗng.

| Bẫy | Số ca | Nội dung |
|---|---|---|
| `phu_dinh` | 30 | không, chưa, ko/k/kg, (-), âm tính, loại trừ, không ghi nhận, hết, không còn |
| `so_khac_chi_so` | 20 | SpO2, cân nặng, tuần tuổi thai, HA, ml sữa, tháng tuổi, chiều cao |
| `viet_tat` | 14 | NT, M, T, VPQP, VTG, NKH, NTH, NTSS, CRNN… |
| `nghi_ngo` | 12 | theo dõi/TD, nghi, chưa loại trừ, ít nghĩ đến |
| `tien_su` | 9 | bệnh đã khỏi, tiền sử |
| `nguoi_khac` | 8 | mẹ, anh trai, ông, cả lớp, bạn cùng nhà |
| `xuong_dong` | 8 | phiếu nhiều dòng, khối theo ngày |
| `so_loi_ke` | 7 | số đo ở nhà do người nhà kể |
| `bang_chung_chim` | 6 | bằng chứng thật nằm lẫn trong phiếu dài |
| `so_dinh_lien` | 5 | "39độ5", "38°5", "NT50l/p", "T39,3" |
| `phu_dinh_kep` | 4 | chưa hết, không loại trừ, chưa loại trừ được |
| `so_lan_truoc` | 4 | số của lần khám trước, giấy chuyển tuyến |
| `khong_dau` | 4 | phiếu gõ không dấu |
| `loi_chinh_ta` | 3 | "amidna", "chảy mũ", "rang ẩm", "nhịp thờ" |
| `tu_khoa_gia` | 3 | từ khoá nhiễm trùng xuất hiện nhưng không phải bằng chứng |
| `prompt_injection` | 3 | lệnh cho hệ thống chèn trong phiếu |
| `nhieu_lan_kham` | 2 | một phiếu ghi nhiều lần khám |
| `khoang_so` | 2 | "NT 48-52", "39-40" |
| `mau_phieu` | 2 | mẫu ô đánh dấu [ ] / [x] |
| `dan_do` | 1 | số và triệu chứng nằm trong lời dặn |

Một ca mang nhiều nhãn nên tổng cột lớn hơn 45.
Điểm mơ hồ liên quan: M-04 19 ca, M-03 11, M-08 9, M-05 3, M-06 2, M-02 1, chưa có mã 1.

## Nhãn yếu, cần bác sĩ xác nhận trước

| Ca | Câu trong phiếu | Nhãn hiện tại | Phụ thuộc |
|---|---|---|---|
| KHO-33 | "chưa loại trừ nhiễm trùng đường tiểu" | V3 dat | M-04 |
| KHO-31 | "TD VTG cấp bên P" | V3 dat | M-04 |
| KHO-42 | bác sĩ chép lại nguyên văn điều kiện quy định | V3 chua_thay | M-04 |
| KHO-34 | "Chưa loại trừ được NKH" | N1 dat | M-08 |
| KHO-35 | "Ít nghĩ đến nhiễm trùng huyết" | N1 chua_thay | M-08 |
| KHO-29 | "NT 48-52 l/p" (ngưỡng 50) | không trích nhịp thở | chưa có mã, M-02 |
| KHO-05, 08, 14 | tái khám, dấu hiệu đã hết | V3 chua_thay | M-05 |
| KHO-10 | số do điều dưỡng đo lúc tiếp đón | được tính là đo tại lần khám | M-03 |
| KHO-44 | ô "[x] chảy mủ tai" | V3 dat | — |
| KHO-20, 45 | "TD NTSS", "TD NTH" (giải chữ viết tắt) | B1 / N1 dat | M-06, M-08 |
| KHO-36 | sốt xuất huyết, tiền sử NTSS | N1 chua_thay (N2 không gắn nhãn) | M-08 |

## Giới hạn đã biết

- `verify()` loại số viết dính kiểu "39độ5"/"38°5" (không có token 39.5 trong trích dẫn),
  trong khi trả sai 39/38 lại qua được. Xem KHO-27, KHO-28.
- `verify()` không chặn được bằng chứng giả nhưng đúng chuỗi con: câu do đoạn chèn lệnh đặt sẵn
  (KHO-40, KHO-41), số trong khoảng hợp lệ của đại lượng khác (38 tuần, 36,5 kg, HA 80/45).
  Các ca này chỉ A1 tự chống được.
- Kiểm tra định dạng: script tạm ngoài repo đã xác nhận mọi `trich_dan` là chuỗi con nguyên văn
  của `phieu_kham`, id không trùng, đáp án mong đợi qua được `verify()` thật.
