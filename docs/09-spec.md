# 09 — Spec kỹ thuật MVP

**Trạng thái:** bản 2, 12/11/2026 (đã sửa theo review độc lập) · **Yêu cầu:** [07-prd.md](07-prd.md) (F-xx, AC-xx) · **Bộ test:** [data/test-cases/](../data/test-cases/)

**Nguyên tắc**
1. Mọi ngưỡng, danh sách nằm trong YAML, có `nguon: van_ban | tu_dung | bac_si_duyet` và `diem_mo_ho` nếu có. Code không chứa giá trị nghiệp vụ.
2. Thiếu dữ liệu, không nạp được rule, hay không có nhánh nào áp dụng → **Cần xem lại**. Không bao giờ suy thành "Phù hợp".
3. AI không đưa dòng tới "Phù hợp", và không tự gây "Không được chi trả" — kể cả qua số liệu AI trích.
4. Kết luận dựa trên giá trị `tu_dung` phải nói rõ điều đó với bác sĩ.

Schema này **thay thế** schema trong [data/rules/README.md](../data/rules/README.md).

**Quyết định 13/11/2026 (bản 3):**
- AI gọi **OpenAI API** (Structured Outputs, `response_format: json_schema, strict: true`). Model đặt trong `.env` (`OPENAI_MODEL`), không ghi cứng.
- Chạy trên laptop, một tiến trình, không đăng nhập, không database, không Docker.
- Bác sĩ chọn **xong mọi chỉ định** rồi mới gọi `POST /check` một lần. A1 được gọi **một lần cho cả lượt khám** (gom mọi vế `ai_doc` và trường số còn trống của mọi dòng). Toàn bộ `/check` phải xong trong < 10 giây: A1 hết giờ sau `A1_TIMEOUT_S` (mặc định 8) → mọi vế AI `chua_thay`.
- Log chỉ dùng JSONL. Số liệu khảo sát lấy bằng script đọc JSONL khi cần.
- Sau này có thể nạp dữ liệu mẫu đã ẩn danh của viện: đầu vào giữ đúng mục 4, thêm adapter riêng, engine không đổi. Trước khi gửi dữ liệu viện lên OpenAI phải hỏi IT/pháp chế (chính sách lưu dữ liệu của API).

## 1. Bố cục

