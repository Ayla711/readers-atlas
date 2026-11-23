"""11-23: Germany, a second pack: 43 more books and 51 more places, to bring the country in line with its weight
(the classics in their own places, the provinces from the Rhine to Rügen, post-war and recent books).

Quotations (11 lines) are cut from Wikisource pages (tools/content/wikisource.py): German Wikisource, and English
Wikisource for Byron (the book is already on the shared list as pt-childe-harold); English and Chinese translations
are our own drafts (translation: "own"). Books in copyright, and public-domain books whose text is not on Wikisource,
have scene notes in our own words; the rest hang on a writer's place.
What a cut changes, named again in that line's `checked`: no-break spaces are written as plain spaces; in the Byron
stanza the editor's note mark is left out.

Coordinates are those of the place's German Wikipedia article (cache/de/coords.json).

Usage: python3 -I add_de1.py <app_dir> <coords.json> <wikisource_root>   (<root>/de and <root>/en hold the pages)"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b
import wikisource as ws

APP, CO, WSR = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8")), sys.argv[3]
DATE = "2026-11-23"
b.init(APP, "", "de", DATE)
W = b.W
DEW = "https://de.wikipedia.org/wiki/"

def BK(id, title, title_zh, title_orig, author, author_zh, year, pd=True, **kw):
    d = dict(id=id, title=title, title_zh=title_zh, title_orig=title_orig, author=author, author_zh=author_zh, author_orig=kw.pop("author_orig", author),
             year=year, orig_lang=kw.pop("lang", "de"), public_domain=pd, source_url=kw.pop("src", None))
    d.update(kw)
    return {k: v for k, v in d.items() if v is not None or k == "source_url"}

def C(pid):
    c = CO[pid]
    return c["lat"], c["lon"], c["st"], c["su"]

def ORIG(pid, name, zh, en_note, zh_note, **kw): return b.ORIG(pid, name, zh, *C(pid), en_note, zh_note, **kw)
def PROTO(pid, name, zh, en_note, zh_note, **kw): return b.PROTO(pid, name, zh, *C(pid), en_note, zh_note, **kw)
def PIL(pid, name, zh, en_note, zh_note, ids, **kw): return b.PIL(pid, name, zh, *C(pid), en_note, zh_note, ids, **kw)
S = b.S

def raw(title, start, end, lang="de"):
    """the page's own text between two markers; the markers are matched with no-break spaces read as spaces"""
    t = ws.text(os.path.join(WSR, lang), title)
    n = t.replace("\xa0", " ")
    i = n.find(start)
    assert i >= 0, (title, start)
    j = n.find(end, i)
    assert j >= 0, (title, start, end)
    return t[i:j + len(end)]

def Q(id, book, place, loc, loc_zh, title, orig, hl_orig, en, hl_en, zh, hl_zh, note=""):
    if "\xa0" in orig:
        orig = re.sub(r" {2,}", " ", orig.replace("\xa0", " "))
        note += " (no-break spaces written as plain spaces)"
    for text, hls in ((orig, hl_orig), (en, hl_en), (zh, hl_zh)):
        for h in hls:
            assert h in text, (id, h)
    assert "  " not in orig and "[" not in orig, (id, "spacing or page mark")
    return dict(id=id, book_id=book, place_ids=[place], location=loc, location_zh=loc_zh,
                text_orig=orig, highlight_orig=hl_orig, text_en=en, highlight_en=hl_en, text_zh=zh, highlight_zh=hl_zh, translation="own",
                status="draft", checked=f"German Wikisource, {title}{note}, {DATE}")

DE = lambda t: ws.url("de", t)
GOE = ("Johann Wolfgang von Goethe", "歌德")
HEI = ("Heinrich Heine", "海涅")
DRO = ("Annette von Droste-Hülshoff", "德罗斯特-许尔斯霍夫")
TMANN = ("Thomas Mann", "托马斯·曼")
T_EG, T_HD, T_WM, T_GZ, T_GT = "Ein Gleiches", "An Heidelberg", "Deutschland. Ein Wintermährchen", "Götz von Berlichingen mit der eisernen Hand", "Der goldne Topf"
T_AT, T_DS, T_RB, T_JB = "Am Thurme", "Die Stadt (Storm)", "Herr von Ribbeck auf Ribbeck im Havelland (Fontane)", "Die Judenbuche"
T_CH = "The Works of Lord Byron (ed. Coleridge, Prothero)/Poetry/Volume 2/Childe Harold's Pilgrimage/Canto III"
BYRON = "pt-childe-harold"

