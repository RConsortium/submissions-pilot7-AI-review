---
study: CDISCPILOT01 (R Consortium Submissions Pilot 5, Dataset-JSON)
date: 2026-10-27
reviewer: Claude (statistical-reviewer skill)
skill: statistical-reviewer
datasets_reviewed: [ADaM (Dataset-JSON v1.1) adsl.json, adadas.json, adae.json, adlbc.json, adtte.json; spec adam-pilot-5.xlsx; adrg.pdf; SDTM (Dataset-JSON v1.1) dm, ae, suppae, cm, ds, suppds, ex, lb, supplb, mh, qs, sv, vs, se, sc, relrec, suppdm, ta, te, ti, tv; programs adsl.r, adadas.r, adae.r, adlbc.r, adtte.r, tlf-demographic.r, tlf-efficacy.r, tlf-kmplot.r, tlf-primary.r, pilot5-helper-fcns.r, renv-lock.txt; outputs pilot5-cmb-report-manual.pdf; m1/us/cover-letter.pdf]
realism_score: 7/10
findings_count: [3 High, 11 Medium, 8 Low]
overall_result: FAIL
---

# Statistical Review Report: CDISCPILOT01 (R Consortium Pilot 5, Dataset-JSON submission)

## Study overview

CDISCPILOT01 is a prospective, randomized, multicentre, double-blind, placebo-controlled, parallel-group study of transdermal xanomeline (low dose 54 mg, high dose 81 mg, titrated from 54 mg) versus placebo in mild to moderate Alzheimer's disease. Subjects applied 2 patches daily for 26 weeks (ADRG §2). 306 subjects were screened, 52 failed screening and 254 were randomized (Placebo 86, Low 84, High 84). The submitted primary efficacy output (Table 14-3.01) is the change from baseline in ADAS-Cog(11) at Week 24 with LOCF imputation, analysed by ANCOVA (treatment + pooled site + baseline) in the Efficacy population (N = 79/81/74). It shows no treatment effect: dose-response p = 0.245; High vs Placebo −1.0 (SE 0.84), p = 0.233; Low vs Placebo −0.5 (0.82), p = 0.569. Supportive outputs are Table 14-2.01 (demographics, ITT), Table 14-3.02 (glucose ANCOVA at Week 20) and Figure 14-1 (Kaplan-Meier, time to first dermatologic AE, safety population). The KM figure shows clearly more and earlier dermatologic events on both xanomeline doses (events 29/62/61 in my reproduction). The package does not state a data cutoff. The study is complete, and the last subject's first dose was 2014-09-02. The pilot's stated purpose (cover letter) is for FDA to "reproduce the JSON datasets and analysis results" from the submitted R programs.

## Review scope

**Provided and reviewed:** 5 ADaM datasets and 21 SDTM datasets in CDISC Dataset-JSON v1.1, the ADaM spec workbook (adam-pilot-5.xlsx; there is no define.xml), the ADRG (37 pp), 5 ADaM programs, 4 TLF programs plus a helper file, renv-lock.txt and the cover letter.

**Location of the TLF outputs:** There are no standalone TLF output files (RTF/PDF/.out) in the package. The rendered outputs for all four displays (Table 14-2.01, Table 14-3.01, Table 14-3.02, Figure 14-1) do exist, but only inside `m5/.../programs/pilot5-cmb-report-manual.pdf` (5 pages, dated 2026-06-28). I used that compiled PDF as the "reported values" for every comparison below (see TLF-GEN-001).

**Layers executed:** TLF + ADaM + SDTM (full cross-layer). There is no SAP, protocol, CSR, define.xml or analysis-results metadata, so I could check SAP compliance only against the spec "Methods" sheet, the ADRG and the table footnotes.

**Method:** I parsed Dataset-JSON with jsonlite in R 4.5.2: column metadata first, then rows coerced by `dataType`. A separate Python json census covered types, lengths and missing-value encoding. I did not execute the sponsor programs, because they need admiral, metacore, datasetjson, Tplyr, rtables and ggsurvfit, which are not installed. All derivations and models were independently reimplemented (reviewer scripts, not included in this repository: `00_load.R`, `02_adsl.R`, `03_adadas.R`, `04_glucose.R`, `05_ae_tte.R`, `05b.R`, `06_sdtm_realism.R`, `07_demog.R`, `json2csv.py`, `meta_compare.py`). The R models use `lm`, `drop1`, `emmeans` (proportional weights, `contr.sum`) and `survival::survfit`/`survdiff`/`coxph`. I did not modify the pilot package.

**Data provenance:** This is the public CDISCPILOT01 test dataset. As instructed, I treated it as real submission data, so realism concerns are reported in the main Findings section.

## Population registry

| Population | Definition (source) | N (ADSL) Pbo / Low / High | N (SDTM DM/DS) | N in TLF | Consistent? | Notes |
|---|---|---|---|---|---|---|
| Screened | All DM records | n/a | 306 | n/a | Yes | 52 screen failures (ARMCD = Scrnfail) |
| Enrolled in ADSL | ADSL rows | 254 (86/84/84) | 254 non-screen-fail | n/a | Yes | ADRG §5.2.1 says "All patients in DM were included in ADSL". This is false (306 vs 254); the spec says screen failures are excluded. |
| Randomized / ITT | ITTFL = Y (ARMCD not missing or Scrnfail) | 254 (86/84/84) | DM.ARM 86/84/84 | T14-2.01 headers 86/84/84 | Yes | n/a |
| Safety | SAFFL = Y (ITT and TRTSDT not missing) | 254 (86/84/84 by TRT01A) | EX: 254 subjects dosed; **DM.ACTARM 86/96/72** | Fig 14-1 at-risk t0 86/84/84 | **No** (actual arm) | 12 High-arm subjects received only 54 mg (ADAM-ADSL-001) |
| Efficacy | EFFFL = Y: SAFFL plus ≥1 post-baseline (VISITNUM > 3) ADAS-Cog and CIBIC+ | 234 (79/81/74) | QS-rederived 234, 0 mismatches | T14-3.01 headers 79/81/74 | Yes | 20 ITT excluded (7/3/10); EFFFL is not defined in the ADRG |
| Week-24 completers | COMP24FL = Y (an SV "WEEK 24" record exists) | 118 (60/28/30) | SV-rederived, 0 mismatches | not used | Yes | Visit attendance, not disposition: 8 non-completers have COMP24FL = Y |
| Completed study | DCDECOD = COMPLETED | 110 (58/25/27) | DS 110 | n/a | Yes | n/a |
| Discontinued for AE | DCSREAS = Adverse Event / DSRAEFL = Y | 92 (8/44/40) | DS DSDECOD = ADVERSE EVENT 92 | n/a | Yes | Cannot be traced to specific AEs (XLAY-AEDISC-001) |
| Deaths | DTHFL = Y | 3 (2/1/0) | DM 3, DS 3, AE fatal 3 | n/a | Yes | All 3 fatal AEs have AESER = N (SDTM-AE-001) |

