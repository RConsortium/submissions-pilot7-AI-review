---
document_type: Statistical Review and Evaluation — Filing Review of an NDA/BLA
study: CDISCPILOT01 (R Consortium R Submission Pilot 1)
date: 2026-11-01
reviewer: Elsa (FDA AI Assistant — draft for human reviewer) AKA Claude Sonnet 4.6
status: DRAFT — requires independent verification and sign-off
---

# STATISTICAL REVIEW AND EVALUATION
# FILING REVIEW OF AN NDA/BLA

---

## Header Information

| Field | Details |
|---|---|
| **NDA/BLA #** | N/A — Pilot Submission (CDISCPILOT01) |
| **Supplement #** | N/A — Original pilot submission |
| **Related IND #** | N/A |
| **Product Name** | Xanomeline Transdermal Therapeutic System (TTS); Low Dose (54 mg / 50 cm²) and High Dose (81 mg / 75 cm²) |
| **Indication(s)** | Mild to moderate Alzheimer's Disease |
| **Applicant** | R Consortium R Submission Working Group (Pilot 1 Project Team) |
| **Submission Date** | November 11, 2021 |
| **Review Priority** | N/A — Pilot/demonstration submission; not a regulatory NDA/BLA |
| **Biometrics Division** | [To be completed by reviewer] |
| **Statistical Reviewer** | [To be completed by reviewer] |
| **Concurring Reviewers** | [To be completed by reviewer] |
| **Medical Division** | [To be completed by reviewer] |
| **Clinical Team** | [To be completed by reviewer] |
| **Project Manager** | [To be completed by reviewer] |

---

## 1. Summary of Efficacy/Safety Clinical Trials to be Reviewed

This submission is a pilot reproducibility package submitted by the R Consortium R
Submission Working Group (November 11, 2021). Its stated objective is to test whether
an R-language-based submission is aligned with FDA requirements and to evaluate code
reviewability and analysis reproducibility. The underlying clinical data derive from the
CDISC SDTM/ADaM Pilot Project (CDISCPILOT01), using de-identified legacy data
originally provided by Eli Lilly and Company.

One study is included. The submission is reviewed as if it were a real NDA/BLA
submission, per the pilot's stated intent.

**Table 1: Summary of Trials to be Assessed in the Statistical Review**

| Trial ID | Design | Treatment / Sample Size | Endpoints / Analysis | Preliminary Findings |
|---|---|---|---|---|
| CDISCPILOT01 | MC (17 sites), R, DB, PG, PC; 26 weeks (24 weeks active treatment) | Xanomeline High Dose (81 mg) N=84; Xanomeline Low Dose (54 mg) N=84; Placebo N=86; Total ITT N=254 | **Primary:** ADAS-Cog(11) change from baseline to Week 24 (LOCF, ANCOVA); CIBIC+ at Week 24 (LOCF, ANOVA). **Key Secondary:** Mean NPI-X total score Weeks 4–24 (ANCOVA). **Safety:** AEs, labs, vital signs, KM for time to first dermatologic AE. | Not significant on primary ADAS-Cog (p=0.245 dose-response; from submitted Table 14-3.01). CIBIC+ not submitted. Large dermatologic AE signal in active arms (KM figure). Efficacy conclusion cannot be fully evaluated without sensitivity analyses. |

*MC: multi-center; R: randomized; DB: double-blind; PG: parallel group; PC: placebo-controlled*

**Notes:**
- No SPA was associated with this pilot submission.
- Planned enrollment per SAP §6 was ~300 (100/arm). Actual enrollment was 254 — a
  ~15% shortfall not addressed in the submitted package.
- No data cutoff date is stated anywhere in the submission. Treatment start dates range
  2012-07-09 to 2014-09-02 (study complete).
- Analyses submitted cover a subset of the SAP-specified analyses: demographics,
  ADAS-Cog primary, glucose safety lab, and a KM plot. CIBIC+ (co-primary), NPI-X
  (secondary), AE frequency tables, SAE table, lab shift tables, vital signs summaries,
  and sex subgroup analyses were not submitted.

---

## 2. Assessment of Protocols and Study Reports

