---
study: CDISCPILOT01 (R Consortium R Submission Pilot 3 package)
date: 2026-10-27
reviewer: Claude (statistical-reviewer skill)
skill: statistical-reviewer
datasets_reviewed: [m1/us/report-tlf-pilot3.pdf, m1/us/cover-letter.pdf, m1/us/response-FDA-IR-pilot3.pdf, m5/sap-cdiscpilot01.pdf (CSR incl. protocol and SAP Appendix 9), ADaM adsl.xpt, adadas.xpt, adae.xpt, adlbc.xpt, adtte.xpt, adrg.pdf, define.xml, adam-pilot-3.xlsx, ADaM programs adsl.r adadas.r adae.r adlbc.r adtte.r, TLF programs tlf-demographic.r tlf-primary.r tlf-efficacy.r tlf-kmplot.r, pilot3utils_0.0.2.zip, SDTM dm ae suppae cm ds suppds ex lb supplb mh qs sc se sv vs suppdm relrec ta te ti ts tv]
realism_score: 7/10
findings_count: 2 High, 8 Medium, 7 Low
overall_result: FAIL
---

# Statistical Review Report: CDISCPILOT01 (R Consortium Submissions Pilot 3)

## Study overview

CDISCPILOT01 is a Phase 2, prospective, randomized, multicenter (17 sites), double-blind, placebo-controlled, parallel-group, 26-week study of transdermal xanomeline (low dose 54 mg/day, high dose 81 mg/day) versus placebo in mild to moderate Alzheimer's disease. The SAP defines two co-primary efficacy endpoints, both tested as a dose-response at alpha = 0.05 with no multiplicity adjustment across them: change from baseline in ADAS-Cog(11) at Week 24 (ANCOVA with baseline score, pooled site and dose as a continuous variable, efficacy population, LOCF), and CIBIC+ at Week 24 (ANOVA). 254 subjects were randomized (86 placebo / 84 low / 84 high). All were treated, and 234 (79/81/74) form the efficacy population. The Pilot 3 package regenerates four outputs from R-built ADaM: Table 14-2.01 (demographics), Table 14-3.01 (primary ADAS-Cog ANCOVA), Table 14-3.02 (glucose ANCOVA at Week 20) and Figure 14-1 (KM curve of time to first dermatologic AE). The reported primary result is a dose-response p = 0.245 (no dose response). Dermatologic AEs were much more frequent on xanomeline. No data cutoff is defined: this is a completed study (first visit 2012-07-09, last first dose 2014-09-02), and all analyses use the final database. The CSR states that the legacy data were de-identified and the dates shifted. The data are publicly known to be a CDISC/R Consortium test dataset. As instructed, this review treats them as a real submission.

## Review scope

- **Provided and reviewed:** the 4 TLFs, the cover letter, the FDA IR response, the CSR with protocol and SAP (Appendix 9, including raw SAS GLM output for Table 14-3.01), all 5 ADaM datasets with define.xml, the specs and the ADRG, all 9 R programs and the proprietary `pilot3utils` helper functions (inspected by lazy-loading the binary package, without installing it), and all 22 SDTM domains.
- **Layers executed:** full package (TLF → ADaM → SDTM, plus SAP compliance). Every number in all four Pilot 3 TLFs was reproduced independently from ADaM. Key ADaM derivations were re-derived from SDTM: population flags, treatment dates, ADAS-Cog total scoring and windowing/LOCF, TRTEMFL, dermatologic first event, and ADTTE event/censor values.
- **Tools:** R 4.5.2 (haven, dplyr, survival, emmeans, nlme, pdftools). The reviewer's scratch scripts (`a1_adsl.R` … `h1.R`) are not included in this repository. Nothing in the pilot package was modified.

## Population registry

| Population | Definition (SAP §6) | N ADSL (P / L / H) | N SDTM (DM/SUPPDM/EX/QS) | N in TLF | Consistent? | Notes |
|---|---|---|---|---|---|---|
| Screened | Informed consent | n/a (excluded from ADSL) | 306 in DM | n/a | Yes | 52 screen failures (DM ARM = "Screen Failure") |
| Randomized / ITT | All randomized | 86 / 84 / 84 = 254 | DM ARMCD ≠ Scrnfail = 254; SUPPDM ITT = 254 | T14-2.01: 86/84/84 | Yes | No DS "RANDOMIZED" record and no randomization date in SDTM |
| Safety | Randomized and ≥1 dose | 86 / 84 / 84 | EX: all 254 have ≥1 record; SUPPDM SAFETY matches | F14-1: 86/84/84 | Yes | TRT01A = TRT01P for all subjects (EXTRT matches ARM) |
| Efficacy | Safety and ≥1 post-baseline ADAS-Cog **and** CIBIC+ | 79 / 81 / 74 = 234 | Re-derived from QS (VISITNUM > 3): 234; SUPPDM EFFICACY matches | T14-3.01: 79/81/74 | Yes | 20 excluded: 17 have neither assessment, 2 have CIBIC+ only, 1 has ADAS-Cog only |
| Completers Wk 24 | Efficacy and completed Visit 12 | 60 / 28 / 30 | SV WEEK 24 visit; SUPPDM COMPLT24 matches | n/a in Pilot 3 | Yes | All COMP24FL = Y subjects have EFFFL = Y |
| Completed study | DS COMPLETED | 58 / 25 / 27 | DS = 110 | n/a | Yes | |
| Glucose Wk 20 analysis set | ITT, placebo/high dose, observed Week 20 glucose | 65 / – / 31 | LB | T14-3.02: 65/31 | Yes | Observed cases only (see TLF-14-3.02-001) |

