---
title: Statistical-reviewer vs yamma — complementary review of Submission Pilots 1, 3 and 5
date: 2026-10-27
sources:
  stat_reviewer: report1_stat-reviewer_findings_pilots_1_3_5_2026-10-27.md (+ the three per-pilot reports)
  yamma: https://rconsortium.github.io/submissions-pilot7-synthetic-data/ (Pilot 7 "Agentic data standardization"; dashboard revision 24a55b1, engine yamaa 0.6.2, generated 2026-10-27)
study_mapping:
  Pilot 1: yamma "CDISC Pilot 01" (same ten ADaM datasets)
  Pilot 3: yamma "Submission Pilot 3"
  Pilot 5: yamma "Submission Pilot 5"
---

# Statistical-reviewer vs yamma: two complementary reviews of the same submissions

## 1. Bottom line

The two reviews ask different questions about the same three packages, and each finds things the other cannot.

| | **yamma** (Pilot 7) | **statistical-reviewer** skill |
|---|---|---|
| Core question | *Does the documented process reproduce the datasets?* | *Do the submitted data and results hold up?* |
| Approach | Rebuilds every ADaM dataset from SDTM using executable specifications. Compares the result cell by cell with the submitted datasets. Then checks every documented rule (define.xml, ADRG, SAP, spec workbook) clause by clause against that implementation. | Works from the data as submitted. Reproduces the reported numbers (TLF → ADaM → SDTM), challenges populations, denominators and missing-data handling, and judges whether the data are clinically plausible. It does not re-execute the derivation process. |
| Typical finding | "Define-XML says X; the data were derived as Y; on Z records the documented rule gives a different value." | "36 AEs meet seriousness criteria but are flagged not serious; the SAE count of 3 is understated." |
| Best used for | **Operational fixes:** specifications, define.xml, ADRG and program corrections before submission. | **Interpretation signals:** what the CSR, safety narrative and benefit-risk discussion must explain. |
| Blind spot | If the source data and the submitted datasets are wrong in the same way, the process reproduces perfectly and nothing is flagged. | Does not audit documentation text clause by clause, so it misses many documentation-versus-implementation mismatches. |

**Use both.** yamma flags the operational fixes the programming and standards teams need to make. The statistical-reviewer flags the signals that need further interpretation in the CSR.

## 2. Scale of each review

| | Pilot 1 / CDISC Pilot 01 | Pilot 3 | Pilot 5 |
|---|---|---|---|
| **yamma:** ADaM datasets rebuilt | 10 | 5 | 5 |
| **yamma:** cells matched to reference | 9,119,605 / 9,119,605 (100%) | 2,291,147 / 2,291,147 (100%) | 2,291,147 / 2,291,147 (100%) |
| **yamma:** consistency issues | 388 | 248 | 233 |
| **yamma:** conflict / divergence / gap | 63 / 191 / 120 | 23 / 66 / 150 | 18 / 51 / 156 |
| **yamma:** own review (agreed / disputed / not reviewed) | 260 / 112 / 14 (+2 mixed) | 167 / 72 / 9 | 142 / 83 / 8 |
| **stat-reviewer:** findings (High / Medium / Low) | 3 / 8 / 5 | 2 / 8 / 7 | 3 / 11 / 8 |
| **stat-reviewer:** overall result | PASS WITH FINDINGS | FAIL | FAIL |
| **stat-reviewer:** primary result reproduced | Yes (p = 0.245) | Yes | Yes |

yamma issue kinds:

- **conflict:** sources disagree with each other, or the documented rule run as written does not reproduce the data.
- **divergence:** the specification differs from a documented clause.
- **gap:** a specification clause is not documented anywhere.

yamma describes its own items as "automated observations and pending review tasks… not confirmed clinical defects".

**Both reproduce the data.** yamma shows the full SDTM → ADaM process can be re-executed with a 100% match. The statistical-reviewer shows the ADaM → TLF results can be reproduced: every efficacy and demographic number matches. Neither found a reproducibility failure in the submitted numbers. The differences are in what each looks at beyond reproduction.

## 3. Topic-by-topic overlap

