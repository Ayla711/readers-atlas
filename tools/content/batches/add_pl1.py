"""11-22: Poland, first pack: 60 new books (and Effi Briest and The Good Soldier Švejk, already on the shared list),
70 places. Polish literature from Kochanowski and Mickiewicz to Miłosz, Szymborska's generation and Tokarczuk; the
German writers of Silesia, Pomerania and the Baltic coast (Eichendorff, Hauptmann, Fontane, Grass, Christa Wolf); the
Yiddish Poland of Isaac Bashevis Singer; and well-known foreign books set here. Fictional settings hang on the real
place the book is modelled on, or on the writer's own place, and the note says which.

Quotations (20 books, 26 lines) are cut from Wikisource pages (tools/content/wikisource.py): Polish, German, English
and Czech Wikisource; English and Chinese translations are our own drafts (translation: "own"). Every other book has a
scene note or hangs on a writer's place.
What a cut changes, named again in that line's `checked`: a no-break space is written as a space; the thin space that
indents a paragraph is dropped; in one line a double space is written as one; the English text of Conrad's essay is
re-flowed (line breaks and double spaces written as single spaces).

Coordinates are those of the place's Polish (twice English) Wikipedia article (cache/pl/coords.json).

Usage: python3 -I add_pl1.py <app_dir> <coords.json> <wikisource_dir>"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b
import wikisource as ws

APP, CO, WS = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8")), sys.argv[3]
DATE = "2026-11-22"
b.init(APP, "", "pl", DATE)
W = b.W
PLW = "https://pl.wikipedia.org/wiki/"

def BK(id, title, title_zh, author, author_zh, year, pd=True, **kw):
    d = dict(id=id, title=title, title_zh=title_zh, author=author, author_zh=author_zh, year=year,
             orig_lang=kw.pop("lang", "pl"), public_domain=pd, source_url=kw.pop("src", None))
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

def Q(id, book, place, loc, loc_zh, site, title, orig, hl_orig, en, hl_en, zh, hl_zh, note=""):
    if "\xa0" in orig:
        orig = orig.replace("\xa0", " ")
        note += " (a no-break space written as a space)"
    if " " in orig:
        orig = orig.replace(" ", "")
        note += " (paragraph indent dropped)"
    if "  " in orig:
        orig = orig.replace("  ", " ")
        note += " (a double space written as one)"
    for text, hls in ((orig, hl_orig), (en, hl_en), (zh, hl_zh)):
        for h in hls:
            assert h in text, (id, h)
    assert "  " not in orig and "[" not in orig, (id, "spacing or page mark")
    return dict(id=id, book_id=book, place_ids=[place], location=loc, location_zh=loc_zh,
                text_orig=orig, highlight_orig=hl_orig, text_en=en, highlight_en=hl_en, text_zh=zh, highlight_zh=hl_zh, translation="own",
                status="draft", checked=f"{site} Wikisource, {title}{note}, {DATE}")

PL = lambda t: ws.url("pl", t)
MICK = ("Adam Mickiewicz", "密茨凯维奇")
SLOW = ("Juliusz Słowacki", "斯沃瓦茨基")
PRUS = ("Bolesław Prus", "普鲁斯")
SIEN = ("Henryk Sienkiewicz", "显克维奇")
REYM = ("Władysław Reymont", "莱蒙特")
ZER = ("Stefan Żeromski", "热罗姆斯基")
WYSP = ("Stanisław Wyspiański", "维斯皮扬斯基")
TOK = ("Olga Tokarczuk", "托卡尔丘克")
SING = ("Isaac Bashevis Singer", "艾萨克·巴什维斯·辛格")
PT1 = "Pan Tadeusz (wyd. 1921)/Księga pierwsza: Gospodarstwo"
PT4 = "Pan Tadeusz (wyd. 1921)/Księga czwarta: Dyplomatyka i łowy"
KRZ = "Krzyżacy (Sienkiewicz, 1900)/"
ZO1 = "Ziemia Obiecana (Reymont, 1899)/Tom pierwszy/Rozdział I"
EFFI, SVEJK = "effi-briest", "cz-svejk"

# ============================== books ==============================
books = [
    BK("pl-de-revolutionibus", "On the Revolutions of the Heavenly Spheres", "天体运行论", "Nicolaus Copernicus", "哥白尼", "1543", lang="la",
       title_orig="De revolutionibus orbium coelestium", aliases=["De revolutionibus", "Kopernik", "Copernicus", "O obrotach sfer niebieskich"]),
    BK("pl-fraszki", "Epigrams", "戏谑短诗集", "Jan Kochanowski", "科哈诺夫斯基", "1584", title_orig="Fraszki", src=PL("Ziemia polska w pieśni/Na lipę"),
       aliases=["Fraszki", "Na lipę", "Kochanowski", "Czarnolas", "Treny"]),
    BK("pl-monachomachia", "Monachomachia, or the War of the Monks", "修士之战", "Ignacy Krasicki", "克拉西茨基", "1778", title_orig="Monachomachia, czyli Wojna mnichów",
       aliases=["Monachomachia", "Krasicki", "Bajki i przypowieści", "Satyry"]),
    BK("pl-pan-tadeusz", "Pan Tadeusz", "塔杜施先生", *MICK, "1834", title_orig="Pan Tadeusz, czyli ostatni zajazd na Litwie", src=PL("Pan Tadeusz (wyd. 1921)"),
       aliases=["Pan Tadeusz", "Mickiewicz", "Soplicowo", "Litwo! Ojczyzno moja", "Master Thaddeus"]),
    BK("pl-kordian", "Kordian", "科尔迪安", *SLOW, "1834", title_orig="Kordian", src=PL("Kordian"), aliases=["Kordian", "Słowacki", "Slowacki", "Spisek koronacyjny"]),
    BK("pl-zemsta", "Revenge", "复仇", "Aleksander Fredro", "弗雷德罗", "1834", title_orig="Zemsta", aliases=["Zemsta", "Fredro", "Cześnik", "Rejent", "Papkin"]),
    BK("pl-nie-boska", "The Un-Divine Comedy", "非神曲", "Zygmunt Krasiński", "克拉辛斯基", "1835", title_orig="Nie-Boska komedia", aliases=["Nie-Boska komedia", "Krasiński", "Krasinski", "Undivine Comedy"]),
    BK("pl-eichendorff-gedichte", "Poems", "诗集", "Joseph von Eichendorff", "艾兴多夫", "1837", lang="de", title_orig="Gedichte", src=ws.url("de", "Abschied (Eichendorff)"),
       aliases=["Abschied", "O Täler weit, o Höhen", "Eichendorff", "Lubowitz"]),
    BK("pl-balladyna", "Balladyna", "巴拉迪娜", *SLOW, "1839", title_orig="Balladyna", src=PL("Balladyna"), aliases=["Balladyna", "Goplana", "Kirkor", "Słowacki"]),
    BK("pl-stara-basn", "An Ancient Tale", "古老的传说", "Józef Ignacy Kraszewski", "克拉舍夫斯基", "1876", title_orig="Stara baśń", src=PL("Stara baśń"),
       aliases=["Stara baśń", "Stara basn", "Kraszewski", "Popiel", "Piast"]),
    BK("pl-w-tatrach", "In the Tatras", "在塔特拉山中", "Adam Asnyk", "阿斯尼克", "1880", title_orig="W Tatrach", src=PL("Morskie Oko (Asnyk, wyd. 1898)"),
       aliases=["W Tatrach", "Asnyk", "Morskie Oko"]),
    BK("pl-potop", "The Deluge", "洪流", *SIEN, "1886", title_orig="Potop", src=PL("Potop (Sienkiewicz)"), aliases=["Potop", "Sienkiewicz", "Kmicic", "Jasna Góra", "Trylogia"]),
    BK("pl-lalka", "The Doll", "玩偶", *PRUS, "1890", title_orig="Lalka", src=PL("Lalka (Prus)"), aliases=["Lalka", "Prus", "Wokulski", "Rzecki", "Izabela Łęcka"]),
    BK("pl-weber", "The Weavers", "织工", "Gerhart Hauptmann", "豪普特曼", "1892", lang="de", title_orig="Die Weber", aliases=["Die Weber", "De Waber", "Hauptmann", "Peterswaldau"]),
    BK("pl-tetmajer-poezje", "Poems, Second Series", "诗集（第二辑）", "Kazimierz Przerwa-Tetmajer", "泰特马耶尔", "1894", title_orig="Poezje. Seria druga",
       src=PL("Melodya mgieł nocnych (Tetmajer, wyd. 1901)"), aliases=["Melodia mgieł nocnych", "Tetmajer", "Poezje"]),
    BK("pl-syzyfowe-prace", "The Labours of Sisyphus", "西西弗斯的劳役", *ZER, "1897", title_orig="Syzyfowe prace", src=PL("Syzyfowe prace"),
       aliases=["Syzyfowe prace", "Żeromski", "Zeromski", "Marcin Borowicz", "Kleryków"]),
    BK("pl-ziemia-obiecana", "The Promised Land", "福地", *REYM, "1899", title_orig="Ziemia obiecana", src=PL("Ziemia Obiecana (Reymont, 1899)"),
       aliases=["Ziemia obiecana", "Reymont", "Borowiecki", "Łódź", "Lodz"]),
    BK("pl-krzyzacy", "The Knights of the Cross", "十字军骑士", *SIEN, "1900", title_orig="Krzyżacy", src=PL("Krzyżacy (Sienkiewicz, 1900)"),
       aliases=["Krzyżacy", "Krzyzacy", "The Teutonic Knights", "Zbyszko", "Danusia", "Grunwald"]),
    BK("pl-ludzie-bezdomni", "Homeless People", "无家可归的人们", *ZER, "1900", title_orig="Ludzie bezdomni", aliases=["Ludzie bezdomni", "Judym", "Cisy", "Żeromski"]),
    BK("pl-wesele", "The Wedding", "婚礼", *WYSP, "1901", title_orig="Wesele", src=PL("Wesele (Wyspiański)"), aliases=["Wesele", "Wyspiański", "Wyspianski", "Chochoł", "Bronowice"]),
    BK("pl-akropolis", "Akropolis", "卫城", *WYSP, "1904", title_orig="Akropolis", src=PL("Akropolis"), aliases=["Akropolis", "Acropolis", "Wyspiański", "Wawel"]),
    BK("pl-chlopi", "The Peasants", "农民", *REYM, "1904–1909", title_orig="Chłopi", src=PL("Chłopi (Reymont)"), aliases=["Chłopi", "Chlopi", "Reymont", "Boryna", "Jagna", "Lipce"]),
    BK("pl-pan-balcer", "Mr Balcer in Brazil", "巴尔采尔先生在巴西", "Maria Konopnicka", "科诺普尼茨卡", "1910", title_orig="Pan Balcer w Brazylii", aliases=["Pan Balcer w Brazylii", "Konopnicka", "Rota"]),
    BK("pl-notes-life-letters", "Notes on Life and Letters", "生活与文学札记", "Joseph Conrad", "康拉德", "1921", lang="en", src=ws.url("en", "Notes on Life and Letters"),
       aliases=["Poland Revisited", "Conrad", "Korzeniowski"]),
    BK("pl-krol-macius", "King Matt the First", "麦提国王一世", "Janusz Korczak", "科扎克", "1923", title_orig="Król Maciuś Pierwszy", aliases=["Król Maciuś Pierwszy", "Korczak", "King Matt"]),
    BK("pl-przedwiosnie", "The Spring to Come", "早春", *ZER, "1924", title_orig="Przedwiośnie", src=PL("Przedwiośnie (Żeromski)"),
       aliases=["Przedwiośnie", "Przedwiosnie", "The Coming Spring", "Cezary Baryka", "szklane domy"]),
    BK("pl-puszcza-jodlowa", "The Fir Forest", "冷杉林", *ZER, "1925", title_orig="Puszcza jodłowa", src=PL("Puszcza jodłowa"), aliases=["Puszcza jodłowa", "Puszcza jodlowa", "Żeromski", "Łysica"]),
    BK("pl-pozegnanie-jesieni", "Farewell to Autumn", "告别秋天", "Stanisław Ignacy Witkiewicz (Witkacy)", "维特凯维奇（维特卡西）", "1927", title_orig="Pożegnanie jesieni",
       aliases=["Pożegnanie jesieni", "Witkacy", "Witkiewicz", "Atanazy Bazakbal"]),
    BK("pl-noce-i-dnie", "Nights and Days", "黑夜与白昼", "Maria Dąbrowska", "东布罗夫斯卡", "1931–1934", pd=False, title_orig="Noce i dnie",
       aliases=["Noce i dnie", "Dąbrowska", "Dabrowska", "Barbara Niechcic", "Bogumił", "Kaliniec"]),
    BK("pl-dwa-ksiezyce", "Two Moons", "两个月亮", "Maria Kuncewiczowa", "孔采维奇娃", "1933", pd=False, title_orig="Dwa księżyce", aliases=["Dwa księżyce", "Kuncewiczowa", "Kazimierz Dolny"]),
    BK("pl-panny-z-wilka", "The Maids of Wilko", "维尔科的姑娘们", "Jarosław Iwaszkiewicz", "伊瓦什凯维奇", "1933", pd=False, title_orig="Panny z Wilka",
       aliases=["Panny z Wilka", "Iwaszkiewicz", "The Wilko Girls", "Stawisko"]),
    BK("pl-poemat-lublin", "A Poem about the City of Lublin", "卢布林城之诗", "Józef Czechowicz", "切霍维奇", "1934", title_orig="Poemat o mieście Lublinie",
       aliases=["Poemat o mieście Lublinie", "Czechowicz"]),
    BK("pl-satan-goray", "Satan in Goray", "撒旦在戈雷", *SING, "1935", pd=False, lang="yi", title_orig="Der sotn in Goray", aliases=["Der sotn in Goray", "Satan in Goray", "Singer", "Sabbatai Zevi"]),
    BK("pl-ferdydurke", "Ferdydurke", "费尔迪杜凯", "Witold Gombrowicz", "贡布罗维奇", "1937", pd=False, title_orig="Ferdydurke", aliases=["Ferdydurke", "Gombrowicz", "Józio", "Pimko"]),
    BK("pl-westerplatte-piesn", "Song of the Soldiers of Westerplatte", "韦斯特普拉特士兵之歌", "Konstanty Ildefons Gałczyński", "加乌琴斯基", "1939", pd=False,
       title_orig="Pieśń o żołnierzach z Westerplatte", aliases=["Pieśń o żołnierzach z Westerplatte", "Gałczyński", "Galczynski", "Westerplatte"]),
    BK("pl-treblinka-hell", "The Hell of Treblinka", "特雷布林卡地狱", "Vasily Grossman", "格罗斯曼", "1944", pd=False, lang="ru", title_orig="Треблинский ад",
       aliases=["Треблинский ад", "Grossman", "Treblinka"]),
    BK("pl-ocalenie", "Rescue", "拯救", "Czesław Miłosz", "米沃什", "1945", pd=False, title_orig="Ocalenie", aliases=["Ocalenie", "Campo dei Fiori", "Miłosz", "Milosz"]),
    BK("pl-pianista", "The Pianist", "钢琴家", "Władysław Szpilman", "什皮尔曼", "1946", pd=False, title_orig="Śmierć miasta", aliases=["Pianista", "Śmierć miasta", "Szpilman", "The Pianist"]),
    BK("pl-pozegnanie-z-maria", "This Way for the Gas, Ladies and Gentlemen", "女士们先生们，请进毒气室", "Tadeusz Borowski", "博罗夫斯基", "1948", pd=False,
       title_orig="Pożegnanie z Marią", aliases=["Pożegnanie z Marią", "Proszę państwa do gazu", "Borowski", "Farewell to Maria"]),
    BK("pl-kronika-olsztynska", "Olsztyn Chronicle", "奥尔什丁纪事", "Konstanty Ildefons Gałczyński", "加乌琴斯基", "1952", pd=False, title_orig="Kronika olsztyńska",
       aliases=["Kronika olsztyńska", "Gałczyński", "Pranie"]),
    BK("pl-family-moskat", "The Family Moskat", "莫斯卡特一家", *SING, "1950", pd=False, lang="yi", title_orig="Di familye Mushkat", aliases=["Di familye Mushkat", "The Family Moskat", "Singer", "Krochmalna"]),
    BK("pl-blechtrommel", "The Tin Drum", "铁皮鼓", "Günter Grass", "君特·格拉斯", "1959", pd=False, lang="de", title_orig="Die Blechtrommel",
       aliases=["Die Blechtrommel", "Grass", "Oskar Matzerath", "Danzig", "Blaszany bębenek"]),
    BK("pl-magician-lublin", "The Magician of Lublin", "卢布林的魔术师", *SING, "1960", pd=False, lang="yi", title_orig="Der kuntsnmakher fun Lublin",
       aliases=["Der kuntsnmakher fun Lublin", "The Magician of Lublin", "Yasha Mazur", "Singer"]),
    BK("pl-jakob", "Jacob the Liar", "说谎者雅各布", "Jurek Becker", "尤雷克·贝克尔", "1969", pd=False, lang="de", title_orig="Jakob der Lügner", aliases=["Jakob der Lügner", "Jurek Becker", "Jakob Heym"]),
    BK("pl-pamietnik-powstania", "A Memoir of the Warsaw Uprising", "华沙起义回忆录", "Miron Białoszewski", "比亚沃舍夫斯基", "1970", pd=False, title_orig="Pamiętnik z powstania warszawskiego",
       aliases=["Pamiętnik z powstania warszawskiego", "Białoszewski", "Bialoszewski"]),
    BK("pl-erste-polka", "The First Polka", "第一支波尔卡", "Horst Bienek", "比内克", "1975", pd=False, lang="de", title_orig="Die erste Polka", aliases=["Die erste Polka", "Bienek", "Gleiwitz", "Gliwice"]),
    BK("pl-kindheitsmuster", "Patterns of Childhood", "童年典范", "Christa Wolf", "克里斯塔·沃尔夫", "1976", pd=False, lang="de", title_orig="Kindheitsmuster",
       aliases=["Kindheitsmuster", "A Model Childhood", "Christa Wolf", "Nelly Jordan", "Landsberg"]),
    BK("pl-zdazyc", "Shielding the Flame", "赶在上帝之前", "Hanna Krall", "汉娜·克拉尔", "1977", pd=False, title_orig="Zdążyć przed Panem Bogiem",
       aliases=["Zdążyć przed Panem Bogiem", "Krall", "Marek Edelman", "To Outwit God"]),
    BK("pl-szosta-klepka", "The Sixth Stave", "第六块桶板", "Małgorzata Musierowicz", "穆谢罗维奇", "1977", pd=False, title_orig="Szósta klepka",
       aliases=["Szósta klepka", "Jeżycjada", "Jezycjada", "Musierowicz", "Borejko", "Kwiat kalafiora"]),
    BK("pl-mala-apokalipsa", "A Minor Apocalypse", "小小的启示录", "Tadeusz Konwicki", "康维茨基", "1979", pd=False, title_orig="Mała apokalipsa", aliases=["Mała apokalipsa", "Konwicki"]),
    BK("pl-schindler", "Schindler's Ark", "辛德勒的名单", "Thomas Keneally", "托马斯·基尼利", "1982", pd=False, lang="en", aliases=["Schindler's List", "Schindler's Ark", "Keneally", "Oskar Schindler"]),
    BK("pl-weiser", "Who Was David Weiser?", "魏泽尔·达维德克", "Paweł Huelle", "帕维乌·许勒", "1987", pd=False, title_orig="Weiser Dawidek", aliases=["Weiser Dawidek", "Huelle"]),
    BK("pl-hanemann", "Hanemann", "哈内曼", "Stefan Chwin", "斯特凡·赫文", "1995", pd=False, title_orig="Hanemann", aliases=["Hanemann", "Chwin", "Death in Danzig"]),
    BK("pl-widnokrag", "Horizon", "地平线", "Wiesław Myśliwski", "梅希里夫斯基", "1996", pd=False, title_orig="Widnokrąg", aliases=["Widnokrąg", "Widnokrag", "Myśliwski", "Mysliwski"]),
    BK("pl-dukla", "Dukla", "杜克拉", "Andrzej Stasiuk", "斯塔休克", "1997", pd=False, title_orig="Dukla", aliases=["Dukla", "Stasiuk"]),
    BK("pl-dom-dzienny", "House of Day, House of Night", "白天的房子，夜晚的房子", *TOK, "1998", pd=False, title_orig="Dom dzienny, dom nocny",
       aliases=["Dom dzienny, dom nocny", "Tokarczuk", "Nowa Ruda", "Marta"]),
    BK("pl-smierc-w-breslau", "Death in Breslau", "布雷斯劳之死", "Marek Krajewski", "马雷克·克拉耶夫斯基", "1999", pd=False, title_orig="Śmierć w Breslau",
       aliases=["Śmierć w Breslau", "Krajewski", "Eberhard Mock"]),
    BK("pl-czarny-ogrod", "The Black Garden", "黑色花园", "Małgorzata Szejnert", "谢伊内特", "2007", pd=False, title_orig="Czarny ogród", aliases=["Czarny ogród", "Szejnert", "Giszowiec", "Nikiszowiec"]),
    BK("pl-plug", "Drive Your Plow Over the Bones of the Dead", "糜骨之壤", *TOK, "2009", pd=False, title_orig="Prowadź swój pług przez kości umarłych",
       aliases=["Prowadź swój pług przez kości umarłych", "Tokarczuk", "Janina Duszejko", "Drive Your Plough"]),
    BK("pl-empuzjon", "The Empusium", "恩普西翁", *TOK, "2022", pd=False, title_orig="Empuzjon", aliases=["Empuzjon", "Empusium", "Tokarczuk", "Görbersdorf", "Wojnicz"]),
]

# ============================== places ==============================
places = [
    # ---- Masovia: Warsaw ----
    ORIG("pl-krakowskie-przedmiescie", "Krakowskie Przedmieście, Warsaw", "华沙克拉科夫郊区街",
         "The first stretch of Warsaw's Royal Route, running south from the Castle Square past the university. Prus put the fancy-goods shop of J. Mincel and S. Wokulski here, and plaques on two houses of the street mark where, by readers' reckoning, Wokulski and the old clerk Rzecki 'lived'",
         "华沙“王家大道”的第一段，从城堡广场向南，经过大学。普鲁斯把“J. 明采尔与 S. 沃库尔斯基”杂货店安在这条街上；街上有两幢房子挂着纪念牌，标出读者们推算出来的沃库尔斯基和老店员热茨基的“住处”"),
    ORIG("pl-powisle", "Powiśle, Warsaw", "华沙滨河区",
         "The low district along the Vistula, below the escarpment on which the university stands. In The Doll Wokulski walks down Karowa Street to the river and sees the hovels of the poor and the rubbish heaps beside the city's water supply",
         "维斯瓦河边的低地街区，就在大学所在的陡坡之下。《玩偶》里，沃库尔斯基沿卡罗瓦街走下河边，看见穷人的窝棚，以及紧挨着城市水源的垃圾堆"),
    ORIG("pl-lazienki", "Łazienki Park, Warsaw", "华沙瓦津基公园",
         "The park of the Palace on the Isle, the summer residence of Stanisław August, the last king of Poland. In The Doll Izabela Łęcka walks here with her aunt, and Wokulski waits by the pond in the hope of a greeting",
         "水上宫殿所在的园林，波兰末代国王斯坦尼斯瓦夫·奥古斯特的夏宫。《玩偶》里，伊扎贝拉·文茨卡陪姑母在这里散步，沃库尔斯基守在池塘边，盼着她打个招呼"),
    ORIG("pl-zamek-krolewski", "Royal Castle, Warsaw", "华沙王宫城堡",
         "Act III of Kordian opens on the square before the castle on the day in 1829 when Tsar Nicholas I is crowned King of Poland; that night Kordian goes through the castle rooms to kill him and faints at the bedroom door. The castle was blown up by the Germans in 1944 and rebuilt in 1971–84",
         "《科尔迪安》第三幕在城堡前的广场上开场：1829 年沙皇尼古拉一世加冕为波兰国王的那一天；当夜科尔迪安穿过城堡里的一间间屋子去刺杀他，却昏倒在卧室门口。城堡 1944 年被德军炸毁，1971–1984 年重建"),
    ORIG("pl-belweder", "Belweder Palace, Warsaw", "华沙贝尔维德宫",
         "The classical palace at the southern end of Ujazdów Avenue, rebuilt around 1820 for the tsar's brother, Grand Duke Constantine, and after 1918 the residence of Józef Piłsudski as head of state. The Spring to Come ends with Cezary Baryka walking at the head of a workers' march towards it",
         "乌亚兹多夫大道南端的古典式宫殿，1820 年前后为沙皇的弟弟康斯坦丁大公改建，1918 年以后是国家元首毕苏斯基的官邸。《早春》的结尾，采扎雷·巴雷卡走在一支工人游行队伍的最前面，向它走去"),
    ORIG("pl-plac-krasinskich", "Krasiński Square, Warsaw", "华沙克拉辛斯基广场",
         "The square lay just outside the wall of the Warsaw ghetto. At Easter 1943, while the ghetto uprising was being put down on the other side, a carousel was turning here; Miłosz's poem 'Campo dei Fiori', written in Warsaw that spring, sets it beside the burning of Giordano Bruno in Rome",
         "这座广场紧挨着华沙犹太隔离区的围墙。1943 年复活节，墙那边的隔离区起义正遭到镇压，这里的旋转木马却照常转着；米沃什那年春天在华沙写下《鲜花广场》，把它同罗马烧死布鲁诺的场面并排放在一起"),
    ORIG("pl-stare-miasto", "Old Town Market Square, Warsaw", "华沙老城集市广场",
         "The Old Town was held by the insurgents through August 1944 and bombed and shelled into rubble; what stands now was rebuilt after the war. Białoszewski, who was twenty-two, lived through those weeks in its cellars, and they are at the heart of his Memoir",
         "1944 年 8 月，起义者守了老城一个月，老城被炸成了瓦砾；现在看到的是战后重建的。比亚沃舍夫斯基当时二十二岁，在老城的地下室里熬过了这几个星期，这也是他那本《回忆录》的核心部分"),
    ORIG("pl-umschlagplatz", "Umschlagplatz, Warsaw", "华沙转运广场",
         "The loading yard beside the railway siding on Stawki Street from which, in the summer of 1942, the Jews of the Warsaw ghetto were sent to Treblinka. A monument of white and black stone, unveiled in 1988, stands on the spot",
         "斯塔夫基街铁路岔道旁的装运场；1942 年夏天，华沙隔离区的犹太人就是从这里被送往特雷布林卡的。原址上立着一座 1988 年落成的黑白石纪念碑"),
    ORIG("pl-pkin", "Palace of Culture and Science, Warsaw", "华沙文化科学宫",
         "The Soviet-built tower, finished in 1955 as Stalin's 'gift' to Warsaw. The narrator of A Minor Apocalypse, a tired writer, is asked by fellow dissidents to set fire to himself in front of it that evening, and spends the day walking the city",
         "苏联人建造的高楼，1955 年完工，是斯大林送给华沙的“礼物”。《小小的启示录》的叙述者是个疲惫的作家，持不同政见的朋友们请他当天晚上在楼前自焚，于是他在城里走了一整天"),
    PIL("pl-krochmalna", "Korczak's Orphanage, Krochmalna Street, Warsaw", "华沙克罗赫马尔纳街科扎克孤儿院",
        "Janusz Korczak ran the Jewish orphanage Dom Sierot in this building from 1912; its address was then 92 Krochmalna Street. In 1940 the home was moved into the ghetto, and in August 1942 Korczak went with his children to Treblinka. Krochmalna was also the street of Isaac Bashevis Singer's childhood, and much of his fiction comes back to it",
        "从 1912 年起，雅努什·科扎克在这幢楼里主持犹太孤儿院“孤儿之家”，当时的门牌是克罗赫马尔纳街 92 号。1940 年孤儿院被迁入隔离区，1942 年 8 月科扎克同他的孩子们一起去了特雷布林卡。克罗赫马尔纳街也是艾萨克·巴什维斯·辛格童年住的街，他的许多小说都回到这条街上", ["pl-krol-macius"]),
    PIL("pl-powazki", "Powązki Cemetery, Warsaw", "华沙波瓦兹基公墓",
        "Warsaw's old cemetery, opened in 1790. Bolesław Prus, Władysław Reymont and Maria Dąbrowska are among the writers buried here",
        "华沙的老公墓，1790 年启用。葬在这里的作家有普鲁斯、莱蒙特和东布罗夫斯卡等", ["pl-lalka", "pl-chlopi", "pl-noce-i-dnie"]),
    # ---- Masovia outside Warsaw ----
    ORIG("pl-czarnolas", "Czarnolas", "黑森林村（查尔诺拉斯）",
         "Jan Kochanowski's estate, where he settled in the 1570s and wrote the Laments and many of his songs and epigrams. Neither his house nor the linden he wrote under survives; a nineteenth-century manor in the park holds his museum",
         "扬·科哈诺夫斯基的庄园。他 16 世纪 70 年代在这里定居，写下《哀歌》和许多歌与短诗。他的房子和他常在树下写作的那棵椴树都已不存；园中一座 19 世纪的庄园宅邸是他的纪念馆"),
    PIL("pl-wsola", "Gombrowicz Museum, Wsola", "弗索拉贡布罗维奇博物馆",
        "The manor that belonged to Witold Gombrowicz's brother Jerzy, where the writer was a frequent guest between the wars; the idea of Ferdydurke is said to have come to him here. It is now the Witold Gombrowicz Museum",
        "这座庄园宅邸原属维托尔德·贡布罗维奇的哥哥耶日，两次大战之间作家常来这里做客，据说《费尔迪杜凯》的构思就产生在这里。现在是维托尔德·贡布罗维奇博物馆", ["pl-ferdydurke"]),
    PIL("pl-stawisko", "Stawisko, Podkowa Leśna", "斯塔维斯科",
        "The house in the woods at Podkowa Leśna built in 1928 for Jarosław Iwaszkiewicz and his wife Anna. He lived here until his death in 1980, and most of his work was written here. It is kept as a museum",
        "波德科瓦莱希纳林中的宅子，1928 年为雅罗斯瓦夫·伊瓦什凯维奇和妻子安娜而建。他在这里一直住到 1980 年去世，大部分作品都写于此。现为纪念馆", ["pl-panny-z-wilka"]),
    PIL("pl-opinogora", "Museum of Romanticism, Opinogóra", "奥皮诺古拉浪漫主义博物馆",
        "The small neo-Gothic castle on the Krasiński family estate, the home of Zygmunt Krasiński, author of The Un-Divine Comedy; he is buried in the family crypt of the parish church here. The castle has been a Museum of Romanticism since 1961",
        "克拉辛斯基家族庄园里的新哥特式小城堡，《非神曲》作者齐格蒙特·克拉辛斯基的家；他葬在本地堂区教堂的家族墓室里。城堡自 1961 年起是浪漫主义博物馆", ["pl-nie-boska"]),
    ORIG("pl-treblinka", "Treblinka", "特雷布林卡",
         "The extermination camp where, from July 1942 to the autumn of 1943, some 800,000 Jews were murdered, most of the Warsaw ghetto among them. Vasily Grossman reached the site with the Red Army in 1944 and wrote 'The Hell of Treblinka' from what survivors and local people told him. A field of thousands of stones now marks it",
         "这座灭绝营从 1942 年 7 月到 1943 年秋天杀害了约八十万犹太人，华沙隔离区的大部分居民都在其中。1944 年格罗斯曼随红军到达这里，根据幸存者和当地人的讲述写下《特雷布林卡地狱》。如今遗址上是一片由数千块石头组成的纪念场"),
    # ---- Lesser Poland ----
    ORIG("pl-wawel", "Wawel Cathedral, Kraków", "克拉科夫瓦维尔主教座堂",
         "The coronation church and burial place of the Polish kings; Mickiewicz and Słowacki lie in its Crypt of the Bards. Wyspiański's Akropolis takes place in the cathedral on Easter night, when the figures on the tombs and in the tapestries come to life",
         "波兰历代国王加冕和安葬的教堂；密茨凯维奇和斯沃瓦茨基葬在这里的“诗圣墓室”。维斯皮扬斯基的《卫城》写的是复活节之夜的这座教堂：陵墓上和挂毯里的人物都活了过来"),
    ORIG("pl-mariacki", "St Mary's Basilica, Kraków", "克拉科夫圣母圣殿",
         "The brick church with two unequal towers on the Main Market Square; a bugle call is played from the taller one every hour. Conrad, who had lived in Kraków as a schoolboy, came back in the summer of 1914 and described a midnight walk across the square in 'Poland Revisited'",
         "中央集市广场上的砖砌教堂，两座塔楼一高一矮；高塔上每个整点吹响号角。康拉德少年时在克拉科夫上过学，1914 年夏天重回这里，在《重访波兰》里写了午夜穿过广场的那次散步"),
    ORIG("pl-bronowice", "Rydlówka, Bronowice", "布罗诺维采的雷德尔之家",
         "The manor-cottage where, in November 1900, the wedding party of the poet Lucjan Rydel and the peasant girl Jadwiga Mikołajczykówna was held. Wyspiański was among the guests, and The Wedding was on stage in Kraków the following March. The house is now a museum",
         "1900 年 11 月，诗人卢茨扬·雷德尔同农家姑娘雅德维加·米科瓦伊契克的婚宴就在这座乡间宅子里举行。维斯皮扬斯基是宾客之一，第二年 3 月《婚礼》就在克拉科夫上演了。宅子现在是博物馆"),
    ORIG("pl-tyniec", "Tyniec Abbey", "蒂涅茨修道院",
         "The Benedictine abbey on a limestone cliff above the Vistula, a few miles upstream from Kraków, founded in the eleventh century. The Knights of the Cross opens in an inn that belongs to it",
         "本笃会修道院，坐落在维斯瓦河边的石灰岩峭壁上，在克拉科夫上游几英里处，创建于 11 世纪。《十字军骑士》就从修道院名下的一家客店写起"),
    PIL("pl-skalka", "Skałka, Kraków", "克拉科夫岩上教堂",
        "The Pauline church 'on the Rock'. Its Crypt of Merit holds the graves of Stanisław Wyspiański, Adam Asnyk, Józef Ignacy Kraszewski and, since 2004, Czesław Miłosz",
        "保禄隐修会的“岩上”教堂。教堂的“功臣墓室”里安葬着维斯皮扬斯基、阿斯尼克、克拉舍夫斯基，2004 年起还有米沃什", ["pl-wesele", "pl-w-tatrach", "pl-stara-basn", "pl-ocalenie"]),
    ORIG("pl-fabryka-schindlera", "Schindler's Factory, Kraków", "克拉科夫辛德勒工厂",
         "The enamelware works at 4 Lipowa Street that Oskar Schindler took over in 1939. By employing Jews from the Kraków ghetto and the Płaszów camp, and by moving his workers to Brünnlitz in the Sudetenland in 1944, he kept more than a thousand people alive. The office building is now a museum of Kraków under the occupation",
         "利波瓦街 4 号的搪瓷厂，1939 年由奥斯卡·辛德勒接手。他雇用克拉科夫隔离区和普瓦舒夫集中营的犹太人，1944 年又把工人迁往苏台德地区的布吕恩利茨，使一千多人活了下来。办公楼现在是展示占领时期克拉科夫的博物馆"),
    PIL("pl-peksowy-brzyzek", "Pęksowy Brzyzek Cemetery, Zakopane", "扎科帕内佩克索维公墓",
        "The old cemetery of Zakopane beside its wooden church, where the people who made the mountain town a capital of the arts are buried, among them Tytus Chałubiński, Stanisław Witkiewicz and Kornel Makuszyński. Witkiewicz's son Witkacy, the author of Farewell to Autumn, who also lived in Zakopane, killed himself in September 1939 in what is now Ukraine; the remains brought here in 1988 turned out not to be his, so his grave is a symbolic one",
        "扎科帕内木教堂旁的老公墓，葬着把这座山城变成艺术之都的人们，其中有哈乌宾斯基、斯坦尼斯瓦夫·维特凯维奇和马库申斯基。维特凯维奇的儿子、《告别秋天》的作者维特卡西也住在扎科帕内；1939 年 9 月他在今天的乌克兰境内自杀，1988 年迁回这里的遗骨后来证实并不是他的，所以他在这里的墓只是一座象征性的墓", ["pl-pozegnanie-jesieni"]),
    ORIG("pl-morskie-oko", "Morskie Oko", "海眼湖",
         "The largest lake of the Tatras, lying at about 1,395 m under the walls of Mięguszowieckie Szczyty and Rysy. Asnyk, a keen walker in the Tatras, wrote a sonnet sequence about it",
         "塔特拉山最大的湖，海拔约 1395 米，卧在门古绍维茨峰群和雷塞峰的峭壁之下。阿斯尼克热爱在塔特拉山中徒步，为它写了一组十四行诗"),
    ORIG("pl-czarny-staw", "Czarny Staw Gąsienicowy", "加雄尼措瓦黑湖",
         "A tarn at about 1,620 m at the head of the Gąsienicowa Valley, above Zakopane. Tetmajer's 'Melody of the Night Mists', which every Polish schoolchild meets, carries its name in the subtitle",
         "加雄尼措瓦山谷尽头的冰斗湖，海拔约 1620 米，在扎科帕内上方。泰特马耶尔的《夜雾的旋律》是波兰学生人人读过的诗，副标题里写着这座湖的名字"),
    ORIG("pl-auschwitz", "Auschwitz-Birkenau", "奥斯威辛-比克瑙",
         "The largest of the German camps, where more than a million people, most of them Jews, were murdered between 1940 and 1945. Tadeusz Borowski was a prisoner here from 1943; the stories he wrote soon after the war are told by a prisoner who survives by working at the unloading ramp of Birkenau",
         "德国集中营中最大的一座，1940 至 1945 年间有一百多万人在这里被杀害，其中大多数是犹太人。塔德乌什·博罗夫斯基从 1943 年起被关在这里；他战后不久写的那些小说，叙述者是一个靠在比克瑙卸车站台上干活而活下来的囚犯"),
    # ---- Silesia ----
    ORIG("pl-jasna-gora", "Jasna Góra, Częstochowa", "琴斯托霍瓦光明山修道院",
         "The Pauline monastery that keeps the icon of the Black Madonna, the chief shrine of Poland. At the end of 1655 it held out against a Swedish siege, which is the turning point of The Deluge; Pan Tadeusz opens with an invocation to its Virgin",
         "保禄隐修会的修道院，供奉着“黑圣母”圣像，是波兰最重要的朝圣地。1655 年底它顶住了瑞典军队的围攻，这是《洪流》的转折点；《塔杜施先生》开篇就向这里的圣母祈祷"),
    ORIG("pl-lubowice", "Łubowice (Lubowitz)", "武博维采（卢博维茨）",
         "Joseph von Eichendorff was born in the manor here above the Oder in 1788 and grew up in its park and woods, which return in his poems all his life. The house was wrecked in 1945; only ruined walls are left",
         "1788 年，约瑟夫·冯·艾兴多夫出生在奥得河上方这里的庄园里，在庄园的花园和树林中长大；这些树林一辈子都回到他的诗里。宅子毁于 1945 年，如今只剩残墙"),
    ORIG("pl-nikiszowiec", "Nikiszowiec, Katowice", "卡托维兹尼基绍维茨",
         "A miners' estate of red-brick blocks with inner courtyards, built from 1908 for the workers of the Giesche mine. The Black Garden tells a century of Nikiszowiec and its neighbour Giszowiec through the families who lived there",
         "红砖楼房围着内院的矿工住宅区，1908 年起为吉舍矿的工人兴建。《黑色花园》通过住在那里的一个个家庭，讲述尼基绍维茨和邻近的吉绍维茨一百年的历史"),
    ORIG("pl-radiostacja", "Gliwice Radio Tower", "格利维采广播电台",
         "The wooden transmitter mast of the Gleiwitz radio station, 111 m high. On the evening of 31 August 1939 SS men staged a 'Polish attack' on the station as a pretext for the invasion of Poland. Bienek's The First Polka takes place in Gleiwitz on that day",
         "格莱维茨广播电台的木结构发射塔，高 111 米。1939 年 8 月 31 日晚，党卫军在这里导演了一场“波兰人袭击”，作为入侵波兰的借口。比内克的《第一支波尔卡》写的就是那一天的格莱维茨"),
    # ---- Opole ----
    PIL("pl-nysa", "Eichendorff's grave, Nysa", "尼萨的艾兴多夫墓",
        "Eichendorff spent his last years with his daughter's family in Neisse and died there on 26 November 1857. He lies beside his wife in the Jerusalem Cemetery",
        "艾兴多夫晚年住在尼萨（奈塞）女儿家，1857 年 11 月 26 日在那里去世。他同妻子并排葬在耶路撒冷公墓", ["pl-eichendorff-gedichte"]),
    # ---- Lower Silesia ----
    PIL("pl-muzeum-pana-tadeusza", "Pan Tadeusz Museum, Wrocław", "弗罗茨瓦夫《塔杜施先生》博物馆",
        "The manuscript of Pan Tadeusz has belonged since 1999 to the Ossolineum, the library that moved from Lwów to Wrocław after 1945. Since 2016 it has been shown in this museum in a house on the Market Square",
        "《塔杜施先生》的手稿 1999 年起归奥索林斯基图书馆所有，这家图书馆 1945 年以后从利沃夫迁到弗罗茨瓦夫。2016 年起，手稿在集市广场一幢房子里的这家博物馆展出", ["pl-pan-tadeusz"]),
    ORIG("pl-wroclaw-glowny", "Wrocław Main Station", "弗罗茨瓦夫中央火车站",
         "Breslau's turreted main station, opened in 1857. Death in Breslau begins in 1933 with the bodies of a baron's daughter and her maid found in a railway carriage, and Criminal Counsellor Eberhard Mock takes the case",
         "布雷斯劳带塔楼的中央车站，1857 年启用。《布雷斯劳之死》开头是 1933 年：一节火车车厢里发现了一位男爵的女儿和她女仆的尸体，刑事参事埃伯哈德·莫克接手此案"),
    PIL("pl-jagniatkow", "Hauptmann House, Jagniątków", "亚格尼翁特库夫豪普特曼故居",
        "Haus Wiesenstein, the villa Gerhart Hauptmann had built in 1900–01 at Agnetendorf in the Karkonosze, his home for the rest of his life. He died here in June 1946. It is now a museum",
        "“草地石之家”，豪普特曼 1900–1901 年在克尔科诺谢山的阿格内滕多夫建造的别墅，此后一直是他的家。1946 年 6 月他在这里去世。现为博物馆", ["pl-weber"]),
    ORIG("pl-pieszyce", "Pieszyce (Peterswaldau)", "皮耶希采（彼得斯瓦尔道）",
         "The weaving village under the Owl Mountains where the rising of the Silesian weavers began on 4 June 1844 with an attack on the house of the manufacturers Zwanziger; next day it spread to Bielawa (Langenbielau), where soldiers fired on the crowd. Hauptmann's The Weavers follows those days, with Zwanziger renamed Dreissiger",
         "猫头鹰山下的织工村。1844 年 6 月 4 日，西里西亚织工起义从袭击厂主茨万齐格的宅子开始；第二天蔓延到别拉瓦（朗根比劳），军队向人群开了枪。豪普特曼的《织工》写的就是这几天，茨万齐格在剧中改名德赖西格"),
    ORIG("pl-sokolowsko", "Sokołowsko (Görbersdorf)", "索科沃夫斯科（格贝尔斯多夫）",
         "A village in a wooded valley of the Stone Mountains where Hermann Brehmer opened, in the 1850s, the first sanatorium to treat tuberculosis with mountain air; Davos followed its example. The Empusium is set here in the autumn of 1913",
         "石山一条林木山谷里的村庄。19 世纪 50 年代，赫尔曼·布雷默在这里开办了第一家用高山空气治疗肺结核的疗养院，达沃斯是后来学它的。《恩普西翁》的故事发生在 1913 年秋天的这里"),
    ORIG("pl-nowa-ruda", "Nowa Ruda", "新鲁达",
         "A former coal-mining town in the Kłodzko land, close to the Czech border. Tokarczuk has had a house in the nearby hamlet of Krajanów since the 1990s; House of Day, House of Night is made of the stories of the town and its valley, and Drive Your Plow is set on a plateau in the same borderland",
         "克沃兹科地区的旧煤矿小城，离捷克边境很近。托卡尔丘克 20 世纪 90 年代起在附近的小村克拉亚努夫有一处房子；《白天的房子，夜晚的房子》由这座小城和山谷里的故事织成，《糜骨之壤》则发生在同一片边境地带的一处高地上"),
    # ---- Lubusz ----
    ORIG("pl-gorzow", "Gorzów Wielkopolski (Landsberg an der Warthe)", "大波兰地区戈茹夫（瓦尔塔河畔兰茨贝格）",
         "Christa Wolf was born here in 1929 and fled west with her family in January 1945. Patterns of Childhood is built around a short visit she made to the town in the summer of 1971",
         "克里斯塔·沃尔夫 1929 年生在这里，1945 年 1 月随家人向西逃难。《童年典范》围绕她 1971 年夏天回到这座城市的一次短暂访问展开"),
    # ---- West Pomerania ----
    PROTO("pl-swinoujscie", "Świnoujście (Swinemünde)", "希维诺乌伊希切（斯维内明德）",
          "Kessin, the small Baltic port where Effi Briest is taken as a bride. Fontane spent five years of his childhood in Swinemünde, where his father kept the pharmacy from 1827, and drew Kessin from his memories of it",
          "凯辛：艾菲·布里斯特婚后被带去的波罗的海小港。冯塔纳童年在斯维内明德住过五年，他父亲 1827 年起在那里开药房；凯辛就是照着他对这座小城的记忆写的"),
    # ---- Pomerania ----
    ORIG("pl-poczta-polska", "Polish Post Office, Gdańsk", "格但斯克波兰邮局",
         "On 1 September 1939 the staff of the Polish post office in the Free City of Danzig defended the building from dawn until evening against German police and SS units; those who surrendered were later shot. 'The Polish Post Office' is one of the central chapters of The Tin Drum. Part of the building is a museum",
         "1939 年 9 月 1 日，但泽自由市波兰邮局的职员在这幢楼里从清晨到傍晚抵抗德国警察和党卫军；投降的人后来被枪决。“波兰邮局”是《铁皮鼓》里最重要的章节之一。楼里有一部分辟为博物馆"),
    ORIG("pl-wrzeszcz", "Wrzeszcz (Langfuhr), Gdańsk", "格但斯克弗热什奇（朗富尔）",
         "The suburb where Günter Grass was born in 1927 and grew up above his parents' grocery in Labesweg, now ul. Lelewela; Oskar Matzerath's childhood is set in the same street. Huelle's Who Was David Weiser? is set in the same district in the summer of 1957",
         "君特·格拉斯 1927 年出生的郊区；他在拉贝斯路（今莱莱韦尔街）父母开的杂货店楼上长大，奥斯卡·马策拉特的童年也被安排在这条街上。许勒的《魏泽尔·达维德克》写的是 1957 年夏天的同一片街区"),
    ORIG("pl-oliwa", "Oliwa, Gdańsk", "格但斯克奥利瓦",
         "The district of the old Cistercian abbey and its cathedral, below wooded moraine hills. Hanemann is set in a villa street here in 1945 and after, as the German owners leave and Polish families from the east move into their houses",
         "古老的西多会修道院及其主教座堂所在的城区，背靠林木覆盖的冰碛丘陵。《哈内曼》写的是 1945 年前后这里的一条别墅街：德国房主离去，从东部来的波兰人家搬进他们的房子"),
    ORIG("pl-westerplatte", "Westerplatte", "韦斯特普拉特",
         "The peninsula at the mouth of Gdańsk harbour where a Polish garrison of about two hundred men held out for seven days after the first shots of the war on 1 September 1939. Gałczyński's poem, written that same month, sends the fallen soldiers marching straight to heaven",
         "格但斯克港口的半岛。1939 年 9 月 1 日战争打响第一枪之后，约两百人的波兰守军在这里坚守了七天。加乌琴斯基当月写下的那首诗，让阵亡的士兵列队径直走进天堂"),
    ORIG("pl-malbork", "Malbork Castle", "马尔堡城堡",
         "The brick fortress on the Nogat, from 1309 the seat of the Grand Masters of the Teutonic Order and one of the largest castles in Europe. In The Knights of the Cross Polish envoys are shown round it so that its strength may frighten them",
         "诺加特河畔的砖砌要塞，1309 年起是条顿骑士团大团长的驻地，也是欧洲最大的城堡之一。《十字军骑士》里，波兰使者被领着参观城堡，为的是用它的威势吓住他们"),
    # ---- Warmia-Masuria ----
    ORIG("pl-grunwald", "Grunwald battlefield", "格伦瓦尔德古战场",
         "On 15 July 1410 the army of Poland and Lithuania under King Władysław Jagiełło defeated the Teutonic Order on these fields; the Grand Master Ulrich von Jungingen was killed. The battle is the last great scene of The Knights of the Cross",
         "1410 年 7 月 15 日，国王瓦迪斯瓦夫·雅盖沃率领的波兰-立陶宛联军在这片原野上击败条顿骑士团，大团长乌尔里希·冯·容金根阵亡。这场战役是《十字军骑士》最后的大场面"),
    PIL("pl-frombork", "Cathedral Hill, Frombork", "弗龙堡主教座堂山",
        "Copernicus was a canon of the Warmia chapter and lived on this hill above the Vistula Lagoon for most of the years from 1510 until his death in 1543; here he made his observations and wrote On the Revolutions. He is buried in the cathedral",
        "哥白尼是瓦尔米亚教士会的教士，从 1510 年到 1543 年去世，大部分时间住在维斯瓦潟湖边的这座山上；他在这里观测天象，写成《天体运行论》。他葬在主教座堂里", ["pl-de-revolutionibus"]),
    PIL("pl-lidzbark", "Bishops' Castle, Lidzbark Warmiński", "利兹巴克瓦尔米亚主教城堡",
        "The Gothic castle of the bishops of Warmia. Ignacy Krasicki lived here as prince-bishop from 1767 to 1795, and here he wrote the Monachomachia, the Fables and the Satires",
        "瓦尔米亚主教的哥特式城堡。伊格纳齐·克拉西茨基 1767 至 1795 年以采邑主教的身份住在这里，《修士之战》《寓言集》和《讽刺诗》都写于此", ["pl-monachomachia"]),
    PIL("pl-pranie", "Pranie Forester's Lodge", "普拉涅护林员小屋",
        "The forester's lodge on Lake Nidzkie in Masuria where Konstanty Ildefons Gałczyński spent the summers of his last years, 1950–53; the Olsztyn Chronicle and other late poems were written here. It is now his museum",
        "马祖里地区尼兹凯湖畔的护林员小屋，加乌琴斯基在生命的最后几年（1950–1953）来这里度夏，《奥尔什丁纪事》等晚期诗作就写于此。现为他的纪念馆", ["pl-kronika-olsztynska"]),
    # ---- Podlaskie ----
    ORIG("pl-bialowieza", "Białowieża Forest", "比亚沃维耶扎原始森林",
         "The best-preserved primeval lowland forest in Europe, on the border with Belarus, and the home of the European bison. Book IV of Pan Tadeusz opens by addressing its trees",
         "欧洲保存最完好的低地原始森林，位于波兰同白俄罗斯的边境上，也是欧洲野牛的家园。《塔杜施先生》第四卷开头就是对这里的树木说话"),
    # ---- Kuyavia-Pomerania ----
    ORIG("pl-goplo", "Mouse Tower, Kruszwica", "克鲁什维察鼠塔",
         "The brick tower on Lake Gopło is what is left of a fourteenth-century castle; legend puts here the wicked prince Popiel, who was eaten by mice. Kraszewski's An Ancient Tale tells the fall of Popiel on this shore, and Słowacki set Balladyna 'near Lake Gopło'",
         "戈普沃湖畔的这座砖塔是一座 14 世纪城堡的遗存；传说恶王波皮耶尔就是在这里被老鼠吃掉的。克拉舍夫斯基的《古老的传说》在这片湖岸上讲了波皮耶尔的覆灭，斯沃瓦茨基也把《巴拉迪娜》安排在“戈普沃湖附近”"),
    PIL("pl-torun-kopernik", "Copernicus House, Toruń", "托伦哥白尼故居",
        "The Gothic merchant's house in the old town held to be the birthplace of Nicolaus Copernicus, born in Toruń on 19 February 1473. It is a museum",
        "老城里的哥特式商人住宅，相传是哥白尼的出生地；他 1473 年 2 月 19 日生于托伦。现为博物馆", ["pl-de-revolutionibus"]),
    # ---- Greater Poland ----
    ORIG("pl-kalisz", "Kalisz", "卡利什",
         "Maria Dąbrowska was born at Russów, a few miles away, in 1889 and went to school in Kalisz. It is the Kaliniec of Nights and Days, and the novel ends in August 1914, when German troops shelled and burned the town",
         "玛丽亚·东布罗夫斯卡 1889 年出生在几英里外的鲁苏夫，在卡利什上过学。这座城就是《黑夜与白昼》里的卡利涅茨；小说结束在 1914 年 8 月，德军炮轰并烧毁了这座城"),
    ORIG("pl-jezyce", "Jeżyce, Poznań", "波兹南耶日采区",
         "A district of turn-of-the-century tenements west of the city centre. Musierowicz's long series of novels about the Borejko family and their neighbours is set at 5 Roosevelt Street and in the streets around, and readers call it the Jeżycjada",
         "市中心以西的街区，满是世纪之交的公寓楼。穆谢罗维奇那套写博雷伊科一家和邻居们的长篇系列小说，就发生在罗斯福街 5 号和周围的街道上，读者管它叫“耶日采记”"),
    PIL("pl-smielow", "Mickiewicz Museum, Śmiełów", "希米耶武夫密茨凯维奇博物馆",
        "The classical country house where Mickiewicz stayed in the late summer of 1831, hoping to cross into the Russian partition and join the November Uprising, which fell before he could. The house and its people are thought to have left their mark on Pan Tadeusz, written in Paris soon after",
        "一座古典式乡间宅邸。1831 年夏末密茨凯维奇住在这里，想越境进入俄占区参加十一月起义，但没等他过去起义就失败了。一般认为，这座宅子和这里的人在他不久后于巴黎写成的《塔杜施先生》里留下了痕迹", ["pl-pan-tadeusz"]),
    # ---- Łódź ----
    ORIG("pl-piotrkowska", "Piotrkowska Street, Łódź", "罗兹彼得科夫斯卡大街",
         "The main street of Łódź, more than four kilometres long, lined with the tenements, banks and palaces of the cotton boom. The Promised Land begins on a wet morning as the factory hands hurry along it to work",
         "罗兹的主街，长四公里多，两旁是棉纺业繁荣年代留下的公寓楼、银行和宫殿。《福地》开头是一个下雨的清晨，工人们沿着这条街匆匆赶去上工"),
    ORIG("pl-palac-poznanskiego", "Poznański Palace, Łódź", "罗兹波兹南斯基宫",
         "The palace of the cotton manufacturer Izrael Poznański, built beside his mill, which is now the Manufaktura complex. Men like him are the models for the factory kings of The Promised Land. The palace houses the Museum of the City of Łódź",
         "棉纺厂主伊兹拉埃尔·波兹南斯基的宫殿，就建在他的工厂旁边；工厂如今改成了“曼努法克图拉”商业文化区。《福地》里那些工厂大王就是照着他这样的人写的。宫殿现为罗兹城市博物馆"),
    ORIG("pl-lipce", "Lipce Reymontowskie", "利普采-莱蒙托夫斯凯",
         "Reymont worked on the Warsaw–Vienna railway near this village around 1890 and gave its name to the Lipce of The Peasants, which follows one village through the four seasons of a year. In 1983 the village added his name to its own",
         "1890 年前后，莱蒙特在这个村子附近的华沙—维也纳铁路上工作，后来把村名给了《农民》里的利普采；小说跟着一个村庄走过一年四季。1983 年，村子在自己的名字后面加上了他的名字"),
    ORIG("pl-radegast", "Radegast Station, Łódź", "罗兹拉德加斯特车站",
         "The loading station of the Łódź ghetto, from which its people were sent to the death camps at Chełmno and Auschwitz in 1942–44. Jurek Becker, born in Łódź, probably in 1937, spent his early childhood in that ghetto; the ghetto of Jacob the Liar has no name, but it is drawn from it",
         "罗兹隔离区的装运车站；1942–1944 年，隔离区的人就是从这里被送往海乌姆诺和奥斯威辛的灭绝营。尤雷克·贝克尔生于罗兹（大概是 1937 年），幼年在这个隔离区度过；《说谎者雅各布》里的隔离区没有名字，却是照着它写的"),
    # ---- Świętokrzyskie ----
    ORIG("pl-kielce", "Żeromski's School, Kielce", "凯尔采热罗姆斯基母校",
         "The former boys' gymnasium of Kielce, where Stefan Żeromski was a pupil from 1874 to 1886. It is the school of Kleryków in The Labours of Sisyphus, where Polish boys are taught in Russian and taught to despise their own language. It is now a museum of the writer's school years",
         "凯尔采旧日的男子中学，热罗姆斯基 1874 至 1886 年在这里读书。它就是《西西弗斯的劳役》里克莱里科夫的那所学校：波兰孩子在这里用俄语上课，还被教着瞧不起自己的语言。现在是作家学生时代纪念馆"),
    ORIG("pl-swiety-krzyz", "Łysa Góra (Święty Krzyż)", "韦萨山（圣十字山）",
         "The second summit of the Świętokrzyskie Mountains, also called Łysiec, with its old Benedictine abbey among fir and beech forest. Żeromski grew up below these hills at Ciekoty; The Fir Forest, one of his last works, is a hymn to them",
         "圣十字山脉的第二高峰，又名韦希耶茨山，山上古老的本笃会修道院隐在冷杉和山毛榉林中。热罗姆斯基在山下的切科蒂村长大；《冷杉林》是他最后的作品之一，是献给这片山林的颂歌"),
    PIL("pl-oblegorek", "Sienkiewicz Manor, Oblęgorek", "奥布文戈雷克显克维奇庄园",
        "The manor bought by public subscription and given to Sienkiewicz in 1900 to mark twenty-five years of his writing life, the year The Knights of the Cross came out as a book. He used it as a summer house until 1914. It has been a museum since 1958",
        "这座庄园由公众募捐买下，1900 年赠给显克维奇，纪念他写作二十五周年；《十字军骑士》的单行本也在这一年出版。到 1914 年为止，他一直把这里当作夏季住所。1958 年起为博物馆", ["pl-krzyzacy", "pl-potop"]),
    ORIG("pl-sandomierz", "Sandomierz", "桑多梅日",
         "The old town on a bluff above the Vistula. Wiesław Myśliwski was born at Dwikozy, just outside it, in 1932 and went to school here; the hill town of Horizon, where the boy and his parents live after the war, is drawn from it",
         "维斯瓦河边高坡上的古城。维斯瓦夫·梅希里夫斯基 1932 年出生在城外的德维科齐，在这里上过学；《地平线》里男孩和父母战后住的那座山城，就是照着它写的"),
    # ---- Lublin ----
    ORIG("pl-lublin", "Old Town, Lublin", "卢布林老城",
         "The walled old town above the former Jewish quarter of Podzamcze. The Magician of Lublin begins here in the last decades of the nineteenth century. Czechowicz, born in Lublin in 1903 and killed in it by a German bomb in September 1939, made his Poem about the City of Lublin a night walk through its streets",
         "有城墙的老城，下方是昔日的犹太区“城堡下”。《卢布林的魔术师》从 19 世纪最后几十年的这里写起。切霍维奇 1903 年生于卢布林，1939 年 9 月在这座城里死于德军的炸弹；他的《卢布林城之诗》是一次穿过城中街巷的夜行"),
    ORIG("pl-kazimierz-dolny", "Kazimierz Dolny", "下卡齐米日",
         "The Renaissance grain-trading town on the Vistula, a painters' colony between the wars. Maria Kuncewiczowa set the linked stories of Two Moons here, and the house she and her husband built in the 1930s is now a museum",
         "维斯瓦河畔的文艺复兴式粮商小城，两次大战之间是画家聚居地。玛丽亚·孔采维奇娃把《两个月亮》里那些互相勾连的短篇安排在这里；她和丈夫 20 世纪 30 年代盖的房子现在是纪念馆"),
    PIL("pl-naleczow", "Żeromski's Cottage, Nałęczów", "纳文丘夫热罗姆斯基小屋",
        "The cottage in the Zakopane style that Żeromski had built in 1905 as a place to write in the spa of Nałęczów, where he had worked as a tutor around 1890 and met his first wife. The spa of Cisy in Homeless People is modelled on Nałęczów. The cottage has been a museum since 1928",
        "热罗姆斯基 1905 年在疗养地纳文丘夫盖的扎科帕内式小屋，用作写作的地方；1890 年前后他在这里当过家庭教师，并结识了第一任妻子。《无家可归的人们》里的疗养地“齐塞”就是以纳文丘夫为原型的。小屋 1928 年起为纪念馆", ["pl-ludzie-bezdomni"]),
    ORIG("pl-goraj", "Goraj", "戈拉伊",
         "A small town in the hills south of Lublin. Singer, who spent part of his youth in nearby Biłgoraj, where his grandfather had been rabbi, set his first novel here in 1665–66, when news of the false messiah Sabbatai Zevi reaches a community that has barely recovered from the Cossack massacres of 1648",
         "卢布林以南丘陵里的小镇。辛格的外祖父曾是附近比乌戈拉伊的拉比，他自己青年时代也在那里住过；他把第一部长篇安排在 1665–1666 年的戈拉伊：假弥赛亚沙巴泰·泽维的消息传到了一个刚从 1648 年哥萨克屠杀中缓过气来的社区"),
    # ---- Subcarpathia ----
    PROTO("pl-odrzykon", "Kamieniec Castle, Odrzykoń", "奥德日孔卡缅涅茨城堡",
          "The castle of Revenge. In the seventeenth century this hilltop castle near Krosno was owned in two halves by quarrelling neighbours; Fredro, whose wife brought half of it as her dowry, found the court records of their dispute over a wall and made the comedy out of them",
          "《复仇》里的城堡。17 世纪时，克罗斯诺附近山顶上的这座城堡分属两家互相争吵的邻居；弗雷德罗的妻子带来的嫁妆里有半座城堡，他从中发现了两家为一堵墙打官司的法庭记录，写成了这部喜剧"),
    PIL("pl-zarnowiec", "Konopnicka Manor, Żarnowiec", "扎尔诺维茨科诺普尼茨卡庄园",
        "The manor given to Maria Konopnicka by the nation in 1903 to mark twenty-five years of her writing. She spent the warmer months here until 1910 and finished Mr Balcer in Brazil in it. It is now her museum",
        "1903 年，为纪念玛丽亚·科诺普尼茨卡写作二十五周年，国人把这座庄园赠给了她。到 1910 年为止，她每年天暖的时候都住在这里，并在这里写完了《巴尔采尔先生在巴西》。现为她的纪念馆", ["pl-pan-balcer"]),
    ORIG("pl-dukla", "Dukla", "杜克拉",
         "A small town below the Dukla Pass in the Low Beskids, with a market square, a baroque palace and two churches. Stasiuk, who lives in a village of the same hills, keeps coming back to it in the book that bears its name",
         "低贝斯基德山杜克拉山口下的小城，有一座集市广场、一座巴洛克宫殿和两座教堂。斯塔休克住在同一片山里的一个村子，在以它为名的那本书里一次次回到这里"),
    ORIG("pl-sanok", "Sanok", "萨诺克",
         "The town on the San where, in Book III of Hašek's novel, Švejk's march battalion leaves the train and sets out on foot towards the front. A bronze Švejk sits on a bench in the main street",
         "桑河边的城市。哈谢克小说第三卷里，帅克所在的先遣营在这里下了火车，徒步开往前线。城里的主街上有一尊坐在长椅上的帅克铜像"),
]

# ============================== lines ==============================
lines = [
    # ---- quotations ----
    Q("pl-pan-tadeusz-1", "pl-pan-tadeusz", "pl-jasna-gora", "Book I, lines 5–7", "第一卷，第 5–7 行", "Polish", PT1,
      raw(PT1, "Panno święta, co Jasnej bronisz Częstochowy", "z jego wiernym ludem!"), ["Częstochowy"],
      "Holy Virgin, who guard bright Częstochowa and shine in the Ostra Gate! You who shelter the castle town of Nowogródek with its faithful people!", ["Częstochowa"],
      "圣洁的童贞女啊，你守护着光明山上的琴斯托霍瓦，在尖门之上放射光辉！你庇护着诺沃格鲁代克的城堡和城中忠诚的百姓！", ["琴斯托霍瓦"]),
    Q("pl-pan-tadeusz-2", "pl-pan-tadeusz", "pl-bialowieza", "Book IV, lines 1–4", "第四卷，第 1–4 行", "Polish", PT4,
      raw(PT4, "Rówienniki litewskich", "wielkiego Mindowy,"), ["Białowieży"],
      "Trees coeval with the grand dukes of Lithuania, trees of Białowieża, Świteź, Ponary, Kuszelewo! whose shade once fell on the crowned heads of dread Witenes and great Mindowe,", ["Białowieża"],
      "与立陶宛历代大公同龄的树木啊，比亚沃维耶扎、希维泰什、波纳雷、库舍莱沃的树木！你们的浓荫曾落在威严的维泰尼斯和伟大的明道加斯戴着王冠的头上，", ["比亚沃维耶扎"]),
    Q("pl-kordian-1", "pl-kordian", "pl-zamek-krolewski", "Act III, Scene 1, stage direction", "第三幕第一场，舞台说明", "Polish", "Kordian/Akt III",
      raw("Kordian/Akt III", "Plac przed zamkiem królewskim w Warszawie", "patrząc na zamek rozmawiają."), ["zamkiem królewskim"],
      "The square before the Royal Castle in Warsaw; the windows of the houses around are hung with carpets and full of spectators. – A great scaffold covered with red cloth fills most of the square – on it women in their finery sit in rows... Nearest the audience stands Sigismund's Column, with the common people seated on its base... People of every rank stand about, looking at the castle and talking.", ["Royal Castle"],
      "华沙王宫城堡前的广场，四周房屋的窗口挂着毯子，挤满了看热闹的人。——一座蒙着红布的大看台占去了广场的大半——盛装的妇女一排排坐在上面……离观众最近的是西吉斯蒙德圆柱，百姓坐在柱基上……各色人等站在四周，望着城堡交谈。", ["王宫城堡"]),
    Q("pl-balladyna-1", "pl-balladyna", "pl-goplo", "Act I, Scene 2", "第一幕第二场", "Polish", "Balladyna/Akt pierwszy",
      raw("Balladyna/Akt pierwszy", "Inna część lasu — widać jezioro Gopło.", "Spi jeszcze w Gople."), ["Gopło"],
      "Another part of the forest — Lake Gopło can be seen.\nSKIERKA AND CHOCHLIK (enter.)\nSKIERKA.\nWhere is Goplana, our queen?\nCHOCHLIK.\nStill asleep in Gopło.", ["Gopło"],
      "森林的另一处——可以望见戈普沃湖。\n斯凯尔卡和霍赫利克（上。）\n斯凯尔卡：\n我们的女王戈普拉娜在哪儿？\n霍赫利克：\n还在戈普沃湖里睡着呢。", ["戈普沃湖"]),
    Q("pl-stara-basn-1", "pl-stara-basn", "pl-goplo", "Volume III, Chapter 1", "第三卷第一章", "Polish", "Stara baśń/Tom III/I",
      raw("Stara baśń/Tom III/I", "Ciągnęli kmiecie ze wszech stron nad Gopło", "ale nie chcąc ustąpić."), ["Gopło"],
      "From every side the freeholders made their way to Gopło; the Leszeks rode too, grim-faced, with fear in their hearts, but unwilling to give way.", ["Gopło"],
      "自由农从四面八方向戈普沃湖赶来；莱谢克家族的人也骑马来了，脸色阴沉，心里害怕，却不肯退让。", ["戈普沃湖"]),
    Q("pl-fraszki-1", "pl-fraszki", "pl-czarnolas", "'On the Linden Tree', lines 1–4", "《咏椴树》第 1–4 行", "Polish", "Ziemia polska w pieśni/Na lipę",
      raw("Ziemia polska w pieśni/Na lipę", "Gościu, siądź pod mym liściem", "rozstrzelane cienie."), ["pod mym liściem"],
      "Guest, sit down beneath my leaves and take your rest; the sun will not reach you here, I promise you, though it climb its highest and its straight rays draw the scattered shadows in beneath the trees.", ["beneath my leaves"],
      "客人啊，请坐在我的叶荫下歇一歇，我向你保证，太阳照不到这里，哪怕它升到最高处，直射的光线把四散的树影都收拢到树下。", ["我的叶荫下"]),
    Q("pl-lalka-1", "pl-lalka", "pl-krakowskie-przedmiescie", "Volume I, Chapter 1", "第一卷第一章", "Polish", "Lalka (Prus)/Tom I/I",
      raw("Lalka (Prus)/Tom I/I", "W początkach r. 1878", "pod firmą J. Mincel i S. Wokulski."), ["Krakowskiego Przedmieścia"],
      "At the beginning of 1878, when the political world was occupied with the peace of San Stefano, the election of a new pope, or the chances of a European war, the merchants of Warsaw, and likewise the educated public of a certain part of Krakowskie Przedmieście, were no less warmly interested in the future of the fancy-goods shop trading as J. Mincel and S. Wokulski.", ["Krakowskie Przedmieście"],
      "1878 年初，政界正忙着谈论圣斯特凡诺和约、新教皇的选举或欧洲开战的可能，华沙的商人们，还有克拉科夫郊区街某一带的知识界，却同样热切地关心着“J. 明采尔与 S. 沃库尔斯基”这家时髦杂货店的前途。", ["克拉科夫郊区街"]),
    Q("pl-lalka-2", "pl-lalka", "pl-powisle", "Volume I, Chapter 8", "第一卷第八章", "Polish", "Lalka (Prus)/Tom I/VIII",
      raw("Lalka (Prus)/Tom I/VIII", "Wokulski doszedł do brzegu Wisły", "którą piła Warszawa."), ["Wisły"],
      "Wokulski came to the bank of the Vistula and stopped in amazement. Over several acres there rose a hill of the most loathsome refuse, stinking, almost stirring in the sun, and a few dozen paces further on lay the reservoirs of the water that Warsaw drank.", ["Vistula"],
      "沃库尔斯基走到维斯瓦河岸边，愣住了。几亩大的一片地上，隆起一座最令人作呕的垃圾山，臭气熏天，在太阳底下几乎在蠕动，而几十步开外，就是华沙人饮用水的蓄水池。", ["维斯瓦河"]),
    Q("pl-lalka-3", "pl-lalka", "pl-lazienki", "Volume I, Chapter 11", "第一卷第十一章", "Polish", "Lalka (Prus)/Tom I/XI",
      raw("Lalka (Prus)/Tom I/XI", "Znalazłszy się w Łazienkach", "zapominając o świecie."), ["Łazienkach"],
      "Once in the Łazienki park he would leap from the carriage and run to the pond where the countess, who liked to feed the swans, usually walked. He came too early, and then he would drop onto a bench somewhere, bathed in cold sweat, and sit motionless, his eyes turned towards the palace, forgetting the world.", ["Łazienki"],
      "一到瓦津基公园，他就跳下马车，跑向池塘边——喜欢喂天鹅的伯爵夫人通常在那里散步。他总是来得太早，于是随便倒在一张长椅上，浑身冷汗，一动不动地坐着，眼睛望着宫殿的方向，忘了整个世界。", ["瓦津基公园"]),
    Q("pl-krzyzacy-1", "pl-krzyzacy", "pl-tyniec", "Part 1, Chapter 1", "第一部第一章", "Polish", KRZ + "Część pierwsza/I",
      raw(KRZ + "Część pierwsza/I", "W Tyńcu, w gospodzie", "w podróży doznał."), ["Tyńcu"],
      "At Tyniec, in the inn 'Under the Savage Aurochs', which belonged to the abbey, a few men sat listening to the tale of a soldier who had seen the world and who, come from distant parts, was telling them of the adventures he had met with in war and on the road.", ["Tyniec"],
      "在蒂涅茨，修道院名下的“猛野牛”客店里，坐着几个人，正听一位见过世面的武士讲故事；他从远方来，给他们讲自己在战场上和旅途中的种种遭遇。", ["蒂涅茨"]),
    Q("pl-krzyzacy-2", "pl-krzyzacy", "pl-malbork", "Part 9, Chapter 6", "第九部第六章", "Polish", KRZ + "Część dziewiąta/VI",
      raw(KRZ + "Część dziewiąta/VI", "A przedewszystkiem sam widok Malborga", "przybliżeniu porównać."), ["Malborga"],
      "And above all the mere sight of Malbork could strike dread into the heart of any Pole, for with that fortress, counting the High Castle, the Middle Castle and the Outer Bailey, no other in the whole world could even approximately compare.", ["Malbork"],
      "尤其是，单是马尔堡的景象就足以让任何一个波兰人心生恐惧，因为这座要塞连同高堡、中堡和外堡在内，全世界没有哪一座能勉强同它相比。", ["马尔堡"]),
    Q("pl-krzyzacy-3", "pl-krzyzacy", "pl-grunwald", "Part 11, Chapter 5", "第十一部第五章", "Polish", KRZ + "Część jedenasta/V",
      raw(KRZ + "Część jedenasta/V", "W środku owej przestrzeni", "smutne ugory Tannenberga."), ["Grunwaldu"],
      "In the middle of that expanse, which rose gently towards the west, the water-meadows of Grunwald showed green, and a little further off the thatched roofs and sad fallows of Tannenberg showed grey.", ["Grunwald"],
      "这片向西缓缓升高的原野中央，格伦瓦尔德的河滩草地一片青绿，稍远处是坦能堡灰蒙蒙的茅草屋顶和凄凉的休耕地。", ["格伦瓦尔德"]),
    Q("pl-potop-1", "pl-potop", "pl-jasna-gora", "Volume III, Chapter 16", "第三卷第十六章", "Polish", "Potop (Sienkiewicz)/Tom III/Rozdział XVI",
      raw("Potop (Sienkiewicz)/Tom III/Rozdział XVI", "Kraj cały był jako okręt", "koniec masztu nad falami."), ["klasztor"],
      "The whole country was like a ship already sunk in the abyss, and only that monastery still stood out like the tip of a mast above the waves.", ["monastery"],
      "整个国家像一艘已沉入深渊的船，只有那座修道院还像桅杆的尖顶一样露在波涛之上。", ["修道院"]),
    Q("pl-chlopi-1", "pl-chlopi", "pl-lipce", "Spring, Chapter 1", "《春》第一章", "Polish", "Chłopi (Reymont)/Wiosna/I",
      raw("Chłopi (Reymont)/Wiosna/I", "Aż dopiero, gdy sygnaturka", "padając na kolana."), ["Lipieckim"],
      "Only when the little bell began to twitter on Lipce church, like a small bird calling to prayer, did the old woman suddenly come to herself and fall on her knees.", ["Lipce"],
      "直到利普采教堂上的小钟像一只召唤人祈祷的小鸟似的啁啾起来，老太婆才猛然回过神，双膝跪下。", ["利普采"]),
    Q("pl-ziemia-1", "pl-ziemia-obiecana", "pl-palac-poznanskiego", "Volume I, Chapter 1", "第一卷第一章", "Polish", ZO1,
      raw(ZO1, "Łódź się budziła.", "hasło do pracy."), ["Łódź"],
      "Łódź was waking.\nThe first shrill factory whistle tore the silence of the early morning, and after it, in every part of the city, others began to start up ever more noisily and screamed in hoarse, unruly voices, like a choir of monstrous cocks crowing the call to work from metal throats.", ["Łódź"],
      "罗兹正在醒来。\n第一声尖厉的工厂汽笛撕破了清晨的寂静，接着，全城各处别的汽笛也一个比一个喧闹地响起来，用嘶哑、不听管束的嗓音嚎叫，像一群怪物般的公鸡，用金属的喉咙啼出上工的号令。", ["罗兹"]),
    Q("pl-ziemia-2", "pl-ziemia-obiecana", "pl-piotrkowska", "Volume I, Chapter 1", "第一卷第一章", "Polish", ZO1,
      raw(ZO1, "Deszcz mrzył bezustannie", "pałacem fabrykanta."), ["Piotrkowskiej ulicy"],
      "The rain drizzled without stopping and slanted in, reaching halfway up the windows of the little houses that stood close together at this end of Piotrkowska Street, pushed apart only here and there by a giant of a factory or a manufacturer's splendid palace.", ["Piotrkowska Street"],
      "雨下个不停，斜斜地打过来，直打到小房子的半截窗户上；在彼得科夫斯卡大街的这一头，这些小房子一幢挨着一幢，只是偶尔被一座巨人般的工厂或厂主的华丽宫殿挤开。", ["彼得科夫斯卡大街"]),
    Q("pl-syzyfowe-1", "pl-syzyfowe-prace", "pl-kielce", "Chapter 3", "第三章", "Polish", "Syzyfowe prace/III",
      raw("Syzyfowe prace/III", "Na dolnym korytarzu gimnazjum", "jedną kategorję: rodziców."), ["Klerykowie"],
      "In the lower corridor of the classical gymnasium in Kleryków there was a great crowd of people. There were officials, gentry, priests, tradesmen, and even the better-off peasants. At that moment the whole crowd made up a single category: parents.", ["Kleryków"],
      "克莱里科夫古典中学楼下的走廊里挤满了人。有官吏、乡绅、神父、工商业者，甚至还有富裕些的农民。此刻这一大群人只属于同一类：家长。", ["克莱里科夫"]),
    Q("pl-przedwiosnie-1", "pl-przedwiosnie", "pl-belweder", "Part 3, last pages", "第三部结尾", "Polish", "Przedwiośnie (Żeromski)/Część trzecia",
      raw("Przedwiośnie (Żeromski)/Część trzecia", "Tego dnia właśnie od Nowego Światu", "w stronę Belwederu."), ["Belwederu"],
      "On that very day, from Nowy Świat across Three Crosses Square, a great workers' demonstration was moving towards the Belweder.", ["Belweder"],
      "就在这一天，一支浩大的工人游行队伍从新世界街出发，穿过三十字广场，向贝尔维德宫走去。", ["贝尔维德宫"]),
    Q("pl-puszcza-1", "pl-puszcza-jodlowa", "pl-swiety-krzyz", "Opening", "开篇", "Polish", "Puszcza jodłowa",
      raw("Puszcza jodłowa", "W uszach moich trwa szum twój", "wszystkie dalekie siostrzyce."), ["Łysiec"],
      "Your rustling is still in my ears, forest of my childhood and youth — though for so many years I have not been allowed to hear it waking! In my dreams I range the lofty mountains — Łysica, Łysiec, Strawczana, Bukowa, Klonowa, Stróżna — my own home mountains — Radostowa and Kamień — and all their distant sisters.", ["Łysiec"],
      "你的涛声还在我耳边回响，我童年和青年时代的森林啊——虽然这么多年我再也没能在醒着的时候听到它！我在梦想中跑遍那些高高的山——韦希察山、韦希耶茨山、斯特拉夫恰纳山、布科瓦山、克洛诺瓦山、斯特鲁日纳山——我家门口的山——拉多斯托瓦山和卡缅山——还有它们远方所有的姊妹。", ["韦希耶茨山"]),
    Q("pl-wesele-1", "pl-wesele", "pl-bronowice", "Act I, the set", "第一幕，布景说明", "Polish", "Wesele (Wyspiański)/Akt I",
      raw("Wesele (Wyspiański)/Akt I", "Noc Listopadowa; w chacie, w świetlicy.", "którzy się przez nią przesuną."), ["chacie"],
      "A November night; in a peasant cottage, in the best room. The room is whitewashed a grey that is almost blue, a single greyish half-blue tone that takes in both the furniture and the people who will pass through it.", ["cottage"],
      "十一月的夜晚；农舍里，正屋中。屋子刷成发灰的白色，近乎淡蓝，一种灰蒙蒙的半蓝色调把家具和将从屋里走过的人都罩在里面。", ["农舍"]),
    Q("pl-akropolis-1", "pl-akropolis", "pl-wawel", "Act I, opening lines", "第一幕开头", "Polish", "Akropolis/Akt pierwszy",
      raw("Akropolis/Akt pierwszy", "Poszli i na kościele ostawili dymu", "pokłony bijąc u ołtarza-trumny."), ["kościele"],
      "They have gone, and in the church they have left a trailing cloud of smoke; — it has wound about the columns. The singers who sang the songs of Rome, bowing low before the coffin-altar.", ["church"],
      "他们走了，在教堂里留下一片拖曳的烟云；——它缠绕着廊柱。那些唱罗马圣歌的歌者，方才还在棺椁祭坛前深深叩拜。", ["教堂"]),
    Q("pl-w-tatrach-1", "pl-w-tatrach", "pl-morskie-oko", "'Morskie Oko', I, lines 1–4", "《海眼湖》其一，第 1–4 行", "Polish", "Morskie Oko (Asnyk, wyd. 1898)",
      raw("Morskie Oko (Asnyk, wyd. 1898)", "Ponad płaszczami borów", "głazów świat zamarły."), ["jezioro"],
      "Above the cloaks of the forests, hemmed in by a barrier of giant walls that have closed in a ring, a sombre lake spreads its dark waters, mirroring in its depths a dead world of boulders.", ["lake"],
      "在森林的披风之上，被合围成一圈的巨壁紧紧锁住，一座阴郁的湖铺开它幽暗的水，湖心映出一个死寂的巨石世界。", ["湖"]),
    Q("pl-tetmajer-1", "pl-tetmajer-poezje", "pl-czarny-staw", "'Melody of the Night Mists', lines 1–2", "《夜雾的旋律》第 1–2 行", "Polish", "Melodya mgieł nocnych (Tetmajer, wyd. 1901)",
      raw("Melodya mgieł nocnych (Tetmajer, wyd. 1901)", "(Nad Czarnym Stawem Gąsienicowym).", "po przestworów głębinie..."), ["Czarnym Stawem Gąsienicowym"],
      "(Above Czarny Staw Gąsienicowy.)\nHush, hush, let us not wake the water sleeping in the hollow, lightly let us dance with the wind over the deeps of the open air...", ["Czarny Staw Gąsienicowy"],
      "（在加雄尼措瓦黑湖之上。）\n轻些，轻些，别惊醒山坳里沉睡的水，让我们随风轻舞，掠过长空的深处……", ["加雄尼措瓦黑湖"]),
    Q("pl-eichendorff-1", "pl-eichendorff-gedichte", "pl-lubowice", "'Abschied', first stanza", "《告别》第一节", "German", "Abschied (Eichendorff)",
      raw("Abschied (Eichendorff)", "Im Walde bei Lubowitz.", "du grünes Zelt!"), ["Lubowitz"],
      "In the forest near Lubowitz.\nO valleys wide, o heights, o fair green wood, devout abode of my joy and my sorrows! Out there, forever cheated, the busy world roars by; once more throw your arches round me, you green tent!", ["Lubowitz"],
      "在卢博维茨附近的森林里。\n啊，宽阔的山谷，啊，高冈，啊，美丽青翠的森林，你是我欢乐与悲愁的虔诚居所！外面，那永远受骗的忙碌世界呼啸而过；再一次用你的拱顶把我环抱吧，你这绿色的帐幕！", ["卢博维茨"]),
    Q("pl-svejk-1", SVEJK, "pl-sanok", "Book III, Chapter 4", "第三卷第四章", "Czech", "Osudy dobrého vojáka Švejka za světové války/Marschieren marsch!",
      raw("Osudy dobrého vojáka Švejka za světové války/Marschieren marsch!", "Objevilo se, když se přijelo do Sanoku", "nedostal batalión ničeho."), ["Sanoku"],
      "When they reached Sanok it turned out that the men on the wagon with the Eleventh's field kitchen, where the well-fed Baloun was farting with bliss, had on the whole been right: there would be supper, and besides supper some army bread would be handed out for all the days when the battalion had got nothing.", ["Sanok"],
      "到了萨诺克才发现，十一连炊事车上的人——吃饱了的巴伦正在车上惬意地放着屁——大体上没说错：晚饭是有的，而且除了晚饭，还要补发军用面包，把全营一无所得的那些天都补上。", ["萨诺克"]),
]

# Conrad wrote in English: the passage is the original, re-flowed.
_c = re.sub(r"\s+", " ", raw("Notes on Life and Letters", "To our right the unequal massive towers", "sheen on the others."))
assert "St. Mary's Church" in _c
lines.append(dict(id="pl-conrad-1", book_id="pl-notes-life-letters", place_ids=["pl-mariacki"], location="'Poland Revisited', Part III", location_zh="《重访波兰》第三节",
                  text_en=_c, highlight_en=["St. Mary's Church"], translation="original",
                  text_zh="在我们右边，圣母教堂那两座高矮不一的粗壮塔楼高耸入空中缥缈的清辉，背光的一面漆黑，另一面泛着柔和的磷光。", highlight_zh=["圣母教堂"],
                  status="draft", checked=f"English Wikisource, Notes on Life and Letters (line breaks and double spaces written as single spaces), {DATE}"))

lines += [
    # ---- scene notes ----
    S("pl-ocalenie-s1", "pl-ocalenie", "pl-plac-krasinskich", "'Campo dei Fiori'", "《鲜花广场》",
      "The poem begins in Rome, on the square where Giordano Bruno was burned and where, the moment the fire died, the market went on. Then it turns to Warsaw on a fine spring evening: by the carousel on Krasiński Square couples ride up into the air to cheerful music while, behind the ghetto wall, the houses burn and the wind carries the smuts over. Miłosz's subject is the loneliness of the dying, and the poet who will speak of it later.",
      "诗从罗马写起：布鲁诺被烧死的那座广场上，火刚熄，集市就照常开张。接着转到一个晴朗春夜的华沙：克拉辛斯基广场的旋转木马旁，一对对男女随着欢快的音乐升上半空，而隔离区的墙后面，房子在燃烧，风把黑色的灰烬吹过来。米沃什写的是垂死者的孤独，以及日后将要说起这一切的诗人。",
      ["Krasiński Square"], ["克拉辛斯基广场"], W + "Czes%C5%82aw_Mi%C5%82osz"),
    S("pl-pamietnik-s1", "pl-pamietnik-powstania", "pl-stare-miasto", "August 1944", "1944 年 8 月",
      "Białoszewski tells the sixty-three days as a civilian who never held a gun: running from cellar to cellar, queueing for water, counting the minutes between bombs, carrying the wounded, losing track of the date. He wrote it more than twenty years later in the broken, breathless speech of someone still telling it aloud. From the Old Town he escapes, like thousands of others, through the sewers.",
      "比亚沃舍夫斯基以一个从没拿过枪的平民的身份讲这六十三天：从一个地下室跑到另一个地下室，排队打水，数着两次轰炸之间隔了几分钟，抬伤员，记不清日子。二十多年后他才把它写下来，用的是断断续续、上气不接下气的口语，仿佛还在当面讲给人听。同成千上万的人一样，他是钻下水道逃出老城的。",
      ["Old Town"], ["老城"], PLW + "Pami%C4%99tnik_z_powstania_warszawskiego"),
    S("pl-pianista-s1", "pl-pianista", "pl-umschlagplatz", "August 1942", "1942 年 8 月",
      "Szpilman, a pianist at Polish Radio, is driven to the Umschlagplatz with his parents, brother and two sisters. They wait all day in the heat; his father buys a single caramel and cuts it into six pieces. As the crowd is pushed towards the wagons a Jewish policeman pulls him out of the line by the collar. He never sees his family again, and lives in hiding in Warsaw until the Russians come.",
      "什皮尔曼是波兰广播电台的钢琴师，他同父母、弟弟和两个姐妹一起被赶到转运广场。他们在酷热中等了一整天；父亲买了一块奶糖，切成六份。人群被推向车厢的时候，一个犹太警察揪着衣领把他从队伍里拽了出来。他从此再没见过家人，此后一直躲藏在华沙，直到苏军到来。",
      ["Umschlagplatz"], ["转运广场"], W + "The_Pianist_(memoir)"),
    S("pl-zdazyc-s1", "pl-zdazyc", "pl-umschlagplatz", "Throughout", "全书",
      "Hanna Krall talks with Marek Edelman, the last surviving commander of the ghetto uprising and by then a cardiologist in Łódź. In the summer of 1942 he stood day after day at the gate of the Umschlagplatz as a hospital messenger, pulling out those who could be passed off as sick, and watched four hundred thousand people go by. He refuses to make the uprising more heroic than the walk to the wagons; his work on the cardiac ward, he says, is a race with God for a life.",
      "汉娜·克拉尔同马雷克·埃德尔曼交谈；他是隔离区起义最后一位在世的指挥者，这时已是罗兹的心脏科医生。1942 年夏天，他以医院通信员的身份日复一日站在转运广场的门口，把能冒充病人的人拉出来，眼看着四十万人从面前走过。他不肯把起义说得比走向车厢更英勇；他说，他在心脏科病房里做的事，是在同上帝抢一条命。",
      ["Umschlagplatz"], ["转运广场"], PLW + "Zd%C4%85%C5%BCy%C4%87_przed_Panem_Bogiem"),
    S("pl-mala-apokalipsa-s1", "pl-mala-apokalipsa", "pl-pkin", "Throughout", "全书",
      "In the morning two friends from the opposition come to tell the narrator that it has been decided: at eight that evening he is to burn himself in front of the Palace of Culture, where the Party is in session. He spends the day crossing a Warsaw where bridges fall down, nobody knows the date and the country is about to join the Soviet Union, collecting his petrol and matches and looking for a reason. The book came out in the underground press.",
      "早上，两个反对派的朋友来通知叙述者：事情已经定了，今晚八点他要在文化科学宫前自焚，党正在里面开会。他花了一天穿过华沙——桥在塌，没人知道今天是几号，国家就要并入苏联——一边去取汽油和火柴，一边找一个理由。这本书最初是由地下出版社印行的。",
      ["Palace of Culture"], ["文化科学宫"], PLW + "Ma%C5%82a_apokalipsa"),
    S("pl-family-moskat-s1", "pl-family-moskat", "pl-krochmalna", "Throughout", "全书",
      "The novel follows the household of the rich Warsaw patriarch Meshulam Moskat and the young man from the provinces, Asa Heshel Bannet, who marries into it, from before the First World War to September 1939: the Hasidic courtyards, the markets and prayer houses of streets like Krochmalna, the children who turn to Zionism, Communism or America. It ends with German bombs falling on the city.",
      "小说写华沙富有的大家长梅舒拉姆·莫斯卡特一家，以及从外省来、后来娶了他家姑娘的青年阿萨·赫舍尔·班内特，从第一次世界大战前一直写到 1939 年 9 月：哈西德派的院落，克罗赫马尔纳街这类街道上的集市和祈祷所，转向犹太复国主义、共产主义或美国的下一代。结尾是德国人的炸弹落在城里。",
      ["Krochmalna"], ["克罗赫马尔纳街"], W + "The_Family_Moskat"),
    S("pl-treblinka-s1", "pl-treblinka-hell", "pl-treblinka", "Throughout", "全文",
      "Grossman walks the reader along the route the victims took: the fake station with its painted clock and timetables, the square where families were parted, the 'road of no return' between fences of pine branches, the building with the gas chambers. He describes the revolt of August 1943, and ends on the sandy field itself, which gives up scraps of the dead underfoot.",
      "格罗斯曼领着读者沿受害者走过的路走了一遍：画着钟面和时刻表的假车站，一家人被拆散的广场，两道松枝篱笆之间的“不归路”，设有毒气室的那座房子。他写了 1943 年 8 月的暴动，最后落在那片沙地本身：脚下的土里还不断翻出死者的零碎遗物。",
      ["station"], ["车站"], W + "Vasily_Grossman"),
    S("pl-schindler-s1", "pl-schindler", "pl-fabryka-schindlera", "Throughout", "全书",
      "Keneally builds the book from the testimony of the survivors. Schindler, a Sudeten German on the make, arrives in Kraków in 1939, takes over a bankrupt enamel works and staffs it with cheap Jewish labour; by 1943 the factory in Lipowa Street has become a refuge whose owner bribes, drinks with and lies to the SS to keep his people off the transports, and at last buys them a place on the list for his new plant at Brünnlitz.",
      "基尼利根据幸存者的证词写成此书。辛德勒是个一心想发财的苏台德德国人，1939 年来到克拉科夫，接手一家破产的搪瓷厂，雇用廉价的犹太劳工；到 1943 年，利波瓦街的这家工厂已成了避难所，老板靠行贿、陪酒和撒谎对付党卫军，让自己的人不被送上列车，最后又花钱把他们买进那份名单，带到布吕恩利茨的新厂。",
      ["Lipowa Street"], ["利波瓦街"], W + "Schindler%27s_Ark"),
    S("pl-borowski-s1", "pl-pozegnanie-z-maria", "pl-auschwitz", "'This Way for the Gas, Ladies and Gentlemen'", "《女士们先生们，请进毒气室》",
      "A summer day at the Birkenau ramp. The narrator, a Polish political prisoner, joins the 'Canada' squad that unloads a transport of Jews; in return the squad keeps the food from the wagons. Train after train comes in; he carries out the dead infants, is sick, and goes back to work. Borowski gives the narrator his own first name and no excuses.",
      "比克瑙站台上的一个夏日。叙述者是波兰政治犯，他跟着“加拿大”工作队去卸一车犹太人；作为报酬，工作队可以留下车厢里的食物。列车一趟接一趟开来；他把死去的婴儿抬出来，吐了，又回去接着干。博罗夫斯基让叙述者用了自己的名字，没有替他辩解一句。",
      ["Birkenau"], ["比克瑙"], W + "This_Way_for_the_Gas,_Ladies_and_Gentlemen"),
    S("pl-czarny-ogrod-s1", "pl-czarny-ogrod", "pl-nikiszowiec", "Throughout", "全书",
      "Szejnert, a reporter, follows the Giesche company's two model settlements from their founding: the garden village of Giszowiec and the brick blocks of Nikiszowiec. Through parish books, company files and family memories she tells what plebiscite, three uprisings, two wars and changing borders did to people who said of themselves only that they were from here.",
      "记者出身的谢伊内特从建村写起，追踪吉舍公司的两处模范住宅区：花园式的吉绍维茨和砖楼成片的尼基绍维茨。她靠堂区登记册、公司档案和各家的回忆，讲述公民投票、三次起义、两场战争和一再变动的国界，给这些只说自己是“本地人”的人带来了什么。",
      ["Nikiszowiec"], ["尼基绍维茨"], PLW + "Ma%C5%82gorzata_Szejnert"),
    S("pl-erste-polka-s1", "pl-erste-polka", "pl-radiostacja", "31 August 1939", "1939 年 8 月 31 日",
      "One day in the border town, seen mostly from the Piontek household: Valeska, the piano teacher, is marrying off her daughter Irma; her husband lies ill in bed; her son Josel roams the town. German and the local Polish dialect mix in people's speech. In the evening some of them become witnesses of the staged raid on the radio station.",
      "边境小城里的一天，主要从皮翁泰克一家的角度来看：钢琴教师瓦莱斯卡忙着操办女儿伊尔玛的婚礼；她的丈夫卧病在床；儿子约泽尔在城里游荡。人们说话时德语和当地的波兰方言混在一起。傍晚，他们当中有人成了那场伪造的广播电台袭击的目击者。",
      ["radio station"], ["广播电台"], W + "Horst_Bienek"),
    S("pl-weber-s1", "pl-weber", "pl-pieszyce", "Acts I and IV", "第一幕、第四幕",
      "The play opens in the manufacturer Dreissiger's house at Peterswaldau, where the home weavers queue to hand in their cloth and have their pay docked. By Act IV they are in the street outside, singing the song of the 'bloody justice'; Dreissiger and his family slip away and the crowd goes through the house, breaking what it finds. The last act moves to Langenbielau and the soldiers' volley.",
      "戏从彼得斯瓦尔道厂主德赖西格的家里开场：家庭织工排着队来交布，工钱被东扣西扣。到第四幕，他们已经站在门外的街上，唱着那首“血腥的审判”之歌；德赖西格一家溜走了，人群冲进宅子，见什么砸什么。最后一幕转到朗根比劳，军队开了枪。",
      ["Peterswaldau"], ["彼得斯瓦尔道"], W + "The_Weavers_(play)"),
    S("pl-empuzjon-s1", "pl-empuzjon", "pl-sokolowsko", "Throughout", "全书",
      "Mieczysław Wojnicz, a student from Lwów, comes to Görbersdorf in September 1913 to be treated for consumption and lodges in a guesthouse for gentlemen. Every evening the lodgers drink the local liqueur and discourse on the inferiority of women; every November, he learns, a young man of the village is killed. Tokarczuk calls the book a health-resort horror story and writes it in the shadow of The Magic Mountain.",
      "利沃夫来的大学生梅奇斯瓦夫·沃伊尼奇 1913 年 9 月到格贝尔斯多夫治肺病，住进一家只收男客的膳宿公寓。房客们每晚喝着当地的利口酒，高谈女人如何低劣；他又听说，每年十一月村里都有一个年轻男人被杀。托卡尔丘克管这本书叫“疗养地恐怖小说”，它是在《魔山》的影子里写成的。",
      ["Görbersdorf"], ["格贝尔斯多夫"], W + "The_Empusium"),
    S("pl-dom-dzienny-s1", "pl-dom-dzienny", "pl-nowa-ruda", "Throughout", "全书",
      "The narrator and her husband move into a house in a valley outside Nowa Ruda, in land that was German until 1945. The book is made of what gathers there: the talk of her neighbour Marta, a wig-maker; dreams collected from the internet; recipes for mushrooms; the legend of the bearded saint Kummernis and of the monk who wrote her life; the story of the Germans who left and come back to look.",
      "叙述者和丈夫搬进新鲁达城外山谷里的一所房子，这片土地 1945 年以前属于德国。全书由聚拢到这里的东西组成：做假发的邻居玛尔塔的闲谈，从互联网上收集来的梦，蘑菇菜谱，长胡子的圣女库梅尔尼斯的传说和为她写传的修士的故事，还有那些离开了又回来看一眼的德国人。",
      ["Nowa Ruda"], ["新鲁达"], W + "House_of_Day,_House_of_Night"),
    S("pl-plug-s1", "pl-plug", "pl-nowa-ruda", "Throughout", "全书",
      "Janina Duszejko, an elderly former engineer who teaches English and looks after the summer houses on a windy plateau by the Czech border, is woken one winter night: her neighbour, a poacher she calls Big Foot, lies dead with a deer bone in his throat. More hunters die. She writes to the police that the animals are taking revenge, casts horoscopes, and translates Blake.",
      "雅尼娜·杜舍伊科上了年纪，从前是工程师，如今教英语，还替人照看捷克边境旁一处多风高地上的避暑房子。一个冬夜她被叫醒：她称作“大脚”的邻居、一个偷猎者死了，喉咙里卡着一块鹿骨。接着又有猎人死去。她写信告诉警察这是动物在复仇，一边排星盘，一边翻译布莱克。",
      ["plateau"], ["高地"], W + "Drive_Your_Plow_Over_the_Bones_of_the_Dead"),
    S("pl-breslau-s1", "pl-smierc-w-breslau", "pl-wroclaw-glowny", "Opening", "开篇",
      "The investigation takes Eberhard Mock, a policeman with a taste for chess, Latin and brothels, through the Breslau of the first months of Nazi rule: the police headquarters, the freemasons he belongs to, the Gestapo who want a Jewish culprit. Krajewski gives every street its German name, and the city itself, which no longer exists under that name, is the book's real subject.",
      "这桩案子领着埃伯哈德·莫克——一个爱下棋、爱拉丁文、也爱逛妓院的警察——走遍纳粹上台头几个月的布雷斯劳：警察总局，他所属的共济会，一心要找个犹太人顶罪的盖世太保。克拉耶夫斯基给每条街都用了德语旧名；这座已不再叫这个名字的城市，才是书真正的主角。",
      ["Breslau"], ["布雷斯劳"], PLW + "%C5%9Amier%C4%87_w_Breslau"),
    S("pl-kindheitsmuster-s1", "pl-kindheitsmuster", "pl-gorzow", "Throughout", "全书",
      "The narrator drives to the Polish town with her husband, brother and teenage daughter and walks its streets looking for the child she was, whom she can only call by another name, Nelly: the family grocery, the Hitler Youth meetings she loved, the night the synagogue burned, the trek west in 1945. The question the book keeps asking is how one became what one was.",
      "叙述者同丈夫、弟弟和十几岁的女儿开车来到这座已属波兰的城市，在街上寻找当年的那个孩子——她只能用另一个名字“内莉”来称呼她：家里的杂货店，她曾经喜爱的希特勒青年团集会，犹太会堂被烧的那一夜，1945 年向西的逃难。全书反复追问的是：人是怎么变成当初那个样子的。",
      ["Polish town"], ["这座已属波兰的城市"], W + "Patterns_of_Childhood"),
    S("pl-effi-s1", EFFI, "pl-swinoujscie", "Chapters 6–22", "第六至二十二章",
      "Effi, seventeen, arrives in Kessin as the wife of the district governor Innstetten. The town has a harbour, a pier, dunes and a wood, and a few consuls and a hunchbacked apothecary for society; their house has an upper room no one uses, a stuffed shark in the hall and the story of a Chinaman buried among the dunes. Here, bored and frightened, she lets Major Crampas ride beside her along the beach.",
      "十七岁的艾菲作为县长殷士台顿的妻子来到凯辛。小城有港口、栈桥、沙丘和一片树林，社交圈里只有几位领事和一个驼背的药剂师；他们家楼上有间没人用的屋子，门厅里挂着鲨鱼标本，还有一个中国人葬在沙丘间的传说。就在这里，又闷又怕的她让克拉姆巴斯少校骑马陪她走在海滩上。",
      ["Kessin"], ["凯辛"], W + "Effi_Briest"),
    S("pl-blechtrommel-s1", "pl-blechtrommel", "pl-poczta-polska", "Book One, 'The Polish Post Office'", "第一篇“波兰邮局”",
      "Oskar takes his broken drum to the caretaker Kobyella at the Polish Post Office to have it mended, and so is inside with his presumptive father Jan Bronski when the attack begins. In the room where the letters are stored the three of them play skat while shells hit the building, the dying Kobyella held upright with braces to make a third. Jan is taken out with the others and shot.",
      "奥斯卡带着敲坏的鼓去波兰邮局找看门人科比埃拉修理，于是进攻开始时，他正同他那位可能的生父扬·布朗斯基一起待在楼里。炮弹打在楼上，他们三个在存放信件的房间里玩斯卡特牌，垂死的科比埃拉被人用背带捆着坐直，好凑成三家。扬后来同其他人一起被押出去枪毙了。",
      ["Polish Post Office"], ["波兰邮局"], W + "The_Tin_Drum"),
    S("pl-blechtrommel-s2", "pl-blechtrommel", "pl-wrzeszcz", "Book One", "第一篇",
      "Oskar Matzerath is born in Langfuhr, in the flat behind his parents' grocery in Labesweg, under two sixty-watt bulbs. On his third birthday he is given a tin drum and decides to stop growing; from the cellar steps, the courtyard and the tram to the city he watches the suburb's grocers, greengrocers and bakers turn into Nazis.",
      "奥斯卡·马策拉特出生在朗富尔，拉贝斯路父母杂货店后面的住房里，头顶是两只六十瓦的灯泡。三岁生日那天他得到一面铁皮鼓，决定不再长高；他在地窖的台阶上、院子里和进城的电车上，看着这片郊区的杂货商、菜贩和面包师一个个变成纳粹。",
      ["Langfuhr"], ["朗富尔"], W + "The_Tin_Drum"),
    S("pl-weiser-s1", "pl-weiser", "pl-wrzeszcz", "Summer 1957", "1957 年夏天",
      "A hot summer; fish are dying in the bay and the priest preaches punishment. The narrator and his friends fall under the spell of a thin Jewish boy, Dawid Weiser, who tames a panther at the Oliwa zoo, plays football like a master and sets off explosions in the hollow behind the shooting range. After the last one he and the girl Elka are gone. Years later the narrator is still being questioned, by the school and by himself.",
      "一个炎热的夏天；海湾里的鱼成片死去，神父在布道时说这是惩罚。叙述者和伙伴们被一个瘦瘦的犹太男孩达维德·魏泽尔迷住了：他在奥利瓦动物园驯服了一头黑豹，踢起球来像个行家，还在靶场后面的洼地里引爆炸药。最后一次爆炸之后，他和女孩埃尔卡都不见了。多年以后叙述者仍在受盘问——先是学校问他，后来是他自己问自己。",
      ["Oliwa"], ["奥利瓦"], PLW + "Weiser_Dawidek"),
    S("pl-hanemann-s1", "pl-hanemann", "pl-oliwa", "Throughout", "全书",
      "Hanemann, a professor of anatomy in Danzig, gives up his chair after the woman he loves drowns when an excursion steamer sinks, and when the Germans flee in 1945 he lets the last ship go without him. The narrator, a boy whose Polish parents have been given the flat below, tells of the silent German upstairs and of the things the departed left behind: china, linen, door handles, a way of living.",
      "哈内曼是但泽的解剖学教授。他爱的女人在一艘游船沉没时淹死了，他从此放弃教席；1945 年德国人逃离的时候，他任凭最后一班船开走而没有上去。叙述者是个男孩，他的波兰父母分到了楼下的那套房子；他讲的是楼上那个沉默的德国人，还有离开的人留下的东西：瓷器，床单桌布，门把手，一种过日子的方式。",
      ["Danzig"], ["但泽"], W + "Stefan_Chwin"),
    S("pl-westerplatte-s1", "pl-westerplatte-piesn", "pl-westerplatte", "Whole poem", "全诗",
      "A short ballad written in the first weeks of the war. When their days are fulfilled and it is time to die in summer, the soldiers of Westerplatte march off to heaven in ranks; the summer is fine, heather is in flower in the heavenly meadows, and they promise to come down again to Warsaw when the cold winds blow. Gałczyński himself was taken prisoner that September.",
      "战争头几个星期写成的一首短歌谣。大限已到，该在夏天死去的时候，韦斯特普拉特的士兵们列着队向天堂走去；那个夏天很美，天上的草地里石楠开着花，他们许诺等寒风吹起时再下来回到华沙。加乌琴斯基本人就在那个九月当了俘虏。",
      ["Westerplatte"], ["韦斯特普拉特"], W + "Konstanty_Ildefons_Ga%C5%82czy%C5%84ski"),
    S("pl-szosta-klepka-s1", "pl-szosta-klepka", "pl-jezyce", "Throughout", "全书",
      "The first of the Jeżyce books belongs to the Żak family, crowded into one flat of an old tenement: Celestyna, called Cesia, a schoolgirl sure that she is plain and dull, her beautiful elder sister Julia, a father everyone calls Żaczek, a mother busy with her own work, a grandfather, an aunt and little Bobcio. Over a school year of homework and first love she finds out otherwise. The Borejkos, who take over the series, arrive in a later volume.",
      "“耶日采记”的第一本写的是挤在一幢老公寓某一套房子里的扎克一家：中学生采莱斯蒂娜（小名采霞）认定自己又平凡又乏味，她有个漂亮的姐姐尤利娅，一个人人都叫他“扎切克”的爸爸，一个忙着自己工作的妈妈，还有爷爷、姑姑和小博布乔。在做功课、初次恋爱的那个学年里，她发现事情并非如此。后来成为整套书主角的博雷伊科一家，要到后面的一本才登场。",
      ["Jeżyce"], ["耶日采"], PLW + "Sz%C3%B3sta_klepka"),
    S("pl-noce-i-dnie-s1", "pl-noce-i-dnie", "pl-kalisz", "Throughout", "全书",
      "Barbara Ostrzeńska, a girl from an impoverished gentry family in Kaliniec, marries Bogumił Niechcic, a veteran of the 1863 rising, without loving him, and spends thirty years beside him on the estates he manages, restless where he is content. After his death she moves back to town. When the Germans shell Kaliniec in 1914 she drives out of the burning streets in a cart, looking for her children.",
      "芭尔芭拉·奥斯特任斯卡出身卡利涅茨一个破落的乡绅家庭，她并不爱博古米乌·涅赫齐茨——一个参加过 1863 年起义的老兵——却嫁给了他，在他替人经管的庄园里陪他过了三十年；他安于现状，她总是心神不定。丈夫死后她搬回城里。1914 年德军炮轰卡利涅茨，她坐着一辆大车驶出燃烧的街道，去找自己的孩子。",
      ["Kaliniec"], ["卡利涅茨"], PLW + "Noce_i_dnie_(powie%C5%9B%C4%87)"),
    S("pl-jakob-s1", "pl-jakob", "pl-radegast", "Throughout", "全书",
      "Jakob Heym, who once sold potato pancakes, is sent to the German guard post for being out after curfew and there overhears a radio report that the Russians are near. To make a friend believe him he says he has a radio, which in the ghetto means death. People stop killing themselves; so day after day he has to invent the news. The narrator, a survivor, offers two endings, and says which one happened.",
      "雅各布·海姆从前是卖土豆饼的。他因为宵禁后还在街上，被打发去德国岗哨，在那里偷听到一条广播：俄国人已经不远了。为了让一个朋友相信，他说自己有一台收音机——在隔离区里这是死罪。人们不再自杀了；于是他只好一天接一天地编造新闻。叙述者是个幸存者，他给出了两个结局，并且说明了哪一个才是真的。",
      ["ghetto"], ["隔离区"], W + "Jacob_the_Liar"),
    S("pl-widnokrag-s1", "pl-widnokrag", "pl-sandomierz", "Throughout", "全书",
      "Piotr, grown up, turns over the photographs of his childhood: the village of his mother's family during the war, and then the town on the hill, where his father is slowly dying. The long stairs between the upper town and the suburb by the river are climbed again and again; a lost shoe, a dog, a first cigarette each open a whole chapter.",
      "已经长大的彼得翻看着童年的照片：战时母亲娘家所在的村子，然后是山坡上的那座城；父亲在城里慢慢地走向死亡。上城和河边郊区之间那道长长的台阶被一遍遍地爬过；一只丢了的鞋、一条狗、第一支烟，各自引出整整一章。",
      ["town on the hill"], ["山坡上的那座城"], W + "Wies%C5%82aw_My%C5%9Bliwski"),
    S("pl-magician-s1", "pl-magician-lublin", "pl-lublin", "Chapter 1", "第一章",
      "Yasha Mazur, tightrope walker, lock-picker and conjurer, comes home to Lublin for the holidays, to his pious wife Esther and his house with its horses, monkey and crow. He does not keep the commandments; he is known in every tavern and has a woman in every town on the road to Warsaw. From here he sets out towards the city, a Christian widow and a burglary that will end with him walled up in a cell in his own yard.",
      "雅夏·马祖尔是走钢丝的、开锁的、变戏法的；他回卢布林过节，回到虔诚的妻子埃丝特身边，回到养着马、猴子和乌鸦的家里。他不守诫命，各家酒馆都认得他，去华沙的路上每个镇子里都有他的女人。他从这里出发，走向那座城市，走向一位信基督教的寡妇和一桩入室行窃——最后他把自己砌进了自家院子里的一间小屋。",
      ["Lublin"], ["卢布林"], W + "The_Magician_of_Lublin_(novel)"),
    S("pl-poemat-s1", "pl-poemat-lublin", "pl-lublin", "Throughout", "全诗",
      "A wanderer comes back to his native town at dusk and walks through it by night under a summer moon: through the old town, past the castle and down the lanes of the Jewish quarter. Each poem of the cycle is one stop on the walk. Czechowicz wrote it as a text for radio.",
      "一个漂泊者在黄昏回到故乡，在夏夜的月光下穿城而行：穿过老城，经过城堡，走进犹太区的小巷。组诗里的每一首是这次夜行的一站。切霍维奇是把它当作广播稿来写的。",
      ["old town"], ["老城"], PLW + "J%C3%B3zef_Czechowicz_(poeta)"),
    S("pl-dwa-ksiezyce-s1", "pl-dwa-ksiezyce", "pl-kazimierz-dolny", "Throughout", "全书",
      "Linked stories of one small town in which two worlds live side by side and hardly look at each other: the locals, Polish and Jewish, boatmen, shopkeepers, beggars and a blind man who knows every stone; and the summer people, painters and their models from Warsaw, for whom the market square is scenery.",
      "一组互相勾连的短篇，写的是同一座小城：两个世界在这里并排过日子，彼此几乎不看一眼——一边是本地人，波兰人和犹太人，船夫、小店主、乞丐，还有一个认得每块石头的盲人；另一边是来消夏的人，华沙来的画家和他们的模特，在他们眼里集市广场只是一道风景。",
      ["small town"], ["小城"], W + "Maria_Kuncewiczowa"),
    S("pl-satan-s1", "pl-satan-goray", "pl-goraj", "Throughout", "全书",
      "Goray, a small town lost among the hills at the back of beyond, has been half emptied by Khmelnytsky's Cossacks. Seventeen years later messengers bring word that the Messiah has appeared; the old rabbi who resists is driven out, fasts turn into feasts, laws are thrown over, and the prophetess of the new age is Rechele, a sick girl in whom, by the end, a dybbuk speaks.",
      "戈拉伊这座深藏在群山之中、仿佛在世界尽头的小镇，被赫梅利尼茨基的哥萨克洗劫得只剩一半人。十七年后，信使带来弥赛亚已经显现的消息；抵制这股风潮的老拉比被赶走，斋戒变成了宴饮，律法被抛到一边，新时代的女先知是病弱的姑娘蕾海莱——到最后，是一个附体的恶灵借她的嘴说话。",
      ["Goray"], ["戈拉伊"], W + "Satan_in_Goray"),
    S("pl-dukla-s1", "pl-dukla", "pl-dukla", "Title piece", "同名长篇散文",
      "Stasiuk drives or walks into the little town again and again, at different hours and seasons, to watch what light does to it: to the empty market square, the bus stop, the tomb of Maria Amalia Mniszech in the parish church with her marble slippers and lace. Memories of a boyhood summer and a girl dancing surface and sink. Nothing happens; the book is about looking.",
      "斯塔休克一次次开车或步行来到这座小城，挑不同的钟点、不同的季节，看光线怎样落在它身上：空荡荡的集市广场，汽车站，堂区教堂里玛丽亚·阿玛利亚·姆尼舍赫的陵墓——大理石雕出的便鞋和蕾丝。少年时代某个夏天和一个跳舞女孩的记忆浮上来，又沉下去。什么也没有发生；这是一本关于“看”的书。",
      ["little town"], ["小城"], W + "Andrzej_Stasiuk"),
    S("pl-zemsta-s1", "pl-zemsta", "pl-odrzykon", "Throughout", "全剧",
      "Two neighbours share one castle and hate each other: the hot-headed Cupbearer Raptusiewicz and the soft-spoken, implacable Notary Milczek. When the Notary hires masons to mend the wall between their halves, the Cupbearer sends his men to drive them off. Each plots a marriage to spite the other, the braggart Papkin carries messages and makes his will, and the young lovers from the two sides are married before either old man can stop it.",
      "两个邻居共住一座城堡，彼此恨之入骨：火暴脾气的司酒官拉普图谢维奇，和说话轻声细气却毫不让步的公证人米尔切克。公证人雇泥瓦匠修两家之间的那堵墙，司酒官就派手下把他们轰走。两人各自盘算着一门亲事来气对方，吹牛大王帕普金来回传话，还立下了遗嘱；两家的一对年轻恋人赶在两个老头来得及阻拦之前成了亲。",
      ["castle"], ["城堡"], W + "Zemsta"),
]

# ============================== write ==============================
used = {p for l in lines for p in l["place_ids"]}
for p in places:
    assert p["id"] in used or p.get("book_ids"), ("place without a line or a book", p["id"])
assert {p["id"] for p in places} == set(CO), set(CO) ^ {p["id"] for p in places}
EXIST = {EFFI, SVEJK}
bids = {x["id"] for x in books} | EXIST
for l in lines:
    assert l["book_id"] in bids, l["id"]
lined = {l["book_id"] for l in lines}
pilgrim = {i for p in places for i in p.get("book_ids", [])}
assert pilgrim <= bids, pilgrim - bids
assert not ({x["id"] for x in books} - lined - pilgrim), {x["id"] for x in books} - lined - pilgrim
assert len({x["id"] for x in places}) == len(places) and len({x["id"] for x in lines}) == len(lines) and len({x["id"] for x in books}) == len(books)

HEAD = "// Poland, hand-written content (tools/content/batches/add_pl1.py, 2026-11-22).\n"
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
