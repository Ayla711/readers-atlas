"""Patch 3 (11-24 evening): clear stale "未核" notes now that D/E are read; Switzerland rows from the editoreric list that v1 skipped;
source texts updated to say what was read. Run after p2_all.py: python3 -I verify/p3_cleanup.py"""
import sys, os, re
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import specio
NOTE = {
 ("ch","Heidi"): "D 839 · Goodreads 216,602",
 ("ch","On the Lake"): "歌德的诗《湖上》（苏黎世湖）；不在 D 前 2000 · Goodreads 查不到单独条目（只有 2 人的德文本）",
 ("dz","The Sheltering Sky"): "奥兰、撒哈拉；D 596 · Goodreads 32,010",
 ("fi","The Summer Book"): "扬松第二本；D 1228 · Goodreads 69,158",
 ("ma","Naked Lunch"): "丹吉尔；D 253 · Goodreads 101,400",
 ("ua","Voices from Chernobyl"): "普里皮亚季；D 1281 · Goodreads 67,995",
 ("ua","Red Cavalry"): "沃伦、加利西亚；D 517 · Goodreads 4,595",
 ("za","The Story of an African Farm"): "卡鲁；D 1285 · Goodreads 3,219",
}
NEW_CH = [
 ("The Pledge","Friedrich Dürrenmatt","本国",{"A1":3,"D":1,"E":1},"","迪伦马特第二本；苏黎世州、格劳宾登；D 1613 · Goodreads 12,453"),
 ("The Visit","Friedrich Dürrenmatt","本国",{"A1":3,"E":1},"不收（没有真实地点）","居伦镇是虚构的；不在 D 前 2000 · Goodreads 41,778"),
 ("The Physicists","Friedrich Dürrenmatt","本国",{"A1":3,"E":1},"不收（没有真实地点）","疗养院是虚构的；不在 D 前 2000 · Goodreads 46,886"),
 ("Homo Faber","Max Frisch","本国（写美洲、欧洲）",{"A1":3,"D":1,"E":1},"不算瑞士","故事不在瑞士；D 857 · Goodreads 33,585"),
 ("Swiss Family Robinson","Johann David Wyss","本国（写荒岛）",{"A1":3,"E":2},"不算瑞士","故事在荒岛；Goodreads 111,609"),
]
specs = {}
S_ = lambda cc: specs.setdefault(cc, specio.load(cc))
for (cc, t), n in NOTE.items(): specio.setrow(S_(cc), t, note=n)
S = S_("ch")
for r in NEW_CH:
    if not any(x[0] == r[0] for x in S["rows"]): S["rows"].append(r)
S["sources"]["E"] = "Goodreads 评分人数（11-24 逐本查 Goodreads 自动补全接口，取该作品各版本中最大的一条）"
S["sources"]["A1"] = S["sources"]["A1"].replace("32 部", "33 部") + "；名单里写在瑞士以外、或没有真实地点的书在表里注明“不算瑞士”“没有真实地点”"
S = S_("fi"); S["sources"]["D"] = "thegreatestbooks.org 总榜名次（11-24 逐页读前 2000 名：《卡勒瓦拉》1017、《夏日之书》1228、《无名战士》1233；其余不在前 2000）"
S = S_("eg"); S["sources"]["A2"] = S["sources"]["A2"].replace("第 51–100 名没找到，书不在前 50 的记为“未核”", "第 51–100 名找不到全表（查过 Goodreads 两个转录帖、arablit、The Arab Weekly），这部分在本名单上记 0；已有的书不会因此被删")
S = S_("dz"); S["sources"]["A4"] = S["sources"]["A4"].replace("第 51–100 名未核", "第 51–100 名找不到全表，记 0")
for cc in "au nz eg za ng dz ma ke fi hu is tr ua ro nl be ch dk no se".split():
    S = S_(cc)
    for k in list(S["sources"]):
        if k in ("D",) and "逐页" not in S["sources"][k]:
            S["sources"][k] = S["sources"][k] + "；11-24 对照总榜前 2000 名逐页重读，表中 D 以重读为准"
        if k == "E" and "自动补全" not in S["sources"][k]:
            S["sources"][k] = S["sources"][k] + "；11-24 用 Goodreads 自动补全接口逐本重查，表中 E 以重查为准"
for cc, S in specs.items(): specio.save(cc, S)
print("ok", sorted(specs))
