# Testing the premise: do VNPT-HIS, Viettel HIS and FPT.eHospital already warn about BHYT when the doctor orders?

Research date: 2026-11-10. About 17 tool calls. This file builds on `Đối thủ BHYT tại Việt Nam/his-vendors.md` and does not repeat it.

Labels used below:
- VERIFIED: I fetched or extracted the source text myself.
- SNIPPET: the claim comes from a search summary or snippet only.
- INFERRED: my own reasoning from the evidence.

**Bottom line:** the public web has no user manual, video, release note or help-desk page for VNPT, Viettel or FPT that shows what their order screen does about BHYT. The premise "the big 3 don't do this" therefore cannot be proven or disproven from public sources. Two things do weaken a strong version of it:
1. Simple order-time warnings (duplicate service, duplicate drug or antibiotic group, drug interaction, quantity over định mức, order outside phác đồ) are listed as **commodity HIS functions**. They appear even in an open-source HIS feature list mapped to TT 54.
2. FPT.eHospital has a verified order-time CDSS, but it covers drug safety and phác đồ, not BHYT payability.

The defensible claim is narrower: "No evidence that the big 3 give doctors a BHYT payability or xuất toán risk check at order time (ICD↔DVKT fit, danh mục/điều kiện thanh toán, tần suất). Generic duplicate and quantity warnings probably exist and are table stakes."

---

## 1. Do the big 3 have order-time BHYT warnings that are simply not marketed?

### Takeaway
I found no public product documentation for any of the three that shows BHYT warnings on the order screen, so the question stays open. Public procurement and feature lists show that a "cảnh báo chỉ định trùng dịch vụ" (duplicate-order warning) is a standard expected HIS function. Every mainstream HIS very likely has some form of it, but none of the sources check BHYT rules such as ICD↔service fit or payment conditions.

