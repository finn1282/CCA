// SawitSense presentation engine: scenes, build steps, keyboard, presenter sync, interactive scenes.
(function () {
  "use strict";
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
  const CFG = Object.assign({}, window.SAWIT_CONFIG || {});
  // ?dash=<url> overrides the primary dashboard URL (rehearsal convenience)
  try { const q = new URLSearchParams(location.search).get("dash"); if (q) CFG.DASHBOARD_URL = q; } catch (e) { /* ignore */ }
  const LOCAL = window.SAWIT_LOCAL || {};
  const META = SAWIT.SCENES;
  const scenes = $$(".scene");
  const store = {
    get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set(k, v) { try { localStorage.setItem(k, v); } catch (e) { /* ignore */ } }
  };

  // ---------- stage scaling ----------
  const stage = $("#stage");
  function fit() {
    const s = Math.min(window.innerWidth / 1920, window.innerHeight / 1080);
    stage.style.transform = `scale(${s})`;
  }
  window.addEventListener("resize", fit); fit();

  // ---------- theme ----------
  function setTheme(t) { document.documentElement.dataset.theme = t; store.set("sawit-theme", t); }
  setTheme(store.get("sawit-theme") === "day" ? "day" : "estate");

  // speaker pill on every scene
  scenes.forEach((el, i) => {
    const w = document.createElement("div");
    w.className = "who"; w.textContent = META[i] ? META[i].speaker : "";
    el.appendChild(w);
  });

  // ---------- estate map ----------
  let seed = 7;
  const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
  function star(r) {
    const pts = [];
    for (let k = 0; k < 16; k++) {
      const a = (Math.PI * 2 * k) / 16, rr = k % 2 ? r * 0.45 : r;
      pts.push((Math.cos(a) * rr).toFixed(1) + "," + (Math.sin(a) * rr).toFixed(1));
    }
    return pts.join(" ");
  }
  const CROWN = star(15);
  // Hidden Ganoderma cluster: block B2, spreading from one corner (root contact ~4 rows)
  const INFECT = { B2: [0, 1, 6, 7, 2, 12, 13, 8], B1: [] };
  function estateSVG() {
    seed = 7;
    const W = 960, H = 480, bw = 220, bh = 205;
    let s = `<svg class="estate" viewBox="0 0 ${W} ${H}" preserveAspectRatio="xMidYMid meet" aria-label="Demo estate map (simulated)">`;
    s += `<rect class="road" x="0" y="0" width="${W}" height="${H}" rx="18"/>`;
    SAWIT.BLOCKS.forEach((b, bi) => {
      const col = bi % 4, row = Math.floor(bi / 4);
      const x = 12 + col * 236, y = 25 + row * 225;
      s += `<g data-block="${b.id}"><rect class="blk" x="${x}" y="${y}" width="${bw}" height="${bh}" rx="10"/>`;
      s += `<text class="bl" x="${x + 10}" y="${y + 24}">${b.id}</text>`;
      let n = 0;
      for (let r = 0; r < 4; r++) for (let c = 0; c < 6; c++) {
        const px = x + 22 + c * 35 + (r % 2 ? 17 : 0), py = y + 52 + r * 44;
        if (px > x + bw - 12) { n++; continue; }
        const ripe = rnd() < 0.45, over = ripe && rnd() < b.over * 3.2;
        const inf = (INFECT[b.id] || []).indexOf(n);
        s += `<g class="palm" transform="translate(${px},${py})">` +
          `<circle class="root${inf >= 0 ? " inf" : ""}" r="19" style="--d:${(inf * 0.35).toFixed(2)}s"/>` +
          `<polygon class="crown" points="${CROWN}"/>` +
          `<circle class="ffb${ripe ? " ripe" : ""}${over ? " over" : ""}" cx="7" cy="7" r="6" style="--d:${(1.2 + rnd() * 1.6).toFixed(2)}s"/></g>`;
        n++;
      }
      s += `</g>`;
    });
    // soil veil for the X-ray (drawn under roots? roots must be above veil: re-draw roots on top)
    s += `<rect class="soilveil" x="0" y="0" width="${W}" height="${H}" rx="18"/>`;
    s += `<g class="rootlayer"></g>`;
    // two harvesters, only reaching two blocks
    s += `<g class="harv" fill="var(--gold)"><circle cx="70" cy="215" r="10"/><rect x="62" y="226" width="16" height="22" rx="5"/>` +
         `<circle cx="540" cy="215" r="10"/><rect x="532" y="226" width="16" height="22" rx="5"/></g>`;
    s += `</svg>`;
    return s;
  }
  function mountEstate(host) {
    host.innerHTML = estateSVG();
    // move root circles above the veil so the X-ray shows them through the soil
    const svg = host.firstChild, layer = $(".rootlayer", svg);
    $$(".palm", svg).forEach((p) => {
      const r = $(".root", p);
      if (!r.classList.contains("inf")) return;
      const g = document.createElementNS("http://www.w3.org/2000/svg", "g");
      g.setAttribute("transform", p.getAttribute("transform"));
      g.appendChild(r); layer.appendChild(g);
    });
    if (host.dataset.mode) svg.classList.add(host.dataset.mode);
    return svg;
  }
  $$(".estate-host").forEach(mountEstate);
  function mapMode(host, mode) {
    const svg = host.firstChild;
    svg.classList.remove("m-p1", "m-xray", "m-dim");
    void svg.getBoundingClientRect();
    if (mode) mode.split(" ").forEach((m) => svg.classList.add(m));
  }

  // ---------- counters ----------
  function runCounters(scope) {
    $$("[data-count]", scope).forEach((el) => {
      const to = +el.dataset.count, dec = +(el.dataset.dec || 0), delay = +(el.dataset.delay || 0);
      const fmt = (v) => (el.dataset.prefix || "") +
        (el.dataset.sep ? Math.round(v).toLocaleString("en-US") : v.toFixed(dec)) + (el.dataset.suffix || "");
      el.textContent = fmt(0);
      clearTimeout(el._t); cancelAnimationFrame(el._r);
      el._t = setTimeout(() => {
        const t0 = performance.now(), D = 1300;
        const tick = (t) => {
          const p = Math.min(1, (t - t0) / D), e = 1 - Math.pow(1 - p, 3);
          el.textContent = fmt(to * e);
          if (p < 1) el._r = requestAnimationFrame(tick);
        };
        el._r = requestAnimationFrame(tick);
      }, delay);
    });
  }

  // ---------- scene hooks ----------
  const hooks = {};
  hooks.hook = { enter(el) { runCounters(el); } };
  hooks.problems = {
    step(el, k) {
      const host = $("#map-problems");
      mapMode(host, k === 0 ? "m-p1" : k === 1 ? "m-xray" : "m-dim");
      const days = Math.ceil((Date.UTC(2026, 11, 30) - Date.now()) / 86400000);
      $("#eudr-clock").textContent = days > 0 ? days + " days" : "now in force";
    }
  };
  hooks.architecture = {
    step(el, k) { $("#layers").classList.toggle("flowing", k >= 6); }
  };
  $$(".layer").forEach((l) => l.addEventListener("click", () => l.classList.toggle("open")));

  // risks grid (Table 5)
  const CAT = { tech: "Technical", ops: "Operational", vendor: "Vendor & cost" };
  (function buildRisks() {
    const g = $("#riskgrid");
    let html = "";
    for (let L = 3; L >= 1; L--) {
      html += `<div class="ax">L${L}</div>`;
      for (let I = 1; I <= 3; I++) {
        const heat = L * I, bg = heat >= 9 ? "rgba(224,74,50,.45)" : heat >= 6 ? "rgba(245,160,40,.32)" : heat >= 4 ? "rgba(244,201,93,.18)" : "rgba(166,210,90,.10)";
        html += `<div class="cell" style="background:${bg}">` +
          SAWIT.RISKS.filter((r) => r.L === L && r.I === I).map((r) => `<span class="rchip ${r.cat}" data-n="${r.n}">${r.n}</span>`).join("") + `</div>`;
      }
    }
    html += `<div></div><div class="ax">Impact 1</div><div class="ax">Impact 2</div><div class="ax">Impact 3</div>`;
    g.innerHTML = html;
    $$(".rchip", g).forEach((c) => c.addEventListener("click", () => showRisk([+c.dataset.n])));
  })();
  function showRisk(ns) {
    $$(".rchip").forEach((c) => c.classList.toggle("sel", ns.includes(+c.dataset.n)));
    $("#riskinfo").innerHTML = ns.map((n) => {
      const r = SAWIT.RISKS[n - 1];
      return `<div style="margin-bottom:18px"><b class="hl">#${r.n} ${CAT[r.cat]} · L${r.L}×I${r.I}</b><div><b>${r.risk}</b></div>` +
        `<div class="small">Mitigation: ${r.mit}</div><div class="small muted">Owner: ${r.owner}</div></div>`;
    }).join("");
  }
  hooks.roadmap = {
    step(el, k) {
      if (k === 2) showRisk([1]);
      if (k >= 3) {
        showRisk([1, 2]);
        $("#riskinfo").insertAdjacentHTML("beforeend",
          `<div class="hl-leaf" style="font-size:30px">Top risks are data and people, not technology → a human approves every decision in the pilot.</div>`);
      }
    }
  };

  // ---------- demo scene ----------
  const demo = { base: CFG.DASHBOARD_URL || "http://localhost:8000", usingFallback: false, up: null, timer: null, loaded: false };
  const dash = $("#dash"), fbox = $("#framebox");
  function withToken(base) {
    const u = base.replace(/\/+$/, "") + "/";
    return LOCAL.token ? u + "?token=" + encodeURIComponent(LOCAL.token) : u;
  }
  function frameTo(panel) {
    const url = withToken(demo.base) + (panel ? "#" + panel : "");
    if (dash.getAttribute("src") !== url) dash.setAttribute("src", url);
    demo.loaded = true;
  }
  function setBase(b, fallback) {
    demo.base = b; demo.usingFallback = fallback; demo.loaded = false;
    dash.removeAttribute("src");
    $("#hurl").textContent = (fallback ? "FALLBACK: " : "PRIMARY: ") + b;
    frameTo(currentPanel()); checkHealth();
  }
  async function checkHealth() {
    const url = demo.base.replace(/\/+$/, "") + "/api/v1/health";
    let ok = false;
    try {
      const ctl = new AbortController(); const t = setTimeout(() => ctl.abort(), 3000);
      const r = await fetch(url, { cache: "no-store", signal: ctl.signal });
      clearTimeout(t); ok = r.ok;
    } catch (e) { ok = false; }
    demo.up = ok;
    $("#hlight").className = "light " + (ok ? "ok" : "bad");
    $("#hstatus").textContent = ok ? "backend healthy" : "backend not responding";
    $("#downurl").textContent = demo.base;
    fbox.classList.toggle("down", !ok);
    if (ok && !demo.loaded) frameTo(currentPanel());
  }
  function currentPanel() { return cur === sceneIndex("demo") ? (SAWIT.DEMO_BEATS[step] || {}).panel : ""; }
  (function buildBeats() {
    $("#beats").innerHTML = SAWIT.DEMO_BEATS.map((b, i) =>
      `<div class="beat" data-i="${i}"><span class="t">${b.t}</span><span>${b.label}</span><span class="w">${b.who}</span></div>`).join("");
    $$("#beats .beat").forEach((b) => b.addEventListener("click", () => go(cur, +b.dataset.i)));
  })();
  hooks.demo = {
    enter() {
      checkHealth(); clearInterval(demo.timer);
      demo.timer = setInterval(checkHealth, CFG.HEALTH_INTERVAL_MS || 5000);
    },
    step(el, k) {
      $$("#beats .beat").forEach((b, i) => { b.classList.toggle("cur", i === k); b.classList.toggle("done", i < k); });
      if (demo.up !== false) frameTo(SAWIT.DEMO_BEATS[k].panel);
    },
    leave() { clearInterval(demo.timer); }
  };
  $("#hurl").textContent = "PRIMARY: " + demo.base;
  frameTo("");           // warm the dashboard up at load time
  // focus hint: keys typed while the iframe has focus go to the dashboard, not the slides
  setInterval(() => fbox.classList.toggle("focused", document.activeElement === dash), 500);
  function simCmd() { return (CFG.SIMULATOR_CMD || "").replace("{BASE}", demo.base.replace(/\/+$/, "")); }
  function toggleSim(clear) {
    if (clear) { fbox.classList.remove("sim-on"); $("#simmodal").classList.remove("show"); return; }
    $("#simcmd").textContent = simCmd(); $("#simmsg").textContent = "";
    $("#simmodal").classList.toggle("show");
    fbox.classList.add("sim-on");
  }
  $("#simcopy").addEventListener("click", async () => {
    try { await navigator.clipboard.writeText(simCmd()); $("#simmsg").textContent = "copied"; }
    catch (e) { $("#simmsg").textContent = "copy blocked: select the text instead"; }
  });

  // ---------- novelty: evidence chain + tamper ----------
  const chain = SAWIT.CHAIN.map((r) => Object.assign({}, r));
  const PH_ORIG = "3.8";
  function body(r, ph) {
    const reason = r.editable ? r.reason.replace(PH_ORIG, ph) : r.reason;
    return JSON.stringify({ id: r.id, block: r.block, decision: r.decision, reason, cf: r.cf, approval: r.approval, clause: r.clause });
  }
  const GENESIS = "0".repeat(64);
  (function seal() { let prev = GENESIS; chain.forEach((r) => { r.prev = prev; r.hash = sha256hex(prev + body(r, PH_ORIG)); prev = r.hash; }); })();
  (function renderChain() {
    $("#chain").innerHTML = chain.map((r, i) => {
      const reason = r.editable ? r.reason.replace(PH_ORIG, `<input id="ph" value="${PH_ORIG}" aria-label="pH value">`) : r.reason;
      return `<div class="rec" id="rec${i}"><div class="id">${r.id} · block ${r.block}</div><div class="dec">${r.decision}</div>` +
        `<div class="f">reason: <b>${reason}</b></div><div class="f">counterfactual: <b>${r.cf}</b></div>` +
        `<div class="f">${r.approval}</div><div class="f">${r.clause}</div><div class="h" id="h${i}"></div></div>`;
    }).join("");
    $("#ph").addEventListener("input", verifyChain);
  })();
  function verifyChain() {
    const ph = ($("#ph").value || "").trim();
    let prev = GENESIS, broken = -1;
    chain.forEach((r, i) => {
      const now = sha256hex(prev + body(r, ph));
      const bad = broken >= 0 || now !== r.hash;
      if (bad && broken < 0) broken = i;
      $("#rec" + i).classList.toggle("bad", bad);
      $("#h" + i).innerHTML = !bad ? `<span class="lab">hash</span> ${r.hash.slice(0, 16)}…` :
        i === broken ? `<span class="lab">stored</span> ${r.hash.slice(0, 12)}…<br><span class="lab">now</span> ${now.slice(0, 12)}… ≠` :
        `<span class="lab">prev link broken</span><br>${r.hash.slice(0, 12)}…`;
      prev = now;
    });
    const v = $("#verdict");
    v.className = "verdict " + (broken < 0 ? "ok" : "bad");
    v.textContent = broken < 0 ? "VERIFIED" : `TAMPERED at record ${broken + 1}`;
  }
  let typing = null;
  function tamper() {
    clearInterval(typing);
    const inp = $("#ph"), target = "5.0"; let i = 0;
    inp.value = ""; verifyChain();
    typing = setInterval(() => { inp.value = target.slice(0, ++i); verifyChain(); if (i >= target.length) clearInterval(typing); }, 260);
  }
  function undo() { clearInterval(typing); $("#ph").value = PH_ORIG; verifyChain(); }
  $("#tamper").addEventListener("click", tamper);
  $("#undo").addEventListener("click", undo);
  verifyChain();
  hooks.novelty = { enter() { undo(); } };

  // ---------- engine ----------
  let cur = 0, step = 0, t0 = null, sceneT0 = Date.now();
  const sceneIndex = (id) => META.findIndex((m) => m.id === id);
  const nSteps = (i) => +(scenes[i].dataset.steps || 1);
  function applySteps(el, k) {
    $$("[data-b]", el).forEach((e) => e.classList.toggle("on", k >= +e.dataset.b));
    $$("[data-only]", el).forEach((e) => e.classList.toggle("on", e.dataset.only.split(",").map(Number).includes(k)));
  }
  function go(i, k, fromRemote) {
    i = Math.max(0, Math.min(scenes.length - 1, i));
    k = Math.max(0, Math.min(nSteps(i) - 1, k));
    const changed = i !== cur || !scenes[i].classList.contains("active");
    if (changed) {
      const old = scenes[cur], oh = hooks[META[cur].id];
      if (old.classList.contains("active") && oh && oh.leave) oh.leave(old);
      scenes.forEach((s, j) => s.classList.toggle("active", j === i));
      cur = i; sceneT0 = Date.now();
    }
    step = k;
    const el = scenes[i], h = hooks[META[i].id];
    applySteps(el, k);
    if (changed && h && h.enter) h.enter(el);
    if (h && h.step) h.step(el, k);
    $("#progress").style.width = ((META[i].start + META[i].dur * (k + 1) / nSteps(i)) / SAWIT.TALK_S * 100).toFixed(2) + "%";
    try { history.replaceState(null, "", "#" + (i + 1) + "." + k); } catch (e) { /* file:// may refuse */ }
    broadcast();
  }
  function next() {
    if (t0 === null) t0 = Date.now();
    if (step < nSteps(cur) - 1) go(cur, step + 1); else if (cur < scenes.length - 1) go(cur + 1, 0);
  }
  function prev() {
    if (step > 0) go(cur, step - 1); else if (cur > 0) go(cur - 1, nSteps(cur - 1) - 1);
  }

  // ---------- presenter sync ----------
  let presenter = null, chan = null;
  try { chan = new BroadcastChannel("sawit-presenter"); chan.onmessage = (e) => onCmd(e.data); } catch (e) { chan = null; }
  function state() { return { type: "state", cur, step, steps: nSteps(cur), t0, sceneT0, now: Date.now() }; }
  function broadcast() {
    const s = state();
    if (chan) try { chan.postMessage(s); } catch (e) { /* ignore */ }
    if (presenter && !presenter.closed) try { presenter.postMessage(s, "*"); } catch (e) { /* ignore */ }
  }
  setInterval(broadcast, 1000);
  function onCmd(d) {
    if (!d || d.type !== "cmd") return;
    if (d.cmd === "next") next(); else if (d.cmd === "prev") prev();
    else if (d.cmd === "go") go(d.i, 0);
    else if (d.cmd === "start") { t0 = Date.now(); broadcast(); }
    else if (d.cmd === "hello") broadcast();
  }
  window.addEventListener("message", (e) => onCmd(e.data));

  // ---------- keyboard ----------
  document.addEventListener("keydown", (e) => {
    if (e.target && /INPUT|TEXTAREA|SELECT/.test(e.target.tagName)) { if (e.key === "Escape") e.target.blur(); return; }
    if (e.ctrlKey || e.metaKey || e.altKey) return;
    const k = e.key, inDemo = cur === sceneIndex("demo");
    if (["ArrowRight", " ", "PageDown", "Enter"].includes(k)) { e.preventDefault(); next(); }
    else if (["ArrowLeft", "PageUp", "Backspace"].includes(k)) { e.preventDefault(); prev(); }
    else if (/^[1-9]$/.test(k)) go(+k - 1, 0);
    else if (k === "0") go(9, 0);
    else if (k === "-") go(10, 0);
    else if (k === "Home") go(0, 0);
    else if (k === "End") go(scenes.length - 1, 0);
    else if (k === "p" || k === "P") presenter = window.open("presenter.html", "sawit-presenter", "width=1100,height=760");
    else if (k === "t" || k === "T") setTheme(document.documentElement.dataset.theme === "day" ? "estate" : "day");
    else if (k === "b" || k === "B" || k === ".") $("#black").classList.toggle("show");
    else if (k === "z" || k === "Z") { t0 = Date.now(); broadcast(); }
    else if ((k === "r" || k === "R") && cur === sceneIndex("novelty")) undo();
    else if (inDemo && (k === "f" || k === "F")) setBase(demo.usingFallback ? (CFG.DASHBOARD_URL || demo.base) : (CFG.FALLBACK_URL || "http://localhost:8000"), !demo.usingFallback);
    else if (inDemo && (k === "o" || k === "O")) window.open(withToken(demo.base) + (currentPanel() ? "#" + currentPanel() : ""), "_blank");
    else if (inDemo && (k === "u" || k === "U")) { dash.removeAttribute("src"); demo.loaded = false; frameTo(currentPanel()); }
    else if (inDemo && k === "s") toggleSim(false);
    else if (inDemo && k === "S") toggleSim(true);
    else if (k === "Escape") { $("#simmodal").classList.remove("show"); $("#black").classList.remove("show"); }
  });
  // clickers / mouse: click on empty stage area does nothing (avoid accidental advance)

  // ---------- start ----------
  const m = /^#(\d+)\.(\d+)$/.exec(location.hash);
  go(m ? +m[1] - 1 : 0, m ? +m[2] : 0);
  if (!window.SHA256_SELFTEST) console.warn("SHA-256 self-test failed");
  else if (window.crypto && crypto.subtle) {
    crypto.subtle.digest("SHA-256", new TextEncoder().encode("sawit")).then((b) => {
      const hex = Array.from(new Uint8Array(b), (x) => x.toString(16).padStart(2, "0")).join("");
      console.log("sha256 cross-check vs crypto.subtle:", hex === sha256hex("sawit") ? "match" : "MISMATCH");
    }).catch(() => {});
  }
})();
