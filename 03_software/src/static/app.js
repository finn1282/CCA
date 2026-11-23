// SawitSense dashboard — vanilla JS, polls the API (no external network needed).
const API = "/api/v1";
const TOKEN = new URLSearchParams(location.search).get("token") || "";
const $ = (id) => document.getElementById(id);
const esc = (s) => String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const css = (v) => getComputedStyle(document.documentElement).getPropertyValue(v).trim();

async function get(path) {
  const r = await fetch(API + path, { cache: "no-store", headers: TOKEN ? { "X-Admin-Token": TOKEN } : {} });
  if (!r.ok) throw new Error(`${r.status} ${path}`);
  return r.json();
}
async function post(path, body) {
  const r = await fetch(API + path, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...(TOKEN ? { "X-Admin-Token": TOKEN } : {}) },
    body: JSON.stringify(body),
  });
  const j = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(j.detail || r.status);
  return j;
}

let soilDevice = null, currentEv = null, lastRipenessEv = null, chart = null, ndviChart = null;

// ---------- live soil + recommendation
const TILES = [
  ["soil_moisture_pct", "Soil moisture", "%"], ["soil_ph", "Soil pH", ""], ["tds_ppm", "TDS", " ppm"],
  ["ec_us_cm", "EC", " µS/cm"], ["soil_temp_c", "Soil temp", " °C"], ["air_temp_c", "Air temp", " °C"],
  ["air_rh_pct", "Air RH", " %"],
];

function renderSoil(s) {
  $("soil-dev").textContent = `${s.device_id} · block ${s.block_id} · seq ${s.seq ?? "—"} · ${s.received_at}`;
  $("tiles").innerHTML = TILES.map(([k, l, u]) => {
    const v = s.reading[k];
    const lab = k === "ec_us_cm" && s.reading.ec_derived ? "EC (≈TDS/0.5)" : l;
    return `<div class="tile ${v == null ? "null" : ""}"><div class="v">${v == null ? "sensor offline" : esc(v) + u}</div><div class="l">${lab}</div></div>`;
  }).join("");
  const r = s.recommendation;
  currentEv = s.evidence_id;
  $("rec-main").querySelector(".led").className = "led " + r.led;
  $("rec-main").querySelector(".act").textContent = r.action.replace("_", " ");
  $("rec-main").querySelector(".conf").textContent = `confidence ${(r.confidence * 100).toFixed(0)}%` + (r.needs_review ? " · needs review" : "");
  $("rec-reason").textContent = r.reason;
  $("rec-actions").innerHTML = r.actions.map((a) =>
    `<li class="sev-${a.severity}"><span class="rid">${esc(a.rule_id)}</span> ${esc(a.action)} — ${esc(a.reason)}</li>`).join("") +
    (r.notes || []).map((n) => `<li class="sev-low">${esc(n)}</li>`).join("");
  $("rec-cf").textContent = r.counterfactual ? "Counterfactual: " + r.counterfactual : "";
  $("rec-sim").classList.toggle("hidden", !r.simulated);
  if (r.ml) {
    const att = r.ml.attributions.map((a) => `${a.feature} ${a.contribution > 0 ? "+" : ""}${a.contribution}`).join(", ");
    $("rec-ml").textContent = `ML check (${r.ml.model_version}, trained on SIMULATED data): ${r.ml.agrees_with_rules ? "agrees" : "DISAGREES"} with rules` +
      (att ? ` · drivers: ${att}` : "");
  } else $("rec-ml").textContent = "";
  $("rec-ev").textContent = s.evidence_id;
  const rv = s.reviews || [];
  $("rec-review").textContent = rv.length ? rv.map((x) => `${x.decision} by ${x.by}${x.override_action ? " → " + x.override_action : ""}`).join("; ") : "";
}

async function renderChart(device) {
  const rows = await get(`/readings?device_id=${encodeURIComponent(device)}&limit=60`);
  const labels = rows.map((r) => r.received_at.slice(11, 19));
  const ds = [
    ["Moisture %", rows.map((r) => r.soil_moisture_pct), css("--brand"), "y"],
    ["pH ×10", rows.map((r) => (r.soil_ph == null ? null : r.soil_ph * 10)), css("--accent"), "y"],
    ["TDS ppm", rows.map((r) => r.tds_ppm), css("--sim"), "y2"],
  ];
  if (!chart) {
    chart = new Chart($("soil-chart"), {
      type: "line",
      data: { labels, datasets: ds.map(([l, d, c, y]) => ({ label: l, data: d, borderColor: c, backgroundColor: c, yAxisID: y, pointRadius: 0, tension: 0.25, spanGaps: false })) },
      options: { animation: false, maintainAspectRatio: false, interaction: { mode: "index", intersect: false },
        scales: { y: { min: 0, max: 100, title: { display: true, text: "% / pH×10" } }, y2: { position: "right", grid: { display: false }, title: { display: true, text: "ppm" } } } },
    });
  } else {
    chart.data.labels = labels;
    ds.forEach(([, d], i) => (chart.data.datasets[i].data = d));
    chart.update();
  }
}

