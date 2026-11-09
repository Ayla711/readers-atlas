"""WAVE-style accessibility self-check (WebAIM WAVE's error and alert rules, re-implemented for a headless run, since the
WAVE extension needs a browser session). Runs the same views as check_contrast.py, in both languages, and prints every
rule hit once with an example. Usage: python3 -I check_wave.py <app_dir>"""
import json, sys
from playwright.sync_api import sync_playwright
APP = sys.argv[1]

JS = r"""
() => {
  const out = [];
  const add = (kind, rule, el, note) => out.push({kind, rule, el: el ? describe(el) : "", note: note || ""});
  const describe = el => {
    if (!el || !el.tagName) return String(el);
    let s = el.tagName.toLowerCase();
    if (el.id) s += "#" + el.id;
    const c = (typeof el.className === "string" ? el.className : (el.getAttribute && el.getAttribute("class")) || "").trim().split(/\s+/).filter(Boolean).slice(0, 2);
    if (c.length) s += "." + c.join(".");
    const t = (el.textContent || "").trim().replace(/\s+/g, " ").slice(0, 40);
    return s + (t ? ` “${t}”` : "");
  };
  const visible = el => { let e = el; while (e && e.nodeType === 1) { const s = getComputedStyle(e); if (s.display === "none" || s.visibility === "hidden") return false; e = e.parentElement; } return true; };
  const hiddenFromAT = el => { let e = el; while (e && e.nodeType === 1) { if (e.getAttribute("aria-hidden") === "true") return true; e = e.parentElement; } return !visible(el); };
  const accName = el => {
    const lb = el.getAttribute("aria-labelledby");
    if (lb) { const t = lb.split(/\s+/).map(id => document.getElementById(id)).filter(Boolean).map(e => e.textContent.trim()).join(" ").trim(); if (t) return t; }
    const al = el.getAttribute("aria-label"); if (al && al.trim()) return al.trim();
    if (el.id) { const l = document.querySelector(`label[for="${CSS.escape(el.id)}"]`); if (l && l.textContent.trim()) return l.textContent.trim(); }
    const pl = el.closest && el.closest("label"); if (pl && pl.textContent.trim()) return pl.textContent.trim();
    const imgs = [...el.querySelectorAll("img[alt], svg title")].map(i => i.tagName === "IMG" ? i.getAttribute("alt") : i.textContent).join(" ").trim(); if (imgs) return imgs;
    const own = (el.textContent || "").trim(); if (own) return own;
    const t = el.getAttribute("title"); if (t && t.trim()) return t.trim();
    if (el.tagName === "INPUT" && ["submit","reset","button"].includes(el.type) && el.value) return el.value;
    if (el.tagName === "INPUT" && el.type === "image" && el.alt) return el.alt;
    return "";
  };
  // ---- document
  if (!document.documentElement.getAttribute("lang")) add("error", "Document language missing", document.documentElement);
  if (!document.title.trim()) add("error", "Missing or empty page title", null);
  if (!document.querySelector("main, [role=main]")) add("alert", "No main landmark", null);
  // ---- images
  for (const img of document.querySelectorAll("img")) {
    if (!visible(img)) continue;
    const alt = img.getAttribute("alt");
    const linked = img.closest("a, button");
    if (alt === null) add("error", linked ? "Linked image missing alternative text" : "Missing alternative text", img, img.getAttribute("src"));
    else if (alt.trim() === "" && linked && !accName(linked)) add("error", "Linked image missing alternative text", img);
    else if (alt && /\.(jpe?g|png|gif|svg)$|^(image|photo|picture|graphic|img)( of)?$/i.test(alt.trim())) add("alert", "Suspicious alternative text", img, alt);
    else if (alt && alt.length > 100) add("alert", "Long alternative text", img, alt.length + " chars");
    const near = img.parentElement && img.parentElement.textContent.replace(alt || "", "").trim();
    if (alt && near && near.toLowerCase().includes(alt.trim().toLowerCase()) && alt.trim().length > 12) add("alert", "Redundant alternative text", img, alt);
  }
  for (const svg of document.querySelectorAll("svg")) {
    if (!visible(svg) || hiddenFromAT(svg)) continue;
    if (svg.getAttribute("role") === "img" || svg.closest("button, a")) {
      if (!accName(svg) && !svg.querySelector("title") && !(svg.closest("button, a") && accName(svg.closest("button, a")))) add("error", "Inline SVG without accessible name", svg);
    } else if (!svg.getAttribute("role") && !svg.getAttribute("aria-label") && !svg.querySelector("title") && svg.getBoundingClientRect().width > 24) {
      add("alert", "Inline SVG with no role, title or aria-hidden", svg);
    }
  }
  // ---- links and buttons
  for (const a of document.querySelectorAll("a")) {
    if (!visible(a) || hiddenFromAT(a)) continue;
    const href = a.getAttribute("href");
    if (!accName(a)) add("error", "Empty link", a, href);
    if (href && href.startsWith("#") && href.length > 1 && !document.getElementById(decodeURIComponent(href.slice(1))) && !document.querySelector(`[name="${href.slice(1)}"]`)) add("alert", "Broken same-page link", a, href);
    if (!href || href === "#" || href.startsWith("javascript:")) add("alert", "Link without a real destination (should be a button?)", a);
    if (a.target === "_blank" && !/new (window|tab)|新窗口|新标签/i.test(a.getAttribute("title") || a.getAttribute("aria-label") || a.textContent)) add("alert", "Link opens new window without warning", a, href);
    const n = a.nextElementSibling; if (n && n.tagName === "A" && n.getAttribute("href") === href && href) add("alert", "Redundant link (adjacent, same destination)", a, href);
    if (a.getAttribute("title") && a.getAttribute("title").trim().toLowerCase() === (a.textContent || "").trim().toLowerCase()) add("alert", "Redundant title text", a);
    if (href && /\.pdf(\?|$)/i.test(href)) add("alert", "Link to PDF document", a, href);
  }
  for (const b of document.querySelectorAll("button, [role=button], input[type=button], input[type=submit], input[type=reset], input[type=image]")) {
    if (!visible(b) || hiddenFromAT(b)) continue;
    if (!accName(b)) add("error", "Empty button", b);
    if (b.getAttribute("title") && b.getAttribute("title").trim().toLowerCase() === (b.textContent || "").trim().toLowerCase()) add("alert", "Redundant title text", b);
  }
  // ---- forms
  for (const f of document.querySelectorAll("input:not([type=hidden]):not([type=button]):not([type=submit]):not([type=reset]):not([type=image]), select, textarea")) {
    if (!visible(f)) continue;
    const labels = f.id ? document.querySelectorAll(`label[for="${CSS.escape(f.id)}"]`).length : 0;
    if (!accName(f)) add("error", "Missing form label", f, f.type || f.tagName);
    else if (labels === 0 && !f.closest("label") && !f.getAttribute("aria-label") && !f.getAttribute("aria-labelledby") && f.getAttribute("title")) add("alert", "Form control labelled only by title", f);
    if (labels > 1) add("error", "Multiple form labels", f);
    if (f.placeholder && !f.id && !f.getAttribute("aria-label")) add("alert", "Placeholder used as the only label", f);
  }
  for (const l of document.querySelectorAll("label")) {
    if (!visible(l)) continue;
    const f = l.getAttribute("for");
    if (f && !document.getElementById(f)) add("alert", "Orphaned form label", l, "for=" + f);
    if (!f && !l.querySelector("input, select, textarea")) add("alert", "Orphaned form label", l);
  }
  const radios = {}; for (const r of document.querySelectorAll("input[type=radio]")) if (visible(r)) (radios[r.name] = radios[r.name] || []).push(r);
  for (const [name, rs] of Object.entries(radios)) if (rs.length > 1 && !rs[0].closest("fieldset") && !rs[0].closest("[role=radiogroup], [role=group]")) add("alert", "Missing fieldset for radio group", rs[0], name);
  // ---- headings
  const hs = [...document.querySelectorAll("h1,h2,h3,h4,h5,h6,[role=heading]")].filter(visible);
  if (!hs.length) add("alert", "No heading structure", null);
  if (hs.length && !hs.some(h => h.tagName === "H1" || h.getAttribute("aria-level") === "1")) add("alert", "Missing first level heading", null);
  let prev = 0;
  for (const h of hs) {
    const lv = h.tagName[0] === "H" ? +h.tagName[1] : +(h.getAttribute("aria-level") || 2);
    if (!h.textContent.trim() && !h.querySelector("img[alt]")) add("error", "Empty heading", h);
    if (prev && lv > prev + 1) add("alert", "Skipped heading level", h, `h${prev} → h${lv}`);
    prev = lv;
  }
  for (const p of document.querySelectorAll("p, div, span")) {
    if (!visible(p) || p.children.length) continue;
    const t = p.textContent.trim(); if (!t || t.length > 60) continue;
    const s = getComputedStyle(p); const fw = parseInt(s.fontWeight) || 400; const fs = parseFloat(s.fontSize);
    if (fs >= 20 && fw >= 600 && !p.closest("h1,h2,h3,h4,h5,h6,button,a,[role=heading],svg")) add("alert", "Possible heading (large bold text not marked up as heading)", p);
  }
  // ---- text
  const smallSeen = new Set();
  for (const el of document.querySelectorAll("body *")) {
    if (!visible(el) || hiddenFromAT(el)) continue;
    let own = ""; for (const n of el.childNodes) if (n.nodeType === 3) own += n.textContent; if (!own.trim()) continue;
    const s = getComputedStyle(el);
    const fs = parseFloat(s.fontSize);
    if (fs < 10 && !el.closest("svg")) { const k = describe(el).split(" “")[0]; if (!smallSeen.has(k)) { smallSeen.add(k); add("alert", "Very small text (< 10px)", el, fs + "px"); } }
    if (s.textAlign === "justify") add("alert", "Justified text", el);
    if (s.textDecorationLine.includes("underline") && !el.closest("a") && el.tagName !== "U" && el.tagName !== "INS") add("alert", "Underlined text that is not a link", el);
  }
  // ---- aria / keyboard
  for (const el of document.querySelectorAll("[aria-labelledby], [aria-describedby], [aria-controls], [aria-owns]")) {
    for (const attr of ["aria-labelledby", "aria-describedby", "aria-controls", "aria-owns"]) {
      const v = el.getAttribute(attr); if (!v) continue;
      for (const id of v.split(/\s+/)) if (!document.getElementById(id)) add("error", "Broken ARIA reference", el, `${attr}=${id}`);
    }
  }
  for (const el of document.querySelectorAll("[tabindex]")) { const t = +el.getAttribute("tabindex"); if (t > 0) add("alert", "Tabindex greater than 0", el, "tabindex=" + t); }
  for (const el of document.querySelectorAll("[aria-hidden=true]")) {
    if (el.matches("a[href], button, input, select, textarea, [tabindex]:not([tabindex='-1'])") || el.querySelector("a[href], button:not([disabled]), input, select, textarea, [tabindex]:not([tabindex='-1'])")) {
      if (visible(el)) add("error", "ARIA hidden element contains focusable content", el);
    }
  }
  for (const el of document.querySelectorAll("[role]")) {
    const r = el.getAttribute("role");
    const known = ["button","link","img","heading","list","listitem","dialog","alertdialog","alert","status","tab","tablist","tabpanel","navigation","main","region","banner","contentinfo","complementary","search","group","radiogroup","presentation","none","switch","checkbox","menu","menuitem","menubar","option","listbox","combobox","tooltip","progressbar","note","separator","toolbar","application","document","figure","form","log","marquee","math","grid","gridcell","row","rowgroup","columnheader","rowheader","table","cell","term","definition","article","feed","timer","slider","spinbutton","textbox","tree","treeitem","meter"];
    if (!known.includes(r)) add("error", "Invalid or unknown ARIA role", el, r);
    if (["tab","switch","checkbox","radio","menuitemcheckbox","option"].includes(r) && !el.hasAttribute("aria-selected") && !el.hasAttribute("aria-checked") && !el.hasAttribute("aria-pressed")) add("alert", `role=${r} without state attribute`, el);
    if (r === "button" && !el.matches("button, a, input, [tabindex]")) add("error", "role=button on an element that is not keyboard focusable", el);
    if (r === "dialog" && !el.getAttribute("aria-label") && !el.getAttribute("aria-labelledby")) add("alert", "Dialog without accessible name", el);
    if (r === "img" && !accName(el)) add("error", "role=img without accessible name", el);
  }
  for (const el of document.querySelectorAll("[onmouseover], [onmouseout], [onclick]")) {
    if (el.hasAttribute("onmouseover") && !el.hasAttribute("onfocus")) add("alert", "Device dependent event handler", el);
    if (el.hasAttribute("onclick") && !el.matches("a, button, input, select, textarea, [tabindex]")) add("alert", "Device dependent event handler (onclick on non-focusable)", el);
  }
  for (const el of document.querySelectorAll("[accesskey]")) add("alert", "Accesskey", el, el.getAttribute("accesskey"));
  for (const el of document.querySelectorAll("iframe")) if (!el.getAttribute("title")) add("error", "Frame missing title", el);
  for (const el of document.querySelectorAll("video, audio")) add("alert", "HTML5 media: check captions / transcript", el);
  if (document.querySelector("noscript")) add("alert", "Noscript element", document.querySelector("noscript"));
  for (const t of document.querySelectorAll("table")) {
    if (!visible(t)) continue;
    if (!t.querySelector("th")) add("alert", "Table without header cells (layout table?)", t);
    for (const th of t.querySelectorAll("th")) if (!th.textContent.trim()) add("error", "Empty table header", th);
  }
  // clickable things that are not focusable (WAVE flags these through onclick; we check listeners by class convention: cursor pointer)
  const ptrSeen = new Set();
  for (const el of document.querySelectorAll("body *")) {
    if (!visible(el)) continue;
    if (el.closest("svg")) continue;
    const s = getComputedStyle(el);
    if (s.cursor === "pointer" && !el.matches("a[href], button, input, select, textarea, label, summary, [tabindex], [role=button], [role=link]") && !el.closest("a[href], button, label, summary, [tabindex], [role=button]")) {
      const k = describe(el).split(" “")[0]; if (!ptrSeen.has(k)) { ptrSeen.add(k); add("alert", "Clickable element not keyboard focusable (cursor: pointer, no tabindex/role)", el); }
    }
  }
  // focus visibility: elements that remove outline without an alternative
  const fsSeen = new Set();
  for (const el of document.querySelectorAll("a[href], button, input, select, textarea, [tabindex]")) {
    if (!visible(el)) continue;
    el.focus({preventScroll: true});
    if (document.activeElement !== el) continue;
    const s = getComputedStyle(el);
    const noOutline = s.outlineStyle === "none" || parseFloat(s.outlineWidth) === 0;
    const noShadow = s.boxShadow === "none";
    if (noOutline && noShadow) { const k = describe(el).split(" “")[0]; if (!fsSeen.has(k)) { fsSeen.add(k); add("alert", "No visible focus indicator (keyboard)", el); } }
  }
  if (document.activeElement && document.activeElement.blur) document.activeElement.blur();
  // landmarks / skip link
  if (!document.querySelector("a[href^='#']:first-child, .skip-link, a.skip")) add("alert", "No skip link to main content", null);
  return out;
}
"""

