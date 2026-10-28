---
study: CDISCPILOT01 (R Consortium R Submission Pilot 1)
date: 2026-10-27
reviewer: Claude (statistical-reviewer skill)
skill: statistical-reviewer
datasets_reviewed: [m1/us/cover-letter.pdf, m1/us/report-tlf.pdf, m1/us/response-to-fda-1.pdf, adsl.xpt, adadas.xpt, adcibc.xpt, adae.xpt, adtte.xpt, adlbc.xpt, adlbcpv.xpt, adlbh.xpt, adlbhpv.xpt, adlbhy.xpt, adnpix.xpt, advs.xpt, adrg.pdf, define.xml, programs/tlf-demographic.r, programs/tlf-primary.r, programs/tlf-efficacy.r, programs/tlf-kmplot.r, programs/r0pkg.txt (pilot1wrappers 0.1.1)]
realism_score: 7/10
findings_count: 3 High, 8 Medium, 5 Low
overall_result: PASS WITH FINDINGS
---

# Statistical Review Report: CDISCPILOT01 (R Consortium Submissions Pilot 1)

## Study overview

CDISCPILOT01 is a prospective, randomized, multi-center, double-blind, placebo-controlled, parallel-group study of transdermal xanomeline (Low Dose, 54 mg; High Dose, 81 mg) versus placebo in mild to moderate Alzheimer's disease. Treatment lasted 26 weeks (ADRG §2.2). The ADRG names two primary efficacy endpoints: ADAS-Cog(11) (ADADAS) and CIBIC+ (ADCIBC). 254 subjects were randomized and treated (Placebo 86, Low 84, High 84). The submitted package has four outputs:

- Table 14-2.01: demographics.
- Table 14-3.01: ADAS-Cog(11) change from baseline to Week 24, LOCF ANCOVA. Not significant: High−Placebo −1.0 (SE 0.84), p=0.233; Low−Placebo −0.5 (0.82), p=0.569; dose-response p=0.245.
- Table 14-3.02: glucose ANCOVA at Week 20. High−Placebo 0.07, p=0.822.
- Figure 14-1: Kaplan-Meier (KM) plot of time to first dermatologic adverse event, which shows a large excess in both xanomeline arms.

No data cutoff date is stated anywhere in the package. The study is complete: treatment start dates run from 2012-07-09 to 2014-09-02. This is the public CDISC pilot synthetic/test dataset. As instructed, it is reviewed as if it were real submission data.

## Review scope

| Layer | Provided | Reviewed |
|---|---|---|
| TLF | report-tlf.pdf (4 outputs, all embedded images; rendered and read visually) | Yes. Every numeric cell of Tables 14-2.01, 14-3.01, 14-3.02 and the Figure 14-1 risk table was compared against ADaM |
| ADaM | 12 .xpt datasets | Yes. Population flags, endpoint derivations (ACTOT, EFFFL, LOCF, TRTEMFL, CQ01NAM, AOCC01FL, ADTTE), safety reconciliation, exposure, realism |
| Metadata | define.xml (v2.0), adrg.pdf | Yes. Derivation methods were checked against the data |
| Programs | 4 TLF R programs + pilot1wrappers (r0pkg.txt) | Read in full. Models were re-implemented independently (R 4.5.2: haven, dplyr, emmeans, survival). The sponsor programs were not executed |
| SDTM | **Not provided** | Not possible |
| SAP / Protocol / CSR | **Not provided** | Not possible |

The review layer is **TLF + ADaM**. The reviewer's scratch code (R scripts `01_explore.R` to `18_sd.R`) is not included in this repository.

## Population registry

| Population | Definition (define.xml / ADRG) | Placebo | Xan Low | Xan High | Total | Consistent with TLFs? |
|---|---|---:|---:|---:|---:|---|
| Screened | Not available (no SDTM DM/DS) | – | – | – | – | n/a |
| Randomized / ITT (ITTFL) | ARMCD not blank | 86 | 84 | 84 | 254 | Yes (Table 14-2.01 header) |
| Safety (SAFFL) | ITTFL=Y and TRTSDT not missing | 86 | 84 | 84 | 254 | Yes (Figure 14-1 at-risk row at t=0) |
| Efficacy (EFFFL) | SAFFL=Y and at least one post-baseline ADAS-Cog **and** at least one post-baseline CIBIC+ (QS VISITNUM>3) | 79 | 81 | 74 | 234 | Yes (Table 14-3.01 header). Rule re-derived exactly: 234/234 |
| Excluded from EFFFL | – | 7 | 3 | 10 | 20 | 19 had no post-baseline ADAS-Cog; 1 (01-709-1007) had no post-baseline CIBIC+ |
| Completers Week 24 (COMP24FL) | SV visit 12 attended | 60 | 28 | 30 | 118 | Not used in TLFs |
| Completed study (EOSSTT) | – | 58 | 25 | 27 | 110 | Not used in TLFs |
| Discontinued due to AE (DSRAEFL / DCDECOD) | – | 8 | 44 | 40 | 92 | No disposition TLF |
| Deaths (DTHFL = DCDECOD "DEATH" = AESDTH) | – | 2 | 1 | 0 | 3 | No death TLF. Reconciled across ADSL/ADAE |
| Glucose Week 20 evaluable (ITT, ADLBC) | Observed Week 20 value | 65 | – | 31 | 96 | Yes (Table 14-3.02) |

## Denominator registry

