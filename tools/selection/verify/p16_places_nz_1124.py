"""Patch 16 (11-24, night): places checked while adding the 13 New Zealand books of rule v2 (data: tools/content/batches/
add_nz2.py). Invented places are hung on the real place tied to them, with an honest note. Other Halves and The 10pm
Question share a city-level pin on Christchurch: neither names a checkable place (Other Halves: one reader's review says
it opens in 1970s Christchurch; The 10pm Question: the city is unnamed, De Goldi sets all her novels in Christchurch).
Also corrects two notes: Other Halves is not tied to Auckland (only the 1984 film is), and Ashleigh Young's prize is the
Windham-Campbell Prize. The Frame row ("Autobiography: To the Is-Land / An Angel at My Table") is matched to the app's
book "An Autobiography" (frame-autobiography) by existing_alias, since the titles differ.
Only the notes change; decisions come from build.py (rule v2).
Run in tools/selection: python3 -I verify/p16_places_nz_1124.py, then make_existing.py and build all."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import specio
S = specio.load("nz")
S.setdefault("existing_alias", {})["Autobiography: To the Is-Land / An Angel at My Table"] = "frame-autobiography"
def upd(t, add, drop=None, repl=None):
    r = next(x for x in S["rows"] if x[0] == t); n = r[5]
    if drop:
        assert drop in n, (t, drop); n = n.replace(drop, repl or "")
    assert "核地点" not in n, t
    specio.setrow(S, t, note=n + "；核地点：" + add)
upd("Plumb", "三部曲大部分以西奥克兰亨德森为背景（书中的卢米斯），一家人住的“和平居”在那里；挂亨德森（原型）")
upd("Autobiography: To the Is-Land / An Angel at My Table", "挂在已有的奥马鲁（伊登街五十六号）")
upd("Once Were Warriors", "松林街区是罗托鲁阿福德兰兹的化身（Te Ara；达夫本人也这样说），挂福德兰兹（原型）", drop="需找挂靠依据；")
upd("Potiki", "维基百科：社区很像格雷斯的家乡洪戈埃卡，挂洪戈埃卡湾（原型）", drop="需找挂靠依据；")
upd("Can You Tolerate This?", "蒂库伊蒂，扬长大的地方，散文《蒂库伊蒂地下》", drop="温斯顿奖；需确认写到的真实地点；", repl="温德姆-坎贝尔奖；")
upd("Smith's Dream", "史密斯独居在科罗曼德尔外海的小岛，挂科罗曼德尔半岛")
upd("Other Halves", "书里的城市没能对照原文核实：一位读者的书评说开篇是 70 年代的克赖斯特彻奇，1984 年电影放在奥克兰；挂克赖斯特彻奇市中心点，说明里已写明", drop="奥克兰；")
upd("The 10pm Question", "书里没写城市名；德戈尔迪说她的小说都设在克赖斯特彻奇，挂克赖斯特彻奇市中心点，说明里已写明")
upd("Pounamu Pounamu", "怀图希，伊希马埃拉在故事里按想象重建的家乡（原型）")
upd("Tu", "一家人搬去的惠灵顿（市中心点）")
upd("Season of the Jew", "马塔怀罗，1868 年 11 月 10 日特库蒂袭击的地方，小说从这一天讲起；英文维基没有条目，坐标取自维基数据")
upd("Under the Mountain", "普普克湖，双胞胎暑假住的地方")
upd("The Changeover", "花园谷是马希给克赖斯特彻奇毕晓普代尔起的名字，挂毕晓普代尔（原型）")
specio.save("nz", S)
print("ok")
