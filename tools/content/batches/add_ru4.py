"""11-23: Russia, fourth pack: 43 more books and 61 more places, to bring the country in line with its weight
(Pushkin's and Tolstoy's own places, the provinces from Smolensk to Kamchatka, Soviet and later books).

Quotations (22 lines) are cut from Wikisource pages (tools/content/wikisource.py): Russian Wikisource, and French
Wikisource for Jules Verne; English and Chinese translations are our own drafts (translation: "own").
Books still in copyright, and Hašek's Bugulma stories (not on Wikisource), have scene notes; the rest hang on a
writer's place.
What a cut changes, named again in that line's `checked`: no-break and thin spaces are written as plain spaces; the
indent of a verse line is dropped; the Crime and Punishment page is hard-wrapped plain text, so its lines are joined
and its doubled spaces written as one.

Coordinates are those of the place's Russian (once English) Wikipedia article (cache/ru/coords.json).

Usage: python3 -I add_ru4.py <app_dir> <coords.json> <wikisource_root>   (<root>/ru and <root>/fr hold the pages)"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b
import wikisource as ws

APP, CO, WSR = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8")), sys.argv[3]
DATE = "2026-11-23"
b.init(APP, "", "ru", DATE)
W = b.W
RUW = "https://ru.wikipedia.org/wiki/"
GAP = b.GAP

def BK(id, title, title_zh, title_orig, author, author_zh, author_orig, year, pd=True, **kw):
    d = dict(id=id, title=title, title_zh=title_zh, title_orig=title_orig, author=author, author_zh=author_zh, year=year,
             orig_lang=kw.pop("lang", "ru"), public_domain=pd, source_url=kw.pop("src", None), author_orig=author_orig)
    d.update(kw)
    return {k: v for k, v in d.items() if v is not None or k == "source_url"}

def C(pid):
    c = CO[pid]
    return c["lat"], c["lon"], c["st"], c["su"]

def ORIG(pid, name, zh, en_note, zh_note, **kw): return b.ORIG(pid, name, zh, *C(pid), en_note, zh_note, **kw)
def PROTO(pid, name, zh, en_note, zh_note, **kw): return b.PROTO(pid, name, zh, *C(pid), en_note, zh_note, **kw)
def PIL(pid, name, zh, en_note, zh_note, ids, **kw): return b.PIL(pid, name, zh, *C(pid), en_note, zh_note, ids, **kw)
S = b.S

def raw(title, start, end, lang="ru"):
    """the page's own text between two markers; the markers are matched with no-break and thin spaces read as spaces"""
    t = ws.text(os.path.join(WSR, lang), title)
    n = re.sub("[\xa0\u202f\u2009\u2007]", " ", t)
    i = n.find(start)
    assert i >= 0, (title, start)
    j = n.find(end, i)
    assert j >= 0, (title, start, end)
    return t[i:j + len(end)]

def flow(s):
    """a hard-wrapped plain-text page: lines joined, doubled spaces written as one"""
    return re.sub(r" {2,}", " ", s.replace("\n", " "))

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

RU = lambda t: ws.url("ru", t)
PUSH = ("Alexander Pushkin", "亚历山大·普希金", "Александр Пушкин")
LERM = ("Mikhail Lermontov", "米哈伊尔·莱蒙托夫", "Михаил Лермонтов")
CHEK = ("Anton Chekhov", "安东·契诃夫", "Антон Чехов")
T_KD = "Капитанская дочка (Пушкин)/1978 (СО)"
T_PD = "Пиковая дама (Пушкин)"
T_BG = "Борис Годунов (Пушкин)"
T_VC = "Воспоминания в Царском Селе (Навис покров угрюмой нощи — Пушкин)"
T_BO = "Бородино (Лермонтов)/ПСС 1989 (СО)"
T_NP = "Невский проспект (Гоголь)/Версия 2"
T_MU = "Муму (Тургенев)"
T_MD = "Записки из Мёртвого дома (Достоевский)/Часть 1/Глава 1"
T_LE = "Левша (Лесков)/Версия 2"
T_SA = "Остров Сахалин (Чехов)/Глава 02"
T_KU = "На поле Куликовом (Блок)/3"
T_CM = "Стихи о Москве (Цветаева)/8"
T_RA = "Путешествие из Петербурга в Москву (Радищев)"
T_AK = "Детские годы Багрова-внука (С. Т. Аксаков)/Уфа"
T_GI = "Москва и москвичи (Гиляровский)/Хитровка"
T_TA = "Герой нашего времени (Лермонтов)/СО/Тамань"
T_O1 = "Евгений Онегин (Пушкин)/ПСС 1977 (СО)/Глава 1"
T_O7 = "Евгений Онегин (Пушкин)/ПСС 1977 (СО)/Глава 7"
T_CP = "Преступление и наказание (Достоевский)/Часть VI/Глава VIII"
T_GD = "Детство (Горький)/I"
T_WP = "Война и мир (Толстой)/Том 3"
T_ML = "В лесах. Книга 2-я (Мельников-Печерский)"
T_MS = "Michel Strogoff/Partie 1/Chapitre 5"

