"""11-27: Colombia, the new books of the selection re-check (tools/selection/co.md, rule v2; on 11-27 the user took these six).
The book records go to the shared South American list (data/sa/books.js). Places, with the reason for each:
- Orocué for La vorágine: the novel's first part is set in the Llanos of Casanare, and names Orocué, the river port on the
  Meta; Rivera stayed there. La vorágine (1924) is in the US public domain: one verbatim passage, from es.wikisource
  "La vorágine/Primera parte" (fetched with tools/content/wikisource.py). That page keeps a hard-wrapped plain-text
  layout, with line ends in the middle of sentences; inside the passage each line end is joined with one space, and
  nothing else is changed. English and Chinese translations are our own (translation: "own").
- Cartagena (existing co-cartagena-clock-tower) for La tejedora de coronas: the 1697 French sack of Cartagena.
- Ciénaga for La casa grande: the banana massacre of 6 December 1928 at Ciénaga.
- Medellín for El desbarrancadero: Fernando goes back to the family house in Medellín.
- Aracataca (existing co-aracataca-ggm) for El coronel no tiene quien le escriba: the town is unnamed; García Márquez said
  the colonel was drawn from his grandfather, who never got his promised pension, and this is the grandfather's house
  (A-24, said in the note).
- Cartagena (existing co-cartagena-clock-tower) for Del amor y otros demonios: Sierva María is shut in the convent of Santa
  Clara in Cartagena; neither Wikipedia nor Wikidata gives coordinates for the convent, so the line goes on the existing
  Cartagena place.
The other five are in copyright: scene notes, no quotation.
Usage: python3 -I tools/content/batches/add_co_v2_1127.py <app_dir> tools/content/batches/coords/add_co_v2_1127.json <wikisource_dir>"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b
import wikisource as ws

APP, CO, WS = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8")), sys.argv[3]
DATE = "2026-11-27"
b.init(APP, "", "co", DATE)
SA_BOOKS = os.path.join(APP, "data", "sa", "books.js")
def C(pid):
    c = CO[pid]; return c["lat"], c["lon"], c["st"], c["su"]

VOR = "La vorágine/Primera parte"
def joined(title, start, end):
    """the passage from `start` to the end of `end`; the page's hard line ends inside it become single spaces"""
    t = ws.text(WS, title)
    i = t.find(start); assert i >= 0, (title, start)
    assert t.find(start, i + 1) < 0, (title, start, "not unique")
    j = t.find(end, i); assert j >= 0, (title, start, end)
    s = t[i:j + len(end)].replace("\n", " ")
    assert "  " not in s and "\xa0" not in s and "[" not in s, (title, start)
    return s

def Q(id, book, place, loc, loc_zh, title, orig, hl_orig, en, hl_en, zh, hl_zh):
    for text, hls in ((orig, hl_orig), (en, hl_en), (zh, hl_zh)):
        for h in hls:
            assert h in text, (id, h)
    return dict(id=id, book_id=book, place_ids=[place], location=loc, location_zh=loc_zh, text_orig=orig, highlight_orig=hl_orig,
                text_en=en, highlight_en=hl_en, text_zh=zh, highlight_zh=hl_zh, translation="own", status="draft",
                checked=f"es Wikisource, {title}, {DATE}")

GGM = ("Gabriel García Márquez", "加夫列尔·加西亚·马尔克斯")
books = [
    dict(id="la-voragine", title="The Vortex", title_zh="漩涡", title_orig="La vorágine", author="José Eustasio Rivera",
         author_zh="何塞·欧斯塔西奥·里维拉", year="1924", orig_lang="es", public_domain=True, source_url=ws.url("es", "La vorágine"),
         aliases=["La vorágine", "Arturo Cova"]),
    dict(id="la-tejedora-de-coronas", title="La tejedora de coronas", title_zh="编织王冠的女人", title_orig="La tejedora de coronas",
         author="Germán Espinosa", author_zh="赫尔曼·埃斯皮诺萨", year="1982", orig_lang="es", public_domain=False, source_url=None,
         aliases=["La tejedora de coronas", "Genoveva Alcocer"]),
    dict(id="la-casa-grande", title="La casa grande", title_zh="大宅", title_orig="La casa grande", author="Álvaro Cepeda Samudio",
         author_zh="阿尔瓦罗·塞佩达·萨穆迪奥", year="1962", orig_lang="es", public_domain=False, source_url=None,
         aliases=["La casa grande", "Masacre de las bananeras"]),
    dict(id="el-desbarrancadero", title="The Abyss", title_zh="深渊", title_orig="El desbarrancadero", author="Fernando Vallejo",
         author_zh="费尔南多·巴列霍", year="2001", orig_lang="es", public_domain=False, source_url=None, aliases=["El desbarrancadero"]),
    dict(id="no-one-writes-to-the-colonel", title="No One Writes to the Colonel", title_zh="没有人给他写信的上校",
         title_orig="El coronel no tiene quien le escriba", author=GGM[0], author_zh=GGM[1], year="1961", orig_lang="es",
         public_domain=False, source_url=None, aliases=["El coronel no tiene quien le escriba"]),
    dict(id="of-love-and-other-demons", title="Of Love and Other Demons", title_zh="爱情和其他魔鬼", title_orig="Del amor y otros demonios",
         author=GGM[0], author_zh=GGM[1], year="1994", orig_lang="es", public_domain=False, source_url=None,
         aliases=["Del amor y otros demonios", "Sierva María"]),
]

