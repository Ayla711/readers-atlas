"""Build tools/selection/<cc>.json and <cc>.md from spec_<cc>.py (run inside tools/selection:
python3 -I build.py spec_au.py). Rule v2 (11-24, see docs/selection-rubric.md):
- score = sum of points; signals: each A list separately, B, C (prize, Nobel), I (BK world library, D thegreatestbooks), E (Goodreads)
- a book qualifies when it has >= 2 signals, or is in the top 10 of an A list (A value 4)
- new book: qualifies -> add, else not added
- book already in the app: qualifies -> keep; 1 category -> keep (flagged); 0 -> user decides (11-24: user agreed to delete the zero-evidence books
  left after the re-check; the spec marks them 用户同意删); never deleted on score alone
- same author: every qualifying book is taken
- rows marked by hand as not about this country / no real place are left as written
existing.json (tools/selection/make_existing.py, from data/) tells which books are already in the app; books in the app with no row are
listed as unscored, except books another country holds and books shown only at a writer's house or memorial (see rubric section 11)."""
import json, sys, re, os
CATS = {"A": "A", "B": "B", "C": "C", "N": "C", "BK": "I", "D": "I", "E": "E", "EP": "E"}
def cat(k): return k if k.startswith("A") else CATS.get(k, k)
def norm(s): return re.sub(r"[^a-z0-9]", "", s.lower())
def build(spec):
    cc = spec["cc"]
    ex = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "existing.json"), encoding="utf-8")).get(cc, [])
    alias = spec.get("existing_alias", {})
    used = set(); rows = []
    for t, a, kind, pts, dec, note in spec["rows"]:
        hit = None
        if t in alias:
            hit = alias[t]
            for h in (hit if isinstance(hit, list) else [hit]): used.add(h)
        else:
            for b in ex:
                if b.get("title") and (norm(b["title"]) == norm(t) or (norm(b["title"]) in norm(t) and len(norm(b["title"])) > 5) or (norm(t) in norm(b["title"]) and len(norm(t)) > 5)):
                    hit = b["id"]; break
        if hit and not isinstance(hit, list): used.add(hit)
        cats = sorted({cat(k) for k, v in pts.items() if v})
        q = len(cats) >= 2 or any(k.startswith("A") and v >= 4 for k, v in pts.items())
        manual = ("不算" in dec) or ("没有真实地点" in dec) or ("没有真实地点" in note and "不收" in dec)
        unver = "未核" in note or "未查" in note
        if manual: new = dec
        elif hit:
            new = "保留" if q else ("保留（只有一类证据）" if cats else ("删除（零项，复核后用户同意删）" if "用户同意删" in dec else "你定（零分）"))
            if not q and unver: new += "；数据未核，先核"
        else:
            new = "新增" if q else ("不收；数据未核，先核" if unver else "不收")
        rows.append(dict(title=t, author=a, kind=kind, points=pts, score=sum(pts.values()), cats=cats,
                         in_app=(", ".join(hit) if isinstance(hit, list) else hit), decision=new, first_draft=dec, note=note))
    for b in ex:
        if b["id"] not in used:
            other = b.get("home") != cc
            house = "line" not in b.get("via", ["line"])   # shown here only at a writer's house or memorial
            rows.append(dict(title=b.get("title"), author=b.get("author"), kind="他国书目" if other else ("作家故居" if house else "本国"),
                             points={}, score=0, cats=[], in_app=b["id"],
                             decision=("属于 %s 的书，挂在这里，不在此评" % b.get("home")) if other else
                                      ("作家故居、纪念地标注的代表作，不按选书规则评" if house else "未评（要补评）"),
                             first_draft="", note=""))
    out = dict(cc=cc, name=spec["name"], date=spec["date"], rule="v2", sources=spec["sources"], size_note=spec["size_note"], rows=rows)
    json.dump(out, open(cc + ".json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    L = [f"# {spec['name']} 选书评分（{spec['date']}，规则 v2）", "", "## 来源", ""]
    for k, v in spec["sources"].items(): L.append(f"- **{k}** {v}")
    L += ["", "## 候选与得分", "", "证据项：每份本国书单（A1、A2……）各算一项，另有 B 课本与全集、C 奖项（含诺贝尔）、I 国际经典（世界文库、thegreatestbooks）、E 读者面（Goodreads）。有两项以上，或进某份 A 名单前 10，就够线。", "",
          "| # | 书 | 作者 | 类 | 明细 | 分 | 证据项 | 已在应用里 | 处理（v2） | v1 初稿（作废，仅供对照） | 说明 |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    order = lambda r: (r["kind"] == "他国书目", "不算" in r["decision"], not r["kind"].startswith("本国"), -len(r["cats"]), -r["score"])
    for i, r in enumerate(sorted(rows, key=order), 1):
        det = " ".join(f"{k}{v:+d}" for k, v in r["points"].items() if v)
        L.append(f"| {i} | {r['title']} | {r['author']} | {r['kind']} | {det} | {r['score']} | {len(r['cats'])} | {'是' if r['in_app'] else ''} | {r['decision']} | {r['first_draft']} | {r['note']} |")
    L += ["", "## 说明", spec["size_note"], ""]
    open(cc + ".md", "w", encoding="utf-8").write("\n".join(L))
if __name__ == "__main__":
    import importlib.util
    s = importlib.util.spec_from_file_location("s", sys.argv[1]); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); build(m.SPEC)
