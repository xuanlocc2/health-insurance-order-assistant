# 09 — Spec kỹ thuật MVP

**Trạng thái:** bản 2, 12/11/2026 (đã sửa theo review độc lập) · **Yêu cầu:** [07-prd.md](07-prd.md) (F-xx, AC-xx) · **Bộ test:** [data/test-cases/](../data/test-cases/)

**Nguyên tắc**
1. Mọi ngưỡng, danh sách nằm trong YAML, có `nguon: van_ban | tu_dung | bac_si_duyet` và `diem_mo_ho` nếu có. Code không chứa giá trị nghiệp vụ.
2. Thiếu dữ liệu, không nạp được rule, hay không có nhánh nào áp dụng → **Cần xem lại**. Không bao giờ suy thành "Phù hợp".
3. AI không đưa dòng tới "Phù hợp", và không tự gây "Không được chi trả" — kể cả qua số liệu AI trích.
4. Kết luận dựa trên giá trị `tu_dung` phải nói rõ điều đó với bác sĩ.

Schema này **thay thế** schema trong [data/rules/README.md](../data/rules/README.md).

## 1. Bố cục

```
data/rules/
  danh-muc.yaml        # R1: 50 dịch vụ {ma, ten, bi_danh[], bhyt: co|dieu_kien|khong_thay|xac_minh}, chuyển một lần từ file .md
  dieu-kien.yaml       # R3: điều kiện của CRP, PCT, Doppler (mục 2)
  tham-so.yaml         # ngưỡng, tuổi, tham chiếu (mục 3)
src/
  engine.py            # một lượt khám → trạng thái từng dòng (mục 4–6); quy tắc R2 viết thẳng ở đây
  a1.py                # gọi LLM + kiểm tra trích dẫn (mục 7); có stub cho test
  log.py               # JSONL (mục 9)
  app.py               # Streamlit (mục 10)
tests/                 # mục 11
```

## 2. Schema điều kiện (`dieu-kien.yaml`)

Nhánh (HOẶC) → vế (VÀ) → loại trừ. Khoảng luôn **nửa mở** `[tu, den)`, đơn vị ghi rõ.

```yaml
"23.0228.1483":
  ten: "Định lượng CRP"
  nguyen_van: "Chẩn đoán, theo dõi một trong các trường hợp sau đây: ..."
  can_cu: [{ van_ban: "TT 35/2016 sđ TT 39/2024", phu_luc: "DM1", stt: 7 }]
  nhanh:
    - id: a_tre_em
      ap_dung: { tuoi_thang: [0, "@tre_em_den_thang"] }
      ve:
        - id: V1
          mo_ta: "Nhiệt độ ≤ 36°C hoặc ≥ 38,3°C"
          hoac:
            - { loai: so_sanh, truong: nhiet_do, toan_tu: "<=", gia_tri: 36 }
            - { loai: so_sanh, truong: nhiet_do, toan_tu: ">=", gia_tri: 38.3 }
        - id: V2
          mo_ta: "Nhịp tim hoặc nhịp thở quá giới hạn sinh lý theo tuổi"
          hoac:
            - { loai: nguong_theo_tuoi, truong: nhip_tho, bang: "@nhip_tho_nhanh" }
            - { loai: nguong_theo_tuoi, truong: mach, bang: "@nhip_tim_nhanh" }
        - id: V3
          mo_ta: "Nghi ngờ có ổ nhiễm trùng"
          kiem: { loai: ai_doc, cau_hoi: "Phiếu khám có ghi một ổ hoặc dấu hiệu nhiễm trùng cụ thể của chính bệnh nhân không?" }
    - id: b_so_sinh
      ap_dung: { tuoi_ngay: [0, 29], nguon: tu_dung, diem_mo_ho: M-06 }
      ve:
        - id: B1
          mo_ta: "Nhiễm trùng sơ sinh"
          kiem: { loai: icd_trong, ds: ["P36"], nguon: tu_dung, neu_khong_khop: ai_doc,
                  cau_hoi: "Phiếu khám có ghi nghi ngờ hoặc dấu hiệu nhiễm trùng sơ sinh không?" }
    - id: c_mach_vanh
      ve: [{ id: C1, mo_ta: "Bệnh mạch vành, nhồi máu cơ tim", kiem: { loai: icd_trong, ds: ["I20", "I21", "I22", "I23", "I24", "I25"], nguon: tu_dung } }]
    - id: d_tu_mien
      ve: [{ id: D1, mo_ta: "Viêm da nhiễm độc, các bệnh tự miễn",
             kiem: { loai: icd_trong, ds: ["M30.3", "M08", "M32", "D69.0", "L51"], nguon: tu_dung, diem_mo_ho: M-07 } }]
  diem_mo_ho: [M-01, M-02, M-04, M-06, M-07]
```

