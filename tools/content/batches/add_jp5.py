"""11-23: Japan, fifth pack: 25 more books and 32 more places, to bring the country in line with its weight
(Soseki, Ogai, Basho's road north, Takuboku and Kenji in Iwate, Toson's Kiso road, Shikoku, Kyushu, Hokkaido, Nagasaki).

Quotations (15 lines) are cut from Wikisource pages (tools/content/wikisource.py): Japanese Wikisource, French
Wikisource for Loti and English Wikisource for Isabella Bird; English and Chinese translations are our own drafts.
Books in copyright, and public-domain books whose text is not on Wikisource, have scene notes in our own words.
What a cut changes, named again in that line's `checked`: the full-width indent of a line is dropped.

Coordinates are those of the place's Japanese (sometimes English) Wikipedia article (cache/jp/coords.json).

Usage: python3 -I add_jp5.py <app_dir> <coords.json> <wikisource_root>"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b
import wikisource as ws

APP, CO, WSR = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8")), sys.argv[3]
DATE = "2026-11-23"
b.init(APP, "", "jp", DATE)
W = b.W
JAW = "https://ja.wikipedia.org/wiki/"
GAP = b.GAP

def BK(id, title, title_zh, title_orig, author, author_zh, author_orig, year, pd=True, **kw):
    d = dict(id=id, title=title, title_zh=title_zh, title_orig=title_orig, author=author, author_zh=author_zh, year=year,
             orig_lang=kw.pop("lang", "ja"), public_domain=pd, source_url=kw.pop("src", None), author_orig=author_orig)
    d.update(kw)
    return {k: v for k, v in d.items() if v is not None or k == "source_url"}

def C(pid):
    c = CO[pid]
    return c["lat"], c["lon"], c["st"], c["su"]

def ORIG(pid, name, zh, en_note, zh_note, **kw): return b.ORIG(pid, name, zh, *C(pid), en_note, zh_note, **kw)
def PROTO(pid, name, zh, en_note, zh_note, **kw): return b.PROTO(pid, name, zh, *C(pid), en_note, zh_note, **kw)
def PIL(pid, name, zh, en_note, zh_note, ids, **kw): return b.PIL(pid, name, zh, *C(pid), en_note, zh_note, ids, **kw)
S = b.S

def raw(title, start, end, lang="ja"):
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

JA = lambda t: ws.url("ja", t)
SOSEKI = ("Natsume Soseki", "夏目漱石", "夏目漱石")
JW, EW, FW = "Japanese", "English", "French"
IND = " (the indent of a line dropped)"
def ind(s):
    return re.sub(r"(?m)^　+", "", s)
T_OKU, T_BOT, T_SAN, T_KUS, T_TAK, T_ICH, T_YOA, T_KON, T_KOK, T_SUM, T_MAN = ("おくのほそ道", "坊つちやん", "三四郎", "草枕", "高瀬舟", "一握の砂",
    "夜明け前/第一部上", "金色夜叉", "こころ", "源氏物語/須磨", "万葉集 (鹿持雅澄訓訂)/巻第五")
T_BIRD, T_LOTI = "Unbeaten Tracks in Japan/LETTER VII", "Madame Chrysanthème, 1899/02"

books = [
    BK("botchan", "Botchan", "哥儿", "坊っちゃん", *SOSEKI, "1906", src=JA(T_BOT), aliases=["Botchan", "少爷", "Matsuyama", "Dogo Onsen", "道後温泉"]),
    BK("sanshiro", "Sanshiro", "三四郎", "三四郎", *SOSEKI, "1908", src=JA(T_SAN), aliases=["Sanshirō", "Mineko", "stray sheep", "三四郎池"]),
    BK("kusamakura", "Kusamakura (The Three-Cornered World)", "草枕", "草枕", *SOSEKI, "1906", src=JA(T_KUS), aliases=["The Three-Cornered World", "Grass Pillow", "那古井", "Nakoi"]),
    BK("takasebune", "The Boat on the Takase River", "高濑舟", "高瀬舟", "Mori Ogai", "森鸥外", "森鷗外", "1916", src=JA(T_TAK), aliases=["Takasebune", "Mori Ōgai", "喜助", "Kisuke"]),
    BK("kappa-akutagawa", "Kappa", "河童", "河童", "Ryunosuke Akutagawa", "芥川龙之介", "芥川龍之介", "1927", aliases=["Kamikochi", "上高地", "Akutagawa"]),
    BK("night-on-the-galactic-railroad", "Night on the Galactic Railroad", "银河铁道之夜", "銀河鉄道の夜", "Kenji Miyazawa", "宫泽贤治", "宮沢賢治", "1934",
       aliases=["Milky Way Railroad", "Giovanni", "Campanella", "雨ニモマケズ", "Ame ni mo makezu", "宮澤賢治"]),
    BK("a-handful-of-sand", "A Handful of Sand", "一握砂", "一握の砂", "Ishikawa Takuboku", "石川啄木", "石川啄木", "1910", src=JA(T_ICH), aliases=["Ichiaku no suna", "Takuboku", "tanka", "渋民"]),
    BK("at-kinosaki", "At Kinosaki", "在城崎", "城の崎にて", "Naoya Shiga", "志贺直哉", "志賀直哉", "1917", pd=False, aliases=["Kinosaki ni te", "Shiga Naoya", "城崎にて"]),
    BK("the-old-capital", "The Old Capital", "古都", "古都", "Yasunari Kawabata", "川端康成", "川端康成", "1962", pd=False, aliases=["Koto", "Chieko", "Naeko", "千重子"]),
    BK("sound-of-waves", "The Sound of Waves", "潮骚", "潮騒", "Yukio Mishima", "三岛由纪夫", "三島由紀夫", "1954", pd=False, aliases=["Shiosai", "Utajima", "歌島", "Shinji", "Hatsue"]),
    BK("tsugaru", "Tsugaru", "津轻", "津軽", "Osamu Dazai", "太宰治", "太宰治", "1944", aliases=["Return to Tsugaru", "たけ", "Take", "小泊"]),
    BK("roof-tile-of-tempyo", "The Roof Tile of Tempyo", "天平之甍", "天平の甍", "Yasushi Inoue", "井上靖", "井上靖", "1957", pd=False, aliases=["Tempyō no iraka", "Ganjin", "鉴真", "鑑真", "Jianzhen"]),
    BK("ryoma-ga-yuku", "Ryoma Goes His Way", "龙马奔走", "竜馬がゆく", "Ryotaro Shiba", "司马辽太郎", "司馬遼太郎", "1963–1966", pd=False, aliases=["Ryoma ga Yuku", "Sakamoto Ryoma", "坂本龍馬", "坂本龙马", "龙马来了"]),
    BK("points-and-lines", "Points and Lines", "点与线", "点と線", "Seicho Matsumoto", "松本清张", "松本清張", "1958", pd=False, aliases=["Ten to Sen", "Tokyo Express", "香椎", "Kashii"]),
    BK("kafka-on-the-shore", "Kafka on the Shore", "海边的卡夫卡", "海辺のカフカ", "Haruki Murakami", "村上春树", "村上春樹", "2002", pd=False, aliases=["Umibe no Kafuka", "Kafka Tamura", "Nakata", "高松"]),
    BK("glimpses-of-unfamiliar-japan", "Glimpses of Unfamiliar Japan", "陌生日本的一瞥", None, "Lafcadio Hearn", "小泉八云", "Lafcadio Hearn", "1894", lang="en",
       aliases=["Lafcadio Hearn", "Koizumi Yakumo", "小泉八雲", "Kwaidan", "怪谈", "In a Japanese Garden"]),
    BK("ainu-shinyoshu", "Ainu Shin'yoshu (Songs of the Ainu Gods)", "阿伊努神谣集", "アイヌ神謡集", "Chiri Yukie", "知里幸惠", "知里幸恵", "1923",
       aliases=["Ainu Shinyoshu", "Chiri Yukie", "The Song the Owl God Sang", "銀の滴降る降るまわりに", "yukar"]),
    BK("freezing-point", "Freezing Point", "冰点", "氷点", "Ayako Miura", "三浦绫子", "三浦綾子", "1965", pd=False, aliases=["Hyōten", "Hyoten", "Yoko", "陽子", "旭川"]),
    BK("bells-of-nagasaki", "The Bells of Nagasaki", "长崎的钟", "長崎の鐘", "Takashi Nagai", "永井隆", "永井隆", "1949", aliases=["Nagasaki no kane", "Nagai Takashi", "Urakami", "浦上"]),
    BK("a-pale-view-of-hills", "A Pale View of Hills", "远山淡影", None, "Kazuo Ishiguro", "石黑一雄", "Kazuo Ishiguro", "1982", pd=False, lang="en", aliases=["Ishiguro", "Etsuko", "Inasa", "稲佐"]),
    BK("floating-clouds", "Floating Clouds", "浮云", "浮雲", "Fumiko Hayashi", "林芙美子", "林芙美子", "1951", aliases=["Ukigumo", "Hayashi Fumiko", "Yukiko", "屋久島"]),
    BK("before-the-dawn", "Before the Dawn", "黎明之前", "夜明け前", "Shimazaki Toson", "岛崎藤村", "島崎藤村", "1929–1935", src=JA("夜明け前"), aliases=["Yoake mae", "Aoyama Hanzo", "青山半蔵", "馬籠", "Magome", "Kiso Road"]),
    BK("konjiki-yasha", "The Golden Demon", "金色夜叉", "金色夜叉", "Ozaki Koyo", "尾崎红叶", "尾崎紅葉", "1897–1902", src=JA(T_KON), aliases=["Konjiki Yasha", "Kan'ichi", "Omiya", "貫一", "お宮", "熱海"]),
    BK("madame-chrysantheme", "Madame Chrysanthème", "菊子夫人", "Madame Chrysanthème", "Pierre Loti", "皮埃尔·洛蒂", "Pierre Loti", "1887", lang="fr", src=ws.url("fr", "Madame Chrysanthème, 1899"),
       aliases=["Madame Chrysantheme", "Loti", "Madame Butterfly", "蝴蝶夫人"]),
    BK("unbeaten-tracks-in-japan", "Unbeaten Tracks in Japan", "日本奥地纪行", None, "Isabella Bird", "伊莎贝拉·伯德", "Isabella Bird", "1880", lang="en", src=ws.url("en", "Unbeaten Tracks in Japan"),
       aliases=["Isabella Bird", "日本奥地紀行", "Nikko", "Ezo"]),
]

places = [
    ORIG("jp-dogo", "Dogo Onsen Honkan, Matsuyama", "道后温泉本馆，松山",
         "Soseki taught English at the middle school in Matsuyama in 1895 and 1896 and went almost daily to this bathhouse, then just rebuilt. In Botchan the spa town is called 'Sumita', and the hero's trips to the baths and the dumpling shop are reported on the blackboard by his pupils. A room on the third floor is kept as the 'Botchan room'",
         "漱石 1895 年到 1896 年在松山的中学教英语，几乎天天来这座当时刚重建的浴场。《哥儿》里这个温泉町叫“住田”，主人公去泡温泉、吃团子的事，第二天就被学生写在了黑板上。三楼有一间“哥儿之间”"),
    ORIG("jp-sanshiro-pond", "Sanshiro Pond, University of Tokyo", "三四郎池，东京大学",
         "The pond in the old garden of the Kaga lords, in the middle of the Hongo campus. Sanshiro, newly arrived from Kyushu, squats beside it and first sees Mineko on the bank above. The pond has been called after the novel ever since",
         "本乡校区中央、旧加贺藩主庭园里的池子。刚从九州来的三四郎蹲在池边，第一次看见站在对面高处的美祢子。从那以后，这个池子就以小说的名字相称"),
    PROTO("jp-oama", "Oama Onsen (Tensui), Kumamoto", "小天温泉（天水），熊本",
          "At the turn of 1897 to 1898 Soseki, then a teacher in Kumamoto, walked over the hills to the hot spring of Oama and stayed at the villa of the Maeda family. It became the inn at 'Nakoi' where the painter of Kusamakura lodges, and the daughter of the house the model for Nami",
          "1897 年底到 1898 年初，在熊本教书的漱石翻过山丘来到小天温泉，住在前田家的别邸。这里成了《草枕》里画家投宿的“那古井”温泉旅馆，前田家的女儿则是那美的原型"),
    ORIG("jp-takase", "Takase River (Ichi-no-Funairi), Kyoto", "高濑川（一之船入），京都",
         "The canal dug by the merchant Suminokura Ryoi in the early seventeenth century to bring goods from Fushimi into Kyoto in flat-bottomed boats. The first boat basin survives at Nijo. Ogai's story is set on one of the boats, carrying a condemned man down to Osaka at night",
         "十七世纪初豪商角仓了以开凿的运河，用平底小船把货物从伏见运进京都。二条的第一处泊船港湾至今还在。鸥外的小说就发生在一条夜里把罪人送往大阪的高濑舟上"),
    ORIG("jp-yamadera", "Risshaku-ji (Yamadera)", "立石寺（山寺）",
         "The mountain temple founded in 860, its halls strung up a cliff above a thousand stone steps. Basho turned back seven leagues to see it in the summer of 1689 and wrote the cicada poem here",
         "860 年创建的山寺，殿堂沿着悬崖分布，要登上千级石阶。1689 年夏天，芭蕉特意折回七里路来看它，在这里写下了那首蝉声的俳句"),
    ORIG("jp-matsushima", "Matsushima", "松岛",
         "The bay of some two hundred and sixty pine-covered islets, one of the 'three views of Japan'. Seeing it was one of the aims of Basho's journey of 1689",
         "海湾里散布着约二百六十座长满松树的小岛，“日本三景”之一。看一看松岛，是芭蕉 1689 年这趟旅行的目的之一"),
    ORIG("jp-izumozaki", "Izumozaki", "出云崎",
         "The old port on the Echigo coast from which the gold of Sado was landed; the island lies across the water. Basho spent a night here in the seventh month of 1689, and the Sado poem is associated with the town",
         "越后海岸的古港，佐渡的黄金从这里上岸，佐渡岛就在海对面。1689 年七月芭蕉在这里住了一夜，那首写佐渡的俳句同这座小城联系在一起"),
    ORIG("jp-shibutami", "Takuboku Memorial Museum, Shibutami", "石川啄木纪念馆，涩民",
         "Takuboku grew up in the temple of Shibutami village, north of Morioka, under Mount Iwate, and taught for a year at its primary school before leaving for good. The tanka of his first collection keep coming back to it",
         "啄木在盛冈以北、岩手山下的涩民村寺院里长大，在村里的小学代过一年课，然后永远离开了。他第一本歌集里的短歌一再回到这个村子"),
    ORIG("jp-magome", "Magome-juku", "马笼宿",
         "The post town on the stone-paved Nakasendo where Toson was born in 1872, in the family that had kept the official inn for generations. Before the Dawn is the story of his father, the innkeeper 'Aoyama Hanzo', through the fall of the shogunate. A Toson museum stands on the site of the inn",
         "铺着石板的中山道上的驿站。藤村 1872 年生于此地，他家世代经营本阵。《黎明之前》写的就是他的父亲——小说里的本阵主人“青山半藏”——在幕府崩溃前后的一生。本阵旧址上建有藤村纪念馆"),
    ORIG("jp-atami", "Omiya's Pine, Atami", "阿宫之松，热海",
         "The pine on the Atami seafront that marks the best-known scene of Meiji popular fiction, with a bronze of the two lovers beside it",
         "热海海滨的一棵松树，标记着明治通俗小说里最有名的一幕；旁边立着这对恋人的铜像"),
    ORIG("jp-zoshigaya", "Zoshigaya Cemetery, Tokyo", "杂司谷灵园，东京",
         "In Kokoro Sensei goes every month to a grave in this cemetery, and it is here that the student first follows him. Soseki himself was buried in Zoshigaya in 1916",
         "《心》里的先生每个月都到这座墓地给某人扫墓，那位青年学生第一次跟踪他也是在这里。漱石自己 1916 年也葬在杂司谷"),
    ORIG("jp-dazaifu", "Sakamoto Hachiman Shrine, Dazaifu", "坂本八幡宫，太宰府",
         "The shrine is one of the places proposed as the site of the residence of Otomo no Tabito, governor-general of Dazaifu. In the first month of 730 he gave a banquet there at which thirty-two poems on the plum blossom were composed, and the Chinese preface to their poems is the source of the era name Reiwa",
         "这座神社是大宰帅大伴旅人官邸旧址的推定地之一。730 年正月，他在府中设宴，席上众人以梅花为题作歌三十二首；那组和歌的汉文序就是年号“令和”的出处"),
    ORIG("jp-suma", "Suma Bay, Kobe", "须磨海岸，神户",
         "The shore west of Kobe to which Genji withdraws in disgrace, an exile modelled on that of the courtier-poet Ariwara no Yukihira. The 'Suma' chapter made its autumn wind and sound of waves a fixed image of Japanese poetry",
         "神户以西的海岸。源氏失势后退居此地，这段流寓以贵族歌人在原行平的遭遇为蓝本。《须磨》卷让这里的秋风和涛声成了日本诗歌里的固定意象"),
    PIL("jp-ishiyama", "Ishiyama-dera, Otsu", "石山寺，大津",
        "Tradition says Murasaki Shikibu came on retreat to this temple above the Seta river and, watching the full moon of the eighth month over Lake Biwa, began The Tale of Genji. A small room off the main hall is shown as the 'Genji room'",
        "相传紫式部到濑田川畔的这座寺院闭居参拜，望着琵琶湖上八月十五的满月，开始写《源氏物语》。正殿旁有一间小屋，称作“源氏之间”",
        ["tale-of-genji"]),
    PIL("jp-hanamaki", "Hanamaki", "花卷",
        "Kenji Miyazawa was born in Hanamaki in 1896 and died here in 1933, almost unpublished. He taught at the agricultural school, farmed, and worked for the poor farmers of Iwate, the 'Ihatov' of his stories. A memorial museum stands on a hill above the town",
        "宫泽贤治 1896 年生于花卷，1933 年在这里去世，生前几乎没有发表过作品。他在农学校教书、种地，为岩手的贫苦农民奔走——岩手就是他童话里的“伊哈托布”。城外山丘上建有纪念馆",
        ["night-on-the-galactic-railroad"]),
    ORIG("jp-kappabashi", "Kappa Bridge, Kamikochi", "河童桥，上高地",
         "The wooden suspension bridge over the Azusa river in the high valley of Kamikochi, under the Hotaka peaks. Akutagawa, who had walked here as a schoolboy, begins his satire with a climber who chases a kappa through the mist of this valley",
         "穗高连峰下、上高地谷地里梓川上的木吊桥。芥川少年时来这里徒步过，他这部讽刺小说就从一个登山者在这片山谷的雾里追赶河童写起"),
    ORIG("jp-kinosaki", "Kinosaki Onsen", "城崎温泉",
         "The willow-lined hot-spring town on the Japan Sea side of Hyogo. Shiga came here in the autumn of 1913 to recover after being hit by a train in Tokyo, and wrote his best-known story about those weeks",
         "兵库县日本海一侧、柳树成行的温泉町。1913 年秋天，志贺在东京被电车撞伤后来这里疗养，后来把这几个星期写成了他最有名的短篇"),
    ORIG("jp-heian", "Heian Shrine, Kyoto", "平安神宫，京都",
         "The shrine built in 1895 as a scaled-down copy of the first imperial palace, with a garden famous for its weeping cherries. Kawabata's novel of Kyoto through one year begins with a visit to see them",
         "1895 年按最初的皇宫缩小仿建的神社，庭园里的红枝垂樱很有名。川端这部按一年四季写京都的小说，就从去看这些樱花开始"),
    ORIG("jp-kamishima", "Kamishima", "神岛",
         "A small fishing island at the mouth of Ise Bay. Mishima stayed here in 1953 and set his story of a young fisherman and a diver's daughter on it, under the name Utajima; the lighthouse, the shrine steps and the wartime observation post of the novel are all still there",
         "伊势湾口的小渔岛。三岛 1953 年来这里住过，把年轻渔夫和海女之女的故事安排在岛上，改名“歌岛”；小说里的灯塔、神社石阶和战时的监视哨至今都在", offshore_island=True),
    ORIG("jp-kodomari", "Kodomari, Tsugaru", "小泊，津轻",
         "The fishing village on the west coast of the Tsugaru peninsula. Dazai's wartime journey round his native region ends here, where he finds Take, the nursemaid who brought him up",
         "津轻半岛西岸的渔村。太宰治战时环游故乡的旅程在这里结束：他找到了把自己带大的保姆阿竹"),
    ORIG("jp-toshodaiji", "Toshodai-ji, Nara", "唐招提寺，奈良",
         "The temple founded in 759 by the Chinese monk Jianzhen (Ganjin), who reached Japan blind at his sixth attempt. Inoue's novel follows the young Japanese monks sent to China to bring such a master back",
         "759 年由中国僧人鉴真创建的寺院。鉴真第六次东渡才抵达日本，那时已经双目失明。井上靖的小说写的是那几位被派往中国延请传戒高僧的年轻日本僧人"),
    ORIG("jp-katsurahama", "Katsurahama, Kochi", "桂滨，高知",
         "The beach south of Kochi where a bronze Sakamoto Ryoma has looked out over the Pacific since 1928. Shiba's long novel made the Tosa swordsman who brokered the alliance against the shogunate the best-loved figure of modern Japanese history",
         "高知以南的海滩，坂本龙马的铜像自 1928 年起在这里眺望太平洋。司马辽太郎的长篇小说，让这位撮合倒幕同盟的土佐剑客成了日本近代史上最受喜爱的人物"),
    ORIG("jp-kashii", "Kashii, Fukuoka", "香椎，福冈",
         "The suburb on Hakata Bay where the novel's two bodies are found on the rocky shore. The two Kashii stations, a few minutes' walk apart, are part of the puzzle",
         "博多湾边的郊区，小说里的两具尸体就是在这里的礁石海岸上被发现的。相隔几分钟路程的两个香椎车站也是谜题的一部分"),
    ORIG("jp-takamatsu", "Takamatsu", "高松",
         "The port city on Shikoku to which the fifteen-year-old runaway of Murakami's novel takes the night bus from Tokyo. The private library where he finds shelter is invented",
         "四国的港口城市。村上这部小说里十五岁的离家少年从东京坐夜行巴士来到这里。他栖身的那座私人图书馆是虚构的"),
    ORIG("jp-yashima", "Yashima", "屋岛",
         "The flat-topped headland east of Takamatsu where the Heike made their base and where Yoshitsune surprised them in 1185. The Tale of the Heike sets one of its most famous episodes on the shore below",
         "高松以东的平顶山岬。平家曾在此设营，1185 年源义经在这里奇袭了他们。《平家物语》最著名的段落之一就发生在山下的海边"),
    PIL("jp-matsue", "Lafcadio Hearn's Former Residence, Matsue", "小泉八云旧居，松江",
        "Hearn came to Matsue as an English teacher in 1890 and lived in this samurai house by the castle moat in 1891. The essay 'In a Japanese Garden' in his first Japanese book describes its three small gardens",
        "赫恩 1890 年到松江当英语教师，1891 年住在护城河边的这幢武士宅邸里。他第一本写日本的书里那篇《日本的庭院》，写的就是这里的三个小庭院",
        ["glimpses-of-unfamiliar-japan"]),
    PIL("jp-chiri", "Chiri Yukie Memorial Museum, Noboribetsu", "知里幸惠 银之滴纪念馆，登别",
        "Chiri Yukie was born in Noboribetsu in 1903. She wrote down thirteen of her people's sacred songs in Ainu with her own Japanese translation, and died in Tokyo at nineteen on the night she finished correcting the proofs",
        "知里幸惠 1903 年生于登别。她用阿伊努语记下本民族的十三篇神谣，并亲自译成日文；校完清样的当晚，她在东京去世，年仅十九岁",
        ["ainu-shinyoshu"]),
    ORIG("jp-miura", "Miura Ayako Literature Museum, Asahikawa", "三浦绫子纪念文学馆，旭川",
         "The museum stands in the plantation of foreign trees on the edge of Asahikawa beside which the doctor's family of Freezing Point lives, and where the novel's first and last scenes take place",
         "纪念馆坐落在旭川市郊的外国树种样本林里。《冰点》里医生一家就住在林子旁边，小说的开头和结尾都发生在这片树林"),
    ORIG("jp-urakami", "Urakami Cathedral, Nagasaki", "浦上天主堂，长崎",
         "The cathedral of Nagasaki's old Christian district stood five hundred metres from the centre of the explosion of 9 August 1945 and was destroyed. One of its bells was dug out of the rubble and rung that Christmas, which gave the radiologist Nagai Takashi the title of his account",
         "长崎旧天主教徒聚居区的主教座堂，距 1945 年 8 月 9 日原子弹爆炸中心仅五百米，被彻底摧毁。人们从瓦砾中挖出一口钟，在那年圣诞节敲响，放射科医生永井隆的纪实因此得名"),
    ORIG("jp-inasa", "Mount Inasa, Nagasaki", "稻佐山，长崎",
         "The hill across the harbour from the city, reached by cable car. Ishiguro, who was born in Nagasaki in 1954 and left at five, sends the women of his first novel up it on a day's outing. Seventy years earlier Pierre Loti had sailed into the bay below",
         "隔着港湾与市区相望的山，有缆车可上。石黑一雄 1954 年生于长崎，五岁离开；他在第一部小说里让几位女主人公到这座山上郊游了一天。再早七十年，皮埃尔·洛蒂的军舰就驶进了山下的海湾"),
    ORIG("jp-yakushima", "Yakushima", "屋久岛",
         "The mountainous island south of Kyushu where, people say, it rains thirty-five days a month. Hayashi Fumiko travelled here in 1950 for the last chapters of her last finished novel",
         "九州以南的多山岛屿，俗话说这里“一个月下三十五天雨”。1950 年林芙美子为了写她最后一部完成的长篇的结尾几章，专程来过这里"),
    ORIG("jp-nikko", "Kanaya Hotel, Nikko", "金谷饭店，日光",
         "In June 1878 Isabella Bird, setting out for the north, stayed for some days at Nikko in the house of Kanaya Zenichiro, who had begun letting rooms to foreigners. The house is kept as a museum, and the hotel he went on to build stands on the hill above the sacred bridge",
         "1878 年 6 月，准备北上的伊莎贝拉·伯德在日光金谷善一郎的家里住了一些日子，当时他刚开始把房间租给外国人。那幢房子今为纪念馆；他后来建的饭店就在神桥上方的山坡上"),
]

lines = [
    Q("botchan-1", "botchan", "jp-dogo", "Chapter 3", "第三章", JW, T_BOT,
      raw(T_BOT, "この住田と云う所は温泉のある町で", "公園もある上に遊廓がある。"), ["住田と云う所は温泉のある町"],
      "This place called Sumita is a hot-spring town, ten minutes or so from the castle town by train and thirty on foot, with restaurants and hot-spring inns and a park, and a licensed quarter on top of that.",
      ["Sumita is a hot-spring town"],
      "这个叫住田的地方是个温泉町，从城下坐火车十来分钟，走路三十分钟就到，有饭馆，有温泉旅店，有公园，此外还有花街。",
      ["住田的地方是个温泉町"]),
    Q("sanshiro-1", "sanshiro", "jp-sanshiro-pond", "Chapter 2", "第二章", JW, T_SAN,
      raw(T_SAN, "三四郎がじっとして池の面を見つめていると", "遠くかつはるかな心持ちがした。"), ["池の面"],
      "As Sanshiro sat still, gazing at the surface of the pond, he saw any number of great trees reflected in the depths of the water, and deeper still the blue sky. At that moment he felt far away, farther than the trams, farther than Tokyo, farther than Japan.",
      ["the surface of the pond"],
      "三四郎一动不动地凝视着池面，只见许多大树倒映在水底，再往下还能看见蓝天。这一刻，三四郎觉得自己离得很远很远，比电车远，比东京远，比日本还远。",
      ["池面"]),
    Q("kusamakura-1", "kusamakura", "jp-oama", "Opening", "开头", JW, T_KUS,
      ind(raw(T_KUS, "山路を登りながら、こう考えた。", "とかくに人の世は住みにくい。")), ["山路"],
      "Climbing the mountain path, I thought:\nWork by reason, and you grow sharp-edged. Pole along the stream of feeling, and you are swept away. Insist on your own will, and you are cramped. In short, this world of men is a hard place to live.",
      ["the mountain path"],
      "一边登着山路，一边这样想：\n凭理智行事，就会棱角毕露；顺着感情撑篙，就会被水冲走；固执己见，又处处受窘。总之，人世是难住的。",
      ["山路"], note=IND),
    Q("takasebune-1", "takasebune", "jp-takase", "Opening", "开头", JW, T_TAK,
      raw(T_TAK, "高瀬舟は京都の高瀬川を上下する小舟である。", "大阪へ廻されることであつた。"), ["京都の高瀬川"],
      "A Takase boat is a small boat that goes up and down the Takase River in Kyoto. In the Tokugawa period, when a criminal of Kyoto was sentenced to exile on a distant island, his relatives were summoned to the jail and allowed to take leave of him there. Then the criminal was put on a Takase boat and sent round to Osaka.",
      ["the Takase River in Kyoto"],
      "高濑舟是在京都高濑川上来往的小船。德川时代，京都的罪人被判流放远岛之后，他的亲属会被叫到牢房，获准在那里同他诀别。然后罪人就被送上高濑舟，押往大阪。",
      ["京都高濑川"]),
    Q("oku-yamadera", "oku-no-hosomichi", "jp-yamadera", "Risshaku-ji", "立石寺", JW, T_OKU,
      ind(raw(T_OKU, "山形領に立石寺といふ山寺あり", "閑さや岩にしみ込せみの聲")), ["立石寺"],
      "In the domain of Yamagata there is a mountain temple called Risshaku-ji, founded by the Great Teacher Jikaku, a place of rare purity and stillness. People urged us to see it, so we turned back from Obanazawa, a distance of some seven leagues. It was still light. We took lodgings at a priest's house at the foot and climbed to the halls on the mountain. Rock is piled on boulder to make the hill, the pines and cypresses are old, the earth and stones are aged and smooth with moss, and the doors of the halls on the rocks were shut, with not a sound to be heard. We went round the cliff and crept over the rocks to worship at the Buddha hall, and in the lovely scene and the silence I felt only my heart growing clear.\nThe stillness:\nsinking into the rocks,\nthe cicadas' cry.",
      ["Risshaku-ji"],
      "山形领内有一座山寺，叫立石寺，是慈觉大师开创的，格外清静。人们都劝我们去看一看，于是从尾花泽折回去，其间约有七里。天色尚早，先在山脚的僧坊订好住处，然后登上山上的佛堂。岩上叠岩成山，松柏苍老，土石古旧，青苔滑润；岩上各院的门扉紧闭，听不到一点声响。绕过崖边，爬过岩石，参拜了佛阁，只觉得佳景寂寞，心也澄净下来。\n寂静啊，\n渗入岩石里的\n蝉声。",
      ["立石寺"], note=IND + " (this edition prints the poem as しみ込, 'sinking in')"),
    Q("oku-matsushima", "oku-no-hosomichi", "jp-matsushima", "Matsushima", "松岛", JW, T_OKU,
      raw(T_OKU, "抑事ふりにたれど松島は扶桑第一の好風にして", "兒孫を愛するがごとし"), ["松島"],
      "It has been said many times before, but Matsushima is the finest scenery in all Japan, and need not blush before Dongting or the West Lake. The sea comes in from the south-east and fills a bay three leagues across, brimming like the tide of Zhejiang. Islands beyond counting: those that rise point to the sky, those that lie low crawl upon the waves. Some are piled in two layers, some folded in three; they part to the left and join to the right. Some carry others on their backs, some hold them in their arms, as if fondling children and grandchildren.",
      ["Matsushima"],
      "这话早已被人说旧了，可松岛实在是扶桑第一的好风景，决不逊于洞庭、西湖。海水从东南涌入，湾内三里，满盈如浙江之潮。岛屿不可胜数：耸立的直指青天，低伏的匍匐波上；有的叠作两层，有的折成三重，左边分开，右边相连；有的背着，有的抱着，好像在疼爱儿孙。",
      ["松岛"]),
    Q("oku-sado", "oku-no-hosomichi", "jp-izumozaki", "Echigo", "越后路", JW, T_OKU,
      ind(raw(T_OKU, "あら海や佐渡に橫たふ天河", "あら海や佐渡に橫たふ天河")), ["佐渡"],
      "The rough sea:\nstretching out over Sado,\nthe River of Heaven.",
      ["Sado"],
      "汹涌的海啊，\n横卧在佐渡之上的\n银河。",
      ["佐渡"]),
    Q("takuboku-1", "a-handful-of-sand", "jp-shibutami", "'Smoke', part 2", "《烟》之二", JW, T_ICH,
      raw(T_ICH, "ふるさとの山に向ひて", "ふるさとの山はありがたきかな"), ["ふるさとの山"],
      "Facing the mountain of my home\nI have nothing to say.\nThe mountain of my home: how thankful I am for it.",
      ["mountain of my home"],
      "面对故乡的山，\n无话可说，\n故乡的山，真叫人感激啊。",
      ["故乡的山"]),
    Q("yoake-1", "before-the-dawn", "jp-magome", "Part 1, prologue", "第一部序章", JW, T_YOA,
      raw(T_YOA, "木曾路はすべて山の中である。", "一筋の街道はこの深い森林地帯を貫いていた。"), ["木曾路"],
      "The Kiso road lies entirely among the mountains. In one place it is a path along a cliff, clinging to the precipice; in another it is the bank of the Kiso river, many tens of yards above the water; in another it is the entrance to a valley, rounding the tail of a mountain. A single highway ran through this deep forest country.",
      ["The Kiso road"],
      "木曾路全在山里。有的地方是贴着峭壁走的崖道，有的地方是下临数十间深的木曾川岸，有的地方是绕过山尾的谷口。一条大道贯穿着这片幽深的森林地带。",
      ["木曾路"]),
    Q("konjiki-1", "konjiki-yasha", "jp-atami", "Part 1, chapter 8", "前编第八章", JW, T_KON,
      raw(T_KON, "一月の十七日、宮さん、善く覚えてお置き。", "死んでも僕は忘れんよ！"), ["今月今夜"],
      "The seventeenth of January, Miya: remember it well. Next year, on this night of this month, where will Kan'ichi be looking at this moon! The year after, on this night of this month… ten years from now, on this night of this month… all my life I shall not forget this night of this month. How could I forget it? Even dead I shall not forget!",
      ["this night of this month"],
      "一月十七日，阿宫，你好好记住。明年的今月今夜，贯一会在什么地方看这个月亮呢！后年的今月今夜……十年后的今月今夜……我一辈子也忘不了今月今夜，怎么忘得了，就是死了我也忘不了！",
      ["今月今夜"]),
    Q("kokoro-zo1", "kokoro", "jp-zoshigaya", "Part 1, chapter 4", "上篇第四节", JW, T_KOK,
      raw(T_KOK, "先生は例月その日になると雑司ヶ谷の墓地にある", "習慣なのだそうである。"), ["雑司ヶ谷の墓地"],
      "Every month on that day, I was told, Sensei was in the habit of going to lay flowers at a certain grave in the cemetery at Zoshigaya.",
      ["the cemetery at Zoshigaya"],
      "据说先生有个习惯，每月到了那一天，都要去杂司谷墓地给某位故人献花。",
      ["杂司谷墓地"]),
    Q("genji-suma1", "tale-of-genji", "jp-suma", "Chapter 12, 'Suma'", "第十二帖《须磨》", JW, T_SUM,
      raw(T_SUM, "須磨には、いとど心尽くしの秋風に", "かかる所の秋なりけり。"), ["須磨"],
      "At Suma the autumn wind brought ever deeper melancholy; the sea was some way off, but the waves of the bay, of which the counsellor Yukihira once sang that the wind 'blows across the barrier', sounded very near indeed night after night, and nothing could be more moving than autumn in such a place.",
      ["Suma"],
      "须磨这地方，秋风越发叫人愁肠百转。海虽然离得稍远，但行平中纳言吟咏过“越关吹来”的那片海湾的波涛，夜夜听来却近在耳边；再没有什么比这种地方的秋天更令人感伤的了。",
      ["须磨"]),
    Q("manyo-ume1", "manyoshu", "jp-dazaifu", "Book 5, preface to the thirty-two plum-blossom poems", "卷五《梅花歌三十二首》序", JW, T_MAN,
      raw(T_MAN, "天平二年正月の十三日、帥の老の宅に萃ひて", "蘭は珮後の香を薫らす。"), ["帥の老の宅"],
      "On the thirteenth day of the first month of the second year of Tenpyo we gathered at the residence of the old Governor-General and held a banquet. It was the fair month of early spring; the air was fresh and the wind gentle. The plum blossoms opened like powder before a mirror, and the orchids breathed the fragrance of a sachet.",
      ["the residence of the old Governor-General"],
      "天平二年正月十三日，聚集在帅老的宅邸，开宴会。时值初春令月，气淑风和；梅花绽开，如镜前的脂粉，兰草吐香，如佩后的香囊。",
      ["帅老的宅邸"]),
    Q("loti-1", "madame-chrysantheme", "jp-inasa", "Chapter 2", "第二章", FW, T_LOTI,
      raw(T_LOTI, "Quand Nagasaki parut, ce fut une déception pour nos yeux", "c’était une ville tout à fait quelconque.", "fr"), ["Nagasaki"],
      "When Nagasaki came into view, it was a disappointment to our eyes: at the foot of the green overhanging mountains, it was a town of the most ordinary kind.",
      ["Nagasaki"],
      "等到长崎出现在眼前，我们的眼睛却失望了：在高悬的青山脚下，它不过是一座再平常不过的城市。",
      ["长崎"]),
]
# Isabella Bird wrote in English: the passage is the original.
_k1 = raw(T_BIRD, "Kanaya is the chief man in the village", "apparently well educated.", "en")
_k2 = raw(T_BIRD, "Of late, to help his income, he has let these charming rooms", "Europeanising his beautiful home.", "en")
assert "[" not in _k1 + _k2
lines.append(dict(id="bird-nikko1", book_id="unbeaten-tracks-in-japan", place_ids=["jp-nikko"], location="Letter VII", location_zh="第七封信",
                  text_en=_k1 + GAP + _k2, highlight_en=["Kanaya"], translation="original",
                  text_zh="金谷是村里的头面人物，很聪明，看得出受过良好教育。\n…\n近来为了贴补收入，他把这些可爱的房间租给带着介绍信来的外国人；他很想让客人满意，而他的好品味又使他不肯把自己美丽的家弄得洋里洋气。",
                  highlight_zh=["金谷"], status="draft", checked=f"English Wikisource, {T_BIRD} (a gap marked …), {DATE}"))
lines += [
    S("kappa-s1", "kappa-akutagawa", "jp-kappabashi", "Chapters 1–2", "第一、二章",
      "Patient No. 23 of a mental hospital tells anyone who will listen how, three summers ago, he set out alone from the hot-spring inn at Kamikochi to climb Mount Hotaka. In the mist by the Azusa river he saw a kappa looking at him, chased it through the bamboo grass, fell into a hole, and woke up in the country of the kappas.",
      "某精神病院的第二十三号病人逢人便讲：三年前的夏天，他独自从上高地的温泉旅馆出发去登穗高山。在梓川边的雾里，他看见一只河童正望着自己，便穿过山白竹丛追上去，掉进一个洞里，醒来已经到了河童的国度。",
      ["Kamikochi"], ["上高地"], W + "Kappa_(novella)"),
    S("kinosaki-s1", "at-kinosaki", "jp-kinosaki", "The whole story", "全篇",
      "Convalescing alone at the hot spring after an accident that might have killed him, the narrator watches three small deaths: a bee lying still on the roof outside his window, a rat with a skewer through its neck being stoned as it swims the stream, and a newt he kills himself with a carelessly thrown pebble. Being alive and being dead come to seem to him not so far apart.",
      "叙述者在一场险些丧命的事故之后，独自到温泉疗养，目睹了三次微小的死亡：窗外屋顶上一动不动的蜜蜂，脖子上穿着竹签、在小河里挣扎着被人扔石头的老鼠，还有被他自己随手扔出的石子打死的蝾螈。他渐渐觉得，活着和死去并不是相隔多远的两回事。",
      ["the hot spring"], ["温泉"], JAW + "城の崎にて"),
    S("koto-s1", "the-old-capital", "jp-heian", "Chapter 1, 'The Flowers of Spring'", "第一章《春花》",
      "Chieko, the adopted daughter of a kimono wholesaler, goes with her childhood friend Shin'ichi to see the weeping cherries in the garden of the Heian Shrine, and under the blossoms tells him she was a foundling. Later that year, at the Gion festival, she will meet a girl from the cedar village in the northern hills who has her own face.",
      "和服批发商的养女千重子同青梅竹马的真一去平安神宫的神苑看红枝垂樱，在花下告诉他自己是个弃儿。这一年稍后的祇园祭上，她将遇见一个来自北山杉村、长着同她一模一样面孔的姑娘。",
      ["the Heian Shrine"], ["平安神宫"], W + "The_Old_Capital"),
    S("shiosai-s1", "sound-of-waves", "jp-kamishima", "Chapter 8", "第八章",
      "Shinji, a poor young fisherman, and Hatsue, the daughter of the richest man on the island, shelter from a storm in the ruined observation post on the hill. They dry their clothes on either side of a fire, and she tells him to jump across it to her. The island's gossip does the rest, until Shinji proves himself in a typhoon at sea.",
      "穷苦的年轻渔夫新治和岛上首富的女儿初江，在山上废弃的监视哨里躲避暴风雨。两人隔着一堆火烘干衣服，她叫他从火上跳过来。此后岛上流言四起，直到新治在海上的台风中证明了自己。",
      ["the ruined observation post"], ["废弃的监视哨"], W + "The_Sound_of_Waves"),
    S("tsugaru-s1", "tsugaru", "jp-kodomari", "Chapter 5, 'The West Coast'", "第五章《西海岸》",
      "On the last day of his journey Dazai takes the bus to Kodomari to find Take, the nursemaid he has not seen for nearly thirty years. Her house is locked: the whole village is at the school sports day. He walks round the crowded field until a girl leads him to her, and the two sit side by side watching the races, hardly speaking.",
      "旅行的最后一天，太宰坐公共汽车到小泊去找阿竹——将近三十年没见面的保姆。她家锁着门：全村人都去看学校的运动会了。他在拥挤的操场上转来转去，直到一个女孩把他领到她跟前；两人并肩坐着看赛跑，几乎没说话。",
      ["Kodomari"], ["小泊"], JAW + "津軽_(小説)"),
    S("tempyo-s1", "roof-tile-of-tempyo", "jp-toshodaiji", "The whole novel", "全书",
      "In 733 young monks sail for Tang China with the embassy, Yoei and Fusho among them, charged to bring back a master who can ordain priests properly. Of the others, one wanders off into the country and one settles there; Yoei dies in the south; the old monk Gyogo, who has spent his life copying sutras, goes down with his manuscripts on the voyage home. Only Fusho stays the course, and twenty years later lands in Japan with the old, blind Jianzhen.",
      "733 年，荣叡、普照等几个年轻僧人随遣唐使船前往唐土，奉命请回一位能如法传戒的高僧。其余的人，一个云游四方，一个留在了那里；荣叡死在南方；抄了一辈子经的老僧业行，在归国途中连同经卷一起沉入海底。只有普照坚持到底，二十年后同年老失明的鉴真一起踏上日本的土地。",
      ["Jianzhen"], ["鉴真"], JAW + "天平の甍"),
    S("ryoma-s1", "ryoma-ga-yuku", "jp-katsurahama", "The whole novel", "全书",
      "The youngest son of a merchant-samurai family of Kochi, a late bloomer whom nobody expected much of, leaves Tosa for a fencing school in Edo in the year the American ships arrive. Over the next fourteen years he flees his domain, founds a trading company with a navy of its own, reconciles Satsuma and Choshu, and is cut down in Kyoto a month after the shogun resigns.",
      "高知一个商人出身的乡士家里的小儿子，开窍很晚，谁也没指望他有什么出息；就在美国军舰到来的那一年，他离开土佐去江户的剑术道场。此后十四年里，他脱藩出走，办起一家自带海军的商社，撮合了萨摩和长州，又在将军交还大政一个月后在京都遇刺。",
      ["Kochi"], ["高知"], W + "Ryōma_ga_Yuku"),
    S("ten-s1", "points-and-lines", "jp-kashii", "Chapters 1–4", "第一至四章",
      "On a January morning a ministry official and a waitress from a Tokyo restaurant are found lying side by side on the shore at Kashii, poisoned with cyanide: to all appearances a lovers' suicide. An old Fukuoka detective is bothered by a dining-car receipt for one. The case comes to turn on the four minutes a day in which one platform of Tokyo Station can be seen from another.",
      "一月的一个早晨，某部的一名官员和东京一家餐馆的女招待被发现并排躺在香椎的海岸上，死于氰化物中毒——怎么看都是殉情。福冈的一位老刑警却对一张只有一人份的餐车收据放心不下。案子最后的关键，是东京站一天之中只有四分钟能从一个站台望见另一个站台。",
      ["the shore at Kashii"], ["香椎的海岸"], W + "Points_and_Lines"),
    S("kafka-s1", "kafka-on-the-shore", "jp-takamatsu", "Chapters 1–7", "第一至七章",
      "On his fifteenth birthday a boy who calls himself Kafka Tamura leaves his father's house in Tokyo and takes the night bus to Takamatsu, for no better reason than that Shikoku is far away and warm. He spends his days in a small private library kept by an elegant woman and a young assistant, and is taken in there.",
      "一个自称田村卡夫卡的少年在十五岁生日那天离开东京父亲的家，坐夜行巴士去了高松，理由不过是四国够远，也够暖和。他每天泡在一座小小的私人图书馆里，图书馆由一位优雅的女士和一个年轻馆员打理，后来他就被收留在那里。",
      ["Takamatsu"], ["高松"], W + "Kafka_on_the_Shore"),
    S("heike-yashima", "tale-of-the-heike", "jp-yashima", "Book 11, 'Nasu no Yoichi'", "卷十一《那须与一》",
      "At dusk, with the fighting broken off, a boat puts out from the Heike fleet with a fan fixed to a pole and a lady beckoning beside it. Yoshitsune orders the young archer Nasu no Yoichi to shoot. He rides into the sea, prays, and looses; the fan flies up and falls into the waves, and both sides beat their quivers and the sides of their ships in applause.",
      "黄昏时分，战斗暂歇，平家船队里划出一条小船，竿头插着一把扇子，旁边一位女官招手示意。义经命令年轻的射手那须与一去射。他策马走进海里，祈祷之后放箭；扇子飞上半空，落进波浪，两军一齐敲着箭筒和船舷喝彩。",
      ["the Heike fleet"], ["平家船队"], W + "Nasu_no_Yoichi"),
    S("hyoten-s1", "freezing-point", "jp-miura", "The whole novel", "全书",
      "While the doctor's wife is entertaining an admirer, their small daughter wanders out and is strangled by the river beyond the wood. To punish his wife, the doctor secretly adopts a baby girl he believes to be the murderer's daughter and lets her bring the child up as her own. The girl, Yoko, grows up loved by everyone, until the wife finds his diary.",
      "医生的妻子在家里接待一位爱慕者的时候，年幼的女儿独自跑了出去，在树林那边的河滩上被人掐死。为了惩罚妻子，医生瞒着她收养了一个他以为是凶手女儿的女婴，让她当作亲生女儿抚养。这个叫阳子的女孩在人人疼爱中长大，直到妻子发现了丈夫的日记。",
      ["the wood"], ["树林"], W + "Freezing_Point_(novel)"),
    S("nagai-s1", "bells-of-nagasaki", "jp-urakami", "The whole book", "全书",
      "Nagai, a radiologist at the medical college, already ill with leukaemia, is at work when the bomb falls on 9 August 1945. He describes the relief party he led for days among the dying, finding his wife's remains in the ashes of their kitchen, and his own attempt, as a doctor and a Catholic, to make sense of what had happened to Urakami.",
      "医科大学的放射科医生永井当时已患白血病，1945 年 8 月 9 日原子弹落下时他正在上班。他记下了自己带领救护队在垂死的人中间连续工作的那些天，在自家厨房的灰烬里找到妻子的遗骨，以及他作为医生和天主教徒，试图理解浦上遭遇的这一切。",
      ["Urakami"], ["浦上"], W + "The_Bells_of_Nagasaki"),
    S("pale-s1", "a-pale-view-of-hills", "jp-inasa", "Chapter 7", "第七章",
      "Etsuko, living in England after her elder daughter's death, remembers a summer in Nagasaki a few years after the bomb, and one day in particular: the cable car up to the hills of Inasa with her neighbour Sachiko and Sachiko's strange little girl, the harbour below, and how happy they were.",
      "大女儿死后独居英国的悦子，回忆起原子弹爆炸几年之后在长崎度过的一个夏天，特别是其中一天：她同邻居佐知子和佐知子那个古怪的小女儿坐缆车上了稻佐的山，港口在脚下，那天她们多么快活。",
      ["the hills of Inasa"], ["稻佐的山"], W + "A_Pale_View_of_Hills"),
    S("ukigumo-s1", "floating-clouds", "jp-yakushima", "Final chapters", "结尾几章",
      "Yukiko and Tomioka became lovers as forestry officials in wartime Indochina; back in ruined Tokyo he will neither keep her nor let her go. When he takes a post on Yakushima she follows him, already ill, and dies alone in the forestry lodging while the rain comes down and he is up in the mountains.",
      "雪子和富冈战时在法属印度支那的林业部门相识相恋；回到一片废墟的东京后，他既不肯同她在一起，又不肯放她走。他到屋久岛任职，已经病重的她跟了去；大雨倾盆，他上山去了，她独自死在林业署的宿舍里。",
      ["Yakushima"], ["屋久岛"], W + "Floating_Clouds"),
]

ids = lambda name: set(re.findall(r'\{ id: "([^"]+)"', open(b.data(name), encoding="utf-8").read()))
old_books, old_places, old_lines = ids("books.js"), ids("places.js"), ids("lines.js")
new_b, new_p, new_l = {x["id"] for x in books}, {x["id"] for x in places}, {x["id"] for x in lines}
assert len(new_b) == len(books) and len(new_p) == len(places) and len(new_l) == len(lines)
assert not new_b & old_books and not new_p & old_places and not new_l & old_lines, (new_b & old_books, new_p & old_places, new_l & old_lines)
assert new_p == set(CO), new_p ^ set(CO)
bids, pids = new_b | old_books, new_p | old_places
for l in lines:
    assert l["book_id"] in bids and all(p in pids for p in l["place_ids"]), l["id"]
used = {p for l in lines for p in l["place_ids"]}
for p in places:
    assert p["id"] in used or p.get("book_ids"), p["id"]
    assert all(i in bids for i in p.get("book_ids", [])), p["id"]
covered = {l["book_id"] for l in lines} | {i for p in places for i in p.get("book_ids", [])}
assert not new_b - covered, new_b - covered

if __name__ == "__main__":
    M = "11-23: fifth pack (tools/content/batches/add_jp5.py)"
    b.append(b.data("books.js"), books, M)
    b.append(b.data("places.js"), places, M)
    b.append(b.data("lines.js"), lines, M)
    print(len(books), "books,", len(places), "places,", len(lines), "lines (", sum(1 for l in lines if l.get("kind") != "scene"), "quotations )")