# ============================== books ==============================
books = [
    BK("captains-daughter", "The Captain's Daughter", "上尉的女儿", "Капитанская дочка", *PUSH, "1836", src=RU("Капитанская дочка (Пушкин)"),
       aliases=["Pugachev", "Grinyov", "Belogorsk", "普加乔夫", "Пугачёв"]),
    BK("queen-of-spades", "The Queen of Spades", "黑桃皇后", "Пиковая дама", *PUSH, "1834", src=RU(T_PD),
       aliases=["Hermann", "Germann", "three cards", "赫尔曼", "Германн"]),
    BK("boris-godunov", "Boris Godunov", "鲍里斯·戈都诺夫", "Борис Годунов", *PUSH, "1831", src=RU(T_BG),
       aliases=["Godunov", "False Dmitry", "Pimen", "戈都诺夫", "Годунов"]),
    BK("reminiscences-tsarskoye", "Reminiscences in Tsarskoye Selo", "皇村回忆", "Воспоминания в Царском Селе", *PUSH, "1814", src=RU(T_VC),
       aliases=["Recollections in Tsarskoe Selo", "Lyceum", "皇村", "Лицей"]),
    BK("borodino-lermontov", "Borodino", "波罗金诺", "Бородино", *LERM, "1837", src=RU("Бородино (Лермонтов)"),
       aliases=["Скажи-ка, дядя", "Battle of Borodino"]),
    BK("nevsky-prospekt", "Nevsky Prospekt", "涅瓦大街", "Невский проспект", "Nikolai Gogol", "尼古拉·果戈理", "Николай Гоголь", "1835", src=RU("Невский проспект (Гоголь)"),
       aliases=["Nevsky Prospect", "Petersburg Tales", "彼得堡故事", "Piskaryov", "Pirogov"]),
    BK("mumu", "Mumu", "木木", "Муму", "Ivan Turgenev", "伊万·屠格涅夫", "Иван Тургенев", "1854", src=RU(T_MU), aliases=["Gerasim", "格拉西姆", "Герасим"]),
    BK("house-of-the-dead", "Notes from the House of the Dead", "死屋手记", "Записки из Мёртвого дома", "Fyodor Dostoevsky", "陀思妥耶夫斯基", "Фёдор Достоевский", "1860–1862",
       src=RU("Записки из Мёртвого дома (Достоевский)"), aliases=["The House of the Dead", "Goryanchikov", "Omsk", "鄂木斯克"]),
    BK("lefty", "The Tale of Cross-eyed Lefty from Tula and the Steel Flea", "左撇子", "Левша", "Nikolai Leskov", "尼古拉·列斯科夫", "Николай Лесков", "1881", src=RU("Левша (Лесков)"),
       aliases=["Lefty", "The Steel Flea", "Levsha", "钢跳蚤", "Platov"]),
    BK("sakhalin-island", "Sakhalin Island", "萨哈林旅行记", "Остров Сахалин", *CHEK, "1895", src=RU("Остров Сахалин (Чехов)"),
       aliases=["The Island of Sakhalin", "A Journey to Sakhalin", "库页岛", "萨哈林岛"]),
    BK("on-the-field-of-kulikovo", "On the Field of Kulikovo", "在库利科沃原野上", "На поле Куликовом", "Alexander Blok", "亚历山大·勃洛克", "Александр Блок", "1908",
       src=RU("На поле Куликовом (Блок)"), aliases=["Kulikovo", "Nepryadva", "Mamai", "库利科沃"]),
    BK("poems-about-moscow", "Poems about Moscow", "莫斯科诗抄", "Стихи о Москве", "Marina Tsvetaeva", "玛丽娜·茨维塔耶娃", "Марина Цветаева", "1916",
       src=RU("Стихи о Москве (Цветаева)"), aliases=["Tsvetaeva", "Verses about Moscow", "茨维塔耶娃"]),
    BK("journey-petersburg-moscow", "A Journey from St Petersburg to Moscow", "从彼得堡到莫斯科旅行记", "Путешествие из Петербурга в Москву", "Alexander Radishchev", "亚历山大·拉季舍夫",
       "Александр Радищев", "1790", src=RU(T_RA), aliases=["Radishchev", "拉吉舍夫"]),
    BK("childhood-years-bagrov", "Childhood Years of Bagrov the Grandson", "孙子巴格罗夫的童年", "Детские годы Багрова-внука", "Sergei Aksakov", "谢尔盖·阿克萨科夫", "Сергей Аксаков", "1858",
       src=RU("Детские годы Багрова-внука (С. Т. Аксаков)"), aliases=["Aksakov", "The Scarlet Flower", "A Family Chronicle", "Years of Childhood", "阿克萨科夫"]),
    BK("moscow-and-muscovites", "Moscow and Muscovites", "莫斯科和莫斯科人", "Москва и москвичи", "Vladimir Gilyarovsky", "弗拉基米尔·吉利亚罗夫斯基", "Владимир Гиляровский", "1926",
       src=RU("Москва и москвичи (Гиляровский)"), aliases=["Gilyarovsky", "Khitrovka", "Uncle Gilyai", "吉利亚罗夫斯基"]),
    BK("childhood-gorky", "Childhood", "童年", "Детство", "Maxim Gorky", "马克西姆·高尔基", "Максим Горький", "1913–1914", src=RU("Детство (Горький)"),
       aliases=["My Childhood", "Alyosha Peshkov", "Kashirin", "阿廖沙"]),
    BK("michael-strogoff", "Michael Strogoff", "沙皇的信使", "Michel Strogoff", "Jules Verne", "儒勒·凡尔纳", "Jules Verne", "1876", lang="fr",
       src=ws.url("fr", "Michel Strogoff"), aliases=["The Courier of the Czar", "Michel Strogoff", "米歇尔·斯特罗戈夫", "Irkutsk"]),
    BK("in-the-forests", "In the Forests", "在森林中", "В лесах", "Pavel Melnikov-Pechersky", "帕维尔·梅利尼科夫-佩切尔斯基", "Павел Мельников-Печерский", "1871–1874",
       src=RU(T_ML), aliases=["Melnikov", "Kitezh", "Svetloyar", "基捷日", "Китеж"]),
    BK("commandant-of-bugulma", "The Commandant of the Town of Bugulma", "布古利马城防司令", "Velitelem města Bugulmy", "Jaroslav Hašek", "雅罗斯拉夫·哈谢克", "Jaroslav Hašek", "1921", lang="cs",
       aliases=["Bugulma stories", "The Red Commissar", "Hasek", "Гашек", "Yerokhimov"]),
    BK("snow-maiden", "The Snow Maiden", "雪姑娘", "Снегурочка", "Alexander Ostrovsky", "亚历山大·奥斯特洛夫斯基", "Александр Островский", "1873",
       aliases=["Snegurochka", "The Storm", "Ostrovsky", "Berendey", "大雷雨"]),
    BK("who-is-happy-in-russia", "Who Is Happy in Russia?", "谁在俄罗斯能过好日子", "Кому на Руси жить хорошо", "Nikolay Nekrasov", "尼古拉·涅克拉索夫", "Николай Некрасов", "1866–1877",
       aliases=["Who Lives Well in Russia", "Who Can Be Happy and Free in Russia", "Nekrasov", "涅克拉索夫"]),
    BK("three-sisters", "Three Sisters", "三姊妹", "Три сестры", *CHEK, "1901", aliases=["The Three Sisters", "Prozorov", "To Moscow", "三姐妹"]),
    BK("life-of-arseniev", "The Life of Arseniev", "阿尔谢尼耶夫的一生", "Жизнь Арсеньева", "Ivan Bunin", "伊万·蒲宁", "Иван Бунин", "1930",
       aliases=["Arsenyev", "The Well of Days", "Bunin", "Yelets"]),
    BK("anna-snegina", "Anna Snegina", "安娜·斯涅金娜", "Анна Снегина", "Sergei Yesenin", "谢尔盖·叶赛宁", "Сергей Есенин", "1925",
       aliases=["Yesenin", "Esenin", "Konstantinovo", "叶赛宁", "Есенин"]),
    BK("voronezh-notebooks", "Voronezh Notebooks", "沃罗涅日笔记本", "Воронежские тетради", "Osip Mandelstam", "奥西普·曼德尔施塔姆", "Осип Мандельштам", "1935–1937", pd=False,
       aliases=["Mandelstam", "Mandelshtam", "Voronezh", "曼德尔施塔姆", "Мандельштам"]),
    BK("meshchora-side", "The Meshchora Side", "梅晓拉地区", "Мещёрская сторона", "Konstantin Paustovsky", "康斯坦丁·帕乌斯托夫斯基", "Константин Паустовский", "1939", pd=False,
       aliases=["Meshchera", "Paustovsky", "Solotcha", "帕乌斯托夫斯基", "梅肖拉"]),
    BK("dersu-uzala", "Dersu Uzala", "德尔苏·乌扎拉", "Дерсу Узала", "Vladimir Arsenyev", "弗拉基米尔·阿尔谢尼耶夫", "Владимир Арсеньев", "1923", src=RU("Дерсу Узала"),
       aliases=["Dersu the Trapper", "Across the Ussuri Kray", "Arseniev", "在乌苏里的莽林中", "德尔苏"]),
    BK("matryonas-place", "Matryona's Place", "玛特辽娜的家", "Матрёнин двор", "Aleksandr Solzhenitsyn", "亚历山大·索尔仁尼琴", "Александр Солженицын", "1963", pd=False,
       aliases=["Matryona's Home", "Matryona's House", "Talnovo", "玛特廖娜的家"]),
    BK("village-folk", "Country Folk (stories)", "乡村居民（短篇集）", "Сельские жители", "Vasily Shukshin", "瓦西里·舒克申", "Василий Шукшин", "1963", pd=False,
       aliases=["Shukshin", "Srostki", "The Red Snowball Tree", "舒克申", "Шукшин"]),
    BK("last-bow", "The Last Bow", "最后的问候", "Последний поклон", "Viktor Astafyev", "维克托·阿斯塔菲耶夫", "Виктор Астафьев", "1968", pd=False,
       aliases=["Astafyev", "Astafiev", "Ovsyanka", "Tsar-Fish", "鱼王", "阿斯塔菲耶夫"]),
    BK("in-a-room-and-a-half", "In a Room and a Half", "一个半房间", None, "Joseph Brodsky", "约瑟夫·布罗茨基", "Иосиф Бродский", "1985", pd=False, lang="en",
       aliases=["Less Than One", "Brodsky", "Muruzi House", "小于一", "布罗茨基", "Бродский"]),
    BK("front-line-stalingrad", "Front-line Stalingrad", "在斯大林格勒的战壕里", "В окопах Сталинграда", "Viktor Nekrasov", "维克托·涅克拉索夫", "Виктор Некрасов", "1946", pd=False,
       aliases=["In the Trenches of Stalingrad", "Kerzhentsev", "Mamayev Kurgan"]),
    BK("heart-of-parma", "The Heart of Parma", "帕尔马之心", "Сердце пармы", "Alexei Ivanov", "阿列克谢·伊万诺夫", "Алексей Иванов", "2003", pd=False,
       aliases=["Cherdyn", "Perm the Great", "Prince Mikhail", "Сердце Пармы"]),
    BK("gorky-park", "Gorky Park", "高尔基公园", None, "Martin Cruz Smith", "马丁·克鲁兹·史密斯", None, "1981", pd=False, lang="en",
       aliases=["Arkady Renko", "Renko", "伦科"]),
    BK("winter-queen", "The Winter Queen", "阿扎泽尔", "Азазель", "Boris Akunin", "鲍里斯·阿库宁", "Борис Акунин", "1998", pd=False,
       aliases=["Azazel", "Fandorin", "Erast Fandorin", "凡多林", "Фандорин"]),
    BK("tale-of-igors-campaign", "The Tale of Igor's Campaign", "伊戈尔远征记", "Слово о полку Игореве", "Anonymous", "佚名", None, "c. 1185",
       aliases=["The Lay of Igor's Host", "The Song of Igor", "Slovo o polku Igoreve", "伊戈尔出征记"]),
    BK("malachite-box", "The Malachite Box", "孔雀石箱", "Малахитовая шкатулка", "Pavel Bazhov", "帕维尔·巴若夫", "Павел Бажов", "1939",
       aliases=["The Malachite Casket", "Bazhov", "The Mistress of the Copper Mountain", "The Stone Flower", "铜山娘娘", "巴若夫"]),
    BK("children-of-the-arbat", "Children of the Arbat", "阿尔巴特街的儿女", "Дети Арбата", "Anatoly Rybakov", "阿纳托利·雷巴科夫", "Анатолий Рыбаков", "1987", pd=False,
       aliases=["Rybakov", "Sasha Pankratov", "Arbat", "雷巴科夫"]),
    BK("blockade-book", "A Book of the Blockade", "围困纪事", "Блокадная книга", "Ales Adamovich and Daniil Granin", "阿达莫维奇、格拉宁", "Алесь Адамович, Даниил Гранин", "1977–1981", pd=False,
       aliases=["Leningrad Under Siege", "The Blockade Book", "Granin", "Adamovich", "Siege of Leningrad", "列宁格勒围困"]),
    BK("disappearing-earth", "Disappearing Earth", "消失的大地", None, "Julia Phillips", "朱莉娅·菲利普斯", None, "2019", pd=False, lang="en",
       aliases=["Kamchatka", "Petropavlovsk", "堪察加"]),
    BK("what-is-to-be-done", "What Is to Be Done?", "怎么办？", "Что делать?", "Nikolay Chernyshevsky", "尼古拉·车尔尼雪夫斯基", "Николай Чернышевский", "1863",
       aliases=["Chernyshevsky", "Vera Pavlovna", "Rakhmetov", "车尔尼雪夫斯基"]),
    BK("vasily-tyorkin", "Vasily Tyorkin", "瓦西里·焦尔金", "Василий Тёркин", "Aleksandr Tvardovsky", "亚历山大·特瓦尔多夫斯基", "Александр Твардовский", "1942–1945", pd=False,
       aliases=["Vasili Tyorkin", "Terkin", "A Book About a Soldier", "Tvardovsky", "特瓦尔多夫斯基", "Тёркин"]),
    BK("the-monastery-prilepin", "The Monastery", "修道院", "Обитель", "Zakhar Prilepin", "扎哈尔·普里列平", "Захар Прилепин", "2014", pd=False,
       aliases=["Obitel", "Prilepin", "Solovki", "索洛韦茨基"]),
]