PCT có thêm `tan_suat` và `loai_tru`:

```yaml
"23.0130.1549":
  nhanh:
    - id: n1_nhiem_trung_huyet
      ap_dung: { tuoi_thang: [0, "@tre_em_den_thang"] }
      ve: [{ id: N1, mo_ta: "Nhiễm trùng huyết", kiem: { loai: ai_doc, cau_hoi: "..." } }]
    - id: n2_suy_da_co_quan
      ap_dung: { tuoi_thang: [0, "@tre_em_den_thang"] }
      ve: [{ id: N2, mo_ta: "Rối loạn chức năng từ 2 cơ quan trở lên",
             kiem: { loai: ai_doc, cau_hoi: "...", toi_da: chua_thay, diem_mo_ho: M-09 } }]   # A1 chỉ trích, không tự đạt
  tan_suat: { toi_thieu_gio: 24, nen_gio: 48, nguon: tu_dung, diem_mo_ho: M-10 }
  loai_tru:
    mo_ta: "Hết dấu hiệu chỉ định và Procalcitonin ≤ 02 lần giá trị tham chiếu"
    ve:
      - { id: X1, mo_ta: "Hết dấu hiệu chỉ định", kiem: { loai: ai_doc, cau_hoi: "Phiếu khám có ghi bệnh nhân đã hết các dấu hiệu nhiễm trùng không?" } }
      - { id: X2, mo_ta: "PCT lần trước ≤ 2 × tham chiếu",
          kiem: { loai: lich_su_so_sanh, ma: "23.0130.1549", toan_tu: "<=", he_so: 2, tham_chieu: "@pct_tham_chieu" } }
```

Doppler: một nhánh, một vế `{ loai: khong_cung_luot, ma_hoac_bi_danh: ["Siêu âm tim cản âm", "Siêu âm tim có cản âm"], diem_mo_ho: M-11 }`.

### Loại kiểm tra

| Loại | Kết quả |
|---|---|
| `so_sanh` | `dat` / `khong_dat`. Ô trống → nhờ A1 trích số (mục 7). Vẫn trống → `chua_du_du_lieu` |
| `nguong_theo_tuoi` | như trên; tuổi không có dòng trong bảng → `chua_du_du_lieu` |
| `icd_trong` | so tiền tố. `icd: []` → `chua_du_du_lieu`. Có ICD, không khớp → `neu_khong_khop` (mặc định `khong_dat`, hoặc `ai_doc`) |
| `ai_doc` | `dat` / `chua_thay` (A1). Có `toi_da: chua_thay` → `dat` bị hạ xuống `chua_thay`, giữ trích dẫn |
| `lich_su_so_sanh` | bản ghi cùng mã gần nhất; ưu tiên `tham_chieu_tren` của bản ghi, rồi mới tới tham số. Không có lịch sử → `chua_du_du_lieu` |
| `khong_cung_luot` | `khong_dat` nếu dịch vụ đó có trong cùng `luot_kham`, ngược lại `dat` |

## 3. tham-so.yaml

```yaml
tre_em_den_thang: { gia_tri: 192, nguon: tu_dung, diem_mo_ho: M-01 }   # [0, 192) tháng
nhip_tho_nhanh:
  nguon: tu_dung
  diem_mo_ho: M-02
  bang:                     # tuổi tháng [tu, den) → ngưỡng ≥
    - { tu: 0, den: 2, nguong: 60 }
    - { tu: 2, den: 12, nguong: 50 }
    - { tu: 12, den: 60, nguong: 40 }
nhip_tim_nhanh: { nguon: tu_dung, diem_mo_ho: M-02, bang: [] }
pct_tham_chieu: { gia_tri: 0.5, don_vi: ng/mL, nguon: tu_dung, diem_mo_ho: M-10 }
khoang_hop_le: { nhiet_do: [34, 43], mach: [40, 250], nhip_tho: [10, 120] }   # chặn số A1 trích nhầm
```

## 4. Đầu vào và tuổi

Đầu vào một lượt khám giống cấu trúc ca test (trừ `ky_vong`, `he_chi_rule`): `luot_kham`, `lan_tich`, `ngay_kham`, `benh_nhan {tuoi_ngay | tuoi_thang, the}`, `icd[]`, `sinh_hieu`, `phieu_kham`, `lich_su[]`, `chi_dinh[{ma, ten}]`.

