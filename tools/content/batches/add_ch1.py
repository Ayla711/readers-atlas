"""11-23: Switzerland, first pack: 27 new books and 17 books already on other countries' lists, 41 places.
Schiller's Tell at the Rütli and the Hohle Gasse; Byron at Chillon, on the Jungfrau and at Clarens; Rousseau on the
Île Saint-Pierre; Goethe on Lake Zurich; Gotthelf's Emmental; the English and American travellers (Dickens, Wordsworth,
Twain, James, Conan Doyle); Tolstoy at Lucerne; the Swiss classics and moderns (Spyri, Keller, Meyer, Walser, Ramuz,
Dürrenmatt, Frisch) and the foreign writers who lived and are buried here (Rilke, Hesse, Joyce, Borges, Mann,
Remarque, Nabokov, Highsmith). Fictional settings hang on the real place the book names or is drawn from, and the
note says which.

Quotations (15 lines) are cut from Wikisource pages (tools/content/wikisource.py): German, French, Russian and
English Wikisource; translations of the German, French and Russian are our own drafts (translation: "own"). Books in
copyright, and two books whose text we could not reach, have scene notes in our own words. What a cut changes, named
in `checked`: the edition's page marks and line numbers are left out; one note mark in Byron is left out; hard-wrapped
French is re-flowed; no-break spaces are written as spaces; verse indents are dropped.

Coordinates are those of the place's German, French, Italian or English Wikipedia article (cache/ch/coords.json).

Usage: python3 -I add_ch1.py <app_dir> <coords.json> <wikisource_root>"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b
import wikisource as ws

APP, CO, WSR = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8")), sys.argv[3]
DATE = "2026-11-23"
b.init(APP, "", "ch", DATE)
W = b.W
DEW = "https://de.wikipedia.org/wiki/"
FRW = "https://fr.wikipedia.org/wiki/"
GAP = b.GAP

def BK(id, title, title_zh, title_orig, author, author_zh, author_orig, year, pd=True, **kw):
    d = dict(id=id, title=title, title_zh=title_zh, title_orig=title_orig, author=author, author_zh=author_zh, year=year,
             orig_lang=kw.pop("lang", "de"), public_domain=pd, source_url=kw.pop("src", None), author_orig=author_orig)
    d.update(kw)
    return {k: v for k, v in d.items() if v is not None or k == "source_url"}

def C(pid):
    c = CO[pid]
    return c["lat"], c["lon"], c["st"], c["su"]

def ORIG(pid, name, zh, en_note, zh_note, **kw): return b.ORIG(pid, name, zh, *C(pid), en_note, zh_note, **kw)
def PIL(pid, name, zh, en_note, zh_note, ids, **kw): return b.PIL(pid, name, zh, *C(pid), en_note, zh_note, ids, **kw)
S = b.S

def raw(title, start, end, lang="de"):
    """the page's own text between two markers; the markers are matched with no-break and thin spaces read as spaces"""
    t = ws.text(os.path.join(WSR, lang), title)
    n = re.sub("[\xa0   ]", " ", t)
    i = n.find(start)
    assert i >= 0, (title, start)
    j = n.find(end, i)
    assert j >= 0, (title, start, end)
    return t[i:j + len(end)]

def flow(s):
    """a hard-wrapped page: lines joined, doubled spaces written as one"""
    return re.sub(r" {2,}", " ", s.replace("\n", " "))

def drop(s, mark):
    """leave out one page mark or line number the edition prints inside the text"""
    assert s.count(mark) == 1, (mark, s[:40])
    return s.replace(mark, "")

def Q(id, book, place, loc, loc_zh, site, title, orig, hl_orig, en, hl_en, zh, hl_zh, note=""):
    if re.search("[\xa0   ]", orig):
        orig = re.sub("[\xa0   ]+", " ", orig)
        orig = re.sub(r" {2,}", " ", orig)
        note += " (no-break and thin spaces written as plain spaces)"
    if re.search(r"(?m)^ +", orig):
        orig = re.sub(r"(?m)^ +", "", orig)
        note += " (verse indent dropped)"
    for text, hls in ((orig, hl_orig), (en, hl_en), (zh, hl_zh)):
        for h in hls:
            assert h in text, (id, h)
    assert "  " not in orig and "[" not in orig, (id, "spacing or page mark")
    return dict(id=id, book_id=book, place_ids=[place], location=loc, location_zh=loc_zh,
                text_orig=orig, highlight_orig=hl_orig, text_en=en, highlight_en=hl_en, text_zh=zh, highlight_zh=hl_zh, translation="own",
                status="draft", checked=f"{site} Wikisource, {title}{note}, {DATE}")

def EN(id, book, place, loc, loc_zh, title, text, hl, zh, hl_zh, note=""):
    assert "[" not in text and "\xa0" not in text and "  " not in text and " " not in text, (id, text[:40])
    for h in hl: assert h in text, (id, h)
    for h in hl_zh: assert h in zh, (id, h)
    return dict(id=id, book_id=book, place_ids=[place], location=loc, location_zh=loc_zh, text_en=text, highlight_en=hl, translation="original",
                text_zh=zh, highlight_zh=hl_zh, status="draft", checked=f"English Wikisource, {title}{note}, {DATE}")

DE, FR, RU = "German", "French", "Russian"
T_TELL2, T_TELL4 = "Wilhelm Tell/Zweiter Aufzug", "Wilhelm Tell/Vierter Aufzug"
T_SPIN, T_SEE = "Die schwarze Spinne", "Auf dem See"
T_REV, T_LUZ = "Les Rêveries du promeneur solitaire/Cinquième Promenade", "Люцерн (Толстой)"
T_CHIL = "The Works of Lord Byron (ed. Coleridge, Prothero)/Poetry/Volume 4/The Prisoner of Chillon"
T_CH3 = "The Works of Lord Byron (ed. Coleridge, Prothero)/Poetry/Volume 2/Childe Harold's Pilgrimage/Canto III"
T_MANF = "Manfred, a dramatic poem/Act 1 Scene 2"
T_FP = "The Strand Magazine/Volume 6/Issue 36/The Adventure of the Final Problem"
T_DM = "Daisy Miller: A Study (unsourced edition)/Part 1"
T_LD = "Little Dorrit/Book 2/Chapter 1"
T_PREL = "The Prelude (Wordsworth)/Book VI"
T_FRANK = "Frankenstein, or the Modern Prometheus (Revised Edition, 1831)/Chapter 7"
T_TRAMP = "A Tramp Abroad/XXVIII"
SCHILLER = ("Friedrich Schiller", "席勒")
BYRON_ = ("Lord Byron", "拜伦")

# books already on another country's list, used here
BYRON, FRANK, TRAMP = "pt-childe-harold", "frankenstein", "a-tramp-abroad"
EXIST = {BYRON, FRANK, TRAMP, "pt-night-train", "the-magic-mountain", "thus-spoke-zarathustra", "ulysses", "el-aleph", "ficciones",
         "fr-candide", "speak-memory", "farewell-to-arms", "talented-mr-ripley", "all-quiet-on-the-western-front", "buddenbrooks",
         "steppenwolf", "narcissus-and-goldmund"}

