# Quy tắc BHYT (rules)

Thư mục này chứa các quy tắc dùng để kiểm tra dòng chỉ định có phù hợp quy tắc BHYT hay không (R1–R4 trong [docs/02-giai-phap.md](../../docs/02-giai-phap.md)). Quy tắc viết bằng **YAML**. YAML là nguồn duy nhất. Bảng để bác sĩ duyệt được xuất từ YAML, không sửa tay.

## File đang dùng (MVP)

| File | Nội dung |
|---|---|
| [danh-muc.yaml](danh-muc.yaml) | R1: 50 dịch vụ (55 dòng mã), tên theo PL01 TT 23/2024, trạng thái `co`, `dieu_kien`, `khong_thay`, `xac_minh` |
| [dieu-kien.yaml](dieu-kien.yaml) | R3: điều kiện thanh toán của các dịch vụ `dieu_kien`, kèm nguyên văn |
| [tham-so.yaml](tham-so.yaml) | Ngưỡng và bảng tự dựng, mỗi giá trị gắn một điểm mơ hồ M-xx |
| [NGUON.md](NGUON.md) | Sổ kiểm chứng: file, trang, câu nguyên văn và cách hiểu của từng quy tắc; mục "R2 thẻ BHYT" |
| [check_rules.py](check_rules.py) | Kiểm tra ba file YAML: `python data/rules/check_rules.py` |

## Ba lớp

| Lớp | Thư mục | Nội dung | Ai sửa |
|---|---|---|---|
| 1. Quốc gia | `national/` | Danh mục, tỷ lệ, điều kiện theo văn bản của BYT, gắn với mã kỹ thuật chuẩn | Nhóm dự án, theo văn bản |
| 2. Bệnh viện | `hospital/` *(chưa làm)* | Mã nội bộ Vinmec ↔ mã chuẩn, danh mục viện đã đăng ký, giá | Viện |
| 3. Ghi đè nội bộ | `overrides/` *(chưa làm)* | File Excel BHYT của viện, rút kinh nghiệm từ các lần bị xuất toán | Viện |

Lớp sau ghi đè lớp trước. Lớp 2 và 3 chỉ làm khi có dữ liệu thật của viện.

## Lớp 1: cấu trúc file

> **Đã thay thế (12/11/2026):** MVP dùng schema nhánh → vế → loại trừ ở [docs/09-spec.md](../../docs/09-spec.md) mục 1–3 (3 file: `danh-muc.yaml`, `dieu-kien.yaml`, `tham-so.yaml`). Phần dưới giữ để tham khảo hướng 3 lớp sau MVP.

Mỗi file là một dịch vụ, đặt tên theo nhóm: `national/<nhom>/<ten-ngan>.yaml`.

```yaml
ma_chuan: "..."               # mã kỹ thuật TT 23/2024 PL01 (cột 2 = STT theo TT 43/2013, TT 21/2017); dùng đến 31/12/2027
ma_pl02: null                 # mã TT 23/2024 PL02, chỉ áp dụng từ 01/01/2028 (TT 25/2026 lùi mốc); điền sau
ten: "Định lượng CRP"         # tên đúng như trong văn bản
nhom: xet_nghiem              # xet_nghiem | cdha | tdcn
bhyt:
  trong_danh_muc: true        # true | false | null (chưa tra)
  ty_le_thanh_toan: 100       # % theo văn bản; null nếu chưa tra
  dieu_kien:
    nguyen_van: null          # chép NGUYÊN VĂN điều kiện trong văn bản, không diễn giải
    ve:                       # tách điều kiện thành từng vế; mọi vế phải đạt
      - mo_ta: "Nhiệt độ ≤ 36°C hoặc ≥ 38,3°C"
        kiem_bang: rule       # rule (trường có cấu trúc) | ai (A1 đọc phiếu khám)
        kiem_tra_may: "nhiet_do <= 36 or nhiet_do >= 38.3"   # null → "Cần xem lại"
      - mo_ta: "Nghi ổ nhiễm trùng"
        kiem_bang: ai
        kiem_tra_may: null
can_cu:                       # bắt buộc khi trong_danh_muc khác null
  - van_ban: "TT 35/2016/TT-BYT, sửa bởi TT 39/2024/TT-BYT"
    phu_luc: "..."
    stt: 0
    file: data/van-ban/...    # file văn bản gốc đã tải
hieu_luc: { tu: 2025-01-01, den: null }
icd_phu_hop:                  # R3: hiện KHÔNG có bảng chính thức ICD ↔ dịch vụ
  nguon: tu_dung              # van_ban | tu_dung | bac_si_duyet
  ma: []                      # mã hoặc khoảng mã ICD-10, ví dụ "J00-J22"
tan_suat:                     # R4
  nguon: tu_dung
  toi_thieu_cach_ngay: null
duyet: { nguoi: null, ngay: null }
```

## Ba nguyên tắc

1. **Mọi trường đều ghi nguồn.** Lấy từ văn bản thì phải có `can_cu`. Phần tự dựng (ICD, tần suất) thì ghi `nguon: tu_dung` cho đến khi bác sĩ duyệt. Không ai được nhầm phần tự dựng là quy định của Bộ Y tế.
2. **Không chắc thì để `null`.** Engine coi `null` là "Cần xem lại". Engine không bao giờ đoán thành "Phù hợp quy tắc BHYT".
3. **Có ngày hiệu lực.** Khi văn bản thay đổi, đóng `hieu_luc.den` của quy tắc cũ rồi thêm quy tắc mới, không xóa quy tắc cũ. Nhờ vậy, khi bị xuất toán vẫn tra lại được quy tắc đúng vào ngày chỉ định.

Danh sách dịch vụ đang làm: [data/danh-muc/nhi-ngoai-tru-de-xuat.md](../danh-muc/nhi-ngoai-tru-de-xuat.md). Văn bản gốc: [data/van-ban/](../van-ban/).
