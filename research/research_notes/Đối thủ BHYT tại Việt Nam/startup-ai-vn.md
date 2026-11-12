# Vietnamese health-tech / AI startups and private-hospital initiatives touching BHYT or insurance claims

Research date: 2026-11-10. About 20 search and fetch calls. Labels: **[V]** means verified by fetching or reading the page. **[S]** means it comes from a search-result snippet or summary and the page was not fetched. **[I]** means my own inference.

## 1. Startups and AI products: what exists around claims checking, ICD coding, documentation and order-time decision support?

### Takeaway
I found **no Vietnamese product, startup or vendor that publicly offers order-time (at chỉ định) BHYT checking for doctors**. The products that do exist sit elsewhere:
- **(a) Post-hoc BHYT data review for hospital finance and IT teams:** MEDTECH's MDinsight.
- **(b) Private-insurance claims adjudication on the payer/TPA side:** Papaya, GreenNode IDP, MedCAT AI Insurance.
- **(c) Clinical imaging AI:** VinBrain DrAid, now owned by NVIDIA.
- **(d) Generic "AI frameworks" with no BHYT or ICD specifics:** FPT MediSight.

I found no Vietnamese LLM medical scribe or ICD auto-coding product with public deployment evidence.

### Cited Findings

**MEDTECH – MDinsight (BHYT payment data review, rules/BI, works after the encounter).** This is the closest existing BHYT-specific tool.
- The National Health Information Center (Trung tâm Thông tin y tế Quốc gia, official letter 419/TTTTYTQG) partnered with MEDTECH Software Technology JSC (Công ty CP Công nghệ phần mềm MEDTECH) to deploy software that "hỗ trợ rà soát dữ liệu thanh toán bảo hiểm" (helps review insurance payment data) — [S] [419 TTTTYTQG, posted on Đồng Nai DOH](https://syt.dongnai.gov.vn/Lists/Vn%20bn/Attachments/9430/419%20TTTTYTQG.pdf). The PDF returned 404 when I fetched it, so this comes only from the search snippet.
- It is deployed at more than 80 healthcare facilities nationwide. Each facility installs "MDinsight Adaptor", which syncs data automatically. "MDinsight BI" then standardizes the data against set criteria for statistics, reporting and risk management, and serves both facilities and provincial health departments (Sở Y tế) — [S] same source.
- The letter does not say whether it uses AI. It also gives no date, price or independent results — [S] same source.
- [I] Users are the hospital BHYT/finance office and Sở Y tế, not doctors. The step is after the encounter, before or after the claim is sent to the BHXH giám định portal. This is the most direct "competitor" in the BHYT space, but it does not overlap with a doctor-facing order-time tool.

**Papaya (HCMC insurtech; private health/life insurance claims, FWA).**
- It describes itself as an "AI-native platform for Health and Life insurers" for fraud, waste and abuse (FWA) and claims automation. It says it is live in Thailand, Vietnam and Hong Kong and that its claims product runs 17 AI agents — [S] [Papaya site](https://papaya-indol.vercel.app/), [About](https://papaya-indol.vercel.app/company). Caution: the domain is a vercel.app preview URL, so I could not confirm it is the official site.
- A sponsor post claims "20+ global insurers, 3x reduced leakage, 5x faster cycle times". These are vendor-reported figures — [S] [LinkedIn sponsor post](https://vn.linkedin.com/in/ibaohiem).
- Papaya started as a TPA running health-claims operations for insurers in Vietnam — [S] [LinkedIn](https://vn.linkedin.com/in/ibaohiem).
- Funding records conflict. CB Insights' last listed round is a business-plan competition in December 2020 — [S] [CB Insights](https://www.cbinsights.com/company/papaya/financials). PitchBook lists a 2023 later-stage VC deal and a 2024 accelerator deal. Listed investors include Google Accelerator, 500 Startups Vietnam, Ascend Vietnam Ventures (AVV) and Cento Ventures, with amounts undisclosed — [S] [PitchBook](https://pitchbook.com/profiles/company/327498-85).
- It covers **private insurance only**. I found nothing linking it to BHYT or to hospital-side direct billing (bảo lãnh viện phí).
- [I] Papaya is relevant as proof that LLM claims adjudication works in Vietnam on the payer side. Its rule logic (diagnosis–procedure–drug consistency) is the same family of checks a BHYT order assistant would run, but its users are insurers, not doctors.

**GreenNode IDP (VNG's AI cloud unit; claims document processing).**
- It classifies and extracts claim documents (BHYT card, prescription, discharge paper, lab results, VAT invoice), including handwritten Vietnamese. It cross-checks the documents against ICD codes and policy benefit rules, suggests a payout, flags forgery and routes each claim to auto-approval or manual review — [V] [GreenNode blog, 16 Jul 2026](https://greennode.ai/blog/tu-dong-hoa-boi-thuong-bao-hiem-suc-khoe-greennode-idp).
- At one unnamed TPA, claim time fell from about 30 minutes to under 5 minutes and document-handling labor fell 70–80%. Field-level accuracy is 99% for printed text and 94% for handwriting — [V] same source. These are vendor figures, and no clients are named.
- The page does not say whether it supports BHYT or private insurance. [I] It is almost certainly private insurance/TPA, since BHYT claims go to BHXH electronically as XML and not as scanned documents.

**MedCAT AI Insurance (AI4VN 2024 award entry).**
- It turns scanned medical records into structured data (MedCAT IDUS) and then checks claims. Its checks include whether the prescription fits the diagnosis and whether the diagnosis fits clinical and paraclinical data. It also calculates compensation. It claims productivity rises "at least 5 times" (tối thiểu 5 lần) — [V] [VnExpress AI4VN entry](https://vnexpress.net/medcat-ai-insurance-4776372.html).
- The page names no builder, insurer, deployment or scheme — [V] same source. [I] It is likely aimed at private insurance.

**VinBrain DrAid (Vingroup → NVIDIA; imaging AI, not claims).**
- NVIDIA acquired VinBrain in December 2024 for an undisclosed price. Vingroup had invested more than USD 126M and held 49.7% — [S] [Vietnam News](https://vietnamnews.vn/economy/1688629/nvidia-acquires-vingroup-s-ai-healthcare-solution-company.html), [The Investor](https://theinvestor.vn/nvidia-acquires-ai-unit-of-vietnamese-private-giant-vingroup-d13667.html).
- DrAid is used by "nearly 2,000 doctors at more than 100 hospitals" in Vietnam (date unclear) — [S] [SGGP](https://www.sggp.org.vn/vinbrain-cung-co-vi-the-tren-thi-truong-noi-dia-voi-nen-tang-draid-post759403.html). Another report says 182 hospitals across Vietnam, the US, India, Australia and other countries — [S] [Vietnam News](https://vietnamnews.vn/economy/1688629/nvidia-acquires-vingroup-s-ai-healthcare-solution-company.html).
- In September 2024 VinBrain signed agreements with Medlatec and Vikomed to deploy DrAid — [S] [Doanhnhanplus](https://doanhnhanplus.vn/vinbrain-hop-tac-medlatec-vikomed-trien-khai-draid-637139.html).
- Vinmec, the National Lung Hospital (Bệnh viện Phổi TƯ) and VinBrain signed an MoU on an "AI doctor assistant" (AI trợ lý bác sĩ) for diagnostic imaging — [S] [Vinmec topic page](https://www.vinmec.com/vie/chu-de/ai-tro-ly-bac-si).
- [I] It is not a competitor on BHYT or claims. It does show that Vinmec already has a precedent for AI-assistant MoUs.

**FPT (HIS vendor plus the MediSight AI framework).**
- FPT MediSight was launched in July 2026. It has three parts: Healthcare Insight Platform (HL7/FHIR/DICOM data), MediSight Crew (AI agents for administrative, clinical and compliance work) and MediSight Verse (apps, including "insurance claims management"). It names **no ICD coding, BHYT checks or hospital clients** — [V] [Tạp chí Công Thương, 17 Jul 2026](https://tapchicongthuong.vn/tap-doan-fpt-thuc-day-tang-toc-chuyen-doi-ai-trong-nganh-y-te-voi-medisight-534534.htm).
- Bạch Mai Hospital and FPT are partnering on a "smart hospital" and on AI platforms — [S] [FPT news](https://fpt.com/en/news/bach-mai-hospital-and-fpt-corporation-join-forces-to-build-a-smart-hospital-model-pioneering-the-future-of-medical-technology-in-vietnam).
- FPT.eHospital has modules for hospital-fee and BHYT payment management. I found no public description of a pre-order BHYT warning feature — [S] search summary, with [baodautu](https://baodautu.vn/dai-gia-vien-thong-dua-bao-san-dich-vu-cong-nghe-nganh-y-d25597.html) as context.
- [I] FPT, Viettel and VNPT HIS products very likely contain basic hard-coded BHYT validity checks, such as the catalog mapping required for XML export. I found no public documentation of these, so this is unverified.

**Viettel.**
- Viettel built the BHXH-side BHYT giám định system starting in 2014–2015, with rollout from 1 July 2015 — [S] [Baodautu](https://baodautu.vn/dai-gia-vien-thong-dua-bao-san-dich-vu-cong-nghe-nganh-y-d25597.html). This is payer-side infrastructure, not a doctor-facing tool.

**Jio Health / Docosan / eDoctor / Medpro.**
- Jio Health is a Series B company with about USD 27.7M raised; its last round was USD 20M, led by Heritas Capital. It runs a hybrid online/offline care model — [S] [CB Insights](https://www.cbinsights.com/investor/jio1), [Entrepreneur APAC](https://apac.entrepreneur.com/news-and-trends/jio-health-raises-20-million-in-series-b/421758).
- Medpro is a booking/patient portal. It publishes consumer articles on BHYT, such as "does Vinmec accept BHYT" — [S] [Medpro](https://medpro.vn/tin-tuc/benh-vien-vinmec-co-kham-bao-hiem-y-te-khong).
- I found no evidence that any of these four offer BHYT claims checking, ICD coding or order-time decision support.

**Saladin (insurtech).**
- Raised a Series A in December 2025 led by SBI Ven Capital, amount undisclosed. It focuses on **digital insurance distribution**, not claims — [S] [e27](https://e27.co/saladin-doubles-down-on-digital-insurance-with-series-a-raise-20251212/), [FinTech Global](https://fintech.global/2025/12/12/vietnams-saladin-secures-series-a-for-insurance-expansion/). Not relevant.

**ICD coding / documentation AI in Vietnam.**
- Vietnam has applied ICD-10 to medical records and BHYT payment since 2014. A 2024 study at Bưu Điện Hospital found ICD-10 coding still limited in detail and accuracy — [S] [Tạp chí Y học Cộng đồng](https://tapchiyhcd.vn/index.php/yhcd/article/download/2480/1783/2052).
- Hospital of University of Medicine and Pharmacy HCMC (BV ĐH Y Dược TP.HCM) won 2nd prize at the Vietnam Medical Achievements 2024 (Thành tựu Y khoa Việt Nam 2024) awards for **SNOMED CT** coding of EMR clinical data. This is SNOMED, not ICD, and it is unclear whether it uses AI — [S] same search summary (Vietcetera/tapchiyhcd).
- RMIT Vietnam (October 2026) argues LLMs should act as a "co-pilot" (cơ phó) for documentation. It warns about hallucination and the lack of quality Vietnamese medical datasets. This is opinion, not a deployment — [S] [RMIT](https://www.rmit.edu.vn/vi/tin-tuc/tat-ca-tin-tuc/2026/oct/de-ai-lo-giay-to-dieu-duong-lo-nguoi-benh).

### Inferences
- [I] The market splits by which step it serves and who uses it:
  - The payer side (BHXH, private insurers, TPAs) has the claims AI: Viettel giám định, Papaya, GreenNode, MedCAT.
  - The hospital back office has post-hoc BHYT data review: MDinsight.
  - Clinicians have imaging AI: DrAid.
  - Nobody publicly occupies "BHYT-aware decision support at the moment the doctor places an order". That gap is the open position for the Vinmec assistant.
- [I] Papaya and GreenNode are the most transferable technically: LLM rule checks of diagnosis ↔ service ↔ benefit consistency. They are possible partners or benchmarks, not direct competitors, because they serve private payers.

### Gaps
- I could not access MEDTECH/MDinsight's actual rule set, AI use, pricing or client list. The PDF returned 404, and no product site was found.
- I could not confirm Papaya's official domain, Vietnamese clients or recent funding.
- I found no public documentation of BHYT warning features inside the Viettel, VNPT, FPT or OneHealth HIS products. This needs vendor demos or interviews with hospital IT staff.
- No Vietnamese LLM ICD-coder or medical scribe with deployment evidence was found. Absence of evidence is not proof that none exists. Small vendors may not publish.

## 2. Private hospitals (Vinmec, Tâm Anh, Hồng Ngọc, Medlatec, Thu Cúc, FV, Hoàn Mỹ): any published BHYT order-time tool or process?

### Takeaway
No private hospital in Vietnam has published an order-time BHYT checking tool. Their published AI work is imaging and diagnostics (Tâm Anh, Medlatec/VinBrain). Vinmec accepts BHYT at several facilities, with per-facility contracts. Its HIS is Orion Health Enterprise (go-live 2015–2016). I found no public information on any internal Vinmec BHYT checker.

### Cited Findings
- **Vinmec, HIS:**
  - Vinmec chose Orion Health Enterprise in June 2015: initially for four sites, with six more planned, under the goal "One Vinmec – One patient – One Record" — [S] [PR Newswire Asia](https://enmobile.prnasia.com/releases/global/Vinmec_Hospital_Network_Partners_With_Orion_Health_To_Improve_Quality_Of_Healthcare_Services_In_Vietnam-125477.shtml), [Computerworld NZ](https://www2.computerworld.co.nz/article/578996/orion-health-expands-southeast-asia-presence-two-significant-vietnam-wins/).
  - Go-live at the second new hospital came on 28 April 2016 — [S] [BioSpectrum Asia](https://www.biospectrumasia.com/news/53/7913/orion-health-expands-into-asia-with-new-vietnam-contracts.html).
  - Amalga (formerly Microsoft, later Orion Health) also delivered HIS to Vinmec — [S] [Healthcare IT News](https://www.healthcareitnews.com/news/asia/vietnams-hospitals-early-stage-going-smart).
  - I found no 2024–2026 source on the current HIS or EMR.
- **Vinmec, BHYT acceptance:**
  - Vinmec accepts BHYT both in-route (đúng tuyến) and out-of-route (trái tuyến), at 100%, 95% or 80% depending on patient group. Out-of-route rates differ by facility level (basic vs specialized) under Thông tư 01/2025/TT-BYT. A transfer letter (giấy chuyển tuyến) is required if the card is not registered for initial care at Vinmec — [S] [Vinmec FAQ](https://www.vinmec.com/vi/huong-dan-khach-hang/bao-hiem/cac-cau-hoi-thuong-gap-ve-quyen-loi-bao-hiem-y-te-tai-vinmec), [Vinmec BHYT guide](https://vinmec.com/vi/huong-dan-khach-hang/bao-hiem/huong-dan-danh-cho-khach-hang-thanh-toan-khi-co-bao-hiem-y-te).
  - Vinmec Cần Thơ began BHYT in December 2025 — [S] [LSVN](https://lsvn.vn/vinmec-can-tho-chinh-thuc-ap-dung-kham-chua-benh-bao-hiem-y-te-a167203.html).
  - Vinmec Hạ Long has accepted BHYT since 2019, according to the search summary.
- **Tâm Anh:** Its published materials describe an "intelligence map" (bản đồ trí tuệ) linking tests, imaging, prescriptions and AI-assisted diagnosis, plus a 2025 innovation award for HIS/EMR and diagnostic AI. Nothing mentions BHYT claim checks — [S] [Tâm Anh news](https://tamanhhospital.vn/tin-tuc/ban-do-tri-tue-trong-hanh-trinh-kham-chua-benh-tai-he-thong-benh-vien-da-khoa-tam-anh/), [award page](https://tamanhhospital.vn/giai-thuong/doanh-nghiep-ung-dung-khoa-hoc-cong-nghe-va-doi-moi-sang-tao-tieu-bieu-nam-2025/). Tâm Anh also publishes about nationwide BHYT cross-route coverage (thông tuyến) — [S] [Tâm Anh](https://tamanhhospital.vn/tin-tuc/ap-dung-kham-chua-benh-co-bao-hiem-y-te-thong-tuyen-toan-quoc/).
- **Medlatec:** DrAid deployment with VinBrain (September 2024). Listed as an FPT SmartHealth partner — [S] [Doanhnhanplus](https://doanhnhanplus.vn/vinbrain-hop-tac-medlatec-vikomed-trien-khai-draid-637139.html), [FPT SmartHealth deck](https://syt.travinh.gov.vn/SiteFolders/syt/4923/2022/FPT_SmartHealth_Presentation_2020%20TraVinh%20-%201.2.pdf).
- **FV:** Orion Health customer — [S] [Orion Health FV case study](https://orionhealth.com/wp-content/uploads/Franco-Vietnamese-Hospital_A4_Web.pdf). It also publishes direct-billing (private insurance) arrangements — [S] [FV](https://www.fvhospital.com/?p=4311).
- **Hồng Ngọc, Thu Cúc, Hoàn Mỹ:** No relevant AI or BHYT-tool publications were found in my searches. Hoàn Mỹ appears only as an FPT SmartHealth partner — [S] [FPT SmartHealth deck](https://syt.travinh.gov.vn/SiteFolders/syt/4923/2022/FPT_SmartHealth_Presentation_2020%20TraVinh%20-%201.2.pdf).

### Inferences
- [I] Private hospitals compete on service and imaging AI. BHYT is a secondary revenue line for them, so internal BHYT tooling is probably back-office: a BHYT department reviewing XML before submission, possibly with tools like MDinsight. There is no public record of it.
- [I] Because Vinmec runs on Orion Health (a foreign HIS), any BHYT logic is likely custom middleware or done manually. This matters for how an order-time assistant would integrate. It needs confirmation inside Vinmec.

### Gaps
- I have no information on Vinmec's internal BHYT review process, its rejection (xuất toán) rates, or whether Orion Health has been replaced or upgraded since 2020.
- I found no conference talks or LinkedIn posts from private-hospital IT teams about BHYT tooling.

## 3. BHXH/BYT pilots of AI in BHYT giám định (2024–2026)

### Takeaway
BHXH has talked about "AI in giám định" since 2022, and it repeats this in 2025–2026 digital-transformation plans. As of late 2026, the public record shows **rule-based automated giám định plus early-warning analytics, not a named, deployed AI giám định system**.

### Cited Findings
- **September 2022:** BHXH's Center for BHYT Inspection and Multi-route Payment (Trung tâm Giám định BHYT và Thanh toán đa tuyến), led by Dương Tuấn Đức, said it was researching AI for giám định. The data base is about 15 billion records from more than 1 billion visits. Officials called the idea "feasible" but said it needs caution and a pilot. No vendor was named — [V] [VnBusiness, 21 Sep 2022](https://vnbusiness.vn/nghien-cuu-ung-dung-tri-tue-nhan-tao-trong-giam-dinh-bhyt.html).
- **August 2026:** BHXH is pushing further on "data analysis and artificial intelligence" (phân tích dữ liệu và trí tuệ nhân tạo) in BHYT management and giám định. "Early-warning systems" (hệ thống cảnh báo sớm) flag cost anomalies, and the number of provinces over budget fell from 28 to 13. Spending in the first six months was 84,765.8 billion VND (+11.1%), across 3,672 facilities and about 94.4 million visits. There is also a backlog of non-compliant claim files. The article names no specific AI system — [V] [VietnamPlus, 2 Aug 2026](https://www.vietnamplus.vn/siet-giam-dinh-kiem-soat-chat-chi-phi-kham-chua-benh-bao-hiem-y-te-post1127691.vnp).
- **Plan:** BHXH's plan implementing Resolutions NQ57 and NQ03 calls for researching and increasing the use of AI and big data for analysis and forecasting. This is general direction, not a giám định product — [S] [BHXH plan PDF](https://baohiemxahoi.gov.vn:4545/File_Server_BHXH/documents/Quyet%20dinh%20ban%20hanh%20kem%20theo%20KH_thuchienNQ57-NQ03_chuyendoiso_final.pdf).
- **December 2025:** The Ministry of Finance drafted rules for the data-intake portal (Cổng tiếp nhận dữ liệu) of the BHYT giám định information system. The system links to about 14,000 facilities (Nghị định 188/2025/NĐ-CP) — [S] [LSVN](https://lsvn.vn/de-xuat-quy-dinh-ve-cong-tiep-nhan-du-lieu-thuoc-he-thong-thong-tin-giam-dinh-bhyt-cua-bhxh-viet-nam-a166804.html).
- **Other BHXH work:** Fingerprint and chip-ID verification at BHYT visits — [S] [VnBusiness](https://vnbusiness.vn/het-canh-dung-the-giay-quet-van-tay-kham-benh-bhyt-mang-den-loi-ich-lon.html). An AI chatbot for policy Q&A — [S] [VnBusiness](https://vnbusiness.vn/nganh-bhxh-day-manh-chuyen-doi-so-tien-toi-thu-nghiem-cong-nghe-moi-blockchain-big-data-ai.html).
- **Regulatory caution:** The Ministry of Health says the legal framework for AI in health is still being completed, with privacy, liability and ethics open — [S] [VnEconomy](https://vneconomy.vn/bo-y-te-cam-ket-xay-dung-hanh-lang-phap-ly-minh-bach-cho-nen-tang-ai-y-te.htm).

### Inferences
- [I] The payer side is getting better at automated flagging (early warnings, standardized XML rules). That raises the cost of a hospital getting an order wrong, which strengthens the case for catching problems upstream at order time.
- [I] Any BHXH AI that is eventually rolled out will check claims after submission. It will not give doctors anything at order time, so it complements the Vinmec assistant rather than competing with it.

### Gaps
- I found no official 2024–2026 announcement of a named BHXH AI giám định pilot: no vendor, scope or results. The baohiemxahoi.gov.vn news pages appeared in results but were not fetched.
- The rule sets of the automated giám định engine (which checks reject which items) are not public in the sources I found.
