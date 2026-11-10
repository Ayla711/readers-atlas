"""Write review decisions (exported from review.html) back into the data (R-11). Rules: docs/review-rules.md.

Usage: python3 -I tools/apply_review.py reviews/review-decisions-<date>.json [--app .] [--dry-run]

For each decision:
  approve -> status "reviewed"
  reject  -> status "rejected" (the atlas stops showing the line), reasons and note go to docs/review-log.md, and for a
             country imported from a content pack also to packs/<country>/REJECTED-<date>.md for whoever produced it
The status is changed in data/<country>/lines.js and, when the country came from a pack, in packs/<country>/lines.json
too, so a re-import keeps it. A line whose status already matches is left alone.
"""
import argparse
import datetime
import json
import os
import re
import subprocess
import sys

ap = argparse.ArgumentParser()
ap.add_argument("decisions")
ap.add_argument("--app", default=".")
ap.add_argument("--dry-run", action="store_true")
A = ap.parse_args()
APP = os.path.abspath(A.app)
doc = json.load(open(A.decisions, encoding="utf-8"))
if doc.get("app") != "readers-atlas-review":
    sys.exit("not a review decisions file")
D = doc["decisions"]
day = doc.get("day") or (doc.get("exported_at") or datetime.date.today().isoformat())[:10]  # the reviewer's local date
REASONS = {"passing": "地方没有分量", "cut": "选段截得不好", "location": "出处章节不对", "highlight": "高亮不对",
           "translation": "译文有问题", "place": "地点 / 坐标 / 说明不对", "scene-vague": "场景说明是概括",
           "scene-fact": "场景说明事实不对", "scene-wording": "用了原文措辞", "other": "其他"}
NEW = {"approve": "reviewed", "reject": "rejected"}

countries = json.loads(subprocess.check_output(["node", "-e", "global.window={};require('./data/countries.js');console.log(JSON.stringify(window.RA_COUNTRIES))"], cwd=APP))
by_country = {}
for lid, d in D.items():
    by_country.setdefault(d.get("country"), {})[lid] = d

log_rows, changed, missing = [], 0, []
for code, ds in by_country.items():
    path = os.path.join(APP, "data", code, "lines.js")
    if not os.path.exists(path):
        missing += list(ds)
        continue
    s = open(path, encoding="utf-8").read()
    books = {}
    bpath = os.path.join(APP, "data", code, "books.js")
    for m in re.finditer(r'\{ id: "([^"]+)", title: "([^"]*)"', open(bpath, encoding="utf-8").read()):
        books[m.group(1)] = m.group(2)
    pack = os.path.join(APP, "packs", code, "lines.json")
    pack_lines = json.load(open(pack, encoding="utf-8")) if os.path.exists(pack) else None
    pack_by_id = {l["id"]: l for l in pack_lines} if pack_lines else {}
    rejected_for_pack = []
    for lid, d in ds.items():
        new = NEW.get(d.get("decision"))
        if not new:
            continue
        m = re.search(r'(\{ id: "' + re.escape(lid) + r'",[^\n]*?status: ")(draft|reviewed|rejected)(")', s)
        if not m:
            missing.append(lid)
            continue
        if m.group(2) != new:
            s = s[:m.start(2)] + new + s[m.end(2):]
            changed += 1
        if lid in pack_by_id:
            pack_by_id[lid]["status"] = new
        book = books.get(re.search(r'book_id: "([^"]+)"', s[m.start():m.start() + 400]).group(1), "")
        if d["decision"] == "reject":
            why = "、".join(REASONS.get(r, r) for r in d.get("reasons", [])) or "（未勾原因）"
            note = (d.get("note") or "").replace("\n", " ").replace("|", "／")
            log_rows.append(f"| {day} | {code} | `{lid}` | {book} | 打回 | {why} | {note} |")
            rejected_for_pack.append((lid, book, why, note))
        else:
            log_rows.append(f"| {day} | {code} | `{lid}` | {book} | 通过 | | |")
    if A.dry_run:
        continue
    open(path, "w", encoding="utf-8").write(s)
    if pack_lines is not None:
        open(pack, "w", encoding="utf-8").write(json.dumps(pack_lines, ensure_ascii=False, indent=2) + "\n")
        if rejected_for_pack:
            out = os.path.join(APP, "packs", code, f"REJECTED-{day}.md")
            with open(out, "w", encoding="utf-8") as fh:
                fh.write(f"# 审核打回 · {day}\n\n这些条目在网站上已不再显示。请按原因修改后在下一批里重交（保留同一个 id，status 改回 draft），或换成新条目。规则见 `docs/review-rules.md`。\n\n| id | 书 | 原因 | 备注 |\n|---|---|---|---|\n")
                for lid, book, why, note in rejected_for_pack:
                    fh.write(f"| `{lid}` | {book} | {why} | {note} |\n")
            print("wrote", os.path.relpath(out, APP))

log = os.path.join(APP, "docs", "review-log.md")
if not A.dry_run and log_rows:
    if not os.path.exists(log):
        open(log, "w", encoding="utf-8").write("# 审核记录\n\n由 `tools/apply_review.py` 追加，规则见 `docs/review-rules.md`。\n\n| 日期 | 国家 | id | 书 | 决定 | 原因 | 备注 |\n|---|---|---|---|---|---|---|\n")
    open(log, "a", encoding="utf-8").write("\n".join(log_rows) + "\n")
print(f"{len(D)} decisions · {changed} status changes · {sum('打回' in r for r in log_rows)} rejected" + (" (dry run, nothing written)" if A.dry_run else ""))
if missing:
    print("not found (skipped):", ", ".join(missing))