| Topic | yamma | statistical-reviewer | Overlap |
|---|---|---|---|
| **Lab normal-range indicator (ADLBC.ANRIND / BNRIND)** | **Conflict** (P3, P5). Define says low = 'Y', which is not in the L/N/H codelist. Define says 0.5 × "LBSTRNHI" (a misspelled variable), but the runtime uses 1.5 × ULN. "Missing → N" is undocumented. | ANRIND is really a 1.5 × ULN flag, so 1,315 out-of-range values are coded "Normal", and missing values are coded "Normal" too (P3 Medium, P5 Low). | **Both.** The same defect seen from two sides: the documentation is wrong, and the data mean something else. |
| **Treatment-emergent flag (ADAE.TRTEMFL)** | **Conflict** (P3, P5): the documented rule differs on 65 of 1,191 records (36 subjects); "N" or blank is undecided. P1: define.xml and the SAP give different definitions (worsening, recurrence). | P1 Low: no TEAE upper window; TRTEMFL is blank instead of "N"; 11 undated AEs are excluded. | **Partial.** yamma is more detailed. |
| **Dermatologic events (CQ01NAM / AOCC01FL)** | **Conflict:** the literal define rule `CQ01NAM=''` selects the wrong records. CQ01NAM differs on 181 of 1,191 records. | P3 Low: the CQ01 search includes pharyngeal erythema; the define AOCC01FL text is inverted. | **Partial.** |
| **Define.xml quality** | Clause-level, for example: <br>• EFFFL sourced from `ADSL.FASFL`, which does not exist (P1). <br>• `ADTTE.TRTDUR` source does not exist (P3). <br>• BMI formula multiplies height by 100 (P1). <br>• Lab ratio variables use the opposite normal-range limit from the SAP (all three). <br>• ADLBC.BASE origin names LBSTNRHI (P3, P5). | P1 Medium: placeholder methods for the primary variables; the ADRG says "Imputation: Not applicable". | **Both.** yamma is far more thorough. |
| **Time-to-event dates (ADTTE)** | **Conflict** (all three): the documented ADT rule gives a different date for 5 of 254 subjects (strict vs inclusive boundary). | One death censored 1 day after death; EVNTDESC mislabelled; no sensitivity analysis for AE-discontinuation censoring. | **Adjacent.** Same dataset, different defects. |
| **ADAS-Cog derivation (ADADAS)** | **Conflict** (all three): the documented CHG rule differs on 3,800 of 12,463 records, because the runtime adds a baseline-flag condition. 47–55 documentation gaps (P3, P5). | Values re-derived from QS with 0 mismatches. Flags the *amount* of LOCF (17.7 / 39.5 / 44.6%), off-treatment values, and post-discontinuation assessments. P5: `adadas.r` cannot run. | **Complementary.** yamma: the documentation is incomplete. Stat-reviewer: the data are correct, but the missing-data pattern needs interpreting. |
| **Disposition (ADSL.DISCONFL, VISNUMEN)** | **Conflict** (P3, P5): DISCONFL differs on 110 of 254 subjects; VISNUMEN on 254 of 254. P1: the filter term "PROTCOL COMPLETED" matches no record. | — | **yamma only** |
| **Serious AE flag (AESER)** | Documentation gaps only: sort order and partitioning of AOCC02–04FL. | **High (all three):** 36 records meet seriousness criteria but AESER = N, including all 3 deaths. SAE subjects: 3 flagged vs 25 by criteria. | **Stat-reviewer only** |
| **Action taken (AEACN)** | P5: define says it is a plain copy, but the spec derives it (marked disputed). | **High/Medium (all three):** blank on all 1,191 AEs, so 92 AE discontinuations are untraceable. | **Stat-reviewer only** |
| **Actual treatment (TRT01A)** | Naming only: ADVS.TRTA vs TRT01AN; ADTTE.TRTP origins; screen-failure population wording. | **High (P5; also confirmed in P3):** TRT01A = TRT01P, although 12 High Dose subjects received only 54 mg (DM.ACTARM = Low Dose). | **Stat-reviewer only** |
| **Statistical outputs** | Out of scope | Week 24 LOCF and estimand; CIBIC+ not analysed; no multiplicity strategy; KM y-axis mislabelled; glucose table titled "Primary"; no HRs or medians reported. | **Stat-reviewer only** |
| **Source data integrity and realism** | Out of scope. The reference datasets carry the source as is. | 230 duplicated AE pairs; Dataset-JSON "NA" strings and type problems (P5); weekend visits; MMSE inclusion violations. | **Stat-reviewer only** |

## 4. Why each misses what the other catches

**yamma cannot see an error that is faithfully reproduced.** It treats the submitted ADaM datasets as the reference and asks whether the documented process explains them. If SDTM says AESER = "N" for a fatal event, then the ADaM copies "N", the spec says "copy AESER", and everything is consistent. yamma reports 100% agreement, so the SAE under-reporting (C1) never surfaces. The same applies to TRT01A = TRT01P: the spec, the program and the data agree with one another. They just don't agree with what subjects actually received.

**The statistical-reviewer cannot see a documentation defect that doesn't change the data it uses.** It reproduces the reported numbers from the datasets, so a wrong define.xml formula does not affect its result. Examples are BMI × 100 and lab ratios dividing by the wrong limit. The 3,800-record CHG mismatch is a property of the documented rule, not of the data; the statistical-reviewer re-derived CHG from source with 0 mismatches. These are real defects for a reviewer reading define.xml, and only yamma finds them.