# ============================== books ==============================
books = [
    BK("wanderers-nachtlied", "Wanderer's Nightsong II", "浪游者的夜歌", "Wandrers Nachtlied (Ein Gleiches)", *GOE, "1780", src=DE(T_EG),
       aliases=["Über allen Gipfeln", "Ein Gleiches", "Wanderer's Night Song", "Over all the hilltops"]),
    BK("an-heidelberg", "Heidelberg (ode)", "海德堡", "Heidelberg", "Friedrich Hölderlin", "荷尔德林", "1800", src=DE(T_HD),
       aliases=["Lange lieb ich dich schon", "An Heidelberg", "Hölderlin", "Hoelderlin"]),
    BK("harzreise", "The Harz Journey", "哈尔茨山游记", "Die Harzreise", *HEI, "1826", aliases=["Die Harzreise", "Travel Pictures", "Reisebilder", "Harz"]),
    BK("the-robbers", "The Robbers", "强盗", "Die Räuber", "Friedrich Schiller", "席勒", "1781", aliases=["Die Räuber", "Karl Moor", "Schiller"]),
    BK("simplicissimus", "Simplicius Simplicissimus", "痴儿西木传", "Der abenteuerliche Simplicissimus Teutsch", "Hans Jakob Christoffel von Grimmelshausen", "格里美尔斯豪森", "1668",
       aliases=["The Adventurous Simplicissimus", "Simplicissimus", "Grimmelshausen", "Thirty Years' War"]),
    BK("goetz-von-berlichingen", "Götz von Berlichingen", "铁手骑士葛兹·冯·贝利欣根", "Götz von Berlichingen mit der eisernen Hand", *GOE, "1773", src=DE(T_GZ),
       aliases=["Goetz von Berlichingen", "Götz of the Iron Hand", "葛兹"]),
    BK("prince-of-homburg", "The Prince of Homburg", "洪堡亲王", "Prinz Friedrich von Homburg", "Heinrich von Kleist", "克莱斯特", "1821",
       aliases=["Prinz Friedrich von Homburg", "Prince Friedrich of Homburg", "Fehrbellin"]),
    BK("heinrich-von-ofterdingen", "Heinrich von Ofterdingen", "海因里希·冯·奥弗特丁根", "Heinrich von Ofterdingen", "Novalis", "诺瓦利斯", "1802",
       aliases=["Henry of Ofterdingen", "the blue flower", "blaue Blume", "蓝花", "Hardenberg"]),
    BK("the-golden-pot", "The Golden Pot", "金罐", "Der goldne Topf", "E. T. A. Hoffmann", "E. T. A. 霍夫曼", "1814", src=DE(T_GT),
       aliases=["Der goldene Topf", "Anselmus", "Serpentina", "金罐子"]),
    BK("the-jews-beech", "The Jew's Beech", "犹太人的山毛榉", "Die Judenbuche", *DRO, "1842", src=DE(T_JB),
       aliases=["Die Judenbuche", "The Jew's Beech Tree", "Friedrich Mergel", "Droste"]),
    BK("am-turme", "On the Tower", "在塔楼上", "Am Turme", *DRO, "1842", src=DE(T_AT), aliases=["Am Thurme", "Droste", "Meersburg"]),
    BK("die-stadt-storm", "The Town", "城", "Die Stadt", "Theodor Storm", "施托姆", "1852", src=DE(T_DS),
       aliases=["Die graue Stadt am Meer", "The Grey Town by the Sea", "Husum"]),
    BK("herr-von-ribbeck", "Herr von Ribbeck auf Ribbeck im Havelland", "哈弗尔兰的里贝克老爷", "Herr von Ribbeck auf Ribbeck im Havelland", "Theodor Fontane", "冯塔纳", "1889",
       src=DE(T_RB), aliases=["Ribbeck", "the pear tree", "Birnbaum", "Squire von Ribbeck"]),
    BK("max-and-moritz", "Max and Moritz", "马克斯和莫里茨", "Max und Moritz", "Wilhelm Busch", "威廉·布施", "1865",
       aliases=["Max und Moritz", "A Story of Seven Boyish Pranks", "Busch"]),
    BK("winnetou", "Winnetou", "温内图", "Winnetou", "Karl May", "卡尔·迈", "1893", aliases=["Old Shatterhand", "Karl May", "老铁手"]),
    BK("thus-spoke-zarathustra", "Thus Spoke Zarathustra", "查拉图斯特拉如是说", "Also sprach Zarathustra", "Friedrich Nietzsche", "尼采", "1883–1885",
       aliases=["Also sprach Zarathustra", "Zarathustra", "Nietzsche"]),
    BK("lotte-in-weimar", "Lotte in Weimar", "绿蒂在魏玛", "Lotte in Weimar", *TMANN, "1939", aliases=["The Beloved Returns", "Charlotte Kestner"]),
    BK("narcissus-and-goldmund", "Narcissus and Goldmund", "纳尔齐斯与歌尔德蒙", "Narziß und Goldmund", "Hermann Hesse", "赫尔曼·黑塞", "1930", pd=False,
       aliases=["Narziss und Goldmund", "Death and the Lover", "Mariabronn", "知识与爱情"]),
    BK("buckow-elegies", "Buckow Elegies", "布科哀歌", "Buckower Elegien", "Bertolt Brecht", "布莱希特", "1953", pd=False,
       aliases=["Buckower Elegien", "Die Lösung", "The Solution", "Der Radwechsel"]),
    BK("rheinsberg", "Rheinsberg: A Storybook for Lovers", "莱茵斯贝格", "Rheinsberg. Ein Bilderbuch für Verliebte", "Kurt Tucholsky", "图霍尔斯基", "1912",
       aliases=["Rheinsberg", "Ein Bilderbuch für Verliebte", "Tucholsky", "Claire", "Wölfchen"]),
    BK("mephisto", "Mephisto", "梅菲斯特", "Mephisto. Roman einer Karriere", "Klaus Mann", "克劳斯·曼", "1936", aliases=["Hendrik Höfgen", "Gründgens", "Roman einer Karriere"]),
    BK("the-man-outside", "The Man Outside", "在大门外", "Draußen vor der Tür", "Wolfgang Borchert", "沃尔夫冈·博尔谢特", "1947",
       aliases=["Draußen vor der Tür", "Beckmann", "Borchert", "大门之外"]),
    BK("the-german-lesson", "The German Lesson", "德语课", "Deutschstunde", "Siegfried Lenz", "西格弗里德·伦茨", "1968", pd=False,
       aliases=["Deutschstunde", "Siggi Jepsen", "Rugbüll", "Nolde"]),
    BK("the-meeting-at-telgte", "The Meeting at Telgte", "相聚在特尔格特", "Das Treffen in Telgte", "Günter Grass", "君特·格拉斯", "1979", pd=False,
       aliases=["Das Treffen in Telgte", "Simon Dach", "Gruppe 47", "Group 47"]),
    BK("divided-heaven", "Divided Heaven", "分裂的天空", "Der geteilte Himmel", "Christa Wolf", "克里斯塔·沃尔夫", "1963", pd=False,
       aliases=["Der geteilte Himmel", "They Divided the Sky", "Rita Seidel", "Christa Wolf"]),
    BK("anniversaries", "Anniversaries", "周年纪念日", "Jahrestage", "Uwe Johnson", "乌韦·约翰逊", "1970–1983", pd=False,
       aliases=["Jahrestage", "Gesine Cresspahl", "Jerichow", "From a Year in the Life of Gesine Cresspahl"]),
    BK("vertigo-sebald", "Vertigo", "眩晕", "Schwindel. Gefühle.", "W. G. Sebald", "W. G. 塞巴尔德", "1990", pd=False,
       aliases=["Schwindel. Gefühle", "Il ritorno in patria", "Sebald", "Wertach"]),
    BK("visitation", "Visitation", "客乡", "Heimsuchung", "Jenny Erpenbeck", "燕妮·埃彭贝克", "2008", pd=False,
       aliases=["Heimsuchung", "Erpenbeck", "Kairos", "the gardener"]),
    BK("kruso", "Kruso", "克鲁索", "Kruso", "Lutz Seiler", "卢茨·赛勒", "2014", pd=False, aliases=["Hiddensee", "Klausner", "Seiler", "Ed Bendler"]),
    BK("sonnenallee", "The Short End of the Sonnenallee", "太阳大道较短的那一头", "Am kürzeren Ende der Sonnenallee", "Thomas Brussig", "托马斯·布鲁西希", "1999", pd=False,
       aliases=["Am kürzeren Ende der Sonnenallee", "Sonnenallee", "Brussig", "Micha Kuppisch"]),
    BK("stasiland", "Stasiland", "斯塔西之地", None, "Anna Funder", "安娜·方德", "2003", pd=False, lang="en",
       aliases=["Stories from Behind the Berlin Wall", "Stasi", "Miriam Weber", "史塔西"]),
    BK("in-a-german-pension", "In a German Pension", "在德国公寓里", None, "Katherine Mansfield", "凯瑟琳·曼斯菲尔德", "1911", lang="en",
       aliases=["Mansfield", "Wörishofen", "Germans at Meat", "在德国膳宿公寓"]),
    BK("caspar-hauser", "Caspar Hauser", "卡斯帕尔·豪泽尔", "Caspar Hauser oder Die Trägheit des Herzens", "Jakob Wassermann", "雅各布·瓦塞尔曼", "1908",
       aliases=["Kaspar Hauser", "The Inertia of the Heart", "Wassermann", "Die Trägheit des Herzens"]),
    BK("lichtenstein", "Lichtenstein", "列支敦士登城堡", "Lichtenstein", "Wilhelm Hauff", "威廉·豪夫", "1826", src=DE("Lichtenstein"),
       aliases=["Hauff", "Duke Ulrich", "Romantische Sage", "豪夫"]),
    BK("naked-among-wolves", "Naked Among Wolves", "裸露在狼群中", "Nackt unter Wölfen", "Bruno Apitz", "布鲁诺·阿皮茨", "1958", pd=False,
       aliases=["Nackt unter Wölfen", "Buchenwald", "Apitz", "赤手斗群狼"]),
    BK("gladius-dei", "Gladius Dei", "上帝之剑", "Gladius Dei", *TMANN, "1902", aliases=["München leuchtete", "Munich shone", "Hieronymus"]),
    BK("white-rose-leaflets", "Leaflets of the White Rose", "白玫瑰传单", "Flugblätter der Weißen Rose", "Hans Scholl, Alexander Schmorell and others", "汉斯·朔尔、亚历山大·施莫雷尔等", "1942–1943",
       aliases=["Die Weiße Rose", "White Rose", "Sophie Scholl", "白玫瑰", "Flugblätter"]),
    BK("communist-manifesto", "The Communist Manifesto", "共产党宣言", "Manifest der Kommunistischen Partei", "Karl Marx and Friedrich Engels", "马克思、恩格斯", "1848",
       aliases=["Manifest der Kommunistischen Partei", "Marx", "Engels", "Das Kapital"]),
    BK("elizabeth-in-rugen", "The Adventures of Elizabeth in Rügen", "伊丽莎白吕根岛历险记", None, "Elizabeth von Arnim", "伊丽莎白·冯·阿尼姆", "1904", lang="en",
       aliases=["Elizabeth in Rugen", "Elizabeth and Her German Garden", "von Arnim", "Rügen"]),
    BK("christiane-f", "Zoo Station: The Story of Christiane F.", "我们，动物园站的孩子们", "Wir Kinder vom Bahnhof Zoo", "Christiane F., with Kai Hermann and Horst Rieck", "克里斯蒂安娜·F（凯·赫尔曼、霍斯特·里克记录）", "1978",
       pd=False, aliases=["Wir Kinder vom Bahnhof Zoo", "Christiane F.", "We Children from Bahnhof Zoo", "Bahnhof Zoo"]),
    BK("luther-bible", "The September Testament (Luther's New Testament)", "九月圣经（路德译《新约》）", "Das Newe Testament Deutzsch", "Martin Luther (translator)", "马丁·路德（译）", "1522",
       aliases=["Luther Bible", "Lutherbibel", "Septembertestament", "Junker Jörg", "路德圣经"]),
    BK("under-der-linden", "Under the Lime Tree", "菩提树下", "Under der linden", "Walther von der Vogelweide", "瓦尔特·冯·德·福格尔魏德", "c. 1200",
       aliases=["Under der linden", "Unter der Linden", "Walther", "tandaradei", "Minnesang"]),
    BK("fabian-kaestner", "Fabian", "法比安", "Fabian. Die Geschichte eines Moralisten", "Erich Kästner", "埃里希·凯斯特纳", "1931", pd=False,
       aliases=["Fabian: The Story of a Moralist", "Going to the Dogs", "Der Gang vor die Hunde"]),
]

