/* The Reader's Atlas — review page (R-11, 11-09). Rules: docs/review-rules.md.
   Loads every open country's data (js/data.js), lists the excerpts and scene notes, and records a decision per line
   (approve / reject with reasons and a note) in this browser under "ra.review". "导出审核结果" writes the decisions as
   JSON for tools/apply_review.py, which writes them back into the data. Nothing here changes the data files. */
(function () {
  "use strict";
  const KV = window.RA_STORE.kv;
  const OPEN = (window.RA_COUNTRIES || []).filter((c) => c.open);
  const REASONS = [
    ["passing", "地方没有分量"], ["cut", "选段截得不好"], ["location", "出处章节不对"], ["highlight", "高亮不对"],
    ["translation", "译文有问题"], ["place", "地点 / 坐标 / 说明不对"], ["scene-vague", "场景说明是概括"],
    ["scene-fact", "场景说明事实不对"], ["scene-wording", "用了原文措辞"], ["other", "其他"],
  ];
  const TYPE = { original: "原著地点", prototype: "原型地", pilgrimage: "作家朝圣", film_location: "影视取景" };
  const esc = (s) => String(s == null ? "" : s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  function highlight(text, terms) {
    let out = esc(text);
    for (const t of (terms || []).filter(Boolean).sort((a, b) => b.length - a.length)) {
      const e = esc(t).replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
      out = out.replace(new RegExp(e, "g"), "<mark>$&</mark>");
    }
    return out;
  }
  const linkify = (s) => esc(s).replace(/https?:\/\/[^\s,;)]+/g, (u) => `<a href="${u}" target="_blank" rel="noopener">${u.length > 60 ? u.slice(0, 57) + "…" : u}</a>`);
  const gutenbergLink = (checked) => {
    const m = /Gutenberg #(\d+)/.exec(checked || "");
    return m ? `<a href="https://www.gutenberg.org/ebooks/${m[1]}" target="_blank" rel="noopener">古登堡 #${m[1]}</a>` : esc(checked || "");
  };

  // ---------- state ----------
  let decisions = KV.get("review", {}); // line id -> { decision: "approve"|"reject", reasons: [], note, at, country }
  const save = () => KV.set("review", decisions);
  const lines = []; // { l, book, places, country }
  let shown = []; // filtered
  let cursor = 0;

  const $ = (id) => document.getElementById(id);
  const list = $("list");

  function load() {
    list.innerHTML = `<p class="rv-empty">正在加载 ${OPEN.map((c) => c.name_zh).join("、")} 的数据…</p>`;
    let chain = Promise.resolve();
    for (const cfg of OPEN) {
      chain = chain.then(() => window.RA_LOAD.load(cfg)).then(({ data }) => {
        const books = new Map(data.books.map((b) => [b.id, b]));
        const places = new Map(data.places.map((p) => [p.id, p]));
        for (const l of data.lines) lines.push({ l, book: books.get(l.book_id), places: l.place_ids.map((id) => places.get(id)).filter(Boolean), country: cfg });
        const o = document.createElement("option");
        o.value = cfg.code;
        o.textContent = cfg.name_zh;
        $("f-country").append(o);
      });
    }
    chain.then(render, (e) => { list.innerHTML = `<p class="rv-empty">加载失败：${esc(e.message)}</p>`; });
  }

  function statusOf(x) {
    const d = decisions[x.l.id];
    if (d) return d.decision; // approve | reject (this session)
    return x.l.status === "reviewed" ? "reviewed" : x.l.status === "rejected" ? "rejected" : "todo";
  }

  function filter() {
    const c = $("f-country").value, k = $("f-kind").value, st = $("f-status").value, q = $("f-q").value.trim().toLowerCase();
    shown = lines.filter((x) => {
      if (c && x.country.code !== c) return false;
      if (k && (k === "scene") !== (x.l.kind === "scene")) return false;
      if (st && statusOf(x) !== st) return false;
      if (q) {
        const hay = [x.l.id, x.l.text_en, x.l.text_zh, x.book && x.book.title, x.book && x.book.title_zh, x.book && x.book.author, x.book && x.book.author_zh,
          ...x.places.flatMap((p) => [p.id, p.name, p.name_zh])].join(" ").toLowerCase();
        if (!hay.includes(q)) return false;
      }
      return true;
    });
  }

  function progress() {
    const by = { todo: 0, approve: 0, reject: 0, reviewed: 0, rejected: 0 };
    for (const x of lines) by[statusOf(x)]++;
    const perCountry = OPEN.map((cfg) => {
      const xs = lines.filter((x) => x.country.code === cfg.code);
      const done = xs.filter((x) => statusOf(x) !== "todo").length;
      return `${esc(cfg.name_zh)} ${done}/${xs.length}`;
    }).join(" · ");
    $("progress").innerHTML = `<strong>${by.todo}</strong> 待审 · <strong>${by.approve}</strong> 本次通过 · <strong>${by.reject}</strong> 本次打回 · ${by.reviewed} 已通过 · ${by.rejected} 已打回<br><span>${perCountry}</span>`;
  }

  function card(x, i) {
    const l = x.l, b = x.book || {}, scene = l.kind === "scene";
    const d = decisions[l.id];
    const st = statusOf(x);
    const placesHTML = x.places.map((p) => `
      <li>
        <a class="rv-place" href="index.html?intro=0#/place/${encodeURIComponent(p.id)}" target="_blank" rel="noopener">${esc(p.name_zh)} · ${esc(p.name)}</a>
        <span class="rv-tag">${TYPE[p.place_type] || esc(p.place_type)}</span>
        <a class="rv-coord" href="https://www.openstreetmap.org/?mlat=${p.lat}&mlon=${p.lon}#map=14/${p.lat}/${p.lon}" target="_blank" rel="noopener">${p.lat}, ${p.lon}</a>
        ${p.note || p.prototype_of ? `<div class="rv-note">${esc(p.prototype_of ? "原型：" + p.prototype_of : p.note)}</div>` : ""}
        <div class="rv-src">坐标出处：${linkify(p.coord_checked || "")}</div>
      </li>`).join("");
    const reasons = REASONS.map(([code, label]) => `<label><input type="checkbox" value="${code}" ${d && d.reasons && d.reasons.includes(code) ? "checked" : ""}> ${label}</label>`).join("");
    return `
      <article class="rv-card is-${st}${i === cursor ? " is-cursor" : ""}" data-i="${i}" data-id="${esc(l.id)}" tabindex="-1">
        <header>
          <span class="rv-id">${esc(l.id)}</span>
          <span class="rv-tag">${scene ? "场景说明" : "摘句"}</span>
          <span class="rv-tag">${esc(x.country.name_zh)}</span>
          <span class="rv-status">${{ todo: "待审", approve: "本次通过", reject: "本次打回", reviewed: "已通过", rejected: "已打回" }[st]}</span>
        </header>
        <h2><a href="index.html?intro=0#/book/${encodeURIComponent(b.id || "")}" target="_blank" rel="noopener">${esc(b.title_zh || "")}</a>
          <span>${esc(b.title || "")} · ${esc(b.author_zh || "")} ${esc(b.author || "")} · ${esc(b.year || "")}${b.public_domain ? " · 公有领域" : " · 有版权"}</span></h2>
        <p class="rv-loc">${esc(l.location_zh)} · ${esc(l.location)}</p>
        <blockquote lang="en" class="${scene ? "is-scene" : ""}">${highlight(l.text_en, l.highlight_en)}</blockquote>
        ${l.text_zh ? `<blockquote lang="zh" class="is-zh">${highlight(l.text_zh, l.highlight_zh)}</blockquote>` : ""}
        ${l.text_orig ? `<details><summary>原文</summary><blockquote class="is-orig">${highlight(l.text_orig, l.highlight_orig)}</blockquote></details>` : ""}
        <p class="rv-src">${scene ? `情节依据：${linkify(l.fact_source || "（无）")}` : `原文核对：${gutenbergLink(l.checked)}${l.translation && l.translation !== "original" ? ` · 英译：${esc(l.translation)}` : ""}`}</p>
        <ul class="rv-places">${placesHTML}</ul>
        <div class="rv-decide">
          <button type="button" class="ok" data-act="approve">通过 <kbd>A</kbd></button>
          <button type="button" class="no" data-act="reject">打回 <kbd>R</kbd></button>
          ${d ? `<button type="button" class="undo" data-act="undo">撤销 <kbd>U</kbd></button>` : ""}
        </div>
        <div class="rv-why"${st === "reject" ? "" : " hidden"}>
          <div class="rv-reasons">${reasons}</div>
          <textarea placeholder="备注：哪里不对、建议怎么改（小改直接写“小改：……”）" rows="2">${esc(d && d.note || "")}</textarea>
        </div>
      </article>`;
  }

  function render(keepCursor) {
    filter();
    if (!keepCursor) cursor = 0;
    cursor = Math.min(cursor, Math.max(0, shown.length - 1));
    progress();
    list.innerHTML = shown.length ? shown.map(card).join("") : `<p class="rv-empty">这个筛选下没有条目。</p>`;
  }

  function decide(i, act) {
    const x = shown[i];
    if (!x) return;
    const node = list.querySelector(`[data-i="${i}"]`);
    if (act === "undo") delete decisions[x.l.id];
    else {
      const prev = decisions[x.l.id] || {};
      decisions[x.l.id] = { decision: act, reasons: act === "reject" ? prev.reasons || [] : [], note: act === "reject" ? prev.note || "" : "", at: new Date().toISOString(), country: x.country.code };
    }
    save();
    const st = statusOf(x);
    // re-render this card only; the filter may now exclude it, but it stays until the next filter change
    node.outerHTML = card(x, i);
    progress();
    const fresh = list.querySelector(`[data-i="${i}"]`);
    if (act === "reject") { const ta = fresh.querySelector("textarea"); ta.focus(); }
    else if (act === "approve") move(1);
    return st;
  }
  function move(d) {
    cursor = Math.max(0, Math.min(shown.length - 1, cursor + d));
    for (const n of list.querySelectorAll(".rv-card")) n.classList.toggle("is-cursor", Number(n.dataset.i) === cursor);
    const n = list.querySelector(`[data-i="${cursor}"]`);
    if (n) n.scrollIntoView({ block: "center", behavior: "smooth" });
  }

  list.addEventListener("click", (e) => {
    const c = e.target.closest(".rv-card");
    if (!c) return;
    cursor = Number(c.dataset.i);
    for (const n of list.querySelectorAll(".rv-card")) n.classList.toggle("is-cursor", n === c);
    const b = e.target.closest("[data-act]");
    if (b) decide(cursor, b.dataset.act);
  });
  list.addEventListener("change", (e) => {
    const c = e.target.closest(".rv-card");
    if (!c || !e.target.matches(".rv-reasons input")) return;
    const d = decisions[c.dataset.id];
    if (!d) return;
    d.reasons = [...c.querySelectorAll(".rv-reasons input:checked")].map((x) => x.value);
    save();
  });
  list.addEventListener("input", (e) => {
    const c = e.target.closest(".rv-card");
    if (!c || !e.target.matches("textarea")) return;
    const d = decisions[c.dataset.id];
    if (!d) return;
    d.note = e.target.value;
    save();
  });
  document.addEventListener("keydown", (e) => {
    if (e.target.closest("input, textarea, select") || e.metaKey || e.ctrlKey || e.altKey) return;
    const k = e.key.toLowerCase();
    if (k === "j") { e.preventDefault(); move(1); }
    else if (k === "k") { e.preventDefault(); move(-1); }
    else if (k === "a") { e.preventDefault(); decide(cursor, "approve"); }
    else if (k === "r") { e.preventDefault(); decide(cursor, "reject"); }
    else if (k === "u") { e.preventDefault(); decide(cursor, "undo"); }
  });
  for (const id of ["f-country", "f-kind", "f-status"]) $(id).addEventListener("change", () => render());
  $("f-q").addEventListener("input", () => render());

  $("export").addEventListener("click", () => {
    const n = Object.keys(decisions).length;
    if (!n) { alertMsg("还没有任何决定。"); return; }
    const out = { app: "readers-atlas-review", version: 1, exported_at: new Date().toISOString(), decisions };
    const blob = new Blob([JSON.stringify(out, null, 1)], { type: "application/json" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    const t = new Date(), day = `${t.getFullYear()}-${String(t.getMonth() + 1).padStart(2, "0")}-${String(t.getDate()).padStart(2, "0")}`; // local date
    out.day = day;
    a.download = `review-decisions-${day}.json`;
    document.body.append(a); a.click(); a.remove();
    setTimeout(() => URL.revokeObjectURL(a.href), 2000);
  });
  $("import").addEventListener("change", async (e) => {
    const f = e.target.files[0];
    e.target.value = "";
    if (!f) return;
    try {
      const data = JSON.parse(await f.text());
      if (data.app !== "readers-atlas-review") throw new Error("不是审核结果文件");
      decisions = Object.assign({}, decisions, data.decisions);
      save();
      render(true);
    } catch (err) { alertMsg("导入失败：" + err.message); }
  });
  function alertMsg(m) {
    const p = $("progress");
    const s = document.createElement("div");
    s.className = "rv-msg";
    s.textContent = m;
    p.append(s);
    setTimeout(() => s.remove(), 4000);
  }

  load();
})();