## 5. How to use them together

### 5.1 yamma → operational fixes (programming, standards, documentation)

These are concrete, fixable items for the study team, usually before submission:

| Fix | Example from these pilots |
|---|---|
| Correct define.xml derivation text | ANRIND/BNRIND method (low code, multiplier, variable spelling); BMI formula; lab ratio limits; AOCC01FL subset text |
| Fix broken or wrong source references | EFFFL → `ADSL.FASFL`; `ADTTE.TRTDUR`; ADLBC.BASE origin |
| Document undocumented derivation steps | 47–55 ADADAS documentation gaps (windowing, LOCF, DTYPE); missing-value policies |
| Resolve rule-versus-implementation conflicts | DISCONFL (110 subjects); VISNUMEN (all subjects); ADTTE.ADT boundary (5 subjects); TRTEMFL "N" vs blank (65 records) |
| Align ADRG, SAP and specs | Screen-failure population statements; treatment-emergent definition |

### 5.2 Statistical-reviewer → signals needing interpretation in the CSR

These are items the clinical and statistical team must explain, or the data must be corrected before the results are interpreted:

| Signal | What the CSR needs |
|---|---|
| SAEs under-flagged (3 vs 25 subjects) | Restate the SAE summary, deaths and benefit-risk; correct AESER at source |
| AE discontinuations untraceable (92 subjects; dose-related 8 / 44 / 40) | Explain which AEs drove dropout; populate AEACN |
| Differential LOCF and off-treatment Week 24 values | Define the estimand; present sensitivity analyses (the null result is robust: OC p = 0.56, MMRM n.s.) |
| 12 High Dose subjects never escalated to 81 mg | Analyse safety and time-to-event by actual treatment (High: 60/72 vs 61/84); correct the ADRG |
| Co-primary CIBIC+ not analysed; no multiplicity strategy | Report CIBIC+ (reproduced null, p = 0.96); state the multiplicity approach |
| Large dermatologic effect (HR ≈ 4–5) shown in a mislabelled figure | Fix the figure; report the median, HR and log-rank result |

### 5.3 Suggested combined workflow

1. **Run yamma first.** Confirm that the SDTM → ADaM process is reproducible and the documentation matches it. Fix the conflicts and gaps.
2. **Run the statistical-reviewer second,** on the corrected datasets and the draft TLFs. Confirm that the results reproduce, and collect the signals the CSR has to address.
3. **Cross-check the overlap items,** such as ANRIND, TRTEMFL and ADTTE dates. When both tools flag the same variable, it is almost always a real defect.

## 6. Making a submission "AI-reviewer friendly"

An AI reviewer reads every file, cross-references every statement and re-runs whatever it can, and it does so on every submission, not on a sample. Running both tools over Pilots 1, 3 and 5 shows what such a reviewer trips over. Most of it is not wrong data. It is ambiguity, contradiction and missing pieces that a human reviewer would resolve with a phone call or an information request. Each lesson below is tied to evidence from these three pilots.

### 6.1 Make derivations executable, not just descriptive

