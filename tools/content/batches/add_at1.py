"""11-22: Austria, first pack: 53 new books (and three already on the shared list), 63 places. From the Nibelungenlied on
the Danube and Walther's fur coat to Bernhard, Bachmann, Handke and Jelinek, plus the best-known foreign books set in
the country (The Third Man, The Hare with Amber Eyes, Auden at Kirchstetten, Hemingway at Schruns…).
Fictional settings hang on the real place the book is modelled on, or on the writer's own place, and the note says which.

Quotations (5 books, 6 lines) are cut from Wikisource pages (tools/content/wikisource.py): German and English
Wikisource; English and Chinese translations are our own drafts (translation: "own"), Mark Twain's English is the
original. German Wikisource has little Austrian prose; while Project Gutenberg is down, every other book has a scene
note, in copyright or not, and the public-domain ones (Grillparzer, Stifter, Roth, Zweig, Kraus, the Nibelungenlied…)
can take quotations later.

Coordinates come from Wikimedia Commons (median of the geotagged files of the place's category), from the place's
Wikidata item, or from the coordinates of its German Wikipedia article (cache/at/coords.json).
The Nibelungenlied, A Moveable Feast and The Name of the Rose are the books already on the shared list.

Usage: python3 -I add_at1.py <app_dir> <coords.json> <wikisource_dir>"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b
import wikisource as ws

APP, CO, WS = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8")), sys.argv[3]
DATE = "2026-11-22"
b.init(APP, "", "at", DATE)
W = b.W

def BK(id, title, title_zh, author, author_zh, year, pd=True, **kw):
    d = dict(id=id, title=title, title_zh=title_zh, author=author, author_zh=author_zh, year=year,
             orig_lang=kw.pop("lang", "de"), public_domain=pd, source_url=kw.pop("src", None))
    d.update(kw)
    return d

def C(pid):
    c = CO[pid]
    return c["lat"], c["lon"], c["st"], c["su"]

def ORIG(pid, name, zh, en_note, zh_note, **kw): return b.ORIG(pid, name, zh, *C(pid), en_note, zh_note, **kw)
def PROTO(pid, name, zh, en_note, zh_note, **kw): return b.PROTO(pid, name, zh, *C(pid), en_note, zh_note, **kw)
def PIL(pid, name, zh, en_note, zh_note, ids, **kw): return b.PIL(pid, name, zh, *C(pid), en_note, zh_note, ids, **kw)
def FILM(pid, name, zh, en_scene, zh_scene, ids):
    return b.P(pid, name, zh, *C(pid), "film_location", adaptation={"title": "The Sound of Music", "year": 1965, "kind": "电影"},
               scene=zh_scene, book_ids=ids, scene_en=en_scene)
S = b.S

def raw(title, start, end):
    t = ws.text(WS, title)
    i = t.find(start)
    assert i >= 0, (title, start)
    j = t.find(end, i)
    assert j >= 0, (title, start, end)
    return t[i:j + len(end)]

def Q(id, book, place, loc, loc_zh, site, title, orig, hl_orig, en, hl_en, zh, hl_zh, note="", original=False):
    for text, hls in ((orig, hl_orig), (en, hl_en), (zh, hl_zh)):
        for h in hls:
            assert h in text, (id, h)
    assert "  " not in orig and "\xa0" not in orig and "[" not in orig, (id, "spacing or page mark")
    d = dict(id=id, book_id=book, place_ids=[place], location=loc, location_zh=loc_zh)
    if original:
        d.update(text_en=orig, highlight_en=hl_orig, text_zh=zh, highlight_zh=hl_zh, translation="original")
    else:
        d.update(text_orig=orig, highlight_orig=hl_orig, text_en=en, highlight_en=hl_en, text_zh=zh, highlight_zh=hl_zh, translation="own")
    d.update(status="draft", checked=f"{site} Wikisource, {title}{note}, {DATE}")
    return d

DEWS = lambda t: ws.url("de", t)
SCHN = ("Arthur Schnitzler", "施尼茨勒")
ZWEIG = ("Stefan Zweig", "茨威格")
ROTH = ("Joseph Roth", "约瑟夫·罗特")
BERN = ("Thomas Bernhard", "托马斯·伯恩哈德")
BACH = ("Ingeborg Bachmann", "英格博格·巴赫曼")
STIF = ("Adalbert Stifter", "施蒂弗特")
GRILL = ("Franz Grillparzer", "格里尔帕策")
HOF = ("Hugo von Hofmannsthal", "霍夫曼斯塔尔")

# ============================== books ==============================
books = [
    BK("at-walther-songs", "Songs of Walther von der Vogelweide", "瓦尔特·冯·德·福格威德诗歌", "Walther von der Vogelweide", "瓦尔特·冯·德·福格威德", "c. 1190–1230",
       title_orig="Lieder und Sprüche", aliases=["Under der linden", "Minnesang"]),
    BK("at-alpenkoenig", "The King of the Alps and the Misanthrope", "阿尔卑斯山王与厌世者", "Ferdinand Raimund", "费迪南德·莱蒙德", "1828",
       title_orig="Der Alpenkönig und der Menschenfeind", aliases=["Der Alpenkönig und der Menschenfeind", "Rappelkopf"]),
    BK("at-lumpazivagabundus", "The Evil Spirit Lumpazivagabundus", "恶精灵卢姆帕齐", "Johann Nestroy", "内斯特罗伊", "1833",
       title_orig="Der böse Geist Lumpazivagabundus", aliases=["Der böse Geist Lumpazivagabundus", "Knieriem", "Zwirn", "Leim"]),
    BK("at-arme-spielmann", "The Poor Fiddler", "可怜的乐师", *GRILL, "1848", title_orig="Der arme Spielmann", aliases=["Der arme Spielmann", "The Poor Musician"]),
    BK("at-koenig-ottokar", "King Ottokar's Rise and Fall", "奥托卡国王的兴衰", *GRILL, "1825", title_orig="König Ottokars Glück und Ende",
       aliases=["König Ottokars Glück und Ende", "Koenig Ottokars Glueck und Ende", "Rudolf von Habsburg"]),
    BK("at-bergkristall", "Rock Crystal", "水晶", *STIF, "1853", title_orig="Bergkristall", aliases=["Bergkristall", "Bunte Steine", "Colourful Stones", "Gschaid"]),
    BK("at-nachsommer", "Indian Summer", "晚夏", *STIF, "1857", title_orig="Der Nachsommer", aliases=["Der Nachsommer", "Rosenhaus"]),
    BK("at-lenau-poems", "Poems", "莱瑙诗选", "Nikolaus Lenau", "莱瑙", "1832", title_orig="Gedichte", aliases=["Schilflieder", "Reed Songs"]),
    BK("at-steinklopfer", "The Stonebreakers", "凿石工", "Ferdinand von Saar", "费迪南德·冯·萨尔", "1874", title_orig="Die Steinklopfer",
       aliases=["Die Steinklopfer", "Novellen aus Österreich"]),
    BK("at-waldheimat", "The Forest Home", "林中故乡", "Peter Rosegger", "彼得·罗泽格", "1877", title_orig="Waldheimat",
       aliases=["Waldheimat", "Als ich noch der Waldbauernbub war", "Waldbauernbub"]),
    BK("at-waffen-nieder", "Lay Down Your Arms!", "放下武器！", "Bertha von Suttner", "贝尔塔·冯·苏特纳", "1889", title_orig="Die Waffen nieder!",
       src=DEWS("Die Waffen nieder!"), aliases=["Die Waffen nieder"]),
    BK("at-leutnant-gustl", "Lieutenant Gustl", "古斯特少尉", *SCHN, "1900", title_orig="Leutnant Gustl", src=DEWS("Lieutenant Gustl"), aliases=["Leutnant Gustl", "None but the Brave"]),
    BK("at-reigen", "La Ronde", "轮舞", *SCHN, "1900", title_orig="Reigen", aliases=["Reigen", "Hands Around"]),
    BK("at-traumnovelle", "Dream Story", "梦的故事", *SCHN, "1926", title_orig="Traumnovelle", src=DEWS("Traumnovelle"), aliases=["Traumnovelle", "Rhapsody", "Fridolin", "Albertine", "梦幻记"]),
    BK("at-jedermann", "Everyman", "耶德曼", *HOF, "1911", title_orig="Jedermann", aliases=["Jedermann", "Salzburg Festival", "每个人"]),
    BK("at-chandos", "The Lord Chandos Letter", "钱多斯勋爵的信", *HOF, "1902", title_orig="Ein Brief", aliases=["Ein Brief", "Chandos-Brief"]),
    BK("at-trakl-poems", "Poems", "特拉克尔诗集", "Georg Trakl", "特拉克尔", "1913", title_orig="Gedichte", src=DEWS("Gedichte (Trakl)"),
       aliases=["Musik im Mirabell", "Die schöne Stadt", "Sebastian im Traum", "Grodek"]),
    BK("at-wie-ich-es-sehe", "As I See It", "如我所见", "Peter Altenberg", "彼得·阿尔滕贝格", "1896", title_orig="Wie ich es sehe", aliases=["Wie ich es sehe"]),
    BK("at-letzten-tage", "The Last Days of Mankind", "人类的末日", "Karl Kraus", "卡尔·克劳斯", "1919–1922", title_orig="Die letzten Tage der Menschheit",
       aliases=["Die letzten Tage der Menschheit", "Die Fackel"]),
    BK("at-mann-ohne-eigenschaften", "The Man Without Qualities", "没有个性的人", "Robert Musil", "穆齐尔", "1930–1943", title_orig="Der Mann ohne Eigenschaften",
       aliases=["Der Mann ohne Eigenschaften", "Ulrich", "Kakanien", "Kakania"]),
    BK("at-welt-von-gestern", "The World of Yesterday", "昨日的世界", *ZWEIG, "1942", title_orig="Die Welt von Gestern", aliases=["Die Welt von Gestern"]),
    BK("at-schachnovelle", "Chess Story", "象棋的故事", *ZWEIG, "1942", title_orig="Schachnovelle", aliases=["Schachnovelle", "The Royal Game", "Dr. B."]),
    BK("at-brennendes-geheimnis", "Burning Secret", "灼人的秘密", *ZWEIG, "1911", title_orig="Brennendes Geheimnis", aliases=["Brennendes Geheimnis"]),
    BK("at-radetzkymarsch", "The Radetzky March", "拉德茨基进行曲", *ROTH, "1932", title_orig="Radetzkymarsch", aliases=["Radetzkymarsch", "Trotta"]),
    BK("at-kapuzinergruft", "The Emperor's Tomb", "先王冢", *ROTH, "1938", title_orig="Die Kapuzinergruft", aliases=["Die Kapuzinergruft", "The Capuchin Crypt"]),
    BK("at-wiener-wald", "Tales from the Vienna Woods", "维也纳森林的故事", "Ödön von Horváth", "霍尔瓦特", "1931", title_orig="Geschichten aus dem Wiener Wald",
       aliases=["Geschichten aus dem Wiener Wald", "Marianne", "Odon von Horvath"]),
    BK("at-strudlhofstiege", "The Strudlhof Steps", "斯特鲁德霍夫阶梯", "Heimito von Doderer", "多德勒尔", "1951", pd=False, title_orig="Die Strudlhofstiege",
       aliases=["Die Strudlhofstiege", "Melzer"]),
    BK("at-blendung", "Auto-da-Fé", "迷惘", "Elias Canetti", "卡内蒂", "1935", pd=False, title_orig="Die Blendung", aliases=["Die Blendung", "Peter Kien"]),
    BK("at-malina", "Malina", "马利纳", *BACH, "1971", pd=False, title_orig="Malina", aliases=["Ungargassenland"]),
    BK("at-dreissigste-jahr", "The Thirtieth Year", "三十岁", *BACH, "1961", pd=False, title_orig="Das dreißigste Jahr",
       aliases=["Das dreißigste Jahr", "Jugend in einer österreichischen Stadt", "Youth in an Austrian Town"]),
    BK("at-heldenplatz", "Heldenplatz", "英雄广场", *BERN, "1988", pd=False, title_orig="Heldenplatz", aliases=["Heroes' Square"]),
    BK("at-wittgensteins-neffe", "Wittgenstein's Nephew", "维特根斯坦的侄子", *BERN, "1982", pd=False, title_orig="Wittgensteins Neffe", aliases=["Wittgensteins Neffe"]),
    BK("at-ausloeschung", "Extinction", "消除", *BERN, "1986", pd=False, title_orig="Auslöschung", aliases=["Auslöschung", "Ausloeschung", "Wolfsegg", "Murau"]),
    BK("at-ursache", "An Indication of the Cause", "原因", *BERN, "1975", pd=False, title_orig="Die Ursache", aliases=["Die Ursache", "Gathering Evidence"]),
    BK("at-wunschloses-unglueck", "A Sorrow Beyond Dreams", "无欲的悲歌", "Peter Handke", "彼得·汉德克", "1972", pd=False, title_orig="Wunschloses Unglück",
       aliases=["Wunschloses Unglück", "Wunschloses Unglueck"]),
    BK("at-klavierspielerin", "The Piano Teacher", "钢琴教师", "Elfriede Jelinek", "耶利内克", "1983", pd=False, title_orig="Die Klavierspielerin",
       aliases=["Die Klavierspielerin", "Erika Kohut"]),
    BK("at-trafikant", "The Tobacconist", "读报纸的人", "Robert Seethaler", "罗伯特·泽塔勒", "2012", pd=False, title_orig="Der Trafikant", aliases=["Der Trafikant", "Franz Huchel"]),
    BK("at-traumdeutung", "The Interpretation of Dreams", "梦的解析", "Sigmund Freud", "弗洛伊德", "1899", title_orig="Die Traumdeutung", aliases=["Die Traumdeutung"]),
    BK("at-alte-koenig", "The Old King in His Exile", "流放的老国王", "Arno Geiger", "阿尔诺·盖格", "2011", pd=False, title_orig="Der alte König in seinem Exil",
       aliases=["Der alte König in seinem Exil"]),
    BK("at-schlafes-bruder", "Brother of Sleep", "睡眠兄弟", "Robert Schneider", "罗伯特·施奈德", "1992", pd=False, title_orig="Schlafes Bruder",
       aliases=["Schlafes Bruder", "Elias Alder", "Eschberg"]),
    BK("at-reisebilder", "Journey from Munich to Genoa", "从慕尼黑到热那亚的旅行", "Heinrich Heine", "海涅", "1830", title_orig="Reise von München nach Genua",
       aliases=["Reise von München nach Genua", "Reisebilder", "Travel Pictures"]),
    BK("at-third-man", "The Third Man", "第三人", "Graham Greene", "格雷厄姆·格林", "1950", pd=False, lang="en", aliases=["Harry Lime", "Rollo Martins"]),
    BK("at-setting-free-bears", "Setting Free the Bears", "放熊归山", "John Irving", "约翰·欧文", "1968", pd=False, lang="en"),
    BK("at-trapp-family", "The Story of the Trapp Family Singers", "特拉普一家的故事", "Maria Augusta Trapp", "玛丽亚·奥古斯塔·特拉普", "1949", pd=False, lang="en",
       aliases=["The Sound of Music", "音乐之声", "von Trapp"]),
    BK("at-maikaefer", "Fly Away Home", "金龟子飞吧", "Christine Nöstlinger", "克里斯蒂娜·涅斯特林格", "1973", pd=False, title_orig="Maikäfer flieg!",
       aliases=["Maikäfer flieg", "Maikaefer flieg"]),
    BK("at-hungerkuenstler", "A Hunger Artist", "饥饿艺术家", "Franz Kafka", "卡夫卡", "1924", title_orig="Ein Hungerkünstler", src=DEWS("Ein Hungerkünstler (1924)"),
       aliases=["Ein Hungerkünstler", "Josefine die Sängerin"]),
    BK("at-about-the-house", "About the House", "关于寓所", "W. H. Auden", "奥登", "1965", pd=False, lang="en", aliases=["Thanksgiving for a Habitat"]),
    BK("at-stirring-times", "Stirring Times in Austria", "奥地利的动荡时期", "Mark Twain", "马克·吐温", "1898", lang="en", src=ws.url("en", "Stirring Times in Austria")),
    BK("at-time-of-gifts", "A Time of Gifts", "时光的礼物", "Patrick Leigh Fermor", "帕特里克·利·弗莫尔", "1977", pd=False, lang="en"),
    BK("at-die-wand", "The Wall", "隐墙", "Marlen Haushofer", "玛尔伦·豪斯霍费尔", "1963", pd=False, title_orig="Die Wand", aliases=["Die Wand"]),
    BK("at-hare-amber-eyes", "The Hare with Amber Eyes", "琥珀眼睛的兔子", "Edmund de Waal", "埃德蒙·德瓦尔", "2010", pd=False, lang="en", aliases=["Ephrussi", "netsuke"]),
    BK("at-heiligenstadt-testament", "The Heiligenstadt Testament", "海利根施塔特遗书", "Ludwig van Beethoven", "贝多芬", "1802", title_orig="Heiligenstädter Testament",
       src=DEWS("Heiligenstädter Testament"), aliases=["Heiligenstädter Testament", "Heiligenstaedter Testament"]),
    BK("at-felder-leben", "From My Life", "我的一生", "Franz Michael Felder", "弗朗茨·米夏埃尔·费尔德", "1904", title_orig="Aus meinem Leben", aliases=["Aus meinem Leben", "Bregenzerwald"]),
]
NIB, FEAST, ROSE = "the-nibelungenlied", "fr-moveable-feast", "the-name-of-the-rose"

# ============================== places ==============================
places = [
    # ---- Vienna ----
    ORIG("at-brigittenau", "Brigitta Chapel, Brigittenau", "布里吉特瑙 · 布里吉塔小教堂",
         "The Poor Fiddler opens at the Brigitta fair, the great popular festival once held every July in the meadows around this chapel, when all Vienna streamed across the Danube canal. In the crowd the narrator notices an old street musician playing from a music stand, terribly and with rapture",
         "《可怜的乐师》开头写的是布里吉塔庙会：从前每年七月，这座小教堂周围的草地上举行盛大的平民节日，全维也纳的人都涌过多瑙运河来赶会。叙述者就是在人群里注意到一位老街头乐师的，他对着谱架拉琴，拉得很糟，却十分陶醉"),
    PIL("at-theater-an-der-wien", "Theater an der Wien", "维也纳河畔剧院",
        "Nestroy's Lumpazivagabundus was first given here on 11 April 1833, with Nestroy himself as the drunken cobbler Knieriem; it made him the favourite of the Viennese popular stage",
        "内斯特罗伊的《恶精灵卢姆帕齐》1833 年 4 月 11 日在这里首演，他自己演那个醉醺醺的鞋匠克尼里姆；这出戏让他成了维也纳民间戏剧舞台上最受欢迎的人", ["at-lumpazivagabundus"]),
    ORIG("at-prater", "The Prater", "普拉特公园",
         "Vienna's great park between the Danube and the canal, with its fairground at the city end. Lieutenant Gustl, insulted by a baker after a concert, wanders here all night sure that he must shoot himself at dawn. In The Piano Teacher Erika Kohut comes to the Prater meadows after dark to watch couples",
         "多瑙河和运河之间的大公园，靠城的一头是游乐场。古斯特少尉听完音乐会被一个面包师侮辱，在这里游荡了一整夜，认定自己天亮就得开枪自尽。《钢琴教师》里，埃里卡·科胡特天黑后来到普拉特的草地上偷看情侣"),
    ORIG("at-augartenbruecke", "Augarten Bridge", "奥花园桥",
         "The first of the ten dialogues of La Ronde is set 'late in the evening, at the Augarten Bridge': a prostitute stops a soldier on his way back to barracks and takes him down to the bank of the Danube canal",
         "《轮舞》十场对话的第一场，地点就写着“深夜，奥花园桥边”：一个妓女拦住正要回兵营的士兵，把他带到多瑙运河的河岸下"),
    ORIG("at-altes-akh", "Old General Hospital (Altes AKH)", "旧总医院",
         "The hospital founded by Joseph II in 1784, where Schnitzler trained and worked as a young doctor; it is now a university campus. Fridolin, the doctor of Dream Story, lives in the Josefstadt close by, works at the polyclinic, and his search ends the next night in the mortuary of the pathological institute",
         "约瑟夫二世 1784 年创办的医院，施尼茨勒年轻时在这里实习、行医；现在是大学校园。《梦的故事》里的医生弗里多林就住在旁边的约瑟夫城，在门诊部上班，第二天夜里，他的追寻在病理研究所的停尸间结束"),
    PIL("at-cafe-central", "Café Central", "中央咖啡馆",
        "Peter Altenberg gave this coffee-house as his postal address and wrote many of his prose sketches at its tables; a life-size figure of him still sits near the door",
        "彼得·阿尔滕贝格把这家咖啡馆当作自己的通信地址，许多散文小品就是在这里的桌子上写的；门口附近至今坐着一尊和他真人一样大的塑像", ["at-wie-ich-es-sehe"]),
    ORIG("at-sirk-ecke", "Sirk-Ecke (corner of Kärntner Straße and the Ring)", "西尔克街角（克恩滕大街与环城大道路口）",
         "The corner by the Opera, where the Hotel Bristol stands, was the meeting point of the Ringstraße promenade. The prologue and every act of The Last Days of Mankind open here, with newsboys shouting the latest extra edition through the strolling crowd",
         "歌剧院旁的这个街角（布里斯托尔饭店所在的地方）曾是环城大道上散步人群的会合点。《人类的末日》的序幕和每一幕都从这里开始：报童在闲逛的人群中叫卖最新的号外"),
    PIL("at-rasumofskygasse", "Rasumofskygasse", "拉祖莫夫斯基巷",
        "Robert Musil's Vienna flat was at Rasumofskygasse 20, and most of The Man Without Qualities was written there; the plaque on the house gives the years 1921 to 1938, part of which he spent in Berlin",
        "罗伯特·穆齐尔在维也纳的住所是拉祖莫夫斯基巷 20 号，《没有个性的人》大部分是在这里写的；楼上纪念牌写的年份是 1921 至 1938 年，其间他也在柏林住过一段", ["at-mann-ohne-eigenschaften"]),
    ORIG("at-morzinplatz", "Morzinplatz (site of the Hotel Metropole)", "莫尔钦广场（大都会饭店旧址）",
         "The Hotel Metropole on this square was the Vienna headquarters of the Gestapo from 1938; it was destroyed in 1945 and a memorial stands in its place. In Chess Story Dr B. is held in one of its rooms in total isolation, and keeps his mind alive with a stolen book of chess games",
         "这个广场上的大都会饭店从 1938 年起是盖世太保在维也纳的总部，1945 年被毁，原址立了纪念碑。《象棋的故事》里，B 博士被关在饭店的一个房间里，与世隔绝，靠偷来的一本棋谱才没有精神崩溃"),
    ORIG("at-schoenbrunn", "Schönbrunn Palace", "美泉宫",
         "The summer palace of the Habsburgs, where Franz Joseph was born and died. In The Radetzky March the old Emperor lies dying here in the rain of November 1916 while District Captain von Trotta waits in the park. The zoo in its grounds, at Hietzing, is the one the two students of Setting Free the Bears plan to break open",
         "哈布斯堡家族的夏宫，弗朗茨·约瑟夫生在这里，也死在这里。《拉德茨基进行曲》里，1916 年 11 月的雨中，老皇帝在这里弥留，地方长官冯·特罗塔在花园里等着。宫苑里位于希青区的动物园，就是《放熊归山》里两个大学生打算砸开的那一座"),
    ORIG("at-kapuzinergruft", "Imperial Crypt (Kapuzinergruft)", "皇家墓穴（嘉布遣会教堂地下墓室）",
         "The burial vault of the Habsburgs under the Capuchin church on the Neuer Markt. Roth's last novel ends in March 1938: Franz Ferdinand Trotta walks out of a café as the Nazis take over and comes to the crypt where his emperors lie, not knowing where else to go",
         "新市场嘉布遣会教堂地下的哈布斯堡家族墓室。罗特最后一部长篇小说结束在 1938 年 3 月：纳粹接管时，弗朗茨·费迪南德·特罗塔走出咖啡馆，来到埋着他的皇帝们的墓穴前，不知道还能去哪里"),
    ORIG("at-strudlhofstiege", "Strudlhofstiege", "斯特鲁德霍夫阶梯",
         "The Art Nouveau flight of steps of 1910 between Boltzmanngasse and Liechtensteinstraße in the Alsergrund. Doderer made it the centre of his novel of Vienna in 1910–11 and 1923–25, the place where the paths of all its characters cross; a poem of his is on a plaque at the foot",
         "阿尔瑟格伦德区玻尔兹曼巷和列支敦士登大街之间的新艺术风格阶梯，1910 年建成。多德勒尔把它写成了小说的中心——小说讲 1910 至 1911 年和 1923 至 1925 年的维也纳，所有人物的路都在这里交叉；阶梯脚下的纪念牌上刻着他的一首诗"),
    PROTO("at-dorotheum", "Dorotheum", "多罗特姆拍卖行",
          "Vienna's state pawnshop and auction house is, thinly disguised, the 'Theresianum' of Auto-da-Fé, where the dwarf Fischerle and his gang wait to fleece the scholar Kien as he buys back the books that people come to pawn",
          "维也纳这家国营当铺兼拍卖行略加改头换面，就是《迷惘》里的“特蕾西亚当铺”：学者基恩在那里把人们拿来典当的书一本本赎下，侏儒菲舍尔勒和他的同伙就守在那里骗他的钱"),
    ORIG("at-ungargasse", "Ungargasse", "匈牙利巷",
         "The narrator of Malina lives at Ungargasse 6 with Malina, and her lover Ivan at number 9, across the street. She calls the few hundred metres between them her 'Ungargassenland', the only country she wants",
         "《马利纳》的叙述者和马利纳住在匈牙利巷 6 号，她的情人伊万住在街对面的 9 号。两处之间几百米的地方，她叫它“匈牙利巷之国”，那是她唯一想要的国度"),
    ORIG("at-heldenplatz", "Heldenplatz", "英雄广场",
         "On 15 March 1938 Hitler announced the annexation of Austria from the balcony of the Hofburg to a cheering crowd on this square. In Bernhard's last play, set in 1988, Professor Schuster has thrown himself from his flat overlooking it, and his widow still hears the shouting from fifty years before",
         "1938 年 3 月 15 日，希特勒在霍夫堡的阳台上向广场上欢呼的人群宣布吞并奥地利。伯恩哈德最后一部剧作写的是 1988 年：舒斯特教授从正对广场的家里跳楼自尽，他的遗孀至今还听得见五十年前的呼喊声"),
    ORIG("at-steinhof", "Steinhof and the Baumgartner Höhe", "施泰因霍夫与鲍姆加特纳高地",
         "On this hill at the edge of the Vienna Woods, crowned by Otto Wagner's church, stand the psychiatric hospital of Steinhof and, beside it, the lung clinic. Wittgenstein's Nephew begins in 1967 with the narrator in the Hermann pavilion of the one and his friend Paul Wittgenstein two hundred metres away in the Ludwig pavilion of the other",
         "维也纳森林边缘的这座山上，顶上是奥托·瓦格纳设计的教堂，山上有施泰因霍夫精神病院，旁边是肺病疗养院。《维特根斯坦的侄子》从 1967 年写起：叙述者住在肺病院的“赫尔曼”病楼，他的朋友保罗·维特根斯坦就在两百米外精神病院的“路德维希”病楼"),
    ORIG("at-berggasse", "Berggasse 19 (Sigmund Freud Museum)", "贝格巷 19 号（弗洛伊德博物馆）",
         "Freud lived and saw his patients here from 1891 until he was driven out in June 1938; The Interpretation of Dreams was written in this flat. In The Tobacconist the apprentice Franz carries cigars to the old man the neighbourhood calls the 'idiot doctor' and asks his advice about love",
         "弗洛伊德从 1891 年起在这里居住、接诊，直到 1938 年 6 月被迫离开；《梦的解析》就是在这套房子里写的。《读报纸的人》里，学徒弗朗茨给这位被街坊叫做“傻子大夫”的老人送雪茄，向他请教爱情的事", book_ids=["at-traumdeutung"]),
    ORIG("at-riesenrad", "Riesenrad (the Great Wheel)", "普拉特大摩天轮",
         "The giant Ferris wheel of 1897 in the Prater. In The Third Man Rollo Martins meets Harry Lime here in occupied Vienna, and at the top of the wheel Lime looks down at the people below and asks whether Martins would really feel pity if one of those dots stopped moving",
         "普拉特公园里 1897 年建成的大摩天轮。《第三人》里，罗洛·马丁斯在被占领的维也纳同哈里·莱姆在这里见面；转到最高处时，莱姆望着底下的人，问马丁斯：要是其中一个小点不动了，你真会觉得可怜吗"),
    ORIG("at-zentralfriedhof", "Vienna Central Cemetery", "维也纳中央公墓",
         "The Third Man begins and ends here: Martins arrives in Vienna just in time for Harry Lime's funeral in the frozen February ground, and comes back for the second, real one. Beethoven, Schubert, Brahms and Schnitzler are buried in the cemetery",
         "《第三人》在这里开始，也在这里结束：马丁斯到维也纳时，正赶上哈里·莱姆在二月的冻土里下葬；后来他又回来参加第二次、真正的葬礼。贝多芬、舒伯特、勃拉姆斯和施尼茨勒都葬在这座公墓"),
    ORIG("at-neuwaldegg", "Neuwaldegg", "新瓦尔德格",
         "The villa quarter at the western edge of Vienna. In Fly Away Home, Nöstlinger's memoir of spring 1945, the eight-year-old Christel and her family, bombed out of their flat, move into an abandoned villa here, and Russian soldiers are quartered in the house; she makes friends with their cook, Cohn",
         "维也纳西郊的别墅区。《金龟子飞吧》是涅斯特林格对 1945 年春天的回忆：八岁的克里斯特尔一家被炸得无家可归，搬进这里一座没人住的别墅，苏军士兵也住了进来；她和他们的炊事兵科恩成了朋友"),
    ORIG("at-parlament", "Parliament, Vienna", "维也纳议会大厦",
         "Mark Twain lived in Vienna from 1897 to 1899 and sat in the gallery of the Reichsrat through the riotous sittings of autumn 1897, including Dr Lecher's twelve-hour speech and the night the police were marched in to drag deputies out",
         "马克·吐温 1897 至 1899 年住在维也纳，1897 年秋天帝国议会吵翻天的那些会议，他都坐在旁听席上：莱歇尔博士十二小时的演说，还有警察开进来把议员拖出去的那一夜"),
    ORIG("at-palais-ephrussi", "Palais Ephrussi", "埃弗吕西宫",
         "The Ringstraße palace built for the banker Ignace von Ephrussi in the 1870s. The Hare with Amber Eyes follows a collection of 264 Japanese netsuke that arrived here from Paris as a wedding present in 1899 and was saved in 1938, when the Gestapo took the house, by the maid Anna, who hid the carvings in her mattress",
         "19 世纪 70 年代为银行家伊格纳茨·冯·埃弗吕西修建的环城大道宫殿。《琥珀眼睛的兔子》追踪的是 264 件日本根付：1899 年它们作为结婚礼物从巴黎来到这里；1938 年盖世太保占了这座房子，女仆安娜把这些小雕件藏进自己的床垫，保了下来"),
    ORIG("at-heiligenstadt", "House of the Heiligenstadt Testament (Probusgasse 6)", "海利根施塔特遗书之家（普罗布斯巷 6 号）",
         "Beethoven spent the summer of 1802 in the wine village of Heiligenstadt on his doctor's advice, and in October wrote to his brothers the letter, found only after his death, in which he confesses his deafness and his thoughts of suicide. Tradition names this house, now a museum, as the place",
         "1802 年夏天，贝多芬遵医嘱住在酿酒小村海利根施塔特；十月，他给两个弟弟写下一封信，坦白自己耳聋，也说到自杀的念头，这封信到他死后才被发现。相传信就是在这座房子里写的，现在这里是博物馆"),
    PIL("at-rodaun", "Hofmannsthal-Schlössl, Rodaun", "罗道恩 · 霍夫曼斯塔尔小宫",
        "Hofmannsthal moved into this small baroque house on the edge of Vienna when he married in 1901 and lived here until his death in 1929. The Chandos Letter, Everyman and the librettos for Richard Strauss were written here",
        "1901 年结婚后，霍夫曼斯塔尔搬进维也纳城边这座巴洛克小楼，一直住到 1929 年去世。《钱多斯勋爵的信》《耶德曼》和为理查·施特劳斯写的歌剧脚本都是在这里写的", ["at-chandos", "at-jedermann"]),
    # ---- Lower Austria ----
    ORIG("at-poechlarn", "Pöchlarn (Bechelaren)", "珀希拉恩（贝希拉恩）",
         "The Bechelaren of the Nibelungenlied, seat of Margrave Rüdiger. Kriemhild rests here on her way down the Danube to marry Etzel; years later the Burgundians are feasted here for days on their way to his court, and Giselher is betrothed to Rüdiger's daughter",
         "《尼伯龙根之歌》里的贝希拉恩，边疆伯爵吕狄格的驻地。克里姆希尔特沿多瑙河而下去嫁埃策尔时在这里歇脚；多年以后，勃艮第人去埃策尔的宫廷，途中在这里被款待了好几天，吉赛尔赫还同吕狄格的女儿订了婚"),
    ORIG("at-tulln", "Tulln (Nibelungen Fountain)", "图尔恩（尼伯龙根喷泉）",
         "In the Nibelungenlied it is at Tulln on the Danube that King Etzel, with a retinue of many peoples, rides out to meet his bride Kriemhild before the wedding in Vienna. A bronze fountain on the riverbank shows the meeting",
         "《尼伯龙根之歌》里，埃策尔王带着由许多民族组成的随从，就是在多瑙河畔的图尔恩迎接新娘克里姆希尔特的，然后去维也纳举行婚礼。河岸上的青铜喷泉表现的就是这次相见"),
    PIL("at-zeiselmauer", "Zeiselmauer", "蔡瑟尔毛尔",
        "The only document that names Walther von der Vogelweide in his lifetime was written here: on 12 November 1203 the travel accounts of Bishop Wolfger of Passau record five shillings given 'to the singer Walther de Vogelweide for a fur coat'",
        "瓦尔特·冯·德·福格威德生前唯一提到他的文献就写于此地：1203 年 11 月 12 日，帕绍主教沃尔夫格的旅行账簿记着，给“歌手瓦尔特·德·福格威德”五先令，买一件皮袍", ["at-walther-songs"]),
    ORIG("at-melk", "Melk Abbey", "梅尔克修道院",
         "The Benedictine abbey on its rock above the Danube. The narrator of The Name of the Rose is Adso of Melk, who writes down as an old monk here what he saw as a novice in Italy. Patrick Leigh Fermor, walking to Constantinople in 1934, was shown through its baroque library and church",
         "多瑙河畔山岩上的本笃会修道院。《玫瑰的名字》的叙述者是梅尔克的阿德索，他年老时在这里写下自己做见习修士时在意大利的见闻。1934 年徒步去君士坦丁堡的帕特里克·利·弗莫尔，被人领着参观了这里的巴洛克图书馆和教堂"),
    ORIG("at-duernstein", "Dürnstein and the Wachau", "迪恩施泰因与瓦豪河谷",
         "The stretch of the Danube between Melk and Krems, with its vineyards and castle ruins. Tales from the Vienna Woods begins and ends 'out in the Wachau', in front of a cottage at the foot of a ruined castle, where Alfred's mother and grandmother live and where Marianne's child is put out to nurse",
         "梅尔克和克雷姆斯之间的一段多瑙河，两岸是葡萄园和城堡废墟。《维也纳森林的故事》开头和结尾都在“外面的瓦豪”，一座城堡废墟脚下的小屋前；阿尔弗雷德的母亲和祖母住在那里，玛丽安娜的孩子也寄养在那里"),
    PIL("at-kierling", "Kafka's last rooms, Kierling", "基尔林 · 卡夫卡去世的房间",
        "Kafka, unable to speak or swallow from tuberculosis of the larynx, spent his last weeks in Dr Hoffmann's small sanatorium in this house and died here on 3 June 1924. On his deathbed he corrected the proofs of A Hunger Artist. There is a memorial room",
        "患喉结核、已经不能说话也不能吞咽的卡夫卡，最后几个星期住在这座房子里霍夫曼医生的小疗养院，1924 年 6 月 3 日在这里去世。临终前他还在校对《饥饿艺术家》的清样。这里设有纪念室", ["at-hungerkuenstler"]),
    PIL("at-weidling", "Weidling cemetery", "魏德林墓地",
        "Lenau, who had lost his mind in 1844, died in the asylum at Oberdöbling in 1850 and was buried, as he had wished, in the churchyard of this valley in the Vienna Woods",
        "莱瑙 1844 年精神失常，1850 年死在上德布灵的疯人院，按他生前的愿望葬在维也纳森林这个山谷里的墓地", ["at-lenau-poems"]),
    ORIG("at-kirchstetten", "Kirchstetten", "基希施泰滕",
         "W. H. Auden bought a farmhouse in this village in 1957, the first home he ever owned, and spent every summer here until his death in 1973. The cycle 'Thanksgiving for a Habitat' in About the House goes through it room by room. He is buried in the churchyard",
         "1957 年奥登在这个村子买下一座农舍，这是他一生中第一处属于自己的房子；此后每年夏天他都在这里度过，直到 1973 年去世。《关于寓所》里的组诗《感恩一处居所》一间屋子一间屋子地写这座房子。他就葬在村里教堂的墓地"),
    PIL("at-gutenstein", "Gutenstein", "古滕施泰因",
        "Ferdinand Raimund loved this valley, bought a country house nearby, at Pernitz, in 1834, and is buried in the hillside cemetery of Gutenstein; he shot himself in 1836, believing he had been bitten by a rabid dog",
        "费迪南德·莱蒙德喜爱这个山谷，1834 年在附近的佩尼茨买下一处乡间住宅，死后葬在古滕施泰因的山坡墓地；1836 年，他以为自己被疯狗咬了，开枪自尽", ["at-alpenkoenig"]),
    PIL("at-harmannsdorf", "Schloss Harmannsdorf", "哈曼斯多夫城堡",
        "Bertha von Suttner lived at her husband's family castle from 1885 to 1902, and here wrote Lay Down Your Arms!, the novel that made her the voice of the peace movement and, in 1905, the first woman to receive the Nobel Peace Prize",
        "贝尔塔·冯·苏特纳 1885 至 1902 年住在丈夫家族的这座城堡里，在这里写下《放下武器！》；这部小说让她成了和平运动的代言人，1905 年她成为第一位获得诺贝尔和平奖的女性", ["at-waffen-nieder"]),
    ORIG("at-semmering", "Semmering (Südbahnhotel)", "塞默灵（南方铁路饭店）",
         "The mountain resort two hours from Vienna, with its grand hotels above the railway. Burning Secret is set in one of them: a bored young baron befriends a twelve-year-old boy in order to reach the boy's mother, and the child slowly understands that he is being used",
         "离维也纳两小时车程的山间度假地，铁路上方立着一座座大饭店。《灼人的秘密》就发生在其中一家：一个无聊的年轻男爵为了接近一位母亲，先同她十二岁的儿子交朋友，孩子慢慢明白自己被利用了"),
    ORIG("at-kalte-rinne", "Kalte Rinne viaduct, Semmering railway", "塞默灵铁路 · 冷沟高架桥",
         "The Semmering line, the first mountain railway in Europe, was built between 1848 and 1854 by thousands of labourers. Saar's The Stonebreakers, among the first stories in German about industrial workers, is set among the people who broke stone for it",
         "塞默灵铁路是欧洲第一条山地铁路，1848 至 1854 年由成千上万的工人修成。萨尔的《凿石工》是德语文学里最早写产业工人的小说之一，写的就是为这条铁路凿石头的人"),
    ORIG("at-duernkrut", "Dürnkrut (battlefield on the Marchfeld)", "迪恩克鲁特（马希费尔德古战场）",
         "On 26 August 1278 Rudolf of Habsburg defeated and killed King Ottokar II of Bohemia between Dürnkrut and Jedenspeigen, and the Habsburgs' six centuries in Austria began. The last act of Grillparzer's tragedy is this battle",
         "1278 年 8 月 26 日，哈布斯堡的鲁道夫在迪恩克鲁特和耶登施派根之间打败并杀死了波希米亚国王奥托卡二世，哈布斯堡家族在奥地利六百年的统治由此开始。格里尔帕策这部悲剧的最后一幕写的就是这场战役"),
    # ---- Upper Austria ----
    PIL("at-stifterhaus", "StifterHaus, Linz", "林茨 · 施蒂弗特故居",
        "Adalbert Stifter lived in a flat in this house on the Danube from 1848, working as inspector of schools, and wrote Indian Summer and the final version of Rock Crystal here. He died in it in 1868",
        "阿达尔贝特·施蒂弗特从 1848 年起住在多瑙河边这座楼里的一套房间，担任学校督学；《晚夏》和《水晶》的定稿都是在这里写的。1868 年他在这里去世", ["at-nachsommer", "at-bergkristall"]),
    PROTO("at-hallstatt", "Hallstatt", "哈尔施塔特",
          "Stifter visited Hallstatt in 1845, and the sight of two children caught by a storm, together with the geographer Simony's picture of a glacier cave, gave him Rock Crystal; the mountain village of Gschaid and the glacier above it are generally taken to be drawn from here",
          "1845 年施蒂弗特来到哈尔施塔特，看见两个被暴风雨困住的孩子，又看到地理学家西莫尼画的冰川洞穴，由此有了《水晶》；小说里的山村格沙伊德和村子上方的冰川，一般认为写的就是这里"),
    ORIG("at-wolfsegg", "Schloss Wolfsegg", "沃尔夫斯埃格城堡",
         "The castle above the Hausruck is the Wolfsegg of Extinction. Franz-Josef Murau, living in Rome, receives a telegram that his parents and brother are dead, comes back to the estate he hates for the funeral, and decides what to do with his inheritance",
         "豪斯鲁克山上的这座城堡就是《消除》里的沃尔夫斯埃格。住在罗马的弗朗茨-约瑟夫·穆劳接到电报，得知父母和哥哥都死了，回到他憎恨的这处庄园参加葬礼，并决定怎样处置自己继承的遗产"),
    PIL("at-ohlsdorf", "Thomas Bernhard's house, Obernathal (Ohlsdorf)", "奥尔斯多夫 · 伯恩哈德故居",
        "In 1965 Bernhard bought a ruined four-sided farmhouse here with literary prize money, rebuilt it himself, and wrote in it for the rest of his life. It is kept as he left it",
        "1965 年，伯恩哈德用文学奖的奖金买下这里一座破败的四合院式农庄，亲手修复，此后一直在这里写作。房子保持着他离开时的样子", ["at-ausloeschung", "at-wittgensteins-neffe", "at-heldenplatz", "at-ursache"]),
    ORIG("at-attersee", "Nußdorf am Attersee", "阿特湖畔努斯多夫",
         "The lakeside village in the Salzkammergut where The Tobacconist begins: in the summer of 1937 the seventeen-year-old Franz Huchel is sent from his mother's cottage here to Vienna, to be apprenticed in a tobacconist's shop",
         "萨尔茨卡默古特的湖边村子，《读报纸的人》从这里开始：1937 年夏天，十七岁的弗朗茨·胡赫尔离开母亲在这里的小屋，被送到维也纳一家烟草报刊店当学徒"),
    PIL("at-molln", "Molln (Effertsbach valley)", "莫尔恩（埃弗茨巴赫山谷）",
        "Marlen Haushofer was born in 1920 in the forester's house at Effertsbach, in the wooded hills above Molln. The hunting lodge and alpine pasture of The Wall, where a woman finds herself cut off from the world by an invisible barrier, are drawn from the valleys of her childhood",
        "玛尔伦·豪斯霍费尔 1920 年生在莫尔恩山上林区埃弗茨巴赫的护林人小屋。《隐墙》里，一个女人被一堵看不见的墙同世界隔开；书中的猎屋和高山牧场，取材于她童年的这些山谷", ["at-die-wand"]),
    FILM("at-mondsee", "Mondsee Basilica", "蒙德湖教堂",
         "the wedding of Maria and Captain von Trapp. The real couple were married in 1927 in the church of Nonnberg Abbey in Salzburg; the film used the larger, brighter church at Mondsee",
         "玛丽亚和冯·特拉普上校的婚礼。现实中两人 1927 年是在萨尔茨堡农贝格修道院的教堂结的婚；电影用了蒙德湖这座更大、更明亮的教堂", ["at-trapp-family"]),
    # ---- Salzburg ----
    ORIG("at-mirabell", "Mirabell Gardens, Salzburg", "萨尔茨堡 · 米拉贝尔花园",
         "The baroque garden of the Mirabell palace, with its fountains and its marble gods and dwarfs. Trakl, who grew up a few streets away, set one of his best-known early poems here at evening",
         "米拉贝尔宫的巴洛克花园，有喷泉，有大理石的神像和矮人像。特拉克尔就在几条街外长大，他早期最有名的诗之一写的就是这里的傍晚"),
    ORIG("at-st-peter-friedhof", "St Peter's Cemetery, Salzburg", "萨尔茨堡 · 圣彼得墓地",
         "The oldest churchyard in Salzburg, pressed against the rock wall of the Mönchsberg, with catacombs cut into the cliff. Trakl wrote a poem about it in 1909, one of the earliest in which his own voice is heard",
         "萨尔茨堡最古老的墓地，紧贴着僧侣山的岩壁，崖上凿有地下墓室。特拉克尔 1909 年写过一首关于它的诗，是最早听得出他自己声音的作品之一", book_ids=["at-trakl-poems"]),
    PIL("at-trakl-haus", "Trakl's birthplace, Waagplatz", "瓦格广场 · 特拉克尔出生的房子",
        "Georg Trakl was born in this house on 3 February 1887, the son of an ironmonger, and grew up in the old town; it is now a memorial and research centre. The square opens onto the Residenzplatz with its fountain of horses",
        "1887 年 2 月 3 日，格奥尔格·特拉克尔生在这座房子里，父亲是五金商；他在老城长大。这里现在是纪念馆和研究中心。广场通向主教宫广场，那里有一座骏马喷泉", ["at-trakl-poems"]),
    ORIG("at-domplatz", "Cathedral Square, Salzburg", "萨尔茨堡 · 大教堂广场",
         "On 22 August 1920 Max Reinhardt staged Hofmannsthal's Everyman on a wooden platform in front of the cathedral, and the Salzburg Festival began. The play of the rich man summoned by Death has been given here almost every summer since, with the calls of 'Jedermann!' coming from the towers around the square",
         "1920 年 8 月 22 日，马克斯·赖因哈特在大教堂前的木台上排演了霍夫曼斯塔尔的《耶德曼》，萨尔茨堡音乐节由此开始。这出讲富人被死神召唤的戏，此后几乎每年夏天都在这里上演，“耶德曼！”的呼喊声从广场四周的塔楼上传来"),
    PIL("at-kapuzinerberg", "Paschinger Schlössl, Kapuzinerberg", "嘉布遣山 · 帕辛格小宫",
        "Stefan Zweig bought this old hunting lodge on the hill above Salzburg during the First World War and lived in it from 1919 to 1934, the years of his world fame. He left for London after the police searched the house for weapons; The World of Yesterday looks back on it from exile",
        "斯蒂芬·茨威格在第一次世界大战期间买下萨尔茨堡城上山坡的这座旧猎宫，1919 至 1934 年住在这里，那是他名满天下的年月。警察来搜查武器之后，他去了伦敦；《昨日的世界》是他在流亡中对这一切的回望", ["at-welt-von-gestern"]),
    ORIG("at-nonnberg", "Nonnberg Abbey, Salzburg", "萨尔茨堡 · 农贝格修道院",
         "The Benedictine convent above the old town where Maria Kutschera was a postulant when, in 1926, the abbess sent her to be governess to one of the children of the widowed Captain von Trapp. She married him in the abbey church the next year",
         "老城上方的本笃会女修道院。1926 年，玛丽亚·库切拉还是这里的望会生，院长派她去给丧偶的冯·特拉普上校的一个孩子当家庭教师。第二年，她就在修道院的教堂里嫁给了上校"),
    ORIG("at-moenchsberg", "Mönchsberg, Salzburg", "萨尔茨堡 · 僧侣山",
         "The rock ridge that shuts in the old town. In An Indication of the Cause Bernhard remembers his boarding-school years in Salzburg from 1943: the tunnels in the rock where the town sheltered from the bombs, and the Mönchsberg as the place from which the desperate threw themselves",
         "把老城围在里面的岩石山脊。《原因》里，伯恩哈德回忆 1943 年起在萨尔茨堡寄宿学校的岁月：全城人躲避轰炸的山岩隧洞，还有，僧侣山是绝望的人往下跳的地方"),
    FILM("at-leopoldskron", "Schloss Leopoldskron", "利奥波德斯克龙宫",
         "the lake and garden terrace of the Trapp villa, where the children and Maria fall out of the boat; the scenes were shot on the lake here, in the grounds of the palace and of the property next to it. The rococo palace once belonged to Max Reinhardt, founder of the Salzburg Festival; the family's real house was at Aigen, on the other side of the town",
         "特拉普家别墅的湖和花园露台，孩子们和玛丽亚从船上掉进水里的那场戏，就是在这片湖上、在宫苑和相邻的庄园里拍的。这座洛可可宫殿曾属于萨尔茨堡音乐节的创办人马克斯·赖因哈特；特拉普一家真正的住宅在城另一头的艾根", ["at-trapp-family"]),
    # ---- Styria ----
    ORIG("at-alpl", "Rosegger's birthplace, Alpl (Kluppeneggerhof)", "阿尔普尔 · 罗泽格出生的农舍",
         "Peter Rosegger was born in 1843 in this smoke-blackened mountain farmhouse, the eldest of seven children of poor peasants. The Forest Home is his book of childhood stories from it: the first railway he ever saw, the walk through the snow to Christmas mass",
         "1843 年，彼得·罗泽格生在这座被烟熏黑的山间农舍里，是穷苦农民家七个孩子中的老大。《林中故乡》写的就是他在这里的童年故事：平生第一次看见火车，踏着雪去望圣诞子夜弥撒"),
    PIL("at-krieglach", "Rosegger's house, Krieglach", "克里格拉赫 · 罗泽格故居",
        "With the success of his books Rosegger built a country house in the valley below his native hills in 1877; he spent his summers here and died in it in 1918. It is a museum, with his study as he left it",
        "书畅销之后，罗泽格 1877 年在故乡山下的河谷里盖了一座乡间住宅；他每年夏天住在这里，1918 年在这里去世。现在是博物馆，书房保持着原样", ["at-waldheimat"]),
    # ---- Carinthia ----
    ORIG("at-griffen", "Griffen", "格里芬",
         "Peter Handke was born in this market town in southern Carinthia in 1942. A Sorrow Beyond Dreams, written within weeks of his mother's suicide here in November 1971, tells her life: a Slovene carpenter's daughter who wanted to learn something and was allowed nothing",
         "1942 年彼得·汉德克生在克恩顿南部的这个集镇。1971 年 11 月母亲在这里自杀，几周之内他就写出了《无欲的悲歌》，讲述她的一生：一个斯洛文尼亚木匠的女儿，想学点什么，却什么都不被允许"),
    ORIG("at-klagenfurt", "Klagenfurt (Neuer Platz)", "克拉根福（新广场）",
         "Ingeborg Bachmann was born in Klagenfurt in 1926 and grew up here. 'Youth in an Austrian Town', the story that opens The Thirtieth Year, goes back through the town of her childhood: the rented houses, the school, the day the soldiers marched in, the bombs",
         "英格博格·巴赫曼 1926 年生在克拉根福，在这里长大。《三十岁》的开篇故事《一座奥地利城市里的少年时代》重新走过她童年的这座城：租来的房子，学校，军队开进来的那一天，轰炸"),
    PIL("at-musil-haus", "Robert Musil Literature Museum, Klagenfurt", "克拉根福 · 罗伯特·穆齐尔文学博物馆",
        "Robert Musil was born in this house by the station on 6 November 1880, the son of an engineer; the family left Klagenfurt within a year. It is now a museum for Musil and for the Carinthian writers Ingeborg Bachmann and Christine Lavant",
        "1880 年 11 月 6 日，罗伯特·穆齐尔生在火车站旁的这座房子里，父亲是工程师；不到一年全家就搬离了克拉根福。现在这里是博物馆，纪念穆齐尔，也纪念克恩顿作家英格博格·巴赫曼和克里斯蒂娜·拉万特", ["at-mann-ohne-eigenschaften"]),
    # ---- Tyrol ----
    ORIG("at-hofkirche", "Hofkirche, Innsbruck", "因斯布鲁克 · 宫廷教堂",
         "The church built for the empty tomb of Emperor Maximilian I, ringed by twenty-eight larger-than-life bronze figures of his ancestors and heroes; Andreas Hofer, the leader of the Tyrolean rising of 1809, is buried in the left aisle. Heine, passing through in 1828, lingers among the 'black men' and tells Hofer's story",
         "为皇帝马克西米利安一世的空墓修建的教堂，墓的四周立着二十八尊比真人还大的青铜像，都是他的祖先和他敬仰的英雄；1809 年蒂罗尔起义的领袖安德烈亚斯·霍费尔葬在左侧廊。1828 年海涅路过这里，在这些“黑色的人”中间流连，还讲了霍费尔的故事"),
    PIL("at-muehlau", "Mühlau, Innsbruck", "因斯布鲁克 · 米劳",
        "Ludwig von Ficker, who published Trakl's poems in his journal Der Brenner, lived in Mühlau, and Trakl was often his guest. Trakl died in a military hospital in Kraków in November 1914; in 1925 Ficker had his remains brought to the cemetery here",
        "路德维希·冯·菲克尔在自己办的杂志《燃烧者》上发表特拉克尔的诗，他住在米劳，特拉克尔常在他家做客。1914 年 11 月特拉克尔死在克拉科夫的军医院；1925 年，菲克尔把他的遗骨迁到了这里的墓地", ["at-trakl-poems"]),
    # ---- Vorarlberg ----
    ORIG("at-schruns", "Schruns", "施伦斯",
         "Hemingway spent the winters of 1924–25 and 1925–26 in this village in the Montafon with his wife Hadley and their small son, living cheaply at the Hotel Taube, skiing, and rewriting The Sun Also Rises. The last chapter of A Moveable Feast is about those winters",
         "1924 至 1925 年和 1925 至 1926 年的两个冬天，海明威带着妻子哈德莉和年幼的儿子住在蒙塔丰山谷的这个村子，在鸽子旅馆过着花钱不多的日子，滑雪，重写《太阳照常升起》。《流动的盛宴》最后一章写的就是这两个冬天"),
    ORIG("at-wolfurt", "Wolfurt", "沃尔富特",
         "Arno Geiger's home village near Bregenz. The Old King in His Exile is about his father August, who was born here, was sent to the front at eighteen, came back from Soviet captivity and never wanted to leave again, and who in old age, with Alzheimer's, keeps asking to be taken home while sitting in the house he built",
         "阿尔诺·盖格在布雷根茨附近的家乡。《流放的老国王》写他的父亲奥古斯特：生在这里，十八岁被送上前线，从苏军战俘营回来以后再也不想离开；晚年患了阿尔茨海默病，坐在自己亲手盖的房子里，却一再要人带他回家"),
    PROTO("at-meschach", "Meschach, above Götzis", "格齐斯山上的梅沙赫",
          "Robert Schneider grew up in this hamlet in the hills above the Rhine valley and has gone on living in Götzis. It is the model for Eschberg, the inbred mountain village of Brother of Sleep, where the musical genius Elias Alder is born in 1803 and never heard by the world",
          "罗伯特·施奈德在莱茵河谷上方山间的这个小村长大，后来也一直住在格齐斯。它是《睡眠兄弟》里埃施贝格的原型：一个近亲通婚的山村，音乐天才埃利亚斯·阿尔德 1803 年生在那里，世人从未听到过他"),
    PIL("at-schoppernau", "Franz Michael Felder Museum, Schoppernau", "肖珀瑙 · 弗朗茨·米夏埃尔·费尔德博物馆",
        "Felder was born in 1839 in this village at the head of the Bregenzerwald, half-blind from a botched operation, and remained a farmer here all his life while writing novels and founding a cheese-trading cooperative and a cattle insurance society. He wrote From My Life just before his death at twenty-nine",
        "1839 年费尔德生在布雷根茨森林尽头的这个村子，因为一次失败的手术几乎失明；他一辈子在这里务农，同时写小说，还办了奶酪销售合作社和牲畜保险社。二十九岁去世前不久，他写下了《我的一生》", ["at-felder-leben"]),
]

# ============================== lines ==============================
gustl = raw("Lieutenant Gustl", "Das ist nicht schlecht, jetzt bin ich gar im Prater", "es ist ganz schön …")
traum = raw("Traumnovelle", "Auf der Straße mußte er den Pelz öffnen.", "daß er zu spät gekommen war.")
beeth = raw("Heiligenstädter Testament", "Komm, wann du willst", "Heiglnstadt am 6ten october 1802")
assert beeth.count("\n") == 2, beeth

lines = [
    Q("at-trakl-1", "at-trakl-poems", "at-mirabell", "'Musik im Mirabell', stanzas 1–2", "《米拉贝尔的音乐》第一、二节", "German", "Musik im Mirabell",
      raw("Musik im Mirabell", "Ein Brunnen singt.", "ins Dunkel gleiten."), ["den alten Garten"],
      "A fountain sings. The clouds stand\nin the clear blue, white and tender.\nUnhurried, silent people walk\nat evening through the old garden.\nThe marble of the ancestors has greyed.\nA flight of birds trails into the distance.\nA faun with dead eyes gazes\nafter shadows gliding into the dark.",
      ["the old garden"],
      "喷泉在歌唱。云朵停在\n澄澈的蓝天里，洁白，轻柔。\n傍晚，人们从容而安静地\n走过古老的花园。\n先祖的大理石像已经灰暗。\n一行飞鸟掠向远方。\n一尊牧神用死去的眼睛\n望着滑入黑暗的影子。",
      ["古老的花园"]),
    Q("at-trakl-2", "at-trakl-poems", "at-trakl-haus", "'Die schöne Stadt', stanzas 1–3", "《美丽的城市》第一至三节", "German", "Die schöne Stadt",
      raw("Die schöne Stadt", "Alte Plätze sonnig schweigen.", "dort am Brunnen."), ["Alte Plätze", "Rösser tauchen aus dem Brunnen"],
      "Old squares keep their sunny silence.\nSpun deep into blue and gold,\ngentle nuns hurry as in a dream\nunder the silence of sultry beeches.\nOut of the brown-lit churches\ngaze death's pure images,\nthe fair escutcheons of great princes.\nCrowns shimmer in the churches.\nHorses rise out of the fountain.\nClaws of blossom threaten from the trees.\nBoys, confused with dreams, play\nsoftly there by the fountain in the evening.",
      ["Old squares", "Horses rise out of the fountain"],
      "古老的广场在阳光里沉默。\n深深织进蓝色与金色之中，\n温柔的修女如在梦里匆匆走过，\n头上是闷热的山毛榉的沉默。\n从棕色微明的教堂里，\n死亡纯净的画像向外张望，\n还有大公们华美的盾徽。\n王冠在教堂里闪烁。\n骏马从喷泉中跃出。\n花的利爪在树上作势。\n男孩们做梦做得恍惚，\n傍晚在喷泉边轻声玩耍。",
      ["古老的广场", "骏马从喷泉中跃出"]),
    Q("at-gustl-1", "at-leutnant-gustl", "at-prater", "The night in the Prater", "普拉特之夜", "German", "Lieutenant Gustl", gustl, ["im Prater"],
      "Well, this is a fine thing, now I'm actually in the Prater … in the middle of the night … I'd never have thought this morning that I'd be going for a walk in the Prater tonight … What must that policeman over there be thinking? … Well, let's just keep walking … it's quite nice …",
      ["in the Prater"],
      "这可真不赖，我居然走到普拉特来了……深更半夜的……今天早上我怎么也想不到，今晚会到普拉特来散步……那边那个警察会怎么想？……算了，接着走吧……这儿挺好的……",
      ["普拉特"]),
    Q("at-traum-1", "at-traumnovelle", "at-altes-akh", "Chapter 2, opening", "第二章开头", "German", "Traumnovelle", traum, ["Josefstadt nahe dem Allgemeinen Krankenhaus"],
      "Out in the street he had to open his fur coat. A thaw had suddenly set in, the snow on the pavement had almost melted away, and a breath of the coming spring was in the air. From Fridolin's home in the Josefstadt, near the General Hospital, it was barely a quarter of an hour to the Schreyvogelgasse; and so Fridolin was soon climbing the badly lit, winding stairs of the old house to the second floor and pulling the bell; but before the old-fashioned ring could be heard he noticed that the door was only ajar; he went through the unlit hall into the living room and saw at once that he had come too late.",
      ["the Josefstadt, near the General Hospital"],
      "到了街上，他不得不敞开皮大衣。天突然回暖，人行道上的雪差不多化尽了，空气里飘着一丝将至的春意。弗里多林的家在约瑟夫城，离总医院不远，从那里到施赖福格尔巷不过一刻钟的路；不一会儿，他就沿着那座老房子昏暗曲折的楼梯上到三楼，拉了门铃；可是没等那老式的铃声响起来，他就发现门只是虚掩着；他穿过没点灯的前厅走进起居室，一眼就看出自己来晚了。",
      ["约瑟夫城，离总医院不远"]),
    Q("at-beethoven-1", "at-heiligenstadt-testament", "at-heiligenstadt", "The close of the letter of 6 October 1802", "1802 年 10 月 6 日信的结尾", "German", "Heiligenstädter Testament",
      beeth, ["Heiglnstadt"],
      "Come when you will, I go to meet you bravely – farewell, and do not quite forget me in death; I have deserved it of you, for in my life I often thought of you, of how to make you happy; be so –\nLudwig van Beethoven\nHeiligenstadt, 6 October 1802",
      ["Heiligenstadt"],
      "你什么时候来都行，我会勇敢地迎上去——永别了，我死后别把我全忘了；这是我应得的，因为我活着的时候常常想着你们，想让你们幸福；愿你们幸福——\n路德维希·凡·贝多芬\n海利根施塔特，1802 年 10 月 6 日",
      ["海利根施塔特"], " (Beethoven's own spelling; he is speaking to death, then to his brothers)"),
    Q("at-twain-1", "at-stirring-times", "at-parlament", "Part II", "第二部分", "English", "Stirring Times in Austria",
      raw("Stirring Times in Austria", "It was a good place for theatrical effects.", "Its plan is that of an opera-house."), ["Senate House"], "", [],
      "这是个适合制造戏剧效果的地方。我想，没有哪一座议会大厅像这一座这样匀称，装饰得这样富丽、这样招摇。它的格局就是一座歌剧院。",
      ["议会大厅"], original=True),

    # ---------- scene notes ----------
    S("at-nib-s1", NIB, "at-poechlarn", "Adventures 21 and 27", "第二十一歌、第二十七歌",
      "Margrave Rüdiger of Bechelaren, Etzel's vassal, has wooed Kriemhild for his king and sworn to avenge any wrong done to her. He lodges her at his castle on the Danube on her way east; thirteen years later he entertains her brothers there for four days and loads them with gifts, before his oath to her forces him to fight them.",
      "贝希拉恩的边疆伯爵吕狄格是埃策尔的封臣，他替国王向克里姆希尔特求婚，并发誓为她报一切冤仇。她东去途中，他在多瑙河边的城堡里接待了她；十三年后，他又在那里款待她的兄弟们四天，送了许多礼物——后来，对她立下的誓言却逼得他不得不同他们交战。",
      ["Bechelaren"], ["贝希拉恩"], W + "Nibelungenlied"),
    S("at-nib-s2", NIB, "at-tulln", "Adventure 22", "第二十二歌",
      "Etzel rides up the Danube to meet Kriemhild at Tulln with a train of Russians and Greeks, Poles and Wallachians, Danes and Thuringians. She kisses the king and twelve of his princes; then they go on to Vienna, where the wedding is held at Whitsun and lasts seventeen days.",
      "埃策尔沿多瑙河而上，到图尔恩迎接克里姆希尔特，随从里有罗斯人和希腊人，波兰人和瓦拉几亚人，丹麦人和图林根人。她吻了国王和他的十二位王公；然后他们前往维也纳，婚礼在圣灵降临节举行，持续了十七天。",
      ["Tulln", "Vienna"], ["图尔恩", "维也纳"], W + "Nibelungenlied"),
    S("at-spielmann-s1", "at-arme-spielmann", "at-brigittenau", "Throughout", "全篇",
      "Following the old fiddler home from the Brigitta fair, the narrator hears his story: the slow-witted son of a powerful councillor, he failed at school and in the office, loved Barbara, a grocer's daughter, whose song is the only tune he can play, was cheated of his inheritance and lost her to a butcher. He dies after carrying his neighbours' children and belongings out of the great flood; Barbara keeps his violin.",
      "叙述者从布里吉塔庙会一路跟着老乐师回家，听他讲了自己的身世：他是一位有权势的宫廷顾问的儿子，脑子迟钝，书读不成，差事也当不好；他爱上杂货商的女儿巴尔巴拉，她唱的那支歌是他唯一拉得出的曲子；遗产被人骗走，她嫁给了一个屠户。大洪水时，他把邻居的孩子和家当一趟趟背出来，自己却死了；巴尔巴拉留下了他的小提琴。",
      ["the Brigitta fair"], ["布里吉塔庙会"], "https://de.wikipedia.org/wiki/Der_arme_Spielmann"),
    S("at-ottokar-s1", "at-koenig-ottokar", "at-duernkrut", "Act 5", "第五幕",
      "Ottokar of Bohemia, at the height of his power, casts off his wife, loses the imperial election to the plain Count Rudolf of Habsburg, and has to kneel to him for his lands. Goaded by his new queen, he breaks the peace. Before the battle on the Marchfeld he stands at the deathbed of the wife he wronged and sees what he has been; then he is cut down, and Rudolf invests his own sons with Austria over the corpse.",
      "波希米亚的奥托卡在权势的顶点休掉了妻子，在皇帝选举中败给朴素的哈布斯堡伯爵鲁道夫，还得为保住领地向他下跪。在新王后的挑唆下，他撕毁了和约。马希费尔德决战之前，他站在被自己亏待的前妻的灵床前，看清了自己的一生；随后他被砍倒，鲁道夫就在他的尸体旁把奥地利封给了自己的儿子。",
      ["the Marchfeld"], ["马希费尔德"], W + "K%C3%B6nig_Ottokars_Gl%C3%BCck_und_Ende"),
    S("at-bergkristall-s1", "at-bergkristall", "at-hallstatt", "Throughout", "全篇",
      "On Christmas Eve the shoemaker's children, Konrad and little Sanna, walk over the pass from their grandmother's in the next valley. Snow begins to fall, the red post that marks the way is gone, and they climb by mistake onto the glacier. They look into a cave of blue ice, are frightened by it, and spend the night awake under a roof of boulders, hearing the ice crack, and are found on Christmas morning by the men of both villages.",
      "圣诞前夜，鞋匠的两个孩子康拉德和小珊娜从邻谷的外婆家翻山回家。下起了雪，标路的红柱子不见了，他们误上了冰川。他们见到一个蓝色的冰洞，吓得退了出来，在乱石搭成的石棚下熬了一夜没睡，耳边是冰层开裂的声音；圣诞节早晨，两个村子的男人们找到了他们。",
      ["the glacier"], ["冰川"], W + "Rock_Crystal_(novella)"),
    S("at-steinklopfer-s1", "at-steinklopfer", "at-kalte-rinne", "Throughout", "全篇",
      "Georg, a discharged soldier weak from fever, breaks stone on the Semmering line under a brutal overseer and loves Tertschka, the overseer's stepdaughter, who is worked like a beast. When the overseer attacks them Georg strikes him dead. The court, moved by their story, lets him off lightly, and the two end as keepers of a signal hut beside the finished railway.",
      "格奥尔格是个退伍兵，发过热病，身子虚弱，在塞默灵铁路工地上给一个凶暴的工头凿石头；他爱上了工头的继女特尔奇卡，她被当牲口一样使唤。工头对他们动手，格奥尔格失手把他打死了。法庭被两人的遭遇打动，从轻发落；后来他们在修好的铁路边守一间信号房。",
      ["the Semmering line"], ["塞默灵铁路"], W + "Ferdinand_von_Saar"),
    S("at-waldheimat-s1", "at-waldheimat", "at-alpl", "Throughout", "全书",
      "The forest farmer's boy tells of the world as it looked from Alpl: walking with his godfather to see the new steam train come out of the Semmering tunnel, and their terror at it; carrying the Christmas dinner home through the night; the poor relation, the pedlars, the school kept by a wandering teacher; and the weakness that made him a tailor's apprentice instead of a farmer.",
      "林农的儿子讲述从阿尔普尔看出去的世界：跟着教父走去看新通车的蒸汽火车钻出塞默灵隧道，两人吓得魂不附体；连夜把圣诞节的饭菜背回家；穷亲戚，货郎，流浪教师办的学堂；还有，因为身子骨弱，他没当成农民，去做了裁缝学徒。",
      ["Alpl"], ["阿尔普尔"], W + "Peter_Rosegger"),
    S("at-reigen-s1", "at-reigen", "at-augartenbruecke", "Scene 1", "第一场",
      "Ten couples, ten encounters, each with a line of dashes in the middle: the prostitute and the soldier, the soldier and the parlourmaid, the parlourmaid and the young gentleman, and on through the married lady, her husband, the sweet girl, the poet, the actress and the count, who ends where it began, with the prostitute. Printed privately in 1900, the play caused riots and a trial when it was staged in Berlin and Vienna in 1920–21.",
      "十对男女，十次相遇，每场中间都有一行破折号：妓女和士兵，士兵和女仆，女仆和少爷，接着是少妇、她的丈夫、甜姐儿、诗人、女演员和伯爵，最后伯爵又回到开头的妓女那里。剧本 1900 年只是私下印行；1920 至 1921 年在柏林和维也纳公演时引发了骚乱和一场官司。",
      ["the prostitute and the soldier"], ["妓女和士兵"], W + "La_Ronde_(play)"),
    S("at-jedermann-s1", "at-jedermann", "at-domplatz", "Throughout", "全剧",
      "God sends Death to fetch Everyman, a rich man in the middle of a banquet. He begs for a companion on the journey: his friend, his cousins and his money all refuse. Only his Works, too weak to stand, and her sister Faith go with him to the grave, and the Devil arrives too late to claim him.",
      "上帝派死神去召回耶德曼——一个正在大摆宴席的富人。他央求有人陪他上路：朋友、表亲和他的钱财统统拒绝。只有虚弱得站不起来的“善行”和她的姐妹“信仰”陪他走进坟墓，魔鬼赶来索要他时已经晚了。",
      ["Everyman"], ["耶德曼"], W + "Jedermann_(play)"),
    S("at-kraus-s1", "at-letzten-tage", "at-sirk-ecke", "Prologue and Act 1, scene 1", "序幕与第一幕第一场",
      "More than two hundred scenes, most of them cut from what was actually said and printed between 1914 and 1918: officers flirting on the corner while they discuss the casualty lists, the war reporter Alice Schalek touring the trenches, the patriotic Subscriber, the Grumbler who answers them. Kraus said the play was meant for a theatre on Mars; it would take ten evenings to perform.",
      "两百多场戏，大部分是从 1914 至 1918 年间人们真正说过、报上真正登过的话里剪下来的：军官们在街角一边谈伤亡名单一边调情，战地女记者爱丽丝·沙莱克巡视战壕，爱国的“订报人”，还有回敬他们的“抱怨者”。克劳斯说，这出戏是给火星上的剧院写的；演完要十个晚上。",
      ["on the corner"], ["街角"], W + "The_Last_Days_of_Mankind"),
    S("at-musil-s1", "at-mann-ohne-eigenschaften", "at-rasumofskygasse", "Book 1", "第一卷",
      "On a fine August day in 1913 Ulrich, thirty-two, a mathematician who has decided to take a year's leave from his life, is living in a small rococo house in Vienna. He is drawn into the Parallel Campaign, a committee searching for a great idea with which to celebrate the Emperor's seventieth jubilee in 1918, in the empire Musil calls Kakania.",
      "1913 年八月一个晴朗的日子，三十二岁的数学家乌尔里希决定给自己的人生放一年假，住在维也纳一座洛可可小楼里。他被卷进“平行行动”——一个委员会，要为 1918 年皇帝登基七十周年找出一个伟大的理念；穆齐尔把这个帝国叫做“卡卡尼亚”。",
      ["Vienna", "Kakania"], ["维也纳", "卡卡尼亚"], W + "The_Man_Without_Qualities"),
    S("at-welt-s1", "at-welt-von-gestern", "at-kapuzinerberg", "'Homecoming to Austria' and after", "“重返奥地利”及以后各章",
      "Zweig describes the 'golden age of security' of his Viennese childhood, the Europe of friends he built before 1914, and the house on the Kapuzinerberg where Romain Rolland, Thomas Mann, Joyce and Toscanini came to visit, from whose terrace he could see across the border to the mountain at Berchtesgaden where the man lived who would destroy it all.",
      "茨威格写他在维也纳度过的童年，那个“太平的黄金时代”；写 1914 年以前他结交的满欧洲的朋友；也写嘉布遣山上的那座房子，罗曼·罗兰、托马斯·曼、乔伊斯和托斯卡尼尼都来做过客，从露台上能望见国境线那边贝希特斯加登的山，山上住着后来毁掉这一切的那个人。",
      ["the Kapuzinerberg"], ["嘉布遣山"], W + "The_World_of_Yesterday"),
    S("at-schach-s1", "at-schachnovelle", "at-morzinplatz", "Dr B.'s story", "B 博士的讲述",
      "On a liner to Buenos Aires a stranger holds the world chess champion to a draw. He is Dr B., a Viennese lawyer whom the Gestapo kept for months in a bare hotel room with nothing to read or look at, to break him. He stole a book from a coat pocket; it was a collection of master games. He played them all in his head, then played against himself until his mind split.",
      "开往布宜诺斯艾利斯的邮轮上，一个陌生人同国际象棋世界冠军下成了和棋。他是 B 博士，维也纳的律师；盖世太保把他在饭店一间空荡荡的房间里关了好几个月，没有任何东西可读可看，想以此摧垮他。他从一件大衣口袋里偷到一本书，是一部名局棋谱。他在脑子里把这些棋全下了一遍，然后自己同自己下，直到精神分裂。",
      ["hotel room"], ["饭店"], W + "The_Royal_Game"),
    S("at-geheimnis-s1", "at-brennendes-geheimnis", "at-semmering", "Throughout", "全篇",
      "Edgar, twelve and convalescent, is overjoyed when a baron at the hotel treats him as a friend, and bewildered when the two grown-ups begin to send him to bed early. He spies on them, attacks the baron in the corridor at night, runs away by train to his grandmother in Baden, and, when his father asks what happened, keeps his mother's secret.",
      "十二岁的埃德加正在病后休养，饭店里的一位男爵把他当朋友，他高兴极了；等到两个大人开始早早打发他上床，他又糊涂了。他偷偷盯着他们，夜里在走廊上扑向男爵，然后坐火车逃到巴登的祖母家；父亲问起出了什么事，他替母亲守住了秘密。",
      ["the hotel"], ["饭店"], W + "Burning_Secret"),
    S("at-radetzky-s1", "at-radetzkymarsch", "at-schoenbrunn", "Part 3", "第三部",
      "A Slovene lieutenant saves the young Emperor's life at Solferino and is made Baron Trotta. His son becomes a district captain who hears the Radetzky March played under his balcony every Sunday; his grandson Carl Joseph, a weak officer in a garrison on the Russian border, is killed in 1914 fetching water for his men. The old district captain is granted an audience with the Emperor, and dies on the day of the Emperor's funeral.",
      "一个斯洛文尼亚裔少尉在索尔费里诺救了年轻皇帝的命，被封为特罗塔男爵。他的儿子当了地方长官，每个星期天都听着阳台下奏响《拉德茨基进行曲》；孙子卡尔·约瑟夫是个软弱的军官，驻守在俄国边境，1914 年为士兵们打水时阵亡。老地方长官曾获准觐见皇帝，后来死在皇帝下葬的那一天。",
      ["the Emperor"], ["皇帝"], W + "Radetzky_March_(novel)"),
    S("at-gruft-s1", "at-kapuzinergruft", "at-kapuzinergruft", "Final chapter", "最后一章",
      "Franz Ferdinand Trotta, a cousin of the Trottas of The Radetzky March, tells how he idled through the last spring of the monarchy, went to war, came back from Siberia to a Vienna in which he had no place, mortgaged the family house and lost his wife. On the night of the Anschluss he is left alone in his café and walks to the crypt, where a Capuchin friar turns him away.",
      "弗朗茨·费迪南德·特罗塔是《拉德茨基进行曲》里特罗塔家的远亲。他讲自己怎样在帝国最后一个春天里游手好闲，怎样上了战场，从西伯利亚回到一个再没有他位置的维也纳，抵押了祖宅，失去了妻子。德奥合并的那一夜，咖啡馆里只剩下他一个人；他走到皇家墓穴前，一位嘉布遣会修士把他挡在了门外。",
      ["the crypt"], ["皇家墓穴"], W + "The_Emperor%27s_Tomb"),
    S("at-wienerwald-s1", "at-wiener-wald", "at-duernstein", "Part 1, scene 1, and the last scenes", "第一部第一场与结尾几场",
      "In a quiet street in Vienna's eighth district Marianne, the toy-shop owner's daughter, is to marry the butcher Oskar. At the engagement picnic by the Danube she runs off with the idler Alfred. He leaves her; their baby is sent to his grandmother in the Wachau, who lets it die of a chill. At the end Oskar gets his way, as he promised: 'You will not escape my love.'",
      "在维也纳第八区一条安静的街上，玩具店老板的女儿玛丽安娜要嫁给屠户奥斯卡。在多瑙河边的订婚野餐上，她跟着游手好闲的阿尔弗雷德跑了。他后来抛弃了她；两人的婴儿被送到瓦豪他祖母那里，祖母故意让孩子着凉死去。到头来，奥斯卡如愿以偿，就像他说过的那样：你逃不出我的爱。",
      ["the Wachau"], ["瓦豪"], W + "Tales_from_the_Vienna_Woods_(play)"),
    S("at-strudlhof-s1", "at-strudlhofstiege", "at-strudlhofstiege", "Throughout", "全书",
      "The novel, subtitled 'Melzer and the Depth of the Years', moves between the summers of 1911 and 1925. Major Melzer, a former officer now in the tobacco monopoly, slowly becomes a human being; around him go the Stangeler family, the twins Editha and Mimi Pastré with their smuggling scheme, and Mary K., who on 21 September 1925 loses a leg under a tram while Melzer saves her life.",
      "小说的副标题是“梅尔策与岁月的深处”，在 1911 年和 1925 年的夏天之间来回穿行。梅尔策少校当过军官，如今在烟草专卖局做事，慢慢地成为一个“人”；他周围是施坦格勒一家，是搞走私勾当的孪生姐妹埃迪塔和咪咪·帕斯特雷，还有玛丽·K——1925 年 9 月 21 日，她被电车轧断一条腿，梅尔策救了她的命。",
      ["Melzer"], ["梅尔策"], W + "The_Strudlhof_Steps"),
    S("at-blendung-s1", "at-blendung", "at-dorotheum", "Part 2, 'Headless World'", "第二部“没有头脑的世界”",
      "Peter Kien, the greatest sinologist of his day, lives for his library of twenty-five thousand volumes and marries his housekeeper Therese because she handles a book with gloves. She drives him out. In the underworld of the city he falls in with the hunchbacked dwarf Fischerle, who dreams of becoming world chess champion and sets his friends to pawning the same parcels of books to Kien again and again.",
      "彼得·基恩是当代最伟大的汉学家，为自己两万五千册的藏书而活；他娶了女管家特蕾莎，只因为她戴着手套拿书。她把他赶出了家门。在城市的底层，他同驼背侏儒菲舍尔勒混到一起；此人梦想当国际象棋世界冠军，叫同伙把同几包书一遍遍拿到当铺，让基恩一次次赎下。",
      ["pawning"], ["当铺"], W + "Auto-da-F%C3%A9_(novel)"),
    S("at-malina-s1", "at-malina", "at-ungargasse", "Throughout", "全书",
      "A woman writer, never named, lives between two men: Ivan, whom she loves and waits for by the telephone, and Malina, the calm civil servant at the Army Museum with whom she shares the flat. In the middle part her father murders her again and again in dreams. At the end she disappears into a crack in the wall, and the book's last sentence calls it murder.",
      "一位始终没有名字的女作家生活在两个男人之间：一个是伊万，她爱他，守着电话等他；一个是马利纳，军事博物馆里那位沉静的公务员，同她住在一套房子里。小说中间一部分，她的父亲在梦里一次又一次杀死她。结尾，她消失在墙上的一道裂缝里，全书最后一句话把这叫做谋杀。",
      ["Ivan", "Malina"], ["伊万", "马利纳"], W + "Malina_(novel)"),
    S("at-dreissig-s1", "at-dreissigste-jahr", "at-klagenfurt", "'Youth in an Austrian Town'", "《一座奥地利城市里的少年时代》",
      "Someone comes back to a town in the south and, by a tree burning with autumn colour, remembers the children who lived there: moved from one rented house to another, taught not to whistle and not to ask, watching the wall of the cemetery, the aeroplanes, the soldiers, then digging trenches and carrying the dead. The town is not named.",
      "有人回到南方的一座城市，在一棵秋色如火的树旁想起曾经住在这里的孩子们：从一处租来的房子搬到另一处，被教导不许吹口哨、不许多问，望着墓地的墙、飞机、士兵，后来去挖战壕、抬死人。这座城市没有写出名字。",
      ["a town in the south"], ["南方的一座城市"], W + "Ingeborg_Bachmann"),
    S("at-heldenplatz-s1", "at-heldenplatz", "at-heldenplatz", "Throughout", "全剧",
      "Josef Schuster, a Jewish professor of mathematics, came back from Oxford to Vienna after the war; in March 1988, days before he was to return to England, he jumped from the window. After the funeral his brother Robert tells the family that there are more Nazis in Vienna now than in 1938. At the table the widow hears the roar from the square rise until she falls face down among the plates.",
      "犹太裔数学教授约瑟夫·舒斯特战后从牛津回到维也纳；1988 年 3 月，就在他准备重返英国的前几天，他从窗口跳了下去。葬礼之后，他的弟弟罗伯特对家人说，如今维也纳的纳粹比 1938 年还多。饭桌上，遗孀听见广场上的吼声越来越响，最后一头栽倒在盘子中间。",
      ["the square"], ["广场"], W + "Heldenplatz_(play)"),
    S("at-neffe-s1", "at-wittgensteins-neffe", "at-steinhof", "Opening", "开头",
      "The narrator, operated on for a lung tumour, and Paul Wittgenstein, nephew of the philosopher, mad and locked up, lie two hundred metres apart on the same hill, and neither can cross to the other. From there the book tells twelve years of friendship: their walks, their opera evenings, their loathing of prizes, and how the narrator avoided Paul as he lay dying.",
      "叙述者做了肺部肿瘤手术，哲学家的侄子保罗·维特根斯坦疯了、被关着，两人躺在同一座山上，相隔两百米，谁也过不去。书由此讲起十二年的友谊：一起散步，一起听歌剧，一起厌恶各种奖，也讲保罗临终时叙述者怎样躲着他。",
      ["the same hill"], ["同一座山"], W + "Wittgenstein%27s_Nephew"),
    S("at-ausloeschung-s1", "at-ausloeschung", "at-wolfsegg", "Part 2, 'The Will'", "第二部“遗嘱”",
      "In Rome Murau tells his pupil Gambetti everything he detests in Wolfsegg: the hunters, the gardeners he loved, the five libraries kept locked, the Children's Villa where his parents hid Nazi officials after the war. At the funeral the same men stand at the grave. He gives the whole estate, as it stands, to the Jewish community of Vienna.",
      "在罗马，穆劳把沃尔夫斯埃格让他厌恶的一切都讲给学生甘贝蒂听：那些猎人，他喜欢的园丁，五间一直锁着的图书室，还有“儿童别墅”——战后他父母在那里藏过纳粹官员。葬礼上，还是那批人站在墓旁。他把整座庄园原封不动地赠给了维也纳的犹太社团。",
      ["Wolfsegg"], ["沃尔夫斯埃格"], W + "Extinction_(Bernhard_novel)"),
    S("at-ursache-s1", "at-ursache", "at-moenchsberg", "'Grünkranz'", "“格林克兰茨”一章",
      "At thirteen Bernhard is put into a National Socialist boarding school in the Schrannengasse, practises the violin in the shoe closet and thinks of hanging himself there. The bombers come; he sees a child's severed hand in the rubble of the Gstättengasse. After the war the same school is Catholic, the portrait of Hitler replaced by a crucifix on the same nail, and nothing else has changed.",
      "十三岁的伯恩哈德被送进施兰嫩巷的一所纳粹寄宿学校，在放鞋的小屋里练小提琴，也在那里想过上吊。轰炸机来了；他在格施泰滕巷的瓦砾里看见一只孩子的断手。战后，同一所学校成了天主教学校，希特勒像换成了十字架，挂在同一颗钉子上，别的什么都没变。",
      ["Schrannengasse"], ["施兰嫩巷"], "https://de.wikipedia.org/wiki/Die_Ursache._Eine_Andeutung"),
    S("at-handke-s1", "at-wunschloses-unglueck", "at-griffen", "Throughout", "全书",
      "A newspaper notice: a housewife of fifty-one has killed herself with an overdose of sleeping pills. Her son sets down her life in the formulas such lives were told in: the girl who begged to be allowed to learn, the brief happiness with a German soldier, the marriage to another, the poverty, the reading that came late, the headaches, the letters of farewell.",
      "报上的一则消息：一位五十一岁的家庭妇女服用过量安眠药自杀。她的儿子用人们讲述这类人生时惯用的套话写下她的一生：那个央求着要读书的女孩，同一个德国士兵短暂的幸福，嫁给另一个人，贫穷，迟来的阅读，头痛，诀别的信。",
      ["a housewife of fifty-one"], ["五十一岁的家庭妇女"], W + "A_Sorrow_Beyond_Dreams"),
    S("at-klavier-s1", "at-klavierspielerin", "at-prater", "Part 1", "第一部",
      "Erika Kohut, a piano teacher at the Vienna Conservatory in her late thirties, shares a bed with her mother, who has trained her for genius since birth. In secret she visits peep shows, and at night walks out to the Prater meadows to crouch in the dark near couples. Her pupil Walter Klemmer sets out to conquer her; she answers with a letter of instructions.",
      "埃里卡·科胡特年近四十，是维也纳音乐学院的钢琴教师，同母亲睡一张床；母亲从她出生起就照着“天才”来训练她。她偷偷去看窥视秀，夜里走到普拉特的草地上，在黑暗中蹲在情侣近旁。学生瓦尔特·克雷默尔一心要征服她；她的回答是一封写满指令的信。",
      ["the Prater meadows"], ["普拉特的草地"], W + "The_Piano_Teacher_(Jelinek_novel)"),
    S("at-trafikant-s1", "at-trafikant", "at-attersee", "Opening", "开头",
      "A thunderstorm over the lake kills the rich man who has been keeping Franz's mother, and so she writes to an old acquaintance in Vienna, the one-legged tobacconist Otto Trsnjek. Franz takes the train with a suitcase and a head full of nothing, and from Vienna sends his mother postcards, which she answers from the cottage by the water.",
      "湖上的一场雷雨劈死了一直供养弗朗茨母亲的那个有钱人，于是她给维也纳的一位旧相识写了信——独腿的烟草店主奥托·特尔斯涅克。弗朗茨提着一只箱子坐上火车，脑子里空空的；到了维也纳，他给母亲寄明信片，母亲在湖边的小屋里给他回信。",
      ["the lake"], ["湖"], W + "The_Tobacconist"),
    S("at-trafikant-s2", "at-trafikant", "at-berggasse", "Throughout", "全书",
      "Among the shop's customers is Professor Freud. Franz, lovesick for a Bohemian variety girl called Anezka, waylays him on the Berggasse with cigars and gets, instead of a cure, the advice to write down his dreams. After the Anschluss the tobacconist is taken by the Gestapo; Franz sees the old man once more before the Freuds leave for London, and then does one brave, hopeless thing.",
      "店里的顾客中有弗洛伊德教授。弗朗茨害了相思病，爱上一个名叫阿内日卡的波希米亚杂耍女郎；他带着雪茄在贝格巷拦住教授，没有得到药方，得到的建议是把梦记下来。德奥合并之后，店主被盖世太保抓走；弗洛伊德一家动身去伦敦之前，弗朗茨又见了老人一面，然后做了一件勇敢而无望的事。",
      ["the Berggasse"], ["贝格巷"], W + "The_Tobacconist"),
    S("at-geiger-s1", "at-alte-koenig", "at-wolfurt", "Throughout", "全书",
      "For years the family took the father's slips for stubbornness. Now the son learns to follow him into his world instead of correcting him, and writes down what he says: that nothing in the house is his, that he must go home now, and, of his own life, that it has gone well enough, taken all in all. Between these scenes he tells the story of a village boy, the prisoner of war who nearly died of dysentery, the municipal clerk.",
      "多年来，家里人把父亲的种种失误当成固执。如今儿子学着跟随他走进他的世界，不再纠正他，并记下他说的话：这屋里没有一样东西是他的，他现在得回家了；说到自己的一生，他说，总的来看还算不错。在这些场景之间，儿子讲述了一个乡村少年、一个差点死于痢疾的战俘、一个乡镇办事员的故事。",
      ["home"], ["回家"], W + "Arno_Geiger"),
    S("at-schneider-s1", "at-schlafes-bruder", "at-meschach", "Throughout", "全书",
      "Elias Alder is born in Eschberg with hearing so fine that at five he hears the whole universe sound and his eyes turn yellow. He teaches himself the organ in the village church, loves his cousin Elsbeth without ever telling her, wins an improvisation contest in the cathedral of Feldberg, and at twenty-two decides to stay awake until he dies, since whoever sleeps does not love.",
      "埃利亚斯·阿尔德生在埃施贝格，听觉灵敏得出奇，五岁那年他听见了整个宇宙的声响，眼睛变成了黄色。他在村里的教堂自学管风琴，爱着表妹埃尔斯贝特却从未开口，在费尔德贝格大教堂的即兴演奏比赛中夺魁；二十二岁时，他决定不再睡觉，直到死去，因为睡着的人不在爱。",
      ["Eschberg"], ["埃施贝格"], W + "Brother_of_Sleep"),
    S("at-heine-s1", "at-reisebilder", "at-hofkirche", "The Innsbruck chapters", "因斯布鲁克几章",
      "Travelling south from Munich in the rain, Heine stops at Innsbruck. He mocks the Tyroleans for their loyalty to an emperor who abandoned them, then stands in the Hofkirche among the bronze men and women around Maximilian's tomb, and tells how Andreas Hofer was betrayed, taken to Mantua and shot.",
      "海涅冒雨从慕尼黑南下，在因斯布鲁克停留。他嘲笑蒂罗尔人对一位抛弃了他们的皇帝那样忠心，随后站在宫廷教堂里，置身于马克西米利安墓四周的青铜男女像中间，讲述安德烈亚斯·霍费尔怎样被出卖、押往曼托瓦枪决。",
      ["the Hofkirche"], ["宫廷教堂"], "https://de.wikipedia.org/wiki/Hofkirche_(Innsbruck)"),
    S("at-third-s1", "at-third-man", "at-zentralfriedhof", "Chapters 1–2 and the end", "第一、二章与结尾",
      "Rollo Martins, a writer of cheap westerns, comes to four-power Vienna just after the war at the invitation of his school friend Harry Lime and finds him just buried, knocked down by a car. Two men carried the body, say the witnesses; a neighbour saw a third. The police officer who tells the story explains what Lime was selling: stolen penicillin, watered down.",
      "罗洛·马丁斯是个写廉价西部小说的作家，应老同学哈里·莱姆之邀来到战后四国共管的维也纳，却发现莱姆刚刚下葬，说是被汽车撞死的。证人说，抬尸体的是两个人；一位邻居却看见了第三个。讲述这个故事的警官解释了莱姆卖的是什么：偷来的、掺了水的青霉素。",
      ["just buried"], ["刚刚下葬"], "https://de.wikipedia.org/wiki/Der_dritte_Mann_(Roman)"),
    S("at-third-s2", "at-third-man", "at-riesenrad", "The meeting on the Great Wheel", "大摩天轮上的会面",
      "Lime, alive, agrees to meet Martins at the Great Wheel in the Russian zone. Alone in a swaying car high over the wrecked Prater, he is as charming as ever: he explains that nobody thinks in terms of human beings any more, offers Martins a share, and for a moment has his hand on the door. Martins goes to the police, and the hunt ends in the sewers.",
      "还活着的莱姆答应在苏占区的大摩天轮同马丁斯见面。两人单独待在一节摇晃的车厢里，高高悬在残破的普拉特上空；他还是那么有魅力：他解释说，如今谁也不再把人当人来考虑了，还提出分给马丁斯一份，有一刻他的手就搭在车门上。马丁斯去找了警察，追捕在下水道里结束。",
      ["the Great Wheel"], ["大摩天轮"], "https://de.wikipedia.org/wiki/Der_dritte_Mann_(Roman)"),
    S("at-bears-s1", "at-setting-free-bears", "at-schoenbrunn", "Parts 1 and 3", "第一、三部",
      "In the spring of 1967 two Vienna students, Siggy Javotnik and Hannes Graff, buy an old motorcycle and ride out into the country. Siggy goes back to spend a night hidden in the Hietzing Zoo, keeping a notebook of the watchman's cruelties and of his own family's story under the Nazis and the Russians. After Siggy's death Graff carries out the great zoo break alone.",
      "1967 年春天，维也纳的两个大学生西吉·亚沃特尼克和汉内斯·格拉夫买了一辆旧摩托车，骑到乡下去。西吉又回城，在希青动物园里藏了一夜，用笔记本记下守夜人的种种残忍，也记下自己一家在纳粹和苏军统治下的遭遇。西吉死后，格拉夫独自完成了那场动物园大逃亡。",
      ["the Hietzing Zoo"], ["希青动物园"], W + "Setting_Free_the_Bears"),
    S("at-trapp-s1", "at-trapp-family", "at-nonnberg", "Part 1", "第一部",
      "Maria, an orphan and a mountain-climber, is the despair of the novice mistress: she whistles in the corridors and slides down the banisters. Sent for ten months to the Trapp villa at Aigen, she teaches the seven children to sing in parts. The Captain asks her to stay as their mother; she runs back to the convent to ask the abbess, and is told it is God's will. The family leaves Austria in 1938.",
      "玛丽亚是个孤儿，爱爬山，让见习修女的导师伤透了脑筋：她在走廊里吹口哨，顺着楼梯扶手往下滑。她被派到艾根的特拉普别墅去十个月，教七个孩子唱多声部合唱。上校请她留下来当孩子们的母亲；她跑回修道院去问院长，得到的回答是：这是天主的旨意。1938 年，一家人离开了奥地利。",
      ["the convent"], ["修道院"], W + "The_Story_of_the_Trapp_Family_Singers"),
    S("at-maikaefer-s1", "at-maikaefer", "at-neuwaldegg", "Throughout", "全书",
      "The grown-ups are afraid of the Russians; Christel is not. Her father, a deserter with wounded legs, hides in the villa; the major's men drink, shoot at the ceiling and share their food. She attaches herself to Cohn, the small, ugly, short-sighted cook from Leningrad, who is the gentlest person she has met, and when he is sent away she sets off to look for him.",
      "大人们怕苏军，克里斯特尔不怕。她的父亲是个逃兵，腿上有伤，躲在别墅里；少校手下的兵喝酒，朝天花板开枪，也把吃的分给他们。她缠上了科恩——那个来自列宁格勒的炊事兵，又矮又丑，还近视，却是她见过的最和气的人；他被调走以后，她就出发去找他。",
      ["the villa"], ["别墅"], W + "Christine_N%C3%B6stlinger"),
    S("at-auden-s1", "at-about-the-house", "at-kirchstetten", "'Thanksgiving for a Habitat'", "《感恩一处居所》",
      "A sequence of poems for the rooms of the house, most of them dedicated to friends: the study that is 'the cave of making', the cellar, the attic, the kitchen where Chester Kallman cooks, the bath, the guest room, the living room where no one may be bored. At fifty Auden says he has at last what he never expected, a place he may call his own and where he hopes to die.",
      "一组诗，写房子里的各个房间，大多各题献给一位朋友：书房是“创作的洞穴”，还有地窖、阁楼、切斯特·卡尔曼做饭的厨房、浴室、客房，以及谁也不许觉得无聊的起居室。年过五十的奥登说，他终于有了从没指望过的东西：一处可以称作自己的地方，他希望将来死在这里。",
      ["the house"], ["房子"], W + "About_the_House"),
    S("at-fermor-s1", "at-time-of-gifts", "at-melk", "The Danube chapters", "多瑙河各章",
      "Eighteen years old, walking from the Hook of Holland to Constantinople in the winter of 1933–34, Leigh Fermor follows the Danube from castle to castle through the snow. At Melk a young Benedictine leads him through the marble hall, the library and the church, and the description becomes one long sentence of gold, light and music.",
      "1933 至 1934 年的冬天，十八岁的利·弗莫尔从荷兰角徒步走向君士坦丁堡，沿着多瑙河在雪中从一座城堡走到另一座城堡。在梅尔克，一位年轻的本笃会修士领他穿过大理石厅、图书馆和教堂，他的描写化成了一个由金色、光线和音乐组成的长句。",
      ["Melk"], ["梅尔克"], W + "A_Time_of_Gifts"),
    S("at-rose-s1", ROSE, "at-melk", "Prologue", "序章",
      "Knowing that his life is near its end, the aged Adso sits in his cell at Melk to leave on parchment his testimony of the terrible events he witnessed in his youth, in the last week of November 1327, in an abbey in northern Italy whose name he thinks it right to leave unsaid.",
      "年迈的阿德索自知罪人的一生将尽，在梅尔克修道院的斗室里准备把见证留在羊皮纸上：年轻时，1327 年 11 月的最后一周，他在意大利北部一座修道院里亲眼见到的可怕事件——那座修道院的名字，他认为还是不说为好。",
      ["Melk"], ["梅尔克"], W + "The_Name_of_the_Rose"),
    S("at-feast-s1", FEAST, "at-schruns", "'There Is Never Any End to Paris'", "“巴黎永远没有个完”",
      "Once the baby was born, Paris was too cold for the family in winter, and Hemingway took them to Schruns in the Vorarlberg, to the Taube, with its big warm rooms and generous meals. They climbed on skins to ski down from the Madlener Haus, played poker with the hotel owner and the gendarme behind closed shutters, and that is where the rich found them.",
      "孩子出生以后，巴黎的冬天对这一家来说太冷了，海明威带他们去了福拉尔贝格的施伦斯，住进鸽子旅馆——房间宽敞暖和，饭菜丰盛。他们在滑雪板底贴上海豹皮爬上马德莱纳小屋再滑下来，关上百叶窗同旅馆老板和宪兵打扑克——有钱人也就是在那里找到了他们。",
      ["Schruns"], ["施伦斯"], W + "A_Moveable_Feast"),
    S("at-wand-s1", "at-die-wand", "at-molln", "Throughout", "全书",
      "A woman of about forty goes with her cousin and his wife to their hunting lodge. The couple walk to the village and do not return; next morning she finds an invisible wall across the valley, and beyond it people and animals turned to stone. She writes her report on the backs of old calendars: two and a half years with a dog, a cow, a cat, the potatoes, the hay, the alp in summer, and the day a man appears.",
      "一个四十岁上下的女人跟着表姐夫妇去他们的猎屋。夫妇俩步行去村里，再没回来；第二天早上，她发现一堵看不见的墙横在山谷里，墙外的人和动物都成了石头。她在旧日历的背面写下自己的报告：两年半的日子，一条狗，一头母牛，一只猫，土豆，干草，夏天的高山牧场，还有一个男人出现的那一天。",
      ["hunting lodge"], ["猎屋"], W + "The_Wall_(novel)"),
    S("at-hare-s1", "at-hare-amber-eyes", "at-palais-ephrussi", "Parts 2 and 3", "第二、三部",
      "The netsuke live in a black lacquer vitrine in Emmy von Ephrussi's dressing room, where her children are allowed to play with them while she dresses. In March 1938 the mob breaks in on the night of the Anschluss; within weeks the bank, the pictures and the library are gone. After the war Elisabeth, the eldest daughter, comes back to an emptied house and is handed the 264 carvings by Anna.",
      "这些根付放在埃米·冯·埃弗吕西更衣室的一只黑漆玻璃柜里，她梳妆的时候，孩子们可以拿出来玩。1938 年 3 月德奥合并的当夜，暴徒闯了进来；几个星期之内，银行、藏画和藏书全没了。战后，长女伊丽莎白回到被搬空的房子，安娜把 264 件小雕件交到了她手里。",
      ["netsuke"], ["根付"], W + "The_Hare_with_Amber_Eyes"),
]

# ============================== write ==============================
used = {p for l in lines for p in l["place_ids"]}
for p in places:
    assert p["id"] in used or p.get("book_ids"), ("place without a line or a book", p["id"])
assert {p["id"] for p in places} == set(CO), set(CO) ^ {p["id"] for p in places}
bids = {x["id"] for x in books} | {NIB, FEAST, ROSE}
for l in lines:
    assert l["book_id"] in bids, l["id"]
lined = {l["book_id"] for l in lines}
pilgrim = {i for p in places for i in p.get("book_ids", [])}
assert pilgrim <= bids, pilgrim - bids
assert not ({x["id"] for x in books} - lined - pilgrim), {x["id"] for x in books} - lined - pilgrim
assert len({x["id"] for x in places}) == len(places) and len({x["id"] for x in lines}) == len(lines) and len({x["id"] for x in books}) == len(books)

HEAD = "// Austria, hand-written content (tools/content/batches/add_at1.py, 2026-11-22).\n"
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