The following is based on review of the Statistical Analysis Plan (SAP, CDISCPILOT01,
Final CSR, 27 June 2006, pp. 1–20) and Analysis Data Reviewer's Guide (ADRG, v0.1.1).
A full clinical study report was not submitted; the ADRG notes that only a representative
subset of analyses is included.

**Table 2: Summary of Information Based Upon Review of the Protocol(s) and Study Report(s)**

| Content Parameter | Response / Comments |
|---|---|
| Designs utilized are appropriate for the indications requested. | Yes. Randomized, double-blind, placebo-controlled, 3-arm parallel-group design is appropriate for dose-response evaluation in mild-to-moderate Alzheimer's Disease. Transdermal patch delivery is appropriate given the mechanistic rationale (muscarinic agonism). No unusual or complex design elements. |
| Endpoints and methods of analysis are specified in the protocols/statistical analysis plans. | Yes, for the submitted analyses. SAP pre-specifies: primary ANCOVA (ADAS-Cog, LOCF, treatment as continuous for dose-response, categorical for pairwise); primary ANOVA (CIBIC+); supportive MMRM for ADAS-Cog; ANCOVA for NPI-X. Significance level α=0.05, two-sided, throughout. However, **the CIBIC+ primary analysis was not submitted**, and the pre-specified MMRM sensitivity analysis for ADAS-Cog was not submitted. The submitted CIBIC+ dataset (ADCIBC) is present and contains 234 efficacy-population Week 24 records. |
| Interim analyses (if present) were pre-specified in the protocol with appropriate associated analyses. DSMB meeting minutes and data are available. | No interim analyses are described in the SAP or ADRG. No DSMB is referenced. N/A. |
| Appropriate details and/or references for novel statistical methodology (if present) are included. | No novel statistical methodology is employed. ANCOVA, ANOVA, MMRM, Kaplan-Meier, and CMH are standard. The pilot's novelty is R-based programming, not statistical methods. |
| Investigation of effect of missing data and discontinued follow-up on statistical analyses appears to be adequate. | **No.** LOCF imputation is pre-specified (SAP §8.1) but is not an assumption-free method. Imputation rates at Week 24 are markedly differential: Placebo 17.7%, Low Dose 39.5%, High Dose 44.6% (confirmed from ADADAS). The pre-specified MMRM sensitivity analysis (SAP §10.1.1) was not submitted. No tipping-point, multiple imputation, or on-treatment sensitivity analysis is provided. For CIBIC+, LOCF rates are similarly differential (16.5% / 42.0% / 45.9%) with no sensitivity analysis pre-specified at all. The differential dropout is driven by a 5-fold excess of AE-related discontinuations in active arms (Placebo 8, Low 44, High 40 — confirmed from ADSL). |

---

## 3. Electronic Data Assessment

**Table 3: Information Regarding the Data**