books = [
    BK("wilhelm-tell", "William Tell", "威廉·退尔", "Wilhelm Tell", *SCHILLER, "Friedrich Schiller", "1804", src=ws.url("de", "Wilhelm Tell"),
       aliases=["Wilhelm Tell", "Tell", "Rütlischwur", "Rütli oath", "Gessler", "Hohle Gasse", "退尔"]),
    BK("prisoner-of-chillon", "The Prisoner of Chillon", "西庸的囚徒", None, *BYRON_, "Lord Byron", "1816", lang="en", src=ws.url("en", T_CHIL),
       aliases=["Chillon", "Bonivard", "Bonnivard", "锡隆的囚徒"]),
    BK("manfred", "Manfred", "曼弗雷德", None, *BYRON_, "Lord Byron", "1817", lang="en", src=ws.url("en", "Manfred, a dramatic poem"),
       aliases=["Manfred: A Dramatic Poem", "Jungfrau", "曼佛雷德"]),
    BK("reveries-solitary-walker", "Reveries of the Solitary Walker", "一个孤独漫步者的遐想", "Les Rêveries du promeneur solitaire", "Jean-Jacques Rousseau", "卢梭",
       "Jean-Jacques Rousseau", "1782", lang="fr", src=ws.url("fr", "Les Rêveries du promeneur solitaire"),
       aliases=["Rêveries du promeneur solitaire", "Fifth Walk", "Cinquième Promenade", "Île Saint-Pierre", "St. Petersinsel", "孤独漫步者的遐想"]),
    BK("auf-dem-see", "On the Lake", "在湖上", "Auf dem See", "Johann Wolfgang von Goethe", "歌德", "Johann Wolfgang von Goethe", "1789", src=ws.url("de", T_SEE),
       aliases=["Auf dem See", "Zürichsee", "Lake Zurich", "Goethe"]),
    BK("black-spider", "The Black Spider", "黑蜘蛛", "Die schwarze Spinne", "Jeremias Gotthelf", "耶雷米亚斯·戈特赫尔夫", "Jeremias Gotthelf", "1842",
       src=ws.url("de", T_SPIN), aliases=["Die schwarze Spinne", "Gotthelf", "Emmental", "Sumiswald", "Hans von Stoffeln"]),
    BK("final-problem", "The Final Problem", "最后一案", None, "Arthur Conan Doyle", "柯南·道尔", "Arthur Conan Doyle", "1893", lang="en",
       src=ws.url("en", T_FP), aliases=["The Adventure of the Final Problem", "Sherlock Holmes", "Moriarty", "Reichenbach", "福尔摩斯", "最后的难题"]),
    BK("daisy-miller", "Daisy Miller", "黛西·米勒", None, "Henry James", "亨利·詹姆斯", "Henry James", "1878", lang="en",
       src=ws.url("en", "Daisy Miller: A Study (unsourced edition)"), aliases=["Daisy Miller: A Study", "Winterbourne", "Vevey", "苔丝·密勒"]),
    BK("lucerne-tolstoy", "Lucerne", "卢塞恩", "Люцерн", "Leo Tolstoy", "列夫·托尔斯泰", "Лев Толстой", "1857", lang="ru", src=ws.url("ru", T_LUZ),
       aliases=["Luzern", "Люцерн", "Schweizerhof", "Nekhlyudov", "琉森"]),
    BK("little-dorrit", "Little Dorrit", "小杜丽", None, "Charles Dickens", "查尔斯·狄更斯", "Charles Dickens", "1855–1857", lang="en",
       src=ws.url("en", "Little Dorrit"), aliases=["Amy Dorrit", "Marshalsea", "Great Saint Bernard", "小杜丽特"]),
    BK("the-prelude", "The Prelude", "序曲", None, "William Wordsworth", "威廉·华兹华斯", "William Wordsworth", "1850", lang="en",
       src=ws.url("en", "The Prelude (Wordsworth)"), aliases=["Prelude", "Wordsworth", "Simplon", "crossing the Alps"]),
    BK("heidi", "Heidi", "海蒂", "Heidi", "Johanna Spyri", "约翰娜·施皮里", "Johanna Spyri", "1880–1881",
       aliases=["Heidis Lehr- und Wanderjahre", "Alm-Öhi", "Alm-Uncle", "Maienfeld", "Dörfli", "小海蒂", "阿尔卑斯山的少女"]),
    BK("kleider-machen-leute", "Clothes Make the Man", "人靠衣装", "Kleider machen Leute", "Gottfried Keller", "戈特弗里德·凯勒", "Gottfried Keller", "1874",
       aliases=["Kleider machen Leute", "Seldwyla", "Goldach", "Wenzel Strapinski", "衣冠楚楚"]),
    BK("green-henry", "Green Henry", "绿衣亨利", "Der grüne Heinrich", "Gottfried Keller", "戈特弗里德·凯勒", "Gottfried Keller", "1855",
       aliases=["Der grüne Heinrich", "Heinrich Lee", "绿衣亨利希"]),
    BK("duino-elegies", "Duino Elegies", "杜伊诺哀歌", "Duineser Elegien", "Rainer Maria Rilke", "里尔克", "Rainer Maria Rilke", "1923",
       aliases=["Duineser Elegien", "Rilke", "Muzot", "Sonnets to Orpheus", "致奥尔弗斯的十四行诗"]),
    BK("judge-and-his-hangman", "The Judge and His Hangman", "法官和他的刽子手", "Der Richter und sein Henker", "Friedrich Dürrenmatt", "迪伦马特",
       "Friedrich Dürrenmatt", "1950", pd=False, aliases=["Der Richter und sein Henker", "Bärlach", "Tschanz", "Gastmann", "Twann", "Lamboing"]),
    BK("the-visit", "The Visit", "老妇还乡", "Der Besuch der alten Dame", "Friedrich Dürrenmatt", "迪伦马特", "Friedrich Dürrenmatt", "1956", pd=False,
       aliases=["Der Besuch der alten Dame", "The Visit of the Old Lady", "Claire Zachanassian", "Güllen"]),
    BK("man-in-the-holocene", "Man in the Holocene", "人类出现于全新世", "Der Mensch erscheint im Holozän", "Max Frisch", "马克斯·弗里施", "Max Frisch",
       "1979", pd=False, aliases=["Der Mensch erscheint im Holozän", "Herr Geiser", "Frisch", "Ticino"]),
    BK("siddhartha", "Siddhartha", "悉达多", "Siddhartha", "Hermann Hesse", "赫尔曼·黑塞", "Hermann Hesse", "1922", pd=False,
       aliases=["Siddhartha: Eine indische Dichtung", "Hesse", "Montagnola", "流浪者之歌"]),
    BK("the-walk-walser", "The Walk", "散步", "Der Spaziergang", "Robert Walser", "罗伯特·瓦尔泽", "Robert Walser", "1917", pd=False,
       aliases=["Der Spaziergang", "Walser", "Biel"]),
    BK("derborence", "Derborence", "德博朗斯", "Derborence", "Charles Ferdinand Ramuz", "拉缪", "Charles Ferdinand Ramuz", "1934", lang="fr",
       aliases=["Ramuz", "Diablerets", "Antoine Pont", "When the Mountain Fell"]),
    BK("corinne", "Corinne, or Italy", "柯丽娜", "Corinne ou l'Italie", "Germaine de Staël", "斯塔尔夫人", "Germaine de Staël", "1807", lang="fr",
       aliases=["Corinne ou l'Italie", "Madame de Staël", "Coppet", "Oswald Nelvil", "高丽娜"]),
    BK("jurg-jenatsch", "Jürg Jenatsch", "于尔格·耶纳奇", "Jürg Jenatsch", "Conrad Ferdinand Meyer", "康拉德·费迪南德·迈耶", "Conrad Ferdinand Meyer", "1876",
       aliases=["Jenatsch", "Lucretia Planta", "Graubünden", "Bündnergeschichte"]),
    BK("stranger-in-the-village", "Stranger in the Village", "村里的陌生人", None, "James Baldwin", "詹姆斯·鲍德温", "James Baldwin", "1953", lang="en",
       pd=False, aliases=["Notes of a Native Son", "Baldwin", "Leukerbad", "土生子札记"]),
    BK("praise-of-folly", "The Praise of Folly", "愚人颂", "Moriae encomium", "Desiderius Erasmus", "伊拉斯谟", "Desiderius Erasmus", "1511", lang="la",
       aliases=["Moriae Encomium", "Stultitiae Laus", "In Praise of Folly", "Erasmus", "愚神礼赞"]),
    BK("prose-transsiberian", "The Prose of the Trans-Siberian", "西伯利亚大铁路散文", "La Prose du Transsibérien et de la petite Jehanne de France",
       "Blaise Cendrars", "布莱斯·桑德拉尔", "Blaise Cendrars", "1913", lang="fr", pd=False,
       aliases=["Prose du Transsibérien", "Trans-Siberian", "Cendrars", "Frédéric-Louis Sauser"]),
    BK("julie-new-heloise", "Julie, or the New Heloise", "新爱洛伊丝", "Julie ou la Nouvelle Héloïse", "Jean-Jacques Rousseau", "卢梭", "Jean-Jacques Rousseau",
       "1761", lang="fr", aliases=["La Nouvelle Héloïse", "Julie", "Saint-Preux", "Clarens", "新爱洛绮丝"]),
]