// ---------- camera
function renderRipeness(r) {
  if (!r) return;
  $("cam-heat").src = r.heatmap_url + "?v=" + r.evidence_id;
  $("cam-heat").classList.toggle("hidden", !r.heatmap_url);
  $("cam-res").textContent = `${r.label} · ${(r.confidence * 100).toFixed(0)}%`;
  const ORDER = ["unripe", "underripe", "ripe", "overripe"];   // ripeness order, not alphabetical
  const rank = (k) => { const i = ORDER.indexOf(k); return i < 0 ? 99 : i; };
  const probs = Object.entries(r.probs).sort(([a], [b]) => rank(a) - rank(b));
  $("cam-probs").innerHTML = probs.map(([k, v]) =>
    `<div class="bar"><span>${esc(k)}</span><div class="track"><div class="fill" style="width:${(v * 100).toFixed(0)}%"></div></div><span>${(v * 100).toFixed(0)}%</span></div>`).join("");
  $("cam-exp").textContent = r.explanation;
  $("cam-adv").textContent = "Harvest advice (rule-based schedule): " + r.harvest_advice;
  $("cam-model").textContent = `${r.model_version} · ${r.evidence_id} · ${r.created_at}`;
  if (lastRipenessEv && r.evidence_id !== lastRipenessEv) $("cam-msg").textContent = "New result received.";
  lastRipenessEv = r.evidence_id;
}

$("capture").onclick = async () => {
  try {
    await post("/devices/cam-01/commands", { cmd: "capture" });
    $("cam-msg").textContent = "Capture requested — waiting for camera…";
  } catch (e) { $("cam-msg").textContent = "Failed: " + e.message; }
};

// ---------- reviews
document.querySelectorAll("[data-review]").forEach((b) => (b.onclick = async () => {
  if (!currentEv) return;
  const decision = b.dataset.review;
  const body = { decision, by: "agronomist", note: decision === "override" ? "field judgement" : "checked" };
  if (decision === "override") body.override_action = $("ovr-act").value;
  try { const r = await post(`/evidence/${currentEv}/review`, body); $("rec-review").textContent = `${decision} logged as ${r.evidence_id}`; }
  catch (e) { $("rec-review").textContent = "Failed: " + e.message; }
}));

// ---------- calibration
async function loadCal() {
  const dev = $("cal-dev").value;
  if (!dev) return;
  const c = await get(`/devices/${dev}/calibration`).catch(() => null);
  if (c) {
    $("cal-base").value = c.tds_baseline_ppm ?? "";
    $("cal-margin").value = c.tds_margin;
    $("cal-msg").textContent = c.tds_baseline_ppm ? `Baseline ${c.tds_baseline_ppm} ppm ±${Math.round(c.tds_margin * 100)}% (set ${c.updated_at})` : "Not calibrated — TDS rules skipped.";
  }
}
$("cal-dev").onchange = loadCal;
$("cal-save").onclick = async () => {
  try { await post(`/devices/${$("cal-dev").value}/calibration`, { tds_baseline_ppm: +$("cal-base").value, tds_margin: +$("cal-margin").value }); loadCal(); }
  catch (e) { $("cal-msg").textContent = "Failed: " + e.message; }
};
$("cal-latest").onclick = async () => {
  try { await post(`/devices/${$("cal-dev").value}/calibration`, { use_latest: true, tds_margin: +$("cal-margin").value }); loadCal(); }
  catch (e) { $("cal-msg").textContent = "Failed: " + e.message; }
};

// ---------- evidence + MSPO
async function renderEvidence() {
  const rows = await get(`/evidence?limit=25&non_ok=${$("ev-nonok").checked}`);
  $("ev-tbl").querySelector("tbody").innerHTML = rows.map((e) => {
    const o = e.record.output || {};
    const d = o.action || o.label || e.record.decision || "";
    const why = o.reason || o.explanation || "";
    return `<tr><td class="mono"><a href="${API}/evidence/${e.evidence_id}${TOKEN ? "?token=" + encodeURIComponent(TOKEN) : ""}" target="_blank">${e.evidence_id}</a></td><td>${e.created_at.slice(5, 19).replace("T", " ")}</td>
      <td>${esc(e.kind)}</td><td>${esc(e.block_id ?? "—")}</td><td class="wrap"><b>${esc(d)}</b> ${o.simulated ? '<span class="badge sim">SIM</span>' : ""} <span class="muted">${esc(why)}</span></td>
      <td class="small">${e.mspo.join(", ")}</td><td class="mono">${e.hash.slice(0, 10)}</td></tr>`;
  }).join("");
}
$("ev-nonok").onchange = renderEvidence;
$("verify").onclick = async () => {
  const v = await get("/evidence/verify");
  $("verify-msg").innerHTML = `<span class="${v.ok ? "ok-txt" : "bad-txt"}">${v.ok ? "✔" : "✘"} ${esc(v.message)}</span>`;
};
async function renderMspo() {
  const c = await get("/compliance/coverage");
  $("mspo").innerHTML = c.criteria.map((k) =>
    `<div class="c ${k.status === "evidenced" ? "ok" : ""}"><b>${esc(k.title)}</b><br>${k.records} records · ${k.status}<br><span class="muted">${esc(k.ref)}</span></div>`).join("");
}