| Output | Population used | Header / reported N (P / L / H) | Reproduced N | Difference | Notes |
|---|---|---|---|---:|---|
| Table 14-2.01 Demographics | ITT | 86 / 84 / 84 | 86 / 84 / 84 | 0 | Weight and BMI are based on n=83 in Low Dose (01-702-1082 missing). This is not displayed (TLF-14-2.01-001) |
| Table 14-3.01 ADAS-Cog Wk 24 | EFFFL & ITTFL & ANL01FL | 79 / 81 / 74 (n at baseline, Wk 24, CHG) | 79 / 81 / 74 | 0 | 79 of 234 Week 24 values are LOCF-imputed (TLF-14-3.01-001) |
| Table 14-3.02 Glucose Wk 20 | ITT, TRTPN in (0,81) | Baseline 86 / – / 84; Wk 20 65 / – / 31 | Same | 0 | Baseline column covers all ITT, not "observable at Baseline and Week 20" as footnote a says (TLF-14-3.02-001) |
| Figure 14-1 KM TTDE | SAFFL | At risk at t=0: 86 / 84 / 84 | 86 / 84 / 84 | 0 | All 33 at-risk cells reproduce exactly |
| CIBIC+ Wk 24 (no TLF) | EFFFL & ANL01FL | not reported | 79 / 81 / 74 | – | Co-primary endpoint not presented (TLF-CIBIC-001) |

**Missing-data / ICE registry (primary-type endpoints)**

| Endpoint | N evaluable (P/L/H) | Imputed or missing at analysis visit (P / L / H) | Flag? | Handling |
|---|---|---|---|---|
| ADAS-Cog Wk 24 | 79 / 81 / 74 | LOCF 14 (17.7%) / 32 (39.5%) / 33 (44.6%) | Yes: >15% in all arms; arm difference >20 points | LOCF (DTYPE). Off-treatment observed values retained (ADAM-ADADAS-001) |
| CIBIC+ Wk 24 | 79 / 81 / 74 | LOCF 13 (16.5%) / 34 (42.0%) / 34 (45.9%) | Yes | LOCF |
| Glucose Wk 20 | 86 / – / 84 ITT | Missing 21 (24.4%) / – / 53 (63.1%) | Yes | Observed case only (titled "LOCF") |
| TTDE | 86 / 84 / 84 | Censored 57 / 22 / 23 | AE-discontinuation censoring 2 / 12 / 10 | Censored at RFENDT |

**Model registry**

| Output | Model (program) | Reproduced? |
|---|---|---|
| 14-3.01 dose-response | `lm(CHG ~ TRTPN + SITEGR1 + BASE)`, Type III F-test (contr.sum) | Yes. p=0.2447 vs reported 0.245 |
| 14-3.01 pairwise | `lm(CHG ~ TRT factor + SITEGR1 + BASE)`, emmeans proportional weights, t-based CIs, unadjusted | Yes, all 9 cells |
| 14-3.02 | `lm(CHG ~ BASE + TRTPN)` (2 arms), emmeans; difference CI uses z=1.96 | Yes, all cells (TLF-14-3.02-002) |
| Figure 14-1 | visR::estimate_KM (survfit), no HR/test displayed | KM and at-risk counts reproduced exactly |

**Multiplicity registry:** No SAP was provided. The ADRG describes two primary endpoints (ADAS-Cog, CIBIC+). Table 14-3.01 reports two dose-vs-placebo comparisons plus a dose-response test with "p-values without adjustment for multiple comparisons." No testing hierarchy or alpha allocation is documented. No result is nominally significant, so there is no over-claim, but the confirmatory strategy cannot be assessed (TLF-CIBIC-001).

## Data realism assessment

**Overall realism score: 7/10.** The data is realistic, with a few systematic artifacts. The package states that the data comes from the public CDISC pilot (CDISCPILOT01), which is known to be synthetic/test data. As instructed, realism concerns are reported in the main Findings as potential integrity issues.

### Realistic features
| Feature | Evidence |
|---|---|
| Physiological correlations | SBP–DBP r=0.50; Height–Weight r=0.63; Weight–BMI r=0.78; ALT–AST r=0.70; Hgb–Hct r=0.88; Hgb–RBC r=0.80; Na–Cl r=0.56; Creatinine–BUN r=0.48; Age–SBP r=0.25 |
| Clinically coherent instrument correlation | Baseline MMSE vs ADAS-Cog(11) r = −0.83; ADAS-Cog vs disease duration r=0.17 |
| Sex dimorphism | Mean height F 157 / M 173 cm; weight F 59.4 / M 75.9 kg |
| Non-spherical baseline structure | PCA on 7 baseline variables: first two PCs explain 27.5% and 22.6% (structured, not equal) |
| Site heterogeneity | Kruskal-Wallis across SITEGR1: MMSE p=0.0002, ADAS-Cog p=0.0001, Age p=0.0003; Weight p=0.13 |
| Blocked randomization within site | Arm counts within each of the 11 site groups differ by at most 1 |
| Staggered enrollment | 26-month enrollment; site start dates staggered (e.g., 701: 2012-07-22 to 2014-07-01) |
| Visit-timing jitter | ADAS-Cog observed Week 8/16/24 deviation from target: SD 13.5 / 5.7 / 15.3 days; 48 / 29 / 36 unique study days |
| Manual-BP digit preference | Terminal digit 0 in 36.8% of BPs; even digits dominate (as expected for manual sphygmomanometry) |
| AE onset continuity | 156 unique onset days (max 194); 13.8% on multiples of 7 (close to the 1/7 expected by chance) |
| Drug-class AE pattern | Application-site and skin AEs show a clear excess (pruritus 8/21/26; application-site pruritus 6/22/22; application-site erythema 3/12/15 subjects P/L/H). Dermatologic onset median 33–34 days on active vs 74 days on placebo |
| Plausible severity distribution | TEAE records 64.9% mild, 31.4% moderate, 3.6% severe |
| Placebo background AEs | Placebo has 65/86 subjects with any TEAE; diarrhoea 9, pruritus 8, erythema 8 |
| Differential dropout | AE discontinuation 8 / 44 / 40, consistent with the tolerability signal. Discontinuation days vary (28–50 unique values per arm) |
| Informative missingness | Discontinuers have the AE profile expected (71/92 AE discontinuers had a dermatologic AE) |
| No copy-paste trajectories | 128 subjects with 4 observed ADAS-Cog values: 0 duplicated sequences |
| Proration and LOCF mechanics | ACTOT = sum of the 11 ADAS-Cog(11) items for 779/779 complete records. 20 records prorated as sum×70/max-possible. LOCF values equal the prior observed value (0 exceptions) |

