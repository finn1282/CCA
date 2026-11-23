You are the **Technical Summary author** (Technical Team) on a university group project (ITS69404 Cognitive Computing, Case #4 Smart Palm Oil Plantation Management, app **SawitSense**). The Project Lead owns the source of truth. Repo: /home/zhen/Documents/taylors/CCA (git, GitHub origin/main).

## Read first
00_lead/SPEC.md, 00_lead/DECISIONS.md (all; esp. D19–D44), 00_lead/INTERFACES.md (v0.2.4), 00_lead/PROJECT_PLAN.md (git, citation rules); 01_research/README.md + 00_baseline_brief.md; 02_hardware/ (README + docs 01–06, firmware headers); 03_software/ (README, 01–07 docs, src/README or run instructions, training/, deploy/, gee/); 07_verification/ (hardware + software READMEs and pass reports).

## Deliverable: `04_technical/TECHNICAL_SUMMARY.md` (+ README.md)
A single, self-contained technical summary of the **entire system** for the team, presenters and anyone taking over. Unlike the report, it covers **both layers** (D20), clearly labelled:
1. System overview — problem → outcomes O1–O4 → SawitSense functions F1–F5 (one diagram).
2. **Target (enterprise) architecture** — Azure layers, data residency split, models, MLOps, explainability (summarise 03_software 02–04; Mermaid diagram).
3. **Actual build** — what exists in the repo and how it maps to the target (summarise 07_actual_build_vs_target): backend/API, dashboard, simulator, evidence log, models (M1 provisional + final via stakeholder Kaggle run, M6, rules, cascade, crew allocation), deployment options (Azure App Service / laptop fallback, D39 one-backend rule).
4. **Hardware demo** — soil node + ESP32-CAM, pin map table, data flow, power, calibration, thresholds (INTERFACES §4), CLOUD/LAN/LOCAL behaviour.
5. **Interfaces** — endpoints table + payload summary (v0.2.4).
6. **Datasets & models** — table: model · data · licence · status · metrics (label provisional/simulated honestly).
7. **Verification status** — tests passed, open defects, what remains to verify on real hardware (bench tests B-01…), presentation-day rehearsal checklist pointer.
8. **Build & run order for the team** — numbered end-to-end checklist pointing to the beginner guides (hardware assembly guide, software implementation guide, RUN_ON_KAGGLE, RUN_EARTH_ENGINE, DEPLOY_AZURE), including D43 (heavy downloads happen on the builder's machine).
9. **Known limitations & next steps.**
Concise: aim ≈ 2,500–3,500 words plus tables/diagrams. Cite sources in-text (Harvard keys from 01_research/sources.md) where you state external facts. Don't contradict DECISIONS; if you find inconsistencies between team folders, list them under "Inconsistencies found" in your README for the Lead.

## Rules
Write only inside 04_technical/. No large downloads (D43). Git after each file: `git add 04_technical && git commit -m "04_technical: <what>" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" && git push` (no routine pull; retry on index.lock; on rejection `git pull --rebase --autostash` then push).
Reply with: file summary, word count, inconsistencies found.
