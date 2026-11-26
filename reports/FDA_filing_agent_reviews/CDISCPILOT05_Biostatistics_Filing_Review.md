---
document_type: Biostatistics Filing Review Report
application: BLA 111111, Sequence 0007 (provisional) — R Consortium R Submission Pilot 5
study: CDISCPilot01 — Safety and Efficacy of the Xanomeline Transdermal Therapeutic System (TTS) in Patients with Mild to Moderate Alzheimer's Disease
applicant: R Consortium R Submission Working Group
product: Xanomeline Transdermal Therapeutic System — Placebo / Low Dose (50 cm2, 54 mg) / High Dose (75 cm2, 81 mg)
date_of_submission: "TBD, 2025 (as stated in cover letter)"
date_of_review: "2026-11-25"
reviewer: Elsa (FDA AI Assistant) — AI-assisted biostatistics filing reviewer; human expert oversight required
status: Draft — Human Review Required
sources: cover-letter.pdf (m1/us/); adrg.pdf, adam-pilot-5.xlsx, adsl.json, adadas.json, adae.json, adlbc.json, adtte.json (m5/.../adam/datasets/); 21 SDTM domains (m5/.../sdtm/); tlf-primary.r, pilot5-helper-fcns.r, tlf-efficacy.r, tlf-kmplot.r, tlf-demographic.r, adsl.r, adadas.r, adae.r, adlbc.r, adtte.r (m5/.../adam/programs/); mapp6025-4.r1_goodreviewpractice_refusetofile_10-23-25.pdf (pp. 33-35)
human notes: 
-  "Because Elsa can only access eCTD from production submissions, the file tree structure was provided to Elsa within a prompt."
- "The MAPP 6025.4, Rev. 1 pdf file was provided to Elsa. This file contains the Biostatistics Filing Review Template Checklist, which is completed for every filing review. The file is publicly available."
regulatory_basis:
  - MAPP 6025.4, Rev. 1 — Good Review Practice: Refuse to File (Effective 10/23/25); Biostatistics Filing Checklist pp. 33-35
  - CDISC ADaM-IG v1.1 / ADaM v2.1 — referenced in ADRG Section 1.2
  - CDISC SDTM-IG v3.1.2 / SDTM v1.2 — referenced in ADRG Section 1.2
  - CDISC Define-XML v2.0 — referenced in ADRG Section 1.2; used as framework for define file assessment
  - CDISC Dataset-JSON v1.1 — submission transport format; referenced in ADRG Section 1.2 and Appendix 3
  - CDISC ADaM Controlled Terminology 2022-06-24 — referenced in ADRG Section 1.2
  - CDISC SDTM Controlled Terminology 2022-12-16 — referenced in ADRG Section 1.2
  - MedDRA v8.0 — adverse event dictionary; referenced in ADRG Section 1.2
  - FDA Study Data Technical Conformance Guide — referenced in ADRG Section 8
disclaimer: AI-assisted draft. All findings, ratings, assessments, and Python-translated code require independent human expert verification before use in any regulatory determination. The fileability determination (Section 4) is left blank for the human reviewer. Reviewer-side Python results are approximations only. Sponsor R code was not used to generate any AI-inferred Python code.
---

# Biostatistics Filing Review Report
## BLA 111111 — R Consortium R Submission Pilot 5
**Study:** CDISCPilot01 — Xanomeline Transdermal Therapeutic System, Alzheimer's Disease  
**Applicant:** R Consortium R Submission Working Group  
**Submission Sequence:** 0007 (provisional)  
**Date of Review:** 2026-11-25  
**Reviewer:** Elsa (FDA AI Assistant) — *Human expert review required; see disclaimer*  

---


> **IMPORTANT:** This checklist is a sample of a tool used to assist reviewers during the
> filing review of an application. All decisions regarding whether an application can be
> filed are based on a comprehensive review of all relevant information in accordance with
> applicable legal and scientific standards.

---

## 1. Summary of Efficacy/Safety Clinical Trials to be Reviewed

This submission is the R Consortium R Submission Pilot 5, an FDA-industry collaboration
to test R-language and Dataset-JSON (v1.1) based submissions for alignment with FDA
requirements. It is not a standard NDA/BLA regulatory application seeking approval. The
submission contains data and programs from a single clinical study (CDISCPilot01)
originally conducted to evaluate xanomeline transdermal therapeutic system in patients
with mild to moderate Alzheimer's disease. No SPA was identified for this study. No
annotated label, SCE, or ISE was submitted; the submission is explicitly scoped to data
files, R programs, regenerated outputs, and an ADRG. Accordingly, there are no labeling
claims to assess and no trials that will not be reviewed (there is only one). See Appendix
1, Section A2 for full trial detail.

**Table 1: Summary of Trials to be Assessed in the Statistical Review**

| Trial ID | Design* | Treatment / Sample Size | Endpoint / Analysis | Preliminary Findings |
|---|---|---|---|---|
| CDISCPilot01 | MC, R, DB, PG, PC (26 wks) | Xanomeline High Dose (75 cm2/81 mg) / N=84 (ITT); Xanomeline Low Dose (50 cm2/54 mg) / N=84 (ITT); Placebo / N=86 (ITT) | **Primary:** ADAS-Cog(11) change from baseline to Week 24 (LOCF); ANCOVA with treatment, pooled site group (SITEGR1), and baseline as covariate. **Safety:** Time to first dermatologic event (KM); Safety population. **Secondary:** Glucose change from baseline at Week 20; ANCOVA; ITT, Xan High vs. Placebo only. | Reviewer-side Python verification: LS mean diff Xan Hi minus Pbo = -1.006; Xan Lo minus Pbo = -0.467. Dose-response F=1.361, p=0.245 (unadjusted). KM median time to dermatologic event: Placebo=139 days, Xan Low=29.5 days, Xan High=24.5 days. See Appendix 1, Sections A2-A3 for full detail and caveats. |

*MC: multi-center, R: randomized, DB: double-blind, PG: parallel group, PC: placebo controlled

---

## 2. Assessment of Protocols and Study Reports

**Table 2: Summary of Information Based Upon Review of the Protocol(s) and the Study Report(s)**

