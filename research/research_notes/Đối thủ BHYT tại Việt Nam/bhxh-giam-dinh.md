# BHXH Việt Nam electronic claims assessment (Hệ thống thông tin giám định BHYT) and regulatory data flow

Research date: 2026-11-10. "Verified" = I read the source page/PDF myself. "Snippet" = seen only in a search-result summary; the page fetch failed or was not done. "Inferred" = my reasoning, not stated by a source.

## 1. How the cổng giám định works: rule count, rule types, AI

### Takeaway
Hospitals send XML claim data (QĐ 130/QĐ-BYT, amended by QĐ 4750/QĐ-BYT and QĐ 3176/QĐ-BYT) to the Cổng tiếp nhận dữ liệu at gdbhyt.baohiemxahoi.gov.vn. They should send it right after each visit or discharge, and the package must be digitally signed. The Hệ thống thông tin giám định runs a rule engine on every record. The only published rule count I found is "over 300 rules" (2022). A search snippet quotes "175" automatic checks from a BHXH page I could not open. As of 2026, BHXH talks about AI and early-warning analytics in general terms, but I found no published, specific AI adjudication system.

### Cited Findings
- **Timeline (verified):** the data gateway opened on 24/6/2016, and electronic giám định on the system was fully in operation from January 2017. — [Tạp chí Tòa án, 13/07/2022](https://tapchitoaan.vn/he-thong-thong-tin-giam-dinh-giup-quan-ly-quy-bhyt-hieu-qua6819.html)
- **Scale and rules (verified, 2022 data, likely outdated):** the system connected 12,380 facilities. The giám định software had 230 functions and "over 300 appraisal rules", updated regularly. The article gives no rule categories. Example catches: duplicate billing, wrong bed-day counts, misclassified surgeries, and drug-indication misuse. By 05/2022 the system held 14.58 billion detail rows from 875.96 million visits. — [Tạp chí Tòa án](https://tapchitoaan.vn/he-thong-thong-tin-giam-dinh-giup-quan-ly-quy-bhyt-hieu-qua6819.html)
- **Automatic vs manual savings (verified):** from 2018 to mid-2022, giám định cut 5,922.37 billion VND. Of this, 985.51 billion came from automatic giám định (~17%) and 4,936.86 billion from "chủ động" (proactive, human-led) giám định. — [Tạp chí Tòa án](https://tapchitoaan.vn/he-thong-thong-tin-giam-dinh-giup-quan-ly-quy-bhyt-hieu-qua6819.html)
- **Rule types (snippet, unverified because the fetch failed):** BHXH VN set up "175 automatic check rules" covering the card, benefit level (mức hưởng), drug list, technical service (DVKT) list and calculation logic. — [baohiemxahoi.gov.vn ItemID=9242](https://baohiemxahoi.gov.vn/tintuc/Pages/hoat-dong-tinh-thanh-pho.aspx?CateID=0&ItemID=9242). This conflicts with the "300+" figure above. It may count a different subset or come from a different date.
- **Submission timing (verified, primary):** Công văn 4040/BYT-BH of 25/6/2025 requires every facility to send BHYT cost data to the Cổng tiếp nhận dữ liệu of the Hệ thống thông tin giám định "ngay sau khi kết thúc lần khám bệnh hoặc kết thúc đợt điều trị", under Thông tư 48/2017/TT-BYT, with real-time synchronisation. It also piloted digital signing of the XML package from 26/6/2025, to be rolled out together with electronic medical records (bệnh án điện tử). — [CV 4040/BYT-BH PDF](https://static.luatvietnam.vn/xem-noi-dung-file-cong-van-4040-byt-bh-cua-bo-y-te-ve-viec-trien-khai-dong-bo-du-lieu-chi-phi-kham-chua-benh-bao-hiem-y-te-theo-thoi-gian-thuc-va-thi-diem-ky-so-du-lieu-xml-404052-d6/uploaded/vietlawfile/2025/6/4040_byt_bh_280625103953.pdf.aspx)
- **API (verified, same PDF):** the token endpoint is `https://egw.baohiemxahoi.gov.vn/api/token/take`. Check-in (trạng thái KCB, "XML0") goes to `/api/qd130/checkInKcbQd4750`, and claims go to `/api/qd130/guiHoSoXmlQD4750` as a base64 GIAMDINHHS envelope wrapping XML1–XML13. The response returns maKetQua (200/401/403…), maGiaoDich, thoiGianTiepNhan and thongDiep ("thông điệp lỗi nếu có"). The signature is SHA256 inside a CHUKYDONVI tag. Certificates are registered at gdbhyt.baohiemxahoi.gov.vn. — [CV 4040/BYT-BH](https://static.luatvietnam.vn/xem-noi-dung-file-cong-van-4040-byt-bh-cua-bo-y-te-ve-viec-trien-khai-dong-bo-du-lieu-chi-phi-kham-chua-benh-bao-hiem-y-te-theo-thoi-gian-thuc-va-thi-diem-ky-so-du-lieu-xml-404052-d6/uploaded/vietlawfile/2025/6/4040_byt_bh_280625103953.pdf.aspx)
- **Automatic flagging, as hospitals experience it (verified):** records are digitised and uploaded to the electronic giám định portal. The system automatically flags errors, and BHXH (city and national level) also runs thematic audits (chuyên đề) and sends lists back for the hospital to explain. Hospitals handle "tens of thousands of records per quarter". — [VietBao/VietNamNet, 11/05/2026](https://vietbao.vn/bhyt-khong-thanh-toan-hon-900-trieu-benh-vien-ly-giai-viec-yeu-cau-bac-si-boi-hoan-591630.html)
- **Some rejections are automatic and cannot be edited (verified):** in a 2024 study of a private clinic, staff said administrative errors are "rà soát tự động trên phần mềm giám định và bị trừ tự động, không được phép chỉnh sửa". Wrong ICD codes caused by HIS bugs led to records being "tự động từ chối". — [Nguyễn Quỳnh Anh & Đỗ Văn Huy, Tạp chí Y học Cộng đồng 67(CĐ5), 2026, DOI 10.52163/yhc.v67iCD5.5020](https://tapchiyhcd.vn/index.php/yhcd/article/download/5020/4587/5592)
- **Data standards (secondary, cross-checked across several sources):** the chain is QĐ 130/QĐ-BYT (18/01/2023), then QĐ 4750/QĐ-BYT (29/12/2023), then QĐ 3176/QĐ-BYT. Sources disagree on the 3176 date: 29/10/2024 vs 29/12/2024. XML under 4750 has been official since 01/07/2024, and "XML 4210" (QĐ 4210/2017) is now only a legacy name. — [hl7-org-vn (secondary)](https://hl7-org-vn.pages.dev/en/knowledge/fhir-bhyt/); [luatvietnam QĐ 130](https://luatvietnam.vn/y-te/quyet-dinh-130-qd-byt-241607-d1.html); [hethongphapluat QĐ 3176](https://hethongphapluat.com/quyet-dinh-3176-qd-byt-6ff29c2a9402ae578ee567be63935ec1.html)
- **Shared code lists (snippet):** QĐ 2010/QĐ-BYT (19/6/2025) provisionally issued some shared code lists (danh mục mã dùng chung) for sending BHYT cost data. Công văn 2046/BHXH-TTKS (2026) asks facilities to fix how they map those shared lists. — [search summary of BYT documents](https://cntt.pnt.edu.vn/api/upload/20250605uyl3549_BYT-BH_triển_khai_gửi_dữ_liệu_bhyt.doc); [luatvietnam CV 2046](https://luatvietnam.vn/y-te/cong-van-2046-bhxh-ttks-2026-chan-chinh-ma-hoa-danh-muc-dung-chung-trong-lien-thong-du-lieu-kham-chua-benh-438242-d6.html)
- **AI (verified, vague):** an 02/08/2026 article says IT, digital transformation, data analysis and AI "tiếp tục được đẩy mạnh" in BHYT management and giám định, with early-warning of abnormal costs. It names no specific tool. — [VietnamPlus](https://www.vietnamplus.vn/siet-giam-dinh-kiem-soat-chat-chi-phi-kham-chua-benh-bao-hiem-y-te-post1127691.vnp). An older article says the director of the Trung tâm Giám định BHYT và Thanh toán đa tuyến was researching AI for giám định, and experts advised piloting it carefully. — [VnBusiness](https://vnbusiness.vn/nghien-cuu-ung-dung-tri-tue-nhan-tao-trong-giam-dinh-bhyt.html)
- **2026 enforcement push (snippet):** Công văn 2738/BHXH-TTKS of 24/7/2026 is about "tăng cường thực hiện công tác giám định BHYT". Its full text was not accessible. — [luatvietnam](https://luatvietnam.vn/y-te/cong-van-2738-bhxh-ttks-2026-tang-cuong-thuc-hien-giam-dinh-bao-hiem-y-te-442331-d6.html)
- **Scale in 2026 (verified):** 3,672 facilities provide BHYT care (2,354 public, 1,318 private). There were about 94.4 million visits and 84,765.8 billion VND of spending in H1 2026, up 11.1%. — [VietnamPlus 02/08/2026](https://www.vietnamplus.vn/siet-giam-dinh-kiem-soat-chat-chi-phi-kham-chua-benh-bao-hiem-y-te-post1127691.vnp)

### Inferences
- The rule engine checks structure and lists: card validity, benefit level, whether the service or drug is on the facility's approved list, price, duplicates, and time or quantity logic. Clinical appropriateness (does this test fit this ICD?) is mostly judged by human giám định viên in chủ động or chuyên đề reviews. This fits the ~17% automatic vs ~83% proactive savings split. (Inferred.)
- The `thongDiep` field means the gateway returns some error message at submission. It is probably an XML structure or format check, not the full giám định result. (Inferred; the CV 4040 appendix does not list the error codes.)

### Gaps
- No current (2025–2026) official rule count or published rule catalogue. QĐ 1553/QĐ-BHXH/2017 says a "danh mục quy tắc giám định" exists on the system, but I found no public copy. — [caselaw QĐ 1553](https://caselaw.vn/van-ban-phap-luat/308588-quyet-dinh-1553-qd-bhxh-nam-2017-quy-dinh-ve-quan-ly-khai-thac-thong-tin-tren-he-thong-thong-tin-giam-dinh-bao-hiem-y-te-do-bao-hiem-xa-hoi-viet-nam-ban-hanh)
- I could not confirm whether ICD-to-service appropriateness rules are automated. No source lists them.

## 2. Most common reasons for xuất toán of xét nghiệm / CĐHA / DVKT

### Takeaway
Wrong technical-service orders dominate rejected amounts. That includes services that do not match the ICD-10 diagnosis, are beyond the facility's scope or tier, are not on the approved list, or lack enough qualified staff. Administrative and data errors (card, name, missing signatures, XML mismatches) are second. BHXH also flags orders that duplicate recent results and lab/imaging volumes above the norm.

### Cited Findings
- **Private clinic, Đắk Lắk, all of 2024 (verified):** 1,162 rejected records, 244.45 million VND in total. By amount: "chỉ định kỹ thuật sai quy định" 92.7% (717 records, 226.4 million VND), administrative/data entry 6.2%, wrong drug indication 1.1%. Xét nghiệm: 11.0 million VND rejected (133 records). CĐHA-TDCN: 2.77 million VND (35 records). Procedures/surgery (PT-TT): 220.9 million VND. — [Tạp chí Y học Cộng đồng 2026](https://tapchiyhcd.vn/index.php/yhcd/article/download/5020/4587/5592)
- Staff quotes from the same study, giving the stated mechanisms (verified):
  - "chỉ định không đúng với mã ICD-10, hoặc chỉ định vượt quá giới hạn chuyên môn"
  - "chỉ định cận lâm sàng, Xquang, xét nghiệm, siêu âm… không phù hợp với chẩn đoán chính hoặc không có chỉ định y khoa rõ ràng"
  - services mapped on the BHYT portal "nhưng chưa đủ bác sĩ để làm"
  - orders that were clinically correct but rejected because the facility's danh mục kỹ thuật was not updated
  - XML out of sync between the HIS and the portal, causing duplicates or missing data
  - wrong bid prices after a new tender
  - The study also cites earlier research at Vinmec Times City (2019) and other hospitals with the same pattern: wrong orders are the main cause of xuất toán. — [same source](https://tapchiyhcd.vn/index.php/yhcd/article/download/5020/4587/5592)
- **Public hospital, 2026 (verified):** BV Đa khoa Bà Rịa had over 900 million VND refused for Q4 2025 and recovered only ~100 million from doctors. Risk areas: clinical and paraclinical orders (tests, imaging), drugs, and procedures. Causes: incomplete medical records that do not justify the orders, drug contraindications, procedures outside protocol, inconsistent interpretation between facility and giám định viên, and overlapping audits. Quote: ordering fewer tests risks missing a diagnosis, but ordering more "có nguy cơ bị đánh giá là chỉ định rộng rãi hoặc không cần thiết". — [VietBao/VietNamNet 11/05/2026](https://vietbao.vn/bhyt-khong-thanh-toan-hon-900-trieu-benh-vien-ly-giai-viec-yeu-cau-bac-si-boi-hoan-591630.html)
- **BHXH view (snippet; the page fetch failed):** the Northern regional giám định centre reports duplicate orders and lab/imaging orders above what is needed. BHXH says it gives facilities technical tools to look up patients' previous test and imaging results (lịch sử KCB). — [baohiemxahoi.gov.vn "Lạm dụng chỉ định kỹ thuật y tế"](https://baohiemxahoi.gov.vn/tintuc/pages/linh-vuc-bao-hiem-y-te.aspx?CateID=0&ItemID=9143)
- **Imaging timing norms (verified):** QĐ 2775/QĐ-BYT and QĐ 2776/QĐ-BYT (29/8/2025) set reference durations for CĐHA, e.g. X-ray ~6–12 minutes and ultrasound ~6–15 minutes. Some hospitals read these as payment minimums. In 02/2026 BHXH VN said they are reference values, not mandatory, and that making patients "chờ đủ thời gian" is inappropriate. — [LSVN 05/02/2026](https://lsvn.vn/bhxh-viet-nam-lam-ro-giam-dinh-thanh-toan-bhyt-voi-dich-vu-chan-doan-hinh-anh-a169164.html); [Tuổi Trẻ 06/02/2026](https://tuoitre.vn/chup-x-quang-phai-du-6-phut-moi-duoc-bhyt-chi-tra-quy-dinh-phien-ha-lam-kho-nguoi-benh-20260206084931227.htm)

### Inferences
- The BV Bà Rịa case mentions "differing interpretations of procedure-duration parameters". This suggests the timing fields in XML3 (NGAY_YL / NGAY_TH_YL / NGAY_KQ) are checked against staffing and machine throughput: too many studies per machine or per doctor per hour gets flagged. (Inferred.)
- For a doctor-facing assistant, the controllable error classes are: test or imaging ordered without a matching ICD indication, duplicates of a recent result, a service not on the facility's approved danh mục or tier, and documentation gaps. (Inferred.)

### Gaps
- No national BHXH breakdown of xuất toán by service group (xét nghiệm vs CĐHA). I found only single-facility studies and news.
- No pediatric-specific data.

## 3. Rules on chỉ định cận lâm sàng phù hợp chẩn đoán / coverage conditions

### Takeaway
The main list of covered technical services and their payment conditions is still Thông tư 35/2016/TT-BYT, amended by TT 50/2017, TT 13/2020 and TT 39/2024 (17/11/2024). It requires the service to be approved for the facility, done per the technical procedure, and priced. Services with "điều kiện thanh toán" carry specific indication limits. The overarching framework is the amended Luật BHYT (2024, effective 2025) and Nghị định 188/2025/NĐ-CP (01/7/2025), which require facilities to follow MoH professional guidance and use the fund economically. I did not verify whether TT 35 has been fully replaced by a new 2025–2026 circular.

### Cited Findings
- TT 35/2016: a DVKT is paid only if it is approved by a competent authority, done per the technical procedure, and has an approved price. ND 188/2025 requires following MoH professional guidance and using the fund economically. — [LSVN 05/02/2026](https://lsvn.vn/bhxh-viet-nam-lam-ro-giam-dinh-thanh-toan-bhyt-voi-dich-vu-chan-doan-hinh-anh-a169164.html)
- TT 39/2024/TT-BYT (17/11/2024) amends TT 35/2016 on the list, rates and payment conditions for DVKT, including a group "có quy định cụ thể điều kiện thanh toán" (snippet). — [caselaw](https://caselaw.vn/van-ban-phap-luat/413175-thong-tu-so-39-2024-tt-byt-ngay-17-11-2024-cua-bo-truong-bo-y-te-sua-doi-thong-tu-35-2016-tt-byt-ve-danh-muc-va-ty-le-dieu-kien-thanh-toan-doi-voi-dich-vu-ky-thuat-y-te-thuoc-pham-vi-duoc-huong-cua-nguoi-tham-gia-bao-hiem-y-te); TT 13/2020 amended it earlier — [hoatieu](https://hoatieu.vn/phap-luat/thong-tu-13-2020-tt-byt-sua-doi-thong-tu-35-2016-dieu-kien-thanh-toan-dich-vu-ky-thuat-y-te-202415)
- Nghị định 188/2025/NĐ-CP guides the amended Luật BHYT. CV 6872/BYT-BH (2025) and BHXH CV 3055/BHXH-TTKS give implementation guidance (snippets). — [luatvietnam CV 6872](https://luatvietnam.vn/y-te/cong-van-6872-byt-bh-2025-huong-dan-thuc-hien-nghi-dinh-188-2025-nd-cp-413854-d6.html); [ND 188 text](https://syt.khanhhoa.gov.vn/Resources/Docs/000.Nam%202025/CONGVAN/NGHIDINH_188_2025.pdf)
- Giám định process: QĐ 3618/QĐ-BHXH (12/12/2022), applied from 01/01/2023, replaced the 2015 process in QĐ 1456/QĐ-BHXH. — [caselaw QĐ 3618](https://caselaw.vn/van-ban-phap-luat/584258-quyet-dinh-so-3618-qd-bhxh-ngay-12-12-2022-ve-quy-trinh-giam-dinh-bao-hiem-y-te); [Báo Pháp luật](https://doanhnhan.baophapluat.vn/tu-112023-ap-dung-quy-trinh-giam-dinh-bao-hiem-y-te-moi-49228.html)

### Inferences
- In practice, the "appropriate for diagnosis" standard comes from MoH hướng dẫn chẩn đoán và điều trị (clinical guidelines) and quy trình kỹ thuật, applied by giám định viên. No single circular maps ICD codes to allowed tests, apart from the specific payment conditions in TT 35/TT 39. (Inferred.)
- I list TT 22/2023 and TT 23/2024 from the brief without verifying them. TT 22/2023 is generally the circular on service prices (giá DVKT), not coverage. (Inferred; not checked.)

### Gaps
- Did not verify whether a 2025/2026 circular replaced TT 35/2016 after the amended Luật BHYT. Needs a direct check on thuvienphapluat.
- Did not get the full text of the ND 188 articles on giám định.

## 4. Public / commercial tools to pre-validate XML 130

### Takeaway
I found no officially endorsed BHXH pre-check tool, and no named third-party "XML 130 checker" product. Pre-checking sits inside HIS vendors' BHYT modules or is done manually. The gateway returns a `thongDiep` error message when data is submitted. QĐ 4750 required a test-submission (kiểm thử) phase, and research recommends internal checklists and automated ICD, technical-norm and drug-list alerts. That points to a market gap.

### Cited Findings
- MoH asked BHXH to run test modules for receiving XML under QĐ 130 (CV 6218/BYT-BH 2023; CV 1245/BHXH-CNTT 2024 on kiểm thử). — [luatvietnam CV 6218](https://luatvietnam.vn/y-te/cong-van-6218-byt-bh-2023-trien-khai-kiem-thu-tiep-nhan-du-lieu-kcb-bhyt-269169-d6.html); [CV 1245](https://luatvietnam.vn/bao-hiem/cong-van-1245-bhxh-cntt-2024-trien-khai-kiem-thu-tiep-nhan-du-lieu-dien-tu-xml-413387-d6.html)
- The gateway API returns `thongDiep` with error messages (verified). — [CV 4040/BYT-BH](https://static.luatvietnam.vn/xem-noi-dung-file-cong-van-4040-byt-bh-cua-bo-y-te-ve-viec-trien-khai-dong-bo-du-lieu-chi-phi-kham-chua-benh-bao-hiem-y-te-theo-thoi-gian-thuc-va-thi-diem-ky-so-du-lieu-xml-404052-d6/uploaded/vietlawfile/2025/6/4040_byt_bh_280625103953.pdf.aspx)
- The 2026 Đắk Lắk study recommends pre-submission internal audit, checklists, and "tích hợp cảnh báo tự động về mã ICD, định mức kỹ thuật và danh mục thuốc". It also reports that facility software breaks when BHXH upgrades the portal (verified). — [Tạp chí Y học Cộng đồng](https://tapchiyhcd.vn/index.php/yhcd/article/download/5020/4587/5592)
- A Đồng Nai Sở Y tế document (419/TTTTYTQG) reportedly describes the lack of tools to check electronic claim records, and software with a "giao diện báo cáo kiểm tra" for QĐ 130 (snippet only; the URL returned 404). — [syt.dongnai.gov.vn](https://syt.dongnai.gov.vn/Lists/Vn%20b%E1%BA%A3n/Attachments/9430/419%20TTTTYTQG.pdf)
- An open-source HIS document mentions a giám định BHYT module that exports XML 130/4750/3176 (snippet). — [Google Docs export](https://docs.google.com/document/d/1YY51lTdROvrtSCxOogstIHNyRTKEK7vd/export?format=pdf)

### Inferences
- Major HIS vendors (VNPT HIS, FPT eHospital, Viettel, OneHealth and others) almost certainly have built-in XML export and validation. I verified no product names or features, so treat this as unconfirmed.
- Existing tools focus on format and list validity, not clinical appropriateness at the moment of ordering. That is the gap for a doctor-facing order assistant. (Inferred.)

### Gaps
- No vendor names, pricing or feature lists for pre-check tools were verified. A dedicated vendor scan is needed.

## 5. Timeline: when hospitals learn of rejections

### Takeaway
Data goes in in real time (per visit). Automatic rejections of administrative errors show up on the portal soon after. The binding giám định result and settlement figures come quarterly: BHXH notifies the giám định result and the quyết toán number, and from 10/2/2026 the quyết toán minutes (Mẫu 06/BH, TT 12/2026/TT-BTC) are sent at the same time. One deadline found: within 60 days of receiving the facility's Q4 report. Thematic and retrospective audits can reopen earlier quarters, so a doctor may learn of a rejection months after the order.

### Cited Findings
- Real-time submission after each visit or discharge (verified). — [CV 4040/BYT-BH](https://static.luatvietnam.vn/xem-noi-dung-file-cong-van-4040-byt-bh-cua-bo-y-te-ve-viec-trien-khai-dong-bo-du-lieu-chi-phi-kham-chua-benh-bao-hiem-y-te-theo-thoi-gian-thuc-va-thi-diem-ky-so-du-lieu-xml-404052-d6/uploaded/vietlawfile/2025/6/4040_byt_bh_280625103953.pdf.aspx)
- The giám định result and quyết toán number are notified within 60 days of BHXH receiving the facility's Q4 quyết toán report (snippet, from a provincial TTHC list based on the new law). — [Lai Châu TTHC](https://laichau.gov.vn/upload/2000066/20250718/2__DMTTHC_SYT__2306__f815b.pdf)
- From 10/2/2026, BHXH prepares the quyết toán minutes on Mẫu 06/BH (TT 12/2026/TT-BTC) and sends them together with the giám định result (snippet). — [Thư viện Pháp luật](https://thuvienphapluat.vn/hoi-dap-phap-luat/tu-1022026-quyet-toan-chi-phi-kham-benh-chua-benh-bao-hiem-y-te-thuc-hien-ra-sao-138081500.html)
- BV Bà Rịa learned of 900+ million VND refused for Q4 2025 through the quarterly settlement minutes and had to respond within tight deadlines. Records number in the tens of thousands per quarter (verified). — [VietBao 11/05/2026](https://vietbao.vn/bhyt-khong-thanh-toan-hon-900-trieu-benh-vien-ly-giai-viec-yeu-cau-bac-si-boi-hoan-591630.html)
- The Đắk Lắk study used quarterly settlement minutes (Mẫu 82-HD, 4 quarters of 2024). Staff complained there is no fast feedback channel from BHXH (verified). — [Tạp chí Y học Cộng đồng](https://tapchiyhcd.vn/index.php/yhcd/article/download/5020/4587/5592)

### Inferences
- The feedback lag for clinical-appropriateness rejections is roughly 1–5 months: the end of the quarter plus up to ~60 days or more, and longer for thematic audits. That is too late to change ordering behaviour, which supports the case for point-of-order checks. (Inferred.)

### Gaps
- No verified deadlines for Q1–Q3 under ND 188, and no data on how fast the portal shows automatic-rule results.

## 6. Applicability to private hospitals (Vinmec etc.)

### Takeaway
Any facility with a BHYT contract, public or private, uses the same gateway, XML standard and giám định process. CV 4040 is addressed to the Hiệp hội Bệnh viện tư nhân, and 1,318 private facilities were in the BHYT network as of mid-2026.

### Cited Findings
- CV 4040/BYT-BH recipients include "Cơ sở KCB thuộc các Bộ, ngành, địa phương" and the "Hiệp hội Bệnh viện tư nhân Việt Nam". It applies to "các cơ sở KCB trong toàn quốc" (verified). — [CV 4040](https://static.luatvietnam.vn/xem-noi-dung-file-cong-van-4040-byt-bh-cua-bo-y-te-ve-viec-trien-khai-dong-bo-du-lieu-chi-phi-kham-chua-benh-bao-hiem-y-te-theo-thoi-gian-thuc-va-thi-diem-ky-so-du-lieu-xml-404052-d6/uploaded/vietlawfile/2025/6/4040_byt_bh_280625103953.pdf.aspx)
- 1,318 of 3,672 BHYT facilities are private (end of 06/2026, verified). — [VietnamPlus](https://www.vietnamplus.vn/siet-giam-dinh-kiem-soat-chat-chi-phi-kham-chua-benh-bao-hiem-y-te-post1127691.vnp)
- A private clinic had 92.7% of its rejected amount come from wrong orders. Research on Vinmec Times City (2019) is cited in the reference list, though I did not read it directly (verified as a citation only). — [Tạp chí Y học Cộng đồng](https://tapchiyhcd.vn/index.php/yhcd/article/download/5020/4587/5592)
- BHXH Hà Nội threatened to stop BHYT contracts immediately with facilities that deliberately bill incorrectly (snippet). — [hethongphapluat](https://hethongphapluat.com/phap-luat/node/1671)

### Inferences
- Private hospitals face the same rules but have thinner BHYT margins and fewer dedicated BHYT staff, so each xuất toán hurts more. Vinmec's mix of BHYT and self-pay may create mismatches when a test is clinically justified but not BHYT-payable. (Inferred.)

### Gaps
- I did not read the Vinmec Times City thesis, cited as ref [10] in the Đắk Lắk study: Hán Lương Bằng, master's thesis 2020, "Phân tích kết quả thanh quyết toán chi phí KCB BHYT và một số yếu tố ảnh hưởng tại Bệnh viện Vinmec Times City năm 2019". Worth pulling for Vinmec-specific rejection patterns.