# ============================== places ==============================
places = [
    # ---- Pushkin ----
    ORIG("ru-orenburg", "Orenburg", "奥伦堡",
         "The steppe fortress town that Pugachev's rebels besieged from October 1773 to March 1774. Pushkin came here in September 1833 to gather material on the rising, and The Captain's Daughter sends its young officer Grinyov through the town's gates during the siege",
         "草原上的要塞城市。1773 年 10 月到 1774 年 3 月，普加乔夫的起义军围困此城。普希金 1833 年 9 月来这里搜集起义的材料，《上尉的女儿》里年轻军官格里尼奥夫就在围城期间进出这座城的城门"),
    PROTO("ru-queen-of-spades-house", "'House of the Queen of Spades', St Petersburg", "“黑桃皇后之家”，圣彼得堡",
          "The house of Princess Natalya Golitsyna at Malaya Morskaya 10. Petersburg tradition takes the old princess for the model of Pushkin's Countess, and her house for the one Hermann stands in front of",
          "小海军街 10 号，娜塔莉亚·戈利岑娜公爵夫人的宅子。彼得堡人历来认为这位老公爵夫人是普希金笔下老伯爵夫人的原型，赫尔曼深夜站在门前的那幢房子就是这里"),
    ORIG("ru-novodevichy", "Novodevichy Convent, Moscow", "新圣女修道院，莫斯科",
         "In 1598, after Tsar Fyodor's death, his widow Irina, Boris Godunov's sister, withdrew to this convent, and the crowd was brought to the field outside its walls to beg Boris to take the crown. Pushkin sets a scene of his tragedy here",
         "1598 年沙皇费奥多尔死后，他的遗孀、鲍里斯·戈都诺夫的妹妹伊琳娜退居这座修道院，人群被带到墙外的原野上，恳求鲍里斯登基。普希金的悲剧有一场就写这里"),
    ORIG("ru-lyceum", "Imperial Lyceum, Tsarskoye Selo", "皇村学校",
         "Pushkin was a pupil of the Lyceum's first class from 1811 to 1817. At the public examination in January 1815 he recited this poem in front of the old poet Derzhavin. The building, joined to the Catherine Palace, is a museum",
         "普希金是皇村学校第一届学生，1811 年到 1817 年在此就读。1815 年 1 月的公开考试上，他当着老诗人杰尔查文的面朗诵了这首诗。校舍与叶卡捷琳娜宫相连，今为纪念馆"),
    ORIG("ru-summer-garden", "Summer Garden, St Petersburg", "夏花园，圣彼得堡",
         "The formal garden Peter the Great laid out on the Neva from 1704. In the first chapter of Eugene Onegin the boy Onegin is taken here for walks by his French tutor",
         "彼得大帝 1704 年起在涅瓦河畔兴建的规整式花园。《叶甫盖尼·奥涅金》第一章里，小奥涅金由法国家庭教师带到这里散步"),
    ORIG("ru-petrovsky-palace", "Petrovsky Palace, Moscow", "彼得罗夫宫，莫斯科",
         "The red-and-white travelling palace built by Matvey Kazakov for Catherine II on the Petersburg road. Napoleon moved here from the Kremlin in September 1812 while Moscow burned. The Larins' coach passes it as Tatyana is driven into Moscow",
         "马特维·卡扎科夫为叶卡捷琳娜二世在通往彼得堡的大道旁修建的红白两色行宫。1812 年 9 月莫斯科大火时，拿破仑从克里姆林宫迁到这里。塔吉雅娜一家的马车进莫斯科时从它旁边经过"),
    PIL("ru-boldino", "Boldino", "博尔金诺",
        "The Pushkin family estate in the Nizhny Novgorod region. Held here by cholera quarantine in the autumn of 1830, Pushkin finished Eugene Onegin and wrote The Tales of Belkin and the Little Tragedies; he came back in the autumn of 1833 and wrote The Bronze Horseman and The Queen of Spades",
        "下诺夫哥罗德地区的普希金家族庄园。1830 年秋天普希金因霍乱检疫滞留于此，写完了《叶甫盖尼·奥涅金》，写出《别尔金小说集》和几部“小悲剧”；1833 年秋天再来，写了《青铜骑士》和《黑桃皇后》",
        ["eugene-onegin", "tales-of-belkin", "bronze-horseman", "queen-of-spades"]),
    PIL("ru-moika-12", "Pushkin's Last Apartment, Moika 12", "普希金故居，莫伊卡河 12 号",
        "Pushkin rented this apartment on the Moika in the autumn of 1836; he finished The Captain's Daughter here. He was brought back to it wounded from the duel with d'Anthès and died in his study on 29 January (10 February) 1837",
        "普希金 1836 年秋天租下莫伊卡河畔的这套住宅，《上尉的女儿》在这里完稿。同丹特士决斗受伤后他被抬回这里，1837 年 1 月 29 日（公历 2 月 10 日）死在书房里",
        ["captains-daughter", "eugene-onegin", "bronze-horseman"]),
    PIL("ru-svyatogorsky", "Pushkin's Grave, Svyatogorsky Monastery", "普希金墓，圣山修道院",
        "Pushkin was buried in February 1837 beside the Assumption Cathedral of this monastery, a few kilometres from Mikhailovskoye, next to his mother. Dovlatov's guide-narrator in Pushkin Hills leads his tour groups here",
        "1837 年 2 月，普希金葬在这座修道院的圣母升天大教堂旁，紧挨着母亲的墓，离米哈伊洛夫斯科耶只有几公里。多甫拉托夫《普希金山》里当导游的叙述者就带着旅行团到这里来",
        ["eugene-onegin", "pushkin-hills"]),
    # ---- Lermontov, Gogol, Turgenev, Dostoevsky ----
    ORIG("ru-taman", "Lermontov Museum, Taman", "莱蒙托夫故居博物馆，塔曼",
         "Lermontov stopped in this Cossack settlement on the Kerch Strait in September 1837, on his way to the army in the Caucasus, and turned what happened to him into the 'Taman' chapter of A Hero of Our Time. A thatched hut on the cliff has been rebuilt as a museum",
         "1837 年 9 月，莱蒙托夫去高加索部队途中在刻赤海峡边的这个哥萨克村镇停留，把这段经历写成了《当代英雄》里的《塔曼》一章。崖上的茅屋已复建为博物馆", rough_coast=True),
    PIL("ru-tarkhany", "Tarkhany", "塔尔罕内",
        "The Penza estate of Lermontov's grandmother Yelizaveta Arsenyeva, where he spent his childhood. After the duel at Pyatigorsk his coffin was brought here in 1842 and placed in the family vault",
        "莱蒙托夫外祖母伊丽莎白·阿尔谢尼耶娃在奔萨的庄园，他在这里度过童年。在皮亚季戈尔斯克决斗身亡后，他的灵柩 1842 年运回这里，安放在家族墓室中",
        ["hero-of-our-time", "borodino-lermontov"]),
    PROTO("ru-mumu-house", "'Mumu's House', Ostozhenka 37, Moscow", "“木木之家”，奥斯托任卡街 37 号",
          "The wooden house with columns that Turgenev's mother Varvara Petrovna rented from 1840 to 1850. The story's tyrannical lady is drawn from her, and the deaf-mute yardman Gerasim from her serf Andrei. It is now the Turgenev Museum",
          "屠格涅夫的母亲瓦尔瓦拉·彼得罗夫娜 1840 年到 1850 年租住的带圆柱的木屋。小说里专横的女主人以她为原型，聋哑的看院人格拉西姆则以她的农奴安德烈为原型。今为屠格涅夫博物馆"),
    ORIG("ru-omsk-fortress", "Omsk Fortress", "鄂木斯克要塞",
         "Dostoevsky served four years of hard labour, 1850 to 1854, in the convict prison of this fortress, and Notes from the House of the Dead is the book of those years. The prison is gone; the commandant's house holds the Dostoevsky museum",
         "陀思妥耶夫斯基 1850 年到 1854 年在这座要塞的苦役监狱里服了四年苦役，《死屋手记》写的就是这四年。监狱已不存，要塞司令的房子今为陀思妥耶夫斯基文学博物馆"),
    ORIG("ru-sennaya", "Sennaya Square, St Petersburg", "干草市场广场，圣彼得堡",
         "The Haymarket, the crowded heart of the poor quarter where Crime and Punishment is set. Raskolnikov overhears here when the pawnbroker will be alone, and at the end he kneels in the middle of the square and kisses the ground",
         "干草市场是《罪与罚》所写的贫民区里人最挤的地方。拉斯柯尔尼科夫在这里偶然听到放债老太婆何时独自在家；小说结尾，他跪在广场中央亲吻土地"),
    PROTO("ru-optina", "Optina Pustyn", "奥普塔修道院",
          "The hermitage near Kozelsk known for its elders. Dostoevsky came here in June 1878 with Vladimir Solovyov, shortly after the death of his small son Alyosha, and talked with the elder Ambrose; the monastery and the elder Zosima of The Brothers Karamazov draw on the visit. Tolstoy also came several times",
          "科泽利斯克附近以长老制闻名的隐修院。1878 年 6 月，陀思妥耶夫斯基在幼子阿廖沙夭折后不久，同弗拉基米尔·索洛维约夫一起来到这里，见了阿姆夫罗西长老；《卡拉马佐夫兄弟》里的修道院和佐西马长老都带着这次访问的印记。托尔斯泰也来过好几次",
          book_ids=["brothers-karamazov"]),
    # ---- Tolstoy, Leskov, Ostrovsky, Nekrasov ----
    PIL("ru-yasnaya-polyana", "Yasnaya Polyana", "亚斯纳亚·波良纳",
        "Tolstoy was born on this estate near Tula in 1828 and lived here most of his life; War and Peace and Anna Karenina were written in the house. His grave, an unmarked grass mound, is in the wood at the edge of a ravine",
        "托尔斯泰 1828 年生于图拉附近的这座庄园，一生大部分时间住在这里，《战争与和平》和《安娜·卡列尼娜》都写于这幢房子里。他的墓是林中沟谷边一座没有墓碑的草冢",
        ["war-and-peace", "anna-karenina", "resurrection-tolstoy"]),
    PIL("ru-astapovo", "Lev Tolstoy Station (Astapovo)", "列夫·托尔斯泰站（阿斯塔波沃）",
        "Having left home in secret, the eighty-two-year-old Tolstoy fell ill on the train and was carried into the stationmaster's house at Astapovo, where he died on 7 (20) November 1910. The station was later renamed after him and the house is a museum",
        "八十二岁的托尔斯泰秘密离家出走，在火车上病倒，被抬进阿斯塔波沃站站长的家，1910 年 11 月 7 日（公历 20 日）在那里去世。车站后来以他的名字命名，站长的房子今为纪念馆",
        ["war-and-peace", "anna-karenina"]),
    ORIG("ru-poklonnaya", "Poklonnaya Hill, Moscow", "俯首山，莫斯科",
         "The hill on the old Smolensk road from which travellers first saw Moscow. In War and Peace Kutuzov halts here before the council at Fili, and on 2 September 1812 Napoleon stands on it waiting in vain for a deputation with the keys of the city. It is now Victory Park",
         "旧斯摩棱斯克大道上的小山，旅人从这里第一眼望见莫斯科。《战争与和平》里库图佐夫在菲利会议前在此停留；1812 年 9 月 2 日，拿破仑站在山上，白白等着献城钥匙的代表团。今为胜利公园"),
    ORIG("ru-tula-lefty", "Tula Arms Museum", "图拉兵器博物馆",
         "Tula has made arms since Peter the Great founded the works in 1712. Leskov's tale has its gunsmiths, with the cross-eyed Lefty among them, shoe a dancing steel flea made by the English. The city's arms museum tells the three-hundred-year story of the works",
         "彼得大帝 1712 年在图拉设兵工厂，此后这座城一直造枪。列斯科夫的故事里，图拉的枪匠们，其中有斜眼的左撇子，给英国人造的会跳舞的钢跳蚤钉上了马掌。城里的兵器博物馆讲述着兵工厂三百年的历史"),
    PIL("ru-shchelykovo", "Shchelykovo", "谢雷科沃",
        "The dramatist Alexander Ostrovsky's estate in the Kostroma forests. He spent his summers here from 1867, wrote the verse fairy play The Snow Maiden out of its woods and village customs, and died at his desk here in 1886",
        "剧作家亚历山大·奥斯特洛夫斯基在科斯特罗马林区的庄园。1867 年起他每年在此消夏，童话诗剧《雪姑娘》就取材于这里的树林和乡间风俗；1886 年他在这里的书桌前去世",
        ["snow-maiden"]),
    PIL("ru-karabikha", "Karabikha", "卡拉比哈",
        "The estate outside Yaroslavl that Nekrasov bought in 1861. He spent his summers here, and much of his poetry of peasant Russia, Who Is Happy in Russia? among it, was worked on in the house",
        "涅克拉索夫 1861 年买下的雅罗斯拉夫尔城外庄园。他夏天常住在这里，许多写农民俄罗斯的诗，包括《谁在俄罗斯能过好日子》，都在这幢房子里写过",
        ["who-is-happy-in-russia"]),
    # ---- Chekhov, Gorky, the Volga and the Urals ----
    ORIG("ru-aleksandrovsk", "Aleksandrovsk-Sakhalinsky", "萨哈林的亚历山德罗夫斯克",
         "The administrative post of the Sakhalin penal colony. Chekhov landed here in July 1890 after crossing Siberia, spent three months on the island and filled in a census card for nearly every convict and settler. A museum of the book stands in the town",
         "萨哈林流放苦役地的行政中心。契诃夫横穿西伯利亚后，1890 年 7 月在这里登岸，在岛上住了三个月，几乎给每一个苦役犯和移民填了一张调查卡片。城里有一座以这本书为主题的博物馆", rough_coast=True),
    PROTO("ru-perm", "Perm (the House with Figures)", "彼尔姆（“有雕像的房子”）",
          "Pasternak spent several months of 1916 at Vsevolodo-Vilva in the Perm region, and Perm is taken as the model of Yuriatin in Doctor Zhivago; the Gribushin house is identified with the novel's 'house with figures'. Chekhov wrote to Gorky that Three Sisters takes place in a provincial town 'like Perm'",
          "帕斯捷尔纳克 1916 年在彼尔姆省的弗谢沃洛多-维利瓦住过几个月，彼尔姆被认为是《日瓦戈医生》中尤里亚金城的原型；城里的格里布申宅被认作小说里“有雕像的房子”。契诃夫写信告诉高尔基，《三姊妹》的故事发生在一座“像彼尔姆那样的”外省城市",
          book_ids=["three-sisters"]),
    ORIG("ru-kashirin-house", "Kashirin House, Nizhny Novgorod", "卡希林小屋，下诺夫哥罗德",
         "The small wooden house of the dyer Vasily Kashirin, Gorky's grandfather. The boy Alyosha Peshkov was brought here in 1871 after his father's death, and Childhood is the story of the household. It is a museum",
         "染坊主瓦西里·卡希林的小木屋，他是高尔基的外祖父。1871 年父亲死后，小阿廖沙·彼什科夫被带到这里，《童年》写的就是这一家人。今为博物馆"),
    ORIG("ru-nizhny-fair", "Nizhny Novgorod Fair", "下诺夫哥罗德集市",
         "The great fair moved here from Makaryev in 1817 and for a century drew merchants from Europe and Asia each summer. Jules Verne's courier Michael Strogoff reaches it by train from Moscow and takes the Volga steamer on from here. The main fair building of 1890 still stands",
         "这个大集市 1817 年从马卡里耶夫迁来，此后一百年里每年夏天吸引着欧亚各地的商人。凡尔纳笔下的沙皇信使米歇尔·斯特罗戈夫从莫斯科坐火车到这里，再换乘伏尔加河上的轮船。1890 年建成的集市主楼至今还在"),
    ORIG("ru-svetloyar", "Lake Svetloyar", "斯韦特洛亚尔湖",
         "A small round lake in the forests beyond the Volga. Legend says the city of Kitezh sank into it, or became invisible, to escape Batu's army, and pilgrims have long gathered on its hills. Melnikov-Pechersky's novel of the Old Believer merchants beyond the Volga tells the legend",
         "伏尔加河对岸森林里的一个圆形小湖。传说基捷日城为躲避拔都的军队沉入湖中，或者隐了形；朝圣的人历来聚在湖边的山丘上。梅利尼科夫-佩切尔斯基写伏尔加河对岸旧礼仪派商人的长篇小说讲了这个传说"),
    ORIG("ru-bugulma", "Hašek Museum, Bugulma", "哈谢克博物馆，布古利马",
         "In the autumn of 1918 Jaroslav Hašek, then serving with the Red Army, was deputy commandant of this small town in Tatarstan. Back in Prague he turned those weeks into a cycle of comic stories. The wooden house where he lived and worked is a museum",
         "1918 年秋天，在红军中服役的雅罗斯拉夫·哈谢克当过鞑靼斯坦这座小城的副城防司令。回到布拉格后，他把这几个星期写成一组幽默小说。他当年居住和办公的木屋今为博物馆"),
    PIL("ru-ufa-aksakov", "Aksakov House Museum, Ufa", "阿克萨科夫故居博物馆，乌法",
        "Sergei Aksakov was born in Ufa in 1791. This wooden house above the Belaya river belonged to his mother's family, and the Ufa chapters of his childhood memoir take place in it",
        "谢尔盖·阿克萨科夫 1791 年生于乌法。白河岸上的这幢木屋属于他母亲的娘家，他童年回忆录中写乌法的几章就发生在这里",
        ["childhood-years-bagrov"]),
    PIL("ru-goncharov", "Goncharov Museum, Ulyanovsk", "冈察洛夫博物馆，乌里扬诺夫斯克",
        "Ivan Goncharov was born in 1812 in this merchant house in Simbirsk, as the Volga town was then called. The sleepy Oblomovka of Oblomov's dream draws on the Simbirsk of his childhood",
        "伊万·冈察洛夫 1812 年生于辛比尔斯克（这座伏尔加河城市当时的名字）的这幢商人宅子里。《奥勃洛莫夫》里梦中昏昏欲睡的奥勃洛莫夫卡带着他童年时辛比尔斯克的影子",
        ["oblomov"]),
    PIL("ru-bazhov", "Bazhov House Museum, Yekaterinburg", "巴若夫故居博物馆，叶卡捷琳堡",
        "Pavel Bazhov lived in this log house from 1914 and again from the 1920s until his death in 1950. Here he wrote down the Urals miners' tales of The Malachite Box, with the Mistress of the Copper Mountain and the stone flower",
        "帕维尔·巴若夫 1914 年起住在这幢原木房子里，1920 年代搬回，一直住到 1950 年去世。他在这里写下了《孔雀石箱》里乌拉尔矿工的故事，有铜山娘娘，也有石花",
        ["malachite-box"]),
    ORIG("ru-cherdyn", "Cherdyn", "切尔登",
         "A small town on the Kolva in the northern Urals, once the chief town of Perm the Great. Alexei Ivanov's novel is set here in the fifteenth century, when its prince Mikhail stands between the Voguls of the forest and the growing power of Moscow",
         "乌拉尔北部科尔瓦河畔的小城，曾是“大彼尔姆”的首府。阿列克谢·伊万诺夫的小说写的是十五世纪的这里：米哈伊尔公夹在森林里的沃古尔人和日益强大的莫斯科之间"),
    # ---- Moscow ----
    PIL("ru-novodevichy-cemetery", "Novodevichy Cemetery, Moscow", "新圣女公墓，莫斯科",
        "The cemetery beside the convent where Chekhov, Gogol (reburied here in 1931), Bulgakov and Mayakovsky lie. The stone on Bulgakov's grave came from Gogol's first grave",
        "修道院旁的公墓，契诃夫、果戈理（1931 年迁葬于此）、布尔加科夫和马雅可夫斯基都葬在这里。布尔加科夫墓上的那块石头来自果戈理最初的墓",
        ["cherry-orchard", "dead-souls", "master-and-margarita", "cloud-in-trousers"]),
    ORIG("ru-tsvetaeva-house", "Tsvetaeva House Museum, Moscow", "茨维塔耶娃故居博物馆，莫斯科",
         "Marina Tsvetaeva lived in the apartment at Borisoglebsky Lane 6 from 1914 to 1922, and the Poems about Moscow were written here in 1916",
         "玛丽娜·茨维塔耶娃 1914 年到 1922 年住在鲍里索格列布斯基巷 6 号的这套住宅里，《莫斯科诗抄》1916 年写于此"),
    ORIG("ru-khitrovka", "Khitrovka (Khitrovskaya Square), Moscow", "希特罗夫卡，莫斯科",
         "Until the 1920s the square was Moscow's labour market, ringed with doss-houses and thieves' dens. The reporter Gilyarovsky knew it better than anyone and led Stanislavsky's actors through it in 1902 when they were preparing Gorky's The Lower Depths",
         "直到 1920 年代，这个广场都是莫斯科的劳力市场，四周全是小客栈和贼窝。记者吉利亚罗夫斯基比谁都熟悉它；1902 年排演高尔基的《底层》时，他带着斯坦尼斯拉夫斯基的演员们来这里看过"),
    ORIG("ru-bulgakov-house", "Bulgakov House, Bolshaya Sadovaya 10", "布尔加科夫故居，大花园街 10 号",
         "Bulgakov lived in communal flat no. 50 of this building from 1921 to 1924, and gave the address, as 'Sadovaya 302-bis', to the 'evil apartment' where Woland and his retinue settle",
         "布尔加科夫 1921 年到 1924 年住在这幢楼的 50 号合住公寓里，后来把这个地址改成“花园街 302 号乙”，写成沃兰德一伙落脚的那套“凶宅”"),
    ORIG("ru-pashkov-house", "Pashkov House, Moscow", "帕什科夫大楼，莫斯科",
         "The eighteenth-century mansion on the hill facing the Kremlin, long part of the state library. Woland takes his leave of Moscow from its roof terrace",
         "克里姆林宫对面山坡上的十八世纪宅邸，长期属于国家图书馆。沃兰德就是在它的屋顶平台上向莫斯科告别的"),
    ORIG("ru-arbat", "The Arbat, Moscow", "阿尔巴特街，莫斯科",
         "The old Moscow street where Anatoly Rybakov grew up, at no. 51, and where his novel's young people grow up too",
         "莫斯科的老街。阿纳托利·雷巴科夫在 51 号长大，他小说里的那群年轻人也在这条街上长大"),
    ORIG("ru-gorky-park", "Gorky Park, Moscow", "高尔基公园，莫斯科",
         "Moscow's Central Park of Culture and Rest on the river, opened in 1928. Martin Cruz Smith's thriller begins with three bodies found here under the snow",
         "莫斯科河边的中央文化休息公园，1928 年开放。马丁·克鲁兹·史密斯的惊险小说从这里雪下发现的三具尸体写起"),
    ORIG("ru-alexander-garden", "Alexander Garden, Moscow", "亚历山大花园，莫斯科",
         "The public garden laid out along the Kremlin wall after 1812. The first Fandorin novel opens here on a May afternoon in 1876",
         "1812 年之后沿克里姆林宫墙修建的公共花园。第一部凡多林小说就从 1876 年 5 月的一个下午在这里开场"),
    # ---- St Petersburg and the north-west ----
    PIL("ru-peter-paul-fortress", "Peter and Paul Fortress, St Petersburg", "彼得保罗要塞，圣彼得堡",
        "The fortress from which the city began was for two centuries its political prison. Chernyshevsky wrote What Is to Be Done? in a cell of the Alekseyevsky Ravelin between December 1862 and April 1863; Dostoevsky had been held here in 1849",
        "圣彼得堡从这座要塞起步，此后两百年它一直是关押政治犯的监狱。车尔尼雪夫斯基 1862 年 12 月到 1863 年 4 月在阿列克谢三角堡的囚室里写出了《怎么办？》；1849 年陀思妥耶夫斯基也被关在这里",
        ["what-is-to-be-done"]),
    ORIG("ru-muruzi", "Muruzi House, St Petersburg", "穆鲁济大楼，圣彼得堡",
         "The Moorish-style apartment block at Liteyny 24. Joseph Brodsky lived with his parents in a communal flat here from 1955 until he was forced to leave the country in 1972. A museum named after his essay has opened in the flat",
         "铸造厂大街 24 号的摩尔风格公寓楼。约瑟夫·布罗茨基 1955 年起同父母住在这里的一套合住公寓里，直到 1972 年被迫离开苏联。以他那篇随笔命名的博物馆已在这套公寓里开放"),
    PIL("ru-nabokov-house", "Nabokov House, St Petersburg", "纳博科夫故居，圣彼得堡",
        "Vladimir Nabokov was born in 1899 in this house at Bolshaya Morskaya 47 and lived in it until the family fled in 1917. Speak, Memory describes it room by room. The ground floor is a museum",
        "弗拉基米尔·纳博科夫 1899 年生于大海军街 47 号的这幢房子，一直住到 1917 年全家出走。《说吧，记忆》逐间屋子地写过它。底层今为博物馆",
        ["speak-memory"]),
    PIL("ru-komarovo", "Akhmatova's Grave, Komarovo", "阿赫玛托娃墓，科马罗沃",
        "Akhmatova spent her last summers in a small dacha at Komarovo on the Gulf of Finland, which she called her 'booth', and was buried in the village cemetery in March 1966",
        "阿赫玛托娃晚年的夏天都在芬兰湾边科马罗沃的一幢小别墅里度过，她管它叫“小岗亭”。1966 年 3 月，她葬在村里的墓地",
        ["requiem-akhmatova", "poem-without-a-hero"]),
    PIL("ru-piskaryovskoye", "Piskaryovskoye Memorial Cemetery, St Petersburg", "皮斯卡廖夫公墓，圣彼得堡",
        "The largest burial ground of the siege of Leningrad: about half a million people, most of them civilians dead of hunger, lie in its mass graves. Lines by the siege poet Olga Berggolts are cut into the memorial wall",
        "列宁格勒围困时期最大的墓地：约五十万人葬在这里的合葬墓中，大多是饿死的平民。纪念墙上刻着围困时期的诗人奥尔加·别尔戈利茨的诗句",
        ["blockade-book"]),
    ORIG("ru-vyshny-volochyok", "Vyshny Volochyok", "上沃洛乔克",
         "The town of canals and locks on the watershed between the Volga and the Baltic, where Peter the Great's waterway carried grain to St Petersburg. It is one of the post stations that give Radishchev's Journey its chapters",
         "伏尔加河与波罗的海分水岭上的运河与船闸之城，彼得大帝开凿的水道从这里把粮食运往圣彼得堡。它是拉季舍夫《旅行记》各章所用的驿站之一"),
    PIL("ru-shalamov", "Shalamov House, Vologda", "沙拉莫夫故居，沃洛格达",
        "Varlam Shalamov was born in 1907 in this clergy house beside St Sophia's Cathedral, where his father was a priest. His memoir The Fourth Vologda is about the house; the Kolyma Tales came out of his years in the camps of Kolyma",
        "瓦尔拉姆·沙拉莫夫 1907 年生于圣索菲亚大教堂旁的这幢神职人员住宅，他的父亲是那里的神父。他的回忆录《第四个沃洛格达》写的就是这个家；《科雷马故事》则出自他在科雷马劳改营里的岁月",
        ["kolyma-tales"]),
    PIL("ru-yaroslavl-monastery", "Monastery of the Transfiguration, Yaroslavl", "主显圣容修道院，雅罗斯拉夫尔",
        "The only manuscript of The Tale of Igor's Campaign is said to have come from this monastery, acquired by the collector Count Musin-Pushkin in the 1790s. He published it in 1800; the manuscript burned in Moscow in 1812. A museum of the poem is in the monastery",
        "据说《伊戈尔远征记》唯一的抄本出自这座修道院，1790 年代被收藏家穆辛-普希金伯爵得到。他在 1800 年把它刊印出来；1812 年抄本毁于莫斯科大火。修道院里设有这部史诗的博物馆",
        ["tale-of-igors-campaign"]),
    PIL("ru-tyorkin", "Tvardovsky and Tyorkin Monument, Smolensk", "特瓦尔多夫斯基与焦尔金纪念像，斯摩棱斯克",
        "Tvardovsky was a son of the Smolensk countryside, and he made his soldier hero Vasily Tyorkin a Smolensk man too. The bronze of 1995 in the city centre shows the poet and his hero sitting and talking, Tyorkin with his accordion",
        "特瓦尔多夫斯基是斯摩棱斯克乡下人，他把笔下的士兵英雄瓦西里·焦尔金也写成了斯摩棱斯克人。市中心 1995 年落成的铜像上，诗人和他的主人公坐着交谈，焦尔金手里拿着手风琴",
        ["vasily-tyorkin"]),
    # ---- central Russia ----
    ORIG("ru-kulikovo", "Kulikovo Field", "库利科沃原野",
         "The field between the Don and the Nepryadva where, on 8 September 1380, Dmitry of Moscow defeated the army of Mamai. Blok's cycle of 1908 speaks from the night before the battle",
         "顿河与涅普里亚德瓦河之间的原野。1380 年 9 月 8 日，莫斯科的德米特里在这里打败了马麦的军队。勃洛克 1908 年的组诗写的是大战前夜"),
    ORIG("ru-yelets", "Bunin Museum, Yelets", "蒲宁博物馆，叶列茨",
         "Bunin went to the gymnasium at Yelets from 1881 to 1886 and boarded with townspeople; the museum is in one of the houses where he lodged. The schoolboy chapters of The Life of Arseniev are set in the town",
         "蒲宁 1881 年到 1886 年在叶列茨上中学，寄住在市民家里；博物馆就设在他寄住过的一幢房子里。《阿尔谢尼耶夫的一生》里写中学时代的几章发生在这座城"),
    PIL("ru-konstantinovo", "Konstantinovo", "康斯坦丁诺沃",
        "Yesenin's native village on the high bank of the Oka. The landowner's house belonged to Lidia Kashina, the model for the heroine of Anna Snegina, and now holds a museum of the poem",
        "叶赛宁的故乡，在奥卡河的高岸上。村里的地主宅子当年属于莉季娅·卡申娜，她是《安娜·斯涅金娜》女主人公的原型；宅子今为这首长诗的博物馆",
        ["anna-snegina"]),
    ORIG("ru-voronezh-mandelstam", "Mandelstam Monument, Voronezh", "曼德尔施塔姆纪念像，沃罗涅日",
         "Mandelstam lived in exile in Voronezh from 1934 to 1937, and the poems of the Voronezh Notebooks were written here. The monument of 2008 stands at the entrance to a park, close to one of the houses where he rented a room",
         "曼德尔施塔姆 1934 年到 1937 年流放沃罗涅日，《沃罗涅日笔记本》里的诗都写于此。2008 年落成的纪念像立在公园入口处，离他租住过的一幢房子很近"),
    ORIG("ru-solotcha", "Solotcha", "索洛恰",
         "A village among pine woods at the edge of the Meshchora lowland, north of Ryazan. Paustovsky came here year after year from the 1930s and stayed in the house of the engraver Pozhalostin; The Meshchora Side is his book of the country round it",
         "梁赞以北、梅晓拉低地边缘松林里的村子。帕乌斯托夫斯基从 1930 年代起年年来这里，住在版画家波扎洛斯京的房子里；《梅晓拉地区》写的就是这一带"),
    PROTO("ru-miltsevo", "Miltsevo ('Talnovo')", "米利采沃（“塔利诺沃”）",
          "The village in the Vladimir region where Solzhenitsyn, back from exile, lodged in 1956 with Matryona Zakharova while he taught mathematics at the nearby school. In the story it is called Talnovo",
          "弗拉基米尔州的村子。1956 年，刚结束流放的索尔仁尼琴在附近的学校教数学，借住在玛特辽娜·扎哈罗娃家里。小说里这个村子叫塔利诺沃"),
    # ---- Volga south, Siberia, the Far East ----
    ORIG("ru-mamayev-kurgan", "Mamayev Kurgan, Volgograd", "马马耶夫岗，伏尔加格勒",
         "The height above the Volga that both armies fought over for months in the battle of Stalingrad. Viktor Nekrasov fought here as a sapper officer and set his novel on its slopes",
         "伏尔加河边的高地，斯大林格勒战役中双方为它争夺了好几个月。维克托·涅克拉索夫当年是工兵军官，就在这里作战，他的小说也写在这片山坡上"),
    PIL("ru-yelabuga", "Yelabuga", "叶拉布加",
        "Evacuated from Moscow in August 1941, Tsvetaeva came with her son to this small town on the Kama and died here on 31 August. She is buried in the town cemetery; the exact place of the grave is not known",
        "1941 年 8 月，茨维塔耶娃带着儿子从莫斯科疏散到卡马河畔的这座小城，8 月 31 日在这里去世。她葬在城里的公墓，确切的墓址已不可考",
        ["poems-about-moscow"]),
    PIL("ru-srostki", "Srostki", "斯罗斯特基",
        "Vasily Shukshin's native village on the Katun in the Altai. The people of his stories are its people. Readings in his memory are held every July on Mount Piket above the village",
        "瓦西里·舒克申的故乡，在阿尔泰的卡通河畔。他短篇小说里的人物就是这个村子里的人。每年 7 月，村旁的皮克特山上都举行纪念他的朗读会",
        ["village-folk"]),
    ORIG("ru-ovsyanka", "Ovsyanka", "奥夫相卡",
         "Viktor Astafyev's native village on the Yenisei above Krasnoyarsk. The Last Bow is the book of his childhood here with his grandmother; he came back to live in the village in 1980",
         "维克托·阿斯塔菲耶夫的故乡，在克拉斯诺亚尔斯克上游的叶尼塞河畔。《最后的问候》写的是他跟着外祖母在这里度过的童年；1980 年他回到村里定居"),
    PIL("ru-arsenyev", "Arsenyev Museum, Vladivostok", "阿尔谢尼耶夫博物馆，符拉迪沃斯托克",
        "The museum of the Far East that bears the name of the explorer Vladimir Arsenyev, who spent his last years in Vladivostok and died there in 1930. His books follow his expeditions through the Ussuri taiga with the Nanai hunter Dersu Uzala as guide",
        "以探险家弗拉基米尔·阿尔谢尼耶夫命名的远东博物馆。他晚年住在符拉迪沃斯托克，1930 年在那里去世。他的书写的是由那乃族猎人德尔苏·乌扎拉做向导、穿越乌苏里原始森林的几次考察",
        ["dersu-uzala"]),
    PIL("ru-vladivostok-mandelstam", "Mandelstam Monument, Vladivostok", "曼德尔施塔姆纪念像，符拉迪沃斯托克",
        "Arrested again in 1938, Mandelstam died on 27 December of that year in a transit camp on the edge of Vladivostok, on the way to Kolyma. The monument to him is the work of the local sculptor Valery Nenazhivin",
        "1938 年再次被捕的曼德尔施塔姆，在押往科雷马途中，于当年 12 月 27 日死在符拉迪沃斯托克城边的转运营里。这座纪念像出自当地雕塑家瓦列里·涅纳日温之手",
        ["voronezh-notebooks"]),
    ORIG("ru-petropavlovsk", "Petropavlovsk-Kamchatsky", "堪察加彼得罗巴甫洛夫斯克",
         "The port on Avacha Bay, with volcanoes behind it and no road to the rest of Russia. Julia Phillips's novel begins on its shore",
         "阿瓦恰湾边的港口城市，背后是火山，没有公路通往俄罗斯其他地方。朱莉娅·菲利普斯的小说从它的海岸边写起"),
]

