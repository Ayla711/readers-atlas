"""11-26: Belarus, the 8 books the user chose: the literary works in the top 10 of either list of the 2016 vote on the
most important Belarusian books of 500 years (experts' top 50, internet users' top 20; tools/selection/by.md).
Belarus opens with this batch. Five of the eight were published before 1931 and are in the public domain, so they get
quotations, cut from Wikisource and translated by us; the three in copyright get scene notes in our own words.
Places, with the reason for each:
- Orsha (pilgrimage): Karatkievic's birthplace, with his museum; Ears of Rye beneath Your Sickle is set on invented
  Dnieper estates, and its young master rides between Suchodol, Mahiliou and Orsha (scene note).
- Karanioŭka (prototype): the village held to be the prototype of Kurani in People of the Marsh, a few kilometres from
  Melež's native Hlinišča (scene note).
- Byčki (pilgrimage): Bykaŭ's native village, now his museum-estate; the collectivization of The Sign of Misfortune was
  drawn from what he saw there as a child (scene note).
- Lastok (prototype): the forester's lodge that The New Land calls Parečča (quotation, 1923 edition).
- Belavezha Forest: The Song of the Bison names only "the Lithuanian forests"; Belavezha, the royal hunting forest where
  the bison lived on longest, is the nearest real place (quotation, editio princeps 1523).
- Polotsk: the sketch "Połock" in Szlachcic Zawalnia (quotation, Petersburg 1844).
- Slutsk: "The Weavers of Slutsk" in The Wreath (quotation, Vilnius 1914).
- Kušlany (pilgrimage): Bahuševič's estate and museum; The Belarusian Fife has no single place.
The map of Belarus (data/by/geo.js) is built from Natural Earth admin-1: 6 regions and the city of Minsk.
Usage: python3 -I tools/content/batches/add_by1.py <app_dir> tools/content/batches/coords/add_by1.json <wikisource_dir>"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b
import wikisource as ws

APP, CO, WSR = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8")), sys.argv[3]
DATE = "2026-11-26"
b.init(APP, "", "by", DATE)
def C(pid):
    c = CO[pid]; return c["lat"], c["lon"], c["st"], c["su"]
def BK(id, title, title_zh, title_orig, author, author_zh, year, aliases, lang="be", pd=False, src=None):
    return dict(id=id, title=title, title_zh=title_zh, title_orig=title_orig, author=author, author_zh=author_zh, year=year,
                orig_lang=lang, public_domain=pd, source_url=src, aliases=aliases)
def Q(id, book, place, loc, loc_zh, source, orig, hl_orig, en, hl_en, zh, hl_zh):
    for text, hls in ((orig, hl_orig), (en, hl_en), (zh, hl_zh)):
        for h in hls:
            assert h in text, (id, h)
    assert "[" not in orig and "\xa0" not in orig and "  " not in orig, (id, "page mark or odd space")
    return dict(id=id, book_id=book, place_ids=[place], location=loc, location_zh=loc_zh,
                text_orig=orig, highlight_orig=hl_orig, text_en=en, highlight_en=hl_en, text_zh=zh, highlight_zh=hl_zh,
                translation="own", status="draft", checked=f"{source}, {DATE}")
BE, PL, LA = "https://be.wikisource.org/wiki/", "https://pl.wikisource.org/wiki/", "https://la.wikisource.org/wiki/"

books = [
    BK("kalasy-pad-siarpom-tvaim", "Ears of Rye beneath Your Sickle", "你镰刀下的麦穗", "Каласы пад сярпом тваім", "Uladzimir Karatkievič",
       "乌拉济米尔·卡拉特克维奇", "1965", ["Каласы пад сярпом тваім", "Колосья под серпом твоим", "Ales Zahorski", "Алесь Загорскі"]),
    BK("liudzi-na-balocie", "People of the Marsh", "沼泽地的人们", "Людзі на балоце", "Ivan Mielež", "伊万·梅列日", "1962",
       ["Людзі на балоце", "Люди на болоте", "Палеская хроніка", "Polesie Chronicle", "Kurani", "Курані"]),
    BK("znak-biady", "The Sign of Misfortune", "灾难的征兆", "Знак бяды", "Vasil Bykaŭ", "瓦西里·贝科夫", "1982",
       ["Знак бяды", "Знак беды", "Stsiapanida", "Сцепаніда"]),
    BK("novaja-ziamlia", "The New Land", "新的土地", "Новая зямля", "Jakub Kolas", "雅库布·科拉斯", "1923",
       ["Новая зямля", "Новая земля", "Парэчча", "Michal"], pd=True, src=BE + "Новая_зямля_(1923)"),
    BK("piesnia-pra-zubra", "The Song of the Bison", "野牛之歌", "Carmen de statura, feritate ac venatione bisontis", "Mikola Husoŭski",
       "米科拉·古索夫斯基", "1523", ["Песня пра зубра", "Carmen de bisonte", "Nicolaus Hussovianus", "Mikołaj Hussowski"],
       lang="la", pd=True, src=LA + "Carmen_de_statura_feritate_ac_venatione_bisontis"),
    BK("sliachcic-zavalnia", "Squire Zavalnia", "地主扎瓦利尼亚", "Szlachcic Zawalnia, czyli Białoruś w fantastycznych opowiadaniach",
       "Jan Barščeŭski", "扬·巴尔舍夫斯基", "1844", ["Шляхціц Завальня", "Szlachcic Zawalnia", "Jan Barszczewski"],
       lang="pl", pd=True, src=PL + "Szlachcic_Zawalnia_czyli_Białoruś"),
    BK("vianok", "The Wreath", "花冠", "Вянок", "Maksim Bahdanovič", "马克西姆·博格达诺维奇", "1913",
       ["Вянок", "Венок", "Слуцкія ткачыхі", "The Weavers of Slutsk"], pd=True, src=BE + "Вянок_(1914)"),
    BK("dudka-bielaruskaja", "The Belarusian Fife", "白俄罗斯芦笛", "Дудка беларуская", "Francišak Bahuševič", "弗朗齐舍克·博古舍维奇", "1891",
       ["Дудка беларуская", "Dudka białaruskaja", "Мацей Бурачок", "Maciej Buraczok"], pd=True, src=BE + "Dudka_białaruskaja_(1891)"),
]

places = [
    b.PIL("by-orsha-karatkievich", "Karatkievič Museum, Orsha", "奥尔沙的卡拉特克维奇博物馆", *C("by-orsha-karatkievich"),
        "Uladzimir Karatkievič (1930–1984) was born in Orsha, on the Dnieper. The early twentieth-century house at 26 Lenin Street now houses the Uladzimir Karatkievič Museum. His Ears of Rye beneath Your Sickle came first in the internet users' vote of 2016 on the most important Belarusian books of 500 years",
        "乌拉济米尔·卡拉特克维奇（1930—1984）生在第聂伯河边的奥尔沙。列宁街 26 号这座 20 世纪初的房子，如今是乌拉济米尔·卡拉特克维奇博物馆。他的《你镰刀下的麦穗》在 2016 年“500 年来最有分量的白俄罗斯书”网民投票中排第一",
        ["kalasy-pad-siarpom-tvaim"]),
    b.PROTO("by-karanioka", "Karanioŭka", "卡拉尼奥夫卡", *C("by-karanioka"),
        "Kurani, the Palesse village of People of the Marsh: Karanioŭka, a village of the Chojniki district among drainage canals that run to the Prypiać, a few kilometres from Ivan Melež's native Hlinišča, is held to be its prototype",
        "《沼泽地的人们》里的波列西耶村庄库拉尼：霍伊尼基区的卡拉尼奥夫卡被认为是它的原型。村子四周是通往普里皮亚季河的排水渠，离伊万·梅列日的家乡赫利尼什恰只有几公里"),
    b.PIL("by-bychki", "Vasil Bykaŭ Museum-Estate, Byčki", "贝奇基的瓦西里·贝科夫故居博物馆", *C("by-bychki"),
        "Vasil Bykaŭ (1924–2003) was born in the village of Byčki, Ušačy district. His family's farmstead, with the house, cowshed, barn and fence rebuilt, has been a museum since 2004, a branch of the Ušačy museum",
        "瓦西里·贝科夫（1924—2003）生在乌沙奇区的贝奇基村。他家的农舍——房子、牛棚、干草棚和篱笆都重建了——2004 年起是一座博物馆，属于乌沙奇的博物馆",
        ["znak-biady"]),
    b.PROTO("by-lastok", "Lastok", "拉斯托克", *C("by-lastok"),
        "Parečča, the forester's lodge in The New Land: Kolas changed the name; in reality the lodge where his family lived was Lastok, in the Stoŭbcy district, now a memorial estate of Jakub Kolas and the only one that survives almost in its original state",
        "《新的土地》里的护林人小屋帕雷奇恰：科拉斯改了名字，他家住过的那座护林人小屋其实叫拉斯托克，在斯托夫布齐区，如今是雅库布·科拉斯的纪念庄园，也是他几处纪念庄园里唯一几乎保持原样的一处"),
    b.ORIG("by-belavezha", "Belavezha Forest", "别洛韦日森林", *C("by-belavezha"),
        "The great primeval forest on the border with Poland, a royal hunting ground from the fifteenth century and the place where the European bison lived on in the wild longest. Mikola Husoŭski's Latin Song of the Bison (1523), written in Rome for Pope Leo X, names only 'the Lithuanian forests'; Belavezha is the nearest real place",
        "与波兰交界的大片原始森林，15 世纪起是王室猎场，也是欧洲野牛在野外活得最久的地方。米科拉·古索夫斯基 1523 年出版的拉丁文长诗《野牛之歌》是在罗马为教皇利奥十世写的，诗里只说“立陶宛的森林”；别洛韦日是离它最近的真实地点"),
    b.ORIG("by-polotsk", "Polotsk", "波洛茨克", *C("by-polotsk"),
        "The old city on the Dvina where the Palata flows in, with St Sophia on the castle hill. Jan Barščeŭski, who grew up nearby and was taught by the Jesuits of Polotsk, gave the city its own sketch, 'Połock', in his Squire Zavalnia",
        "道加瓦河（西德维纳河）与波洛塔河汇流处的古城，城堡山上有圣索菲亚大教堂。在附近长大、在波洛茨克耶稣会学校读过书的扬·巴尔舍夫斯基，在《地主扎瓦利尼亚》里专门写了一篇《波洛茨克》"),
    b.ORIG("by-slutsk", "Slutsk", "斯卢茨克", *C("by-slutsk"),
        "The town on the Sluch whose manufactory wove the famous Slutsk sashes, the silk belts worn over the kuntush by the nobility of the Grand Duchy; their patterns first copied Eastern models and later took in local flowers such as the cornflower. Production stopped in 1848. Maksim Bahdanovič's poem 'The Weavers of Slutsk' is about the girls who wove them",
        "斯卢奇河边的小城，这里的作坊织出了有名的斯卢茨克腰带——大公国贵族系在长袍外面的丝绸腰带；纹样起初照搬东方，后来织进了矢车菊等本地花草。1848 年停产。马克西姆·博格达诺维奇的诗《斯卢茨克的织女》写的就是织这些腰带的姑娘"),
    b.PIL("by-kusliany", "Bahuševič Museum-Estate, Kušlany", "库什利亚内的博古舍维奇故居博物馆", *C("by-kusliany"),
        "The Bahuševič family estate in Kušlany, Smarhoń district: Francišak Bahuševič built the house in 1896, and it has been a museum since 1990. Under the pen name Maciej Buračok he published The Belarusian Fife in Kraków in 1891; its preface asks his 'dear brothers' not to abandon their Belarusian language, lest they die",
        "斯莫尔贡区库什利亚内的博古舍维奇家族庄园：弗朗齐舍克·博古舍维奇 1896 年盖了这座房子，1990 年起是博物馆。他用笔名“马采伊·布拉乔克”1891 年在克拉科夫出版了《白俄罗斯芦笛》；序言里恳求“亲爱的弟兄们”不要丢下白俄罗斯语，免得自己死去",
        ["dudka-bielaruskaja"]),
]

lines = [
    b.S("by-ka-1", "kalasy-pad-siarpom-tvaim", "by-orsha-karatkievich", "The novel as a whole", "全书",
        "Ears of Rye beneath Your Sickle shows Belarus on the eve of the uprising of 1863, mostly in 1850–1861, through the growing up of Ales Zahorski, heir of a noble family, from eleven to twenty, beside peasant and rebel families and real people such as Kastus Kalinoŭski. Its estates, Zahoršcyna and Suchodol, are invented and lie on the Dnieper; the young master of Zahoršcyna rides between Suchodol, Mahilioŭ and Orsha. Uladzimir Karatkievič was born in Orsha; his maternal grandfather, Vasil Hrynkievič, was the prototype of old Danila Zahorski-Vieža, and from him he heard the legend 'Mother of the Wind'.",
        "《你镰刀下的麦穗》写 1863 年起义前夕的白俄罗斯，主要是 1850 到 1861 年，借贵族之家的继承人阿列西·扎戈尔斯基从 11 岁到 20 岁的成长，同时写农民和起义者的家庭，以及卡斯图西·卡利诺夫斯基等真实人物。书里的庄园扎戈尔希奇纳和苏霍多尔是虚构的，都在第聂伯河边；扎戈尔希奇纳的年轻主人在苏霍多尔、莫吉廖夫和奥尔沙之间来回奔波。乌拉济米尔·卡拉特克维奇就生在奥尔沙；他的外祖父瓦西里·赫林克维奇是老达尼拉·扎戈尔斯基-韦扎的原型，他从外祖父那里听来了《风之母》的传说。",
        ["Orsha"], ["奥尔沙"],
        "https://be.wikipedia.org/wiki/Каласы_пад_сярпом_тваім; https://knihi.com/Uladzimir_Karatkievic/Kalasy_pad_siarpom_tvaim.html; https://www.nslowa.by/2020/12/01/geniyalny-ramantyk-belaruskaj-litaratury-hh-stagoddzya/; https://nlb.by/en/news/through-the-pages-of-the-belarusian-calendar/i-was-i-am-i-will-be/; https://be.wikipedia.org/wiki/Дом_па_вуліцы_Уладзіміра_Леніна,_26_(Орша)"),
    b.S("by-lb-1", "liudzi-na-balocie", "by-karanioka", "The novel as a whole", "全书",
        "People of the Marsh, the first novel of Ivan Melež's Palesse Chronicle, is set in Kurani, a village cut off from the world by the marshes of Palesse, in the 1920s, as the changes begin that end in collectivization; at its centre are human ties, love and survival. Melež was born in 1921 in Hlinišča, in the Chojniki district; Karanioŭka, a few kilometres away, is held to be the prototype of Kurani. The novel and its sequel won the Lenin Prize in 1972.",
        "《沼泽地的人们》是伊万·梅列日《波列西耶纪事》的第一部，故事发生在被波列西耶沼泽与外界隔开的库拉尼村，时间是 20 世纪 20 年代，正是一场以集体化收尾的变革开始的时候；小说的中心是人与人的牵绊、爱情和活下去。梅列日 1921 年生在霍伊尼基区的赫利尼什恰；几公里外的卡拉尼奥夫卡被认为是库拉尼的原型。这部小说和它的续篇 1972 年获得列宁奖。",
        ["Karanioŭka"], ["卡拉尼奥夫卡"],
        "https://person.goub.by/?p=2139 (Bierazjuk, 'Liudzi u balota', Respublika, 20 May 2010: Karanioŭka as the prototype of Kurani); https://cyclowiki.org/wiki/Мележ,_Иван; https://be.wikipedia.org/wiki/Каранёўка_(Хойніцкі_раён)"),
    b.S("by-zb-1", "znak-biady", "by-bychki", "The novella as a whole", "全书",
        "The Sign of Misfortune follows Stsiapanida and Piatrok, an ageing couple on a farmstead near the village of Vyselki, when the German occupiers come: first the local polizei Huž and Kalandzionak, then German soldiers take over their house; Piatrok tries to please them, Stsiapanida will not bow. Through her memories the novella reaches back to the collectivization of the early 1930s. Bykaŭ drew that collectivization from life, from what he saw as a child in his native Byčki, where six of the twelve families were dekulakized and exiled. It won the Lenin Prize in 1986.",
        "《灾难的征兆》写德国占领军到来时，住在维谢尔基村附近一座农舍里的一对老夫妻斯捷帕尼达和彼得罗克：先是本地的伪警察古日和卡兰焦纳克，后来是德国兵，占了他们的房子；彼得罗克一心讨好，斯捷帕尼达却不肯低头。借着她的回忆，小说回溯到 30 年代初的集体化。贝科夫写的集体化是照着生活写的——那是他小时候在家乡贝奇基亲眼看见的：村里 12 户人家，有 6 户被当作富农剥夺财产、流放。这部小说 1986 年获得列宁奖。",
        ["Byčki"], ["贝奇基"],
        "https://be.wikipedia.org/wiki/Знак_бяды; https://nashaniva.com/221375; https://be.wikipedia.org/wiki/Музей-сядзіба_Васіля_Быкава"),
    Q("by-nz-1", "novaja-ziamlia", "by-lastok", "Part VI, 'By the Dugout'", "第六章《土屋旁》",
      "Belarusian Wikisource, Новая зямля (1923)/VI (Minsk 1923 edition)",
      ws.block(WSR, "Новая зямля (1923)/VI", "На першы погляд няцікава", "Аб гаспадарскім нерадзеньні."), ["Парэчча"],
      "At first sight it looked a dreary place,\nthis Parechcha, and sadness rocked the heart\nat that row of old birch trees\nthat stood in the marsh among the forests\nrustling their bare tops.\nEverything here lay scattered about:\nthe low lengths of fence\nhad slipped out of their rotten posts,\nand wood chips lay in heaps\nall over the yard and by the woodpile;\nthe old cowshed with no board under its door,\nthe barn with its little greyed roof\ngrown over with moss and rotting,\nthe lean-to, the house: every last thing\nspoke loud and clear\nof disorder, of neglect,\nof a holding let go to ruin.",
      ["Parechcha"],
      "乍一看，这个帕雷奇恰\n显得冷清无趣，\n那一排老白桦\n立在林间的沼泽上，\n光秃秃的树梢沙沙作响，\n把人的心摇进愁绪里。\n这里一切都乱七八糟：\n低矮的篱笆一节节\n从朽烂的木桩上滑脱，\n木屑一堆一堆\n散满了院子和柴棚；\n门下没有挡板的旧牛棚，\n屋顶发灰的谷仓\n长满青苔、正在霉烂，\n披屋、房子——无一例外，\n都清清楚楚、大声地诉说着\n凌乱、荒废，\n和一个荒疏了的家。",
      ["帕雷奇恰"]),
    Q("by-pz-1", "piesnia-pra-zubra", "by-belavezha", "The bison described", "写野牛",
      "Latin Wikisource, Carmen de statura feritate ac venatione bisontis (editio princeps, Cracow 1523)",
      ws.block(WSR, "Carmen de statura feritate ac venatione bisontis", "Haec fera Litphanis", "cornua bina viri.", number="\xa0"), ["Litphanis"],   # number: the pentameters' indent ({{tab}}, a no-break space) is taken off
      "This beast, by far the fiercest, is born\nin the Lithuanian forests, and grows so huge\nthat when, overcome, it lays its head down to die,\nthree men may sit between its two horns.",
      ["Lithuanian forests"],
      "这头野兽是立陶宛的森林里\n最凶猛的，它生得如此庞大，\n当它被制服、垂下头死去时，\n两只角之间能坐下三个人。",
      ["立陶宛的森林"]),
    Q("by-sz-1", "sliachcic-zavalnia", "by-polotsk", "'Połock'", "《波洛茨克》",
      "Polish Wikisource, Szlachcic Zawalnia czyli Białoruś/Połock (Petersburg 1844–1846 edition)",
      ws.cut(WSR, "Szlachcic Zawalnia czyli Białoruś/Połock", "Minąłem bory", "te mury wyniosłe."), ["Połock"],
      "I passed the pine forests, and there on the wide plain I see the town of Polotsk. The church towers of St Stephen's, and on the castle hill the church of St Sophia, standing in the mist, seem to reach the clouds; their giant shapes rule over the town and all the country round. At this sight the picture of the whole past painted itself in my mind; longing sank into my heart, and with tearful eyes I met those lofty walls.",
      ["Polotsk"],
      "我穿过松林，看见宽阔的平原上就是波洛茨克城。圣斯捷潘教堂的钟楼，还有城堡山上的圣索菲亚教堂，立在雾里，仿佛高入云端；它们巨大的身影俯临全城和四周的乡野。看到这一幕，整个过去的图景在我脑海里浮现出来；思念沉进心底，我含着泪望着那些高耸的城墙。",
      ["波洛茨克"]),
    Q("by-vi-1", "vianok", "by-slutsk", "'Old Belarus': 'The Weavers of Slutsk'", "《旧白俄罗斯》：《斯卢茨克的织女》",
      "Belarusian Wikisource, Вянок (1914)/Старая Беларусь/Слуцкіе ткачыхі (Vilnius 1914 edition)",
      ws.block(WSR, "Вянок (1914)/Старая Беларусь/Слуцкіе ткачыхі", "СЛУЦКІЕ ТКАЧЫХІ.", "Цьвяток радзімы васілька."), ["СЛУЦКІЕ"],
      "THE WEAVERS OF SLUTSK.\nFrom their native fields, from their native home,\nthey were taken, the luckless ones,\nto the lord's manor, for the sake of beauty,\nto weave golden sashes.\nAnd through the long hours,\nforgetting their girlhood dreams,\nthey weave their broad cloths\nin the Persian manner.\nBut beyond the wall the field is laughing,\nthe sky shines in through the window,\nand their thoughts rush, unbidden,\nto where the spring has blossomed,\nwhere the grain gleams in the clear distance,\nthe cornflowers show sweetly blue,\nand the waves of a river running between hills\nglitter like cold silver.\nThe jagged edge of the forest darkens…\nAnd the hand, forgetting itself, weaves,\ninstead of the Persian pattern,\nthe flower of home, the cornflower.",
      ["SLUTSK"],
      "斯卢茨克的织女。\n从家乡的田野，从自己的家，\n这些苦命的姑娘\n为了美观被带进老爷的庄园，\n织金色的腰带。\n漫长的时辰里，\n她们忘了少女的梦，\n照着波斯的样式\n织她们宽宽的布。\n墙外，田野在笑，\n天空从窗口闪着光——\n思绪不由自主地飞向\n春天开花的地方，\n那里庄稼在晴朗的远处闪亮，\n矢车菊蓝得可爱，\n山间流淌的河水\n泛着冷冷的银光。\n参差的林边暗了下来……\n手忘了自己，\n织出的不是波斯的花样，\n而是故乡的花——矢车菊。",
      ["斯卢茨克"]),
]

def ids_in(path): return set(re.findall(r'\{ id: "([^"]+)"', open(path, encoding="utf-8").read()))
all_books = set()
for f in glob.glob(os.path.join(APP, "data", "*", "books.js")):
    all_books |= ids_in(f)
new_b, new_p = {x["id"] for x in books}, {x["id"] for x in places}
assert len(books) == 8 and len(new_b) == 8
assert not new_b & all_books, new_b & all_books
assert new_p == set(CO), new_p ^ set(CO)
for l in lines:
    assert l["book_id"] in new_b and l["place_ids"][0] in new_p, l["id"]
linked = {l["book_id"] for l in lines} | {x for p in places for x in p.get("book_ids", [])}
assert linked == new_b, new_b ^ linked
assert {l["place_ids"][0] for l in lines} | {p["id"] for p in places if p.get("book_ids")} == new_p

HEAD = "// Belarus, hand-written content (tools/content/batches/add_by1.py, 2026-11-26).\n"
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
