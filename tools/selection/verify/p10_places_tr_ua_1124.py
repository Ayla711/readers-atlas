"""Patch 10 (11-24, night): places checked while adding the Turkish and Ukrainian books of rule v2.
- Çalıkuşu: its title reduces to five letters, too short for build.py's title match, so it gets an alias to the book id.
- Not yet added, place to be found (the decision says so; the score is unchanged):
  Tutunamayanlar: the sources found tie it to no place (Ankara, Istanbul and a closing train journey, none fixed).
  Aşk-ı Memnu: the novel opens at Kalender on the Bosphorus, which has no coordinates in any Wikipedia checked (en, tr, de,
  fr, ru, it, nl); the yalı itself is not placed.
  Do the Oxen Low When the Manger Is Full?: the village is Pisky in the Poltava region, on the road to Romodan (the text, ch. I;
  Ukrainian Wikipedia), but which of the villages called Pisky is meant has not been confirmed.
Run in tools/selection: python3 -I verify/p10_places_tr_ua_1124.py, then build all."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import specio
def upd(cc, t, note_add, dec):
    S = specio.load(cc); r = next(x for x in S["rows"] if x[0] == t)
    specio.setrow(S, t, note=r[5] + "；" + note_add, dec=dec); specio.save(cc, S)
S = specio.load("tr"); al = dict(S.get("existing_alias") or {}); al["Çalıkuşu"] = "calikusu"; S["existing_alias"] = al; specio.save("tr", S)
upd("tr", "Tutunamayanlar (The Disconnected)", "核地点：查到的资料没有把它定在哪个地方", "新增（地点待查）")
upd("tr", "Aşk-ı Memnu", "核地点：开篇在博斯普鲁斯海峡边的卡伦德尔，各语种维基都没有它的坐标；雅勒的位置书里没交代", "新增（地点待查）")
upd("ua", "Do the Oxen Low When the Manger Is Full?", "核地点：村子叫皮斯基，在去罗莫丹的路上，但波尔塔瓦州有好几个皮斯基，是哪一个没有核实", "新增（地点待查）")
print("ok")
