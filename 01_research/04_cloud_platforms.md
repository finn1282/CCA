# 04 — Cloud Platforms: Student Credits (what we use) and Enterprise Comparison (what we recommend)

> Owner: Research. Audience: Software & Cloud AI (part a), Report/Presentation (part b). Official pages opened 23 Nov 2026. Keys → `sources.md`.

## Headline
- **Train on:** **Kaggle Notebooks (free GPU)**, Colab as backup. **Deploy on:** **Azure for Students** ($100, no credit card) — inference API + dashboard + IoT ingestion. **Satellite pre-compute:** **Google Earth Engine** (free for academic/noncommercial use).
- **Recommend in the report (enterprise):** **Microsoft Azure (Azure Machine Learning + Azure IoT Hub/IoT Operations, Malaysia West region)** — weighted score 83/100 vs AWS 78, Google 68, IBM 49.
- The two choices are consistent (both Azure), so the demo is a scaled-down version of the recommended architecture — a strong presentation point.

---

## Part (a) — Credits a Malaysian university student can actually get (Nov 2026)

| Platform / offer | Credit | Card needed? | Eligibility from Malaysia | GPU access | Expiry | Gotchas (verified unless marked) |
|---|---|---|---|---|---|---|
| **Azure for Students** [AZ-STUDENT] | **USD 100** + 12 months of free-tier services (incl. Azure Machine Learning, Functions, 750 h burstable VM) + 65 always-free services | **No** | Full-time university students, sign-up with school email; no country exclusion stated | **Effectively none**: Azure for Students is **not eligible for quota increases**; GPU VM families need quota → upgrade to pay-as-you-go required [MSQA-GPU] | Credit within 12 months; renewable yearly while a student | Must verify Taylor's email is accepted (unverified). When credit ends, subscription is disabled unless upgraded. **Malaysia West** region available [AZ-REGIONS]. |
| **Google Cloud Free Trial** [GCP-TRIAL] | **USD 300** for 90 days | **Yes** (card or other payment method; temporary auth hold) | Anyone not previously a paying GCP customer | **No GPUs on Free Trial** VMs; no quota increases | 90 days | **Critical: for sign-ups/upgrades on or after 16 Nov 2026 the $300 credit cannot pay for "Gemini platform" (formerly Vertex AI)** nor Gemini API → useless for Vertex training for us [GCP-TRIAL]. |
| **Google Cloud education credits** [GCP-EDU] | Faculty USD 100; **students up to USD 50** | **No** | Only via a **faculty member's** application, students redeem coupon with school email | Depends on project quota (unverified) | Per coupon | Needs lecturer to apply — ask stakeholder (open issue). |
| **Google Earth Engine (noncommercial)** [GEE-NONCOM] | Free | No (needs a registered Cloud project; billing not stated on page) | Students/academics for research or teaching | n/a (server-side compute) | — | No fee-for-service use. Best tool for Sentinel-2 NDVI pre-computation. |
| **AWS Free Tier (2025+ model)** [AWS-FREE] | USD 100 on sign-up + up to USD 100 more by exploring services; "Free plan" | Page does not say; AWS sign-up normally asks for a payment method (**unverified**) | Open | Free plan limited to select services; GPU not mentioned | Account closes after **6 months** or when credits run out (Free plan) | SageMaker listed but no free-tier detail on page. |
| **SageMaker Studio Lab** [AWS-STUDIOLAB] | Free (GPU 4 h/session, **4 h per 24 h**; CPU 8 h/24 h; 15 GB storage) | No | — | Yes (limited) | — | **"No longer open to new customers"** → **not available to us**. |
| **IBM watsonx.ai Lite** [IBM-WXPLANS] | Free: Runtime **20 CUH/month**, 300k foundation-model tokens/month, 2 req/s | Not stated (IBM Cloud account) | Open; academic access via IBM SkillsBuild only for *selected* universities (unverified for Taylor's) | Not stated | Monthly | Too small for CNN training; Standard plan is USD 1,110/month incl. 2,500 CUH. |
| **Google Colab (free)** [COLAB-FAQ] | Free | No | Open | GPU **not guaranteed**, limits fluctuate and are unpublished | Session ≤ **12 h**, idle timeouts | Fine for fine-tuning a small CNN; save checkpoints to Drive. |
| **Kaggle Notebooks** | Free | No (phone verification required for GPU — commonly reported, **unverified**) | Open | ~30 GPU h/week, P100 or 2×T4 (**unverified** — docs page not machine-readable) | Weekly reset | Datasets D1–D6 can be attached directly; good for reproducible notebooks. |

### Decision for the team (training/deployment within credits)
1. **Model training → Kaggle (primary) / Colab (backup).** Free GPUs, no card, enough for transfer learning on D1 (4.7k images) and YOLOv8n on D4 (1.35k tiles). No cloud vendor's student credit gives GPU access without a card/upgrade (Azure quota, GCP trial, AWS Studio Lab closed).
2. **Deployment → Azure for Students.** CPU inference for a MobileNet/YOLOv8n-sized model is adequate for a live demo. Suggested services (Software to finalise): Azure Container Apps or App Service (API + dashboard), Azure IoT Hub (free tier) or plain HTTPS for the ESP32 payload, Blob Storage for images. Region: **Malaysia West** (data residency story).
3. **Satellite → Google Earth Engine** (noncommercial) pre-computes NDVI anomaly maps; exported PNG/GeoJSON is served from Azure. No live GEE dependency during the presentation.
4. **Fallback (D4 in DECISIONS):** if Azure sign-up fails, deploy the API on a free container host or run it locally on the presenting laptop; training is unaffected.

---

## Part (b) — Enterprise platform comparison (report Part 2, 5 marks)

### Platform facts relevant to this case

| Criterion | Microsoft Azure | AWS | Google Cloud | IBM watsonx |
|---|---|---|---|---|
| **In-country region (PDPA 2010 data residency, latency to estates)** | **Malaysia West (Kuala Lumpur), 3 AZs, live**; second region "Southeast Asia 3" (Senai, Johor) in preview [AZ-REGIONS] | **Asia Pacific (Malaysia) region, live since 21 Aug 2024, 3 AZs**, USD 6.2 bn investment to 2038 [AWS-MYREGION] | **No Malaysian region live**: compute region list shows Singapore, Jakarta, Bangkok only [GCP-REGIONS]; Malaysian region under construction since Oct 2024 groundbreaking [GCP-MY2024] | watsonx data centres: Dallas, Frankfurt, London, Tokyo, Sydney, Toronto (per IBM docs search results — **unverified**); no SE Asia region |
| **IoT ingestion & device management** | **Azure IoT Hub + DPS + Device Registry is Microsoft's recommended path**; IoT Central closed to new apps from 23 Sep 2026, retires 20 Sep 2029 [AZ-IOTC2026] | **AWS IoT Core active** (managed MQTT 3/5 broker, rules) [AWS-IOTCORE]; AWS IoT Analytics discontinued (end of support reported 15 Dec 2025; docs now 404 — **unverified detail**) | **Cloud IoT Core retired 16 Aug 2023** [GCP-IOTCORE]; must use Pub/Sub + partner IoT platform | **Watson IoT Platform retired 1 Dec 2023 "without a direct replacement"** [REG-WIOT] |
| **Geospatial / satellite** | Planetary Computer data catalog (Sentinel-2 L2A via STAC); Planetary Computer Pro announced in public preview May 2025 (GA unverified) | Open-data registry / SageMaker (not opened — unverified) | **Earth Engine**: multi-petabyte catalog incl. Sentinel-2 L2A (10 m, 5-day) and Landsat [GEE-S2] [GEE-L9]; widely used for oil-palm mapping, e.g. global oil-palm map [GEE-OILPALM] | No comparable first-party satellite catalog found |
| **Vision AutoML / custom training** | Azure ML AutoML for images + custom training (vendor docs not opened) | SageMaker training/JumpStart (not opened) | AutoML image classification/detection training **USD 3.465 per hour**; product renamed **"Gemini platform"**, formerly Vertex AI [GCP-PRICING] | AutoAI (tabular focus); vision weaker (unverified) |
| **Edge deployment (offline estates)** | IoT Edge / Azure IoT Operations (edge-to-cloud, major release 2603 announced 2026 — per Microsoft blog search results, unverified) | IoT Greengrass (not opened) | Limited after IoT Core retirement | Limited |
| **MLOps, explainability, governance** | Azure ML pipelines, Responsible AI dashboard (not opened) | SageMaker Pipelines, Clarify (not opened) | Vertex pipelines, Explainable AI (not opened) | **watsonx.governance** is IBM's flagship strength (not opened) |
| **Student / pilot cost entry** | $100 no-card student credit; GPU blocked | Card + 6-month free plan | Card; trial credit excludes Gemini platform (Vertex) from 16 Nov 2026 | Lite plan tiny; Standard $1,110/month |

### Weighted scoring matrix (1 = poor, 5 = excellent)

Weights reflect the Part 1 problems: three data streams (satellite, drone, IoT) + Malaysian estates (residency, connectivity) + explainable recommendations for MSPO audits.

| Criterion (weight) | Why it matters for the case | Azure | AWS | Google | IBM |
|---|---|---|---|---|---|
| IoT ingestion & device mgmt (15) | Soil-sensor network across blocks (O3) | 5 | 4 | 2 | 1 |
| Malaysian region / PDPA residency (15) | Estate, worker & smallholder geolocation data; MSPO/EUDR traceability records | 5 | 5 | 2 | 1 |
| Vision AutoML / custom training (15) | FFB ripeness + Ganoderma models (O1, O2) | 4 | 4 | 5 | 3 |
| Geospatial / satellite (15) | NDVI time series, block mapping, EUDR geolocation (O2, O4) | 3 | 3 | 5 | 2 |
| Edge / offline (10) | Remote estates with patchy coverage (IOI only recently rolled out estate-wide 4G [IOI2026]) | 5 | 5 | 2 | 2 |
| MLOps & explainability (10) | Agronomists must trust and audit recommendations | 4 | 4 | 4 | 5 |
| Cost & pilot accessibility (10) | Pilot on one estate; student build | 4 | 2 | 2 | 3 |
| Integration with enterprise IT (10) | Plantation ERP/office stack (Microsoft 365/Power BI common in Malaysian corporates — assumption, unverified) | 4 | 3 | 3 | 3 |
| **Weighted total /100** | | **83** | **78** | **68** | **49** |

(Total = Σ score × weight ÷ 5.)

### Recommendation
- **Enterprise (report): Microsoft Azure.** It is the only platform of the four that combines (1) a **live in-country Malaysian region** (with a second one coming in Johor, the heart of palm country) and (2) a **live, first-party IoT device platform with edge runtime** — Google retired IoT Core (2023) and IBM retired Watson IoT (2023) with no replacement, while AWS lacks the student-accessible entry and scores slightly lower on integration. Its weakness (geospatial) is mitigated by ingesting open Sentinel-2 data (Planetary Computer catalog or exports from Earth Engine), so the satellite pipeline does not depend on the platform choice.
- **Runner-up: AWS** (Malaysian region + IoT Core + Greengrass). Choose AWS if the plantation already runs on AWS — mention as the vendor-lock-in mitigation.
- **Google** is the best *geospatial and AutoML* platform but is disqualified as the single enterprise platform by no Malaysian region and no first-party IoT service; we still use **Earth Engine as a data source**.
- **IBM watsonx** offers strong governance, but no SE-Asian region, no IoT platform and small free tier make it the weakest fit.

### PDPA 2010 note (only where it constrains integration)
Worker/smallholder personal data (names, IC numbers, plot geolocation linked to individuals) falls under PDPA 2010 → prefer in-country hosting (Azure Malaysia West) and keep personal identifiers out of the ML datasets. Detailed PDPA analysis is out of scope (MLO2) — **PDPA text not opened by Research; Report should cite the Act directly if used**.