| Content Parameter | Response / Comments |
|---|---|
| Dataset location | eCTD structure per Study Data Technical Conformance Guide: `module/datasets/cdiscpilot1/analysis/adam/datasets/`. Consistent with ADRG §8. |
| Were analysis datasets provided? | Yes. 12 ADaM datasets in SAS transport (XPT) format: ADSL, ADAE, ADTTE, ADLBC, ADLBCPV, ADLBH, ADLBHPV, ADLBHY, ADADAS, ADCIBC, ADNPIX, ADVS. All present and accessible. |
| Dataset structure (e.g., SDTM or ADaM) | ADaM v2.1 / ADaM IG v1.0. Source in SDTM v1.4 / SDTM IG v3.1.2. Define.xml v2.0. Controlled terminology: SDTM CT 2011-12-09, ADaM CT 2011-07-22. Three Pinnacle 21 Enterprise v4.1.1 conformance errors documented in ADRG §6.2 (AD0258, AD0018, AD0320) — all explained as having no impact on analyses. |
| Are the define files sufficiently detailed? | **Partially.** Define.xml v2.0 is provided and covers all datasets. However, derivation method text for a large number of variables — particularly across ADLBC, ADLBH, and ADLBHPV — contains placeholder source-field references rather than derivation algorithms (e.g., ADLBH.AVAL, ADLBH.BASE, and ADLBH.CHG all reference "LB.VISITNUM" as their derivation method; ADLBC.AVAL references "LB.LBSTNRHI"). 186 such placeholder instances were confirmed by document scan. AESER and AEACN methods are direct pass-throughs of SDTM source variables with no derivation logic. ADCIBC.AVAL has no codelist — the CIBIC+ scale direction (improvement vs. worsening) is undocumented. |
| List the dataset(s) that contains the primary endpoint(s) | **ADADAS** — ADAS-Cog(11) analysis data (PARAMCD='ACTOT'). **ADCIBC** — CIBIC+ analysis data. Both confirmed present. The primary analysis program (tlf-primary.r) uses ADADAS with EFFFL='Y', ITTFL='Y', PARAMCD='ACTOT', ANL01FL='Y'. No program uses ADCIBC for an output. |
| Are the analysis datasets sufficiently structured and defined to permit analysis of the primary endpoint(s) without excess data manipulation? | Yes for ADAS-Cog. All necessary pre-derived variables are present (CHG, BASE, AVAL, DTYPE, ANL01FL, EFFFL, ITTFL, SITEGR1, TRTPN). CHG = AVAL − BASE confirmed exact (0 mismatches, 234 analysis records). LOCF records confirmed via DTYPE='LOCF'. For CIBIC+, the data are similarly structured but no analysis program is provided, and the AVAL codelist is absent from define.xml. |
| Are there any initial concerns about site(s) that could lead to inspection? | No specific site inspection concerns identified from the submitted package. 17 sites, blocked randomization confirmed. Treatment start date distribution shows ~30% of starts on weekends — plausibly attributable to de-identification date shifting in this legacy dataset, not a data integrity concern. |
| Safety data are organized to permit analyses across clinical trials in the NDA/BLA. | One trial only. Safety datasets (ADAE, ADTTE, ADLBC, ADLBCPV, ADLBH, ADLBHPV, ADLBHY, ADVS) are present and structured per ADaM standards. A Hy's Law dataset (ADLBHY) is included. However: (1) AESER is coded 'N' on all 3 fatal AEs and 36 additional TEAEs that meet ICH seriousness criteria — confirmed from ADAE; (2) AEACN is blank on all 1,191 ADAE records — confirmed from ADAE; (3) no SAE table, AE frequency table, lab shift table, or vital sign summary was submitted. Cross-trial ISS/ISE not applicable. |

---

## 4. Filing Issues

**Table 4: Initial Overview of the NDA/BLA for Refuse-to-File (RTF)**

| Content Parameter | Yes | No | N/A | Comments |
|---|:---:|:---:|:---:|---|
| Index is sufficient to locate necessary reports, tables, data, etc. | X | | | eCTD folder structure and ADRG §8 directory map clearly locate all datasets, programs, and outputs. |
| ISS, ISE, and complete study reports are available (including original protocols, subsequent amendments, etc.). | | | X | Pilot submission. Abbreviated package by design. No full CSR, ISS, or ISE. SAP and ADRG serve as the primary study documentation. Original protocol available publicly via CDISC/PHUSE repository (ADRG §1.3). |
| Safety and efficacy were investigated for gender, racial, ethnic, and geriatric subgroups. | | X | | SAP §7.2 specifies sex subgroup analysis for efficacy. **No subgroup analyses were submitted.** Sex is unbalanced across arms (female %: Placebo 61.6%, Low 59.5%, High 47.6% — confirmed from ADSL) and this imbalance is invisible in Table 14-2.01 because SEX is omitted from the demographic program. Age and race subgroups also not submitted. For a real NDA, submission of gender, age, and race subgroups is required per 21 CFR 314.50. |
| Data sets are accessible, sufficiently documented, and of sufficient quality (e.g., no meaningful data errors). | | X | | Datasets are present and accessible. However: (1) AESER='N' on all 3 fatal AEs and 36 additional TEAEs meeting ICH seriousness criteria; (2) AEACN blank on all 1,191 records; (3) define.xml derivation methods contain systematic placeholders. These are meaningful data quality concerns that would affect the reliability of any safety summary. |
| Application appears to be free from any other deficiency that renders the application unreviewable, administratively incomplete, or inconsistent with regulatory requirements. | | X | | (1) Co-primary CIBIC+ endpoint has no submitted output despite data being present. (2) Pre-specified MMRM sensitivity analysis not submitted. (3) No AE frequency table, SAE table, or disposition summary. (4) ADRG §3.4 states "Imputation: Not applicable" despite confirmed LOCF in both primary endpoints. (5) EFFFL, the primary analysis population, is not defined in the ADRG. Collectively, these deficiencies would materially impede a substantive statistical review. |