### Unrealistic features
| Feature | Evidence | Severity | Recommendation |
|---|---|---|---|
| Visits evenly spread across weekdays, including weekends | ADVS visit dates: Sat 15.5%, Sun 14.3% (29.8% weekend). ADAS-Cog: 29.4% weekend. Treatment start on Sat/Sun for 77/254 (30.3%), close to the 2/7 = 28.6% expected under uniform dates | Medium (see XLAY-REAL-001) | Confirm whether dates were shifted or perturbed for de-identification. Provide source visit dates |
| Efficacy and vitals visits after the study-end date | 37 subjects have ADAS-Cog dated 28–266 days after RFENDT ("Date of Discontinuation/Completion") while EOSSTT=DISCONTINUED | High (ADAM-ADADAS-001) | See finding |
| Discordant seriousness coding | Fatal AEs coded non-serious; 36 TE records meet a seriousness criterion with AESER=N | High (ADAM-ADAE-001) | See finding |
| Very low weight/BMI values | BMI 13.7 (01-717-1109, M, 180 cm, 44.5 kg); 3 other subjects with BMI below 16 | Low | Plausible in frail elderly AD patients. Source verification advised |

### Implications
The core quantitative structure is coherent and the main analyses reproduce exactly: correlations, site effects, the dose-related tolerability signal, and the scoring and imputation mechanics. The weekend-date pattern and the post-discontinuation assessments would prompt a data-integrity query in a real submission. They do not change the efficacy conclusion (see sensitivity analyses). The data is suitable for its stated purpose, which is to test R-based submission and reproducibility.

## Findings — Data integrity

### High

### ADAM-ADADAS-001: Primary-endpoint assessments dated after subjects' study discontinuation date
- **Severity:** High
- **Type:** Traceability / Interpretability (estimand)
- **Dataset/Output:** ADADAS, ADCIBC, ADVS, ADNPIX vs ADSL (RFENDT, EOSSTT, DCDECOD); Table 14-3.01
- **Finding:** For 37 subjects, observed ADAS-Cog(11) assessments (DTYPE blank) are dated **after** ADSL.RFENDT ("Date of Discontinuation/Completion"), even though ADSL shows EOSSTT="DISCONTINUED" (DISCONFL="Did the Subject Discontinue the Study?"). These off-treatment values feed the Week 24 primary analysis directly. Other subjects who discontinued get LOCF from their last on-treatment visit. So the primary analysis mixes a treatment-policy approach (retrieved dropouts) with LOCF, and no estimand or intercurrent-event (ICE) strategy is documented.
- **Evidence:**
  - Post-baseline ACTOT records dated after RFENDT: 37 subjects (by study day: median 119 days after RFENDT, range 28–266).
  - The same pattern appears in ADCIBC (34 subjects), ADVS (36 subjects, 360 records) and ADNPIX (36 subjects). It barely appears in labs (ADLBC 4 subjects) and never in ADAE (0 AEs after RFENDT).
  - Reasons for discontinuation in these 37: Adverse Event 30 (Low 19, High 8, Placebo 3), withdrawal 3, other 4.
  - 38 EFFFL subjects have an observed "Week 24" value more than 14 days after their last dose. Example: 01-701-1181 (High Dose) took treatment for 5 days, then has an observed Week 24 ADAS-Cog on study day 170, about 5 months after RFENDT 2013-12-12. Example: 01-701-1023 (Placebo) has RFENDT 2012-09-02 and a Week 24 ADT of 2013-02-18.
  - Reviewer sensitivity analysis: an on-treatment hypothetical-style LOCF using only values ≤ last dose + 14 days (N=234). Results: High−Placebo −1.00 (SE 0.76, p=0.188); Low−Placebo −0.96 (SE 0.74, p=0.195); dose-response p=0.148. Reported: −1.0 (p=0.233), −0.5 (p=0.569), dose-response p=0.245.
- **Impact:** The conclusion is unchanged (no comparison is significant under either approach). However, the Low Dose estimate roughly doubles (−0.47 to −0.96), which shows the estimate depends on how off-treatment data is handled. The presence of efficacy data after a recorded study discontinuation is also a logical inconsistency between disposition and assessment data. This is exactly the issue a reviewer must resolve before accepting the disposition counts or the primary result.
- **Recommended follow-up:** Clarify whether these are retrieved-dropout visits (follow-up off treatment) or dating errors. If retrieved dropouts, correct RFENDT/EOSSTT semantics and state the estimand (treatment policy vs hypothetical) and the ICE handling. Add a sensitivity analysis that applies one strategy consistently.
- **traceability_path:** Table 14-3.01 Week 24 n → ADADAS (AVISITN=24, ANL01FL=Y, DTYPE blank, ADT) → ADSL.RFENDT / EOSSTT → (SDTM DS/SV not provided)
- **reviewer_question:** For the 37 subjects with ADAS-Cog assessments after their recorded discontinuation date, please confirm the source visit dates and the protocol basis for post-discontinuation efficacy follow-up, and state the intended estimand for Table 14-3.01.