# ============================== places ==============================
places = [
    # ---- Goethe, Schiller, the classics ----
    ORIG("de-kickelhahn", "Kickelhahn (Goethe's hut), Ilmenau", "基克尔汉山（歌德小屋），伊尔默瑙",
         "On the evening of 6 September 1780 Goethe wrote the eight lines of this poem on the wooden wall of a hunters' hut near the top of the Kickelhahn, above Ilmenau. He came back in August 1831, the day before his last birthday, and read them again. The hut burned down in 1870 and was rebuilt",
         "1780 年 9 月 6 日傍晚，歌德在伊尔默瑙上方基克尔汉山顶附近的一间猎人木屋的板壁上写下了这首八行小诗。1831 年 8 月，他在最后一个生日的前一天重回这里，又读了一遍。木屋 1870 年烧毁，后来重建"),
    PIL("de-marbach", "Marbach am Neckar (German Literature Archive)", "内卡河畔马尔巴赫（德国文学档案馆）",
        "Schiller was born in Marbach in 1759; the house of his birth is a museum. On the hill above the town stand the Schiller National Museum and the German Literature Archive, which keeps the papers of German writers from the eighteenth century to the present",
        "席勒 1759 年生于马尔巴赫，出生的房子今为纪念馆。城外山坡上是席勒国家博物馆和德国文学档案馆，后者收藏着十八世纪至今德语作家的手稿和遗物",
        ["the-robbers", "intrigue-and-love", "mary-stuart"]),
    ORIG("de-heidelberg-old-bridge", "Old Bridge, Heidelberg", "老桥，海德堡",
         "The stone bridge over the Neckar, finished in 1788. Hölderlin's ode to the town, written around 1800, remembers standing on it spellbound as a young man passing through",
         "内卡河上的石桥，1788 年建成。荷尔德林约 1800 年写下的这首献给海德堡的颂歌，回忆的就是他年轻时路过此地、站在桥上着了迷的那一刻"),
    ORIG("de-goettingen-rathaus", "Old Town Hall, Göttingen", "老市政厅，哥廷根",
         "Heine studied law at Göttingen, was sent down for a duelling affair, came back and took his doctorate here in 1825. In September 1824 he set off from the town on foot for the Harz, and his account of the walk begins with a mocking portrait of Göttingen and its professors",
         "海涅在哥廷根学法律，因决斗事件被勒令离校，后来又回来，1825 年在这里取得博士学位。1824 年 9 月他从这座城徒步前往哈尔茨山，游记一开头就把哥廷根和它的教授们挖苦了一番"),
    ORIG("de-cologne-cathedral", "Cologne Cathedral", "科隆大教堂",
         "When Heine passed through in 1843 the cathedral was still a torso: building had stopped in the sixteenth century and had only just begun again in 1842. He mocked the patriotic society that was collecting to finish it. It was completed in 1880",
         "1843 年海涅路过时，大教堂还只是半截子工程：十六世纪停工，1842 年才刚刚复工。他嘲笑了那个募款要把它建完的爱国协会。大教堂 1880 年落成"),
    ORIG("de-kyffhaeuser", "Kyffhäuser", "屈夫霍伊泽山",
         "The wooded ridge in northern Thuringia where, legend says, the emperor Frederick Barbarossa sleeps in a cave with his knights until Germany needs him. Heine has his old nurse tell him the legend, and then goes into the mountain to argue with the emperor. The huge monument on the ridge was built in the 1890s",
         "图林根北部林木覆盖的山岭。传说红胡子皇帝腓特烈一世和他的骑士们睡在山洞里，等到德国需要他的时候才醒来。海涅让老乳母给他讲这个传说，然后自己进山去同皇帝争辩。山上那座巨大的纪念碑建于 1890 年代"),
    PIL("de-grimmwelt", "Grimmwelt, Kassel", "格林世界博物馆，卡塞尔",
        "The brothers Grimm lived in Kassel for some thirty years and gathered most of their tales here. The museum, opened in 2015, shows their own annotated copies of the Children's and Household Tales",
        "格林兄弟在卡塞尔住了约三十年，大部分童话是在这里搜集的。这座 2015 年开馆的博物馆展出他们亲手批注的《儿童与家庭童话集》",
        ["grimms-fairy-tales"]),
    PIL("de-hanau-grimm", "Brothers Grimm Monument, Hanau", "格林兄弟纪念像，哈瑙",
        "Jacob and Wilhelm Grimm were born in Hanau, in 1785 and 1786. The bronze of the two brothers on the market square, unveiled in 1896, is the starting point of the German Fairy Tale Route",
        "雅各布·格林和威廉·格林分别于 1785 年和 1786 年生于哈瑙。集市广场上的兄弟二人铜像 1896 年揭幕，是“德国童话之路”的起点",
        ["grimms-fairy-tales"]),
    PIL("de-lusamgaertchen", "Walther's Grave, Lusamgärtchen, Würzburg", "瓦尔特墓，卢萨姆小园，维尔茨堡",
        "Walther von der Vogelweide, the greatest of the Minnesingers, is said to have been buried around 1230 in the cloister of the Neumünster in Würzburg. A memorial stone stands in what remains of the cloister garden, and visitors leave flowers on it",
        "中世纪最伟大的恋歌诗人瓦尔特·冯·德·福格尔魏德，据说约 1230 年葬在维尔茨堡新明斯特教堂的回廊里。回廊花园残存的一角立着一块纪念石，来访的人会在上面放花",
        ["under-der-linden"]),
    PIL("de-wartburg", "Wartburg", "瓦尔特堡",
        "Hidden in this castle above Eisenach from May 1521 to March 1522 under the name 'Junker Jörg', Luther translated the New Testament into German in about eleven weeks. It was printed in September 1522. Legend also sets the medieval contest of the Minnesingers here",
        "1521 年 5 月到 1522 年 3 月，路德化名“容克尔·约尔格”藏身于艾森纳赫上方的这座城堡，用大约十一个星期把《新约》译成德文，1522 年 9 月刊印。传说中世纪恋歌诗人的赛歌会也发生在这里",
        ["luther-bible"]),
    PIL("de-gelnhausen", "Gelnhausen", "盖尔恩豪森",
        "Grimmelshausen was born in this imperial town on the Kinzig around 1622 and lost his home when it was sacked in 1634. The boy hero of his novel of the Thirty Years' War grows up on a farm in the Spessart hills nearby",
        "格里美尔斯豪森约 1622 年生于金齐希河畔的这座帝国城市，1634 年城遭洗劫，他失去了家。他那部写三十年战争的小说里，少年主人公就在附近的施佩萨特山中的农庄长大",
        ["simplicissimus"]),
    ORIG("de-jagsthausen", "Jagsthausen Castle", "雅格斯特豪森城堡",
         "The castle on the Jagst where the knight Götz von Berlichingen, the man with the iron hand, was born around 1480; much of Goethe's play is set in it. The play is performed every summer in the castle courtyard",
         "雅格斯特河畔的城堡，“铁手骑士”葛兹·冯·贝利欣根约 1480 年生于此；歌德这部剧的许多场景就设在城堡里。每年夏天，这部剧都在城堡院子里上演"),
    ORIG("de-fehrbellin", "Fehrbellin", "费尔贝林",
         "The small town in Brandenburg where, in June 1675, the Great Elector Frederick William defeated the Swedes. Kleist's last play is built on the battle",
         "勃兰登堡的小城。1675 年 6 月，大选帝侯腓特烈·威廉在这里打败了瑞典军队。克莱斯特的最后一部剧作就以这场战役为背景"),
    PIL("de-kleist-museum", "Kleist Museum, Frankfurt (Oder)", "克莱斯特博物馆，奥得河畔法兰克福",
        "Heinrich von Kleist was born in Frankfurt on the Oder in 1777. The museum of his life and work is in the former garrison school by the river",
        "海因里希·冯·克莱斯特 1777 年生于奥得河畔法兰克福。纪念他生平和作品的博物馆设在河边从前的驻军学校里",
        ["michael-kohlhaas", "the-marquise-of-o", "prince-of-homburg"]),
    PIL("de-novalis", "Novalis's Birthplace, Schloss Oberwiederstedt", "诺瓦利斯出生地，上维德施泰特宫",
        "Friedrich von Hardenberg, who called himself Novalis, was born in this manor house in 1772. His unfinished novel gave Romanticism its emblem, the blue flower. The house holds a Novalis museum and a research centre for early Romanticism",
        "弗里德里希·冯·哈登贝格（笔名诺瓦利斯）1772 年生于这座庄园宅邸。他未完成的长篇小说给了浪漫派一个象征：蓝花。宅子里设有诺瓦利斯博物馆和早期浪漫派研究中心",
        ["heinrich-von-ofterdingen"]),
    ORIG("de-dresden-albertplatz", "Site of the Black Gate (Albertplatz), Dresden", "黑门旧址（阿尔伯特广场），德累斯顿",
         "The Black Gate was the northern gate of Dresden's Neustadt; it was pulled down in the early nineteenth century, and Albertplatz was laid out where it stood. Hoffmann, who lived in Dresden in 1813 and 1814, starts his fairy tale with a student running through it",
         "黑门是德累斯顿新城的北门，十九世纪初拆除，原址上修了阿尔伯特广场。霍夫曼 1813 年到 1814 年住在德累斯顿，他这篇童话一开头，就是一个大学生从黑门跑过"),
    # ---- the nineteenth century ----
    PIL("de-huelshoff", "Burg Hülshoff", "许尔斯霍夫城堡",
        "Annette von Droste-Hülshoff was born in 1797 in this moated manor house west of Münster and grew up here. It is now a museum and a centre for literature",
        "安内特·冯·德罗斯特-许尔斯霍夫 1797 年生于明斯特以西这座有护城河环绕的庄园宅邸，并在这里长大。今为纪念馆和文学中心",
        ["the-jews-beech", "am-turme"]),
    ORIG("de-meersburg", "Meersburg Castle", "梅尔斯堡城堡",
         "The old castle above Lake Constance belonged to Droste's brother-in-law Joseph von Laßberg. She first came to stay in 1841, wrote many of her best poems here in the winter that followed, and died in the castle in 1848. Her rooms can be visited",
         "博登湖畔高处的古堡，当年属于德罗斯特的姐夫约瑟夫·冯·拉斯贝格。她 1841 年第一次来住，随后那个冬天在这里写出了许多最好的诗，1848 年在堡中去世。她住过的房间可以参观"),
    PROTO("de-bellersen", "Bellersen ('the village of B.')", "贝勒森（“B 村”）",
          "The village in the wooded hills east of Paderborn that the story calls only 'B.'. Droste took the plot from a real case: the murder of a Jewish trader here in 1783. She had heard it told on her grandparents' estate at nearby Bökendorf",
          "帕德博恩以东林木茂密的山丘里的村子，小说里只称“B 村”。德罗斯特的情节取自真事：1783 年一个犹太商贩在这里被杀。她是在附近伯肯多夫的外祖父母家庄园里听人讲起这件事的"),
    ORIG("de-ribbeck", "Ribbeck, Havelland", "里贝克村，哈弗尔兰",
         "The village west of Berlin where the von Ribbeck family had its manor. The pear tree of the ballad stood by the church on the old squire's grave until a storm brought it down in 1911; its stump is kept in the church, and a new tree has been planted",
         "柏林以西的村子，冯·里贝克家族的庄园就在这里。歌谣里的那棵梨树长在教堂旁老庄主的墓上，1911 年被一场风暴刮倒；树桩保存在教堂里，原处又栽了一棵新树"),
    PIL("de-ebergoetzen", "Wilhelm Busch Mill, Ebergötzen", "威廉·布施磨坊，埃伯格岑",
        "Wilhelm Busch was sent here at nine to be taught by his uncle, the village pastor, and stayed from 1841 to 1846. His closest friend was the miller's son Erich Bachmann, and their boyhood in and around the mill is taken as the seed of Max and Moritz. The mill is a museum",
        "威廉·布施九岁时被送到这里，跟当乡村牧师的舅舅读书，从 1841 年住到 1846 年。他最要好的朋友是磨坊主的儿子埃里希·巴赫曼，两人在磨坊里外度过的童年被看作《马克斯和莫里茨》的由来。磨坊今为博物馆",
        ["max-and-moritz"]),
    PIL("de-radebeul", "Karl May Museum, Radebeul", "卡尔·迈博物馆，拉德博伊尔",
        "Karl May lived in the 'Villa Shatterhand' from 1896 until his death in 1912. The villa and the log house in its garden show his study and library and a collection on the Indians of North America, whom he made into heroes for generations of German readers without having seen the West",
        "卡尔·迈从 1896 年起住在这座“老铁手别墅”里，直到 1912 年去世。别墅和花园里的原木屋展出他的书房、藏书和北美印第安人文物。他没有到过美国西部，却把印第安人写成了几代德国读者心目中的英雄",
        ["winnetou"]),
    PIL("de-naumburg-nietzsche", "Nietzsche House, Naumburg", "尼采故居，瑙姆堡",
        "Nietzsche's mother moved into this house in 1858, when he was a schoolboy. After his collapse he was brought back to it in 1890, and she nursed him here until her death in 1897",
        "尼采的母亲 1858 年搬进这幢房子，那时他还是个中学生。精神崩溃之后，他 1890 年被接回这里，由母亲照料，直到她 1897 年去世",
        ["thus-spoke-zarathustra"]),
    ORIG("de-lichtenstein", "Lichtenstein Castle", "利希滕施泰因城堡",
         "Hauff's historical novel of 1826 has the outlawed Duke Ulrich of Württemberg hide near a castle on this crag of the Swabian Alb. Inspired by the book, Count Wilhelm of Württemberg had the present castle built on the old foundations between 1840 and 1842",
         "豪夫 1826 年的历史小说里，被放逐的符腾堡公爵乌尔里希藏身在施瓦本山这块峭壁上的城堡附近。受这本书的启发，符腾堡的威廉伯爵 1840 年到 1842 年在旧基址上建起了今天的城堡",
         book_ids=["lichtenstein"]),
    ORIG("de-drachenfels", "Drachenfels", "龙岩山",
         "The ruined castle on the first of the Seven Hills above the Rhine, south of Bonn. Byron saw it in May 1816 on his way up the river, and the song he set into Childe Harold made it one of the most visited spots on the Rhine",
         "波恩以南、莱茵河畔七峰山第一座山峰上的城堡废墟。拜伦 1816 年 5 月沿莱茵河上行时见到它，他写进《恰尔德·哈洛尔德游记》里的那首歌让这里成了莱茵河上游人最多的地方之一"),
    ORIG("de-ansbach", "Ansbach", "安斯巴赫",
         "The foundling Kaspar Hauser, who had appeared in Nuremberg in 1828 hardly able to speak, lived in Ansbach from 1831. On 14 December 1833 he came home from the court garden with a stab wound and died three days later. Wassermann's novel follows him to this end",
         "弃儿卡斯帕尔·豪泽尔 1828 年出现在纽伦堡时几乎不会说话，1831 年起住在安斯巴赫。1833 年 12 月 14 日，他从宫廷花园带着刀伤回到家，三天后死去。瓦塞尔曼的小说一直写到这个结局"),
    PROTO("de-bad-woerishofen", "Bad Wörishofen", "巴特沃里斯霍芬",
          "The Bavarian spa of Father Kneipp's water cure. Katherine Mansfield, twenty years old, spent the second half of 1909 here, and the sharp sketches of her first book are set in a boarding house like the one she stayed in",
          "巴伐利亚的温泉小城，克奈普神父水疗法的发源地。二十岁的凯瑟琳·曼斯菲尔德 1909 年下半年住在这里，她第一本书里那些尖刻的速写，背景就是一家同她住过的那种膳宿公寓",
          book_ids=["in-a-german-pension"]),
    ORIG("de-ruegen", "Königsstuhl, Rügen", "国王之椅，吕根岛",
         "The white chalk cliff on the Jasmund peninsula, the best-known view on Germany's largest island. Elizabeth von Arnim's comic travel novel takes its narrator round the whole of Rügen by carriage in the summer",
         "亚斯蒙德半岛上的白垩悬崖，德国最大岛屿上最有名的景观。伊丽莎白·冯·阿尼姆的这部诙谐游记小说，让叙述者在夏天乘马车绕吕根岛走了一圈",
         book_ids=["elizabeth-in-rugen"]),
    PIL("de-trier-marx", "Karl Marx House, Trier", "卡尔·马克思故居，特里尔",
        "Karl Marx was born in this house on 5 May 1818. It is a museum of his life and writings",
        "卡尔·马克思 1818 年 5 月 5 日生于这幢房子。今为介绍他生平和著作的博物馆",
        ["communist-manifesto"]),
    # ---- Thomas Mann, Hesse, Brecht, Weimar and Berlin ----
    ORIG("de-hotel-elephant", "Hotel Elephant, Weimar", "大象旅馆，魏玛",
         "The old inn on Weimar's market square. Thomas Mann's novel begins with the arrival here, in 1816, of Charlotte Kestner, the Lotte of Goethe's Werther, now a widow of sixty-three",
         "魏玛集市广场上的老旅馆。托马斯·曼的小说就从 1816 年夏洛特·凯斯特纳来到这里写起，她是歌德《维特》里的绿蒂，这时已是六十三岁的寡妇"),
    PROTO("de-maulbronn", "Maulbronn Monastery", "毛尔布龙修道院",
          "The best-preserved medieval Cistercian monastery north of the Alps, a Protestant seminary since 1556. Hesse was a pupil here from 1891 and ran away in March 1892. It is the seminary that breaks Hans Giebenrath in Beneath the Wheel and the 'Mariabronn' of Narcissus and Goldmund",
          "阿尔卑斯山以北保存最完好的中世纪西多会修道院，1556 年起成为新教神学校。黑塞 1891 年入学，1892 年 3 月逃走。《在轮下》里压垮汉斯·吉本拉特的神学校，《纳尔齐斯与歌尔德蒙》里的“玛利亚布隆”，都是这里",
          book_ids=["beneath-the-wheel"]),
    PIL("de-augsburg-brechthaus", "Brecht House, Augsburg", "布莱希特故居，奥格斯堡",
        "Bertolt Brecht was born on 10 February 1898 in this house between two canals in the old craftsmen's quarter of Augsburg. It is a museum",
        "贝托尔特·布莱希特 1898 年 2 月 10 日生于奥格斯堡旧手工业区两条水渠之间的这幢房子。今为纪念馆",
        ["mother-courage", "life-of-galileo"]),
    ORIG("de-buckow", "Brecht-Weigel House, Buckow", "布莱希特-魏格尔故居，布科",
         "From 1952 Brecht and Helene Weigel spent their summers in this house on the Schermützelsee, east of Berlin. He wrote the short poems of the Buckow Elegies here in the summer of 1953",
         "从 1952 年起，布莱希特和海伦妮·魏格尔每年夏天住在柏林以东舍尔米策尔湖边的这幢房子里。1953 年夏天，他在这里写下了《布科哀歌》里的那些短诗"),
    PIL("de-dorotheenstadt", "Dorotheenstadt Cemetery, Berlin", "多罗特娅城公墓，柏林",
        "The small cemetery on Chausseestraße where Brecht and Helene Weigel are buried, next door to the house they lived in. Hegel and Fichte lie here, and so do Heinrich Mann, Anna Seghers and Christa Wolf",
        "肖塞大街上的小公墓。布莱希特和海伦妮·魏格尔葬在这里，隔壁就是他们住过的房子。黑格尔和费希特也葬在这里，还有亨利希·曼、安娜·西格斯和克里斯塔·沃尔夫",
        ["mother-courage", "the-seventh-cross", "divided-heaven"]),
    ORIG("de-rheinsberg", "Rheinsberg Palace", "莱茵斯贝格宫",
         "The lakeside palace north of Berlin where Frederick the Great spent what he called his happiest years as crown prince. Tucholsky's first success sends two young lovers from Berlin here for a weekend. The palace now houses a Tucholsky museum",
         "柏林以北的湖畔宫殿，腓特烈大帝做王储时在这里度过了他自称最幸福的几年。图霍尔斯基的成名作让一对柏林的年轻恋人到这里过了一个周末。宫里今设有图霍尔斯基文学博物馆"),
    ORIG("de-gendarmenmarkt", "Schauspielhaus (Konzerthaus), Gendarmenmarkt, Berlin", "御林广场剧院（今音乐厅），柏林",
         "Schinkel's theatre on the Gendarmenmarkt was the Prussian State Theatre, which the actor Gustaf Gründgens directed from 1934 under Göring's protection. Klaus Mann, once his brother-in-law, wrote the career into a novel",
         "申克尔设计的御林广场剧院当年是普鲁士国家剧院，演员古斯塔夫·格林德根斯 1934 年起在戈林的庇护下担任院长。曾是他内弟的克劳斯·曼把这段发迹史写成了小说"),
    PIL("de-bebelplatz", "Bebelplatz (book-burning memorial), Berlin", "倍倍尔广场（焚书纪念地），柏林",
        "On the night of 10 May 1933 students burned some twenty thousand books on this square. Erich Kästner stood in the crowd and watched his own go into the fire. A window in the paving looks down into a room of empty white shelves",
        "1933 年 5 月 10 日夜里，大学生们在这个广场上烧掉了约两万册书。埃里希·凯斯特纳站在人群里，看着自己的书被扔进火堆。如今地面上有一扇玻璃窗，往下看是一间摆着空白书架的白色房间",
        ["fabian-kaestner", "emil-and-the-detectives", "all-quiet-on-the-western-front", "book-of-songs"]),
    ORIG("de-bahnhof-zoo", "Bahnhof Zoo, Berlin", "动物园火车站，柏林",
         "West Berlin's main station in the years of the Wall. In the 1970s the area behind it was the city's meeting place for young heroin users, the world this book made known",
         "柏林墙年代西柏林的主要火车站。1970 年代，车站背后一带是城里吸食海洛因的青少年聚集的地方，这本书让外界知道了这个世界"),
    ORIG("de-sonnenallee", "Sonnenallee, Berlin", "太阳大道，柏林",
         "A street nearly five kilometres long, of which the Wall left only the last few hundred metres in East Berlin, with a border crossing at the cut. Brussig's novel is set on that short end in the 1970s",
         "一条将近五公里长的大街，柏林墙只把最后几百米留在了东柏林，截断处设有一个过境口岸。布鲁西希的小说写的就是 1970 年代这短短的一头"),
    # ---- north ----
    ORIG("de-landungsbruecken", "St. Pauli Landungsbrücken, Hamburg", "圣保利栈桥，汉堡",
         "The floating landing stages on the Elbe at St. Pauli. Borchert's play, written in a few days in 1947, the year he died at twenty-six, begins on a pontoon here",
         "易北河圣保利一段的浮码头。博尔谢特的这部剧是 1947 年用几天时间写成的，同年他去世，年仅二十六岁；戏就从这里的一座浮桥上开场"),
    PROTO("de-seebuell", "Nolde's House, Seebüll", "诺尔德故居，泽比尔",
          "The house and garden the painter Emil Nolde built on a mound in the marshes by the Danish border. Nolde, forbidden to paint in 1941, is the evident model for the painter Nansen in Lenz's novel",
          "画家埃米尔·诺尔德在靠近丹麦边境的沼泽地土丘上建的房子和花园。诺尔德 1941 年被禁止作画，伦茨小说里的画家南森显然以他为原型"),
    PROTO("de-kluetz", "Klütz ('Jerichow')", "克吕茨（“耶里肖”）",
          "The small town near the Baltic in north-west Mecklenburg that readers take for the model of Johnson's invented Jerichow. A literature house named after him opened in an old granary here in 2006",
          "梅克伦堡西北部靠近波罗的海的小城，读者认为它是约翰逊虚构的耶里肖的原型。2006 年，以他名字命名的文学之家在这里的一座旧粮仓里开放"),
    ORIG("de-hiddensee", "Gerhart Hauptmann House, Hiddensee", "盖哈特·霍普特曼故居，希登塞岛",
         "The car-free island west of Rügen. Hauptmann bought this summer house at Kloster in 1930 and is buried in the island churchyard. Under the GDR the island drew dropouts who worked the season in its inns, the world of Lutz Seiler's novel",
         "吕根岛以西的无车小岛。霍普特曼 1930 年买下克洛斯特村的这幢消夏别墅，死后葬在岛上的教堂墓地。东德时期，这座岛吸引着一批在旅馆饭店打季节工的“出走者”，卢茨·赛勒的小说写的就是他们",
         book_ids=["pl-weber"]),
    ORIG("de-telgte", "Telgte", "特尔格特",
         "A small pilgrimage town on the Ems, east of Münster, where the Peace of Westphalia was being negotiated in 1647. Grass sets an invented gathering of the German poets of the day here",
         "明斯特以东埃姆斯河畔的朝圣小城；1647 年，威斯特伐利亚和约正在明斯特谈判。格拉斯把一场虚构的当时德语诗人的聚会安排在这里"),
    ORIG("de-scharmuetzelsee", "Scharmützelsee", "沙尔米策尔湖",
         "The long lake south-east of Berlin. Erpenbeck's novel is the story of one summer house on its shore, her own grandparents' house among its models, and of those who lived in it and lost it across the twentieth century",
         "柏林东南的狭长湖泊。埃彭贝克的小说写的是湖边一幢消夏别墅的故事（原型之一是她祖父母的房子），以及二十世纪里在这幢房子住过又失去它的人们"),
    # ---- middle and south ----
    ORIG("de-halle", "Halle (Saale)", "萨勒河畔哈雷",
         "The industrial city where Christa Wolf lived from 1959 to 1962 and worked for a time in a railway-carriage factory. Her novel of a couple parted by the Wall is set here",
         "工业城市。克里斯塔·沃尔夫 1959 年到 1962 年住在这里，还在一家车辆厂工作过一段时间。她那部写一对恋人被柏林墙分开的小说，背景就是这座城"),
    ORIG("de-runde-ecke", "'Runde Ecke' Stasi Museum, Leipzig", "“圆角楼”斯塔西博物馆，莱比锡",
         "The Leipzig district headquarters of the Stasi, occupied by demonstrators on 4 December 1989 and kept as a museum with its offices much as they were left. Several of the people Anna Funder talks to are from Leipzig",
         "斯塔西的莱比锡地区总部。1989 年 12 月 4 日被示威者占领，后来辟为博物馆，办公室大体保持着当时的样子。安娜·方德采访的人里有好几位是莱比锡人"),
    ORIG("de-buchenwald", "Buchenwald Memorial", "布痕瓦尔德纪念馆",
         "The concentration camp on the Ettersberg above Weimar, where some 56,000 people died between 1937 and 1945. Bruno Apitz was a prisoner here for eight years and set his novel in the camp's last weeks",
         "魏玛上方埃特斯山上的集中营，1937 年到 1945 年间约有五万六千人死在这里。布鲁诺·阿皮茨在这里被关了八年，他的小说写的是集中营最后的几个星期"),
    ORIG("de-odeonsplatz", "Odeonsplatz, Munich", "音乐厅广场，慕尼黑",
         "The square at the foot of Ludwigstraße, with the Feldherrnhalle and the Theatine church. Thomas Mann's story of 1902 opens with a walk through the radiant, art-mad city towards it",
         "路德维希大街尽头的广场，旁边是统帅堂和铁阿提纳教堂。托马斯·曼 1902 年的这篇小说，开头就是穿过这座光彩照人、为艺术而疯狂的城市向它走去"),
    PIL("de-lmu-lichthof", "White Rose Memorial, University of Munich", "白玫瑰纪念地，慕尼黑大学",
        "On 18 February 1943 Hans and Sophie Scholl laid the group's sixth leaflet outside the lecture rooms and threw the last copies down into the atrium of the main building. A caretaker saw them; four days later they were executed. A memorial room is beside the atrium",
        "1943 年 2 月 18 日，汉斯·朔尔和索菲·朔尔把小组的第六份传单放在各个教室门口，又把剩下的几份从楼上撒进主楼的中庭。一名校工看见了他们；四天后两人被处决。中庭旁设有纪念室",
        ["white-rose-leaflets"]),
    PROTO("de-wertach", "Wertach ('W.')", "韦尔塔赫（“W 村”）",
          "The village in the Allgäu where W. G. Sebald was born in 1944 and lived until he was eight. It is the 'W.' to which the narrator of Vertigo walks back in the book's last part",
          "阿尔高地区的村子，W. G. 塞巴尔德 1944 年生于此，一直住到八岁。《眩晕》最后一部分里，叙述者步行回去的那个“W 村”就是这里"),
]