---

### IS THE APPLICATION FILEABLE FROM A STATISTICAL PERSPECTIVE?

**NO** — as a simulated regulatory NDA/BLA.

While the submission demonstrates a functional R-based reproducibility infrastructure
and the submitted datasets are internally consistent on key derivations, the following
deficiencies would prevent a substantive statistical review:

1. The co-primary CIBIC+ endpoint has no submitted analysis output.
2. The pre-specified MMRM sensitivity analysis was not submitted.
3. AESER is coded 'N' on all 3 fatal AEs — a fundamental safety data quality issue.
4. AEACN is blank on all records, preventing characterization of AE-related
   discontinuations.
5. No AE frequency table, SAE table, disposition summary, subgroup analyses, or
   lab/vital sign summaries were submitted.

**As a pilot reproducibility submission**, the package is acceptable given its stated
limited scope.

---

## 5. Comments to be Conveyed to the Applicant

### 5.1. Refuse-to-File Issues

**RTF-1: Co-primary CIBIC+ endpoint — no analysis output submitted.**
The ADRG §5.2.7 and SAP §3.2.1 identify CIBIC+ at Week 24 as a co-primary endpoint.
The ADCIBC dataset contains 234 efficacy-population Week 24 records (Placebo 79, Low 81,
High 74), confirming the data are present. None of the four submitted R programs produce
a CIBIC+ analysis table. In a regulatory NDA, absence of an output for a pre-specified
co-primary endpoint would be a refuse-to-file issue.

**RTF-2: AESER='N' on all 3 fatal adverse events — material safety data quality concern.**
Three fatal TEAEs (Sudden Death, Completed Suicide, Myocardial Infarction) are coded
AESER='N' in ADAE, confirmed by data query. An additional 36 TEAEs across 22 subjects
meet ICH seriousness criteria (death, hospitalization, life-threatening, disability, or
cancer) but are coded AESER='N'. In a regulatory NDA, this would constitute a material
data quality deficiency affecting the safety data on which any benefit-risk assessment
would rely.

### 5.2. Information Requests / Review Issues

The following are ordered by severity of the issue identified.

---

**IR-1: Missing data sensitivity analysis not submitted; pre-specified MMRM absent.**
SAP §10.1.1 pre-specifies a supportive MMRM analysis for ADAS-Cog at Week 24. This
was not submitted. LOCF imputation rates at Week 24 — confirmed from ADADAS —
are 17.7% (Placebo), 39.5% (Low Dose), and 44.6% (High Dose). The differential is
driven by AE-related discontinuations: Placebo 8, Low 44, High 40 (confirmed from
ADSL). For a progressive disease where ADAS-Cog worsens over time, LOCF from an
early discontinuation visit is not assumption-free and systematically favors arms with
heavier early dropout. The null primary result cannot be characterized as robust without
the pre-specified MMRM. No sensitivity analysis was provided for CIBIC+ at all.
**Request:** Submit the pre-specified MMRM analysis for ADAS-Cog. Provide an
analogous sensitivity analysis for CIBIC+.

