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
│   ├── 09-spec.md            spec kỹ thuật: schema rule, gộp trạng thái, A1, log
│   ├── 10-gia-dinh.md        giả định đã chốt / tạm giữ (GD-xx)
│   ├── 11-tien-do.md         tiến độ
│   ├── 12-luong-xu-ly.md     bản đồ luồng: văn bản → YAML → rule + AI → đầu ra → eval (ĐỌC TRƯỚC)
│   └── gui-bac-si/           bản HTML/PDF đã gửi bác sĩ (đề xuất, kế hoạch, phiếu hỏi)
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
│   ├── danh-muc/             danh sách 50 dịch vụ MVP; icd10.tsv (ICD-10 TT 06/2026) cho ô tìm chẩn đoán
│   ├── rules/                quy tắc YAML: danh-muc, dieu-kien, tham-so + NGUON.md, AUDIT.md, check_rules.py
│   ├── test-cases/           ca thử có nhãn theo dịch vụ (crp, pct, demo, a1-seed…)
│   ├── eval/                 ca khó cho AI (a1-kho.yaml: phủ định, người nhà, prompt injection…)
│   └── van-ban/              văn bản pháp lý gốc + INDEX
├── src/
│   ├── engine.py             rule R1–R4, gộp trạng thái, hai pha gọi A1
│   ├── a1.py                 A1: prompt, JSON schema, verify() kiểm trích dẫn
│   ├── rules.py, log.py      nạp YAML; ghi log xác nhận
│   └── app.py                FastAPI: /check, /confirm, /cases, /danh-muc, /icd, /gia-dinh
├── web/index.html            màn hình mô phỏng (một file, JS thuần)
├── eval/                     run_eval.py + README (đo engine + AI trên ca có nhãn)
├── tests/                    pytest (A1 giả lập, không gọi OpenAI)
└── prototypes/               bản phác giao diện cũ, không dùng
```

## Lưu ý cho người làm tiếp (và trợ lý AI của bạn)

*Cập nhật 16/11/2026.* Đưa mục này cho AI code cùng bạn (Claude, Copilot, Cursor…) đọc trước khi sửa. Mục này được chép sang [CLAUDE.md](CLAUDE.md) để Claude Code tự đọc. **Sửa một bên thì sửa cả bên kia.**

**Đọc trước:** [docs/12-luong-xu-ly.md](docs/12-luong-xu-ly.md) (bản đồ cả luồng, có link tới từng tài liệu chi tiết). Chi tiết kỹ thuật: [docs/09-spec.md](docs/09-spec.md). Khi tài liệu và code lệch nhau: tin **code + YAML** trước, rồi 09-spec.

**Nguyên tắc không được phá:**
- Rule **không đọc phiếu khám**; chỉ A1 đọc. AI chỉ được nói "có ghi" (`dat`) kèm trích dẫn nguyên văn, code (`a1.verify`) kiểm lại. AI trả "không" → *chưa đủ dữ liệu*, không bao giờ thành "Không được chi trả".
- **App không trả lời câu hỏi lâm sàng.** Câu hỏi cho AI hỏi điều bác sĩ *đã ghi*, không hỏi "triệu chứng này có phải bệnh X không". Đừng thêm luật kiểu "ho + sốt = nghi viêm phổi".
- Giá trị nhóm tự dựng (không có nguyên chữ trong văn bản) phải gắn `nguon: tu_dung` + mã `M-xx`, và **không được tự sinh "Không được chi trả"**.
- Chỉ dữ liệu giả hoặc đã ẩn danh. Không gửi dữ liệu bệnh viện thật lên OpenAI khi chưa hỏi IT/pháp chế. Không commit `.env`, không in API key ra log.

**File quan trọng và chỗ dễ sai:**

| File | Lưu ý |
|---|---|
| `data/rules/dieu-kien.yaml` | Nguồn duy nhất của điều kiện thanh toán. `cau_hoi` của vế `ai_doc` chỉ viết gần nguyên văn văn bản + phần riêng của vế đó; cách đọc dùng chung (mức chắc chắn, thời điểm, mức cụ thể) nằm trong prompt. Sửa xong chạy `python data/rules/check_rules.py`. Mọi thay đổi trong `data/rules/` đổi `phien_ban_rule` (hash cả thư mục) |
| `src/a1.py` | `SYSTEM_PROMPT` có 15 quy tắc; 13–15 là cách đọc chung. Sửa prompt hay câu hỏi → **phải chạy eval live** để so (xem dưới). File dùng xuống dòng CRLF: script sửa tự động phải giữ CRLF |
| `src/an_danh.py` | Ẩn tên, SĐT, số thẻ, mã BN, email, ngày sinh, địa chỉ có nhãn trong phiếu khám **trước khi gửi OpenAI** (A1 và A3, kèm `store=False`). Lọc theo mẫu, không bắt được mọi cách viết. Sửa xong chạy `tests/test_an_danh.py`: số lâm sàng và 102 phiếu mẫu phải giữ nguyên |
| `src/engine.py` | Bảng gộp trạng thái ở 09-spec mục 6. Câu lý do sinh từ mẫu, không dùng LLM; hậu tố "(cách hiểu tạm M-xx, chưa được bác sĩ duyệt)" do engine nối và được lưu nguyên trong log |
| `src/app.py` | Nhớ câu trả lời AI theo phiếu khám + nội dung câu hỏi, lưu qua `src/luu_tru.py` (có `DATABASE_URL` thì ở Neon, không có thì trong bộ nhớ và mất khi khởi động lại). `doc_ai=false` = chỉ chạy lại rule. `A1_MODE` = `live` / `stub` / `off`; `LQ_MODE` (A3) tắt mặc định, không bật cho người dùng |
| `docs/06-diem-mo-ho-bac-si-duyet.md` | Endpoint `/gia-dinh` đọc thẳng các dòng bảng bắt đầu bằng `\| M-` (cột: mã, câu hỏi, vì sao, cách hiểu tạm, bác sĩ trả lời). **Giữ đúng định dạng bảng** khi sửa |
| `web/index.html` | Lý do trên màn hình bỏ hậu tố M-xx, thay bằng dấu `*` + nút "Giả định". Sửa xong kiểm cú pháp JS (lệnh dưới) |
| `data/test-cases/*.yaml`, `data/eval/*.yaml` | Nhãn do nhóm viết, bác sĩ chưa duyệt. **Không sửa nhãn cho khớp hệ thống**; nhãn chỉ đổi khi có quyết định cách hiểu, ghi vào docs/10 |
| `docs/08`, `docs/gui-bac-si/` | Đã gửi bác sĩ 14/11, không sửa nội dung đã gửi |

**Lệnh kiểm tra trước khi giao:**
```bash
python -m pytest -q                                   # A1 giả lập, không tốn tiền
python data/rules/check_rules.py                      # cấu trúc 3 file rule
pytest eval/test_report.py                            # hàm chỉ số eval
python eval/run_eval.py --cases "data/test-cases/*.yaml" "data/eval/*.yaml"   # eval stub
# JS của màn hình:
sed -n '/<script>/,/<\/script>/p' web/index.html | sed '1d;$d' > /tmp/chk.js && node --check /tmp/chk.js
```

**Eval live (gọi OpenAI thật, tốn tiền, ~219 lượt gọi, ~15–20 phút):** chạy mỗi khi đổi prompt hoặc `cau_hoi`.
```bash
python eval/run_eval.py --a1 live --lan 3 --yes --cases "data/test-cases/*.yaml" "data/eval/*.yaml" --out eval/reports/<ten>.md
```
Hai chỉ số phải bằng 0: **dòng quá thuận lợi** và **vế AI đạt sai**. Kết quả các lần trước: bảng ở docs/12 mục 5 (bản 16/11: quá thuận lợi 0, đạt sai 3, khớp trạng thái dòng 99,6%). `eval/reports/` chưa nằm trong `.gitignore`.

**Trên Windows (Git Bash):** đặt `PYTHONIOENCODING=utf-8` để in tiếng Việt; dùng `--basetemp` cho pytest nếu thư mục tạm bị chặn.

## Link

- Báo cáo (Claude Docs): https://claude.ai/artifact/781aX2PhdrnVNHhkrniBpQ
- Slides (artifact): https://claude.ai/artifact/FNTCmpjUMic9oLmP3zqEJx
- Khảo sát gốc: [../vinmec-khao-sat](../vinmec-khao-sat)

## Tái sử dụng slides

`slides/deck/` là bản sao file của artifact Slides (bản 10/11/2026). Mỗi slide là một `<section>` 1920×1080, style inline, ghi chú người nói nằm trong `<aside>`; thứ tự slide nằm ở `deck.json → order`. Để sửa và đăng lại: nhờ Claude publish thư mục này lên cùng URL artifact (root = `slides/deck/..`, đường dẫn phục vụ `project/deck.json`, `project/slides/*.html`), hoặc copy từng `<section>` sang deck khác.

Bảng màu: nền tối `#16324F`, nền sáng `#F7F8F5` / `#EEF3F1`, nhấn `#0F7B6C`, thẻ `#FDFDFB`, chữ `#3E5468`. Font Be Vietnam Pro. Cỡ chữ: eyebrow 34, h2 68, số lớn 80, h3 40, body 34, chú thích 24.

## Chạy demo

### Lần đầu: cài đặt môi trường (Python 3.13)
```powershell
# Windows
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
copy .env.example .env
# Sửa .env: điền OPENAI_API_KEY, OPENAI_MODEL. Không có khóa thì để A1_MODE=off
```

```bash
# Linux/macOS
python -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
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

Mở http://127.0.0.1:8000. Chọn ca mẫu (hoặc tự nhập), thêm/xóa chỉ định và ICD (rule tự chạy lại), bấm "Kiểm tra BHYT" để AI đọc phiếu khám, rồi "Xác nhận" để ghi `logs/xac-nhan.jsonl`. Chỉ dùng dữ liệu giả hoặc đã ẩn danh. Test: `python -m pytest -q` (xem mục "Lưu ý cho người làm tiếp").

Buổi đo Before/After: ca đo và đáp án nằm ở `data/do-luong/bo-ca.yaml`, phân công theo tài khoản ở `src/do_luong.py`. Sau mỗi buổi đo chạy `python -m src.xuat_ket_qua` để xuất kết quả ra file CSV trong `logs/`.
