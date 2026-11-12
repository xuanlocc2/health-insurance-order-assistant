# 05 — Việc cần làm

Tuần 1 ưu tiên thu thập bằng chứng và trả lời câu hỏi ICD; chỉ bắt đầu code từ tuần 3 khi đã có bảng phủ rule.

## Tuần 1 — Thu thập tại khoa
- [ ] Quan sát thứ tự thao tác: ICD nhập trước hay sau khi tích BHYT
- [ ] Bấm giờ tích BHYT ở 5–10 lượt khám
- [ ] Phát phiếu khảo sát 7 câu ([03-kha-thi.md](03-kha-thi.md)) cho bác sĩ Trung tâm Nhi
- [ ] Xin 1–3 ca xuất toán qua lời kể (dịch vụ gì, lý do gì)
- [x] Danh sách 50 dịch vụ Nhi ngoại trú: chốt dùng [nhi-ngoai-tru-de-xuat.md](../data/danh-muc/nhi-ngoai-tru-de-xuat.md) cho MVP (11/11/2026); bác sĩ góp ý thì bổ sung sau
- [ ] Hỏi ai giữ danh mục dịch vụ BHYT và ai báo xuất toán

## Tuần 2 — Bảng phủ rule
- [ ] Xác nhận văn bản BHYT đang hiệu lực cho danh mục dịch vụ kỹ thuật
- [ ] Điền bảng phủ rule cho 50 dịch vụ
- [x] ~~Mapping mã nội bộ ↔ mã BHYT~~: MVP dùng thẳng mã/tên chuẩn (quyết định 11/11/2026)
- [ ] Dựng bảng dịch vụ ↔ nhóm ICD, chỉ từ căn cứ thành văn, nhờ bác sĩ duyệt
- [ ] **R2 (thẻ, mức hưởng):** thu thập quy tắc từ Luật BHYT sửa đổi 51/2024, NĐ 188/2025, TT 01/2025 — hạn thẻ (trẻ < 6 tuổi), mã mức hưởng, giấy chuyển — rồi viết rule
- [ ] **Điều kiện chi trả riêng của viện:** xin file Excel BHYT bác sĩ đang tra, xác định nó là bảng mapping hay bảng điều kiện; đưa vào lớp `overrides/` ([data/rules/README.md](../data/rules/README.md))
- [ ] **Mock data ca bệnh:** bắt đầu dựng sớm (song song tuần 2), theo yêu cầu ở [03-kha-thi.md](03-kha-thi.md) mục 3; lưu `../data/test-cases/`
- [ ] Tổng hợp số liệu khảo sát và bấm giờ
- [x] ~~Chốt giữ A1 hay không~~: A1 là lõi AI của MVP; A2 (chatbot) đã bỏ (quyết định 11/11/2026)
- [ ] Dựng tay checklist từng vế điều kiện cho CRP, Procalcitonin, Doppler tim; sửa schema YAML (`dieu_kien.ve`)
- [ ] Bảng ngưỡng sinh hiệu theo tuổi (nhịp thở, nhịp tim), `nguon: tu_dung` đến khi bác sĩ duyệt (M-02)
- [x] PRD nháp ([07-prd.md](07-prd.md)), 12/11/2026
- [ ] Gửi [phiếu hỏi bác sĩ buổi 1](08-phieu-hoi-bac-si.md)
- [x] Spec bản 2 ([09-spec.md](09-spec.md)), đã review độc lập, 12/11/2026
- [x] Bộ mock 53 ca ([data/test-cases/](../data/test-cases/))
- [ ] **Gửi bác sĩ duyệt [06-diem-mo-ho-bac-si-duyet.md](06-diem-mo-ho-bac-si-duyet.md) (M-01…M-18) — xong mới code rule**
- [x] Bộ mock A1 đầu tiên: 5 ca CRP/PCT ([a1-seed.yaml](../data/test-cases/a1-seed.yaml))

## Tuần 3 — Rule engine và bộ test
- [ ] Code rule R1–R4 (`../src/`)
- [ ] Hoàn thiện bộ test 50–100 ca (đã bắt đầu từ tuần 2), gồm các ca xuất toán kể lại (`../data/test-cases/`)

## Tuần 4 — AI và màn hình demo
- [ ] A1: đọc hồ sơ, checklist từng vế kèm trích dẫn; code kiểm tra trích dẫn khớp nguyên văn
- [ ] Nút "Vì sao?": mẫu câu + nguyên văn căn cứ từ YAML (không LLM)
- [ ] Màn hình mô phỏng sidebar cạnh danh sách chỉ định, có lưu lịch sử xác nhận
- [ ] Nhờ 1 bác sĩ gán nhãn ~30 ca

## Tuần 5 — Đánh giá và báo cáo
- [ ] Chạy bộ test, đo tỷ lệ đúng theo từng rule và mức đồng thuận với bác sĩ
- [ ] Viết báo cáo khả thi: số liệu khảo sát, bảng phủ rule, kết quả demo, giới hạn
- [ ] Chuẩn bị demo, mở đầu bằng một ca xuất toán thật (kể lại)
