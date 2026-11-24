"""Patch 8 (11-24, audit of the re-check by a second pass):
1. thegreatestbooks ranks matched by TITLE over the whole top 2000 (p2 matched title + author surname and missed spelling variants):
   Camera Obscura 1490 (listed under Nicolaas Beets), Reynard the Fox 864, Swiss Family Robinson 1805. No decision changes.
2. Finland: the print-run ranking (Niemi) is readership evidence, not a list anyone chose, so it moves from A2 to EP (category E, 2 points
   for the top 16). Books that had only that evidence are no longer added.
3. Container rule: a short piece with no entry of its own is measured by the collection it was published in.
   The Final Problem: The Memoirs of Sherlock Holmes (Goodreads 109,080), The Complete Sherlock Holmes (rank 209) -> kept.
   Stranger in the Village: Notes of a Native Son (Goodreads 26,150) -> kept, one evidence item.
   Babette's Feast: Anecdotes of Destiny (Goodreads 2,289) -> still zero.
Run in tools/selection: python3 -I verify/p8_audit_1124.py, then build all, then verify/p7_size_notes.py, then build all."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import specio
def upd(cc, t, add=None, note_add=None, dec=None, drop=None):
    S = specio.load(cc); r = next(x for x in S["rows"] if x[0] == t); p = dict(r[3])
    for k in drop or []: p.pop(k, None)
    p.update(add or {})
    specio.setrow(S, t, pts=p, note=(r[5] + "；" + note_add) if note_add else None, dec=dec); specio.save(cc, S)
upd("nl", "Camera Obscura", {"D": 1}, "审核补：D 1490（榜上作者写本名 Nicolaas Beets）")
upd("be", "Of Reynaert the Fox", {"D": 1}, "审核补：D 864（榜上叫 Reynard the Fox）")
upd("ch", "Swiss Family Robinson", {"D": 1}, "审核补：D 1805")
upd("ch", "The Final Problem", {"D": 2, "E": 2}, "按所在集子计：《福尔摩斯回忆录》Goodreads 109,080，《福尔摩斯全集》D 209", dec="保留")
upd("ch", "Stranger in the Village", {"E": 1}, "按所在集子计：《土生子札记》Goodreads 26,150", dec="保留")
upd("no", "Babette's Feast", None, "所在集子《命运轶事》Goodreads 2,289，仍是零项")
S = specio.load("fi")
src = S["sources"]; a2 = src.pop("A2")
src["EP"] = a2.replace("芬兰“市场正典”：", "本国读者面（累计印数，不是谁选出来的书单，所以算 E 类）：") + "；前 16 名记 2"
for j, (t, a, k, p, d, n) in enumerate(S["rows"]):
    if "A2" in p:
        p = dict(p); p.pop("A2"); p["EP"] = 2
        S["rows"][j] = (t, a, k, p, d, n.replace("市场正典", "累计印数榜"))
specio.save("fi", S)
print("ok")
