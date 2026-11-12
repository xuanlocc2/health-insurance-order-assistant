# Regulatory, rule-content and data bottlenecks for an order-time BHYT coverage warning (Vietnam)

Research date: 2026-11-10. This builds on `../Đối thủ BHYT tại Việt Nam/bhxh-giam-dinh.md` (referred to below as "prior note") and does not repeat it.
Labels: **verified** means I read the page myself. **Snippet** means I saw only a search-result summary. **Inferred** means it is my own reasoning.

## 1. Is the payment-condition content machine-readable? How many services carry conditions? Is there an ICD-to-service mapping?

### Takeaway
The legal source is Thông tư 35/2016/TT-BYT, amended by TT 50/2017, TT 13/2020 and TT 39/2024. It is published only as legal text (PDF/DOC/web pages). Services with explicit conditions are a small minority. TT 39/2024 lists 8 services in Danh mục 1 (condition plus rate plus price) and 48 in Danh mục 2 (condition only). Those conditions are written in free-text clinical language, such as "Nghi ngờ có ổ nhiễm trùng, có ít nhất 02 trong 04 tiêu chuẩn", and they cite no ICD codes. I found no official ICD-10 ↔ DVKT mapping, which confirms earlier research. Any vendor would have to hand-encode the conditions and supply the clinical inputs (vital signs, prior results, diagnosis) itself.

