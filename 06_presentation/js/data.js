// SawitSense presentation: shared data (scenes, timings, cues, figures).
// Figures are copied from 05_report/REPORT.md (Tables 1, 4, 5; sections 1.1-3.2). Update them here only.
window.SAWIT = {};

// Talk = 12:30 (D48). Q&A fills 12:30-15:00. dur in seconds; start is computed.
SAWIT.SCENES = [
  { id: "hook", title: "Record harvest, missing harvesters", speaker: "[Member 1]", dur: 35,
    cues: ["Let the three counters run. Say the hook line slowly.",
           "Title appears: introduce SawitSense and the team in one sentence."] },
  { id: "case", title: "The case: FELDA, SD Guthrie, IOI", speaker: "[Member 1]", dur: 60,
    cues: ["Three operating models: settler scheme, multinational, digitising group.",
           "Who uses it and who is affected.",
           "Same weak point everywhere: manual decisions, records kept apart. Hand over to [Member 2]."] },
  { id: "problems", title: "Three problems, ranked", speaker: "[Member 2]", dur: 95,
    cues: ["P1: ripe bunches go over-ripe because harvesters are missing. RM2.2 bn per 0.5 OER point (our calculation).",
           "P2: press for the X-ray. Ganoderma is invisible until 60-70 % infected; -43 % in 6 months.",
           "P3: MSPO records + EUDR from 30 Dec 2026; fertiliser is ~30 % of cost.",
           "Ranking: four criteria, P1 > P2 > P3. They share the same scarce labour."] },
  { id: "cognitive", title: "Why cognitive, not conventional", speaker: "[Member 2]", dur: 55,
    cues: ["Conventional methods on the left: all need scarce people.",
           "P1 flips: computer vision + harvest window + crew optimisation.",
           "P2 flips: satellite -> drone -> ground screening. Screening, not diagnosis (64-84 %).",
           "P3 flips: reasoning + explanation. Read the counterfactual aloud. Hand over to [Member 3]."] },
  { id: "sawitsense", title: "Meet SawitSense", speaker: "[Member 3]", dur: 40,
    cues: ["Sawit = oil palm; sense = sensing and sense-making. Five functions, one per decision.",
           "The users: each gets the view they need."] },
  { id: "architecture", title: "Architecture", speaker: "[Member 3]", dur: 75,
    cues: ["The layers build from the bottom up. Press once per layer.",
           "1 Data sources: satellite, drone, soil sensors, bunch photos, ERP, MSPO standard.",
           "2 Ingestion and big data.",
           "3 Cognitive services: the brain.",
           "4 Cloud and deployment, including the edge for offline blocks.",
           "5 Applications: what each user touches.",
           "Cross-cutting: residency, security, explainability, evidence log, human review.",
           "Built on Microsoft Azure, our chosen platform. Personal data stays in Malaysia West. Hand over to [Member 4]."] },
  { id: "roadmap", title: "Integration, roadmap and risks", speaker: "[Member 4]", dur: 90,
    cues: ["Integration: SAP ERP, mill grading, MSPO reporting, field data.",
           "Roadmap: pilot -> scale and integrate -> optimise and extend. Measure a baseline first.",
           "Risks on likelihood x impact. Click a chip to show its mitigation.",
           "Top two risks are data and people, so a human approves every decision in the pilot. Hand over to [Member 5]: 'let's show you one'."] },
  { id: "demo", title: "Live demo", speaker: "[Member 5] + [Member 3]", dur: 165,
    cues: ["[M5] 0:00 Pot = one block. Node sends moisture, pH, nutrients, temperature every 10 s.",
           "[M5] 0:15 Pot is dry: red IRRIGATE, reason + counterfactual.",
           "[M5] 0:35 Pour ~100 mL, press send. Green OK + new evidence row.",
           "[M5] 0:55 Probes to PLAIN cup, press send: amber FERTILISE (simulated agronomy).",
           "[M5] 1:15 Probes to NUTRIENT cup, press send: SKIP FERTILISER, saving cost and runoff.",
           "[M5] 1:35 FFB print under the camera; [M3] clicks Capture. Label, confidence, heat-map.",
           "[M3] 1:55 Harvester allocation (SIMULATED estate): set crew 30 -> 20, bunches at risk rise.",
           "[M3] 2:15 Screening cascade: satellite flags B2 and C1 (placeholder data), drone stage not yet available, so the ground list waits on it.",
           "[M5] 2:30 Verify chain -> VERIFIED; open the MSPO audit pack. 'And that becomes evidence.'"] },
  { id: "novelty", title: "Novelty: explain-to-audit", speaker: "[Member 5]", dur: 65,
    cues: ["Every decision is a record: data, model, explanation, counterfactual, approval, block, MSPO clause. Each record is hashed and chained.",
           "Click 'Tamper' (pH 3.8 -> 5.0). The chain breaks from record 3. Then Undo: VERIFIED.",
           "Five things off-the-shelf tools don't do, plus what it measures. Hand over to [Member 4]."] },
  { id: "extension", title: "Extension", speaker: "[Member 4]", dur: 45,
    cues: ["Inside the organisation: FELDA settlers via a co-operative app; yield forecasting and N2O accounting.",
           "Other sectors: EUDR's seven commodities; rubber is next.",
           "Evolution: estate tool -> shared traceability layer -> reusable pattern. Hand over to [Member 1]."] },
  { id: "close", title: "Close", speaker: "[Member 1]", dur: 25,
    cues: ["The hook numbers return with the SawitSense answers.",
           "Closing line, then 'Questions?' Q&A runs to 15:00."] }
];
(function () { let t = 0; for (const s of SAWIT.SCENES) { s.start = t; t += s.dur; } SAWIT.TALK_S = t; })();
SAWIT.SLOT_S = 15 * 60;

