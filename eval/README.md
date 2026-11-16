# Eval hệ thống

Đo độ đúng của engine + A1 so với **nhãn nhóm tự viết** (`data/test-cases/*.yaml`, `data/eval/a1-kho.yaml`). Bác sĩ chưa duyệt nhãn, nên đây chưa phải độ đồng thuận với bác sĩ.

## Chạy

```
python eval/run_eval.py                                  # stub, data/test-cases/*.yaml
python eval/run_eval.py --lan 2 --cases "data/test-cases/*.yaml" "data/eval/*.yaml"
python eval/run_eval.py --rules tests/fixtures/rules     # khi data/rules chưa có
python eval/run_eval.py --a1 live --lan 3                # chỉ in ước tính số lần gọi, rồi dừng
python eval/run_eval.py --a1 live --lan 3 --yes          # gọi OpenAI thật, TỐN TIỀN
pytest eval/test_report.py                               # unit test các hàm chỉ số
```

| Tham số | Ý nghĩa |
|---|---|
| `--a1 stub\|live` | `stub` (mặc định): A1 giả sinh từ chính nhãn → đo engine, không đo LLM. `live`: gọi OpenAI. |
| `--lan N` | Lặp mỗi ca N lần; ≥ 2 mới đo được độ ổn định. |
| `--cases` | Một hoặc nhiều glob, tương đối so với gốc repo. |
| `--rules` | Thư mục rule (mặc định `data/rules`). Thiếu file → dừng với thông báo, mã thoát 1. |
| `--out` | Đường dẫn `.md`; `.json` cùng tên chứa chỉ số + toàn bộ bản ghi. Mặc định `eval/reports/<thời gian>.md`. |
| `--yes` | Bắt buộc ở chế độ live. |

Chế độ live đọc từ biến môi trường hoặc `.env`: `OPENAI_API_KEY`, `OPENAI_MODEL` (bắt buộc), `A1_TIMEOUT_S` (mặc định 8), `A1_REASONING_EFFORT`. Muốn có chi phí ước tính thì đặt thêm `EVAL_PRICE_IN_PER_1M`, `EVAL_PRICE_OUT_PER_1M` (USD / 1 triệu token).

## Chỉ số và mục tiêu

| Chỉ số | Mục tiêu |
|---|---|
| Dòng quá thuận lợi | **0** |
| Vế AI đạt sai | **0** |
| `engine.check` p95 | **< 10 s** |

1. **Trạng thái dòng.** Ma trận 4×4 nhãn × hệ thống, thứ tự thuận lợi giảm dần: Phù hợp quy tắc BHYT > Cần xem lại · đủ căn cứ > Cần xem lại > Không được chi trả. **Quá thuận lợi** = hệ thống trả trạng thái thuận lợi hơn nhãn (rủi ro xuất toán), liệt kê từng dòng. Kém thuận lợi = ngược lại (chỉ gây phiền). Dòng không có nhãn `trang_thai` (bộ a1-kho) bị bỏ qua và được đếm riêng.
2. **Vế điều kiện.** So `ket_qua` theo `id` vế, tách vế rule / vế AI (`kiem_bang: ai`). **Đạt sai** = hệ thống `dat`, nhãn khác `dat` (liệt kê). Bỏ sót đạt = nhãn `dat`, hệ thống không. Chia theo thẻ `bay` của vế, không có thì lấy `bay` của ca. **Đạt sai chỗ** = nhãn `dat`, hệ thống `dat`, nhưng trích dẫn không giao (chuỗi con chung ≥ 5 ký tự) với `trich_dan` hay mục nào trong `trich_dan_khac`; không tính là khớp, liệt kê riêng. Với ca không có `trang_thai` (a1-kho), vế AI được chấm theo câu trả lời của A1 sau `verify()` chứ không theo checklist engine (engine có thể hạ, vd N2).
3. **Trích số.** So với `a1_ky_vong_so_lieu`, không có thì `a1_gia_lap.so_lieu`. Loại: đúng (gồm cả đúng là không trích), sai giá trị, bỏ sót, trích thừa. Trường engine không hỏi A1 thì không tính. `chap_nhan_trong: true` → bỏ trống cũng đúng. `a1_ky_vong_so_lieu: []` → trả số nào cũng là trích thừa.
4. **Trích dẫn bị loại.** Số trích dẫn trong đầu ra thô của A1 (vế `dat`, `trich_lien_quan`, số liệu) bị `src.a1.verify` loại: không phải chuỗi con của phiếu khám, cắt mất phủ định, số ngoài khoảng hoặc mâu thuẫn. Tính bằng hiệu giữa đầu ra thô và đầu ra sau verify; chỉ có nghĩa ở chế độ live.
5. **Độ ổn định.** Tỷ lệ dòng / vế đổi kết quả giữa các lần lặp của cùng ca.
6. **Vận hành.** Tỷ lệ lỗi A1 và hết giờ (ghi chú `trich_dan_*` của verify không tính là lỗi gọi), độ trễ `engine.check` và riêng A1 (p50 / p95, nearest-rank), token và chi phí (chỉ live).
7. **Hệ chỉ-rule và giá trị của A1.** Chạy lại mỗi ca với `mode="chi_rule"`. Giá trị của A1 = số dòng hệ chỉ-rule báo "Phù hợp" trong khi nhãn kém thuận lợi hơn, mà hệ đầy đủ không còn quá thuận lợi. Đồng thời đối chiếu nhãn `he_chi_rule` của ca với kết quả máy sinh (dòng đầu của ca).

## Lưu ý

- Bộ a1-kho chạy qua engine: A1 chỉ được hỏi những vế / trường số mà engine cần với rules hiện tại. Vế có nhãn mà engine không hỏi thì lấy kết quả checklist; trường số không hỏi thì không tính.
- Stub trên `a1-kho.yaml` chỉ kiểm tra đường ống: vế AI và số liệu lấy từ chính nhãn. Bộ này chỉ có nghĩa ở chế độ live.
- Phần chỉ số là hàm thuần, không import engine; `test_report.py` chạy được khi chưa có rules.
- Token lấy bằng cách bọc `OpenAI` trong `src.a1` lúc chạy, không sửa `src/`.
