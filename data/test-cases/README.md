# Bộ test mô phỏng

Dữ liệu giả, nhóm tự dựng (bắt đầu 11/11/2026), bác sĩ chưa duyệt. Kỳ vọng dựa trên **cách hiểu tạm** ở [06-diem-mo-ho-bac-si-duyet.md](../../docs/06-diem-mo-ho-bac-si-duyet.md). Ca nào phụ thuộc điểm mơ hồ thì ghi mã trong `diem_mo_ho`; bác sĩ trả lời khác thì chỉ sửa các ca có mã đó.

## Nguyên tắc thiết kế

- **Phủ theo vế, không chia đều theo dịch vụ.** 47 dịch vụ không có điều kiện riêng chỉ cần R1 tra bảng: test bằng một vòng lặp qua [danh sách 50](../danh-muc/nhi-ngoai-tru-de-xuat.md) (cột BHYT sơ bộ → trạng thái), không viết ca riêng. Công sức dồn vào CRP, PCT, Doppler.
- **Kỳ vọng suy ra từ ma trận, không phải từ cảm giác.** Mỗi ca được dựng để một vế cụ thể ra một kết quả cụ thể, rồi mới viết phiếu khám cho khớp.
- **Phiếu khám đa dạng văn phong:** viết tắt (T°, NT, VPQ), câu phủ định, số liệu nằm trong chữ, từ khóa "bẫy" (bệnh của người nhà).
- **Kiểm tra trích dẫn bịa (AC-11) là unit test của code**, không phải ca mock.

## Quy ước chung

- Mặc định (chỉ loader của test và app áp, engine không có mặc định) nếu ca không ghi: `ngay_kham: 2026-11-12`, thẻ còn hạn, mức hưởng 100% (trẻ < 6 tuổi) hoặc 80%.
- `ket_qua` của vế: `dat | khong_dat | chua_thay | chua_du_du_lieu`; so theo `id` vế (V1, N1, X2…). Trong khối loại trừ, `dat` = điều khoản loại trừ khớp. `nguon_ket_qua: a1` khi số liệu do A1 trích.
- `a1_gia_lap`: số liệu A1 giả lập cho chế độ stub (spec mục 7).
- Ô BHYT không ghi trong ca, suy ra từ trạng thái (bảng điền sẵn ở [02-giai-phap.md](../../docs/02-giai-phap.md)).
- `he_chi_rule`: kết quả của một hệ chỉ dùng rule, không đọc phiếu khám. Dùng để đo giá trị của A1.
- Gộp trạng thái và `he_chi_rule`: theo [spec](../../docs/09-spec.md) mục 6.

## Ma trận phủ

| Nhóm | File | Số ca | Phủ |
|---|---|---|---|
| A1 seed | [a1-seed.yaml](a1-seed.yaml) | 5 | Phủ định, số trong chữ, PCT hai nhánh, điều khoản loại trừ |
| CRP | [crp.yaml](crp.yaml) | 19 | Ngưỡng nhiệt (38,3 / 38,2 / ≤ 36), băng tuổi nhịp thở (< 2 th / 2–11 th / 1–5 tuổi / > 5 tuổi chưa có ngưỡng), nhịp tim chưa có ngưỡng, sốt theo lời kể, sinh hiệu trống, viết tắt, từ khóa bẫy, nhánh sơ sinh (rule và AI), tuổi 16, CRP theo dõi |
| PCT | [pct.yaml](pct.yaml) | 5 | Nhiễm trùng huyết đạt, ≥ 2 cơ quan (chỉ trích, không đếm), ngoại trú thường, tần suất 48 giờ, làm lại nhưng không loại trừ |
| Doppler + khác | [doppler-khac.yaml](doppler-khac.yaml) | 4 | Cùng lượt / khác lượt với siêu âm cản âm, Canxi ion hóa |
| R1 danh mục | [r1-r2-r4.yaml](r1-r2-r4.yaml) | 6 | Không thấy, Xác minh, ca đoán sai (Vitamin D, IgE), dịch vụ ngoài danh sách |
| R2 thẻ | (cùng file) | 5 | Hết hạn, đúng ngày hết hạn, mức hưởng 100% / 80%, thiếu thông tin thẻ |
| R4 trùng | (cùng file) | 3 | Trùng cùng lượt, khác lượt |
| Demo tổng hợp | [demo.yaml](demo.yaml) | 8 | Lượt khám 4–6 dòng, cặp cùng một bệnh nhi ở hai thời điểm (DEMO-01, DEMO-02), ca "sạch" (công cụ im lặng) |
| **Tổng** | | **55** | + vòng lặp R1 qua 50 dịch vụ |

Còn chỗ cho 10–20 ca dựng lại từ lời kể xuất toán của bác sĩ (phiếu hỏi câu 11).

## Giới hạn đã biết

- Phiếu khám do LLM viết có thể dễ đọc với LLM hơn phiếu thật. Bù lại bằng: bác sĩ gán nhãn ~30 ca (tuần 4), và nhờ bác sĩ viết lại 3–5 phiếu theo đúng văn phong thường ngày.
- R2 dùng quy tắc tạm (`nguon: tu_dung`) cho đến khi tra xong Luật BHYT sửa đổi 51/2024, TT 01/2025.
- Ca thử để `ma: null` cho siêu âm tim cản âm; mã đã tra là `02.0115.0005`, `02.0444.0005`, `18.0051.0005` (`data/rules/NGUON.md` mục 2.4c).