### ADAM-ADAE-001: Seriousness flag (AESER) contradicts seriousness criteria, including all 3 fatal AEs
- **Severity:** High
- **Type:** Reproducibility / Traceability (safety)
- **Dataset/Output:** ADAE (AESER, AESDTH, AESHOSP, AESLIFE, AESDISAB, AESCAN, AEOUT)
- **Finding:** All three fatal AEs (AESDTH="Y", AEOUT="FATAL") have AESER="N". These are 01-701-1211 SUDDEN DEATH (Low), 01-704-1445 COMPLETED SUICIDE (Placebo) and 01-710-1083 MYOCARDIAL INFARCTION (Placebo). Overall, 36 treatment-emergent records meet at least one seriousness criterion but are coded AESER="N". Hospitalization alone accounts for 25 of them.
- **Evidence:** Subjects with a TEAE that has AESER="Y": Placebo 0, Low 1, High 2 (3 total). Subjects with a TEAE that meets any seriousness criterion: Placebo 6, Low 10, High 9 (25 total). Affected terms include syncope (5), hip fracture (3), myocardial infarction (3), transient ischaemic attack (3), atrial fibrillation (2), pneumonia (2) and malignant fibrous histiocytoma (2).
- **Impact:** Any SAE summary built from AESER would under-report SAEs about 8-fold (3 vs 25 subjects) and would show zero placebo SAEs despite 2 placebo deaths. This affects benefit-risk and labeling. No SAE table is in the package, but ADAE is submitted as the analysis source for safety.
- **Recommended follow-up:** Re-derive AESER from the seriousness criteria (or reconcile against SDTM AE). Confirm that every death is serious. Provide an SAE reconciliation listing.
- **reported_value / expected_value:** SAE subjects (AESER) 0 / 1 / 2 vs criteria-based 6 / 10 / 9.

### XLAY-DISC-001: AE-related discontinuations cannot be traced to a causal AE (AEACN never populated)
- **Severity:** High
- **Type:** Traceability
- **Dataset/Output:** ADAE.AEACN vs ADSL.DSRAEFL / DCDECOD
- **Finding:** AEACN (action taken with study treatment) is blank on all 1,191 ADAE records. So the 92 subjects who discontinued because of an AE (DSRAEFL="Y": Placebo 8, Low 44, High 40) cannot be linked to the AE(s) that caused discontinuation. This is the authoritative-source reconciliation defined in cross-layer workflow §4.7.
- **Evidence:** `table(adae$AEACN)` gives 1191 blank. Partial reassurance: DSRAEFL agrees exactly with DCDECOD="ADVERSE EVENT" (92/92), and all 92 subjects have at least one TEAE. 71 of the 92 had a dermatologic AE.
- **Impact:** An "AE leading to discontinuation" table cannot be produced or verified. That is a core tolerability measure here, given the 5-fold excess of AE discontinuations on active treatment.
- **Recommended follow-up:** Populate AEACN from SDTM AE (or provide a DS-to-AE linkage). Provide a discontinuation-due-to-AE listing by preferred term.

### Medium

### TLF-14-3.01-001: Heavy, differential LOCF imputation in the primary analysis; no missing-data sensitivity analysis provided
- **Severity:** Medium
- **Type:** Interpretability (potentially conclusion-impacting)
- **Dataset/Output:** Table 14-3.01; ADADAS (DTYPE="LOCF")
- **Finding:** 79 of 234 (33.8%) Week 24 values in the primary analysis are LOCF-imputed, and the share differs sharply by arm. ADAS-Cog worsens over time in this population (mean change +1.5 to +2.5). LOCF from Week 8 therefore systematically favors arms with early dropout, and early dropout was concentrated in the active arms (last observed visit Week 8: Placebo 7, Low 25, High 25).
- **Evidence:** Imputed at Week 24: Placebo 14/79 (17.7%), Low 32/81 (39.5%), High 33/74 (44.6%).
  - Observed-case reanalysis (N=155: 65/49/41): High−Placebo −0.65 (p=0.561), Low−Placebo −1.06 (p=0.320), dose-response p=0.416.
  - All-ITT rerun using the ADaM LOCF records (N=254): High−Placebo −1.05 (p=0.172), Low−Placebo −0.48 (p=0.529), dose-response p=0.183.
  - On-treatment LOCF (see ADAM-ADADAS-001): High−Placebo −1.00 (p=0.188).
- **Impact:** The null conclusion holds under every alternative tried. The point estimates move by up to 0.6 points, and LOCF is not an assumption-free method. No sensitivity analysis (MMRM, MI, tipping point) is presented.
- **Recommended follow-up:** Provide the SAP-specified missing-data sensitivity analyses (e.g., MMRM on observed data, reference-based MI). Report the number imputed per arm in the table.

### TLF-CIBIC-001: Co-primary endpoint CIBIC+ not reported; multiplicity strategy not documented
- **Severity:** Medium
- **Type:** Interpretability
- **Dataset/Output:** ADCIBC; ADRG §5.2.6–5.2.7; report-tlf.pdf
- **Finding:** The ADRG calls both ADAS-Cog and CIBIC+ "one of the primary efficacy endpoints," and EFFFL requires post-baseline CIBIC+. However, no CIBIC+ output is submitted. Table 14-3.02 is a glucose table. No multiplicity approach across the 2 endpoints × 2 doses (+ dose-response) is documented.
- **Evidence:** Independent CIBIC+ analysis at Week 24 (LOCF, EFFFL, ANL01FL; N=79/81/74):
  - Category distribution, scores 2/3/4/5/6: Placebo 1/9/38/28/3; Low 1/14/37/27/2; High 0/11/33/25/5. Means: 4.29 / 4.19 / 4.32.
  - ANOVA (treatment + SITEGR1, proportional weights): Low−Placebo −0.09 (95% CI −0.34, 0.16; p=0.489); High−Placebo +0.03 (−0.22, 0.29; p=0.799); dose-response p=0.960.
  - CMH general association by site group: Low vs Placebo p=0.860; High vs Placebo p=0.668.
  - Observed-case sensitivity analysis (N=66/47/40): High−Placebo +0.37 (p=0.025, nominal), dose-response p=0.077.
  - The direction of the CIBIC+ scale cannot be confirmed from the package (define.xml has no decode for AVAL).
