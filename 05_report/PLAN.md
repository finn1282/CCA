# 05_report — PLAN

> Owner: Report member (Outputs Team). Deliverable: `05_report/REPORT.md` (Markdown; stakeholder formats to TNR 12 / 1.5 / justified).
> Inputs: `CCA Group Assignment.pdf` (pp.5–9), `00_lead/SPEC.md`, `DECISIONS.md` (D19, D20, D23, D24, D28, D32), `PROJECT_PLAN.md`, `01_research/` 00, 01, 02 (v2), 06, 07, 08, `sources.md`; `03_software/` design docs 01–05 and `04_technical/` when they exist.

## 1. Approach
1. **Rubric first.** Every heading maps to one PDF sub-task; Appendix B is the cross-reference. Each section opens with the claim, then the evidence, then the critical point (limit, trade-off or counter-evidence), because the Outstanding band asks for *critical* and *insightful* analysis, not description.
2. **Evidence discipline.** Every paragraph with a factual claim carries a Harvard (Author, Year) citation that resolves to a `01_research/sources.md` entry. Research's own arithmetic is labelled "authors' calculation" and shows the working. Simulated data is labelled. The reference list holds only cited sources.
3. **Content rules.** D23 (no hardware/demo detail; capability-only justification; cost only as a Part 2 risk), D20 (fully Azure-native target design; no mention of the build workaround), D32 (residency split, RAI dashboard for the tabular model only, Grad-CAM for image models, Ganoderma as screening). Privacy only where it constrains integration (PDPA 2010 as amended 2024).
4. **Originality.** Paraphrase all sources and synthesise across them (Turnitin <20 % overall, <2 % per source). No source sentence is reused verbatim; short quotations only where wording matters, in quotation marks with a citation.
5. **Order of drafting (this run).** PLAN → README → REPORT skeleton + cover → Part 1 (1.1–1.3) → Introduction → Appendix B. Part 2, Part 3, executive summary and conclusion wait for the Software design docs 01–05 and `04_technical/`.

## 2. Section-by-section evidence plan
| Section | Marks | Core argument | Main evidence (keys) | Status |
|---|---|---|---|---|
| Cover, TOC | — | Placeholders per SPEC §7 | — | This run |
| Executive summary | — | Problems → SawitSense → Azure → roadmap → novelty | All parts | After Part 3 |
| 1 Introduction | — | Why palm oil matters; why a cognitive system; scope and structure of the report | MPOB2025, PARVEEZ2025, MSPO-EFI2025, HL-EUDR2026 | This run |
| 1.1 Case | 2 | Record output masks a fragile production base; three organisations with different exposure; stakeholder map; current information practice | MPOB2025, PARVEEZ2025, EDGE-SDG2025, IOI2026, MSPO-EFI2025, STAR-EUDR2025, EDGE-LAB2026, MPOB-APPS2025 | This run |
| 1.2 Problems | 4 | P1 > P2 > P3 with explicit ranking criteria (scale of loss, urgency, cognitive addressability), evidence and honest nuance | STAR-LAB2026, EDGE-LAB2026, EDGE-SDG2025, MA-POEB, RAMLI2026, AHMAD2020, MPOB-NEWS2020, IBRAHIM2020, BORNEO-GANO2025, KHOO2023, SARMIDI2025, VIBES-REPLANT2025, MSPO-EFI2025, MPOCC-P21/P31, STAR-FERT2026, AAR-SOIL | This run |
| 1.3 Capabilities | 4 | One primary capability per problem + supporting ones; conventional method and its limit; why cognitive is better; limits stated | HASSAN2026, MANSOUR2022, OMAR2024, AHMADI2023, KWANG2025, DARANAGAMA2025, D4-MIMBORO2026, COOPER2011, GEE-S2, KOK2021, KANANG2026, CARR2011, AZ-RAI | This run |
| 2.1 SawitSense | 2 | Name, core functions F1–F5, target users | 03_software docs, D24, D28 | Waits on Software |
| 2.2 Technologies | 3 | Adapted Fig. 4 layered architecture (Mermaid), each technology justified by capability | 06_azure…, 03_software docs | Waits |
| 2.3 Platforms | 5 | Capability-only matrix (Azure 88 / AWS 79 / Google 67 / IBM 49), sensitivity checks, honest caveats, one recommendation linked to P1–P3 | 08_platform…, AZ-*, AWS-*, GCP-*, REG-WIOT | Waits (design doc for integration) |
| 2.4 Integration + roadmap | 3 | SAP/ERP, LoRaWAN → IoT Hub, residency split; short/medium/long per Fig. 6 | AZ-SAP, TTS-AZURE, AZ-IOTOPS, AZ-DPS, MAYER-PDPA2025 | Waits |
| 2.5 Risks | 2 | Technical/operational/vendor & cost, prioritised, mitigations | 08 caveats, ANZUM2022, AZ-RAI, AZ-ACL-RES | Waits |
| 3.1 Novelty | 3 | Explain-to-audit log, counterfactuals, cascade, harvester allocation, cross-country validation | D18, D28, MPOB-APPS2025, AZ-ACL, AZ-RAI | Waits |
| 3.2 Extension | 2 | Organisation (smallholders, mills) and other sectors (rubber, cocoa under EUDR) | HL-EUDR2026 + new sources (request) | Waits |
| Conclusion | — | Answer to the case | — | Last |
| References | — | Harvard, alphabetical, cited only | sources.md | Grows per section |
| Appendix A | — | Progress report placeholders | git log, PROJECT_PLAN | Later |
| Appendix B | — | Sub-task → section map | PDF pp.5–9 | This run |

