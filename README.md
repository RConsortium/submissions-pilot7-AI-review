# Pilot 7: AI review of past R Consortium submissions

**Background:** The R Consortium R Submissions Working Group has completed five open submission pilots with the FDA. The FDA has now started to use AI reviewers. We would like to collaborate with the FDA to explore how to streamline submissions in the AI era.

As part of R Consortium Submissions Pilot 7, the original FDA submission pilots (**Pilot 1, Pilot 3 and Pilot 5**) are run through two **open-source AI review tools**, [yamaa](https://github.com/elong0527/yamaa) and the [statistical-reviewer skill](https://github.com/RConsortium/pharma-skills/tree/main/statistical-reviewer), and through **Elsa**, the FDA AI Assistant.

**Aim:** give sponsors practical suggestions that streamline submissions and the FDA reviewer experience, so that promising treatments reach patients faster.

## Project design

| Step | Question | Approach | Status |
|---|---|---|---|
| **Step 1:** Open-source pre-check vs FDA AI review | Would open-source tools used as pre-submission checks cover the issues an FDA AI-assisted review raises? | Run the original Pilot 1 / 3 / 5 packages through yamaa and the statistical-reviewer skill. Run the same packages through Elsa. Compare the findings item by item. | Open-source review done for Pilots 1, 3 and 5. Elsa review done for Pilot 1 and compared with the open-source tools. |
| **Step 2:** Pre-audited resubmission | Does a pre-audited submission package reduce unnecessary reviewer issues and back-and-forth? | Update each package using the open-source findings. Resubmit the enhanced package and rerun Elsa. Compare the issues raised before and after. | Planned |

## Submission packages

The three packages contain the same study in different submission formats. CDISCPILOT01 is xanomeline vs placebo in mild-to-moderate Alzheimer's disease, and the data are the public CDISC pilot test data.

| Package | Format | Repository |
|---|---|---|
| Pilot 1 | SAS-built ADaM (XPT) + R-generated TLFs | [submissions-pilot1-to-fda](https://github.com/RConsortium/submissions-pilot1-to-fda) |
| Pilot 3 | SDTM + R-built ADaM (XPT) + R-generated TLFs | [submissions-pilot3-adam-to-fda](https://github.com/RConsortium/submissions-pilot3-adam-to-fda) |
| Pilot 5 | SDTM + ADaM as CDISC Dataset-JSON | [submissions-pilot5-datasetjson-to-fda](https://github.com/RConsortium/submissions-pilot5-datasetjson-to-fda) |

## Review tools

| | **yamaa** (open source) | **statistical-reviewer** (open source) | **Elsa** (FDA AI Assistant) |
|---|---|---|---|
| Role | Sponsor pre-check: data standards and programming | Sponsor pre-check: independent statistician | FDA statistical filing review |
| What it asks | *Does the documented process reproduce the datasets?* | *Do the submitted data and results hold up?* | *Is the application fileable, and what must the applicant answer?* |
| How | Rebuilds every ADaM dataset from SDTM with executable specifications, and matches the submitted datasets cell by cell. Then checks define.xml, ADRG, SAP and spec text clause by clause against the implementation. | Works from the data as submitted. Reproduces the reported numbers (TLF → ADaM → SDTM), challenges populations, denominators and missing-data handling, and assesses clinical plausibility. | Follows the FDA filing review process: the NDA/BLA statistics filing template and the refuse-to-file criteria in MAPP 6025.4. Queries the submitted datasets and re-runs the primary analysis. Produces refuse-to-file issues and information requests. |
| Best at | Process-level discrepancies, which call for **operational fixes** to specs, define.xml, the ADRG and programs | Data and analysis signals that **need interpretation in the CSR** | The **regulator's view**: fileability, regulatory completeness, and what the agency will ask |
| Source | [yamaa](https://github.com/elong0527/yamaa); results on the [Pilot 7 dashboard](https://rconsortium.github.io/submissions-pilot7-synthetic-data/) | [statistical-reviewer skill](https://github.com/RConsortium/pharma-skills/tree/main/statistical-reviewer) in [pharma-skills](https://github.com/RConsortium/pharma-skills); results in the [consolidated report](reports/report1_stat-reviewer_findings_pilots_1_3_5_2026-10-27.md) and per-pilot reports ([Pilot 1](reports/statistical_review_pilot1_2026-10-27.md), [Pilot 3](reports/statistical_review_pilot3_2026-10-27.md), [Pilot 5](reports/statistical_review_pilot5_2026-10-27.md)) | [Pilot 1 filing review](reports/FDA_filing_agent_reviews/CDISCPILOT01_Statistical_Filing_Review_v2_python.md) |

## Step 1 results

### A) Pilot 1: yamaa vs statistical-reviewer vs Elsa

The Elsa report found **no refuse-to-file issues within the pilot's stated scope** and left the fileability decision to the human reviewer. It raised 6 review items. It also listed 29 further issues that would matter in a real marketing application; most are components absent by design in this pilot, such as the ISS, ISE, CSR, protocol and SAP.

- **statistical-reviewer:** covered 4 of Elsa's 6 review items in full and 1 in part; only the ANL01FL label item was missed. It also found data issues that Elsa did not raise, such as unflagged serious AEs and a co-primary endpoint with no analysis.
- **yamaa:** overlaps with Elsa only at the documentation level: the efficacy-population flag, the imputation documentation and the time-to-event date rule. It reproduced 100% of the ADaM cells from SDTM (9.1 M), and found documentation defects that neither the statistical-reviewer nor Elsa raised.

In conclusion, the three tools look at different layers. The Elsa report checks the package against the FDA refuse-to-file criteria and re-runs the primary analysis. The statistical-reviewer tests the data and results in depth. yamaa tests whether the documented derivation process reproduces the datasets.

**Raised by Elsa and anticipated by the open-source tools:**

- **Primary result reproduces.** Elsa re-ran the ADAS-Cog analysis in Python and the statistical-reviewer in R. Both get −1.006 (High − Placebo) and −0.467 (Low − Placebo), with dose-response p = 0.245, and both confirmed the model specification in the submitted program.
- **20 subjects (7.9%) excluded from the efficacy population without explanation.** The statistical-reviewer had already characterized them: 19 have no post-baseline ADAS-Cog and 1 has no post-baseline CIBIC+. yamaa found that the define.xml source of the efficacy flag (`ADSL.FASFL`) does not exist.
- **ADRG says "Imputation: Not applicable"** although the primary analysis uses LOCF, and the package states no missing-data strategy.
- **No sensitivity analysis for missing data.** The statistical-reviewer ran observed-case, all-randomized and on-treatment analyses; the null result holds.
- **Time-to-event censoring.** The statistical-reviewer reproduced the KM curves and numbers at risk exactly, and flagged the censoring descriptions.
- **Partly anticipated:** no demographic subgroup analyses (the statistical-reviewer flagged that sex and ethnicity are missing from Table 14-2.01), and the CI quantile method (the statistical-reviewer flagged mixed z- and t-based CIs).

**Raised by Elsa only:**

| Type | Findings |
|---|---|
| Regulatory completeness (absent by design in this pilot) | ISS, ISE, CSR, protocol, SAP and Module 2 summaries; SDTM; case report forms; randomization documentation; financial disclosure, user fee and pediatric (PREA) documentation; Form 356h possibly unsigned |
| Technical | Retired MRAN package repository; ANL01FL label differs across datasets; old MedDRA version (v8.0); no software validation evidence (out of scope by design) |

**Found by the open-source tools but not raised by Elsa:**

| Tool | Findings |
|---|---|
| statistical-reviewer | Co-primary CIBIC+ has no output; AESER = "N" on all 3 fatal AEs, and 25 subjects meet seriousness criteria while only 3 are flagged; AEACN blank on all AEs, so the 92 AE discontinuations are untraceable; differential LOCF (17.7 / 39.5 / 44.6%; 79 of the 234 Week 24 values are imputed); 37 subjects with post-discontinuation ADAS-Cog values in the primary analysis; KM y-axis mislabelled, with no HR or medians; glucose table mislabelled; placeholder derivation methods in define.xml |
| yamaa | Documentation defects: BMI formula; lab-ratio limits; completer flag definition; Hy's Law threshold; VISNUMEN filter term |

All of the statistical-reviewer's items above are visible in the datasets, programs, ADRG and define.xml that Elsa had.

**Answer to Step 1, for Pilot 1:** used together, the open-source tools covered the statistical content of the FDA AI review and caught data issues it did not raise. What they do not check is regulatory completeness: required modules, forms and a restorable computing environment. That is the Elsa report's main focus, and a gap a sponsor can close with a completeness checklist before submission.

### B) Pilots 3 and 5: yamaa vs statistical-reviewer

| | Pilot 3 | Pilot 5 |
|---|---|---|
| yamaa: ADaM cells reproduced from SDTM | 100% (2.3 M) | 100% (2.3 M) |
| yamaa: documentation consistency items (conflict / divergence / gap) | 248 (23 / 66 / 150)\* | 233 (18 / 51 / 156)\* |
| statistical-reviewer: findings (High / Medium / Low) | 2 / 8 / 7 | 3 / 11 / 8 |
| statistical-reviewer: overall result | FAIL | FAIL |
| statistical-reviewer: primary efficacy result reproduced | Yes | Yes |

\* The remaining items (9 / 8) are marked "not reviewed" or "unclear".

The two open-source tools complement each other:

- **yamaa** cannot see an error that the source data and the derived datasets share, such as serious AEs flagged "N" at source.
- **The statistical-reviewer** does not audit documentation text, such as a define.xml formula that is wrong but does not change the numbers.

**Found by both tools:**

- The lab normal-range indicator (ANRIND) holds a 1.5 × ULN flag, so 1,315 out-of-range values are coded "Normal".
- The define.xml rule for the dermatologic-event flag (AOCC01FL) is the opposite of the implemented rule (Pilot 3).

**Found by the statistical-reviewer only:**

- **Same safety and efficacy issues as Pilot 1:** serious AEs under-flagged, AEACN blank, differential LOCF, CIBIC+ not analysed, and mislabelled outputs.
- **Actual treatment = planned treatment:** 12 subjects randomized to High Dose received only 54 mg. This is visible only from SDTM, so it could not be checked in Pilot 1.
- **Duplicated AE records:** 230 pairs.
- **Pilot 5 only:** `adadas.r` cannot regenerate `adadas.json`, and there are Dataset-JSON encoding problems ("NA" strings, types, local paths).

**Found by yamaa only:**

- Documented rules that don't reproduce the data: the disposition flag (110 subjects), the end-of-study visit number (all subjects), the ADAS-Cog change from baseline (3,800 records), the treatment-emergent flag (65 records) and the time-to-event date (5 subjects).
- The statistical-reviewer re-derived two of these from source, the ADAS-Cog values and the treatment-emergent flag, and found no mismatches. For those, the defect is in the documented rule, not in the data.

Details: [consolidated statistical-reviewer findings for Pilots 1, 3 and 5](reports/report1_stat-reviewer_findings_pilots_1_3_5_2026-10-27.md) and the [comparison of the statistical-reviewer and yamaa](reports/report2_stat-reviewer_vs_yamaa_comparison_2026-10-27.md).

## Reports

| Report | Contents |
|---|---|
| **yamaa** | [Pilot 7 dashboard](https://rconsortium.github.io/submissions-pilot7-synthetic-data/): [CDISC Pilot 01 (Pilot 1)](https://rconsortium.github.io/submissions-pilot7-synthetic-data/studies/cdiscpilot01/), [Pilot 3](https://rconsortium.github.io/submissions-pilot7-synthetic-data/studies/submission-pilot3/), [Pilot 5](https://rconsortium.github.io/submissions-pilot7-synthetic-data/studies/submission-pilot5/) |
| **statistical-reviewer** | [Consolidated findings, Pilots 1 / 3 / 5](reports/report1_stat-reviewer_findings_pilots_1_3_5_2026-10-27.md). Per-pilot detail: [Pilot 1](reports/statistical_review_pilot1_2026-10-27.md), [Pilot 3](reports/statistical_review_pilot3_2026-10-27.md), [Pilot 5](reports/statistical_review_pilot5_2026-10-27.md) |
| **Elsa, Pilot 1** | [CDISCPILOT01 statistical filing review](reports/FDA_filing_agent_reviews/CDISCPILOT01_Statistical_Filing_Review_v2_python.md) |
| **Comparison: statistical-reviewer vs yamaa** | [Statistical-reviewer vs yamaa comparison](reports/report2_stat-reviewer_vs_yamaa_comparison_2026-10-27.md): overlap, why each tool misses what the other catches, how to use them together, and **how to make a submission AI-reviewer friendly** (§6) |
| **Comparison: yamaa vs statistical-reviewer vs Elsa, Pilot 1** | [Pilot 1 three-way comparison](reports/report3_yamaa_vs_stat-reviewer_vs_elsa_pilot1_2026-11-01.md): finding-level crosswalk, cross-checked numbers, and what each tool contributes. |

## Practical suggestions for sponsors

- **Pre-check with both kinds of tool.** Use a process-level tool such as yamaa for operational fixes, and a data-level tool such as the statistical-reviewer for signals the CSR must explain.
- **Make derivations executable.** Write define.xml methods with real variable names and codelist values, so they reproduce the data when run literally. Better still, ship a machine-executable specification.
- **Keep documents consistent.** Use one source for each rule across the SAP, define.xml, ADRG and specs, and keep variable labels consistent across datasets. Every claim in the ADRG and CSR should be checkable against the data.
- **Submit what the SAP promises.** Provide an output for every pre-specified endpoint, sensitivity analysis and subgroup analysis, or state why it is absent.
- **Label outputs accurately.** Titles, footnotes and axis labels should describe the analysis actually performed.
- **Ship a complete, machine-readable package.** Include every referenced document. Provide results in structured form (for example ARD or CSV) alongside the PDFs, and use valid Dataset-JSON with no local paths.
- **Make programs rerunnable.** Every program should rebuild the submitted files from a clean, locked environment, with package sources that will still exist at review time.
- **Anticipate the questions.** Populate traceability fields such as AEACN and SRCDOM/SRCVAR. State the estimand and the sensitivity analyses. Explain every population exclusion, such as the 20 subjects outside the efficacy population. Document known data artefacts in the ADRG.
- **Check regulatory completeness too.** Elsa checked the package against the refuse-to-file criteria in MAPP 6025.4: required modules, subgroup analyses and forms. Neither open-source tool does this. Run a completeness checklist, and state in the cover letter anything intentionally omitted and why.

Details, with the evidence from each pilot and a 12-item pre-submission checklist, are in [§6 of the statistical-reviewer vs yamaa comparison](reports/report2_stat-reviewer_vs_yamaa_comparison_2026-10-27.md#6-making-a-submission-ai-reviewer-friendly). Further Pilot 1 lessons are in [§6 of the Pilot 1 three-way comparison](reports/report3_yamaa_vs_stat-reviewer_vs_elsa_pilot1_2026-11-01.md#6-lessons-for-ai-reviewer-friendly-submissions).

## Caveats

- **yamaa results:** the items are automated observations, not confirmed defects; about 30% are marked *disputed* in yamaa's own review step. Counts reflect dashboard revision `24a55b1`, viewed 2026-10-27.
- **Statistical-reviewer results:** each package was reviewed once by an AI agent using the skill. The key cross-pilot findings were spot-checked against source data; see the consolidated report, §5, for corrections.
- **Elsa results:** the Pilot 1 Elsa report is a draft that its own header identifies as "Elsa (FDA AI Assistant — draft for human reviewer) AKA Claude Sonnet 4.5", and it requires human verification. Elsa cannot load an eCTD submission, so the human reviewer gave it the package's README.md for the folder structure; its item G5 ("README.md included in submission package") is an artefact of that setup. It also reports zero missing primary-endpoint values without noting that 79 of the 234 are LOCF-imputed.
- **Test data:** all packages use public CDISC pilot test data. Realism signals, such as weekend visit dates, are expected artefacts of de-identification.
- **Elsa report version:** the Elsa report used here is the revised version (v2). An earlier version is also available in the `reports/FDA_filing_agent_reviews/` folder.
