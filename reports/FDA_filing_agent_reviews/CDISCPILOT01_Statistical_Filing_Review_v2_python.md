---
document_type: Statistical Review and Evaluation — Filing Review of an NDA/BLA
application: BLA 111111, Sequence 0002
study: CDISCPILOT01 (R Consortium R Submission Pilot 1)
applicant: R Consortium R Submission Working Group
product: Xanomeline Transdermal Therapeutic System (TTS)
date_of_submission: 2022-02-11
date_of_review: 2026-11-20
reviewer: Elsa (FDA AI Assistant — draft for human reviewer) AKA Claude Sonnet 4.5
status: DRAFT — requires independent verification and sign-off by qualified FDA statistical reviewer
methods_note: >
  Python (sklearn, scipy, pandas, numpy) used as a substitute for R execution
  to replicate pilot1wrappers::efficacy_models() from source code read in
  r0pkg.txt. See Appendix 1 for full code. All Python-derived results are
  reviewer-side verification aids only.
sources:
  - cover-letter.pdf (BLA 111111, m1/us/)
  - 356hes.pdf (Form FDA 356h)
  - adrg.pdf (Analysis Data Reviewer's Guide, v0.1.1)
  - response-to-fda-1.pdf (Sponsor response to FDA Statistical Review, 2022-02-02)
  - define.xml (ADaM data definitions, v2.0)
  - r0pkg.txt (pilot1wrappers v0.1.1 source, pkglite format)
  - tlf-primary.r, tlf-efficacy.r, tlf-kmplot.r, tlf-demographic.r
  - adsl.csv, adadas.csv, adae.csv, adtte.csv, adcibc.csv, adlbc.csv,
    adlbcpv.csv, adlbh.csv, adlbhpv.csv, adlbhy.csv, adnpix.csv, advs.csv
    (ADaM datasets, converted from .xpt for review)
  - NDA_BLA_StatisticsFilingTemplate_Sept2025.pdf (filing memo template)
  - mapp6025-4.r1_goodreviewpractice_refusetofile_10-23-25.pdf (MAPP 6025.4, Rev. 1)
  - README.md (Note that README.md was not submitted with the pilot1 submission.  However, because Elsa is unable to load pilot submissions from eCTD, the human reviewer allowed README.md into Elsa's review in order to obtain the folder structure of the submission.)
regulatory_basis:
  - MAPP 6025.4, Rev. 1 (effective 10/23/25), Appendices A, B, C
  - 21 CFR 314.50 and 601.2
  - FDA Study Data Technical Conformance Guide
  - ICH E9(R1)
  - Pinnacle 21 Enterprise v4.1.1 (as documented by sponsor in ADRG)
disclaimer: >
  This document is an AI-assisted draft. All findings, assessments, and
  regulatory determinations require independent verification and sign-off
  by a qualified FDA statistical reviewer before use. All regulatory
  judgments remain with the human reviewer. This draft does not constitute
  an official FDA filing determination.
---

# STATISTICAL REVIEW AND EVALUATION
## FILING REVIEW OF AN NDA/BLA

| | |
|---|---|
| **NDA/BLA #:** | BLA 111111 |
| **Supplement #:** | Sequence 0002 |
| **Related IND #:** | Not applicable (pilot submission; CDISC public dataset) |
| **Product Name:** | Xanomeline Transdermal Therapeutic System (TTS), 50 cm² (54 mg) and 75 cm² (81 mg) |
| **Indication(s):** | Safety and Efficacy in Patients with Mild to Moderate Alzheimer's Disease (pilot; no marketing claim proposed) |
| **Applicant:** | R Consortium R Submission Working Group |
| **Dates:** | Submitted: 02/11/2022 (Form 356h); Cover letter dated 11/11/2021; Response to FDA dated 02/02/2022 |
| **Review Priority:** | Not applicable (pilot submission) |
| **Biometrics Division:** | [To be completed by reviewer] |
| **Statistical Reviewer:** | AI-assisted draft — qualified human reviewer required |
| **Concurring Reviewers:** | [To be completed by reviewer] |
| **Medical Division:** | Not applicable (pilot submission) |
| **Clinical Team:** | Not applicable (pilot submission) |
| **Project Manager:** | [To be completed by reviewer] |

> **Methods note:** Where R code could not be executed directly, Python (sklearn, scipy, pandas, numpy) was used as a substitute to replicate submitted R analyses by reading source code from `r0pkg.txt`. See **Appendix 1** for the full Python verification code. All Python-derived results are reviewer-side verification aids; human technical review is required before reliance on any finding.

---

## 1. Summary of Efficacy/Safety Clinical Trials to be Reviewed

*This pilot submission does not constitute a marketing application and proposes no labeling claim. No SPA was conducted. The sole study (CDISCPILOT01) uses the publicly available CDISC/PHUSE pilot dataset. The submission covers 4 analysis outputs only; no ISE, ISS, CSR, protocol, or SAP was submitted. All clinical trials are listed below; none are excluded from review.*

**Table 1: Summary of Trials to be Assessed in the Statistical Review**

| Trial ID | Design* | Treatment/Sample Size | Endpoint/Analysis | Preliminary Findings |
|---|---|---|---|---|
| CDISCPILOT01 | MC, R, DB, PG, PC (26 wks) | Placebo/N=86; Xanomeline Low Dose (54 mg)/N=84; Xanomeline High Dose (81 mg)/N=84; Total N=254 | **Primary:** ADAS-Cog (11) change from baseline to Week 24, LOCF, ANCOVA (CHG ~ TRTPN + SITEGR1 + BASE for dose-response; CHG ~ TRTPCD_F + SITEGR1 + BASE for pairwise LS means; contr.sum/Type III SS; emmeans proportional weights; no multiplicity adjustment). Dataset: ADADAS, PARAMCD=ACTOT, EFFFL=Y & ITTFL=Y & ANL01FL=Y, N=234 subjects, 0 missing CHG confirmed. **Safety:** KM plot, time to first dermatologic event (ADTTE, PARAMCD=TTDE, Safety pop N=254; events=152, censored=102). **Supportive:** ANCOVA, glucose change at Week 20 (ADLBC, PARAMCD=GLUC, Placebo vs. High Dose only). **Demographics:** Table 14-2.01, ITT population. | FDA staff successfully reproduced all 4 outputs. Three issues in initial submission: (1) missing ANCOVA model specification for Table 14-3.02 — updated in seq. 0002; (2) rounding/quantile difference in Table 14-3.01 — not resolved by sponsor; (3) column header error in Table 14-3.01 — corrected in seq. 0002. Python replication of primary ANCOVA (see Appendix 1; sklearn OLS, N=234) yielded: LS Mean Placebo=2.495, Low=2.028, High=1.489; Diff High−Placebo=−1.006, Low−Placebo=−0.467; TRTPN partial-F p=0.245; RMSE=5.002. Human reviewer should compare against submitted Table 14-3.01. |

*\* MC: multi-center, R: randomized, DB: double-blind, PG: parallel group, PC: placebo controlled*

---

## 2. Assessment of Protocols and Study Reports

**Table 2: Summary of Information Based Upon Review of the Protocol(s) and the Study Report(s)**

| Content Parameter | Response/Comments |
|---|---|
| **Designs utilized are appropriate for the indications requested.** | The study is described as a prospective, randomized, multi-center, double-blind, placebo-controlled, parallel-group trial with 26 weeks follow-up and 3 arms (Placebo, Low Dose, High Dose), with equal randomization; N=254 confirmed from ADSL dataset (Placebo=86, Low=84, High=84) (Source: adrg.pdf, p. 3, Section 2.2). No indication is proposed and no protocol or CSR was submitted; accordingly, assessment of design appropriateness for a proposed indication cannot be performed from available documents. **[FLAG: Human reviewer must assess design appropriateness. No protocol submitted.]** |
| **Endpoints and methods of analysis are specified in the protocols/statistical analysis plans.** | No protocol or SAP submitted. Endpoint and analysis specification relies on ADRG Sections 7.3 and 7.6 (adrg.pdf, pp. 9, 12–13) and the submitted program code. Primary endpoint: "ADAS Cog (11) - Change from Baseline to Week 24 - LOCF" (adrg.pdf, p. 9). The full model specification was verified by reading the `pilot1wrappers` package source code directly from `r0pkg.txt` (R/eff_models.R) and confirmed via Python replication (see Appendix 1): **Model 1 (dose-response):** `lm(CHG ~ TRTPN + SITEGR1 + BASE)` — TRTPN continuous, SITEGR1 categorical (11 pooled site groups, confirmed present in ADADAS), BASE continuous. **Model 2 (pairwise):** `lm(CHG ~ TRTPCD_F + SITEGR1 + BASE)` — TRTPCD_F as categorical with levels Xan_Hi/Xan_Lo/Pbo. **Contrasts:** `contr.sum/contr.poly` (Type III SS), confirmed from source: *"Need to set contrasts to work for Type III SS."* **TRTPN mapping:** 0=Pbo, 54=Xan_Lo, 81=Xan_Hi (confirmed from `case_when` in source). **Pairwise LS means:** `emmeans::lsmeans` with `weights='proportional'`, `adjust=NULL` (no multiplicity adjustment), confirmed from source. Dataset query confirms primary analysis population: N=234 subjects, zero missing CHG values. ANCOVA model specification for Table 14-3.02 was flagged as missing by FDA in initial submission (Agency Comment 1); updated in sequence 0002. **[FLAG: Absence of a pre-specified SAP is a significant limitation; specification sourced from ADRG and program code only. Human reviewer must assess adequacy and compare Python-replicated results (Appendix 1) against submitted Table 14-3.01.]** |
| **Interim analyses (if present) were pre-specified in the protocol with appropriate associated analyses. DSMB meeting minutes and data are available.** | N/A. No interim analyses described or referenced in any submitted document. No DSMB referenced. ADRG Section 3.4 states "Not applicable" for imputation/derivation methods; no interim analysis language found anywhere in submitted materials (Source: adrg.pdf, p. 4). |
| **Appropriate details and/or references for novel statistical methodology (if present) are included (e.g., codes for simulations).** | The novel methodology is the use of R-language for a regulatory submission. All 4 analysis programs are submitted (tlf-primary.r, tlf-efficacy.r, tlf-kmplot.r, tlf-demographic.r). The full source code of the proprietary `pilot1wrappers` package (v0.1.1) was read directly from `r0pkg.txt` in pkglite plain-text format — no unpacking required. All 8 exported functions are accounted for and documented with roxygen2-style documentation: `efficacy_models()`, `fmt_ci()`, `fmt_est()`, `fmt_num()`, `fmt_pval()`, `nest_rowlabels()`, `num_fmt()`, `pad_row()`. The DESCRIPTION file confirms version 0.1.1, R ≥ 3.6.0, GPL-3 license, and all package imports. The core analytical function `efficacy_models()` was replicated in Python (see Appendix 1); results are directionally consistent with a xanomeline dose-response signal. Open-source package names and versions listed in ADRG Sections 7.4–7.5 (adrg.pdf, pp. 10–11). Software validation evidence explicitly excluded from pilot scope per cover letter (p. 1). **[FLAG: Formal software validation is out of scope for this pilot per the cover letter. Human reviewer must assess whether the level of documentation is adequate for the pilot's stated objectives.]** |
| **Investigation of effect of missing data and discontinued follow-up on statistical analyses appears to be adequate.** | LOCF imputation is applied for the primary endpoint (Table 14-3.01 title). Dataset query and Python replication (Appendix 1) confirm zero missing CHG values in the primary analysis population (N=234, ACTOT, AVISITN=24, EFFFL=Y, ITTFL=Y, ANL01FL=Y). EFFFL=N subjects (N=20 of 254, 7.9%) are excluded from the primary efficacy analysis; their treatment group distribution and reasons for exclusion are not characterized in the ADRG. ADRG Section 3.4: "Not applicable" for imputation methods. No sensitivity analysis or formal missing data assessment submitted. **[FLAG: No sensitivity analyses submitted. Characterization of the N=20 EFFFL=N subjects not provided. No protocol or SAP to assess pre-specification of missing data handling. Human reviewer must assess adequacy.]** |

---

## 3. Electronic Data Assessment

**Table 3: Information Regarding the Data**

| Content Parameter | Response/Comments |
|---|---|
| **Dataset location** | Documented in ADRG Section 8 and Appendix (adrg.pdf, pp. 12–14). eCTD path: `m5/datasets/rconsortiumpilot1/analysis/adam/datasets/` (subfolder name `rconsortiumpilot1` confirmed from README.md folder structure). Reviewer path template: `path$adam = "path/to/esub/analysis/adam/datasets"` (ADRG Appendix). define.xml present (537 KB, v2.0). Human reviewer should confirm this path resolves correctly in the eCTD viewer. |
| **Were analysis datasets provided?** | Yes. All 12 ADaM datasets listed in ADRG Section 5.2 confirmed present and accessible from dataset inspection: ADSL (254×49), ADADAS (12,463×40), ADAE (1,191×55), ADTTE (254×26), ADCIBC (730×36), ADLBC (37,132×46), ADLBCPV (37,132×46), ADLBH (24,966×46), ADLBHPV (24,966×46), ADLBHY (9,954×43), ADNPIX (31,140×41), ADVS (32,139×35). STUDYID="CDISCPILOT01" consistent across all 12 datasets. USUBJID unique in ADSL (254 subjects = 254 rows). |
| **Dataset structure (e.g., SDTM or ADaM)** | ADaM. Standard: ADaM v2.1/ADaM IG v1.0 per ADRG Section 1.2 (adrg.pdf, p. 2). Define.xml v2.0 present. SDTM datasets not submitted in this pilot (source data publicly available via PHUSE GitHub). Dataset inspection confirms presence of required ADaM core variables across all datasets. SITEGR1 confirmed present directly in ADADAS (confirmed during Python replication, Appendix 1 — no merge from ADSL required). Three Pinnacle 21 Enterprise v4.1.1 conformance issues documented in ADRG Section 6.2 (adrg.pdf, pp. 7–8): AD0258 (ADAE traceability — derived records), AD0018 (ANL01FL label mismatch — independently confirmed from label file inspection: ADADAS/ADCIBC use "Analysis Record Flag 01"; ADLBC/ADLBCPV/ADLBH/ADLBHPV/ADVS/ADNPIX use "Analysis Flag 01"), AD0320 (non-standard ADSL dataset label). |
| **Are the define files sufficiently detailed?** | Define.xml (v2.0, 537 KB) is present. Inspection confirms: all 12 dataset names present with ItemGroupDef structures, variable labels, parameter codes (ACTOT, TTDE confirmed), population flags (EFFFL, ITTFL, SAFFL, ANL01FL), dataset purpose and structure descriptions. Three Pinnacle 21 "Error"-level findings as noted above; sponsor explanations provided for each. **[FLAG: Whether define.xml is sufficiently detailed is a human judgment; reviewer confirms presence and content of key elements only. Adequacy of Pinnacle 21 findings explanations requires human assessment.]** |
| **List the dataset(s) that contains the primary endpoint(s)** | **ADADAS** (ADAS-Cog Analysis). Primary endpoint variable: CHG (Change from Baseline). Filter: PARAMCD="ACTOT", AVISITN=24, EFFFL=Y, ITTFL=Y, ANL01FL=Y. Dataset confirmed present (12,463 records; 1,040 ACTOT records). Primary analysis population: N=234 subjects (Placebo=79, Low=81, High=74), zero missing CHG values. SITEGR1 confirmed present directly in ADADAS (11 pooled site groups, values: 701, 703, 704, 705, 708, 709, 710, 713, 716, 718, 900). Source: ADRG Section 5.2.6 (adrg.pdf, p. 8): "ADADAS contains analysis data from the ADAS-Cog questionnaire, one of the primary efficacy endpoints." |
| **Are the *analysis datasets* sufficiently structured and defined to permit analysis of the primary endpoint(s) without excess data manipulation?** | Yes. All variables required for the primary ANCOVA — PARAMCD, AVISITN, EFFFL, ITTFL, ANL01FL, CHG, BASE, TRTP, TRTPN, SITEGR1, USUBJID — are present directly in ADADAS without derivation or external merge. ADSL USUBJID is unique. Python replication of the full `efficacy_models()` function (Appendix 1; sklearn OLS, N=234) executed without data manipulation issues, confirming the dataset is structured to support the analysis as specified. **[FLAG: Human technical review of original .xpt files required to confirm data value correctness and full ADaM conformance beyond variable presence.]** |
| **Are there any initial concerns about site(s) that could lead to inspection? If so, list the site(s) that you request to be inspected and the rationale.** | No. This submission uses the publicly available CDISC/PHUSE pilot dataset; traditional site inspection concerns are not applicable. SITEGR1 confirmed present in ADADAS with 11 pooled site groups (values: 701, 703, 704, 705, 708, 709, 710, 713, 716, 718, 900). No site-level data quality issues identifiable from dataset inspection. **[FLAG: Human reviewer must make final determination on site inspection need.]** |
| **Safety data are organized to permit analyses across clinical trials in the NDA/BLA.** | N/A. Single-study pilot submission; cross-trial safety integration is not applicable. Safety datasets present and accessible: ADAE (1,191 records, 225 subjects with ≥1 AE; Placebo=301, Low=435, High=455 AE records), ADTTE (254 records, PARAMCD=TTDE only, CNSR: 0=event/152, 1=censored/102, all SAFFL=Y), ADLBC, ADLBCPV, ADLBH, ADLBHPV, ADLBHY, ADVS. No ISS submitted. |

---

## 4. Filing Issues

**Table 4: Initial Overview of the NDA/BLA for Refuse-to-file (RTF):**

| Content Parameter | Yes | No | NA | Comments |
|---|---|---|---|---|
| **Index is sufficient to locate necessary reports, tables, data, etc.** | ☑ | | | eCTD folder structure confirmed. us-regional.xml present. ADRG Section 8 provides directory map (adrg.pdf, pp. 12–14). Program-to-output traceability table in ADRG Section 7.6. eCTD dataset path confirmed as `m5/datasets/rconsortiumpilot1/analysis/adam/datasets/` (README.md). Full eCTD index (index.xml) not reviewed — human reviewer must confirm navigability in eCTD viewer. |
| **ISS, ISE, and complete study reports are available (including original protocols, subsequent amendments, etc.).** | | ☑ | | No ISS, ISE, CSR, protocol, or SAP submitted. By design for this pilot. Cover letter lists all submitted components and does not include these documents (cover-letter.pdf, p. 1). Would be an RTF deficiency in a real marketing application. See Appendix 2, Item A for full analysis. |
| **Safety and efficacy were investigated for gender, racial, ethnic, and geriatric subgroups.** | | ☑ | | Subgroup variables confirmed present in ADSL: Sex (F=143, M=111), Race (White=230, Black/AA=23, AI/AN=1), ETHNIC variable present, Age (mean=75.1 yrs, range 51–89). No subgroup analyses submitted. Would be an RTF consideration in a real marketing application. See Appendix 2, Item B. |
| **Data sets are accessible, sufficiently documented, and of sufficient quality (e.g., no meaningful data errors).** | ☑ | | | All 12 ADaM datasets present and accessible. ADSL: 254 unique subjects, balanced treatment groups, no missing ITTFL. ADADAS primary analysis population: N=234, zero missing CHG at Week 24. Python replication (Appendix 1) ran without data errors. Three Pinnacle 21 Error-level conformance issues documented with explanations. **[FLAG: Data value correctness and full ADaM conformance require human technical review of original .xpt files. See Appendix 2, Item C.]** |
| **Application appears to be free from any other deficiency that render the application unreviewable, administratively incomplete, or inconsistent with regulatory requirements.** | ☑ | | | Within the stated pilot objectives, the submission is reviewable. FDA staff successfully reproduced all 4 analysis outputs (response-to-fda-1.pdf, p. 1). Proprietary package source fully readable from r0pkg.txt; Python replication (Appendix 1) confirms model specification and produces directionally consistent results. Standard RTF criteria are intentionally absent by design. See Appendix 2 for full 18-point assessment. **[FLAG: Human reviewer must make final fileability determination.]** |

**IS THE APPLICATION FILEABLE FROM A STATISTICAL PERSPECTIVE?**
**N/A — Human determination required.** Within the pilot's stated objectives this submission appears complete and reviewable. Standard filing criteria are intentionally absent by design. A qualified human reviewer must make the final determination.

---

## 5. Comments to be Conveyed to the Applicant

### 5.1. Refuse-to-File Issues

None identified within the pilot's stated scope. The following would be RTF considerations in a real marketing application (see Appendix 2 for full detail):

- Absence of ISS and ISE (MAPP 6025.4, Rev. 1, Appendix B; 21 CFR 314.50(d)(5)(v) and (vi))
- Absence of complete study report(s), protocol, and SAP (MAPP 6025.4, Rev. 1, Appendix B)
- Absence of demographic subset analyses (MAPP 6025.4, Rev. 1, Appendix B; 21 CFR 314.50(d)(5)(V) and (VI))

### 5.2. Information Requests/Review Issues

**1. Unresolved quantile calculation difference (Table 14-3.01):**
The sponsor retained its quantile calculation approach despite FDA's identification of value differences. The sponsor's response states: *"The value differences in Table 14-3.01 is because of different approaches used to calculate the 97.5% quantile of the standard normal distribution, where the FDA staff used the approximated value 1.96. We kept our approach in the submission package without further modifications."* (response-to-fda-1.pdf, p. 1). Python replication (Appendix 1) yielded LS mean differences of −1.006 (High−Placebo) and −0.467 (Low−Placebo); the reviewer should compare these against the submitted table values to assess the magnitude of any discrepancy attributable to the quantile approach.

**2. Model specification verified — no information request needed:**
The previously unresolved question about the internal specification of `efficacy_models()` has been resolved by reading the package source directly from `r0pkg.txt` and confirmed via Python replication (Appendix 1). All model components are confirmed: ANCOVA formula, contrast type (contr.sum/Type III SS), SITEGR1 as site covariate present in ADADAS, TRTPN mapping (0/54/81), and emmeans proportional-weights pairwise comparisons with no multiplicity adjustment. No information request to the applicant is needed on this point.

**3. ANL01FL variable label inconsistency (Pinnacle 21 AD0018):**
The label for ANL01FL is "Analysis Record Flag 01" in ADADAS and ADCIBC, but "Analysis Flag 01" in ADLBC, ADLBCPV, ADLBH, ADLBHPV, ADVS, and ADNPIX. Independently confirmed from label file inspection. The sponsor explains this is in conformance with ADaM IG 1.0 and has no analysis impact (adrg.pdf, p. 8). The reviewer should confirm the sponsor's explanation is acceptable.

**4. ADTTE censoring convention:**
Dataset inspection confirms CNSR values of 0 (n=152, events) and 1 (n=102, censored) in ADTTE. This is consistent with the standard SAS/CDISC convention and with the `visR::estimate_KM()` function used in tlf-kmplot.r. The reviewer should verify this is correctly interpreted by the KM analysis.

**5. Characterization of EFFFL=N subjects (N=20):**
Twenty of 254 subjects (7.9%) have EFFFL="N" and are excluded from the primary efficacy analysis. These subjects are not characterized in the ADRG. The reviewer may wish to request characterization (e.g., reasons for exclusion, treatment group distribution).

**6. Python-replicated ANCOVA results for comparison with Table 14-3.01** *(see Appendix 1 for code)*:

| Quantity | Python Result |
|---|---|
| N (primary analysis, Week 24) | 234 (Placebo=79, Low=81, High=74) |
| Baseline mean — Placebo | 24.12 |
| Baseline mean — Low Dose | 24.41 |
| Baseline mean — High Dose | 21.30 |
| Mean CHG at Week 24 — Placebo | 2.55 |
| Mean CHG at Week 24 — Low Dose | 2.00 |
| Mean CHG at Week 24 — High Dose | 1.47 |
| LS Mean — Placebo | 2.495 |
| LS Mean — Xanomeline Low Dose | 2.028 |
| LS Mean — Xanomeline High Dose | 1.489 |
| Diff (High − Placebo) | −1.006 |
| Diff (Low − Placebo) | −0.467 |
| Diff (High − Low) | −0.539 |
| TRTPN partial-F p-value (dose-response) | 0.245 |
| Model RMSE | 5.002 |
| Model R² | 0.094 |

*Note: Python uses treatment-contrast dummy coding for LS mean computation rather than R's contr.sum; for marginal LS means with proportional weights this produces equivalent predictions. The reviewer should assess whether any numerical differences from the submitted table fall within acceptable tolerance or are attributable to the unresolved quantile issue (Agency Comment 2).*

---

## 6. Advisory Committee

| | Response/Comments |
|---|---|
| **If the Advisory Committee Decision Aid (ACDA) is required for this application (it is required for a new molecular entity or original BLA), do you have any comments relevant to the completion of this document?** | This is a pilot submission, not a real original BLA for a new molecular entity. The ACDA is not applicable in the standard sense. The reviewer should consult with the team on whether ACDA requirements apply formally given the BLA 351(a) designation. |
| **Has the review division determined that an Advisory Committee (AC) meeting is needed?** | ☐ Yes ☐ No ☑ To be Determined — Not applicable for a pilot submission; human reviewer must determine. |
| **If an AC meeting may be held for this application, are there any areas of expertise that may be important for AC statistician(s) to have?** | If applicable: expertise in R-based statistical programming for regulatory submissions, software validation, and reproducibility of analysis results in a regulatory context. |

---

---

# APPENDIX 1: Python Verification Code for pilot1wrappers::efficacy_models()

**Purpose:** Reviewer-side replication of the `efficacy_models()` function from `pilot1wrappers` v0.1.1, whose source was read directly from `r0pkg.txt` (R/eff_models.R, pkglite plain-text format). Python was used as a substitute for R execution.

**Packages used:** `pandas`, `numpy`, `scipy.stats`, `sklearn.linear_model.LinearRegression`

**Important disclaimers:**
- The R source code in `r0pkg.txt` was read only — it was not executed
- This Python code was not independently validated
- Python uses treatment-contrast dummy coding (`drop_first=True`) rather than R's `contr.sum`; for marginal LS means with proportional weights the predictions are equivalent, but underlying coefficient estimates differ
- This code is a reviewer-side verification aid only; it does not constitute evidence of sponsor program adequacy, dataset quality, or reproducibility
- Human technical review is required before reliance on any result

```python
import io
import pandas as pd
import numpy as np
from scipy import stats
from sklearn.linear_model import LinearRegression

# ============================================================
# AI REVIEWER-SIDE PYTHON VERIFICATION
# Replicates pilot1wrappers::efficacy_models() (R/eff_models.R)
# as read from r0pkg.txt — source was READ only, not executed.
# OLS fitted via sklearn.LinearRegression; contrasts via pandas
# get_dummies. Pairwise LS means via marginal prediction.
# This code was not validated; human technical review required.
# BLA 111111 | CDISCPILOT01 | Table 14-3.01
# ============================================================

adadas = pd.read_csv(io.BytesIO(read_room_file('adadas.csv')))

# --- Primary analysis filters (ADRG Section 7.6, tlf-primary.r) ---
adas = adadas[
    (adadas['EFFFL']   == 'Y') &
    (adadas['ITTFL']   == 'Y') &
    (adadas['PARAMCD'] == 'ACTOT') &
    (adadas['ANL01FL'] == 'Y') &
    (adadas['AVISITN'] == 24)
].copy()

# TRTPCD mapping confirmed from r0pkg.txt R/eff_models.R case_when:
# 0 -> Pbo, 54 -> Xan_Lo, 81 -> Xan_Hi
adas['TRTPCD'] = adas['TRTPN'].map({0: 'Pbo', 54: 'Xan_Lo', 81: 'Xan_Hi'})

# Drop any rows missing model variables
model_df = adas.dropna(subset=['CHG', 'BASE', 'SITEGR1', 'TRTPN', 'TRTPCD']).copy()
n_model  = len(model_df)  # Confirmed N=234

# ==============================================================
# MODEL 1: CHG ~ TRTPN + SITEGR1 + BASE  (continuous dose, dose-response)
# Confirmed from r0pkg.txt: model1 <- lm(CHG ~ TRTPN + SITEGR1 + BASE, data=data)
# SITEGR1 confirmed present in ADADAS (no merge from ADSL required)
# ==============================================================
site_dummies = pd.get_dummies(
    model_df['SITEGR1'].astype(str), prefix='SITE', drop_first=True
).astype(float)

X1 = pd.concat([
    model_df[['TRTPN', 'BASE']].reset_index(drop=True),
    site_dummies.reset_index(drop=True)
], axis=1)

y = model_df['CHG'].reset_index(drop=True).values

# OLS via sklearn (fit_intercept=True matches R's default intercept)
lm1 = LinearRegression(fit_intercept=True)
lm1.fit(X1, y)

yhat1  = lm1.predict(X1)
resid1 = y - yhat1
n1     = len(y)
p1     = X1.shape[1] + 1       # +1 for intercept
df_res = n1 - p1               # degrees of freedom: 234 - 13 = 221
ss_res = float((resid1 ** 2).sum())
ss_tot = float(((y - y.mean()) ** 2).sum())
r2_m1  = 1.0 - ss_res / ss_tot
rmse   = float(np.sqrt((resid1 ** 2).mean()))  # matches R: sqrt(mean(residuals^2))
mse    = ss_res / df_res

# Standard errors via (X'X)^-1 * MSE
X1_aug  = np.column_stack([np.ones(n1), X1.values])
XtX_inv = np.linalg.inv(X1_aug.T @ X1_aug)
se_all  = np.sqrt(np.diag(XtX_inv) * mse)

coef_map = dict(zip(['Intercept'] + list(X1.columns),
                    np.concatenate([[lm1.intercept_], lm1.coef_])))
se_map   = dict(zip(['Intercept'] + list(X1.columns), se_all))

trtpn_coef = float(coef_map['TRTPN'])
trtpn_se   = float(se_map['TRTPN'])
trtpn_t    = trtpn_coef / trtpn_se
trtpn_p    = float(2 * (1 - stats.t.cdf(abs(trtpn_t), df=df_res)))

base_coef  = float(coef_map['BASE'])
base_se    = float(se_map['BASE'])
base_t     = base_coef / base_se
base_p     = float(2 * (1 - stats.t.cdf(abs(base_t), df=df_res)))

# Partial F-test for TRTPN (Type III SS, controlling for all other predictors)
# Matches R: drop1(model1, .~., test="F")
X1_no_trt = pd.concat([model_df[['BASE']].reset_index(drop=True),
                        site_dummies.reset_index(drop=True)], axis=1)
lm1r = LinearRegression(fit_intercept=True)
lm1r.fit(X1_no_trt, y)
ss_res_reduced = float(((y - lm1r.predict(X1_no_trt)) ** 2).sum())
F_trtpn = ((ss_res_reduced - ss_res) / 1) / mse
p_trtpn = float(1 - stats.f.cdf(F_trtpn, dfn=1, dfd=df_res))

# ==============================================================
# MODEL 2: CHG ~ TRTPCD_F + SITEGR1 + BASE (categorical treatment)
# Confirmed from r0pkg.txt: model2 <- lm(CHG ~ TRTPCD_F + SITEGR1 + BASE, data=data)
# R uses contr.sum (sum-to-zero); Python get_dummies uses treatment coding.
# For marginal LS means with proportional weights, predictions are equivalent.
# ==============================================================
trt_dummies = pd.get_dummies(
    model_df['TRTPCD'], prefix='TRT', drop_first=True
).astype(float)

X2 = pd.concat([
    trt_dummies.reset_index(drop=True),
    model_df[['BASE']].reset_index(drop=True),
    site_dummies.reset_index(drop=True)
], axis=1)

lm2 = LinearRegression(fit_intercept=True)
lm2.fit(X2, y)

# LS Means via marginal prediction at mean BASE, proportional site weights
# Matches: emmeans::lsmeans(model2, ~TRTPCD_F, weights='proportional')
mean_base  = float(model_df['BASE'].mean())
site_props = model_df['SITEGR1'].astype(str).value_counts(normalize=True).to_dict()
trt_groups = ['Pbo', 'Xan_Lo', 'Xan_Hi']
ls_means   = {}

for trt in trt_groups:
    weighted_preds, weights = [], []
    for site_str, wt in site_props.items():
        trt_row = pd.DataFrame({'TRTPCD': [trt]})
        trt_dum = pd.get_dummies(trt_row['TRTPCD'], prefix='TRT').reindex(
            columns=trt_dummies.columns, fill_value=0).astype(float)
        site_row = pd.DataFrame({'SITEGR1': [site_str]})
        site_dum = pd.get_dummies(site_row['SITEGR1'].astype(str), prefix='SITE').reindex(
            columns=site_dummies.columns, fill_value=0).astype(float)
        base_row = pd.DataFrame({'BASE': [mean_base]})
        x_row = pd.concat([trt_dum.reset_index(drop=True),
                            base_row.reset_index(drop=True),
                            site_dum.reset_index(drop=True)], axis=1)
        x_row = x_row.reindex(columns=X2.columns, fill_value=0)
        weighted_preds.append(float(lm2.predict(x_row)[0]))
        weights.append(wt)
    ls_means[trt] = float(np.average(weighted_preds, weights=weights))

# Pairwise LS mean differences
diff_hi_pbo = ls_means['Xan_Hi'] - ls_means['Pbo']   # -1.006
diff_lo_pbo = ls_means['Xan_Lo'] - ls_means['Pbo']   # -0.467
diff_hi_lo  = ls_means['Xan_Hi'] - ls_means['Xan_Lo'] # -0.539
```

**Key findings from execution:**
- N=234, no missing values in any model variable
- Model R²=0.094, RMSE=5.002, df_residual=221
- TRTPN coefficient=−0.0118 (SE=0.0101), partial-F p=0.245
- LS Means: Pbo=2.495, Low=2.028, High=1.489
- LS Mean differences: High−Pbo=−1.006, Low−Pbo=−0.467, High−Low=−0.539

---


# APPENDIX 2: Additional Issues Identified During Review

**Scope:** This appendix documents additional observations and potential concerns identified during review of the submitted documents, datasets, and program code, beyond those addressed in the main memo tables. These findings are grounded in:

- **MAPP 6025.4, Rev. 1** (Appendices A, B, and C — publicly available)
- **21 CFR 314.50 and 601.2** (NDA/BLA content requirements)
- **FDA Study Data Technical Conformance Guide** (publicly available)
- **ICH E9(R1)** (estimands and missing data — publicly available)
- **Pinnacle 21 Enterprise conformance checks** (as documented by the sponsor in the ADRG)
- **Direct inspection of submitted documents, datasets (CSV format), define.xml, and r0pkg.txt source code**

 Where an issue is absent by design for this pilot submission, that is noted explicitly.

---


### A. Missing Required Application Sections

**A1. Integrated Summary of Efficacy (ISE) — 21 CFR 314.50(d)(5)(v)**
- **Finding:** Not submitted. Cover letter confirms scope is limited to 4 analysis outputs, ADRG, datasets, and programs.
- **Real application significance:** RTF basis per MAPP 6025.4, Appendix B. The ISE is a required section under 21 CFR 314.50(d)(5)(v). Its absence alone renders a real marketing application incomplete for review.

**A2. Integrated Summary of Safety (ISS) — 21 CFR 314.50(d)(5)(vi)**
- **Finding:** Not submitted.
- **Real application significance:** RTF basis per MAPP 6025.4, Appendix B. Required under 21 CFR 314.50(d)(5)(vi).

**A3. Clinical Study Report(s) — 21 CFR 314.50(d)(5)**
- **Finding:** Not submitted. No CSR, synopsis, or study report sections present.
- **Real application significance:** RTF basis. MAPP 6025.4, Appendix B states "absence of clinical investigation protocols" and study reports as a basis for RTF.

**A4. Protocol(s) and Statistical Analysis Plan(s) — 21 CFR 314.50(d)(5)**
- **Finding:** Not submitted. No protocol, protocol amendments, or SAP present. Analysis specification relies entirely on ADRG and program code, which are not equivalent to pre-specified SAP documentation.
- **Real application significance:** RTF basis per MAPP 6025.4, Appendix B: *"Absence of clinical investigation protocols, including amendments to the clinical investigation design or statistical analysis plan."* In a real application this would also raise integrity concerns — there is no way to establish that the ANCOVA specification was pre-specified before data unblinding.

**A5. Statistical Evaluation Section — 21 CFR 314.50(d)(6)**
- **Finding:** Not submitted as a formal module. The ADRG partially serves this function but is not a statistical evaluation.
- **Real application significance:** 21 CFR 314.50(d)(6) requires a statistical section. Its absence is a potential RTF basis.

**A6. Summary of Clinical Data — 21 CFR 314.50(c)**
- **Finding:** No Module 2 clinical or statistical summaries submitted (no SCE, no clinical overview, no written summary of clinical pharmacology).
- **Real application significance:** RTF basis. MAPP 6025.4, Appendix B: Module 2 summaries are required.

---

### B. Demographic Subgroup Analyses — 21 CFR 314.50(d)(5)(V) and (VI)

**B1. Sex subgroup**
- **Finding:** SEX variable present in ADSL (F=143, 56.3%; M=111, 43.7%). No sex-stratified efficacy or safety analysis submitted among the 4 outputs.
- **Real application significance:** MAPP 6025.4, Appendix B explicitly lists *"Absence of demographic subset analyses specified in the regulations (21 CFR 314.50(d)(5)(V) and (VI))"* as a potentially significant deficiency supporting RTF. MAPP also cites *"inadequate evaluation of safety and/or effectiveness in the population intended to use the drug product, including pertinent subsets, such as sex, age, and racial subsets."*

**B2. Racial subgroup**
- **Finding:** RACE variable present in ADSL (White=230, 90.6%; Black/AA=23, 9.1%; AI/AN=1, 0.4%). No racial subgroup analyses submitted. The dataset is heavily White-predominant, which would itself be a review issue in a real application.
- **Real application significance:** Same as B1. The racial imbalance (90.6% White) would additionally raise a review issue regarding generalizability.

**B3. Ethnic subgroup**
- **Finding:** ETHNIC variable present in ADSL (confirmed in adsl_labels.csv). No ethnicity subgroup analyses submitted.
- **Real application significance:** Same as B1.

**B4. Geriatric subgroup — 21 CFR 314.50(d)(5)(vi)(b)**
- **Finding:** AGE present in ADSL (mean=75.1 yrs, range 51–89). The study population is itself largely geriatric by conventional definition (≥65 years). No formal geriatric subgroup analysis (e.g., ≥65 vs. <65, or ≥75) submitted. AGEGR1 variable present (pooled age groups confirmed in adsl_labels.csv).
- **Real application significance:** 21 CFR 314.50(d)(5)(vi)(b) requires geriatric subset analyses. Absence would be a filing issue in a real application. Note: the entire population being largely elderly could be offered as context, but a formal sub-analysis is still required.

---

### C. Electronic Data and Dataset Quality Issues

**C1. SDTM datasets not submitted**
- **Finding:** Only ADaM datasets submitted. SDTM source data is publicly available via PHUSE GitHub but not included in the submission package.
- **Real application significance:** MAPP 6025.4, Appendix B and FDA Study Data Technical Conformance Guide require both SDTM and ADaM datasets in a marketing application. SDTM absence would be an RTF basis: *"Missing datasets (the submission must include both the case report tabulation datasets and appropriate analysis files)."*

**C2. Three Pinnacle 21 "Error"-level conformance findings (AD0258, AD0018, AD0320)**
- **Finding:** Documented by sponsor in ADRG Section 6.2. AD0258: ADAE records not traceable to SDTM.AE (derived records). AD0018: ANL01FL label mismatch across 7 datasets (independently confirmed from label files). AD0320: Non-standard ADSL dataset label.
- **Real application significance:** MAPP 6025.4, Appendix B: *"Datasets contain transcription, transposition, or other errors, preventing an independent data review."* The Pinnacle 21 errors are documented with explanations, but in a real marketing application each would require human technical adjudication. AD0258 (ADAE extra records) is particularly notable as it affects traceability between ADAE and SDTM — a core ADaM requirement. SDTM absence means traceability cannot be verified at all in this submission.

**C3. ANL01FL label inconsistency across datasets**
- **Finding:** Independently confirmed from label files: "Analysis Record Flag 01" in ADADAS/ADCIBC vs. "Analysis Flag 01" in ADLBC/ADLBCPV/ADLBH/ADLBHPV/ADVS/ADNPIX. While the sponsor explains this is in conformance with ADaM IG 1.0, the inconsistency across datasets in the same submission is a documentation quality concern.
- **Real application significance:** Would be an information request item in a real application; not an RTF basis given the sponsor's explanation, but flags a documentation quality issue.

**C4. No case report forms (CRFs) submitted — 21 CFR 314.50(f)**
- **Finding:** No CRFs submitted. This is a pilot submission using public demo data; CRFs do not exist.
- **Real application significance:** 21 CFR 314.50(f) requires CRFs for deaths, serious adverse events, and adverse dropouts. Absence in a real marketing application would be an RTF basis per MAPP 6025.4, Appendix B.

**C5. No randomization documentation**
- **Finding:** No randomization information (treatment allocation by site, day, time; randomization scheme; randomization ratio) submitted in any document.
- **Real application significance:** MAPP 6025.4, Appendix B: *"Absence of randomization information such as: treatment allocation by site, day, and time; randomization scheme; and randomization ratio"* is listed as a clinical/statistical deficiency. In a real application this would be flagged as a potential RTF item.

---

### D. Missing Data and Analysis Integrity Issues

**D1. No pre-specified missing data strategy**
- **Finding:** LOCF is applied but not pre-specified in a protocol or SAP (neither document was submitted). ADRG Section 3.4 states "Not applicable" for imputation methods, which is inconsistent with LOCF being used.
- **Real application significance:** MAPP 6025.4, Appendix B: *"Use of a statistical analysis plan that was finalized after data unblinding, raising integrity concerns."* Without a pre-specified SAP, there is no way to confirm that LOCF was planned before database lock. This would be a significant review issue in a real marketing application, potentially affecting confidence in the primary analysis.

**D2. No sensitivity analyses for missing data**
- **Finding:** Only LOCF analysis submitted. No MMRM, pattern mixture, or other sensitivity approaches present.
- **Real application significance:** Modern regulatory standards (ICH E9(R1)) require a primary estimand with appropriate handling of intercurrent events, supplemented by sensitivity analyses. Absence of any sensitivity analysis would be a review issue, and potentially a filing issue if the primary analysis is considered insufficiently supported.

**D3. EFFFL=N subjects (N=20) uncharacterized**
- **Finding:** 20 of 254 subjects (7.9%) have EFFFL="N" and are excluded from the primary efficacy analysis without explanation in any submitted document.
- **Real application significance:** In a real application, the reviewer would need to understand why 7.9% of randomized subjects are excluded from the efficacy population. This could be a review issue affecting interpretation of the ITT principle and potentially a filing issue if the exclusion criteria were not pre-specified.

---

### E. Novel Methodology and Software Validation

**E1. No software validation evidence for R submission**
- **Finding:** Explicitly excluded from scope per cover letter: *"Evaluating FDA's acceptance of system/software validation evidence is not in the scope of this pilot."* The ADRG provides package versions and installation instructions but no formal validation documentation.
- **Real application significance:** FDA's Study Data Technical Conformance Guide and emerging policy on R-based submissions require that submitted software be adequately validated. In a real marketing application, the absence of software validation documentation for a proprietary R package used in the primary analysis would be a significant review issue. This pilot is specifically designed to explore this question — the FDA's response to the initial submission did not raise software validation as a deficiency, suggesting some tolerance for this gap in the pilot context.

**E2. R version and package version dependencies not locked in submission**
- **Finding:** The startup.R file specifies R 4.1.2 and a CRAN snapshot date of 2021-08-31 (MRAN), but MRAN was retired in 2023. The specified snapshot repository (`https://mran.microsoft.com/snapshot/2021-08-31`) is no longer accessible, which would prevent exact reproduction of the computational environment going forward.
- **Real application significance:** In a real marketing application, long-term reproducibility of submitted analyses is an expectation. The reliance on a retired repository (MRAN) means the submitted installation instructions are no longer functional as written. This is a practical reproducibility concern that would warrant an information request in a real review.

**E3. Proprietary package bundled as plain text via pkglite — not a standard submission format**
- **Finding:** `pilot1wrappers` is submitted as `r0pkg.txt` using the `pkglite` package. This is a novel approach specific to R submissions. While the source code is fully readable (and was read and replicated in this review), this is not a standard eCTD submission format for analysis software.
- **Real application significance:** Would be a review issue in a real application, requiring FDA to establish policy on acceptable formats for submitted R packages. The pilot is explicitly designed to inform this policy question.

---

### F. Safety Data Organization and Adequacy

**F1. No integrated safety summary across trials**
- **Finding:** Single-study pilot; ISS not submitted. Safety datasets are present (ADAE, ADTTE, lab datasets, ADVS) but no cross-dataset safety narrative or integrated analysis is provided.
- **Real application significance:** 21 CFR 314.50(d)(5)(vi) requires an ISS. In a real application, absence is an RTF basis.

**F2. No exposure-adjusted safety analysis**
- **Finding:** ADAE contains 1,191 AE records. No exposure-adjusted incidence rates, no time-to-event analyses beyond TTDE, and no summary of AE severity or relatedness provided in the submitted outputs. The KM plot for TTDE is the only safety analysis output.
- **Real application significance:** In a real marketing application for a 26-week trial, reviewers would expect exposure-adjusted AE rates, serious AE summaries, AE-related discontinuation analysis, and possibly laboratory parameter shift tables. The absence of these in the submitted outputs would be a review issue.

**F3. MedDRA version and coding dictionary**
- **Finding:** ADRG Section 1.2 lists MedDRA v8.0, which is a very old version (current as of this review is MedDRA v27.0). No coding dictionary (verbatim to preferred term mapping) is submitted.
- **Real application significance:** MAPP 6025.4 Appendix B (Clinical checklist): *"Has the applicant submitted the coding dictionary used for mapping investigator verbatim terms to preferred terms?"* Use of MedDRA v8.0 in a current submission would be flagged as a review issue. The absence of the coding dictionary is a standard deficiency item.

---

### G. Administrative and Regulatory Items

**G1. Form 356h — unsigned in uploaded file**
- **Finding:** Form 356h (356hes.pdf) shows fields for applicant name and application number (BLA 111111, BLA type, 351(a) checked) but signature fields (Items 37–38) appear unsigned in the uploaded version. Date of submission is 02/11/2022.
- **Real application significance:** MAPP 6025.4 Appendix A lists "Incomplete or missing Form FDA 356h" as a potentially easily correctable deficiency. An unsigned 356h would be communicated to the applicant early in the filing period for correction. Human reviewer must verify signature status in the actual eCTD submission.

**G2. No financial disclosure forms (FDA 3454/3455)**
- **Finding:** Not found in uploaded submission documents.
- **Real application significance:** MAPP 6025.4, Regulatory Project Management checklist: financial disclosure forms are required. Absence is noted as a deficiency item. For a pilot using public data with no financial interests, this may be N/A, but the form or a certification of N/A would typically be expected.

**G3. No user fee cover sheet (FDA 3397/3792)**
- **Finding:** Not found in uploaded submission documents.
- **Real application significance:** Required for a marketing application. Absence is a potentially easily correctable deficiency per MAPP 6025.4.

**G4. No pediatric assessment — PREA applicability unclear**
- **Finding:** No pediatric assessment, waiver, or deferral submitted. Alzheimer's disease is not a pediatric condition, so a PREA waiver would likely apply, but no documentation is present.
- **Real application significance:** MAPP 6025.4 Regulatory Project Management checklist requires confirmation of PREA applicability and, if triggered, an agreed initial Pediatric Study Plan. For this indication, a full waiver would likely be appropriate, but the documentation must be present.

**G5. README.md included in submission package**
- **Finding:** The file is present in the uploaded submission materials. The README.md itself states: *"Do not include README.md and .gitignore files into the final submission."* These are GitHub repository management files not intended for eCTD inclusion.
- **Real application significance:** While not a material deficiency, inclusion of non-eCTD files is a housekeeping issue. Human reviewer should confirm whether these files are present in the actual eCTD sequence 0002 submission and, if so, note as a minor administrative finding. This would typically be communicated informally rather than as a formal deficiency.

---

**Summary of Appendix 2 Findings for a Real Marketing Application:**

| Category | Items | RTF Basis | Review Issue | Pilot-Expected |
|---|---|---|---|---|
| A. Missing required sections | 6 | Yes (all 6) | — | Yes |
| B. Demographic subgroup analyses | 4 | Yes (B1–B4) | — | Yes |
| C. Electronic data issues | 5 | Yes (C1, C4) | C2, C3, C5 | C1, C4 by design |
| D. Missing data / analysis integrity | 3 | Potential (D1) | D2, D3 | Partial |
| E. Novel methodology / software | 3 | — | E1, E2, E3 | Yes (by design) |
| F. Safety data | 3 | Yes (F1) | F2, F3 | F1 by design |
| G. Administrative | 5 | G2, G3 potential | G1, G4, G5 | Partial |

> **Important:** All findings in this appendix that are labeled "RTF Basis" or "Review Issue" apply to a standard real marketing application. For this pilot submission, their absence is acknowledged and expected by both parties. The human reviewer must make all final determinations. This appendix is provided for completeness and to illustrate what a full filing review would surface.

---

> **AI-assisted draft — all entries require verification by a qualified human FDA reviewer before use. Evidence sourced strictly from retrieved submission documents, dataset inspection (CSV files), define.xml, r0pkg.txt source code, and Python verification (Appendix 1). All regulatory judgments remain with the human reviewer.**