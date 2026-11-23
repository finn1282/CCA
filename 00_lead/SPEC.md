# SPEC — Single Source of Truth

> Owner: Project Lead. **Every team member reads this file first.** If anything you find contradicts
> this file, do not silently diverge — write the conflict in your folder's `README.md` under
> "Open issues for Lead" and the Lead will rule on it and update this file + `DECISIONS.md`.

## 1. Assignment (target goal)
- Source: `CCA Group Assignment.pdf` (repo root). Module ITS69404 Cognitive Computing and Applications, Group Assignment One, 30% of module.
- Case study: **#4 Agriculture — Smart Palm Oil Plantation Management** (Malaysia: FELDA, Sime Darby Plantation (now SD Guthrie), IOI).
- **Hard deadline: report submission 15 Dec 2026, 00:00** (i.e. end of 14 Dec). Presentation Week 13, 15 minutes, all 5 members speak, Q&A on any part.
- Report requirements (content): Harvard referencing, **≥10 credible sources** (industry reports, academic papers, vendor docs), progress report with each member's contribution, cover page with names/IDs (placeholders for now). Formatting is handled by the stakeholder — deliver **Markdown**.
- AI-generated content is **permitted** this year (stakeholder confirmed; the PDF clause is from an old template).

## 2. Marking (what we optimise for — aim for "Outstanding" band in every criterion)
| Part | Weight | Sub-tasks (marks) | Outstanding-band requirement |
|---|---|---|---|
| 1 Case Analysis & Problem ID | 10 | Describe case: orgs, stakeholders, current situation (2) · ≥3 problems justified with evidence (4) · cognitive capability per problem (4) | Critical, insightful problem statement; substantial evidence from credible sources; **problems prioritised**; explains **why cognitive computing beats conventional systems for each** |
| 2 Technology Evaluation & Solution | 15 | App name/core functions/target users (2) · underlying technologies justified (3) · **compare ≥3 enterprise platforms** (e.g. watsonx, Vertex AI, Azure AI, SageMaker) on case-relevant criteria, recommend ONE linked to Part 1 problems (5) · integration with existing IT + **phased plan short/medium/long** (3) · integration risks (technical/operational/vendor & cost) + mitigations (2) | Rigorous multi-perspective reasoning with credible evidence; shows why the chosen platform **uniquely** fits; detailed feasible phased plan; **risks prioritised** with concrete actionable mitigations. Privacy/security only where it constrains integration (e.g. PDPA 2010) |
| 3 Creative Thinking & Innovation | 5 | Novelty vs off-the-shelf (3) · future extension to org/other sectors (2) | Novel idea that crosses boundaries/creates new knowledge, convincing account of how it evolves. Unique tech combination, new interface, **AI explainability** |
- The PDF's Figure 4 layered architecture (Data Sources → Ingestion/Big Data → Cognitive Services → Cloud & Deployment → Application & User, plus cross-cutting concerns) must be **adapted** to our case, not copied.
- The PDF's Figure 6 structure (Short/Medium/Long roadmap; Technical/Operational/Vendor & cost risk boxes each with mitigation) must be followed.

## 3. Problems, outcomes, inputs (from stakeholder brief — validate with evidence, do not assume)
**Problems:** P1 yield pressure from labour shortages · P2 ageing trees · P3 MSPO sustainability requirements. (Ganoderma basal stem rot is a core yield threat expected to sit under P1/P2 — Research to confirm framing and priority order with evidence.)
**Outcomes:** O1 predict ripe FFB harvest windows · O2 detect Ganoderma early · O3 optimise fertiliser use · O4 improve yield and meet sustainability (MSPO) requirements.
**Inputs:** satellite imagery · drone (UAV) data · IoT soil sensors.

## 4. Scope rules
- The system design (cloud AI, data, models, platform evaluation, integration) is the **main deliverable**. The hardware is a **small live demo** representing the IoT soil-sensor layer only — it must never dominate the report or presentation.
- Train on a cloud platform if credits allow (Research decides which); fallback = train locally and deploy a simple cloud endpoint/dashboard.
- Prefer real, downloadable, properly licensed datasets. If a dataset doesn't exist for an outcome, say so and use a documented proxy or simulated data, clearly labelled.
- Conserve tokens/credits: Markdown outputs, concise but complete; Mermaid for diagrams (renders on GitHub).

## 5. Demo (draft — Hardware/Software finalise)
- **Prop:** a small potted plant stands in for a palm (stakeholder choice).
- **ESP32 soil node** (NodeMCU ESP32): capacitive soil moisture, pH probe **with signal board (stakeholder has it)**, TDS (EC proxy for nutrient level), DS18B20 soil temp, DHT22 air temp/humidity, 0.96" OLED, LEDs, push buttons, powered by power bank → WiFi → cloud/dashboard → live fertiliser/irrigation recommendation.
- **ESP32-CAM:** captures an image (e.g. printed FFB photo / leaf) → model returns ripeness / disease class live.
- Satellite + drone analytics shown in dashboard as pre-computed results from real datasets.
- Presenting laptop has WiFi; presentation runs from the laptop.
- Extra components: **propose only, with price in MYR and justification; stakeholder chooses within budget.**

## 6. Available hardware (`components.md`)
NodeMCU ESP32 ×1 · ESP32-CAM + USB base ×1 · capacitive soil moisture ×1 · pH electrode E-201-C (+ signal board) ×1 · TDS module ×1 · 0.96" OLED ×1 · DS18B20 ×1 · DHT22 ×1 · resistor kit · 2–3 breadboards · jumpers M-M, F-M · ~4 LEDs · ~2 push buttons · power bank ×1.

## 7. Team placeholders
Members: `[Member 1 – Leader]`, `[Member 2]`, `[Member 3]`, `[Member 4]`, `[Member 5]`; Group No: `[GroupNo]`; Student IDs: `[ID]`.

## 8. Facts confirmed by Research (Lead fills after Phase 1 gate)
_Pending Phase 1._