# ============================== lines ==============================
RW, FW = "Russian", "French"
FLOWED = " (hard-wrapped lines joined, doubled spaces written as one)"
lines = [
    Q("cd-1", "captains-daughter", "ru-orenburg", "Chapter 10, 'The Siege of the Town'", "第十章《围城》", RW, T_KD,
      raw(T_KD, "Приближаясь к Оренбургу", "чинили городскую стену."), ["Оренбургу"],
      "As we approached Orenburg we saw a crowd of convicts with shaven heads and faces disfigured by the executioner's tongs. They were working at the fortifications under the eye of the garrison invalids. Some were carting away the rubbish that filled the ditch, others were digging with spades; on the rampart masons were carrying bricks and mending the town wall.",
      ["Orenburg"],
      "快到奥伦堡的时候，我们看见一群剃了头的囚犯，脸被刽子手的铁钳弄得不成样子。他们在驻防老兵的监督下修筑工事：有的用小车运走填满壕沟的垃圾，有的用铁锹挖土；土墙上，泥瓦匠搬着砖，修补城墙。",
      ["奥伦堡"]),
    Q("qs-1", "queen-of-spades", "ru-queen-of-spades-house", "Chapter 2", "第二章", RW, T_PD,
      raw(T_PD, "Рассуждая таким образом", "Германн затрепетал."), ["домом старинной архитектуры"],
      "Reasoning thus, he found himself in one of the main streets of Petersburg, in front of a house of old-fashioned architecture. The street was crowded with carriages; one after another they rolled up to the lighted entrance. From the carriages there stretched out now the shapely foot of a young beauty, now a jingling jackboot, now a striped stocking and a diplomatic shoe. Fur coats and cloaks flashed past the stately doorman. Hermann stopped.\n'Whose house is this?' he asked the watchman at the corner.\n'The Countess ***'s,' answered the watchman.\nHermann shuddered.",
      ["a house of old-fashioned architecture"],
      "他这样盘算着，不觉来到彼得堡的一条大街上，站在一幢老式建筑的房子前面。街上停满了马车，轿式马车一辆接一辆驶向灯火通明的大门。从车里不时伸出来的，一会儿是年轻美人匀称的脚，一会儿是叮当作响的长筒马靴，一会儿是条纹长袜和外交官的皮鞋。皮大衣和斗篷从威严的看门人身边一闪而过。赫尔曼站住了。\n“这是谁家的房子？”他问街角的岗警。\n“***伯爵夫人的。”岗警回答。\n赫尔曼打了个寒战。",
      ["老式建筑的房子"]),
    Q("bg-1", "boris-godunov", "ru-novodevichy", "Scene 'Maiden's Field. Novodevichy Convent'", "《处女原野·新圣女修道院》一场", RW, T_BG,
      raw(T_BG, "ДЕВИЧЬЕ ПОЛЕ\nНОВОДЕВИЧИЙ МОНАСТЫРЬ", "НОВОДЕВИЧИЙ МОНАСТЫРЬ") + GAP + raw(T_BG, "Один\nНельзя ли нам пробраться за ограду?", "Унизаны народом."),
      ["НОВОДЕВИЧИЙ МОНАСТЫРЬ"],
      "MAIDEN'S FIELD\nNOVODEVICHY CONVENT\n…\nONE\nCan't we get through, inside the wall?\nANOTHER\nNo chance. Even the field is packed,\nnever mind in there. No wonder: all Moscow\nhas crowded here; look: the wall, the roofs,\nevery tier of the cathedral belfry,\nthe domes of the churches, the very crosses\nare strung with people.",
      ["NOVODEVICHY CONVENT"],
      "处女原野\n新圣女修道院\n…\n一人\n咱们能不能挤到围墙里面去？\n另一人\n不行。哪儿挤得进！连原野上都挤满了，\n更别说里面。也难怪：整个莫斯科\n都挤到这儿来了；你看：围墙、屋顶、\n教堂钟楼的每一层、\n各座教堂的圆顶，连十字架上\n都爬满了人。",
      ["新圣女修道院"], note=" (the page prints this scene after the play, among the scenes left out of the final text; a gap marked …)"),
    Q("ts-1", "reminiscences-tsarskoye", "ru-lyceum", "Stanza 2", "第二节", RW, T_VC,
      raw(T_VC, "Не здесь ли мирны дни вели земные боги?", "На лоне мира и отрад?"), ["Царскосельский сад"],
      "Was it not here the gods of earth spent days of peace?\nIs this not the temple of the Russian Minerva?\nIs this not the Elysium of the North,\nthe lovely garden of Tsarskoye Selo,\nwhere, having slain the lion, Russia's mighty eagle\nrested in the lap of peace and joy?",
      ["garden of Tsarskoye Selo"],
      "尘世的众神不就是在这里安度太平岁月？\n这不就是俄罗斯弥涅耳瓦的神殿？\n这不就是北国的乐土，\n美丽的皇村花园——\n俄罗斯的雄鹰击败了狮子，\n在这里安卧于和平与欢乐的怀抱？",
      ["皇村花园"]),
    Q("bor-1", "borodino-lermontov", "ru-borodino", "Opening stanza", "第一节", RW, T_BO,
      raw(T_BO, "«Скажи-ка, дядя, ведь недаром", "Про день Бородина!»"), ["Бородина"],
      "'Tell me, uncle, it was not for nothing\nthat Moscow, burned by fire,\nwas given up to the French?\nThere were battles, after all,\nand what battles, they say!\nNot for nothing does all Russia remember\nthe day of Borodino!'",
      ["Borodino"],
      "“大叔，你说说，莫斯科烧成一片火海，\n交到法国人手里，\n总不是平白无故吧？\n不是打过好些仗吗，\n听说还打得真凶！\n难怪整个俄罗斯都记得\n波罗金诺那一天！”",
      ["波罗金诺"]),
    Q("np-1", "nevsky-prospekt", "ru-anichkov-bridge", "Opening", "开头", RW, T_NP,
      raw(T_NP, "Нет ничего лучше Невского проспекта", "красавица нашей столицы!"), ["Невского проспекта"],
      "There is nothing finer than Nevsky Prospekt, at least in Petersburg; for the city it is everything. What does this street not shine with, the beauty of our capital!",
      ["Nevsky Prospekt"],
      "再没有比涅瓦大街更好的了，至少在彼得堡是这样；对彼得堡来说，它就是一切。这条街——我们首都的美人——有什么不光彩夺目呢！",
      ["涅瓦大街"]),
    Q("mu-1", "mumu", "ru-mumu-house", "Opening", "开头", RW, T_MU,
      raw(T_MU, "В одной из отдаленных улиц Москвы", "скучающей старости."), ["в сером доме с белыми колоннами"],
      "In one of the outlying streets of Moscow, in a grey house with white columns, a mezzanine and a balcony gone crooked, there once lived a lady, a widow, surrounded by a large household of serfs. Her sons were in the service in Petersburg, her daughters were married; she seldom went out and was living through the last years of her miserly and bored old age in solitude.",
      ["a grey house with white columns"],
      "在莫斯科一条偏僻的街上，有一幢灰色的房子，带着白色圆柱、阁楼和歪斜的阳台，从前住着一位太太，是个寡妇，身边围着一大群家奴。她的儿子们在彼得堡做官，女儿们都出嫁了；她很少出门，孤零零地打发着她那吝啬而无聊的晚年。",
      ["灰色的房子"]),
    Q("md-1", "house-of-the-dead", "ru-omsk-fortress", "Part 1, chapter 1, 'The House of the Dead'", "第一部第一章《死屋》", RW, T_MD,
      raw(T_MD, "Острог наш стоял", "вольного неба."), ["на краю крепости"],
      "Our prison stood at the edge of the fortress, right by the fortress rampart. Sometimes you would look through the chinks in the fence at God's world, hoping to see something, and all you would see was a strip of sky and the high earthen rampart overgrown with weeds, and the sentries pacing up and down it day and night; and then you would think that whole years would pass and you would come up in just the same way to look through the chinks in the fence and see the same rampart, the same sentries and the same small strip of sky, not the sky above the prison but another, far-off, free sky.",
      ["the edge of the fortress"],
      "我们的监狱在要塞的边上，紧挨着要塞的土墙。有时从木栅的缝隙里向外面的世界张望，想看看能不能看到点什么——可是看到的只有一小片天空和长满杂草的高高的土墙，哨兵日夜在墙上走来走去；这时你就会想，整整多少年过去之后，你还是会这样走过来，从木栅的缝隙里向外看，看到的还是那道土墙，那些哨兵，那一小片天空——不是监狱上面的天空，而是另一片遥远的、自由的天空。",
      ["要塞的边上"]),
    Q("lf-1", "lefty", "ru-tula-lefty", "Chapter 4", "第四章", RW, T_LE,
      raw(T_LE, "А когда будешь ехать через Тулу", "что-нибудь сделают."), ["через Тулу"],
      "And when you pass through Tula, show my Tula craftsmen this nymphosoria and let them think it over. Tell them from me that my brother marvelled at this thing and praised above all the foreigners who made the nymphosoria, but that I put my trust in my own people, that they are no worse than anyone. They will not let my word fall to the ground, and they will do something.",
      ["through Tula"],
      "你路过图拉的时候，把这个“宁佛索利亚”给我的图拉师傅们看看，让他们琢磨琢磨。你替我告诉他们：我哥哥对这玩意儿赞叹不已，把造出它的外国人夸得比谁都高，可我信得过自己人，他们不比任何人差。他们不会把我的话当耳旁风，总会做出点什么来。",
      ["图拉"]),
    Q("sa-1", "sakhalin-island", "ru-aleksandrovsk", "Chapter 2", "第二章", RW, T_SA,
      raw(T_SA, "Переночевавши в де-Кастри", "на всем пути."), ["Александровский пост"],
      "Having spent the night at De-Kastri, the next day, 10 July, at noon we set off across the Tatar Strait for the mouth of the Duika, where the Alexandrovsk post lies. This time too the weather was calm and clear, such as is very rare here. Over the perfectly smooth sea whales swam in pairs, sending up fountains, and this fine, unusual sight entertained us the whole way.",
      ["Alexandrovsk post"],
      "在德卡斯特里过了一夜，第二天，7 月 10 日，中午我们横渡鞑靼海峡，驶向杜伊卡河口，亚历山德罗夫斯克哨所就在那里。这一次天气也是风平浪静、晴朗明亮，在这里很少见。平滑如镜的海面上，鲸鱼成双成对地游着，喷出水柱，这美妙而奇特的景象让我们一路上都不觉得闷。",
      ["亚历山德罗夫斯克哨所"]),
    Q("ku-1", "on-the-field-of-kulikovo", "ru-kulikovo", "Poem 3", "第三首", RW, T_KU,
      raw(T_KU, "Орлий клёкот над татарским станом", "Не спугнув коня."), ["Непрядва"],
      "An eagle's scream above the Tatar camp\nthreatened disaster,\nand the Nepryadva dressed herself in mist\nas a princess in a veil.\nAnd with the mist over the sleeping Nepryadva,\nstraight towards me\nYou came down, in a robe streaming light,\nnot startling the horse.",
      ["Nepryadva"],
      "鹰的唳叫在鞑靼营地上空\n预示着灾祸，\n涅普里亚德瓦河披上了雾，\n像公主披上面纱。\n随着雾笼罩沉睡的涅普里亚德瓦河，\n你径直向我\n走下来，衣裳流泻着光，\n没有惊动战马。",
      ["涅普里亚德瓦河"]),
    Q("cm-1", "poems-about-moscow", "ru-tsvetaeva-house", "Poem 8", "第八首", RW, T_CM,
      raw(T_CM, "— Москва! — Какой огромный", "Мы все к тебе придём."), ["Москва"],
      "— Moscow! What a vast\nhouse for wayfarers!\nEveryone in Russia is homeless.\nWe shall all come to you.",
      ["Moscow"],
      "——莫斯科！多么巨大的\n一座收留旅人的房子！\n在罗斯，人人无家可归。\n我们都将来到你这里。",
      ["莫斯科"]),
    Q("ra-1", "journey-petersburg-moscow", "ru-vyshny-volochyok", "Chapter 'Vyshny Volochok'", "《上沃洛乔克》一章", RW, T_RA,
      raw(T_RA, "Никогда не проезжал я сего нового города", "для дальнейшего потомства."), ["здешних шлюзов"],
      "I have never passed through this new town without looking at its locks. The first man to whom it occurred to imitate nature in her bounties and to make a river by hand, so as to bring all the ends of a single region into closer communication, deserves a monument for the most distant posterity.",
      ["its locks"],
      "每次路过这座新城，我没有一次不去看看这里的船闸。头一个想到效法大自然的恩惠、用人工造出一条河来，好让一个地区的各个角落更便于往来的人，值得为后世子孙立一座纪念碑。",
      ["这里的船闸"]),
    Q("bag-1", "childhood-years-bagrov", "ru-ufa-aksakov", "Chapter 'Ufa'", "《乌法》一章", RW, T_AK,
      raw(T_AK, "Обратный путь наш в Уфу", "очень нам обрадовались."), ["в Уфу", "В Уфе"],
      "Our journey back to Ufa was quicker and calmer: the frosts were moderate, the little windows of our covered sledge did not fur over completely with snow, and the sledge did not overturn.\nIn Ufa all our friends were very glad to see us.",
      ["Ufa"],
      "我们回乌法的路走得又快又平稳：天气不算太冷，带篷雪橇的小窗没有完全被雪糊住，雪橇也没有翻。\n到了乌法，所有相熟的朋友见到我们都非常高兴。",
      ["乌法"]),
    Q("gi-1", "moscow-and-muscovites", "ru-khitrovka", "Chapter 'Khitrovka'", "《希特罗夫卡》一章", RW, T_GI,
      raw(T_GI, "Лондон мне всегда представлялся", "в шевелящуюся гнилую яму."), ["Хитров рынок"],
      "London always seemed to me the foggiest place in Europe, and the Khitrov market, without doubt, the foggiest place in Moscow.\nA large square in the centre of the capital, near the river Yauza, surrounded by peeling stone houses, lies in a hollow into which several lanes run down like streams into a marsh. It is always steaming. Especially towards evening. And when it is a little misty, or after rain, you look from above, from the top of a lane, and a newcomer is seized with dread: a cloud has settled! You go down the lane into a stirring, rotten pit.",
      ["Khitrov market"],
      "在我的想象里，伦敦一向是欧洲雾最大的地方，而希特罗夫市场无疑是莫斯科雾最大的地方。\n首都中心靠近亚乌扎河的一个大广场，四周是墙皮剥落的砖石房子，它躺在洼地里，几条小巷像溪水流进沼泽一样通到这里。它总是冒着雾气，傍晚尤其如此。稍微起点雾，或者刚下过雨，你从高处、从巷口往下看——初来的人会吓一跳：一团云落下来了！你顺着小巷走下去，走进一个蠕动着的烂泥坑。",
      ["希特罗夫市场"]),
    Q("tam-1", "hero-of-our-time", "ru-taman", "Pechorin's Journal, I: 'Taman'", "毕巧林日记之一《塔曼》", RW, T_TA,
      raw(T_TA, "Тамань — самый скверный городишко", "хотели утопить."), ["Тамань"],
      "Taman is the nastiest little town of all the seaside towns of Russia. I nearly died of hunger there, and on top of that they tried to drown me.",
      ["Taman"],
      "塔曼是俄国所有滨海城市中最糟糕的一个小城。我在那里差点儿饿死，而且还有人想把我淹死。",
      ["塔曼"]),
    Q("eo-sg1", "eugene-onegin", "ru-summer-garden", "Chapter 1, stanza III", "第一章第三节", RW, T_O1,
      raw(T_O1, "Monsieur l’Abbé, француз убогой,", "И в Летний сад гулять водил."), ["Летний сад"],
      "Monsieur l'Abbé, a threadbare Frenchman,\nso as not to wear the child out,\ntaught him everything in jest,\ndid not bore him with stern morals,\nscolded him lightly for his pranks\nand took him walking in the Summer Garden.",
      ["Summer Garden"],
      "Monsieur l'Abbé，一个穷酸的法国人，\n为了不让孩子太累，\n教他什么都像开玩笑，\n不拿严厉的道德说教烦他，\n淘气了也只是轻轻责备几句，\n还带他到夏花园去散步。",
      ["夏花园"]),
    Q("eo-pp1", "eugene-onegin", "ru-petrovsky-palace", "Chapter 7, stanza XXXVII", "第七章第三十七节", RW, T_O7,
      raw(T_O7, "Вот, окружен своей дубравой,", "Глядел на грозный пламень он."), ["Петровский замок"],
      "There, ringed by its own oak wood,\nstands Petrovsky Castle. Gloomily\nit prides itself on recent glory.\nIn vain Napoleon waited here,\ndrunk with his last good fortune,\nfor Moscow on her knees\nwith the keys of the old Kremlin:\nno, my Moscow did not go\nto him with bowed and guilty head.\nNo holiday, no welcoming gift:\nshe was preparing a fire\nfor the impatient hero.\nFrom here, sunk in thought,\nhe gazed upon the dreadful flame.",
      ["Petrovsky Castle"],
      "看，彼得罗夫宫被自己的橡树林环绕着。\n它阴沉地\n为不久前的荣耀而自豪。\n拿破仑陶醉于最后的幸运，\n在这里白白等待\n莫斯科屈膝跪下，\n献上古老克里姆林宫的钥匙：\n不，我的莫斯科没有\n低着认罪的头去见他。\n没有庆典，没有迎接的礼物，\n她给这位急不可耐的英雄\n准备的是一场大火。\n他就是从这里，陷入沉思，\n望着那可怕的火焰。",
      ["彼得罗夫宫"]),
    Q("cp-sn1", "crime-and-punishment", "ru-sennaya", "Part 6, chapter 8", "第六部第八章", RW, T_CP,
      flow(raw(T_CP, "Он вошел на Сенную.", "Он вошел на Сенную.")) + GAP + flow(raw(T_CP, "Он стал на колени среди площади", "другой\nраз.")), ["Сенную"],
      "He walked into the Haymarket.\n…\nHe knelt down in the middle of the square, bowed to the ground and kissed that filthy earth with delight and happiness. He got up and bowed a second time.",
      ["Haymarket"],
      "他走进了干草市场。\n…\n他在广场中央跪下，向大地一躬到底，怀着快乐和幸福吻了吻这肮脏的土地。他站起来，又鞠了一躬。",
      ["干草市场"], note=FLOWED + " (a gap marked …)"),
    Q("gd-1", "childhood-gorky", "ru-kashirin-house", "Chapter 1", "第一章", RW, T_GD,
      raw(T_GD, "Помню детскую радость бабушки при виде Нижнего.", "летят будто!"), ["Нижнего"],
      "I remember grandmother's childlike joy at the sight of Nizhny. Tugging me by the hand, she pushed me to the rail and cried:\n'Look, look how fine it is! There he is, our Nizhny, bless him! That's what he's like, God's own town! The churches, look at them, they seem to be flying!'",
      ["Nizhny"],
      "我记得外祖母看见下诺夫哥罗德时那孩子般的高兴。她拉着我的手，把我推到船舷边，喊道：\n“你看，你看，多好啊！这就是它，老天爷，下诺夫哥罗德！瞧它是什么样子，上帝的城！那些教堂，你瞧，就像在飞！”",
      ["下诺夫哥罗德"]),
    Q("wp-pk1", "war-and-peace", "ru-poklonnaya", "Volume 3, part 3, chapter 19", "第三卷第三部第十九章", RW, T_WP,
      raw(T_WP, "В это же время, в 10 часов утра 2-го сентября, Наполеон стоял", "открывшееся перед ним зрелище."), ["Поклонной горе"],
      "At that same time, at ten in the morning of 2 September, Napoleon was standing among his troops on Poklonnaya Hill and looking at the sight that lay open before him.",
      ["Poklonnaya Hill"],
      "就在这个时候，9 月 2 日上午十点，拿破仑站在自己的军队中间，在俯首山上望着展现在他面前的景象。",
      ["俯首山"]),
    Q("ms-1", "michael-strogoff", "ru-nizhny-fair", "Part 1, chapter 5", "第一部第五章", FW, T_MS,
      raw(T_MS, "Nijni-Novgorod, qui en temps ordinaire", "transportée à Nijni-Novgorod.", "fr"), ["Nijni-Novgorod"],
      "Nizhny Novgorod, which in ordinary times has no more than thirty to thirty-five thousand inhabitants, then held more than three hundred thousand; that is, its population had grown tenfold. This increase was due to the famous fair held within its walls for a period of three weeks. Formerly it was Makaryev that profited from this gathering of merchants, but since 1817 the fair has been moved to Nizhny Novgorod.",
      ["Nizhny Novgorod"],
      "下诺夫哥罗德平时只有三万到三万五千居民，这时却容纳了三十多万人，也就是说人口增加了十倍。这是因为那个著名的集市，它在城里举行，为期三周。从前坐享商贾云集之利的是马卡里耶夫，但自 1817 年起，集市迁到了下诺夫哥罗德。",
      ["下诺夫哥罗德"]),
    Q("ml-1", "in-the-forests", "ru-svetloyar", "Book 2, part 4, chapter 1", "第二卷第四部第一章", RW, T_ML,
      raw(T_ML, "Одно только помнит народ", "только очам праведников."), ["Светлого Яра"],
      "One thing only the people remember: that in olden times, on the hills by Svetly Yar, pagan rites were held on the day of Agrafena Kupalnitsa, and that on those hills there once stood the city of Kitezh… And to this day, they say, that city stands, but it is visible only to the eyes of the righteous.",
      ["Svetly Yar"],
      "人们只记得一件事：古时候，在斯韦特雷亚尔湖边的山丘上，每逢阿格拉费娜浴日都举行异教的祭礼，那些山丘上曾经矗立着基捷日城……据说这座城至今还在，只是唯有义人的眼睛才看得见。",
      ["斯韦特雷亚尔湖"]),
    # ---- scene notes ----
    S("bug-s1", "commandant-of-bugulma", "ru-bugulma", "'The Commandant of the Town of Bugulma'", "《布古利马城防司令》", 
      "In October 1918 the narrator is sent out from Simbirsk with a small escort of Chuvash soldiers and arrives to take over Bugulma as its commandant. He has hardly settled in when Comrade Yerokhimov rides in at the head of the Tver Revolutionary Regiment and declares himself commandant instead, and the two go on issuing orders against each other.",
      "1918 年 10 月，叙述者带着一小队楚瓦什士兵从辛比尔斯克出发，前来接管布古利马，当城防司令。他刚安顿下来，叶罗希莫夫同志就率领特维尔革命团骑马进城，宣布自己才是城防司令，两人从此你一道命令我一道命令地对着干。",
      ["Bugulma"], ["布古利马"], W + "Jaroslav_Hašek"),
    S("zh-s2", "doctor-zhivago", "ru-perm", "Part 9, 'Varykino'", "第九章《瓦雷金诺》",
      "From Varykino Zhivago rides into Yuriatin to read in the town library, and one day sees Lara at a table across the reading room. He takes her address from her order slips and finds her in the yard of the house opposite the 'house with figures', carrying water from the well.",
      "日瓦戈从瓦雷金诺骑马进尤里亚金城，到市图书馆看书，有一天隔着阅览室看见拉拉坐在一张桌子旁。他从她的借书单上抄下地址，在“有雕像的房子”对面那幢房子的院子里找到了她，她正从井边挑水回来。",
      ["Yuriatin", "house with figures"], ["尤里亚金", "有雕像的房子"], W + "Doctor_Zhivago_(novel)"),
    S("arz-s1", "life-of-arseniev", "ru-yelets", "Book 2", "第二卷",
      "Sent to the gymnasium in the district town, the boy Alyosha Arseniev is boarded with the tradesman Rostovtsev. What stays with him is the town itself: the walk to school through frosty streets, the evenings at his landlord's table, and the pride with which that plain, stern man speaks of Russia.",
      "少年阿廖沙·阿尔谢尼耶夫被送到县城上中学，寄住在小市民罗斯托夫采夫家里。留在他记忆里的是这座城本身：穿过结霜的街道去上学的路，房东饭桌旁的夜晚，还有这个朴素而严厉的人说起俄罗斯时的那份自豪。",
      ["the district town"], ["县城"], W + "The_Life_of_Arseniev"),
    S("vor-s1", "voronezh-notebooks", "ru-voronezh-mandelstam", "The three notebooks, 1935–1937", "三本笔记本，1935—1937",
      "Exiled to Voronezh after his first arrest, Mandelstam began to write again in the spring of 1935. The poems of the three notebooks take in the black earth of the fields around, the steep streets of the town and his own confinement in it. His wife Nadezhda kept them, on paper and by heart, through the decades when they could not be printed.",
      "第一次被捕后流放到沃罗涅日的曼德尔施塔姆，1935 年春天重新开始写诗。三本笔记本里的诗写到了四周田野的黑土，城里陡峭的街道，也写到他被困在这里的处境。在这些诗无法发表的几十年里，他的妻子娜杰日达靠纸和记忆把它们保存了下来。",
      ["Voronezh"], ["沃罗涅日"], W + "Osip_Mandelstam"),
    S("mes-s1", "meshchora-side", "ru-solotcha", "'An Ordinary Land'", "《平凡的土地》",
      "Paustovsky begins by admitting that the Meshchora country has no special beauties or riches, nothing but forests, meadows and clear air, and that it holds you all the same. Chapter by chapter he goes through its lakes and peat bogs, its old canals and forest rivers, and the ferrymen, basket-weavers and old men he met along them.",
      "帕乌斯托夫斯基开篇就承认，梅晓拉地区没有什么特别的美景和财富，只有森林、草地和清澈的空气，可它偏偏叫人放不下。他一章一章地写这里的湖泊和泥炭沼泽、旧运河和林间小河，还有一路上遇到的摆渡人、编筐人和老人们。",
      ["Meshchora"], ["梅晓拉"], RUW + "Паустовский,_Константин_Георгиевич"),
    S("matr-s1", "matryonas-place", "ru-miltsevo", "Whole story", "全篇",
      "In the summer of 1956 a teacher back from the camps asks to be sent to some quiet corner of Russia, and takes a bed in the old house of Matryona, a sick, unpaid, uncomplaining peasant woman who helps everyone. She is killed at the railway crossing, helping to haul away the timbers of her own annexe, and only then does he see that she was the righteous one without whom no village can stand.",
      "1956 年夏天，一位从劳改营回来的教师请求分配到俄罗斯某个安静的角落，在玛特辽娜的老屋里借了一张床。玛特辽娜是个多病、没有报酬、从不抱怨、谁家有事都去帮忙的农妇。她在铁路道口帮人拖运从自家偏屋拆下的木料时被火车撞死，直到这时他才明白，她就是那种义人，少了这样的人，一个村子就立不住。",
      ["some quiet corner of Russia"], ["俄罗斯某个安静的角落"], W + "Matryona's_Place"),
    S("lb-s1", "last-bow", "ru-ovsyanka", "'The Horse with the Pink Mane'", "《粉红色鬃毛的马》",
      "The boy is sent to the hillside to pick strawberries for his grandmother to sell in town. The neighbour's children dare him into eating them, and he pads the basket with grass under a layer of berries. His grandmother finds out when she takes the basket to town, comes home scolding, and still brings him the gingerbread horse with the pink mane that she had promised.",
      "外祖母打发男孩上山坡摘草莓，好拿到城里去卖。邻居家的孩子们激他把草莓吃掉了，他就在筐里塞满草，上面铺一层草莓。外祖母把筐带进城才发现上了当，回家把他数落了一通，可还是把答应过的那匹粉红色鬃毛的蜜糖饼小马带给了他。",
      ["the hillside"], ["山坡"], RUW + "Астафьев,_Виктор_Петрович"),
    S("rah-s1", "in-a-room-and-a-half", "ru-muruzi", "The essay", "全文",
      "Writing in English in America, after both his parents had died without being allowed to see him again, Brodsky rebuilds the space the three of them shared in a communal flat: the big room with its Moorish plaster ornament, and his own half-room, walled off with bookshelves and stacked suitcases.",
      "布罗茨基在美国用英文写作此文时，父母都已去世，生前始终未获准再见他一面。他在文中重建了一家三口在合住公寓里共用的那点空间：带着摩尔式石膏装饰的大房间，以及他自己用书架和摞起来的箱子隔出来的那半间。",
      ["a communal flat"], ["合住公寓"], RUW + "Полторы_комнаты"),
    S("fls-s1", "front-line-stalingrad", "ru-mamayev-kurgan", "Part 2", "第二部",
      "Lieutenant Kerzhentsev, a sapper, has retreated with the army across the steppe to the Volga in the summer of 1942, and in Stalingrad he is given a battalion on the slope of Mamayev Kurgan. For weeks the war is a few hundred metres of trench, mines laid at night, and one more attempt on the water tanks at the top of the hill.",
      "工兵中尉克尔任采夫在 1942 年夏天随部队穿过草原退到伏尔加河边，到斯大林格勒后受命带一个营守在马马耶夫岗的山坡上。一连几个星期，战争就是几百米长的战壕、夜里埋下的地雷，以及又一次向山顶水塔发起的冲击。",
      ["Mamayev Kurgan"], ["马马耶夫岗"], RUW + "В_окопах_Сталинграда"),
    S("hp-s1", "heart-of-parma", "ru-cherdyn", "Whole novel", "全书",
      "Prince Mikhail rules Perm the Great from the wooden fortress of Cherdyn. The Vogul prince Asyka comes raiding from beyond the Urals, and from the west Moscow sends first its bishops and then, in 1472, an army to take the land for the Grand Prince.",
      "米哈伊尔公在切尔登的木头城堡里统治着“大彼尔姆”。沃古尔人的王公阿瑟卡从乌拉尔山那边前来劫掠；西边的莫斯科先派来主教，1472 年又派来军队，要把这片土地收归大公。",
      ["Cherdyn"], ["切尔登"], RUW + "Сердце_пармы"),
    S("gp-s1", "gorky-park", "ru-gorky-park", "Part 1, 'Moscow'", "第一部《莫斯科》",
      "Chief Investigator Arkady Renko of the Moscow militia is called out to a clearing in the park, where the thaw has uncovered three bodies: shot, and with their faces and fingertips cut away. Everything about the case says it belongs to the KGB, and the KGB insists that he keep it.",
      "莫斯科民警局的首席侦查员阿尔卡季·伦科被叫到公园里的一片空地上，融雪露出了三具尸体：都是被枪杀的，脸和指尖都被割掉了。这桩案子处处显得该归克格勃管，克格勃却坚持让他办下去。",
      ["the park"], ["公园"], W + "Gorky_Park_(novel)"),
    S("wq-s1", "winter-queen", "ru-alexander-garden", "Chapter 1", "第一章",
      "On 13 May 1876, in front of the strollers in the Alexander Garden, a well-dressed student goes up to a young lady on a bench, puts a revolver to his head and pulls the trigger. The file comes to the desk of a twenty-year-old clerk of the Criminal Investigation Division, Erast Fandorin.",
      "1876 年 5 月 13 日，在亚历山大花园里，一个衣着体面的大学生当着散步人群的面，走到长椅上一位年轻小姐跟前，把左轮手枪顶在自己头上扣动了扳机。案卷送到了刑事侦缉处一个二十岁的文书埃拉斯特·凡多林的桌上。",
      ["Alexander Garden"], ["亚历山大花园"], W + "The_Winter_Queen_(novel)"),
    S("ca-s1", "children-of-the-arbat", "ru-arbat", "Part 1", "第一部",
      "Sasha Pankratov, a student and Komsomol member from a big house on the Arbat, is expelled from his institute over a trifle, arrested, and in 1934 exiled to Siberia. The novel moves between him, the schoolfriends who stay behind on the Arbat, and Stalin.",
      "萨沙·潘克拉托夫是住在阿尔巴特街一幢大楼里的大学生、共青团员。他因为一点小事被学院开除，接着被捕，1934 年流放西伯利亚。小说在他、留在阿尔巴特街的中学同学们和斯大林之间来回切换。",
      ["the Arbat"], ["阿尔巴特街"], W + "Children_of_the_Arbat"),
    S("de-s1", "disappearing-earth", "ru-petropavlovsk", "'August'", "《八月》",
      "On an August afternoon two sisters, Alyona and Sophia, eleven and eight, are alone on the rocky shore of the bay when a man asks them to help him to his car. Each chapter after that is another month, and another woman of Kamchatka living in the shadow of their disappearance.",
      "八月的一个下午，十一岁的阿廖娜和八岁的索菲娅姐妹俩独自在海湾的礁石岸边，一个男人请她们扶他走到车那里。此后每一章是一个月，写的是另一个生活在两姐妹失踪阴影下的堪察加女人。",
      ["the bay"], ["海湾"], W + "Disappearing_Earth"),
    S("mon-s1", "the-monastery-prilepin", "ru-solovki", "Book 1", "第一部",
      "Artyom Goryainov, a young Muscovite, is serving his sentence in the Solovki camp at the end of the 1920s, when its chief Eichmanis still speaks of the place as a laboratory for making new men. The novel follows him from one work detail to the next, and to the punishment cells on Sekirnaya Hill.",
      "年轻的莫斯科人阿尔乔姆·戈里亚伊诺夫 1920 年代末在索洛韦茨基劳改营服刑，当时的营长艾赫马尼斯还把这里说成一座改造新人的实验室。小说跟着他从一个劳动队换到另一个劳动队，最后到了谢基尔山上的禁闭室。",
      ["Solovki"], ["索洛韦茨基"], RUW + "Обитель_(роман)"),
    S("mm-s2", "master-and-margarita", "ru-bulgakov-house", "Chapter 7, 'The Evil Apartment'", "第七章《凶宅》",
      "Styopa Likhodeyev, director of the Variety Theatre, wakes with a hangover in flat no. 50 to find a stranger in black sitting by his bed, with a contract he cannot remember signing. A moment later he is standing on a jetty in Yalta, and Woland and his retinue have the flat.",
      "杂耍剧院经理斯乔帕·利霍杰耶夫宿醉醒来，发现 50 号公寓里他的床边坐着一个穿黑衣的陌生人，手里拿着一份他不记得自己签过的合同。转眼之间，他已经站在雅尔塔的防波堤上，公寓归了沃兰德一伙。",
      ["flat no. 50"], ["50 号公寓"], W + "The_Master_and_Margarita"),
    S("mm-s3", "master-and-margarita", "ru-pashkov-house", "Chapter 29", "第二十九章",
      "At sunset Woland and Azazello sit on the stone terrace of a building the novel calls one of the most beautiful in Moscow, looking out over the city. Matthew Levi comes to them there with the request that the Master be given peace.",
      "日落时分，沃兰德和阿扎泽洛坐在一幢楼的石砌平台上俯瞰全城，小说说这是莫斯科最美的建筑之一。利未·马太来到这里，转达请求：赐予大师安宁。",
      ["the stone terrace"], ["石砌平台"], W + "The_Master_and_Margarita"),
]