places = [
    ORIG("ch-rutli", "Rütli", "吕特利草地",
         "A meadow on the shore of Lake Lucerne below Seelisberg, reached by boat or on foot. In Swiss tradition the men of Uri, Schwyz and Unterwalden swore the oath of the first Confederacy here. Schiller set his night scene of the oath on this meadow, and in 2004, two hundred years after it was written, the play was performed on the Rütli itself",
         "卢塞恩湖岸边、塞利斯贝格村下方的一片草地，可以坐船或步行到达。按瑞士传统的说法，乌里、施维茨和翁特瓦尔登三地的人就在这里立誓结成最初的同盟。席勒把夜里宣誓的那场戏放在这片草地上；2004 年，此剧问世两百年之际，第一次在吕特利草地上演出"),
    ORIG("ch-hohle-gasse", "Hohle Gasse, Küssnacht", "空心巷，屈斯纳赫特",
         "A sunken lane cut between banks on the old road from Küssnacht to Immensee. Legend says that here, in 1307, William Tell shot the Habsburg bailiff Gessler. Since 1937 a bypass has kept the traffic off the old road, and a chapel to Tell stands by the lane",
         "屈斯纳赫特通往伊门塞的老路上一段深陷在两侧土坡之间的低洼小路。传说 1307 年威廉·退尔就在这里射杀了哈布斯堡的总督盖斯勒。1937 年起有绕行公路分走了车流，路边立着一座纪念退尔的小礼拜堂"),
    ORIG("ch-chillon", "Chillon Castle", "西庸城堡",
         "The medieval castle on a rock in Lake Geneva near Montreux, held by the House of Savoy and then, from 1536, by Bern. François Bonivard, prior of St Victor in Geneva, lay chained in its vaults for six years until 1536. Byron came in June 1816 and wrote his poem about him; his name is said to be carved on a pillar of the dungeon",
         "日内瓦湖畔蒙特勒附近、建在湖中岩石上的中世纪城堡，先属萨伏依家族，1536 年起归伯尔尼。日内瓦圣维克托修道院院长弗朗索瓦·博尼瓦尔被锁在它的地牢里六年，直到 1536 年。拜伦 1816 年 6 月来到这里，为他写下这首长诗；据说地牢的一根石柱上还刻着拜伦的名字"),
    ORIG("ch-jungfrau", "Jungfrau", "少女峰",
         "The snow peak of the Bernese Oberland above Lauterbrunnen and Grindelwald. Byron toured the Bernese Alps in September 1816 and wrote most of Manfred on the way. The first act ends on its cliffs: Manfred is about to throw himself down when a chamois hunter holds him back",
         "伯尔尼高地的雪峰，耸立在劳特布伦嫩和格林德瓦之上。1816 年 9 月拜伦游历伯尔尼阿尔卑斯山，《曼弗雷德》大部分就写于这次旅途中。第一幕结束在它的悬崖上：曼弗雷德正要纵身跳下，被一个猎羚羊的人拉了回来"),
    ORIG("ch-ile-st-pierre", "St. Peter's Island, Lake Biel", "圣皮埃尔岛，比尔湖",
         "The island in Lake Biel, now a peninsula joined to the shore. In 1765, driven out of Môtiers, Rousseau spent two months in the old priory here until the Bern authorities expelled him; in the Fifth Walk he looks back on them as the happiest time of his life",
         "比尔湖中的小岛，如今已和湖岸连成半岛。1765 年，被赶出莫蒂埃的卢梭在岛上的旧修道院里住了两个月，直到伯尔尼当局把他驱逐；他在《第五次散步》里回忆这段日子，说那是他一生中最幸福的时光"),
    ORIG("ch-lake-zurich", "Lake Zurich", "苏黎世湖",
         "On 15 June 1775, on his first journey to Switzerland, Goethe was out on the lake on a Thursday morning and wrote eight lines in his notebook under the heading 'aufm Zürchersee'. Reworked, the poem was published in 1789 as 'Auf dem See'",
         "1775 年 6 月 15 日，歌德第一次到瑞士旅行，一个星期四的早晨在湖上泛舟，在笔记本里以“在苏黎世湖上”为题写下了八行诗。后经修改，这首诗 1789 年以《在湖上》为题发表"),
    ORIG("ch-sumiswald", "Sumiswald", "苏米斯瓦尔德",
         "Emmental village. In 1225 its castle was given to the Teutonic Order as a seat and a hospital, and is still called the Spittel. In Gotthelf's novella the grandfather begins his tale of the black spider with Sumiswald, the castle 'where the hospital now is', and the knight Hans von Stoffeln who drove the peasants hard from it",
         "埃门塔尔地区的村子。1225 年，村里的城堡被赠给条顿骑士团作驻地和医院，至今还叫“施皮特尔”（医院）。戈特赫尔夫小说里的祖父讲黑蜘蛛的故事，就从苏米斯瓦尔德讲起：讲那座“如今是医院”的城堡，讲在城堡里狠狠压榨农民的骑士汉斯·冯·施托费恩"),
    ORIG("ch-reichenbach", "Reichenbach Falls, Meiringen", "莱辛巴赫瀑布，梅林根",
         "The falls of the Reichenbach above Meiringen, some 250 metres high, where Holmes and Moriarty go over the edge together at the end of 'The Final Problem' (1893). A memorial plaque stands at the funicular station, and Meiringen has a Sherlock Holmes museum",
         "梅林根上方的莱辛巴赫瀑布，落差约 250 米。在《最后一案》（1893）的结尾，福尔摩斯和莫里亚蒂一起坠下了这里的深渊。缆车站有一块纪念牌，梅林根镇上还有一座福尔摩斯博物馆"),
    ORIG("ch-vevey", "Hôtel des Trois Couronnes, Vevey", "三王冠酒店，沃韦",
         "The grand hotel on the lake front at Vevey, on Lake Geneva. Henry James set the opening of Daisy Miller here: Winterbourne meets Daisy in the hotel garden, and from here the two make their trip to Chillon",
         "日内瓦湖畔沃韦的一家豪华酒店。亨利·詹姆斯把《黛西·米勒》的开头放在这里：温特伯恩在酒店花园里认识了黛西，两人又从这里一起去游西庸城堡"),
    ORIG("ch-schweizerhof", "Hotel Schweizerhof, Lucerne", "施魏策尔霍夫酒店，卢塞恩",
         "The hotel on the lake front at Lucerne, built in 1845. Tolstoy stayed here in July 1857; after watching the guests on the balconies give nothing to a wandering singer, he sat down that same night in his room and wrote the story 'Lucerne'",
         "卢塞恩湖滨的酒店，建于 1845 年。1857 年 7 月托尔斯泰住在这里，看到阳台上的客人对一个流浪歌手一个子儿也不给，当天夜里就在房间里坐下来写了短篇《卢塞恩》"),
    ORIG("ch-great-st-bernard", "Great St Bernard Hospice", "大圣伯纳德救济院",
         "The hospice at the top of the Great St Bernard Pass, 2,469 metres up, founded about 1050 by Bernard of Menthon and kept ever since by a community of canons; the St Bernard dog was bred here. The second book of Little Dorrit opens with the Dorrits' party climbing up to it on mules at nightfall",
         "大圣伯纳德山口顶上的救济院，海拔 2469 米，约 1050 年由芒通的伯纳德创立，此后一直由一个修会的教士们看守；圣伯纳德犬就是在这里培育出来的。《小杜丽》第二部一开头，杜丽一家的队伍就在夜色中骑着骡子爬上山来"),
    ORIG("ch-simplon", "Simplon Pass", "辛普朗山口",
         "The pass between the Valais and Italy, over which Napoleon had a carriage road built in 1801–1805. Wordsworth crossed it on foot on his walking tour of 1790, before the road. In The Prelude he remembers how he and his friend lost the track and learned from a peasant that they had already crossed the Alps without knowing it",
         "瓦莱州通往意大利的山口，拿破仑在 1801—1805 年间在这里修了马车路。1790 年华兹华斯徒步旅行时翻过这里，那时还没有这条路。他在《序曲》里回忆，他和同伴走岔了路，从一个农夫口中才知道，他们不知不觉间已经越过了阿尔卑斯山"),
    ORIG("ch-clarens", "Clarens", "克拉朗",
         "Lakeside village between Vevey and Montreux. Rousseau set Julie, or the New Heloise (1761) here, and the novel made the place famous all over Europe; Byron came in 1816 and wrote his Clarens stanzas into Childe Harold",
         "沃韦和蒙特勒之间的湖滨村庄。卢梭把《新爱洛伊丝》（1761）的故事放在这里，这部小说让它名扬全欧；1816 年拜伦来到这里，在《恰尔德·哈洛尔德游记》里为克拉朗写了几节诗",
         book_ids=["julie-new-heloise"]),
    ORIG("ch-plainpalais", "Plaine de Plainpalais, Geneva", "普兰帕莱广场，日内瓦",
         "The great open square of Geneva. In Frankenstein, Victor's little brother William goes missing here on an evening walk and is found murdered; Victor, coming home, goes out to the spot at night and sees the creature in the lightning",
         "日内瓦的大广场。在《弗兰肯斯坦》里，维克多的小弟弟威廉傍晚在这里散步时走失，后来被发现遇害；维克多回到家，夜里来到出事的地方，在闪电中看见了那个怪物"),
    ORIG("ch-rigi", "Rigi Kulm", "瑞吉山顶",
         "The summit of the Rigi, 1,797 metres, between Lake Lucerne and Lake Zug, served since 1871 by Europe's first mountain railway. In A Tramp Abroad Twain walks up from Weggis to see the famous sunrise, oversleeps, and takes the sunset for it",
         "瑞吉山的主峰，海拔 1797 米，夹在卢塞恩湖和楚格湖之间，1871 年起有欧洲第一条登山铁路通上去。在《浪迹海外》里，马克·吐温从韦吉斯步行上山去看有名的日出，结果睡过了头，把日落当成了日出"),
    ORIG("ch-maienfeld", "Maienfeld", "迈恩费尔德",
         "Small wine town in the Rhine valley of Graubünden. Heidi begins on the path up from the old town of Maienfeld to the hamlet of Dörfli and the Alm-Uncle's hut above it",
         "格劳宾登州莱茵河谷里的葡萄酒小城。《海蒂》就从这里开头：一条小路从迈恩费尔德老城出发，通往小村德尔夫利，再通往村子上方阿尔姆大叔的小屋"),
    PIL("ch-keller", "Keller's birthplace, Neumarkt, Zurich", "凯勒出生地，苏黎世新市场街",
        "Gottfried Keller was born on 19 July 1819 in the house 'Zum goldenen Winkel' in Zurich's old town (the pin marks the street, the Neumarkt) and died in Zurich in 1890. Seldwyla, the little town of his stories, among them 'Clothes Make the Man', is imaginary; Green Henry is his own youth, freely retold",
        "戈特弗里德·凯勒 1819 年 7 月 19 日生于苏黎世老城的“金角之家”（地图标在它所在的新市场街上），1890 年在苏黎世去世。他小说里的小城塞尔德维拉——《人靠衣装》等篇都发生在那里——是虚构的；《绿衣亨利》则是他自己的青年时代，经过了自由的改写",
        ["kleider-machen-leute", "green-henry"]),
    PIL("ch-muzot", "Château de Muzot, Veyras", "穆佐城堡，韦拉",
        "A thirteenth-century manor house near Veyras, above Sierre in the Rhône valley. Werner Reinhart bought it in 1921 and let Rilke live there rent-free; in a few weeks of February 1922 Rilke finished the Duino Elegies here and wrote the whole of the Sonnets to Orpheus",
        "罗讷河谷谢尔上方韦拉附近的一座十三世纪庄园宅邸。1921 年维尔纳·莱因哈特买下它，让里尔克免费住在这里；1922 年 2 月的短短几个星期里，里尔克在这里完成了《杜伊诺哀歌》，又写出了全部的《致奥尔弗斯的十四行诗》",
        ["duino-elegies"]),
    PIL("ch-centre-durrenmatt", "Centre Dürrenmatt, Neuchâtel", "迪伦马特中心，纳沙泰尔",
        "Friedrich Dürrenmatt's house on the hill above Neuchâtel, where he lived and wrote from 1952; Mario Botta rebuilt and extended it, and it opened as a museum and study centre in 2000. The Visit, his play about a rich woman who buys a poor town's justice, was written in these years",
        "弗里德里希·迪伦马特在纳沙泰尔城上方山坡上的住宅，他从 1952 年起在这里生活写作；马里奥·博塔改建扩建了它，2000 年作为博物馆和研究中心开放。他那部写富婆用钱买下一个穷镇子的“正义”的剧本《老妇还乡》，就写于这些年里",
        ["the-visit", "judge-and-his-hangman"]),
    PIL("ch-berzona", "Berzona", "贝尔佐纳",
        "Max Frisch's village in the Valle Onsernone, in Ticino, where he made his home in a modernised cottage from 1965. Man in the Holocene, about an old man alone in a rain-bound Ticino mountain village, has long been read against the life he led here",
        "马克斯·弗里施在提契诺州翁塞尔诺内山谷里的村子，1965 年起他在这里一座改建过的农舍里安家。《人类出现于全新世》写一个老人独自困在被大雨隔绝的提契诺山村里，人们一直把它和弗里施在这里的生活对照着读",
        ["man-in-the-holocene"]),
    PIL("ch-montagnola", "Museo Hermann Hesse, Montagnola", "黑塞博物馆，蒙塔诺拉",
        "Hermann Hesse came to Montagnola in 1919, rented four small rooms in the Casa Camuzzi, and lived in the village until his death in 1962; Siddhartha was written here, and Steppenwolf and Narcissus and Goldmund in the years that followed. The museum has been in the Torre Camuzzi, next to the house, since 1997",
        "赫尔曼·黑塞 1919 年来到蒙塔诺拉，在卡穆齐宅租下四个小房间，此后一直住在这个村子里，直到 1962 年去世；《悉达多》就写于这里，《荒原狼》和《纳尔齐斯与歌尔德蒙》也出自此后的岁月。博物馆 1997 年起设在宅子旁边的卡穆齐塔楼里",
        ["siddhartha", "steppenwolf", "narcissus-and-goldmund"]),
    PIL("ch-biel", "Biel/Bienne", "比尔",
        "Robert Walser was born here in 1878 and grew up in Biel, on the border between German and French Switzerland. He came back in 1913 and stayed until 1921, when he moved to Bern; The Walk (1917), a day's stroll through a small town and the country around it, belongs to these Biel years",
        "罗伯特·瓦尔泽 1878 年生于此地，在这座位于德语区和法语区交界处的城市长大。1913 年他回到比尔，一直住到 1921 年才搬去伯尔尼；《散步》（1917）写的是在一座小城和城外乡间度过的一天，正属于这段比尔岁月",
        ["the-walk-walser"]),
    PIL("ch-coppet", "Château de Coppet", "科佩城堡",
        "The château on Lake Geneva that Jacques Necker, Louis XVI's finance minister, took over in 1784. His daughter Germaine de Staël, kept away from Paris by Napoleon, gathered the 'Coppet group' of writers and thinkers here from about 1805 to 1816, and came back here from her journey through Italy with the notebooks from which she made Corinne",
        "日内瓦湖畔的城堡，1784 年由路易十六的财政大臣雅克·内克尔接手。他的女儿斯塔尔夫人被拿破仑挡在巴黎之外，大约从 1805 年到 1816 年在这里聚集起一批作家和思想家，人称“科佩集团”；她游历意大利后带着几本旅行笔记回到这里，后来据此写成了《柯丽娜》",
        ["corinne"]),
    PIL("ch-basel-erasmus", "Basel Minster (Erasmus's grave)", "巴塞尔大教堂（伊拉斯谟墓）",
        "Basel's red sandstone cathedral above the Rhine. Erasmus, who lived and worked in Basel for years among its printers, died in the city in July 1536 and was buried in the Minster with great ceremony, although Basel had turned Protestant",
        "莱茵河畔高处的巴塞尔红砂岩大教堂。伊拉斯谟曾多年在巴塞尔生活工作，同这里的印刷商来往密切；1536 年 7 月他在这座城里去世，虽然巴塞尔已经改信新教，人们仍在大教堂里为他举行了隆重的葬礼",
        ["praise-of-folly"]),
    PIL("ch-la-chaux-de-fonds", "La Chaux-de-Fonds", "拉绍德封",
        "Watchmaking town in the Jura. Blaise Cendrars was born here, at 27 rue de la Paix, on 1 September 1887, as Frédéric-Louis Sauser; his long poem of a train journey across Russia, the Prose of the Trans-Siberian, came out in 1913",
        "汝拉山区的钟表业小城。布莱斯·桑德拉尔 1887 年 9 月 1 日生于此地和平街 27 号，原名弗雷德里克-路易·绍塞尔；他那首写横穿俄国的火车旅行的长诗《西伯利亚大铁路散文》1913 年问世",
        ["prose-transsiberian"]),
    PIL("ch-sils", "Nietzsche-Haus, Sils Maria", "尼采故居，锡尔斯-玛利亚",
        "Nietzsche rented a plain room in this house for a franc a day in the summer of 1881, and again every summer from 1883 to 1888; he called the place 'perla perlissima'. On a walk by nearby Lake Silvaplana in 1881 came the thought of eternal recurrence that lies at the heart of Thus Spoke Zarathustra. The house is now a museum",
        "1881 年夏天，尼采以每天一法郎的价钱在这座房子里租了一间简朴的屋子，1883 年到 1888 年又每年夏天都来；他把这里称作“珍珠中的珍珠”。1881 年在附近的锡尔瓦普拉纳湖边散步时，他想到了“永恒轮回”，这正是《查拉图斯特拉如是说》的核心。这座房子如今是一座博物馆",
        ["thus-spoke-zarathustra"]),
    PIL("ch-fluntern", "Fluntern Cemetery, Zurich (Joyce's grave)", "弗伦特恩公墓，苏黎世（乔伊斯墓）",
        "Joyce spent most of the First World War in Zurich, working on Ulysses. He died in the city in January 1941 and is buried in Fluntern Cemetery on the Zürichberg; his wife Nora Barnacle lies there too",
        "第一次世界大战的大部分时间里，乔伊斯住在苏黎世写《尤利西斯》。1941 年 1 月他在这座城市去世，葬在苏黎世山上的弗伦特恩公墓，他的妻子诺拉·巴纳克尔也葬在那里",
        ["ulysses"]),
    PIL("ch-cimetiere-rois", "Cimetière des Rois, Geneva (Borges's grave)", "国王公墓，日内瓦（博尔赫斯墓）",
        "Geneva's cemetery of notable people, in the Plainpalais quarter. Borges came to Geneva with his family in 1914 and went to the Collège de Genève; he came back at the end of his life, died here in June 1986, and lies under a rough-hewn stone carved with Anglo-Saxon and Norse motifs",
        "日内瓦安葬名人的公墓，在普兰帕莱区。博尔赫斯 1914 年随家人来到日内瓦，在日内瓦中学读书；晚年他又回到这里，1986 年 6 月在此去世，长眠在一块粗凿的墓碑下，碑上刻着盎格鲁-撒克逊和北欧的图案",
        ["el-aleph", "ficciones"]),
    PIL("ch-delices", "Les Délices, Geneva (Voltaire's house)", "“乐园”，日内瓦（伏尔泰故居）",
        "Voltaire's house in Geneva from 1755 to 1760; he is believed to have written part of Candide here. Since 1952 it has housed the Institut et Musée Voltaire",
        "1755 年到 1760 年伏尔泰在日内瓦的住宅，一般认为《老实人》有一部分就写于这里。1952 年起这里是伏尔泰研究所和博物馆",
        ["fr-candide"]),
    PIL("ch-montreux-palace", "Montreux Palace", "蒙特勒皇宫酒店",
        "The belle-époque hotel on the lake front at Montreux, where Nabokov and his wife Véra lived from 1961 to the end of his life in 1977. The revised and enlarged edition of his memoir Speak, Memory came out in 1966, in these years",
        "蒙特勒湖滨的美好年代风格大酒店，纳博科夫和妻子薇拉从 1961 年起住在这里，直到他 1977 年去世。他的回忆录《说吧，记忆》修订增补版 1966 年出版，正在这些年里",
        ["speak-memory"]),
    PIL("ch-tegna", "Tegna", "泰尼亚",
        "Village in Ticino near Locarno. After an operation in 1986, Patricia Highsmith had a house built here that her friends called 'the bunker'; she finished her last books in it, and died in hospital in Locarno in February 1995",
        "提契诺州洛迦诺附近的村子。1986 年动过手术之后，帕特里夏·海史密斯在这里盖了一座房子，朋友们管它叫“地堡”；她在这里写完了最后几本书，1995 年 2 月在洛迦诺的医院去世",
        ["talented-mr-ripley"]),
    PIL("ch-ronco", "Ronco sopra Ascona (Remarque's grave)", "龙科（雷马克墓）",
        "Village above Lake Maggiore. In 1931, with the wealth his books had brought him, Remarque bought the Casa Monte Tabor at Porto Ronco below the village; he died in Locarno in 1970 and is buried in Ronco cemetery",
        "马焦雷湖上方的村子。1931 年，雷马克用作品带给他的财富买下了村子下方波尔托龙科的蒙特塔博尔别墅；1970 年他在洛迦诺去世，葬在龙科的墓地里",
        ["all-quiet-on-the-western-front"]),
    PIL("ch-kilchberg", "Kilchberg (Thomas Mann's grave)", "基尔希贝格（托马斯·曼墓）",
        "Village on the west shore of Lake Zurich. Thomas Mann came back from America in 1952 and settled here, buying his last house in 1954; he died in 1955 and was buried in the village cemetery",
        "苏黎世湖西岸的村子。托马斯·曼 1952 年从美国回到欧洲，在这里定居，1954 年买下了他最后的住宅；1955 年他去世后葬在村里的墓地",
        ["buddenbrooks", "the-magic-mountain"]),
    PIL("ch-diodati", "Villa Diodati, Cologny", "迪奥达蒂别墅，科洛尼",
        "The villa above the lake at Cologny that Byron rented in the summer of 1816, with his doctor John Polidori. The Shelleys and Claire Clairmont were close by; the ghost-story evenings here gave rise to Frankenstein and to Polidori's The Vampyre, and Byron wrote the third canto of Childe Harold that summer",
        "科洛尼湖边山坡上的别墅，1816 年夏天拜伦和他的医生约翰·波利多里租住在这里。雪莱夫妇和克莱尔·克莱蒙特住在附近；这里的鬼故事之夜催生了《弗兰肯斯坦》和波利多里的《吸血鬼》，那个夏天拜伦还写了《恰尔德·哈洛尔德游记》第三章",
        [FRANK, BYRON]),
    ORIG("ch-twann", "Twann", "特万",
         "Wine village on the north shore of Lake Biel, below the road that climbs to Lamboing on the Jura slope. The Judge and His Hangman begins here: the village policeman finds an officer of the Bern police shot dead in his car on the road between Twann and Lamboing",
         "比尔湖北岸的葡萄酒村，村子上方有公路沿汝拉山坡通往兰布万。《法官和他的刽子手》就从这里开始：村里的警察在特万和兰布万之间的公路上，发现一名伯尔尼警官被枪杀在自己的汽车里"),
    ORIG("ch-derborence", "Derborence", "德博朗斯",
         "Lake in a cirque below the Diablerets, in the Valais. Rockfalls from the mountain buried the pastures in 1714 and again in 1749, and the second made the lake. Ramuz's novel tells of the first",
         "瓦莱州迪亚布勒雷山下冰斗里的湖。1714 年和 1749 年，山上两次崩塌的岩石掩埋了这里的牧场，第二次崩塌堵出了这个湖。拉缪的小说写的是第一次"),
    ORIG("ch-chur", "Chur", "库尔",
         "The capital of Graubünden. The real Jörg Jenatsch was killed here in January 1639, in carnival time, by masked conspirators at an inn; in 2012 his grave was identified in the cathedral. Meyer's novel of 1876 ends with his death in Chur",
         "格劳宾登州首府。历史上的约尔格·耶纳奇 1639 年 1 月狂欢节期间在这里的一家小酒馆里被一伙戴面具的密谋者杀死；2012 年人们在大教堂里确认了他的坟墓。迈耶 1876 年的小说就以他死在库尔结束"),
    ORIG("ch-leukerbad", "Leukerbad", "洛伊克巴德",
         "Spa village high in the Valais, known for its hot springs. James Baldwin came here in the summer of 1951 with his friend the painter Lucien Happersberger, and wrote about it in 'Stranger in the Village' (1953)",
         "瓦莱州高山上的温泉村。1951 年夏天，詹姆斯·鲍德温和他的朋友、画家吕西安·哈珀斯贝格尔来到这里，后来在《村里的陌生人》（1953）里写了它"),
    ORIG("ch-bern-kirchenfeld", "Kirchenfeld Bridge, Bern", "基尔兴费尔德桥，伯尔尼",
         "The bridge over the Aare between the old town of Bern and the Kirchenfeld quarter, where the Gymnasium Kirchenfeld stands. Night Train to Lisbon starts on this bridge",
         "伯尔尼老城和基尔兴费尔德区之间横跨阿勒河的大桥，基尔兴费尔德文理中学就在桥那头的城区里。《开往里斯本的夜车》就从这座桥上开始"),
    ORIG("ch-davos", "Davos", "达沃斯",
         "High valley town in Graubünden. In 1912 Thomas Mann spent three weeks here visiting his wife, who was being treated at Dr Jessen's Waldsanatorium; the visit became The Magic Mountain, whose Berghof sanatorium stands above Davos",
         "格劳宾登州的高山谷地小城。1912 年托马斯·曼来这里看望在耶森医生的森林疗养院治病的妻子，住了三个星期；这次探访后来成了《魔山》，书中的山庄疗养院就在达沃斯上方"),
    ORIG("ch-lausanne", "Lausanne", "洛桑",
         "City on the north shore of Lake Geneva. At the end of A Farewell to Arms, Frederic and Catherine come down from the mountain above Montreux to wait for the baby near the hospital here",
         "日内瓦湖北岸的城市。《永别了，武器》的结尾，弗雷德里克和凯瑟琳从蒙特勒上方的山上搬下来，住到这里的医院附近等孩子出生"),
]