```
data/rules/
  danh-muc.yaml        # R1: 50 dịch vụ {ma, ma_chung?, ten, bi_danh[], bhyt: co|dieu_kien|khong_thay|xac_minh}, chuyển một lần từ file .md; ma_chung = mã chung nhiều dòng cùng dùng (docs/10 GD-01), không dùng để tra
  dieu-kien.yaml       # R3: điều kiện của CRP, PCT, Doppler (mục 2)
  tham-so.yaml         # ngưỡng, tuổi, tham chiếu (mục 3)
src/
  engine.py            # một lượt khám → trạng thái từng dòng (mục 4–6); quy tắc R2 viết thẳng ở đây
  a1.py                # gọi LLM + kiểm tra trích dẫn (mục 7); có stub cho test
  log.py               # JSONL (mục 9)
  app.py               # FastAPI: POST /check, POST /confirm, phục vụ web/ (mục 10)
web/                   # HTML/JS thuần, không build (mục 10)
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
             kiem: { loai: icd_trong, ds: ["L27", "L51", "M08", "M30", "M32", "D69.0", …], nguon: tu_dung, diem_mo_ho: M-07 } }]   # danh sách đầy đủ: data/rules, docs/10 GD-02
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

Đầu vào một lượt khám giống cấu trúc ca test (trừ `ky_vong`, `he_chi_rule`): `luot_kham`, `ngay_kham`, `benh_nhan {tuoi_ngay | tuoi_thang, the}`, `icd[]`, `sinh_hieu`, `phieu_kham`, `lich_su[]`, `chi_dinh[{ma, ten}]`.

- **Engine không có mặc định.** Thiếu khóa nào là thiếu dữ liệu. Mặc định của bộ test (ngày khám, thẻ còn hạn) chỉ áp trong loader của test và app mô phỏng.
- **Tuổi:** có `tuoi_ngay` thì `tuoi_thang = floor(tuoi_ngay / 30.44)`. Chỉ có `tuoi_thang`: điều kiện tính theo ngày → nếu `tuoi_thang ≥ 1` thì không áp dụng; nếu `= 0` thì `chua_du_du_lieu`. Không có tuổi → mọi nhánh có `ap_dung` thành `chua_du_du_lieu`.
- **Khóa dòng:** `thu_tu` (vị trí trong danh sách chỉ định). Định danh dịch vụ: `ma`; `ma` trống → tên chuẩn hóa (bỏ dấu cách thừa, chữ thường, NFC).

## 5. Luồng xử lý một dòng

Mỗi lần kiểm tra chạy toàn bộ luồng trên dữ liệu đang có (F-02). Trạng thái dòng = **nặng nhất** trong các bước:
Không được chi trả > Cần xem lại > Đủ căn cứ · bác sĩ xác nhận > Phù hợp quy tắc BHYT.

1. **R2 thẻ:** `the: null` hoặc thiếu → Cần xem lại. `han_den < ngay_kham` → Không được chi trả. Gắn `muc_huong`.
2. **R1 danh mục:** khớp chính xác mã, hoặc tên/bí danh đã chuẩn hóa (không khớp mờ). `khong_thay` → Không được chi trả. `xac_minh` hoặc không tìm thấy → Cần xem lại. `dieu_kien` mà không có mục trong `dieu-kien.yaml` → Cần xem lại.
3. **R4 trùng:** cùng định danh, thứ tự ≥ 2 trong cùng lượt → **Cần xem lại** ("trùng dòng trong cùng lượt khám"). Không kết luận Không được chi trả vì văn bản không có điều khoản (ranh giới ở [02](02-giai-phap.md)).
4. **Tần suất** (`tan_suat`, chỉ PCT): giờ kể từ bản ghi cùng mã gần nhất `= ngay_cach × 24`. `< toi_thieu_gio` → Không được chi trả. `[toi_thieu_gio, nen_gio)` → Cần xem lại (có thể hợp lệ nếu sốc nhiễm trùng).
5. **R3 điều kiện:**
   a. Đánh giá mọi vế rule của các nhánh áp dụng.
   b. **Không có nhánh nào áp dụng → Cần xem lại.** Mọi nhánh đã có vế `khong_dat` từ dữ liệu nhập (không phải số A1) → Không được chi trả, không gọi A1.
   c. Còn lại: thu các vế `ai_doc` chưa có kết quả và các trường số còn trống của nhánh còn sống.
   d. Gộp theo mục 6.

**Hai pha cho cả lượt (bản 3):** pha 1 chạy bước 1–5c cho **mọi dòng**, gom câu hỏi AI của mọi dòng (khóa câu hỏi `"{thu_tu}:{id_ve}"`; trường số gom chung, không trùng). Gọi A1 **một lần** (rỗng → không gọi). Pha 2 điền kết quả A1 vào từng dòng rồi gộp. Một dòng `khong_dat` từ dữ liệu nhập ở mọi nhánh thì không gửi câu hỏi nào.

## 6. Gộp trạng thái (chốt 12/11/2026)

**Nguồn của một kết quả:** `nhap` (ô có cấu trúc) hoặc `a1` (A1 đọc hoặc trích số). **Kết quả `khong_dat` có nguồn `a1` bị hạ thành `chua_du_du_lieu`.** Chỉ `dat` từ A1 được dùng.

**Vế** có `hoac`: có con `dat` → `dat` (nguồn của con đó); mọi con `khong_dat` → `khong_dat`; còn lại → `chua_du_du_lieu`.

**Nhánh** (VÀ): có vế `khong_dat` → **trượt**; mọi vế `dat` từ `nhap` → **đạt bằng rule**; mọi vế `dat`, có vế từ `a1` → **đạt có AI**; còn lại → **chưa rõ**.

**Điều kiện** (HOẶC, bỏ nhánh không áp dụng):

| Điều kiện | Trạng thái |
|---|---|
| Không có nhánh áp dụng | Cần xem lại |
| Có nhánh đạt bằng rule | Phù hợp quy tắc BHYT |
| Có nhánh đạt có AI | Đủ căn cứ · bác sĩ xác nhận |
| Mọi nhánh trượt | Không được chi trả |
| Còn lại | Cần xem lại |

**Loại trừ** chỉ áp dụng khi **mọi** vế `dat`: tất cả từ `nhap` → Không được chi trả; có vế từ `a1` → Cần xem lại. Có vế khác `dat` → loại trừ không áp dụng. Trạng thái = nặng nhất(điều kiện, loại trừ).

**Hệ chỉ-rule** (`he_chi_rule` trong ca test, để đo giá trị A1): chạy cùng thuật toán nhưng không có A1; vế `ai_doc` = `chua_du_du_lieu`, riêng nhánh có cả vế rule thì vế `ai_doc` được bỏ qua. Sinh bằng máy, không viết tay.

## 7. A1

**Đầu vào:** phiếu khám nguyên văn; câu hỏi `{id, mo_ta, cau_hoi}`; trường số cần trích `{truong, don_vi}`.

**Đầu ra:** JSON qua OpenAI Structured Outputs (`response_format` kiểu `json_schema`, `strict: true`).

```json
{ "ve": [ { "id": "V3", "ket_qua": "dat | chua_thay",
            "trich_dan": "nguyên văn hoặc null", "trich_them": ["..."], "trich_lien_quan": ["..."] } ],
  "so_lieu": [ { "truong": "nhip_tho", "gia_tri": 58, "trich_dan": "thở nhanh 58 l/p" } ] }