## Denominator registry

| Output | Population used | Header N | Reproduced N | Difference | Subject-level reason categories |
|---|---|---:|---:|---:|---|
| Table 14-2.01 Demographics | ITT | 86 / 84 / 84 | 86 / 84 / 84 | 0 | Weight and BMI in the low-dose arm are based on n = 83, not shown (01-702-1082 has no Visit 3 weight) |
| Table 14-3.01 Primary ADAS-Cog | Efficacy, ANL01FL, Week 24 LOCF | 79 / 81 / 74 | 79 / 81 / 74 | 0 | 79 LOCF-imputed (14 / 32 / 33) |
| Table 14-3.02 Glucose | ITT, Pbo + High | Baseline 86 / 84; Wk 20 65 / 31 | 86 / 84; 65 / 31 | 0 | Baseline column uses all subjects, not the "observable at Baseline and Week 20" set stated in the footnote |
| Figure 14-1 KM | Safety | 86 / 84 / 84 | 86 / 84 / 84 | 0 | Events 29 / 62 / 61; censored 57 / 22 / 23 |

## Data realism assessment

**Overall realism score: 7/10.** The data look like real, de-identified legacy trial data with one clear operational artifact (consistent with the date shifting the CSR describes). The data are known to be a public CDISC test dataset. Per instructions, realism concerns are reported in the main Findings section.

### Realistic features
| Feature | Evidence |
|---|---|
| Visit timing jitter | Actual minus nominal study day: mean +1.3 to +3.7 days, SD 3.1–8.9 by visit, 61–83% within ±3 days, range −24 to +93 |
| Within-system correlations | Height–weight r = 0.63; weight–BMI r = 0.78; supine SBP–DBP r = 0.41; ALT–AST r = 0.70; Hgb–Hct r = 0.88 |
| Sex dimorphism | Mean height 173 cm (M) vs 157 cm (F); weight 75.9 vs 59.4 kg |
| Site heterogeneity | Baseline ADAS-Cog differs by pooled site (ANOVA p = 0.0012); SITEGR1 is significant in the primary model (p = 0.025) |
| Digit preference | SBP last digit: 0 = 37.7%, even digits dominate (manual BP recording) |
| AE pattern | 156 distinct onset days (14% on multiples of 7); severity 65% mild / 31% moderate / 4% severe; placebo background TEAE rate 75.6%; strong dermatologic signal on active arms |
| Dropout pattern | 144 discontinuations on 87 distinct study days (median day 63); more active-arm dropout (57 / 59 vs 28 placebo), mostly AE-driven with dermatologic AEs in 71 / 92 AE discontinuations |
| Score derivation fidelity | ADAS-Cog(11) totals reproduce exactly from items, including the SAP §14.2 prorating for 1–3 missing items (21 records) |

### Unrealistic features
| Feature | Evidence | Severity | Recommendation |
|---|---|---|---|
| Outpatient visits evenly spread across weekdays | SV visit dates: Sat 15.7%, Sun 14.2%, Mon–Fri 12.8–16.3% | Medium (see REAL-SV-001) | Confirm that the date shifting kept the day of week; otherwise explain the weekend clinic activity |
| Eligibility breach without a deviation record | MMSE = 24 in 2 subjects (inclusion 10–23); no DV domain | Low | See SDTM-QS-001 |
| Repeated AE records | 460 AE rows (114 subjects) are repeats of the same event with an updated outcome | Medium | See SDTM-AE-002 |

### Implications
The statistical structure (correlations, site effects, AE and dropout patterns) supports the data being clinically plausible. The uniform weekday distribution is an operational inconsistency that a regulator would query for real data. It is most likely an artifact of de-identification date shifting, and it does not affect any derived analysis value, because all analysis days are relative.

## Findings — Data integrity

### High

