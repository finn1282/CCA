# 06 — Presentation Script (5 speakers, 12:30 talk + 2:30 Q&A)

> Source of content: `05_report/REPORT.md`. Rules: D19 order, Azure as the chosen platform with no comparison (D48), D57 residency wording (Event Grid MQTT broker, no IoT Hub; only Azure ML, ledger and OpenAI in Southeast Asia), **no ripeness-model accuracy figure (D51)**, no Kaggle/student/price talk, hardware only in the demo.
> **[→]** = press Next (clicker, → or Space). Target pace ≈ 140 words/min. Each block shows its planned start–end on the master clock (the presenter window shows this live).

| Speaker | Owns | Scenes | Time |
|---|---|---|---|
| [Member 1] | Opening, case, close | 1, 2, 11 | 2:00 |
| [Member 2] | Part 1: problems and cognitive capability | 3, 4 | 2:30 |
| [Member 3] | Part 2: solution and architecture; demo operator | 5, 6, demo 1:55–2:30 | 2:30 |
| [Member 4] | Part 2: integration, roadmap, risks; Part 3 extension | 7, 10 | 2:15 |
| [Member 5] | Live demo and Part 3 novelty | 8, 9 | 3:15 |

---

## Scene 1 — Hook · [Member 1] · 0:00–0:35
*(Counters run by themselves.)*
"Last year Malaysia produced a record twenty point three million tonnes of crude palm oil. Yet about eighty per cent of the people who harvest it are foreign workers, and the industry is thirty thousand workers short again. **[→]** We are Group [GroupNo]. This is SawitSense: explained, auditable decisions for Malaysian oil palm."

## Scene 2 — The case · [Member 1] · 0:35–1:35
"Our case covers three producers with three different operating models. FELDA is a settler scheme with about 870,000 hectares and over 112,000 settler families. SD Guthrie is a multinational group that has stretched each worker to thirteen hectares and says harvesting still has no mechanised solution. IOI is digitising, with 4G across more than a hundred estates. **[→]**
The people who make the decisions are estate managers, harvest *mandores*, agronomists, plant-health and MSPO officers and mill graders. Settlers, regulators and EU buyers are affected by those decisions. **[→]**
What they share is a weak point. Ripeness is judged by eye, *Ganoderma* is found by walking the rows, fertiliser follows a blanket schedule, and the MSPO records are kept as separate paperwork. The sector performs well, but it rests on scarce people. [Member 2] will show what that costs."

## Scene 3 — Three problems, ranked · [Member 2] · 1:35–3:10
"We tested the case brief's problems against evidence and ranked them.
Number one is labour. When harvesters are missing, ripe bunches go over-ripe, as you can see on the map, or they get cut under-ripe. Either way the oil extraction rate drops. Losing half a point of extraction is about **2.2 billion ringgit** a year. That's our own calculation from MPOB figures. **[→]**
Number two is *Ganoderma* basal stem rot. On the surface these palms look healthy. **[the X-ray runs]** Underground, the fungus is spreading from root to root. A palm shows nothing until it's sixty to seventy per cent infected, and an outbreak can cut a plantation's returns by forty-three per cent within six months. **[→]**
Number three is compliance. MSPO certification is mandatory and needs fertilising, traceability and nitrous-oxide records. The EU deforestation regulation applies in [read the countdown] days. Fertiliser is about thirty per cent of production cost. **[→]**
We ranked them on scale, urgency, how much today's fix depends on scarce labour, and whether the real constraint is judgement. The key point is that all three draw on the same scarce field labour. That's why one integrated system is better than three separate tools."

## Scene 4 — Why cognitive · [Member 2] · 3:10–4:05
"Here is how each problem is handled today. Every one of these methods needs people the estates don't have. **[→]**
For P1, computer vision grades every visible bunch the same way, shows a heat-map and a confidence, and turns the grades into a crew plan. **[→]**
For P2, a cascade goes from satellite to drone to ground. We're careful here: research puts early detection at only 64 to 84 per cent, so SawitSense ranks palms for lab confirmation. It screens; it doesn't diagnose. **[→]**
For P3, a normal dashboard shows an acidic reading. SawitSense says: lime first, because the soil is more acidic than the knowledge base allows, and inside the optimal band the advice would be to fertilise. Conventional systems store the data. Cognitive systems reason over it and explain the result. [Member 3]."