# ============================== lines ==============================
lines = [
    Q("de-wn-1", "wanderers-nachtlied", "de-kickelhahn", "The whole poem", "全诗", T_EG,
      raw(T_EG, "Ueber allen Gipfeln", "Ruhest du auch."), ["allen Gipfeln"],
      "Over all the hilltops\nis peace,\nin all the treetops\nyou feel\nhardly a breath;\nthe little birds are silent in the wood.\nOnly wait: soon\nyou too will rest.",
      ["all the hilltops"],
      "群峰之巅\n一片寂静，\n所有的树梢上\n你几乎\n感觉不到一丝风；\n林中的小鸟默默无声。\n且等着，不久\n你也将安息。",
      ["群峰之巅"]),
    Q("de-hd-1", "an-heidelberg", "de-heidelberg-old-bridge", "Stanzas 1–2", "第一、二节", T_HD,
      raw(T_HD, "Lange lieb’ ich dich schon", "Die von Wagen und Menschen tönt."), ["die Brücke"],
      "Long have I loved you, and would, for my own delight,\ncall you mother and give you an artless song,\nyou, of all my country's towns\nthe loveliest in its setting that I have seen.\nAs the bird of the forest flies over the peaks,\nso over the river, where it gleams past you,\nswings light and strong the bridge\nthat rings with wagons and people.",
      ["the bridge"],
      "我爱你已久，为了自己高兴，\n真想叫你一声母亲，献给你一首朴拙的歌，\n你啊，在我见过的祖国城市里，\n风光最美的一座！\n像林中的鸟飞越山巅，\n在那条从你身旁闪光流过的河上，\n轻盈而有力地飞架着那座桥，\n车马行人在桥上喧响。",
      ["那座桥"]),
    Q("de-wm-k1", "germany-a-winters-tale", "de-cologne-cathedral", "Caput IV", "第四章", T_WM,
      raw(T_WM, "Doch siehe! dort im Mondenschein", "Die deutsche Vernunft verschmachten!"), ["Dom von Cöllen"],
      "But look! There in the moonlight,\nthat colossal fellow!\nHe looms up devilishly black:\nthat is the cathedral of Cologne.\nIt was meant to be the Bastille of the spirit,\nand the cunning Romanists thought:\nin this gigantic dungeon\nGerman reason will pine away!",
      ["cathedral of Cologne"],
      "可是看哪！月光下\n那个庞然大物！\n它黑得像魔鬼一样耸立着，\n那就是科隆大教堂。\n它本该成为精神的巴士底狱，\n狡猾的罗马信徒们想：\n在这座巨大的牢狱里，\n德意志的理性将会憔悴而死！",
      ["科隆大教堂"]),
    Q("de-wm-ky1", "germany-a-winters-tale", "de-kyffhaeuser", "Caput XIV", "第十四章", T_WM,
      raw(T_WM, "Sie hat mir versichert, er sey nicht todt,", "Die hochgewölbten Sääle."), ["Kiffhäuser"],
      "She assured me he was not dead,\nas the scholars believe;\nhe lives hidden in a mountain\nwith his companions in arms.\nKyffhäuser is the mountain's name,\nand inside it is a cavern;\nthe lamps light up so ghostly\nthe high-vaulted halls.",
      ["Kyffhäuser"],
      "她向我保证，他并没有死，\n不像学者们以为的那样；\n他藏身在一座山里，\n同他的战友们住在一起。\n那座山名叫屈夫霍伊泽，\n山里有一个洞窟；\n灯盏幽幽地照亮\n那些穹顶高耸的大厅。",
      ["屈夫霍伊泽"]),
    Q("de-gz-1", "goetz-von-berlichingen", "de-jagsthausen", "Act 1, 'Jaxthausen. Götz's castle'", "第一幕“雅克斯特豪森·葛兹的城堡”", T_GZ,
      raw(T_GZ, "Karl. Jaxthausen ist ein Dorf", "Karl sieht ihn starr an."), ["Jaxthausen"],
      "KARL. Jaxthausen is a village and castle on the Jaxt, and has belonged for two hundred years to the lords of Berlichingen by inheritance and in their own right.\nGÖTZ. Do you know the lord of Berlichingen?\nKarl stares at him.",
      ["Jaxthausen"],
      "卡尔：雅克斯特豪森是雅克斯特河边的一个村子和一座城堡，两百年来世世代代归贝利欣根家的老爷们所有。\n葛兹：你认识贝利欣根老爷吗？\n卡尔呆呆地看着他。",
      ["雅克斯特豪森"]),
    Q("de-gt-1", "the-golden-pot", "de-dresden-albertplatz", "First Vigil", "第一夜", T_GT,
      raw(T_GT, "Am Himmelfahrtstage, Nachmittags um drei Uhr", "zugeworfen."), ["Schwarze Thor"],
      "On Ascension Day, at three in the afternoon, a young man ran through the Black Gate in Dresden and straight into a basket of apples and cakes that an ugly old woman was offering for sale, so that everything that had happily escaped being crushed was flung out, and the street urchins merrily shared the booty the hasty gentleman had thrown them.",
      ["Black Gate"],
      "升天节那天下午三点钟，一个年轻人在德累斯顿跑过黑门，一头撞进一个丑老太婆摆着卖的一篮苹果和糕饼里，没被压烂的全给撞飞了出去，街上的顽童们高高兴兴地分掉了这位冒失先生抛给他们的战利品。",
      ["黑门"]),
    Q("de-at-1", "am-turme", "de-meersburg", "Stanza 1", "第一节", T_AT,
      raw(T_AT, "Ich steh’ auf hohem Balkone am Thurm,", "Auf Tod und Leben dann ringen!"), ["Balkone am Thurm"],
      "I stand on the high balcony of the tower,\nthe shrieking starling sweeping round me,\nand like a maenad I let the storm\ntear at my streaming hair;\nO wild fellow, O mad young blade,\nI would throw my arms tight around you\nand, sinew to sinew, two steps from the edge,\nwrestle with you for life or death!",
      ["balcony of the tower"],
      "我站在塔楼高高的阳台上，\n尖叫的椋鸟在身边掠过，\n我像酒神的女祭司，任凭风暴\n撕扯我飞扬的头发；\n啊，狂野的伙伴，疯癫的小子，\n我真想紧紧抱住你，\n筋骨相抵，离边缘两步，\n同你拼个你死我活！",
      ["塔楼高高的阳台"]),
    Q("de-ds-1", "die-stadt-storm", "de-storm-husum", "The whole poem", "全诗", T_DS,
      raw(T_DS, "Am grauen Strand, am grauen Meer", "Du graue Stadt am Meer."), ["graue Stadt am Meer"],
      "By the grey shore, by the grey sea,\nand off to one side, lies the town;\nthe fog weighs heavy on the roofs,\nand through the stillness the sea roars\nmonotonously round the town.\nNo forest rustles, no bird sings\nin May without a pause;\nonly the wild goose with its harsh cry\nflies past on autumn nights,\nand on the shore the grass blows.\nYet my whole heart clings to you,\nyou grey town by the sea;\nthe magic of youth for ever and ever\nrests smiling still on you, on you,\nyou grey town by the sea.",
      ["grey town by the sea"],
      "在灰色的海滩，灰色的大海旁，\n偏在一边，坐落着这座城；\n雾沉沉地压着屋顶，\n大海穿过寂静，\n单调地绕城喧响。\n没有森林的涛声，五月里\n也没有鸟儿不停地歌唱；\n只有大雁带着刺耳的叫声\n在秋夜里飞过，\n海滩上野草飘荡。\n可我的整颗心都系在你身上，\n你这海边的灰色的城；\n青春的魔力永远永远\n仍微笑着留在你身上，你身上，\n你这海边的灰色的城。",
      ["海边的灰色的城"]),
    Q("de-rb-1", "herr-von-ribbeck", "de-ribbeck", "Lines 1–10", "第 1—10 行", T_RB,
      raw(T_RB, "Herr von Ribbeck auf Ribbeck im Havelland,\nEin Birnbaum", "ick hebb’ ne Birn.“"), ["Ribbeck im Havelland"],
      "Squire von Ribbeck at Ribbeck in Havelland,\na pear tree in his garden stood,\nand when the golden autumn came\nand the pears shone far and wide,\nthen, when noon rang from the tower,\nvon Ribbeck stuffed both his pockets full,\nand if a boy came by in clogs\nhe called: 'Lad, d'you want a pear?'\nAnd if a girl came, he called: 'Little lass,\ncome over here, I've got a pear.'",
      ["Ribbeck in Havelland"],
      "哈弗尔兰的里贝克村有位冯·里贝克老爷，\n他的园子里长着一棵梨树，\n每到金色的秋天，\n梨子四下里闪闪发亮，\n钟楼敲响正午的钟声，\n冯·里贝克就把两个口袋塞得满满，\n要是有个穿木屐的男孩走过，\n他就喊：“小子，要个梨不？”\n要是来了个女孩，他就喊：“小丫头，\n过来吧，我这儿有梨。”",
      ["哈弗尔兰的里贝克村"]),
    Q("de-jb-1", "the-jews-beech", "de-bellersen", "Opening", "开头", T_JB,
      raw(T_JB, "Friedrich Mergel, geboren 1738", "geschichtlich merkwürdigen Gebirges."), ["Dorfe B."],
      "Friedrich Mergel, born in 1738, was the only son of a so-called half-farmer, or landowner of the lower class, in the village of B., which, badly built and smoky as it may be, yet catches every traveller's eye by the extremely picturesque beauty of its position in the green wooded gorge of a considerable and historically notable range of hills.",
      ["village of B."],
      "弗里德里希·梅格尔生于 1738 年，是 B 村一个所谓“半份农”即下等地主的独生子。这个村子尽管房屋简陋、烟熏火燎，却因为坐落在一条有名的、在历史上颇值得一提的山脉的绿色林谷里，景色格外如画，吸引着每一个过路人的目光。",
      ["B 村"]),
]