## Denominator registry

| Output | Population used | Header N (reported) | Reproduced N | Difference | Subject-level reasons |
|---|---|---:|---:|---:|---|
| Table 14-2.01 Demographics | ITT | 86/84/84 | 86/84/84 | 0 | Weight/BMI have n = 83 in Low Dose (01-702-1082 has no Visit-3 weight), and the table does not show it (TLF-14-2.01-001) |
| Table 14-3.01 ADAS-Cog W24 | Efficacy (EFFFL & ITTFL), ANL01FL = Y | 79/81/74 | 79/81/74 | 0 | Week-24 n: observed 65/49/41 plus LOCF 14/32/33 |
| Table 14-3.02 Glucose W20 | ITT, Placebo & High only | Baseline 86/84; W20 65/31 | 86/84; 65/31 | 0 | Baseline column uses all ITT, although footnote (a) says only subjects with baseline and Week 20 data (65/31) |
| Figure 14-1 KM TTDE | Safety, TRT01A | at risk 86/84/84 | 86/84/84 | 0 | By DM.ACTARM it would be 86/96/72 |
| AE flags (ADAE) | Safety | no AE table submitted | Any TEAE 65/77/76 subjects | n/a | n/a |

**Missing-data / ICE registry (primary endpoint, Efficacy population, Week 24):**

| Endpoint | N evaluable | Observed at W24 window | LOCF-imputed | % imputed | Arm difference | ICE handling |
|---|---|---|---|---|---|---|
| ADAS-Cog(11) CHG W24 | 79/81/74 | 65/49/41 | 14/32/33 | 17.7% / 39.5% / 44.6% | +26.9 points (High vs Pbo) | Not documented: LOCF for dropouts, while off-treatment retrieved values (up to Day 286) count as observed for 41 subjects (5/23/13) |

The registry flags missingness above 15% in all arms, with an absolute arm difference above 5% (see ADAM-ADADAS-002).

**Multiplicity registry:** There is no SAP or hierarchy in the package. Table 14-3.01 reports one dose-response test and three pairwise tests, with the footnote "p-values without adjustment for multiple comparisons". None is significant, so no gate question arises. The ADRG calls ADAS-Cog "one of the primary efficacy endpoints", but the other primary (CIBIC+) is not analysed (TLF-14-3.01-002).

## Data realism assessment

**Overall realism score: 7/10**. Mostly realistic, with a few operational tells. This is consistent with the publicly known origin of CDISCPILOT01: a real trial that was de-identified and perturbed (dates shifted).

### Realistic features
| Feature | Evidence |
|---|---|
| Visit timing jitter | Actual minus planned visit day, scheduled WEEK visits: SD 5.7 days; 88.9% within ±7 days; only 9–19% exactly on the nominal day; tails of −30 to +93 days |
| Physiological correlations | r(SBP, DBP) = 0.41; r(height, weight) = 0.63; r(weight, BMI) = 0.78; r(ALT, AST) = 0.70; r(Hgb, Hct) = 0.88; r(BUN, creatinine) = 0.48; r(MMSE, baseline ADAS) = −0.83 |
| Sex dimorphism | Mean height F 157.2 / M 172.5 cm; weight F 59.4 / M 75.9 kg |
| Site heterogeneity | Kruskal-Wallis across pooled sites: age p = 3e-4, MMSE p = 2e-4, ADAS p = 1e-4, SBP p = 5e-4; staggered site enrolment, 2012-07 to 2014-09 |
| Dropout pattern | Discontinued subjects' TRTDURD spans 1–176 days with 94 distinct values among 144 subjects; more AE dropout on active (8 / 44 / 40); dropouts have a worse baseline (ADAS 24.7 vs 22.4, MMSE 17.8 vs 18.6) |
| AE patterns | Severity 64.9% mild / 31.4% moderate / 3.6% severe; TEAE onset uses 156 distinct study days (13.8% on multiples of 7); a clear dose-related excess of application-site and skin AEs (subjects with derm events 29 / 62 / 61); placebo has background diarrhoea, URTI and pruritus |
| Digit preference | BP last digit 0 = 36.8%, with even digits dominating (manual sphygmomanometry); weight recorded in whole pounds (92.7% end in 0) |
| Longitudinal noise | No duplicated ADAS trajectories (0/177 subjects with ≥3 observations); SD of the W24 change is 4.3–5.8 per arm |
| Plausible ranges | Age 51–89; BMI 13.7–40.1; ALT up to 129 U/L; glucose 2.7–26.4 mmol/L; no impossible values |

### Unrealistic features
| Feature | Evidence | Severity | Recommendation |
|---|---|---|---|
| Visits evenly spread across all weekdays, including weekends | Saturday 15.7%, Sunday 14.2%, Monday 12.8% … Wednesday 16.3% (SV, n = 3,559); 29.9% of clinic visits fall on weekends | Medium (see XLAY-REAL-001) | Explain the date-perturbation algorithm. If dates are real, weekend clinic visits at every site need operational explanation. |
| Seriousness flags incoherent with criteria | 36 AE records with a seriousness criterion = Y but AESER = N, including all 3 deaths | High (SDTM-AE-001) | Reconcile against the source CRF/SAE database |
| Paired duplicate AE records | 230 pairs (460 of 1,191 records) identical except for outcome/AESPID | Medium (SDTM-AE-002) | Explain the recording convention |
| Dictionary placeholders | MedDRA codes all missing; HLT/HLGT are tokens such as "HLT_0617" | Low (SDTM-AE-003) | Provide coded MedDRA hierarchy |
| Weak multivariate structure | First 3 principal components of 16 baseline variables explain 16% / 13% / 12% | Low | Expected given variables from unrelated organ systems; not by itself a concern |

### Implications
Correlation, site and AE patterns look like real-patient data. The main operational tells are the weekend-visit distribution and the incoherent seriousness/duplicate AE coding. For a real submission these would need sponsor explanation before the safety database could be accepted. The efficacy data (QS/ADADAS) show no fabrication signals.

---

## Findings — Data integrity

### High