VIEWS = [
    ("world", "#/", []), ("uk", "#/uk", []), ("region", "#/region/TLI", []), ("place", "#/place/tintagel-castle", []),
    ("book", "#/book/persuasion", []), ("book-orig", "#/book/sir-gawain-green-knight", ["click:.orig-toggle"]),
    ("author", "#/author/Jane%20Austen", []), ("travel", "#/travel", []), ("reading", "#/reading", []),
    ("search", "#/uk", ["fill:#search-input:Dickens"]), ("shelf", "#/reading", ["seed"]), ("open-book", "#/reading", ["seed", "click:.shelf-book"]),
    ("trip-dialog", "#/place/tintagel-castle", ["click:[data-act=trip], .btn-trip, button:has-text('itinerary'), button:has-text('行程')"]),
    ("journal-dialog", "#/travel", ["click:button:has-text('journal'), button:has-text('日志'), [data-act=journal]"]),
]
SEED = """() => { localStorage.setItem('ra.faves', JSON.stringify(['persuasion','jane-eyre','wuthering-heights']));
  localStorage.setItem('ra.wishlist', JSON.stringify(['baker-street'])); localStorage.setItem('ra.visited', JSON.stringify(['tintagel-castle']));
  localStorage.setItem('ra.shelf', JSON.stringify({'persuasion':'read','dracula':'want'})); }"""

