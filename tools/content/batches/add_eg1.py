"""11-24: Egypt, first pack: 5 new books (Herodotus and Cavafy shared with Greece, The Innocents Abroad with Italy), 8 places.
Herodotus at the Great Pyramid, Mark Twain at the Sphinx, Cavafy's flat in Alexandria, Shelley's Ozymandias at the Ramesseum,
Mahfouz's Bayn al-Qasrayn and his museum, the Yacoubian Building and the Old Cataract Hotel at Aswan (Christie).
The map has Egypt's 27 governorates.

Quotations (4 lines) are cut from Greek and English Wikisource pages (tools/content/wikisource.py); translations are our
own drafts. Books in copyright get scene notes with a fact source. What a cut changes is named in `checked`.

Coordinates are those of the place's English Wikipedia article, the museum's from Wikidata (coords/add_eg1.json). Midaq Alley
has no place of its own: no source gave coordinates for the alley, so the book hangs on the Mahfouz museum.

The Ramesseum carries region EG-LX: the map's outlines (Natural Earth) still show Luxor as the small city governorate
of before 2009, so the west bank would otherwise be counted in Qena.

Usage: python3 -I add_eg1.py <app_dir> <coords.json> <wikisource_root>"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b
import wikisource as ws

APP, CO, WSR = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8")), sys.argv[3]
DATE = "2026-11-24"
b.init(APP, "", "eg", DATE)
W = b.W
GAP = b.GAP

def BK(id, title, title_zh, title_orig, author, author_zh, author_orig, year, pd=True, **kw):
    d = dict(id=id, title=title, title_zh=title_zh, title_orig=title_orig, author=author, author_zh=author_zh, year=year,
             orig_lang=kw.pop("lang", "nl"), public_domain=pd, source_url=kw.pop("src", None), author_orig=author_orig)
    d.update(kw)
    return {k: v for k, v in d.items() if v is not None or k == "source_url"}

def C(pid):
    c = CO[pid]
    return c["lat"], c["lon"], c["st"], c["su"]

def ORIG(pid, name, zh, en_note, zh_note, **kw): return b.ORIG(pid, name, zh, *C(pid), en_note, zh_note, **kw)
def PIL(pid, name, zh, en_note, zh_note, ids, **kw): return b.PIL(pid, name, zh, *C(pid), en_note, zh_note, ids, **kw)
S = b.S

def raw(title, start, end, lang="nl"):
    t = ws.text(os.path.join(WSR, lang), title)
    n = re.sub("[\xa0   ]", " ", t)
    i = n.find(start)
    assert i >= 0, (title, start)
    j = n.find(end, i)
    assert j >= 0, (title, start, end)
    return t[i:j + len(end)]

def flow(s):
    """a hard-wrapped paragraph: lines joined, doubled spaces written as one"""
    return re.sub(r" {2,}", " ", s.replace("\n", " "))

def Q(id, book, place, loc, loc_zh, title, orig, hl_orig, en, hl_en, zh, hl_zh, note="", site="Dutch"):
    if re.search("[\xa0   ]", orig):
        orig = re.sub("[\xa0   ]+", " ", orig)
        note += " (no-break spaces written as plain spaces)"
    if "  " in orig:
        orig = re.sub(" {2,}", " ", orig)
        note += " (a doubled space written as one)"
    for text, hls in ((orig, hl_orig), (en, hl_en), (zh, hl_zh)):
        for h in hls:
            assert h in text, (id, h)
    assert "[" not in orig and "Sjabloon" not in orig, (id, "page mark or broken template")
    return dict(id=id, book_id=book, place_ids=[place], location=loc, location_zh=loc_zh,
                text_orig=orig, highlight_orig=hl_orig, text_en=en, highlight_en=hl_en, text_zh=zh, highlight_zh=hl_zh, translation="own",
                status="draft", checked=f"{site} Wikisource, {title}{note}, {DATE}")

def EN(id, book, place, loc, loc_zh, title, text, hl, zh, hl_zh, note=""):
    assert "[" not in text and "]" not in text and "\xa0" not in text and "  " not in text, (id, text[:40])
    for h in hl: assert h in text, (id, h)
    for h in hl_zh: assert h in zh, (id, h)
    return dict(id=id, book_id=book, place_ids=[place], location=loc, location_zh=loc_zh, text_en=text, highlight_en=hl, translation="original",
                text_zh=zh, highlight_zh=hl_zh, status="draft", checked=f"English Wikisource, {title}{note}, {DATE}")

T_HD = "Ιστορίαι (Ηροδότου)/Ευτέρπη"
T_CV = "Απολείπειν ο θεός Αντώνιον"
T_IA = "The Innocents Abroad/Chapter 58"
T_OZ = "The Complete Poetical Works of Percy Bysshe Shelley (ed. Hutchinson, 1914)/Ozymandias"
EXIST = {"histories", "cavafy", "innocents-abroad"}

def once(title, s, lang):
    """the cut must start at the only place the words stand on the page"""
    n = ws.text(os.path.join(WSR, lang), title).count(s)
    assert n == 1, (title, s, n)
    return s

MAHFOUZ = dict(author="Naguib Mahfouz", author_zh="纳吉布·马哈福兹", author_orig="نجيب محفوظ")
books = [
    BK("ozymandias", "Ozymandias", "奥兹曼迪亚斯", "Ozymandias", "Percy Bysshe Shelley", "珀西·比希·雪莱", "Percy Bysshe Shelley", "1818",
       lang="en", src=ws.url("en", T_OZ), aliases=["Ramesses II", "Ramesseum", "King of Kings", "Percy Shelley", "珀西·雪莱", "拉美西斯二世"]),
    BK("palace-walk", "Palace Walk", "宫间街", "بين القصرين", MAHFOUZ["author"], MAHFOUZ["author_zh"], MAHFOUZ["author_orig"], "1956",
       lang="ar", pd=False, aliases=["Bayn al-Qasrayn", "Cairo Trilogy", "开罗三部曲", "Amina", "al-Sayyid Ahmad", "Mahfouz", "马哈福兹"]),
    BK("midaq-alley", "Midaq Alley", "梅达格胡同", "زقاق المدق", MAHFOUZ["author"], MAHFOUZ["author_zh"], MAHFOUZ["author_orig"], "1947",
       lang="ar", pd=False, aliases=["Zuqaq al-Midaq", "Midaqq Alley", "Hamida", "Kirsha", "Mahfouz", "马哈福兹"]),
    BK("yacoubian-building", "The Yacoubian Building", "亚库比恩大厦", "عمارة يعقوبيان", "Alaa Al Aswany", "阿拉·阿斯万尼", "علاء الأسواني", "2002",
       lang="ar", pd=False, aliases=["Imarat Yaqubian", "Yacoubian", "Zaki Bey", "Suleiman Pasha Street", "Talaat Harb", "Al Aswany"]),
    BK("death-on-the-nile", "Death on the Nile", "尼罗河上的惨案", "Death on the Nile", "Agatha Christie", "阿加莎·克里斯蒂", "Agatha Christie", "1937",
       lang="en", pd=False, aliases=["Poirot", "Karnak", "Linnet Doyle", "Cataract Hotel", "Assuan", "波洛"]),
]

places = [
    ORIG("eg-great-pyramid", "Great Pyramid of Giza", "吉萨大金字塔",
         "The largest of the three pyramids of Giza, built for the Fourth-Dynasty king Khufu (Cheops to the Greeks) in the 26th century BC; it was about 146 m high when new, on a base of about 230 m a side. Herodotus travelled in Egypt in the fifth century BC and wrote down what he was told there about its building. His eight plethra, about 240 m, is close to the real length of a side; the height he gives is not",
         "吉萨三座金字塔中最大的一座，公元前 26 世纪为第四王朝的国王胡夫（希腊人叫他基奥普斯）而建；建成时高约 146 米，底边每边约 230 米。希罗多德公元前 5 世纪到过埃及，把在当地听来的造塔经过记了下来。他说的八普列特隆约合 240 米，和真实的边长相近；他说的高度则不对"),
    ORIG("eg-sphinx", "Great Sphinx of Giza", "吉萨狮身人面像",
         "A lion's body with a king's head, cut from the bedrock below the pyramid of Khafre and generally dated to his reign in the 26th century BC; about 73 m long and 20 m high. Mark Twain rode out from Cairo on a donkey with other passengers of the Quaker City on 5 October 1867 and saw the pyramids and the Sphinx in one day; he spells it 'Sphynx'",
         "狮身、国王头像，就着哈夫拉金字塔下方的岩床凿成，一般认为是公元前 26 世纪哈夫拉在位时所造；长约 73 米，高约 20 米。1867 年 10 月 5 日，马克·吐温和“教友城号”的几位旅伴从开罗骑驴出发，一天之内看了金字塔和狮身人面像；他把它拼作“Sphynx”"),
    ORIG("eg-cavafy-house", "Cavafy House, Alexandria", "卡瓦菲斯故居，亚历山大",
         "The second-floor apartment at 4 C. P. Cavafy Street (10 Rue Lepsius in his day) where Constantine Cavafy lived from 1907 until his death in 1933; a museum since 1992, restored by the Onassis Foundation and reopened on 11 May 2024. Cavafy was born in Alexandria in 1863. The poem, first printed in 1911, takes its title from Plutarch: on the night before Alexandria fell to Octavian in 30 BC, Antony is said to have heard an unseen procession with music leaving the city, the god deserting him",
         "C. P. 卡瓦菲斯街 4 号（当年是莱普修斯街 10 号）二楼的公寓，康斯坦丁·卡瓦菲斯从 1907 年住到 1933 年去世；1992 年起辟为博物馆，经奥纳西斯基金会修复，2024 年 5 月 11 日重新开放。卡瓦菲斯 1863 年生于亚历山大。这首诗 1911 年初次刊出，题目出自普鲁塔克：公元前 30 年亚历山大落入屋大维之手的前夜，传说安东尼听见一支看不见的队伍奏着音乐出城而去，那是神离弃了他"),
    ORIG("eg-ramesseum", "The Ramesseum, Luxor", "拉美西姆祭庙，卢克索",
         "Mortuary temple of Ramesses II on the west bank of the Nile at Thebes. The Greek historian Diodorus Siculus described it as the tomb of Osymandyas, whose statue bore an inscription calling him king of kings; a colossal seated statue of the king lies shattered in its court. In 1816 Giovanni Belzoni took from here, for the British Museum, the bust known as the Younger Memnon. Shelley never went to Egypt; he wrote the sonnet at the end of December 1817 in a friendly competition with Horace Smith, and it appeared in The Examiner on 11 January 1818",
         "拉美西斯二世的祭庙，在底比斯的尼罗河西岸。希腊史家狄奥多罗斯把它写成“奥西曼迪亚斯之墓”，说他的雕像上有铭文自称万王之王；庭院里倒着一尊碎裂的国王巨型坐像。1816 年，乔瓦尼·贝尔佐尼从这里为大英博物馆运走了被称作“小门农”的半身像。雪莱从未到过埃及；1817 年 12 月底，他和霍勒斯·史密斯比赛写十四行诗时写下这首诗，1818 年 1 月 11 日发表在《检查者》周报上",
         region="EG-LX"),
    ORIG("eg-bayn-al-qasrayn", "Bayn al-Qasrayn, Cairo", "宫间街，开罗",
         "The stretch of al-Mu'izz Street in the Gamaliya district of medieval Cairo whose name means 'between the two palaces', after the two Fatimid palaces that once faced each other here; it is now lined with Mamluk monuments such as the complex of Sultan Qalawun. Naguib Mahfouz was born in Gamaliya in 1911 and named the three novels of his Cairo Trilogy after streets of the district; the family of Palace Walk lives on this one",
         "开罗老城贾马利亚区穆伊兹街的一段，街名意思是“两宫之间”，因法蒂玛王朝的东西两座宫殿曾在这里隔街相对而得名；如今街边是盖拉温苏丹建筑群等马穆鲁克时代的古迹。纳吉布·马哈福兹 1911 年生在贾马利亚，他的“开罗三部曲”三部小说都以这一区的街道命名；《宫间街》里的一家人就住在这条街上"),
    ORIG("eg-yacoubian", "Yacoubian Building, Talaat Harb Street, Cairo", "亚库比恩大厦，开罗塔拉特·哈尔卜街",
         "Apartment block at 34 Talaat Harb Street in downtown Cairo, a street Cairenes and the novel still call by its old name, Suleiman Pasha; it is named after its owner, the Armenian businessman Hagop Yacoubian. Alaa Al Aswany, a dentist, had his first clinic in the building. The building of the novel stands at the same address, but its description differs from the real one",
         "开罗市中心塔拉特·哈尔卜街 34 号的公寓楼，开罗人和小说里仍用这条街的旧名苏莱曼帕夏街；楼以业主、亚美尼亚裔商人哈格普·亚库比恩命名。阿拉·阿斯万尼是牙医，他的第一间诊所就开在这栋楼里。小说里的大厦在同一个地址，写出来的样子却和真楼不同"),
    ORIG("eg-old-cataract", "Old Cataract Hotel, Aswan", "老瀑布酒店，阿斯旺",
         "Hotel on a granite bluff above the Nile, facing Elephantine Island, built by Thomas Cook in 1899 and opened in January 1900. Agatha Christie stayed here, and is believed to have written part of Death on the Nile in the hotel; in the novel it is the 'Cataract Hotel at Assuan'",
         "尼罗河边花岗岩高地上的酒店，对着象岛，1899 年由托马斯·库克公司兴建，1900 年 1 月开业。阿加莎·克里斯蒂在这里住过，据信《尼罗河上的惨案》有一部分就是在酒店里写的；小说里它叫“阿斯旺的瀑布酒店”"),
    PIL("eg-mahfouz-museum", "Naguib Mahfouz Museum, Cairo", "纳吉布·马哈福兹博物馆，开罗",
        "Museum in the tekkiyya (dervish lodge) of the complex that Muhammad Bey Abu al-Dhahab built beside al-Azhar Mosque in 1774; opened on 14 July 2019. It holds Mahfouz's belongings and personal library, and stands in Gamaliya, near the house where he was born in 1911. Midaq Alley, the dead-end lane of his 1947 novel, is a real alley in the same old quarter",
        "博物馆设在穆罕默德贝伊·阿布·达哈卜 1774 年在爱资哈尔清真寺旁所建建筑群的苦修院（泰基亚）里，2019 年 7 月 14 日开放。馆内收藏马哈福兹的遗物和私人藏书；这里属贾马利亚区，离他 1911 年出生的房子不远。他 1947 年的小说《梅达格胡同》写的那条死胡同，是同在这片老城里的一条真巷子",
        ["palace-walk", "midaq-alley"]),
]

lines = [
    Q("eg-hd-1", "histories", "eg-great-pyramid", "Book 2, 124", "第二卷第 124 节", T_HD,
      raw(T_HD, once(T_HD, "ἐργάζοντο δὲ κατὰ δέκα μυριάδας", "el"), "τὴν τρίμηνον ἑκάστην.", "el") + "\n…\n"
      + raw(T_HD, once(T_HD, "τῇ δὲ πυραμίδι αὐτῇ χρόνον γενέσθαι", "el"), "τριήκοντα ποδῶν ἐλάσσων.", "el").replace(once(T_HD, "ὀκτὼ. πλέθρα", "el"), "ὀκτὼ πλέθρα"),
      ["πυραμίδι"],
      "They worked a hundred thousand men at a time, each gang for three months.\n…\nThe pyramid itself was twenty years in the making. It is square, each face eight plethra long, and its height is the same; it is of polished stone, most exactly fitted together, and none of the stones is less than thirty feet long.",
      ["pyramid"],
      "他们每十万人一批，每批劳作三个月。\n…\n金字塔本身造了二十年。它是方形的，每一面长八普列特隆，高度也一样；用磨光的石块砌成，接缝极其严密，没有一块石头短于三十尺。",
      ["金字塔"], note=" (the first sentence of 124.3, then 124.5; a full stop that stands after ὀκτὼ on the page left out)", site="Greek"),
    Q("eg-cv-1", "cavafy", "eg-cavafy-house", "'The God Abandons Antony'", "《天神放弃安东尼》", T_CV,
      raw(T_CV, once(T_CV, "Σὰν ἔξαφνα, ὥρα μεσάνυχτ’, ἀκουσθεῖ", "el"), "τὴν Ἀλεξάνδρεια ποῦ χάνεις.", "el"), ["Ἀλεξάνδρεια"],
      "When suddenly, at the midnight hour, you hear\nan invisible company passing by\nwith exquisite music, with voices—\nyour fortune that gives way now, your works\nthat have failed, the plans of your life\nthat all turned out illusions, do not mourn them uselessly.\nAs one long since prepared, as one with courage,\nsay goodbye to her, to the Alexandria that is leaving.\nAbove all do not fool yourself, do not say it was\na dream, that your hearing was deceived;\ndo not stoop to empty hopes like these.\nAs one long since prepared, as one with courage,\nas befits you who were found worthy of such a city,\ngo steadily up to the window\nand listen with feeling, but not\nwith the pleas and complaints of cowards,\nlisten, as a last delight, to the sounds,\nthe exquisite instruments of the mystic company,\nand say goodbye to her, to the Alexandria you are losing.",
      ["Alexandria"],
      "当午夜时分，你忽然听见\n一支看不见的队伍走过，\n伴着美妙的音乐，伴着人声——\n你的运气正在离去，你的事业\n已经失败，你一生的计划\n全都成了幻梦，不要徒然哀叹。\n像早有准备的人，像有勇气的人，\n向她告别吧，向正在离去的亚历山大。\n最要紧的是不要自欺，不要说那是\n一场梦，是你的耳朵听错了；\n不要屈就于这样空洞的希望。\n像早有准备的人，像有勇气的人，\n像配得上这样一座城市的你应当做的那样，\n稳稳地走到窗前，\n带着深情去听，但不要带着\n懦夫的哀求和抱怨，\n把这些声音当作最后的享受来听，\n听那神秘队伍的美妙乐器，\n向她告别吧，向你正在失去的亚历山大。",
      ["亚历山大"], note=" (the whole poem, as printed in Grammata, April 1911)", site="Greek"),
    EN("eg-ia-1", "innocents-abroad", "eg-sphinx", "Chapter 58", "第 58 章", T_IA,
       raw(T_IA, once(T_IA, "After years of waiting, it was before me at last. The great", "en"), "The great", "en") + " "
       + raw(T_IA, once(T_IA, "face was so sad, so earnest", "en"), "and far into the past.", "en") + "\n…\n"
       + raw(T_IA, once(T_IA, "The Sphynx is grand in its loneliness;", "en"), "hangs over its story.", "en"),
       ["Sphynx"],
       "盼了这么多年，它终于在我眼前了。那张巨大的脸是那样悲伤，那样恳切，那样渴望，那样有耐心。它的神态里有一种不属于尘世的庄严，它的面容里有一种任何人脸上都不曾有过的慈和。它是石头，却仿佛有知觉。如果石像也会思想，它就是在思想。它望着地平线的尽头，却什么也没在看——只有远方和虚空。它的目光越过眼前的一切，远远望进过去。\n…\n斯芬克斯因孤独而宏伟，因巨大而威严，因笼罩着它身世的神秘而令人难忘。",
       ["斯芬克斯"], note=" (the caption of a picture, 'PYRAMIDS AND SPHYNX.', which the page sets inside the second sentence, left out; Chinese is our own)"),
    EN("eg-oz-1", "ozymandias", "eg-ramesseum", "The whole poem", "全诗", T_OZ,
       re.sub(r" (5|10)$", "", raw(T_OZ, once(T_OZ, "I met a traveller from an antique land", "en"), "stretch far away.", "en"), flags=re.M).replace(".\xa0.\xa0.", ". . ."),
       ["Ozymandias"],
       "我遇见一位来自古国的旅人，\n他说：有两条巨大的石腿，没有身躯，\n立在沙漠中……近旁的沙土里，\n半埋着一张破碎的脸，那皱起的眉，\n那抿紧的唇，那冷冷发令的轻蔑，\n说明雕刻者深深读懂了那些情欲，\n它们印在这无生命的石头上，至今犹存，\n比摹刻它们的手、滋养它们的心活得更久：\n而基座上刻着这样的字：\n“我是奥兹曼迪亚斯，万王之王：\n强者们，看看我的功业，绝望吧！”\n此外什么也没有留下。在那巨大残骸的\n废墟四周，无边无际，一片荒凉，\n只有寂寞平坦的黄沙伸向远方。",
       ["奥兹曼迪亚斯"], note=" (the edition's line numbers 5 and 10 left out; the no-break spaces in the ellipsis written as plain spaces; Chinese is our own)"),
    S("eg-pw-1", "palace-walk", "eg-bayn-al-qasrayn", "Chapter 1 and the novel as a whole", "第一章及全书",
      "The novel opens at midnight in 1917: Amina wakes to wait for her husband, al-Sayyid Ahmad Abd al-Jawad, and looks out through the wooden lattice of the balcony at the street below, where Bayn al-Qasrayn runs north and al-Nahhasin, the Coppersmiths' street, runs south. She is hardly ever allowed out of the house; he, a shopkeeper who is stern at home, spends his evenings in pleasure. The book follows the family to the revolution of 1919, in which the student son Fahmy is shot dead at a demonstration.",
      "小说从 1917 年的一个午夜开始：艾米娜醒来，等丈夫阿赫麦德·阿卜杜·贾瓦德老爷回家，隔着阳台的木格窗望向楼下的街道——宫间街向北，铜匠街向南。她几乎从不被允许出门；他是个店主，在家里威严，晚上却在外面寻欢作乐。小说一直写到 1919 年革命，还在读书的儿子法赫米在一次示威中中弹身亡。",
      ["Bayn al-Qasrayn"], ["宫间街"], "https://en.wikipedia.org/wiki/Palace_Walk; https://core.ac.uk/download/268163536.pdf"),
    S("eg-yb-1", "yacoubian-building", "eg-yacoubian", "The novel as a whole", "全书",
      "The novel follows the people of the Yacoubian Building on Suleiman Pasha Street around 1990, at the time of the Gulf War: Zaki Bey el Dessouki, an ageing aristocrat who keeps an office there; Hatim Rasheed, a newspaper editor; the businessman Hagg Azzam; and, in the small rooms on the roof, built for storage and now home to poor families, Taha, the doorkeeper's son, who is turned away from the police academy, and Busayna, the girl he hopes to marry.",
      "小说写的是 1990 年前后、海湾战争时期，苏莱曼帕夏街上亚库比恩大厦里的人：在楼里留着一间办公室的没落贵族扎基贝伊·德苏基，报纸主编哈蒂姆·拉希德，商人阿扎姆哈吉；还有楼顶上那些原本用来堆东西、如今住满穷人家的小房间里，被警察学院拒之门外的看门人之子塔哈，和他想娶的姑娘布赛娜。",
      ["Yacoubian Building", "Suleiman Pasha Street"], ["亚库比恩大厦", "苏莱曼帕夏街"],
      "https://en.wikipedia.org/wiki/The_Yacoubian_Building; https://en.wikipedia.org/wiki/Yacoubian_Building_(Cairo)"),
    S("eg-dn-1", "death-on-the-nile", "eg-old-cataract", "Part 2, 'Egypt'", "第二部“埃及”",
      "The Egyptian part of the novel opens outside the Cataract Hotel at Assuan. Here Hercule Poirot, on holiday, meets the heiress Linnet Doyle, on honeymoon with her husband Simon and followed everywhere by Jacqueline de Bellefort, once her friend and his fiancée. The party goes on up the Nile towards Wadi Halfa on the steamer Karnak, and on board Linnet is found shot dead.",
      "小说的埃及部分从阿斯旺的瀑布酒店门外写起。来度假的赫尔克里·波洛在这里遇见女继承人琳内特·多伊尔；她正和丈夫西蒙度蜜月，而她昔日的好友、西蒙从前的未婚妻杰奎琳·德贝尔福一路紧跟着他们。一行人乘“卡纳克号”汽船沿尼罗河上行，驶向瓦迪哈勒法，琳内特在船上被人开枪打死。",
      ["Cataract Hotel"], ["瀑布酒店"],
      "https://www.smithsonianmag.com/history/how-agatha-christies-love-of-archaeology-influenced-death-on-the-nile-180979544/; https://en.wikipedia.org/wiki/Death_on_the_Nile"),
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

HEAD = "// Egypt, hand-written content (tools/content/batches/add_eg1.py, 2026-11-24).\n"
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