- **Impact:** The second primary endpoint does not support efficacy, and its observed-case sensitivity analysis gives a nominally significant between-arm difference whose direction is undocumented. A reviewer cannot judge the overall efficacy claim without this endpoint and a stated multiplicity rule.
- **Recommended follow-up:** Submit the CIBIC+ primary table and the pre-specified analysis method. Document the decision rule for the two primary endpoints and the two doses. Add a CIBIC+ codelist to define.xml.

### TLF-14-3.02-001: Glucose table mislabeled as "Primary Endpoint Analysis … LOCF"; baseline column inconsistent with its footnote; large differential missingness undisclosed
- **Severity:** Medium
- **Type:** Interpretability
- **Dataset/Output:** Table 14-3.02; ADLBC (PARAMCD="GLUC"); tlf-efficacy.r
- **Finding:** (a) Glucose is a safety laboratory parameter, not a primary endpoint (the ADRG lists ADAS-Cog and CIBIC+). (b) ADLBC has no DTYPE variable and no LOCF records; the Week 20 analysis is observed-case only. (c) Footnote a says the table covers "participants who have observable data at Baseline and Week 20," but the Baseline column summarizes all ITT subjects (N=84/86), while the Week 20 and model columns use 31/65.
- **Evidence:** All numbers reproduce:
  - Baseline: 5.4 (1.34) N=84 High; 5.6 (2.14) N=86 Placebo.
  - Week 20: 5.8 (1.61) N=31; 5.8 (1.50) N=65. Change: 0.2 (1.47); 0.1 (2.08).
  - LS means 0.16 (−0.31, 0.63) and 0.09 (−0.23, 0.42). Difference 0.07 (−0.50, 0.63), p=0.822.
  - Missing Week 20 glucose among ITT: High 53/84 (63.1%) vs Placebo 21/86 (24.4%).
- **Impact:** A reader would think this is an imputed primary analysis on a consistent population. In fact 63% of the High Dose arm is missing. The result cannot support any claim of "no glucose effect."
- **Recommended follow-up:** Retitle the table (safety, observed case). Restrict the baseline column to the analysis set or fix the footnote. Show the number missing per arm. Use the safety population.

### ADAM-META-001: define.xml derivation methods for primary-endpoint variables are placeholders or incorrect
- **Severity:** Medium
- **Type:** Standard/metadata, Traceability
- **Dataset/Output:** define.xml (MethodDef)
- **Finding:** The method definitions for the variables that drive the primary analysis are non-informative or wrong:
  - MT.ADQSADAS.AVAL, BASE, CHG, ANL01FL, EFFFL, ABLFL, AWTARGET, ITTFL, PCHG: all read "LB.VISITNUM".
  - MT.ADQSCIBC.AVAL, DTYPE, ANL01FL, EFFFL: "LB.VISITNUM".
  - MT.ADADAS.AVAL and MT.ADADAS.DTYPE: "ADSL.USUBJID".
  - MT.ADLBC.AVAL, BASE, CHG, ANL01FL: "LB.LBSTNRHI".
  - MT.ADAE.AOCC01FL says "Subset to CQ01NAM=''". The data actually implements CQ01NAM non-missing; the reviewer re-derived AOCC01FL and it matched for 152/152 subjects.
  - No Analysis Results Metadata is included, although pilot1wrappers::efficacy_models cites "analysis results metadata for table 14-3.01."
  - The CIBIC+ AVAL has no codelist or decode.
- **Evidence:** See the reviewer's extract of define.xml methods (not included in this repository). The reviewer could reproduce ACTOT (11-item sum; prorated ×70/max-possible when items are missing), LOCF, ANL01FL selection (closest to target day) and EFFFL only by reverse-engineering the data.
- **Impact:** The primary endpoint derivation cannot be traced from the submitted metadata. That defeats the purpose of define.xml for an independent reviewer.
- **Recommended follow-up:** Replace the placeholder methods with the actual algorithms (windows, ANL01FL tie-breaking, LOCF rules, ACTOT item set and proration rule). Correct the AOCC01FL text. Add ARM for the four outputs.

### ADAM-ADRG-001: ADRG omits or misstates key analysis conventions
- **Severity:** Medium
- **Type:** Standard/metadata
- **Dataset/Output:** adrg.pdf §1.2, §3.3, §3.4, §5.2.1
- **Finding:** The ADRG has several gaps and errors:
  - §3.4 says "Imputation/Derivation Methods: Not applicable." The primary analysis uses LOCF (DTYPE), and ACTOT is prorated for 20 records with 8–10 of 11 items, including one with only 8 items (01-711-1012).
  - §5.2.1 lists only SAFFL and ITTFL as key population flags, but the primary analysis uses EFFFL, which is never defined in the ADRG.
  - §3.3 says windowing was used but does not give the windows. From the data: Baseline ≤ Day 1, Week 8 Days 2–84, Week 16 Days 85–140, Week 24 > Day 140 with no upper bound (observed Week 24 values up to Day 286).
  - The SITEGR1 pooling rule is not described (sites with small enrolment are pooled to "900").
  - §1.2 lists MedDRA v8.0 as the "Medications Dictionary."
- **Impact:** A reviewer reading the ADRG would not know the primary analysis is modified ITT with LOCF and prorated scores.
- **Recommended follow-up:** Update the ADRG to document EFFFL, visit windows, LOCF, proration rules and site pooling. Correct the dictionary entry.

### TLF-14-2.01-001: Demographic table omits sex and ethnicity, and does not show n for variables with missing data
- **Severity:** Medium
- **Type:** Interpretability
- **Dataset/Output:** Table 14-2.01; tlf-demographic.r (`vars` excludes SEX and ETHNIC)
- **Finding:** Sex and ethnicity are not summarized, although both are in ADSL and sex is unbalanced across arms. Weight and BMI for Low Dose are computed on 83 subjects (rtables silently drops the NA), but no n row is shown.
- **Evidence:**
  - Female: Placebo 53/86 (61.6%), Low 50/84 (59.5%), High 40/84 (47.6%); χ² p=0.14.
  - Hispanic or Latino: 3 / 6 / 3.
  - Low Dose weight mean 67.28 (14.12) and BMI 25.06 (4.27) reproduce only with n=83 (01-702-1082 has no baseline weight).
  - All displayed numbers reproduce exactly. Examples: Age 75.21 (8.59) / 75.67 (8.29) / 74.38 (7.89); Race White 78 / 78 / 74; MMSE 18.05 (4.27) / 17.87 (4.22) / 18.51 (4.16).