### SDTM-AE-001: Seriousness flag inconsistent with seriousness criteria; fatal and hospitalized AEs are not flagged serious
- **Severity:** High
- **Type:** Conclusion-impacting
- **Dataset/Output:** SDTM AE → ADAE (AESER, AOCC02FL/AOCC03FL/AOCC04FL); CSR §12.2–12.3
- **Finding:** AESER = "N" on 36 AE records (25 subjects: 6 placebo / 10 low / 9 high) that have at least one seriousness criterion = "Y". These include all 3 fatal AEs (AESDTH = Y, AEOUT = FATAL: SUDDEN DEATH 01-701-1211, COMPLETED SUICIDE 01-704-1445, MYOCARDIAL INFARCTION 01-710-1083) and 28 records with AESHOSP = Y (e.g., pneumonia, myocardial infarction, congestive cardiac failure, GI haemorrhage, hip fracture, TIA). Only 3 records (3 subjects) have AESER = "Y".
- **Evidence:** `table(AESER, anycrit)`: N/TRUE = 36, Y/TRUE = 3, Y/FALSE = 0. Excluding cancer-only criteria, 23 subjects (6/9/8) meet a death, hospitalization, life-threatening or disability criterion. ADAE copies AESER, so the SAE first-occurrence flags (AOCC02FL–AOCC04FL) cover only 3 subjects.
- **Impact:** Any SAE summary built from these data (SAP §11.3, CSR Table 14-5.02, which reports "3 SAEs in 3 subjects") understates serious events by up to about 8-fold, and fatal events would be omitted from SAE tables. This would distort the safety profile and the labeling.
- **Recommended follow-up:** Reconcile AESER with the seriousness criteria (ICH E2A: death or hospitalization implies serious), correct SDTM AE, re-derive ADAE, and regenerate SAE outputs.
- **reviewer_question:** Please explain why AEs with AESDTH = Y or AESHOSP = Y have AESER = N, and provide a corrected SAE summary.

### XLAY-AEDISC-001: AE-related discontinuations cannot be traced to a causative AE, and some are coded under non-AE reasons
- **Severity:** High
- **Type:** Traceability
- **Dataset/Output:** SDTM DS, AE (AEACN); ADSL DSRAEFL/DCSREAS; ADAE
- **Finding:** AEACN is missing on all 1,191 AE records (as is SUPPAE, which holds only AETRTEM). The 92 DS "ADVERSE EVENT" discontinuations (8 / 44 / 40) therefore cannot be linked to the AE(s) that caused them. In addition, 5 discontinuations whose DSTERM text describes an AE or tolerability problem are coded DSDECOD = PHYSICIAN DECISION or WITHDRAWAL BY SUBJECT, so DSRAEFL is not set for them: 01-701-1360 (High, "PMD DECISION DUE TO AE'S"), 01-705-1186 (Placebo, "HYPERBILIRUBINEMIA"), 01-718-1328 (High, "PATIENT UNABLE TO TOLERATE DERMAL IRRITATION AT PATCH SITE"), 01-708-1272 (Low, "PATCH DISCOMFORT") and 01-702-1082 (Low, "PT FINDS PATCHES INCONVENIENT & ITCHY").
- **Evidence:** DS AE set = ADSL DSRAEFL set (92 = 92, exact match). ADAE AEACN = "DISCONTINUED": 0 subjects. All 92 DS-AE subjects have ≥1 AE record; 71 have a dermatologic AE.
- **Impact:** This is the key benefit-risk driver of the study: the CSR attributes the 52% / 46% active-arm AE dropout to dermatologic events. That attribution cannot be verified from the data, and AE discontinuations are undercounted by at least 5 (2 low, 2 high, 1 placebo).
- **Recommended follow-up:** Populate AEACN (or provide the CRF action data), recode the 5 DS records as AE-related or justify their coding, and provide a subject-level DS–AE reconciliation listing.
- **traceability_path:** DS.DSDECOD → ADSL.DSRAEFL → ADAE.AEACN (missing) → AE.AEACN (missing)

### Medium

### TLF-14-3.02-001: Glucose ANCOVA is mislabeled as a "Primary Endpoint Analysis", contradicts the SAP, and has an inaccurate title and footnote
- **Severity:** Medium
- **Type:** Interpretability
- **Dataset/Output:** Table 14-3.02 (tlf-efficacy.r; ADLBC GLUC)
- **Finding:**
  - The table is titled "Primary Endpoint Analysis: Glucose (mmol/L) – Summary at Week 20 – LOCF". Glucose is not an efficacy endpoint, and SAP §15.3 states "No ANCOVA analyses will be performed for laboratory data".
  - Its number collides with the SAP/CSR Table 14-3.02, which is the co-primary CIBIC+ analysis.
  - The title says LOCF, but the analysis is observed cases only (Week 20 N = 31 high / 65 placebo of 84 / 86).
  - Footnote (a) says the table uses subjects with data at both Baseline and Week 20, but the Baseline column uses all subjects (N = 84 / 86).
  - The 95% CI for the difference uses ±1.96·SE rather than the t-quantile.
  - The "Root Mean Squared Error" divides by n, not by the residual df.
- **Evidence:** All reported values reproduce: LS means 0.16 (−0.31, 0.63) and 0.09 (−0.23, 0.42); difference 0.07 (−0.50, 0.63), p = 0.822; RMSE 1.30. The t-based CI is (−0.51, 0.64), and model sigma is 1.32. For the Week 20 cohort, baseline means are 5.58 / 5.75, not the 5.4 / 5.6 shown.
- **Impact:** A reader may treat a safety lab ANCOVA as a primary efficacy result and confuse it with the CIBIC+ co-primary. The output is not pre-specified, and it is mislabeled.
- **Recommended follow-up:** Retitle (e.g., "Supportive/ad hoc: Glucose change from baseline at Week 20 – Observed cases"), renumber, label it as not pre-specified, fix the footnote, and use t-based CIs.

