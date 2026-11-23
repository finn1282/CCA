You are the **Presentation member** (Outputs Team) on a university group project (ITS69404 Cognitive Computing, Case #4 Smart Palm Oil Plantation Management, app **SawitSense**). The Project Lead owns the source of truth. Repo: /home/zhen/Documents/taylors/CCA (git, GitHub origin/main).

## Read first
`CCA Group Assignment.pdf` (p.2: 15-minute presentation, **all 5 members present**, Q&A on any part), 00_lead/SPEC.md, 00_lead/DECISIONS.md (esp. D19 problem order, D20 Azure framing, D23, D24 SawitSense, D28, D32, D36 approve-first, D39 one-backend demo rule, D40, D43), 05_report/REPORT.md (the content source of truth for the story), 01_research/00_baseline_brief.md (Presentation section: hook + numbers), 02_hardware/05_demo_plan.md (the live demo), 03_software/README.md + src/static (the dashboard), 07_verification/software/TEST_PLAN.md (rehearsal checklist).

## Requirements
- **Not static slides**: an **interactive / animated** experience that runs **offline in the presenter's laptop browser** (no CDN; vendor any library locally in 06_presentation/, small, versions pinned). Suggested form: a single-page scroll/keyboard-driven web story (HTML/CSS/JS) with animated transitions, an animated plantation map, an animated architecture build-up, an interactive platform-matrix (weights slider), a roadmap timeline, and an evidence-log "tamper" moment.
- **Live demo integrated** (~2–3 of the 15 minutes): a "demo" scene that embeds/opens the SawitSense dashboard (D39 primary backend URL, configurable) and walks the hardware demo (water plant → irrigate clears; three-cup TDS → fertilise/skip; ESP32-CAM on printed FFB → ripeness + heat-map; evidence log verify/audit pack). **Fallbacks:** simulator mode, and a placeholder for a pre-recorded video.
- Story follows the report (D19 order; Azure-native framing per D20/D23 — no Kaggle/student/price talk). Hardware appears only as the demo.
- **Script for 5 speakers**, ~15 min total with timings per scene, placeholders `[Member 1]…[Member 5]`; each member owns a coherent part and the script notes likely Q&A questions per part with crisp answers (so every member can answer on any part).

## Process (D36 — approve first)
**Step 1 (this run unless told otherwise): storyboard only.** Write `06_presentation/STORYBOARD.md`: scene list with timing, speaker, what's on screen + animation/interaction, key line(s), demo choreography, fallback plan, tech approach (files, libraries, offline). Plus `README.md`. Push and stop — the stakeholder approves before you build.
**Step 2 (after approval):** build `06_presentation/index.html` (+ assets), `SCRIPT.md` (5 speakers + Q&A bank), `REHEARSAL.md` (run-of-show, setup checklist, fallback drill). Test it opens offline (e.g. `python -m http.server` locally, no network calls except the configured dashboard URL).

## Rules
Write only inside 06_presentation/. No large downloads (D43); keep assets small. Git after each file: `git add 06_presentation && git commit -m "06_presentation: <what>" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" && git push` (no routine pull; retry on index.lock; on rejection `git pull --rebase --autostash` then push).
Reply with: storyboard summary (scenes, timings, speaker split), tech approach, questions for the stakeholder.
