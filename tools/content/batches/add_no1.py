"""11-23: Norway, first pack: 18 new books and 3 books already on the Danish list (Wollstonecraft's letters and two
Holberg books), 19 places. Hamsun's Kristiania and Nordland, Ibsen's Peer Gynt on the Gjendin ridge and Terje Vigen at
Fjære, Undset's Sel, Bjørnson, Kielland's Stavanger, Collett, Petter Dass, Snorri's Stiklestad, Verne's Telemark,
Wollstonecraft at Tønsberg, Blixen's Berlevåg, Vesaas, Heyerdahl and Knausgård. Fictional settings hang on the real
place the book names or is drawn from, and the note says which.

Quotations (6 lines) are cut from Wikisource pages (tools/content/wikisource.py): Norwegian, French and English
Wikisource; translations are our own drafts (translation: "own"). Books in copyright, and PD books whose text we could
not use, have scene notes in our own words or hang on a writer's place. What a cut changes, named in `checked`:
hard-wrapped English is re-flowed; in Peer Gynt only Peer's lines are kept.

Coordinates are those of the place's Norwegian (once English) Wikipedia article (cache/no/coords.json).

Usage: python3 -I add_no1.py <app_dir> <coords.json> <wikisource_root>"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b
import wikisource as ws

APP, CO, WSR = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8")), sys.argv[3]
DATE = "2026-11-23"
b.init(APP, "", "no", DATE)
W = b.W
NOW = "https://no.wikipedia.org/wiki/"
GAP = b.GAP

def BK(id, title, title_zh, title_orig, author, author_zh, author_orig, year, pd=True, **kw):
    d = dict(id=id, title=title, title_zh=title_zh, title_orig=title_orig, author=author, author_zh=author_zh, year=year,
             orig_lang=kw.pop("lang", "no"), public_domain=pd, source_url=kw.pop("src", None), author_orig=author_orig)
    d.update(kw)
    return {k: v for k, v in d.items() if v is not None or k == "source_url"}

def C(pid):
    c = CO[pid]
    return c["lat"], c["lon"], c["st"], c["su"]

def ORIG(pid, name, zh, en_note, zh_note, **kw): return b.ORIG(pid, name, zh, *C(pid), en_note, zh_note, **kw)
def PIL(pid, name, zh, en_note, zh_note, ids, **kw): return b.PIL(pid, name, zh, *C(pid), en_note, zh_note, ids, **kw)
S = b.S

def raw(title, start, end, lang="no"):
    t = ws.text(os.path.join(WSR, lang), title)
    n = re.sub("[\xa0   ]", " ", t)
    i = n.find(start)
    assert i >= 0, (title, start)
    j = n.find(end, i)
    assert j >= 0, (title, start, end)
    return t[i:j + len(end)]

def flow(s):
    """a hard-wrapped paragraph: lines joined, doubled spaces written as one"""
    return re.sub(r" {2,}", " ", s.replace("\n", " "))

def Q(id, book, place, loc, loc_zh, title, orig, hl_orig, en, hl_en, zh, hl_zh, note="", site="Norwegian"):
    if re.search("[\xa0   ]", orig):
        orig = re.sub("[\xa0   ]+", " ", orig)
        note += " (no-break spaces written as plain spaces)"
    for text, hls in ((orig, hl_orig), (en, hl_en), (zh, hl_zh)):
        for h in hls:
            assert h in text, (id, h)
    assert "  " not in orig and "[" not in orig, (id, "spacing or page mark")
    return dict(id=id, book_id=book, place_ids=[place], location=loc, location_zh=loc_zh,
                text_orig=orig, highlight_orig=hl_orig, text_en=en, highlight_en=hl_en, text_zh=zh, highlight_zh=hl_zh, translation="own",
                status="draft", checked=f"{site} Wikisource, {title}{note}, {DATE}")

def EN(id, book, place, loc, loc_zh, title, text, hl, zh, hl_zh, note=""):
    assert "[" not in text and "]" not in text and "\xa0" not in text and "  " not in text, (id, text[:40])
    for h in hl: assert h in text, (id, h)
    for h in hl_zh: assert h in zh, (id, h)
    return dict(id=id, book_id=book, place_ids=[place], location=loc, location_zh=loc_zh, text_en=text, highlight_en=hl, translation="original",
                text_zh=zh, highlight_zh=hl_zh, status="draft", checked=f"English Wikisource, {title}{note}, {DATE}")

HAM = ("Knut Hamsun", "克努特·汉姆生", "Knut Hamsun")
IBS = ("Henrik Ibsen", "易卜生", "Henrik Ibsen")
T_SULT, T_PAN, T_PG, T_TV = "Sult/01", "Pan/01", "Peer Gynt/Første akt", "Terje Vigen"
T_WOLL = "Letters Written during a Short Residence in Sweden, Norway, and Denmark/Letter VIII"
T_VERNE = "Un billet de loterie/I"
WOLL = "wollstonecraft-letters"
EXIST = {WOLL, "jeppe-on-the-hill", "peder-paars"}

books = [
    BK("hunger", "Hunger", "饥饿", "Sult", *HAM, "1890", src=ws.url("no", "Sult"), aliases=["Sult", "Kristiania", "Hamsun", "饥饿的艺术"]),
    BK("pan-hamsun", "Pan", "牧羊神", "Pan", *HAM, "1894", src=ws.url("no", "Pan"), aliases=["Pan", "Lieutenant Glahn", "Thomas Glahn", "Nordland"]),
    BK("growth-of-the-soil", "Growth of the Soil", "大地的成长", "Markens Grøde", *HAM, "1917",
       aliases=["Markens Grøde", "Isak Sellanraa", "Sellanraa", "大地硕果"]),
    BK("peer-gynt", "Peer Gynt", "培尔·金特", "Peer Gynt", *IBS, "1867", src=ws.url("no", "Peer Gynt"),
       aliases=["Peer Gynt", "Gjendin-Eggen", "Besseggen", "Grieg", "皮尔·金特"]),
    BK("a-dolls-house", "A Doll's House", "玩偶之家", "Et Dukkehjem", *IBS, "1879", aliases=["Et dukkehjem", "Nora", "Helmer", "娜拉"]),
    BK("hedda-gabler", "Hedda Gabler", "海达·高布乐", "Hedda Gabler", *IBS, "1890", aliases=["Hedda", "Tesman", "Løvborg"]),
    BK("terje-vigen", "Terje Vigen", "泰耶·维根", "Terje Vigen", *IBS, "1862", src=ws.url("no", T_TV),
       aliases=["Fjære", "Grimstad", "Ibsen poem"]),
    BK("kristin-lavransdatter", "Kristin Lavransdatter", "克丽斯汀·拉夫朗斯达特", "Kristin Lavransdatter", "Sigrid Undset", "西格丽德·温塞特",
       "Sigrid Undset", "1920–1922", aliases=["Kransen", "Husfrue", "Korset", "The Wreath", "Jørundgård", "新娘·主人·十字架"]),
    BK("synnove-solbakken", "Synnøve Solbakken", "索尔巴肯的辛诺维", "Synnøve Solbakken", "Bjørnstjerne Bjørnson", "比约恩斯滕·比昂松",
       "Bjørnstjerne Bjørnson", "1857", src=ws.url("no", "Synnøve Solbakken"), aliases=["Bjørnson", "Thorbjørn", "Solbakken"]),
    BK("garman-and-worse", "Garman & Worse", "加尔曼与沃尔塞", "Garman & Worse", "Alexander Kielland", "亚历山大·基兰", "Alexander L. Kielland", "1880",
       src=ws.url("no", "Garman og Worse"), aliases=["Garman og Worse", "Kielland", "Stavanger"]),
    BK("babettes-feast", "Babette's Feast", "芭贝特的盛宴", None, "Karen Blixen", "凯伦·布里克森", "Karen Blixen", "1950", lang="en", pd=False,
       aliases=["Babettes Gæstebud", "Isak Dinesen", "Berlevåg", "巴贝特之宴"]),
    BK("my-struggle", "My Struggle", "我的奋斗", "Min kamp", "Karl Ove Knausgård", "卡尔·奥韦·克瑙斯高", "Karl Ove Knausgård", "2009–2011", pd=False,
       aliases=["Min kamp", "A Death in the Family", "Knausgaard", "Tromøya"]),
    BK("the-ice-palace", "The Ice Palace", "冰宫", "Is-slottet", "Tarjei Vesaas", "塔尔耶·韦索斯", "Tarjei Vesaas", "1963", pd=False,
       aliases=["Is-slottet", "Unn", "Siss", "Vesaas"]),
    BK("lottery-ticket", "The Lottery Ticket", "一张彩票", "Un billet de loterie", "Jules Verne", "儒勒·凡尔纳", "Jules Verne", "1886", lang="fr",
       src=ws.url("fr", "Un billet de loterie"), aliases=["Un billet de loterie", "Ticket No. 9672", "Hulda Hansen", "Telemark", "Dal"]),
    BK("heimskringla", "Heimskringla", "挪威王列传", "Heimskringla", "Snorri Sturluson", "斯诺里·斯图鲁松", "Snorri Sturluson", "c. 1230", lang="non",
       aliases=["Snorre", "Kongesagaer", "Saga of St Olaf", "Olav den helliges saga", "Stiklestad", "挪威列王传"]),
    BK("nordlands-trompet", "The Trumpet of Nordland", "诺尔兰的号角", "Nordlands Trompet", "Petter Dass", "彼得·达斯", "Petter Dass", "1739",
       src=ws.url("no", "Nordlands Trompet"), aliases=["Nordlands Trompet", "Petter Dass", "Alstahaug", "Helgeland"]),
    BK("kon-tiki", "The Kon-Tiki Expedition", "孤筏重洋", "Kon-Tiki ekspedisjonen", "Thor Heyerdahl", "托尔·海尔达尔", "Thor Heyerdahl", "1948", pd=False,
       aliases=["Kon-Tiki", "Heyerdahl", "By Raft Across the South Seas", "康提基号"]),
    BK("amtmandens-dottre", "The District Governor's Daughters", "州长的女儿们", "Amtmandens Døttre", "Camilla Collett", "卡米拉·科莱特", "Camilla Collett",
       "1854–1855", aliases=["Amtmandens Døtre", "Collett", "Wergeland"]),
]

places = [
    ORIG("no-karl-johan", "Karl Johans gate, Oslo", "卡尔·约翰大街，奥斯陆",
         "The main street of Oslo, from the railway station up to the Royal Palace. In Hunger the starving writer wanders the streets of Kristiania, as the city was then called: Karl Johan, Pilestredet, the Palace Park, the market square",
         "奥斯陆的主街，从火车站一直通到王宫。在《饥饿》里，饿着肚子的写作者在克里斯蒂安尼亚——当时的城名——的街上游荡：卡尔·约翰大街、皮勒街、王宫公园、集市广场"),
    ORIG("no-besseggen", "Besseggen", "贝塞根山脊",
         "The steep ridge in eastern Jotunheimen between the lakes Gjende and Bessvatnet. Ibsen, who travelled through Gudbrandsdalen in 1862, based Peer Gynt's wild ride on the back of a reindeer buck over 'the Gjendin ridge' on a story told here",
         "约通黑门山东部的陡峭山脊，夹在耶恩德湖和贝斯湖之间。易卜生 1862 年游历过古德布兰斯谷，培尔·金特骑着驯鹿公鹿飞越“吉恩丁山脊”的那段狂奔，就取材于这一带流传的故事"),
    PIL("no-ibsen-museum", "Ibsen Museum, Oslo", "易卜生博物馆，奥斯陆",
        "The flat on what is now Henrik Ibsens gate where Ibsen and his wife Suzannah lived from 1895 to 1906, his last home after the long years abroad in which he wrote A Doll's House and Hedda Gabler. The rooms have been restored and opened as a museum",
        "今天亨里克·易卜生街上的一套公寓，易卜生和妻子苏珊娜 1895 年到 1906 年住在这里。这是他在国外漂泊多年之后最后的家，《玩偶之家》和《海达·高布乐》都写于那些国外的年月。房间已经修复，作为博物馆开放",
        ["a-dolls-house", "hedda-gabler"]),
    ORIG("no-fjaere", "Fjære Church, Grimstad", "弗耶勒教堂，格里姆斯塔",
         "The stone church of about 1150 near Grimstad, known as the place where Terje Vigen of Ibsen's poem lies buried. The poem draws on tales of this coast during the Napoleonic wars and the blockade of 1808–1811, when Terje rows to Denmark for grain",
         "格里姆斯塔附近一座约建于 1150 年的石头教堂，以易卜生诗中的泰耶·维根葬在这里而闻名。这首诗取材于拿破仑战争和 1808—1811 年封锁期间这一带海岸流传的故事——泰耶·维根划船去丹麦运粮"),
    ORIG("no-jorundgard", "Jørundgard Medieval Centre, Sel", "约伦德加尔中世纪中心，塞尔",
         "Kristin Lavransdatter grows up at Jørundgård, the farm of her father Lavrans in Sel in Gudbrandsdalen. The farm of sixteen log houses and a stave church copy at Nord-Sel was built for the 1994 film of the novel; the statue of Kristin stands at Nord-Sel church nearby",
         "克丽斯汀·拉夫朗斯达特在父亲拉夫朗斯的农庄约伦德加尔长大，农庄在古德布兰斯谷的塞尔。北塞尔这座有十六栋木屋和一座木板教堂复制品的农庄，是为 1994 年的电影而建的；附近的北塞尔教堂边立着克丽斯汀的雕像"),
    PIL("no-bjerkebaek", "Bjerkebæk, Lillehammer", "比耶克贝克，利勒哈默尔",
        "Sigrid Undset's home in Lillehammer, now a museum. She moved here in 1919, the year before Kristin Lavransdatter began to appear, and lived here until her death in 1949, except for the war years 1940–45, which she spent in the United States",
        "西格丽德·温塞特在利勒哈默尔的家，如今是博物馆。她 1919 年搬到这里，第二年《克丽斯汀·拉夫朗斯达特》开始出版；除了 1940—1945 年战争期间她住在美国，她一直住在这里，直到 1949 年去世",
        ["kristin-lavransdatter"]),
    PIL("no-aulestad", "Aulestad, Gausdal", "奥勒斯塔，高斯达尔",
        "The farm in Gausdal that Bjørnstjerne Bjørnson bought in 1874 and that was his and Karoline Bjørnson's home for many years; it is now a museum. Synnøve Solbakken (1857), his first book, is a story of farm people in the valleys",
        "比约恩斯滕·比昂松 1874 年在高斯达尔买下的农庄，多年里是他和妻子卡罗琳的家，如今是一座博物馆。他的第一部作品《索尔巴肯的辛诺维》（1857）写的就是山谷里的农家人",
        ["synnove-solbakken"]),
    ORIG("no-stavanger", "Stavanger", "斯塔万格",
         "Alexander Kielland was born in Stavanger in 1849. His novels are set in a small coastal town that is never named but is recognisably Stavanger; Garman & Worse is laid in the town of the 1870s",
         "亚历山大·基兰 1849 年生于斯塔万格。他的小说都发生在一座从未点名、却一眼就能认出是斯塔万格的海边小城；《加尔曼与沃尔塞》写的就是十九世纪七十年代的这座城"),
    PIL("no-holberg-bergen", "Holberg Statue, Vågsallmenningen, Bergen", "霍尔堡雕像，瓦格斯广场，卑尔根",
        "Ludvig Holberg was born in Bergen on 3 December 1684 and spent his working life in Copenhagen. A six-metre statue of him stands on Vågsallmenningen, the square by the harbour",
        "路德维·霍尔堡 1684 年 12 月 3 日生于卑尔根，一生的事业都在哥本哈根。港口边的瓦格斯广场上立着他一座六米高的雕像",
        ["jeppe-on-the-hill", "peder-paars"]),
    ORIG("no-berlevag", "Berlevåg", "贝勒沃格",
         "Fishing village on the Arctic coast of Finnmark. Karen Blixen set Babette's Feast in a little Norwegian town of this name; the 1987 film moved the story to the west coast of Jutland",
         "芬马克北冰洋海岸的渔村。凯伦·布里克森把《芭贝特的盛宴》放在一座同名的挪威小城里；1987 年的电影则把故事搬到了日德兰西海岸"),
    ORIG("no-tromoya", "Tromøya, Arendal", "特罗姆岛，阿伦达尔",
         "Island off Arendal on the south coast, where Karl Ove Knausgård grew up in the 1970s; his boyhood here runs through the first books of My Struggle",
         "南部海岸阿伦达尔外的岛屿，卡尔·奥韦·克瑙斯高七十年代在这里长大；他在岛上的童年贯穿了《我的奋斗》的前几卷"),
    PIL("no-vinje", "Vinje", "温耶",
        "Mountain district in Telemark. Tarjei Vesaas was born here in 1897 on the remote farm of Vesås, and from 1934 lived with his wife Halldis Moren Vesaas at Midtbø in Vinje. The Ice Palace, his best-known novel, won the Nordic Council's prize in 1964",
        "泰勒马克的山区。塔尔耶·韦索斯 1897 年生于这里偏僻的韦索斯农庄，1934 年起和妻子哈尔迪丝·莫伦·韦索斯住在温耶的米德博农庄。他最有名的小说《冰宫》1964 年获北欧理事会文学奖",
        ["the-ice-palace"]),
    ORIG("no-tinnsjo", "Tinnsjå (Lake Tinn)", "廷湖",
         "The long lake in Telemark below the Hardangervidda. Jules Verne set The Lottery Ticket (1886) at the inn of Dame Hansen at Dal in Telemark, from which her son Joël guides travellers to the lake",
         "泰勒马克哈当厄高原下的狭长湖泊。儒勒·凡尔纳把《一张彩票》（1886）放在泰勒马克达尔村汉森大娘的客栈里，她的儿子约埃尔从这里给旅客带路去湖边"),
    ORIG("no-stiklestad", "Stiklestad", "斯蒂克莱斯塔",
         "Farm and church in Trøndelag where King Olav Haraldsson fell in battle on 29 July 1030 and was declared a saint a year later. Snorri's saga of St Olaf, the heart of Heimskringla, ends here",
         "特伦德拉格的农庄和教堂，1030 年 7 月 29 日奥拉夫·哈拉尔松国王在这里战死，一年后被封为圣徒。斯诺里《挪威王列传》的核心——《圣奥拉夫传》——就在这里结束"),
    PIL("no-alstahaug", "Alstahaug Church", "阿尔斯塔豪格教堂",
        "The medieval church on Alstahaug in Helgeland, where Petter Dass (c. 1647–1707) was parish priest. His Trumpet of Nordland, published after his death, describes the coast and people of the north in verse",
        "黑尔格兰阿尔斯塔豪格的中世纪教堂，彼得·达斯（约 1647—1707）曾在这里当教区牧师。他死后出版的《诺尔兰的号角》用诗句描写了北方的海岸和人民",
        ["nordlands-trompet"]),
    PIL("no-kon-tiki", "Kon-Tiki Museum, Bygdøy", "康提基博物馆，比格迪",
        "Museum on Bygdøynes in Oslo for Thor Heyerdahl's expeditions, first opened on 15 May 1950. It holds the balsa raft Kon-Tiki, on which he and five companions crossed the Pacific from South America to Polynesia in 1947",
        "奥斯陆比格迪半岛上纪念托尔·海尔达尔探险的博物馆，1950 年 5 月 15 日首次开放。馆里陈列着轻木筏“康提基号”——1947 年，他和五个同伴乘着它从南美洲横渡太平洋到达波利尼西亚",
        ["kon-tiki"]),
    PIL("no-hamsun", "Hamsun Centre, Hamarøy", "汉姆生中心，哈马略",
        "The national centre for Knut Hamsun at Presteid in Hamarøy, in Nordland, where he grew up; the tower by Steven Holl was finished on 4 August 2009, 150 years after his birth. Pan is the story of a summer in a hunting hut in Nordland, and Growth of the Soil of a settler breaking new ground somewhere in the north",
        "诺尔兰哈马略普雷斯泰德的国家汉姆生中心，汉姆生就在哈马略长大；斯蒂文·霍尔设计的塔楼于 2009 年 8 月 4 日、他诞辰一百五十周年时落成。《牧羊神》写的是诺尔兰一间猎人小屋里的一个夏天，《大地的成长》写的是一个拓荒者在北方某处开垦荒地",
        ["growth-of-the-soil"]),
    PIL("no-eidsvoll", "Eidsvoll Vicarage", "埃兹沃尔牧师住宅",
        "The vicarage at Eidsvoll, home of the priest Nicolai Wergeland and his children, the poet Henrik Wergeland and Camilla Collett. Her only novel, The District Governor's Daughters (1854–55), argues for marriage for love against marriage for reason",
        "埃兹沃尔的牧师住宅，牧师尼古拉·韦格兰和他的孩子们——诗人亨里克·韦格兰和卡米拉·科莱特——的家。她唯一的小说《州长的女儿们》（1854—1855）讨论的是为爱情结婚还是为理智结婚",
        ["amtmandens-dottre"]),
    ORIG("no-tonsberg", "Slottsfjellet, Tønsberg", "城堡山，滕斯贝格",
         "The hill in Tønsberg with the ruins of a church and of the medieval fortress of Tunsberghus, which burned in 1503. Mary Wollstonecraft spent three weeks in Tønsberg in the summer of 1795 and walked here alone",
         "滕斯贝格城里的一座山丘，山顶有一座教堂和中世纪滕斯贝格城堡的废墟——城堡在 1503 年焚毁。1795 年夏天，玛丽·沃斯通克拉夫特在滕斯贝格住了三个星期，常常独自到这里散步"),
]

_pg = raw(T_PG, "Har du sett den Gjendin-Eggen nogen Gang?", "Aldrig red jeg slig en Fole!")
_tv = raw(T_TV, "Ved Fjære kirke jeg så en grav,", "men med vilde blomster iblandt.")
lines = [
    Q("no-sult-1", "hunger", "no-karl-johan", "Part 1, opening", "第一部开头", T_SULT,
      raw(T_SULT, "Det var i den Tid, jeg gik omkring og sulted i Kristiania", "Mærker af den"), ["Kristiania"],
      "It was in the days when I wandered about starving in Kristiania, that strange city which no one leaves before it has left its marks on him",
      ["Kristiania"],
      "那是我在克里斯蒂安尼亚四处游荡、忍饥挨饿的日子，这座奇怪的城市，谁都要被它打上印记才离得开",
      ["克里斯蒂安尼亚"]),
    Q("no-pan-1", "pan-hamsun", "no-hamsun", "Chapter 1, opening", "第一章开头", T_PAN,
      raw(T_PAN, "I de sidste Dage har jeg tænkt", "for min Fornøjelses Skyld."), ["Nordlandssommerens"],
      "These last few days I have been thinking and thinking of the endless day of the Nordland summer. I sit here and think of it, and of a hut I lived in, and of the forest behind the hut, and I am beginning to write something down to pass the time and for my own pleasure.",
      ["Nordland summer"],
      "这些天来，我一直在想啊想，想着诺尔兰夏天那永不落幕的白昼。我坐在这里想着它，想着我住过的一间小屋，想着小屋后面的树林，于是动笔写点东西，好打发时间，也图自己高兴。",
      ["诺尔兰夏天"]),
    Q("no-pg-1", "peer-gynt", "no-besseggen", "Act 1, Scene 1", "第一幕第一场", T_PG, _pg, ["Gjendin-Eggen"],
      "Have you ever seen the Gjendin ridge?\nIt's half a Norwegian mile long,\nsharp along the top as a scythe.\nOver glaciers, screes and slopes,\nstraight down the grey rockfalls,\nyou can see on either side\nright into the waters, lying asleep,\nblack and heavy, more than thirteen\nhundred ells below. —\nAlong the ridge he and I\ncut our way through the air.\nNever did I ride such a colt!",
      ["Gjendin ridge"],
      "你见过那座吉恩丁山脊吗？\n它有半挪威里长，\n脊背锋利得像一把镰刀。\n越过冰川、塌方和山坡，\n顺着灰色的乱石滩往下看，\n两边都能一直看到\n沉睡的湖水，\n又黑又沉，在一千三百多\n厄尔的下面。——\n我和它沿着山脊，\n在空中劈开一条路。\n我从没骑过这样的马驹！",
      ["吉恩丁山脊"], note=" (Peer's lines only)"),
    Q("no-tv-1", "terje-vigen", "no-fjaere", "The last stanza", "最后一节", T_TV, _tv, ["Fjære kirke"],
      "By Fjære church I saw a grave;\nit lay in a weather-beaten spot;\nit was not tended, was sunken and low,\nbut still it bore its black board.\nThere stood 'Thærie Wiighen' in white-painted letters,\nand the year he found his rest. —\nHe was laid where the sun burns and the winds blow,\nand so the grass grew harsh and stiff,\nbut with wild flowers in among it.",
      ["Fjære church"],
      "在弗耶勒教堂边我看见一座坟，\n它在风吹雨打的地方；\n没人照料，塌陷而低矮，\n却还立着一块黑木牌。\n上面用白漆写着“泰耶·维根”，\n还有他安息的那一年。——\n他葬在烈日和风吹之下，\n所以那里的草又硬又粗，\n中间却开着野花。",
      ["弗耶勒教堂"]),
    Q("no-verne-1", "lottery-ticket", "no-tinnsjo", "Chapter 1", "第一章", T_VERNE,
      raw(T_VERNE, "Non, ma mère. Joël est allé", "revenir à Dal.", "fr"), ["lac Tinn", "Dal"],
      "'No, mother. Joël has gone to take a traveller to Lake Tinn, and as he left very late I don't think he can be back at Dal before tomorrow.'",
      ["Lake Tinn", "Dal"],
      "“没有，妈妈。约埃尔送一位旅客去廷湖了，他走得很晚，我想他明天以前回不了达尔。”",
      ["廷湖", "达尔"], site="French"),
]
_woll = flow(raw(T_WOLL, "Tonsberg was formerly", "lying close to\nit.", "en"))
lines += [
    EN("no-woll-1", WOLL, "no-tonsberg", "Letter VIII", "第八封信", T_WOLL, _woll, ["Tonsberg"],
       "滕斯贝格从前是挪威一位小国王的驻地；附近一座山上还留着一座堡垒的遗迹——它被瑞典人攻破了——海湾的入口就紧挨着它。",
       ["滕斯贝格"], note=" (the page's line ends joined)"),
]
lines += [
    S("no-garman-s1", "garman-and-worse", "no-stavanger", "Throughout", "全书",
      "The novel follows the old merchant family behind the firm of Garman & Worse, and the people of their house and their town, in a small west-coast town in the 1870s. The town is never named, but it is Kielland's own Stavanger, as he himself wrote.",
      "小说写的是“加尔曼与沃尔塞”商行背后的老商人家族，以及他们宅里和城里的人们，故事发生在十九世纪七十年代西海岸的一座小城。小城从未点名，但正如基兰自己所说，那就是他的家乡斯塔万格。",
      ["Stavanger"], ["斯塔万格"], NOW + "Garman_%26_Worse"),
    S("no-kristin-s1", "kristin-lavransdatter", "no-jorundgard", "The Wreath", "第一部《花冠》",
      "Kristin grows up at Jørundgård in Sel, the daughter of the rich farmer Lavrans, who loves her dearly. At fifteen she is promised to Simon Darre of the neighbouring farm Formo, but while she waits for the wedding at the convent of Nonneseter in Oslo she meets Erlend, who saves her from robbers, and gives her heart to him.",
      "克丽斯汀在塞尔的约伦德加尔农庄长大，是富农拉夫朗斯的掌上明珠。十五岁时，她被许配给邻近福尔莫农庄的西蒙·达勒；可是在奥斯陆的诺内塞特修道院待嫁时，她遇见了从强盗手里救下她的埃伦德，把心交给了他。",
      ["Sel"], ["塞尔"], NOW + "Kristin_Lavransdatter"),
    S("no-babette-s1", "babettes-feast", "no-berlevag", "Throughout", "全篇",
      "In Berlevåg, a small town on a Norwegian fjord, two elderly sisters, daughters of a pious pastor, keep their late father's little congregation together. They take in Babette, a refugee from Paris, as their cook. Years later she wins a lottery and spends every franc on a single French dinner for them and their flock.",
      "在挪威一条峡湾边的小城贝勒沃格，一位虔诚牧师的两个年老的女儿，守着父亲留下的小小教会。她们收留了从巴黎逃难来的芭贝特，让她做厨娘。多年以后，芭贝特中了彩票，把每一个法郎都花在了一顿法国大餐上，请她们和教友们吃。",
      ["Berlevåg"], ["贝勒沃格"], W + "Babette%27s_Feast"),
    S("no-knaus-s1", "my-struggle", "no-tromoya", "Book 1", "第一卷",
      "The first book moves between Karl Ove's boyhood in the 1970s on Tromøya, the island off Arendal where he grew up in fear of his father, and the days after that father's death, when Karl Ove and his brother come to clear the house in which he drank himself to death.",
      "第一卷在两条线之间来回：一条是卡尔·奥韦七十年代在阿伦达尔外的特罗姆岛上度过的童年——他在对父亲的畏惧中长大；另一条是父亲死后的那些天，卡尔·奥韦和哥哥去清理父亲把自己喝死在里面的那座房子。",
      ["Tromøya"], ["特罗姆岛"], W + "Karl_Ove_Knausg%C3%A5rd"),
    S("no-olav-s1", "heimskringla", "no-stiklestad", "The Saga of St Olaf", "《圣奥拉夫传》",
      "Driven from his kingdom, King Olav Haraldsson comes back from exile in Russia to win Norway again. At Stiklestad, on 29 July 1030, he meets an army of farmers and chieftains and falls in the battle; within a year the dead king is honoured as a saint.",
      "被逐出王国的奥拉夫·哈拉尔松国王从俄罗斯流亡归来，要重新夺回挪威。1030 年 7 月 29 日，他在斯蒂克莱斯塔迎战农民和酋长们组成的大军，战死沙场；不到一年，这位死去的国王就被尊为圣徒。",
      ["Stiklestad"], ["斯蒂克莱斯塔"], NOW + "Slaget_p%C3%A5_Stiklestad"),
]

# ============================== checks ==============================
def ids_in(path): return set(re.findall(r'\{ id: "([^"]+)"', open(path, encoding="utf-8").read()))
all_books = set()
for f in glob.glob(os.path.join(APP, "data", "*", "books.js")):
    if os.path.dirname(f) != os.path.dirname(b.data("books.js")):
        all_books |= ids_in(f)
new_b, new_p, new_l = {x["id"] for x in books}, {x["id"] for x in places}, {x["id"] for x in lines}
assert len(new_b) == len(books) and len(new_p) == len(places) and len(new_l) == len(lines)
assert not new_b & all_books, new_b & all_books
assert EXIST <= all_books, EXIST - all_books
assert new_p == set(CO), new_p ^ set(CO)
bids = new_b | EXIST
for l in lines:
    assert l["book_id"] in bids and all(p in new_p for p in l["place_ids"]), l["id"]
used = {p for l in lines for p in l["place_ids"]}
for p in places:
    assert p["id"] in used or p.get("book_ids"), p["id"]
    assert all(i in bids for i in p.get("book_ids", [])), p["id"]
covered = {l["book_id"] for l in lines} | {i for p in places for i in p.get("book_ids", [])}
assert not new_b - covered, new_b - covered
assert not EXIST - covered, EXIST - covered

HEAD = "// Norway, hand-written content (tools/content/batches/add_no1.py, 2026-11-23).\n"
def write(name, key, entries, extra=""):
    os.makedirs(os.path.dirname(b.data(name)), exist_ok=True)
    with open(b.data(name), "w", encoding="utf-8") as fh:
        fh.write(HEAD + extra + "window.RA_DATA = window.RA_DATA || {};\nwindow.RA_DATA." + key + " = [\n"
                 + ",\n".join("  " + b.obj(e) for e in entries) + "\n];\n")
if __name__ == "__main__":
    for f in ("books.js", "places.js", "lines.js"):
        assert not os.path.exists(b.data(f)), ("already there", f)
    write("books.js", "books", books)
    write("places.js", "places", places, "// Each place's admin-1 region is worked out from its coordinates by app.js.\n")
    write("lines.js", "lines", lines)
    print(len(books), "books,", len(places), "places,", len(lines), "lines (", sum(1 for l in lines if l.get("kind") != "scene"), "quotations )")