### ADAM-ADADAS-001: Submitted ADADAS program cannot regenerate the submitted primary-endpoint dataset
- **Severity:** High
- **Type:** Reproducibility
- **Dataset/Output:** adadas.r → adadas.json → Table 14-3.01
- **Finding:** `adadas.r` builds the final dataset as `adadas <- adas5 %>% ...` (line 183). The attribute-fix loop and the write step then reference an object `adas` that is never created in the program: `for (col in colnames(adas))` (line 197) and `write_dataset_json_with_metadata(adas, adadas_spec, "adadas", ...)` (line 206). In the ADRG-prescribed run order (adsl → adadas → … → TLFs, ADRG §9.5), the program stops with "object 'adas' not found" and writes nothing. If `tlf-primary.r` has already been run in the same R session, it leaves an `adas` object behind (the filtered ACTOT/EFFFL/ANL01FL subset), and `adadas.r` would silently overwrite `adadas.json` with that analysis subset instead of the full dataset.
- **Evidence:** Dataset-JSON headers: `adadas.json` `datasetJSONCreationDateTime` = 2026-05-05T17:10:43, while adsl/adae/adlbc/adtte = 2026-06-28T22:27–22:28. The submitted ADADAS was therefore not produced in the same run as the other ADaM datasets, which is consistent with the write step failing. Independent check: re-deriving ADADAS ACTOT from QS + ADSL (ADY windows, closest-to-target ANL01FL, LOCF to visits 0/8/16/24) reproduces all 1,016 ANL01FL = Y records and all 222 LOCF records, with 0 mismatches in AVAL, CHG or DTYPE. ADSL-derived variables in ADADAS (TRTSDT, EFFFL, TRTP, SITEGR1, COMP24FL) agree with the current ADSL for all 254 subjects. So the content is correct; the program is not.
- **Impact:** The pilot's stated objective (cover letter: FDA to "reproduce the JSON datasets and analysis results") fails for the dataset behind the primary efficacy table. A reviewer following the ADRG cannot regenerate ADADAS, and could unknowingly create a wrong one.
- **Recommended follow-up:** Replace `adas` with `adadas` on lines 197–206. Re-run the full pipeline in a clean session, regenerate adadas.json, diff it against the submitted file and resubmit with a single consistent creation timestamp.
- **reviewer_question:** Please confirm how the submitted adadas.json (created 2026-05-05) was generated, given that the submitted adadas.r cannot write it.

### ADAM-ADSL-001: Actual treatment set equal to planned treatment; 12 subjects randomized to High Dose received only Low Dose, contradicting the ADRG
- **Severity:** High
- **Type:** Traceability / Conclusion-impacting (safety)
- **Dataset/Output:** ADSL.TRT01A/TRT01AN; ADAE.TRTA; ADTTE.TRTA; Figure 14-1; ADRG §3.2
- **Finding:** `adsl.r` hard-codes `TRT01A = TRT01P`, with the program comment "It is assumed TRT01A=TRT01P which is not really true". ADRG §3.2 states: "All subjects received the treatment arm to which they were randomised and so the planned treatment is equivalent to the actual treatment for all subjects." SDTM contradicts both: DM.ACTARM = "Xanomeline Low Dose" for 12 subjects with ARM = "Xanomeline High Dose".
- **Evidence:** DM ARM × ACTARM: High→High 72, High→Low 12. EX for those 12 has a single 54 mg record and no 81 mg exposure. TRTDURD is 1–14 days (median 5.5), and all 12 discontinued (AE 5, withdrawal 3, protocol violation 2, physician decision 1, sponsor 1). Subjects: 01-701-1181, 01-701-1360, 01-703-1403, 01-705-1382, 01-708-1213, 01-708-1236, 01-708-1372, 01-709-1329, 01-709-1424, 01-711-1433, 01-714-1425, 01-716-1030. Figure 14-1 by TRT01A gives High 84 at risk / 61 events and HR vs placebo 5.03 (3.18–7.94). By DM.ACTARM it gives High 72 / 60 events, HR 5.18 (3.28–8.18), and Low 96 / 63 events, HR 4.06 (2.59–6.36). One of the 12 (01-701-1360) had a derm event on Day 3 while on 54 mg, which is currently attributed to High Dose.
- **Impact:** Every safety analysis "by actual treatment" (ADRG §3.2) is actually by planned treatment. The direction of the dermatologic dose-response is unchanged, but dose-specific safety rates, exposure (AVGDD for High Dose 54–78.6 mg/day) and any label dose-response statement are attributed to the wrong dose for 14% of the High-Dose arm. The ADRG statement is factually incorrect.
- **Recommended follow-up:** Derive TRT01A from EX/DM.ACTARM (or document the rule used to define actual treatment during titration). Correct ADRG §3.2. Re-run Figure 14-1 and the ADAE/ADTTE safety summaries by actual treatment.
- **traceability_path:** Figure 14-1 strata → ADTTE.TRTA → ADSL.TRT01A (= TRT01P) → DM.ACTARM / EX.EXDOSE

### SDTM-AE-001: AESER = "N" for 36 AE records that meet seriousness criteria, including all 3 fatal AEs
- **Severity:** High
- **Type:** Conclusion-impacting (safety) / Traceability
- **Dataset/Output:** SDTM AE → ADAE.AESER, AOCC02FL/AOCC03FL/AOCC04FL (serious first-occurrence flags)
- **Finding:** AESER is inconsistent with the seriousness criteria. Only 3 records (3 subjects) have AESER = Y. Another 36 records have at least one criterion = Y but AESER = N: AESHOSP 30, AESLIFE 5, AESCAN 4, AESDISAB 1 and AESDTH 3 (some records have more than one).
- **Evidence:** All 3 fatal AEs have AEOUT = FATAL, AESDTH = Y and AESER = N: 01-701-1211 SUDDEN DEATH (Low Dose), 01-704-1445 COMPLETED SUICIDE (Placebo), 01-710-1083 MYOCARDIAL INFARCTION (Placebo). Other examples: colon cancer, prostate cancer and malignant fibrous histiocytoma (AESCAN = Y), and hip fractures, TIA and GI haemorrhage with hospitalization (AESHOSP = Y). Subjects with an AESER-based treatment-emergent SAE: Placebo 0 / Low 1 / High 2. Subjects with any seriousness criterion (TEAE): Placebo 6 / Low 10 / High 9. ADAE serious first-occurrence flags (AOCC02FL etc.) are keyed on AESER = Y, so they flag only 3 records.
- **Impact:** Any SAE summary built from ADAE would under-report serious AEs about 8-fold (3 vs 25 subjects) and would report zero serious fatal events while 3 deaths occurred. This directly affects benefit-risk, expedited-reporting reconciliation and labeling. No AE summary table was submitted, so the defect would not be visible to a reviewer of the TLFs alone.
- **Recommended follow-up:** Reconcile AESER against the seriousness criteria and the SAE database. Correct SDTM AE, regenerate ADAE (AOCC02FL–AOCC04FL) and provide an SAE/death listing.
- **reviewer_question:** Were events with AESHOSP/AESLIFE/AESDTH = Y and AESER = N reported as SAEs to the safety database?

