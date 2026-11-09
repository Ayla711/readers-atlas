"""11-04: review item 2 (film and pilgrimage places for thin areas), Harry Potter 2–7, Zhu Ziqing's London Miscellany.
All these books are in copyright (Zhu Ziqing: public domain in the UK and China, but in US copyright until the
end of 2038, per the Wikisource notice), so the text entries are scene notes in our own words (kind: "scene").
Every coordinate has a source (coord_checked).
Usage: python3 -I add_batch4.py <app_dir>"""
import json
import re
import sys

APP = sys.argv[1]
D = ", 2026-11-04"
W = "https://en.wikipedia.org/wiki/"
GBG = "https://www.thegreatbritainguide.com/place/"

def js(v):
    return json.dumps(v, ensure_ascii=False)

def append(path, entries, marker):
    s = open(path, encoding="utf-8").read()
    i = s.rstrip().rfind("];")
    s = s[:i].rstrip() + ",\n  // —— " + marker + " ——\n" + ",\n".join("  { " + ", ".join(f"{k}: {js(v)}" for k, v in e.items()) + " }" for e in entries) + "\n];\n"
    open(path, "w", encoding="utf-8").write(s)

def B(id, title, title_zh, author, author_zh, year, **kw):
    d = dict(id=id, title=title, title_zh=title_zh, author=author, author_zh=author_zh, year=year,
             orig_lang="en", public_domain=False, source_url=None)
    d.update(kw)
    return d

HP = "J. K. Rowling", "罗琳"
books = [
    B("harry-potter-2", "Harry Potter and the Chamber of Secrets", "哈利·波特与密室", *HP, "1998"),
    B("harry-potter-3", "Harry Potter and the Prisoner of Azkaban", "哈利·波特与阿兹卡班囚徒", *HP, "1999"),
    B("harry-potter-4", "Harry Potter and the Goblet of Fire", "哈利·波特与火焰杯", *HP, "2000"),
    B("harry-potter-5", "Harry Potter and the Order of the Phoenix", "哈利·波特与凤凰社", *HP, "2003"),
    B("harry-potter-6", "Harry Potter and the Half-Blood Prince", "哈利·波特与“混血王子”", *HP, "2005"),
    B("harry-potter-7", "Harry Potter and the Deathly Hallows", "哈利·波特与死亡圣器", *HP, "2007"),
    B("brideshead-revisited", "Brideshead Revisited", "故园风雨后", "Evelyn Waugh", "伊夫林·沃", "1945"),
    B("a-game-of-thrones", "A Game of Thrones", "权力的游戏", "George R. R. Martin", "乔治·R·R·马丁", "1996"),
    B("under-milk-wood", "Under Milk Wood", "牛奶树下", "Dylan Thomas", "迪伦·托马斯", "1954"),
    B("london-miscellany", "London Miscellany", "伦敦杂记", "Zhu Ziqing", "朱自清", "1943", title_orig="伦敦杂记", author_orig="朱自清",
      orig_lang="zh", source_url="https://zh.wikisource.org/wiki/%E5%80%AB%E6%95%A6%E9%9B%9C%E8%A8%98"),
]

def P(id, name, name_zh, lat, lon, src_title, src_url, type, **kw):
    d = dict(id=id, name=name, name_zh=name_zh, lat=lat, lon=lon, place_type=type)
    d.update(kw)
    d["coord_checked"] = f"{src_title} — {src_url}{D}"
    return d

def FILM(id, name, name_zh, lat, lon, st, su, title, year, kind, scene_en, scene_zh, book_ids, **kw):
    return P(id, name, name_zh, lat, lon, st, su, "film_location", adaptation=dict(title=title, year=year, kind=kind),
             scene=scene_zh, book_ids=book_ids, scene_en=scene_en, **kw)

