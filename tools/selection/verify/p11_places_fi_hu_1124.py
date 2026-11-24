"""Patch 11 (11-24, night): places checked while adding the Finnish and Hungarian books of rule v2.
No real place (not added): Tales from Moominvalley and Mr Boo (invented worlds); Embers (the general's castle is unnamed);
The Tót Family (Mátraszentanna is an invented village).
Place to be found (still to add; score unchanged):
  True: set in Helsinki, but the sources tie it to no particular place.
  Meek Heritage: Juha Toivola is born in an unnamed parish of north-east Satakunta (the text, ch. I); his later parish is not named.
  The Unknown Soldier: its main places (Petrozavodsk, the Svir, the Karelian Isthmus) are now in Russia; whether to hang a
  Finnish book there is for the user to decide.
Run in tools/selection: python3 -I verify/p11_places_fi_hu_1124.py, then build all."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import specio
def upd(cc, t, note_add, dec):
    S = specio.load(cc); r = next(x for x in S["rows"] if x[0] == t)
    specio.setrow(S, t, note=r[5] + "；" + note_add, dec=dec); specio.save(cc, S)
upd("fi", "Tales from Moominvalley", "核地点：姆明谷是虚构的", "不收（没有真实地点）")
upd("fi", "Mr Boo", "核地点：童书里的地方是虚构的", "不收（没有真实地点）")
upd("fi", "True (Totta)", "核地点：故事在赫尔辛基，但查到的资料没有落到具体地点", "新增（地点待查）")
upd("fi", "Meek Heritage", "核地点：主人公生在萨塔昆塔东北一个没有名字的教区，后来的教区也没点名", "新增（地点待查）")
upd("fi", "The Unknown Soldier", "核地点：主要地点（彼得罗扎沃茨克、斯维尔河、卡累利阿地峡）今属俄罗斯，挂到哪里待用户定", "新增（地点待查）")
upd("hu", "Embers", "核地点：将军的城堡没有地名", "不收（没有真实地点）")
upd("hu", "The Tót Family (Tóték)", "核地点：马特劳圣安娜是虚构的村子", "不收（没有真实地点）")
print("ok")