| Content Parameter | Response / Comments |
|---|---|
| Designs utilized are appropriate for the indications requested. | The study employed a prospective, randomized, multi-center, double-blind, placebo-controlled, parallel-group design for mild to moderate Alzheimer's disease (3 arms, 26 weeks). Design is documented in the ADRG (Section 2.2.2). **No protocol or clinical study report was submitted.** Clinical appropriateness cannot be determined from the ADRG alone. **[Human review required]** |
| Endpoints and methods of analysis are specified in the protocols/statistical analysis plans. | The primary ANCOVA model (CHG ~ TRTPN/TRTPCD_F + SITEGR1 + BASE, Type III SS via contr.sum, proportional LS means via emmeans) and LOCF imputation are specified in the analysis programs and in the ADRG output program table (Section 7.3). **No protocol or SAP PDF was submitted.** The ADRG references SAP Sections 8.2 and 14.2 for derivation details, but those documents are absent. **[Human review required; potential information request — see Section 5.2]** |
| Interim analyses (if present) were pre-specified in the protocol with appropriate associated analyses. DSMB meeting minutes and data are available. | No interim analyses were identified in any submitted document. No DSMB minutes are present or referenced. **N/A** pending human confirmation that no interim analyses were conducted. |
| Appropriate details and/or references for novel statistical methodology (if present) are included (e.g., codes for simulations). | No novel statistical methodology identified. Standard ANCOVA via lm() and emmeans::lsmeans() with proportional weighting is used for the primary endpoint; Kaplan-Meier via ggsurvfit::survfit2() for the safety endpoint. References to published emmeans documentation are provided in program comments (pilot5-helper-fcns.r). **N/A.** |
| Investigation of effect of missing data and discontinued follow-up on statistical analyses appears to be adequate. | LOCF imputation is implemented for the primary endpoint (ACTOT, ADADAS). Reviewer-side verification confirmed 222 LOCF-imputed records out of 1,040 total ACTOT records; **99 of 234 subjects analyzed at Week 24 (42%) have LOCF-imputed values.** No sensitivity analyses, pattern-mixture models, or multiple imputation methods are present in the submitted programs or ADRG. Known QC discrepancy: 19 subjects have differing DTYPE=LOCF assignment vs. original CDISC data (ADRG Appendix 2, pp. 30-33). **[Human review required; adequacy of missing data investigation is a concern given 42% LOCF rate at the primary timepoint]** |

---

## 3. Electronic Data Assessment

**Table 3: Information Regarding the Data**

| Content Parameter | Response / Comments |
|---|---|
| Dataset location | Documented in ADRG Section 8 (Directory Structure, pp. 16-17). **ADaM datasets:** m5/datasets/rconsortiumpilot5/analysis/adam/datasets/. **SDTM datasets:** m5/datasets/rconsortiumpilot5/tabulations/sdtm/. **Analysis programs:** m5/datasets/rconsortiumpilot5/analysis/adam/programs/. All locations confirmed by reviewer-side file verification. |
| Were analysis datasets provided? | **Yes — with qualification.** Five ADaM datasets were provided: ADSL, ADADAS, ADAE, ADLBC, ADTTE. All are in **Dataset-JSON v1.1 format** (not standard XPT). All 21 SDTM datasets are also present. All 26 datasets confirmed readable; declared record counts match actual row counts. CDISC P21C does not currently support Dataset-JSON v1.1 validation; conformance was assessed via XPT conversion (no P21C issues found on converted XPT). **[Human review required re: Dataset-JSON v1.1 acceptability as transport format]** |
| Dataset structure (e.g., SDTM or ADaM) | ADaM-IG v1.1 / ADaM v2.1 (ADaM datasets); SDTM-IG 3.1.2 / SDTM v1.2 (SDTM datasets). Confirmed in ADRG Section 1.2. ADaM dataset classes: ADSL = Subject-Level; ADADAS, ADLBC, ADTTE = Basic Data Structure; ADAE = Occurrence Data Structure. Transport format is Dataset-JSON v1.1. All required SDTM variables confirmed present in key domains (DM, AE, EX, DS, LB, QS, VS, MH, SV) via reviewer-side check. |
| Are the define files sufficiently detailed? | **define.xml is not present in the submission.** The adam-pilot-5.xlsx file (11 sheets: Define, Datasets, Variables, ValueLevel, Codelists, Dictionaries, Methods, Comments, Documents, Analysis Displays, Analysis Results) provides substantive ADaM metadata covering 6 of 10 define.xml v2.0 required elements fully (dataset metadata, variable metadata, codelists, value-level metadata for ADADAS, computational methods, origin metadata). The ADRG supplements with dataset narratives and QC documentation. **Gaps:** SDTM variable and codelist metadata not covered; value-level metadata for ADLBC and ADTTE AVAL incomplete; no formal OID structure. **[Human review required; potential information request — see Section 5.2, IR-1]** |
| List the dataset(s) that contains the primary endpoint(s) | **Efficacy primary endpoint (ADAS-Cog):** ADADAS (adadas.json), PARAMCD=ACTOT. Confirmed in ADRG Section 5.2.2 and program tlf-primary.r. **Safety endpoint (time to first dermatologic event):** ADTTE (adtte.json), PARAMCD=TTDE. Confirmed in ADRG Section 5.2.5 and program tlf-kmplot.r. |
| Are the analysis datasets sufficiently structured and defined to permit analysis of the primary endpoint(s) without excess data manipulation?* | **Yes — with qualification.** Reviewer-side Python code executed the primary ANCOVA directly from adadas.json using simple row filtering (EFFFL="Y", ITTFL="Y", PARAMCD="ACTOT", ANL01FL="Y", AVISITN=24) with no additional derivation required. All required variables (CHG, BASE, TRTPN, SITEGR1, TRTP, AVISITN) are present and correctly derived (CHG = AVAL minus BASE verified with 0 mismatches across 786 records). **Qualification:** Dataset-JSON v1.1 format requires specialized parsing tools; known QC discrepancy in ADADAS (19 subjects, LOCF DTYPE differences) affects primary endpoint values for those subjects. **[Human technical review required]** |
| Are there any initial concerns about site(s) that could lead to inspection? If so, list the site(s) that you request to be inspected and the rationale. | This is a pilot submission using public CDISC pilot data; no real clinical sites are involved. No site-level data anomalies or integrity concerns were identified by reviewer-side checks. Sites with fewer than 3 subjects per treatment arm are pooled into SITEGR1="900" (sites 702, 706, 707, 711, 714, 715, 717) per the sponsor's pooling algorithm (pilot5-helper-fcns.r). **No inspection concerns identified. [Human determination required]** |
| Safety data are organized to permit analyses across clinical trials in the NDA/BLA. | **N/A.** This is a single-study pilot submission. No ISS or cross-trial safety database was submitted or expected. |

*This might lead to the need for an information request or be a refuse to file issue depending on the ability to review the data.

---

## 4. Filing Issues

**Table 4: Initial Overview of the NDA/BLA for Refuse-to-file (RTF):**