### TLF-14-1-001: KM figure y-axis is mislabeled; no group comparison, medians or censoring footnote
- **Severity:** Medium
- **Type:** Interpretability
- **Dataset/Output:** Figure 14-1 (tlf-kmplot.r; ADTTE TTDE)
- **Finding:**
  - The y-axis reads "Probability of event", but the curves are event-free (survival) probabilities: placebo plateaus at about 0.63, which is the proportion *without* an event.
  - SAP §11.2 requires the time to first dermatologic event to be "compared across the treatment groups", but no test, median or HR is shown.
  - There is no footnote on the event definition (CQ01NAM) or the censoring rules.
  - The high-dose legend key is drawn as a thin grey line, unlike its plotted color.
- **Evidence:** Numbers at risk at days 0–200 reproduce exactly for all 3 arms (Placebo 86, 75, 65, 59, 50, 47, 45, 42, 40, 35, 0; Low 84, 58, 31, 20, 14, 12, 8, 6, 6, 5, 0; High 84, 48, 31, 14, 7, 4, 4, 4, 4, 3, 0). Reproduced from ADTTE:
  - Events 29 / 62 / 61.
  - KM median: placebo not reached; low dose 33 days (95% CI 27–48, log-log; 28–51, log); high dose 36 days (23–46 log-log; 25–47 log).
  - Log-rank χ² = 60.3 on 2 df, p = 8×10⁻¹⁴.
  - Cox HR vs placebo: low 4.15 (2.65–6.50), high 5.03 (3.18–7.94).
- **Impact:** With the current axis label, readers could reverse the interpretation (reading 63% as the placebo event probability). The pre-specified comparison is not reported in the package.
- **Recommended follow-up:** Relabel the axis "Probability of no dermatologic event" (or plot 1−S(t)). Add the log-rank p-value, medians with CI method, the event definition and the censoring rule.

### XLAY-SCOPE-001: The co-primary endpoint CIBIC+ is not analyzed and has no ADaM dataset
- **Severity:** Medium
- **Type:** Traceability
- **Dataset/Output:** Package scope; SAP §3.2.1, §10.1.2
- **Finding:** The SAP's primary objective needs both ADAS-Cog(11) and CIBIC+. The Pilot 3 package provides an ADaM dataset and a TLF only for ADAS-Cog. CIBIC+ exists only in SDTM QS, and EFFFL depends on it.
- **Evidence:** Reviewer re-derivation from QS using the SAP windows and LOCF, with ANOVA on dose (continuous) and pooled site: Week 24 n = 79 / 81 / 74, means 4.29 / 4.19 / 4.32, dose-response p = 0.960. Week 8 p = 0.167 (n 77 / 81 / 73); Week 16 p = 0.214. These match the legacy CSR Tables 14-3.02/14-3.04/14-3.06.
- **Impact:** The efficacy conclusion ("no dose response on either co-primary") cannot be verified from the submitted analysis datasets. A reviewer has to reprogram from SDTM. The reproduced result agrees with the CSR, so the conclusion is not affected.
- **Recommended follow-up:** Provide ADCIBC (or include CIBIC+ in an ADQS dataset) and the corresponding Table 14-3.02 CIBIC+ output, or state the scope limitation explicitly in the ADRG and cover letter.

### ADAM-ADADAS-001: Heavy, differential missingness at Week 24 handled only by LOCF
- **Severity:** Medium
- **Type:** Interpretability
- **Dataset/Output:** ADADAS (ACTOT, DTYPE = LOCF); Table 14-3.01
- **Finding:** In the efficacy population, the share of Week 24 values that are LOCF-imputed is 17.7% placebo (14/79), 39.5% low (32/81) and 44.6% high (33/74). This exceeds the 15% threshold and differs between arms by up to 27 points. Dropout is mostly AE-driven on the active arms. In a progressive disease, LOCF carries forward earlier (better) scores, which favors the arm with more early dropouts (active). No sensitivity analysis is included in the Pilot 3 package.
- **Evidence:** Reviewer sensitivity analyses (dose-response p):
  - Primary LOCF: 0.245 (reproduced).
  - Observed-case windowed Week 24: N = 155, p = 0.416.
  - Completers observed-case: N = 116 (59 / 27 / 30), p = 0.234 (matches CSR Table 14-3.07).
  - Baseline-carried-forward for imputed records: p = 0.191.
  - MMRM per SAP §10.1.1 (unstructured covariance; treatment × visit, site, baseline × visit): Week 24 differences vs placebo −0.59 (SE 1.01, p = 0.56) and −0.83 (SE 1.07, p = 0.44).
