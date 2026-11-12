# Ý tưởng ban đầu (đã bỏ): BHYT Evidence & Audit Copilot

> Lưu lại để tham chiếu. Đã chuyển hướng sang trợ lý cho bác sĩ lúc chỉ định — lý do ở [../docs/01-bai-toan.md](../docs/01-bai-toan.md).

**AI hỗ trợ tìm, đối chiếu và xác minh bằng chứng thanh toán BHYT**

- **Core product:** Rule engine kiểm tra quyền lợi và điều kiện thanh toán.
- **AI module:** Xử lý các rule không thể kết luận do thiếu dữ liệu cấu trúc, đối chiếu hồ sơ, hỗ trợ mapping phức tạp và chuẩn bị bằng chứng giám định.
- **Người sử dụng:** Nhân viên BHYT, phòng KHTH, khoa dược, bộ phận viện phí, quản lý chất lượng.
- **Không thực hiện:** Tự chẩn đoán, đề xuất chỉ định để tối đa hóa thanh toán, tự sửa bệnh án hay tự quyết định kết quả giám định.

**Hai câu hỏi nghiên cứu quyết định**
- *Kỹ thuật:* Trong HIS/EMR hiện tại, điều kiện BHYT nào vẫn không kiểm tra được bằng mã hoặc trường có cấu trúc?
- *Kinh doanh:* Nhân viên BHYT mất nhiều thời gian nhất ở đâu — chuẩn hóa danh mục, kiểm tra hồ sơ trước gửi, tìm tài liệu chứng minh hay giải trình khoản bị từ chối?

Nếu mọi điều kiện đã mã hóa hoàn chỉnh và kiểm tra chạy tự động thì không nên đưa AI vào. Nếu nút thắt là chứng minh điều kiện thanh toán đã được đáp ứng bằng tài liệu thực tế, Evidence Verification là bài toán AI có lý do tồn tại.

**Vì sao bỏ:** viện không có phòng BHYT/KHTH và không có phần mềm xử lý BHYT → không có người dùng. Hai câu hỏi trên vẫn còn giá trị: câu kỹ thuật chính là "bảng phủ rule" trong [../docs/03-kha-thi.md](../docs/03-kha-thi.md).