| Content Parameter | Yes | No | NA | Comments |
|---|---|---|---|---|
| Index is sufficient to locate necessary reports, tables, data, etc. | | X | | ADRG Section 8 provides a directory listing and program-to-output mapping (Section 7.3). No formal eCTD index file is verifiable from the provided materials; no hyperlinks accessible; no CSR/ISE/ISS present to be indexed. For the pilot context, the ADRG directory listing may be sufficient; human determination required. |
| ISS, ISE, and complete study reports are available (including original protocols, subsequent amendments, etc.). | | X | | No ISS, ISE, CSR, SAP, or protocol was submitted. The cover letter explicitly scopes deliverables to: cover letter, Dataset-JSON data files, R programs, regenerated outputs, and ADRG. Absence of these documents is consistent with the pilot scope but would constitute potential RTF issues in a standard NDA/BLA filing. |
| Safety and efficacy were investigated for sex, racial, ethnic, and geriatric subgroups. | | X | | Variables SEX, RACE, ETHNIC, AGEGR1 are present in ADSL and carried into analysis datasets. Table 14-2.01 (tlf-demographic.r) summarizes age group and race by treatment arm in the ITT population. No formal subgroup efficacy or safety analyses by sex, race, ethnicity, or geriatric status were submitted. Sample is predominantly White (Pbo: 78/86, Xan Low: 78/84, Xan High: 74/84); no Hispanic/Latino subgroup analysis identified. |
| Data sets are accessible, sufficiently documented, and of sufficient quality (e.g., no meaningful data errors). | | | Flagged | **Accessible:** All ADaM and SDTM datasets confirmed readable. **Documented:** ADRG + adam-pilot-5.xlsx provide substantial ADaM metadata; SDTM metadata coverage is a gap; define.xml absent. **Quality:** Reviewer-side checks found no merge key integrity issues (0 orphaned records across all datasets), no CHG derivation errors (0 mismatches in 786 records), correct LOCF counts per ADRG. Known QC discrepancies documented in ADRG Appendix 2: 19-subject ADADAS LOCF DTYPE difference; 6 missing EXENDTC in SDTM EX; 18 ADLBC PARAMCD entries in codelist absent from submitted data. No other meaningful errors found by reviewer-side checks, but human technical review is required for final determination. See Appendix 1, Section A5. |
| Application appears to be free from any other deficiency that render the application unreviewable, administratively incomplete, or inconsistent with regulatory requirements. | | | Flagged | Pilot submission — explicitly not a standard NDA/BLA regulatory application. Major filing elements are absent by design. Dataset-JSON v1.1 is not yet standard-validated by P21C. Human determination required as to whether these represent deficiencies in the pilot context. |

**IS THE APPLICATION FILEABLE FROM A STATISTICAL PERSPECTIVE? [ ] Yes / [ ] No**

> *To be determined by the human reviewer. See Appendix 1 for full supporting detail.
> AI-generated findings are a draft aid only and do not constitute a regulatory determination.*

---

## 5. Comments to be Conveyed to the Applicant

### 5.1. Refuse-to-File Issues

None identified that would apply in the pilot context. For a standard NDA/BLA, the absence
of ISS, ISE, CSR, SAP, protocol, and define.xml would each require evaluation as potential
RTF issues. Human reviewer should make the final RTF determination for this pilot submission.

### 5.2. Information Requests / Review Issues

**IR-1 — define.xml not submitted:**
The submission references define.xml in the ADRG (Section 6.1: "Were the ADaM datasets
evaluated in relation to define.xml? Yes") and in the analysis programs
(metadata_ref = file.path(path$adam, "define.xml")), but the define.xml file is not present
in the submission package. If a define.xml was generated as part of this pilot, please provide
it. The adam-pilot-5.xlsx file provides substantial ADaM variable-level metadata and may serve
as an interim substitute for reviewer purposes, but the absence of define.xml for SDTM datasets
is a gap.

**IR-2 — Dataset-JSON v1.1 tool support:**
The submitted datasets use Dataset-JSON v1.1 format. As noted in the ADRG (Section 6.2),
Pinnacle 21 Community 4.1.0 and Enterprise do not currently support Dataset-JSON v1.1
validation. The sponsor conducted conformance checks via XPT conversion (no P21C issues found)
and via Dataset-JSON 1.0 conversion (label mismatch and date format findings flagged — AD0018,
AD0041A — across all five datasets). The Agency requests confirmation that the
XPT-conversion-based P21C validation is considered the operative conformance check, and notes
that updated P21C support for Dataset-JSON v1.1 is expected.

**IR-3 — ADADAS LOCF discrepancy (19 subjects, primary endpoint):**
The ADRG (Appendix 2, pp. 30-33) documents that 19 subjects have differing AVAL/CHG/PCHG
values at the primary endpoint timepoint between Pilot 5 and the original CDISC ADADAS
dataset, due to differences in DTYPE=LOCF assignment. The sponsor's explanation is that
the original CDISC dataset incorrectly assigned DTYPE=LOCF to actual observations, and that
the Pilot 5 derivation is correct. Please confirm that the Pilot 5 ADADAS is the intended
correct version for this submission, and provide any additional documentation supporting
the derivation decision.

**IR-4 — ADLBC missing "change from previous visit" parameters:**
The adam-pilot-5.xlsx codelist (PARAMCD_ADLBC) specifies 18 "change from previous visit
relative to normal range" parameters (e.g., _GLUC, _ALB, _ALT, etc.), but none of these
underscore-prefixed PARAMCDs are present in the submitted adlbc.json. The ADRG
(Section 5.2.4) describes two sets of lab parameters in ADLBC including "change from previous
visit relative to normal range values." Please confirm whether these parameters were
intentionally excluded from the Pilot 5 submission or represent a data gap, and if excluded,
provide the rationale.

**IR-5 — Pairwise comparisons unadjusted for multiplicity:**
Table 14-3.01 footnote [3] states: "Pairwise comparison with treatment as a categorical
variable: p-values without adjustment for multiple comparisons." Three pairwise comparisons
are presented (Xan Hi vs. Pbo, Xan Lo vs. Pbo, Xan Hi vs. Xan Lo) without multiplicity
adjustment. For information purposes, please confirm whether this was pre-specified in the
SAP and whether this approach is consistent with the study objectives.

---

## 6. Advisory Committee

| | Response / Comments |
|---|---|
| If the Advisory Committee Decision Aid (ACDA) is required for this application (it is required for a new molecular entity or original BLA), do you have any comments relevant to the completion of this document? | Not applicable — this is a pilot submission to test Dataset-JSON/R submission format, not a regulatory application for a new molecular entity or original BLA in the standard sense. |
| Has the review division determined that an Advisory Committee (AC) meeting is needed? | [ ] Yes  [ ] No  [X] To be Determined — not applicable for this pilot. |
| If an AC meeting may be held for this application, are there any areas of expertise that may be important for AC statistician(s) to have? | Not applicable for this pilot. |

---
---

# Appendix 1: Extended Review Findings

*This appendix contains findings that go beyond or provide more granular detail than the
MAPP template entries above. All findings are AI-assisted draft outputs requiring human
expert verification.*

---

## A1. Regulatory History

No Meeting Minutes (Module 1.6), Annotated Label (1.14.1.2), SCE (2.7.3), or ISE (5.3.5.3)
are present in this submission. Regulatory history cannot be assessed from the available
documents.

The cover letter establishes the submission context: *"This is an FDA-industry collaboration
through the non-profit organization R Consortium"* and *"The objective of this portion of
the R Consortium R submission Pilot 5 Project is to test the concept that a R-language based
submission package is aligned with FDA requirements and meets the expectations of the FDA
staff, including assessing code review and analyses reproducibility."* (Source:
cover-letter.pdf, p. 1)

