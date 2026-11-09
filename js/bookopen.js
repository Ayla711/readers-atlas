/* Pull a book off the favourites shelf and open it (spec F9, 11-07).
   Click a spine: the book slides out of the shelf, turns to show its cover while it flies to the middle of the screen,
   and the cover swings open into a two-page spread. Closing runs the same steps backwards and puts the book back in its gap.
   Sounds are short public-domain recordings (js/sounds.js): the book sliding out, the cover turning, the book shutting,
   the book going back. The speaker button mutes them (saved as ra.sound).
   With "reduce motion" the spread just fades in and out.
   window.RA_BOOKOPEN.open(spineElement, opts) — opts: { id, cover: { title, author }, left, right (HTML strings),
   labels: { close, soundOn, soundOff }, onClick(event, api), onInput(event), onClose() }.
   api: { update(left, right), close(fast) }. hideSpine(root) keeps the open book's gap empty after the shelf redraws. */
window.RA_BOOKOPEN = (() => {
  "use strict";
  const reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  const NS = "http://www.w3.org/2000/svg";
  const LINE = "#5b4636";
  let cur = null;   // the open book

  // ---------------- sound ----------------
  let ctx = null, noise = null;
  const soundOn = () => window.RA_STORE ? window.RA_STORE.prefs.get("sound", true) !== false : true;
  const setSound = (v) => { if (window.RA_STORE) window.RA_STORE.prefs.set("sound", v); };
  function audio() {
    if (!soundOn()) return null;
    try {
      if (!ctx) {
        ctx = new (window.AudioContext || window.webkitAudioContext)();
        noise = ctx.createBuffer(1, ctx.sampleRate, ctx.sampleRate);
        const d = noise.getChannelData(0);
        for (let i = 0; i < d.length; i++) d[i] = Math.random() * 2 - 1;
      }
      if (ctx.state === "suspended") ctx.resume();
      return ctx;
    } catch (e) { return null; }
  }
  function env(g, t, pts) { g.gain.setValueAtTime(0.0001, t); for (const [dt, v] of pts) g.gain.linearRampToValueAtTime(v, t + dt); }
  function noiseSrc(a, t, dur) { const s = a.createBufferSource(); s.buffer = noise; s.start(t, Math.random() * 0.5); s.stop(t + dur); return s; }
  // paper-and-cloth friction: band-passed noise with a fast grain, the band sliding up (out) or down (in)
  function scrape(a, out, t, dur, f0, f1, level) {
    const s = noiseSrc(a, t, dur + 0.05), bp = a.createBiquadFilter(), g = a.createGain(), grain = a.createGain(), lfo = a.createOscillator(), depth = a.createGain();
    bp.type = "bandpass"; bp.Q.value = 1.1;
    bp.frequency.setValueAtTime(f0, t); bp.frequency.exponentialRampToValueAtTime(f1, t + dur);
    lfo.type = "triangle"; lfo.frequency.setValueAtTime(34, t); lfo.frequency.linearRampToValueAtTime(52, t + dur);
    depth.gain.value = 0.35; grain.gain.value = 0.65;
    lfo.connect(depth).connect(grain.gain); lfo.start(t); lfo.stop(t + dur + 0.05);
    env(g, t, [[0.035, level], [dur * 0.7, level * 0.8], [dur, 0.0001]]);
    s.connect(bp).connect(grain).connect(g).connect(out);
    // the duller rub of the book's body against its neighbours
    const s2 = noiseSrc(a, t, dur + 0.05), lp = a.createBiquadFilter(), g2 = a.createGain();
    lp.type = "lowpass"; lp.frequency.value = 380;
    env(g2, t, [[0.05, level * 0.9], [dur * 0.75, level * 0.6], [dur, 0.0001]]);
    s2.connect(lp).connect(g2).connect(out);
  }
  // a soft knock of the book landing (in the hand, or back on the board)
  function knock(a, out, t, level, pitch) {
    const o = a.createOscillator(), g = a.createGain();
    o.type = "sine"; o.frequency.setValueAtTime(pitch, t); o.frequency.exponentialRampToValueAtTime(pitch * 0.42, t + 0.12);
    env(g, t, [[0.006, level], [0.16, 0.0001]]);
    o.connect(g).connect(out); o.start(t); o.stop(t + 0.2);
    const s = noiseSrc(a, t, 0.05), lp = a.createBiquadFilter(), g2 = a.createGain();
    lp.type = "lowpass"; lp.frequency.value = 1400;
    env(g2, t, [[0.003, level * 0.45], [0.04, 0.0001]]);
    s.connect(lp).connect(g2).connect(out);
  }
  // the cover swinging: a short airy whoosh with a papery top
  function flap(a, out, t, level) {
    const s = noiseSrc(a, t, 0.4), bp = a.createBiquadFilter(), g = a.createGain();
    bp.type = "bandpass"; bp.Q.value = 0.6;
    bp.frequency.setValueAtTime(500, t); bp.frequency.exponentialRampToValueAtTime(2400, t + 0.22);
    env(g, t, [[0.09, level], [0.3, 0.0001]]);
    s.connect(bp).connect(g).connect(out);
    const s2 = noiseSrc(a, t + 0.2, 0.12), hp = a.createBiquadFilter(), g2 = a.createGain();
    hp.type = "highpass"; hp.frequency.value = 3000;
    env(g2, t + 0.2, [[0.01, level * 0.5], [0.09, 0.0001]]);
    s2.connect(hp).connect(g2).connect(out);
  }
  // recorded clips (js/sounds.js, public-domain recordings from Wikimedia Commons, credits in docs/sound-credits.md),
  // decoded once; the synthesised sounds below are only a fallback if a clip cannot be decoded
  const clips = {};
  function clip(a, kind) {
    const src = window.RA_SOUNDS && window.RA_SOUNDS[kind];
    if (!src) return null;
    if (!clips[kind]) {
      const bin = atob(src.slice(src.indexOf(",") + 1)), buf = new Uint8Array(bin.length);
      for (let i = 0; i < bin.length; i++) buf[i] = bin.charCodeAt(i);
      clips[kind] = new Promise((ok, bad) => a.decodeAudioData(buf.buffer, ok, bad)).catch(() => null);
    }
    return clips[kind];
  }
  function play(kind, delay) {
    const a = audio();
    if (!a) return;
    const c = clip(a, kind), at = a.currentTime + (delay || 0);
    if (c) {
      c.then((b) => {
        if (!b) return synth(a, kind);
        const s = a.createBufferSource(), g = a.createGain();
        s.buffer = b; g.gain.value = 0.9;
        s.connect(g).connect(a.destination); s.start(Math.max(at, a.currentTime));
      });
      return;
    }
    synth(a, kind);
  }
  function synth(a, kind) {
    const out = a.createGain(), t = a.currentTime + 0.01;
    out.gain.value = 0.6; out.connect(a.destination);
    if (kind === "pull") { scrape(a, out, t, 0.3, 650, 1700, 0.55); knock(a, out, t + 0.3, 0.32, 150); }
    if (kind === "open") flap(a, out, t, 0.32);
    if (kind === "shut") { flap(a, out, t, 0.26); knock(a, out, t + 0.42, 0.22, 120); }
    if (kind === "push") { scrape(a, out, t, 0.26, 1500, 600, 0.45); knock(a, out, t + 0.26, 0.4, 130); }
  }

  // ---------------- geometry ----------------
  // where a spine is on screen: its centre, size in screen pixels, rotation, and whether it lies flat
  function spineBox(g) {
    const r = g.querySelector("rect"), b = r.getBBox(), m = r.getScreenCTM();
    const c = new DOMPoint(b.x + b.width / 2, b.y + b.height / 2).matrixTransform(m);
    const s = Math.hypot(m.a, m.b);
    return { cx: c.x, cy: c.y, w: b.width * s, h: b.height * s, bx: b.x, by: b.y, bw: b.width, bh: b.height, s,
             angle: Math.atan2(m.b, m.a) * 180 / Math.PI, lying: b.width > b.height };
  }
  function layout() {
    const pw = Math.round(Math.max(230, Math.min(320, (innerWidth - 120) / 2)));
    const ph = Math.round(Math.min(innerHeight - 110, pw * 1.42));
    return { pw, ph, x: Math.round(innerWidth / 2 - pw), y: Math.round((innerHeight - ph) / 2) };
  }
  // a copy of the spine drawing, used while the book is in the air
  function spineFlier(g, box) {
    const pad = 1;
    const svg = document.createElementNS(NS, "svg");
    svg.setAttribute("viewBox", `${box.bx - pad} ${box.by - pad} ${box.bw + 2 * pad} ${box.bh + 2 * pad}`);
    svg.setAttribute("width", (box.bw + 2 * pad) * box.s);
    svg.setAttribute("height", (box.bh + 2 * pad) * box.s);
    const c = g.cloneNode(true);
    c.removeAttribute("tabindex"); c.removeAttribute("data-shelf-book"); c.style.visibility = "visible";
    svg.appendChild(c);
    const el = document.createElement("div");
    el.className = "ob-flier";
    el.appendChild(svg);
    const w = (box.bw + 2 * pad) * box.s, h = (box.bh + 2 * pad) * box.s;
    Object.assign(el.style, { left: `${box.cx - w / 2}px`, top: `${box.cy - h / 2}px`, width: `${w}px`, height: `${h}px` });
    return el;
  }
  function colours(g) {
    const rects = g.querySelectorAll("rect"), line = g.querySelector("line");
    return { fill: rects[0].getAttribute("fill"), dk: line ? line.getAttribute("stroke") : LINE, tint: rects[rects.length - 1].getAttribute("fill") };
  }
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  function coverHTML(col, cover) {
    return `<div class="ob-front" style="--c-fill:${col.fill};--c-dk:${col.dk};--c-tint:${col.tint}">
      <span class="ob-hinge"></span><span class="ob-band ob-band-top"></span><span class="ob-band ob-band-bot"></span>
      <div class="ob-label"><span class="ob-cover-title">${esc(cover.title)}</span><span class="ob-cover-rule"></span><span class="ob-cover-author">${esc(cover.author)}</span></div>
    </div>`;
  }

  // the outward pull: standing books slide up along their own length, lying books slide sideways out of the stack
  function pullVector(box) {
    if (box.lying) {
      const shelf = document.querySelector(".shelf"), sr = shelf ? shelf.getBoundingClientRect() : null;
      const dir = sr && box.cx > sr.left + sr.width / 2 ? -1 : 1;
      return [dir * 16, -2];
    }
    const a = box.angle * Math.PI / 180;
    return [Math.sin(a) * 14, -Math.cos(a) * 14];
  }
  const T = (tx, ty, r, ry, s) => `perspective(900px) translate(${tx}px, ${ty}px) rotateY(${ry}deg) rotate(${r}deg) scale(${s})`;
  const anim = (el, frames, ms, easing) => el.animate(frames, { duration: ms, easing, fill: "forwards" }).finished;

  // ---------------- open / close ----------------
  function build(opts, col, L) {
    const root = document.createElement("div");
    root.className = "ob";
    root.setAttribute("role", "dialog");
    root.setAttribute("aria-modal", "true");
    root.setAttribute("aria-label", opts.cover.title);
    root.innerHTML = `<div class="ob-backdrop"></div>
      <div class="ob-book">
      <div class="ob-tools">
        <button type="button" class="ob-tool ob-sound" aria-pressed="${soundOn()}"></button>
        <button type="button" class="ob-tool ob-close" aria-label="${esc(opts.labels.close)}" title="${esc(opts.labels.close)}">
          <svg viewBox="0 0 16 16" width="16" height="16" aria-hidden="true"><path d="M3.5 3.5l9 9M12.5 3.5l-9 9" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg></button>
      </div>
        <div class="ob-page ob-right"></div>
        <div class="ob-cover">${coverHTML(col, opts.cover)}<div class="ob-page ob-back"></div></div>
      </div>`;
    const book = root.querySelector(".ob-book");
    Object.assign(book.style, { left: `${L.x}px`, top: `${L.y}px`, width: `${2 * L.pw}px`, height: `${L.ph}px` });
    book.style.setProperty("--pw", `${L.pw}px`);
    return root;
  }
  function soundButton(btn, L) {
    const on = soundOn();
    btn.setAttribute("aria-pressed", String(on));
    btn.setAttribute("aria-label", on ? L.soundOn : L.soundOff);
    btn.title = on ? L.soundOn : L.soundOff;
    btn.innerHTML = `<svg viewBox="0 0 16 16" width="16" height="16" aria-hidden="true"><path d="M2.5 6h2.5l3.5-3v10l-3.5-3h-2.5z" fill="currentColor"/>${on
      ? `<path d="M10.8 5.6a3.2 3.2 0 0 1 0 4.8M12.6 3.9a5.6 5.6 0 0 1 0 8.2" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/>`
      : `<path d="M10.5 6l4 4M14.5 6l-4 4" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/>`}</svg>`;
  }

  async function open(g, opts) {
    if (cur) return;
    const a0 = audio();
    if (a0) ["pull", "open", "shut", "push"].forEach((k) => clip(a0, k));
    const box = spineBox(g), col = colours(g), L = layout();
    const root = build(opts, col, L);
    const book = root.querySelector(".ob-book"), cover = root.querySelector(".ob-cover"), right = root.querySelector(".ob-right"), back = root.querySelector(".ob-back");
    const state = cur = { id: opts.id, opts, root, box, L, busy: true, from: document.activeElement };
    const fill = (l, r) => { back.innerHTML = l; right.innerHTML = r; };
    fill(opts.left, opts.right);
    const api = { update: fill, close: (fast) => close(fast) };
    state.api = api;
    const sb = root.querySelector(".ob-sound");
    soundButton(sb, opts.labels);
    root.addEventListener("click", (e) => {
      if (state.busy) return;
      if (e.target.closest(".ob-close") || e.target.classList.contains("ob-backdrop")) return close();
      if (e.target.closest(".ob-sound")) { setSound(!soundOn()); return soundButton(sb, opts.labels); }
      opts.onClick(e, api);
    });
    root.addEventListener("input", (e) => opts.onInput && opts.onInput(e));
    root.addEventListener("keydown", (e) => {
      if (e.key === "Escape") { e.preventDefault(); if (!state.busy) close(); return; }
      if (e.key !== "Tab") return;
      const f = [...root.querySelectorAll("button, a[href], textarea, input, [tabindex='0']")].filter((x) => x.offsetParent !== null);
      if (!f.length) return;
      if (e.shiftKey && document.activeElement === f[0]) { e.preventDefault(); f[f.length - 1].focus(); }
      else if (!e.shiftKey && document.activeElement === f[f.length - 1]) { e.preventDefault(); f[0].focus(); }
    });

    g.style.visibility = "hidden";
    if (reduce) {
      root.classList.add("is-open");
      document.body.appendChild(root);
      await anim(root, [{ opacity: 0 }, { opacity: 1 }], 160, "ease-out");
      state.busy = false;
      root.querySelector(".ob-close").focus();
      return;
    }
    // 1. slide out of the shelf
    play("pull");
    const flier = spineFlier(g, box);
    document.body.appendChild(flier);
    const [px, py] = pullVector(box);
    await anim(flier, [{ transform: T(0, 0, box.angle, 0, 1), filter: "drop-shadow(0 0 0 rgba(43,52,60,0))" },
                       { transform: T(px, py, box.angle, 0, 1.06), filter: "drop-shadow(0 6px 8px rgba(43,52,60,.28))" }], 300, "cubic-bezier(.3,.7,.4,1)");
    // 2. turn edge-on while flying halfway to the middle, then the cover turns to face us as it lands
    root.style.visibility = "hidden";
    document.body.appendChild(root);
    const endX = L.x + L.pw * 1.5 - L.pw / 2, endY = L.y + L.ph / 2;   // centre of the closed book (spread shifted half a page left)
    const midX = (box.cx + px + endX) / 2, midY = (box.cy + py + endY) / 2;
    const upright = box.lying ? 90 : 0;
    const spineLen = Math.max(box.w, box.h), k1 = Math.min(2.2, (L.ph * 0.6) / spineLen);
    const backdrop = root.querySelector(".ob-backdrop");
    backdrop.style.opacity = "0";
    root.style.visibility = "visible";
    book.style.visibility = "hidden";
    backdrop.animate([{ opacity: 0 }, { opacity: 1 }], { duration: 520, easing: "ease-out", fill: "forwards" });
    await anim(flier, [{ transform: T(px, py, box.angle, 0, 1.06) }, { transform: T(midX - box.cx, midY - box.cy, upright, 90, k1) }], 260, "cubic-bezier(.5,0,.9,.6)");
    flier.remove();
    book.style.visibility = "visible";
    book.style.transform = `translateX(${-L.pw / 2}px)`;
    const kc = (spineLen * k1) / L.ph;
    const coverX = L.x + L.pw * 1.5 - L.pw / 2, coverY = L.y + L.ph / 2;   // where the cover's centre sits once landed
    right.style.visibility = "hidden";
    cover.style.transformOrigin = "50% 50%";
    await anim(cover, [{ transform: `perspective(900px) translate(${midX - coverX}px, ${midY - coverY}px) rotateY(-90deg) scale(${kc})` },
                       { transform: "perspective(900px) translate(0, 0) rotateY(0deg) scale(1)" }], 320, "cubic-bezier(.15,.6,.35,1)");
    right.style.visibility = "visible";
    cover.getAnimations().forEach((a) => a.cancel());
    cover.style.transformOrigin = "";
    // 3. the cover swings open and the spread slides to the centre
    play("open");
    await Promise.all([
      anim(cover, [{ transform: "rotateY(0deg)" }, { transform: "rotateY(-180deg)" }], 700, "cubic-bezier(.45,.05,.3,1)"),
      anim(book, [{ transform: `translateX(${-L.pw / 2}px)` }, { transform: "translateX(0)" }], 700, "cubic-bezier(.45,.05,.3,1)"),
    ]);
    root.classList.add("is-open");
    cover.getAnimations().forEach((a) => a.cancel()); book.getAnimations().forEach((a) => a.cancel());
    book.style.transform = "";
    state.busy = false;
    root.querySelector(".ob-close").focus();
  }

  function findSpine(id) {
    return [...document.querySelectorAll("#reader [data-shelf-book]")].find((x) => x.dataset.shelfBook === id) || null;
  }
  async function close(fast) {
    const state = cur;
    if (!state || state.busy) return;
    state.busy = true;
    const { root, L, opts } = state;
    const book = root.querySelector(".ob-book"), cover = root.querySelector(".ob-cover"), right = root.querySelector(".ob-right");
    const backdrop = root.querySelector(".ob-backdrop");
    const finish = (g) => {
      root.remove();
      if (g) g.style.visibility = "";
      cur = null;
      if (opts.onClose) opts.onClose();
      const again = findSpine(state.id);
      if (!fast && again) again.focus({ preventScroll: true });
    };
    if (fast || reduce) {
      await anim(root, [{ opacity: 1 }, { opacity: 0 }], fast ? 180 : 160, "ease-in");
      return finish(findSpine(state.id));
    }
    // 1. the cover shuts and the closed book slides back to the middle
    root.classList.remove("is-open");
    play("shut", 0.5);   // the thump lands as the cover meets the pages
    await Promise.all([
      anim(cover, [{ transform: "rotateY(-180deg)" }, { transform: "rotateY(0deg)" }], 600, "cubic-bezier(.45,.05,.3,1)"),
      anim(book, [{ transform: "translateX(0)" }, { transform: `translateX(${-L.pw / 2}px)` }], 600, "cubic-bezier(.45,.05,.3,1)"),
    ]);
    const g = findSpine(state.id);
    backdrop.animate([{ opacity: 1 }, { opacity: 0 }], { duration: 480, easing: "ease-in", fill: "forwards" });
    if (!g) {   // the book has left the shelf (unfavourited, or the shelf is on another page): just let it fade
      await anim(book, [{ opacity: 1, transform: `translateX(${-L.pw / 2}px)` }, { opacity: 0, transform: `translateX(${-L.pw / 2}px) scale(.9)` }], 300, "ease-in");
      return finish(null);
    }
    const box = spineBox(g);
    const [px, py] = pullVector(box);
    const endX = L.x + L.pw, endY = L.y + L.ph / 2;
    const midX = (box.cx + px + endX) / 2, midY = (box.cy + py + endY) / 2;
    const upright = box.lying ? 90 : 0;
    const spineLen = Math.max(box.w, box.h), k1 = Math.min(2.2, (L.ph * 0.6) / spineLen), kc = (spineLen * k1) / L.ph;
    // 2. the cover turns edge-on as it leaves, the spine turns back towards us on its way to the gap
    right.style.visibility = "hidden";
    cover.getAnimations().forEach((a) => a.cancel());
    cover.style.transformOrigin = "50% 50%";
    await anim(cover, [{ transform: `perspective(900px) translateX(0) rotateY(0deg) scale(1)` },
                       { transform: `perspective(900px) translate(${midX - endX}px, ${midY - endY}px) rotateY(-90deg) scale(${kc})` }], 260, "cubic-bezier(.5,0,.9,.6)");
    book.style.visibility = "hidden";
    const flier = spineFlier(g, box);
    flier.style.transform = T(midX - box.cx, midY - box.cy, upright, 90, k1);
    document.body.appendChild(flier);
    await anim(flier, [{ transform: T(midX - box.cx, midY - box.cy, upright, 90, k1) }, { transform: T(px, py, box.angle, 0, 1.06), filter: "drop-shadow(0 6px 8px rgba(43,52,60,.28))" }], 320, "cubic-bezier(.15,.6,.35,1)");
    // 3. slide it back into its gap
    play("push");
    await anim(flier, [{ transform: T(px, py, box.angle, 0, 1.06), filter: "drop-shadow(0 6px 8px rgba(43,52,60,.28))" },
                       { transform: T(0, 0, box.angle, 0, 1), filter: "drop-shadow(0 0 0 rgba(43,52,60,0))" }], 260, "cubic-bezier(.5,0,.7,1)");
    flier.remove();
    finish(g);
  }

  // keep the open spread centred if the window changes size
  window.addEventListener("resize", () => {
    if (!cur || cur.busy) return;
    const L = cur.L = layout(), book = cur.root.querySelector(".ob-book");
    Object.assign(book.style, { left: `${L.x}px`, top: `${L.y}px`, width: `${2 * L.pw}px`, height: `${L.ph}px` });
    book.style.setProperty("--pw", `${L.pw}px`);
  });
  // after the shelf is redrawn (a button pressed inside the open book), keep the open book's gap empty
  function hideSpine(root) {
    if (!cur) return;
    const g = [...root.querySelectorAll("[data-shelf-book]")].find((x) => x.dataset.shelfBook === cur.id);
    if (g) g.style.visibility = "hidden";
  }
  return { open, close: (fast) => close(fast), hideSpine, isOpen: () => !!cur, play };
})();
