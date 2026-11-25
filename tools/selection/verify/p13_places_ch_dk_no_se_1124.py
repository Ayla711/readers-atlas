"""Patch 13 (11-24, night): places checked while adding the Swiss, Danish, Norwegian and Swedish books of rule v2.
By the rule for famous books (hang them on the nearest real place, with an honest note), books whose own places are unnamed
are hung where they are tied:
  Winter's Tales: Rungstedlund (Blixen was born and lived there, and wrote the collection there during the occupation).
  Mysteries: Lillesand (the town is unnamed; local tradition has Hamsun writing part of it at the Hotel Norge).
  Out Stealing Horses: no place is named; shown at Trysil, where the 2019 film was shot (a film location carries no excerpt,
  so the novel's summary is in the film place's scene text).
  The House with the Blind Glass Windows: Myre in Vesterålen, Wassmo's birthplace.
  The Pledge: Mägendorf is invented; hung at Chur, where the frame story begins.
  Flowering Nettle: Jämshög, the parish where Martinson was born.
Correction: Sophie's World names a real town; Hilde lives in Lillesand.
Run in tools/selection: python3 -I verify/p13_places_ch_dk_no_se_1124.py, then build all."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import specio
def upd(cc, t, note_add, dec, note_drop=None):
    S = specio.load(cc); r = next(x for x in S["rows"] if x[0] == t); n = r[5]
    if note_drop:
        assert note_drop in n, (t, note_drop); n = n.replace(note_drop, "")
    specio.setrow(S, t, note=n + "；" + note_add, dec=dec); specio.save(cc, S)
upd("dk", "Winter's Tales", "核地点：挂在伦斯泰德隆德（布里克森出生、居住的地方，集子写于占领期间）", "新增", note_drop="地点待查；")
upd("no", "Mysteries", "核地点：小城没写名字，挂在利勒桑（当地传说汉姆生部分书稿写于诺格酒店）", "新增", note_drop="，地点待查")
upd("no", "Sophie's World", "核地点：希尔德的家在利勒桑", "新增", note_drop="书里的小镇没写地名；")
upd("no", "Out Stealing Horses", "核地点：书里没写地名，挂在 2019 年电影的取景地特吕西尔（取景地不挂摘句，书的概述写在取景地说明里）", "新增")
upd("no", "The House with the Blind Glass Windows", "核地点：小地方没写名字，挂在瓦斯莫出生地韦斯特罗伦的米勒", "新增")
upd("ch", "The Pledge", "核地点：麦根村是虚构的，挂在框架故事开始的库尔", "新增")
upd("se", "Flowering Nettle", "核地点：挂在马丁松出生的耶姆舍格教区", "新增")
print("ok")
