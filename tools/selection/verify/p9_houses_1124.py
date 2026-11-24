"""Patch 9 (11-24, night): books shown only at writers' houses, and places for the dz / is / dk packs.
1. existing.json is now made by tools/selection/make_existing.py, which counts books.js, the book_id of lines and scenes, and the
   book_ids of places. The old version counted only books with lines, so 32 books were never scored: 30 that the app shows only at a
   writer's house, grave or memorial, and 2 Romanian books whose titles did not match. build.py now marks those "作家故居" and does not score them (rubric section 11, step 1);
   such a book is scored as soon as it gets a line or scene in its country.
   Romania: aliases for Luceafărul and The Last Night of Love, First Night of War (title mismatch), so both now match their rows.
2. Places checked before adding the new books:
   - The Ace (Al-Laz), Tahar Wattar: the story is set in an unnamed Algerian village (ichkalat.univ-tam.dz, summary of the novel)
     -> no real place, not added.
   - The Blue Fox, Sjón: the farm Brekka in an unnamed valley ("the Dale"; the priest of the Dalbúar), both invented
     (bokmenntaborgin.is excerpt; Bjartur blurb on Google Books) -> no real place, not added.
   - Winter's Tales, Karen Blixen: the manor of "Sorrow-Acre" has no name; where the legend comes from was not verified
     -> still to add, place to be found.
   - The Sheltering Sky: the novel opens in Oran, and Kit is brought back to Oran at the end (EBSCO setting notes; Britannica) -> added.
Run in tools/selection: python3 -I verify/p9_houses_1124.py, then build all."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import specio
def upd(cc, t, note_add=None, dec=None):
    S = specio.load(cc); r = next(x for x in S["rows"] if x[0] == t)
    specio.setrow(S, t, note=(r[5] + "；" + note_add) if note_add else None, dec=dec); specio.save(cc, S)
def size(cc, old, new, add=""):
    S = specio.load(cc); s = S["size_note"]; assert old in s, (cc, old)
    S["size_note"] = s.replace(old, new) + add; specio.save(cc, S)
S = specio.load("ro"); al = dict(S.get("existing_alias") or {})
al.update({"Last Night of Love, First Night of War": "ultima-noapte", "Luceafărul": "luceafarul"}); S["existing_alias"] = al; specio.save("ro", S)
upd("dz", "The Ace (Al-Laz)", "核地点：故事在一座不具名的阿尔及利亚村庄，没有真实地点", dec="不收（没有真实地点）")
upd("dz", "The Sheltering Sky", "核地点：开篇在奥兰，结尾基特被送回奥兰", dec="新增")
upd("is", "The Blue Fox", "核地点：布雷卡农庄和那条山谷（“Dalur”）都没有真名，没有真实地点", dec="不收（没有真实地点）")
upd("dk", "Winter's Tales", "核地点：《悲伤田》的庄园没有名字，传说出自哪里没有核实到", dec="新增（地点待查）")
size("dz", "新增 3，保留 5，保留（只有一类证据） 1，删除（零项） 2，不收 6。", "新增 2，保留 5，保留（只有一类证据） 1，删除（零项） 2，不收 6，没有真实地点 1。",
     " 瓦塔尔《王牌》写的是一座不具名的村庄，没有真实地点，不收。")
size("is", "新增 2，保留 1，保留（只有一类证据） 3，删除（零项） 1，不收 1。", "新增 0，保留 2，保留（只有一类证据） 3，删除（零项） 1，不收 1，没有真实地点 1，作家故居（不评） 2。",
     " 《独立的人们》已在应用里，之前因书名没对上被算成新增。肖恩《蓝狐》的农庄和山谷都没有真名，没有真实地点，不收。")
size("dk", "新增 5，保留 6，保留（只有一类证据） 3，删除（零项） 4，他国书目（不在此评） 1。", "新增 4，保留 7，保留（只有一类证据） 3，删除（零项） 4，作家故居（不评） 8，他国书目（不在此评） 1。",
     " 《非此即彼》已在应用里，之前因书名没对上被算成新增。《冬天的故事》的地点还没找到。")
print("ok")
