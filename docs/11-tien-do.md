# 11 — Tiến độ dự án

**Cập nhật:** 14/11/2026 · **Kế hoạch gốc:** [05-ke-hoach.md](05-ke-hoach.md) · **Giả định đang dùng:** [10-gia-dinh.md](10-gia-dinh.md)

## 1. Tóm tắt

MVP đã chạy được từ đầu đến cuối trên laptop: phần kiểm tra bằng rule, phần A1 (OpenAI) chạy ở chế độ stub, màn hình demo, log và eval. Dữ liệu rule đã qua một vòng audit độc lập. **218/218 test qua**. Eval stub khớp 93/93 dòng và không có dòng nào báo thuận lợi hơn kỳ vọng.

Việc còn lại chính: lấy ý kiến bác sĩ để gỡ dần các giả định, chạy eval với OpenAI thật, chuẩn bị demo.

## 2. Đã làm

### Tài liệu

| Việc | File |
|---|---|
| Bài toán, giải pháp, khả thi, rủi ro, kế hoạch | [01](01-bai-toan.md)–[05](05-ke-hoach.md) |
| Điểm mơ hồ cần bác sĩ duyệt (M-01…M-20) | [06](06-diem-mo-ho-bac-si-duyet.md) |
| PRD | [07](07-prd.md) |
| Phiếu hỏi bác sĩ: 19 câu (15 câu chung + 4 tình huống từ ca khó), chỉ hỏi chuyên môn, mỗi câu có ví dụ ca bệnh | [08](08-phieu-hoi-bac-si.md), [bản gửi](gui-bac-si/phieu-hoi-chuyen-mon.html) + PDF |
| Spec kỹ thuật bản 3 (OpenAI, chạy trên laptop, 1 lần /check < 10 giây, log JSONL, hợp đồng giữa các module) | [09](09-spec.md) |
| Sổ giả định (GD-01…GD-18) | [10](10-gia-dinh.md) |
| Đổi giao diện prototype sang kiểu eForm | `prototypes/d-ket-hop.html` |
| Slide ví dụ và kịch bản thuyết trình theo ca a1-seed | `slides/` |

### Dữ liệu rule (`data/rules/`)

- **Danh mục 55 dòng** (50 dịch vụ), đối chiếu PL01 TT 23/2024 và QĐ 3500.
- **Điều kiện riêng:** CRP, Procalcitonin, Doppler tim, Điện tim. Dùng nguyên văn TT 39/2024, cấu trúc nhánh → vế → loại trừ.
- **Mọi giá trị tự dựng** đều gắn nhãn `tu_dung` + M-xx, nên câu lý do có hậu tố "cách hiểu tạm".
- **Nguồn của từng giá trị:** [NGUON.md](../data/rules/NGUON.md).
- **Audit độc lập ngày 14/11:** [AUDIT.md](../data/rules/AUDIT.md). Câu trích, số trang và mã đều đúng. Đã xử lý M-1, M-2, M-4, M-5 và m-1…m-7; B-2, M-3 tạm giữ (xem mục 4 của AUDIT).
- **Quyết định ngày 14/11:**
  - Test nhanh RSV, Adenovirus, liên cầu A: coi như thu theo mã chung, ra Phù hợp (GD-01).
  - CRP nhánh d: danh sách ICD mở rộng còn 25 mã. Câu lý do nêu đủ cả phần nhiệt độ và phần ICD (GD-02).
  - "Trẻ em" là dưới 16 tuổi: bác sĩ đã chốt.
  - Nhịp tim theo thang Úc: tạm dùng bảng RACGP, chỉ có đến 6 tuổi (GD-08).

### Phần mềm

| Thành phần | File | Test |
|---|---|---|
| Đọc rule, engine R1–R4 + điều kiện, gộp trạng thái, câu lý do | `src/rules.py`, `src/engine.py` | 83 unit test, 2.000 lượt khám ngẫu nhiên kiểm bất biến |
| A1: OpenAI Structured Outputs, kiểm câu trích khớp nguyên văn, chặn trích cắt mất phủ định, có hạn giờ tổng | `src/a1.py` | 24 |
| API (FastAPI, chỉ chạy trên localhost) + màn hình demo + log JSONL | `src/app.py`, `src/log.py`, `web/index.html` | 37 |
| Bộ ca thử: 55 ca theo nhóm + 45 ca khó cho A1 | `data/test-cases/`, `data/eval/a1-kho.yaml` | chạy tự động |
| Eval chỉ số "hệ chạy đúng" (ma trận 4×4, dòng báo thuận lợi hơn kỳ vọng = 0, độ ổn định, p95, chi phí) | `eval/run_eval.py` | 17 |

## 3. Cần làm tiếp

### Ưu tiên cao

1. **Gửi phiếu hỏi cho bác sĩ và nhận câu trả lời.** Với mỗi câu đã có trả lời, sửa dữ liệu theo cột "Gỡ giả định" trong [10](10-gia-dinh.md), đổi nhãn sang `bac_si_duyet`, rồi chạy lại test. Bảng tra câu hỏi ↔ M-xx ↔ GD-xx nằm cuối [08](08-phieu-hoi-bac-si.md).
2. **Chạy eval với OpenAI thật (mục 10).**
   - Cần điền `.env`: `OPENAI_API_KEY`, `OPENAI_MODEL` (luna 6.1), `A1_REASONING_EFFORT=low`.
   - Trước khi chạy: sửa lỗi trong `eval/run_eval.py`. Một phản hồi đến sau hạn giờ có thể bị tính nhầm cho lượt khám kế tiếp.
   - Lệnh chạy: `python eval/run_eval.py --a1 live --lan 3 --yes`.
3. **Tích hợp và chạy thử demo:** chạy uvicorn ở chế độ stub và ở chế độ live, đi hết các ca demo trên màn hình, đo thời gian.

### Chờ duyệt (đang chạy theo giả định, xem [10 mục 4](10-gia-dinh.md))

- **PCT làm lại dưới 24 giờ:** hiện ra Không được chi trả. Audit B-2 đề nghị hạ xuống Cần xem lại.
- **Doppler tim / Điện tim cùng phiếu:** hiện ra Không được chi trả. Audit M-3 đề nghị cân nhắc.
- **Danh sách ICD cho nhánh c, d của CRP:** chờ bác sĩ gạch bỏ hoặc bổ sung (câu 7).
- **Ngưỡng nhịp tim cho trẻ 6–15 tuổi:** cần bảng RCH Melbourne hoặc ngưỡng do bác sĩ đưa.
- **Thẻ hết hạn (R2):** chưa có câu văn bản làm căn cứ. Cần bổ sung Luật BHYT và NĐ 188/2025.

### Ưu tiên thấp / dọn dẹp

- Kiểm tra slide hiển thị vừa khung 1080 px.
- Hỏi riêng (ngoài phiếu): cách điền sẵn ô BHYT, ca xuất toán thực tế, file Excel BHYT của viện.
- Trước khi dùng dữ liệu bệnh viện (kể cả đã ẩn danh) với OpenAI: hỏi IT và pháp chế.

### Theo kế hoạch tuần 4–5 ([05](05-ke-hoach.md))

- Bác sĩ gán nhãn khoảng 30 ca để đo mức đồng thuận.
- Khảo sát 7 câu + bấm giờ 5–10 lượt tích BHYT tại khoa.
- Báo cáo chỉ số PRD mục 8, chốt slide, tập demo.
