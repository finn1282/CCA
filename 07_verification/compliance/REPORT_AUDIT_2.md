# Report Audit 2 (REPORT.md @ 7d8b711) — saved by Lead from the Compliance member's text reply
## Verdict
| Criterion | Max | Audit 1 | **Audit 2** | After fixes |
|---|---|---|---|---|
| 1 Problem identification | 10 | 8.5 | **9.0** | 9.5 |
| 2 Technology & solution | 15 | 12.0 | **12.5–13.0** | 13.5–14 |
| 3 Creative thinking | 5 | 4.0 | **4.5** | 4.5–5 |
| **Total** | 30 | ≈24.5 | **≈26–26.5** | **≈28** |

- **Audit 1 items:** all C-xx fixed, except C-05 (stakeholder).
- **Rules:** no violations (D20/D23/D40/D49/D50/D51).
- **Citations:** 32 references ↔ in-text, 1:1; 13 new URLs → HTTP 200.
- **Numbers:** Table 3 (89/85/67/49; 89/86/66/49; 84/80/75/50) and the OER calculation recomputed correct.
- **MSPO:** Part 3-2 clauses 4.1.3, 4.1.3.1, 4.1.3.4, 4.1.3.5, 4.2.2, 4.5.4, 4.5.5 verified in the PDF.
- **Length:** body ≈4,430 words ≈13.5–14 pp (D49 OK; ~1 pp headroom).

## 2.3 defensibility
Low-Outstanding as written (2c ≈4.0/5); ≈4.5/5 with N-01, N-02, N-03, N-04 and N-06.

## Defects
| ID | Sev | Section | Issue | Fix |
|---|---|---|---|---|
| C-05 | major (req.) | App. A | Member contributions placeholders | Stakeholder fills; cover + Declaration Form at formatting |
| N-01 | major | 1.1, 2.3 c2, Exec, Concl | "Weeks offline under the canopy" has no Part 1 evidence | Add connectivity bullet to 1.1: IOI built >100 private 4G/LTE sites (IOI2026, restore → 33 refs). Rename constraint 2 "Long outages on remote blocks (P1–P3)"; drop "weeks"/"under the canopy" |
| N-02 | major | 2.3 | Reads as post-hoc override of our own matrix | State the two-stage method before Table 3 (capability breadth, then case-critical requirements a weighted sum can't trade off); optional 3-row pass/partial table |
| N-03 | major | 2.3, 2.4, risk 6, refs | Residency cited to the Retail Prices API but described as products-by-region | Cite the products-by-region page if it can be confirmed; else retitle "Retail Prices REST API, used as a regional service-availability index" + "(indicative)". Re-add citation to the 2.2 NLP/OpenAI bullet |
| N-04 | minor | 2.3 | C6 AWS 5 vs constraint 3 favouring Azure | C6 scores breadth (Clarify covers images); constraint 3 is about audited tabular decisions (counterfactuals) |
| N-05 | minor | 1.1 | SDG "and accounting on SAP" overclaims | Estate master data held in SAP |
| N-06 | minor | 2.3 c1 | In-country SAP point missing; AppFlow overextended | Logic Apps runs in Malaysia West; "AWS's managed SAP connector, AppFlow, uses OData only" |
| N-07 | minor | 2.3 | Awkward runner-up bullet | Rephrase |
| N-08 | minor | refs | The Edge (n.d.) still has "6 October" | Delete |
| N-09 | minor | 3.1 | "Tamper-evident" cited to the residency page | Add ledger overview source, or move the citation |
| N-10 | minor | 2.4, Fig 1 | DPS with Event Grid MQTT unconfirmed | "certificate-based client registration"; drop DPS unless confirmed |
| N-11 | minor | Exec | 174 vs 150 words | Merge bullets |