### Medium

### ADAM-ADADAS-002: Primary-endpoint missing data are heavily differential, and the estimand mixes LOCF with off-treatment retrieved values
- **Severity:** Medium
- **Type:** Interpretability / Conclusion-impacting
- **Dataset/Output:** ADADAS (PARAMCD = ACTOT, AVISITN = 24); Table 14-3.01
- **Finding:** (1) The Week-24 value is LOCF-imputed for 17.7% of Placebo, 39.5% of Low and 44.6% of High subjects. (2) The Week-24 window is open-ended (ADY > 140, AWHI missing). Off-treatment assessments therefore count as observed Week-24 values, including RETRIEVAL visits up to Day 286, a median of 125 days (range 36–271) after the last dose. (3) The package has no SAP or estimand text describing this hybrid strategy (treatment-policy values for retrieved dropouts, LOCF for the rest).
- **Evidence:** Efficacy population, Week 24: observed 65/49/41, LOCF 14/32/33 (Pbo/Low/High). LOCF sources include Week 2 (11), Week 4 (5), Week 6 (11) and Week 8 (29). Observed values with ADT > TRTEDT: 5/23/13; RETRIEVAL-sourced: 5/21/11. Most imputed High/Low subjects discontinued for AEs (25/22). Reproduced primary results match the table exactly (see Clean checks). Observed-case sensitivity (DTYPE blank, n = 65/49/41): High − Pbo −0.65 (95% CI −2.85, 1.55), p = 0.561; Low − Pbo −1.06 (−3.17, 1.04), p = 0.320; dose-response p = 0.416.
- **Impact:** In a progressive disease, carrying forward early (e.g., Week 2–8) scores from active-arm dropouts understates their decline and biases the result in favour of active treatment. The primary conclusion is null under both approaches, so the conclusion does not change, but the reported LOCF analysis cannot be regarded as a valid estimate of any defined estimand.
- **Recommended follow-up:** Provide the SAP and an estimand definition. Justify the open-ended Week-24 window and the inclusion of off-treatment retrieved data. Provide MMRM/multiple-imputation (e.g., jump-to-reference) sensitivity analyses and tipping-point analyses.
- **estimand_component:** Intercurrent event (treatment discontinuation) strategy; missing-data handling.

### TLF-14-3.02-001: Glucose table is labelled "LOCF" and "Primary Endpoint" but is an observed-case analysis of a safety lab; footnote (a) contradicts the baseline column
- **Severity:** Medium
- **Type:** Interpretability
- **Dataset/Output:** Table 14-3.02 (manual PDF p.4); tlf-efficacy.r; ADLBC
- **Finding:** The rendered title reads "Primary Endpoint Analysis: Glucose (mmol/L) - Summary at Week 20 - LOCF". ADLBC has no DTYPE variable and no imputed records, and `tlf-efficacy.r` analyses only observed AVISITN = 20 records. The program's own title is "ANCOVA of Change from Baseline at Week 20", so the rendered titles do not come from the submitted program. Glucose is a safety laboratory parameter, not the primary endpoint. Footnote (a) says the table is "based on participants who have observable data at Baseline and Week 20", but the baseline column uses all ITT subjects in each arm.
- **Evidence:** Reported values are reproduced exactly. Baseline N 86/84, mean 5.6 (2.14) / 5.4 (1.34); Week-20 N 65/31; LS means 0.09 (−0.23, 0.42) Placebo and 0.16 (−0.31, 0.63) High; difference 0.07 (−0.50, 0.63), p = 0.822; RMSE 1.30. Restricted to subjects with Week-20 data (as the footnote states), baseline would be N 65/31, mean 5.75 (2.44) / 5.58 (1.44). An actual LOCF analysis (last post-baseline value through Week 20) gives N 84/80 and difference 0.25 (−0.20, 0.70), p = 0.279. Week-20 availability is 37% (31/84) in High vs 76% (65/86) in Placebo.
- **Impact:** A reader would believe that missing data were imputed and that this is a primary efficacy result. The conclusion (no difference) is unchanged, but the table cannot be trusted as labelled.
- **Recommended follow-up:** Align the title and footnotes with the program and the analysis actually performed (observed case, safety parameter). Make the baseline column consistent with footnote (a). Regenerate the output from the submitted program.

### TLF-14-1-001: KM figure y-axis is labelled "Probability of event" but plots event-free probability; no numeric TTE summary submitted
- **Severity:** Medium
- **Type:** Interpretability
- **Dataset/Output:** Figure 14-1 (manual PDF p.5); tlf-kmplot.r
- **Finding:** `ggsurvfit(...)` with its default `type = "survival"` plots S(t), and the curves start at 1.00 and decrease. The axis is labelled "Probability of event" (`y_scales name`). Read literally, the figure implies placebo has the highest probability of a derm event (curve ends about 0.63), which is the opposite of the truth. No median, event counts, HR, log-rank p-value or censoring footnote is presented.
- **Evidence:** My reproduced KM at Day 180: S(t) = 0.626 (Pbo), 0.126 (Low), 0.092 (High). These values match the plotted curve end-points, so the plotted quantity is event-free probability. Numbers at risk match exactly (Pbo 86 75 65 59 50 47 45 42 40 35 0; Low 84 58 31 20 14 12 8 6 6 5 0; High 84 48 31 14 7 4 4 4 4 3 0). Reproduced summary: events 29/62/61; median not reached (Pbo), 33 days (95% CI 28–51) (Low), 36 days (25–47) (High). Log-rank χ² = 60.3, 2 df, p = 8e-14. Cox HR vs placebo: Low 4.15 (2.65–6.50), High 5.03 (3.18–7.94).
- **Impact:** This is a labelling error that inverts how a key safety figure is read. Missing numeric summaries prevent figure-to-table cross-checking.
- **Recommended follow-up:** Relabel the axis "Probability of no dermatologic event" or plot `type = "risk"`. Add event/censor counts, medians, HR/CI and a censoring-rule footnote.

