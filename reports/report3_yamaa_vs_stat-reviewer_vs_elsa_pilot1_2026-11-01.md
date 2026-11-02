---
title: yamaa vs statistical-reviewer vs Elsa — detailed comparison on Pilot 1 (CDISCPILOT01)
date: 2026-11-01
study: CDISCPILOT01 (R Consortium Submissions Pilot 1)
sources:
  yamaa: https://rconsortium.github.io/submissions-pilot7-synthetic-data/studies/cdiscpilot01/ (dashboard revision 24a55b1, engine yamaa 0.6.2)
  stat_reviewer: statistical_review_pilot1_2026-10-27.md (statistical-reviewer skill, pharma-skills)
  elsa: https://github.com/RConsortium/submissions-pilot7-AI-review/blob/main/reports/FDA_filing_agent_reviews/CDISCPILOT01_Statistical_Filing_Review.md
---

# yamaa vs statistical-reviewer vs Elsa: Pilot 1

## 1. Bottom line

The three tools review the same submission from three different seats:

| | **yamaa** (open source) | **statistical-reviewer** (open source) | **Elsa** (simulated) |
|---|---|---|---|
| Seat | Data standards / programming | Sponsor-side independent statistician | FDA statistical reviewer at filing |
| Core question | Does the documented process reproduce the datasets? | Do the data and reported results hold up? | Is the application fileable, and what must the applicant answer? |
| Verdict on Pilot 1 | 100% reproduction (9.1 M cells); 388 documentation-consistency items | PASS WITH FINDINGS: 3 High / 8 Medium / 5 Low | **Not fileable** as a simulated NDA: 2 refuse-to-file (RTF) issues and 11 information requests (IRs). Acceptable as a pilot. |

**Key result:** the statistical-reviewer anticipated, at least in part, **12 of Elsa's 13** RTF and IR items. Only IR-11, the retired MRAN package repository, was missed. yamaa touched 5 of them (RTF-1, IR-1, IR-6, IR-7, IR-8), but only at the documentation level. It is the only tool that found the deep documentation defects, such as the BMI formula and lab-ratio definitions, which Elsa did not raise.

In practice, a sponsor running yamaa and the statistical-reviewer before submission would have seen nearly everything this simulated FDA filing review raised.

## 2. Inputs and approach

| | yamaa | statistical-reviewer | Elsa |
|---|---|---|---|
| Datasets used | SDTM (staged) → rebuilt 10 ADaM datasets, compared with the submitted reference | 12 ADaM XPT datasets | 5 ADaM datasets (ADSL, ADADAS, ADCIBC, ADAE, ADTTE), converted to CSV |
| Documents used | define.xml, SAP, data guide, executable specs | TLF report PDF, ADRG, define.xml, cover letter, FDA response letter | ADRG, define.xml, **SAP** (pp. 1–20), cover letter, MAPP 6610.5, FDA filing template |
| Programs | Its own executable specs | 4 TLF programs read; models re-implemented independently | 4 TLF programs read; not executed |
| SAP available? | Yes | **No** (not in the Pilot 1 package) | Yes (supplied separately) |
| Output | Dashboard items: conflict / divergence / gap, with own agreed/disputed review | Findings with severity, type, evidence, reproduced values | Filing memo: fileability decision, RTF issues, ordered IRs, appendix |

The statistical-reviewer had no SAP for Pilot 1. Elsa's SAP-based points therefore have no direct counterpart in its review: MMRM pre-specification, the multiplicity statement in SAP §7.3, the sex subgroup analysis in §7.2 and the planned enrollment of about 300. Even so, the statistical-reviewer reached the same conclusions from the data.

## 3. Finding-level crosswalk

**Legend:**

- **●** raised as a finding
- **◐** partly raised, or raised in a different form
- **—** not raised

The "Verified" column records the result of my own check against the Pilot 1 ADaM data. It is blank where no check was needed.

### 3.1 Elsa's refuse-to-file issues and information requests