**IR-2: Post-discontinuation ADAS-Cog assessments mixed with LOCF in primary analysis;
estimand not specified.**
Confirmed by merging ADADAS with ADSL: 37 subjects with EOSSTT='DISCONTINUED'
have at least one observed (non-LOCF) ADAS-Cog record in the primary analysis set
(ANL01FL='Y', DTYPE not 'LOCF') with ADT > ADSL.RFENDT. Breakdown: Placebo 5,
Low Dose 21, High Dose 11. These off-treatment values enter the primary analysis
directly alongside LOCF values for other discontinuers — producing a mixed
estimand approach with no documentation per ICH E9(R1). The imbalance is highest
in Low Dose (21/81 = 26% of the efficacy population).
**Request:** Clarify whether post-RFENDT visits are protocol-specified
retrieved-dropout assessments or dating errors. State the intended estimand. Provide a
sensitivity analysis applying a consistent ICE strategy (e.g., pure on-treatment LOCF
or a treatment-policy approach applying consistently).

**IR-3: AEACN blank on all 1,191 ADAE records; AE-leading-to-discontinuation
untraceable.**
AEACN ('Action Taken with Study Treatment') is NaN on all 1,191 ADAE records —
confirmed by data query. The define.xml derivation is a direct pass-through of
AE.AEACN. 92 subjects discontinued due to an AE (Placebo 8, Low 44, High 40).
None can be linked to a specific causal AE through this variable. The dermatologic AESI
is the dominant safety signal (Placebo 29, Low 62, High 61 subjects with dermatologic
TEAEs — confirmed from ADAE), making an AE-leading-to-discontinuation table by
preferred term essential.
**Request:** Populate AEACN from SDTM source. Submit AE-leading-to-discontinuation
listing and summary table by preferred term and arm.

**IR-4: Multiplicity strategy not documented across co-primary endpoints.**
SAP §7.3 states no multiplicity adjustment will be made across the two co-primary
endpoints, each tested at α=0.05. This means the familywise Type I error rate is not
controlled. No decision rule specifying what constitutes a positive trial result across
both co-primary endpoints and both doses is documented in any submitted file.
**Request:** Document the confirmatory testing strategy, including the decision rule
across ADAS-Cog and CIBIC+ and the two active doses.

**IR-5: Subgroup analyses not submitted; sex imbalance across arms not visible in
Table 14-2.01.**
SAP §7.2 pre-specifies a sex subgroup analysis for ADAS-Cog. No subgroup analysis
outputs were submitted. Confirmed from ADSL: female percentage by arm is Placebo
61.6%, Low 59.5%, High 47.6% — a ~14-point imbalance between Placebo and High
Dose that is not visible in Table 14-2.01 because SEX is omitted from the demographic
program (confirmed from tlf-demographic.r: SEX not in vars vector). ETHNIC is also
absent. Subgroup analyses by gender, age, and race are required for NDA submission
per 21 CFR 314.50.
**Request:** Submit the pre-specified sex subgroup analysis for ADAS-Cog. Add SEX
and ETHNIC to Table 14-2.01.

**IR-6: KM plot y-axis mislabeled; no hazard ratio, log-rank test, or event count;
EVNTDESC typo.**
Confirmed from tlf-kmplot.r: y_label is hard-coded as "Probability of event."
visR::estimate_KM returns the event-free (survival) probability S(t), which starts at
1.0 and declines — the inverse of the label. Confirmed event counts from ADTTE:
Placebo 29 events / 57 censored, Low 62 / 22, High 61 / 23. Median time to first
dermatologic event (among those with events): Placebo 35 days, Low 27 days, High 24
days. EVNTDESC contains a typographical error: "Dematologic Event Occured" (two
spelling errors). AVAL = ADT − STARTDT + 1 is derivationally exact (0 mismatches).
**Request:** Correct y-axis label to "Probability of no dermatologic event." Fix
EVNTDESC. Add event counts, medians with CI, and hazard ratio with CI.

**IR-7: ADRG §3.4 states "Imputation: Not applicable" — contradicted by confirmed
data; EFFFL undefined; visit windows absent.**
ADRG §3.4 states "Imputation/Derivation Methods: Not applicable." This is directly
contradicted by: (1) LOCF confirmed in ADADAS and ADCIBC (DTYPE='LOCF' present);
(2) 29 non-integer ACTOT values confirming prorated scoring when fewer than 11
ADAS-Cog items are available — a form of derivation not documented anywhere.
Additionally, EFFFL — the primary analysis population used in Table 14-3.01 — is
not defined in ADRG §5.2.1 (only SAFFL and ITTFL are listed). Visit windows are
referenced in §5.2.6–5.2.8 but their values are not provided.
**Request:** Correct §3.4 to document LOCF, proration, and visit windowing. Add EFFFL
definition to §5.2.1. Add the visit window table from SAP §8.2.