### ADAM-ADSL-002: TRTEDT imputed to the disposition date for 4 subjects, beyond the last documented dosing; DM.RFXENDTC is inconsistent with EX
- **Severity:** Medium
- **Type:** Traceability
- **Dataset/Output:** ADSL.TRTEDT, TRTDURD, CUMDOSE, AVGDD; SDTM EX, DM
- **Finding:** When EXENDTC is missing on the last EX record, `adsl.r` imputes the end date to the disposition date (`highest_imputation = "Y", max_dates = EOSDT, date_imputation = "last"`). For 4 subjects this pushes TRTEDT 41–154 days past the last known exposure. Separately, DM.RFXENDTC precedes the start of the last EX record for the same 4 subjects.
- **Evidence:** 01-704-1233 (Placebo): last EXSTDTC 2013-04-05, RFXENDTC 2013-04-04, ADSL TRTEDT 2013-07-14 (+101 d). 01-705-1031: 2013-12-19 / 2013-12-18 / 2014-05-11 (+144 d). 01-705-1303: 2013-12-31 / 2013-12-30 / 2014-06-02 (+154 d). 01-705-1377: 2014-01-26 / 2014-01-25 / 2014-03-07 (+41 d). TRTSDT, TRTEDT, TRTDURD and CUMDOSE otherwise reproduce exactly for all 254 subjects, and TRTSDT = DM.RFXSTDTC for all.
- **Impact:** Treatment duration and cumulative/average dose are overstated for these subjects, and any on-treatment window or exposure-adjusted rate would be inflated. The imputation rule appears only in a program comment, not in the ADRG.
- **Recommended follow-up:** Document the TRTEDT imputation rule and justify using the disposition date. Query the missing EXENDTC values. Correct DM.RFXENDTC so it is not earlier than the last EXSTDTC.

### SDTM-AE-002: 230 pairs of AE records are duplicated, identical except for outcome
- **Severity:** Medium
- **Type:** Reproducibility / Interpretability
- **Dataset/Output:** SDTM AE, ADAE (1:1 with AE)
- **Finding:** 460 of 1,191 AE records (230 pairs) share USUBJID, AEDECOD, AESTDTC, AEENDTC, AESEV and AESER and differ only in AEOUT, AESPID and AEDTC. A typical pair has one record with "NOT RECOVERED/NOT RESOLVED" and one with "RECOVERED/RESOLVED".
- **Evidence:** Examples: 01-701-1023 ERYTHEMA 2012-08-07 (AESEQ 1 & 4); 01-701-1047 HIATUS HERNIA 2013-02-12 (AESEQ 1 & 2); 01-701-1111 ERYTHEMA and PRURITUS 2012-09-02 (AESEQ 1/4, 2/5). Subject-level flags (AOCCFL, AOCCPFL, AOCC01FL) reproduce exactly and are unaffected.
- **Impact:** Any event-level AE count (number of events, events per patient-year) would be inflated by up to 24% (230/961). The 1:1 AE-to-ADAE mapping stated in ADRG §5.2.3 carries the duplication into ADAE. Some pairs (e.g., 01-701-1192 PNEUMONIA, 01-710-1002 TIA) are also among the AESER-inconsistent records.
- **Recommended follow-up:** Explain the recording convention (e.g., an ongoing record re-entered at resolution). Either collapse duplicates in SDTM or add an ADaM flag to exclude them from event counts.

### XLAY-AEDISC-001: AE discontinuations (92 subjects) cannot be traced to any AE record; AEACN is blank for all AEs
- **Severity:** Medium
- **Type:** Traceability
- **Dataset/Output:** SDTM DS, AE; ADSL.DSRAEFL/DCSREAS; ADAE.AEACN
- **Finding:** DS shows 92 subjects discontinued for ADVERSE EVENT (8 / 44 / 40), and ADSL DCSREAS and DSRAEFL agree exactly (92). AE.AEACN is empty for 1,191/1,191 records, and no SUPPAE variable identifies the causative AE.
- **Evidence:** `table(AE$AEACN)` = 1,191 blank. All 92 subjects have at least one AE record, but none can be linked to the discontinuation.
- **Impact:** The standard DS = ADSL = ADAE (AEACN) reconciliation cannot be completed. An "AE leading to discontinuation" table by SOC/PT cannot be produced. Dropout for AEs is the dominant missing-data mechanism for the primary endpoint (ADAM-ADADAS-002).
- **Recommended follow-up:** Populate AEACN (DRUG WITHDRAWN) from source, or provide RELREC links between DS and the causative AE.

### XLAY-DSJSON-001: SDTM Dataset-JSON numeric encoding departs from Dataset-JSON v1.1 conventions
- **Severity:** Medium
- **Type:** Standard/metadata
- **Dataset/Output:** All 21 SDTM .json files
- **Finding:** (1) Missing numeric values are encoded as the strings "NA" or " NA" instead of JSON null: 33,888 values, e.g., AE MedDRA code columns 1,191 each, CMENDY 6,816, LBSTNRLO/LBSTNRHI 2,915, VSTPTNUM 5,024. Zero nulls are used anywhere in SDTM. (2) Every SDTM numeric column, including integers such as --SEQ, AGE, --DY and VISITDY, is typed `decimal`, and no `integer` type is used. (3) Number strings are inconsistently formatted: leading spaces (859,898 values, e.g., AESEQ " 1"), scientific notation (66,135 values, e.g., LBSTRESN "3.800000000000000e+01", CMDOSE "1.000000000000000e+00") and padded precision ("33.0000000000000000"). (4) The dataset `label` is an empty array `[]` in all 21 files, and dataset names are lower-case ("dm").
- **Evidence:** Python census of all JSON columns (`json2csv.py`). ADRG §10.1.3 acknowledges the "NAs introduced by coercion" warnings but does not identify the cause in the data.
- **Impact:** A strict Dataset-JSON consumer, or a non-R reader, may read "NA" as text, fail type validation or mis-convert values. Reproducibility depends on R's lenient `as.double()`. Integer/decimal typing affects the targetDataType conversion to XPT/SAS.
- **Recommended follow-up:** Regenerate SDTM JSON with null for missing values, integer types where appropriate, canonical decimal strings, populated dataset labels and upper-case names. Validate against the v1.1 JSON schema.

### ADAM-DSJSON-001: ADaM Dataset-JSON metadata/value mismatches (length, type, missing-value and decimal formatting, broken references)
- **Severity:** Medium
- **Type:** Standard/metadata
- **Dataset/Output:** adae.json, adsl.json, adadas.json, adlbc.json, adtte.json vs adam-pilot-5.xlsx
- **Finding:** Variable names, order, labels and lengths match the spec for all 216 variables, with these exceptions. (1) ADAE.ADURU is declared length 3, but its values are "DAYS" (4 characters, 718 records), so a length-based conversion to XPT would truncate to "DAY". (2) ADSL.RFSTDTC/RFENDTC are spec type `text` but JSON `dataType` = "datetime", while every value is a date only ("2014-01-02"). (3) Missing decimals are "NA" strings in 16,054 ADaM values (e.g., ADADAS CHG 3,835, PCHG 6,143; ADLBC CHG 4,897), while integer columns use null, so missing values are represented two ways in the same files. (4) Decimal strings carry leading blanks and binary-float artefacts (ADSL WEIGHTBL " 76.40000000000001", CUMDOSE "    0", ADADAS PCHG " -100.0000000000000000"). (5) Integer values are serialized as 63.0 in ADSL/ADADAS but as 63 in ADAE/ADTTE. (6) `metaDataRef` and `fileOID` point to a personal local path ("C:/Users/Sam P/Documents/…/define.xml") and to a define.xml that is not submitted.
- **Evidence:** `meta_compare.py` and JSON census. Dates (dataType "date", targetDataType "integer", DATE9.) are correctly ISO 8601 throughout. Record counts in each header equal the row counts for all 26 files.
- **Impact:** Round-tripping to XPT can truncate values, and strict parsers may reject the files. This may explain why ADRG §6.2.1 reports "No issues" for the XPT route but many label and type issues for the v1.0 route. Personal paths in regulatory metadata are a data-handling concern.
- **Recommended follow-up:** Correct the ADURU length (4) and the RFSTDTC/RFENDTC dataType. Emit null for missing values and canonical decimals. Remove local paths, and reference the submitted define.xml.