places = [
    b.ORIG("co-orocue", "Orocué, Casanare", "卡萨纳雷 · 奥罗奎", *C("co-orocue"),
        "A river town on the Meta in the south-east of Casanare, in the eastern Llanos, 450 km from Bogotá. José Eustasio Rivera stayed here and, the town's history says, wrote part of La vorágine here; the novel's first part, the flight of Arturo Cova and Alicia into the plains of Casanare, names Orocué more than once",
        "卡萨纳雷省东南部、东部大平原上梅塔河边的小城，离波哥大 450 公里。何塞·欧斯塔西奥·里维拉在这里住过，按当地的说法，《漩涡》有一部分就写于此地；小说第一部写阿图罗·科瓦和阿莉西亚私奔到卡萨纳雷平原，书里不止一次提到奥罗奎"),
    b.ORIG("co-cienaga", "Ciénaga, Magdalena", "马格达莱纳 · 谢纳加", *C("co-cienaga"),
        "A Caribbean town between the Sierra Nevada de Santa Marta and the Ciénaga Grande, at the heart of the old banana zone. On the night of 5-6 December 1928 the army, protecting the interests of the United Fruit Company, fired on striking banana workers gathered here, killing hundreds: the massacre that García Márquez put into One Hundred Years of Solitude. Álvaro Cepeda Samudio, who grew up in Ciénaga and heard the story from relatives and neighbours as a child, told it in La casa grande (1962)",
        "加勒比海边的小城，在圣玛尔塔内华达山脉和大沼泽之间，是旧日香蕉种植区的中心。1928 年 12 月 5 日到 6 日夜里，为保护联合果品公司的利益，军队向聚集在这里罢工的香蕉工人开枪，打死数百人：马尔克斯后来把这场屠杀写进了《百年孤独》。在谢纳加长大、小时候从亲戚邻居那里听过这件事的阿尔瓦罗·塞佩达·萨穆迪奥，把它写成了《大宅》（1962）"),
    b.ORIG("co-medellin", "Medellín", "麦德林", *C("co-medellin"),
        "Capital of Antioquia, in the Aburrá valley of the central Andes, and Colombia's second city. Fernando Vallejo was born here in 1942 and left in 1971 for Mexico; his El desbarrancadero (2001) brings his narrator back to the family house in Medellín to see his brother Darío through his last days",
        "安蒂奥基亚省首府，在中部安第斯的阿布拉谷地，哥伦比亚第二大城市。费尔南多·巴列霍 1942 年生在这里，1971 年去了墨西哥；他的《深渊》（2001）让叙述者回到麦德林的老家，陪弟弟达里奥走完最后的日子"),
]