### Cited Findings
**Feature lists that show what "standard" means**
- **VERIFIED.** A Google Docs appendix, "Phục lục nâng cấp HIS", titled "Dịch vụ cài đặt và đào tạo hướng dẫn sử dụng Phần mềm quản lý bệnh viện (HIS) nguồn mở – PHỤ LỤC 01: DANH SÁCH CHỨC NĂNG PHẦN MỀM HIS NGUỒN MỞ", maps features to the TT 54 criteria. The hospital and date are not shown in the extracted text.
  - Its outpatient and inpatient modules list:
    - "Chức năng cảnh báo chỉ định trùng dịch vụ"
    - "Chức năng cảnh báo trùng thuốc, trùng nhóm kháng sinh"
    - "Chức năng cảnh báo tương tác thuốc"
    - "Chức năng cảnh báo thuốc còn sử dụng"
    - "Chức năng cảnh báo số tiền tạm ứng không đủ"
    - "Chức năng cảnh báo kê thuốc vượt định mức trong gói"
    - "Chức năng cảnh báo kê vật tư vượt định mức trong gói"
    - "Chức năng quản lý chặt trẽ người bệnh không có thẻ BHYT (Thu tiền công khám, tiền CLS, tiền thủ thuật)"
  - Its admin functions include "Khóa dịch vụ (tạm thời không cho phép bác sĩ chỉ định dịch vụ/thuốc/vật tư … vì lý do nào đó. VD: máy hỏng."
  - At Mức 6 it adds "Gán thuốc, dịch vụ theo ICD vào phác đồ" and "Cảnh báo chỉ định sai phác đồ".
  - Source: [Google Docs export](https://docs.google.com/document/d/1YY51lTdROvrtSCxOogstIHNyRTKEK7vd/export?format=pdf)
- **VERIFIED.** The Bệnh viện Nhi Trung ương EMR rental tender (thư mời thẩm định giá, 10/2025, 36-month rental 2025–2028) lists "Quản lý chỉ định" for khám, thuốc/VTYT, DVKT, phác đồ and others, plus phác đồ management keyed to ICD. It contains **no requirement for BHYT order-time warnings**. The only "cảnh báo" in the text is the Early Warning Score. — [BV Nhi TƯ](https://benhviennhitrunguong.gov.vn/wp-content/uploads/2025/07/Thu-moi-tham-dinh-gia-PM-Benh-an-dien-tu.pdf)
- **SNIPPET.** A Quảng Ngãi self-assessment against the TT 54 HIS criteria asks for "Quản lý chỉ định lâm sàng, cận lâm sàng" and XML export for BHYT. It has no order-time BHYT check criterion. — [BVĐK Quảng Ngãi](https://bvdk.quangngai.gov.vn/getFile.aspx?ida=115)

**VNPT-HIS**
- **VERIFIED in prior notes, plus SNIPPET.** The only public VNPT manual is the mobile app guide (TL_HDSD_MobileAppHis v1.0.0, 2025). Its list of video topics covers login and room setup, ngoại trú YHCT records, ký số hội chẩn and tra cứu HSBA. The YouTube links are marked "(Chờ bổ sung)", and nothing covers ordering or BHYT. — [VNPT storage PDF](https://storage-vnportal.vnpt.vn/gov-tha/7361/file-document/635878550.638802354440490723.pdf)
- No public desktop HIS L2/L3 manual or YouTube tutorial on chỉ định CLS turned up in four query variants. An earlier search also tried his.vnpthis.vn without results.

**Viettel HIS**
- No manual or tutorial found. Search results only list Viettel HIS among common HIS products. — (no source; this is a gap)
- **SNIPPET.** In one study of e-prescribing software share, Viettel HIS had 11,9%, FPT.eHospital 50,1%, Onemes 22,9% and Medisoft 15,1%. The study's sample and scope are unclear. — [Tạp chí YHCĐ](https://tapchiyhcd.vn/index.php/yhcd/article/download/1493/916/1096)

**FPT.eHospital: the strongest evidence of order-time decision support, but clinical, not BHYT**
- **SNIPPET.** BVĐK tỉnh Quảng Ninh deployed electronic treatment protocols (ICD-10 based) and a "level 3" CDSS drug-alert system integrated in FPT.eHospital. Alerts fire "ngay khi bác sĩ kê đơn" when the prescription doesn't fit the patient or drugs conflict. BHYT payability is not mentioned. — [FPT IS](https://fpt-is.com/en/customers/fpt-partners-with-quang-ninh-general-hospital-to-deploy-electronic-treatment-protocols-and-an-intelligent-clinical-decision-support-system/), [FPT IS alt](https://fpt-is.com/en/fpt-partners-with-quang-ninh-general-hospital-to-develop-electronic-treatment-protocols-and-an-intelligent-clinical-drug-alert-system)

### Inferences
- **INFERRED.** Because duplicate-service and over-định-mức warnings appear in a generic open-source TT 54 feature list, the big 3 very likely have similar warnings, with configuration done by the hospital or vendor. Any pitch that says "HIS has no warnings" will be contradicted by hospital IT staff. Position the product as **BHYT-rule-aware** (ICD↔DVKT, điều kiện thanh toán, tần suất/khoảng cách theo quy định, danh mục kỹ thuật of the facility), not as "warnings exist."
- **INFERRED.** Phác đồ-based warnings ("cảnh báo chỉ định sai phác đồ", FPT's CDSS) overlap partly with xuất toán risk, because "chỉ định không đúng phác đồ" is a common xuất toán reason. FPT is the most likely of the big 3 to extend into this space.

### Gaps
- No vendor manual, screenshot, release note or training video for the order screen of VNPT, Viettel or FPT. These are typically distributed privately to hospitals, for example on vendor support portals or in Zalo groups.
- I could not check which rules are vendor-default and which the hospital configures. The open-source list implies the functions exist but not how their rules are populated.
- I did not access Facebook groups or Zalo, where hospital IT and doctors discuss HIS behaviour. The next step should be direct interviews or demo access, such as asking a Vinmec or partner-hospital IT contact for screenshots.

---

## 2. What do doctors and staff say about HIS warnings and BHYT burden?

### Takeaway
Public doctor voice is about **xuất toán liability**: being made to repay (bồi hoàn), and the dilemma between ordering fully and being flagged. It is not about HIS warnings as such. Qualitative interviews at a Đắk Lắk clinic directly blame the HIS: lack of automatic warnings, danh mục mapping that lags new rules, and system freezes that create duplicate records. I found no public praise or complaint aimed specifically at big-3 order-screen warnings.

### Cited Findings
- **VERIFIED.** At BVĐK Bà Rịa (TP.HCM), BHYT refused more than 900 triệu đồng in Q4/2025, and about 100 triệu was recovered from individual staff. Deputy director BS.CKII Lê Minh Hiếu said bồi hoàn applies only to repeated individual errors after training and warnings. The hospital also "ứng dụng phần mềm cảnh báo chống chỉ định thuốc và tương tác thuốc có hại", which is a drug-safety tool, not a BHYT-rule tool. — [vietbao, 11/5/2026](https://vietbao.vn/bhyt-khong-thanh-toan-hon-900-trieu-benh-vien-ly-giai-viec-yeu-cau-bac-si-boi-hoan-591630.html)
- **VERIFIED.** VietnamNet (19/05/2026), covering the same case:
  - Doctors on staff forums feared that "over-prescribing" means repaying.
  - The article quotes a saying: "A good doctor is the one with the fewest disallowed costs."
  - Doctors face a dilemma: ordering full tests risks being labeled unnecessary, while ordering fewer risks missing lesions.
  - Error filtering is described as happening at the cổng giám định and through a hospital "pre-check" unit. The article does not mention HIS warnings to prescribers.
  - Source: [VietnamNet EN](https://vietnamnet.vn/en/doctors-face-new-stress-paying-bills-denied-by-health-insurers-2515230.html)
- **VERIFIED.** Nguyễn Quỳnh Anh & Đỗ Văn Huy studied PKĐK Tâm Phúc Eakar (Đắk Lắk) in 2024 (Tạp chí YHCĐ 67(CĐ5), accepted 28/04/2026). **This is the primary source of the "92,7%" figure that the earlier notes left unconfirmed.** Note that the setting is a private clinic, not a hospital.
  - Causes of refusal: "Chỉ định kỹ thuật sai quy định (92,7%); Sai hành chính và nhập liệu (6,2%); Kê thuốc sai chỉ định (1,1%)".
  - The authors recommend "tích hợp cảnh báo lỗi tự động về mã ICD, định mức kỹ thuật và danh mục thuốc". This implies the clinic's software lacked these warnings.
  - Interview quotes:
    - "chỉ định đúng chuyên môn nhưng sai ở phần ánh xạ danh mục, phần mềm không cập nhật kịp danh mục kỹ thuật mới nên bị loại" (PVS6)
    - "Hệ thống phần mềm quản lý … nhiều khi dẫn đến việc nhập sai các mã ICD hoặc là nhập thiếu … bị phần mềm Bảo hiểm xã hội tự động từ chối" (PVS5)
    - "Hệ thống HIS đôi khi bị treo, dẫn đến mất dữ liệu hoặc trùng hồ sơ khi nhập lại" (PVS1)
    - "Một số lỗi phần mềm phát sinh khi cơ quan BHXH nâng cấp cổng dữ liệu mà nhà cung cấp phần mềm … chưa kịp cập nhật" (PVS2)
    - Thuốc/VTYT refused because "phần mềm vẫn đang dùng dữ liệu cũ" for thầu and giá trần (PVS6)
  - The authors conclude that the HIS "vẫn là điểm nghẽn kỹ thuật". The paper lists "thiếu cảnh báo tự động" among IT error causes. Automatic deductions on administrative errors "không được phép giải trình", which causes "sự e dè của bác sỹ".
  - The paper does not name the HIS vendor.
  - Source: [Tạp chí YHCĐ](https://tapchiyhcd.vn/index.php/yhcd/article/download/5020/4587/5592)

### Inferences
- **INFERRED.** Doctors' pain is personal financial liability plus clinical ambiguity. That supports a doctor-facing tool that explains *why* an order is risky and offers a justification path, rather than just blocking.
- **INFERRED.** "Annoying warnings" (alert fatigue) was not documented in any Vietnamese public source I found. It remains a design risk, extrapolated from the international CDSS literature, but it is not evidenced here.

### Gaps
- I found no forum or Facebook posts about specific big-3 warning behaviour. Social platforms are not indexed by the search tool.
- No survey of doctor satisfaction with HIS order screens in Vietnam.

---

## 3. Do hospitals build their own add-ons or rules, and has any software warning measurably reduced xuất toán?

### Takeaway
Most hospital-level responses are **post-hoc**: tổ tiền kiểm, XML checkers (MDinsight, Nam Hân and SureCheck, all in the prior notes) and BHXH's own giám định rules engine. I found no public case of a hospital reporting a reduction in xuất toán from order-time BHYT warnings. The one measured before/after result for an order-time warning concerns drug interactions.

### Cited Findings
- **SNIPPET.** At Bệnh viện 198, contraindicated drug-interaction rates fell significantly after warnings were added to the prescribing software. The inpatient rate fell from 0,3404% to 0,0913%. This is a drug-safety warning, not a BHYT one. — [HUP article PDF](https://files.hup.edu.vn/Attachments/2023/5/Ba%CC%80i%20ba%CC%81o-%20Tu%CC%9Bo%CC%9Bng%20ta%CC%81c%20thuo%CC%82%CC%81c%20BV%20198.pdf)
- **SNIPPET.** BHXH Hà Nội's giám định system auto-checks claimed costs against rule sets based on legal regulations and flags anomalies. This happens after submission and on the payer side. — [nhadautu](https://nhadautu.vn/ha-noi-dung-he-thong-giam-dinh-dien-tu-ngan-chan-truc-loi-bhyt-d14384.html)
- **SNIPPET.** Nghị định 75/2023 is cited as the basis for BHXH to send early warnings to facilities. — [PLO](https://plo.vn/kiem-soat-chi-phi-kham-chua-benh-bhyt-bat-hop-ly-post794249.html)
- **SNIPPET.** A third-party HR vendor advertises HIS integration to warn when staff perform y lệnh outside their work schedule, to reduce xuất toán. This is a vendor claim with no data. — surfaced in search; [EasyHRM](https://easyhrm.vn/giai-phap-quan-ly-nhan-su-nganh-y-te/)
- **SNIPPET.** TP.HCM overspent its 2025 BHYT KCB budget by about 900 tỷ, and the city required facilities to build cost-control plans. — [daibieunhandan](https://daibieunhandan.vn/tp-ho-chi-minh-xac-thuc-du-lieu-kham-chua-benh-bhyt-de-tranh-that-thoat-10413528.html)
- **SNIPPET.** In 09/2026 Sở Y tế Hà Nội issued CV 9274/SYT-QLBHYTCNTT, asking facilities to review tiếp đón, kê đơn and cấp phát thuốc processes. — [Báo Pháp luật](https://doanhnhan.baophapluat.vn/ha-noi-ra-soat-chan-chinh-quy-trinh-de-bao-dam-quyen-loi-cho-nguoi-tham-gia-bhyt-f8ab648b.md)

### Inferences
- **INFERRED.** Payer-side automation (BHXH giám định rules, real-time sync under CV 4040) is tightening faster than provider-side order-time tooling. This widens the gap between "rule fires at BHXH" and "doctor knew at order time". That gap is the product's wedge.
- **INFERRED.** Cost pressure in TP.HCM and Hà Nội in 2025–2026 gives public hospitals a budget reason to buy order-time prevention. Their current spend goes to staff (tổ tiền kiểm) and post-hoc checkers.

### Gaps
- No public example of a hospital IT department scripting order-time BHYT rules into VNPT, Viettel or FPT, for example through stored procedures or custom popups. This is plausible but undocumented. Interviews are needed.
- No quantitative before/after xuất toán data tied to any order-time BHYT warning.
- Sources not reachable: the Bắc Giang SYT HIS feature-list PDFs ([2024 list](https://syt.bacgiang.gov.vn/documents/21459/20977109/1714697525727_danh+m%E1%BB%A5c+His+D%C5%A9ng+2024.pdf/c60cad35-6c38-4bd0-98a7-f35e21590c22), [2022 báo giá](https://syt.bacgiang.gov.vn/documents/21459/14278115/1655111211544_C%C3%B4ng+v%C4%83n+%C4%91%E1%BB%81+ngh%E1%BB%8B+b%C3%A1o+gi%C3%A1+%28PM+QLBV+2022%29.pdf/e4642d28-dedd-4424-b248-d40023dac680)) failed on a DNS error. They may contain vendor-specific feature claims.
