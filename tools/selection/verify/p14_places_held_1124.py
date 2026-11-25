"""Patch 14 (11-24, night): the nine famous books held back as "place to be checked" (地点待查) are hung on the nearest
real place under the rule for famous books, with honest notes (data: tools/content/batches/add_fi3.py, add_ru6.py,
add_nl3.py, add_us1.py, add_be3.py, add_tr3.py, add_ua3.py):
  True (Totta): Helsinki (the city is not named in any source found; Pulkkinen lives there).
  Meek Heritage: Hämeenkyrö (the parish is unnamed; Sillanpää's birthplace).
  The Unknown Soldier: Petrozavodsk, Äänislinna in 1941–1944 (in the Russian data).
  Out of Mind (Hersenschimmen): Gloucester, Massachusetts, where the novel is set (in the US data).
  Malpertuis: Ghent (the city is not named; Ray lived all his life there).
  Happe-Chair: the Borinage (le Culot is invented; the novel names the Borinage, chapter XXIX).
  The Disconnected (Tutunamayanlar): Ankara (Turgut goes there to find Selim's friends).
  Aşk-ı Memnu: Kalender has no coordinates; pinned at Yeniköy beside it, which chapter 1 also names.
  Do the Oxen Low: Pisky is not identified; Myrhorod, Myrny's birthplace.
Run in tools/selection: python3 -I verify/p14_places_held_1124.py, then build all."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import specio
def upd(cc, t, note_drop, note_add):
    S = specio.load(cc); r = next(x for x in S["rows"] if x[0] == t); n = r[5]
    assert r[4] == "新增（地点待查）", (t, r[4])
    assert note_drop in n, (t, note_drop)
    specio.setrow(S, t, note=n.replace(note_drop, "") + "；" + note_add, dec="新增"); specio.save(cc, S)
upd("fi", "True (Totta)", "；核地点：故事在赫尔辛基，但查到的资料没有落到具体地点",
    "核地点：查到的资料都没点明城市，挂在普尔基宁读书、生活的赫尔辛基")
upd("fi", "Meek Heritage", "；核地点：主人公生在萨塔昆塔东北一个没有名字的教区，后来的教区也没点名",
    "核地点：教区没写名字，挂在西兰帕出生的海门屈勒（上萨塔昆塔）")
upd("fi", "The Unknown Soldier", "；核地点：主要地点（彼得罗扎沃茨克、斯维尔河、卡累利阿地峡）今属俄罗斯，挂到哪里待用户定",
    "核地点：挂在彼得罗扎沃茨克（1941—1944 年叫 Äänislinna，进攻部分的中心），条目放在俄罗斯数据里")
upd("nl", "Out of Mind (Hersenschimmen)", "；核地点：故事在美国马萨诸塞州格洛斯特附近，挂到哪里待用户定",
    "核地点：挂在故事发生的马萨诸塞州格洛斯特，条目放在美国数据里")
upd("be", "Malpertuis", "；核地点：书里没点城市名，查到的资料都没说房子在根特",
    "核地点：书里没点城市名，查到的资料也没说房子在根特；挂在让·雷一生居住的根特")
upd("be", "Happe-Chair", "；核地点：书里的地名（le Culot、la Californie、Saut-du-Leu）是本地小地名，查到的资料都没对上真实地点（维基文库全文逐章查过）",
    "核地点：勒屈洛等地名没对上真实地点，挂在书里点名的博里纳日（第二十九章，矿工与军队的冲突）")
upd("tr", "Tutunamayanlar (The Disconnected)", "；核地点：查到的资料没有把它定在哪个地方",
    "核地点：挂在安卡拉（图尔古特去那里找塞利姆的朋友苏莱曼·卡尔格和梅廷）")
upd("tr", "Aşk-ı Memnu", "；核地点：开篇在博斯普鲁斯海峡边的卡伦德尔，各语种维基都没有它的坐标；雅勒的位置书里没交代",
    "核地点：开篇的卡伦德尔没有坐标，图钉标在紧挨着它、第一章也点了名的耶尼柯伊；雅勒的位置书里没交代")
upd("ua", "Do the Oxen Low When the Manger Is Full?", "；核地点：村子叫皮斯基，在去罗莫丹的路上，但波尔塔瓦州有好几个皮斯基，是哪一个没有核实",
    "核地点：村子叫皮斯基，波尔塔瓦州有好几个，是哪一个没能确定；挂在米尔尼出生的米尔霍罗德")
print("ok")