lines = [
    Q("co-vor-q1", "la-voragine", "co-orocue", "Part One", "第一部", VOR,
      joined(VOR, "Aquella noche, la primera de Casanare", "Alicia dormía con agitada respiración."), ["Casanare"],
      "That night, the first in Casanare, sleeplessness was my confidant. Through the gauze of the mosquito net I watched the stars flicker in the boundless skies. The leaves of the palms that sheltered us fell silent above us. An infinite silence floated all around, tinting the clear air blue. Beside my hammock, on her narrow travelling cot, Alicia slept, breathing restlessly.",
      ["Casanare"],
      "那一夜，在卡萨纳雷的第一夜，失眠成了我的知己。隔着蚊帐的纱，我望见无边的天空里群星闪烁。为我们遮风挡雨的棕榈叶在头顶沉默下来。无尽的寂静漂浮在四周，把透明的空气染成了蓝色。在我的吊床旁，阿莉西亚睡在窄小的行军床上，呼吸急促不安。",
      ["卡萨纳雷"]),
    b.S("co-tejedora-s1", "la-tejedora-de-coronas", "co-cartagena-clock-tower", "The novel as a whole", "全书",
        "On 3 April 1697 young Federico Goltar, an amateur astronomer in love with Genoveva Alcocer, believes he has found a new planet, which he cannot make public for fear of the Inquisition of Cartagena. Weeks later, in May and June 1697, the French under the Baron de Pointis take and sack the city, and Genoveva's family and Federico are killed. Genoveva tells it all in the first person as an old woman in the hands of the Inquisition, through travels to Paris, Rome and the United States, the Masonic lodges and the Enlightenment. Espinosa worked on it from 1969 to 1981; in 1992 UNESCO took it into its Collection of Representative Works.",
        "1697 年 4 月 3 日，爱着热诺韦瓦·阿尔科塞尔的年轻天文爱好者费德里科·戈尔塔尔以为自己发现了一颗新行星，却因为害怕卡塔赫纳宗教裁判所而不敢公开。几周后，1697 年 5 月到 6 月，德·普安蒂斯男爵率法国人攻占并洗劫了这座城市，热诺韦瓦的家人和费德里科都死了。这一切由落入宗教裁判所之手的老年热诺韦瓦用第一人称讲出来，其间穿插她在巴黎、罗马和美国的游历、共济会和启蒙运动。埃斯皮诺萨从 1969 年写到 1981 年；1992 年联合国教科文组织把它收入“代表作丛书”。",
        ["Cartagena"], ["卡塔赫纳"],
        "https://es.wikipedia.org/wiki/La_tejedora_de_coronas; https://es.wikipedia.org/wiki/Expedici%C3%B3n_de_Cartagena_(1697)"),
    b.S("co-casagrande-s1", "la-casa-grande", "co-cienaga", "The novel as a whole", "全书",
        "Cepeda Samudio's only novel, eight years in the writing, tells the banana massacre of 6 December 1928 at Ciénaga, when the army fired on striking workers of the United Fruit Company and killed hundreds. It is told not by one narrator but in many different voices. Cepeda Samudio grew up in Ciénaga and heard the story as a small boy from his relatives and neighbours. Published in 1962, it has been reprinted more than twelve times and translated into several languages.",
        "这是塞佩达·萨穆迪奥唯一的长篇，写了八年，讲 1928 年 12 月 6 日谢纳加的香蕉工人大屠杀：军队向联合果品公司的罢工工人开枪，打死数百人。书里没有单一的叙述者，而是交织着许多不同的声音。塞佩达·萨穆迪奥在谢纳加长大，小时候从亲戚邻居那里听说了这件事。1962 年出版，至今重印十余次，译成多种语言。",
        ["Ciénaga"], ["谢纳加"],
        "https://es.wikipedia.org/wiki/%C3%81lvaro_Cepeda_Samudio; https://es.wikipedia.org/wiki/Masacre_de_las_bananeras"),
    b.S("co-desbarr-s1", "el-desbarrancadero", "co-medellin", "The novel as a whole", "全书",
        "Fernando, a Colombian writer living in Mexico, comes back to Medellín, the city of his childhood and youth, when he hears that his brother Darío is dying, of what no one knows; it is AIDS. Darío has settled in the family house, and Fernando stays to help him live, and to help him die. In the same year their father dies of liver cancer. Between the two deaths the narrator rages at his mother, the Church, the politicians and a country falling apart, and remembers Santa Anita, the farm that was the lost paradise of their childhood. It is a novel about brotherly love; it won the Rómulo Gallegos Prize in 2003.",
        "旅居墨西哥的哥伦比亚作家费尔南多听说弟弟达里奥快死了、谁也不知道是什么病，便回到童年和青年时代的城市麦德林；那是艾滋病。达里奥已经住进了老家的房子，费尔南多留下来，帮他活下去，也帮他死去。同一年，父亲死于肝癌。在两次死亡之间，叙述者对母亲、教会、政客和这个分崩离析的国家破口大骂，也回忆起童年失去的天堂圣安妮塔庄园。这是一部关于兄弟之爱的小说，2003 年获罗慕洛·加列戈斯奖。",
        ["Medellín"], ["麦德林"],
        "https://es.wikipedia.org/wiki/El_desbarrancadero; https://revistas.udea.edu.co/index.php/lyl/article/view/345990/20816130; https://www.penguinrandomhouse.com/books/586219/el-desbarrancadero--the-abyss-by-fernando-vallejo/; https://congresos.fahce.unlp.edu.ar/citclot/viii-congreso/actas/ponencia-220922105830248653/@@display-file/file/Musitano-%20Julia.pdf"),
    b.S("co-coronel-s1", "no-one-writes-to-the-colonel", "co-aracataca-ggm", "The novella as a whole", "全书",
        "In 1958, in a village on Colombia's Caribbean coast, an old colonel, a veteran of the Thousand Days' War, lives in poverty with his asthmatic wife. For fifteen years he has gone down every Friday to the post office at the port to wait for the letter confirming the veteran's pension he was promised; it never comes. Their only hope is a fighting cock that belonged to their son Agustín, killed for handing out clandestine leaflets, which the colonel keeps feeding for the January fights while the two of them go hungry. García Márquez wrote it in Paris in 1956-57, and said the colonel was drawn from his grandfather, also a colonel, who never received the pension he was promised; he later called it his best book.",
        "1958 年，哥伦比亚加勒比海岸的一个小镇上，一位参加过千日战争的老上校和患哮喘的妻子过着穷日子。十五年来，他每个星期五都到港口的邮局，等那封确认他退伍军人养老金的信；信从来没来。他们唯一的指望是儿子阿古斯丁留下的一只斗鸡（阿古斯丁因散发秘密传单被杀），上校一直喂着它，等一月份的斗鸡比赛，自己和妻子却挨着饿。马尔克斯 1956 至 1957 年在巴黎写成此书，说上校的原型是同样当过上校、始终没拿到承诺的养老金的外祖父；他后来称这是自己最好的书。",
        ["Caribbean coast"], ["加勒比海岸"],
        "https://es.wikipedia.org/wiki/El_coronel_no_tiene_quien_le_escriba; https://en.wikipedia.org/wiki/No_One_Writes_to_the_Colonel"),
    b.S("co-amor-s1", "of-love-and-other-demons", "co-cartagena-clock-tower", "The novel as a whole", "全书",
        "In 18th-century Cartagena de Indias, Sierva María de Todos los Ángeles, the twelve-year-old daughter of a marquis, whose hair has never been cut, is raised by her family's slaves, speaks their African languages and calls herself María Mandinga. Bitten by a rabid dog on her birthday, she shows no sign of rabies, but her fevers are taken for possession and the bishop has her shut in the convent of Santa Clara to be exorcised. The priest sent to exorcise her, Cayetano Delaura, falls in love with her; she dies in the course of the exorcisms. In the prologue García Márquez says the book grew from a legend his grandmother told him and from the day, as a young reporter, he watched old tombs being emptied and saw a girl's skull with 22 metres of hair still attached.",
        "18 世纪的卡塔赫纳，侯爵十二岁的女儿西埃尔瓦·玛丽亚从没剪过头发，由家里的奴隶带大，会说他们的非洲语言，自称“玛丽亚·曼丁加”。她生日那天被一条疯狗咬了，并没有得狂犬病，可她发烧被当成了魔鬼附身，主教下令把她关进圣克拉拉修道院驱魔。奉命为她驱魔的神父卡耶塔诺·德劳拉爱上了她；她死在驱魔之中。马尔克斯在序言里说，这本书源于外祖母讲给他的一个传说，也源于他年轻时当记者，亲眼看着旧墓被清空、见到一个女孩的头骨上还连着 22 米长头发的那一天。",
        ["Cartagena"], ["卡塔赫纳"],
        "https://es.wikipedia.org/wiki/Del_amor_y_otros_demonios_(novela); https://en.wikipedia.org/wiki/Of_Love_and_Other_Demons"),
]

def ids_in(path): return set(re.findall(r'\{ id: "([^"]+)"', open(path, encoding="utf-8").read()))
all_books = set().union(*(ids_in(f) for f in glob.glob(os.path.join(APP, "data", "*", "books.js"))))
all_places = set().union(*(ids_in(f) for f in glob.glob(os.path.join(APP, "data", "*", "places.js"))))
all_lines = set().union(*(ids_in(f) for f in glob.glob(os.path.join(APP, "data", "*", "lines.js"))))
assert not {x["id"] for x in books} & all_books
assert {p["id"] for p in places} == set(CO) and not set(CO) & all_places
assert not {l["id"] for l in lines} & all_lines
assert {"co-cartagena-clock-tower", "co-aracataca-ggm"} <= all_places
if __name__ == "__main__":
    note = "11-27 selection re-check, rule v2 (add_co_v2_1127.py)"
    b.append(SA_BOOKS, books, note)
    b.append(b.data("places.js"), places, note)
    b.append(b.data("lines.js"), lines, note)
    print(len(books), "books,", len(places), "places,", len(lines), "lines")