### Cited Findings
- **TT 39/2024/TT-BYT, structure and dates (verified, caselaw page as rendered; the full original needs a login):**
  - Issued 17/11/2024, effective 01/01/2025. It amends TT 35/2016 and does not replace it.
  - Danh mục 1 has **8 DVKT** "có quy định cụ thể về điều kiện, tỷ lệ và mức giá thanh toán": lọc máu cấp cứu, tắm bỏng, CT 64–128 and ≥256 dãy, PET/CT, tumour markers, CRP and procalcitonin.
  - Danh mục 2 has **48 DVKT** "có quy định cụ thể điều kiện thanh toán": huyết động, lọc máu hấp phụ, video-EEG, PHCN, siêu âm tim, chụp/can thiệp mạch, gene-mutation tests, haematology tests and giải phẫu bệnh.
  - Each row has a "STT theo TT 35" column, so the lists are deltas against TT 35. Art. 2.2 repeals Mục 14 of DM1 and Mục 12, 37, 50 of DM2.
  - Source: [caselaw TT 39/2024](https://caselaw.vn/van-ban-phap-luat/413175-thong-tu-so-39-2024-tt-byt-ngay-17-11-2024-cua-bo-truong-bo-y-te-sua-doi-thong-tu-35-2016-tt-byt-ve-danh-muc-va-ty-le-dieu-kien-thanh-toan-doi-voi-dich-vu-ky-thuat-y-te-thuoc-pham-vi-duoc-huong-cua-nguoi-tham-gia-bao-hiem-y-te)
- **Example conditions, showing how hard each type is to encode (verified, same page):**
  - PET/CT: "Nốt mờ đơn độc ở phổi đường kính ≥ 8 mm". This needs an imaging finding.
  - CRP: "Nghi ngờ có ổ nhiễm trùng, có ít nhất 02 trong 04 tiêu chuẩn sau". This needs vital signs or lab values.
  - Procalcitonin: "Thanh toán tối đa 01 lần/mỗi 24 giờ đối với người bệnh sốc nhiễm trùng". This is a frequency rule plus a diagnosis.
  - CT 256 dãy: "nhịp tim trên 70 chu kỳ/phút". This needs a vital sign.
  - HbA1c: "tối thiểu sau mỗi 90 ± 3 ngày". This is a pure frequency rule and is encodable.
  - Tumour markers: "Chẩn đoán, theo dõi điều trị bệnh ung thư đối với một trong các xét nghiệm sau".
  - Polysomnography: "Để chẩn đoán hội chứng ngừng thở khi ngủ".
  - Art. 4d.6: ultrasound is paid at 55% of price above the maximum case count, which is a volume rule.
  - Source: [caselaw TT 39/2024](https://caselaw.vn/van-ban-phap-luat/413175-thong-tu-so-39-2024-tt-byt-ngay-17-11-2024-cua-bo-truong-bo-y-te-sua-doi-thong-tu-35-2016-tt-byt-ve-danh-muc-va-ty-le-dieu-kien-thanh-toan-doi-voi-dich-vu-ky-thuat-y-te-thuoc-pham-vi-duoc-huong-cua-nguoi-tham-gia-bao-hiem-y-te)
- **No ICD codes in TT 39 (verified):** the words "chẩn đoán" and "chỉ định" appear inside conditions but are not tied to a code table. — [caselaw TT 39/2024](https://caselaw.vn/van-ban-phap-luat/413175-thong-tu-so-39-2024-tt-byt-ngay-17-11-2024-cua-bo-truong-bo-y-te-sua-doi-thong-tu-35-2016-tt-byt-ve-danh-muc-va-ty-le-dieu-kien-thanh-toan-doi-voi-dich-vu-ky-thuat-y-te-thuoc-pham-vi-duoc-huong-cua-nguoi-tham-gia-bao-hiem-y-te)
- **TT 35/2016 itself (snippet):** effective 01/12/2016. It has a DM2 of conditioned services and a list of services "tạm thời chưa thanh toán". It is distributed as a .doc or PDF on vbpl.vn. — [vbpl TT 35 .doc](https://vbpl.vn/TW/Lists/vbpq/Attachments/115653/35_2016_TT-BYT_288918.doc); [hoatieu TT 35](https://hoatieu.vn/phap-luat/thong-tu-35-2016-tt-byt-danh-muc-va-ty-le-dieu-kien-thanh-toan-doi-voi-dich-vu-ky-thuat-y-te-nguoi-tham-gia-bao-hiem-116176)
- **Service codes vary by hospital (snippet):** price tables list the TT 23/2024 technique name together with a facility-assigned "mã tương đương" and the approved price name. Prices are set per facility or province, by BYT decisions per hospital or by HĐND resolutions. — e.g. [QĐ 3295/QĐ-BYT giá BV Phổi TW](https://caselaw.vn/van-ban-phap-luat/508599-quyet-dinh-so-3295-qd-byt-ngay-05-11-2024-cua-bo-truong-bo-y-te-ve-gia-dich-vu-kham-benh-chua-benh-ap-dung-tai-benh-vien-phoi-trung-uong); [BV Thủ Đức price table](https://benhvienthuduc.vn/wp-content/uploads/2025/03/BANG-GIA-CHENH-LECH-GIUA-GIA-THEO-YEU-CAU-VA-GIA-BHYT.pdf)
- **Shared code lists exist for identifiers, not for rules (snippet):**
  - QĐ 1227/QĐ-BYT (2025) issues "danh mục mã dùng chung đối với kỹ thuật, thuật ngữ, chỉ số cận lâm sàng". — [luatvietnam QĐ 1227 PDF](https://static.luatvietnam.vn/xem-noi-dung-file-quyet-dinh-1227-qd-byt-2025-danh-muc-ma-dung-chung-doi-voi-ky-thuat-thuat-ngu-chi-so-can-lam-sang-397987-d1/uploaded/vietlawfile/2025/4/1227_qd_byt_190425092353.pdf.aspx)
  - A 2016–2025 programme review counts "gần 100.000 mã danh mục dùng chung", including 2,964 lab-technique codes. — [SGGP](https://www.sggp.org.vn/lien-thong-ket-qua-xet-nghiem-xay-dung-he-thong-y-te-hien-dai-cong-bang-va-ben-vung-post815390.html)

### Inferences
- About 56 services in TT 39 carry explicit conditions, plus whatever TT 35's DM2 conditions remain unamended. Against a catalogue of thousands of DVKT, that is a small share. For most tests and imaging the only "rule" is general: approved for the facility, done per procedure, priced, and clinically appropriate. Inferred; I did not verify the total size of the TT 35 catalogue.
- Encodable today: frequency or interval rules (HbA1c 90±3 days, PCT 1 per 24 h), volume caps, facility-scope or list membership, and price. Not encodable without structured EMR inputs: CRP's "2 of 4 criteria", heart rate >70, nodule ≥8 mm. Not encodable at all: general "appropriateness". (Inferred.)
- Rule content is owned by MoH (Vụ BHYT) as legal text. Each vendor (VNPT, Viettel, FPT and others) has to transcribe it, so there is no canonical machine-readable source and transcription errors carry risk. (Inferred.)

### Gaps
- I could not verify the exact count of services in TT 35/2016's Danh mục 1 and Danh mục 2 as of 2026, or how many conditions remain after the TT 50/2017, TT 13/2020 and TT 39/2024 amendments. hoatieu returned 403 and caselaw needs a login.
- I could not confirm whether TT 35 will be replaced to align with the new TT 23/2024 technique list, whose Phụ lục 02 has applied since 01/07/2026.
- I found no official Excel, JSON or API release of the payment conditions.

## 2. Does BHXH publish its automatic giám định rules? Is there a pre-check or history API?

### Takeaway
No. BHXH has an internal "danh mục quy tắc giám định" (QĐ 1553/2017; see prior note) but I found no public copy. I also found no published hospital or vendor request asking for one. The only pre-submission feedback is the gateway's `thongDiep` error message (prior note). A "Kiểm tra lịch sử khám chữa bệnh" API function has existed since CV 366/BHXH-CNTT (31/01/2018), and BHXH says it gives facilities tools to view prior test and imaging history. But I found no evidence that this returns payability verdicts, or that it is widely used to block duplicate tests. A 2026 MoH draft circular on cross-facility recognition of more than 400 lab and imaging results with validity windows (for example urea 24 h, HbA1c 60 days) would create the first codified "repeat-test" rule set. It says nothing about any API.

### Cited Findings
- **History-check API (snippet):** a BHXH Đắk Lắk guide on card lookup by chip-ID references the function "Kiểm tra lịch sử khám chữa bệnh" defined in CV 366/BHXH-CNTT of 31/01/2018 and describes its input message. Facilities may query via API or directly on the BHXH portal. — [BHXH Đắk Lắk phụ lục](https://daklak.baohiemxahoi.gov.vn:4545/File_Server_BHXH/documents/39437_Phụ%20lục_hướng%20dẫn%20tra%20cứu%20thẻ%20BHYT%20bằng%20CCCD%20gắn%20chíp.pdf)
- **BHXH says the tools exist but duplicates persist (snippet; the page fetch failed with "socket hang up"):** BHXH cites a patient who received nearly 30 tests plus multiple imaging studies. It says duplicate ordering continues even though tools to look up KCB history have been provided. — [baohiemxahoi.gov.vn "Lạm dụng chỉ định kỹ thuật y tế"](https://baohiemxahoi.gov.vn/tintuc/pages/linh-vuc-bao-hiem-y-te.aspx?CateID=0&ItemID=9143)
- **Draft liên thông circular (verified, LSVN 14/09/2026):**
  - The MoH draft covers "danh mục dịch vụ cận lâm sàng và điều kiện sử dụng kết quả khi liên thông". It has more than 400 techniques in four groups: hoá sinh, huyết học–truyền máu, vi sinh–ký sinh trùng and CĐHA (X-quang, CT, MRI).
  - Each result has its own validity window, for example urea 24 h, uric acid 168 h and HbA1c 60 days.
  - The treating doctor keeps the right to re-order.
  - The article does not say BHYT will refuse repeats inside the window, and it describes no lookup system or API.
  - Source: [LSVN](https://lsvn.vn/du-kien-lien-thong-hon-400-xet-nghiem-dien-quang-giua-cac-co-so-kham-chua-benh-bao-hiem-y-te-a178162.html)
- **2017 predecessor (snippet):** QĐ 3148/QĐ-BYT (2017) set up a lab-result recognition list. Its roadmap aimed at nationwide liên thông by 2025. I found no source confirming that the target was met. — [SGGP](https://www.sggp.org.vn/lien-thong-ket-qua-xet-nghiem-xay-dung-he-thong-y-te-hien-dai-cong-bang-va-ben-vung-post815390.html); [BHXH list of hospitals and tests](https://baohiemxahoi.gov.vn/tintuc/Pages/chuyen-doi-so.aspx?CateID=0&ItemID=8882)
- **Hospital or vendor requests to publish the rules:** none found. Searches for "đề nghị BHXH công khai quy tắc giám định tự động" returned only general BHXH "công khai minh bạch" messaging. — [BHXH ItemID=9391](https://baohiemxahoi.gov.vn/tintuc/Pages/hoat-dong-tinh-thanh-pho.aspx?CateID=0&ItemID=9391)

### Inferences
- A vendor cannot replicate BHXH's automatic rules. The best it can do is reverse-engineer them from the hospital's historical rejection lists (Mẫu 82/06 minutes, explanation requests). Those lists are hospital-owned data, so a vendor needs per-hospital data-sharing agreements. (Inferred.)
- Duplicate-test detection is the most tractable rule family. Intra-hospital history is in the HIS. Cross-facility history is accessible in principle via the BHXH history API. The 2026 draft supplies official validity windows. (Inferred.)

### Gaps
- I could not confirm the current (2025–2026) response schema of the history API. In particular, I could not confirm whether it returns line-level DVKT codes and dates, or only visit-level summaries, or what its rate limits are.
- I could not confirm whether the liên thông circular has been finalised and issued.

## 3. How much xuất toán for tests and imaging is subjective?

### Takeaway
Much of it. About 83% of savings (2018–2022) came from human-led "chủ động" giám định, not automatic rules (prior note). Hospitals report that "inconsistent interpretation of rules between facilities and assessment agencies" causes many explanation requests. Doctors describe a double bind: order less and risk a missed diagnosis, order more and risk being judged "chỉ định rộng rãi". Rejections can be appealed or explained, which shows they are judgment calls. I found no court case or formal dispute statistics.

### Cited Findings
- **Ba Ria hospital (verified, VietNamNet 19/05/2026):**
  - The hospital had over 900 million VND rejected for Q4 2025 and recovered just over 100 million from staff. It absorbed the rest.
  - It cites inconsistent interpretation between facility and assessor as a cause of explanation requests and delays.
  - Staff quote: "A good doctor is the one with the fewest disallowed costs."
  - Source: [VietNamNet EN](https://vietnamnet.vn/en/doctors-face-new-stress-paying-bills-denied-by-health-insurers-2515230.html); [VietBao VN version](https://vietbao.vn/bhyt-khong-thanh-toan-hon-900-trieu-benh-vien-ly-giai-viec-yeu-cau-bac-si-boi-hoan-591630.html)
- **Đắk Lắk clinic study (snippet, consistent with prior note):** "chỉ định kỹ thuật sai quy định" made up 92.7% of the rejected amount. It covers unnecessary orders, orders outside professional scope, and orders not meeting BHYT standards. Xuất toán reports "chưa phải kết luận cuối cùng" and can be changed through giải trình. — [Tạp chí Y học Cộng đồng](https://tapchiyhcd.vn/index.php/yhcd/article/download/5020/4587/5592)
- **Imaging-duration dispute (prior note, verified there):** BHXH had to clarify in 02/2026 that the QĐ 2775/2776 CĐHA durations are reference values, not payment minimums. This shows rule-interpretation conflicts surface publicly. — [LSVN](https://lsvn.vn/bhxh-viet-nam-lam-ro-giam-dinh-thanh-toan-bhyt-voi-dich-vu-chan-doan-hinh-anh-a169164.html)

### Inferences
- An order-time warning can cover the objective layer: list, scope, frequency, duplicates, explicit TT 35/39 conditions, and data completeness. For the subjective "appropriate for this diagnosis" layer it can only offer probabilistic hints, learned from the hospital's own rejection history and MoH guidelines. Those hints should be presented as risk, not as verdicts. (Inferred.)

### Gaps
- No national statistics split objective from subjective rejections for tests and imaging.
- No formal dispute or court cases found. I found no published statistics on appeal (giải trình) success rates.

## 4. How often do the rules change (2023–2026)? What does that mean for maintenance?

### Takeaway
The change rate is high. I found at least 15 or more national instruments in 2023–2026 that touch the technique list, prices, payment conditions, the XML format or code lists. Facility-level price decisions and provincial HĐND resolutions come on top of that. A rule base would need roughly monthly legal monitoring plus a major refresh at least once a year.

### Cited Findings (the issuing documents; label per item)
| Year | Instrument | Effect | Source |
|---|---|---|---|
| 2023 | QĐ 130/QĐ-BYT (18/01/2023) | New XML output standard | [luatvietnam](https://luatvietnam.vn/y-te/quyet-dinh-130-qd-byt-241607-d1.html) (snippet) |
| 2023 | QĐ 4750/QĐ-BYT (29/12/2023) | Amends XML 130 | prior note (secondary) |
| 2023 | Thông tư 32/2023/TT-BYT | Guides the Luật KCB 2023, including medical-record forms | [TVPL](https://thuvienphapluat.vn/van-ban/The-thao-Y-te/Thong-tu-32-2023-TT-BYT-huong-dan-Luat-Kham-benh-chua-benh-593360.aspx) (snippet) |
| 2024 | TT 23/2024/TT-BYT (effective 18/10/2024) | New technique list. Phụ lục 01 applies to 30/6/2026; Phụ lục 02 applies from 01/7/2026 | snippet, search summary |
| 2024 | TT 21/2024/TT-BYT (17/10/2024) | Pricing methodology | [QĐ 4071 citing it](https://static.luatvietnam.vn/xem-noi-dung-file-quyet-dinh-4071-qd-byt-2024-gia-kham-chua-benh-ap-dung-tai-trung-tam-y-te-duong-bo-2-383158-d1/uploaded/vietlawfile/2025/1/4071_qd_byt_010125184740.pdf.aspx) (snippet) |
| 2024 | TT 37/2024/TT-BYT (16/11/2024) | Drug list (out of scope but same cadence) | [caselaw](https://caselaw.vn/van-ban-phap-luat/413126-thong-tu-so-37-2024-tt-byt-ngay-16-11-2024-cua-bo-truong-bo-y-te-quy-dinh-nguyen-tac-tieu-chi-xay-dung-cap-nhat-ghi-thong-tin-cau-truc-danh-muc-va-huong-dan-thanh-toan-doi-voi-thuoc-hoa-duoc-sinh-pham-thuoc-phong-xa-va-chat-danh-dau-thuoc-pham-vi-duoc-huong-cua-nguoi-tham-gia-bao-hiem-y-te) (snippet) |
| 2024 | TT 39/2024/TT-BYT (17/11/2024, effective 01/01/2025) | DVKT payment conditions | [caselaw](https://caselaw.vn/van-ban-phap-luat/413175-thong-tu-so-39-2024-tt-byt-ngay-17-11-2024-cua-bo-truong-bo-y-te-sua-doi-thong-tu-35-2016-tt-byt-ve-danh-muc-va-ty-le-dieu-kien-thanh-toan-doi-voi-dich-vu-ky-thuat-y-te-thuoc-pham-vi-duoc-huong-cua-nguoi-tham-gia-bao-hiem-y-te) (verified) |
| 2024 | QĐ 3176/QĐ-BYT | Amends XML 130 again | prior note |
| 2024–25 | Hundreds of per-hospital price decisions (e.g. QĐ 3295, 4071, 4096, 69, 311/QĐ-BYT) and provincial HĐND price resolutions | Prices | [example QĐ 311/2025](https://static.luatvietnam.vn/xem-noi-dung-file-quyet-dinh-311-qd-byt-2025-gia-kham-chua-benh-ap-dung-tai-benh-vien-truong-dai-hoc-y-duoc-hue-387244-d1/uploaded/vietlawfile/2025/2/311_qd_byt_030225171841.pdf.aspx) (snippet) |
| 2025 | NĐ 188/2025/NĐ-CP (01/7/2025) + CV 6872/BYT-BH | Implements the amended Luật BHYT | prior note |
| 2025 | QĐ 1227/QĐ-BYT | Shared codes for cận lâm sàng | [luatvietnam PDF](https://static.luatvietnam.vn/xem-noi-dung-file-quyet-dinh-1227-qd-byt-2025-danh-muc-ma-dung-chung-doi-voi-ky-thuat-thuat-ngu-chi-so-can-lam-sang-397987-d1/uploaded/vietlawfile/2025/4/1227_qd_byt_190425092353.pdf.aspx) (snippet) |
| 2025 | QĐ 2010/QĐ-BYT; CV 4040/BYT-BH | Shared code lists; real-time XML and digital signing | prior note |
| 2025 | QĐ 2775 and 2776/QĐ-BYT | CĐHA reference durations | prior note |
| 2026 | TT 12/2026/TT-BTC | Quyết toán forms. Facilities updating to it alongside QĐ 130 | [Quảng Ngãi tech doc](https://khanhcuong.quangngai.gov.vn/upload/2007018/20260408/Tài%20liệu%20kỹ%20thuật_TT12-2026-BTC.pdf) (snippet) |
| 2026 | CV 2046/BHXH-TTKS; CV 2738/BHXH-TTKS | Code-mapping fixes; tighter giám định | prior note |
| 2026 | TT 25/2026 | Replaces some TT 32/2023 forms | snippet in a search summary |
| 2026 | Draft circular on liên thông of 400+ lab and imaging results | Validity windows | [LSVN](https://lsvn.vn/du-kien-lien-thong-hon-400-xet-nghiem-dien-quang-giua-cac-co-so-kham-chua-benh-bao-hiem-y-te-a178162.html) (verified) |
| 2026 | Benefit changes from 01/7/2026 (e.g. 50% outpatient benefit at some facility categories) | Benefit level | snippet in a search summary |

- **Vendor fragility (prior note, verified there):** facility software breaks when BHXH upgrades the portal. — [Tạp chí Y học Cộng đồng](https://tapchiyhcd.vn/index.php/yhcd/article/download/5020/4587/5592)

### Inferences
- The 01/7/2026 technique-list switch (TT 23/2024 Phụ lục 02) means every facility's DVKT catalogue and code mapping changed mid-2026. A coverage-rule engine keyed to service codes must be re-mapped at each such switch. (Inferred.)
- The maintenance burden is per hospital, not national. The approved technique list, price list and mã tương đương differ by facility, so the rule engine needs per-site configuration. (Inferred.)

### Gaps
- I could not produce an exhaustive count. Board-level circulars and BHXH công văn are numerous, and many are only snippet-verified.

## 5. Liability: if software says "được chi trả" and BHXH rejects, who pays? Can software influence clinical orders?

### Takeaway
No regulation addresses software-caused xuất toán. In practice the facility bears the rejected cost: the head of the facility is accountable for ordering and payment, and some hospitals pass part of the cost on to individual doctors under internal rules. Vendor liability would rest only on contract. On influencing orders, the Luật Trí tuệ nhân tạo (Luật 134/2025/QH15, passed 10/12/2025) sets the principle that humans keep control and final responsibility. Draft-debate commentary says medical AI should be regulated like a medical device. Whether a coverage-warning tool counts as a medical device under NĐ 98/2021 is unresolved. A tool that warns about payment, rather than diagnosis or treatment, plausibly falls outside, but I could not verify this.

### Cited Findings
- **Facility head accountable (snippet):** "Người đứng đầu cơ sở khám, chữa bệnh chịu trách nhiệm trực tiếp trong việc tự kiểm tra, chấn chỉnh nội bộ về quy trình kê đơn, cấp phát thuốc, chỉ định dịch vụ và thanh toán chi phí BHYT". This comes from a Hà Nội directive article. — [Báo Pháp luật](https://doanhnhan.baophapluat.vn/ha-noi-ra-soat-chan-chinh-quy-trinh-de-bao-dam-quyen-loi-cho-nguoi-tham-gia-bhyt-f8ab648b.md)
- **Doctors paying back (verified):** Ba Ria hospital applies recovery only for repeated individual errors after training. It recovered about 100 of more than 900 million VND, and the article cites no specific legal basis. — [VietNamNet EN](https://vietnamnet.vn/en/doctors-face-new-stress-paying-bills-denied-by-health-insurers-2515230.html)
- **AI law (snippet):**
  - Luật Trí tuệ nhân tạo 2025 was promulgated 10/12/2025, with effect reported from around 03/2026.
  - The principle reported is that humans keep control of, and final responsibility for, decisions and consequences.
  - Press says final treatment decisions require physician oversight.
  - National Assembly deputies argued medical AI should be inspected like medical devices.
  - Sources: [Lệnh công bố, TVPL](https://thuvienphapluat.vn/van-ban/Cong-nghe-thong-tin/Lenh-cong-bo-Luat-Tri-tue-nhan-tao-2025-691385.aspx); [Cần Thơ PBGDPL summary](https://pbgdpl.cantho.gov.vn/mot-so-quy-dinh-cua-luat-tri-tue-nhan-tao-nam-2025); [Đại biểu Nhân dân](https://daibieunhandan.vn/du-thao-luat-tri-tue-nhan-tao-ai-trong-y-te-phai-duoc-kiem-dinh-nhu-thiet-bi-y-te-10397661.html); [Tiền Phong](https://tienphong.vn/ai-khong-thay-the-vai-tro-quyet-dinh-cua-bac-si-post1809166.html)
- **NĐ 98/2021 (snippet):** software is a medical device when its intended purpose is diagnosis, monitoring, treatment and similar. "Phần mềm sử dụng cho trang thiết bị y tế" is excluded from some procedures. Risk classification follows MoH rules. — [TVPL NĐ 98/2021 EN](https://thuvienphapluat.vn/van-ban/EN/The-thao-Y-te/Decree-98-2021-ND-CP-classification-of-medical-devices/495965/tieng-anh.aspx)
- **Practitioners are responsible for e-record entries (snippet; the source is an unverified Google Doc):** practitioners digitally sign and are responsible for the content entered into the electronic medical record (HSBA điện tử). — [Google Doc export](https://docs.google.com/document/d/1zA2bWk3TUIPrZ1Odx4xYhVP5_HIgaKvt/export?format=pdf)

### Inferences
- Liability chain in practice: BHXH rejects, the facility absorbs the cost, and the facility may pass it to the doctor under internal rules. The vendor is liable only by contract. A "được chi trả" assertion creates expectation risk. The safer design shows "không phát hiện vi phạm quy tắc đã biết" or risk levels, never a payability guarantee. (Inferred.)
- A tool that discourages a clinically needed test, because of a coverage warning, raises a patient-safety and ethics concern under the Luật KCB 2023 duty to treat according to professional standards. The warning should present alternatives, such as self-pay or documenting the indication, rather than blocking the order. (Inferred; I did not read the Luật KCB 2023 article text.)

### Gaps
- I did not read the full Luật KCB 2023 (15/2023/QH15) or the Luật AI 2025 article texts. Exact provisions on decision-support software are unverified.
- I found no MoH guidance classifying clinical or administrative decision-support software under NĐ 98/2021.
- I found no case of a vendor held liable for xuất toán.

## 6. Is an ICD required at order time?

### Takeaway
I found no national rule that the phiếu chỉ định cận lâm sàng must carry an ICD-10 code. The XML claim carries the ICD at visit level (main and secondary diagnoses), and each service line carries the order time (NGAY_YL). Facility procedures (SOPs) commonly put "chẩn đoán lâm sàng" (free text) on lab and imaging request slips. So at order time an ICD often does not exist yet, or exists only provisionally. BHXH judges appropriateness against the final visit diagnoses, which are coded later.

### Cited Findings
- **XML ordering time (snippet):** in QĐ 130, Bảng 3 (DVKT and VTYT detail) has NGAY_YL, "thời điểm ra y lệnh", in the format yyyymmddHHmm. In the predecessor QĐ 4210, the disease field held the main ICD-10 (or YHCT) code with secondary codes separated by ";". I did not confirm the exact current XML3 diagnosis fields under QĐ 130/4750. — [luatvietnam QĐ 130](https://luatvietnam.vn/y-te/quyet-dinh-130-qd-byt-241607-d1.html); [TVPL QĐ 4210 EN](https://thuvienphapluat.vn/van-ban/EN/Bao-hiem/Decision-4210-QD-BYT-2017-providing-for-output-data-standards-and-formats-used-in-management/368778/tieng-anh.aspx)
- **Facility SOP requires a diagnosis on the request slip (snippet):** BV Ninh Hòa's pre-analytical SOP has staff check on the phiếu chỉ định xét nghiệm the patient info, sending department, "chẩn đoán lâm sàng", the cận lâm sàng order and the treating doctor. — [BV Ninh Hòa QT 5.8.1](https://benhvienninhhoa.khanhhoa.gov.vn/Portals/0/Quy%20tr%C3%ACnh%20b%E1%BB%87nh%20vi%E1%BB%87n/XN-QTQL%205.8.1%20QUY%20TR%C3%8CNH%20TR%C6%AF%E1%BB%9AC%20XN.pdf)
- **Separate request and result forms in CĐHA processes referencing TT 32/2023 (snippet):** a hospital CĐHA/TDCN procedure lists "Phiếu chỉ định CĐHA/TDCN" and "Phiếu kết quả". — [VNPT-hosted hospital SOP](https://storage-vnportal.vnpt.vn/smeg2/2966/TAILIEU/signed-signed-01.%20qt_%20chan%20doan%20hinh%20anh-tham%20do%20chuc%20nang.docx.pdf)
- **Form regime (snippet):** TT 32/2023 Chương X Art. 51 governs medical-record forms. Some forms were replaced by TT 25/2026. TT 13/2025 on electronic records requires digital signing of result forms. — [TVPL TT 32/2023](https://thuvienphapluat.vn/van-ban/The-thao-Y-te/Thong-tu-32-2023-TT-BYT-huong-dan-Luat-Kham-benh-chua-benh-593360.aspx); [Lạng Sơn EMR guidance](https://soyt.langson.gov.vn/upload/105380/20250617/2025_06_06_CV_Huong_dan_EMR_signed_dc750.pdf)

### Inferences
- The ICD timing problem is structural. Rejections are judged against the claim's ICD set, but the order is placed before final coding. An order-time check must use the provisional or admission diagnosis and re-check at discharge or claim time, when coding staff may add the justifying ICD. That makes a two-stage design (order-time hint plus pre-submission re-check) necessary. (Inferred.)
- For outpatient Nhi visits, the doctor usually enters a working diagnosis with an ICD in the HIS before ordering, because many HIS systems force it. This is vendor practice, not law. (Inferred; not verified.)

### Gaps
- I did not read the actual TT 32/2023 or TT 25/2026 request-slip templates. Hoatieu returned 403 and the TVPL text was not fetched. I could not confirm whether the official template has a "Chẩn đoán" field or an ICD field.
- I did not get the exact QĐ 130/4750 XML3 field list for diagnosis per service line. The luatvietnam PDF rendered empty.