| Lesson | Evidence | Recommendation |
|---|---|---|
| Free-text derivations in define.xml often can't be run as written. | yamma: the ANRIND method names a non-existent variable (`LBSTRNHI`), assigns a code ('Y') that is not in the codelist, and uses 0.5 where the program uses 1.5. EFFFL points to a source variable (`ADSL.FASFL`) that doesn't exist. | Write derivation text using real variable names and codelist values, precise enough to run literally. Better still, submit a machine-executable specification (as yamma's YAML specs are) alongside define.xml. |
| An AI can only confirm a process it can re-execute. | yamma rebuilt all ADaM datasets from SDTM with a 100% cell match, but only from its own executable specs. The submitted define.xml alone would not reproduce them: 3,800 CHG records and 110 DISCONFL subjects differ. | Treat "the documented rule reproduces the dataset" as a pre-submission test. |
| Programs must run end to end in a clean session. | P5: `adadas.r` references an undefined object. The TLF programs depend on session state and set global options. | Run every submitted program from a fresh R session with the locked environment (renv) before packaging. |

### 6.2 Keep documents consistent with each other and with the data

| Lesson | Evidence | Recommendation |
|---|---|---|
| An AI reviewer checks every claim against the data. | The ADRG says all subjects received their randomized treatment, but 12 High Dose subjects received only 54 mg. The CSR says "3 SAEs", but 25 subjects meet seriousness criteria. | Make every factual statement in the ADRG/CSR traceable to a query on the submitted data, and run those queries before submission. |
| Contradictions between SAP, define.xml, ADRG and specs multiply. | yamma raised 388 / 248 / 233 consistency items, many of them one rule worded differently in two documents. Examples: the treatment-emergent definition (SAP vs define), and the screen-failure population (ADRG vs spec). | Keep a single source for each rule and generate the define.xml and ADRG text from it, rather than writing it twice. |
| Titles and labels are read literally. | A glucose table titled "Primary Endpoint … LOCF" that is neither; a KM y-axis "Probability of event" over survival curves. | Check that every output title, footnote and axis label matches the analysis actually performed. |

### 6.3 Ship a complete, machine-readable package

| Lesson | Evidence | Recommendation |
|---|---|---|
| Missing components force an AI reviewer to guess. | P5 has no define.xml, SAP or protocol. P1 has no SDTM, so the actual-treatment issue was invisible there. CIBIC+, a declared primary endpoint, has no output in any pilot. | Include every document a rule refers to, and an output for every pre-specified endpoint. Otherwise state explicitly why one is absent. |
| Outputs locked inside PDFs are hard to verify. | P5's only rendered TLFs are inside a compiled PDF in the programs folder; values had to be scraped. | Alongside the PDF, provide results in a structured form, such as analysis results data (ARD) or CSV/Dataset-JSON per table, with stable output IDs. |
| Format conventions matter more to machines than to people. | P5 Dataset-JSON: missing numbers stored as "NA" strings (33,888 in SDTM), all-decimal typing, a length of 3 for "DAYS", and `metaDataRef` pointing to a personal local path. | Validate Dataset-JSON against the schema and the spec: proper nulls, types and lengths, and only relative references. |

### 6.4 Pre-empt the questions an AI reviewer will raise

| Lesson | Evidence | Recommendation |
|---|---|---|
| Data-quality signals are flagged automatically. | Weekend visits (about 30%), duplicated AE records (230 pairs), MMSE inclusion violations, post-discontinuation assessments. | Explain known artefacts in the ADRG, such as date shifting in de-identified data, so they are not raised as integrity concerns. |
| Missing-data handling is challenged by default. | Differential LOCF (17.7 / 39.5 / 44.6%) with no estimand or sensitivity analysis. | State the estimand, and submit the sensitivity analyses that support the conclusion. |
| Traceability fields are followed. | AEACN blank for all AEs, so discontinuations can't be linked; SRCDOM/SRCVAR/EVNTDESC in ADTTE are generic or mislabelled. | Populate the variables that link outputs back to source records. |

### 6.5 Pre-submission checks that avoid back-and-forth

These come from the findings above. Each check would have prevented at least one finding in these pilots. Most are cheap to automate.

1. **Seriousness consistency:** AESER = "Y" whenever any seriousness criterion (death, hospitalization, life-threatening, disability, congenital anomaly) = "Y".
2. **Disposition traceability:** every discontinuation due to an AE links to at least one AE with AEACN = "DRUG WITHDRAWN".
3. **Actual vs planned treatment:** TRT01A is derived from EX/ACTARM, not copied from TRT01P. List any subjects where they differ.
4. **Duplicate records:** no exact duplicates on the key variables in AE or the other event domains.
5. **Documented rule reproduces data:** each define.xml derivation, run literally, reproduces the submitted variable (yamma-style).
6. **Claims check:** every quantitative statement in the ADRG and CSR is re-computed from the submitted datasets.
7. **Output labels:** titles, footnotes and axis labels match the analysis method and population.
8. **Endpoint coverage:** every primary and key secondary endpoint in the SAP has a dataset and an output, or a stated reason why not.
9. **Clean-session rebuild:** all ADaM and TLF programs regenerate the submitted files from a fresh environment.
10. **Format validation:** Dataset-JSON/XPT types, lengths, null handling and references are checked against the spec; no local paths.
11. **Missing-data summary:** the imputed fraction by arm and visit for the primary endpoint, with sensitivity analyses included.
12. **Known-artefact note:** the ADRG documents data-generation or de-identification artefacts that could look like realism problems.

## 7. Caveats

- **What "data only" means:** the statistical-reviewer worked from the submitted data and outputs. It also read the SAP, ADRG and programs where available, but it did not re-execute the documented derivation process the way yamma does.
- **yamma's own review status:** yamma's items are automated. About 30% are marked *disputed* in its own review step: 112 of 388, 72 of 248 and 83 of 233. Its counts reflect dashboard revision 24a55b1, viewed 2026-10-27.
- **Statistical-reviewer checks:** its findings come from one AI review pass per package. I spot-checked the key findings against source data (see report 1, §5). One error was found and corrected there: the Pilot 3 reviewer missed the TRT01A issue and miscounted subjects for C1.
- **Test data:** all three packages contain the public CDISC pilot test data. The realism signals would carry different weight in a real submission.