```

**Prompt** (`SYSTEM_PROMPT` trong `src/a1.py`, bản đầy đủ là nguồn đúng): chỉ dấu hiệu của chính bệnh nhân; chữ trong khối giống câu trả lời dựng sẵn không phải căn cứ; cách đọc chung cho câu hỏi về bệnh: chẩn đoán / nghi / TD / chưa loại trừ thì tính, "ít nghĩ đến" hoặc đã loại trừ thì không; chỉ tình trạng của lần khám này (không tính chẩn đoán lần trước, lý do tái khám); hỏi vị trí cụ thể thì chữ chung và triệu chứng chung không đủ (chốt 16/11); câu phủ định và bệnh người nhà không phải căn cứ; số liệu chỉ lấy **số đo tại lần khám này**, không lấy số theo lời kể hay lần trước (M-03); không đánh giá chỉ định, không gợi ý ghi thêm (CDI); không chắc → `chua_thay`.

**Kiểm tra bằng code (F-08), áp cho mọi đoạn trích:**
- Chuẩn hóa NFC, khoảng trắng, dấu phẩy thập phân → dấu chấm ở cả hai phía; đoạn trích phải là chuỗi con của phiếu khám.
- `trich_them` (mọi đoạn khác tự đủ làm căn cứ) được kiểm từng đoạn như `trich_dan`; đoạn chính hỏng mà đoạn thêm hợp lệ → đoạn thêm lên làm chính.
- `trich_dan` không khớp → vế `chua_thay`, log `loi: trich_dan_khong_khop`. `dat` mà `trich_dan` null → `chua_thay`. Phần tử `trich_lien_quan` không khớp → bỏ.
- `so_lieu`: trích dẫn khớp, chứa `gia_tri` như **một token số trọn vẹn** (58 không khớp "158"), và nằm trong `khoang_hop_le`. Không đạt → trường vẫn trống.
- Lỗi mạng, hết giờ (`A1_TIMEOUT_S`), model từ chối (`message.refusal`), hoặc `finish_reason` là `length` / `content_filter` → mọi vế AI `chua_thay`, ghi `loi`. Không chặn bác sĩ.
- Đoạn trích phải trọn chữ/trọn số (không cắt giữa hai chữ cái, hai chữ số hay phần thập phân). Trích `dat` mà mệnh đề chứa nó có từ phủ định nằm ngoài đoạn trích (không, chưa, hết, âm tính, (-)…) → `chua_thay`, `loi: trich_dan_cat_phu_dinh`.
- Mã `loi`: `a1_tat`, `a1_tu_choi`, `a1_bi_cat_do_dai`, `a1_bi_chan_noi_dung`, `a1_json_loi`, `a1_loi_<Exception>`, `trich_dan_khong_khop`, `trich_dan_cat_phu_dinh`.
- Hiển thị: mở rộng đoạn trích ra trọn câu chứa nó, để bác sĩ thấy ngữ cảnh ("Mẹ đang viêm họng").

**Model:** `.env` (`OPENAI_API_KEY`, `OPENAI_MODEL`, `A1_TIMEOUT_S`). Chỉ dữ liệu giả hoặc đã ẩn danh. Kết quả chỉ cố định ở chế độ stub.

**Chế độ:** `A1_MODE=stub` (mặc định khi test) sinh kết quả A1 từ `ky_vong` của ca (vế AI + khối `a1_gia_lap.so_lieu` nếu ca cần trích số) → test engine chạy được từ tuần 3, không phụ thuộc LLM. `A1_MODE=live` chỉ dùng để đo chỉ số PRD mục 8.

## 8. Đầu ra một dòng

```json
{ "thu_tu": 2, "ma": "23.0228.1483", "ten": "Định lượng CRP",
  "trang_thai": "Đủ căn cứ · bác sĩ xác nhận", "o_bhyt_goi_y": "tich", "to_mau": true,
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
| `xac_minh` / `chua_tra` | "Có trong danh mục kỹ thuật nhưng chưa tìm thấy giá BHYT tương ứng, cần kiểm tra với bảng giá của viện" / "Ngoài danh sách đã tra" |
| `trung_dong` | "Trùng dịch vụ trong cùng lượt khám" |
| `tan_suat` | "Đã làm cách {gio} giờ; giới hạn {nen_gio} giờ" |
| `ve_khong_dat` | Mỗi nhánh trượt nêu vế trượt đầu tiên: "{mo_ta}: {bang_chung} chưa đạt", nối bằng "; ". Các nhánh ICD gộp thành "ICD {mã} không thuộc nhóm '{mo_ta}', …" |
| `ve_chua_thay` | "Điều kiện có vế '{mo_ta}'; phiếu khám chưa thấy nội dung tương ứng" |
| `ve_chua_du` | "Chưa đủ dữ liệu cho vế '{mo_ta}'" |
| `khong_nhanh` | "Không có nhánh điều kiện áp dụng cho tuổi này" |
| `loai_tru` | "Có thể thuộc điều khoản không thanh toán: {mo_ta}" |

Kết luận dựa trên giá trị `tu_dung` → thêm hậu tố cố định: "(cách hiểu tạm {M-xx}, chưa được bác sĩ duyệt)".

`phien_ban_rule` = hash của cả thư mục `data/rules/`.

## 9. Log (F-12, F-13)

Một dòng JSONL mỗi lần xác nhận một dòng chỉ định, chỉ ghi thêm (`logs/xac-nhan.jsonl`). Khóa: `luot_kham + kiem_tra_id + thu_tu` (`kiem_tra_id` do `/check` cấp, 12 ký tự hex).

```json
{ "thoi_gian": "...", "luot_kham": "...", "kiem_tra_id": "...", "thu_tu": 2, "ma": "...", "ten": "...",
  "trang_thai": "...", "o_bhyt_goi_y": "tich | trong | null", "bac_si_chon": "tich | khong_tich",
  "ly_do_bac_si": { "loai": "nguoi_nha_yeu_cau | loai_tru_theo_doi | khong_dong_y | khac | null", "ghi_chu": "..." },
  "checklist": [...], "can_cu": [...], "phien_ban_rule": "...",
  "dau_vao": { "tuoi": ..., "the": {...}, "icd": [...], "sinh_hieu": {...}, "lich_su_da_dung": [...] } }
```

`ly_do_bac_si` luôn được ghi (không bắt buộc nhập, `loai` = null nếu bác sĩ để trống) khi: bỏ tích dòng gợi ý `tich`, hoặc tích dòng Không được chi trả. Dòng khác: chỉ ghi khi bác sĩ tự thêm lý do/ghi chú; `ghi_chu` dùng được với mọi `loai`, kể cả null.

## 10. Màn hình mô phỏng (F-14)

HTML/JS thuần (`web/`) gọi FastAPI (`src/app.py`); bố cục chốt sau khi duyệt mẫu ở `prototypes/`. Một trang: chọn ca → thẻ, sinh hiệu, ICD, phiếu khám bên trái (nút "Chỉnh sửa" → "Xác nhận sửa"/"Hủy"; xác nhận sửa thì rule chạy lại, AI đọc lại khi bấm "Kiểm tra BHYT"; đang sửa thì khóa nút Kiểm tra và Xác nhận); bảng chỉ định với ô "Tính BHYT" tích sẵn và trạng thái bên phải, thêm/xóa chỉ định và ICD tại chỗ (rule tự chạy lại, AI chỉ đọc khi bấm "Kiểm tra BHYT"); bấm dòng → checklist, trích dẫn tô màu trong phiếu khám, nhãn "cách hiểu tạm" nếu có; nút Xác nhận ghi log. Engine nhận/trả JSON, nên khi gắn Eform/VIS chỉ thay lớp này.

## 11. Test

- Chạy mọi `data/test-cases/*.yaml` ở `A1_MODE=stub`: so `trang_thai` từng dòng (khóa `thu_tu`), và `ket_qua` của vế có `id`.
- Unit test bắt buộc: bảng gộp mục 6 (mọi tổ hợp nhánh, gồm không có nhánh áp dụng); số A1 `khong_dat` bị hạ; `ai_doc` với `toi_da`; trích dẫn sửa một chữ → `chua_thay` (AC-11); 58 không khớp "158"; số ngoài khoảng hợp lệ bị bỏ; R4 với hai dòng `ma: null` khác tên.
- `he_chi_rule` sinh bằng máy theo mục 6 rồi so với giá trị trong ca.

## 11b. Hợp đồng giữa các module (bản 3, để làm song song)

```python
# src/rules.py   (engine-owner viết)
load_rules(dir="data/rules") -> Rules          # đọc 3 YAML, giải "@tham_so", tính phien_ban_rule = sha1 cả thư mục

# src/engine.py
check(luot: dict, rules: Rules, a1: A1Fn | None, mode="full" | "chi_rule") -> dict
#   trả { "phien_ban_rule": str, "a1": {"goi": bool, "loi": str|None, "ms": int}, "dong": [<đầu ra mục 8>, ...] }
#   a1=None ở mode="full" → coi như A1 lỗi (mọi vế AI chua_thay, loi="a1_tat")

A1Fn = Callable[[A1Request], A1Result]
A1Request = { "phieu_kham": str,
              "cau_hoi": [ {"khoa": "2:V3", "mo_ta": str, "cau_hoi": str} ],
              "so_lieu":  [ {"truong": "nhip_tho", "don_vi": "l/p"} ] }
A1Result  = { "ve": [ {"khoa": "2:V3", "ket_qua": "dat"|"chua_thay", "trich_dan": str|None, "trich_lien_quan": [str]} ],
              "so_lieu": [ {"truong": str, "gia_tri": float, "trich_dan": str} ],
              "loi": str|None }              # ĐÃ qua kiểm tra trích dẫn mục 7; engine tin kết quả này

# src/a1.py
make_live(model, timeout_s) -> A1Fn            # OpenAI; luôn trả A1Result, không raise
verify(phieu_kham, raw, khoang_hop_le) -> A1Result   # hàm thuần, kiểm tra mục 7
# tests/stub_a1.py (engine-owner): make_stub(ca_test) -> A1Fn, sinh từ ky_vong + a1_gia_lap

# src/log.py
append(rows: list[dict], path="logs/xac-nhan.jsonl") -> None

# src/app.py (FastAPI)
POST /check   body = lượt khám (mục 4) + doc_ai (mặc định true) → kết quả check() + kiem_tra_id
#   doc_ai=false: chỉ chạy rule, dùng câu trả lời A1 đã nhớ (khóa = phiếu khám chuẩn hóa khoảng trắng + nội dung câu hỏi);
#   câu chưa nhớ → vế đó chua_thay, a1.loi="chua_doc". Lỗi a1_* không được nhớ. Bộ nhớ nằm trong tiến trình, mất khi khởi động lại.
POST /confirm body = {luot_kham, kiem_tra_id, dau_vao, dong: [ {..đầu ra mục 8.., bac_si_chon, ly_do_bac_si} ]} → ghi log, trả {"ghi": n}
GET  /cases   → danh sách ca demo (data/test-cases/demo.yaml, bỏ ky_vong)
GET  /health  → {phien_ban_rule, a1_mode, model}
GET  /        → web/index.html
```

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
