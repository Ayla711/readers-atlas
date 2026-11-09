"""Scene notes (kind: "scene") for books still in copyright: our own one-sentence summaries, no quoted wording.
Coordinates for new places come from coords/new8.json (sourced, see coord_checked).
Usage: python3 -I add_scenes.py <app_dir> <coords_json>"""
import json
import sys

APP, CJ = sys.argv[1], sys.argv[2]
coords = {c["id"]: c for c in json.load(open(CJ))}

def js(v):
    return json.dumps(v, ensure_ascii=False)

def append(path, entries, marker):
    s = open(path, encoding="utf-8").read()
    i = s.rstrip().rfind("];")
    s = s[:i].rstrip() + ",\n  // —— " + marker + " ——\n" + ",\n".join("  { " + ", ".join(f"{k}: {js(v)}" for k, v in e.items()) + " }" for e in entries) + "\n];\n"
    open(path, "w", encoding="utf-8").write(s)

def place(id, name, name_zh, **kw):
    c = coords[id]
    d = dict(id=id, name=name, name_zh=name_zh, lat=round(c["lat"], 4), lon=round(c["lon"], 4), place_type=kw.pop("type", "original"))
    d.update(kw)
    d["coord_checked"] = f'{c["source_title"]} — {c["source_url"]}, 2026-11-03'
    return d

places = [
    place("kings-cross", "King's Cross Station", "国王十字车站"),
    place("salisbury", "Salisbury", "索尔兹伯里", city=True),
    place("weymouth-pier", "Weymouth Pier", "韦茅斯码头"),
    place("st-thomas-hospital", "St Thomas' Hospital", "圣托马斯医院"),
    place("clapham-common", "Holy Trinity Church, Clapham Common", "克拉珀姆公园 · 圣三一教堂"),
    place("clava-cairns", "Clava Cairns", "克拉瓦石冢", type="prototype",
          prototype_of="常被认为是《古战场传奇》里克雷格纳敦立石圈的灵感来源", prototype_of_en="Often named as an inspiration for the stone circle on Craigh na Dun in Outlander"),
    place("paddington-station", "Paddington Station", "帕丁顿车站"),
    place("marble-arch", "Marble Arch", "大理石拱门（玉石牌楼）"),
]

def S(id, book, pid, loc, loc_zh, en, zh, hl_en, hl_zh):
    for h in hl_en: assert h in en, (id, h)
    for h in hl_zh: assert h in zh, (id, h)
    return dict(id=id, kind="scene", book_id=book, place_ids=[pid], location=loc, location_zh=loc_zh,
                text_en=en, text_zh=zh, highlight_en=hl_en, highlight_zh=hl_zh, status="draft")