# ---------- quotations from German, French and Russian ----------
_rutli = drop(raw(T_TELL2, "Der Bergweg öffnet sich, nur frisch mir nach,", "Wir sind am Ziel, hier ist das Rütli."), "\n[69]") \
    + GAP + raw(T_TELL2, "Bei diesem Licht, das uns zuerst begrüßt", "In keiner Noth uns trennen und Gefahr.")
_gasse = drop(raw(T_TELL4, "Durch diese hohle Gasse muß er kommen,", "Die Gelegenheit ist günstig."), "\n[185]")
_see = drop(raw(T_SEE, "Und frische Nahrung, neues Blut", "Sich die reifende Frucht."), "[145]  ")
lines = [
    Q("ch-tell-1", "wilhelm-tell", "ch-rutli", "Act 2, Scene 2", "第二幕第二场", DE, T_TELL2, _rutli, ["das Rütli"],
      "The mountain path opens out; keep close behind me.\nI know the rock and the little cross on top:\nWe are there. This is the Rütli."
      + GAP + "By this light, which greets us first\nOf all the peoples who live far below us,\nBreathing hard in the smoke of the cities,\nLet us swear the oath of our new league.\nWe will be a single people of brothers,\nNever to part in any need or danger.",
      ["the Rütli"],
      "山路开阔了，快跟上我，\n我认得这块岩石和上面的小十字架，\n我们到了，这里就是吕特利。"
      + GAP + "凭着这道光——它先于所有\n住在我们脚下、在城市的烟雾里\n艰难喘息的民族，来问候我们——\n让我们立下新同盟的誓言。\n我们要做一个兄弟同心的民族，\n无论遭遇什么困苦危难，永不分离。",
      ["吕特利"], note=" (Melchthal's arrival and Rösselmann's oath; two page marks left out)"),
    Q("ch-tell-2", "wilhelm-tell", "ch-hohle-gasse", "Act 4, Scene 3", "第四幕第三场", DE, T_TELL4, _gasse, ["hohle Gasse", "Küßnacht"],
      "Through this hollow lane he has to come;\nThere is no other road to Küssnacht. Here\nI'll finish it. The moment is in my favour.",
      ["hollow lane", "Küssnacht"],
      "他一定要穿过这条空心巷，\n去屈斯纳赫特没有别的路——就在这里\n我要了结它——时机正好。",
      ["空心巷", "屈斯纳赫特"], note=" (a page mark left out)"),
    Q("ch-sp-1", "black-spider", "ch-sumiswald", "The frame story: the grandfather begins", "框架故事：祖父开讲", DE, T_SPIN,
      raw(T_SPIN, "Ich habe viel darüber nachgefragt", "aufgeschrieben steht das Nirgends."), ["Sumiswald"],
      "I have asked a great deal about it, but I have been able to learn nothing, except that this part of the country was settled very early, and that Sumiswald is even said to have been a town before our Saviour came into the world; but that is written down nowhere.",
      ["Sumiswald"],
      "这件事我打听过很多，可什么也没问出来，只知道这一带很早就有人住，甚至据说早在我们的救世主降世之前，苏米斯瓦尔德就已经是一座城了；不过这件事哪儿也没有写下来。",
      ["苏米斯瓦尔德"]),
    Q("ch-see-1", "auf-dem-see", "ch-lake-zurich", "The whole poem", "全诗", DE, T_SEE, _see, ["im See"],
      "And fresh nourishment, new blood\nI draw from the free world;\nHow kind and good is Nature,\nWho holds me to her breast!\nThe wave rocks our boat\nUpward to the beat of the oars,\nAnd mountains, cloudy, reaching to the sky,\nCome to meet our course.\nEyes, my eyes, why do you sink?\nGolden dreams, are you coming back?\nAway, you dream, golden though you are;\nHere too are love and life.\nOn the wave there glitter\nA thousand floating stars,\nSoft mists drink in\nThe towering distance all around;\nMorning wind flutters round\nThe shaded bay,\nAnd in the lake is mirrored\nThe ripening fruit.",
      ["in the lake"],
      "我从自由的世界里\n吸取新的养料、新的血液；\n大自然多么温柔多么好，\n把我搂在她的怀里！\n波浪随着划桨的节拍\n把我们的小船轻轻摇荡，\n群山云雾缭绕，直上天空，\n迎着我们的航程而来。\n眼睛啊，我的眼睛，你为何低垂？\n金色的梦啊，你们又回来了吗？\n去吧，梦！哪怕你是金子做的；\n这里也有爱，也有生活。\n波浪上闪烁着\n千万颗浮动的星星，\n柔和的雾霭吸饮着\n四周层叠高耸的远方；\n晨风轻拂着\n树荫遮蔽的湖湾，\n湖水里倒映出\n正在成熟的果实。",
      ["湖水里"], note=" (a page mark left out)"),
    Q("ch-rev-1", "reveries-solitary-walker", "ch-ile-st-pierre", "Fifth Walk", "第五次散步", FR, T_REV,
      flow(raw(T_REV, "De toutes les habitations où j’ai demeuré", "chez nul\nautre.", "fr")), ["l’Isle de St. Pierre"],
      "Of all the places I have lived in (and I have had some charming ones), none made me so truly happy or left me such tender regrets as the Island of St Peter in the middle of the Lake of Bienne. This little island, which in Neuchâtel they call the Île de la Motte, is very little known, even in Switzerland. No traveller, as far as I know, mentions it. Yet it is very pleasant and singularly well placed for the happiness of a man who likes to keep within bounds; for although I am perhaps the only person in the world whose fate has made this a law for him, I cannot believe I am the only one with so natural a taste, though so far I have found it in no one else.",
      ["the Island of St Peter"],
      "在我住过的所有地方中（其中也有很迷人的），没有一处像比尔湖中央的圣皮埃尔岛那样让我真正幸福，给我留下如此温柔的怀念。这座小岛在纳沙泰尔被叫作拉莫特岛，即使在瑞士也很少有人知道。据我所知，没有一个旅行者提到过它。然而它非常宜人，所处的位置特别适合一个喜欢把自己圈在小天地里的人得到幸福；因为，虽然我也许是世上唯一一个被命运把这当作一条法则强加于身的人，我却不能相信自己是唯一有这种如此自然的爱好的人，尽管我至今还没在别人身上发现过它。",
      ["圣皮埃尔岛"], note=" (the page's line ends joined)"),
    Q("ch-luz-1", "lucerne-tolstoy", "ch-schweizerhof", "The narrator's record of 7 July", "叙述者对 7 月 7 日的记录", RU, T_LUZ,
      raw(T_LUZ, "«Седьмого июля 1857 года", "многие смеялись над ним».", "ru"), ["отелем Швейцергофом"],
      "'On the seventh of July 1857, in Lucerne, in front of the Hotel Schweizerhof, where the richest people stay, a wandering beggar singer sang songs and played the guitar for half an hour. About a hundred people listened to him. Three times the singer asked them all to give him something. Not one person gave him anything, and many laughed at him.'",
      ["Hotel Schweizerhof"],
      "“1857 年 7 月 7 日，在卢塞恩，最富有的人下榻的施魏策尔霍夫旅馆门前，一个流浪的穷歌手唱了半个小时的歌，弹着吉他。大约一百个人听他唱。歌手三次请大家给他点什么。没有一个人给他任何东西，许多人还嘲笑他。”",
      ["施魏策尔霍夫旅馆"]),
]