No prior FDA feedback, SPA agreements, meeting minutes, CRLs, or regulatory precedent
documents are available. All topics under a standard regulatory history framework
(pre-submission meetings, program adequacy, prior decisions, guidance, protocol/SAP
discussions, statistical reviews, amendments, DDT qualification) are not assessable from
the submitted documents.

> **Human review required:** Agency records and internal databases should be consulted to
> determine whether any regulatory history relevant to this pilot (e.g., prior correspondence,
> agreed scope, FDA pilot commitments) exists outside this submission package.

---

## A2. Summary of Clinical Trial — CDISCPilot01

- **Protocol Number/Title:** CDISCPilot01 — "Safety and Efficacy of the Xanomeline Transdermal
  Therapeutic System (TTS) in Patients with Mild to Moderate Alzheimer's Disease"
  (Source: adrg.pdf, p. 2, Section 2.1)
- **Design:** Prospective, randomized, multi-center, double-blind, placebo-controlled,
  parallel-group; three arms; 26-week treatment (13 scheduled visits, Week -2 through Week 26).
  (Source: adrg.pdf, pp. 2-3, Sections 2.2.2-2.2.4)
- **Treatment arms:** Placebo; Xanomeline Low Dose (50 cm2/54 mg); Xanomeline High Dose
  (75 cm2/81 mg). Two patches applied daily. (Source: adrg.pdf, p. 3, study schema)
- **Planned N:** 300 (100 per arm). **Actual ITT N:** 254 (Placebo=86, Xan Low=84,
  Xan High=84). DM contains 306 subjects (254 randomized + 52 screen failures). Screen
  failures correctly excluded from ADSL. (Source: adrg.pdf, p. 2; Python verification of
  adsl.json, dm.json)
- **Objectives:** "To evaluate the efficacy and safety of transdermal xanomeline, 50 cm2 and
  75 cm2, and placebo in subjects with mild to moderate Alzheimer's disease."
  (Source: adrg.pdf, p. 2, Section 2.2.2)
- **ADaM datasets:** ADSL (254x49), ADADAS, ADAE, ADLBC, ADTTE (254x26). All in
  Dataset-JSON v1.1.
- **SDTM datasets:** 21 domains present. All confirmed readable and internally consistent.
- **Submitted outputs:** Table 14-2.01 (demographics, ITT), Table 14-3.01 (primary ANCOVA,
  efficacy population), Table 14-3.02 (GLUC ANCOVA, ITT, Xan High vs. Placebo),
  Figure 14-1 (KM plot, safety population).

**Demographics — ITT population (Python-verified from adsl.json):**

| | Placebo (N=86) | Xan Low (N=84) | Xan High (N=84) |
|---|---|---|---|
| Mean Age, yrs (SD) | 75.2 (8.6) | 75.7 (8.3) | 74.4 (7.9) |
| Age <65 | 14 | 8 | 11 |
| Age 65-80 | 42 | 47 | 55 |
| Age >80 | 30 | 29 | 18 |
| White | 78 | 78 | 74 |
| Black/African American | 8 | 6 | 9 |
| American Indian/Alaska Native | 0 | 0 | 1 |

---

## A3. Primary Analysis Variables and Code Traceability

### A3.1 Primary Endpoint Traceability

**Efficacy Primary Endpoint — ADAS-Cog(11) Change from Baseline to Week 24 (LOCF)**

- **Dataset:** ADADAS (adadas.json); endpoint variable: CHG
- **Filter logic:** EFFFL=="Y", ITTFL=="Y", PARAMCD=="ACTOT", ANL01FL=="Y"
  (Source: tlf-primary.r)
- **Timepoints:** AVISITN==0 (Baseline), AVISITN==24 (Week 24)
- **Analysis population:** Efficacy (EFFFL="Y") AND ITT (ITTFL="Y"); N=234 at Week 24
- **Model 1 (dose-response):** CHG ~ TRTPN + SITEGR1 + BASE, TRTPN continuous,
  Type III SS (Source: pilot5-helper-fcns.r — efficacy_models())
- **Model 2 (pairwise):** CHG ~ TRTPCD_F + SITEGR1 + BASE, TRTPCD_F factor levels:
  Xan_Hi, Xan_Lo, Pbo (reference) (Source: pilot5-helper-fcns.r)
- **LS means:** emmeans::lsmeans(model2, ~TRTPCD_F, weights="proportional")
  (Source: pilot5-helper-fcns.r)
- **Pairwise contrasts:** emmeans::contrast(lsm, method="pairwise", adjust=NULL) — unadjusted
  (Source: pilot5-helper-fcns.r)

**Core Model Variable Mapping (ADaM):**

| Variable Role | ADaM Variable | Dataset | Source |
|---|---|---|---|
| Endpoint variable | CHG, AVAL | ADADAS | adam-pilot-5.xlsx Variables sheet |
| Endpoint filter | PARAMCD="ACTOT", ANL01FL="Y", EFFFL="Y", ITTFL="Y" | ADADAS | tlf-primary.r; adam-pilot-5.xlsx |
| Treatment (continuous) | TRTPN | ADADAS | adam-pilot-5.xlsx |
| Treatment (categorical) | TRTP / TRTPCD_F | ADADAS | pilot5-helper-fcns.r |
| Treatment reference group | Pbo (TRTPN=0) — last in factor level order | ADADAS | pilot5-helper-fcns.r |
| Baseline covariate | BASE | ADADAS | adam-pilot-5.xlsx ADADAS.BASE method |
| Stratification / covariate | SITEGR1 | ADADAS | pilot5-helper-fcns.r; ADSL.SITEGR1 method |
| Subject variable | USUBJID | ADADAS/ADSL | adam-pilot-5.xlsx |
| Visit filter | AVISITN==24 (Week 24), AVISITN==0 (Baseline) | ADADAS | tlf-primary.r |

**Reviewer-side Python results (approximations — not reproduction of sponsor output):**

