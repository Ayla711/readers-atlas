/* The Reader's Atlas — opening animation (spec F1).
   A spinning globe unfolds into the flat world map, the title appears, then the map flies to the UK.
   Drawn on its own canvas; every vertex has a globe position (orthographic) and a flat position
   (the main map's Mercator projection and exact world view), blended by one factor. When the blend
   reaches 1 the canvas matches the SVG map underneath and fades away.
   Rules: any click / key / wheel skips; reduced motion skips; plays once per browser session.
   Testing: ?intro=1 forces it on, ?intro=0 forces it off. */
(function () {
  "use strict";

  const SEEN_KEY = "ra.introSeen";
  const params = new URLSearchParams(window.location.search);
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // timeline in ms after loading ends (spec F1)
  const T = {
    spinEnd: 2000,      // globe scales in and turns to face Europe
    unfoldStart: 500,   // globe → flat, overlapping the spin
    unfoldEnd: 2500,
    handoff: 2500,      // canvas fades out, SVG map and region washes appear
    handoffLen: 400,
    title: 2700,        // title, then tagline 400 ms later
    enter: 4300,        // title moves into the top bar, map flies to the UK
    enterLen: 900,
  };
  const LOADING_MAX = 500;
  const SPIN_DEGREES = 200;
  const TILT = 22 * Math.PI / 180;

  const ease = {
    quadOut: (t) => 1 - (1 - t) * (1 - t),
    quintOut: (t) => 1 - Math.pow(1 - t, 5),
    cubicInOut: (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2),
  };
  const clamp01 = (v) => Math.max(0, Math.min(1, v));
  const lerp = (a, b, t) => a + (b - a) * t;

  function seen() { try { return sessionStorage.getItem(SEEN_KEY) === "1"; } catch (e) { return false; } }
  function markSeen() { try { sessionStorage.setItem(SEEN_KEY, "1"); } catch (e) { /* storage unavailable */ } }

  window.RA_INTRO = {
    shouldRun() {
      if (params.get("intro") === "1") return true;
      if (params.get("intro") === "0") return false;
      // a shared link to a place, book or region opens that view directly
      if (/^#\/(region|place|book|travel|reading)/.test(window.location.hash)) return false;
      const canvasOK = !!document.createElement("canvas").getContext;
      return !reduceMotion && !seen() && canvasOK && Array.isArray(window.RA_INTRO_GEO);
    },
    run,
  };

  function run(api) {
    markSeen();
    const css = getComputedStyle(document.documentElement);
    const color = (name) => css.getPropertyValue(name).trim();
    const C = {
      paper: color("--paper"), sea: color("--sea"), land: color("--world-land"),
      edge: color("--world-edge"), uk: color("--wash-ochre"), ink: color("--ink"),
    };
    const t = api.t();

    // ---------- overlay ----------
    const overlay = document.createElement("div");
    overlay.className = "intro-overlay";
    overlay.innerHTML = `
      <canvas class="intro-canvas" aria-hidden="true"></canvas>
      <p class="intro-loading">${t.introLoading}</p>
      <div class="intro-title"><h2 class="intro-name">The Reader's Atlas</h2><p class="intro-tagline">${t.introTagline}</p></div>
      <p class="intro-skip">${t.introSkip}</p>`;
    document.body.append(overlay);
    const canvas = overlay.querySelector("canvas");
    const ctx = canvas.getContext("2d");
    const name = overlay.querySelector(".intro-name");
    const tagline = overlay.querySelector(".intro-tagline");

    const vw = window.innerWidth, vh = window.innerHeight, dpr = Math.min(2, window.devicePixelRatio || 1);
    canvas.width = vw * dpr; canvas.height = vh * dpr;
    canvas.style.width = vw + "px"; canvas.style.height = vh + "px";
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

    // where the SVG map sits on screen, and the world view it is showing
    const mapRect = document.getElementById("map").getBoundingClientRect();
    const V = api.worldView;
    const cx = mapRect.left + mapRect.width / 2, cy = mapRect.top + mapRect.height / 2;
    const R = Math.min(mapRect.width, mapRect.height) * 0.38;
    // the flat world view is centred on this longitude; the globe ends facing it
    const lonCentre = ((mapRect.width / 2 - V.x) / V.k / 1000) * 360 - 180;

    // ---------- precompute both positions for every vertex ----------
    const rings = [];
    for (const c of window.RA_INTRO_GEO) {
      for (const ring of c.g) {
        const n = ring.length;
        const lam = new Float32Array(n), cosPhi = new Float32Array(n), sinPhi = new Float32Array(n);
        const fx = new Float32Array(n), fy = new Float32Array(n);
        for (let i = 0; i < n; i++) {
          const [lon, lat] = ring[i];
          const phi = lat * Math.PI / 180;
          lam[i] = lon * Math.PI / 180;
          cosPhi[i] = Math.cos(phi); sinPhi[i] = Math.sin(phi);
          const [px, py] = api.project(lon, lat);
          fx[i] = mapRect.left + V.x + V.k * px;
          fy[i] = mapRect.top + V.y + V.k * py;
        }
        rings.push({ uk: c.uk, n, lam, cosPhi, sinPhi, fx, fy, x: new Float32Array(n), y: new Float32Array(n), depth: 0 });
      }
    }

    // ---------- drawing ----------
    function draw(rel) {
      const spin = ease.quintOut(clamp01(rel / T.spinEnd));
      const grow = ease.quadOut(clamp01(rel / T.spinEnd));
      const u = ease.cubicInOut(clamp01((rel - T.unfoldStart) / (T.unfoldEnd - T.unfoldStart)));
      const lam0 = (lonCentre + SPIN_DEGREES * (1 - spin)) * Math.PI / 180;
      const r = R * (0.8 + 0.2 * grow);
      const cosT = Math.cos(TILT * (1 - u)), sinT = Math.sin(TILT * (1 - u));
      const appear = clamp01(rel / 300); // the globe fades in as it starts to turn

      // background: paper, then the sea of the flat map fading in as the globe opens
      ctx.globalAlpha = 1;
      ctx.fillStyle = C.paper;
      ctx.fillRect(0, 0, vw, vh);
      ctx.save();
      ctx.beginPath();
      ctx.rect(mapRect.left, mapRect.top, mapRect.width, mapRect.height);
      ctx.clip();
      ctx.globalAlpha = u;
      ctx.fillStyle = C.sea;
      ctx.fillRect(mapRect.left, mapRect.top, mapRect.width, mapRect.height);

      // the globe: soft halo, then a shaded sphere
      if (u < 1) {
        ctx.globalAlpha = (1 - u) * appear;
        const halo = ctx.createRadialGradient(cx, cy, r * 0.96, cx, cy, r * 1.12);
        halo.addColorStop(0, "rgba(44, 74, 140, 0.35)");
        halo.addColorStop(1, "rgba(44, 74, 140, 0)");
        ctx.fillStyle = halo;
        ctx.beginPath(); ctx.arc(cx, cy, r * 1.12, 0, Math.PI * 2); ctx.fill();
        const sphere = ctx.createRadialGradient(cx - r * 0.35, cy - r * 0.4, r * 0.1, cx, cy, r);
        sphere.addColorStop(0, "#2f4268");
        sphere.addColorStop(1, C.sea);
        ctx.fillStyle = sphere;
        ctx.beginPath(); ctx.arc(cx, cy, r, 0, Math.PI * 2); ctx.fill();
      }

      // positions: orthographic globe blended into the flat map
      for (const g of rings) {
        let zsum = 0;
        for (let i = 0; i < g.n; i++) {
          const dl = g.lam[i] - lam0;
          const cp = g.cosPhi[i], sp = g.sinPhi[i];
          let gx = cp * Math.sin(dl);
          let gy = cosT * sp - sinT * cp * Math.cos(dl);
          const z = sinT * sp + cosT * cp * Math.cos(dl);
          if (z < 0) { // behind the globe: pin to the horizon so partly hidden shapes keep a clean edge
            const m = Math.hypot(gx, gy) || 1;
            gx /= m; gy /= m;
          }
          zsum += z;
          g.x[i] = lerp(cx + r * gx, g.fx[i], u);
          g.y[i] = lerp(cy - r * gy, g.fy[i], u);
        }
        g.depth = zsum / g.n;
      }
      // far side first; it is faint on the globe and fills in as the map opens
      rings.sort((a, b) => a.depth - b.depth);
      ctx.lineJoin = "round";
      for (const g of rings) {
        const front = g.depth > 0;
        ctx.globalAlpha = (front ? 1 : Math.max(0.12, u)) * appear;
        ctx.beginPath();
        ctx.moveTo(g.x[0], g.y[0]);
        for (let i = 1; i < g.n; i++) ctx.lineTo(g.x[i], g.y[i]);
        ctx.closePath();
        ctx.fillStyle = g.uk ? C.uk : C.land;
        ctx.fill();
        ctx.strokeStyle = C.edge;
        ctx.lineWidth = 0.6;
        ctx.stroke();
      }
      ctx.restore();
      ctx.globalAlpha = 1;
    }

    // ---------- timeline ----------
    const stats = { frames: 0, start: 0, end: 0 };
    window.__introStats = stats;
    let t0 = 0, rafId = 0, done = false;
    const timers = [];
    const later = (ms, fn) => timers.push(setTimeout(fn, ms));

    function frame(now) {
      const rel = now - t0;
      stats.frames++;
      draw(rel);
      if (rel < T.unfoldEnd) rafId = requestAnimationFrame(frame);
      else {
        draw(T.unfoldEnd);
        stats.end = performance.now();
        if (params.get("debug") === "1") showFps();
      }
    }

    // ?debug=1: report the measured frame rate in the corner (spec F1 acceptance: ≥ 50 fps)
    function showFps() {
      const fps = stats.frames / ((stats.end - stats.start) / 1000);
      const tag = document.createElement("div");
      tag.className = "intro-fps";
      tag.textContent = `Intro: ${fps.toFixed(1)} fps (${stats.frames} frames)`;
      document.body.append(tag);
    }

    function begin() {
      overlay.classList.add("is-playing");
      t0 = performance.now();
      stats.start = t0;
      rafId = requestAnimationFrame(frame);
      later(T.handoff, () => {
        api.revealRegions();
        canvas.style.transition = `opacity ${T.handoffLen}ms ease-out`;
        canvas.style.opacity = "0";
        overlay.classList.add("is-handoff");
      });
      later(T.title, () => overlay.classList.add("show-title"));
      later(T.enter, enter);
    }

    // the title glides into the top bar while the map flies to the UK
    function enter() {
      overlay.classList.add("is-entering");
      const brand = document.querySelector(".brand-en");
      const from = name.getBoundingClientRect(), to = brand.getBoundingClientRect();
      const s = to.height / from.height;
      const dx = to.left - from.left, dy = to.top - from.top;
      if (name.animate) {
        name.animate(
          [{ transform: "translate(0, 0) scale(1)", opacity: 1 },
           { transform: `translate(${dx}px, ${dy}px) scale(${s})`, opacity: 1, offset: 0.85 },
           { transform: `translate(${dx}px, ${dy}px) scale(${s})`, opacity: 0 }],
          { duration: T.enterLen, easing: "cubic-bezier(.45,0,.2,1)", fill: "forwards" });
      }
      api.finish(true);
      later(T.enterLen, cleanup);
    }

    function cleanup() {
      done = true;
      cancelAnimationFrame(rafId);
      timers.forEach(clearTimeout);
      overlay.remove();
      window.removeEventListener("pointerdown", skip, true);
      window.removeEventListener("keydown", skip, true);
      window.removeEventListener("wheel", skip, true);
    }

    function skip(e) {
      if (done) return;
      if (e && e.type === "keydown" && (e.metaKey || e.ctrlKey)) return; // let browser shortcuts through
      if (overlay.classList.contains("is-entering")) return; // already finishing
      cleanup();
      api.revealRegions();
      api.finish(false);
    }
    window.addEventListener("pointerdown", skip, true);
    window.addEventListener("keydown", skip, true);
    window.addEventListener("wheel", skip, { capture: true, passive: true });

    // loading: plain paper and one line of text; start once fonts are in (or after LOADING_MAX)
    ctx.fillStyle = C.paper;
    ctx.fillRect(0, 0, vw, vh);
    const ready = document.fonts && document.fonts.ready ? document.fonts.ready : Promise.resolve();
    Promise.race([ready, new Promise((res) => setTimeout(res, LOADING_MAX))]).then(() => { if (!done) begin(); });
  }
})();
