# BHYT Order Assistant — TC-03 Trung tâm Nhi, Vinmec Times City

Trợ lý báo cho bác sĩ, ngay lúc tích BHYT, dòng xét nghiệm/CĐHA/dịch vụ nào phù hợp quy tắc BHYT, dòng nào cần xem lại, kèm lý do và căn cứ. Bác sĩ vẫn là người xác nhận.

- **Người dùng:** bác sĩ khám ngoại trú Trung tâm Nhi (gồm phòng khám Ngoại Nhi — chỉ ngoại trú, không PT/TT).
- **Phạm vi MVP:** xét nghiệm, CĐHA, dịch vụ. Không thuốc, không PT/TT, không nội trú. Demo trên màn hình mô phỏng, không tích hợp thật.
- **Mục tiêu 5 tuần:** chứng minh tính khả thi (số liệu khảo sát, bảng phủ rule, demo trên bộ test đủ thật). Chưa cần hiệu năng cao.
- **Làm độc lập**, không phối hợp nhóm khác.

## Cấu trúc thư mục

```
bhyt-order-assistant/
├── README.md                 ← file này
├── docs/                     ← thiết kế ý tưởng (bản md của báo cáo)
│   ├── 01-bai-toan.md        bối cảnh, nỗi đau, bằng chứng, ý tưởng đã đổi thế nào
│   ├── 02-giai-phap.md       giải pháp, phạm vi, ranh giới cứng, rule vs AI, lợi ích
│   ├── 03-kha-thi.md         phiếu khảo sát, bảng phủ rule, bộ test
│   ├── 04-rui-ro.md          rủi ro và câu hỏi mở
│   ├── 05-ke-hoach.md        việc cần làm tuần 1–5
│   ├── 06-diem-mo-ho-bac-si-duyet.md  điểm mơ hồ cần bác sĩ duyệt trước khi xây rule
│   ├── 07-prd.md             PRD MVP: yêu cầu, tiêu chí nghiệm thu, chỉ số
│   ├── 08-phieu-hoi-bac-si.md  phiếu hỏi bác sĩ buổi 1 (~25 phút)
│   └── 09-spec.md            spec kỹ thuật: schema rule, gộp trạng thái, A1, log
├── research/                 ← dữ liệu khảo sát, insight
│   ├── y-tuong-ban-dau.md    đề xuất "BHYT Evidence & Audit Copilot" (đã bỏ)
│   ├── insight-cac-nhom.md   insight BHYT từ 17 nhóm khác
│   ├── khao-sat-nhi.md       số liệu, quan sát BHYT trích từ ../vinmec-khao-sat
│   ├── doi-thu.md            research đối thủ VN + tham chiếu quốc tế
│   ├── diem-nghen-his.md     vì sao VNPT/Viettel/FPT chưa làm cảnh báo chi trả BHYT lúc chỉ định
│   ├── phan-tich-diem-nghen.md  phân tích sâu 3 điểm nghẽn khó nhất + ví dụ + hướng scale
│   └── research_notes/       ghi chú gốc (có nguồn) của research đối thủ
├── slides/
│   ├── kich-ban-thuyet-trinh.md   script ~3 phút
│   └── deck/                 bản sao artifact Slides (deck.json + slides/*.html)
├── data/
│   ├── danh-muc/             danh sách 50 dịch vụ MVP (mã chuẩn, giá tham khảo, BHYT sơ bộ)
│   ├── rules/                quy tắc YAML theo 3 lớp (quốc gia / bệnh viện / ghi đè)
│   ├── test-cases/           bộ test 50–100 ca mô phỏng (bắt đầu: a1-seed.yaml)
│   └── van-ban/              văn bản pháp lý gốc + INDEX
└── src/                      code rule engine + AI (bắt đầu từ tuần 3)
```

## Link

- Báo cáo (Claude Docs): https://claude.ai/artifact/781aX2PhdrnVNHhkrniBpQ
- Slides (artifact): https://claude.ai/artifact/FNTCmpjUMic9oLmP3zqEJx
- Khảo sát gốc: [../vinmec-khao-sat](../vinmec-khao-sat)

## Tái sử dụng slides

`slides/deck/` là bản sao file của artifact Slides (bản 10/11/2026). Mỗi slide là một `<section>` 1920×1080, style inline, ghi chú người nói nằm trong `<aside>`; thứ tự slide nằm ở `deck.json → order`. Để sửa và đăng lại: nhờ Claude publish thư mục này lên cùng URL artifact (root = `slides/deck/..`, đường dẫn phục vụ `project/deck.json`, `project/slides/*.html`), hoặc copy từng `<section>` sang deck khác.

Bảng màu: nền tối `#16324F`, nền sáng `#F7F8F5` / `#EEF3F1`, nhấn `#0F7B6C`, thẻ `#FDFDFB`, chữ `#3E5468`. Font Be Vietnam Pro. Cỡ chữ: eyebrow 34, h2 68, số lớn 80, h3 40, body 34, chú thích 24.

## Chạy demo

### Lần đầu: cài đặt môi trường
```powershell
# Windows
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
# Sửa .env: điền OPENAI_API_KEY, OPENAI_MODEL. Không có khóa thì để A1_MODE=off
```

```bash
# Linux/macOS
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Sửa .env: điền OPENAI_API_KEY, OPENAI_MODEL
```

### Lần sau: kích hoạt môi trường rồi chạy
```powershell
# Windows
.\venv\Scripts\Activate.ps1
python -m uvicorn src.app:app --host 127.0.0.1 --port 8000
```

```bash
# Linux/macOS
source venv/bin/activate
uvicorn src.app:app --host 127.0.0.1 --port 8000
```

Mở http://127.0.0.1:8000. Chọn ca và lần tích, tích các chỉ định, bấm "Kiểm tra BHYT" (một lần gọi `/check`), rồi "Xác nhận" để ghi `logs/xac-nhan.jsonl`. Chỉ dùng dữ liệu giả hoặc đã ẩn danh. Test: `pytest tests/test_app.py`.