| | Placebo | Xan Low | Xan High |
|---|---|---|---|
| N (Week 24 analyzed) | 79 | 81 | 74 |
| Baseline Mean AVAL (SD) | 24.1 (12.2) | 24.4 (12.9) | 21.3 (11.7) |
| Week 24 Mean CHG (SD) | +2.54 (5.80) | +2.00 (5.55) | +1.47 (4.26) |
| LS Mean (approx.) | 2.495 | 2.028 | 1.489 |

| Comparison | Diff in LS Means | Dose-Response F | p (unadj.) |
|---|---|---|---|
| Xan Hi minus Pbo | -1.006 | 1.361 | 0.245 |
| Xan Lo minus Pbo | -0.467 | — | — |
| Xan Hi minus Xan Lo | -0.539 | — | — |

RMSE = 5.001. R2 = 0.095. LS means are reviewer-side approximations via proportional site
weighting; must be compared to sponsor emmeans output by human reviewer. Pairwise p-values
not computable without emmeans (not available in reviewer-side sandbox).

**Safety Endpoint — Time to First Dermatologic Event (KM)**

- **Dataset:** ADTTE (adtte.json) merged with ADSL; filter: SAFFL="Y", PARAMCD="TTDE"
- **Event coding:** CNSR=0 (event occurred), CNSR=1 (censored); Surv(AVAL, 1-CNSR)
  (Source: tlf-kmplot.r)
- **Time variable:** AVAL (days from treatment start to event/censoring)
  (Source: adam-pilot-5.xlsx ADTTE.AVAL)

| Arm | N | Events | Censored | KM Median Time (days) |
|---|---|---|---|---|
| Placebo | 86 | 29 (34%) | 57 | 139 |
| Xanomeline Low Dose | 84 | 62 (74%) | 22 | 29.5 |
| Xanomeline High Dose | 84 | 61 (73%) | 23 | 24.5 |

> KM medians are reviewer-side approximations. No formal log-rank test was specified in the
> available documents. Human review required to confirm whether this is a purely descriptive
> analysis.

### A3.2 Sponsor Program Traceability

All four output programs are explicitly mapped in ADRG Section 7.3 (pp. 13-14):

| Program | Output | Table / Figure |
|---|---|---|
| tlf-primary.r + pilot5-helper-fcns.r | tlf-primary-pilot5.rtf | Table 14-3.01 |
| tlf-efficacy.r | tlf-efficacy-pilot5.rtf | Table 14-3.02 |
| tlf-kmplot.r | tlf-kmplot-pilot5.pdf | Figure 14-1 |
| tlf-demographic.r | tlf-demographic-pilot5.out | Table 14-2.01 |

ADaM programs: adsl.r, adadas.r, adae.r, adlbc.r, adtte.r (Source: adrg.pdf, p. 12,
Section 7.2). Helper functions in pilot5-helper-fcns.r called by tlf-primary.r.

**Known discrepancy:** ADRG Appendix 2 documents differences between Pilot 5 and original
CDISC ADADAS for 19 subjects at ACTOT Week 8/16/24 (AVAL/CHG/PCHG differences due to
DTYPE=LOCF assignment errors in original CDISC data). Pilot 5 derivation is stated to be
the correct version. Impact on primary endpoint requires human evaluation (see IR-3).

---

## A4. Define File Assessment — Detail

As established in Table 3 above, define.xml is not present. The adam-pilot-5.xlsx file —
explicitly used by all five ADaM programs as the operative specification
(spec_to_metacore("adam-pilot-5.xlsx")) — provides the following coverage of define.xml v2.0
required elements for ADaM datasets:

| Define-XML v2.0 Element | xlsx Coverage | ADRG Coverage | Gap |
|---|---|---|---|
| Study-level metadata | Partial (Define sheet — name, description, standard, language) | Partial (Section 1.2 standards; Section 2.1 protocol title) | No formal OID/XML structure |
| Dataset-level metadata | Full (Datasets sheet — name, label, class, structure, keys, repeating, reference data) | Full (Section 5.2 — all 5 datasets described) | SDTM datasets not covered in xlsx |
| Variable-level metadata | Full for ADaM (Variables sheet — name, label, type, length, digits, format, mandatory, 100+ rows) | Partial (Section 3.1 — core variables with descriptions only) | SDTM variable metadata absent; some significant digits blank |
| Controlled terminology / codelists | Full for ADaM (Codelists sheet — ID, NCI code, type, terms, decoded values) | Partial (Section 1.2 — references only) | SDTM codelists not in xlsx; NCI codes partially populated |
| Value-level metadata | Full for ADADAS AVAL (ValueLevel sheet — 15 PARAMCD entries) | Partial (Section 5.2 — narrative) | ADLBC and ADTTE value-level entries absent |
| Computational methods | Full for ADaM (Methods sheet — 100+ derivation algorithms) | Partial (Sections 3.4, Appendix 2) | Narrative text only, not formal expressions; SDTM absent |
| External codelist references | Partial (Dictionaries sheet — MedDRA 8.0; NCI codes in Codelists) | Present (Section 1.2 — MedDRA 8.0, CDISC CT versions) | No formal href/URI links to external files |
| Document references | Present (Documents sheet — ADRG href=adrg.pdf) | Self-referential | No protocol or SAP reference (documents not submitted) |
| Origin metadata | Full for ADaM (Variables sheet — Origin + Predecessor columns for all variables) | Partial (Section 3.2 — treatment variable traceability) | Some entries blank; CRF page references N/A |
| Comments / developer notes | Present (Comments sheet — ADADAS window variables only) | Full (Appendix 2 — extensive QC notes and explanations) | Comments limited to ADADAS window variables in xlsx |

**Summary:** 6 of 10 define.xml v2.0 elements are fully covered for ADaM by adam-pilot-5.xlsx
alone. Combined with the ADRG, meaningful coverage exists for 8 of 10 elements. The two most
significant remaining gaps are: (1) complete absence of SDTM variable and codelist metadata,
and (2) incomplete value-level metadata for ADLBC and ADTTE. Whether this combined coverage
constitutes a sufficient define.xml substitute is a human policy determination.

---

## A5. Data Quality Findings

### ADaM Datasets — Reviewer-Side Verification Results