- **Impact:** The "no dose response" conclusion holds under every alternative tried. The estimates still depend on assumptions, and the direction of LOCF bias favors the active arms.
- **Recommended follow-up:** Include the SAP-specified completers and MMRM supportive analyses (CSR Tables 14-3.07, 14-3.11) and a missing-data summary by arm and reason.
- **estimand_component:** Missing data handling / ICE (treatment discontinuation due to AE)

### SDTM-AE-002: Repeated AE records inflate event counts and give conflicting outcomes
- **Severity:** Medium
- **Type:** Reproducibility
- **Dataset/Output:** SDTM AE / ADAE (event-level counts, ADURN)
- **Finding:** 460 AE records (114 subjects) duplicate another record on USUBJID, AEDECOD, AESTDTC, AEENDTC and AESEV. They differ only in AEDTC (reporting visit) and AEOUT (e.g., "NOT RECOVERED" then "RECOVERED" for the same event). Many share the same AESPID.
- **Evidence:** 01-701-1023 ERYTHEMA AESPID E08 appears as AESEQ 1 and 4; 01-701-1192 PNEUMONIA AESPID E10 appears as AESEQ 7 and 10 with different outcomes. ADAE keeps all 1,191 records (1:1 with AE). Subject-level first-occurrence flags and TTDE are unaffected.
- **Impact:** Event-level counts ("[AEs]" columns in TEAE tables), AE duration and outcome summaries are inflated or inconsistent.
- **Recommended follow-up:** Collapse repeated reports into a single event per AESPID (latest outcome), or document the multi-record convention in the SDRG/ADRG and count unique events in the tables.

### ADAM-ADLBC-001: ANRIND holds threshold flags, not the reference-range indicator, and missing values are set to "Normal"
- **Severity:** Medium
- **Type:** Standard/metadata
- **Dataset/Output:** ADLBC ANRIND/BNRIND (adlbc.r lines 227–228)
- **Finding:** ANRIND is derived as "H" if AVAL > 1.5×ULN and "L" if AVAL < 0.5×LLN; this is the SAP "threshold range", not the normal range. ANRIND is also set to "N" when AVAL is missing.
- **Evidence:** Against LBNRIND: 943 HIGH and 372 LOW records have ANRIND = "N"; 10 records with missing AVAL have ANRIND = "N".
- **Impact:** Any shift or abnormality table built on ANRIND/BNRIND (SAP Tables 21–24) would misclassify reference-range abnormalities and count missing results as normal.
- **Recommended follow-up:** Derive ANRIND from ANRLO/ANRHI, keep the threshold flags in a separate variable (e.g., ATOXGR or a CRITy flag), and leave the indicator missing when AVAL is missing.

### TLF-14-2.01-001: Demographic table omits SAP-required characteristics and n's
- **Severity:** Medium
- **Type:** Interpretability
- **Dataset/Output:** Table 14-2.01 (tlf-demographic.r)
- **Finding:** SAP §9.2/Template 3 requires sex, duration of disease, years of education, BMI category, a Total column and ANOVA/chi-square p-values. All are absent. No n row is shown, and rtables silently drops the missing value, so low-dose weight and BMI are summarized on 83 of 84 subjects.
- **Evidence:** Every displayed value reproduces exactly (e.g., age 75.21 (8.59) / 75.67 (8.29) / 74.38 (7.89); weight 62.76 / 67.28 / 70.00; MMSE max 23 / 24 / 24). The omitted SAP p-values show a baseline imbalance: weight ANOVA p = 0.003, BMI p = 0.013. Sex is 33 / 34 / 44 male (p = 0.14).
- **Impact:** The table hides the weight/BMI imbalance and the sex distribution (52% male on high dose vs 38% on placebo), both relevant for safety interpretation of a weight-dosed transdermal product.
- **Recommended follow-up:** Add the SAP-specified rows, n per variable, Total and p-values.

### REAL-SV-001: Clinic visits evenly distributed across weekends
- **Severity:** Medium
- **Type:** Standard/metadata (operational plausibility)
- **Dataset/Output:** SDTM SV (also QS, LB, VS dates)
- **Finding:** 29.9% of scheduled outpatient visits fall on Saturday or Sunday, about the same as any weekday (12.8–16.3%).
- **Evidence:** `prop.table(table(weekdays(SVSTDTC)))`: Sat 0.157, Sun 0.142, Mon 0.128, Tue 0.132, Wed 0.163, Thu 0.144, Fri 0.134.
- **Impact:** For real data, uniform weekend activity at 17 outpatient sites is implausible. It suggests date manipulation, and this is a data-integrity query. The CSR states that dates were shifted for de-identification, which would explain it. Relative timing, and so every analysis, is unaffected.
- **Recommended follow-up:** Document the date-shifting algorithm in the SDRG/ADRG and confirm it shifted all dates of a subject by a constant.

### Low