- **Impact:** A standard demographic variable is missing from the baseline table, and the denominator for weight and BMI is not disclosed.
- **Recommended follow-up:** Add sex and ethnicity. Add an n (or missing) row for each continuous variable.

### TLF-14-1-001: KM figure y-axis mislabeled, and no supporting time-to-event statistics
- **Severity:** Medium
- **Type:** Interpretability
- **Dataset/Output:** Figure 14-1; tlf-kmplot.r; ADTTE (PARAMCD="TTDE")
- **Finding:** The y-axis is labeled "Probability of event," but the curves plot the event-free (survival) probability: they start at 1.0 and decline. Read literally, the figure says Placebo has about a 63% probability of a dermatologic event, when the reproduced KM estimate is about 37% at Day 180. The figure also reports no event counts, medians, hazard ratio (HR) or test. The legend order (Placebo, High, Low) differs from the risk-table order (Placebo, Low, High).
- **Evidence:**
  - Reproduced from ADTTE (SAFFL): events 29 / 62 / 61; censored 57 / 22 / 23.
  - KM event-free probability at Day 180: 0.626 / 0.126 / 0.092, which matches the plotted plateaus.
  - Median time to event: not estimable (NE) / 33 days (95% CI 28–51) / 36 days (25–47).
  - Cox HR vs Placebo: Low 4.08 (2.59–6.42), High 4.92 (3.08–7.85). Log-rank p<0.001 for each comparison; 3-arm χ²=60.3, df=2. Proportional-hazards test p=0.32 / 0.39.
  - All 33 numbers-at-risk reproduce exactly (Placebo 86, 75, 65, 59, 50, 47, 45, 42, 40, 35, 0; Low 84, 58, 31, 20, 14, 12, 8, 6, 6, 5, 0; High 84, 48, 31, 14, 7, 4, 4, 4, 4, 3, 0).
- **Impact:** The mislabeled axis invites a reversed reading of a key safety (AESI) result.
- **Recommended follow-up:** Relabel the axis "Probability of no dermatologic event" (or plot 1−S(t)). Add a summary table with events, censoring, medians and HR with CI.

### XLAY-REAL-001: Visit and treatment-start dates spread evenly across all seven weekdays
- **Severity:** Medium
- **Type:** Traceability (realism / operational plausibility)
- **Dataset/Output:** ADSL.TRTSDT; ADVS/ADADAS ADT
- **Finding:** Outpatient visit dates show no weekday clustering. About 30% fall on Saturday or Sunday at every site, which is what uniformly random dates would produce and is atypical for clinic-based visits in a 26-week outpatient trial.
- **Evidence:** ADVS unique subject-visit dates: Sat 15.5%, Sun 14.3%, Mon 12.8%, Tue 12.9%, Wed 16.6%, Thu 14.5%, Fri 13.4%. ADAS-Cog: weekend 29.4%. TRTSDT: Sat 42, Sun 35 of 254 (30.3%).
- **Impact:** If the dates are real, this is implausible operational behavior and needs a data-integrity query. If the dates were shifted for de-identification, the shift method should be disclosed. Relative-day derivations (ADY, AVAL in ADTTE) are internally consistent: 100% of ADY values reproduce.
- **Recommended follow-up:** Confirm whether calendar dates were offset or perturbed, and the method used.

### Low

### TLF-14-3.02-002: Inconsistent CI method and non-standard RMSE in Table 14-3.02
- **Severity:** Low
- **Type:** Reproducibility
- **Dataset/Output:** Table 14-3.02; tlf-efficacy.r
- **Finding:** The LS-mean CIs use the t distribution (emmeans, df=93), but the treatment-difference CI uses z=1.96. The "Root Mean Squared Error" is computed as √(mean(residual²)), which divides by n, instead of the conventional model root MSE √(RSS/df).
- **Evidence:** The t-based difference CI is (−0.51, 0.64) vs reported (−0.50, 0.63), which is within the ±0.01 tolerance. RMSE is √(mean res²) = 1.30 (as reported), while the model σ = 1.32. The sponsor's FDA response attributes the earlier discrepancy to the quantile choice and an RMSE update.
- **Recommended follow-up:** Use one CI method throughout. Label the statistic precisely, or report the model root MSE.

### TLF-14-3.01-002: Range display hides non-integer (prorated) ADAS-Cog scores
- **Severity:** Low
- **Type:** Interpretability
- **Dataset/Output:** Table 14-3.01 (`f_str('xx.x (xxx;xx)')`)
- **Finding:** Min and max are shown as integers, while 33 of 1,040 ACTOT values are non-integer because of proration.
- **Evidence:** Low Dose baseline maximum is 56.72 (displayed "57"). Placebo and High Dose Week 24 maximum is 61.55 (displayed "62"). All other cells reproduce exactly:
  - Baseline: 24.1 (12.19), 24.4 (12.92), 21.3 (11.74).
  - Week 24: 26.7 (13.79), 26.4 (13.18), 22.8 (12.48).
  - Change: 2.5 (5.80), 2.0 (5.55), 1.5 (4.26).
  - Pairwise: −0.5 (0.82) (−2.1; 1.1) p=0.569; −1.0 (0.84) (−2.7; 0.7) p=0.233; −0.5 (0.84) (−2.2; 1.1) p=0.520.
- **Recommended follow-up:** Display min/max to one decimal, or footnote the proration.

