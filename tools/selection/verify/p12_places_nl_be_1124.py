"""Patch 12 (11-24, night): places checked while adding the Dutch and Belgian books of rule v2.
No real place (not added): The Misfortunates (Reetveerdegem is an invented village).
Place to be found (still to add; score unchanged):
  Out of Mind (Hersenschimmen): set near Gloucester, Massachusetts; whether to hang a Dutch book there is for the user to decide.
  Malpertuis: the town is not named, and no source found places the house in Ghent.
  Happe-Chair: its places (le Culot, la Californie, le Saut-du-Leu) are local names that no source found ties to a real place
  (the Wikisource text was searched chapter by chapter, 11-24).
The Angel Maker: Wolfheim is invented; hung on the Drielandenpunt (Vaalserberg) beside it, which the novel visits.
Run in tools/selection: python3 -I verify/p12_places_nl_be_1124.py, then build all."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import specio
def upd(cc, t, note_add, dec):
    S = specio.load(cc); r = next(x for x in S["rows"] if x[0] == t)
    specio.setrow(S, t, note=r[5] + "；" + note_add, dec=dec); specio.save(cc, S)
upd("nl", "Out of Mind (Hersenschimmen)", "核地点：故事在美国马萨诸塞州格洛斯特附近，挂到哪里待用户定", "新增（地点待查）")
upd("be", "The Misfortunates", "核地点：雷特维尔德海姆是虚构的村子", "不收（没有真实地点）")
upd("be", "Malpertuis", "核地点：书里没点城市名，查到的资料都没说房子在根特", "新增（地点待查）")
upd("be", "Happe-Chair", "核地点：书里的地名（le Culot、la Californie、Saut-du-Leu）是本地小地名，查到的资料都没对上真实地点（维基文库全文逐章查过）", "新增（地点待查）")
upd("be", "The Angel Maker", "核地点：沃尔夫海姆是虚构的，挂在旁边书里写到的瓦尔瑟山三国交界点", "新增")
print("ok")