**IR-8: define.xml derivation methods contain systematic placeholder references;
ADCIBC.AVAL has no codelist.**
Confirmed by scanning define.xml: derivation method text for variables across ADLBH,
ADLBHPV, and ADLBC contains source-field references instead of derivation algorithms
(e.g., ADLBH.AVAL → "LB.VISITNUM"; ADLBH.CHG → "LB.VISITNUM"; ADLBC.AVAL →
"LB.LBSTNRHI"). 186 such instances confirmed. AESER and AEACN derivation methods
reference only their SDTM source variable with no logic. ADCIBC.AVAL has no CodeListRef
— the CIBIC+ scale direction (higher = improvement or worsening?) is undocumented.
**Request:** Replace placeholder derivation texts with actual algorithms. Add AVAL
codelist to ADCIBC documenting scale direction and value meanings.

**IR-9: Glucose table (Table 14-3.02) mislabeled; 63% missing in High Dose arm;
denominator inconsistency.**
Table 14-3.02 presents a glucose safety laboratory ANCOVA at Week 20, not a primary
endpoint analysis. ADLBC has no DTYPE column — confirmed from data — meaning the
Week 20 analysis is observed-case only, not LOCF as the table labeling implies. At Week 20:
Placebo 65/86 evaluable (24.4% missing), High Dose 31/84 (63.1% missing). The baseline
column uses all ITT subjects (N=84/86) while the Week 20 model uses only 31/65 —
an undisclosed denominator shift that contradicts footnote (a).
**Request:** Correct the table title to reflect a safety laboratory endpoint. Align
denominators or add a footnote disclosing the different analysis sets. Report the number
missing per arm at Week 20.

**IR-10: WEIGHTBL denominator for Low Dose arm undisclosed in Table 14-2.01.**
One Low Dose subject has missing WEIGHTBL — confirmed from ADSL. The rtables
function used in tlf-demographic.r silently computes weight and BMI means on n=83
while the column header displays N=84.
**Request:** Add a denominator or missing-count row for continuous variables in
Table 14-2.01.

**IR-11: MRAN snapshot repository retired; R package reproducibility at risk.**
The ADRG appendix specifies installation of R packages from the MRAN snapshot dated
2021-08-31. MRAN (Microsoft R Application Network) has since been retired, meaning
the exact package versions cannot be reliably restored using the specified method.
**Request:** Specify an alternative reproducible package management mechanism for
future submissions (e.g., Posit Package Manager snapshot, renv lockfile, or equivalent).

---

## 6. Advisory Committee

| Item | Response |
|---|---|
| If the ACDA is required (required for NME or original BLA), any comments? | N/A — pilot submission, not an NME NDA or original BLA. |
| Has the review division determined that an AC meeting is needed? | N/A — pilot submission. No AC meeting required or anticipated. |
| If an AC meeting may be held, are there areas of expertise important for AC statistician(s)? | N/A. If FDA were to convene a stakeholder meeting on R-language submissions, expertise in open-source statistical computing, software validation, and reproducible research would be relevant. |

---

---

# APPENDIX: Additional Statistical Issues Identified During Filing Review

*The following findings go beyond the standard filing review template scope but were
identified during the filing review process and are documented here for completeness.
They are drawn from review of the submitted documents and ADaM
datasets. All quantitative findings were confirmed by direct data query.*

---

## A. Population and Disposition

**A.1 EFFFL re-derivation consistent with ADSL flag.**
EFFFL is defined (from SAP §6) as SAFFL=Y plus ≥1 post-baseline ADAS-Cog AND ≥1
post-baseline CIBIC+ assessment. Applying this rule to ADADAS and ADCIBC yields
234 subjects — exactly matching ADSL.EFFFL. Rule confirmed: Placebo 79, Low 81,
High 74.

