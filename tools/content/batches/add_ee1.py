"""11-25: Estonia, the 10 books that selection rule v2 adds under the user's narrower rule for Estonia (only the top 10
of the 2026 National Library survey; tools/selection/ee.md). Estonia opens with this batch.
Three books are out of copyright and get quotations cut from Estonian Wikisource (translations are our own drafts):
Truth and Justice I (1926; Wikisource follows the 1974 Eesti Raamat edition), Spring (1912 first edition) and
Kalevipoeg (1961 edition). The others are in copyright and get scene notes in our own words. Places, with the reason for each:
- Vargamäe: Tammsaare's birthplace farm, now the A. H. Tammsaare Museum; trails lead from it to the novel's places.
- Palamuse (prototype): Paunvere of Spring is an invented village that closely resembles Luts's home, Palamuse.
- Iru ämm: in canto III of Kalevipoeg, Linda is turned to stone on Iru hill; a sculpture has stood in place of the lost
  boulder since 1970.
- Tallinn (city-level pin): The Man Who Spoke Snakish names no place; Kivirähk was born in Tallinn (A-24).
- Võisiku manor: the estate of Timotheus von Bock, hero of The Czar's Madman.
- Kaali crater: one of the threads of Silverwhite.
- Tartu (city-level pin): Sipsik and Three Jolly Fellows name no town; Eno Raud was born in Tartu (A-24).
- Tänassilma: Viivi Luik's birthplace. The Seventh Spring of Peace draws on her childhood in Viljandi County; its village
  is not named (A-24).
- Estonian Open Air Museum (film location): November (2017), the film of Old Barny, was shot there among other places;
  the novel's village and manor have no names, so Old Barny has no line.
Usage: python3 -I tools/content/batches/add_ee1.py <app_dir> tools/content/batches/coords/add_ee1.json <wikisource_dir>"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b
import wikisource as ws

APP, CO, WSR = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8")), sys.argv[3]
DATE = "2026-11-25"
b.init(APP, "", "ee", DATE)
def C(pid):
    c = CO[pid]; return c["lat"], c["lon"], c["st"], c["su"]
def BK(id, title, title_zh, title_orig, author, author_zh, year, aliases, pd=False, src=None):
    return dict(id=id, title=title, title_zh=title_zh, title_orig=title_orig, author=author, author_zh=author_zh, year=year,
                orig_lang="et", public_domain=pd, source_url=src, aliases=aliases)
def Q(id, book, place, loc, loc_zh, title, edition, orig, hl_orig, en, hl_en, zh, hl_zh):
    for text, hls in ((orig, hl_orig), (en, hl_en), (zh, hl_zh)):
        for h in hls:
            assert h in text, (id, h)
    assert "[" not in orig and "\xa0" not in orig and "  " not in orig, (id, "page mark or odd space")
    return dict(id=id, book_id=book, place_ids=[place], location=loc, location_zh=loc_zh,
                text_orig=orig, highlight_orig=hl_orig, text_en=en, highlight_en=hl_en, text_zh=zh, highlight_zh=hl_zh,
                translation="own", status="draft", checked=f"Estonian Wikisource, {title} ({edition}), {DATE}")
WS = "https://et.wikisource.org/wiki/"

books = [
    BK("tode-ja-oigus", "Truth and Justice", "真理与正义", "Tõde ja õigus", "A. H. Tammsaare", "A. H. 塔姆萨雷", "1926",
       ["Tõde ja õigus", "Vargamäe", "Andres Paas"], pd=True, src=WS + "Tõde_ja_õigus_I"),
    BK("kevade-luts", "Spring", "春天", "Kevade", "Oskar Luts", "奥斯卡·卢茨", "1912", ["Kevade", "Paunvere", "Arno Tali", "Toots"],
       pd=True, src=WS + "Kevade_I"),
    BK("kalevipoeg", "Kalevipoeg", "卡列维波埃格", "Kalevipoeg", "Friedrich Reinhold Kreutzwald", "弗里德里希·莱因霍尔德·克罗伊茨瓦尔德",
       "1857", ["Kalevipoeg", "Linda", "Kalev's son"], pd=True, src=WS + "Kalevipoeg"),
    BK("rehepapp", "Old Barny, or November", "谷仓老汉，又名十一月", "Rehepapp ehk November", "Andrus Kivirähk", "安德鲁斯·基维拉赫克", "2000",
       ["Rehepapp", "Rehepapp ehk November", "Old Barny", "November"]),
    BK("sipsik", "Sipsik", "布娃娃西普西克", "Sipsik", "Eno Raud", "埃诺·劳德", "1962", ["Sipsik", "Raggie"]),
    BK("naksitrallid", "Three Jolly Fellows", "三个快活的小人儿", "Naksitrallid", "Eno Raud", "埃诺·劳德", "1972",
       ["Naksitrallid", "Muhv", "Kingpool", "Sammalhabe", "Muff, Halfshoe and Mossbeard"]),
    BK("mees-kes-teadis-ussisonu", "The Man Who Spoke Snakish", "懂蛇语的人", "Mees, kes teadis ussisõnu", "Andrus Kivirähk", "安德鲁斯·基维拉赫克",
       "2007", ["Mees, kes teadis ussisõnu", "Leemet"]),
    BK("seitsmes-rahukevad", "The Seventh Spring of Peace", "和平的第七个春天", "Seitsmes rahukevad", "Viivi Luik", "维维·卢伊克", "1985",
       ["Seitsmes rahukevad"]),
    BK("keisri-hull", "The Czar's Madman", "沙皇的疯子", "Keisri hull", "Jaan Kross", "扬·克罗斯", "1978", ["Keisri hull", "Timotheus von Bock"]),
    BK("hobevalge", "Silverwhite", "银白", "Hõbevalge", "Lennart Meri", "伦纳特·梅里", "1976", ["Hõbevalge"]),
]

def film(pid, name, zh, ids, en_scene, zh_scene):
    return b.P(pid, name, zh, *C(pid), "film_location", adaptation={"title": "November", "year": 2017, "kind": "电影"},
               scene=zh_scene, book_ids=ids, scene_en=en_scene)

places = [
    b.PROTO("ee-vargamae", "Vargamäe (A. H. Tammsaare Museum)", "瓦尔加梅（塔姆萨雷博物馆）", *C("ee-vargamae"),
        "Vargamäe, the farm on a hill among the bogs in Truth and Justice, is drawn from Tammsaare's birthplace, the Tammsaare-Põhja farm in Järva County (the writer's name comes from the farm's). The farm is now the A. H. Tammsaare Museum, and trails from it lead to the places of the novel",
        "《真理与正义》里沼泽环绕的山丘农庄瓦尔加梅，取材于塔姆萨雷的出生地——耶尔瓦县的塔姆萨雷-北农庄（作家的笔名就来自农庄的名字）。农庄如今是 A. H. 塔姆萨雷博物馆，从这里出发的步道通往小说里的各处地方"),
    b.PROTO("ee-palamuse", "Palamuse", "帕拉穆塞", *C("ee-palamuse"),
        "Paunvere, the village of Spring and the other Toots stories, is invented, but it closely resembles Oskar Luts's home, Palamuse. The parish school building of 1873, where the school ran until 1975, is now the O. Luts Parish School Museum, which shows the life of a late-19th-century parish school through Spring",
        "《春天》和其他托茨故事里的保恩韦雷是虚构的村镇，但和奥斯卡·卢茨的家乡帕拉穆塞非常相像。1873 年建成的教区学校校舍一直用到 1975 年，如今是 O. 卢茨教区学校博物馆，借《春天》展示 19 世纪末教区学校的生活"),
    b.ORIG("ee-iru-amm", "Iru ämm, Iru hill", "伊鲁山的伊鲁老奶奶", *C("ee-iru-amm"),
        "Iru ämm, the 'Granny of Iru', was an elongated boulder on Iru hill near the Pirita River, venerated in old times. It was destroyed in the mid-19th century by careless Midsummer bonfires, and its pieces went into the Iru bridge in 1865–1867; since 1970 a stone sculpture by Juhan Raudsepp has stood in its place. In the third canto of Kalevipoeg, the widow Linda is turned to stone here",
        "“伊鲁老奶奶”原是皮里塔河边伊鲁山上的一块长条巨石，古时受人敬拜。19 世纪中叶，人们在旁边随意点篝火过仲夏节，把它毁了，碎块在 1865—1867 年修伊鲁桥时用掉；1970 年起，原地立着尤汉·劳德塞普雕刻的一座石像。《卡列维波埃格》第三章里，寡妇琳达就在这里变成了石头"),
    b.ORIG("ee-tallinn", "Tallinn", "塔林", *C("ee-tallinn"),
        "The capital of Estonia. Andrus Kivirähk's The Man Who Spoke Snakish names no place; Kivirähk was born in Tallinn, so it is pinned here",
        "爱沙尼亚首都。安德鲁斯·基维拉赫克的《懂蛇语的人》不写任何地名；基维拉赫克生在塔林，所以挂在这里"),
    b.ORIG("ee-voisiku", "Võisiku manor", "沃伊西库庄园", *C("ee-voisiku"),
        "A knight's manor (German Woiseck) in the old parish of Kolga-Jaani, now in Põltsamaa rural municipality. In the early 19th century it belonged to Timotheus Eberhard von Bock, the hero of Jaan Kross's The Czar's Madman. The one-storey main house was built in the 1750s–1760s; since 1925 it has housed a home for the elderly, today a care home",
        "旧时科尔加-亚尼教区的一座骑士庄园（德语叫沃伊塞克），如今属于珀尔察马乡。19 世纪初，它的主人是蒂莫特乌斯·埃贝哈德·冯·博克，扬·克罗斯《沙皇的疯子》的主人公。一层的主楼建于 18 世纪 50—60 年代；1925 年起这里是收容老人的地方，今天是一家护理院"),
    b.ORIG("ee-kaali", "Kaali crater, Saaremaa", "萨雷马岛的卡利陨石坑", *C("ee-kaali"),
        "A meteorite crater 110 metres across, with eight smaller craters around it, 20 km north-east of Kuressaare on Saaremaa; the latest measurements date it to about 1530–1450 BC. The Kaali impact and what it may have meant for the myths of Europe is one of the threads of Lennart Meri's Silverwhite",
        "萨雷马岛上库雷萨雷东北 20 公里处的陨石坑，主坑直径 110 米，周围还有八个小坑；最新的测量把它的形成年代定在约公元前 1530—前 1450 年。卡利陨石撞击，以及它可能给欧洲神话留下的影响，是伦纳特·梅里《银白》的线索之一"),
    b.ORIG("ee-tartu", "Tartu", "塔尔图", *C("ee-tartu"),
        "Estonia's university town. Eno Raud, the author of Sipsik and Three Jolly Fellows, was born here in 1928; those books name no town, so they are pinned here",
        "爱沙尼亚的大学城。《布娃娃西普西克》和《三个快活的小人儿》的作者埃诺·劳德 1928 年生在这里；这两部书不写是哪座城，所以挂在这里"),
    b.ORIG("ee-tanassilma", "Tänassilma", "塔纳西尔马", *C("ee-tanassilma"),
        "A village 15 km east of Viljandi, where Viivi Luik was born in 1946. Her autobiographical novel The Seventh Spring of Peace draws on her childhood in Viljandi County; its village is not named, so the novel is pinned to her birthplace",
        "维尔扬迪以东 15 公里的村子，维维·卢伊克 1946 年生在这里。她的自传体小说《和平的第七个春天》取材于她在维尔扬迪县的童年；小说里的村子没有名字，所以挂在她的出生地"),
    film("ee-open-air-museum", "Estonian Open Air Museum, Rocca al Mare", "罗卡阿尔马雷的爱沙尼亚露天博物馆", ["rehepapp"],
        "Rainer Sarnet's black-and-white film November (2017), made from Kivirähk's Old Barny, was shot over sixteen months in many corners of Estonia; scenes were filmed at the Estonian Open Air Museum at Rocca al Mare, among them at its Roosta farm, while Malla manor stood in for the manor's exterior and Kolga manor for its rooms. The novel, told in thirty chapters from the first to the thirtieth of November, is set in a 19th-century Estonian village and manor where kratts, werewolves, the Plague and the Devil are part of everyday life; the village girl Liina loves Hans, the manor's bailiff, who loves the baron's young daughter.",
        "赖纳·萨尔内特 2017 年把基维拉赫克的《谷仓老汉》拍成黑白电影《十一月》，花了十六个月，几乎走遍爱沙尼亚各地；其中一部分在罗卡阿尔马雷的爱沙尼亚露天博物馆拍摄，包括博物馆里的罗斯塔农庄，马拉庄园演庄园的外景，科尔加庄园演庄园的内景。小说分三十章，从 11 月 1 日写到 11 月 30 日，背景是 19 世纪爱沙尼亚的一个村子和庄园，克拉特、狼人、瘟疫和魔鬼都是日常生活的一部分；村姑莉娜爱着庄园的监工汉斯，汉斯却爱上了男爵家年轻的小姐。"),
]

lines = [
    Q("ee-to-1", "tode-ja-oigus", "ee-vargamae", "Part I, chapter I", "第一部第一章", "Tõde ja õigus I/I", "1974 Eesti Raamat edition",
      ws.cut(WSR, "Tõde ja õigus I/I", "„Seal ta ongi, see Vargamäe,“", "poolkuivad juba.“"), ["Vargamäe"],
      "'There it is, that's Vargamäe,' said the man, pointing across the bog to the next hill, where a cluster of low buildings crouched. 'Our buildings you can see; the others stand behind the hill, in the hollow, so folk call them Mäe and Oru, Hill and Hollow, though in the manor's books they are Eespere and Tagapere. That clump of pines on the right, high up at the end of the hill, is ours: everlasting old gnarled things, some of them half dead already.'",
      ["Vargamäe"],
      "“那就是了，那就是瓦尔加梅。”男人说，抬手指向沼泽对面的下一座山丘，那里蹲着一片低矮的房子。“我们的房子看得见，别人家的在山后的洼地里，所以老百姓管它们叫‘山上’和‘洼地’，庄园的账簿上却写作‘前庄’和‘后庄’。右手边山顶高处那片松树是我们的：一棵棵老掉牙的歪脖子树，有几棵已经半枯了。”",
      ["瓦尔加梅"]),
    Q("ee-ke-1", "kevade-luts", "ee-palamuse", "Part I, chapter XII", "第一部第十二章", "Kevade I/XII", "1912 first edition",
      ws.cut(WSR, "Kevade I/XII", "Ja nüüd taheti teda lahti lasta", "arwanud olewat."), ["Paunwere"],
      "And now they meant to dismiss him, more, of course, for the denying than for the misdeed itself, for Kristjan Lible had got up to plenty of mischief at the Paunvere parsonage before and had always got off with a whole skin, by saying that of course it was he who had done it, and had done it because he had thought it better so.",
      ["Paunvere"],
      "现在他们要辞退他，当然更多是因为他不认账，而不是因为那件坏事本身；因为克里斯蒂安·利布莱在保恩韦雷的牧师庄园里早就干过不少荒唐事，可每次都毫发无损地过了关——他总是说，当然是他干的，而且他这么干，是因为他觉得这样更好。",
      ["保恩韦雷"]),
    Q("ee-ka-1", "kalevipoeg", "ee-iru-amm", "Canto III", "第三章", "Kalevipoeg/III", "1961 edition",
      ws.block(WSR, "Kalevipoeg/III", "Kaljuks moondud kodukana,", "Poisid kübara panema.", number=r"\d{2,4}"), ["Iru mäe", "Iru ämma"],
      "The hen of the home turned to rock,\nLinda, the widow of the Kalevs,\nyou may witness to this day,\nsee her plainly with your eyes.\nOn Iru hill the widow sits,\nthe daughter hatched from a grouse's egg,\nLinda sits beside the highway,\nas those who go to town well know,\nthough the children of this age,\nin the dullness of these days,\nhave let Linda's name slip from mind.\nThe people call the block of stone\nmostly the Granny of Iru.\nThose who go to town the first time\nmust, after the old custom,\ngreet the Granny of Iru,\nand in honour of the granny\nboys must set a hat upon her head.",
      ["Iru hill", "Granny of Iru"],
      "化作岩石的家中母鸡，\n卡列夫家的寡妇琳达，\n今天你们还能作证，\n亲眼清清楚楚看见。\n寡妇坐在伊鲁山上，\n那松鸡蛋里孵出的女儿，\n琳达坐在大路旁边，\n进城的人都知道，\n虽然这一代的孩子们，\n在如今的麻木里，\n早把琳达的名字忘了。\n人们管这块大石头\n大多叫“伊鲁老奶奶”。\n第一次进城的人\n按照古老的规矩\n要向伊鲁老奶奶问好，\n为了表示敬意，\n小伙子们要把帽子戴在老奶奶头上。",
      ["伊鲁山", "伊鲁老奶奶"]),
    b.S("ee-us-1", "mees-kes-teadis-ussisonu", "ee-tallinn", "The last man", "最后一个人",
        "In a fantastical thirteenth-century Estonia of the Northern Crusades, Leemet is one of the last Estonians who still live in the forest, hunting and keeping the old faith in sacred groves. As a boy he learns Snakish from his uncle Vootele: the ancient language that snakes taught humans, which lets its speakers understand and command most animals. One by one the forest people leave for the villages, for farming and for Christianity, alongside the iron men and the monks, until Leemet is the last man who knows the snake words. The forest and its village have no names; Andrus Kivirähk was born in Tallinn, so the novel is pinned here.",
        "在一个幻想出来的、北方十字军时代的 13 世纪爱沙尼亚，莱梅特是最后几个仍住在森林里的爱沙尼亚人之一，他们打猎为生，在神圣的树林里守着古老的信仰。小时候，他跟舅舅沃泰勒学会了蛇语：那是蛇教给人类的古老语言，会说的人能听懂并驱使大多数动物。森林里的人一个个搬进村子，种地、信基督教，和铁甲骑士、僧侣们生活在一起，最后莱梅特成了最后一个懂蛇语的人。森林和村子都没有名字；安德鲁斯·基维拉赫克生在塔林，所以挂在这里。",
        ["Tallinn"], ["塔林"],
        "https://en.wikipedia.org/wiki/The_Man_Who_Spoke_Snakish; https://et.wikipedia.org/wiki/Mees,_kes_teadis_ussisõnu; https://en.wikipedia.org/wiki/Andrus_Kivirähk"),
    b.S("ee-kh-1", "keisri-hull", "ee-voisiku", "Timo and Eeva", "蒂莫与埃娃",
        "Timotheus Eberhard von Bock (1787–1836), lord of Võisiku manor in Livonia, is a friend of Emperor Alexander I, admired for his learning and his courage in battle. He shocks the nobility by turning down a brilliant match, a natural daughter of the emperor, and marrying Eeva, a girl from among the serfs. For a letter he writes to the Czar he is imprisoned for nine years, then released to house arrest as a 'madman'. The story is told in the diary of Eeva's brother Jakob; Kross built it on the real diary of Jakob Mättik, and Bock and most of the people in it really lived.",
        "蒂莫特乌斯·埃贝哈德·冯·博克（1787—1836）是利沃尼亚沃伊西库庄园的主人，学识出众、作战英勇，是沙皇亚历山大一世的朋友。他回绝了一门显赫的亲事——沙皇的私生女，转而娶了农奴中的姑娘埃娃，让贵族圈子大为震惊。他因为给沙皇写了一封信坐了九年牢，出狱后又以“疯子”的名义被软禁。故事借埃娃的哥哥雅各布的日记讲出来；克罗斯依据的是雅各布·梅蒂克真实的日记，博克和书里大多数人物都确有其人。",
        ["Võisiku"], ["沃伊西库"],
        "https://et.wikipedia.org/wiki/Keisri_hull; https://en.wikipedia.org/wiki/The_Czar%27s_Madman; https://et.wikipedia.org/wiki/Võisiku_mõis"),
    b.S("ee-hv-1", "hobevalge", "ee-kaali", "The Kaali meteorite", "卡利陨石",
        "Silverwhite calls itself 'a travelogue of the wind and of ancient poetry', but there is almost no travelling in it: it is a half-scholarly, imaginative meditation on the past of the Estonians and the other Baltic Finns, built largely from folk songs and customs. One of its threads is the Kaali meteorite on Saaremaa. Lennart Meri ties the impact to the explorations and world descriptions of antiquity, hears its echo in the Greek myth of Phaethon's sun chariot falling to earth, and proposes that the Thule of the Greek traveller Pytheas was Saaremaa; these ideas became popular, though scholars dispute them. The title refers to the old Estonian custom of offering silver scrapings, 'silverwhite', to springs.",
        "《银白》的副标题是“关于风和古代诗歌的游记”，书里却几乎没有旅行：这是一部半学术、充满想象的著作，主要借民歌和习俗来思索爱沙尼亚人和其他波罗的海芬兰人的过去。贯穿全书的线索之一，是萨雷马岛上的卡利陨石。伦纳特·梅里把这次撞击同古代的地理发现和对世界的描述联系起来，认为希腊神话里法厄同的太阳车坠落人间就是它的回声，又提出希腊旅行家皮提亚斯写到的图勒就是萨雷马岛；这些说法在民间很流行，学界却有争议。书名指的是爱沙尼亚人往泉水里献祭银屑的古老风俗，这银屑就叫“银白”。",
        ["Kaali"], ["卡利"],
        "https://et.wikipedia.org/wiki/Hõbevalge; https://et.wikipedia.org/wiki/Kaali_kraater"),
    b.S("ee-si-1", "sipsik", "ee-tartu", "Anu's birthday", "安努的生日",
        "Mart starts making a doll for Anu's birthday: on the first day the body, on the second the head, on the third two arms, on the fourth two legs, and then he sews it all together. The doll gets a big shock of black hair, a laughing face with big eyes and a blue-and-white striped suit, and becomes Sipsik. The models for the children Mart and Anu were Eno Raud himself and his sister Anu Raud. The book names no town, so it is pinned to Tartu, where Raud was born in 1928.",
        "马特开始给安努做一个布娃娃当生日礼物：第一天做身子，第二天做头，第三天做两只胳膊，第四天做两条腿，然后把它们都缝到一起。娃娃有一大蓬黑头发、一张大眼睛的笑脸，穿着蓝白条纹的衣服，它就是西普西克。书里两个孩子马特和安努的原型，就是埃诺·劳德自己和他的妹妹安努·劳德。书里没写是哪座城，所以挂在劳德 1928 年出生的塔尔图。",
        ["Tartu"], ["塔尔图"],
        "https://et.wikipedia.org/wiki/Sipsik; https://et.wikipedia.org/wiki/Eno_Raud"),
    b.S("ee-na-1", "naksitrallid", "ee-tartu", "At the ice-cream kiosk", "冰淇淋亭旁",
        "Three odd little men meet by chance at an ice-cream kiosk: Mossbeard, whose beard of soft moss grows last summer's lingonberries; Halfshoe, who has cut the toes off his shoes so that he can wiggle his toes; and Muff, who wears a big muff instead of ordinary clothes. Halfshoe and Mossbeard have always roamed with no home, and Muff has a van, so they join up and travel round Estonia in it, a moving home for all three. The books are about the balance of nature. The roads they travel have no names, so the book is pinned to Tartu, where Eno Raud was born.",
        "三个古怪的小人儿在冰淇淋亭旁偶然碰到一起：苔藓胡子的胡子是软软的苔藓，上面长着去年夏天的越橘；半只鞋把鞋尖剪掉了，好让脚趾活动自在；穆夫不穿普通衣服，身上套着一个大暖手筒。半只鞋和苔藓胡子一直无家可归地四处流浪，穆夫有一辆厢式货车，于是三个人结伴，开着车在爱沙尼亚漫游，车就是他们共同的流动的家。这套书讲的是大自然的平衡。他们走过的路没有地名，所以挂在埃诺·劳德的出生地塔尔图。",
        ["Tartu"], ["塔尔图"],
        "https://www.goodreads.com/book/show/2749067; https://estinst.ee/wp-content/uploads/2022/01/Naksitrallid_eesti-keeles.pdf; https://et.wikipedia.org/wiki/Naksitrallid"),
    b.S("ee-sr-1", "seitsmes-rahukevad", "ee-tanassilma", "August 1950 to spring 1951", "1950 年 8 月到 1951 年春",
        "The Seventh Spring of Peace is an autobiographical novel built on Viivi Luik's memories of her childhood in Viljandi County. Its narrator is a child of almost five, through whose eyes it shows everyday life in a Soviet Estonian village in the early 1950s, from August 1950 to the early spring of 1951; the present is broken by the child's visions of the future, by looks back from the 1980s, and by many lines of verse. Luik was born in 1946 in Tänassilma, east of Viljandi. The village of the novel is not named, so it is pinned to her birthplace.",
        "《和平的第七个春天》是一部自传体小说，取材于维维·卢伊克在维尔扬迪县度过的童年。叙述者是一个快满五岁的孩子，小说借她的眼睛写 20 世纪 50 年代初一个苏维埃爱沙尼亚村庄的日常生活，时间从 1950 年 8 月到 1951 年早春；眼前的描写中不时穿插孩子对未来的幻想、从 80 年代回望的片段，还夹着许多诗句。卢伊克 1946 年生在维尔扬迪以东的塔纳西尔马。小说里的村子没有名字，所以挂在她的出生地。",
        ["Tänassilma"], ["塔纳西尔马"],
        "https://et.wikipedia.org/wiki/Seitsmes_rahukevad; https://et.wikipedia.org/wiki/Viivi_Luik; https://et.wikipedia.org/wiki/Tänassilma"),
]

def ids_in(path): return set(re.findall(r'\{ id: "([^"]+)"', open(path, encoding="utf-8").read()))
all_books = set()
for f in glob.glob(os.path.join(APP, "data", "*", "books.js")):
    all_books |= ids_in(f)
new_b, new_p = {x["id"] for x in books}, {x["id"] for x in places}
assert len(books) == 10 and len(new_b) == 10
assert not new_b & all_books, new_b & all_books
assert new_p == set(CO), new_p ^ set(CO)
line_places = {p["id"] for p in places if p["place_type"] != "film_location"}
for l in lines:
    assert l["book_id"] in new_b and l["place_ids"][0] in line_places, l["id"]
linked = {l["book_id"] for l in lines} | {x for p in places for x in p.get("book_ids", [])}
assert linked == new_b, new_b ^ linked
assert {l["place_ids"][0] for l in lines} | {p["id"] for p in places if p.get("book_ids")} == new_p

HEAD = "// Estonia, hand-written content (tools/content/batches/add_ee1.py, 2026-11-25).\n"
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
    print(len(books), "books,", len(places), "places,", len(lines), "lines")