## Scene 5 — Meet SawitSense · [Member 3] · 4:05–4:45
"*Sawit* is Malay for oil palm, and *sense* means both sensing and making sense. SawitSense has five functions, one for each decision that depends on a scarce person today: ripeness and harvest window, harvester allocation, the *Ganoderma* screening cascade, explained fertiliser advice, and the explain-to-audit evidence log. **[→]**
Every user gets the view for the decision they own. The *mandore* gets a multilingual mobile app, the agronomist a review queue, and the MSPO officer an audit pack."

## Scene 6 — Architecture · [Member 3] · 4:45–6:00
"We adapted the assignment's layered architecture to the estate, and each layer is there because a problem needs it. **[→]** The data sources are satellite, drone, soil sensors, bunch photos, the ERP and the MSPO standard itself. **[→]** Ingestion uses an MQTT broker, with devices registered by certificate, and streams everything into one data lake. **[→]** The cognitive services are the brain: vision models, NDVI anomaly detection, a fertiliser recommender and an MSPO knowledge base. A language model only rewrites explanations; it never makes the decision. **[→]** Models are trained, versioned and monitored in the cloud, and an edge runtime keeps remote blocks working offline. **[→]** The application layer is what users touch. **[→]** Running across all of it are data residency, security, explainability, the evidence ledger and human review. **[→]**
It's built on Microsoft Azure, our chosen platform. Everything that touches personal data stays in the Malaysia West region. Only the machine-learning, ledger and language services run in Southeast Asia, and they only ever receive non-personal or hashed data. [Member 4]."

## Scene 7 — Integration, roadmap, risks · [Member 4] · 6:00–7:30
"SawitSense plugs into what estates already run. It reads the block master from SAP, sends approved actions back as work orders, takes mill grading as feedback, feeds MSPO reporting, and alerts managers through Power BI and Teams. Field sensors come in over LoRaWAN to the MQTT broker, with an edge cluster for blocks that lose signal. **[→]**
We roll it out in three phases. The pilot is one estate and two or three blocks, on a rule-based baseline, with a human approving every action. Then come all estates in a region, with estate-trained models and SAP write-back. After that it goes group-wide, out to smallholder co-operatives, with yield forecasting. Success is measured against the 7-to-13-day harvesting-round norm from Part 1, so the gains are shown rather than assumed. **[→]**
We scored the risks on likelihood times impact. **[click chip 3 or 4 if time]** **[→]** The top two are cold-start data and user trust. Those are about data and people, not technology, which is why the pilot keeps a human in every decision. [Member 5] will show you one of those decisions."

