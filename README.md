# Pilot 7: AI review of past R Consortium submissions

**Background:** The R Consortium R Submissions Working Group has completed five open submission pilots with the FDA. The FDA has now started to use AI reviewers. We would like to collaborate with the FDA to explore how to streamline submissions in the AI era.

As part of R Consortium Submissions Pilot 7, the original FDA submission pilots (**Pilot 1, Pilot 3 and Pilot 5**) are run through two **open-source AI review tools**, [yamaa](https://github.com/elong0527/yamaa) and the [statistical-reviewer skill](https://github.com/RConsortium/pharma-skills/tree/main/statistical-reviewer), and through **Elsa**, the FDA AI Assistant.

**Aim:** give sponsors practical suggestions that streamline submissions and the FDA reviewer experience, so that promising treatments reach patients faster.

## Submission pilots 1, 3 and 5

The three pilots reviewed here submit the same study, CDISCPILOT01: xanomeline vs placebo in mild-to-moderate Alzheimer's disease, using the public CDISC pilot test data. Each pilot tested a different part of an R-based submission:

- **Pilot 1, R for tables and figures:** tables, listings and figures (TLFs) are generated in R from ADaM datasets built in SAS. The submission WG's helper R package is submitted as plain text (pkglite).
- **Pilot 3, R for ADaM:** extends Pilot 1 to the analysis datasets. The ADaM datasets are built in R from SDTM, and the TLFs are generated in R. SDTM and ADaM are submitted as SAS transport (XPT) files.
- **Pilot 5, Dataset-JSON:** submits SDTM and ADaM as CDISC Dataset-JSON instead of XPT, together with the R programs that build and analyse them.

| Pilot | Submitted | Repository |
|---|---|---|
| Pilot 1 | ADaM (XPT, built in SAS) + R-generated TLFs | [submissions-pilot1-to-fda](https://github.com/RConsortium/submissions-pilot1-to-fda) |
| Pilot 3 | SDTM + ADaM (XPT, ADaM built in R) + R-generated TLFs | [submissions-pilot3-adam-to-fda](https://github.com/RConsortium/submissions-pilot3-adam-to-fda) |
| Pilot 5 | SDTM + ADaM (Dataset-JSON, ADaM built in R) + R-generated TLFs | [submissions-pilot5-datasetjson-to-fda](https://github.com/RConsortium/submissions-pilot5-datasetjson-to-fda) |

## Project design

| Step | Question | Approach | Status |
|---|---|---|---|
| **Step 1:** Open-source pre-check vs FDA AI review | Would open-source tools used as pre-submission checks cover the issues an FDA AI-assisted review raises? | Run the original Pilot 1 / 3 / 5 packages through yamaa and the statistical-reviewer skill. Run the same packages through Elsa. Compare the findings item by item. | Open-source and Elsa reviews done for Pilots 1, 3 and 5, and compared item by item. |
| **Step 2:** Pre-audited resubmission | Does a pre-audited submission package reduce unnecessary reviewer issues and back-and-forth? | Update each package using the open-source findings. Resubmit the enhanced package and rerun Elsa. Compare the issues raised before and after. | Planned |
| **Step 3:** AI-ready submission format | In the AI era, is there an alternative file format or file structure that can make FDA AI review more efficient and human oversight more streamlined? | Start with an ADRG.json file: a machine-readable reviewer's guide that specifies the lineage of every number in the primary and key secondary endpoint tables, from the displayed value back to the datasets, filters and programs that produce it. | Proposed |

## Review tools

| | **yamaa** (open source) | **statistical-reviewer** (open source) | **Elsa** (FDA AI Assistant) |
|---|---|---|---|
| Role | Sponsor pre-check: data standards and programming | Sponsor pre-check: independent statistician | FDA statistical filing review |
| What it asks | *Does the documented process reproduce the datasets?* | *Do the submitted data and results hold up?* | *Is the application fileable, and what must the applicant answer?* |
| How | Rebuilds every ADaM dataset from SDTM with executable specifications, and matches the submitted datasets cell by cell. Then checks define.xml, ADRG, SAP and spec text clause by clause against the implementation. | Works from the data as submitted. Reproduces the reported numbers (TLF → ADaM → SDTM), challenges populations, denominators and missing-data handling, and assesses clinical plausibility. | Follows the FDA filing review process: the NDA/BLA statistics filing template and the refuse-to-file criteria in MAPP 6025.4. Queries the submitted datasets and re-runs the primary analysis. Produces refuse-to-file issues and information requests. |
| Best at | Process-level discrepancies, which call for **operational fixes** to specs, define.xml, the ADRG and programs | Data and analysis signals that **need interpretation in the CSR** | The **regulator's view**: fileability, regulatory completeness, and what the agency will ask |
| Source | [yamaa](https://github.com/elong0527/yamaa); results on the [Pilot 7 dashboard](https://rconsortium.github.io/submissions-pilot7-synthetic-data/) | [statistical-reviewer skill](https://github.com/RConsortium/pharma-skills/tree/main/statistical-reviewer) in [pharma-skills](https://github.com/RConsortium/pharma-skills); results in the [consolidated report](reports/report1_stat-reviewer_findings_pilots_1_3_5_2026-10-27.md) and per-pilot reports ([Pilot 1](reports/statistical_review_pilot1_2026-10-27.md), [Pilot 3](reports/statistical_review_pilot3_2026-10-27.md), [Pilot 5](reports/statistical_review_pilot5_2026-10-27.md)) | Filing reviews: [Pilot 1](reports/FDA_filing_agent_reviews/CDISCPILOT01_Statistical_Filing_Review_v2_python.md), [Pilot 3](reports/FDA_filing_agent_reviews/CDISCPILOT03_Biostatistics_Filing_Review.md), [Pilot 5](reports/FDA_filing_agent_reviews/CDISCPILOT05_Biostatistics_Filing_Review.md) |

## Step 1 results

### Summary across Pilots 1, 3 and 5

In all three pilots, Elsa found no refuse-to-file issues within the pilot's scope, left the fileability decision to the human reviewer, and reproduced the primary ADAS-Cog result in Python. Its review items focus on regulatory completeness and the review environment rather than on the data.

**Answer to Step 1:** used together, the open-source tools anticipated the statistical items Elsa raised in all three pilots, and found data issues it did not raise. In these pilot runs, Elsa was given only the MAPP 6025.4 Rev. 1 (refuse-to-file) rules, and its reviews did not cover the same safety-data defects in any pilot: serious AEs not flagged as serious (AESER), and AE discontinuations that can't be traced to an event (AEACN). In Pilots 3 and 5 they also did not cover the 12 subjects randomized to High Dose who received only 54 mg. In practice, an FDA reviewer may use more tailored rules and prompts. What the Elsa setup in this pilot checks is regulatory completeness: required modules and documents, package formats, and whether the computing environment can be restored.

**AI pre-audits enable earlier correction.** Running AI "pre-audits" before submission can capture the issues an FDA AI review is likely to raise. In these pilots, the open-source tools flagged Elsa's statistical items in advance, such as the missing-data handling, the unanalysed CIBIC+ endpoint, the missing define.xml and the multiplicity strategy. Sponsors who run such pre-audits can correct these issues before submission rather than in response to information requests, which makes for a smoother review experience. Step 2 will test this by resubmitting the pre-audited packages to Elsa.

**yamaa vs statistical-reviewer.** The two open-source tools complement each other. yamaa cannot see an error that the source data and the derived datasets share, such as serious AEs flagged "N" at source. The statistical-reviewer does not audit documentation text, such as a define.xml formula that is wrong but does not change the numbers. For two of yamaa's rule conflicts, the ADAS-Cog values and the treatment-emergent flag, the statistical-reviewer re-derived the variables from source and found no mismatches: the defect is in the documented rule, not in the data. Details: the [consolidated statistical-reviewer findings for Pilots 1, 3 and 5](reports/report1_stat-reviewer_findings_pilots_1_3_5_2026-10-27.md) and the [comparison of the statistical-reviewer and yamaa](reports/report2_stat-reviewer_vs_yamaa_comparison_2026-10-27.md).

### A) Pilot 1: yamaa vs statistical-reviewer vs Elsa

| | Pilot 1 |
|---|---|
| Elsa: refuse-to-file issues within the pilot's scope | None |
| Elsa: review items | 6 |
| Elsa: primary efficacy result reproduced (Python) | Yes |
| yamaa: ADaM cells reproduced from SDTM | 100% (9.1 M) |
| yamaa: documentation consistency items (conflict / divergence / gap) | 388 (63 / 191 / 120)\* |
| statistical-reviewer: findings (High / Medium / Low) | 3 / 8 / 5 |
| statistical-reviewer: primary efficacy result reproduced | Yes |

\* The remaining 14 items are marked "not reviewed" or "unclear".

The package includes ADaM only: no SDTM, SAP, protocol or CSR. yamaa used SDTM from outside the package.

**Elsa's review items:**

1. The 97.5% normal quantile behind the CIs in Table 14-3.01 differs from FDA's earlier re-calculation (which used 1.96), and the sponsor kept its own approach.
2. The model specification was verified from the package source, so no information request is needed.
3. The ANL01FL label differs across datasets.
4. Confirm the ADTTE censoring convention.
5. 20 subjects (7.9%) are excluded from the efficacy population without explanation.
6. A Python re-run of the primary analysis, for comparison with Table 14-3.01.

Elsa also listed 29 further issues that would matter in a real marketing application; most are components absent by design in this pilot.

**Raised by Elsa and anticipated by the open-source tools:**

- **Primary result** (items 2 and 6). Elsa re-ran the ADAS-Cog analysis in Python and the statistical-reviewer in R. Both get −1.006 (High − Placebo) and −0.467 (Low − Placebo), with dose-response p = 0.245, and both confirmed the model specification in the submitted program.
- **Excluded subjects** (item 5). The statistical-reviewer had already characterized them: 19 have no post-baseline ADAS-Cog and 1 has no post-baseline CIBIC+. yamaa found that the define.xml source of the efficacy flag (`ADSL.FASFL`) does not exist.
- **Time-to-event censoring** (item 4). The statistical-reviewer reproduced the KM curves and numbers at risk exactly, and flagged the censoring descriptions. yamaa found that the documented time-to-event date rule gives a different date for 5 subjects.
- **CI method** (item 1, partly). The statistical-reviewer flagged mixed z- and t-based CIs.
- **Missing-data handling,** from Elsa's appendix: the ADRG says "Imputation: Not applicable" although the primary analysis uses LOCF, and there is no sensitivity analysis. The statistical-reviewer flagged both, and ran observed-case, all-randomized and on-treatment analyses; the null result holds. yamaa flagged divergences in the documented LOCF and proration rules.
- **Subgroups,** from Elsa's appendix (partly): no demographic subgroup analyses. The statistical-reviewer flagged that sex and ethnicity are missing from Table 14-2.01.

**Raised by Elsa only:** the ANL01FL label (item 3); regulatory completeness, absent by design in this pilot (ISS, ISE, CSR, protocol, SAP and Module 2 summaries; SDTM; case report forms; randomization documentation; financial disclosure, user fee and pediatric (PREA) documentation; Form 356h possibly unsigned); and technical items (retired MRAN package repository; old MedDRA version, v8.0; no software validation evidence, out of scope by design).

**Found by the open-source tools but not raised by Elsa:**

| Tool | Findings |
|---|---|
| statistical-reviewer | Co-primary CIBIC+ has no output; AESER = "N" on all 3 fatal AEs, and 25 subjects meet seriousness criteria while only 3 are flagged; AEACN blank on all AEs, so the 92 AE discontinuations are untraceable; differential LOCF (17.7 / 39.5 / 44.6%; 79 of the 234 Week 24 values are imputed); 37 subjects with post-discontinuation ADAS-Cog values in the primary analysis; KM y-axis mislabelled, with no HR or medians; glucose table mislabelled; placeholder derivation methods in define.xml |
| yamaa | Documentation defects: BMI formula; lab-ratio limits; completer flag definition; Hy's Law threshold; VISNUMEN filter term |
| Both | Treatment-emergent definition: no upper window and TRTEMFL blank instead of "N" (statistical-reviewer); define.xml and the SAP give different definitions (yamaa) |

Details: [Elsa's Pilot 1 filing review](reports/FDA_filing_agent_reviews/CDISCPILOT01_Statistical_Filing_Review_v2_python.md), the [statistical-reviewer's Pilot 1 report](reports/statistical_review_pilot1_2026-10-27.md) and the [yamaa Pilot 1 dashboard](https://rconsortium.github.io/submissions-pilot7-synthetic-data/studies/cdiscpilot01/).

### B) Pilot 3: yamaa vs statistical-reviewer vs Elsa

| | Pilot 3 |
|---|---|
| Elsa: refuse-to-file issues within the pilot's scope | None |
| Elsa: review items | 5 |
| Elsa: primary efficacy result reproduced (Python) | Yes |
| yamaa: ADaM cells reproduced from SDTM | 100% (2.3 M) |
| yamaa: documentation consistency items (conflict / divergence / gap) | 248 (23 / 66 / 150)\* |
| statistical-reviewer: findings (High / Medium / Low) | 2 / 8 / 7 |
| statistical-reviewer: primary efficacy result reproduced | Yes |

\* The remaining 9 items are marked "not reviewed" or "unclear".

The package includes SDTM, and the SAP inside the CSR.

**Elsa's review items:**

1. CIBIC+, a co-primary endpoint, has no ADaM dataset.
2. The source of the `pilot3utils` package can't be read from the submitted Windows binary zip. Elsa does not run R yet, so this did not affect its review: it re-ran the primary analysis in Python.
3. Confirm the R 4.2.3 / renv environment.
4. ADADAS LOCF flags differ from the original CDISC data for 19 subjects.
5. Zeros are stored as SAS floating-point values (~5.4e-79) in TRTPN and CNSR. *(possible AI error, pending human review)* The XPT file stores exact zeros; ~5.4e-79 is how Python's pandas reader converts an exact zero.

**Raised by Elsa and anticipated by the open-source tools:**

- **CIBIC+ not analysed** (item 1). The statistical-reviewer also reproduced the null CIBIC+ result (p = 0.960).
- **ADADAS LOCF flags** (item 4). yamaa flagged gaps in the documented LOCF and windowing rules.
- **Missing-data handling,** which Elsa flagged for the human reviewer. The statistical-reviewer quantified the LOCF (17.7 / 39.5 / 44.6% of Week 24 values) and ran sensitivity analyses, including the MMRM in the SAP; the null result holds.

**Raised by Elsa only:** the helper package and R environment (items 2 and 3); SAS floating-point zeros (item 5, possible AI error); and regulatory completeness (no ISS, ISE or complete CSR).

**Found by the open-source tools but not raised by Elsa:**

| Tool | Findings |
|---|---|
| statistical-reviewer | AESER under-flagged; AEACN blank, and 5 AE discontinuations coded under other reasons; actual treatment set equal to planned treatment, although 12 subjects randomized to High Dose received only 54 mg (found when cross-checking the reviews; see the consolidated report, §5); 230 duplicated AE record pairs; mislabelled glucose table and KM axis; treatment end date imputed past the last dose for 6 subjects; 2 subjects who violate the MMSE inclusion criterion |
| yamaa | Documented rules that don't reproduce the data: the disposition flag (110 subjects), the end-of-study visit number (all subjects), the ADAS-Cog change from baseline (3,800 records), the treatment-emergent flag (65 records) and the time-to-event date (5 subjects); a define.xml source that does not exist (`ADTTE.TRTDUR`) |
| Both | ANRIND holds a 1.5 × ULN flag, so 1,315 out-of-range values are coded "Normal"; the define.xml rule for the dermatologic-event flag (AOCC01FL) is the opposite of the implemented rule |

Details: [Elsa's Pilot 3 filing review](reports/FDA_filing_agent_reviews/CDISCPILOT03_Biostatistics_Filing_Review.md), the [statistical-reviewer's Pilot 3 report](reports/statistical_review_pilot3_2026-10-27.md) and the [yamaa Pilot 3 dashboard](https://rconsortium.github.io/submissions-pilot7-synthetic-data/studies/submission-pilot3/).

### C) Pilot 5: yamaa vs statistical-reviewer vs Elsa

| | Pilot 5 |
|---|---|
| Elsa: refuse-to-file issues within the pilot's scope | None |
| Elsa: review items | 5 |
| Elsa: primary efficacy result reproduced (Python) | Yes |
| yamaa: ADaM cells reproduced from SDTM | 100% (2.3 M) |
| yamaa: documentation consistency items (conflict / divergence / gap) | 233 (18 / 51 / 156)\* |
| statistical-reviewer: findings (High / Medium / Low) | 3 / 11 / 8 |
| statistical-reviewer: primary efficacy result reproduced | Yes |

\* The remaining 8 items are marked "not reviewed" or "unclear".

The package includes SDTM, but no SAP, protocol or define.xml.

**Elsa's review items:**

1. No define.xml.
2. Dataset-JSON v1.1 can't yet be validated by Pinnacle 21.
3. ADADAS LOCF flags differ from the original CDISC data for 19 subjects.
4. 18 ADLBC parameters are in the specification but not in the data.
5. Pairwise comparisons are not adjusted for multiplicity.

**Raised by Elsa and anticipated by the open-source tools:**

- **No define.xml** (item 1). The statistical-reviewer flagged the missing define.xml, SAP and protocol.
- **Dataset-JSON** (item 2). Elsa noted the validation-tool gap; the statistical-reviewer found concrete encoding problems: "NA" strings, wrong types and lengths, and a local file path.
- **ADADAS LOCF flags** (item 3). yamaa flagged gaps in the documented LOCF and windowing rules, and the statistical-reviewer re-derived ADADAS from QS (222 LOCF records, matching).
- **Multiplicity** (item 5). The statistical-reviewer flagged that multiplicity across endpoints and dose comparisons is undefined.
- **Missing-data handling,** which Elsa called a material concern, citing 99 of 234 Week 24 values (42%) as LOCF-imputed *(possible AI error, pending human review)*. The primary analysis set has 79 (34%). The statistical-reviewer quantified the LOCF (17.7 / 39.5 / 44.6% of Week 24 values) and found off-treatment values counted as observed, with no estimand.
- **Treatment end date.** Elsa flagged 6 missing EX end dates; the statistical-reviewer found the treatment end date imputed past the last dose for 4 subjects.

**Raised by Elsa only:** 18 ADLBC parameters missing from the data (item 4); enrollment of 254 against 300 planned; and regulatory completeness (no ISS, ISE, CSR, SAP, protocol or subgroup analyses).

**Found by the open-source tools but not raised by Elsa:**

| Tool | Findings |
|---|---|
| statistical-reviewer | Actual treatment set equal to planned treatment, although 12 subjects randomized to High Dose received only 54 mg; `adadas.r` cannot regenerate the submitted `adadas.json`; AESER under-flagged; AEACN blank; 230 duplicated AE record pairs; co-primary CIBIC+ not analysed; mislabelled glucose table and KM axis; TLF programs depend on session state, and the rendered TLFs exist only inside a compiled PDF |
| yamaa | Documented rules that don't reproduce the data: the disposition flag (110 subjects), the end-of-study visit number (all subjects), the ADAS-Cog change from baseline (3,800 records), the treatment-emergent flag (65 records) and the time-to-event date (5 subjects) |
| Both | ANRIND holds a 1.5 × ULN flag, so out-of-range values are coded "Normal" |

Details: [Elsa's Pilot 5 filing review](reports/FDA_filing_agent_reviews/CDISCPILOT05_Biostatistics_Filing_Review.md), the [statistical-reviewer's Pilot 5 report](reports/statistical_review_pilot5_2026-10-27.md) and the [yamaa Pilot 5 dashboard](https://rconsortium.github.io/submissions-pilot7-synthetic-data/studies/submission-pilot5/).

## Reports

| Report | Contents |
|---|---|
| **yamaa** | [Pilot 7 dashboard](https://rconsortium.github.io/submissions-pilot7-synthetic-data/): [CDISC Pilot 01 (Pilot 1)](https://rconsortium.github.io/submissions-pilot7-synthetic-data/studies/cdiscpilot01/), [Pilot 3](https://rconsortium.github.io/submissions-pilot7-synthetic-data/studies/submission-pilot3/), [Pilot 5](https://rconsortium.github.io/submissions-pilot7-synthetic-data/studies/submission-pilot5/) |
| **statistical-reviewer** | [Consolidated findings, Pilots 1 / 3 / 5](reports/report1_stat-reviewer_findings_pilots_1_3_5_2026-10-27.md). Per-pilot detail: [Pilot 1](reports/statistical_review_pilot1_2026-10-27.md), [Pilot 3](reports/statistical_review_pilot3_2026-10-27.md), [Pilot 5](reports/statistical_review_pilot5_2026-10-27.md) |
| **Elsa** | Filing reviews: [Pilot 1](reports/FDA_filing_agent_reviews/CDISCPILOT01_Statistical_Filing_Review_v2_python.md), [Pilot 3](reports/FDA_filing_agent_reviews/CDISCPILOT03_Biostatistics_Filing_Review.md), [Pilot 5](reports/FDA_filing_agent_reviews/CDISCPILOT05_Biostatistics_Filing_Review.md) |
| **Comparison: statistical-reviewer vs yamaa** | [Statistical-reviewer vs yamaa comparison](reports/report2_stat-reviewer_vs_yamaa_comparison_2026-10-27.md): overlap, why each tool misses what the other catches, how to use them together, and **how to make a submission AI-reviewer friendly** (§6) |
| **Comparison: yamaa vs statistical-reviewer vs Elsa, Pilot 1** | [Pilot 1 three-way comparison](reports/report3_yamaa_vs_stat-reviewer_vs_elsa_pilot1_2026-11-01.md): finding-level crosswalk, cross-checked numbers, and what each tool contributes. |

## Practical suggestions for sponsors

- **Pre-audit with AI tools.** Use a process-level tool (yamaa), a data-level tool (statistical-reviewer) and a completeness check against the refuse-to-file criteria (MAPP 6025.4).
- **Make derivations executable.** define.xml methods should reproduce the data when run literally; better still, ship an executable specification.
- **Keep documents consistent with each other and with the data.** Use one source for each rule across the SAP, define.xml, ADRG and specs.
- **Submit what the SAP promises, labelled accurately.** Provide an output for every pre-specified analysis, or state why it is absent, with titles and labels that match the analysis.
- **Ship a complete, rerunnable package.** Include every referenced document and structured results alongside the PDFs, and make programs rebuild the files in a locked environment.
- **Anticipate the questions.** Populate traceability fields such as AEACN, state the estimand and sensitivity analyses, and explain population exclusions and known data artefacts.

Details and a 12-item pre-submission checklist are in [§6 of the statistical-reviewer vs yamaa comparison](reports/report2_stat-reviewer_vs_yamaa_comparison_2026-10-27.md#6-making-a-submission-ai-reviewer-friendly); more Pilot 1 lessons are in [§6 of the Pilot 1 three-way comparison](reports/report3_yamaa_vs_stat-reviewer_vs_elsa_pilot1_2026-11-01.md#6-lessons-for-ai-reviewer-friendly-submissions).

## Caveats

- **yamaa results:** the items are automated observations, not confirmed defects; about 30% are marked *disputed* in yamaa's own review step. Counts reflect dashboard revision `24a55b1`, viewed 2026-10-27.
- **Statistical-reviewer results:** each package was reviewed once by an AI agent using the skill. The key cross-pilot findings were spot-checked against source data; see the consolidated report, §5, for corrections.
- **Elsa results:** the Elsa reports are drafts that require human verification. The Pilot 1 report identifies itself as "Elsa (FDA AI Assistant — draft for human reviewer) AKA Claude Sonnet 4.5"; the Pilot 3 and 5 reports don't name a model. Elsa cannot load an eCTD submission, so the human reviewer supplied the folder structure: the package's README.md for Pilot 1, and a file tree in the prompt for Pilots 3 and 5. Pilot 1 item G5 ("README.md included in submission package") is an artefact of that setup. Some Elsa statements do not match the data:
  - Pilot 1 reports zero missing primary-endpoint values without noting that 79 of the 234 are LOCF-imputed. *(possible AI error, pending human review)*
  - Pilot 5 says 99 of 234 Week 24 values (42%) are LOCF-imputed. The primary analysis set has 79 (14 / 32 / 33); 99 is the count over all Week 24 records. *(possible AI error, pending human review)*
  - Pilot 5 gives KM medians of 139 / 29.5 / 24.5 days. The data give not reached / 33 / 36 days; placebo event-free probability is still 0.63 at Day 180. *(possible AI error, pending human review)*
  - Pilot 3 says zeros in TRTPN and CNSR are stored as ~5.4e-79. The XPT file stores exact zeros; the value comes from Python's pandas reader. *(possible AI error, pending human review)*
- **Test data:** all packages use public CDISC pilot test data. Realism signals, such as weekend visit dates, are expected artefacts of de-identification.
- **Elsa report version:** the Pilot 1 Elsa report used here is the revised version (v2). An earlier version is also available in the `reports/FDA_filing_agent_reviews/` folder.