### ADAM-ADAE-002: TEAE definition has no upper window; undated AEs silently excluded; TRTEMFL not set to "N"
- **Severity:** Low
- **Type:** Interpretability
- **Dataset/Output:** ADAE.TRTEMFL; define MT.ADAE.TRTEMFL / ASTDT
- **Finding:** TRTEMFL = "ASTDT ≥ TRTSDT," with no end-of-treatment window. 35 TEAEs began 1–14 days after the last dose, including 2 TTDE events (one Placebo, one High). 11 AEs with an unimputable start date have TRTEMFL blank (define says "N") and are excluded from TEAE and TTDE. One of them is a DERMATITIS ATOPIC (01-718-1355). Define calls this exclusion "conservative," but for safety purposes it is anti-conservative.
- **Evidence:** TRTEMFL was re-derived and matches the submitted flag 1126/1126. CQ01NAM was re-derived per define: 493/493 agree.
- **Recommended follow-up:** Document the TEAE risk window. Set TRTEMFL="N" explicitly. Justify excluding AEs with partial dates.

### ADAM-ADTTE-001: Censoring description and informative-censoring considerations for TTDE
- **Severity:** Low
- **Type:** Interpretability
- **Dataset/Output:** ADTTE (EVNTDESC, CNSR, ADT)
- **Finding:** All 102 censored subjects carry EVNTDESC="Study Completion Date," but 58 of them discontinued (Placebo 20, Low 17, High 21). The event text has typos ("Dematologic Event Occured"). Censoring at discontinuation is concentrated among AE discontinuers in the active arms (Placebo 2, Low 12, High 10). That is plausibly informative or competing with a dermatologic event, but no sensitivity analysis is provided.
- **Evidence:** ADTTE↔ADAE reconciliation is clean: 152 events = 152 AOCC01FL records; ADT = ASTDT and SRCSEQ = AESEQ for all events; censor ADT = RFENDT for all 102; AVAL = ADT − STARTDT + 1 for all 254; STARTDT = TRTSDT.
- **Recommended follow-up:** Correct the EVNTDESC values. Consider a sensitivity analysis that treats AE discontinuation as an event or a competing risk.

### ADAM-ADLB-001: ADT stored as unformatted numeric in ADLBC/ADLBH
- **Severity:** Low
- **Type:** Standard/metadata
- **Dataset/Output:** ADLBC, ADLBH (ADT)
- **Finding:** ADT has no SAS DATE format in ADLBC and ADLBH, unlike ADADAS, ADCIBC, ADVS, ADNPIX and ADLBHY. Readers that rely on the format will misread these dates (the reviewer had to apply the 1960 origin manually).
- **Recommended follow-up:** Apply the DATE9. format consistently.

## Findings — Simulation realism

Not applicable. As instructed, the package is reviewed as a real submission, so realism concerns appear in the main Findings above (XLAY-REAL-001, ADAM-ADADAS-001, ADAM-ADAE-001).

## Findings summary table
| # | Severity | Type | Category | Output/Dataset | Finding (short) |
|---|---|---|---|---|---|
| 1 | High | Traceability / Interpretability | Integrity | ADADAS/ADCIBC vs ADSL; T14-3.01 | 37 subjects have efficacy assessments 28–266 days after their recorded study discontinuation; off-treatment and LOCF data mixed; Low−Pbo estimate −0.47 → −0.96 on-treatment |
| 2 | High | Reproducibility / Traceability | Integrity | ADAE | AESER=N for all 3 fatal AEs and 36 TE records meeting seriousness criteria; SAE subjects 3 vs 25 |
| 3 | High | Traceability | Integrity | ADAE.AEACN vs ADSL.DSRAEFL | AEACN blank on all 1,191 records; 92 AE discontinuations untraceable to an AE |
| 4 | Medium | Interpretability | Integrity | T14-3.01 | LOCF imputes 17.7% / 39.5% / 44.6% at Week 24; no sensitivity analysis; null result holds under OC, ITT and on-treatment reruns |
| 5 | Medium | Interpretability | Integrity | ADCIBC; ADRG | Co-primary CIBIC+ not reported (reproduced null: p=0.49 / 0.80); OC High−Pbo +0.37 p=0.025; no multiplicity strategy |
| 6 | Medium | Interpretability | Integrity | T14-3.02 | Glucose titled "Primary … LOCF" but observed-case safety lab; baseline N contradicts footnote; 63% missing in High Dose |
| 7 | Medium | Standard/metadata | Integrity | define.xml | Placeholder methods ("LB.VISITNUM", "LB.LBSTNRHI") for primary variables; AOCC01FL text inverted; no ARM |
| 8 | Medium | Standard/metadata | Integrity | ADRG | "Imputation: Not applicable" despite LOCF and proration; EFFFL, windows and site pooling undocumented |
| 9 | Medium | Interpretability | Integrity | T14-2.01 | Sex and ethnicity omitted (female 61.6% / 59.5% / 47.6%); weight/BMI n=83 not shown |
| 10 | Medium | Interpretability | Integrity | Fig 14-1 | Y-axis "Probability of event" plots event-free probability; no events, median or HR reported (reproduced HR 4.08 / 4.92) |
| 11 | Medium | Traceability | Realism | ADSL/ADVS/ADADAS dates | About 30% of visits and treatment starts on weekends; dates look uniformly distributed |
| 12 | Low | Reproducibility | Integrity | T14-3.02 | z-based difference CI vs t-based LS-mean CIs; RMSE divides by n (1.30 vs model 1.32) |
| 13 | Low | Interpretability | Integrity | T14-3.01 | Integer range display hides prorated scores (56.72 → 57) |
| 14 | Low | Interpretability | Integrity | ADAE | No TEAE upper window; 11 undated AEs excluded; TRTEMFL blank instead of "N" |
| 15 | Low | Interpretability | Integrity | ADTTE | EVNTDESC "Study Completion Date" for 58 discontinuers; typos; AE-discontinuation censoring 2 / 12 / 10 with no sensitivity analysis |
| 16 | Low | Standard/metadata | Integrity | ADLBC/ADLBH | ADT numeric with no DATE format |