**A.2 Disposition.**

| Event | Placebo | Low | High | Total |
|---|---:|---:|---:|---:|
| ITT (ITTFL=Y) | 86 | 84 | 84 | 254 |
| Safety (SAFFL=Y) | 86 | 84 | 84 | 254 |
| Efficacy (EFFFL=Y) | 79 | 81 | 74 | 234 |
| Completers Week 24 (COMP24FL=Y) | 60 | 28 | 30 | 118 |
| Completed study (EOSSTT=COMPLETED) | 58 | 25 | 27 | 110 |
| Discontinued due to AE (DCDECOD) | 8 | 44 | 40 | 92 |
| Deaths (DTHFL=Y) | 2 | 1 | 0 | 3 |

ITTFL = SAFFL for all 254 subjects (0 discrepancies). No disposition TLF was submitted.
The 5-fold excess of AE-related discontinuations in active arms is the dominant driver
of differential LOCF imputation in the primary analyses.

---

## B. Data Derivation Integrity Checks

| Check | Result | Source |
|---|---|---|
| ADAS-Cog CHG = AVAL − BASE | 0 mismatches (234 records) | ADADAS |
| TTDE AVAL = ADT − STARTDT + 1 | 0 mismatches (254 records) | ADTTE |
| TRTDURD = TRTEDT − TRTSDT + 1 | 0 mismatches (254 subjects) | ADSL |
| Deaths: ADSL.DTHFL vs. ADAE.AESDTH | 3 subjects confirmed: Placebo ×2, Low ×1, High ×0 | ADSL / ADAE |
| ITTFL = SAFFL (all subjects) | Confirmed 254/254 | ADSL |
| LOCF records via DTYPE='LOCF' | Placebo 14, Low 32, High 33 at Wk 24 | ADADAS |
| Prorated ACTOT (non-integer AVAL) | 29 records confirmed | ADADAS |

---

## C. Primary Efficacy — Additional Detail

**ADAS-Cog LOCF missing data at Week 24 (confirmed from ADADAS):**

| Arm | Efficacy N | LOCF at Wk 24 | % Imputed |
|---|---:|---:|---:|
| Placebo | 79 | 14 | 17.7% |
| Xanomeline Low Dose | 81 | 32 | 39.5% |
| Xanomeline High Dose | 74 | 33 | 44.6% |

From submitted Table 14-3.01: dose-response p=0.245; High−Placebo −1.0 (SE 0.84),
p=0.233; Low−Placebo −0.5 (SE 0.82), p=0.569. Neither co-primary endpoint approaches
statistical significance.

**CIBIC+ (co-primary, confirmed from ADCIBC, no submitted table):**

| Arm | N (Wk 24) | Mean AVAL | LOCF N | % Imputed |
|---|---:|---:|---:|---:|
| Placebo | 79 | 4.291 | 13 | 16.5% |
| Xanomeline Low Dose | 81 | 4.185 | 34 | 42.0% |
| Xanomeline High Dose | 74 | 4.324 | 34 | 45.9% |

Scale range in data: 2–6. No codelist; direction undocumented. No formal test submitted.
Numerically no meaningful difference across arms.

---

## D. Safety — Additional Detail

**D.1 Dermatologic AESI (confirmed from ADAE and ADTTE).**

| Arm | Subjects with derm TEAE | Events (CNSR=0) | Censored | Median days to event |
|---|---:|---:|---:|---:|
| Placebo | 29 | 29 | 57 | 35 |
| Xanomeline Low Dose | 62 | 62 | 22 | 27 |
| Xanomeline High Dose | 61 | 61 | 23 | 24 |

AVAL derivation (ADT − STARTDT + 1): 0 mismatches. 24 AE discontinuers are
censored in the TTDE analysis (Placebo 2, Low 12, High 10) with EVNTDESC='Study
Completion Date' — an inaccurate description for premature discontinuers. This
censoring is concentrated in active arms where AE discontinuation correlates with
dermatologic events, making it potentially informative. No sensitivity analysis addressing
this was provided.

