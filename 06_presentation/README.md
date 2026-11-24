# 06_presentation — README

## Status (24 Nov 2026)
| Step | State |
|---|---|
| Step 1: storyboard | Approved with changes (D48); `STORYBOARD.md` v3 records the changes (D48, D51, D57, Audit 1) |
| Step 2: build | **Done**: interactive presentation, `SCRIPT.md`, `REHEARSAL.md` |

## What this is
The 15-minute group presentation for SawitSense (Case #4): a **12:30 interactive, animated web story** plus 2:30 of Q&A. It runs **offline** in Chrome, uses a palm-plantation theme, and has a live-demo scene that embeds the SawitSense dashboard. Fallbacks: laptop backend (F), new tab (O) and simulator (S).

## How to run
```bash
cd 06_presentation && python -m http.server 8080      # open http://localhost:8080/  (file:// also works)
```
- Set the demo backend in `config.js`: `DASHBOARD_URL` is the primary chosen at the rehearsal (D39), `FALLBACK_URL` is the laptop.
- For rehearsals you can override the primary with `http://localhost:8080/?dash=http://localhost:8000`.
- A cloud admin token goes only in the git-ignored `config.local.js` (`window.SAWIT_LOCAL = { token: "…" };`).
- Keys: → / Space next, ← back, `P` presenter window, `T` daylight theme, `B` black screen, `1`–`9`/`0`/`-` jump to a scene. Full list in `REHEARSAL.md` §3.

## Files
| Path | Content |
|---|---|
| `index.html` | 11 scenes (markup) |
| `presenter.html` | Presenter view: cues per step, talk clock vs plan, scene timer, time left in the slot |
| `config.js` | Dashboard URLs, simulator command, health-check interval |
| `css/style.css` | Plantation theme (estate greens, FFB orange/red, soil browns, frond motif) + daylight variant |
| `js/data.js` | Scene timings, speakers, cues, demo beats, report figures (risks, estate blocks, evidence records) |
| `js/main.js` | Scene engine, keyboard, estate map, architecture, risks, demo embed + fallbacks, evidence chain, presenter sync |
| `js/sha256.js` | Own SHA-256 implementation (self-tested at load) |
| `STORYBOARD.md` | Approved storyboard v2 + changelog |
| `SCRIPT.md` | Word-for-word script for 5 speakers with timings + Q&A bank |
| `REHEARSAL.md` | Run-of-show, D39 one-backend rule, setup checklist, fallback drill, visual check list |

No third-party libraries, no CDN, no web fonts. The only network calls go to the configured dashboard (iframe + `/api/v1/health`). The folder is well under 1 MB.

## Rules followed
D19 problem order · Azure as the chosen platform with no comparison (D48) · D57 residency wording (Event Grid MQTT, no IoT Hub) · no ripeness-model accuracy figure (D51) · no Kaggle/student/price talk (D20/D23) · hardware only in the demo · Harvard in-text citations on every scene (D11) · no large downloads (D43) · browser checks limited to our own localhost pages (D52/D53).

## Open issues for Lead
- If the platform decision or the report's figures change, update `js/data.js` (cues, risks) and scene 6 in `index.html`. Service names live only in scene 6, its cues, and `SCRIPT.md`.
- The demo cascade panel shows placeholder satellite data and "Drone screening not yet available" until the satellite pipeline runs on real Sentinel-2 imagery and the drone model exists. The script says so on stage.
