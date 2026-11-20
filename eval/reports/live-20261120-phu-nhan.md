# Eval hệ thống — 2026-11-20 23:46

A1: `live` (gpt-6-luna, reasoning_effort=low) · lần lặp: 3 · ca: 102 · rules: `e23cb8743ff6` · file ca: data/test-cases/*.yaml, data/eval/*.yaml

## Tóm tắt

| Chỉ số | Giá trị | Mục tiêu |
|---|---|---|
| Dòng QUÁ THUẬN LỢI (got thuận lợi hơn nhãn) | 1 | 0 — **CHƯA ĐẠT** |
| Dòng kém thuận lợi | 3 |  |
| Khớp trạng thái dòng | 281/285 (98.6%) |  |
| Vế AI đạt sai (got dat, nhãn ≠ dat) | 1 | 0 — **CHƯA ĐẠT** |
| Vế AI bỏ sót đạt | 7 |  |
| Vế AI đạt nhưng trích sai chỗ (không giao trich_dan / trich_dan_khac) | 2 |  |
| Khớp ket_qua vế (mọi vế có id) | 377/396 (95.2%) |  |
| Trích số khớp | 285/285 (100.0%) |  |
| Trích dẫn A1 bị loại / lần gọi | 0/725 (0.0) |  |
| Lật trạng thái dòng qua các lần | 3/147 (2.0%) |  |
| A1 lỗi / hết giờ | 0 / 0 trên 219 lần gọi |  |
| engine.check p50 / p95 (ms) | 2825 / 4729 | p95 < 10000 — ĐẠT |
| Hệ chỉ-rule báo Phù hợp sai → hệ đầy đủ bắt được | 14/14 |  |

## 1. Trạng thái dòng

Hàng = nhãn, cột = hệ thống trả. Bỏ qua 156 dòng không có nhãn `trang_thai`.

| nhãn \ got | Phù hợp quy tắc BHYT | Đủ căn cứ · bác sĩ xác nhận | Cần xem lại | Không được chi trả |
|---|---|---|---|---|
| Phù hợp quy tắc BHYT | 141 | 0 | 0 | 0 |
| Đủ căn cứ · bác sĩ xác nhận | 0 | 39 | 3 | 0 |
| Cần xem lại | 0 | 1 | 80 | 0 |
| Không được chi trả | 0 | 0 | 0 | 21 |

**Quá thuận lợi** (1)

| ca | lần | dòng | dịch vụ | nhãn | got |
|---|---|---|---|---|---|
| A1-01 | 2 | 1 | 23.0228.1483 | Cần xem lại | Đủ căn cứ · bác sĩ xác nhận |

**Kém thuận lợi** (3)

| ca | lần | dòng | dịch vụ | nhãn | got |
|---|---|---|---|---|---|
| CRP-04 | 1 | 1 | 23.0228.1483 | Đủ căn cứ · bác sĩ xác nhận | Cần xem lại |
| CRP-05 | 2 | 1 | 23.0228.1483 | Đủ căn cứ · bác sĩ xác nhận | Cần xem lại |
| CRP-05 | 3 | 1 | 23.0228.1483 | Đủ căn cứ · bác sĩ xác nhận | Cần xem lại |

## 2. Vế điều kiện

| nhóm | n | khớp | đạt sai | bỏ sót đạt | đạt sai chỗ |
|---|---|---|---|---|---|
| tat_ca | 396 | 95.2% | 1 | 7 | 2 |
| rule | 126 | 100.0% |  |  |  |
| ai | 270 | 93.0% | 1 | 7 | 2 |
| bẫy: bang_chung_chim | 24 | 100.0% | 0 | 0 | 0 |
| bẫy: dan_do | 9 | 100.0% | 0 | 0 | 0 |
| bẫy: khoang_so | 6 | 100.0% | 0 | 0 | 0 |
| bẫy: khong_dau | 12 | 100.0% | 0 | 0 | 0 |
| bẫy: loi_chinh_ta | 9 | 100.0% | 0 | 0 | 0 |
| bẫy: mau_phieu | 6 | 100.0% | 0 | 0 | 0 |
| bẫy: nghi_ngo | 42 | 100.0% | 0 | 0 | 0 |
| bẫy: nguoi_khac | 30 | 100.0% | 0 | 0 | 0 |
| bẫy: nhieu_lan_kham | 6 | 100.0% | 0 | 0 | 0 |
| bẫy: phu_dinh | 129 | 90.7% | 0 | 3 | 0 |
| bẫy: phu_dinh_kep | 18 | 83.3% | 0 | 3 | 0 |
| bẫy: prompt_injection | 21 | 100.0% | 0 | 0 | 0 |
| bẫy: so_dinh_lien | 15 | 100.0% | 0 | 0 | 0 |
| bẫy: so_khac_chi_so | 78 | 100.0% | 0 | 0 | 0 |
| bẫy: so_lan_truoc | 12 | 75.0% | 0 | 0 | 0 |
| bẫy: so_loi_ke | 24 | 100.0% | 0 | 0 | 0 |
| bẫy: tien_su | 45 | 73.3% | 0 | 3 | 0 |
| bẫy: tu_khoa_gia | 9 | 100.0% | 0 | 0 | 0 |
| bẫy: viet_tat | 51 | 100.0% | 0 | 0 | 0 |
| bẫy: xuong_dong | 30 | 100.0% | 0 | 0 | 0 |

**Vế AI đạt sai** (1)

| ca | lần | dòng | vế | nhánh | nhãn | got | trích dẫn | bẫy |
|---|---|---|---|---|---|---|---|---|
| A1-01 | 2 | 1 | V3 | a_tre_em | chua_thay | dat | Vết tiêm sưng nhẹ. |  |

**Vế AI bỏ sót đạt** (7)

| ca | lần | dòng | vế | nhánh | nhãn | got | trích dẫn | bẫy |
|---|---|---|---|---|---|---|---|---|
| A1-05 | 1 | 1 | X1 | loai_tru | dat | chua_thay | — |  |
| CRP-04 | 1 | 1 | V3 | a_tre_em | dat | chua_thay | — |  |
| CRP-05 | 2 | 1 | V3 | a_tre_em | dat | chua_thay | — |  |
| CRP-05 | 3 | 1 | V3 | a_tre_em | dat | chua_thay | — |  |
| KHO-06 | 1 | 1 | V3 | a_tre_em | dat | chua_du_du_lieu | — | phu_dinh, phu_dinh_kep, tien_su |
| KHO-06 | 2 | 1 | V3 | a_tre_em | dat | chua_du_du_lieu | — | phu_dinh, phu_dinh_kep, tien_su |
| KHO-06 | 3 | 1 | V3 | a_tre_em | dat | chua_du_du_lieu | — | phu_dinh, phu_dinh_kep, tien_su |

**Vế AI đạt nhưng trích sai chỗ** (2)

| ca | lần | dòng | vế | nhánh | nhãn | got | trích dẫn | bẫy |
|---|---|---|---|---|---|---|---|---|
| CRP-11 | 2 | 1 | V3 | a_tre_em | dat | dat | CĐ: VPQ. |  |
| CRP-11 | 3 | 1 | V3 | a_tre_em | dat | dat | CĐ: VPQ. |  |

## 3. Trích số

Khớp 285, sai giá trị 0, bỏ sót 0, trích thừa 0, engine không hỏi 30 (không tính).


## 4. Trích dẫn bị loại khi kiểm tra

0 trên 725 trích dẫn, 219 lần gọi; lần gọi có `loi: trich_dan_*`: 0.


## 5. Độ ổn định qua các lần lặp

Dòng lật: 3/147 (2.0%) · vế lật: 4/132 (3.0%)

| khóa | giá trị qua các lần |
|---|---|
| A1-01/1 | Cần xem lại → Đủ căn cứ · bác sĩ xác nhận → Cần xem lại |
| CRP-04/1 | Cần xem lại → Đủ căn cứ · bác sĩ xác nhận → Đủ căn cứ · bác sĩ xác nhận |
| CRP-05/1 | Đủ căn cứ · bác sĩ xác nhận → Cần xem lại → Cần xem lại |
| A1-01/1/V3 | chua_thay → dat → chua_thay |
| A1-05/1/X1 | chua_thay → dat → dat |
| CRP-04/1/V3 | chua_thay → dat → dat |
| CRP-05/1/V3 | dat → chua_thay → chua_thay |

## 6. Vận hành

|  | giá trị |
|---|---|
| lượt × lần | 306 |
| lần gọi A1 | 219 |
| lỗi A1 | 0 (0.0%)  |
| hết giờ | 0 (0.0%) |
| engine.check p50 / p95 / max (ms) | 2825 / 4729 / 7204 |
| A1 p50 / p95 (ms) | 3368 / 4973 |
| token vào / ra | 365427 / 59806 (219 lần gọi có usage) |
| chi phí ước tính (USD) | — |

## 7. Hệ chỉ-rule và giá trị của A1

Hệ chỉ-rule (máy sinh, mode=chi_rule) khớp nhãn dòng: 76/95. Báo Phù hợp nhưng nhãn kém thuận lợi hơn: 14, hệ đầy đủ bắt được 14.
Nhãn `he_chi_rule` của ca khớp máy sinh: 31/31.

**A1 có giá trị** (14)

| ca | dòng | dịch vụ | nhãn | chỉ-rule | đầy đủ |
|---|---|---|---|---|---|
| A1-01 | 1 | 23.0228.1483 | Cần xem lại | Phù hợp quy tắc BHYT | Cần xem lại |
| A1-02 | 1 | 23.0228.1483 | Đủ căn cứ · bác sĩ xác nhận | Phù hợp quy tắc BHYT | Đủ căn cứ · bác sĩ xác nhận |
| A1-06 | 1 | 23.0228.1483 | Cần xem lại | Phù hợp quy tắc BHYT | Cần xem lại |
| A1-07 | 1 | 23.0228.1483 | Đủ căn cứ · bác sĩ xác nhận | Phù hợp quy tắc BHYT | Đủ căn cứ · bác sĩ xác nhận |
| CRP-01 | 1 | 23.0228.1483 | Đủ căn cứ · bác sĩ xác nhận | Phù hợp quy tắc BHYT | Đủ căn cứ · bác sĩ xác nhận |
| CRP-03 | 1 | 23.0228.1483 | Đủ căn cứ · bác sĩ xác nhận | Phù hợp quy tắc BHYT | Đủ căn cứ · bác sĩ xác nhận |
| CRP-04 | 1 | 23.0228.1483 | Đủ căn cứ · bác sĩ xác nhận | Phù hợp quy tắc BHYT | Cần xem lại |
| CRP-05 | 1 | 23.0228.1483 | Đủ căn cứ · bác sĩ xác nhận | Phù hợp quy tắc BHYT | Đủ căn cứ · bác sĩ xác nhận |
| CRP-07 | 1 | 23.0228.1483 | Cần xem lại | Phù hợp quy tắc BHYT | Cần xem lại |
| CRP-15 | 1 | 23.0228.1483 | Cần xem lại | Phù hợp quy tắc BHYT | Cần xem lại |
| CRP-17 | 1 | 23.0228.1483 | Cần xem lại | Phù hợp quy tắc BHYT | Cần xem lại |
| DEMO-01 | 2 | 23.0228.1483 | Đủ căn cứ · bác sĩ xác nhận | Phù hợp quy tắc BHYT | Đủ căn cứ · bác sĩ xác nhận |
| DEMO-02 | 2 | 23.0228.1483 | Đủ căn cứ · bác sĩ xác nhận | Phù hợp quy tắc BHYT | Đủ căn cứ · bác sĩ xác nhận |
| R4-01 | 1 | 23.0228.1483 | Đủ căn cứ · bác sĩ xác nhận | Phù hợp quy tắc BHYT | Đủ căn cứ · bác sĩ xác nhận |

## Ghi chú

- Chưa đặt EVAL_PRICE_IN_PER_1M / EVAL_PRICE_OUT_PER_1M (USD / 1M token) nên không tính chi phí.
