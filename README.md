# Pilot 7: AI review of past R Consortium submissions

Part of the remit of R Consortium Submissions Pilot 7 is to run the earlier FDA submission pilots (**Pilot 1, Pilot 3 and Pilot 5**) through AI review tools and learn from what those tools find.

## Purpose

1. **Make submissions "AI-reviewer friendly".** FDA has begun using AI to support regulatory review; in June 2025 it announced an agency-wide generative-AI tool for reviewers. An AI reviewer reads every file, cross-checks every statement and re-runs whatever it can. This work identifies what in a submission package helps or hinders that kind of review.
2. **Recommend pre-submission checks to industry.** Many issues an AI reviewer raises are cheap to detect before submission. Catching them early avoids information requests and back-and-forth with the agency.

## What was reviewed

The three packages contain the same study in different submission formats. CDISCPILOT01 is xanomeline vs placebo in mild-to-moderate Alzheimer's disease, and the data are the public CDISC pilot test data.

| Package | Format | Repository |
|---|---|---|
| Pilot 1 | SAS-built ADaM (XPT) + R-generated TLFs | [submissions-pilot1-to-fda](https://github.com/RConsortium/submissions-pilot1-to-fda) |
| Pilot 3 | SDTM + R-built ADaM (XPT) + R-generated TLFs | [submissions-pilot3-adam-to-fda](https://github.com/RConsortium/submissions-pilot3-adam-to-fda) |
| Pilot 5 | SDTM + ADaM as CDISC Dataset-JSON | [submissions-pilot5-datasetjson-to-fda](https://github.com/RConsortium/submissions-pilot5-datasetjson-to-fda) |

## The two AI review tools

| | **yamma** | **statistical-reviewer** |
|---|---|---|
| What it asks | *Does the documented process reproduce the datasets?* | *Do the submitted data and results hold up?* |
| How | Rebuilds every ADaM dataset from SDTM with executable specifications. Matches the submitted datasets cell by cell (100% in all three pilots). Then checks define.xml, ADRG, SAP and spec text clause by clause against the implementation. | Works from the data as submitted. Reproduces the reported numbers (TLF → ADaM → SDTM), challenges populations, denominators and missing-data handling, and assesses clinical plausibility. |
| What it is good at | Detailed, process-level discrepancies, which call for **operational fixes** (specs, define.xml, ADRG, programs) | Data and analysis signals that **need interpretation in the CSR** |
| Source | Pilot 7 dashboard (engine: yamaa) | `statistical-reviewer` skill from [pharma-skills](https://github.com/RConsortium/pharma-skills) |

The two tools complement each other. yamma cannot see an error the source data and the derived datasets share, such as serious AEs flagged "N" at source. The statistical-reviewer does not audit documentation text, such as a define.xml formula that is wrong but does not change the numbers.

## Reports

| Report | Contents |
|---|---|
| **yamma report** | [Pilot 7 dashboard](https://rconsortium.github.io/submissions-pilot7-synthetic-data/): [CDISC Pilot 01 (Pilot 1)](https://rconsortium.github.io/submissions-pilot7-synthetic-data/studies/cdiscpilot01/), [Pilot 3](https://rconsortium.github.io/submissions-pilot7-synthetic-data/studies/submission-pilot3/), [Pilot 5](https://rconsortium.github.io/submissions-pilot7-synthetic-data/studies/submission-pilot5/) |
| **Statistical-reviewer report** | [Consolidated findings, Pilots 1 / 3 / 5](reports/report1_stat-reviewer_findings_pilots_1_3_5_2026-10-27.md). Per-pilot detail: [Pilot 1](reports/statistical_review_pilot1_2026-10-27.md), [Pilot 3](reports/statistical_review_pilot3_2026-10-27.md), [Pilot 5](reports/statistical_review_pilot5_2026-10-27.md) |
| **Comparison report** | [statistical-reviewer vs yamma](reports/report2_stat-reviewer_vs_yamma_comparison_2026-10-27.md): overlap, why each tool misses what the other catches, how to use them together, and **how to make a submission AI-reviewer friendly** (§6) |

## Key results

| | Pilot 1 | Pilot 3 | Pilot 5 |
|---|---|---|---|
| yamma: ADaM cells reproduced from SDTM | 100% (9.1 M) | 100% (2.3 M) | 100% (2.3 M) |
| yamma: documentation consistency items (conflict / divergence / gap) | 388 (63 / 191 / 120)\* | 248 (23 / 66 / 150) | 233 (18 / 51 / 156) |
| statistical-reviewer: findings (High / Medium / Low) | 3 / 8 / 5 | 2 / 8 / 7 | 3 / 11 / 8 |
| statistical-reviewer: primary efficacy result reproduced | Yes | Yes | Yes |

\* The remaining items (14 / 9 / 8) are marked "not reviewed" or "unclear".

**Findings common to all three pilots:**

- **Serious AEs under-flagged:** 3 subjects flagged vs 25 meeting the seriousness criteria, including all 3 deaths.
- **AE discontinuations untraceable:** AE action taken (AEACN) is blank, so discontinuations can't be linked to an event.
- **Heavy imputation:** Week 24 LOCF is differential by arm (17.7 / 39.5 / 44.6%).
- **Co-primary endpoint missing:** CIBIC+ is never analysed.
- **Mislabelled outputs:** the KM figure's y-axis and the glucose table's title.
- **Documentation conflicts:** many conflicts between define.xml and the implementation, for example the lab normal-range indicator, the treatment-emergent flag and disposition flags.

## Making a submission AI-reviewer friendly

- **Make derivations executable.** Write define.xml methods with real variable names and codelist values, so they reproduce the data when run literally. Better still, ship a machine-executable specification.
- **Keep documents consistent.** Use one source for each rule across the SAP, define.xml, ADRG and specs. Every claim in the ADRG and CSR should be checkable against the data.
- **Label outputs accurately.** Titles, footnotes and axis labels should describe the analysis actually performed.
- **Ship a complete, machine-readable package.** Include every referenced document and an output for each pre-specified endpoint. Provide results in structured form (for example ARD or CSV) alongside the PDFs, and use valid Dataset-JSON with no local paths.
- **Make programs rerunnable.** Every program should rebuild the submitted files from a clean, locked environment.
- **Anticipate the questions.** Populate traceability fields such as AEACN and SRCDOM/SRCVAR. State the estimand and the sensitivity analyses. Document known data artefacts in the ADRG.

Details, with the evidence from each pilot and a 12-item pre-submission checklist, are in [comparison report §6](reports/report2_stat-reviewer_vs_yamma_comparison_2026-10-27.md#6-making-a-submission-ai-reviewer-friendly).

## Caveats

- **yamma results:** the items are automated observations, not confirmed defects; about 30% are marked *disputed* in yamma's own review step. Counts reflect dashboard revision `24a55b1`, viewed 2026-10-27.
- **Statistical-reviewer results:** each package was reviewed once by an AI agent using the skill. The key cross-pilot findings were spot-checked against source data; see the consolidated report, §5, for corrections.
- **Test data:** all packages use public CDISC pilot test data. Realism signals, such as weekend visit dates, are expected artefacts of de-identification.