# ---------- English originals ----------
_chil = raw(T_CHIL, "Lake Leman lies by Chillon's walls:", "The death that would have set me free.", "en")
for _n in ("sent110\n", "high120\n"):   # the line numbers printed at the end of lines 110 and 120
    assert _chil.count(_n) == 1, _n
    _chil = _chil.replace(_n, _n[:-4] + "\n")
assert not re.search(r"\d", _chil), _chil
_manf = raw(T_MANF, "The Mountain of the Jungfrau.", "I cannot love ye.", "en")
_manf = drop(_manf, " ").replace("beautiful?  I", "beautiful? I")
_fp = raw(T_FP, "We had strict injunctions, however,", "out of the abyss.", "en")
_dm = raw(T_DM, "At the little town of Vevey,", "a lake that it behooves every tourist to visit.", "en") + GAP \
    + raw(T_DM, "One of the hotels at Vevey, however,", "of luxury and of maturity.", "en")
_ld = raw(T_LD, "In the autumn of the year,", "the highest ridges of the Alps.", "en") + GAP \
    + raw(T_LD, "Seen from these solitudes,", "floated on the shadowy waves.", "en")
_prel = raw(T_PREL, "When from the Vallais we had turned,", "Their noon-tide meal.", "en") + GAP \
    + raw(T_PREL, "Loth to believe what we so grieved to hear,", "that we had crossed the Alps.", "en")