| Check | Finding | Assessment |
|---|---|---|
| Record count vs. declared (all 5 ADaM) | All match | Pass |
| Missing values — ADSL key variables | 0 missing in all key variables | Pass |
| Missing values — ADTTE key variables | 0 missing in all key variables | Pass |
| Missing values — ADADAS (AVAL) | 25 records (0.20%) | Flag — confirm source-driven |
| Missing values — ADADAS (BASE) | 22 records (0.18%) | Flag — confirm source-driven |
| Missing values — ADADAS (CHG, ANL01FL, DTYPE) | Expected — null at baseline, outside windows, non-LOCF records | Pass |
| Subject count consistency | ADSL=254, ADADAS=254, ADLBC=254, ADTTE=254; ADAE=225 (expected) | Pass |
| Population flag consistency | 0 flag inconsistencies across all checks | Pass |
| CHG = AVAL minus BASE (ACTOT, non-baseline) | 0 mismatches across 786 records; max diff = 0.000 | Pass |
| LOCF counts (ACTOT) | 818 non-LOCF + 222 LOCF = 1,040 total; matches ADRG exactly. 99/234 (42%) at Week 24 are LOCF. | Pass / Flag — 42% LOCF |
| Merge key integrity (USUBJID cross-dataset) | 0 orphaned records across all 5 ADaM datasets | Pass |
| PARAMCD codelist — ADADAS, ADTTE | 0 unexpected, 0 missing vs. adam-pilot-5.xlsx codelists | Pass |
| PARAMCD codelist — ADLBC | 18 underscore-prefixed PARAMCDs in codelist but absent from submitted data | Flag — see IR-4 |
| CNSR coding validity (ADTTE) | CNSR=0: 152 events, CNSR=1: 102 censored; all AVAL > 0 | Pass |

### SDTM Datasets — Reviewer-Side Verification Results

| Check | Domains | Finding | Assessment |
|---|---|---|---|
| Record count vs. declared | All 21 | All 21 datasets match declared counts | Pass |
| USUBJID vs. DM | 15 subject-level domains | 0 USUBJIDs in any domain not found in DM | Pass |
| Required variables present | DM, AE, EX, DS, LB, QS, VS, MH, SV | All required SDTM-IG variables present in all checked domains | Pass |
| Missing values — DM (RFSTDTC/RFENDTC) | DM | 52 missing = exactly the 52 screen failures (expected) | Pass |
| Missing values — EX (EXENDTC) | EX | 6 missing (1.0%) | Flag — confirm derivation handling |
| Screen failure handling | DM to ADSL | 52 screen failures correctly excluded from ADSL; 0 non-screen-failures absent | Pass |
| QS ACTOT source records | QS | 818 QSTESTCD=ACTOT records across 254 subjects; matches ADRG Appendix 2 exactly | Pass |

**Items flagged for human follow-up:**
1. ADADAS: 25 missing AVAL / 22 missing BASE — confirm source-driven, not processing artifact
2. ADADAS: 42% LOCF at Week 24 — sensitivity analysis absence is a material concern
3. ADLBC: 18 underscore-prefixed PARAMCDs absent from submitted data (see IR-4)
4. EX: 6 missing EXENDTC — confirm handled correctly in ADSL TRTEDT derivation
5. Planned N=300 vs. actual N=254 — reconciliation not explicitly addressed in ADRG

---
---

# Appendix 2: Python Code — Translation of Submitted R Analysis Programs

> **Mandatory Disclaimer:** All code in this appendix is AI-inferred reviewer-side verification
> code. Sponsor-submitted analysis program code (R) was NOT used to generate any of the Python
> code below. This code was executed in a sandboxed reviewer-side environment and results are
> approximations only — it was not executed or validated against Sponsor results in a production
> environment. Human technical review is required before any use. This code does not constitute
> evidence of Sponsor program adequacy, dataset adequacy, or analysis reproducibility.

**R programs translated:**
- tlf-primary.r — primary analysis filter, descriptive statistics, model calls (Table 14-3.01)
- pilot5-helper-fcns.r — efficacy_models() function: dose-response F-test, categorical ANCOVA,
  LS means, pairwise contrasts
- tlf-efficacy.r — GLUC ANCOVA at Week 20 (Table 14-3.02)
- tlf-kmplot.r — Kaplan-Meier analysis of time to first dermatologic event (Figure 14-1)

**Key translation decisions:**
- lm() with options(contrasts=c("contr.sum","contr.poly")) translated to numpy/scipy OLS
  with sum-coding (deviation coding) design matrix, implemented via scipy.linalg.lstsq
- emmeans::lsmeans(..., weights="proportional") translated to Python proportional
  site-weight marginal mean computation
- emmeans::contrast(..., adjust=NULL) translated to manual pairwise differences from LS means
- drop1(..., test="F") translated to partial F-test via RSS comparison between full and
  reduced models
- ggsurvfit::survfit2(Surv(AVAL, 1-CNSR) ~ TRT01A) translated to reviewer-side KM median
  estimator in pure Python

**Executed results summary:**

| Output | Value |
|---|---|
| Week 24 N analyzed | Placebo=79, Xan Low=81, Xan High=74 |
| Dose-response F-statistic | 1.361 |
| Dose-response p-value | 0.245 |
| LS Mean — Placebo (approx.) | 2.495 |
| LS Mean — Xan Low (approx.) | 2.028 |
| LS Mean — Xan High (approx.) | 1.489 |
| Xan Hi minus Pbo (diff) | -1.006 |
| Xan Lo minus Pbo (diff) | -0.467 |
| Xan Hi minus Xan Lo (diff) | -0.539 |
| Primary RMSE | 5.001 |
| KM median — Placebo | 139 days |
| KM median — Xan Low | 29.5 days |
| KM median — Xan High | 24.5 days |
| GLUC ANCOVA RMSE | 1.303 |

**Not computable in reviewer-side sandbox (emmeans not available):**
- SE and 95% CI for LS means
- Pairwise p-values for primary ANCOVA
- LS means table for GLUC ANCOVA (Table 14-3.02)
- KM confidence intervals and log-rank test

The full annotated Python code follows on the next page.


