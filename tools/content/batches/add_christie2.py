"""More Agatha Christie, the famous later books (all in copyright): scene notes in our own words,
plus The Mousetrap as a pilgrimage place. Usage: python3 -I add_christie2.py <app_dir> <coords_json>"""
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

def B(id, title, title_zh, year):
    return dict(id=id, title=title, title_zh=title_zh, author="Agatha Christie", author_zh="阿加莎·克里斯蒂", year=year,
                orig_lang="en", public_domain=False, source_url=None)

books = [
    B("abc-murders", "The ABC Murders", "ABC 谋杀案", "1936"),
    B("evil-under-the-sun", "Evil Under the Sun", "阳光下的罪恶", "1941"),
    B("the-mousetrap", "The Mousetrap", "捕鼠器", "1952"),
]

def place(id, name, name_zh, **kw):
    c = coords[id]
    assert c["lat"] is not None, id
    d = dict(id=id, name=name, name_zh=name_zh, lat=round(c["lat"], 4), lon=round(c["lon"], 4), place_type=kw.pop("type", "original"))
    d.update(kw)
    d["coord_checked"] = f'{c["source_title"]} — {c["source_url"]}, 2026-11-03'
    return d

places = [
    place("andover", "Andover", "安多弗", city=True),
    place("bexhill", "Bexhill-on-Sea", "滨海贝克斯希尔", city=True),
    place("churston", "Churston Ferrers", "彻斯顿费勒斯"),
    place("doncaster", "Doncaster", "唐卡斯特", city=True),
    place("st-martins-theatre", "St Martin's Theatre", "圣马丁剧院", type="pilgrimage",
          note="克里斯蒂的剧本《捕鼠器》1952 年首演，1974 年起在这里上演，是世界上连续上演时间最长的戏",
          note_en="Home since 1974 of The Mousetrap, Christie's play, which opened in 1952 and is the longest-running play in the world",
          book_ids=["the-mousetrap"]),
]

def S(id, book, pid, loc, loc_zh, en, zh, hl_en, hl_zh):
    for h in hl_en: assert h in en, (id, h)
    for h in hl_zh: assert h in zh, (id, h)
    return dict(id=id, kind="scene", book_id=book, place_ids=[pid], location=loc, location_zh=loc_zh,
                text_en=en, text_zh=zh, highlight_en=hl_en, highlight_zh=hl_zh, status="draft")

lines = [
    S("abc-s1", "abc-murders", "andover", "The first murder: A", "第一起：A",
      "After a letter signed ABC warns Poirot, Alice Ascher is found dead in her little tobacco and newspaper shop in Andover, with an ABC railway guide beside her.",
      "波洛收到一封署名 ABC 的预告信；不久，安多弗一家烟草报刊小店的店主艾丽斯·阿舍被发现死在店里，身边放着一本 ABC 铁路时刻表。",
      ["Andover"], ["安多弗"]),
    S("abc-s2", "abc-murders", "bexhill", "The second murder: B", "第二起：B",
      "The second letter names Bexhill-on-Sea; the young waitress Betty Barnard is found strangled on the beach there, and again an ABC guide lies nearby.",
      "第二封信指向滨海贝克斯希尔；年轻的女招待贝蒂·巴纳德被发现勒死在海滩上，旁边又是一本 ABC 时刻表。",
      ["Bexhill-on-Sea"], ["滨海贝克斯希尔"]),
    S("abc-s3", "abc-murders", "churston", "The third murder: C", "第三起：C",
      "At Churston in Devon the victim is Sir Carmichael Clarke, killed on his evening walk near his house, and the alphabet pattern becomes impossible to ignore.",
      "在德文郡的彻斯顿，死者是卡迈克尔·克拉克爵士，他在住所附近散步时遇害；按字母排列的规律再也不容忽视。",
      ["Churston"], ["彻斯顿"]),
    S("abc-s4", "abc-murders", "doncaster", "The fourth murder: D", "第四起：D",
      "The fourth letter points to Doncaster during St Leger race week, and the killing comes in a crowded cinema, where the wrong man dies.",
      "第四封信指向圣莱杰赛马周期间的唐卡斯特；命案发生在一家拥挤的电影院里，死的却不是凶手要找的那个人。",
      ["Doncaster"], ["唐卡斯特"]),
    S("eus-s1", "evil-under-the-sun", "burgh-island", "Smugglers' Island", "走私者岛",
      "On holiday at the Jolly Roger Hotel on Smugglers' Island off the Devon coast, Poirot watches the guests circle the actress Arlena Marshall, until she is found strangled in a hidden cove.",
      "波洛在德文郡海边走私者岛上的快乐罗杰酒店度假，看着客人们围着女演员阿莲娜·马歇尔打转，直到她被发现勒死在一处僻静的小海湾。",
      ["Smugglers' Island"], ["走私者岛"]),
]

if __name__ == "__main__":
    append(f"{APP}/data/books.js", books, "11-03 夜 阿加莎·克里斯蒂 第二批：后期名作（受版权保护，只有场景说明）")
    append(f"{APP}/data/places.js", places, "11-03 夜 阿加莎·克里斯蒂 第二批（坐标均有出处）")
    append(f"{APP}/data/lines.js", lines, "11-03 夜 阿加莎·克里斯蒂 第二批：场景说明（kind: scene，自己的话）")
    print(len(books), "books,", len(places), "places,", len(lines), "scene notes")
