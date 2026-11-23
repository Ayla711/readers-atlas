"""11-22: Czechia, first pack: 51 new books (and Apollinaire's Alcools, already on the shared list), 63 places.
Czech literature from Comenius and Mácha to Hrabal, Kundera and Havel; the German writers of Prague and the Bohemian
lands (Kafka, Rilke, Meyrink, Stifter, Musil, Ebner-Eschenbach); and well-known foreign books set here (Austerlitz, Utz,
HHhH, The Glass Room). Fictional settings hang on the real place the book is modelled on, or on the writer's own place,
and the note says which.

Quotations (12 books, 17 lines) are cut from Wikisource pages (tools/content/wikisource.py): Czech, German and French
Wikisource; English and Chinese translations are our own drafts (translation: "own"). Every other book has a scene note
or hangs on a writer's place.
What a cut changes, named again in that line's `checked`: a no-break space is written as a space.

Coordinates come from Wikimedia Commons (median of the geotagged files of the place's category) or from the coordinates
of the place's Czech Wikipedia article (cache/cz/coords.json).

Usage: python3 -I add_cz1.py <app_dir> <coords.json> <wikisource_dir>"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b
import wikisource as ws

APP, CO, WS = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8")), sys.argv[3]
DATE = "2026-11-22"
b.init(APP, "", "cz", DATE)
W = b.W

def BK(id, title, title_zh, author, author_zh, year, pd=True, **kw):
    d = dict(id=id, title=title, title_zh=title_zh, author=author, author_zh=author_zh, year=year,
             orig_lang=kw.pop("lang", "cs"), public_domain=pd, source_url=kw.pop("src", None))
    d.update(kw)
    return d

def C(pid):
    c = CO[pid]
    return c["lat"], c["lon"], c["st"], c["su"]

def ORIG(pid, name, zh, en_note, zh_note, **kw): return b.ORIG(pid, name, zh, *C(pid), en_note, zh_note, **kw)
def PROTO(pid, name, zh, en_note, zh_note, **kw): return b.PROTO(pid, name, zh, *C(pid), en_note, zh_note, **kw)
def PIL(pid, name, zh, en_note, zh_note, ids, **kw): return b.PIL(pid, name, zh, *C(pid), en_note, zh_note, ids, **kw)
S = b.S

def raw(title, start, end):
    t = ws.text(WS, title)
    i = t.find(start)
    assert i >= 0, (title, start)
    j = t.find(end, i)
    assert j >= 0, (title, start, end)
    return t[i:j + len(end)]

NBSP = " (a no-break space written as a space)"
def Q(id, book, place, loc, loc_zh, site, title, orig, hl_orig, en, hl_en, zh, hl_zh, note=""):
    if "\xa0" in orig:
        orig = orig.replace("\xa0", " ")
        note += NBSP
    for text, hls in ((orig, hl_orig), (en, hl_en), (zh, hl_zh)):
        for h in hls:
            assert h in text, (id, h)
    assert "  " not in orig and "[" not in orig, (id, "spacing or page mark")
    d = dict(id=id, book_id=book, place_ids=[place], location=loc, location_zh=loc_zh,
             text_orig=orig, highlight_orig=hl_orig, text_en=en, highlight_en=hl_en, text_zh=zh, highlight_zh=hl_zh, translation="own",
             status="draft", checked=f"{site} Wikisource, {title}{note}, {DATE}")
    return d

CS = lambda t: ws.url("cs", t)
DE = lambda t: ws.url("de", t)
KAFKA = ("Franz Kafka", "卡夫卡")
CAPEK = ("Karel Čapek", "卡雷尔·恰佩克")
JIR = ("Alois Jirásek", "伊拉塞克")
HRABAL = ("Bohumil Hrabal", "赫拉巴尔")
KUND = ("Milan Kundera", "米兰·昆德拉")
HAVEL = ("Václav Havel", "哈维尔")
SPS = "Staré pověsti české (1959)/"
SV = "Osudy dobrého vojáka Švejka za světové války/"

# ============================== books ==============================
books = [
    BK("cz-labyrint", "The Labyrinth of the World and the Paradise of the Heart", "世界迷宫与心灵天堂", "John Amos Comenius", "夸美纽斯", "1631",
       title_orig="Labyrint světa a ráj srdce", src=CS("Labyrint světa a ráj srdce"), aliases=["Labyrint světa a ráj srdce", "Jan Amos Komenský", "Komensky"]),
    BK("cz-maj", "May", "五月", "Karel Hynek Mácha", "马哈", "1836", title_orig="Máj", src=CS("Máj (Mácha)/1"), aliases=["Máj", "Maj", "Macha", "Vilém", "Jarmila"]),
    BK("cz-kytice", "A Bouquet of Folk Legends", "花束集", "Karel Jaromír Erben", "爱尔本", "1853", title_orig="Kytice z pověstí národních",
       src=CS("Kytice z pověstí národních"), aliases=["Kytice", "Vodník", "Polednice", "Svatební košile"]),
    BK("cz-babicka", "The Grandmother", "外祖母", "Božena Němcová", "聂姆佐娃", "1855", title_orig="Babička", src=CS("Babička"), aliases=["Babička", "Babicka", "Nemcova", "Granny"]),
    BK("cz-tyrolske-elegie", "Tyrolean Elegies", "蒂罗尔哀歌", "Karel Havlíček Borovský", "哈夫利切克", "1861", title_orig="Tyrolské elegie", aliases=["Tyrolské elegie", "Havlicek"]),
    BK("cz-povidky-malostranske", "Tales of the Lesser Quarter", "小城故事", "Jan Neruda", "扬·聂鲁达", "1878", title_orig="Povídky malostranské",
       src=CS("Povídky malostranské"), aliases=["Povídky malostranské", "Prague Tales", "Hastrman", "Malá Strana"]),
    BK("cz-filosofska-historie", "A Philosophers' Story", "哲学生的故事", *JIR, "1878", title_orig="Filosofská historie", src=CS("Filosofská historie"), aliases=["Filosofská historie", "Vavřena", "Frybort"]),
    BK("cz-noc-na-karlstejne", "A Night at Karlštejn", "卡尔施泰因之夜", "Jaroslav Vrchlický", "弗尔赫利茨基", "1884", title_orig="Noc na Karlštejně",
       src=CS("Noc na Karlštejně"), aliases=["Noc na Karlštejně", "Noc na Karlstejne", "Vrchlicky"]),
    BK("cz-lesni-samoty", "From the World of Forest Solitudes", "来自林中孤寂的世界", "Karel Klostermann", "克洛斯特曼", "1892", title_orig="Ze světa lesních samot",
       src=CS("Ze světa lesních samot"), aliases=["Ze světa lesních samot", "Šumava", "Sumava"]),
    BK("cz-stare-povesti", "Old Czech Legends", "捷克古老传说", *JIR, "1894", title_orig="Staré pověsti české", src=CS("Staré pověsti české (1959)"),
       aliases=["Staré pověsti české", "Stare povesti ceske", "Praotec Čech", "Libuše", "Blaničtí rytíři"]),
    BK("cz-slezske-pisne", "Silesian Songs", "西里西亚之歌", "Petr Bezruč", "贝兹鲁奇", "1909", pd=False, title_orig="Slezské písně", aliases=["Slezské písně", "Maryčka Magdónova", "Bezruc"]),
    BK("cz-stribrny-vitr", "The Silver Wind", "银色的风", "Fráňa Šrámek", "什拉梅克", "1910", title_orig="Stříbrný vítr", aliases=["Stříbrný vítr", "Stribrny vitr", "Jan Ratkin", "Sramek"]),
    BK("cz-liska-bystrouska", "The Cunning Little Vixen", "狡猾的小狐狸", "Rudolf Těsnohlídek", "捷斯诺赫利德克", "1920", title_orig="Liška Bystrouška",
       src=CS("Liška Bystrouška"), aliases=["Liška Bystrouška", "Liska Bystrouska", "Vixen Sharp-Ears", "Janáček"]),
    BK("cz-rur", "R.U.R.", "罗素姆万能机器人", *CAPEK, "1920", title_orig="R.U.R.", src=CS("R.U.R."), aliases=["Rossum's Universal Robots", "robot", "Capek"]),
    BK("cz-svejk", "The Good Soldier Švejk", "好兵帅克", "Jaroslav Hašek", "哈谢克", "1921–1923", title_orig="Osudy dobrého vojáka Švejka za světové války",
       src=CS("Osudy dobrého vojáka Švejka za světové války"), aliases=["Švejk", "Svejk", "Schweik", "Hasek", "Osudy dobrého vojáka Švejka"]),
    BK("cz-tezka-hodina", "A Difficult Hour", "沉重的时刻", "Jiří Wolker", "沃尔克", "1922", title_orig="Těžká hodina", aliases=["Těžká hodina", "Balada o očích topičových"]),
    BK("cz-rozmarne-leto", "Summer of Caprice", "任性的夏天", "Vladislav Vančura", "万楚拉", "1926", title_orig="Rozmarné léto", aliases=["Rozmarné léto", "Capricious Summer", "Vancura"]),
    BK("cz-zahradnikuv-rok", "The Gardener's Year", "园丁的一年", *CAPEK, "1929", title_orig="Zahradníkův rok", src=CS("Zahradníkův rok"), aliases=["Zahradníkův rok"]),
    BK("cz-valka-s-mloky", "War with the Newts", "鲵鱼之乱", *CAPEK, "1936", title_orig="Válka s mloky", src=CS("Válka s mloky"), aliases=["Válka s mloky", "Valka s mloky", "Povondra"]),
    BK("cz-zahada-hlavolamu", "The Mystery of the Puzzle", "谜之锁", "Jaroslav Foglar", "福格拉", "1941", pd=False, title_orig="Záhada hlavolamu",
       aliases=["Záhada hlavolamu", "Rychlé šípy", "Stínadla", "ježek v kleci"]),
    BK("cz-bylo-nas-pet", "There Were Five of Us", "我们五个", "Karel Poláček", "波拉切克", "1946", title_orig="Bylo nás pět", src=CS("Bylo nás pět"), aliases=["Bylo nás pět", "Petr Bajza"]),
    BK("cz-zbabelci", "The Cowards", "懦夫们", "Josef Škvorecký", "什克沃雷茨基", "1958", pd=False, title_orig="Zbabělci", aliases=["Zbabělci", "Danny Smiřický", "Skvorecky"]),
    BK("cz-mendelssohn", "Mendelssohn Is on the Roof", "门德尔松在屋顶上", "Jiří Weil", "伊日·魏尔", "1960", pd=False, title_orig="Na střeše je Mendelssohn", aliases=["Na střeše je Mendelssohn"]),
    BK("cz-zahradni-slavnost", "The Garden Party", "游园会", *HAVEL, "1963", pd=False, title_orig="Zahradní slavnost", aliases=["Zahradní slavnost", "Hugo Pludek"]),
    BK("cz-ostre-sledovane-vlaky", "Closely Watched Trains", "严密监视的列车", *HRABAL, "1965", pd=False, title_orig="Ostře sledované vlaky",
       aliases=["Ostře sledované vlaky", "Closely Observed Trains", "Miloš Hrma"]),
    BK("cz-spalovac", "The Cremator", "焚尸人", "Ladislav Fuks", "富克斯", "1967", pd=False, title_orig="Spalovač mrtvol", aliases=["Spalovač mrtvol", "Kopfrkingl"]),
    BK("cz-zert", "The Joke", "玩笑", *KUND, "1967", pd=False, title_orig="Žert", aliases=["Žert", "Zert", "Ludvík Jahn"]),
    BK("cz-obsluhoval", "I Served the King of England", "我曾侍候过英国国王", *HRABAL, "1971", pd=False, title_orig="Obsluhoval jsem anglického krále",
       aliases=["Obsluhoval jsem anglického krále", "Jan Dítě"]),
    BK("cz-smrt-krasnych-srncu", "The Death of the Beautiful Roebucks", "美丽牡鹿之死", "Ota Pavel", "奥塔·帕维尔", "1971", pd=False, title_orig="Smrt krásných srnců",
       aliases=["Smrt krásných srnců", "How I Came to Know Fish", "Jak jsem potkal ryby"]),
    BK("cz-postriziny", "Cutting It Short", "一缕秀发", *HRABAL, "1976", pd=False, title_orig="Postřižiny", aliases=["Postřižiny", "Postriziny", "Uncle Pepin"]),
    BK("cz-prilis-hlucna-samota", "Too Loud a Solitude", "过于喧嚣的孤独", *HRABAL, "1976", pd=False, title_orig="Příliš hlučná samota", aliases=["Příliš hlučná samota", "Haňťa"]),
    BK("cz-moc-bezmocnych", "The Power of the Powerless", "无权者的权力", *HAVEL, "1978", pd=False, title_orig="Moc bezmocných", aliases=["Moc bezmocných"]),
    BK("cz-kniha-smichu", "The Book of Laughter and Forgetting", "笑忘录", *KUND, "1979", pd=False, title_orig="Kniha smíchu a zapomnění", aliases=["Kniha smíchu a zapomnění"]),
    BK("cz-vsecky-krasy", "All the Beauties of the World", "世界美如斯", "Jaroslav Seifert", "塞弗尔特", "1981", pd=False, title_orig="Všecky krásy světa", aliases=["Všecky krásy světa"]),
    BK("cz-nesnesitelna-lehkost", "The Unbearable Lightness of Being", "不能承受的生命之轻", *KUND, "1984", pd=False, title_orig="Nesnesitelná lehkost bytí",
       aliases=["Nesnesitelná lehkost bytí", "Tomáš", "Tereza"]),
    # ---- German writers of Prague and the Bohemian lands ----
    BK("cz-hochwald", "The High Forest", "高山森林", "Adalbert Stifter", "施蒂弗特", "1842", lang="de", title_orig="Der Hochwald", aliases=["Der Hochwald", "Wittinghausen"]),
    BK("cz-mozart-prag", "Mozart's Journey to Prague", "莫扎特在去布拉格的路上", "Eduard Mörike", "默里克", "1855", lang="de", title_orig="Mozart auf der Reise nach Prag",
       src=DE("Mozart auf der Reise nach Prag"), aliases=["Mozart auf der Reise nach Prag", "Don Giovanni"]),
    BK("cz-marienbad-elegie", "Marienbad Elegy", "玛丽恩巴德悲歌", "Johann Wolfgang von Goethe", "歌德", "1827", lang="de", title_orig="Marienbader Elegie",
       src=DE("Marienbader Elegie"), aliases=["Marienbader Elegie", "Trilogie der Leidenschaft", "Ulrike von Levetzow"]),
    BK("cz-krambambuli", "Krambambuli", "克兰巴姆布里", "Marie von Ebner-Eschenbach", "埃布纳-埃申巴赫", "1883", lang="de", title_orig="Krambambuli", aliases=["Dorf- und Schloßgeschichten"]),
    BK("cz-larenopfer", "Offerings to the Lares", "宅神祭品", "Rainer Maria Rilke", "里尔克", "1895", lang="de", title_orig="Larenopfer", src=DE("Larenopfer"), aliases=["Larenopfer", "Der Hradschin"]),
    BK("cz-toerless", "The Confusions of Young Törless", "学生托乐思的迷惘", "Robert Musil", "穆齐尔", "1906", lang="de", title_orig="Die Verwirrungen des Zöglings Törleß",
       aliases=["Die Verwirrungen des Zöglings Törleß", "Toerless", "Torless"]),
    BK("cz-verwandlung", "The Metamorphosis", "变形记", *KAFKA, "1915", lang="de", title_orig="Die Verwandlung", aliases=["Die Verwandlung", "Gregor Samsa"]),
    BK("cz-golem", "The Golem", "魔像", "Gustav Meyrink", "梅林克", "1915", lang="de", title_orig="Der Golem", aliases=["Der Golem", "Athanasius Pernath", "Rabbi Löw"]),
    BK("cz-landarzt", "A Country Doctor", "乡村医生", *KAFKA, "1920", lang="de", title_orig="Ein Landarzt", aliases=["Ein Landarzt"]),
    BK("cz-prozess", "The Trial", "审判", *KAFKA, "1925", lang="de", title_orig="Der Process", src=DE("Der Prozess"), aliases=["Der Prozess", "Der Process", "Josef K.", "Vor dem Gesetz"]),
    BK("cz-schloss", "The Castle", "城堡", *KAFKA, "1926", lang="de", title_orig="Das Schloss", aliases=["Das Schloss", "Das Schloß"]),
    BK("cz-austerlitz", "Austerlitz", "奥斯特利茨", "W. G. Sebald", "塞巴尔德", "2001", pd=False, lang="de", title_orig="Austerlitz"),
    # ---- from elsewhere ----
    BK("cz-poema-gory", "Poem of the Hill", "山之诗", "Marina Tsvetaeva", "茨维塔耶娃", "1926", lang="ru", title_orig="Поэма горы", aliases=["Поэма горы", "Poem of the Mountain", "Поэма конца"]),
    BK("cz-utz", "Utz", "乌兹", "Bruce Chatwin", "布鲁斯·查特文", "1988", pd=False, lang="en"),
    BK("cz-glass-room", "The Glass Room", "玻璃屋", "Simon Mawer", "西蒙·莫尔", "2009", pd=False, lang="en", aliases=["Landauer", "Villa Tugendhat"]),
    BK("cz-hhhh", "HHhH", "HHhH", "Laurent Binet", "洛朗·比内", "2010", pd=False, lang="fr", aliases=["Himmlers Hirn heißt Heydrich", "Operation Anthropoid", "Heydrich"]),
]
ALCOOLS = "fr-alcools"

# ============================== places ==============================
places = [
    # ---- Prague ----
    ORIG("cz-hrad", "Prague Castle (Hradčany)", "布拉格城堡（赫拉德恰尼）",
         "The castle on its ridge above the Vltava, seat of the Bohemian kings. In Jirásek's legends Princess Libuše, standing on Vyšehrad, foresees a great city and tells her people to build a castle where they find a man hewing a threshold (práh) and to call it Praha. Rilke, born in Prague in 1875, wrote of the 'weathered brow of the old castle' in his first book of Prague poems",
         "伏尔塔瓦河上方山脊上的城堡，波希米亚国王的驻地。伊拉塞克的传说里，女大公莉布舍站在维谢赫拉德预见一座大城，吩咐族人到一个正在凿门槛（práh）的人那里去建城堡，并把它叫做布拉格（Praha）。里尔克 1875 年生在布拉格，他的第一本布拉格诗集里写到“古老王宫风雨剥蚀的额头”"),
    PROTO("cz-svaty-vit", "St Vitus Cathedral", "圣维特大教堂",
          "The cathedral inside Prague Castle. The Trial never names its city, but the cathedral where Josef K. waits in the dark for an Italian client, and where a priest calls him by name from the pulpit and tells him the parable 'Before the Law', is taken to be this one. The agates in which Apollinaire saw his own face are in its St Wenceslas Chapel",
          "布拉格城堡里的主教座堂。《审判》从不说出城市的名字；约瑟夫·K 在黑暗中等一位意大利客户、一位神父从讲坛上直呼他的名字并给他讲“在法的门前”这则寓言的那座大教堂，一般认为就是这里。阿波利奈尔在其中看见自己面孔的玛瑙，就在这里的圣瓦茨拉夫礼拜堂"),
    PIL("cz-zlata-ulicka", "Golden Lane no. 22", "黄金巷 22 号",
        "The tiny house in the castle wall that Kafka's sister Ottla rented in 1916. Kafka came up here to write in the evenings through the winter of 1916–17 and wrote most of the stories of A Country Doctor in it",
        "城堡围墙里的这座小屋是卡夫卡的妹妹奥特拉 1916 年租下的。1916 至 1917 年的那个冬天，卡夫卡每天傍晚上来写作，《乡村医生》里的大部分短篇都是在这里写的", ["cz-landarzt"]),
    PIL("cz-kafka-rodny", "Kafka's birthplace, Náměstí Franze Kafky", "弗朗茨·卡夫卡广场 · 卡夫卡出生地",
        "Franz Kafka was born on 3 July 1883 in a house on this corner beside the Church of St Nicholas, at the edge of the Old Town Square. The house was later rebuilt; only the portal is original, and a bust marks the spot. Almost his whole life was spent within a few hundred metres of it",
        "1883 年 7 月 3 日，弗朗茨·卡夫卡生在老城广场边、圣尼古拉教堂旁这个街角的一座房子里。房子后来重建过，只有大门是原物，墙上有一尊半身像。他几乎一生都生活在离这里几百米的范围之内", ["cz-verwandlung", "cz-prozess"]),
    PIL("cz-kafka-hrob", "Kafka's grave, New Jewish Cemetery", "新犹太公墓 · 卡夫卡墓",
        "Kafka died in a sanatorium near Vienna on 3 June 1924 and was buried here a week later. His parents lie in the same grave; a plaque at its foot remembers his three sisters, who were murdered in the Holocaust",
        "1924 年 6 月 3 日卡夫卡死在维也纳附近的一家疗养院，一周后葬在这里。父母与他同墓；墓脚下的一块牌子纪念他的三个妹妹，她们都死于大屠杀", ["cz-prozess", "cz-schloss", "at-hungerkuenstler"]),
    ORIG("cz-vysehrad", "Vyšehrad", "维谢赫拉德",
         "The rock above the Vltava where legend puts the first seat of the Czech princes. In Jirásek's Old Czech Legends Libuše sits in judgement here under a lime tree, and from here she sends for the ploughman Přemysl and prophesies Prague. Mácha, Němcová, Neruda and Karel Čapek are buried in the cemetery on the rock",
         "伏尔塔瓦河畔的岩石高地，传说中捷克王公最早的驻地。伊拉塞克的《捷克古老传说》里，莉布舍在这里的椴树下断案，从这里派人去请农夫普热米斯尔，并预言了布拉格。马哈、聂姆佐娃、聂鲁达和卡雷尔·恰佩克都葬在高地上的墓园"),
    ORIG("cz-mala-strana", "Malá Strana (Lesser Quarter Square)", "小城区（小城广场）",
         "The quarter of palaces, gardens and steep lanes below the castle. Rilke's Larenopfer walks through it house by house; Neruda's tales are set in its streets",
         "城堡脚下满是宫殿、花园和陡巷的街区。里尔克的《宅神祭品》一座房子一座房子地走过这里；聂鲁达的故事就发生在这里的街巷"),
    ORIG("cz-nerudova", "House at the Two Suns, Nerudova Street", "聂鲁达街 · “两个太阳”之家",
         "Jan Neruda grew up in this house on the steep street up to the castle, then called Ostruhová and now named after him; from 1838 his father kept a shop here, later a tobacconist's. The people of the street are the characters of Tales of the Lesser Quarter",
         "扬·聂鲁达在这条通往城堡的陡街上的这座房子里长大，这条街当时叫马刺街，如今以他的名字命名；他父亲 1838 年起在这里开小铺，后来改卖烟草。街上的人就是《小城故事》里的人物"),
    ORIG("cz-u-kalicha", "U Kalicha (The Chalice)", "“杯子”酒馆",
         "The pub in Na Bojišti street where The Good Soldier Švejk begins: just after the Sarajevo assassination Švejk comes in for a beer, and he and the landlord Palivec are arrested by the plain-clothes man Bretschneider. Later, parting from the sapper Vodička, Švejk tells him to look for him here after the war, any evening from six",
         "战场街上的酒馆，《好兵帅克》从这里开始：萨拉热窝刺杀事件刚发生，帅克进来喝啤酒，结果他和老板帕利韦茨都被便衣警察布雷特施奈德抓走。后来同工兵沃吉契卡分手时，帅克叫他打完仗以后到这里来找他：每天晚上六点起他都在"),
    ORIG("cz-strelecky-ostrov", "Střelecký Island and the Vltava by the National Theatre", "射手岛与民族剧院前的伏尔塔瓦河",
         "At the end of War with the Newts old Mr Povondra, once the doorman who let Captain van Toch in to see the magnate Bondy, is fishing here on a Sunday afternoon with his son, sure that landlocked Bohemia is safe, when a black head rises from the river",
         "《鲵鱼之乱》结尾，老波冯德拉先生——当年就是他当门房时把凡·托赫船长放进去见大亨邦迪的——星期天下午带着儿子在这里钓鱼，满以为没有海岸的波希米亚平安无事，这时河里冒出了一个黑脑袋"),
    ORIG("cz-zidovska-radnice", "Jewish Town Hall", "犹太市政厅",
         "The town hall of the old Jewish quarter has, below its ordinary clock, a second one with Hebrew letters whose hands run backwards. Apollinaire, who visited Prague in 1902, put it into 'Zone', the opening poem of Alcools",
         "旧犹太区的市政厅，在普通的钟下面还有一座刻着希伯来字母的钟，指针是倒着走的。阿波利奈尔 1902 年到过布拉格，把它写进了《醇酒集》的开篇诗《地带》"),
    ORIG("cz-staronova", "Old-New Synagogue", "老新犹太会堂",
         "The thirteenth-century synagogue of the Prague ghetto. Legend says that the clay golem made by Rabbi Löw lies in its attic. Meyrink's novel, set in the lanes of the ghetto just before they were pulled down, makes the Golem a figure that walks the quarter every thirty-three years",
         "布拉格犹太区十三世纪的会堂。传说勒夫拉比用泥土造的魔像就躺在它的阁楼上。梅林克的小说写的是犹太区的小巷拆除前夕，在书里，魔像每三十三年在这一带出现一次"),
    ORIG("cz-stary-zidovsky-hrbitov", "Old Jewish Cemetery", "老犹太公墓",
         "Some twelve thousand tilted gravestones in a walled plot, in use from the fifteenth century to 1787. In Chatwin's Utz the collector of Meissen porcelain lives in a two-room flat at No. 5 Široká Street, overlooking it",
         "围墙里挤着约一万二千块歪斜的墓碑，从十五世纪一直用到 1787 年。查特文的《乌兹》里，那位迈森瓷器收藏家住在宽街 5 号的一套两居室里，俯瞰着这片墓地"),
    ORIG("cz-staromestske-namesti", "Kinský Palace, Old Town Square", "老城广场 · 金斯基宫",
         "From the balcony of this palace Klement Gottwald spoke to the crowd in February 1948 as the Communists took power. The Book of Laughter and Forgetting opens with the photograph of that moment, from which the minister Clementis was later removed, leaving only the fur hat he had put on Gottwald's head. Kafka went to school in the same building",
         "1948 年 2 月共产党夺取政权时，克莱门特·哥特瓦尔德就是在这座宫殿的阳台上向人群讲话的。《笑忘录》以那一刻的照片开篇：后来部长克莱门蒂斯从照片上被抹掉了，只剩下他给哥特瓦尔德戴上的那顶皮帽。卡夫卡的中学也在这座楼里"),
    ORIG("cz-petrin", "Petřín Hill", "佩特任山",
         "The wooded hill above the Lesser Quarter. In The Unbearable Lightness of Being Tereza climbs it, in what turns out to be a dream, and finds a man with a rifle who helps people to die, if it is their own choice. Tsvetaeva, who lived in Prague from 1922 to 1925, wrote her 'Poem of the Hill' about it. Mácha's statue stands among the trees, where lovers bring flowers on the first of May",
         "小城区上方林木茂密的山。《不能承受的生命之轻》里，特蕾莎登上这座山（后来才知道那是一场梦），遇见一个带枪的人——谁自己选择去死，他就帮谁去死。茨维塔耶娃 1922 至 1925 年住在布拉格，她的《山之诗》写的就是这座山。马哈的雕像立在树林间，每年五月一日恋人们来这里献花", book_ids=["cz-maj"]),
    ORIG("cz-na-zabradli", "Theatre on the Balustrade", "栏杆剧院",
         "The small theatre near the Charles Bridge where Havel worked from 1960, first as a stagehand and then as dramaturge. The Garden Party was first performed here in December 1963",
         "查理大桥附近的小剧院，哈维尔从 1960 年起在这里工作，先当舞台工人，后来做戏剧顾问。《游园会》1963 年 12 月在这里首演"),
    PIL("cz-u-zlateho-tygra", "U Zlatého tygra (The Golden Tiger)", "金虎酒馆",
        "The beer hall in Husova Street where Hrabal sat at the same table for decades, listening and telling stories. In January 1994 President Havel brought Bill Clinton here to meet him",
        "胡斯街上的啤酒馆，赫拉巴尔几十年里总坐在同一张桌子旁，听人讲故事，也自己讲。1994 年 1 月，哈维尔总统带着比尔·克林顿到这里来见他", ["cz-prilis-hlucna-samota", "cz-obsluhoval"]),
    ORIG("cz-spalena", "Spálená Street", "焚烧街",
         "Hrabal worked in a waste-paper depot in a cellar in this street from 1954 to 1959. Out of it came Haňťa, the narrator of Too Loud a Solitude, who has been compacting old paper and banned books in a hydraulic press for thirty-five years",
         "1954 至 1959 年，赫拉巴尔在这条街一处地下室的废纸回收站干活。《过于喧嚣的孤独》的叙述者汉嘉就是从这里来的：他用一台液压打包机压废纸和禁书，压了三十五年"),
    ORIG("cz-hotel-pariz", "Hotel Paříž", "巴黎饭店",
         "The hotel beside the Municipal House, designed in 1904 and finished in 1907, neo-Gothic with Art Nouveau detail. In I Served the King of England the small waiter Jan Dítě works here under the head waiter Skřivánek, who knows what every guest will order because, as he says, he served the King of England",
         "市民会馆旁的饭店，1904 年设计、1907 年建成，新哥特式里带着新艺术风格的装饰。《我曾侍候过英国国王》里，小个子侍者扬·迪特在这里跟着领班斯克希万涅克做事；领班能猜出每位客人要点什么，用他的话说，那是因为他侍候过英国国王"),
    PIL("cz-capkova-vila", "The Čapek brothers' house, Vinohrady", "维诺赫拉迪 · 恰佩克兄弟的住宅",
        "Karel Čapek and his brother Josef, the painter, built this double house in 1923–24. Karel's half held the Friday gatherings to which President Masaryk came, and its garden is the one of The Gardener's Year. He died here on 25 December 1938",
        "卡雷尔·恰佩克和当画家的哥哥约瑟夫 1923 至 1924 年盖了这座双拼住宅。卡雷尔那一半里举行“星期五聚会”，总统马萨里克也来参加；《园丁的一年》写的就是这里的花园。1938 年 12 月 25 日他在这里去世", ["cz-zahradnikuv-rok", "cz-valka-s-mloky", "cz-rur"]),
    ORIG("cz-cyril-metodej", "Church of Sts Cyril and Methodius, Resslova Street", "雷斯洛瓦街 · 圣西里尔和美多德教堂",
         "After attacking Reinhard Heydrich on 27 May 1942, the parachutists Jozef Gabčík and Jan Kubiš and five others hid in the crypt of this Orthodox church. Betrayed, they were surrounded by hundreds of SS men on 18 June; three fought from the gallery, four held the crypt while it was flooded, and none was taken alive. HHhH is Binet's account of the attack, and of his own struggle to tell it without inventing",
         "1942 年 5 月 27 日袭击莱因哈德·海德里希之后，伞兵约瑟夫·加布奇克、扬·库比什和另外五人躲进这座东正教堂的地下墓室。因为有人出卖，6 月 18 日他们被几百名党卫军包围：三人在楼座上抵抗，四人守着被灌水的地下墓室，没有一个被活捉。《HHhH》是比内对这次行动的叙述，也写了他自己怎样努力做到不虚构"),
    ORIG("cz-rudolfinum", "Rudolfinum", "鲁道夫音乐厅",
         "The concert hall on the Vltava, with statues of composers along its roof. Weil's novel begins with an order from Heydrich to take down the statue of the Jew Mendelssohn; the workmen, not knowing which he is, look for the biggest nose and start to pull down Wagner",
         "伏尔塔瓦河畔的音乐厅，屋顶上排列着作曲家的雕像。魏尔的小说从海德里希的一道命令写起：把犹太人门德尔松的像拆掉；工人们不知道哪一尊是他，就去找鼻子最大的，结果动手拆起了瓦格纳"),
    ORIG("cz-stavovske", "Estates Theatre", "庄园剧院",
         "Mozart conducted the first performance of Don Giovanni here on 29 October 1787. Mörike's novella imagines one day of the journey from Vienna to that premiere",
         "1787 年 10 月 29 日，莫扎特在这里亲自指挥了《唐璜》的首演。默里克的中篇小说虚构的，就是从维也纳赶来参加这次首演的旅途中的一天"),
    PIL("cz-zizkov", "Žižkov", "日什科夫",
        "Jaroslav Seifert, the only Czech writer to receive the Nobel Prize, was born in 1901 in this working-class quarter of tenements and pubs. His memoirs, All the Beauties of the World, keep coming back to it",
        "雅罗斯拉夫·塞弗尔特是唯一获得诺贝尔文学奖的捷克作家，1901 年生在这个满是出租公寓和小酒馆的工人区。他的回忆录《世界美如斯》一再回到这里", ["cz-vsecky-krasy"]),
    PROTO("cz-stinadla", "Haštalské Square and the old lanes", "哈什塔尔广场一带的老巷",
          "The crooked lanes of old Prague, those of the northern Old Town among them, are generally taken as the model for the Stínadla, the dark quarter into which Foglar's five boys, the Rychlé šípy, go in search of the diary of Jan Tleskač and the puzzle called the hedgehog in the cage",
          "布拉格老城区那些弯弯曲曲的小巷——老城北部这一带就在其中——一般被认为是“斯蒂纳德拉”的原型：福格拉笔下的五个男孩“快箭小队”走进这片昏暗的街区，去找扬·特莱斯卡奇的日记和那件叫“笼中刺猬”的机关玩具"),
    PIL("cz-zbraslav", "Vančura's villa, Zbraslav", "兹布拉斯拉夫 · 万楚拉故居",
        "Vladislav Vančura practised as a doctor at Zbraslav, on the river south of Prague, and built this house there in 1924, to a design by Jaromír Krejcar. The river baths of Summer of Caprice are modelled on those at Zbraslav. He was shot by the Germans on 1 June 1942",
        "弗拉迪斯拉夫·万楚拉在布拉格以南河边的兹布拉斯拉夫行医，1924 年请亚罗米尔·克雷察尔设计，在这里盖了这座房子。《任性的夏天》里的河边浴场，原型就是兹布拉斯拉夫的河滨浴场。1942 年 6 月 1 日他被德国人枪杀", ["cz-rozmarne-leto"]),
    # ---- Central Bohemia ----
    ORIG("cz-karlstejn", "Karlštejn Castle", "卡尔施泰因城堡",
         "The castle Charles IV built from 1348 to guard the imperial crown jewels and relics. Vrchlický's comedy turns on the tradition that no woman might spend the night in it: the Empress and a cup-bearer's sweetheart both get in, disguised as pages",
         "查理四世从 1348 年起修建的城堡，用来保存帝国的王冠珍宝和圣物。弗尔赫利茨基的喜剧抓住一个传说做文章：任何女人不得在城堡里过夜；结果皇后和一个司酒官的恋人都扮成侍童混了进来"),
    ORIG("cz-blanik", "Blaník", "布拉尼克山",
         "The forested hill in which, the last of Jirásek's legends says, an army of knights sleeps under the command of St Wenceslas, to ride out when the Czech land is in its worst need",
         "一座长满森林的山。伊拉塞克最后一则传说讲，山里沉睡着一支由圣瓦茨拉夫统领的骑士军队，等到捷克土地最危难的时候就会出山"),
    ORIG("cz-kostomlaty", "Kostomlaty nad Labem station", "易北河畔科斯托姆拉蒂火车站",
         "Hrabal worked on the railway here during the war, as a labourer and then as a train dispatcher. Closely Watched Trains is set in such a station in 1945: the apprentice Miloš Hrma, back from a failed suicide attempt, the dispatcher Hubička who has stamped the telegraphist's bottom with the station stamps, and a German ammunition train to be blown up",
         "战争期间，赫拉巴尔在这里的铁路上工作，先当铁路工人，后来当调度员。《严密监视的列车》写的就是 1945 年这样一个小站：自杀未遂刚回来的见习生米洛什·赫尔玛，在女报务员屁股上盖满车站公章的调度员胡比奇卡，还有一列要炸掉的德国军火列车"),
    ORIG("cz-nymburk", "Nymburk Brewery", "宁布尔克啤酒厂",
         "Hrabal grew up in this brewery, where his stepfather Francin was the manager. Cutting It Short is his mother's story, told in her voice: Maryška with her knee-length golden hair, the pig-killings, and loud Uncle Pepin, who came for a fortnight and stayed for good",
         "赫拉巴尔在这座啤酒厂里长大，继父弗朗茨是厂里的经理。《一缕秀发》用母亲的口吻讲她自己的故事：留着及膝金发的玛丽什卡，杀猪的日子，还有嗓门奇大的贝宾大伯——他说来住两个星期，结果住下就没再走"),
    PIL("cz-kersko", "Kersko", "克尔斯科",
        "The pine wood on the Elbe plain where Hrabal bought a cottage in 1965 and wrote much of his later work, feeding a growing tribe of cats. The stories of The Snowdrop Festival are about his neighbours here",
        "易北河平原上的松林。1965 年赫拉巴尔在这里买了一座小屋，后期的许多作品都是在这里写的，他还喂着一群越来越多的猫。《雪绒花的庆典》里的故事写的就是他在这里的邻居", ["cz-postriziny", "cz-prilis-hlucna-samota"]),
    PIL("cz-stara-hut", "Karel Čapek Memorial, Strž (Stará Huť)", "旧胡季 · 卡雷尔·恰佩克纪念馆（斯特尔日）",
        "The country house by a pond that Čapek was given the use of for life as a wedding present in 1935. He spent his last three years of summers here, and War with the Newts and The White Disease were among the works written in it",
        "池塘边的这座乡间住宅是 1935 年恰佩克结婚时别人送给他终身使用的礼物。生命的最后三年他常来这里度夏，《鲵鱼之乱》《白色病》等作品都有一部分是在这里写的", ["cz-valka-s-mloky"]),
    ORIG("cz-berounka", "Branov on the Berounka", "贝龙卡河畔布拉诺夫",
         "Ota Pavel's family came every summer to the ferryman Prošek's house at Luh, below Branov, on the river Berounka. His stories are about his father, a Jewish travelling salesman of vacuum cleaners and a passionate fisherman, and the title story about the roebuck poached with the ferryman's dog to feed his sons before they were sent to the camps",
         "奥塔·帕维尔一家每年夏天都到贝龙卡河边、布拉诺夫村下面卢赫的摆渡人普罗谢克家来住。他的故事写的是父亲——一个推销吸尘器的犹太旅行推销员，也是个钓鱼迷；同名的那一篇，讲父亲带着摆渡人的狗偷猎一头牡鹿，好让两个儿子在被送进集中营之前吃上一顿"),
    # ---- South Bohemia ----
    ORIG("cz-putim", "Putim", "普季姆",
         "The village near Písek where Švejk's 'Budějovice anabasis' ends: having missed his train and walked in a great circle looking for his regiment, he is arrested by the gendarmerie sergeant Flanderka, who is certain he has caught a Russian spy",
         "皮塞克附近的村子，帅克的“布杰约维采远征”在这里收场：他误了火车，为了找自己的团兜了一个大圈子，最后被宪兵队长弗兰德尔卡抓住，队长认定自己逮到了一个俄国间谍"),
    PROTO("cz-pisek", "Písek (Stone Bridge)", "皮塞克（石桥）",
          "Šrámek went to the grammar school in Písek, and the unnamed town of The Silver Wind, where the schoolboy Jan Ratkin falls in love, quarrels with his teachers and his father, and feels the wind of youth blowing through everything, is drawn from it",
          "什拉梅克在皮塞克读的文科中学。《银色的风》里那座没有名字的小城就取材于这里：中学生扬·拉特金在那里恋爱，同老师和父亲闹翻，觉得青春的风吹过一切"),
    PIL("cz-horni-plana", "Stifter's birthplace, Horní Planá", "上普拉纳 · 施蒂弗特出生地",
        "Adalbert Stifter was born in this house in the market town of Oberplan on 23 October 1805, the son of a linen weaver. The forests of the Bohemian Forest above the Vltava are the landscape of many of his stories",
        "1805 年 10 月 23 日，阿达尔贝特·施蒂弗特生在集镇上普拉纳（德语名奥伯普兰）的这座房子里，父亲是亚麻织工。伏尔塔瓦河上游波希米亚森林的林海，是他许多小说的风景", ["cz-hochwald", "at-bergkristall", "at-nachsommer"]),
    ORIG("cz-vitkuv-kamen", "Vítkův kámen (Wittinghausen)", "维特库夫卡门（维廷豪森城堡遗址）",
         "The highest castle ruin in Bohemia, on a ridge of the Bohemian Forest. In The High Forest, set in the Thirty Years' War, its lord hides his two daughters in a wooden house by a lake deep in the forest; through a telescope they watch the castle on the skyline, until one morning it has no roof",
         "波希米亚海拔最高的城堡遗址，坐落在波希米亚森林的山脊上。《高山森林》写的是三十年战争：城堡主人把两个女儿藏进森林深处湖边的一座木屋；她们用望远镜望着天际线上的城堡，直到有一天早晨它没有了屋顶"),
    # ---- Plzeň Region ----
    ORIG("cz-breznik", "Březník (Pürstling)", "布热兹尼克（皮尔斯特林克）",
         "The forester's lodge on a high moor of the Šumava, half an hour from the Bavarian border, below Mount Luzný. Klostermann's novel is set here in the 1860s, with the forester Kořán and the long winters that cut the lodge off from the world",
         "舒马瓦高地沼泽上的林务所，离巴伐利亚边界半小时路程，就在卢兹尼山下。克洛斯特曼的小说写的是 19 世纪 60 年代的这里：林务官科热恩，还有把林务所同外界隔绝的漫长冬天"),
    # ---- Karlovy Vary Region ----
    ORIG("cz-marianske-lazne", "Mariánské Lázně (Marienbad)", "玛丽亚温泉市（玛丽恩巴德）",
         "The spa where Goethe spent the summers of 1821 to 1823 and, in 1823, asked for the hand of the nineteen-year-old Ulrike von Levetzow, fifty-four years his junior; refused, he began the Marienbad Elegy in the carriage on the way home. In Austerlitz it is the place of a last family holiday in 1938, and of a return in 1972 that goes inexplicably wrong",
         "歌德 1821 至 1823 年在这座温泉城度夏，1823 年向比他小五十四岁、年方十九的乌尔丽克·冯·莱韦措求婚；被拒绝之后，他在回程的马车上动笔写《玛丽恩巴德悲歌》。在《奥斯特利茨》里，这里是 1938 年一家人最后一次度假的地方，也是 1972 年一次莫名其妙变了味的重访之地"),
    # ---- Ústí nad Labem Region ----
    ORIG("cz-rip", "Říp", "日普山",
         "The round hill that stands alone in the plain north of Prague. In the first of Jirásek's legends Forefather Čech climbs it, looks over the country and tells his people that this is the promised land. A Romanesque rotunda stands on the top",
         "布拉格以北平原上孤零零的一座圆形小山。伊拉塞克的第一则传说里，先祖切赫登上山顶眺望四野，告诉族人这就是应许之地。山顶上有一座罗马式圆形小教堂"),
    ORIG("cz-terezin", "Terezín (Theresienstadt)", "泰雷津（特莱西恩施塔特）",
         "The fortress town built under Joseph II, made by the Germans in 1941 into a ghetto through which some 140,000 Jews passed, most of them on the way to the death camps. In Sebald's novel Jacques Austerlitz, sent from Prague to Wales on a children's transport in 1939, comes here in search of his mother Agáta and walks through streets of shut doors",
         "约瑟夫二世时修建的要塞城，1941 年被德国人改成隔都，约十四万犹太人经过这里，大多数被转送到灭绝营。塞巴尔德的小说里，雅克·奥斯特利茨 1939 年随儿童专列从布拉格被送到威尔士，后来到这里寻找母亲阿加塔，走过一条条门户紧闭的街道"),
    PIL("cz-litomerice", "Litoměřice", "利托梅日采",
        "Mácha came to Litoměřice in the autumn of 1836 to work as a legal clerk and died here on 6 November, days before his twenty-sixth birthday and his own wedding; May had come out that spring. He was buried here; in October 1938 his remains were exhumed, and in May 1939 they were reburied at Vyšehrad",
        "1836 年秋天，马哈到利托梅日采当司法见习书记员，11 月 6 日死在这里，再过几天就是他二十六岁生日和婚礼；《五月》是那年春天出版的。他先葬在这里；1938 年 10 月遗骨被起出，1939 年 5 月改葬维谢赫拉德", ["cz-maj"]),
    # ---- Liberec Region ----
    ORIG("cz-machovo-jezero", "Lake Mácha (Máchovo jezero)", "马哈湖",
         "The great pond below the castle of Bezděz, near Doksy, which Mácha knew from his walking tours and made the setting of May: the lake at evening, the girl waiting on the shore, the prisoner in the tower across the water and the execution hill. It has been called by his name since the twentieth century",
         "多克西附近、贝兹杰兹城堡脚下的大池塘。马哈徒步旅行时来过这里，把它写成了《五月》的背景：黄昏的湖，在岸边等待的姑娘，湖对面塔里的囚徒，还有刑场的山丘。二十世纪以来，它就以他的名字命名"),
    # ---- Hradec Králové Region ----
    ORIG("cz-ratiborice", "Ratibořice (Grandmother's Valley)", "拉蒂博日采（外祖母山谷）",
         "Božena Němcová spent her childhood on the estate of Ratibořice, where her father was a groom to the Duchess of Sagan. The Grandmother, written in Prague in poverty after the death of her son, goes back to it: the Old Bleachery, the mill, the weir where mad Viktorka sings, the château and its princess",
         "聂姆佐娃的童年是在拉蒂博日采庄园度过的，父亲是扎甘女公爵的马夫。《外祖母》是她在布拉格的贫困中、在儿子死后写的，写的就是回到这里：老漂布场，磨坊，疯姑娘维克多卡唱歌的水坝，还有庄园和公爵夫人"),
    PIL("cz-miletin", "Erben's birthplace, Miletín", "米莱廷 · 爱尔本出生地",
        "Karel Jaromír Erben, archivist of the city of Prague and collector of folk songs and tales, was born in this small town in 1811. Kytice, his one book of poems, turns folk legends into ballads, thirteen poems in its final form: the water goblin, the noon witch, the wedding shirts",
        "卡雷尔·雅罗米尔·爱尔本是布拉格市的档案官，也是民歌和民间故事的搜集者，1811 年生在这个小镇。《花束集》是他唯一的一本诗集，把民间传说写成了叙事谣曲，定本共十三首：水鬼，正午女巫，婚礼衬衫", ["cz-kytice"]),
    PIL("cz-hronov", "Jirásek's birthplace, Hronov", "赫罗诺夫 · 伊拉塞克出生地",
        "Alois Jirásek was born in this wooden cottage in 1851, the son of a baker and weaver. He taught history for a living and wrote the historical novels and the Old Czech Legends from which generations of Czech children learned their past",
        "1851 年，阿洛伊斯·伊拉塞克生在这座木屋里，父亲是面包师兼织工。他以教历史为业，写了许多历史小说和《捷克古老传说》，一代代捷克孩子都是从这些书里认识本民族的过去的", ["cz-stare-povesti", "cz-filosofska-historie"]),
    PIL("cz-male-svatonovice", "Čapek Brothers Museum, Malé Svatoňovice", "小斯瓦托纽维采 · 恰佩克兄弟博物馆",
        "Karel Čapek was born in this house on 9 January 1890, the son of a country doctor. The word 'robot', which his play R.U.R. gave to the world in 1920, was suggested to him by his brother Josef",
        "1890 年 1 月 9 日，卡雷尔·恰佩克生在这座房子里，父亲是乡村医生。1920 年他的剧本《罗素姆万能机器人》让全世界有了“robot（机器人）”这个词，这个词是哥哥约瑟夫给他出的主意", ["cz-rur", "cz-valka-s-mloky"]),
    PROTO("cz-nachod", "Náchod", "纳霍德",
          "Škvorecký was born in Náchod in 1924, and it is the Kostelec of The Cowards: eight days in May 1945, seen by the saxophonist Danny Smiřický, who cares more for jazz and girls than for the town's cautious uprising against the retreating Germans",
          "什克沃雷茨基 1924 年生在纳霍德，这里就是《懦夫们》里的科斯特莱茨：1945 年 5 月的八天，由萨克斯手丹尼·斯米日茨基讲述——比起小城对撤退德军那场小心翼翼的起义，他更在乎爵士乐和姑娘"),
    PROTO("cz-rychnov", "Rychnov nad Kněžnou", "克涅日纳河畔里赫诺夫",
          "Karel Poláček was born in this small town in 1892, the son of a Jewish shopkeeper. He wrote There Were Five of Us, the adventures of the schoolboy Petr Bajza and his four friends, in the months before he was deported in 1943; he did not come back, and the book appeared in 1946",
          "1892 年卡雷尔·波拉切克生在这座小城，父亲是犹太店主。《我们五个》写的是小学生彼得·巴伊扎和四个伙伴的故事，是他在 1943 年被遣送之前的几个月里写的；他没能回来，书在 1946 年出版"),
    PIL("cz-hradecek", "Hrádeček", "赫拉德切克",
        "Havel bought this farmhouse in the foothills of the Krkonoše in 1967. In the years when his plays were banned he lived here under secret-police surveillance, and here in the autumn of 1978 he wrote The Power of the Powerless. He died in the house on 18 December 2011",
        "1967 年，哈维尔买下克尔科诺谢山麓的这座农舍。在剧本遭禁的年月里他住在这里，受着秘密警察的监视；1978 年秋天他在这里写了《无权者的权力》。2011 年 12 月 18 日，他在这座房子里去世", ["cz-moc-bezmocnych", "cz-zahradni-slavnost"]),
    # ---- Pardubice Region ----
    ORIG("cz-litomysl", "Litomyšl", "利托米什尔",
         "The arcaded town with its Renaissance château, where Jirásek taught at the grammar school from 1874 to 1888. A Philosophers' Story is set among its students in 1847–48: their forbidden May festival, their lodgings with the old maid Miss Elis, and the barricades of Prague",
         "有拱廊街道和文艺复兴式城堡的小城，伊拉塞克 1874 至 1888 年在这里的文科中学教书。《哲学生的故事》写的是 1847 至 1848 年这里的学生：被禁止的五月节，他们寄宿的老姑娘埃莉斯小姐家，还有布拉格的街垒"),
    PIL("cz-brandys-orlice", "Brandýs nad Orlicí", "奥尔利采河畔布兰迪斯",
        "After the defeat of the Bohemian Protestants, Comenius found shelter on the estate of Karel the Elder of Žerotín at Brandýs. The Labyrinth of the World, whose first version he finished in 1623 and dedicated to Žerotín, belongs to these years of hiding",
        "波希米亚新教徒战败之后，夸美纽斯在老卡雷尔·热罗丁位于布兰迪斯的庄园里得到庇护。《世界迷宫与心灵天堂》的初稿完成于 1623 年，题献给热罗丁，正是这段躲藏岁月的作品", ["cz-labyrint"]),
    b.P("cz-krematorium", "Crematorium, Pardubice", "帕尔杜比采火葬场", *C("cz-krematorium"), "film_location",
        adaptation={"title": "Spalovač mrtvol (The Cremator)", "year": 1969, "kind": "电影"},
        scene="科普夫金格尔先生工作的火葬场。尤拉伊·赫尔茨的这部电影有一部分是在帕维尔·亚纳克设计的这座立体主义风格建筑里拍的；小说里的火葬场在布拉格",
        book_ids=["cz-spalovac"],
        scene_en="the crematorium where Mr Kopfrkingl works. Juraj Herz shot part of his film in this building designed by Pavel Janák; the crematorium of the novel is in Prague"),
    # ---- Vysočina ----
    PIL("cz-lipnice", "Lipnice nad Sázavou", "萨扎瓦河畔利普尼采",
        "Hašek came to this village under its castle in August 1921 and stayed. He dictated most of The Good Soldier Švejk in the inn U České koruny, bought a small house below the castle, and died in it, with the novel unfinished, on 3 January 1923. He is buried in the village",
        "1921 年 8 月，哈谢克来到城堡脚下的这个村子，就此住了下来。《好兵帅克》的大部分是他在“捷克王冠”客栈里口述的；他在城堡下买了一座小房子，1923 年 1 月 3 日死在里面，小说没有写完。他葬在村里", ["cz-svejk"]),
    PIL("cz-borova", "Havlíčkova Borová", "哈夫利切克的博罗瓦",
        "Karel Havlíček, the founder of Czech political journalism, was born here in 1821. In December 1851 the police took him from his bed and carried him to exile at Brixen in the Tyrol; the Tyrolean Elegies tell the journey as a mocking ballad",
        "捷克政论新闻的奠基人卡雷尔·哈夫利切克 1821 年生在这里。1851 年 12 月，警察把他从床上带走，押往蒂罗尔的布里克森流放；《蒂罗尔哀歌》用嘲讽的谣曲讲了这趟旅程", ["cz-tyrolske-elegie"]),
    # ---- South Moravia ----
    PROTO("cz-tugendhat", "Villa Tugendhat, Brno", "布尔诺 · 图根哈特别墅",
          "The house Mies van der Rohe built in 1929–30 for Fritz and Grete Tugendhat, with a wall of onyx and a living room whose glass front sinks into the floor. It is the Landauer House of The Glass Room, which follows it through the family's flight, the German occupation, the Soviet soldiers quartered in it in 1945 and decades as a children's physiotherapy centre",
          "密斯·凡·德·罗 1929 至 1930 年为弗里茨和格蕾特·图根哈特夫妇建造的住宅，有一面缟玛瑙墙，起居室的玻璃立面能沉入地板。它就是《玻璃屋》里的兰道尔宅；小说跟着这座房子走过主人一家的逃亡、德国占领、1945 年驻扎进来的苏军士兵，以及做儿童理疗中心的几十年"),
    ORIG("cz-bilovice", "Bílovice nad Svitavou", "斯维塔瓦河畔比洛维采",
         "The village in the wooded valley north of Brno where Těsnohlídek lived and where he set the story of the forester and the vixen he brings home as a cub. It ran as a serial in the Brno paper Lidové noviny in 1920, written to fit a set of drawings by Stanislav Lolek; Janáček made his opera from it",
         "布尔诺以北林木茂密的河谷里的村子，捷斯诺赫利德克在这里住过，林务官把小母狐带回家的故事也发生在这里。1920 年它在布尔诺的《人民报》上连载，是配着斯坦尼斯拉夫·洛莱克的一组画写的；雅纳切克根据它写了歌剧"),
    # ---- Olomouc Region ----
    PROTO("cz-hranice", "Military Academy, Hranice (Mährisch Weißkirchen)", "赫拉尼采军事学院（梅里施-魏斯基兴）",
          "Musil was a cadet at the military school here from 1894 to 1897; Rilke had entered it in 1890 and left within months. It is the remote boarding school of Young Törless, where two boys torment a third, Basini, in an attic room, and Törless watches and takes part",
          "1894 至 1897 年，穆齐尔是这所军校的学员；里尔克 1890 年也进过这所学校，没几个月就离开了。它就是《学生托乐思的迷惘》里那所偏僻的寄宿学校：两个男生在阁楼的密室里折磨第三个男生巴西尼，托乐思在一旁看着，也参与其中"),
    PIL("cz-prostejov", "Wolker's birthplace, Prostějov", "普罗斯捷约夫 · 沃尔克出生地",
        "Jiří Wolker was born in this house in 1900 and died of tuberculosis at home in Prostějov in January 1924, not yet twenty-four. A Difficult Hour, his second and last book, holds the ballads of the stoker's eyes and of the unborn child",
        "1900 年，伊日·沃尔克生在这座房子里；1924 年 1 月，他因肺结核在普罗斯捷约夫的家中去世，还不满二十四岁。《沉重的时刻》是他的第二本、也是最后一本诗集，收有《司炉的眼睛》《未出生的孩子》等叙事谣曲", ["cz-tezka-hodina"]),
    # ---- Zlín Region ----
    PROTO("cz-vlcnov", "Vlčnov (Ride of the Kings)", "弗尔奇诺夫（国王骑行）",
          "On the last Sunday in May a boy in women's costume, a rose between his teeth, rides through this village with his mounted escort. The Joke ends at such a Ride of the Kings in Ludvík Jahn's unnamed home town in Moravian Slovakia, and Jaromil Jireš filmed the scene here in 1968",
          "每年五月的最后一个星期天，一个身穿女装、嘴里衔着玫瑰的男孩在骑马护卫的簇拥下穿过这个村子。《玩笑》的结尾就是这样一场“国王骑行”，地点是路德维克·扬在摩拉维亚斯洛伐克地区的家乡小城，书里没有写出城名；1968 年亚罗米尔·伊雷什在这里拍了这场戏"),
    PIL("cz-zdislavice", "Zdislavice", "兹迪斯拉维采",
        "Marie von Ebner-Eschenbach was born at the château of Zdislavice in 1830, of the Dubsky family, and lies in the family tomb here. The villagers, foresters and dogs of her Moravian stories, Krambambuli among them, belong to this countryside",
        "玛丽·冯·埃布纳-埃申巴赫 1830 年生在兹迪斯拉维采的庄园，娘家姓杜布斯基，死后葬在这里的家族墓室。她那些摩拉维亚故事里的村民、林务员和狗——包括克兰巴姆布里——都属于这片乡土", ["cz-krambambuli"]),
    # ---- Moravia-Silesia ----
    ORIG("cz-stare-hamry", "Staré Hamry", "旧哈姆里",
         "The village in the Beskids of Bezruč's ballad 'Maryčka Magdónova': the daughter of a miner killed on his way home from the pub, caught gathering wood in the Marquis Gero's forest, throws herself into the Ostravice as she is led under guard to Frýdek. Her monument stands in the village",
         "贝兹鲁奇的叙事诗《玛丽奇卡·马格多诺娃》写的贝斯基德山村：一个矿工从酒馆回家路上丧了命，他的女儿在赫罗侯爵的林子里拾柴被抓，被押往弗里代克的路上，她跳进了奥斯特拉维采河。村里立着她的纪念像"),
    ORIG("cz-ostrava", "Ostrava (Michal Mine)", "奥斯特拉瓦（米哈尔矿井）",
         "The city of coal and steel. In The Joke Ludvík Jahn, expelled from the Party and the university for a postcard, is sent here in the early 1950s to a penal battalion of 'blacks', soldiers without weapons who work in the mines; here he meets Lucie. The Michal pit is kept as it was on its last working day",
         "煤和钢的城市。《玩笑》里，路德维克·扬因为一张明信片被开除党籍和学籍，20 世纪 50 年代初被送到这里的惩戒营——营里的“黑帮兵”不发枪，只下矿井干活；他在这里遇见了露茜。米哈尔矿井保持着最后一个工作日的原样"),
]

# ============================== lines ==============================
lines = [
    Q("cz-maj-1", "cz-maj", "cz-machovo-jezero", "Canto 1, opening", "第一歌开篇", "Czech", "Máj (Mácha)/1",
      raw("Máj (Mácha)/1", "Byl pozdní večer — první máj —", "planoucí tam co slzy lásky."), ["Jezero hladké"],
      "It was late evening – the first of May –\nan evening in May – it was love's hour.\nThe turtle-dove's voice called to love\nwhere the pine grove gave its scent.\nThe quiet moss whispered of love;\nthe flowering tree feigned love's sorrow,\nthe nightingale sang his love to the rose,\nand the rose answered with a fragrant sigh.\nThe smooth lake in the shady bushes\nsounded darkly a secret pain,\nthe shore embraced it round and round;\nand the bright suns of other worlds\nwandered along the bands of azure,\nburning there like tears of love.",
      ["The smooth lake"],
      "夜已深——五月的第一天——\n五月的夜晚——正是爱的时光。\n斑鸠的声音在呼唤爱情，\n松林在那里散发幽香。\n静静的青苔低语着爱；\n开花的树假装为爱忧伤，\n夜莺向玫瑰歌唱它的爱，\n玫瑰用一声芬芳的叹息回应。\n平滑的湖在幽暗的灌木丛间\n低沉地响着隐秘的痛苦，\n湖岸把它一圈一圈地拥抱；\n别的世界里那些明亮的太阳\n沿着蔚蓝的天带游荡，\n在那里燃烧，像爱的泪珠。",
      ["平滑的湖"]),
    Q("cz-babicka-1", "cz-babicka", "cz-ratiborice", "Chapter 1", "第一章", "Czech", "Babička/I",
      raw("Babička/I", "Jakého to očekávání, jakého radování na Starém bělidle!", "za byt vykázáno bylo."), ["Starém bělidle"],
      "What expectation, what rejoicing there was at the Old Bleachery! For that was what people called the lonely building in a lovely little valley which had been assigned as a home to Mrs Prošek, Grandmother's daughter.",
      ["the Old Bleachery"],
      "老漂布场上，大家是怎样地盼望、怎样地欢喜啊！人们就是这样称呼那座孤零零的房子的，它坐落在一个可爱的小山谷里，是拨给外祖母的女儿普罗什科娃太太一家住的。",
      ["老漂布场"]),
    Q("cz-neruda-1", "cz-povidky-malostranske", "cz-nerudova", "'Hastrman' (The Water Sprite)", "《水鬼》", "Czech", "Povídky malostranské/Hastrman",
      raw("Povídky malostranské/Hastrman", "Bylo to v sluneční den srpnový", "kráčejícím dolů."), ["Ostruhovou ulicí"],
      "It was a sunny August day, about three o'clock in the afternoon. Whoever happened to be walking along Ostruhová Street stopped; whoever happened to be standing outside in his house clothes quickly called something indoors; people ran out of the shops. Everyone was looking after Mr Rybář, who was walking down the hill.",
      ["Ostruhová Street"],
      "那是八月里一个晴朗的日子，下午三点钟光景。正走在马刺街上的人都站住了；穿着家常衣服站在门外的人，赶忙朝屋里喊一声；店铺里的人也跑了出来。大家都望着正往坡下走的雷巴日先生。",
      ["马刺街"]),
    Q("cz-povesti-1", "cz-stare-povesti", "cz-rip", "'O Čechovi' (Of Čech)", "《切赫的故事》", "Czech", SPS + "O Čechovi",
      raw(SPS + "O Čechovi", "Došli a položili se na úpatí hory, jež slove Říp.", "jako rozlité stříbro."), ["Říp"],
      "They came and lay down at the foot of the mountain that is called Říp. The chieftains and the elders of the clan looked over the land around and saw that it was fertile. In the morning, at first light, Čech rose and set out all alone up to the top of Říp through the quiet forest, still full of the gloom of night.\nWhen he had climbed the mountain it was morning; and behold, a wide, wide country spread before him into the far distance, level and open as far as the bluish mountains, forest and thicket, meadows and fields. Through its lush green the rivers shone like spilt silver.",
      ["Říp"],
      "他们来到一座名叫日普的山脚下安顿下来。首领们和族中的长老察看了四周的土地，见它很肥沃。第二天清晨，天刚破晓，切赫起身，独自一人穿过还笼罩着夜色的寂静森林，登上日普山顶。\n他登上山时天已大亮；看哪，辽阔的原野在他面前伸展到望不到头的远方，平坦而开阔，直到泛着蓝色的群山，有森林和灌丛，有田野和草地。在一片浓绿之中，河流像泼洒的白银一样闪光。",
      ["日普"]),
    Q("cz-povesti-2", "cz-stare-povesti", "cz-vysehrad", "'O Libuši' (Of Libuše)", "《莉布舍的故事》", "Czech", SPS + "O Libuši",
      raw(SPS + "O Libuši", "Žádný nechtěl v tom sporu povoliti", "kobercem prostřeném."), ["Vyšehrad"],
      "Neither would give way in the dispute, each was as hard as flint, and as soon as the time came when the princess sat in judgement, both hurried to Vyšehrad.\nThere Libuše, a snow-white band about her brow, sat judging under a spreading lime tree, on a raised seat laid with a carpet.",
      ["Vyšehrad"],
      "两人在这场争执里谁也不肯让步，都硬得像燧石；一到女大公升座断案的时候，两人就急忙赶往维谢赫拉德。\n莉布舍额上束着雪白的头带，坐在一棵枝繁叶茂的椴树下，在铺着毯子的高座上审理案件。",
      ["维谢赫拉德"]),
    Q("cz-povesti-3", "cz-stare-povesti", "cz-hrad", "'Libušina proroctví' (Libuše's Prophecies)", "《莉布舍的预言》", "Czech", SPS + "Libušina proroctví",
      raw(SPS + "Libušina proroctví", "„Město vidím veliké", "bude slovutno světu.“"), ["Prahou", "Vltava řeka"],
      "'I see a great city, whose glory will touch the stars.\nThere in the forest is a place, thirty furlongs from here, and the river Vltava flows around it.\nOn the north the brook Brusnice bounds it with a deep ravine, and on the south a rocky hill beside the forest of Strahov.\nWhen you come there you will find a man in the midst of the forest, hewing the threshold of a house.\nAnd you shall call the castle that you build Praha. And as princes and chieftains bow their heads before a threshold, so shall they bow before my city.\nHonour and praise shall be its portion, and it shall be famed through the world.'",
      ["Praha", "the river Vltava"],
      "“我看见一座大城，它的荣耀将与星辰相接。\n那边森林里有一处地方，离这里约三十弗隆，伏尔塔瓦河环绕着它。\n北面有布鲁斯尼采溪的深谷为界，南面是斯特拉霍夫森林旁的一座石山。\n你们到了那里，会在林中遇见一个人，他正在凿一座房子的门槛。\n你们建起的城堡，就叫它布拉格。正如王公和首领在门槛前要低头，他们在我的城前也要低头。\n它将享有尊荣和赞美，名扬世界。”",
      ["布拉格", "伏尔塔瓦河"]),
    Q("cz-povesti-4", "cz-stare-povesti", "cz-blanik", "'Blaničtí rytíři' (The Knights of Blaník)", "《布拉尼克的骑士》", "Czech", SPS + "Blaničtí rytíři",
      raw(SPS + "Blaničtí rytíři", "Hle, Blaník hora v hávu tmavého lesa", "pláně málo úrodné."), ["Blaník"],
      "Behold Blaník, a mountain in a robe of dark forest that flows down from its crown over all its sides. Gravely, even sullenly, it looks down on a country remote from the world, on its hills and its plains of little fertility.",
      ["Blaník"],
      "看那布拉尼克山，披着深色森林的长袍，从山顶一直垂到四面山坡。它庄重地、甚至阴沉地俯视着这片远离尘世的土地，俯视着那些丘陵和不大肥沃的平野。",
      ["布拉尼克"]),
    Q("cz-filosofska-1", "cz-filosofska-historie", "cz-litomysl", "Prologue", "序幕", "Czech", "Filosofská historie/Prolog",
      raw("Filosofská historie/Prolog", "Vedle starožitného, šestitřídního gymnasia", "obmezeny na dva."), ["v Litomyšli"],
      "Beside the ancient six-class grammar school, philosophical studies were set up at Litomyšl by Francis I in 1802, at first with three years, which in 1842 were reduced to two.",
      ["at Litomyšl"],
      "除了那所古老的六年制文科中学，1802 年弗朗茨一世又在利托米什尔设立了哲学班，起初是三个年级，1842 年减为两个。",
      ["利托米什尔"]),
    Q("cz-karlstejn-1", "cz-noc-na-karlstejne", "cz-karlstejn", "Act 1, scene 1", "第一幕第一场", "Czech", "Noc na Karlštejně/Jednání první",
      raw("Noc na Karlštejně/Jednání první", "Jeho Milost jede sem pouze na dva nebo tři dny;", "vystavěn Karlštejn!"), ["Karlštejn"],
      "His Grace is coming here for only two or three days; – here he wants to have peace, he wants to rest; he is not even here yet, and already his quiet is in danger! Truly, that is not what Karlštejn was built for!",
      ["Karlštejn"],
      "陛下到这里来只住两三天；——他想在这里图个清静，想歇一歇；人还没到，他的安宁就已经受到威胁了！卡尔施泰因可真不是为这个建的！",
      ["卡尔施泰因"]),
    Q("cz-klostermann-1", "cz-lesni-samoty", "cz-breznik", "Chapter 1, opening", "第一章开篇", "Czech", "Ze světa lesních samot/I.",
      raw("Ze světa lesních samot/I.", "Bůh ví, jaký osud zanesl revírníka Kořána", "sotva lidská noha cestu našla."), ["do Pürstlinku"],
      "God knows what fate carried the forester Kořán, in the year 186*, to Pürstling, which lies half an hour from the Bavarian border in the midst of forests and peat bogs, where thirty years earlier a human foot had hardly found its way.",
      ["to Pürstling"],
      "天知道是什么命运，在一八六几年把林务官科热恩带到了皮尔斯特林克——那地方离巴伐利亚边界半小时路程，四周是森林和泥炭沼，三十年前几乎还没有人迹。",
      ["皮尔斯特林克"]),
    Q("cz-svejk-1", "cz-svejk", "cz-u-kalicha", "Part 1, chapter 1", "第一卷第一章", "Czech", SV + "Zasáhnutí dobrého vojáka Švejka do světové války",
      raw(SV + "Zasáhnutí dobrého vojáka Švejka do světové války", "V hospodě U kalicha seděl jen jeden host.", "ve službách státní policie."), ["U kalicha"],
      "In the pub U Kalicha there sat only one customer. It was the plain-clothes policeman Bretschneider, who was in the service of the state police.",
      ["U Kalicha"],
      "“杯子”酒馆里只坐着一位客人。那是便衣警察布雷特施奈德，在国家警察局当差。",
      ["“杯子”酒馆"]),
    Q("cz-svejk-2", "cz-svejk", "cz-putim", "Part 2, chapter 2, 'Švejk's Budějovice Anabasis'", "第二卷第二章“帅克的布杰约维采远征”", "Czech", SV + "Švejkova budějovická anabaze",
      raw(SV + "Švejkova budějovická anabaze", "Švejk šel opět hnedle celou noc", "našel v poli stoh."), ["u Putimě"],
      "Švejk again walked almost the whole night, until somewhere near Putim he found a haystack in a field.",
      ["near Putim"],
      "帅克又差不多走了一整夜，直到在普季姆附近的田里找到一个草垛。",
      ["普季姆"]),
    Q("cz-mloci-1", "cz-valka-s-mloky", "cz-strelecky-ostrov", "Book 3, 'Mr Povondra Takes It upon Himself'", "第三卷“波冯德拉先生把责任揽到自己身上”", "Czech", "Válka s mloky/Pan Povondra to bere na sebe",
      raw("Válka s mloky/Pan Povondra to bere na sebe", "Bylo ticho nad vodou.", "postupovala pomalu proti proudu."), ["Střeleckém ostrově", "před Národním divadlem"],
      "It was quiet over the water. The trees on Střelecký Island were already laying long, delicate shadows on the surface of the Vltava. A tram tinkled on the bridge; along the embankment strolled nannies with prams and sober Sunday people –\n“Dad,” breathed young Povondra, almost like a child.\n“What is it?”\n“Isn't that a catfish over there?”\n“Where?”\nOut of the Vltava, right in front of the National Theatre, a big black head was showing above the water and moving slowly upstream.",
      ["Střelecký Island", "in front of the National Theatre"],
      "水面上一片寂静。射手岛上的树已经把又长又柔的影子投在伏尔塔瓦河面上。桥上电车叮当作响，沿河大道上走着推童车的保姆和稳重的、过星期天的人们——\n“爸，”小波冯德拉像孩子似的轻轻叫了一声。\n“怎么啦？”\n“那边那个是不是鲶鱼？”\n“哪儿？”\n就在民族剧院前面的伏尔塔瓦河里，一个又大又黑的脑袋露出水面，慢慢地逆流而上。",
      ["射手岛", "民族剧院前面"]),
    Q("cz-kafka-1", "cz-prozess", "cz-svaty-vit", "Chapter 9, 'In the Cathedral'", "第九章“在大教堂里”", "German", "Der Prozess/9. Kapitel",
      raw("Der Prozess/9. Kapitel", "Der Domplatz war ganz leer", "jetzt hierherzukommen."), ["Domplatz", "im Dom"],
      "The cathedral square was quite empty; K. remembered that even as a small child he had noticed that in the houses of this narrow square almost all the window blinds were always down. In today's weather, though, it was more understandable than usual. The cathedral seemed to be empty too; naturally it occurred to nobody to come here now.",
      ["cathedral square", "The cathedral"],
      "大教堂广场上空无一人；K. 想起来，他还是个小孩子的时候就注意到，这个狭窄广场四周的房子，窗帘几乎总是全都放下的。不过像今天这样的天气，这倒比平时更好理解。大教堂里似乎也是空的，这种时候自然谁也不会想到上这儿来。",
      ["大教堂广场", "大教堂里"]),
    Q("cz-rilke-1", "cz-larenopfer", "cz-hrad", "'Der Hradschin', stanzas 1–2", "《赫拉德恰尼》第一、二节", "German", "Der Hradschin",
      raw("Der Hradschin", "Schau so gerne die verwetterte", "ernst auf ihn."), ["Hradschin", "der alten Hofburg"],
      "I so like to look at the weathered\nbrow of the old castle;\nalready the child's gaze used to climb\nup there.\nAnd even the hurrying\nwaves of the Vltava greet the Hradschin,\nand from the bridge the saints\nlook gravely towards it.",
      ["Hradschin", "the old castle"],
      "我多爱看那古老王宫\n风雨剥蚀的额头；\n孩提时我的目光就已\n向那上面攀登。\n连伏尔塔瓦河匆匆的波浪\n也向赫拉德恰尼致意，\n桥上的圣徒们\n神情庄重地望着它。",
      ["赫拉德恰尼", "古老王宫"]),
    Q("cz-rilke-2", "cz-larenopfer", "cz-mala-strana", "'Auf der Kleinseite', stanzas 1–2", "《在小城区》第一、二节", "German", "Auf der Kleinseite",
      raw("Auf der Kleinseite", "Alte Häuser, steilgegiebelt,", "rieseln Rosenketten."), ["Alte Häuser"],
      "Old houses, steeply gabled,\nhigh towers full of ringing bells –\ninto the narrow courtyards flirts\nonly a tiny scrap of sky.\nAnd on every newel post,\nsmiling wearily – cupids;\nhigh on the roof, round baroque\nvases, trickle chains of roses.",
      ["Old houses"],
      "老房子，山墙陡峭，\n高塔上钟声不断——\n挤进狭窄院落里调情的\n只有小小的一片天。\n每一根楼梯柱头上，\n都有疲倦地微笑着的小爱神；\n高高的屋顶上，巴洛克花瓶四周\n垂落着一串串玫瑰。",
      ["老房子"]),
    Q("cz-zone-1", ALCOOLS, "cz-zidovska-radnice", "'Zone'", "《地带》", "French", "Alcools/Zone",
      raw("Alcools/Zone", "Épouvanté tu te vois dessiné dans les agates de Saint-Vit", "chanter des chansons tchèques"), ["l’horloge du quartier juif"],
      "Appalled you see yourself drawn in the agates of Saint Vitus\nYou were sad enough to die the day you saw yourself there\nYou look like Lazarus bewildered by the daylight\nThe hands of the clock in the Jewish quarter go backwards\nAnd you too go slowly backwards in your life\nClimbing up to the Hradchin and in the evening listening\nTo Czech songs being sung in the taverns",
      ["the clock in the Jewish quarter"],
      "你惊恐地看见自己被画在圣维特的玛瑙里\n在那里看见自己的那天你悲伤得要死\n你像被日光惊呆的拉撒路\n犹太区那座钟的指针在倒着走\n你也在自己的生命里慢慢后退\n一边登上赫拉德恰尼 晚上一边听\n小酒馆里唱着捷克的歌",
      ["犹太区那座钟"]),

    # ---------- scene notes ----------
    S("cz-golem-s1", "cz-golem", "cz-staronova", "Throughout", "全书",
      "The narrator dreams himself into the life of Athanasius Pernath, a cutter of gems who lives in the Prague ghetto and cannot remember his past. A stranger brings him a book to repair and is gone; the neighbours say the Golem has been seen again. Around him move the junk dealer Wassertrum, the student Charousek who hates him, the archivist Hillel and his daughter Mirjam, until Pernath is thrown into prison for a murder and comes out to find the ghetto being torn down.",
      "叙述者在梦中进入了阿塔纳修斯·佩尔纳特的生活——一个住在布拉格犹太区、记不起自己过去的宝石雕刻匠。一个陌生人拿来一本书请他修补，转眼就不见了；邻居们说，魔像又出现了。他周围是旧货商瓦塞特鲁姆、恨透了此人的大学生哈罗塞克、档案员希勒尔和他的女儿米丽娅姆；后来佩尔纳特因一桩命案被投进监狱，出来时发现犹太区正在被拆除。",
      ["the Prague ghetto"], ["布拉格犹太区"], W + "The_Golem_(Meyrink_novel)"),
    S("cz-utz-s1", "cz-utz", "cz-stary-zidovsky-hrbitov", "Throughout", "全书",
      "Kaspar Utz, of minor nobility, has kept his thousand and more pieces of Meissen through the German occupation and the Communist state by never leaving them; each year he travels to Vichy thinking he will defect, and each year he comes back to his shelves. The narrator meets him in Prague in 1967. When Utz dies in 1974 the collection, promised to the state museum, is nowhere to be found.",
      "卡斯帕·乌兹出身小贵族，他靠着寸步不离，把一千多件迈森瓷器保过了德国占领和共产党国家；每年他去一趟维希，心想这回就不回来了，可每年又回到自己的架子前。叙述者 1967 年在布拉格认识了他。1974 年乌兹去世，那批已经许给国家博物馆的藏品却不知去向。",
      ["Meissen"], ["迈森瓷器"], W + "Utz_(novel)"),
    S("cz-smich-s1", "cz-kniha-smichu", "cz-staromestske-namesti", "Part 1, 'Lost Letters'", "第一部“失落的信”",
      "It was snowing, Kundera writes, and Gottwald was bareheaded, so Clementis took off his own fur hat and set it on the leader's head. Four years later Clementis was hanged and the propaganda section removed him from every photograph; where he stood there is only the palace wall. From this the book goes to Mirek, who in 1971 wants to get back his old love letters, and to the struggle of memory against forgetting.",
      "昆德拉写道，当时下着雪，哥特瓦尔德光着头，克莱门蒂斯就摘下自己的皮帽戴在领袖头上。四年后克莱门蒂斯被绞死，宣传部门把他从所有照片上抹去；他站过的地方只剩下宫殿的墙。书由此写到米雷克——1971 年他想要回自己当年的情书——也写到记忆同遗忘的斗争。",
      ["the palace wall"], ["宫殿的墙"], W + "The_Book_of_Laughter_and_Forgetting"),
    S("cz-lehkost-s1", "cz-nesnesitelna-lehkost", "cz-petrin", "Part 4, 'Soul and Body'", "第四部“灵与肉”",
      "Tomáš, a surgeon and a womaniser, and Tereza, the waitress who arrived from a provincial town with a heavy suitcase, live through the Soviet invasion of 1968; they emigrate to Zurich, she goes back, he follows, and he ends as a window-cleaner. In one chapter, a dream, Tomáš tells her to go up Petřín, where a man with a rifle is helping people to die among the trees; at the last moment she says that it was not her own choice.",
      "外科医生托马斯风流成性，特蕾莎是从外省小城提着沉重箱子来的女招待；两人经历了 1968 年苏军入侵，一度移居苏黎世，她先回来，他也跟着回来，最后当了擦窗工。有一章写的是一场梦：托马斯叫她上佩特任山去；树林间有个带枪的人在帮人去死，她在最后一刻说，这不是她自己的选择。",
      ["Petřín"], ["佩特任山"], W + "The_Unbearable_Lightness_of_Being"),
    S("cz-zert-s1", "cz-zert", "cz-ostrava", "Part 3, 'Ludvík'", "第三部“路德维克”",
      "To tease a solemn girl, the student Ludvík sends her a postcard mocking optimism and cheering Trotsky. His friends vote to expel him. In the barracks at Ostrava, among the men with black insignia, he meets Lucie, a quiet girl who brings him flowers through the wire, and loses her through his own impatience.",
      "大学生路德维克为了逗一个一本正经的姑娘，给她寄了一张嘲笑乐观主义、为托洛茨基叫好的明信片。朋友们举手表决把他开除了。在奥斯特拉瓦的营房里，在那些佩黑色领章的人中间，他认识了露茜——一个隔着铁丝网给他送花的安静姑娘；因为自己的急躁，他失去了她。",
      ["Ostrava"], ["奥斯特拉瓦"], W + "The_Joke_(novel)"),
    S("cz-zert-s2", "cz-zert", "cz-vlcnov", "Part 7", "第七部",
      "Fifteen years later Ludvík comes home to take his revenge by seducing the wife of the man who had him expelled, and finds that the joke is again on him. His old friend Jaroslav, who has given his life to folk music, believes that his own son is the veiled king riding through the town; at the end the two men play together in a garden restaurant, and Jaroslav collapses.",
      "十五年后，路德维克回到家乡，想靠勾引当年开除他的那个人的妻子来报复，结果发现这个玩笑又开到了自己头上。老朋友雅罗斯拉夫把一生都献给了民间音乐，他以为骑马穿过小城的那位蒙面“国王”是自己的儿子；结尾，两人在一家露天餐馆里一起演奏，雅罗斯拉夫倒了下去。",
      ["the veiled king"], ["蒙面“国王”"], W + "The_Joke_(novel)"),
    S("cz-slavnost-s1", "cz-zahradni-slavnost", "cz-na-zabradli", "Throughout", "全剧",
      "Hugo Pludek's parents send him to a garden party of the Liquidation Office to meet an influential man. Hugo listens to the officials, learns to speak in their phrases, and talks his way upward until he is made head of the new Central Commission for Inauguration and Liquidation. When he comes home his parents do not know him, and neither does he.",
      "胡戈·普鲁戴克的父母打发他去参加清理局的游园会，好结识一位有势力的人物。胡戈听官员们说话，学会了用他们的套话，一路说着往上爬，直到当上新成立的“开幕与清理中央委员会”的头头。等他回到家，父母已经认不出他，他自己也认不出自己了。",
      ["a garden party"], ["游园会"], W + "The_Garden_Party_(play)"),
    S("cz-samota-s1", "cz-prilis-hlucna-samota", "cz-spalena", "Throughout", "全书",
      "For thirty-five years Haňťa has worked in wastepaper, and he tells it as a love story. He rescues books from the press, carries them home until his bed is roofed with two tons of them, and builds each bale around an open volume of Kant or Lao-tzu. Then he sees the new giant press at Bubny, worked by young people in gloves drinking milk, and understands that his time is over.",
      "汉嘉在废纸堆里干了三十五年，他把这讲成一个爱情故事。他从打包机里抢救书籍，一本本背回家，直到床顶上压着两吨书；他打的每一个纸包，中间都裹着一本翻开的康德或老子。后来他看到布勃内那台新的巨型打包机，操作它的是戴着手套、喝着牛奶的年轻人，他明白自己的时代结束了。",
      ["thirty-five years"], ["三十五年"], W + "Too_Loud_a_Solitude"),
    S("cz-kral-s1", "cz-obsluhoval", "cz-hotel-pariz", "Chapter 3", "第三章",
      "Jan Dítě starts as a busboy selling frankfurters at a station, wanting only to be a millionaire and to be taken for the equal of tall men. At the Hotel Paříž he learns his trade and serves the Emperor of Ethiopia at a state banquet, for which he gets a medal. He marries Lise, a German, grows rich on stamps taken from deported Jews, builds his own hotel, loses it after 1948, and ends mending a road in the mountains with a few animals for company.",
      "扬·迪特最初是在火车站卖熏肠的小伙计，一心只想当百万富翁，让高个子们把他平等看待。在巴黎饭店他学成了手艺，在一次国宴上侍候了埃塞俄比亚皇帝，得了一枚勋章。他娶了德国姑娘丽莎，靠从被遣送的犹太人那里弄来的邮票发了财，盖起自己的饭店，1948 年以后又失去了它，最后在山里修路，只有几只动物做伴。",
      ["the Hotel Paříž"], ["巴黎饭店"], W + "I_Served_the_King_of_England"),
    S("cz-vlaky-s1", "cz-ostre-sledovane-vlaky", "cz-kostomlaty", "Throughout", "全书",
      "Miloš comes from a family of men who did no work: a great-grandfather pensioned at eighteen, a grandfather who tried to hypnotise the German tanks into turning back. He has cut his wrists after failing with the conductress Máša. On the night the 'closely watched' ammunition train passes, a woman of the resistance cures him, and he drops the bomb from the signal gantry onto the train and is shot by a German soldier whom he shoots in turn.",
      "米洛什出身于一个男人们都不干活的家庭：曾祖父十八岁就领退休金，祖父想用催眠术让德国坦克掉头。他同女列车员玛莎没能成事，割了腕。在那列“严密监视的”军火列车经过的夜里，一位抵抗组织的女人治好了他的心病；他从信号架上把炸弹扔到列车上，同时与一个德国兵互相射中。",
      ["ammunition train"], ["军火列车"], "https://cs.wikipedia.org/wiki/Ost%C5%99e_sledovan%C3%A9_vlaky_(novela)"),
    S("cz-postriziny-s1", "cz-postriziny", "cz-nymburk", "Throughout", "全书",
      "Maryška eats and drinks with a butcher's appetite, rides her bicycle through the town with her hair flying, and climbs the brewery chimney with Uncle Pepin to look at the world. Francin, her careful husband, looks on in alarm. At the end, since everything is being shortened, the working day and the table legs and the dog's tail, she has her hair cut off too.",
      "玛丽什卡吃喝起来有屠夫一样的胃口，骑着自行车穿过小城，头发在风里飞扬，还同贝宾大伯一起爬上啤酒厂的烟囱看世界。她那位谨小慎微的丈夫弗朗茨在一旁提心吊胆。到最后，既然什么都在缩短——工作日，桌子腿，狗尾巴——她也把自己的头发剪掉了。",
      ["the brewery chimney"], ["啤酒厂的烟囱"], W + "Cutting_It_Short"),
    S("cz-hhhh-s1", "cz-hhhh", "cz-cyril-metodej", "Part 2", "第二部",
      "Binet follows Heydrich from his childhood to the Wannsee conference and the Castle of Prague, and Gabčík and Kubiš from their training in Britain to the bend in the road at Libeň where the Sten gun jams and the grenade is thrown. He keeps stopping to say what he does not know and will not make up. The last pages are the seven men in the church, three in the gallery and four in the flooded crypt, holding off the SS for hours.",
      "比内跟着海德里希，从童年写到万湖会议和布拉格城堡；也跟着加布奇克和库比什，从在英国受训写到利本区那个拐弯处——司登冲锋枪卡了壳，手榴弹扔了出去。他不时停下来，说明哪些是他不知道、也不愿编造的。最后几页写的是教堂里的七个人——三个在楼座上，四个在灌了水的地下墓室里——同党卫军对峙了好几个小时。",
      ["crypt"], ["地下墓室"], W + "HHhH"),
    S("cz-mendelssohn-s1", "cz-mendelssohn", "cz-rudolfinum", "Opening", "开头",
      "The official Schlesinger, who gave the order, is terrified when he finds his men with a rope round Wagner's neck. From the roof the novel moves down into occupied Prague: Dr Rabinovich, the scholar made to run a Jewish museum for the Germans, two little girls hidden with one family after another, and Heydrich's death and what was done in revenge.",
      "下命令的官员施莱辛格发现手下人把绳子套在了瓦格纳的脖子上，吓得魂飞魄散。小说从屋顶往下，写进被占领的布拉格：被迫替德国人主持犹太博物馆的学者拉比诺维奇博士，在一户又一户人家之间辗转躲藏的两个小女孩，还有海德里希之死和随后的报复。",
      ["the roof"], ["屋顶"], W + "Mendelssohn_Is_on_the_Roof"),
    S("cz-mozart-s1", "cz-mozart-prag", "cz-stavovske", "Throughout", "全篇",
      "In the autumn of 1787 Mozart and Constanze stop at a village inn on the road to Prague. Walking in a count's park, he absent-mindedly picks an orange from a tree kept for the betrothal of the count's niece, is caught, and is invited to the feast. He plays them the unfinished Don Giovanni, the churchyard scene last, and the bride, Eugenie, feels that a man who burns so fast cannot live long.",
      "1787 年秋天，莫扎特和康斯坦策在去布拉格的路上，在一家乡村客栈歇脚。他在一位伯爵的花园里散步，心不在焉地从一棵橘树上摘下一个橘子——那棵树是为伯爵的侄女订婚准备的——被人当场抓住，反倒被请去赴宴。他给大家弹了还没写完的《唐璜》，最后弹的是墓地那一场；新娘欧根妮觉得，一个燃烧得这样快的人活不长。",
      ["the road to Prague"], ["去布拉格的路上"], "https://de.wikipedia.org/wiki/Mozart_auf_der_Reise_nach_Prag"),
    S("cz-foglar-s1", "cz-zahada-hlavolamu", "cz-stinadla", "Throughout", "全书",
      "Mirek Dušín, Jarka Metelka, Jindra Hojer, Červenáček and Rychlonožka hear of a locksmith's apprentice, Jan Tleskač, who fell from a church bell-tower years ago, and of the puzzle he carried, a small metal hedgehog that only he could free from its cage. The trail leads into the Stínadla, where the boys of the quarter, the Vonts, wear yellow pins and are about to elect their Great Vont.",
      "米雷克·杜欣、亚尔卡·梅特尔卡、因德拉·霍耶尔、“小红帽”和“飞毛腿”听说多年前有个锁匠学徒扬·特莱斯卡奇从教堂钟楼上摔了下来，还听说他随身带着一件机关玩具：一只小金属刺猬，只有他能把它从笼子里取出来。线索通向斯蒂纳德拉——那里的男孩们自称“冯特”，别着黄色别针，正要选出他们的“大冯特”。",
      ["the Stínadla"], ["斯蒂纳德拉"], W + "Rychl%C3%A9_%C5%A1%C3%ADpy"),
    S("cz-pavel-s1", "cz-smrt-krasnych-srncu", "cz-berounka", "'The Death of the Beautiful Roebucks'", "《美丽牡鹿之死》",
      "Before the war Leo Popper is the best vacuum-cleaner salesman in the country and buys a pond that turns out to hold one carp. Under the occupation, wearing the star and forbidden to travel, he cycles out to the Berounka, borrows the ferryman's wolfhound Holan, who can pull down a deer, and brings the meat back to Buštěhrad past the patrols, because his two elder sons are to leave for the camp in the morning.",
      "战前，莱奥·波佩尔是全国最出色的吸尘器推销员，还买下过一口后来发现只有一条鲤鱼的池塘。占领时期，他戴着黄星、被禁止出行，却骑车赶到贝龙卡河边，借来摆渡人那条能扑倒鹿的狼狗霍兰，躲过巡逻队把鹿肉带回布什捷赫拉德——因为第二天早上，两个大儿子就要动身去集中营。",
      ["the Berounka"], ["贝龙卡河"], W + "Ota_Pavel"),
    S("cz-sramek-s1", "cz-stribrny-vitr", "cz-pisek", "Throughout", "全书",
      "Jan Ratkin goes through the classes of a small-town grammar school at the end of the century: the catechist who hounds him, his cold father, the uncle who alone understands him and who shoots himself, the young teacher Ramler, the girl Anička who only plays with him. Each disappointment costs him something, and each spring the silver wind comes again from far away.",
      "世纪末，扬·拉特金在一座小城的文科中学一级级地读上去：处处同他作对的教义课教师，冷漠的父亲，唯一懂他、后来开枪自杀的叔叔，年轻的教师拉姆勒，只是同他逢场作戏的姑娘安妮奇卡。每一次失望都让他失去一点什么，而每到春天，银色的风又从远方吹来。",
      ["the silver wind"], ["银色的风"], W + "Fr%C3%A1%C5%88a_%C5%A0r%C3%A1mek"),
    S("cz-hochwald-s1", "cz-hochwald", "cz-vitkuv-kamen", "Throughout", "全篇",
      "The old huntsman Gregor takes Clarissa and Johanna through the trackless forest to the lake under the Plöckenstein cliff. One day a hunter appears on the shore: Ronald, a Swedish king's natural son, whom Clarissa has loved since childhood. He rides to the castle to speak for peace and is killed, unrecognised, by her father; the Swedes burn the castle, and the sisters live out their lives unmarried in the ruin.",
      "老猎人格雷戈尔带着克拉丽莎和约翰娜穿过没有路的森林，来到普勒肯施泰因峭壁下的湖边。有一天，湖岸上出现了一个猎手：罗纳德，一位瑞典国王的私生子，克拉丽莎从小就爱着他。他骑马到城堡去劝和，没被认出来，死在她父亲手下；瑞典人烧了城堡，姐妹俩终身未嫁，在废墟里度过了余生。",
      ["the lake under the Plöckenstein cliff"], ["普勒肯施泰因峭壁下的湖"], W + "Adalbert_Stifter"),
    S("cz-goethe-s1", "cz-marienbad-elegie", "cz-marianske-lazne", "Throughout", "全诗",
      "Twenty-three stanzas begun in the coach on 5 September 1823 and finished by the time he reached Weimar a week later: the gate of paradise shut behind him, her last kiss, her image more present than the mountains passing the window. The poem ends without consolation: the gods who once favoured him have tested him and now destroy him. Goethe showed it only to his closest friends.",
      "二十三节诗，1823 年 9 月 5 日在马车里动笔，一周后回到魏玛时已经写完：天堂的门在他身后关上，她最后的一吻，她的形象比窗外掠过的群山更加真切。诗没有以安慰收尾：曾经眷顾他的众神考验了他，如今要毁掉他。歌德只把它拿给最亲近的朋友看。",
      ["the coach"], ["马车"], W + "Marienbad_Elegy"),
    S("cz-austerlitz-s1", "cz-austerlitz", "cz-terezin", "The Prague and Terezín pages", "布拉格与泰雷津部分",
      "Brought up as Dafydd Elias by a Welsh preacher, Austerlitz learns his real name at school and for decades avoids knowing more. Then a radio programme overheard in a London bookshop, two women recalling their Kindertransport, sends him to Prague, where his old nursemaid Věra still lives in the same flat and tells him of his mother Agáta, an actress and singer, deported to Terezín. At Terezín he stares into the window of a junk shop; later he searches a Nazi propaganda film of the ghetto, slowed down, for her face.",
      "奥斯特利茨被一位威尔士牧师当作“戴维德·伊莱亚斯”养大，上中学时才知道自己的真名，此后几十年都回避去了解更多。后来他在伦敦一家书店里偶然听到广播，两个女人在回忆当年的儿童专列，这才动身去布拉格：当年的保姆维拉还住在原来的房子里，给他讲他的母亲阿加塔——一位演员兼歌唱家，被遣送到泰雷津。在泰雷津，他久久盯着一家旧货店的橱窗；后来他把一部纳粹拍的隔都宣传片放慢了速度，在里面寻找她的脸。",
      ["Terezín"], ["泰雷津"], W + "Austerlitz_(novel)"),
    S("cz-austerlitz-s2", "cz-austerlitz", "cz-marianske-lazne", "The Marienbad pages", "玛丽恩巴德部分",
      "Věra remembers a happy stay at Marienbad in the summer of 1938, the last holiday of the family. Austerlitz had been there again in 1972 with Marie de Verneuil, not knowing he had ever seen it before, and had been seized among the half-ruined spa buildings by a blind fear that made him push away the one person who loved him.",
      "维拉记得 1938 年夏天在玛丽恩巴德度过的那段愉快日子，那是一家人最后一次度假。1972 年，奥斯特利茨曾同玛丽·德·韦纳伊再到那里，却不知道自己从前来过；在半已破败的温泉建筑之间，一阵说不出缘由的恐惧攫住了他，使他推开了唯一爱他的人。",
      ["Marienbad"], ["玛丽恩巴德"], W + "Austerlitz_(novel)"),
    S("cz-zbabelci-s1", "cz-zbabelci", "cz-nachod", "Throughout", "全书",
      "From Friday 4 May to Friday 11 May 1945. The town's worthies form a local army whose main purpose is to keep order until someone else arrives; Danny and the band are given armbands and no guns. The SS pass through, the Red Army arrives, prisoners straggle home from the camps, and Danny, who with his friend Přema knocks out a German tank with a hidden machine gun, thinks mostly of Irena, who loves someone else.",
      "从 1945 年 5 月 4 日星期五到 5 月 11 日星期五。城里的头面人物组织了一支地方武装，主要任务是在别人到来之前维持秩序；丹尼和乐队的伙伴们只领到袖章，没领到枪。党卫军路过，红军开到，从集中营出来的囚徒三三两两往家走；丹尼同朋友普谢马用一挺藏了多年的机枪打掉了一辆德国坦克，心里想的却多半是爱着别人的伊蕾娜。",
      ["May 1945"], ["1945 年 5 月"], W + "The_Cowards"),
    S("cz-polacek-s1", "cz-bylo-nas-pet", "cz-rychnov", "Throughout", "全书",
      "Petr Bajza, the grocer's son, tells it all in the solemn language of a schoolboy trying to write properly: the war with the boys of the next street, the circus that comes to town, the maid Kristýna who laughs at everything. In a fever he dreams that he rides to India on an elephant with his friends Čeněk Jirsák, Antonín Bejval, Éda Kemlink and Pepek Zilvar from the poorhouse.",
      "杂货店老板的儿子彼得·巴伊扎用一个努力想写得规规矩矩的小学生那种一本正经的口气，把什么都讲了出来：同隔壁街男孩们的战争，来到城里的马戏团，见什么都笑的女佣克里斯蒂娜。发高烧时，他梦见自己同伙伴们——切涅克·伊尔萨克、安东宁·贝瓦尔、埃达·凯姆林克，还有贫民院的佩佩克·齐尔瓦尔——骑着大象去了印度。",
      ["on an elephant"], ["骑着大象"], W + "Karel_Pol%C3%A1%C4%8Dek"),
    S("cz-liska-s1", "cz-liska-bystrouska", "cz-bilovice", "Throughout", "全书",
      "The forester Bartoš, sleeping off his drink in the woods, catches a fox cub and takes her home for his children. Tied up in the yard, she kills the hens and escapes, drives a badger from his sett, marries the fox Zlatohřbítek and raises a litter. The men of the village, the schoolmaster and the priest, grow old over their cards at the inn; she is always a step ahead of them.",
      "林务官巴尔托什在林子里醉后酣睡，逮到一只小狐狸，带回家给孩子们玩。她被拴在院子里，咬死了母鸡逃走，把一只獾赶出洞穴，嫁给了公狐“金背”，生下一窝小狐狸。村里的男人们——教师和神父——在客栈的牌桌上慢慢老去；而她总是比他们快一步。",
      ["a fox cub"], ["小狐狸"], W + "The_Cunning_Little_Vixen"),
    S("cz-glass-s1", "cz-glass-room", "cz-tugendhat", "Throughout", "全书",
      "On their honeymoon in Venice in 1929 Viktor Landauer, a Jewish car manufacturer, and his wife Liesel meet the architect Rainer von Abt, who promises them not a house but a space. In the Glass Room Liesel's friend Hana tells her secrets, Viktor's mistress Kata arrives as a refugee, and when the Germans come the family flees. German scientists then measure skulls in the room, and Hana becomes the lover of one of them.",
      "1929 年在威尼斯度蜜月时，犹太裔汽车制造商维克托·兰道尔和妻子莉泽尔遇见建筑师赖纳·冯·阿布特，他许诺给他们的不是一座房子，而是一个空间。在“玻璃屋”里，莉泽尔的朋友哈娜吐露自己的秘密，维克托的情人卡塔以难民的身份到来；德国人来了，一家人逃走了。此后德国科学家在这间屋子里测量头骨，哈娜成了其中一人的情人。",
      ["the Glass Room"], ["“玻璃屋”"], W + "The_Glass_Room"),
    S("cz-toerless-s1", "cz-toerless", "cz-hranice", "Throughout", "全书",
      "Reiting and Beineberg find that their classmate Basini has stolen money, and instead of reporting him they make him their creature: one to study power, the other to try out his Indian philosophy of the soul. Törless, drawn in, is troubled less by the cruelty than by the fact that such things can be done by ordinary daylight people, the same puzzle that imaginary numbers set him in mathematics.",
      "赖廷和拜内贝格发现同学巴西尼偷了钱，他们不去告发，而是把他变成任自己摆布的人：一个为了研究权力，另一个为了试验自己那套关于灵魂的印度哲学。托乐思被卷了进去，让他不安的与其说是残忍，不如说是这种事竟然能由白天里再普通不过的人做出来——就像数学课上的虚数给他出的那个难题一样。",
      ["Basini"], ["巴西尼"], W + "The_Confusions_of_Young_T%C3%B6rless"),
    S("cz-bezruc-s1", "cz-slezske-pisne", "cz-stare-hamry", "'Maryčka Magdónova'", "《玛丽奇卡·马格多诺娃》",
      "The poems speak in the voice of a miner-bard of a small Silesian people ground between German mine-owners and Polish priests. Maryčka's mother has been crushed by a coal cart; five orphans are cold. She gathers a bundle of wood on the mountain that belongs to the Marquis Gero, the mayor Hochfelder sees her, and the ballad asks at each stanza what she will say.",
      "这些诗用一位矿工歌者的口吻说话，他属于西里西亚一个人数不多的族群，被德国矿主和波兰神父夹在中间碾磨。玛丽奇卡的母亲被运煤车轧死了；五个孤儿挨着冻。她在属于赫罗侯爵的山上拾了一捆柴，被村长霍赫费尔德看见；叙事诗在每一节都问：她会说些什么。",
      ["Marquis Gero"], ["赫罗侯爵"], W + "Petr_Bezru%C4%8D"),
    S("cz-gory-s1", "cz-poema-gory", "cz-petrin", "Throughout", "全诗",
      "Written in January 1924, as her love affair with Konstantin Rodzevich was ending. The hill where they met is made into a mountain as great as their love, one that mourns their parting; she curses the shopkeepers who will build their summer houses on it and live there in peace. Its companion, the Poem of the End, walks through the last evening across the city's bridges.",
      "写于 1924 年 1 月，那时她同康斯坦丁·罗泽维奇的恋情正走向结束。两人相会的小山被写成一座同他们的爱情一样巨大的山，一座为他们的离别哀悼的山；她诅咒那些将来要在山上盖避暑屋、在那里安稳度日的小店主。姊妹篇《终结之诗》写的则是最后一个傍晚，走过这座城市的一座座桥。",
      ["The hill where they met"], ["两人相会的小山"], W + "Marina_Tsvetaeva"),
]

# ============================== write ==============================
used = {p for l in lines for p in l["place_ids"]}
for p in places:
    assert p["id"] in used or p.get("book_ids"), ("place without a line or a book", p["id"])
assert {p["id"] for p in places} == set(CO), set(CO) ^ {p["id"] for p in places}
EXIST = {ALCOOLS, "at-hungerkuenstler", "at-bergkristall", "at-nachsommer"}
bids = {x["id"] for x in books} | EXIST
for l in lines:
    assert l["book_id"] in bids, l["id"]
lined = {l["book_id"] for l in lines}
pilgrim = {i for p in places for i in p.get("book_ids", [])}
assert pilgrim <= bids, pilgrim - bids
assert not ({x["id"] for x in books} - lined - pilgrim), {x["id"] for x in books} - lined - pilgrim
assert len({x["id"] for x in places}) == len(places) and len({x["id"] for x in lines}) == len(lines) and len({x["id"] for x in books}) == len(books)

HEAD = "// Czechia, hand-written content (tools/content/batches/add_cz1.py, 2026-11-22).\n"
def write(name, key, entries, extra=""):
    os.makedirs(os.path.dirname(b.data(name)), exist_ok=True)
    with open(b.data(name), "w", encoding="utf-8") as fh:
        fh.write(HEAD + extra + "window.RA_DATA = window.RA_DATA || {};\nwindow.RA_DATA." + key + " = [\n"
                 + ",\n".join("  " + b.obj(e) for e in entries) + "\n];\n")
if __name__ == "__main__":
    write("books.js", "books", books)
    write("places.js", "places", places, "// Each place's admin-1 region is worked out from its coordinates by app.js.\n")
    write("lines.js", "lines", lines)
    print(len(books), "books,", len(places), "places,", len(lines), "lines (", sum(1 for l in lines if l.get("kind") != "scene"), "quotations )")