| Elsa item | Elsa | statistical-reviewer | yamaa | Verified |
|---|---|---|---|---|
| **RTF-1** Co-primary CIBIC+ has no output (234 Week 24 records present) | ● | ● Medium. Also reproduced the analysis: null, p = 0.49 / 0.80. | ◐ Documentation items on ADQSCIBC only: AVISITN conflict on 168 of 730 records; AVAL LOCF on 10 records | ✔ 234 efficacy records |
| **RTF-2** AESER = "N" on all 3 fatal AEs; seriousness criteria met but not flagged | ● | ● High. "SAE subjects 3 vs 25" | — Only sort/partition gaps on AOCC02–04FL. The source and the submitted datasets agree, so yamaa cannot see it. | ✔ with correction: Elsa says "3 fatal + 36 additional AEs across 22 subjects". There are **36 records in total, including the 3 fatal ones**, in 22 subjects (6 / 9 Low / 7 High). 25 subjects meet any criterion, counting the 3 already flagged serious. |
| **IR-1** Pre-specified MMRM not submitted; differential LOCF 17.7 / 39.5 / 44.6% | ● | ● Medium. Also ran sensitivity analyses: OC, ITT, on-treatment; the null holds. | ◐ LOCF documentation divergences/gaps in ADQSADAS | ✔ |
| **IR-2** 37 subjects with post-discontinuation observed ADAS-Cog values in the primary analysis (5 / 21 / 11); estimand not stated | ● | ● High. Same 37 subjects; on-treatment re-analysis gives Low − Pbo −0.96 | — | ✔ 37 subjects; Placebo 5, Low 21, High 11 |
| **IR-3** AEACN blank on all 1,191 records; 92 AE discontinuations (8 / 44 / 40) untraceable | ● | ● High | — | ✔ |
| **IR-4** No multiplicity strategy across the co-primary endpoints and doses | ● (cites SAP §7.3) | ● Medium, within the CIBIC+ finding | — | |
| **IR-5** Sex subgroup analysis not submitted; female 61.6 / 59.5 / 47.6% hidden by omitting SEX from T14-2.01 | ● | ◐ Medium: sex and ethnicity omitted from T14-2.01, same percentages. Did not flag the missing subgroup analysis (no SAP). | — | ✔ |
| **IR-6** KM y-axis mislabelled; no HR, log-rank or counts; EVNTDESC typo | ● | ● Medium (label; reproduced HR 4.08 / 4.92) and Low (EVNTDESC, censoring) | ◐ ADTTE.ADT documented rule differs on 5 subjects | ✔ with correction: Elsa's "median days to event" (35 / 27 / 24) are medians **among subjects with an event**, not KM medians. The KM medians are not reached (Placebo), 33 days (Low, 95% CI 28–51) and 36 days (High, 25–47). The statistical-reviewer reported the KM medians correctly. |
| **IR-7** ADRG "Imputation: Not applicable"; 29 prorated ACTOT values; EFFFL undefined; visit windows missing | ● | ● Medium (same ADRG statement, proration, EFFFL and windows) | ◐ EFFFL define source is `ADSL.FASFL`, which does not exist; proration and LOCF rule divergences | |
| **IR-8** define.xml placeholder methods (186 instances); ADCIBC.AVAL has no codelist | ● | ● Medium (same placeholders; CIBIC+ codelist missing) | ◐ 388 clause-level items, much deeper than placeholders (see §3.3) | |
| **IR-9** Glucose table mislabelled; 63% missing in High Dose; denominator shift | ● | ● Medium | — | |
| **IR-10** Weight/BMI computed on n = 83 under header N = 84 | ● | ● Medium, within the demographics finding | — | |
| **IR-11** MRAN snapshot retired, so the package environment can't be restored | ● | — | — | Not checked |

### 3.2 Elsa appendix items

| Elsa item | Elsa | statistical-reviewer | yamaa |
|---|---|---|---|
| Enrollment 254 vs about 300 planned (SAP §6) | ● | — (no SAP) | — |
| No data cutoff date stated | ● | ● (limitation) | — |
| Weekend treatment starts (~30%), judged a de-identification artefact | ● (not a concern) | ● Medium realism finding | — |
| Censoring of AE discontinuers in TTDE potentially informative (2 / 12 / 10) | ● | ● Low | — |
| Potential unblinding through visible application-site reactions | ● | — | — |
| z-based CI and n-divisor RMSE in T14-3.02 | ● | ● Low | — |
| pilot1wrappers not inspectable without unpacking | ● | ◐ Noted; programs re-implemented instead | — |
| Derivation checks: CHG, TTDE AVAL, TRTDURD, ITTFL = SAFFL | ● Clean | ● Clean | ● 100% cell match on all variables |

### 3.3 Raised only by the statistical-reviewer or only by yamaa

| Finding | statistical-reviewer | yamaa |
|---|---|---|
| Treatment-emergent definition: no upper window; TRTEMFL blank instead of "N"; 11 undated AEs | ● Low | ● Conflict: define.xml and the SAP give different definitions (worsening, recurrence) |
| Integer range display hides prorated scores | ● Low | — |
| ADLBC/ADLBH ADT stored as numeric with no date format | ● Low | — |
| BMI formula multiplies height by 100 instead of dividing | — | ● Conflict, 253 subjects |
| Lab ratio variables (R2A1HI/LO, BR2A1HI/LO) divide by the opposite normal-range limit from the SAP | — | ● Conflict, 36,000+ records |
| COMP24FL: the SAP restricts completers to the efficacy population; define.xml does not | — | ● Conflict |
| VISNUMEN filter uses "PROTCOL COMPLETED", which matches no record | — | ● Conflict |
| EDUCLVL source named YEARSEDU; the data use EDLEVEL | — | ● Conflict |
| Hy's Law threshold: the SAP gives both 1.5 × and 2 × ULN | — | ● Conflict |
| ADVS.PCHG documented rule differs on 23,060 records | — | ● Conflict |
| Dermatologic flag rule `CQ01NAM=''` selects the wrong records (327 records) | — | ● Conflict |

