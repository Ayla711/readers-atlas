"""Patch 4 (11-24 evening): drop v1 commentary from notes (cut-off talk such as "N 分", "只收这本", "进前十 → 请你定", "见名额说明").
Under rule v2 these no longer decide anything; the v1 decision itself stays in the 初稿 column for comparison.
Run after p3: python3 -I verify/p4_notes.py"""
import sys, os, re
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import specio
BAD = re.compile(r"(请你定|名额说明|前十|^\d+ 分|，\d+ 分|\d+ 分不|同分|只收这本|见说明|得分最高的一本|^换成|^0 分|^1 分|^2 分|^3 分|^4 分|^5 分|^7 分)")
total = 0
for cc in "au nz eg za ng dz ma ke fi hu is tr ua ro nl be ch dk no se".split():
    S = specio.load(cc)
    for j, (t, a, k, p, d, n) in enumerate(S["rows"]):
        segs = [s for s in re.split("；", n) if s]
        keep = [s for s in segs if ("v2" in s) or not BAD.search(s.strip())]
        # one D figure is enough
        dd = [s for s in keep if re.fullmatch(r"D \d+", s.strip())]
        if dd and any(re.search(r"D \d+ ·", s) for s in keep): keep = [s for s in keep if s not in dd]
        new = "；".join(keep)
        if new != n:
            total += 1; S["rows"][j] = (t, a, k, p, d, new)
    specio.save(cc, S)
print("notes cleaned:", total)
# (11-24) three Goodreads figures in p1 notes replaced by the fuller p2 re-query: Nuptials -> Noces 2,380; Memories of My Boyhood 7,169; A Dunánál 25 (done by hand, see PROGRESS.md)