def PIL(id, name, name_zh, lat, lon, st, su, en, zh, book_ids, **kw):
    return P(id, name, name_zh, lat, lon, st, su, "pilgrimage", note=zh, book_ids=book_ids, note_en=en, **kw)

def ORIG(id, name, name_zh, lat, lon, st, su, en, zh, **kw):
    return P(id, name, name_zh, lat, lon, st, su, "original", note=zh, note_en=en, **kw)

places = [
    # —— review item 2 ——
    FILM("lyme-park", "Lyme Park, Cheshire", "柴郡 · 莱姆庄园", 53.3381, -2.0548, "Lyme Park (Wikipedia)", W + "Lyme_Park",
         "Pride and Prejudice", 1995, "电视剧", "The exterior of Pemberley, Mr Darcy's house", "达西先生的彭伯里庄园外景", ["pride-and-prejudice"]),
    FILM("castle-howard", "Castle Howard", "霍华德城堡", 54.1214, -0.9058, "Castle Howard (Wikipedia)", W + "Castle_Howard",
         "Brideshead Revisited", 1981, "电视剧", "Brideshead, the Flytes' house (again in the 2008 film)", "弗莱特家族的布赖兹赫德庄园（2008 年电影也在这里拍）", ["brideshead-revisited"]),
    FILM("dark-hedges", "The Dark Hedges, County Antrim", "安特里姆郡 · 黑暗树篱", 55.1344, -6.3806, "Dark Hedges (The Great Britain Guide)", GBG + "dark-hedges/",
         "Game of Thrones", 2011, "电视剧", "The Kingsroad", "国王大道", ["a-game-of-thrones"]),
    PIL("dylan-thomas-boathouse", "Dylan Thomas Boathouse, Laugharne", "拉恩 · 迪伦·托马斯船屋", 51.7722, -4.4562, "Dylan Thomas Boathouse (Wikipedia)", W + "Dylan_Thomas_Boathouse",
        "Dylan Thomas's home for his last four years, 1949–53; he wrote in a shed a little further along Cliff Road, above the Taf estuary",
        "迪伦·托马斯生命最后四年（1949–1953）的家；他在悬崖路稍远处的一间小棚屋里写作，俯瞰塔夫河口", ["under-milk-wood"]),
    PIL("abbotsford", "Abbotsford", "阿博茨福德", 55.5997, -2.7819, "Abbotsford (Wikishire)", "https://wikishire.co.uk/wiki/Abbotsford",
        "Walter Scott's house on the Tweed near Galashiels, built between 1817 and 1825; he died here in 1832",
        "沃尔特·司各特在加拉希尔斯附近特威德河畔的宅第，1817 至 1825 年间建成；他 1832 年在这里去世", ["marmion", "lady-of-the-lake"]),
    PIL("dr-johnsons-house", "Dr Johnson's House, Gough Square", "高夫广场 · 约翰生博士故居", 51.5149, -0.1082, "Dr Johnson's House (The Great Britain Guide)", GBG + "dr-johnsons-house/",
        "17 Gough Square, where Samuel Johnson lived from 1748 to 1759 and compiled his Dictionary; a museum since 1914",
        "高夫广场 17 号，塞缪尔·约翰生 1748 至 1759 年住在这里，编成了他的《英语词典》；1914 年起成为博物馆",
        ["life-of-johnson", "journey-western-islands", "london-miscellany"]),
    # —— Harry Potter 2–7: real places named in the books ——
    ORIG("tottenham-court-road", "Tottenham Court Road", "托特纳姆宫路", 51.5162, -0.1309, "Tottenham Court Road station (Wikipedia)", W + "Tottenham_Court_Road_station",
         "A busy shopping street running south from Euston Road to St Giles Circus; the marker is at its south end, by the station",
         "从尤斯顿路向南通到圣吉尔斯圆环的繁忙商业街；标记在它南端的车站旁"),
    ORIG("forest-of-dean", "Forest of Dean", "迪安森林", 51.79, -2.54, "Forest of Dean (Wikishire)", "https://wikishire.co.uk/wiki/Forest_of_Dean",
         "An ancient forest in west Gloucestershire, between the Wye and the Severn", "格洛斯特郡西部的古老森林，位于怀伊河和塞文河之间"),
    # —— Harry Potter 2–7: film locations ——
    FILM("gloucester-cathedral", "Gloucester Cathedral cloisters", "格洛斯特大教堂回廊", 51.8675, -2.2467, "Gloucester Cathedral (Wikipedia)", W + "Gloucester_Cathedral",
         "Harry Potter and the Chamber of Secrets", 2002, "电影", "Hogwarts corridors (also in the first and sixth films)", "霍格沃茨的走廊（第一部和第六部电影也在这里拍）",
         ["harry-potter-1", "harry-potter-2", "harry-potter-6"]),
    FILM("clachaig-gully", "Clachaig Gully, Glen Coe", "格伦科 · 克拉哈格沟", 56.6644, -5.0595, "Clachaig Inn (The Great Britain Guide); the sets stood just north of the inn (Wikipedia, Glen Coe)", GBG + "clachaig-inn/",
         "Harry Potter and the Prisoner of Azkaban", 2004, "电影", "Sets for Hagrid's hut and the Hogwarts grounds, built near the foot of the gully", "海格小屋和霍格沃茨场地的布景，搭在山沟脚下",
         ["harry-potter-3"]),
    FILM("steall-falls", "Steall Falls, Glen Nevis", "尼维斯谷 · 斯蒂尔瀑布", 56.7698, -4.9786, "Steall Waterfall (Wikipedia)", W + "Steall_Waterfall",
         "Harry Potter and the Goblet of Fire", 2005, "电影", "Backdrop to the first task, when Harry flies from the Hungarian Horntail", "第一个项目里哈利骑扫帚躲避匈牙利树蜂龙时的背景",
         ["harry-potter-4"]),
    FILM("claremont-square", "Claremont Square, Islington", "伊斯灵顿 · 克莱蒙特广场", 51.5311, -0.1103, "Claremont Square (Wikipedia)", W + "Claremont_Square",
         "Harry Potter and the Order of the Phoenix", 2007, "电影", "12 Grimmauld Place, headquarters of the Order of the Phoenix", "凤凰社总部格里莫广场 12 号",
         ["harry-potter-5"]),
    FILM("millennium-bridge", "Millennium Bridge", "千禧桥", 51.5102, -0.0984, "Millennium Bridge, London (Wikipedia)", W + "Millennium_Bridge,_London",
         "Harry Potter and the Half-Blood Prince", 2009, "电影", "The bridge the Death Eaters destroy in the opening scenes", "开场食死徒摧毁的那座桥",
         ["harry-potter-6"]),
    FILM("freshwater-west", "Freshwater West, Pembrokeshire", "彭布罗克郡 · 弗雷什沃特西海滩", 51.6566, -5.0599, "Freshwater West (Wikipedia), grid ref SR884997", W + "Freshwater_West",
         "Harry Potter and the Deathly Hallows", 2010, "电影", "Shell Cottage and Dobby's grave", "贝壳小屋和多比的墓", ["harry-potter-7"]),
    FILM("malham-cove", "Malham Cove", "马勒姆湾", 54.0708, -2.1586, "Malham Cove (Wikipedia)", W + "Malham_Cove",
         "Harry Potter and the Deathly Hallows – Part 1", 2010, "电影", "Where Harry and Hermione camp while on the run", "哈利和赫敏逃亡途中扎营的地方", ["harry-potter-7"]),
    FILM("lavenham", "De Vere House, Lavenham", "拉文纳姆 · 德维尔宅", 52.1075, 0.7957, "Lavenham (Wikipedia), grid ref TL915491", W + "Lavenham",
         "Harry Potter and the Deathly Hallows – Part 1", 2010, "电影", "Backgrounds for Godric's Hollow, with De Vere House", "戈德里克山谷的背景，用的是德维尔宅", ["harry-potter-7"]),
    # —— Zhu Ziqing ——
    ORIG("charing-cross-road", "Charing Cross Road", "查令十字路", 51.5147, -0.1301, "Foyles (Wikipedia), the shop at 107 Charing Cross Road", W + "Foyles",
         "A West End street long known for its bookshops; Foyles moved from its old building at 111–119 to No. 107 next door in 2014",
         "西区一条以书店闻名的街道；福伊尔斯书店 2014 年从 111–119 号的老楼搬到隔壁 107 号"),
    ORIG("caledonian-market", "Caledonian Park clock tower", "加尔东尼公园钟楼", 51.5471, -0.1236, "Caledonian Park Clock Tower (Wikipedia)", W + "Caledonian_Park_Clock_Tower",
         "The clock tower is what remains of the Metropolitan Cattle Market, opened in 1855; the Caledonian Market that Zhu visited was held on this site",
         "钟楼是 1855 年启用的大都会牲畜市场留下的主体建筑；朱自清逛的加尔东尼市场就开在这块场地上"),
]