## Clean checks

- **Cross-table N:** ITT 86/84/84 (Table 14-2.01), Safety 86/84/84 (Figure 14-1 at t=0) and Efficacy 79/81/74 (Table 14-3.01) all match the ADSL flags. ITTFL=SAFFL for all 254 subjects. ARM = TRT01P = TRT01A for all subjects; there were no treatment switches.
- **Table 14-2.01:** all 60 displayed statistics (age, age groups, race, height, weight, BMI, MMSE) reproduce exactly. AGEGR1 derivation: 0 mismatches. BMIBL = WEIGHTBL/HEIGHTBL² within 0.05. WEIGHTBL equals the ADVS baseline weight.
- **Table 14-3.01:** every cell reproduces within tolerance: n, mean, SD, median, range, LS-mean differences, SEs, 95% CIs and p-values (0.245, 0.569, 0.233, 0.520). The column headers are correctly ordered; the FDA's earlier comment about switched headers is resolved in this version. The model matches the footnote (treatment + site group + baseline).
- **ADADAS derivations:** CHG = AVAL − BASE (0 differences); BASE equals the baseline AVAL; ACTOT equals the sum of the 11 ADAS-Cog(11) items (779/779); proration rule reproduced (20/20); LOCF values equal the prior observed value (0 exceptions); ANL01FL picks the record closest to the target day; one record per subject per visit in the analysis set; EFFFL rule re-derived 234/234; ADADAS EFFFL, TRTP and SITEGR1 match ADSL (0 mismatches).
- **Table 14-3.02:** all 19 numbers reproduce (z-based difference CI as programmed).
- **Figure 14-1 / ADTTE:** KM curves and all 33 numbers-at-risk reproduce exactly. ADTTE events = AOCC01FL first dermatologic TEAE (152/152). ADT, SRCSEQ, STARTDT and AVAL are all consistent. Events + censored = N in every arm.
- **ADAE derivations:** TRTEMFL re-derived (1126/1126). CQ01NAM re-derived (493/493). AOCC01FL re-derived (152/152). No duplicate USUBJID/AESEQ.
- **Deaths:** ADSL.DTHFL (3) = DCDECOD "DEATH" (3) = ADAE AESDTH/AEOUT FATAL (3), same subjects. Arm counts: Placebo 2, Low 1, High 0.
- **Disposition:** DSRAEFL = DCDECOD "ADVERSE EVENT" (92/92); DISCONFL = EOSSTT "DISCONTINUED" (144); DCSREAS maps to DCDECOD one-to-one; all AE discontinuers have at least one TEAE.
- **Exposure:** TRTDURD = TRTEDT − TRTSDT + 1 (0 mismatches); TRTSDT = RFSTDTC; RFENDT ≥ TRTEDT for all subjects; AVGDD = CUMDOSE/TRTDURD; Low Dose CUMDOSE = 54 × duration; High Dose average dose 54–78.6 mg, consistent with titration.
- **Hy's Law screen (ADLBC):** only one subject has concurrent ALT or AST > 3×ULN with bilirubin > 2×ULN: 01-705-1186 (Placebo), on Days 16–25 (ALT 3.34×, AST 3.97×, bilirubin 5.94×ULN on Day 22). ALP was 4.9×ULN at baseline and 5.7×ULN on Day 22, a cholestatic pattern, so this does not meet classic Hy's Law (which excludes ALP > 2×ULN). It is consistent with ADLBHY HYLAW=1 at Weeks 2 and 4. There are no cases in the xanomeline arms. (Minor: ADY is missing on those ADLBHY HYLAW records.)
- **Program review:** program logic matches the ADRG selection criteria. The efficacy model uses Type III sums of squares with sum contrasts and proportional emmeans weights, consistent with the SAS PROC GLM OM approach cited in the code.

## Limitations

- **No SDTM.** ADaM-to-source traceability (DM, DS, EX, AE, QS, LB, SV) could not be checked. This includes the post-RFENDT assessments, the AESER/seriousness discordance, the AEACN gap and the partial-date imputation.
- **No SAP or protocol.** The pre-specified primary model, estimand, ICE strategy, visit windows, missing-data and sensitivity analyses, multiplicity hierarchy, EFFFL definition and CIBIC+ analysis method could not be verified. CIBIC+ was analyzed with reviewer-chosen methods (ANOVA with site group; CMH), and the direction of the scale is not documented in the package.
- **No CSR or label.** Cross-document consistency (TLF ↔ CSR text) could not be assessed.
- **No disposition, exposure, AE summary, SAE, lab shift or vital sign TLFs** are in the package. Those checks were done at the ADaM level only.
- **No data cutoff date** is stated.
- **The TLF PDF is image-only.** Values were read visually from 170–260 dpi renders.
- **The sponsor programs were not executed.** They require pilot1wrappers and R 4.1.2-era package versions. Results were independently re-implemented, which is the stronger test of reproducibility.
- **The FDA statistical review** referred to in response-to-fda-1.pdf is not in the package. Only the sponsor's response was available.
- **External sources were not consulted,** per skill rules. The data is known to be the public CDISC pilot synthetic/test dataset (stated in the cover letter and ADRG). Realism findings are framed as they would be for a real submission.

**Overall result rationale (PASS WITH FINDINGS):** All four submitted outputs reproduce from ADaM within the skill's tolerances. The three High findings concern data provenance (post-discontinuation efficacy data) and safety-flag integrity (AESER, AEACN). Reviewer sensitivity analyses (observed case, all-ITT, on-treatment LOCF) do not change the primary conclusion that ADAS-Cog shows no significant effect, and no submitted TLF depends on AESER or AEACN. In a real submission, the High findings would still need sponsor resolution before safety summaries built from ADAE could be accepted.
