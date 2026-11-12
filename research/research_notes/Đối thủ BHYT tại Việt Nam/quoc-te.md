# International reference products: insurance coverage checks at order entry and before claim submission

Research date: 2026-11-10. Sources: about 18 searches and fetches. Much of the vendor outcome data is self-reported. Each such claim is flagged below.

## 1. Point-of-order coverage checks (Medicare NCD/LCD, ABN, EHR medical necessity checking, RCM vendors)

### Takeaway
In the US, the established pattern runs like this. The doctor orders a test with a diagnosis code. The EHR or a vendor rules engine checks the order against payer rules (Medicare NCD/LCD covered diagnosis lists, frequency, duplication). If the order fails, the doctor either picks a supported diagnosis or the patient signs an ABN, a liability waiver. The workflow is mature and mostly deterministic, driven by rule tables. Hard, independent outcome data is scarce, and most published numbers come from vendors.

### Cited Findings
- University of Florida (Jacksonville) Epic procedure: when a Medicare Part B service is ordered with a diagnosis that does not meet LCD criteria, Epic alerts the provider. The provider can view the LCD reference list of covered diagnoses, then either choose a supported diagnosis or print an ABN. The policy notes that the diagnosis may not be the only coverage requirement, and that a non-covered service should not be performed without a signed ABN. — [UF AMB-03-043](https://med.jax.ufl.edu/compliance/documents/AMB-03-043.pdf)
- Experian Health Passport Medical Necessity checks orders against payer rules for medical necessity, frequency, duplication and modifiers, and can prepare an ABN for e-signature. — [Experian brochure](https://www.experian.com/assets/healthcare/brochures/passport-medical-necessity.pdf)
- Craneware InSight Medical Necessity generates ABNs or waivers for non-covered services. It cites industry research that more than 40% of organizations estimate 10–15% of their denials come from medical necessity errors. This is a vendor-cited statistic. — [Craneware](https://thecranewaregroup.com/solutions/revenue/insight-medical-necessity)
- IMO Health argues for preventing medical necessity denials "at the source", meaning during order entry and documentation. — [IMO Health](https://www.imohealth.com/resources/improving-denials-management-at-the-source/)
- A MEDHOST vendor blog claims real-time medical necessity checks on lab and radiology orders reduce denials. It gives no numbers. — [MEDHOST](https://www.medhost.com/blog/streamlining-lab-radiology-orders-a-path-to-better-care-coordination-and-fewer-denials)
- An eOrder pilot had physician offices screen outpatient orders for medical necessity before sending them to the hospital. It "dramatically reduced" phone calls between offices and the hospital. No denial percentage is reported. — [Relias Media](https://reliasmedia.com/articles/85677-collaborative-spirit-marks-success-of-eorder-pilot)
- Epic's direction: real-time prior authorization and coverage requirement checks inside the EHR via Coverage Requirements Discovery (CRD) and Payer Platform. Four health systems (including Ochsner and Denver Health) went live with real-time prior auth checks in Epic. Full article was blocked (403), so no figures were retrieved. — [Fierce Healthcare](https://www.fiercehealthcare.com/health-tech/ochsner-summit-health-among-health-systems-launch-real-time-prior-authorization-checks); [Becker's – Epic 2026](https://www.beckershospitalreview.com/healthcare-information-technology/ehrs/what-epic-is-signaling-for-2026)
- St. Luke's and UnitedHealthcare automated claim status updates for 88% of claims exchanged through Epic Payer Platform. This covers claim status, not coverage checks, and the figure comes from Epic's Almanac. — [Becker's Payer](https://www.beckerspayer.com/?p=27573)
- CMS-0057-F (Interoperability and Prior Authorization Final Rule, January 2024) requires MA, Medicaid/CHIP and ACA-regulated commercial payers to provide FHIR APIs, including a Prior Authorization API, with most compliance dates starting January 1, 2027. Some operational requirements took effect in 2026. — [CMS fact sheet](https://www.cms.gov/newsroom/fact-sheets/cms-interoperability-and-prior-authorization-final-rule-cms-0057-f)

### Inferences
- The core of point-of-order checking is a lookup table: test/service × covered ICD codes (+ frequency, duplicates). It needs no AI. Vietnam's BHYT has equivalent material (lists of covered services, payment conditions, and the circulars on services and medical supplies). That makes a rule-table MVP feasible.
- The US workflow always ends in one of two actions: "fix the diagnosis code" or "patient signs a self-pay acknowledgement (ABN)". The Vietnamese equivalent would be: add the right ICD-10, or tell the patient the service is not BHYT-covered and they pay out of pocket.
- US systems show the payer rule (the LCD text) next to the alert. Showing the source text of the BHYT regulation builds trust.

### Gaps
- No peer-reviewed study was found that measures the reduction in medical necessity denials from order-entry checks in Epic or Cerner/Oracle Health. Existing case studies (Hennepin, Providence/bServed) were found only on anonymous paste sites (rentry.co, paste.rs) and were not used.
- No primary documentation was found for medical necessity products from Optum, Change Healthcare, Waystar, Availity, ZOTEC or Nuance/Microsoft. They are known to exist, but we have no figures.

## 2. Imaging appropriate use criteria / CDS (CMS AUC program) and alert fatigue

### Takeaway
The CMS AUC program, which required consulting CDS before ordering CT/MRI/PET for Medicare, was paused and its regulations rescinded effective January 1, 2024, after years of delay. The main reasons: CMS could not operationalize it, plus risks to data integrity and patient access. The evidence shows imaging CDS often fails to match orders to criteria, is overridden very often, and has only a small effect on ordering behaviour.

### Cited Findings
- CMS paused the AUC program and rescinded the regulations at 42 CFR 414.94 in the CY2024 PFS final rule. Claims no longer need to carry AUC consultation information. CMS cited risks to "data integrity and accuracy, beneficiary access, and potential beneficiary liability". The program remains in statute (PAMA) and has no restart date. — [CMS AUC Program](https://www.cms.gov/medicare/quality/appropriate-use-criteria-program); [ACC](https://www.acc.org/Latest-in-Cardiology/Articles/2023/12/14/15/16/CMS-Pauses-AUC-Program-For-Advanced-diagnostic-Imaging-Rescinds-Current-Regulations)
- The proposed rule stated that CMS had "exhausted all reasonable options" for operationalizing the program. AUC codes and modifiers ended December 31, 2024. ASNC asked Congress to formally repeal the mandate. — [AHRA](https://link.ahra.org/Article/cms-proposal-rescinds-appropriate-use-criteria-auc-regulations); [Cardiovascular Business](https://cardiovascularbusiness.com/topics/healthcare-management/healthcare-policy/asnc-asks-congress-officially-repeal-auc-mandate-advanced-medical-imaging)
- Medicare Imaging Demonstration (RAND evaluation, about 2015): the CDS tools could not assign appropriateness ratings to many orders, either because no criteria existed or because the tool could not match them. This limited effectiveness. There was no significant improvement in appropriate ordering and no effect on advanced imaging utilization. Physicians spent about 3 extra minutes on ordering. RAND recommended broader guideline coverage. The two sources give different sample sizes: 3,916 physicians / 139,757 orders versus 3,340 / 117,348. — [RAND RR706](https://www.rand.org/pubs/research_reports/RR706.html); [AuntMinnie](https://www.auntminnie.com/imaging-informatics/enterprise-imaging/is/article/15611281/rand-study-questions-whether-decision-support-really-works)
- Washington University ED (CareSelect, JACR, via a news summary): 17,355 imaging orders over 6 months. Alerts fired on about 3% of orders. Only about 0.1% of orders switched to the suggested alternative, which the authors called a "relatively marginal" effect. — [Radiology Business](https://radiologybusiness.com/node/245811)
- Repeat-CT alerts: about 95% were overridden. Requiring a clinical justification to override produced a 23% relative improvement and prevented about 1 in 13 repeat CT orders (AJR). — [AJR/typeset](https://typeset.io/pdf/journal-club-requiring-clinical-justification-to-override-pn5u4uwkvr.pdf)
- CT pulmonary angiography: the yield was 4.2% when CDS was overridden versus 11.2% when it was followed (Radiology 2016). — [Radiology](https://pubs.rsna.org/doi/10.1148/radiol.2016151985)
- Medication CDS: 52.6% of alerts were overridden (JAMIA, via Becker's). — [Becker's](https://www.beckershospitalreview.com/healthcare-information-technology/the-most-commonly-overridden-cds-alarms/)

### Inferences
- Lesson 1: if the rule set does not cover most orders, the system is mostly "no rating" noise. An MVP should pick a narrow scope (TC-03 Paediatrics, the most common tests and imaging) and cover it well rather than cover everything thinly.
- Lesson 2: alert only when the issue has direct consequences (BHYT will refuse to pay), not for "appropriateness" advice. The AUC program failed partly because it added steps without a clear reward or penalty for doctors.
- Lesson 3: a few targeted alerts, each with a specific fix (add ICD X), beat broad alerts. Low-value alerts get overridden 50–95% of the time.
- Lesson 4: the 3 minutes per order in the MID is a warning about burden. A Vietnamese assistant should add near-zero clicks when an order is valid.

### Gaps
- The original JACR CareSelect paper was not checked directly. The figures above come from a news summary.

## 3. Claim scrubbing / pre-submission edits (NCCI, MUE, frequency)

### Takeaway
The US uses public, deterministic edit tables (NCCI PTP, MUE, add-on) that CMS updates quarterly, and claim scrubbers apply them before submission. Industry surveys show denials are still rising, with the top cause being missing or inaccurate data rather than clinical judgement.

### Cited Findings
- NCCI has 3 edit types. PTP edits flag code pairs that should not be billed together, and a modifier can override some of them. MUEs set the maximum units of a service per patient per day. Add-on code edits are the third type. Edits are updated quarterly. Some MUE values are confidential. An MUE is not a usage guideline, and the payer can still review claims under the threshold. Commercial payers may apply them differently. — [CMS NCCI Policy Manual 2026 ch.1](https://www.cms.gov/files/document/01-chapter1-ncci-medicare-policy-manual-2026-final.pdf); [CMS MLN NCCI](https://www.cms.gov/outreach-and-education/mln/educational-tools/mln901346-how-to-use-the-medicare-ncci/ncci-medicare/chapter_1_introduction/)
- Experian Health State of Claims 2025 (250 respondents, June–July 2025): 41% report denial rates above 10%. 50% name missing or inaccurate data as the top cause (46% in 2024), 35% name authorizations, and 32% name registration errors. 54% say claim errors are rising. Some summaries disagree on the intake-error figure (68% versus about a quarter). — [Experian press release](https://www.experianplc.com/newsroom/press-releases/2025/experian-health-s-3rd-annual-state-of-claims-survey-finds-denial); [report PDF](https://www.experian.com/content/dam/noindex/na/us/healthcare/state-of-claims-2025.pdf)

### Inferences
- The NCCI pattern (code pairs that conflict, maximum frequency per day) maps directly onto BHYT rules (e.g., services that cannot be billed together, frequency limits per visit or treatment course). The cheapest MVP layer is a check on the data actually entered against these tables.
- Since most US denials come from data errors rather than clinical judgement, the Vietnamese MVP should check data completeness first (ICD present and matching, valid BHYT card, scope of benefits), and only then go further.

### Gaps
- No independent study was found measuring how much claim scrubbers raise the clean claim rate. Vendor figures were not cited because no primary source was available.

## 4. AI/LLM in prior authorization and coverage decisions, and controversies

### Takeaway
AI is widely used on the payer side (auto-approval, fast review), with self-reported auto-approval rates of 85–90%. It is highly controversial when used to deny claims, with major lawsuits against UnitedHealth, Cigna and Humana. CMS launched WISeR (AI-assisted prior auth for traditional Medicare, 2026–2031) and it faces strong opposition. The general principle that has emerged: AI may approve or assist, but a denial must be made by a human.

### Cited Findings
- Cohere Health: self-reports auto-approving 85% (some pages say up to 90%) of prior authorizations in real time, with the rest going to clinician review. It processes about 5.5 million requests per year (15 million members, 420,000 providers). It integrated with Epic Payer Platform in April 2024 so providers can submit requests from inside the EHR. No independent audit exists. — [Cohere decision](https://coherehealth.com/decision); [PR Newswire](https://prnewswire.com/news-releases/cohere-health-to-further-reduce-administrative-burden-for-providers-via-epics-payer-platform-302106162.html)
- An Epic executive said AI is "far from fixing prior authorization". — [Becker's](https://www.beckershospitalreview.com/digital-health/ai-far-from-fixing-prior-authorization-epic-exec-says/)
- CMS WISeR: runs January 1, 2026 to December 31, 2031, in 6 states (AZ, NJ, OH, OK, TX, WA), traditional Medicare only. It combines AI algorithms with clinician review and excludes emergencies and inpatient-only services. In April 2026 CMS delayed 2 service groups. On May 12, 2026 the GAO concluded WISeR is a "rule" under the APA, and congressional Democrats pushed for repeal. EFF filed a FOIA suit (March 2026) over the AI tools used. CMS says final decisions remain with clinicians. — [Georgetown CHIR](https://medicare.chir.georgetown.edu/?p=985); [Georgetown CHIR – WISeR concerns](https://medicare.chir.georgetown.edu/new-cms-wiser-model-revives-concerns-of-prior-authorization-and-artificial-intelligence/); [Healthcare Dive](https://www.healthcaredive.com/news/cmmi-prior-authorization-medicare-model/751985/)
- UnitedHealth/naviHealth nH Predict: class action filed November 2023 alleging the algorithm overrode physician judgement on post-acute care. Plaintiffs say about 90% of appealed denials were reversed by ALJs, and only 0.2% of denials were appealed (KFF). In February 2025 the court dismissed 5 of 7 counts and the case continues. Humana faces a similar suit. — [Healthcare Dive](https://www.healthcaredive.com/news/unitedhealth-algorithm-lawsuit-care-denials/699834/); [Fierce Healthcare](https://www.fiercehealthcare.com/payers/unitedhealthcare-hit-class-action-over-alleged-use-ai-deny-medicare-advantage-claims); [Healthcare Finance News](https://www.healthcarefinancenews.com/news/humana-sued-allegedly-using-ai-medicare-advantage-denials)
- Cigna PxDx: ProPublica reported more than 300,000 claims denied in 2 months of 2022, averaging 1.2 seconds per claim. Cigna says this was "simple sorting technology", not AI. — [Becker's Payer](https://www.beckerspayer.com/payer/home-page/unitedhealth-cigna-face-lawsuits-over-alleged-automated-claims-denials.html)

### Inferences
- For a doctor-facing tool (provider side, not payer side), the controversy risk is lower, but the same principle applies. An LLM should only explain and suggest, with citations to the regulation. The pass/fail BHYT decision should come from a deterministic rule table, and the doctor makes the final call.
- An LLM fits best for: (a) mapping free-text diagnoses to ICD-10, (b) explaining in plain language why a service would not be paid, (c) extracting rules from circulars into the rule table offline, with human review.

### Gaps
- No primary data was found on Infinitus or Rhyme (outcomes). No information was found on settlements or rulings after February 2025 in the nH Predict case.

## 5. Asian references (Korea HIRA, Taiwan NHI, Japan, Thailand)

### Takeaway
Korea and Taiwan have national real-time systems that warn doctors at the point of prescribing or ordering (DUR, PharmaCloud/MediCloud), but they focus mainly on drugs and duplication, not "will insurance pay for this test". BHYT-style payment checks in Asia mostly sit at the claims stage: HIRA's PARE/CRS layered screening, Japan's in-hospital receipt (レセプト) check software, and Thailand's NHSO pre-audit. Japan has a precedent for checking orders against registered diagnoses at the moment the doctor confirms an order.

### Cited Findings
- Korea DUR: online prospective DUR has run nationally since December 2010. It checks each prescription before dispensing and alerts doctors and pharmacists in real time (contraindications, duplicate active ingredients). 98.6% of institutions used it by March 2011. A systematic review found contraindicated drug use and drug costs fell. — [HIR 2016](https://synapse.koreamed.org/upload/synapsedata/pdfdata/1088hir/hir-22-39.pdf); [KoreaScience review](https://koreascience.kr/article/JAKO201913458199136.page)
- Korea HIRA claims review: two layers. PARE checks claim "syntax" (wrong codes, missing information), and CRS supports expert review of claims that pass PARE. A 2011 study found CRS detected multi-error claims at 23.1% (inpatient) and 2.9% (outpatient). — [PMC3483480](https://pmc.ncbi.nlm.nih.gov/articles/PMC3483480)
- HIRA September 2026: first use of AI imaging-reading results in claims review, starting with knee osteoarthritis. AI does not decide alone, final decisions rest with human reviewers, and complex cases go to a committee. — [Asia Economy](https://view.asiae.co.kr/en/article/2026090110305894717); [HIRA AI ADB 2024](https://events.development.asia/system/files/materials/2024/09/202409-ai-utilization-hira-health-insurance-review-assessment-service-experiences-and-challenges.pdf)
- Korea (hospital side, 2026): a preprint describes a hospital tool that screens diagnosis coding under the New DRG system, evaluating 17,138 targets across 15,388 episodes over 12 months. — [JMIR Preprints](https://preprints.jmir.org/preprint/108989)
- Taiwan NHI MediCloud: doctors can view imaging and CT results from other hospitals to avoid duplicate testing. NHIA projected about 1 billion points saved from duplicate tests in 2018–2020. This is a projection, not a measured result. PharmaCloud: 5.83% of prescriptions were flagged as possible duplicates, and 42.06% of those alerts led doctors to cancel the drug (JMIR Med Inform). — [TMU HPRC](https://tmuhprc.tmu.edu.tw/en/?p=7131); [Cardiovascular Business](https://cardiovascularbusiness.com/node/88106); [NHI Taiwan](https://www.nhi.gov.tw/en/cp-255-ae437-8-2.html)
- Japan: a 2001 UMIN paper describes an add-on module for order entry that checks drug orders against the patient's registered diagnoses at the moment the doctor confirms the order, warns, and logs every check. A municipal hospital tender (Higashiosaka 2023) requires a receipt-check tool to check: diagnosis present, primary diagnosis, procedure–diagnosis match, and test/drug–diagnosis match. Many vendors sell receipt checks (e.g., Medicom ASP, Reze AI cloud) to catch errors before submission, since that is cheaper than handling returned claims. — [UMIN](https://www.umin.ac.jp/renraku/h13/pdf8.pdf); [Higashiosaka spec](https://www.higashiosaka-mc.jp/bid_deals/img/20230222_02_specification_details2.pdf); [Gentosha GOLD Online](https://gentosha-go.com/articles/-/60414?page=2); [Medicom](https://www.phchd.com/jp/medicom/park/idea/management-asp)
- Thailand: hospitals must check data against NHSO standards before submission, with financial and non-financial penalties for errors. There is a pre-audit step in the e-claim workflow. In April 2026, BDI and NHSO built AI to support outpatient pre-audit. No figures were published. — [BMC HSR 2011](https://link.springer.com/content/pdf/10.1186/1472-6963-11-290.pdf); [MOPH Finance Data Hub](https://bdh.moph.go.th/site/wp-content/uploads/2023/08/2-3.3-finance-data-hub.pdf); [Thairath](https://en.thairath.co.th/news/governmentpolicy/2929196)

### Inferences
- Japan's "test/drug ↔ diagnosis" check (病名漏れ, missing diagnosis) is the closest model to Vietnam's BHYT payment-denial problem: a single payer, standard national lists, and the main error being an order without a matching diagnosis. A Vietnamese MVP can copy this logic and move it up from the claims stage to the order-entry stage.
- Korea's DUR shows that real-time checks at national scale are feasible and widely adopted when the payer mandates them. In Vietnam the payer (BHXH) does not offer an equivalent order-time API, so a hospital-side tool has to maintain its own rule table.

### Gaps
- No current official HIRA English documentation was found on point-of-order checks for tests and imaging (not drugs). Nothing was found on whether Taiwan or Korea warn doctors at order time that a test will not be paid.
- Thailand's NHSO pre-audit rule set and error codes were not found.

## 6. Measured outcomes (denials, time, alert fatigue, acceptance rates)

### Takeaway
Reliable outcome numbers are scarce. The independent figures are mostly about alert fatigue and the limited impact of CDS. Figures on denial reduction and auto-approval are mostly self-reported by vendors.

### Cited Findings
- Alert acceptance and override: imaging CDS at WashU shifted 0.1% of orders and fired on 3% of them. 95% of repeat-CT alerts were overridden, falling 23% relative when a justification was required. 52.6% of medication alerts were overridden. 42% of PharmaCloud duplicate alerts led to cancellation. — [Radiology Business](https://radiologybusiness.com/node/245811); [AJR](https://typeset.io/pdf/journal-club-requiring-clinical-justification-to-override-pn5u4uwkvr.pdf); [Becker's](https://www.beckershospitalreview.com/healthcare-information-technology/the-most-commonly-overridden-cds-alarms/); [Cardiovascular Business](https://cardiovascularbusiness.com/node/88106)
- Time burden: in the MID, ordering imaging through CDS added about 3 minutes. — [AuntMinnie](https://www.auntminnie.com/imaging-informatics/enterprise-imaging/is/article/15611281/rand-study-questions-whether-decision-support-really-works)
- Prior auth automation: Cohere self-reports 85–90% auto-approval. Epic/St. Luke's/UHC automated claim status for 88% of claims. — [Cohere](https://coherehealth.com/decision); [Becker's Payer](https://www.beckerspayer.com/?p=27573)
- Denials: 41% of US providers have denial rates above 10%, and data errors are the top cause (50%). — [Experian 2025](https://www.experianplc.com/newsroom/press-releases/2025/experian-health-s-3rd-annual-state-of-claims-survey-finds-denial)
- Medical necessity: more than 40% of organizations estimate 10–15% of denials come from medical necessity errors (vendor statistic). — [Craneware](https://thecranewaregroup.com/solutions/revenue/insight-medical-necessity)

### Inferences (lessons for a small MVP)
1. Use deterministic rules for the pass/fail result and the LLM only to explain and suggest, citing the source text (as US LCD alerts and HIRA's "AI does not decide alone" do).
2. Scope narrowly and cover it deeply (TC-03 Paediatrics, the top tests and imaging). Avoid the MID/AUC failure where most orders cannot be matched.
3. Each alert should carry a fix action: suggest the missing ICD-10, or flag that the service is not BHYT-covered so the patient can be told. This mirrors "supported dx / ABN".
4. Stay silent when the order is valid. Target a low alert rate and track the acceptance rate. The override benchmark in the literature is 50–95%, so an MVP should aim for acceptance clearly above that range.
5. Metrics to measure in the pilot: alert rate per order, acceptance/override rate, time added per order, and the BHXH rejection rate for tests and imaging before and after (department level).
6. Check data quality first (ICD, card, scope of benefits). That is the most common cause of denials according to US surveys and the PARE layer in Korea.

### Gaps
- No RCT or independent study was found that measures the reduction in payer denials from order-entry coverage checks (US or Asia). This is a real evidence gap. The MVP should design its own before/after measurement.