### XLAY-DOC-001: Key package components are missing, and the ADRG contains statements contradicted by the package
- **Severity:** Medium
- **Type:** Traceability
- **Dataset/Output:** ADRG; package inventory
- **Finding:** The package has no define.xml, SAP, protocol or analysis-results metadata. The spec "Analysis Results" sheet is empty, although the helper code says "See analysis results metadata for table 14-3.01", and the ACTOT method refers to "SAP section 14.2". ADRG inaccuracies: (a) §5.2.1 "All patients in DM were included in ADSL" (306 in DM vs 254 in ADSL); (b) §3.2 "all subjects received the treatment arm to which they were randomised" (see ADAM-ADSL-001); (c) §6.1 says define.xml was evaluated, but none is submitted; (d) §7.2 names output files adas.json and adlb.json, whereas the actual files are adadas.json and adlbc.json; (e) the text refers to "Pilot 3" in several places (§5.1, §7.2); (f) §7.1 says programs were created on Linux, but the JSON `sourceSystem` is "R on mingw32" (Windows); (g) §7.4 lists visR 0.3.1, which is not in renv-lock, while ggsurvfit 1.1.0 (used by tlf-kmplot.r) is not listed; (h) EFFFL and COMP24FL are listed as core variables, but their definitions are not given (EFFFL requires both ADAS-Cog and CIBIC+ post-baseline, which excludes 20 ITT subjects); (i) the ADRG title for Table 14-3.02 differs from the rendered title.
- **Impact:** The reviewer cannot verify that the analyses follow pre-specified methods, and several ADRG statements cannot be relied on.
- **Recommended follow-up:** Submit define.xml (with ARM), the SAP and the protocol. Correct the ADRG statements listed above.

### TLF-14-3.01-002: The other primary endpoint (CIBIC+) is not analysed, and multiplicity across endpoints and dose comparisons is undefined
- **Severity:** Medium
- **Type:** Interpretability
- **Dataset/Output:** Table 14-3.01; ADRG §5.2.2; ADSL.EFFFL
- **Finding:** The ADRG calls ADAS-Cog "one of the primary efficacy endpoints", and EFFFL requires CIBIC+ data, but the package contains no CIBIC+ ADaM dataset or output. Table 14-3.01 presents 1 dose-response and 3 pairwise tests without adjustment, and there is no pre-specified testing strategy.
- **Evidence:** QS contains CIBIC records (used only for the EFFFL derivation). There is no ADCIBC dataset or TLF.
- **Impact:** The efficacy assessment is incomplete. Because ADAS-Cog is null (all p ≥ 0.23), there is no over-claiming risk, but the benefit side of the benefit-risk assessment cannot be fully evaluated.
- **Recommended follow-up:** Provide the CIBIC+ analysis and the pre-specified multiplicity strategy for the co-primary endpoints and the dose comparisons.

### XLAY-REAL-001: Visit dates are evenly distributed across all seven weekdays, with about 30% of clinic visits on weekends
- **Severity:** Medium
- **Type:** Interpretability (data realism / operational plausibility)
- **Dataset/Output:** SDTM SV (also LB, VS, QS dates)
- **Finding:** Out-patient clinic visits are normally concentrated on weekdays. Here the weekday distribution is nearly uniform.
- **Evidence:** SV, n = 3,559: Mon 12.8%, Tue 13.2%, Wed 16.3%, Thu 14.4%, Fri 13.4%, Sat 15.7%, Sun 14.2%. All other realism signals are plausible (visit-day SD 5.7 d; physiological correlations; site effects).
- **Impact:** For a real submission this suggests systematic date shifting/perturbation or an operational artefact. All study-day derivations (ADY, windows, TEAE, TTE) depend on these dates. The data are known to be the de-identified public CDISC pilot dataset, so date perturbation is the likely explanation.
- **Recommended follow-up:** Document any date de-identification and confirm that relative study days are preserved. Otherwise explain the weekend visit activity by site.

### Low

### ADAM-ADTTE-001: ADTTE censoring source and description inconsistencies; one subject censored after the date of death
- **Severity:** Low
- **Type:** Traceability
- **Dataset/Output:** ADTTE (PARAMCD = TTDE); adtte.r
- **Finding:** (1) Censoring uses the DS disposition date (EOSDT), or RFENDTC for deaths, but SRCVAR = "RFENDT" and EVNTDESC = "Study Completion Date" for all 102 censored subjects, including 58 who discontinued. (2) For death subject 01-710-1083, DTHDTC = 2013-08-02 and DS death date = 2013-08-02, but RFENDTC = 2013-08-03, so the subject is censored one day after death (ADT 2013-08-03). SV also contains a WEEK 2 visit dated 2013-08-03, after death. (3) EVNTDESC has a spelling error ("Dematologic Event Occured"). (4) TRTEMFL has no end-of-treatment window, so events through study end are eligible; 2 events start after TRTEDT (both within 30 days).
- **Evidence:** ADTTE reproduces exactly from ADAE + DS + ADSL (254/254: CNSR, ADT, AVAL, STARTDT = TRTSDT; AOCC01FL 152/152). An on-treatment sensitivity analysis (censored at TRTEDT) gives events 28/62/60 and log-rank χ² = 63.4 (vs 60.3), so the conclusion is unchanged.
- **Impact:** Minor. Traceability metadata misdescribe the censoring source, and a censoring date after death is logically invalid.
- **Recommended follow-up:** Censor deaths at DTHDTC. Set SRCDOM/SRCVAR to DS/DSSTDTC and describe the censoring reason accurately. Query the post-death SV record.