// ---------- harvest
async function renderHarvest() {
  const h = await get(`/harvest/plan?crew=${+$("crew").value || 30}`);
  if (!h.available) return;
  $("hv-sum").textContent = `${h.bunches_at_risk_total} bunches at risk · ${h.unassigned_harvesters} harvesters spare · ${h.method}`;
  $("hv-tbl").querySelector("tbody").innerHTML = h.blocks.map((b) =>
    `<tr><td>${esc(b.block_id)}</td><td>${b.ripe_bunches_est}</td><td>${Math.round(b.overripe_share * 100)}%</td><td>${b.harvester_days_needed}</td>
     <td>${b.assigned_harvesters}</td><td>${b.bunches_at_risk}</td><td class="st-${b.status}">${b.status}</td></tr>`).join("");
}
$("crew").onchange = renderHarvest;

// ---------- cascade
let cascadeLoaded = false;
async function renderCascade() {
  const c = await get("/screening");
  if (!c.available) return;
  cascadeLoaded = true;
  const s1 = c.stage1_satellite, s2 = c.stage2_drone, s3 = c.stage3_ground;
  $("sat-src").textContent = `${s1.source} · ${s1.flagged.length}/${s1.blocks_total} blocks below z ${s1.threshold_z}`;
  $("sat-flag").innerHTML = s1.flagged.map((b) => `<li>Block ${esc(b.block_id)}: NDVI z = ${b.ndvi_z}${b.ndvi != null ? ` (NDVI ${b.ndvi})` : ""} → drone survey</li>`).join("") || "<li>No anomalous blocks</li>";
  $("drone-src").textContent = s2.source ? `${s2.source} · block ${s2.block} · ${s2.palms_scored} palms scored` : "Drone screening not yet available";
  if (s2.image) { $("drone-img").src = s2.image; $("drone-img").classList.remove("hidden"); }
  $("drone-metrics").textContent = s2.metrics ? Object.entries(s2.metrics).map(([k, v]) => `${k}: ${v}`).join(" · ") : "";
  $("ground-note").textContent = s3.note;
  $("ground-list").innerHTML = s3.ranked.map((p) => `<li>${esc(p.palm_id)} — p=${p.p_ganoderma}${p.dist_to_confirmed_m != null ? `, ${p.dist_to_confirmed_m} m from confirmed case` : ""} → priority ${p.priority}</li>`).join("") || "<li class='muted'>No palms above threshold</li>";

  const sat = await get("/satellite");
  if (sat.available !== false && sat.blocks) {
    if (sat.image) { $("sat-img").src = sat.image; $("sat-img").classList.remove("hidden"); }
    const months = sat.months || [];
    const ser = sat.estate_ndvi || [];
    if (!ndviChart && months.length) {
      ndviChart = new Chart($("ndvi-chart"), { type: "line",
        data: { labels: months, datasets: [{ label: "Estate median NDVI", data: ser, borderColor: css("--brand"), pointRadius: 2, tension: 0.2 }] },
        options: { animation: false, maintainAspectRatio: false, plugins: { legend: { display: false } } } });
    }
  }
}

// ---------- main loop
async function tick() {
  try {
    const l = await get("/latest");
    $("conn").textContent = "live"; $("conn").className = "pill ok";
    $("mode").textContent = l.mode === "cloud" ? "CLOUD" : "LOCAL";
    $("clock").textContent = l.server_time.slice(11, 19) + " UTC · " + l.evidence_count + " evidence records";
    const devs = l.soil.map((s) => s.device_id);
    if (!soilDevice || !devs.includes(soilDevice)) soilDevice = devs.find((d) => d.startsWith("soilnode")) || devs[0];
    const calDevs = [...new Set([...devs, "soilnode-01"])];
    if ($("cal-dev").options.length !== calDevs.length) { $("cal-dev").innerHTML = calDevs.map((d) => `<option>${d}</option>`).join(""); loadCal(); }
    const s = l.soil.find((x) => x.device_id === soilDevice);
    if (s) { renderSoil(s); renderChart(soilDevice); }
    renderRipeness(l.ripeness);
  } catch (e) {
    $("conn").textContent = "offline"; $("conn").className = "pill bad";
  }
}
let n = 0;
if (TOKEN) {  // carry the token on links opened in new tabs (cloud mode protects reads)
  $("export").href += "?token=" + encodeURIComponent(TOKEN);
  document.querySelector('a[href="/harvester"]').href += "?token=" + encodeURIComponent(TOKEN);
}
async function loop() {
  await tick();
  if (n % 2 === 0) renderEvidence().catch(() => {});
  if (n % 8 === 0) { renderMspo().catch(() => {}); renderHarvest().catch(() => {}); }
  if (!cascadeLoaded && n % 5 === 0) renderCascade().catch(() => {});   // retry until the backend answers
  n++;
  setTimeout(loop, 2000);
}
loop();