def S(id, book, pids, loc, loc_zh, en, zh, hl_en, hl_zh):
    for h in hl_en: assert h in en, (id, h)
    for h in hl_zh: assert h in zh, (id, h)
    return dict(id=id, kind="scene", book_id=book, place_ids=pids, location=loc, location_zh=loc_zh,
                text_en=en, text_zh=zh, highlight_en=hl_en, highlight_zh=hl_zh, status="draft")

lines = [
    S("bh-s1", "brideshead-revisited", ["oxford"], "Book 1", "第一部",
      "Charles Ryder, an undergraduate at Oxford, meets Lord Sebastian Flyte after Sebastian, drunk, is sick through the window of Charles's ground-floor rooms; the friendship takes Charles to Brideshead.",
      "牛津大学生查尔斯·赖德和塞巴斯蒂安·弗莱特勋爵相识，是因为喝醉的塞巴斯蒂安从查尔斯底楼房间的窗口吐了进来；这段友谊把查尔斯带到了布赖兹赫德。",
      ["Oxford"], ["牛津"]),
    S("hp2-s1", "harry-potter-2", ["kings-cross"], "Chapter 5", "第 5 章",
      "Harry and Ron find the barrier to Platform Nine and Three-Quarters sealed, miss the Hogwarts Express, and fly to school in Mr Weasley's Ford Anglia.",
      "哈利和罗恩发现通往九又四分之三站台的隔墙封死了，赶不上霍格沃茨特快列车，只好开着韦斯莱先生的福特安格里亚飞去学校。",
      ["Platform Nine and Three-Quarters"], ["九又四分之三站台"]),
    S("hp7-s1", "harry-potter-7", ["tottenham-court-road"], "Chapter 9", "第 9 章",
      "When the Ministry falls and the wedding breaks up, Hermione Disapparates with Harry and Ron to Tottenham Court Road, where two Death Eaters track them down in a small café.",
      "魔法部陷落，婚礼乱成一团，赫敏带着哈利和罗恩幻影移形到托特纳姆宫路；两个食死徒在路边一家小咖啡馆里找到了他们。",
      ["Tottenham Court Road"], ["托特纳姆宫路"]),
    S("hp7-s2", "harry-potter-7", ["forest-of-dean"], "Chapter 19", "第 19 章",
      "Harry and Hermione camp in the Forest of Dean, where Hermione once came with her parents; at night a silver doe leads Harry to a frozen pool with the sword of Gryffindor beneath the ice.",
      "哈利和赫敏在迪安森林扎营，赫敏小时候和父母来这里露营过；夜里一头银色的牝鹿把哈利引到一个结冰的池塘，格兰芬多宝剑就沉在冰下。",
      ["Forest of Dean"], ["迪安森林"]),
    S("zz-s1", "london-miscellany", ["charing-cross-road"], "Three Bookshops", "《三家书店》",
      "Zhu finds London's second-hand bookshops gathered on Charing Cross Road, a short, narrow street crowded with stalls, and likes best the dim basement of Foyle's, the biggest of them, where you can browse old literature for hours.",
      "朱自清写伦敦卖旧书的铺子集中在切林克拉斯路：街又窄又短，两旁满是书摊；他最爱其中最大的福也尔书店那间昏暗的地下室，满是旧文学书，待几个钟头也没人管。",
      ["Charing Cross Road", "Foyle's"], ["切林克拉斯路", "福也尔"]),
    S("zz-s2", "london-miscellany", ["caledonian-market"], "The Caledonian Market", "《加尔东尼市场》",
      "Zhu likens the Caledonian Market, a junk market open only on Tuesdays and Fridays, to the temple fairs of Beiping; he haggles over a brass lion paperweight without buying it, and comes home with a thick book of sample greeting cards for fourpence.",
      "加尔东尼市场每星期只在星期二、星期五开放，朱自清把它比作北平的庙会和小市；他为一个铜狮子镇纸讲了价没买成，最后花四便士买回一大本贺年片样本。",
      ["Caledonian Market"], ["加尔东尼市场"]),
    S("zz-s3", "london-miscellany", ["dr-johnsons-house"], "Writers' Houses", "《文人宅》",
      "Zhu visits Dr Johnson's house in the old City, a three-storey house on the corner of a quiet little square, where Johnson lived for eleven years from 1748 and his assistants compiled the Dictionary in a small room on the top floor.",
      "朱自清参观旧城里的约翰生博士故宅：一个清静的小方场角上的三层楼房，约翰生 1748 年搬进来，住了十一年，他的助手就在三楼的小屋里编成了那部大字典。",
      ["Dr Johnson's house"], ["约翰生博士故宅"]),
    S("zz-s4", "london-miscellany", ["keats-house"], "Writers' Houses", "《文人宅》",
      "In Keats's house in Hampstead, then still countryside, Zhu recalls that Keats lived, fell in love and wrote most of his best poems here, and retells Brown's memory of Keats sitting under a plum tree in the garden one spring morning in 1819 and coming in with the Ode to a Nightingale.",
      "朱自清写汉姆司台德的济慈宅：那时这里还是乡下，济慈在这儿住，在这儿恋爱，好诗大多在这儿写成；他还转述布朗的回忆：1819 年春天一个早晨，济慈在园中梅树下坐了两三个钟头，进屋时手里拿着的就是《夜莺歌》。",
      ["Hampstead"], ["汉姆司台德"]),
]

if __name__ == "__main__":
    append(f"{APP}/data/books.js", books, "11-04 哈利·波特 2–7、取景地相关书目、朱自清《伦敦杂记》（均受版权保护，只有场景说明）")
    append(f"{APP}/data/places.js", places, "11-04 薄弱大区的取景地与朝圣地、哈利·波特 2–7、朱自清（坐标均有出处）")
    append(f"{APP}/data/lines.js", lines, "11-04 场景说明（kind: scene，自己的话）")
    # the earlier Harry Potter film places also serve the second book
    s = open(f"{APP}/data/places.js", encoding="utf-8").read()
    for pid in ["alnwick-castle", "glenfinnan", "christ-church"]:
        m = re.search(r'(\{ id: "' + pid + r'",[^\n]*?book_ids: )\["harry-potter-1"\]', s)
        assert m, pid
        s = s[:m.start()] + m.group(1) + '["harry-potter-1", "harry-potter-2"]' + s[m.end():]
    open(f"{APP}/data/places.js", "w", encoding="utf-8").write(s)
    print(len(books), "books,", len(places), "places,", len(lines), "scene notes")
