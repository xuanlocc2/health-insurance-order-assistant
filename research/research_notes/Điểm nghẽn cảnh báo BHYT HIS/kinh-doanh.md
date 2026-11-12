# Vì sao VNPT/Viettel/FPT chưa có (hoặc không quảng bá) cảnh báo BHYT lúc chỉ định: lý do kinh doanh

Ký hiệu: **[XM]** đã đọc nguồn gốc · **[TT]** chỉ thấy qua snippet/tóm tắt tìm kiếm · **[SL]** suy luận. Ngày tra cứu: 10/11/2026. Không lặp lại các fact đã có trong `doi-thu.md`.

## 1. Mô hình mua sắm HIS: đấu thầu, thuê dịch vụ, giá và việc hồ sơ mời thầu (HSMT) quy định tính năng

### Takeaway
Bệnh viện công mua HIS bằng hình thức thuê dịch vụ CNTT qua đấu thầu. HSMT và các bản tự đánh giá đều bám theo checklist chức năng của TT 54/2017. Checklist này chỉ đặt BHYT ở khâu thanh toán: viện phí, duyệt hồ sơ, gửi XML lên cổng. Ở khâu chỉ định, yêu cầu chỉ là "tiếp nhận và quản lý chỉ định". Không có tiêu chí nào đòi cảnh báo BHYT lúc chỉ định, và trong các tài liệu tìm được cũng không có HSMT nào đòi tính năng này. Vendor không bị chấm điểm theo tính năng đó, nên họ không có lý do để làm.