- **Engine không có mặc định.** Thiếu khóa nào là thiếu dữ liệu. Mặc định của bộ test (ngày khám, thẻ còn hạn) chỉ áp trong loader của test và app mô phỏng.
- **Tuổi:** có `tuoi_ngay` thì `tuoi_thang = floor(tuoi_ngay / 30.44)`. Chỉ có `tuoi_thang`: điều kiện tính theo ngày → nếu `tuoi_thang ≥ 1` thì không áp dụng; nếu `= 0` thì `chua_du_du_lieu`. Không có tuổi → mọi nhánh có `ap_dung` thành `chua_du_du_lieu`.
- **Khóa dòng:** `thu_tu` (vị trí trong danh sách chỉ định). Định danh dịch vụ: `ma`; `ma` trống → tên chuẩn hóa (bỏ dấu cách thừa, chữ thường, NFC).

## 5. Luồng xử lý một dòng

Mỗi lần tích chạy toàn bộ luồng trên dữ liệu đang có (F-02). Trạng thái dòng = **nặng nhất** trong các bước:
Không được chi trả > Cần xem lại > Cần xem lại · đủ căn cứ > Phù hợp quy tắc BHYT.

1. **R2 thẻ:** `the: null` hoặc thiếu → Cần xem lại. `han_den < ngay_kham` → Không được chi trả. Gắn `muc_huong`.
2. **R1 danh mục:** khớp chính xác mã, hoặc tên/bí danh đã chuẩn hóa (không khớp mờ). `khong_thay` → Không được chi trả. `xac_minh` hoặc không tìm thấy → Cần xem lại. `dieu_kien` mà không có mục trong `dieu-kien.yaml` → Cần xem lại.
3. **R4 trùng:** cùng định danh, thứ tự ≥ 2 trong cùng lượt → **Cần xem lại** ("trùng dòng trong cùng lượt khám"). Không kết luận Không được chi trả vì văn bản không có điều khoản (ranh giới ở [02](02-giai-phap.md)).
4. **Tần suất** (`tan_suat`, chỉ PCT): giờ kể từ bản ghi cùng mã gần nhất `= ngay_cach × 24`. `< toi_thieu_gio` → Không được chi trả. `[toi_thieu_gio, nen_gio)` → Cần xem lại (có thể hợp lệ nếu sốc nhiễm trùng).
5. **R3 điều kiện:**
   a. Đánh giá mọi vế rule của các nhánh áp dụng.
   b. **Không có nhánh nào áp dụng → Cần xem lại.** Mọi nhánh đã có vế `khong_dat` từ dữ liệu nhập (không phải số A1) → Không được chi trả, không gọi A1.
   c. Còn lại: gọi A1 **một lần** cho các vế `ai_doc` chưa có kết quả và các trường số còn trống của nhánh còn sống. Danh sách rỗng → không gọi.
   d. Gộp theo mục 6.

## 6. Gộp trạng thái (chốt 12/11/2026)

**Nguồn của một kết quả:** `nhap` (ô có cấu trúc) hoặc `a1` (A1 đọc hoặc trích số). **Kết quả `khong_dat` có nguồn `a1` bị hạ thành `chua_du_du_lieu`.** Chỉ `dat` từ A1 được dùng.

**Vế** có `hoac`: có con `dat` → `dat` (nguồn của con đó); mọi con `khong_dat` → `khong_dat`; còn lại → `chua_du_du_lieu`.

**Nhánh** (VÀ): có vế `khong_dat` → **trượt**; mọi vế `dat` từ `nhap` → **đạt bằng rule**; mọi vế `dat`, có vế từ `a1` → **đạt có AI**; còn lại → **chưa rõ**.

**Điều kiện** (HOẶC, bỏ nhánh không áp dụng):

| Điều kiện | Trạng thái |
|---|---|
| Không có nhánh áp dụng | Cần xem lại |
| Có nhánh đạt bằng rule | Phù hợp quy tắc BHYT |
| Có nhánh đạt có AI | Cần xem lại · đủ căn cứ |
| Mọi nhánh trượt | Không được chi trả |
| Còn lại | Cần xem lại |

**Loại trừ** chỉ áp dụng khi **mọi** vế `dat`: tất cả từ `nhap` → Không được chi trả; có vế từ `a1` → Cần xem lại. Có vế khác `dat` → loại trừ không áp dụng. Trạng thái = nặng nhất(điều kiện, loại trừ).