### TLF-14-3.01-001: Pairwise comparisons shown although the dose-response gate failed; incomplete source header
- **Severity:** Low
- **Type:** Interpretability
- **Dataset/Output:** Table 14-3.01
- **Finding:**
  - SAP §7.3/§10.1.1 says pairwise comparisons are performed only if the dose-response test is significant. The test was not significant (p = 0.245), but the table presents pairwise p-values and CIs without a "descriptive only" label.
  - The page header reads "Page 1 of" (count missing), and the source line reads "Source: <run interactively>", not the program path.
- **Evidence:** Reproduced exactly from ADADAS with the SAP model (CHG ~ dose [0/54/81] + SITEGR1 + BASE; N = 234):
  - Dose-response: Type III F = 1.36, p = 0.2447 (matches the CSR SAS GLM output).
  - Low − Placebo −0.47 (SE 0.82), CI (−2.08, 1.15), p = 0.569.
  - High − Placebo −1.01 (SE 0.84), CI (−2.66, 0.65), p = 0.233.
  - High − Low −0.54 (SE 0.84), CI (−2.19, 1.11), p = 0.520.
  - Summary statistics also match (e.g., placebo change 2.5 (5.80)).
- **Impact:** Minor over-presentation of non-gated comparisons and a gap in output traceability. Conclusions are unaffected.
- **Recommended follow-up:** Footnote the pairwise results as descriptive (gate not passed), and print the program path and page count.

### ADAM-ADTTE-001: Censoring-date and description defects in ADTTE
- **Severity:** Low
- **Type:** Traceability
- **Dataset/Output:** ADTTE (adtte.r), Figure 14-1
- **Finding:**
  - The program comment says deaths are censored at the death date, but the code uses RFENDTC. Subject 01-710-1083 (placebo) is censored on 2013-08-03, one day after DTHDTC 2013-08-02.
  - EVNTDESC = "Study Completion Date" for all 102 censored subjects, including early discontinuers.
  - The event text has a typo ("Dematologic Event Occured").
  - The censoring rule (end of study, up to 91 days after last dose for 49 subjects; 2 events occur after TRTEDT) is not pre-specified in the SAP or footnoted.
- **Evidence:** An independent re-derivation from ADAE/ADSL/DS reproduces AVAL, CNSR and ADT for all 254 subjects (0 mismatches). An on-treatment censoring sensitivity gives log-rank χ² = 62.8 and medians of 31 / 36 days.
- **Impact:** Negligible effect on results. Censoring after death is a logical error, and the descriptions reduce traceability.
- **Recommended follow-up:** Use DTHDTC for deaths, set EVNTDESC by disposition reason, correct the spelling, and document the censoring rule.

### ADAM-ADAE-001: Dermatologic CQ string matching differs from the CSR medical list; define text is inverted
- **Severity:** Low
- **Type:** Standard/metadata
- **Dataset/Output:** ADAE CQ01NAM/AOCC01FL, define.xml, CSR Table 12-2
- **Finding:**
  - The string match on "ERYTHEMA" captures PHARYNGEAL ERYTHEMA (respiratory SOC; 01-709-1029, 2 records).
  - The CQ also includes DERMATITIS ATOPIC and RASH PAPULAR, which are not in CSR Table 12-2.
  - The define.xml derivation for AOCC01FL reads "Subset to CQ01NAM=''", which is the opposite of the implemented rule.
- **Evidence:** Removing PHARYNGEAL ERYTHEMA changes no subject's TTDE event or time (0 subjects; the other CQ events occur earlier or are pre-treatment).
- **Impact:** No numerical impact on Figure 14-1. Metadata cannot be relied on as written.
- **Recommended follow-up:** Define the CQ by an explicit PT list matching the CSR, and correct the define text.

### ADAM-ADSL-001: TRTEDT imputed months after the last documented dose for 6 subjects
- **Severity:** Low
- **Type:** Traceability
- **Dataset/Output:** ADSL TRTEDT/TRTDURD/CUMDOSE/AVGDD
- **Finding:** When the last EX record has no end date, TRTEDT is set to the disposition date. This follows the CSR §12.1 convention, but it can add long undocumented exposure.
- **Evidence:**
  - 01-705-1303 (High, AE discontinuation): last EX record starts 2013-12-31 with no end date; TRTEDT = 2014-06-02 (TRTDURD 169, CUMDOSE 13,284 mg).
  - 01-704-1233 (Placebo): last documented end 2013-04-04, TRTEDT 2013-07-14.
  - TRTEDT ≠ DM.RFXENDTC for 4 subjects; RFXENDTC is missing for 2.
- **Impact:** Exposure is overstated in a few subjects. No effect on the reviewed TLFs, because TEAE has no upper window and ADTTE censors at end of study.
- **Recommended follow-up:** Flag imputed TRTEDT (TRTEDTF) and present the exposure summary with and without imputation.

