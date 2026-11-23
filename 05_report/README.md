# 05_report — README

## Status (24 Nov 2026, revision 2 after compliance audit 2: N-01…N-11 applied; body prose 3,715 + tables 767 ≈ 4,480 words, ≈4,560 with Figure 1; 34 references; 6 tables + 1 figure plus Table 4)

### Previous status (revision 1)
REPORT.md has been revised against REPORT_AUDIT_1 (C-01…C-23), research file 10, D49, D50 and D51. OUTLINE.md is at v4.

| Section | Prose words | Table words |
|---|---|---|
| Executive summary | 175 | — |
| 1 Introduction | 158 | — |
| 1.1 | 353 | — |
| 1.2 (Table 1) | 511 | 98 |
| 1.3 (Table 2) | 445 | 103 |
| 2.1 | 231 | — |
| 2.2 (Figure 1, ≈80 words in Mermaid not counted) | 242 | — |
| 2.3 (Table 3) | 468 | 108 |
| 2.4 (Table 4) | 276 | 156 |
| 2.5 (Table 5) | 58 | 237 |
| 3.1 | 324 | — |
| 3.2 | 202 | — |
| Conclusion | 151 | — |
| **Body total** | **3,594** | **702** → **≈4,300 (≈4,380 with Figure 1)** |

The body is within D49 (about 4,300–4,700 words; references and appendix excluded). There are 32 references.

## Inputs used
Assignment PDF; `00_lead/` SPEC, DECISIONS D1–D40, PROJECT_PLAN, `briefs/report.md`; `01_research/` 00, 01, 02, 06, 07, 08, 09 and `sources.md`; `03_software/` docs 01–05.

## Outputs
| File | Content |
|---|---|
| `REPORT.md` | Submission report (Markdown) |
| `OUTLINE.md` | Living outline (v3), with changelog (D36/D37) |
| `RUBRIC_MAP.md` | Sub-task → section cross-reference (internal, moved out of the report per D40) |
| `PLAN.md` | Original plan and proposals REP-P1–P3 (P1 and P2 accepted in D34) |

## Core reference list (34). Reuse only these
The assembler mapping is fixed. In-text form → key:
- Abdul Hadi et al. (2026) → MPOB-TT698
- Ahmad et al. (2020) → AHMAD2020
- Amazon Web Services (2025) → AWS-REGTABLE
- Amazon Web Services (n.d.a) → AWS-CLARIFY
- Amazon Web Services (n.d.b) → AWS-APPFLOW-SAP
- Amazon Web Services (n.d.c) → AWS-GG
- BSI Services Malaysia (2023) → BSI-SDG-RSPO2023
- Che Hassan et al. (2026) → HASSAN2026
- Chong (2026) → STAR-FERT2026
- Clark (2022) → REG-WIOT
- European Commission (2026) → EC-EUDR
- Google Cloud (2026) → GCP-REGIONS
- Google Cloud (n.d.) → GCP-IOTCORE
- Google Earth Engine (n.d.) → GEE-S2
- IOI Corporation Berhad (2020) → IOI-S4HANA2020
- Khoo and Chong (2023) → KHOO2023
- Kwang et al. (2025) → KWANG2025
- MPOB (2026) → MPOB2025
- MPOCC (2023a) → MPOCC-P32
- MPOCC (2023b) → MPOCC-P41
- MSPO and EFI (2025) → MSPO-EFI2025
- Mayer Brown (2025) → MAYER-PDPA2025
- Microsoft (2025) → AZ-RAI
- Microsoft (2026a) → AZ-PRICES-API
- Microsoft (2026b) → AZ-IOTOPS
- Microsoft (n.d.a) → AZ-ACL
- Microsoft (n.d.b) → AZ-SAP
- Microsoft (n.d.c) → AZ-ACL-RES
- IOI Corporation Berhad (2026) → IOI2026
- New Straits Times (2019) → NST-FELDA2019
- Ramendran (2026) → STAR-LAB2026
- The Edge Malaysia (2025) → EDGE-SDG2025
- The Edge Malaysia (2026) → EDGE-LAB2026
- The Edge Malaysia (n.d.) → EDGE-FELDA

Dropped in revision 1: Ma (n.d.), IOI2026, Amazon (2024), AZ-REGIONS, AZ-AOAI-MODELS, MPOCC-P31.

## Compliance notes
- D20/D40: no Kaggle, Colab, student, prototype or "simulated" wording. Validation is described as a planned step.
- D23: platforms are compared on capability only; cost appears only as risk 5.
- D32: residency split in 2.4 and risk 6; Responsible AI dashboard for the tabular model only and Grad-CAM for the image models; *Ganoderma* is described as screening.
- RM2.2 bn is labelled as the authors' calculation and RM7.5–20 bn as an employer estimate.

## Open issues for Lead
1. **C-05:** member contributions and the Appendix A placeholders need the stakeholder.
2. **MSPO clause numbering:** research confirms 4.1.3, 4.2.2, 4.5.4 and 4.5.5 in Part 3-2. Sub-indicators 4.1.3.4 (block reference) and 4.1.3.5 (IPM) are confirmed only in Part 3-1. I listed them in 3.1 to match the code's audit pack (D45). A quick check against the Part 3-2 guidance would settle it.
3. **Residency evidence:** Malaysia West availability is cited to the Azure Retail Prices API, which is indicative only (research file 10). The text therefore says placement follows Microsoft's products-by-region listing at deployment.
4. **C-08:** resolved by removing the uncited pH numbers. The counterfactual example now refers to the knowledge base's band, so KANANG2026 was not needed.
5. **C-09:** "export Mermaid as an image" is for the stakeholder at the formatting stage.