_cl = drop(raw(T_CH3, "Clarens! sweet Clarens", "then mocks.", "en"), "N21")
_fr = raw(T_FRANK, "Last Thursday (May 7th),", "but that he did not return.", "en")
_tr = raw(T_TRAMP, "THE Rigi-Kulm is an imposing Alpine mass,", "This village is at the foot of the mountain.", "en")
lines += [
    EN("ch-chil-1", "prisoner-of-chillon", "ch-chillon", "Stanza VI", "第六节", T_CHIL, _chil, ["Chillon's walls"],
       "莱芒湖紧挨着西庸的城墙：\n在它下面一千英尺深处，\n沉重的湖水汇合、流淌；\n测深绳从西庸雪白的雉堞上\n放下去，测出的就是这么深，\n湖水把城堡团团围住：\n墙壁和波浪，造成了双重的地牢——\n就像一座活的坟墓。\n在湖面以下，\n是我们被关押的那座黑暗拱顶：\n我们日日夜夜听见湖水荡漾，\n它在我们头顶上拍打作响；\n风势大作、在欢乐的天空里\n肆意狂舞的时候，\n我感到冬天的浪花\n穿过铁栏冲刷进来；\n这时，就连岩石也摇晃起来，\n我感到它在颤动，却毫不惊慌，\n因为我本可以微笑着迎接\n那将给我自由的死亡。",
       ["西庸的城墙"], note=" (the editor's line numbers left out)"),
    EN("ch-manf-1", "manfred", "ch-jungfrau", "Act 1, Scene 2", "第一幕第二场", T_MANF, _manf, ["The Mountain of the Jungfrau"],
       "少女峰上。——时间：早晨。——曼弗雷德独自站在悬崖上。\n曼：我召来的精灵离弃了我——\n我研习的咒语让我失望——\n我指望的解药折磨着我；\n我不再倚仗超人的帮助，\n它对过去无能为力，至于\n未来，在过去沉入黑暗之前，\n我也无意去寻求。——我的大地母亲！\n还有你，初破晓的白昼，还有你们，群山，\n你们为什么这样美？我无法爱你们。",
       ["少女峰"], note=" (an em space before the speaker's name and a double space left out)"),
    EN("ch-fp-1", "final-problem", "ch-reichenbach", "Watson's account", "华生的叙述", T_FP, _fp, ["the falls of Reichenbach"],
       "不过我们得到了再三叮嘱：经过莱辛巴赫瀑布时，无论如何都要稍微绕点路去看一看——瀑布大约在半山腰。\n那真是个可怕的地方。融雪使激流暴涨，一头扎进一个巨大的深渊，水沫像失火房子里冒出的浓烟一样翻滚上来。河水冲进的那个竖井是一道极深的裂谷，两壁是闪亮的、煤一样黑的岩石，越往下越窄，成了一口深不可测、泡沫翻腾的沸井，水满溢出来，又从参差的井口把激流抛向前去。长长的一片绿水永不停歇地咆哮着往下冲，厚厚的一道闪动的水帘永不停歇地嘶嘶往上喷，那不停的旋转和喧嚣叫人头晕目眩。我们站在边上，俯视着远远下方黑色岩石间碎浪的闪光，倾听着那像人的呼喊一样、随着水雾从深渊里轰然升起的声音。",
       ["莱辛巴赫瀑布"], note=" (first printing, December 1893)"),
    EN("ch-dm-1", "daisy-miller", "ch-vevey", "Part 1, opening", "第一部开头", T_DM, _dm, ["Vevey"],
       "在瑞士的小城沃韦，有一家特别舒适的旅馆。其实那里旅馆很多，因为招待游客正是这地方的营生——许多旅行者都还记得，它坐落在一片蓝得出奇的湖边，那是每个游客都该去看看的湖。"
       + GAP + "不过，沃韦的旅馆中有一家很有名，甚至可以说是经典，它带着一种既豪华又老成的气派，同许多新冒出来的邻居截然不同。",
       ["沃韦"]),
    EN("ch-ld-1", "little-dorrit", "ch-great-st-bernard", "Book 2, Chapter 1, 'Fellow Travellers'", "第二部第一章《旅伴》", T_LD, _ld,
       ["the convent of the Great Saint Bernard"],
       "那年秋天，黑暗和夜色正朝阿尔卑斯山的最高峰爬去。"
       + GAP + "从这些荒僻的高处望去，从大圣伯纳德山口——它也是其中之一——望去，升起的夜色像上涨的潮水一样漫上山来。当它终于涨到大圣伯纳德修道院的围墙时，那座饱经风霜的建筑仿佛成了另一只方舟，漂浮在阴影的波涛上。",
       ["大圣伯纳德修道院"]),
    EN("ch-prel-1", "the-prelude", "ch-simplon", "Book VI", "第六卷", T_PREL, _prel, ["Simplon"],
       "我们从瓦莱州拐过来，沿着\n辛普朗山口陡峭崎岖的道路攀登，\n跟在一队赶骡人后面，来到\n一处歇脚的地方，大家都在那里\n吃午饭。"
       + GAP + "我们不愿相信这令人伤心的消息，\n因为我们的希望还指向云端，\n就一遍又一遍地问他；\n可是农夫嘴里说出的每一句回答，\n经过我们的感受一翻译，\n结论都是这样——我们已经越过了阿尔卑斯山。",
       ["辛普朗山口"]),
    EN("ch-byron-1", BYRON, "ch-clarens", "Canto III, stanza 99", "第三章第九十九节", T_CH3, _cl, ["Clarens"],
       "克拉朗！可爱的克拉朗，深沉爱情的诞生地！\n你的空气是热烈思想的青春气息；\n你的树木扎根于爱情；高处的白雪，\n连冰川都染上了它的颜色，\n夕阳在上面晕出玫瑰的色调，\n那些光线在那里温柔地安睡：岩石，\n那些永恒的峭壁，都在诉说爱情——爱神\n曾在它们中间躲避尘世的打击，\n那打击用希望撩拨、刺痛灵魂，先是引诱，然后嘲弄。",
       ["克拉朗"], note=" (the editor's note mark left out)"),
    EN("ch-frank-1", FRANK, "ch-plainpalais", "Chapter 7, Alphonse Frankenstein's letter", "第七章，父亲的来信", T_FRANK, _fr, ["Plainpalais"],
       "上星期四（5 月 7 日），我、我的侄女和你的两个弟弟一起去普兰帕莱散步。傍晚温暖而宁静，我们比平常走得远些。天已经黑了，我们才想起回家；这时才发现先走在前面的威廉和欧内斯特不见了。我们就在长椅上休息，等他们回来。不一会儿欧内斯特来了，问我们看见他弟弟没有：他说他一直在和威廉玩，威廉跑开躲起来了，他怎么找也找不到，后来又等了他很久，可他一直没有回来。",
       ["普兰帕莱"], note=" (1831 edition)"),
    EN("ch-tramp-1", TRAMP, "ch-rigi", "Chapter 28", "第二十八章", T_TRAMP, _tr, ["Rigi-Kulm"],
       "瑞吉山顶是一座雄伟的阿尔卑斯山体，高六千英尺，孤零零地矗立着，俯瞰着一片壮阔的景色：蓝色的湖泊、绿色的山谷和积雪的群山——一幅紧凑而壮丽的图画，方圆三百英里。登山可以坐火车，可以骑马，也可以步行，随各人的喜好。一个晴朗的早晨，我和我的代理人披挂上步行的行头，坐汽船沿湖而下，在韦吉斯村上了岸——那里离卢塞恩有三刻钟的路程。这个村子就在山脚下。",
       ["瑞吉山顶"]),
]