### SDTM-QS-001: Two randomized subjects violate the MMSE inclusion criterion and have no deviation record
- **Severity:** Low
- **Type:** Interpretability
- **Dataset/Output:** QS (MMSE), ADSL MMSETOT, Table 14-2.01
- **Finding:** MMSE = 24 for 01-707-1037 (Low) and 01-709-1238 (High). The inclusion range is 10–23 (SAP §1.2, CSR §9.3). The package has no DV domain and no per-protocol flag.
- **Evidence:** MMSE is collected once (Screening), and MMSETOT re-sums exactly from the 6 MMSE records per subject.
- **Impact:** Both subjects remain in ITT and efficacy, which is appropriate under ITT. The missing deviation data prevents any assessment of eligibility or protocol violations.
- **Recommended follow-up:** Provide the protocol-deviation data, or confirm whether these were approved waivers.

### ADAM-ADADAS-002: Study-day convention differs from the SAP window formula
- **Severity:** Low
- **Type:** Reproducibility
- **Dataset/Output:** ADADAS ADY/AVISIT; SAP §8.2
- **Finding:** The SAP defines day as "visit date − randomization date" (no +1), but its window table uses target day 1 for baseline. ADADAS uses ADY with the +1 convention relative to TRTSDT. No randomization date exists in SDTM.
- **Evidence:** 3 assessments change window under the literal SAP formula (01-705-1292 and 01-718-1250 move from Week 24 to Week 16; 01-709-1238 from Week 16 to Week 8). The re-run dose-response p is 0.249 (vs 0.245).
- **Impact:** Negligible. The SAP wording is ambiguous.
- **Recommended follow-up:** Clarify the day convention in the ADRG, and add a randomization record or date (DS or ADSL RANDDT).

### XLAY-DOC-001: Inconsistencies across ADRG, IR response and CSR
- **Severity:** Low
- **Type:** Traceability
- **Dataset/Output:** adrg.pdf §7.2, §9.2.4; response-FDA-IR-pilot3.pdf Comment 5; CSR §12.3.4
- **Finding:**
  - ADRG §9.2.4 states that the R ADADAS differs from the CDISC ADADAS in AVAL/CHG for 19 subjects. The IR response states that the discrepancy was resolved by subsetting to ANL01FL before LOCF. The submitted ADADAS reproduces the SAP derivation exactly (see Clean checks), and the TLF matches Pilot 1 exactly. The ADRG text therefore appears stale.
  - The ADRG lists the outputs as "adas.xpt"/"adlb.xpt" and the program file as "renv.lock" (the files are adadas.xpt, adlbc.xpt, renv-lock.txt).
  - CSR death narratives cite 01-701-1445 and 01-701-1083; the data IDs are 01-704-1445 and 01-710-1083.
- **Impact:** Confusing for reviewers. No numerical impact.
- **Recommended follow-up:** Update ADRG §9.2.4 and §7.2, and correct the CSR subject IDs.

## Findings summary table

| # | Severity | Type | Category | Output/Dataset | Finding (short) |
|---|---|---|---|---|---|
| 1 | High | Conclusion-impacting | Integrity | AE/ADAE | AESER = N on 36 records (25 subjects) with seriousness criteria, incl. all 3 deaths; only 3 SAEs flagged |
| 2 | High | Traceability | Integrity | DS/AE/ADSL/ADAE | AEACN missing for all AEs; 92 AE discontinuations untraceable; 5 AE-related discontinuations coded as non-AE |
| 3 | Medium | Interpretability | Integrity | Table 14-3.02 | Glucose ANCOVA titled "Primary Endpoint", against SAP §15.3; "LOCF" title on observed data; wrong footnote |
| 4 | Medium | Interpretability | Integrity | Figure 14-1 | Y-axis "Probability of event" on survival curves; no log-rank/median despite SAP |
| 5 | Medium | Traceability | Integrity | Package scope | Co-primary CIBIC+ has no ADaM dataset or TLF (reproduced p = 0.960) |
| 6 | Medium | Interpretability | Integrity | ADADAS/T14-3.01 | Week 24 LOCF 17.7% / 39.5% / 44.6%; sensitivity analyses absent (conclusion robust) |
| 7 | Medium | Reproducibility | Integrity | AE/ADAE | 460 repeated AE records inflate event counts and give conflicting outcomes |
| 8 | Medium | Standard/metadata | Integrity | ADLBC | ANRIND = threshold flag; 1,315 out-of-range values coded N; missing → N |
| 9 | Medium | Interpretability | Integrity | Table 14-2.01 | SAP-required sex, education, disease duration, BMI category, p-values and n omitted |
| 10 | Medium | Standard/metadata | Realism | SV | Visits evenly on weekends (Sat + Sun 29.9%) |
| 11 | Low | Interpretability | Integrity | Table 14-3.01 | Pairwise results shown despite failed gate; source/page header incomplete |
| 12 | Low | Traceability | Integrity | ADTTE | Death censored 1 day after death; generic EVNTDESC; typo; censoring rule undocumented |
| 13 | Low | Standard/metadata | Integrity | ADAE/define | CQ01 regex includes pharyngeal erythema; define AOCC01FL text inverted |
| 14 | Low | Traceability | Integrity | ADSL | TRTEDT imputed up to about 5 months past last documented dose (6 subjects) |
| 15 | Low | Interpretability | Realism | QS/ADSL | 2 subjects with MMSE 24 violate inclusion; no DV data |
| 16 | Low | Reproducibility | Integrity | ADADAS | SAP day formula vs ADY: 3 assessments re-window (p 0.249 vs 0.245) |
| 17 | Low | Traceability | Integrity | ADRG/IR/CSR | Stale ADRG QC text, wrong file names, wrong narrative subject IDs |