SAWIT.fmt = function (s) {
  const neg = s < 0; s = Math.abs(Math.round(s));
  return (neg ? "-" : "") + Math.floor(s / 60) + ":" + String(s % 60).padStart(2, "0");
};

// Demo estate (SIMULATED), mirrors 03_software/src/static/precomputed/estate_blocks.json
SAWIT.BLOCKS = [
  { id: "A1", over: 0.07, ripe: 690, z: -0.61 }, { id: "A2", over: 0.21, ripe: 292, z: -0.64 },
  { id: "A3", over: 0.08, ripe: 376, z: -1.04 }, { id: "B1", over: 0.25, ripe: 529, z: -0.61 },
  { id: "B2", over: 0.06, ripe: 375, z: -2.10 }, { id: "B3", over: 0.03, ripe: 277, z: -0.37 },
  { id: "C1", over: 0.14, ripe: 556, z: -1.58 }, { id: "C2", over: 0.06, ripe: 208, z: -0.93 }
];

// Demo beats: which dashboard panel each beat scrolls to (ids from 03_software/src/static/index.html)
SAWIT.DEMO_BEATS = [
  { t: "0:00", who: "M5", label: "Soil node: live readings", panel: "soil-card" },
  { t: "0:15", who: "M5", label: "Dry pot: IRRIGATE + reason", panel: "rec-card" },
  { t: "0:35", who: "M5", label: "Water: OK + evidence row", panel: "ev-card" },
  { t: "0:55", who: "M5", label: "PLAIN cup: FERTILISE", panel: "rec-card" },
  { t: "1:15", who: "M5", label: "NUTRIENT cup: SKIP", panel: "rec-card" },
  { t: "1:35", who: "M5", label: "Camera: ripeness + heat-map", panel: "cam-card" },
  { t: "1:55", who: "M3", label: "Harvester allocation", panel: "harvest-card" },
  { t: "2:15", who: "M3", label: "Screening cascade", panel: "cascade-card" },
  { t: "2:30", who: "M5", label: "Verify chain + audit pack", panel: "ev-card" }
];

// Evidence chain for the tamper moment (illustrative records; same scheme as evidence.py: sha256(prev + body))
SAWIT.CHAIN = [
  { id: "EV-0101", block: "B2", decision: "IRRIGATE", reason: "moisture 24 % < 30 %", cf: "OK at moisture >= 30 %", approval: "approved: agronomist", clause: "MS 2530 4.5.5" },
  { id: "EV-0102", block: "B2", decision: "FERTILISE", reason: "nutrients 0.6 x block baseline", cf: "skip at >= 1.3 x baseline", approval: "approved: agronomist", clause: "MS 2530 4.1.3.1" },
  { id: "EV-0103", block: "C1", decision: "LIME NOW", reason: "pH 3.8 < 4.0", cf: "fertilise at pH >= 4.2", approval: "approved: agronomist", clause: "MS 2530 4.1.3.1", editable: true },
  { id: "EV-0104", block: "C1", decision: "HARVEST: RIPE", reason: "ripeness grade + heat-map reviewed", cf: "re-check in 3 days if under-ripe", approval: "approved: mandore", clause: "MS 2530 4.1.3.1" },
  { id: "EV-0105", block: "B2", decision: "GROUND CHECK", reason: "NDVI z -2.1; neighbour of confirmed palm", cf: "no check if z > -1.5", approval: "override: re-check in 30 days", clause: "MS 2530 4.1.3.5" }
];

// Table 5 (report 2.5): prioritised risks
SAWIT.RISKS = [
  { n: 1, cat: "tech", L: 3, I: 3, risk: "Cold start: no labelled estate data; early-BSR accuracy only 64-84 %", mit: "Launch on a rule-based agronomic baseline with human review; Ganoderma as screening with ground confirmation; validate across countries; retrain on drift", owner: "Data science lead" },
  { n: 2, cat: "ops", L: 3, I: 2, risk: "Low adoption and trust in a largely foreign, mixed-literacy workforce", mit: "Multilingual counterfactual explanations; one-tap approve/override; mandore champions; paper fallback in pilot", owner: "Estate manager" },
  { n: 3, cat: "tech", L: 2, I: 3, risk: "Legacy SAP customisation; weak coverage on remote blocks", mit: "Read-only integration first, write-back in phase 2; block-master clean-up; edge buffering with local rules", owner: "IT lead" },
  { n: 4, cat: "vendor", L: 2, I: 2, risk: "Platform lock-in", mit: "Open formats (ONNX, STAC, Kafka protocol, MLflow); containerised API; documented fallback platform", owner: "Architecture board" },
  { n: 5, cat: "vendor", L: 2, I: 2, risk: "Enterprise spend growth (GPU training, endpoints, messages)", mit: "Budgets and alerts; edge aggregation; scheduled autoscale; drift-triggered retraining; quarterly FinOps review", owner: "Finance and IT" },
  { n: 6, cat: "vendor", L: 2, I: 2, risk: "Services not offered in Malaysia West; PDPA cross-border transfer", mit: "Residency split, only non-personal data offshore; template text if the LLM is unavailable; DPO sign-off before phase 2", owner: "Data protection officer" }
];