# Byron wrote in English: the stanza is the original; the editor's note mark after "Drachenfels" is left out.
_b = raw(T_CH, "The castled Crag of DrachenfelsN10\nFrowns", "With double joy wert thou with me.", "en")
assert _b.count("N10") == 1 and "[" not in _b
_b = _b.replace("DrachenfelsN10", "Drachenfels")
lines.append(dict(id="de-byron-1", book_id=BYRON, place_ids=["de-drachenfels"], location="Canto III, the song after stanza 55", location_zh="第三章第 55 节后的歌",
                  text_en=_b, highlight_en=["Drachenfels"], translation="original",
                  text_zh="德拉亨费尔斯的峭壁上城堡高踞，\n俯视着宽阔蜿蜒的莱茵河，\n河水的胸膛浩荡地鼓起，\n两岸是结满葡萄的山坡，\n山丘上开满花的树木繁茂，\n田野预示着谷物和美酒，\n散落的城镇点缀其间，\n远处的白墙沿岸闪耀，\n铺展成一片风景——若有你在身旁，\n我看它时会加倍欢畅。",
                  highlight_zh=["德拉亨费尔斯"], status="draft",
                  checked=f"English Wikisource, {T_CH} (the editor's note mark left out), {DATE}"))

lines += [
    S("de-hz-s1", "harzreise", "de-goettingen-rathaus", "Opening", "开头",
      "Heine begins his walking tour by taking leave of Göttingen: a town famous, he says, for its sausages and its university, whose inhabitants he sorts into students, professors, philistines and cattle. Then he shoulders his knapsack and sets out for the mountains.",
      "海涅的徒步旅行从告别哥廷根写起：他说这座城以香肠和大学闻名，城里的居民可以分成大学生、教授、市侩和牲口四类。然后他背起行囊，向山里走去。",
      ["Göttingen"], ["哥廷根"], W + "Die_Harzreise"),
    S("de-ph-s1", "prince-of-homburg", "de-fehrbellin", "Acts 2 and 5", "第二幕和第五幕",
      "The young prince, dreaming of glory, does not hear his orders, charges too soon at Fehrbellin and helps win the battle. The Elector has him court-martialled and condemned for disobedience, and only when the prince accepts the sentence as just is he pardoned.",
      "年轻的亲王一心梦想荣誉，没有听清命令，在费尔贝林提前发起冲锋，帮着打赢了这一仗。选帝侯却把他交军事法庭，以抗命罪判了死刑；直到亲王自己承认判决公正，才得到赦免。",
      ["Fehrbellin"], ["费尔贝林"], W + "The_Prince_of_Homburg_(play)"),
    S("de-lw-s1", "lotte-in-weimar", "de-hotel-elephant", "Chapter 1", "第一章",
      "One morning in September 1816 the mail coach sets down three women at the Elephant. The waiter Mager, reading the register, realises that the elderly lady from Hanover is Werther's Lotte, and before she has unpacked, half of Weimar is on its way to look at her.",
      "1816 年 9 月的一个早晨，驿车在大象旅馆门前放下三位女客。茶房马格尔看了登记簿，认出这位从汉诺威来的老太太就是维特的绿蒂；她行李还没打开，半个魏玛城的人已经赶来看她了。",
      ["the Elephant"], ["大象旅馆"], W + "Lotte_in_Weimar:_The_Beloved_Returns"),
    S("de-ng-s1", "narcissus-and-goldmund", "de-maulbronn", "Chapter 1", "第一章",
      "The book begins with the old chestnut tree at the gate of the monastery of Mariabronn. The boy Goldmund is brought there by his father to become a monk and attaches himself to the young teacher Narcissus, who sees that his friend is made for the world outside and tells him so.",
      "小说从玛利亚布隆修道院大门口那棵老栗子树写起。少年歌尔德蒙被父亲送来，准备将来当修士，他依恋上了年轻的教师纳尔齐斯；纳尔齐斯却看出这位朋友属于外面的世界，并把这话告诉了他。",
      ["Mariabronn"], ["玛利亚布隆"], W + "Narcissus_and_Goldmund"),
    S("de-be-s1", "buckow-elegies", "de-buckow", "The cycle", "组诗",
      "Written in the weeks after the workers' rising of 17 June 1953, the poems are a few plain lines each: smoke from a house by the lake, a man waiting while his driver changes a wheel, the garden, the firs at dawn. The sharpest of them, on the government and the people, was not printed in East Germany in his lifetime.",
      "这些诗写于 1953 年 6 月 17 日工人起义之后的几个星期，每首只有寥寥几行朴素的句子：湖边房子升起的炊烟，等着司机换车轮的人，花园，黎明时的冷杉。其中最尖锐的一首写的是政府与人民，在他生前没有在东德发表。",
      ["by the lake"], ["湖边"], DEW + "Buckower_Elegien"),
    S("de-rh-s1", "rheinsberg", "de-rheinsberg", "The whole story", "全篇",
      "Claire and Wolfgang, not married and pretending to be, take the train from Berlin for three days in Rheinsberg. They row on the lake, are shown round the palace by a castellan, tease each other in Claire's private baby-talk, and go home. Almost nothing happens, and that lightness made the little book a bestseller.",
      "克莱尔和沃尔夫冈没有结婚，却冒充夫妻，从柏林坐火车到莱茵斯贝格玩了三天。他们在湖上划船，由管理员领着参观宫殿，用克莱尔自创的娃娃腔互相打趣，然后回家。几乎什么事也没发生，而正是这份轻盈让这本小书成了畅销书。",
      ["Rheinsberg"], ["莱茵斯贝格"], DEW + "Rheinsberg:_Ein_Bilderbuch_für_Verliebte"),
    S("de-me-s1", "mephisto", "de-gendarmenmarkt", "The later chapters", "后半部",
      "Hendrik Höfgen, a provincial actor with left-wing friends, makes his name playing Mephisto. When the Nazis come to power he lets the prime minister, a fat man who loves the theatre, become his patron, drops those who could compromise him, and ends as director of the State Theatre in Berlin.",
      "亨德里克·赫夫根原是个结交左派朋友的外省演员，靠扮演梅菲斯特成名。纳粹上台后，他让那位爱看戏的胖总理当了自己的靠山，甩掉一切可能连累他的人，最后当上了柏林国家剧院的院长。",
      ["the State Theatre in Berlin"], ["柏林国家剧院"], W + "Mephisto_(novel)"),
    S("de-mo-s1", "the-man-outside", "de-landungsbruecken", "Prologue and 'The Dream'", "序幕和“梦”",
      "Beckmann, a sergeant back from three years as a prisoner in Siberia with a stiff knee and gas-mask glasses, finds another man in his wife's bed and throws himself into the Elbe from a pontoon at St. Pauli. The river, an old woman who has no patience with him, spits him out again on the sand at Blankenese.",
      "下士贝克曼在西伯利亚当了三年战俘，带着一条僵直的腿和一副防毒面具眼镜回到家，发现妻子床上躺着别的男人，就从圣保利的一座浮桥上跳进了易北河。易北河是个对他毫无耐心的老太婆，又把他吐回到布兰克内泽的沙滩上。",
      ["a pontoon at St. Pauli"], ["圣保利的一座浮桥"], W + "The_Man_Outside"),
    S("de-gl-s1", "the-german-lesson", "de-seebuell", "The essay Siggi writes", "西吉写的那篇作文",
      "In 1943 the policeman of Rugbüll, the northernmost police post in Germany, is ordered to deliver a ban on painting to his neighbour and old friend, the painter Nansen, and to see that it is kept. His son Siggi, who hides the pictures, tells the story years later in a reformatory, set to write an essay on 'The Joys of Duty'.",
      "1943 年，德国最北端的警察哨所鲁格比尔的警察奉命把一纸禁画令送给邻居兼老友、画家南森，并监督执行。他的儿子西吉把那些画藏了起来；多年后，西吉在少年教养所里被罚写一篇题为《尽职的快乐》的作文，讲出了这段往事。",
      ["Rugbüll"], ["鲁格比尔"], W + "The_German_Lesson"),
    S("de-tt-s1", "the-meeting-at-telgte", "de-telgte", "The whole tale", "全篇",
      "In the summer of 1647 the Königsberg poet Simon Dach calls the scattered poets of Germany together. Turned away from their first inn, they are quartered at the Bridge Inn in Telgte by a soldier called Gelnhausen, read their manuscripts to one another for three days and draft an appeal for peace. The inn burns down, and the appeal with it.",
      "1647 年夏天，柯尼斯堡诗人西蒙·达赫把散居各地的德意志诗人召集到一起。第一家客栈不收留他们，一个名叫盖尔恩豪森的士兵把他们安顿在特尔格特的桥头客栈。他们互相朗读手稿三天，还起草了一份和平呼吁书。客栈起火烧毁，呼吁书也一同化为灰烬。",
      ["Telgte"], ["特尔格特"], W + "The_Meeting_at_Telgte"),
    S("de-dh-s1", "divided-heaven", "de-halle", "The whole novel", "全书",
      "Rita Seidel, training to be a teacher, works in a brigade at the railway-carriage works; Manfred, the chemist she lives with, grows bitter when his invention is turned down. In the summer of 1961 he goes to West Berlin. She visits him once, comes back, and after the Wall is built she collapses between two moving wagons at the works.",
      "正在读师范的丽塔·赛德尔在车辆厂的一个生产队里劳动；同她一起生活的化学家曼弗雷德因为发明被否决而日渐消沉。1961 年夏天，他去了西柏林。她去看过他一次，又回来了；柏林墙建起之后，她在厂里两节移动的车皮之间昏倒。",
      ["the railway-carriage works"], ["车辆厂"], DEW + "Der_geteilte_Himmel"),
    S("de-an-s1", "anniversaries", "de-kluetz", "The whole novel", "全书",
      "Day by day from August 1967 to August 1968, Gesine Cresspahl, a bank employee on Riverside Drive in New York, reads the New York Times and tells her ten-year-old daughter Marie about the small Mecklenburg town of Jerichow: her father the cabinet-maker, the Nazi years, the Soviet occupation and the early GDR.",
      "从 1967 年 8 月到 1968 年 8 月，一天接一天，住在纽约河滨大道的银行职员格西内·克雷斯帕尔读着《纽约时报》，给十岁的女儿玛丽讲梅克伦堡小城耶里肖的往事：做细木工的父亲，纳粹年代，苏军占领，还有民主德国的最初岁月。",
      ["Jerichow"], ["耶里肖"], W + "Anniversaries_(novel)"),
    S("de-vs-s1", "vertigo-sebald", "de-wertach", "Part 4, 'Il ritorno in patria'", "第四部分《归乡》",
      "In November 1987 the narrator comes over the pass from Austria on foot and walks down through the gorge to W., the village he has not seen since childhood. He takes a room at the inn where his family once lived and goes over the people and houses of the place as they were when he was a boy.",
      "1987 年 11 月，叙述者从奥地利徒步翻过山口，穿过峡谷走下来，回到自童年以后就没再见过的 W 村。他在全家当年住过的那家旅店里要了一个房间，把村里的人和房子按自己小时候的样子一一回想了一遍。",
      ["W."], ["W 村"], DEW + "Schwindel._Gefühle."),
    S("de-vi-s1", "visitation", "de-scharmuetzelsee", "The whole novel", "全书",
      "A plot of land by a Brandenburg lake passes from a farmer's daughters to a Berlin architect, who builds a summer house on it. His Jewish neighbours sell up and are murdered; a young Red Army soldier is quartered in the house; a writer back from exile is given it by the state; her granddaughter loses it after 1990. Only the gardener is there through all of it.",
      "勃兰登堡一个湖边的一块地，从农家女儿们手里转给了一位柏林建筑师，他在上面盖了一幢消夏别墅。他的犹太邻居卖掉产业后遭到杀害；一个年轻的红军士兵在房子里驻扎过；一位流亡归来的女作家从国家手里得到了它；1990 年以后，她的孙女又失去了它。自始至终都在的只有那个园丁。",
      ["a Brandenburg lake"], ["勃兰登堡一个湖边"], DEW + "Heimsuchung_(Roman)"),
    S("de-kr-s2", "kruso", "de-hiddensee", "The whole novel", "全书",
      "In the summer of 1989 the student Ed, running from a loss, takes the ferry to Hiddensee and is hired as a dishwasher at the Klausner, an inn on the cliff. Its unofficial captain is Kruso, who shelters the 'shipwrecked' of the country, people who hope to swim for Denmark, and wants to teach them a freedom that needs no escape. By autumn the staff are leaving one by one for the opened border.",
      "1989 年夏天，大学生埃德为了逃开失去亲近之人的痛苦，乘渡船来到希登塞岛，在崖上的克劳斯纳旅店当了洗碗工。旅店里不挂名的头领是克鲁索，他收留这个国家的“海难者”——那些指望游到丹麦去的人，想教给他们一种不必出逃的自由。到了秋天，店里的人一个接一个奔向已经打开的边境。",
      ["Hiddensee"], ["希登塞岛"], DEW + "Kruso"),
    S("de-sa-s1", "sonnenallee", "de-sonnenallee", "The whole novel", "全书",
      "Micha Kuppisch and his friends are fifteen, live in the flats at the short end of the Sonnenallee, in sight of the western viewing platform, and are all in love with Miriam. Micha's first love letter from her is blown unread into the death strip, and most of the book is his campaign to get it back.",
      "米夏·库皮施和他的朋友们十五岁，住在太阳大道较短那一头的公寓楼里，抬头就能看见西边的瞭望台，而且个个都爱着米丽亚姆。她写给米夏的第一封情书还没拆开就被风吹进了死亡地带，全书大半篇幅就是他想方设法要把信弄回来。",
      ["the short end of the Sonnenallee"], ["太阳大道较短那一头"], DEW + "Am_kürzeren_Ende_der_Sonnenallee"),
    S("de-sl-s1", "stasiland", "de-runde-ecke", "The Leipzig chapters", "莱比锡部分",
      "Funder, an Australian working in Berlin in the 1990s, goes looking for people who resisted the Stasi and people who worked for it. In Leipzig she meets Miriam, who at sixteen was arrested for pasting up leaflets, got as far as the last fence of the Berlin Wall on her own, and is still trying to learn how her husband died in a Stasi cell.",
      "澳大利亚人方德 1990 年代在柏林工作，开始寻访当年反抗过斯塔西的人和为斯塔西工作过的人。在莱比锡她见到了米丽亚姆：十六岁因张贴传单被捕，后来独自翻到了柏林墙的最后一道铁丝网前，如今仍在追查丈夫是怎样死在斯塔西牢房里的。",
      ["Leipzig"], ["莱比锡"], W + "Stasiland"),
    S("de-ch-s1", "caspar-hauser", "de-ansbach", "The Ansbach chapters", "安斯巴赫部分",
      "Passed from one guardian to the next, the gentle foundling is brought to Ansbach and put in the house of the pedantic schoolmaster Quandt, who is set on proving him a fraud. Lured into the court garden on a snowy December afternoon by a stranger who promises news of his mother, he is stabbed, and even on his deathbed is not believed.",
      "这个温顺的弃儿从一个监护人手里转到另一个监护人手里，最后被带到安斯巴赫，安置在迂腐的教师克万特家里，而克万特一心要证明他是个骗子。十二月一个下雪的下午，一个陌生人谎称有他母亲的消息，把他骗进宫廷花园，刺了他一刀；直到临终，人们还是不相信他。",
      ["Ansbach", "the court garden"], ["安斯巴赫", "宫廷花园"], DEW + "Caspar_Hauser_oder_Die_Trägheit_des_Herzens"),
    S("de-nw-s1", "naked-among-wolves", "de-buchenwald", "The whole novel", "全书",
      "Early in 1945 a Polish prisoner arrives at Buchenwald with a three-year-old Jewish boy hidden in his suitcase. The prisoners of the storeroom hide the child, moving him from hut to hut while the SS search, although every hiding place puts the camp's secret resistance and its plans for a rising at risk.",
      "1945 年初，一个波兰囚犯带着藏在手提箱里的三岁犹太男孩来到布痕瓦尔德。储藏室的囚犯们把孩子藏了起来，在党卫军搜查时把他从一个棚屋转移到另一个棚屋，尽管每一个藏身之处都会危及营里的秘密抵抗组织和起义计划。",
      ["Buchenwald"], ["布痕瓦尔德"], W + "Naked_Among_Wolves_(novel)"),
    S("de-gd-s1", "gladius-dei", "de-odeonsplatz", "The whole story", "全篇",
      "On a brilliant June day a gaunt young man in a hooded cloak, Hieronymus, walks down from Schwabing through the cheerful crowds. In the window of a fine-art dealer's by Odeonsplatz hangs the reproduction of a sensual Madonna that the whole town admires. He goes in and demands that it be burned, and the packer throws him out into the square.",
      "六月里阳光灿烂的一天，瘦削的年轻人希罗尼穆斯披着带兜帽的斗篷，从施瓦宾区穿过欢快的人群走来。音乐厅广场旁一家艺术品商店的橱窗里挂着一幅肉感的圣母像的复制品，全城人都在赞赏。他走进去，要求把它烧掉，结果被店里的打包工扔到了广场上。",
      ["Odeonsplatz"], ["音乐厅广场"], DEW + "Gladius_Dei"),
    S("de-cf-s1", "christiane-f", "de-bahnhof-zoo", "The whole book", "全书",
      "Christiane grows up in the tower blocks of Gropiusstadt, starts on pills and hashish at twelve at a church youth club, and at fourteen is injecting heroin and earning the money for it around Bahnhof Zoo, where her friends are dying one after another. Two reporters from Stern recorded her account, and the book came out in 1978.",
      "克里斯蒂安娜在格罗皮乌斯城的高楼群里长大，十二岁在教会的青少年活动中心开始接触药片和大麻，十四岁已经在注射海洛因，并在动物园火车站一带挣买毒品的钱，身边的朋友一个接一个地死去。《明星》周刊的两名记者记录下了她的讲述，书在 1978 年出版。",
      ["Bahnhof Zoo"], ["动物园火车站"], DEW + "Wir_Kinder_vom_Bahnhof_Zoo"),
]

