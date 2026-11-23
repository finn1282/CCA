# Report Audit 1 — compliance & rubric (REPORT.md @ 29344b9)
> Findings by the Compliance member; saved by the Lead (the member's file write was blocked by tooling). Audited against the PDF pp.2–9, SPEC, DECISIONS D1–D44, OUTLINE v3, RUBRIC_MAP, 01_research.

## Estimated marks
| Criterion | Band | Now | After fixes |
|---|---|---|---|
| P1 Problem identification (10) | Outstanding (low–mid) | 8.5 | 9.5 |
| P2 Technology & solution (15) | Low Outstanding (2.3 borderline Mastering) | 12.0 (11.5–12.5) | 13.5–14 |
| P3 Creative thinking (5) | Low Outstanding | 4.0 (4.0–4.5) | 4.5–5 |
| **Total (30)** | | **≈24.5** | **≈28** |
Sub-tasks: 1a 1.7/2 · 1b 3.5/4 · 1c 3.3/4 · 2a 1.8/2 · 2b 2.4/3 · 2c 3.8/5 · 2d 2.4/3 · 2e 1.7/2 · 3a 2.4/3 · 3b 1.6/2.

## Defects
| ID | Sev | Section | Issue | Fix |
|---|---|---|---|---|
| C-01 | major | 2.3, Exec, Concl | "Azure is the only platform… in-country region + first-party IoT/offline edge + native SAP" contradicted by Table 3 (AWS 5/5/4); AWS C7=3 "not assessed" | Research AWS IoT Core/Greengrass/SageMaker vision/SAP integration; rescore AWS with citations; recommend on evidenced differentiators; "best fits" not "uniquely" (+~1.5) |
| C-02 | major | 2.3 | "AWS was researched in less depth" admits incomplete evaluation | Delete; replace with evidenced AWS limitation; add AWS citations (+0.5) |
| C-03 | major | 2.4, 2.3 C7, Exec | SAP use by FELDA/FGV/SDG/IOI unverified, yet C7=5 relies on it | Find citable ERP evidence, else "the estate ERP (e.g. SAP S/4HANA or ECC)" (+0.5–1) |
| C-04 | major (rule) | whole | Body ≈4,240 words OK, but body+tables+figure ≈13 pp, refs 2.5–3 pp, App. A ≈0.7 pp → ≈16–17 pp total vs D35 "10–15 total" | Stakeholder to rule whether refs/appendix count; if yes cut 400–600 words (1.2 +57 over; trim Table 5 mitigations; compress Fig. 1) |
| C-05 | major (req.) | App. A | Member contributions placeholders (PDF requires) | Stakeholder fills (placeholders per D8/D40) |
| C-06 | minor | 2.4, 3.1 | Azure confidential ledger uncited | Cite AZ-ACL-RES |
| C-07 | minor | 1.2 | 43 % and 860,610 ha are secondary | "(Olaniyi and Szulczyk, 2020, cited in Khoo and Chong, 2023)" |
| C-08 | minor | 1.3/3.1 | pH 4.0/4.2 thresholds uncited; 4.0–4.2 band undefined | Cite KANANG2026; define watch band |
| C-09 | minor | Fig. 1 | Cross-cutting linked only to L3; Power BI missing in L5 | Link to all layers; add Power BI; export Mermaid as image |
| C-10 | minor | Table 3 | Geospatial-heavy weights unstated | Caption: C4=30; C1,C2,C5,C7=10; C3,C6=15 |
| C-11 | minor | Table 3 | Linked-problem column | C2→P1,P3; C6→P1–P3 |
| C-12 | minor | Table 5 | Risk 6 category not a Fig. 6 category | "Vendor & cost (service availability)" |
| C-13 | minor | Table 4 | Long-term lacks "continuous learning and governance" | Add retraining from overrides + quarterly model-governance review |
| C-14 | minor | Refs | The Edge (n.d.) entry has internal note | Remove note |
| C-15 | minor | Refs | Kwang conference entry lacks "in *Proceedings*" | Fix format |
| C-16 | minor | Refs/1.2 | MPOCC Part 3-1 guidance (40.46–500 ha) vs large estates; "MS 2530:2022" vs "MS2530-3-1:2022" | Research confirm clause numbers / Part 4 equivalence |
| C-17 | minor | 2.2 | Planetary Computer/STAC uncited | Cite GEE (n.d.) or MPC-S2 |
| C-18 | minor | 1.1 | "Current situation" rests on undated Ma (n.d.) | Add recent co-citation |
| C-19 | minor | 1.1 | Stakeholders listed without stakes | ~30 words of stakes |
| C-20 | minor | 1.2 | Missing strongest P1 evidence | Harvest rounds 7–13 → 20–25 days (AHMAD2020); use as Table 4 baseline |
| C-21 | minor | RUBRIC_MAP | Claims M365 in 2.4, absent in report | Align |
| C-22 | minor | 1.3/2.1 | P1 forecast/optimiser method unnamed | Name method |
| C-23 | minor | 3.2 | Evolution not tied to roadmap; no "new knowledge" | Tie steps to Table 4 phases; pooled anonymised override data → sector benchmark |

## Checks passed
- **Rules D20/D23/D32/D40:** no violations (grep of kaggle, colab, student, credit, free, simulat, prototype, price, esp32, hardware… all acceptable hits).
- **Citations:** 26 refs ↔ 26 in-text sources, 1:1. 12 URLs spot-checked → HTTP 200.
- **Numbers:** key numbers match 01_research; OER calc and Table 3 totals (88/79/67/49; equal 89/80/66/49) recomputed correct.
- **Consistency:** problem order, names, numbering and captions all consistent.