## 4. Agreement on numbers

Where two or more tools reported the same quantity, I checked it against the Pilot 1 ADaM data:

| Quantity | Elsa | statistical-reviewer | Data |
|---|---|---|---|
| Week 24 LOCF % (ADAS-Cog) | 17.7 / 39.5 / 44.6 | 17.7 / 39.5 / 44.6 | ✔ |
| Week 24 LOCF n (CIBIC+) | 13 / 34 / 34 | — | ✔ 13 / 34 / 34 |
| AE discontinuations | 8 / 44 / 40 | 8 / 44 / 40 | ✔ |
| Post-discontinuation ADAS-Cog subjects | 37 (5 / 21 / 11) | 37 | ✔ |
| Female % | 61.6 / 59.5 / 47.6 | 61.6 / 59.5 / 47.6 | ✔ |
| Deaths (DTHFL) | 2 / 1 / 0 | 3 | ✔ |
| AESER = N with a criterion met | "3 fatal + 36 additional" | 36 records; SAE subjects 3 vs 25 | **36 records in total (the 3 fatal included)**; 22 subjects among them; 25 with any criterion |
| TTDE events | 29 / 62 / 61 | 29 / 62 / 61 | ✔ |
| TTDE median | 35 / 27 / 24 "median days to event" | KM 33 (Low) / 36 (High) | **KM:** not reached / 33 / 36. Elsa's values are medians among events only. |
| Primary result | p = 0.245 (taken from the submitted table) | p = 0.2447 (independently reproduced) | ✔ |

Both discrepancies are on Elsa's side, and both would matter in a real review:

- **Overstated SAE count:** "36 additional" serious events overstates the count by 3.
- **Non-KM median:** a "median days to event" computed among events only understates time-to-event and is not comparable across arms with very different event rates.

## 5. What each tool contributes

| | Unique contribution on Pilot 1 | Typical use |
|---|---|---|
| **yamaa** | Proves the SDTM → ADaM process is reproducible: 100% of 9.1 M cells. Finds documentation defects no data-level review can see, such as BMI, lab ratios, COMP24FL, VISNUMEN and the Hy's Law threshold. | **Operational fixes** before submission: specs, define.xml, ADRG, programs |
| **statistical-reviewer** | Independently reproduces the reported results and quantifies their robustness: OC, ITT and on-treatment re-analyses; HRs; KM medians. It anticipated 12 of Elsa's 13 RTF/IR items without the SAP. | **Sponsor pre-check:** signals that need interpretation in the CSR, and the IRs to expect |
| **Elsa** (simulated) | Regulatory framing: fileability, RTF vs IR, ordering by severity, citations to regulation (21 CFR 314.50) and the SAP. Raises items outside the data, such as the retired MRAN, the enrollment shortfall and the unblinding risk. | **Regulator's lens:** what the agency will ask, and how serious it is |

## 6. Lessons for AI-reviewer-friendly submissions

1. **Expect the AI reviewer to re-query the data.** Elsa confirmed every quantitative statement "by direct data query". Every claim in the ADRG ("Imputation: Not applicable") and every output label ("Probability of event") was tested against the data and failed. Run the same queries before submission.
2. **Submit what the SAP promises.** Both RTF issues and IR-1, IR-4 and IR-5 come from the gap between the SAP and the submitted outputs: CIBIC+, MMRM, the multiplicity decision rule and subgroups. An AI reviewer finds every SAP commitment without a matching output.
3. **Fix the safety data at source.** The two most serious data findings, AESER and AEACN, are invisible to process-level tools like yamaa. They need a data-level check (statistical-reviewer) before the regulator finds them (Elsa).
4. **Give definitions the reviewer can use.** Elsa needed the EFFFL rule, visit windows, the CIBIC+ scale direction and an estimand, and could not find them. Ambiguity becomes an IR.
5. **Keep the computing environment restorable.** IR-11 (MRAN retired) is the one item neither sponsor-side tool flagged. Pin package sources that will still exist at review time, such as an renv lockfile with a Posit Package Manager snapshot.
6. **Expect the AI reviewer to make mistakes too.** Elsa overcounted SAEs and reported a non-KM median. AI review output needs the same verification as any draft review; Elsa's memo itself carries that disclaimer.

## 7. Caveats

- **Elsa is simulated:** the "Elsa" memo is a simulated FDA review (Claude Sonnet 4.6) and a draft by its own description. It is not an FDA position.
- **Unequal inputs:** the three tools had different inputs. Only Elsa and yamaa had the SAP, and only yamaa had SDTM. yamaa covers 10 of Pilot 1's 12 ADaM datasets; ADLBCPV and ADLBHPV are not rebuilt.
- **yamaa review status:** yamaa's items are automated; 112 of 388 are marked *disputed* in its own review step.
- **Statistical-reviewer findings:** these come from one AI review pass. The cross-tool numbers in §4 were re-checked against the ADaM data on 2026-11-01.