```python

# ===========================================================================
# AI INFERRED REVIEWER-SIDE PYTHON VERIFICATION CODE
# Translated from R programs: tlf-primary.r, pilot5-helper-fcns.r,
#   tlf-efficacy.r, tlf-kmplot.r
# Sponsor-submitted analysis program code was NOT used to generate this code.
# This code was not executed or validated against Sponsor results.
# Human technical review is required before use.
# ANCOVA implemented via numpy least-squares (scipy.linalg.lstsq) with
# dummy-coded design matrices (sum/deviation coding = contr.sum equivalent).
# ===========================================================================

import json
import io
import pandas as pd
import numpy as np
from scipy import stats
from scipy.linalg import lstsq

# ---------------------------------------------------------------------------
# Helper: parse CDISC Dataset-JSON and coerce numerics
# ---------------------------------------------------------------------------
def parse_dsj(path):
    raw = read_room_text(path)
    data = json.loads(raw)
    rows = data.get('rows', None)
    cols = [item['name'] for item in data.get('columns', [])]
    if rows is not None and cols:
        df = pd.DataFrame(rows, columns=cols)
        for c in df.columns:
            df[c] = pd.to_numeric(df[c], errors='ignore')
        return df
    return None

# ---------------------------------------------------------------------------
# OLS helper returning coefficients, residuals, R2, F-stat for a submodel drop
# ---------------------------------------------------------------------------
def ols_fit(X, y):
    """Return (coef, fitted, resid, ssr) via least squares."""
    coef, res, rank, sv = lstsq(X, y)
    fitted = X @ coef
    resid  = y - fitted
    ssr    = float(np.sum(resid**2))
    return coef, fitted, resid, ssr

def f_test_drop(ssr_full, ssr_red, df_num, df_den):
    f = ((ssr_red - ssr_full) / df_num) / (ssr_full / df_den)
    p = float(stats.f.sf(f, df_num, df_den))
    return float(f), p

# ---------------------------------------------------------------------------
# Sum/deviation coding helper (contr.sum equivalent)
# For k levels, returns k-1 columns; last level = -1 on all.
# ---------------------------------------------------------------------------
def sum_coding(series):
    levels = sorted(series.unique())
    k = len(levels)
    dummies = pd.DataFrame(index=series.index)
    for lev in levels[:-1]:  # drop last
        dummies[lev] = (series == lev).astype(float)
    # last level gets -1 on all columns
    for lev in levels[:-1]:
        dummies.loc[series == levels[-1], lev] = -1.0
    return dummies, levels

# ---------------------------------------------------------------------------
# Load datasets
# ---------------------------------------------------------------------------
adsl   = parse_dsj('adsl.json')
adadas = parse_dsj('adadas.json')
adlbc  = parse_dsj('adlbc.json')
adtte  = parse_dsj('adtte.json')

for col in ['AVAL','CHG','BASE','TRTPN','AVISITN']:
    for df in [adadas, adlbc]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
for col in ['AVAL','CNSR']:
    if col in adtte.columns:
        adtte[col] = pd.to_numeric(adtte[col], errors='coerce')

# ===========================================================================
# TABLE 14-3.01  Primary ANCOVA
# Filter: EFFFL/ITTFL/PARAMCD=ACTOT/ANL01FL  Week 24
# ===========================================================================
trt_map = {0.0:'Placebo', 54.0:'Xanomeline Low Dose', 81.0:'Xanomeline High Dose'}

adas_prim = adadas[
    (adadas['EFFFL']   == 'Y') &
    (adadas['ITTFL']   == 'Y') &
    (adadas['PARAMCD'] == 'ACTOT') &
    (adadas['ANL01FL'] == 'Y')
].copy()

adas_bl   = adas_prim[adas_prim['AVISITN'] == 0].copy()
adas_wk24 = adas_prim[adas_prim['AVISITN'] == 24].dropna(
    subset=['CHG','BASE','TRTPN','SITEGR1']
).copy()

adas_bl['TRT_label']   = adas_bl['TRTPN'].map(trt_map)
adas_wk24['TRT_label'] = adas_wk24['TRTPN'].map(trt_map)

# --- Descriptive ---
bl_desc   = adas_bl.groupby('TRT_label')['AVAL'].agg(['count','mean','std']).round(2)
wk24_desc = adas_wk24.groupby('TRT_label')[['AVAL','CHG']].agg(
    ['count','mean','std']
).round(2)

# --- Model 1: dose-response (TRTPN continuous) ---
site_dummies1, site_levs = sum_coding(adas_wk24['SITEGR1'].astype(str))
X1_full = np.column_stack([
    np.ones(len(adas_wk24)),
    adas_wk24['TRTPN'].values,
    site_dummies1.values,
    adas_wk24['BASE'].values
])
X1_red = np.column_stack([
    np.ones(len(adas_wk24)),
    site_dummies1.values,
    adas_wk24['BASE'].values
])
y = adas_wk24['CHG'].values.astype(float)
n = len(y)
p_full = X1_full.shape[1]

coef1f, fit1f, res1f, ssr1f = ols_fit(X1_full, y)
coef1r, fit1r, res1r, ssr1r = ols_fit(X1_red,  y)
df_den_m1 = n - p_full
F_dose, p_dose = f_test_drop(ssr1f, ssr1r, 1, df_den_m1)
rmse_m1 = float(np.sqrt(ssr1f / df_den_m1))

# --- Model 2: categorical treatment (sum coding) ---
trt_dummies, trt_levs = sum_coding(adas_wk24['TRT_label'])
site_dummies2, _      = sum_coding(adas_wk24['SITEGR1'].astype(str))
X2 = np.column_stack([
    np.ones(len(adas_wk24)),
    trt_dummies.values,
    site_dummies2.values,
    adas_wk24['BASE'].values
])
coef2, fit2, res2, ssr2 = ols_fit(X2, y)
rmse_m2 = float(np.sqrt(np.mean(res2**2)))

# SS total for R2
sst = float(np.sum((y - np.mean(y))**2))
r2  = round(1 - ssr2/sst, 4)

# --- LS means (proportional site weighting, mean BASE) ---
mean_base  = float(adas_wk24['BASE'].mean())
site_props = adas_wk24['SITEGR1'].astype(str).value_counts(normalize=True)

ls_means_dict = {}
for trt in ['Placebo','Xanomeline Low Dose','Xanomeline High Dose']:
    weighted_preds = []
    for site, weight in site_props.items():
        # Build single-row design vector
        trt_row  = trt_dummies.loc[adas_wk24.index[0]].copy() * 0  # zero row
        site_row = site_dummies2.loc[adas_wk24.index[0]].copy() * 0
        for col in trt_dummies.columns:
            if col == trt:
                trt_row[col] = 1.0
            elif trt == trt_levs[-1]:  # last level = -1
                trt_row[col] = -1.0
        for col in site_dummies2.columns:
            if col == site:
                site_row[col] = 1.0
            elif site == sorted(adas_wk24['SITEGR1'].astype(str).unique())[-1]:
                site_row[col] = -1.0
        x_row = np.concatenate([[1.0], trt_row.values, site_row.values, [mean_base]])
        weighted_preds.append(weight * float(x_row @ coef2))
    ls_mean = sum(weighted_preds)
    n_trt   = int((adas_wk24['TRT_label'] == trt).sum())
    ls_means_dict[trt] = {'n': n_trt, 'ls_mean': round(ls_mean, 3)}

pw = {
    'Xan_Hi - Pbo':    round(ls_means_dict['Xanomeline High Dose']['ls_mean'] - ls_means_dict['Placebo']['ls_mean'], 3),
    'Xan_Lo - Pbo':    round(ls_means_dict['Xanomeline Low Dose']['ls_mean']  - ls_means_dict['Placebo']['ls_mean'], 3),
    'Xan_Hi - Xan_Lo': round(ls_means_dict['Xanomeline High Dose']['ls_mean'] - ls_means_dict['Xanomeline Low Dose']['ls_mean'], 3),
}

# ===========================================================================
# TABLE 14-3.02  GLUC ANCOVA at Week 20
# Filter: ITTFL=="Y", TRTPN in (0,81), PARAMCD=="GLUC", AVISITN==20
# Model: CHG ~ BASE + TRTPN_adj  (Placebo TRTPN=0 recoded to 99)
# ===========================================================================
for col in ['TRTPN','AVISITN','CHG','BASE','AVAL']:
    if col in adlbc.columns:
        adlbc[col] = pd.to_numeric(adlbc[col], errors='coerce')

itt_subj = adsl[adsl['ITTFL'] == 'Y'][['STUDYID','USUBJID']].copy()
adlb1 = adlbc.merge(itt_subj, on=['STUDYID','USUBJID'], how='inner')
adlb1 = adlb1[
    (adlb1['TRTPN'].isin([0.0, 81.0])) &
    (adlb1['PARAMCD'] == 'GLUC') &
    (adlb1['AVISITN'].notna())
].copy()
adlb1['TRTPN_adj'] = adlb1['TRTPN'].apply(lambda x: 99.0 if x == 0.0 else x)

gluc_wk20 = adlb1[adlb1['AVISITN'] == 20].dropna(subset=['CHG','BASE','TRTPN_adj']).copy()
Xg = np.column_stack([
    np.ones(len(gluc_wk20)),
    gluc_wk20['BASE'].values.astype(float),
    gluc_wk20['TRTPN_adj'].values.astype(float)
])
yg = gluc_wk20['CHG'].values.astype(float)
coefg, fitg, resg, ssrg = ols_fit(Xg, yg)
gluc_rmse = float(np.sqrt(np.mean(resg**2)))

gluc_bl_stats   = adlb1[adlb1['AVISITN'] == 0].groupby('TRTPN_adj')['AVAL'].agg(
    ['count','mean','std']
).round(3)
gluc_wk20_stats = gluc_wk20.groupby('TRTPN_adj')[['AVAL','CHG']].agg(
    ['count','mean','std']
).round(3)

# ===========================================================================
# KM SUMMARY: ADTTE PARAMCD=="TTDE", SAFFL=="Y"
# Event: CNSR==0, Censored: CNSR==1
# ===========================================================================
anl_tte   = adsl[adsl['SAFFL'] == 'Y'][['STUDYID','USUBJID','TRT01A']].copy()
adtte_sub = adtte[
    (adtte['PARAMCD'] == 'TTDE') &
    (adtte['STUDYID'] == 'CDISCPILOT01')
][['STUDYID','USUBJID','AVAL','CNSR']].copy()
anl = anl_tte.merge(adtte_sub, on=['STUDYID','USUBJID'])
tte_sum = anl.groupby('TRT01A').agg(
    n_total    =('USUBJID','count'),
    n_events   =('CNSR', lambda x: int((x == 0).sum())),
    n_censored =('CNSR', lambda x: int((x == 1).sum())),
    median_time=('AVAL','median')
).round(2)

# ===========================================================================
# DEMOGRAPHICS
# ===========================================================================
adsl_itt = adsl[
    (adsl['STUDYID'] == 'CDISCPILOT01') &
    (adsl['ITTFL']   == 'Y')
].copy()
for col in ['AGE','HEIGHTBL','WEIGHTBL','BMIBL','MMSETOT']:
    adsl_itt[col] = pd.to_numeric(adsl_itt[col], errors='coerce')

demo_num     = adsl_itt.groupby('TRT01P')[['AGE','HEIGHTBL','WEIGHTBL','BMIBL','MMSETOT']].agg(
    ['count','mean','std']
).round(2)
demo_race    = adsl_itt.groupby(['TRT01P','RACE']).size().unstack(fill_value=0)
demo_age_grp = adsl_itt.groupby(['TRT01P','AGEGR1']).size().unstack(fill_value=0)
n_itt        = adsl_itt.groupby('TRT01P').size().to_dict()

results = {
    # Primary
    'primary_filter_n':  len(adas_prim),
    'wk24_analyzed_n':   len(adas_wk24),
    'n_per_trt_wk24':    adas_wk24.groupby('TRT_label').size().to_dict(),
    'bl_mean':           bl_desc['mean'].to_dict(),
    'bl_sd':             bl_desc['std'].to_dict(),
    'bl_n':              bl_desc['count'].to_dict(),
    'wk24_chg_n':        wk24_desc['CHG']['count'].to_dict(),
    'wk24_chg_mean':     wk24_desc['CHG']['mean'].to_dict(),
    'wk24_chg_sd':       wk24_desc['CHG']['std'].to_dict(),
    'dose_response_F':   round(F_dose, 4),
    'dose_response_p':   round(p_dose, 4),
    'ls_means':          ls_means_dict,
    'pairwise_diffs':    pw,
    'primary_rmse':      round(rmse_m2, 4),
    'model2_r2':         r2,
    'model2_n':          n,
    # GLUC
    'gluc_wk20_n':       len(gluc_wk20),
    'gluc_coef_BASE':    round(float(coefg[1]), 4),
    'gluc_coef_TRTPN':   round(float(coefg[2]), 4),
    'gluc_rmse':         round(gluc_rmse, 4),
    'gluc_bl_n':         gluc_bl_stats['count'].to_dict(),
    'gluc_bl_mean':      gluc_bl_stats['mean'].to_dict(),
    'gluc_wk20_chg_n':   gluc_wk20_stats['CHG']['count'].to_dict(),
    'gluc_wk20_chg_mean':gluc_wk20_stats['CHG']['mean'].to_dict(),
    'gluc_wk20_chg_sd':  gluc_wk20_stats['CHG']['std'].to_dict(),
    # KM
    'tte_n_total':       tte_sum['n_total'].to_dict(),
    'tte_n_events':      tte_sum['n_events'].to_dict(),
    'tte_n_censored':    tte_sum['n_censored'].to_dict(),
    'tte_median_time':   tte_sum['median_time'].to_dict(),
    # Demographics
    'n_itt_per_trt':     n_itt,
    'age_mean':          demo_num['AGE']['mean'].to_dict(),
    'age_sd':            demo_num['AGE']['std'].to_dict(),
    'race_counts':       demo_race.to_dict(),
    'agegrp_counts':     demo_age_grp.to_dict(),
}

```

---

*End of Report*

*Elsa — FDA AI Assistant — 2026-11-25*
*All findings are AI-assisted draft outputs. Human expert review and verification is required before use in any regulatory determination.*