scenes = [
    S("hp-s1", "harry-potter-1", "kings-cross", "Chapter 6", "第 6 章",
      "Harry, ticket in hand, cannot find Platform Nine and Three-Quarters until Mrs Weasley tells him to walk straight at the barrier between platforms nine and ten.",
      "哈利拿着车票，怎么也找不到九又四分之三站台，直到韦斯莱夫人告诉他：径直走向九号和十号站台之间的隔墙。",
      ["Platform Nine and Three-Quarters"], ["九又四分之三站台"]),
    S("rd-s1", "remains-of-the-day", "salisbury", "Day One, Evening: Salisbury", "第一天 · 傍晚 · 索尔兹伯里",
      "Stevens ends the first day of his motoring trip at a guest house in Salisbury, thinking back over the rolling English countryside he stopped to admire, and over what makes a butler great.",
      "开车旅行的第一天，史蒂文斯住进索尔兹伯里的一家小旅馆，回想白天停车眺望的英格兰起伏田野，也思索怎样才算一位伟大的管家。",
      ["Salisbury"], ["索尔兹伯里"]),
    S("rd-s2", "remains-of-the-day", "weymouth-pier", "Day Six, Evening: Weymouth", "第六天 · 傍晚 · 韦茅斯",
      "At the end of his journey, Stevens sits on a bench on the pier at Weymouth as the coloured lights come on, and looks back on his years of service at Darlington Hall.",
      "旅程的最后，史蒂文斯坐在韦茅斯码头的长椅上，看着彩灯一盏盏亮起，回想自己在达林顿府服务的那些年。",
      ["Weymouth"], ["韦茅斯"]),
    S("at-s1", "atonement", "st-thomas-hospital", "Part Three", "第三部",
      "Briony, now a probationer nurse at St Thomas' Hospital across the river from Parliament, helps care for the wounded soldiers brought back from Dunkirk.",
      "布里奥妮成了圣托马斯医院的见习护士，医院隔着泰晤士河与议会大厦相望；她和同伴们照料从敦刻尔克撤回的伤兵。",
      ["St Thomas' Hospital"], ["圣托马斯医院"]),
    S("at-s2", "atonement", "clapham-common", "Part Three", "第三部",
      "Briony slips away to watch Lola marry Paul Marshall in the church on Clapham Common, then walks on to Balham to find her sister Cecilia.",
      "布里奥妮悄悄去克拉珀姆公园旁的教堂，看罗拉嫁给保罗·马歇尔，之后又走到巴勒姆去找姐姐塞西莉亚。",
      ["Clapham Common"], ["克拉珀姆公园"]),
    S("ol-s1", "outlander", "inverness", "Part One", "第一部",
      "In 1945 Claire Randall and her husband Frank take a second honeymoon in Inverness, where Frank looks into an ancestor who served with the English army in the 1740s.",
      "1945 年，克莱尔·兰德尔和丈夫弗兰克来因弗内斯度第二次蜜月；弗兰克在这里查访一位 18 世纪 40 年代在英军中服役的祖先。",
      ["Inverness"], ["因弗内斯"]),
    S("ol-s2", "outlander", "clava-cairns", "Part One", "第一部",
      "Back at the circle of standing stones on Craigh na Dun to gather plants, Claire touches the tallest, cleft stone and comes to in 1743.",
      "克莱尔回到克雷格纳敦山上的立石圈采集植物，触到最高的那块裂开的立石，醒来时已是 1743 年。",
      ["Craigh na Dun"], ["克雷格纳敦"]),
    S("pd-s1", "paddington", "paddington-station", "Chapter One", "第 1 章",
      "Mr and Mrs Brown find a small bear sitting on a suitcase near the lost property office at Paddington Station, with a label round his neck asking whoever finds him to look after him.",
      "布朗夫妇在帕丁顿车站失物招领处附近发现一只坐在手提箱上的小熊，脖子上挂着一张标签，请发现它的人照顾它。",
      ["Paddington Station"], ["帕丁顿车站"]),
    S("mm-s1", "mr-ma-and-son", "marble-arch", "Part One", "第一段",
      "The novel opens with Ma Wei walking alone towards Marble Arch at the corner of Hyde Park, before the story turns back to how he and his father came to London.",
      "小说开篇，马威独自朝海德公园角上的玉石牌楼走去；随后故事才回到他和父亲初到伦敦的时候。",
      ["Marble Arch"], ["玉石牌楼"]),
    S("mm-s2", "mr-ma-and-son", "st-pauls", "The Ma family's curio shop", "马家的古玩铺",
      "Old Mr Ma and his son Ma Wei come to London to take over the curio shop that Mr Ma's late elder brother kept near St Paul's Cathedral.",
      "老马和儿子马威来到伦敦，接手马先生已故哥哥在圣保罗教堂附近开的古玩铺。",
      ["St Paul's Cathedral"], ["圣保罗教堂"]),
]

if __name__ == "__main__":
    append(f"{APP}/data/places.js", places, "11-03 夜 场景说明用的地点（坐标均有出处）")
    s = open(f"{APP}/data/lines.js", encoding="utf-8").read()
    if "kind: \"scene\"" not in s:
        s = s.replace("window.RA_DATA.lines = [", "// kind: \"scene\" = 受版权保护的书，用自己的话写的场景说明（不是原文摘句）；页面上不加标注，只在数据里区分\nwindow.RA_DATA.lines = [", 1)
        open(f"{APP}/data/lines.js", "w", encoding="utf-8").write(s)
    append(f"{APP}/data/lines.js", scenes, "11-03 夜 场景说明（kind: scene，自己的话，不含原文）")
    print(len(places), "places,", len(scenes), "scene notes")