### ADAM-ADLBC-001: ANRIND/BNRIND do not represent the normal-range indicator; ANL01FL is not unique
- **Severity:** Low
- **Type:** Standard/metadata
- **Dataset/Output:** ADLBC
- **Finding:** ANRIND is derived as L if AVAL < 0.5×LLN and H if AVAL > 1.5×ULN, which is a clinically-significant threshold rather than the reference range. It is set to "N" when AVAL is missing (10 records), and it never takes the value "L". ANL01FL = "Y" appears twice for 1,063 subject-parameters because the EOT copy record shares its LBSEQ.
- **Evidence:** ANRIND H = 189 vs LBNRIND HIGH = 1,132. 10 records have AVAL missing and ANRIND = "N". AVAL equals LB.LBSTRESN for all records.
- **Impact:** None of the submitted TLFs use these variables. A future shift table built from ANRIND would mislead.
- **Recommended follow-up:** Rename the variable or align its definition with ADaM (use the reference range). Leave ANRIND missing when AVAL is missing. Make ANL01FL unique or define it at the AVISIT level.

### TLF-14-2.01-001: Demographic table hides missing weight/BMI and omits sex
- **Severity:** Low
- **Type:** Interpretability
- **Dataset/Output:** Table 14-2.01; ADSL
- **Finding:** Low Dose weight and BMI summaries are based on n = 83, not the header N of 84, with no n row. The missing subject is 01-702-1082: there is no Visit-3 weight, although screening and Week-2 weights (54.43 kg) exist. Sex and ethnicity, which are standard demographic variables available in ADSL, are not displayed.
- **Evidence:** All displayed cells reproduce exactly. Examples: Age mean (SD) 75.21 (8.59) / 75.67 (8.29) / 74.38 (7.89); age groups 14/42/30, 8/47/29, 11/55/18; race counts; height, weight, BMI and MMSE mean (SD), median, min–max. Sex F/M: 53/33, 50/34, 40/44.
- **Recommended follow-up:** Add n rows for continuous variables, and add sex and ethnicity. Document the Visit-3-only baseline weight rule (ADRG §10.3).

### TLF-14-3.02-002: Glucose CI uses a normal quantile; RMSE uses an n divisor
- **Severity:** Low
- **Type:** Reproducibility
- **Dataset/Output:** Table 14-3.02; tlf-efficacy.r
- **Finding:** The pairwise CI is computed as estimate ± 1.96×SE instead of using t(93), and the "Root Mean Squared Error" is sqrt(mean(residual²)) rather than the model σ. Footnote (b) does not describe either choice.
- **Evidence:** Reported (−0.50, 0.63) vs t-based (−0.51, 0.64). Reported RMSE 1.30 vs σ = 1.32.
- **Recommended follow-up:** Use t-based limits consistent with the LS-mean CIs, or footnote the choice.

### TLF-PROG-001: TLF programs depend on session state and have side effects
- **Severity:** Low
- **Type:** Reproducibility
- **Dataset/Output:** tlf-primary.r, pilot5-helper-fcns.r
- **Finding:** `tlf-primary.r` calls `str_replace_all()`, and the helper functions call `str_pad()`, `glue()` and `tibble()`, but neither file attaches stringr, glue or tibble. They run only because earlier programs in the same session loaded these packages. `efficacy_models()` sets `options(contrasts = c("contr.sum", "contr.poly"))` and never restores it, which changes the contrasts for any later model in the session.
- **Recommended follow-up:** Make each program self-contained with explicit `library()` calls or `pkg::` prefixes, and restore options with `on.exit(options(op))`.

### TLF-GEN-001: Rendered outputs exist only as a compiled report inside the programs folder
- **Severity:** Low
- **Type:** Traceability
- **Dataset/Output:** pilot5-cmb-report-manual.pdf
- **Finding:** No individual TLF output files (the rtf/pdf/out files that ADRG §9.5 says the programs create) are submitted. The four displays appear only in a compiled "manual" PDF placed in `programs/`. Table 14-3.01 shows "Source: <run interactively>". The outputs are dated 2026-06-28, after the ADADAS creation date (2026-05-05). Titles in the compiled PDF differ from the program titles (see TLF-14-3.02-001).
- **Recommended follow-up:** Submit each output as a separate file in the expected eCTD location, generated by the submitted programs, with program-path footers.

### SDTM-AE-003: MedDRA coding incomplete; relationship missing for 4 TEAEs
- **Severity:** Low
- **Type:** Standard/metadata
- **Dataset/Output:** SDTM AE, ADAE
- **Finding:** All MedDRA numeric codes (AELLTCD, AEPTCD, AEHLTCD, AEHLGTCD, AEBDSYCD, AESOCCD) are missing ("NA"). AEHLT/AEHLGT contain placeholder tokens (e.g., "HLT_0617", "HLGT_0152"). The MedDRA version is 8.0. AEREL is blank for 4 TEAEs (01-704-1135 RASH ×2; 01-718-1254 DYSPHAGIA, FOOD CRAVING).
- **Recommended follow-up:** Provide a fully coded MedDRA hierarchy (current version) and complete causality.

### SDTM-DM-001: Informed consent date not populated
- **Severity:** Low
- **Type:** Traceability
- **Dataset/Output:** SDTM DM
- **Finding:** RFICDTC is blank for all 306 subjects (declared length 1), so the order consent ≤ randomization ≤ first dose cannot be verified.
- **Recommended follow-up:** Populate RFICDTC from the DS informed-consent milestone, or explain why it is absent.

---

## Findings — Simulation realism

Not applicable: the package was reviewed as a real submission, so realism concerns appear above (XLAY-REAL-001, SDTM-AE-001, SDTM-AE-002, SDTM-AE-003).

## Findings summary table