### Cited Findings
- Bản tự đánh giá theo TT 54/2017 của BVĐK tỉnh Quảng Ngãi (tháng 5/2025), dùng làm phụ lục cho thông báo mua sắm. **[XM]** ([bvdk.quangngai.gov.vn](https://bvdk.quangngai.gov.vn/getFile.aspx?ida=115)). Đã trích văn bản từ PDF. Các mục HIS liên quan BHYT gồm:
  - Mức 1, mục 35 "Quản lý viện phí và thanh toán BHYT": "Quản lý danh sách bệnh nhân thanh toán; Thu tiền bệnh nhân; Duyệt hồ sơ bệnh nhân; Gửi hồ sơ bảo hiểm lên cổng giám định bảo hiểm".
  - Mức 1, mục 36: "Kết nối với BHXH thanh quyết toán BHYT (tập tin XML)… xuất dữ liệu XML, báo cáo 19, 20, 21, 79, 80".
  - Mức 2, mục 37 "Quản lý chỉ định lâm sàng, cận lâm sàng" chỉ yêu cầu "Tiếp nhận và quản lý được các chỉ định của bác sỹ; Quản lý các danh mục dịch vụ, kỹ thuật…; Quản lý các mẫu". Mục này **không có yêu cầu kiểm điều kiện thanh toán**.
  - Trong cả phần HIS và LIS, chữ "cảnh báo" chỉ xuất hiện ở cảnh báo thuốc/tương tác thuốc (mục Dược; Mức 6 "Quản lý tương tác thuốc") và cảnh báo kết quả xét nghiệm bất thường (LIS). Mức 6 "Quản lý phác đồ điều trị" có "chỉ định theo phác đồ", nhưng là tiêu chí lâm sàng, không gắn với thanh toán.
  - BV này còn "Chưa đáp ứng" Mức 6–7. Tức là ngay cả tiêu chí lâm sàng nâng cao cũng chưa đạt, chưa nói đến tính năng ngoài checklist.
- TT 54/2017/TT-BYT chia tiêu chí thành 8 nhóm (hạ tầng, quản lý điều hành, HIS, RIS-PACS, LIS, phi chức năng, bảo mật, EMR) và xếp HIS theo mức 1–7 **[TT]** ([thuvienphapluat](https://thuvienphapluat.vn/documents/law.aspx?id=k%3Dpjek1qa3TX); [hoatieu](https://hoatieu.vn/phap-luat/thong-tu-54-2017-tt-byt-1533)).
- HSMT do bệnh viện viết đến mức rất chi tiết từng tính năng. Ví dụ, thư mời báo giá phần mềm Quản lý nhà thuốc của BV Nhi Trung ương (3/2024) liệt kê từng cảnh báo cụ thể: giá nhập lệch giá khai báo, giá bán vượt tỷ lệ, hạn thầu, hạn dùng, tương tác thuốc **[XM]** ([BV Nhi TW](https://benhviennhitrunguong.gov.vn/wp-content/uploads/2024/03/TMBG-PM-QLNT-CS1.2024_compressed.pdf)). Điều này cho thấy: khi bệnh viện muốn một cảnh báo, họ ghi thẳng vào HSMT. Các cảnh báo được ghi ở đây phục vụ đúng khoa/phòng ra đề bài, ở ví dụ này là Dược.
- Giá các gói thầu:
  - BV HNĐK Nghệ An thuê HIS + EMR 36 tháng (2026–2028), giá gói dự kiến **12,6 tỷ đồng**, tức khoảng 350 triệu/tháng. Đăng ngày 27/02/2026 **[XM]** ([Báo Đấu thầu](https://baodauthau.vn/benh-vien-huu-nghi-da-khoa-nghe-an-yeu-cau-bao-gia-post194237.html)).
  - BV Nhi TW khái toán thuê nhiều phần mềm 24,76 tỷ, trong đó HIS Cơ sở 2 là 8,24 tỷ **[TT]** ([BV Nhi TW thư mời 255](https://benhviennhitrunguong.gov.vn/wp-content/uploads/2024/06/Thu-moi-BG-so-255-TM-BVNTW-ngay-3-6-2024-Thue-dich-vu-CNTT_v_compressed.pdf)).
  - Một gói nhỏ tuyến cơ sở dự toán 300 triệu/năm (hỏi đáp năm 2019) **[TT]** ([thuvienphapluat](https://thuvienphapluat.vn/hoi-dap-phap-luat/thue-phan-mem-cntt-co-duoc-ap-dung-chao-hang-canh-tranh-khong-299798.html)).
  - Năm 2015, một bệnh viện thuê VNPT-HIS trọn gói **10 triệu đồng/tháng** **[XM]** ([Báo Đầu tư, 18/4/2015](https://baodautu.vn/dai-gia-vien-thong-dua-bao-san-dich-vu-cong-nghe-nganh-y-d25597.html)).
- Bộ trưởng Y tế (2015) chủ trương "thuê dịch vụ CNTT" là cách nhanh và hiệu quả nhất. Viettel chọn tuyến xã/huyện vì đó là "thị trường rất lớn nhưng đang bỏ ngỏ" do năng lực CNTT ở tuyến này yếu **[XM]** ([Báo Đầu tư](https://baodautu.vn/dai-gia-vien-thong-dua-bao-san-dich-vu-cong-nghe-nganh-y-d25597.html)).
- VNPT-HIS ở Hà Nam được chạy thử 6 tháng rồi mới ký thuê. VNPT tự nhận "mức giá thị trường tốt nhất" và có mặt ở khoảng 6.920/13.800 cơ sở **[TT]** ([VietTimes](https://viettimes.vn/vnpt-day-manh-trien-khai-giai-phap-vnpt-his-trong-nganh-y-te-ha-nam-post83012.html)).
- Bộ Y tế nói bệnh viện "hoàn toàn có thể ra đề bài" để nhà cung cấp chọn giải pháp phù hợp **[TT]** (tóm tắt tìm kiếm, nguồn: [VnEconomy](https://vneconomy.vn/bo-y-te-thuc-tien-do-trien-khai-benh-an-dien-tu.htm)).

### Inferences
- **[SL]** Vendor xây sản phẩm theo checklist TT 54, QĐ 130 và TT 13/2025, vì đó là thứ được chấm thầu và nghiệm thu. Cảnh báo BHYT lúc chỉ định nằm ngoài cả ba văn bản, nên không có giá trị trong chấm thầu.
- **[SL]** Ở tuyến xã/huyện (thị trường chính của VNPT/Viettel), giá thuê chỉ ở mức hàng chục triệu/tháng. Với biên lợi nhuận đó, vendor không thể làm và duy trì nội dung rule lâm sàng–BHYT cho từng cơ sở.
- **[SL]** Người ra đề bài HIS thường là phòng CNTT phối hợp các phòng nghiệp vụ. Phòng nào chịu áp lực thì ghi cảnh báo của phòng đó (Dược ghi cảnh báo giá/hạn thầu). Bác sĩ lâm sàng hiếm khi là bên viết HSMT.

### Gaps
- Chưa mở được HSMT HIS đầy đủ nào trên muasamcong (cần đăng nhập/tải e-HSMT). Không thể khẳng định 100% rằng *không* có HSMT nào đòi "cảnh báo BHYT khi chỉ định". Chỉ có thể nói: không tìm thấy qua tìm kiếm, và các mẫu đã xem đều không có.
- Chưa đọc trực tiếp TT 46/2018 và TT 13/2025 để liệt kê đầy đủ phần bắt buộc và tùy chọn. Theo snippet, TT 13/2025 có hiệu lực 21/7/2025 **[TT]**.
- Một trang Bắc Giang (danh mục HIS Dũng 2024) và trang SYT Bắc Giang không truy cập được (lỗi DNS).

## 2. Ưu tiên của vendor 2023–2026: QĐ 130/4750, EMR 30/9/2025, VNeID/Đề án 06

### Takeaway
Giai đoạn 2023–2026 liên tiếp có các đợt tuân thủ bắt buộc, có hạn chót và có chế tài: XML theo QĐ 130 (từ 01/7/2024), đồng bộ thời gian thực và ký số XML (CV 4040, 6/2025), EMR trước 30/9/2025, và các nhiệm vụ Đề án 06. Năng lực của vendor dồn vào các việc này. Dù vậy, đến hạn EMR vẫn chỉ khoảng một nửa số bệnh viện đạt.

### Cited Findings
- Thủ tướng yêu cầu triển khai EMR toàn quốc trước 30/9/2025. Đến 25/9/2025, mới 630 cơ sở bỏ bệnh án giấy, 84/125 BV tỉnh hạng 1 và 140/399 BV tư đã triển khai. Bộ Y tế xác nhận sẽ trễ. Nguyên nhân được nêu gồm khó khăn phần mềm khi chuyển bộ quản lý, sắp xếp đơn vị hành chính, và đấu thầu chậm. Về Đề án 06, Bộ Y tế mới xong 7/10 nhiệm vụ **[XM]** ([VnEconomy 25/9/2025](https://vneconomy.vn/trien-khai-benh-an-dien-tu-tren-toan-quoc-chua-the-ve-dich-trong-thang-92025.htm)).
- Đến 4/10/2025, "gần 50% bệnh viện chậm công bố triển khai EMR" **[TT]** ([Tuổi Trẻ](https://tuoitre.vn/gan-50-benh-vien-ca-nuoc-cham-cong-bo-trien-khai-benh-an-dien-tu-20251004181752363.htm); [Nhân Dân](https://nhandan.vn/moi-co-hon-50-co-so-y-te-trien-khai-benh-an-dien-tu-post912980.html)). Người đứng đầu bệnh viện không hoàn thành có thể bị xem xét trách nhiệm và thi đua **[TT]** (cùng nguồn).
- Viettel Solutions tự nhận đã triển khai EMR cho hơn 200 cơ sở **[TT/VC]** ([Nhân Dân](https://nhandan.vn/benh-vien-thong-minh-khong-phai-dich-den-ma-la-mot-qua-trinh-post924400.html)).
- Theo snippet, thách thức lớn nhất của EMR là chi phí đầu tư cao trong khi tài chính bệnh viện hạn chế **[TT]** ([Tuổi Trẻ 8/7/2025](https://tuoitre.vn/khai-tu-benh-an-giay-co-dung-hen-20250708231259942.htm)).
- Các mốc QĐ 130 và CV 4040 đã nêu trong `doi-thu.md`, không lặp lại ở đây.

### Inferences
- **[SL]** Mỗi văn bản kể trên đều có hạn chót, gắn trách nhiệm người đứng đầu, và gắn với dòng tiền: XML sai thì không được thanh toán. Cảnh báo lúc chỉ định là tính năng "nice-to-have", không có văn bản nào ép. Khi nhân lực triển khai có hạn, vendor ưu tiên những gì khách hàng sẽ bị phạt nếu thiếu.
- **[SL]** Vendor lớn đã có sẵn một kênh nhận lỗi ở phía sau: cổng BHXH trả về `thongDiep` khi gửi XML. Kênh này đủ để thỏa yêu cầu "kết nối giám định", nên không có áp lực đẩy kiểm tra lên trước, vào lúc chỉ định.

### Gaps
- Không tìm thấy phát biểu công khai nào của VNPT, Viettel hay FPT về lộ trình (roadmap) cho tính năng kiểm BHYT lúc chỉ định, và cũng không có nguồn nào nói vendor "quá tải".

## 3. Ai chịu tiền khi BHYT xuất toán, và người đó có ngân sách/quyền mua công cụ không

### Takeaway
Ở bệnh viện công, phần lớn tiền xuất toán do bệnh viện gánh từ nguồn thu chung. Hệ quả là thu nhập tăng thêm của toàn bộ nhân viên giảm. Chỉ một phần nhỏ bị đòi lại từ bác sĩ, và chỉ với lỗi cá nhân lặp lại. Bác sĩ, khoa lâm sàng là người chịu thiệt nhưng không có ngân sách mua phần mềm. Người có ngân sách và quyền ra đề bài (ban giám đốc, phòng TCKT, phòng BHYT/KHTH) thì đang xử lý vấn đề bằng tổ giám sát và công cụ rà hồ sơ sau khám.

### Cited Findings
- BVĐK Bà Rịa: BHYT từ chối hơn 900 triệu của quý 4/2025. Chỉ "hơn 100 triệu" được thu lại từ cá nhân, phần lớn còn lại bệnh viện tự chịu. Phó GĐ Lê Minh Hiếu nói việc thu lại chỉ áp dụng với "lỗi cá nhân rõ ràng", đã nhắc nhở và tập huấn nhiều lần mà vẫn tái diễn. Lý do ông đưa ra: nếu nguồn thu chung bù cho sai sót thì "thu nhập tăng thêm của những nhân viên khác cũng bị ảnh hưởng". Ông cũng nói "nhiều cơ sở khác cũng áp dụng biện pháp tương tự". Bệnh viện có "Tổ giám sát chi phí BHYT" với bộ phận tiền kiểm rà hồ sơ trước khi đẩy lên cổng, khối lượng hàng chục nghìn hồ sơ mỗi quý **[XM]** ([VietnamNet EN](https://vietnamnet.vn/en/doctors-face-new-stress-paying-bills-denied-by-health-insurers-2515230.html); [VietBao](https://vietbao.vn/bhyt-khong-thanh-toan-hon-900-trieu-benh-vien-ly-giai-viec-yeu-cau-bac-si-boi-hoan-591630.html)).
- Không tìm thấy văn bản quy phạm nào quy định việc trừ tiền xuất toán vào lương hay thu nhập tăng thêm. Việc này do quy chế chi tiêu nội bộ của từng bệnh viện quyết định **[TT]** (kết quả tìm kiếm không có văn bản; xem [VietBao](https://vietbao.vn/bhyt-khong-thanh-toan-hon-900-trieu-benh-vien-ly-giai-viec-yeu-cau-bac-si-boi-hoan-591630.html)).
- Công cụ trả phí duy nhất có dấu vết mua sắm thuộc lớp "rà soát dữ liệu thanh toán BHYT" sau lượt khám (MDinsight, adaptor đồng bộ, ">80 cơ sở"), do Trung tâm Thông tin y tế QG giới thiệu cho Sở Y tế và cơ sở **[TT]** ([419/TTTTYTQG](https://syt.dongnai.gov.vn/Lists/Vn%20bn/Attachments/9430/419%20TTTTYTQG.pdf)). Một hồ sơ dự toán thuê dịch vụ CNTT (HIS/EMR/PACS) liệt kê riêng hạng mục "Phân hệ giám định BHYT điện tử" **[TT]** (snippet; [docs.google.com](https://docs.google.com/document/d/1RojENFaWHwLCejCehbZltJsOY2EsvWi_/export?format=pdf)).
- Vinmec (tư nhân): theo thông tin nội bộ của người dùng, **bác sĩ trả tiền xuất toán theo user**. Chưa có nguồn công khai **[nội bộ, chưa kiểm]**.

### Inferences
- **[SL]** Ở bệnh viện công, thiệt hại bị chia mỏng: một phần vào thu nhập tăng thêm của toàn viện, một phần nhỏ cho bác sĩ. Khi đó không cá nhân nào vừa đau đủ nhiều vừa có ngân sách. Người có ngân sách là ban giám đốc và phòng TCKT. Họ coi xuất toán là việc của phòng BHYT, và mua (hoặc lập) công cụ rà hồ sơ, tổ tiền kiểm, tức thứ phục vụ chính họ.
- **[SL]** Ở Vinmec, nếu bác sĩ trả theo user thì đây là trường hợp hiếm: người chịu thiệt chính là người ra chỉ định. Tuy vậy, bác sĩ vẫn không phải người mua phần mềm. Người mua là bệnh viện. Lập luận bán hàng vì thế phải nhắm vào lợi ích của bệnh viện: giữ chân bác sĩ, giảm tranh chấp nội bộ, giảm doanh thu bị mất.

### Gaps
- Chưa có số liệu hệ thống về tỷ lệ xuất toán được thu lại từ bác sĩ ở các bệnh viện công khác.
- Chưa có quy chế chi tiêu nội bộ công khai nào mô tả cơ chế khấu trừ.

## 4. Tùy biến theo từng bệnh viện: danh mục, giá, phạm vi hợp đồng BHYT

### Takeaway
Mọi HIS đều phải quản lý danh mục dịch vụ, giá và mapping danh mục dùng chung *của từng bệnh viện*. Một bộ rule "dịch vụ ↔ ICD ↔ tần suất ↔ phạm vi hợp đồng BHYT" sẽ phải viết riêng cho từng cơ sở và cập nhật mỗi lần danh mục hoặc giá thay đổi. Với mô hình thuê trọn gói giá thấp, chi phí nội dung này không có ai trả.

### Cited Findings
- TT 54, mục 31 "Quản lý danh mục dùng chung" đòi quản lý danh mục ICD và danh mục dịch vụ khám, xét nghiệm, CĐHA, PTTT, phụ thu *của bệnh viện* **[XM]** ([Quảng Ngãi](https://bvdk.quangngai.gov.vn/getFile.aspx?ida=115)). Danh mục là dữ liệu riêng của từng bệnh viện, HIS chỉ cung cấp khung để nhập.
- VNPT bán HIS "trọn gói" và triển khai hàng loạt theo tỉnh, ví dụ 173 trạm y tế ở Tiền Giang hay 110 trạm ở Hà Nam **[XM/TT]** ([Báo Đầu tư](https://baodautu.vn/dai-gia-vien-thong-dua-bao-san-dich-vu-cong-nghe-nganh-y-d25597.html); [VietTimes](https://viettimes.vn/vnpt-day-manh-trien-khai-giai-phap-vnpt-his-trong-nganh-y-te-ha-nam-post83012.html)). Đây là mô hình một sản phẩm cho nhiều cơ sở.
- Bản thân BHXH không công bố bộ quy tắc giám định (xem `doi-thu.md`). Không có nguồn rule chuẩn quốc gia nào để vendor nạp sẵn.

### Inferences
- **[SL]** Phần khó của tính năng là nội dung chứ không phải code: bảng rule có căn cứ, có người chịu trách nhiệm khi rule sai. Vendor HIS bán phần mềm và hạ tầng, không bán nội dung lâm sàng–pháp lý. Nếu rule sai, bác sĩ bỏ chỉ định cần thiết hoặc bệnh viện vẫn bị xuất toán, và trách nhiệm pháp lý dồn về vendor.
- **[SL]** Bệnh viện lớn (tuyến TW, tỉnh hạng 1) có thể đòi tùy biến, nhưng khi đó họ ưu tiên EMR, PACS, ký số. Bệnh viện tuyến dưới thì dùng bản chuẩn.

### Gaps
- Không có nguồn công khai so sánh mức tùy biến HIS giữa VNPT, Viettel và FPT.

## 5. Vendor có coi kiểm BHYT là tính năng cho phòng BHYT/viện phí thay vì cho bác sĩ không

### Takeaway
Có. Toàn bộ tài liệu chuẩn (TT 54) và tài liệu thầu xếp BHYT vào phân hệ "Viện phí và thanh toán BHYT" và "Kết nối BHXH". Các công cụ BHYT bán riêng cũng phục vụ khâu rà hồ sơ. Không thấy vendor lớn nào gắn kiểm BHYT vào màn hình chỉ định.

### Cited Findings
- Trong TT 54, BHYT xuất hiện ở các mục "Quản lý viện phí và thanh toán BHYT" và "Kết nối với BHXH thanh quyết toán BHYT (XML)", không xuất hiện ở mục chỉ định **[XM]** ([Quảng Ngãi](https://bvdk.quangngai.gov.vn/getFile.aspx?ida=115)).
- FPT.eHospital được mô tả với module "insurance billing" (thanh toán bảo hiểm) **[XM]** ([Báo Đầu tư](https://baodautu.vn/dai-gia-vien-thong-dua-bao-san-dich-vu-cong-nghe-nganh-y-d25597.html)).
- Từ 12/2014, Viettel làm phần mềm giám định và thanh toán *cho BHXH*, tức phía bên chi trả **[XM]** (cùng nguồn).
- Sở Y tế Đồng Nai tham chiếu các "báo cáo trùng y lệnh nội trú/ngoại trú" và "báo cáo trùng thời gian thực hiện PTTT". Đây là báo cáo sau sự việc, không phải cảnh báo lúc bác sĩ chỉ định **[TT]** ([419/TTTTYTQG](https://syt.dongnai.gov.vn/Lists/Vn%20bn/Attachments/9430/419%20TTTTYTQG.pdf)).

### Inferences
- **[SL]** Khung tư duy của vendor và bệnh viện là "BHYT là chuyện của viện phí". Tính năng BHYT được thiết kế cho người duyệt hồ sơ (báo cáo, danh sách lỗi), không cho người ra y lệnh. Ngoài ra, chèn cảnh báo vào luồng chỉ định làm chậm bác sĩ. Đây là rủi ro bị bác sĩ phàn nàn, trong khi người hưởng lợi (phòng TCKT) không ngồi ở màn hình đó.

### Gaps
- Không tìm thấy tài liệu sản phẩm chi tiết (user manual) của VNPT/Viettel/FPT để xác nhận có hoặc không có cấu hình cảnh báo trùng chỉ định do IT bệnh viện tự bật.

## 6. Bệnh viện tư: ai sẽ làm cho Vinmec/Tâm Anh

### Takeaway
Nhận định "vendor lớn không phục vụ bệnh viện tư" chỉ đúng một phần. FPT có phục vụ chuỗi tư (Hoàn Mỹ, Medlatec), nhưng không quảng bá tính năng BHYT nào cho các khách này. Vinmec chạy Orion Health (hệ ngoại), nên vendor nội địa không có kênh để bán. Orion cũng không có động cơ làm logic BHYT Việt Nam cho một khách hàng. Khoảng trống này chỉ có thể lấp bằng middleware nội bộ hoặc bên thứ ba.

### Cited Findings
- FPT.eHospital 2.0 cộng FPT Cloud được triển khai cho toàn mạng Hoàn Mỹ (14 bệnh viện, 4 phòng khám). Không nhắc đến BHYT hay kiểm claim **[XM]** ([FPT IS – Hoàn Mỹ](https://fpt-is.com/en/customers/partnering-with-hoan-my-medical-corporation-to-drive-digital-transformation-in-healthcare-services/)).
- Medlatec có tên trong danh sách khách hàng FPT (FPT.EMR) **[TT]** ([FPT IS medical](https://fpt-is.com/en/medical-healthcare/)).
- Đến 25/9/2025 mới 140/399 bệnh viện tư triển khai EMR **[XM]** ([VnEconomy](https://vneconomy.vn/trien-khai-benh-an-dien-tu-tren-toan-quoc-chua-the-ve-dich-trong-thang-92025.htm)). Ở khối tư, năng lực CNTT cũng đang dồn vào EMR.
- Không tìm thấy nguồn công khai về HIS của Tâm Anh hay Hồng Ngọc (tự phát triển hay mua) **[gap]**. Vinmec dùng Orion Health: xem `doi-thu.md`.

### Inferences
- **[SL]** Với bệnh viện tư dùng HIS ngoại, rào cản là cấu trúc. Vendor ngoại không làm rule BHYT Việt Nam, vendor nội không chạm được vào HIS. Người duy nhất có cả động cơ lẫn quyền truy cập dữ liệu là chính bệnh viện, qua IT nội bộ hoặc một dự án như project này.
- **[SL]** Ở bệnh viện tư, BHYT chiếm tỷ trọng doanh thu nhỏ hơn so với dịch vụ và bảo hiểm tư. Ưu tiên CNTT vì thế nghiêng về trải nghiệm khách hàng và bảo hiểm tư, cũng là lý do thị trường "AI claims" hướng về TPA (xem `doi-thu.md`). Điểm này chưa có số liệu kiểm chứng.

### Gaps
- Chưa có tỷ trọng doanh thu BHYT ở Vinmec hay Tâm Anh.
- Chưa có thông tin HIS hiện tại (sau 2020) của Vinmec, Tâm Anh, Hồng Ngọc.