# ============================== checks, then append ==============================
ids = lambda name: set(re.findall(r'\{ id: "([^"]+)"', open(b.data(name), encoding="utf-8").read()))
old_books, old_places, old_lines = ids("books.js"), ids("places.js"), ids("lines.js")
new_b, new_p, new_l = {x["id"] for x in books}, {x["id"] for x in places}, {x["id"] for x in lines}
assert len(new_b) == len(books) and len(new_p) == len(places) and len(new_l) == len(lines)
assert not new_b & old_books, new_b & old_books
assert not new_p & old_places, new_p & old_places
assert not new_l & old_lines, new_l & old_lines
assert new_p == set(CO), new_p ^ set(CO)
bids, pids = new_b | old_books | {BYRON, "pl-weber"}, new_p | old_places
for l in lines:
    assert l["book_id"] in bids, l["id"]
    assert all(p in pids for p in l["place_ids"]), l["id"]
used = {p for l in lines for p in l["place_ids"]}
for p in places:
    assert p["id"] in used or p.get("book_ids"), ("place without a line or a book", p["id"])
    assert all(i in bids for i in p.get("book_ids", [])), p["id"]
covered = {l["book_id"] for l in lines} | {i for p in places for i in p.get("book_ids", [])}
assert not new_b - covered, new_b - covered

if __name__ == "__main__":
    M = "11-23: second pack (tools/content/batches/add_de1.py)"
    b.append(b.data("books.js"), books, M)
    b.append(b.data("places.js"), places, M)
    b.append(b.data("lines.js"), lines, M)
    print(len(books), "books,", len(places), "places,", len(lines), "lines (", sum(1 for l in lines if l.get("kind") != "scene"), "quotations )")