**Hệ chỉ-rule** (`he_chi_rule` trong ca test, để đo giá trị A1): chạy cùng thuật toán nhưng không có A1; vế `ai_doc` = `chua_du_du_lieu`, riêng nhánh có cả vế rule thì vế `ai_doc` được bỏ qua. Sinh bằng máy, không viết tay.

## 7. A1

**Đầu vào:** phiếu khám nguyên văn; câu hỏi `{id, mo_ta, cau_hoi}`; trường số cần trích `{truong, don_vi}`.

**Đầu ra:** JSON qua `output_config.format` (structured output; không dùng ép `tool_choice`).

```json
{ "ve": [ { "id": "V3", "ket_qua": "dat | chua_thay",
            "trich_dan": "nguyên văn hoặc null", "trich_lien_quan": ["..."] } ],
  "so_lieu": [ { "truong": "nhip_tho", "gia_tri": 58, "trich_dan": "thở nhanh 58 l/p" } ] }
```

**Prompt:** chỉ dấu hiệu của chính bệnh nhân; câu phủ định và bệnh người nhà không phải căn cứ; số liệu chỉ lấy **số đo tại lần khám này**, không lấy số theo lời kể hay lần trước (M-03); không đánh giá chỉ định, không gợi ý ghi thêm (CDI); không chắc → `chua_thay`.

**Kiểm tra bằng code (F-08), áp cho mọi đoạn trích:**
- Chuẩn hóa NFC, khoảng trắng, dấu phẩy thập phân → dấu chấm ở cả hai phía; đoạn trích phải là chuỗi con của phiếu khám.
- `trich_dan` không khớp → vế `chua_thay`, log `loi: trich_dan_khong_khop`. `dat` mà `trich_dan` null → `chua_thay`. Phần tử `trich_lien_quan` không khớp → bỏ.
- `so_lieu`: trích dẫn khớp, chứa `gia_tri` như **một token số trọn vẹn** (58 không khớp "158"), và nằm trong `khoang_hop_le`. Không đạt → trường vẫn trống.
- Lỗi mạng, hết giờ, `stop_reason` là `refusal` hoặc `max_tokens` → mọi vế AI `chua_thay`. Không chặn bác sĩ.
- Hiển thị: mở rộng đoạn trích ra trọn câu chứa nó, để bác sĩ thấy ngữ cảnh ("Mẹ đang viêm họng").

**Model:** `.env`, mặc định `claude-opus-5-5`. Chỉ dữ liệu giả. Không chỉnh được `temperature`, nên kết quả chỉ cố định ở chế độ stub.

**Chế độ:** `A1_MODE=stub` (mặc định khi test) sinh kết quả A1 từ `ky_vong` của ca (vế AI + khối `a1_gia_lap.so_lieu` nếu ca cần trích số) → test engine chạy được từ tuần 3, không phụ thuộc LLM. `A1_MODE=live` chỉ dùng để đo chỉ số PRD mục 8.

## 8. Đầu ra một dòng

```json
{ "thu_tu": 2, "ma": "23.0228.1483", "ten": "Định lượng CRP",
  "trang_thai": "Cần xem lại · đủ căn cứ", "o_bhyt_goi_y": "tich", "to_mau": true,
  "ly_do": "...", "muc_huong": 100,
  "checklist": [ { "nhanh": "a_tre_em", "id": "V2", "mo_ta": "...", "ket_qua": "dat",
                   "nguon_ket_qua": "a1", "bang_chung": "A1 trích 'NT 45 l/p' → 45 ≥ 40",
                   "trich_dan": null, "nguon_quy_tac": "tu_dung", "diem_mo_ho": ["M-02"] } ],
  "can_cu": [ ... ], "phien_ban_rule": "..." }
```

**Ô BHYT gợi ý:** Phù hợp → `tich`; đủ căn cứ → `tich` + `to_mau`; Không được chi trả → `trong`; Cần xem lại → `null` (bác sĩ tự chọn). Ba dòng `if` trong code; đổi khi có câu trả lời phiếu hỏi câu 10.

**Lý do:** lấy từ bước nặng nhất, theo thứ tự R2 → R1 → R4/tần suất → R3. Mẫu câu (không LLM):