## 3. Ideas
- **Explicit prioritisation criteria** in 1.2 (economic loss, urgency/time-to-harm, labour dependence of the current fix, cognitive addressability) scored in a small table, so "prioritised" is argued rather than asserted.
- **Interdependence argument:** P2 and P3 both worsen P1 (visual census and manual record-keeping consume the same scarce labour; tall ageing palms cut harvester output), which justifies P1 as the root priority and the integrated system in Part 2.
- **"Conventional vs cognitive" comparison table** in 1.3 (one row per problem) and a Mermaid figure mapping problems → capabilities → outcomes O1–O4.
- **Balanced claims:** say what cognitive computing *cannot* do (replanting capital; diagnosis of BSR; no public soil-sensor data) — rewarded as critical reasoning.

## 4. Conflicts / cautions
| # | Issue | Handling |
|---|---|---|
| C1 | SPEC §8 says "64 entries"; `sources.md` now has 95 (D32). | Use the 95-entry file. No action needed. |
| C2 | Baseline brief cites the old 83/78/68/49 matrix; D32 supersedes with 88/79/67/49. | Use D32 / `08_…` figures in 2.3. |
| C3 | RM7.5–20 bn loss figure is an employer-federation estimate; RM2.2 bn is Research's calculation. | Labelled as such in text. |
| C4 | FGV/FELDA ownership change was "not opened, unverified". | Not asserted; FELDA described only as the organised-smallholder scheme operator. |
| C5 | No source in `sources.md` for FELDA's own scale or for rubber/cocoa EUDR coverage (needed in 3.2). | Request R-REP1 in `01_research/REQUESTS.md`. |

## 5. Proposals
| ID | Proposal | Why | Impact | Lead ruling |
|---|---|---|---|---|
| REP-P1 | Score the problem ranking in 1.2 with four explicit criteria (Table 2) rather than an unstructured argument. | Rubric's Outstanding band requires that problems be *prioritised*; a transparent rule is easier for a marker to credit and for the presenter to defend in Q&A. | Presentation may reuse Table 2. | Pending |
| REP-P2 | Add a short "interdependence" paragraph showing P2 and P3 aggravate P1. | Gives an "insightful" problem statement and pre-justifies an integrated platform in Part 2. | None. | Pending |
| REP-P3 | Request one source on FELDA scale and one on EUDR commodity scope (rubber, cocoa) — R-REP1. | 1.1 would otherwise describe FELDA without a citation; 3.2 needs evidence for the cross-sector extension. | Research wave on demand. | Pending |
