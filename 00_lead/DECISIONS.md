# Decisions Log (Lead-owned, append-only)

| # | Date | Decision | Source |
|---|---|---|---|
| D1 | 2026-11-23 | Case study #4 Smart Palm Oil Plantation Management; problems/outcomes/inputs per `initial_plan.md` | Stakeholder |
| D2 | 2026-11-23 | AI-generated content is permitted (PDF clause outdated) | Stakeholder |
| D3 | 2026-11-23 | Deadline 15 Dec 2026 00:00 | Stakeholder |
| D4 | 2026-11-23 | Prefer training on a cloud platform; Research picks the platform based on Malaysian student credits/limits + fit. Fallback: local training + simple cloud deployment | Stakeholder |
| D5 | 2026-11-23 | Stakeholder owns the pH signal board. Demo prop = small potted plant. Extra parts: propose with MYR price, stakeholder chooses | Stakeholder |
| D6 | 2026-11-23 | Presentation runs from the stakeholder's laptop with WiFi | Stakeholder |
| D7 | 2026-11-23 | All deliverables in Markdown (stakeholder does final formatting) | Stakeholder |
| D8 | 2026-11-23 | Member names/IDs/group no. are placeholders | Stakeholder |
| D9 | 2026-11-23 | Lead checks in with stakeholder after Phase 1, then runs Phases 2–5 autonomously, reporting at gates. Problems must be validated by research, not assumed | Stakeholder |
| D10 | 2026-11-23 | Work runs as a parallel pipeline: research on demand (via `01_research/REQUESTS.md`), Hardware ∥ Software from the start, verification passes run alongside the builds at each milestone, outputs handed on as soon as they exist | Stakeholder |
| D11 | 2026-11-23 | In-text Harvard citations required in every section of the report and other deliverables, not just a reference list at the end | Stakeholder |
| D12 | 2026-11-23 | A baseline research wave (incl. `01_research/00_baseline_brief.md` giving direction per team) runs and passes the Lead gate BEFORE any other team starts; after that teams run in parallel with on-demand research | Stakeholder |
| D13 | 2026-11-23 | Each team writes its own `PLAN.md` (approach, ideas, conflicts, proposals) before building; the Lead rules on every proposal (accept → DECISIONS/SPEC updated, reject with reason, or escalate to stakeholder). The project plan and SPEC are living documents changed only through this route | Stakeholder |
| D14 | 2026-11-23 | Research wave 1 passed Lead gate: URLs for primary datasets + Azure/GEE pages resolve (HTTP 200); Zenodo D2 licence CC BY 4.0 confirmed via API; GCP trial exclusion of Vertex/"Gemini platform" for sign-ups ≥16 Nov 2026 and no-GPU-on-trial confirmed on official page; Azure for Students $100/no card confirmed; Azure "no quota increase" claim rests on Microsoft Q&A, not official docs (non-blocking) | Lead |
| D15 | 2026-11-23 | Enterprise platform recommended in report = **Microsoft Azure** (83/100), AWS runner-up, Google 68, IBM 49 (R-P3). Report must call Google's product "Gemini platform (formerly Vertex AI)" | Lead |
| D16 | 2026-11-23 | Primary datasets: D1 Kamal et al. (Mendeley, ripeness, train) + D2 Rosbi (Zenodo, Malaysian, test/fine-tune); D4 Mimboro et al. v2 (UAV RGB Ganoderma/palm detection, keep geographic split); Sentinel-2 L2A + global oil-palm mask in Earth Engine; fertiliser = SIMULATED from literature thresholds (labelled). No Roboflow, no GanoTrunk (R-P4) | Lead |
| D17 | 2026-11-23 | Shared demo thresholds (HW firmware + SW rules): pH 4.2–5.5 OK, <4.0 lime; moisture <30 % irrigate, >80 % drainage warning (demo calibration values, not literature); TDS calibrated on the day. pH/TDS probes measure soil-water slurry (R-P5) | Lead |
| D18 | 2026-11-23 | Part 3 novelty anchor = "explain-to-audit" MSPO/EUDR evidence log; supporting ideas: satellite→drone→ground screening cascade, harvester allocation from ripeness, train-Indonesia/test-Malaysia generalisation (R-P8) | Lead |