**D.2 Seriousness coding errors (confirmed from ADAE).**

| Fatal AE Subject | Preferred Term | Arm | AESER | AEOUT |
|---|---|---|---|---|
| 01-701-1211 | SUDDEN DEATH | Xanomeline Low Dose | N | FATAL |
| 01-704-1445 | COMPLETED SUICIDE | Placebo | N | FATAL |
| 01-710-1083 | MYOCARDIAL INFARCTION | Placebo | N | FATAL |

36 additional TEAEs across 22 subjects (Placebo 6, Low 9, High 7) meet at least one ICH
seriousness criterion but are coded AESER='N'. Top preferred terms: SYNCOPE (5),
TIA (3), HIP FRACTURE (3), MI (3), PNEUMONIA (2), ATRIAL FIBRILLATION (2),
MALIGNANT FIBROUS HISTIOCYTOMA (2). The AOCC02FL, AOCC03FL, and AOCC04FL
flags — which all require AESER='Y' per define.xml — are equally affected by these
errors. No SAE table was submitted.

**D.3 AEACN blank on all records.**
AEACN = NaN on all 1,191 ADAE records (100%). 92 AE discontinuers cannot be linked
to a causal AE. An AE-leading-to-discontinuation table by preferred term cannot be
produced from the submitted data.

---

## E. Analysis Plan Issues

**E.1 Estimand not specified per ICH E9(R1).**
The primary analysis uses LOCF for most discontinuers but retains post-discontinuation
observed data for 37 subjects (confirmed by matching ADADAS ADT to ADSL.RFENDT
among EOSSTT='DISCONTINUED' subjects). This produces a mixed approach — part
treatment-policy, part on-treatment — without documentation of an estimand or ICE
strategy.

**E.2 Trial design appropriateness note — potential inadvertent unblinding.**
The transdermal formulation is associated with a large dermatologic signal (active arms:
~74% event rate vs. ~34% in Placebo). Application-site reactions are visible to subjects
and investigators, creating a potential inadvertent unblinding risk that is not addressed
in the submitted package.

---

## F. Program and Metadata Review

**F.1 R programs reviewed:** tlf-demographic.r, tlf-primary.r, tlf-efficacy.r,
tlf-kmplot.r. Program logic is consistent with ADRG §7.3 output list and §7.6
selection criteria. No discrepancies found between program selection criteria and ADRG
documentation.

**F.2 pilot1wrappers package:** Proprietary R package (v0.1.1) submitted as r0pkg.txt.
Restoration instructions provided in ADRG appendix via pkglite::unpack. Package not
executed in this review. The efficacy_models() function encapsulates the ANCOVA
for Table 14-3.01 and cannot be independently inspected without unpacking.

**F.3 Inconsistent CI method in Table 14-3.02 (confirmed from tlf-efficacy.r).**
LS-mean CIs use the t-distribution (emmeans), while the pairwise treatment-difference
CI uses z=1.96 (hard-coded: estimate ± 1.96 × SE). These are inconsistent methods
within the same table. RMSE is computed as sqrt(mean(residuals²)) — dividing by n
rather than n−p — which is non-standard.

---

*DISCLAIMER: This filing review memo was drafted with AI assistance (Elsa). All
quantitative findings are based on direct queries of the ADaM CSV datasets or document
scans. This draft requires independent verification and sign-off by the assigned
statistical reviewer and concurring reviewer before use in any official FDA regulatory
context. Human judgment, expertise, and accountability remain essential.*

---

**Sources:**
- adsl.csv, adadas.csv, adae.csv, adcibc.csv, adtte.csv (converted from XPT)
- adrg.pdf (ADRG v0.1.1)
- define.xml (v2.0)
- SAP.pdf (CDISCPILOT01, Final SAP, 27 June 2006, pp. 1–20)
- tlf-primary.r, tlf-efficacy.r, tlf-kmplot.r, tlf-demographic.r
- MAPP 6610.5 (Statistical Review of NDAs and BLAs, effective 06/30/2023, pp. 2–24)
- NDA_BLA_StatisticsFilingTemplate_Sept2025.pdf
- cover-letter.pdf