# ============================== checks, then append ==============================
old_books = {m for m in re.findall(r'\{ id: "([^"]+)"', open(b.data("books.js"), encoding="utf-8").read())}
old_places = {m for m in re.findall(r'\{ id: "([^"]+)"', open(b.data("places.js"), encoding="utf-8").read())}
old_lines = {m for m in re.findall(r'\{ id: "([^"]+)"', open(b.data("lines.js"), encoding="utf-8").read())}
new_b, new_p, new_l = {x["id"] for x in books}, {x["id"] for x in places}, {x["id"] for x in lines}
assert len(new_b) == len(books) and len(new_p) == len(places) and len(new_l) == len(lines)
assert not new_b & old_books, new_b & old_books
assert not new_p & old_places, new_p & old_places
assert not new_l & old_lines, new_l & old_lines
assert new_p == set(CO), new_p ^ set(CO)
bids, pids = new_b | old_books, new_p | old_places
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
    M = "11-23: fourth pack (tools/content/batches/add_ru4.py)"
    b.append(b.data("books.js"), books, M)
    b.append(b.data("places.js"), places, M)
    b.append(b.data("lines.js"), lines, M)
    print(len(books), "books,", len(places), "places,", len(lines), "lines (", sum(1 for l in lines if l.get("kind") != "scene"), "quotations )")