# ---------- scene notes ----------
lines += [
    S("ch-heidi-s1", "heidi", "ch-maienfeld", "Part 1, Chapter 1", "第一部第一章",
      "Heidi begins on the footpath that climbs from the old town of Maienfeld through green meadows to the hamlet of Dörfli and on up to the Alm. Aunt Dete, who has found a place in Frankfurt, is taking five-year-old Heidi up to her grandfather, the gruff Alm-Uncle who lives alone in a hut above the village.",
      "《海蒂》开篇是一条小路：从古老的迈恩费尔德小城出发，穿过绿色的草地，经过小村德尔夫利，一直爬上高山牧场。在法兰克福找到了差事的姨妈德特，正带着五岁的海蒂上山，去投奔她的爷爷：那个独自住在村子上方小屋里、脾气古怪的“阿尔姆大叔”。",
      ["Maienfeld"], ["迈恩费尔德"], W + "Heidi"),
    S("ch-judge-s1", "judge-and-his-hangman", "ch-twann", "Chapter 1", "第一章",
      "On the morning of Thursday 3 November 1948, Clenin, the village policeman of Twann, finds a car standing on the road between Twann and Lamboing with Schmied, Inspector Bärlach's best man in the Bern police, dead at the wheel. Schmied had been working under a false name in the circle of the shadowy Gastmann, and the old, sick Bärlach takes up his last case.",
      "1948 年 11 月 3 日星期四早晨，特万村的警察克莱宁在特万和兰布万之间的公路上发现一辆汽车，伯尔尼警局巴尔拉赫探长手下最得力的施密德死在驾驶座上。施密德生前化名混进了神秘人物加斯特曼的圈子；年老多病的巴尔拉赫接手了他的最后一个案子。",
      ["Twann"], ["特万"], DEW + "Der_Richter_und_sein_Henker"),
    S("ch-holo-s1", "man-in-the-holocene", "ch-berzona", "Throughout", "全书",
      "Days of rain in early autumn cut off a mountain village in Ticino, and the slopes are already sliding. Herr Geiser, a seventy-three-year-old widower from Basel, fears the whole mountain may come down. Losing his memory, he copies and cuts out what he knows from encyclopedias and pins the slips to the walls of his house; once he sets out over the pass for Basel, then turns back.",
      "初秋连下了好几天的雨，提契诺的一个山村与外界隔绝，山坡已经开始滑塌。来自巴塞尔的七十三岁鳏夫盖泽尔先生担心整座山都会塌下来。他的记忆在衰退，就从百科全书上抄下、剪下他知道的东西，把纸条钉满屋子的墙；有一次他背起背包翻过山口往巴塞尔去，走到半路又折了回来。",
      ["Ticino"], ["提契诺"], DEW + "Der_Mensch_erscheint_im_Holoz%C3%A4n"),
    S("ch-derb-s1", "derborence", "ch-derborence", "Throughout", "全书",
      "In 1714, one night in the summer pasture of Derborence, the mountain falls: a mass of rock breaks off the Diablerets and buries the huts and the herdsmen. Antoine Pont, married only two months, is counted among the dead. Seven weeks and a day later he comes down to the village, and everyone takes him for a ghost until his wife Thérèse believes him; then he goes back up into the fallen rock to look for his uncle Séraphin.",
      "1714 年夏天的一个夜里，德博朗斯的高山牧场上，山崩了：迪亚布勒雷山上一大块岩石崩落下来，埋住了小屋和牧人。结婚才两个月的安托万·蓬也被算进了死者之中。七个星期零一天之后，他走下山回到村里，人人都把他当成鬼魂，直到他的妻子泰蕾兹相信了他；后来他又回到崩塌的乱石堆里，去寻找他的舅舅塞拉芬。",
      ["Derborence"], ["德博朗斯"], FRW + "Derborence_(roman)"),
    S("ch-jen-s1", "jurg-jenatsch", "ch-chur", "The last chapter", "最后一章",
      "The novel ends in Chur in 1639. Jenatsch, the pastor turned soldier who has freed the Grisons from the French, turning Catholic and allying himself with Spain to do it, is cut down by his enemies; the final blow is struck by Lucretia Planta, who has loved him all her life, with the same axe with which he killed her father.",
      "小说结束在 1639 年的库尔。耶纳奇原是牧师，后来成了军人，为了把格劳宾登从法国人手里解放出来，他改信天主教，又同西班牙结了盟；最后他被仇人围杀，给他致命一击的是一直爱着他的卢克蕾齐娅·普兰塔——她用的正是当年他杀死她父亲的那把斧头。",
      ["Chur"], ["库尔"], DEW + "J%C3%BCrg_Jenatsch"),
    S("ch-stranger-s1", "stranger-in-the-village", "ch-leukerbad", "The essay", "全文",
      "Baldwin writes of a small village high in the Swiss mountains where, as far as he could tell, no black man had ever set foot before him. Children shout after him in the street and the villagers stare. From the village he looks at the West, and at America, where, he concludes, black and white can no longer be strangers to each other.",
      "鲍德温写的是瑞士高山上的一个小村子——据他所知，在他之前从没有黑人踏进过这里。孩子们在街上追着他喊，村民们盯着他看。他从这个村子出发去审视西方，审视美国；他的结论是，在美国，黑人和白人再也不可能是彼此的陌生人了。",
      ["village"], ["村子"], W + "Stranger_in_the_Village"),
    S("ch-ntl-s1", "pt-night-train", "ch-bern-kirchenfeld", "Opening", "开篇",
      "One morning in pouring rain, on his way to the Gymnasium where he has taught Latin, Greek and Hebrew for thirty-three years, Raimund Gregorius sees a woman on the Kirchenfeld Bridge reading a letter; she crumples it and throws it into the river, and he fears she is about to jump. She is Portuguese. Later that day he finds a book by a Portuguese doctor, Amadeu de Prado, in an antiquarian bookshop, and soon he is on the night train to Lisbon.",
      "一个大雨滂沱的早晨，在一所文理中学教了三十三年拉丁文、希腊文和希伯来文的赖蒙德·格雷戈里乌斯去上课的路上，看见基尔兴费尔德桥上有个女人在读一封信；她把信揉成一团扔进河里，他担心她要跳下去。她是葡萄牙人。当天晚些时候，他在一家旧书店里发现了葡萄牙医生阿马德乌·德·普拉多的一本书，不久就登上了开往里斯本的夜车。",
      ["Kirchenfeld Bridge"], ["基尔兴费尔德桥"], DEW + "Nachtzug_nach_Lissabon"),
    S("ch-mm-s1", "the-magic-mountain", "ch-davos", "Chapter 1, 'Arrival'", "第一章《到达》",
      "Hans Castorp, a young engineer from Hamburg about to start work, takes the train up to Davos to spend three weeks with his cousin Joachim, a patient at the Berghof sanatorium high above the valley. He stays seven years, until the war breaks out.",
      "汉斯·卡斯托尔普是汉堡的一个年轻工程师，正要开始工作；他坐火车上山来到达沃斯，打算在山谷高处的山庄疗养院陪他住院治病的表兄约阿希姆住三个星期。结果他一住就是七年，直到战争爆发。",
      ["Davos"], ["达沃斯"], W + "The_Magic_Mountain"),
    S("ch-fta-s1", "farewell-to-arms", "ch-lausanne", "Book 5", "第五部",
      "After their escape across the lake, Frederic and Catherine spend the winter in a wooden house on the mountain above Montreux. In spring they move down to Lausanne to be near the hospital. Catherine's labour goes badly: the baby is stillborn, she haemorrhages and dies, and Frederic walks back to the hotel in the rain.",
      "两人划船越过湖面逃出来以后，弗雷德里克和凯瑟琳在蒙特勒上方山上的一座木屋里过了一冬。春天，他们搬到洛桑，好离医院近些。凯瑟琳难产：孩子生下来就死了，她大出血，也死了；弗雷德里克冒着雨走回旅馆。",
      ["Lausanne"], ["洛桑"], W + "A_Farewell_to_Arms"),
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

HEAD = "// Switzerland, hand-written content (tools/content/batches/add_ch1.py, 2026-11-23).\n"
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
