# HIS/EMR vendors in Vietnam and their BHYT-checking features

Research date: 2026-11-10. Budget: about 25 tool calls. Public evidence for vendor-specific BHYT features is **thin**. Most vendors do not publish user manuals or feature-level detail, and many search hits were aggregator blogs. Each claim below is marked as VERIFIED (a source states it) or INFERRED.

---

## 1. Which vendors exist and how widely are they deployed?

### Takeaway
VNPT-HIS has by far the largest footprint, but its count is of "cơ sở y tế" (mostly commune and district facilities), not hospitals. Viettel and FPT come next. FPT.eHospital targets large hospitals (about 100). No authoritative market-share figure exists in public sources. Private chains (Vinmec, Tâm Anh) use other systems: Orion Health at Vinmec (2015 info), and Tâm Anh's vendor is not disclosed.

### Cited Findings
- **VNPT-HIS:** VNPT claims "7.500 cơ sở từ tuyến 1 cho đến tuyến 4" / "hơn 7.500 đơn vị". The article is dated 26/11/2020, so the figure is old. — [VNPT](https://vnpt.vn/gioi-thieu/tin-tuc/vnpt-his-phan-mem-quan-ly-toan-dien-cho-cac-benh-vien.html)
- **VNPT-HIS (other figure):** VNPT Vĩnh Long gives "hơn 6.920 cơ sở y tế" out of about 13.000 nationwide. The page is undated and the figure is probably older. — [VNPT Vĩnh Long](https://vinhlong.vnpt.vn/service/1557/2/vnpthis-phan-mem-quan-ly-va-kham-chua-benh)
- **VNPT-HIS hospital examples:** BV Nguyễn Trãi (TP.HCM, 800 giường) runs "VNPT-HIS level 02", and BV Bưu điện runs VNPT HIS + VNPT PACS. Both come from old news articles. — [SGGP](https://www.sggp.org.vn/so-hoa-benh-vien-va-nhung-ket-qua-an-tuong-post742083.html), [Báo Pháp luật](https://baophapluat.vn/vnpt-his-cung-cap-giai-phap-tong-the-cho-nganh-y-post276897.html)
- **VNPT mobile app:** VNPT publishes a user manual for a mobile VNPT-HIS app ("TL_HDSD_MobileAppHis", v1.0.0, hiệu lực 10/02/2025). It covers login, room setup and outpatient records. The excerpts found say nothing about BHYT warnings. — [VNPT storage PDF](https://storage-vnportal.vnpt.vn/gov-tha/7361/file-document/635878550.638802354440490723.pdf)
- **FPT.eHospital:** FPT IS says it is deployed at "gần 100 bệnh viện lớn và đầu ngành", both public and private (article dated 13/04/2024). A 2020 FPT deck said "hơn 30 bệnh viện lớn". — [FPT IS](https://fpt-is.com/goc-nhin-so/phan-mem-quan-ly-benh-vien/), [FPT SmartHealth deck, Trà Vinh](https://syt.travinh.gov.vn/SiteFolders/syt/4923/2022/FPT_SmartHealth_Presentation_2020%20TraVinh%20-%201.2.pdf)
- **Viettel HIS (scale):** Blog figures conflict: "hơn 11.000 cơ sở y tế" in one, "gần 300 bệnh viện" in another. Neither is a primary source. — summarised from aggregator results ([YouMed list](https://youmed.vn/tin-tuc/phan-mem-quan-ly-benh-vien/), [CloudGO](https://cloudgo.vn/phan-mem-quan-ly-benh-vien))
- **Viettel HIS in Khánh Hòa (2023):** A provincial report says "04 đơn vị đang thuê hệ thống HIS của Viettel; 11 đơn vị thuê HIS khác". — [Khánh Hòa Sở Y tế report](https://syt.khanhhoa.gov.vn/Resources/Docs/Nam%202023/Chuyen%20doi%20so/TCHC.BAOCAO.3494.STTTT.signed.signed%20(1).pdf)
- **Other vendors in an FPT IS "Top 10" list (2024):** HSOFT, Sao Việt, NANO Hospital, TCSOFT, Moss Hospital, N-HIS and EvoMed. The list gives no deployment numbers and no BHYT-specific features. — [FPT IS](https://fpt-is.com/goc-nhin-so/phan-mem-quan-ly-benh-vien/)
- **Vinmec:** In 2015 Vinmec contracted Orion Health (NZ) to deploy its enterprise system across the whole chain ("One Vinmec – One patient – One record"). — [Hải quan online](https://haiquanonline.com.vn/apicenter@/print_article&i=65513), [BioSpectrum Asia](https://www.biospectrumasia.com/index.php/article/pdf/7398)
- **Tâm Anh:** Tâm Anh is recognised by the Bộ Y tế for comprehensive EMR and accepts BHYT thông tuyến at its Q7 site. Its HIS vendor is not named. — [Tâm Anh](https://tamanhhospital.vn/tin-tuc/ap-dung-kham-chua-benh-co-bao-hiem-y-te-thong-tuyen-toan-quoc/)
- **National context:** About 1.210 of 1.650 hospitals had deployed EMR as of 2026. — from search summary citing [Vietnam News](https://vietnamnews.vn/society/1729858/hospitals-expand-electronic-records-as-viet-nam-pushes-toward-unified-digital-health-system.html) (not fetched directly)

### Inferences
- Public hospitals at tuyến tỉnh/huyện are dominated by VNPT and Viettel under rental (thuê dịch vụ) models. FPT and the in-house or Orion Health systems cover the large and private segment.
- Vinmec's Orion Health deployment is 2015-era information. The current state of the Vinmec HIS needs internal confirmation.

### Gaps
- I found no public data for ISOFH (iSofH), OneHealth/OneHIS, Vimes, Medisoft, Hồng Phát (HPSoft), Bravo/Mediplus, Vietsens or Vietinsoft: no deployment counts and no BHYT feature descriptions. The only ISOFH hit was a CafeF company tag ([cafef](https://cafef.vn/isofh.html)).
- I found no authoritative market-share study from the Bộ Y tế or an analyst.

---

## 2. BHYT features per vendor: (a) card check, (b) danh mục mapping, (c) rule checks at ordering, (d) pre-submission XML validation, (e) AI

### Takeaway
All vendors must, by regulation, support (a) card lookup via cổng BHXH, (b) danh mục dùng chung mapping and (d) XML 4210/130 export. These are table stakes under TT 54/2017 and QĐ 130, and vendor marketing barely mentions them. **For (c), real-time BHYT rule checks when the doctor orders, I found explicit public claims from only one small vendor (MyHospital).** I found none for VNPT, Viettel or FPT. AI features from the big vendors are generic (CDSS, chatbot, voice ordering) and none are BHYT-specific.

### Cited Findings
**Regulatory baseline (applies to every vendor)**
- At tiếp đón, the cơ sở KCB looks up card information on cổng BHXH, either via API or directly. — [BHXH VN, PL hướng dẫn](https://baohiemxahoi.gov.vn/content/tintuc/Lists/News/Attachments/26339/PL%20huong%20dan.pdf)
- The TT 54/2017 HIS criteria list mandatory groups that include viện phí, thanh toán BHYT and khám ngoại trú. Hospital self-assessments test whether the HIS can "xuất dữ liệu XML, báo cáo 19, 20, 21, 79, 80" for BHYT. — [Dự thảo bộ tiêu chí UDCNTT](https://files.lawnet.vn//uploads/attachfiles/2017/06/02/170621Duthao-BotieuchiUDCNTT.pdf); [BVĐK Quảng Ngãi self-assessment, 07/05/2025](https://bvdk.quangngai.gov.vn/getFile.aspx?ida=115)
- Hospitals are responsible for upgrading their HIS to meet the QĐ 130 output-data standard. Since 01/7/2024 the cổng giám định accepts only QĐ 130 XML (amended by QĐ 4750 and QĐ 3176), not QĐ 4210. — [QĐ 130 text](https://cntt.pnt.edu.vn/api/upload/20250605g3w130_QD-BYT_chuandinh_dang_du_lieu_dau_ra.doc); [MyHospital (vendor)](https://myhospital.vn/tin-tuc/xuat-file-xml-4210-giam-dinh-bhyt/)
- CV 4040/BYT-BH (06/2025) requires real-time sync of BHYT cost data and piloting of XML digital signatures. — [luatvietnam](https://static.luatvietnam.vn/xem-noi-dung-file-cong-van-4040-byt-bh-cua-bo-y-te-ve-viec-trien-khai-dong-bo-du-lieu-chi-phi-kham-chua-benh-bao-hiem-y-te-theo-thoi-gian-thuc-va-thi-diem-ky-so-du-lieu-xml-404052-d6/uploaded/vietlawfile/2025/6/4040_byt_bh_280625103953.pdf.aspx)

**VNPT-HIS**
- No BHYT-check features are described in VNPT's own product article (2020). Planned smart features were "Nhận dạng giọng nói hỗ trợ ra chỉ định" and "Chatbot thông minh", described as "sẽ tiếp tục được bổ sung", i.e. not yet built at that time. — [VNPT](https://vnpt.vn/gioi-thieu/tin-tuc/vnpt-his-phan-mem-quan-ly-toan-dien-cho-cac-benh-vien.html)

**Viettel HIS**
- The 2024 FPT IS list says only that Viettel HIS manages "bảo hiểm y tế, dữ liệu viện phí". It mentions no ordering-time checks. — [FPT IS](https://fpt-is.com/goc-nhin-so/phan-mem-quan-ly-benh-vien/)
- A 2025 paper by a Viettel Solutions author concludes that Vietnamese HIS have reached international standards on EMR, infrastructure and security, but "còn hạn chế trong triển khai AI, Big Data và tự động hóa". It lists e-Claim and BHYT payment among the mandatory components. — [Khổng Văn Đông, Tạp chí Y học Cộng đồng 66(CD15), 2025](https://tapchiyhcd.vn/index.php/yhcd/article/download/3311/3082/3479)

**FPT.eHospital**
- FPT markets eHospital as integrating "chữ ký số, bệnh án điện tử, BHXH/BHYT". Its AI claims are CDSS, a chatbot and "phân tích dữ liệu lớn/trí tuệ nhân tạo". It makes no BHYT-at-ordering claim. — [FPT IS](https://fpt-is.com/goc-nhin-so/phan-mem-quan-ly-benh-vien/)
- FPT's Mobile Check-in Station checks the BHYT card at reception. — [FPT Digital Healthcare Offer 1.7 (Trà Vinh)](https://syt.travinh.gov.vn/SiteFolders/syt/4923/2020/Digital-Healthcare-Offer_1.7.pdf)

**MyHospital (smaller HIS vendor). This is the only vendor found that explicitly claims ordering-time BHYT checks.**
- MyHospital claims "cảnh báo vượt trần và trùng chỉ định theo thời gian thực khi bác sĩ và thu ngân viện phí thao tác", "tự động kiểm tra mức hưởng theo nhóm đối tượng" and "cảnh báo sai mã danh mục ngay khi thao tác" (published 9/7/2026). — [MyHospital](https://myhospital.vn/tin-tuc/quy-trinh-giam-dinh-bhyt/)
- For CLS orders it describes "bộ quy tắc gắn chỉ định với mã ICD, phác đồ điều trị và định mức dịch vụ được cấu hình sẵn". A non-compliant order is blocked, or the doctor must add a justification. "Khi bác sĩ chuẩn bị lưu một chỉ định mới, HIS rà soát toàn bộ chỉ định và kết quả đã có trong cùng đợt điều trị". It also warns on orders that "vượt định mức số lượng" (published 19/7/2026). — [MyHospital](https://myhospital.vn/tin-tuc/xuat-toan-chi-dinh-can-lam-sang/)
- These are marketing claims. The articles give no deployment count and no independent validation.

**Third-party and add-on XML checkers (post-hoc, used by BHYT/viện phí staff, not doctors)**
- **MDinsight Adaptor (Đồng Nai):** The cơ sở installs an adaptor that syncs data to MDinsight BI for statistics and risk management. It reportedly gives "hơn 1.800 cảnh báo, báo lỗi liên quan đến nghiệp vụ y tế", including card errors ("thẻ không tồn tại / hết hạn"), and is deployed at "hơn 80 cơ sở KCB". The same document says checking electronic claims is otherwise "hoàn toàn thủ công". These details come from search-result snippets only: the PDF returned 404 when I fetched it, so treat them as unverified. — [Sở Y tế Đồng Nai 419/TTTTYTQG](https://syt.dongnai.gov.vn/Lists/Vn%20bn/Attachments/9430/419%20TTTTYTQG.pdf)
- **"Nam Hân" tool (TTYT Long Phú, Sóc Trăng, 2023):** Built by a 2-person team, it reviews exported XML. It checks card and admin data, mapping, order intervals, wrong DVKT, duplicate drugs and services, drug versus ICD, and order time versus the doctor's duty roster. It claims "100 hồ sơ/giây" against about 30 minutes per record manually. It is used at Long Phú and some other facilities and needs a cổng giám định account. — [VnExpress Sáng kiến KH 2023](https://vnexpress.net/khoa-hoc/cuoc-thi-sang-kien-khoa-hoc-2023/y-tuong/phan-mem-ho-tro-giam-dinh-xml-han-che-xuat-toan-bhyt-tai-co-so-kham-chua-benh-1085903608)
- **LQT SureCheck:** An online XML checker that claims to detect "83 loại lỗi" under the latest BYT/BHXH rules. This is a self-claim. — [checkxml.lqt.id.vn](https://checkxml.lqt.id.vn/)

### Inferences
- **Card validity check (a)** happens at reception, through the cổng BHXH API that every HIS must integrate. Its user is the receptionist, not the doctor.
- **Danh mục mapping (b) and XML 130 export (d)** are universal because the regulations force them. Pre-submission validation is commonly done by BHYT/viện phí staff, often with third-party tools (MDinsight, Nam Hân, SureCheck), and by the cổng giám định's own rejection feedback.
- **Ordering-time BHYT guidance for doctors (c)** is the clear gap. The big three (VNPT, Viettel, FPT) make no public claim, and their own author (Viettel, 2025) admits automation is limited. MyHospital's claim shows the idea is marketable, but there is no evidence it is deployed at scale.
- **(e) AI:** no vendor publicly claims AI or ML for BHYT coverage prediction. The only AI claims are generic (CDSS, chatbots, voice ordering).

### Gaps
- No public user manuals for VNPT, Viettel or FPT describing the order screen (màn hình chỉ định CLS). Hospital-specific configurations, such as a hospital adding duplicate-order warnings through its own vendor, may exist without being published.
- Could not verify the MDinsight figures (PDF 404).
- I did not search muasamcong tender specs, which could reveal required "cảnh báo khi chỉ định" features. That is worth a follow-up.
- Nothing found on Vinmec's in-house or Orion Health BHYT logic.

---

## 3. Who uses the BHYT feature and at which workflow step?

### Takeaway
Today, BHYT checking happens mostly **before** the doctor (card check at reception) and **after** the doctor (internal tiền kiểm and XML review by the giám định or viện phí team, then BHXH's own giám định). The doctor's ordering step is where xuất toán originates but where tooling is weakest.

### Cited Findings
- Hospitals set up a "Tổ giám sát chi phí BHYT" with a "tiền kiểm" unit that reviews records before data is sent to the cổng. This is a manual, staff-driven process. — from search summary of [BVĐK Gia Lai](https://benhviendakhoa.gialai.gov.vn/giai-phap-han-che-xuat-toan-bhyt-tai-co-so-kham-chua-benh/) and [vietbao](https://vietbao.vn/bhyt-khong-thanh-toan-hon-900-trieu-benh-vien-ly-giai-viec-yeu-cau-bac-si-boi-hoan-591630.html) (not fetched directly)
- In one provincial inspection, "Chỉ định kỹ thuật sai quy định" made up 92,7% of the xuất toán amount. — search summary of [BHXH VN Hệ thống giám định article](https://baohiemxahoi.gov.vn/tintuc/Pages/chuyen-doi-so.aspx?CateID=0&ItemID=8761) and related docs. The exact source document for 92,7% is not confirmed.
- Professional errors behind payment refusals often come from "chỉ định dịch vụ không phù hợp với chẩn đoán" or orders beyond the facility's chuyên môn scope (study of private clinics, Đắk Lắk). — [Tạp chí YHCĐ](https://tapchiyhcd.vn/index.php/yhcd/article/download/5020/4587/5592)
- BHXH's Hệ thống thông tin giám định BHYT issues warnings (for example repeated visits, high-error service themes) **to BHXH and provinces**, after the fact. — [lsvn](https://lsvn.vn/he-thong-thong-tin-giam-dinh-bhyt-cua-bhxh-viet-nam-lien-tuc-canh-bao-cac-truong-hop-di-kham-chua-benh-nhieu-lan-co-dau-hieu-truc-loi-quy-bhyt1616570678.html); [Báo Thanh tra](https://thanhtra.com.vn/hoan-thien-the-che-D4AD3DB96/siet-chat-quan-ly-quy-kham-chua-benh-bao-hiem-y-te-9CA24BC9.html)
- Some hospitals have made doctors repay (bồi hoàn) BHYT amounts that were refused. One case exceeded 900 million VND. — [vietbao](https://vietbao.vn/bhyt-khong-thanh-toan-hon-900-trieu-benh-vien-ly-giai-viec-yeu-cau-bac-si-boi-hoan-591630.html) (title only, not fetched)

### Inferences
- Users by step:
  - Tiếp đón (card lookup): receptionist.
  - Chỉ định: the doctor, who currently has little or no BHYT guidance in mainstream HIS.
  - Thu ngân: viện phí staff.
  - Tiền kiểm / XML: the BHYT/giám định team.
  - Post-submission: BHXH giám định viên.
- A doctor-facing, ordering-time BHYT assistant targets the step with the highest financial impact and the weakest tooling. MyHospital is the only identified vendor that explicitly markets into this space.

### Gaps
- No quantitative data on how many hospitals have any ordering-time BHYT warning.
- The 92,7% figure needs its primary document confirmed.