def steps(pg, st):
    for s in st:
        try:
            if s == "seed": pg.evaluate(SEED); pg.reload(); pg.wait_for_timeout(1000)
            elif s.startswith("click:"):
                done = False
                for sel in s[6:].split(", "):
                    try: pg.click(sel, timeout=1500); done = True; break
                    except Exception: pass
                if not done: print("  (no element for)", s)
                pg.wait_for_timeout(1400)
            elif s.startswith("fill:"):
                _, sel, val = s.split(":", 2); pg.fill(sel, val); pg.wait_for_timeout(900)
        except Exception as e: print("  step failed:", s, str(e).split("\n")[0][:80])

agg = {}
with sync_playwright() as p:
    br = p.chromium.launch()
    for lang in ("en", "zh"):
        pg = br.new_page(viewport={"width": 1440, "height": 900})
        pg.goto(f"file://{APP}/index.html?intro=0#/uk"); pg.wait_for_timeout(900)
        if lang == "zh": pg.click("#lang-toggle"); pg.wait_for_timeout(700)
        for name, route, st in VIEWS:
            pg.goto(f"file://{APP}/index.html?intro=0{route}"); pg.wait_for_timeout(1300)
            steps(pg, st)
            rows = pg.evaluate(JS)
            print(f"{lang}/{name}: {sum(r['kind']=='error' for r in rows)} errors, {sum(r['kind']=='alert' for r in rows)} alerts")
            for r in rows:
                k = (r["kind"], r["rule"], r["el"].split(" “")[0], r["note"][:60])
                a = agg.setdefault(k, dict(r, views=[]))
                if f"{lang}/{name}" not in a["views"]: a["views"].append(f"{lang}/{name}")
        pg.close()
    br.close()

json.dump(list(agg.values()), open("wave.json", "w"), ensure_ascii=False, indent=1)
print("\n==== UNIQUE FINDINGS", len(agg))
for kind in ("error", "alert"):
    print(f"\n-- {kind.upper()}S")
    byrule = {}
    for k, a in agg.items():
        if a["kind"] == kind: byrule.setdefault(a["rule"], []).append(a)
    for rule, items in sorted(byrule.items(), key=lambda kv: -len(kv[1])):
        print(f"{rule}  ×{len(items)}")
        for a in items[:6]:
            print(f"    {a['el'][:90]}  {a['note'][:50]}  [{len(a['views'])} views]")
        if len(items) > 6: print(f"    … {len(items)-6} more")