## Clean checks

- **Primary endpoint (Table 14-3.01):** Every cell reproduces exactly: n, mean (SD), median (range) at Baseline, Week 24 and change; dose-response p = 0.245 (Type III F, SITEGR1 with 11 levels); all LS-mean differences, SEs, CIs and p-values. These also match the legacy SAS output in the CSR.
- **ADAS-Cog derivation (SDTM → ADaM):** ACTOT re-scored from 11 items, including the SAP §14.2 prorating (0 mismatches in 818 records). SAP windowing (closest to target, earlier on ties) and LOCF from targeted assessments re-derived independently: 0 mismatches in AVAL, BASE or DTYPE at Weeks 8, 16 and 24 for all 234 efficacy subjects. All baseline assessments are on Day 1, pre-dose.
- **Population flags:** ITTFL, SAFFL, EFFFL, COMP8FL, COMP16FL and COMP24FL each match the independent derivation and SUPPDM exactly (0 mismatches). ADSL has one record per subject (254).
- **ADSL vs SDTM:** TRTSDT = RFSTDTC = RFXSTDTC = min EXSTDTC (0 mismatches). TRTDURD = TRTEDT − TRTSDT + 1. AGE, SEX, RACE and SITEID match DM. AGEGR1 categories are correct. HEIGHTBL (Visit 1) and WEIGHTBL (Visit 3) match VS (differences only from round-half-up). BMIBL is recomputed exactly. DURDIS, EDUCLVL and MMSETOT verified. DTHFL matches DM (3 deaths).
- **SITEGR1:** The hard-coded pooling (702, 706, 707, 711, 714, 715, 717 → 900) reproduces the SAP §7.1 rule and CSR Table 14-1.03.
- **Demographics (Table 14-2.01):** All displayed values reproduce exactly.
- **Glucose (Table 14-3.02):** All displayed values reproduce exactly (labeling issues aside).
- **KM (Figure 14-1):** At-risk counts at all 11 time points × 3 arms reproduce exactly. ADTTE AVAL, CNSR and ADT re-derived for 254/254 subjects. Event counts (29 / 62 / 61) match CSR §12.3.3 (34% / 74% / 73%).
- **TRTEMFL:** Matches the SAP rule, including partial-date handling (same year-month as treatment start → TE): 0 disagreements; 1,126 TE and 65 not TE. ASTDY verified. No AE starts after death, and no AE has start > end.
- **Deaths:** Reconcile across DM (DTHFL/DTHDTC), DS (DEATH), AE (AEOUT = FATAL) and ADSL: 3 subjects (2 placebo, 1 low). No exposure after death.
- **DS ↔ ADSL:** The DSRAEFL subject set equals DS DSDECOD = ADVERSE EVENT (92). Every DS-AE subject has ≥1 AE record. EOSSTT and DCDECOD are consistent with DS.
- **Treatment assignment:** ARM = TRT01P = TRT01A, consistent with EXTRT/EXDOSE patterns for all subjects (high dose: 54 mg titrated to 81 mg).
- **Cross-table N:** ITT 254 (86 / 84 / 84) is consistent across Table 14-2.01, Figure 14-1 and the CSR. Efficacy 234 is consistent between Table 14-3.01 and ADSL.
- **Supporting checks:** CIBIC+ (QS re-derivation) matches the CSR at Weeks 8, 16 and 24. Completers observed-case p = 0.234 matches CSR Table 14-3.07.

## Limitations

- No CIBIC+, NPI-X, vital-sign, concomitant-medication or exposure ADaM datasets, and no disposition or AE summary TLFs, are included in the Pilot 3 scope. Those analyses were checked only at SDTM level or not at all.
- There is no DV (protocol deviation) domain, so the per-protocol and eligibility review was limited.
- There is no randomization date or stratification record: randomization was unstratified per the SAP, and TRTSDT served as the randomization proxy.
- The original CDISC SAS ADaM datasets referenced in the ADRG QC section are not in the package, so ADRG §9.2 claims could not be checked directly.
- The MMRM was fitted in nlme (REML, unstructured) and may differ numerically from the legacy SAS PROC MIXED output. It is not part of the Pilot 3 TLFs.
- The proprietary `pilot3utils` functions were inspected from the compiled package, not from source, and the renv environment was not rebuilt. Reproduction used independent code, not the sponsor programs.
- The define.xml was reviewed only for selected derivations (CQ01NAM, AOCC01FL, SITEGR1).
- Per the skill's rules, no external sources were consulted.
