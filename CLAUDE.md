# CLAUDE.md — BHYT Order Assistant

Trợ lý cho bác sĩ Nhi (Vinmec, TC-03): lúc chỉ định xét nghiệm/CĐHA, báo dòng nào phù hợp quy tắc BHYT, dòng nào cần xem lại, kèm lý do và căn cứ. Bác sĩ là người quyết định. Tổng quan dự án và cách chạy: [README.md](README.md).

> Nội dung dưới đây chép từ mục "Lưu ý cho người làm tiếp" của README (16/11/2026). **Sửa một bên thì sửa cả bên kia.**

**Khi làm việc trong repo này:**
- Không commit, không push nếu người dùng chưa yêu cầu.
- Eval live gọi OpenAI thật và tốn tiền: báo trước số lượt gọi trước khi chạy.
- Thay đổi quy tắc còn tranh cãi (cách hiểu văn bản, nhãn ca thử) thì hỏi người dùng chọn, không tự quyết. Không bắt người dùng tự trả lời từng câu hỏi lâm sàng.
- Viết tài liệu và giao diện bằng tiếng Việt.

## Lưu ý cho người làm tiếp (và trợ lý AI của bạn)

*Cập nhật 16/11/2026.* Đưa mục này cho AI code cùng bạn (Claude, Copilot, Cursor…) đọc trước khi sửa.

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