| Mã | Mẫu |
|---|---|
| `the_het_han` | "Thẻ BHYT hết hạn {han_den}" |
| `the_thieu` | "Chưa có thông tin thẻ BHYT" |
| `khong_thay` | "Không tìm thấy trong danh mục kỹ thuật đã tra" |
| `xac_minh` / `chua_tra` | "Chưa xác minh trong danh mục" / "Ngoài danh sách đã tra" |
| `trung_dong` | "Trùng dịch vụ trong cùng lượt khám" |
| `tan_suat` | "Đã làm cách {gio} giờ; giới hạn {nen_gio} giờ" |
| `ve_khong_dat` | "{mo_ta}: {bang_chung} chưa đạt" |
| `ve_chua_thay` | "Điều kiện có vế '{mo_ta}'; phiếu khám chưa thấy nội dung tương ứng" |
| `ve_chua_du` | "Chưa đủ dữ liệu cho vế '{mo_ta}'" |
| `khong_nhanh` | "Không có nhánh điều kiện áp dụng cho tuổi này" |
| `loai_tru` | "Có thể thuộc điều khoản không thanh toán: {mo_ta}" |

Kết luận dựa trên giá trị `tu_dung` → thêm hậu tố cố định: "(cách hiểu tạm {M-xx}, chưa được bác sĩ duyệt)".

`phien_ban_rule` = hash của cả thư mục `data/rules/`.

## 9. Log (F-12, F-13)

Một dòng JSONL mỗi lần xác nhận một dòng chỉ định, chỉ ghi thêm (`logs/xac-nhan.jsonl`). Khóa: `luot_kham + lan_tich + thu_tu`.

```json
{ "thoi_gian": "...", "luot_kham": "...", "lan_tich": 1, "thu_tu": 2, "ma": "...", "ten": "...",
  "trang_thai": "...", "o_bhyt_goi_y": "tich | trong | null", "bac_si_chon": "tich | khong_tich",
  "ly_do_bac_si": { "loai": "nguoi_nha_yeu_cau | loai_tru_theo_doi | khac", "ghi_chu": "..." },
  "checklist": [...], "can_cu": [...], "phien_ban_rule": "...",
  "dau_vao": { "tuoi": ..., "the": {...}, "icd": [...], "sinh_hieu": {...}, "lich_su_da_dung": [...] } }
```

`ly_do_bac_si` bắt buộc khi: bỏ tích dòng gợi ý `tich`, hoặc tích dòng Không được chi trả. Dòng Cần xem lại (gợi ý `null`) chọn gì cũng không cần lý do.

## 10. Màn hình mô phỏng (F-14)

Streamlit, một trang: chọn ca → thẻ, sinh hiệu, ICD, phiếu khám bên trái; bảng chỉ định với ô BHYT gợi ý và trạng thái bên phải; bấm dòng → checklist, trích dẫn tô màu trong phiếu khám, nhãn "cách hiểu tạm" nếu có; nút Xác nhận ghi log. Engine nhận/trả JSON, nên khi gắn Eform/VIS chỉ thay lớp này.

## 11. Test

- Chạy mọi `data/test-cases/*.yaml` ở `A1_MODE=stub`: so `trang_thai` từng dòng (khóa `thu_tu`), và `ket_qua` của vế có `id`.
- Unit test bắt buộc: bảng gộp mục 6 (mọi tổ hợp nhánh, gồm không có nhánh áp dụng); số A1 `khong_dat` bị hạ; `ai_doc` với `toi_da`; trích dẫn sửa một chữ → `chua_thay` (AC-11); 58 không khớp "158"; số ngoài khoảng hợp lệ bị bỏ; R4 với hai dòng `ma: null` khác tên.
- `he_chi_rule` sinh bằng máy theo mục 6 rồi so với giá trị trong ca.

## 12. Truy vết PRD

| PRD | Spec |
|---|---|
| F-01, F-09 | Mục 6 |
| F-02 | Mục 4, 5 |
| F-03, F-04, F-06 | Mục 5 bước 1–3 |
| F-05 | Mục 2, 3, 5 bước 5 |
| F-07, F-08 | Mục 7 |
| F-10, F-11 | Mục 8 |
| F-12, F-13 | Mục 9 |
| F-14 | Mục 10 |
| AC-01…AC-12 | Mục 11 |

## Còn mở

- Ngưỡng nhịp tim theo tuổi (M-02): đến khi có, V2 chỉ đạt qua nhịp thở.
- Danh sách ICD nhánh c, d của CRP là tạm (M-07).
- Quy tắc R2: tạm, chờ tra Luật BHYT sửa đổi 51/2024, TT 01/2025.
- Mã siêu âm tim cản âm: chưa tra, đang khớp bằng bí danh.