| # | Severity | Type | Category | Output/Dataset | Finding (short) |
|---|---|---|---|---|---|
| 1 | High | Reproducibility | Integrity | adadas.r / ADADAS | Program writes undefined object `adas`; cannot regenerate submitted adadas.json (content independently reproduced) |
| 2 | High | Traceability / Conclusion-impacting | Integrity | ADSL.TRT01A, Fig 14-1, ADRG | TRT01A = TRT01P; 12 High-arm subjects received only 54 mg; ADRG claim false |
| 3 | High | Conclusion-impacting | Integrity | SDTM AE / ADAE | AESER = N for 36 records meeting seriousness criteria incl. all 3 deaths; SAE subjects 3 vs 25 |
| 4 | Medium | Interpretability | Integrity | ADADAS / T14-3.01 | Differential LOCF (17.7/39.5/44.6%) plus off-treatment retrieved W24 values; no estimand |
| 5 | Medium | Interpretability | Integrity | T14-3.02 | Labelled LOCF / "Primary Endpoint" but observed-case safety lab; footnote vs baseline N |
| 6 | Medium | Interpretability | Integrity | Fig 14-1 | Y-axis "Probability of event" but plots survival; no numeric TTE summary |
| 7 | Medium | Traceability | Integrity | ADSL TRTEDT / EX / DM | TRTEDT imputed to EOS (+41 to +154 d) for 4 subjects; RFXENDTC < last EXSTDTC |
| 8 | Medium | Reproducibility | Integrity | AE / ADAE | 230 duplicated AE pairs differing only by outcome |
| 9 | Medium | Traceability | Integrity | DS / AE / ADSL | AEACN blank; 92 AE discontinuations untraceable to AEs |
| 10 | Medium | Standard/metadata | Integrity | SDTM JSON | "NA" strings for missing (33,888), all-decimal typing, sci-notation/padded strings, empty labels |
| 11 | Medium | Standard/metadata | Integrity | ADaM JSON vs spec | ADURU length 3 vs "DAYS"; RFSTDTC datetime type; "NA" strings; float artefacts; local-path define ref |
| 12 | Medium | Traceability | Integrity | ADRG / package | No define.xml / SAP / protocol / ARM; multiple false ADRG statements |
| 13 | Medium | Interpretability | Integrity | T14-3.01 | CIBIC+ primary not analysed; multiplicity undefined |
| 14 | Medium | Interpretability | Realism | SV dates | Uniform weekday distribution, ~30% weekend visits |
| 15 | Low | Traceability | Integrity | ADTTE | Censor metadata mislabelled; death censored 1 day after death; typo |
| 16 | Low | Standard/metadata | Integrity | ADLBC | ANRIND not reference-range based; "N" when missing; ANL01FL duplicates |
| 17 | Low | Interpretability | Integrity | T14-2.01 | Weight/BMI n = 83 not shown; sex/ethnicity omitted |
| 18 | Low | Reproducibility | Integrity | T14-3.02 | z-based CI; n-divisor RMSE |
| 19 | Low | Reproducibility | Integrity | TLF programs | Unattached package dependencies; contrasts option leak |
| 20 | Low | Traceability | Integrity | Outputs | Only a compiled PDF in programs/; "<run interactively>" source |
| 21 | Low | Standard/metadata | Realism | AE | MedDRA codes missing / placeholders; AEREL blank ×4 |
| 22 | Low | Traceability | Integrity | DM | RFICDTC blank for all subjects |

## Clean checks

- **Table 14-3.01 primary ANCOVA:** all cells reproduce exactly from ADADAS. N 79/81/74. Baseline mean (SD) 24.1 (12.19) / 24.4 (12.92) / 21.3 (11.74). Week 24 26.7 (13.79) / 26.4 (13.18) / 22.8 (12.48). CHG 2.5 (5.80) / 2.0 (5.55) / 1.5 (4.26), medians and ranges as displayed. Dose-response F-test p = 0.2447 (reported 0.245). Low − Pbo −0.467 (SE 0.818), 95% CI (−2.08, 1.15), p = 0.5688 (reported −0.5 (0.82), (−2.1; 1.1), 0.569). High − Pbo −1.006 (0.841), (−2.66, 0.65), p = 0.2326 (reported −1.0 (0.84), (−2.7; 0.7), 0.233). High − Low −0.539 (0.836), (−2.19, 1.11), p = 0.5196 (reported −0.5 (0.84), (−2.2; 1.1), 0.520). Model, covariates (SITEGR1, BASE) and proportional LS-mean weighting match footnote [1].
- **ADADAS from SDTM QS:** ACTOT equals the item sum for all 797 records with complete items. Windows (≤1, 2–84, 85–140, >140), ANL01FL (closest to target, ties to the later record) and LOCF give 0 mismatches. BASE and ABLFL are present for all 254 subjects. This includes the 19 DTYPE corrections the ADRG documents relative to the legacy CDISC ADADAS.
- **Table 14-3.02 glucose:** every number reproduces (Ns, means, SDs, LS means/CIs, difference, p = 0.822, RMSE 1.30).
- **Table 14-2.01 demographics:** all cells reproduce, and the header N matches ITT.
- **Figure 14-1:** at-risk numbers at all 11 time points reproduce exactly for all 3 arms. ADTTE reproduces from ADAE/DS/ADSL for 254/254 subjects. Events + censored = N in every arm (29 + 57 = 86; 62 + 22 = 84; 61 + 23 = 84).
- **ADSL:** one record per subject. TRTSDT = first EX start = DM.RFXSTDTC (254/254). TRTDURD = TRTEDT − TRTSDT + 1. CUMDOSE reproduces. AGE = DM.AGE; AGEGR1, HEIGHTBL, WEIGHTBL and BMIBL (round-half-up) reproduce. MMSETOT = item sum. SITEGR1 pooling exactly follows the "<3 subjects in any arm" rule (sites 702, 706, 707, 711, 714, 715, 717 → 900). SAFFL, ITTFL, EFFFL and COMP24FL re-derive with 0 mismatches. DCSREAS mapping (Protocol Violation split into I/E Not Met ×3) is consistent with DS.
- **Deaths:** 3 deaths agree across DM, DS, AE (fatal) and ADSL. There are no EX, LB, VS or QS records after death.
- **Screen failures** have no EX, AE or post-baseline QS records. No start date is after its end date in AE, EX or CM.
- **ADAE:** TRTEMFL, ASTDY, ADURN, CQ01NAM, AOCCFL and AOCC01FL re-derive with 0 mismatches. There are no AEs after death. Partial-date imputation (day → 01) never falls in the TRTSDT month, so no TEAE misclassification results. The 11 year-only AE dates (1977–2007) are correctly left non-treatment-emergent.
- **Dataset-JSON:** header `records` = row count for all 26 files. ADaM variable names, order, labels and spec lengths match the spec for all 216 variables (apart from items in ADAM-DSJSON-001). Date variables are ISO 8601 with targetDataType integer.
- **Multiplicity:** no result is presented as statistically significant, and unadjusted p-values are labelled as such.

## Limitations

- There is no SAP, protocol, CSR or define.xml, so I could not check compliance with pre-specified methods, windows, estimands or multiplicity. Footnotes, the spec "Methods" sheet and the ADRG were used instead.
- I did not execute the sponsor programs, because the required packages (admiral, metacore, metatools, xportr, datasetjson, Tplyr, rtables, pharmaRTF, r2rtf, ggsurvfit) are not installed. The program defects (ADAM-ADADAS-001, TLF-PROG-001) come from code inspection and file metadata, not from a run log.
- No AE, SAE, disposition, exposure, lab-shift or vital-sign TLFs were submitted, so the safety review was limited to dataset-level reconciliation.
- CIBIC+ (the other primary) and the ADLBC parameters other than glucose were not analysed in depth.
- Realism checks are descriptive. The known public, de-identified origin of the data limits how far operational artefacts (e.g., weekday distribution) can be interpreted.
- The review used only the package contents; no external sources were consulted.