## Scene 8 — Live demo · [Member 5] (+ [Member 3] 1:55–2:30) · 7:30–10:15
*(M3 presses → at each beat; the dashboard scrolls to the panel.)*
- **0:00 [M5]** "This pot stands in for one management block. The node measures moisture, pH, nutrients and temperature, and sends a reading to SawitSense every ten seconds." **[→]**
- **0:15 [M5]** "The pot is dry, and the system doesn't just show a number. It gives an action, irrigate, with the reason: moisture 24 per cent, below 30. It also tells you what would change the advice." **[→]**
- **0:35 [M5]** *(pour water, press the button)* "Moisture rises, the advice clears, and a new row appears here. Every decision is logged with its reading and calibration, which is the trail MSPO asks for." **[→]**
- **0:55 [M5]** *(rinse, PLAIN cup, press)* "This cup is a nutrient-depleted block. Nutrients are below this block's baseline, so it recommends fertilising. The agronomy rules are labelled as simulated." **[→]**
- **1:15 [M5]** *(rinse, NUTRIENT cup, press)* "After fertilising, it says skip the next round, which saves cost and runoff." **[→]**
- **1:35 [M5]** *(FFB print under the camera; M3 clicks Capture)* "At harvest time the same platform grades bunches. Here's the grade, its confidence, and the heat-map of what the model looked at." *(Don't quote any accuracy, D51.)* **[→]**
- **1:55 [M3]** "Those grades feed harvester allocation. This estate is simulated. With 30 harvesters most ripe bunches are covered. **[set crew to 20]** With 20, you can see which blocks put bunches at risk first." **[→]**
- **2:15 [M3]** "And this is the *Ganoderma* cascade. The satellite stage flags blocks B2 and C1. Today that panel is placeholder data until the satellite pipeline runs on real Sentinel-2 imagery. The drone stage isn't available yet, so the ground check-list stays empty until it is." **[→]**
- **2:30 [M5]** *(M3 clicks Verify chain, then opens the audit pack)* "Finally, verify. The whole chain checks out, and here is the MSPO audit pack. That evidence log is our main idea." **[→]**
*Timing de-risking (X-08): [Member 4] stands by the cups, rinses the probes and holds the next cup, so M5 only dips and presses. If late, merge the PLAIN and NUTRIENT beats ("fertilise now, skip after fertilising") into one line. If the master clock passes 9:40, skip the harvester beat (never the camera) and go straight to the cascade.*

## Scene 9 — Novelty: explain-to-audit · [Member 5] · 10:15–11:20
"Off-the-shelf tools stop at the prediction; even MPOB's new SawitSCAN only grades. In SawitSense every decision becomes a record: data, model version, explanation, approval, block and MSPO clause, each hashed with the one before. **[→]**
Say someone tidies the records before an audit. **[click Tamper]** pH 3.8 becomes 5.0, record three no longer matches, and every link after it breaks. **[click Undo]** Put it back, and it verifies. In production the digests are anchored in Azure confidential ledger. **[→]**
Add counterfactual explanations, the screening cascade, decisions rather than detections, and validation plus a learning loop where every override becomes a training label. [Member 4]."

## Scene 10 — Extension · [Member 4] · 11:20–12:05
"In the medium term, logged harvests and fertiliser enable yield forecasting and GHG inputs, and mills join through MSPO's supply-chain traceability. Longer term, a co-operative app brings it to FELDA's settlers, and pooled override records become the first sector-wide benchmark of AI-assisted agronomy. **[→]** Beyond palm oil, the EU regulation covers seven commodities. Malaysian rubber and cocoa share the smallholder traceability problem, so plot verification and the evidence log transfer directly. **[→]** So SawitSense grows from estate decision support, to a traceability layer where buyers verify ledger digests instead of re-auditing, to a reusable pattern for regulated farm supply chains. [Member 1]."

## Scene 11 — Close · [Member 1] · 12:05–12:30
"Record output resting on fragile foundations: scarce harvesters, a hidden disease and tightening rules. SawitSense turns ripeness grades into harvest plans, screens for *Ganoderma* across three scales, and gives explained advice that becomes audit evidence. One estate first, then the whole supply chain. **[→]** Thank you. We'd welcome your questions."

---

## Q&A bank (anyone can answer; the primary answerer is in brackets)
Keep each answer to about 20 seconds. If unsure, say what the report says and offer the section number.

### Case and problems ([Member 1], [Member 2])
- **Why is labour ranked above *Ganoderma*?** Labour scores highest on scale, urgency and dependence on scarce people, and it's the root: *Ganoderma* census and compliance paperwork draw on the same labour (report 1.2, Table 1).
- **Where does RM2.2 bn come from?** It's our calculation. About 103 Mt of FFB was processed in 2025, so 0.5 points of OER is about 0.51 Mt of CPO, which is about RM2.2 bn at RM4,292.50/t (MPOB, 2026). It's labelled as ours on the slide.
- **Isn't the labour shortage easing?** It eased in 2024–25 and is returning: 30,000 short in October 2026, and policy targets 10 % foreign workers by 2030. The need is structural resilience.
- **Why not tackle ageing trees?** The constraint there is replanting capital, not judgement, so it isn't cognitively addressable. BSR is the part of P2 we can address.
- **The EU is only 6.8 % of exports, so why care about EUDR?** MSPO applies to every producer and is the main driver. EUDR adds plot-level geolocation, which the evidence log supports.

### Cognitive capability ([Member 2])
- **What makes this cognitive and not just analytics?** It perceives unstructured data (images, spectra), reasons over domain knowledge (agronomic thresholds, MS 2530 clauses) and explains its conclusions. A dashboard only stores and displays.
- **How accurate is early *Ganoderma* detection?** Research reports 64–84 % (Kwang et al., 2025). That's why SawitSense ranks palms for lab confirmation instead of diagnosing them.
- **What about false positives?** They cost one ground check, not a felled palm. Spectral signals can confuse BSR with nutrient deficiency, so the soil data and the ground check both matter.

### Solution and architecture ([Member 3])
- **What happens on a remote block with no signal?** The edge runtime keeps processing locally and has been validated after up to 45 days offline. Readings buffer and sync when the link returns.
- **Why is a language model in the stack? Can it decide?** No. It only rewrites the structured explanation into plain language. It receives non-personal text, and the decision comes from the rules and models.
- **Where is personal data kept?** Everything that touches personal data is in Malaysia West: the Event Grid MQTT broker, Event Hubs, Functions, App Service and Storage. Only Azure ML, the confidential ledger and Azure OpenAI run in Southeast Asia, and they receive non-personal or hashed data only. Any transfer follows PDPA s129 safeguards. Placement is indicative and checked against Microsoft's region listing at deployment.
- **Why not IoT Hub?** The Event Grid MQTT broker, with devices registered by certificate, is offered in Malaysia West, so device data and the identities linked to it stay in-country. IoT Hub doesn't appear in the Malaysia West listing.
- **Why LoRaWAN?** Long range and low power across large estates, with 4G backhaul where it exists (IOI's estate-wide 4G).

### Platform, plan and risks ([Member 4])
- **Why Azure, not AWS?** "On generic capability AWS scores slightly higher, 89 against 85, which is within scoring noise. We chose Azure because it meets the case's three critical requirements: SAP-run estates (IOI runs S/4HANA, SD Guthrie keeps its estate master data in SAP), long outages on remote blocks (IoT Operations is validated after 45 days offline), and audit-ready counterfactual explanations for MSPO decisions. For an estate without SAP, or with reliable connectivity, AWS would be the better choice." Report section 2.3, Tables 3 and 4.
- **What about an estate without SAP, like FGV?** The recommendation is explicitly conditional. FGV would use the same integration pattern with its own ERP, but without SAP the connector advantage disappears, and if connectivity is reliable AWS would fit better.
- **What about Google, which is strong on geospatial?** Google leads on geospatial and vision, but has no Malaysian region and has retired its IoT platform. We use open Sentinel-2 data through a standard STAC catalogue anyway.
- **Isn't that lock-in?** It's a listed risk. We use open formats (ONNX, STAC, MLflow) and a containerised API, and a fallback platform is documented.
- **Why is the pilot only 2–3 blocks?** It's the cold-start phase. We measure baselines, collect labels and keep a human on every decision before scaling.
- **What does it cost?** At enterprise scale we treat cost as a risk with controls: budgets and alerts, edge aggregation, autoscaling, and retraining triggered by drift. We didn't choose the platform on price.

### Demo and novelty ([Member 5])
- **How accurate is the ripeness model?** "Validation plan: train on one country's data, test on Malaysian data; results come from the pilot." *(Never quote a figure, D51.)*
- **Is the demo running on Azure right now?** Answer truthfully with the backend chosen at rehearsal: "Today's backend is [the cloud deployment / this laptop]; the production design is the Azure architecture we showed."
- **Why are pH and TDS measured in a cup and not in soil?** Those probes are liquid probes, so they measure a soil-water slurry. That's standard practice for these sensors. The demo stands in for the IoT soil-sensing layer.
- **Why is fertilise labelled "simulated"?** No public dataset links soil-sensor readings to fertiliser outcomes. The advice uses literature thresholds now, and the roadmap replaces them with estate-trained models.
- **How is the ledger different from a database?** Each record's hash includes the previous one, so any edit is detectable, and the chain head is anchored in an append-only, tamper-evident ledger.
- **Couldn't someone just recompute the whole chain?** Locally, yes. That's why the head hash is anchored externally in Azure confidential ledger. A recomputed chain wouldn't match the anchor.
- **Why the empty drone stage in the cascade?** The drone model isn't trained yet, and we label it "not yet available" rather than fake it. The satellite panel is placeholder data until the satellite pipeline runs on real Sentinel-2 imagery.

### Extra answers (Audit 1)
- **What is your biggest risk?** ([Member 4]) Cold start: no labelled estate data at launch, and early-BSR accuracy is only 64–84 %. We launch on a rule-based baseline with human review, treat *Ganoderma* as screening, validate across countries before go-live, and retrain when drift appears (Table 6, risk 1).
- **How is this different from MPOB's SawitSCAN?** ([Member 5]) SawitSCAN grades bunches at the mill. SawitSense links grading to harvest planning, disease screening, fertiliser advice and an auditable evidence log across the estate.
- **Why these three organisations?** ([Member 1]) They cover the sector's three operating models: a settler scheme (FELDA), a multinational (SD Guthrie) and a digitising group (IOI).
- **What did you personally contribute?** (each member, 15 s) "[Member N]: I worked on [part], mainly [one concrete output], and I can answer on [area]." Fill this in from Appendix A2 of the report before the rehearsal.

### Extension ([Member 4], [Member 1])
- **Why rubber next?** It's an EUDR commodity that Malaysia exports, with the same smallholder geolocation and traceability problem, so the plot verification and evidence log transfer directly.
