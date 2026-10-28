---
title: Statistical-reviewer findings — R Consortium Submission Pilots 1, 3 and 5
date: 2026-10-27
reviewer: Claude (statistical-reviewer skill, pharma-skills)
study: CDISCPILOT01 (xanomeline vs placebo, mild-to-moderate Alzheimer's disease)
packages:
  - RConsortium/submissions-pilot1-to-fda @ dc0d243
  - RConsortium/submissions-pilot3-adam-to-fda @ 1af41d8
  - RConsortium/submissions-pilot5-datasetjson-to-fda @ 0801a04
per_pilot_reports:
  - statistical_review_pilot1_2026-10-27.md
  - statistical_review_pilot3_2026-10-27.md
  - statistical_review_pilot5_2026-10-27.md
---

# Statistical-reviewer findings: Submission Pilots 1, 3 and 5

## 1. Summary

The `statistical-reviewer` skill reviewed three R Consortium FDA submission packages separately. A different reviewer handled each package and saw none of the others' work. All three packages carry the same study, CDISCPILOT01, in a different submission format:

- **Pilot 1:** R-generated tables, listings and figures (TLFs) from SAS-built ADaM datasets.
- **Pilot 3:** R-built ADaM datasets plus TLFs.
- **Pilot 5:** ADaM and SDTM delivered as Dataset-JSON.

The data are the public CDISC pilot test data.

**Headline:**

- **Efficacy results reproduce.** In all three packages, every submitted efficacy and demographic number reproduces within tolerance: ADAS-Cog Week 24, demographics, glucose, and the numbers at risk in the time-to-event figure. The primary conclusion, no dose response, holds under every sensitivity analysis the reviewers ran.
- **The real problems are elsewhere.** They are in the safety source data and in what the outputs do or do not say. Several of them would need explanation in a clinical study report (CSR):
  - Serious adverse events are under-flagged.
  - Discontinuations due to adverse events can't be traced to an event.
  - Week 24 imputation is heavy and differs by arm.
  - Actual treatment is set equal to planned treatment.
  - A co-primary endpoint was never analysed.

| | Pilot 1 | Pilot 3 | Pilot 5 |
|---|---|---|---|
| Format | XPT ADaM + R TLFs | XPT SDTM + R-built ADaM + R TLFs | Dataset-JSON SDTM + ADaM |
| Layers reviewed | TLF + ADaM | TLF + ADaM + SDTM + SAP | ADaM + SDTM + TLFs (only inside a compiled PDF) |
| Overall result | PASS WITH FINDINGS | FAIL | FAIL |
| Findings (High / Medium / Low) | 3 / 8 / 5 | 2 / 8 / 7 | 3 / 11 / 8 |
| Data realism score | 7/10 | 7/10 | 7/10 |

> **Note on overall results.** Pilot 1 got PASS WITH FINDINGS while Pilots 3 and 5 got FAIL, even though all three share the same High safety findings. The Pilot 1 reviewer judged that the High findings do not affect any submitted table. The Pilot 3 and 5 reviewers weighted the SAE under-reporting as conclusion-impacting. On a harmonized reading, all three packages share the same safety-data defects. The rating difference reflects how the reviewers applied the severity rule, not a difference in the data.

## 2. Primary and key results: reproduction

| Output | Reported | Reproduced | Status |
|---|---|---|---|
| T14-3.01 ADAS-Cog (11) Week 24, dose-response p | 0.245 | 0.2447 | Match (all three pilots) |
| T14-3.01 Low vs Placebo, LS-mean difference / p | −0.5 / 0.569 | −0.467 / 0.5688 | Match |
| T14-3.01 High vs Placebo, LS-mean difference (SE) / p | −1.0 (0.84) / 0.233 | −1.006 (0.841) / 0.2326 | Match |
| T14-2.01 Demographics N | 86 / 84 / 84 | 86 / 84 / 84 | Match |
| T14-3.02 Glucose ANCOVA, difference / p | 0.07 / 0.822 | 0.07 / 0.822 | Match (but the table is mislabelled; see §3) |
| Fig 14-1 KM numbers at risk (33 cells) | — | Exact | Match |
| Fig 14-1 hazard ratios vs placebo (not reported) | not reported | Low ≈ 4.1, High ≈ 4.9–5.0; log-rank p < 0.001 | Reproduced by the reviewers |

The hazard ratios differ slightly between reviewers: Pilot 1 got 4.08 / 4.92 and Pilot 3 got 4.15 / 5.03. That is a difference in model specification, not in the data. I re-ran a three-arm Efron Cox model on both packages' ADTTE and got the identical result, 4.148 / 5.026.

**Robustness of the primary result (High vs Placebo):**

| Analysis | Estimate | p |
|---|---|---|
| Submitted (LOCF ANCOVA) | −1.01 | 0.233 |
| Observed cases | −0.65 | 0.56 |
| On-treatment values only (Pilot 1) | −1.00 | 0.188 |
| All randomized (Pilot 1) | −1.05 | 0.172 |
| MMRM per SAP (Pilot 3) | n.s. | n.s. |
| Dose-response: OC / completers / BOCF (Pilot 3) | — | 0.416 / 0.234 / 0.191 |

## 3. Findings common to all three packages

Severity is shown as each pilot's reviewer assigned it. "—" means the reviewer could not see the issue (layer not provided) or did not raise it.

| # | Finding | Pilot 1 | Pilot 3 | Pilot 5 | Where it belongs |
|---|---|---|---|---|---|
| C1 | **Serious AEs under-flagged.** AESER = "N" on 36 AE records that meet at least one seriousness criterion, including all 3 fatal AEs. Subjects with an SAE: 3 by AESER vs 25 by the criteria. | High | High | High | CSR safety narrative; data fix |
| C2 | **AE discontinuations can't be traced.** AEACN is blank on all 1,191 AE records, so the 92 discontinuations due to AEs (8 / 44 / 40) can't be linked to a causative AE. Pilot 3 also found 5 AE-related discontinuations coded as physician or subject decision. | High | High | Medium | CSR disposition; data fix |
| C3 | **Differential Week 24 LOCF.** 17.7% (Placebo), 39.5% (Low) and 44.6% (High) of Week 24 ADAS-Cog values are imputed. No sensitivity analysis or estimand is submitted. The conclusion is robust (§2). | Medium | Medium | Medium | CSR efficacy interpretation |
| C4 | **Co-primary CIBIC+ not analysed.** There is no output for it, and no multiplicity strategy across the two primary endpoints. Reproduced: Week 24 is null (Pilot 3 p = 0.960; Pilot 1 p = 0.49 / 0.80). | Medium | Medium | Medium | CSR efficacy; package scope |
| C5 | **Glucose table mislabelled.** T14-3.02 is titled "Primary Endpoint … LOCF" but is an observed-case analysis of a safety lab. SAP §15.3 rules out ANCOVA for labs, and 63% of High Dose values are missing. | Medium | Medium | Medium | Output correction; CSR |
| C6 | **KM figure mislabelled.** The y-axis says "Probability of event" but the curves are event-free probability. There are no medians, HRs or log-rank results, although the SAP asks for them. | Medium | Medium | Medium | Output correction; CSR |
| C7 | **Weekend visits.** About 30% of clinic visits and treatment starts fall on Saturday or Sunday, with a uniform weekday distribution. This is likely an artefact of date shifting during de-identification. | Medium | Medium | Medium | Realism signal; explain in reviewer's guide |
| C8 | **Demographic table incomplete.** Sex and ethnicity are omitted (female 61.6% / 59.5% / 47.6%), and weight/BMI n = 83 is not shown. | Medium | Medium | Low | Output correction |
| C9 | **Time-to-event metadata.** One death is censored 1 day after the death. EVNTDESC is generic or mislabelled. AE-discontinuation censoring is 2 / 12 / 10 with no sensitivity analysis. | Low | Low | Low | ADTTE documentation; CSR |
| C10 | **Glucose CI method.** The difference CI uses a normal (z) quantile, not t, and the RMSE uses an n divisor (1.30 vs model 1.32). | Low | — | Low | Output correction |

## 4. Findings seen in only one or two packages

| # | Finding | Pilot | Severity | Note |
|---|---|---|---|---|
| S1 | **Efficacy assessments after discontinuation.** 37 subjects have ADAS-Cog scores 28–266 days after their recorded study discontinuation. On-treatment only, Low vs Placebo moves from −0.47 to −0.96 (p = 0.195). | 1 | High | The Pilot 5 reviewer raised the same pattern inside C3 ("off-treatment retrieved W24 values up to Day 286"). It was not raised for Pilot 3. |
| S2 | **Actual treatment = planned treatment.** 12 subjects randomized to High Dose received only 54 mg: SDTM DM.ACTARM = "Xanomeline Low Dose", and EX shows only 54 mg. `adsl.r` sets TRT01A = TRT01P, and the program comments that this "is not really true". The ADRG claims everyone received their randomized arm. By actual treatment, High Dose is 60 events in 72 subjects, not 61 in 84. | 5 | High | **Also present in Pilot 3:** confirmed in Pilot 3's DM/EX, same 12 subjects, same `TRT01A = TRT01P` line in `adsl.r`. The Pilot 3 reviewer missed it and listed treatment assignment as a clean check. Pilot 1 has no SDTM, so it was not visible there. |
| S3 | **ADADAS program can't regenerate the dataset.** `adadas.r` writes an undefined object (`adas`), so it cannot regenerate `adadas.json`; the dataset's date stamp also differs from the other ADaMs. The content itself was independently reproduced from QS: 1,016 analysis records and 222 LOCF records. | 5 | High | Program reproducibility |
| S4 | **Duplicated AE records.** 230 pairs (460 records) are identical except for outcome, inflating event counts and giving conflicting outcomes. | 3, 5 | Medium | Not visible in Pilot 1 (no SDTM) |
| S5 | **ANRIND is not a normal-range indicator.** It holds a 1.5 × ULN threshold flag: 1,315 values outside the reference range are coded "N", and missing values are also coded "N". | 3, 5 | Medium / Low | Not raised for Pilot 1 |
| S6 | **TRTEDT imputed past last dose.** Treatment end date is imputed to the disposition date, up to about 5 months after the last documented dose (6 subjects in Pilot 3, 4 in Pilot 5). | 3, 5 | Low / Medium | |
| S7 | **Define.xml placeholders.** Placeholder methods ("LB.VISITNUM", "LB.LBSTNRHI") are given for primary variables, and the AOCC01FL text is inverted. The ADRG says "Imputation: Not applicable" despite LOCF. | 1 (3: AOCC01FL only) | Medium | |
| S8 | **Dataset-JSON encoding.** Missing numbers are stored as "NA" text (33,888 in SDTM, 16,054 in ADaM). Other issues: all-decimal typing, scientific-notation strings, ADURU length 3 vs "DAYS", and `metaDataRef` pointing to a personal local path. | 5 | Medium | Format-specific |
| S9 | **Missing package components.** No define.xml, SAP or protocol; the rendered TLFs exist only inside `pilot5-cmb-report-manual.pdf`; and several ADRG statements are contradicted by the data. | 5 | Medium | |
| S10 | **Pairwise results despite failed gate.** Pairwise comparisons are shown although the dose-response gate failed. | 3 | Low | |
| S11 | **Day-formula re-windowing.** The SAP's day formula vs ADY re-windows 3 assessments (p 0.249 vs 0.245). | 3 | Low | |
| S12 | **MMSE inclusion violations.** 2 subjects with MMSE 24 violate inclusion, and there are no protocol-deviation data. | 3 | Low | |
| S13 | **Incomplete coding.** MedDRA coding is incomplete, AEREL is blank for 4 TEAEs, and RFICDTC is blank for all subjects. | 5 | Low | |

## 5. Verification notes

I re-checked the main cross-pilot findings directly against the source data after the reviews finished:

- **C1, confirmed** in Pilot 3 SDTM AE. Using AESDTH, AESHOSP, AESLIFE, AESDISAB, AESCONG and AESCAN, 36 records have a criterion = Y with AESER = N, and 3 records have AESER = Y.
  - **Correction to the Pilot 3 report:** its count of "25 subjects" for the 36 unflagged records should be **22 subjects**. 25 is the number of subjects with any seriousness criterion, including the 3 that are flagged.
  - **Second correction:** the unflagged records include **30** with AESHOSP = Y, not 28.
- **C2, confirmed.** AEACN is empty on all 1,191 records.
- **S2, confirmed in both Pilot 3 and Pilot 5.** 12 High Dose subjects have DM.ACTARM = Low Dose and only 54 mg in EX.
- **KM hazard ratios, re-run.** Identical across Pilot 1 and Pilot 3 ADTTE (§2).

The per-pilot reports have not been changed. These notes supersede them where they differ.

## 6. Signals needing interpretation in the CSR

These items are statistically or clinically meaningful. The tables themselves reproduce, so the issue is how the results are explained.

1. **Safety profile under-states seriousness (C1).** The CSR's "3 SAEs" statement is not supported by the source data. Any SAE summary, the benefit-risk discussion and labeling text would need restating.
2. **Discontinuations due to AEs (C2).** Discontinuations are dose-related (8 / 44 / 40), but they can't be attributed to specific AEs. The CSR cannot describe which events drove dropout.
3. **Missing-data handling of the primary endpoint (C3, S1).** The CSR needs to explain:
   - The large, dose-related LOCF fraction.
   - The mixing of off-treatment retrieved values with LOCF.
   - The absence of a defined estimand.

   Present the sensitivity analyses that support the null result.
4. **Actual vs planned treatment (S2).** 14% of the High Dose arm never reached 81 mg. Safety and time-to-event analyses by actual treatment would differ (High Dose: 60/72 events vs 61/84). The ADRG statement that everyone received their randomized arm is incorrect.
5. **Co-primary endpoint and multiplicity (C4).** CIBIC+ is a declared primary endpoint but has no analysis, and no multiplicity strategy covers the two primaries.
6. **Dermatologic events (C6).** The time-to-first-dermatologic-event effect is large (HR ≈ 4–5, median 33–36 days on active treatment), but the figure is mislabelled and gives no numeric summary.

## 7. Limitations

- **Pilot 1:** no SDTM, SAP, protocol or CSR, so the cross-layer findings (S2, S4) could not be checked there.
- **Pilot 5:** no define.xml, SAP or protocol. Reported values were taken from the compiled PDF inside `programs/`.
- **No sponsor programs run:** the sponsor programs were not executed as submitted. All reproduction used independent R code (haven, survival, emmeans).
- **Public test data:** the data are the public CDISC pilot test data. Realism signals (C7) are expected artefacts of de-identification and would carry different weight in a real submission.
