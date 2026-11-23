# 05_report — README

## Status (23 Nov 2026, after D40)
**Full draft of REPORT.md complete**, following OUTLINE v3 (approved v2 + D40 changes). No cover page, TOC or formatting (the stakeholder adds them).

| Section | Prose words | Table words | Status |
|---|---|---|---|
| Executive summary | 153 | — | Drafted |
| 1 Introduction | 147 | — | Drafted |
| 1.1 Case | 288 | — | Drafted |
| 1.2 Problems (Table 1) | 515 | 96 | Drafted |
| 1.3 Capabilities (Table 2) | 460 | 98 | Drafted |
| 2.1 SawitSense | 238 | — | Drafted |
| 2.2 Technologies (Figure 1) | 399 (incl. ~75 in Mermaid) | — | Drafted |
| 2.3 Platforms (Table 3) | 454 | 104 | Drafted |
| 2.4 Integration and roadmap (Table 4) | 212 | 148 | Drafted |
| 2.5 Risks (Table 5) | 59 | 242 | Drafted |
| 3.1 Novelty | 349 | — | Drafted |
| 3.2 Extension | 158 | — | Drafted |
| Conclusion | 152 | — | Drafted |
| **Total body** | **≈3,580** | **≈690** | **≈4,270 words, inside the D35 budget (≈4,300)** |
| References | 26 Harvard entries, cited only | | |
| Appendix A | Timeline + contribution tables, placeholders | | ≤1 page |

Six captioned tables and figures: Tables 1–5 and Figure 1.

## Inputs used
Assignment PDF; `00_lead/` SPEC, DECISIONS D1–D40, PROJECT_PLAN, `briefs/report.md`; `01_research/` 00, 01, 02, 06, 07, 08, 09 and `sources.md`; `03_software/` docs 01–05.

## Outputs
| File | Content |
|---|---|
| `REPORT.md` | Submission report (Markdown) |
| `OUTLINE.md` | Living outline (v3), with changelog (D36/D37) |
| `RUBRIC_MAP.md` | Sub-task → section cross-reference (internal, moved out of the report per D40) |
| `PLAN.md` | Original plan and proposals REP-P1–P3 (P1 and P2 accepted in D34) |

## Core reference list (26). Reuse only these
In-text form → `sources.md` key:
- Amazon (2024) → AWS-MYREGION
- Che Hassan et al. (2026) → HASSAN2026
- Chong (2026) → STAR-FERT2026
- Clark (2022) → REG-WIOT
- European Commission (2026) → EC-EUDR
- Google Cloud (2026) → GCP-REGIONS
- Google Cloud (n.d.) → GCP-IOTCORE
- Google Earth Engine (n.d.) → GEE-S2
- IOI Corporation Berhad (2026) → IOI2026
- Khoo and Chong (2023) → KHOO2023
- Kwang et al. (2025) → KWANG2025
- Ma (n.d.) → MA-POEB
- MPOB (2026) → MPOB2025
- MPOCC (2023) → MPOCC-P31
- MSPO and EFI (2025) → MSPO-EFI2025
- Mayer Brown (2025) → MAYER-PDPA2025
- Microsoft (2025) → AZ-RAI
- Microsoft (2026a) → AZ-AOAI-MODELS
- Microsoft (2026b) → AZ-REGIONS
- Microsoft (2026c) → AZ-IOTOPS
- Microsoft (n.d.) → AZ-SAP
- New Straits Times (2019) → NST-FELDA2019
- Ramendran (2026) → STAR-LAB2026
- The Edge Malaysia (2025) → EDGE-SDG2025
- The Edge Malaysia (2026) → EDGE-LAB2026
- The Edge Malaysia (n.d.) → EDGE-FELDA

## Compliance notes
- D20/D40: no Kaggle, Colab, student, prototype or "simulated" wording. Validation is described as a planned step.
- D23: platforms are compared on capability only; cost appears only as risk 5.
- D32: residency split in 2.4 and risk 6; Responsible AI dashboard for the tabular model only and Grad-CAM for the image models; *Ganoderma* is described as screening.
- RM2.2 bn is labelled as the authors' calculation and RM7.5–20 bn as an employer estimate.

## Open issues for Lead
1. Placeholders remain: [GroupNo], [Lecturer name], [Member n], [ID], and the roles and contributions in Table A2. Timeline owners in Table A1 are illustrative and need the stakeholder's real allocation.
2. Azure confidential ledger is named in 2.4 and 3.1 without its own citation, because AZ-ACL-RES was left out to stay at 26. Swap it in for one reference if you want the "replicates to a paired region" point cited.
3. The 2.3 AWS caveat (C7 researched in less depth) is stated openly, as research file 08 recommends.
