"""11-23: Sweden, first pack: 16 new books, 16 places. Strindberg's Stockholm and Kymmendö, Söderberg's Klara,
Lagerlöf's Värmland, Skåne and Dalarna, Bellman's Djurgården, Almqvist at Riddarholmen, Fröding, Moberg's Småland,
Astrid Lindgren's Vimmerby, and the modern Stockholm and Skåne of Larsson, Mankell and Lindqvist. Fictional settings
hang on the real place the book names or is drawn from, and the note says which.

Quotations (6 lines) are cut from Swedish Wikisource pages (tools/content/wikisource.py); translations are our own
drafts (translation: "own"). Books in copyright, and PD books whose text we could not reach, have scene notes in our
own words or hang on a writer's place. What a cut changes, named in `checked`: hard-wrapped lines are re-flowed; the
Red Room cut ends at the first clause of a long sentence.

Coordinates are those of the place's Swedish Wikipedia article (cache/se/coords.json).

Usage: python3 -I add_se1.py <app_dir> <coords.json> <wikisource_root>"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b
import wikisource as ws

APP, CO, WSR = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8")), sys.argv[3]
DATE = "2026-11-23"
b.init(APP, "", "se", DATE)
W = b.W
SVW = "https://sv.wikipedia.org/wiki/"
GAP = b.GAP

def BK(id, title, title_zh, title_orig, author, author_zh, author_orig, year, pd=True, **kw):
    d = dict(id=id, title=title, title_zh=title_zh, title_orig=title_orig, author=author, author_zh=author_zh, year=year,
             orig_lang=kw.pop("lang", "sv"), public_domain=pd, source_url=kw.pop("src", None), author_orig=author_orig)
    d.update(kw)
    return {k: v for k, v in d.items() if v is not None or k == "source_url"}

def C(pid):
    c = CO[pid]
    return c["lat"], c["lon"], c["st"], c["su"]

def ORIG(pid, name, zh, en_note, zh_note, **kw): return b.ORIG(pid, name, zh, *C(pid), en_note, zh_note, **kw)
def PIL(pid, name, zh, en_note, zh_note, ids, **kw): return b.PIL(pid, name, zh, *C(pid), en_note, zh_note, ids, **kw)
S = b.S

def raw(title, start, end, lang="sv"):
    t = ws.text(os.path.join(WSR, lang), title)
    n = re.sub("[\xa0   ]", " ", t)
    i = n.find(start)
    assert i >= 0, (title, start)
    j = n.find(end, i)
    assert j >= 0, (title, start, end)
    return t[i:j + len(end)]

def flow(s):
    """a hard-wrapped paragraph: lines joined, doubled spaces written as one"""
    return re.sub(r" {2,}", " ", s.replace("\n", " "))

def Q(id, book, place, loc, loc_zh, title, orig, hl_orig, en, hl_en, zh, hl_zh, note="", site="Swedish"):
    if re.search("[\xa0   ]", orig):
        orig = re.sub("[\xa0   ]+", " ", orig)
        note += " (no-break spaces written as plain spaces)"
    for text, hls in ((orig, hl_orig), (en, hl_en), (zh, hl_zh)):
        for h in hls:
            assert h in text, (id, h)
    assert "  " not in orig and "[" not in orig, (id, "spacing or page mark")
    return dict(id=id, book_id=book, place_ids=[place], location=loc, location_zh=loc_zh,
                text_orig=orig, highlight_orig=hl_orig, text_en=en, highlight_en=hl_en, text_zh=zh, highlight_zh=hl_zh, translation="own",
                status="draft", checked=f"{site} Wikisource, {title}{note}, {DATE}")

def EN(id, book, place, loc, loc_zh, title, text, hl, zh, hl_zh, note=""):
    assert "[" not in text and "]" not in text and "\xa0" not in text and "  " not in text, (id, text[:40])
    for h in hl: assert h in text, (id, h)
    for h in hl_zh: assert h in zh, (id, h)
    return dict(id=id, book_id=book, place_ids=[place], location=loc, location_zh=loc_zh, text_en=text, highlight_en=hl, translation="original",
                text_zh=zh, highlight_zh=hl_zh, status="draft", checked=f"English Wikisource, {title}{note}, {DATE}")

STR = ("August Strindberg", "斯特林堡", "August Strindberg")
LAG = ("Selma Lagerlöf", "塞尔玛·拉格洛夫", "Selma Lagerlöf")
LIN = ("Astrid Lindgren", "阿斯特丽德·林格伦", "Astrid Lindgren")
T_RR, T_DG, T_GB, T_NH = "Röda rummet/Kapitel 1", "Doktor Glas/12 juni", "Gösta Berlings saga/Kapitel 03", "Nils Holgerssons underbara resa genom Sverige/1"
T_DGA, T_FE = "Det går an/Kapitel 1", "Fredmans epistel n:o 33"
EXIST = set()

books = [
    BK("red-room", "The Red Room", "红房间", "Röda rummet", *STR, "1879", src=ws.url("sv", "Röda rummet"),
       aliases=["Röda rummet", "Arvid Falk", "Mosebacke", "Strindberg"]),
    BK("hemsoborna", "The People of Hemsö", "海姆斯岛上的人们", "Hemsöborna", *STR, "1887", aliases=["Hemsöborna", "Carlsson", "Kymmendö", "Hemsö"]),
    BK("miss-julie", "Miss Julie", "朱丽小姐", "Fröken Julie", *STR, "1888", aliases=["Fröken Julie", "Jean", "Midsummer Eve", "Strindberg"]),
    BK("doktor-glas", "Doctor Glas", "格拉斯医生", "Doktor Glas", "Hjalmar Söderberg", "雅尔玛尔·瑟德尔贝里", "Hjalmar Söderberg", "1905",
       src=ws.url("sv", "Doktor Glas"), aliases=["Doktor Glas", "Tyko Gabriel Glas", "Pastor Gregorius", "Klara"]),
    BK("gosta-berlings-saga", "Gösta Berling's Saga", "骑士的传说", "Gösta Berlings saga", *LAG, "1891", src=ws.url("sv", "Gösta Berlings saga"),
       aliases=["The Story of Gösta Berling", "Ekeby", "Löven", "Fryken", "Värmland", "古斯泰·贝林的故事"]),
    BK("nils-holgersson", "The Wonderful Adventures of Nils", "尼尔斯骑鹅旅行记", "Nils Holgerssons underbara resa genom Sverige", *LAG, "1906–1907",
       src=ws.url("sv", "Nils Holgerssons underbara resa genom Sverige"), aliases=["Nils Holgersson", "Akka", "Mårten", "Västra Vemmenhög", "骑鹅旅行记"]),
    BK("jerusalem-lagerlof", "Jerusalem", "耶路撒冷", "Jerusalem", *LAG, "1901–1902", src=ws.url("sv", "Jerusalem"),
       aliases=["Ingmarssönerna", "Ingmar Ingmarsson", "Nås", "Dalarna"]),
    BK("fredmans-epistlar", "Fredman's Epistles", "弗雷德曼书简", "Fredmans epistlar", "Carl Michael Bellman", "贝尔曼", "Carl Michael Bellman", "1790",
       src=ws.url("sv", "Fredmans epistlar"), aliases=["Fredmans epistlar", "Bellman", "Movitz", "Ulla Winblad", "Stolta stad"]),
    BK("det-gar-an", "Sara Videbeck", "这样也行", "Det går an", "Carl Jonas Love Almqvist", "阿尔姆奎斯特", "C. J. L. Almqvist", "1839",
       src=ws.url("sv", "Det går an"), aliases=["Det går an", "Why Not?", "Sara Videbeck", "Yngve Frey", "Almqvist"]),
    BK("the-emigrants", "The Emigrants", "移民", "Utvandrarna", "Vilhelm Moberg", "威廉·莫贝里", "Vilhelm Moberg", "1949", pd=False,
       aliases=["Utvandrarna", "Karl Oskar", "Kristina", "Ljuder", "Småland"]),
    BK("pippi-longstocking", "Pippi Longstocking", "长袜子皮皮", "Pippi Långstrump", *LIN, "1945", pd=False,
       aliases=["Pippi Långstrump", "Villa Villekulla", "Lindgren"]),
    BK("emil-of-lonneberga", "Emil of Lönneberga", "淘气包埃米尔", "Emil i Lönneberga", *LIN, "1963", pd=False,
       aliases=["Emil i Lönneberga", "Katthult", "Lönneberga", "Lindgren"]),
    BK("girl-with-the-dragon-tattoo", "The Girl with the Dragon Tattoo", "龙文身的女孩", "Män som hatar kvinnor", "Stieg Larsson", "斯蒂格·拉森",
       "Stieg Larsson", "2005", pd=False, aliases=["Män som hatar kvinnor", "Millennium", "Mikael Blomkvist", "Lisbeth Salander", "千禧年"]),
    BK("faceless-killers", "Faceless Killers", "无面杀手", "Mördare utan ansikte", "Henning Mankell", "亨宁·曼凯尔", "Henning Mankell", "1991", pd=False,
       aliases=["Mördare utan ansikte", "Wallander", "Kurt Wallander", "Ystad"]),
    BK("let-the-right-one-in", "Let the Right One In", "生人勿进", "Låt den rätte komma in", "John Ajvide Lindqvist", "约翰·阿伊维德·林德奎斯特",
       "John Ajvide Lindqvist", "2004", pd=False, aliases=["Låt den rätte komma in", "Oskar", "Eli", "Blackeberg", "血色入侵"]),
    BK("guitar-and-concertina", "Guitar and Concertina", "吉他与手风琴", "Guitarr och dragharmonika", "Gustaf Fröding", "古斯塔夫·弗勒丁", "Gustaf Fröding",
       "1891", aliases=["Guitarr och dragharmonika", "Fröding", "Värmland"]),
]

places = [
    ORIG("se-mosebacke", "Mosebacke, Södermalm", "莫塞巴克，南岛",
         "The square and terrace on the heights of Södermalm, with a wide view over the Saltsjön and the city. The Red Room opens in the garden of the Mosebacke inn, in a chapter called 'Stockholm from a Bird's-Eye View', where the young Arvid Falk looks down on the city",
         "南岛高处的广场和观景台，可以远眺盐湖和全城。《红房间》就从莫塞巴克酒馆的花园开始，第一章题为《鸟瞰斯德哥尔摩》，年轻的阿尔维德·法尔克在这里俯视全城"),
    ORIG("se-kymmendo", "Kymmendö", "许门德岛",
         "Island in the Stockholm archipelago, the model for Hemsö. Strindberg first came here in 1871 as a summer guest with student friends and came back for many summers",
         "斯德哥尔摩群岛中的一座岛，“海姆斯岛”的原型。斯特林堡 1871 年第一次和几个同学来这里消夏，此后又来过许多个夏天"),
    PIL("se-strindberg-museum", "Strindberg Museum (the Blue Tower), Stockholm", "斯特林堡博物馆（蓝塔），斯德哥尔摩",
        "Strindberg's last home, at Drottninggatan 85: he moved into the newly built house, which he called the Blue Tower, in 1908 and lived here for the last four years of his life. The museum opened in 1973",
        "斯特林堡最后的住所，在王后街 85 号。1908 年他搬进这座新落成、被他称作“蓝塔”的楼房，在这里度过了一生最后的四年。博物馆 1973 年开放",
        ["miss-julie"]),
    ORIG("se-klara", "Klara Church, Stockholm", "克拉拉教堂，斯德哥尔摩",
         "The church in central Stockholm with its tree-shaded churchyard. Doctor Glas, the diary of a Stockholm doctor through one hot summer, has him walk home past it at night with his thoughts of killing a pastor",
         "斯德哥尔摩市中心的教堂，墓园里绿树成荫。《格拉斯医生》是一位斯德哥尔摩医生在一个炎热夏天写下的日记，他满脑子想着要杀死一个牧师，夜里从这座教堂边走回家"),
    ORIG("se-rottneros", "Rottneros Manor (Ekeby)", "罗特内罗斯庄园（埃克比）",
         "Manor on Lake Fryken in Värmland, the model for Ekeby in Gösta Berling's Saga; the lake of the book, called Löven, is Fryken. The old manor house burned on Lucia night 1929",
         "韦姆兰弗吕肯湖畔的庄园，《骑士的传说》中埃克比的原型；书中叫作勒文湖的那片湖就是弗吕肯湖。老宅在 1929 年的露西亚之夜被烧毁"),
    PIL("se-marbacka", "Mårbacka", "莫尔巴卡",
        "The manor in Värmland where Selma Lagerlöf was born and grew up, now kept as a memorial museum to her",
        "韦姆兰的庄园，塞尔玛·拉格洛夫在这里出生、长大，如今作为她的纪念博物馆保存下来",
        ["gosta-berlings-saga", "nils-holgersson"]),
    ORIG("se-vemmenhog", "Västra Vemmenhög Church", "西韦姆恩赫格教堂",
         "The church of Nils Holgersson's home parish in southern Skåne. His journey begins here on Sunday 20 March and ends when he comes home on 8 November; the course centre named after him beside the church burned down in 2004",
         "斯科讷南部尼尔斯·霍尔格松家乡教区的教堂。他的旅行在 3 月 20 日星期天从这里开始，11 月 8 日回到家时结束；教堂旁以他命名的培训农庄在 2004 年烧毁了"),
    ORIG("se-nas", "Nås, Dalarna", "诺斯，达拉纳",
         "Parish in Dalarna from which 37 farmers sold everything they owned in 1896 and went to Jerusalem, where they joined a Christian colony. Lagerlöf's Jerusalem is built on their story, and every summer the Ingmar plays are performed here",
         "达拉纳的一个教区，1896 年这里有 37 位农民卖掉了全部家产去耶路撒冷，加入了那里的一个基督徒聚居团体。拉格洛夫的《耶路撒冷》就以他们的故事为本，这里每年夏天都上演“英格玛戏剧”"),
    ORIG("se-djurgarden", "Djurgården", "动物园岛",
         "The royal park island east of the old town; in Bellman's day it was an oasis with some thirty taverns and inns, and an old oak near Hasselbacken is called Bellman's oak, under which he is said to have written his epistles. Epistle 33, 'Stolta stad', follows Father Movitz across the water to Djurgården",
         "老城以东的皇家园林岛。贝尔曼的时代，这里是一片有三十来家小酒馆和客栈的绿洲；哈瑟尔巴肯附近有一棵老橡树叫“贝尔曼橡树”，据说他就是坐在树下写他的书简的。第三十三首书简《骄傲的城》写的就是莫维茨老爹渡海去动物园岛"),
    ORIG("se-riddarholmen", "Riddarholm Church, Stockholm", "骑士岛教堂，斯德哥尔摩",
         "The church on Riddarholmen in Stockholm, burial church of Swedish kings. Almqvist's Det går an begins with travellers hurrying past it down to the steamboat Yngve Frey, on which the glazier's daughter Sara Videbeck and Sergeant Albert travel towards Lidköping",
         "斯德哥尔摩骑士岛上的教堂，瑞典国王的安葬之所。阿尔姆奎斯特的《这样也行》开篇，旅客们匆匆走过这座教堂，下到“英格维·弗雷”号轮船上——玻璃匠的女儿萨拉·维德贝克和中士阿尔伯特就乘这艘船驶往利德雪平"),
    ORIG("se-ljuder", "Ljuder Church, Småland", "柳德教堂，斯莫兰",
         "Church of Ljuder parish in Småland, where Karl Oskar and Kristina have their farm in Moberg's The Emigrants",
         "斯莫兰柳德教区的教堂。在莫贝里的《移民》里，卡尔·奥斯卡和克里斯蒂娜的农庄就在这个教区"),
    PIL("se-vimmerby", "Astrid Lindgren's Näs, Vimmerby", "阿斯特丽德·林格伦的内斯，维默比",
        "The cultural centre at Vimmerby around Näs, the farm where Astrid Lindgren was born in 1907 and grew up, and the old vicarage beside it; its pavilion was opened on 12 June 2007. Emil lives at Katthult in Lönneberga parish, in the same Småland countryside",
        "维默比围绕内斯农庄建起的文化中心——阿斯特丽德·林格伦 1907 年在这里出生、长大——旁边还有老牧师住宅；展馆于 2007 年 6 月 12 日落成。埃米尔住在同一片斯莫兰乡间的伦讷贝加教区的卡特胡尔特农庄",
        ["pippi-longstocking", "emil-of-lonneberga"]),
    ORIG("se-mariaberget", "Bellmansgatan 1, Mariaberget", "贝尔曼街 1 号，玛丽亚山",
         "The building on Mariaberget, Södermalm, where Mikael Blomkvist of the Millennium books has his top-floor flat, reached from a footbridge over the street and looking out over Gamla Stan; walking tours of Larsson's Stockholm start here",
         "南岛玛丽亚山上的楼房，“千禧年”系列里米凯尔·布隆克维斯特的顶楼公寓就在这里，要从街上的人行天桥进去，窗外是老城。拉森笔下斯德哥尔摩的徒步游就从这里出发"),
    ORIG("se-ystad", "Ystad", "于斯塔德",
         "Old town on the south coast of Skåne. Henning Mankell's Kurt Wallander books are largely set here, where Wallander is a detective of the local police",
         "斯科讷南岸的古城。亨宁·曼凯尔的库尔特·瓦兰德系列大部分发生在这里，瓦兰德是当地警局的探长"),
    ORIG("se-blackeberg", "Blackeberg", "布拉克贝里",
         "Working-class suburb in western Stockholm, where Let the Right One In takes place in the early 1980s",
         "斯德哥尔摩西郊的工人住宅区，《生人勿进》的故事就发生在八十年代初的这里"),
    PIL("se-alster", "Alster Manor", "阿尔斯特庄园",
        "Manor near Karlstad in Värmland where Gustaf Fröding was born on 22 August 1860; it is kept as a memorial to him. His first collection, Guitar and Concertina (1891), was quickly popular",
        "韦姆兰卡尔斯塔德附近的庄园，古斯塔夫·弗勒丁 1860 年 8 月 22 日生于此地，如今是他的纪念馆。他的第一部诗集《吉他与手风琴》（1891）很快就风行一时",
        ["guitar-and-concertina"]),
]

_rr = raw(T_RR, "Stockholm i fågelperspektiv.", "rabatterna voro ej uppgrävda;")
_dg = flow(raw(T_DG, "Men jag\ntror, att om jag kunde döda", "göra det.")) + "\n" + flow(raw(T_DG, "Då jag gick hem i den onaturliga", "druckna ögon."))
_fe = raw(T_FE, "N:o 33.", "Ge rum vid Roddar-trappan.")
lines = [
    Q("se-rr-1", "red-room", "se-mosebacke", "Chapter 1, 'Stockholm from a Bird's-Eye View'", "第一章《鸟瞰斯德哥尔摩》", T_RR, _rr, ["Mosebacke"],
      "Stockholm from a Bird's-Eye View.\nIt was an evening at the beginning of May. The little garden on Mosebacke had not yet been opened to the public, and the flower-beds had not yet been dug;",
      ["Mosebacke"],
      "鸟瞰斯德哥尔摩。\n那是五月初的一个傍晚。莫塞巴克的小花园还没有向公众开放，花坛也还没有翻土；",
      ["莫塞巴克"], note=" (cut at the end of the first clause)"),
    Q("se-dg-1", "doktor-glas", "se-klara", "Entry for 12 June", "6 月 12 日的日记", T_DG, _dg, ["Klara kyrka"],
      "But I believe that if I could kill that priest by pressing a button in the wall, I would do it.\nAs I walked home in the unnatural, pale twilight of the night, the heat seemed as oppressive again as at midday, as if saturated with anguish; the red clouds of dust that lay banked beyond the factory chimneys on Kungsholmen had darkened and looked like sleeping disasters. I walked homewards with long strides down towards Klara church, hat in hand, for the sweat was trickling on my forehead. Not even under the great trees of the churchyard was there any coolness, but on almost every bench a couple sat whispering, and some sat on each other's knees and kissed with drunken eyes.",
      ["Klara church"],
      "可我相信，要是按一下墙上的按钮就能杀死那个牧师，我会这样做的。\n我在反常的、苍白的夜色中走回家去，炎热似乎又像正午一样逼人，仿佛浸透了焦虑；堆积在国王岛那些工厂烟囱后面的红色尘雾已经暗了下来，像一场场沉睡的灾祸。我大步朝克拉拉教堂走回家，手里拿着帽子，因为汗水正从额头上渗出来。就连教堂墓地的大树底下也没有一丝凉意，可几乎每张长椅上都坐着一对人在窃窃私语，有的坐在对方膝上，醉眼迷离地接吻。",
      ["克拉拉教堂"], note=" (the page's line ends joined)"),
    Q("se-gb-1", "gosta-berlings-saga", "se-rottneros", "'The Landscape'", "《风景》", T_GB,
      flow(raw(T_GB, "NU MÅSTE JAG beskriva den långa sjön", "framlevde sin lustiga tillvaro.")), ["den långa sjön", "Ekebykavaljererna"],
      "Now I must describe the long lake, the rich plain and the blue mountains, since they were the stage on which Gösta Berling and the cavaliers of Ekeby lived out their merry lives.",
      ["the long lake", "cavaliers of Ekeby"],
      "现在我必须描写一下那长长的湖、富饶的平原和蓝色的群山，因为它们就是戈斯塔·贝林和埃克比的骑士们过他们那快活日子的舞台。",
      ["长长的湖", "埃克比的骑士们"], note=" (the page's line ends joined)"),
    Q("se-nh-1", "nils-holgersson", "se-vemmenhog", "Chapter 1, 'The Boy'", "第一章《男孩》", T_NH,
      flow(raw(T_NH, "Ute var det allra vackraste vårväder.", "där var våren redan i full gång.")), ["Västra Vemmenhögs socken"],
      "Outside it was the loveliest spring weather. The year had come no further than the twentieth of March, but the boy lived in the parish of Västra Vemmenhög, far down in southern Skåne, and there spring was already in full swing.",
      ["parish of Västra Vemmenhög"],
      "外面是最美好的春日天气。这一年才到三月二十日，可男孩住在斯科讷南部最南边的西韦姆恩赫格教区，那里的春天已经热热闹闹地来了。",
      ["西韦姆恩赫格教区"], note=" (the page's line ends joined)"),
    Q("se-dga-1", "det-gar-an", "se-riddarholmen", "Chapter 1", "第一章", T_DGA,
      flow(raw(T_DGA, "En skön thorsdagsmorgon i julii månad", "der ångbåtarne lågo.")), ["Riddarholmskyrkan i Stockholm"],
      "One fine Thursday morning in July a great many people streamed past the Riddarholm Church in Stockholm and hurried down the slope between the Kammarrätt and the Statskontor, so as to get down in good time to the shore of Lake Mälaren, where the steamboats lay.",
      ["Riddarholm Church in Stockholm"],
      "七月里一个晴朗的星期四早晨，许多人涌过斯德哥尔摩的骑士岛教堂，匆匆走下审计院和国库署之间的坡道，好及时赶到梅拉伦湖边——轮船就停在那里。",
      ["斯德哥尔摩的骑士岛教堂"], note=" (the page's line ends joined)"),
    Q("se-fe-1", "fredmans-epistlar", "se-djurgarden", "Epistle 33, opening", "第三十三首开头", T_FE, _fe, ["Djurgården"],
      "No. 33.\nFREDMAN'S EPISTLE,\nfirst, on Father Movitz's crossing to Djurgården, and\nsecond, on the virtuous Susanna.\nWas ist das? Make room at the boatmen's stairs.",
      ["Djurgården"],
      "第三十三首。\n弗雷德曼书简，\n一、莫维茨老爹渡海去动物园岛；\n二、贞洁的苏珊娜。\nWas ist das？在船夫码头的台阶边让开！",
      ["动物园岛"]),
]
lines += [
    S("se-hemso-s1", "hemsoborna", "se-kymmendo", "Throughout", "全书",
      "Carlsson, a mainlander, comes out one April evening to the island of Hemsö to run the farm for the widow Madame Flod. He takes over the place, marries the widow and quarrels with her son Gusten; at the end, as they take her coffin across the ice, it goes through, and Carlsson is presumed drowned.",
      "大陆人卡尔松在一个四月的傍晚来到海姆斯岛，替寡妇弗洛德太太经营农庄。他接管了农庄，娶了寡妇，又和她的儿子古斯滕闹翻；故事末尾，他们拉着她的棺材过冰面时冰裂了，棺材沉了下去，人们以为卡尔松也淹死了。",
      ["Hemsö"], ["海姆斯岛"], SVW + "Hems%C3%B6borna"),
    S("se-jer-s1", "jerusalem-lagerlof", "se-nas", "Part 1, 'In Dalarna'", "第一部《在达拉纳》",
      "In a parish in Dalarna, the Ingmarssons, the old leading family of the farmers, are caught up in a religious revival that divides the village. In the end a group of farmers sell their farms and leave for the Holy Land, as the farmers of Nås did in 1896.",
      "达拉纳的一个教区里，农民中历来的领头人家英格玛松一家被卷进了一场分裂村庄的宗教复兴运动。最后，一群农民卖掉农庄，动身前往圣地——就像 1896 年诺斯的农民们所做的那样。",
      ["Dalarna"], ["达拉纳"], SVW + "Jerusalem_(roman)"),
    S("se-emig-s1", "the-emigrants", "se-ljuder", "Throughout", "全书",
      "Karl Oskar Nilsson and his wife Kristina struggle on a poor farm in Ljuder parish in Småland, where the soil is thin and the harvests fail. Around 1850 they sell up and, with others from the parish, sail from Karlshamn across the Atlantic to America.",
      "卡尔·奥斯卡·尼尔松和妻子克里斯蒂娜在斯莫兰柳德教区一座穷农庄上苦苦挣扎，那里土地贫瘠，年年歉收。1850 年前后，他们卖掉了家产，和教区里的另一些人一起从卡尔斯港乘船横渡大西洋去美国。",
      ["Ljuder"], ["柳德"], W + "The_Emigrants_(Moberg_novel)"),
    S("se-millennium-s1", "girl-with-the-dragon-tattoo", "se-mariaberget", "Part 1", "第一部",
      "Mikael Blomkvist, the journalist who publishes the magazine Millennium, has just lost a libel case. He lives alone in his top-floor flat at Bellmansgatan 1 on Södermalm, looking out over Gamla Stan, when an old industrialist hires him to find out what happened to his great-niece, who vanished decades before.",
      "出版《千禧年》杂志的记者米凯尔·布隆克维斯特刚刚输掉一场诽谤官司。他独自住在南岛贝尔曼街 1 号的顶楼公寓里，窗外就是老城；这时一位老实业家雇他去查清几十年前失踪的侄孙女究竟出了什么事。",
      ["Bellmansgatan 1"], ["贝尔曼街 1 号"], "https://visitstockholm.com/o/bellmansgatan-1"),
    S("se-wall-s1", "faceless-killers", "se-ystad", "Chapter 1", "第一章",
      "An old farming couple are found savagely attacked in their isolated farmhouse on the plain of Skåne; the man is dead and his wife, left with a noose round her neck, dies soon after. Kurt Wallander, a forty-two-year-old detective of the Ystad police, takes the case.",
      "斯科讷平原上一座偏僻的农舍里，一对年老的农民夫妇遭到残忍的袭击：丈夫已经死了，脖子上套着绞索的妻子不久也死去。四十二岁的于斯塔德警探库尔特·瓦兰德接手了这个案子。",
      ["Ystad"], ["于斯塔德"], W + "Faceless_Killers"),
    S("se-letright-s1", "let-the-right-one-in", "se-blackeberg", "Throughout", "全书",
      "In Blackeberg, a working-class suburb of Stockholm, in the early 1980s, Oskar, a bullied twelve-year-old, makes friends with Eli, the strange child who has just moved into the flat next door and who is a centuries-old vampire.",
      "八十年代初，斯德哥尔摩的工人住宅区布拉克贝里，受欺负的十二岁男孩奥斯卡，和刚搬进隔壁的怪孩子伊莱交上了朋友——伊莱是一个活了几百年的吸血鬼。",
      ["Blackeberg"], ["布拉克贝里"], W + "Let_the_Right_One_In_(novel)"),
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

HEAD = "// Sweden, hand-written content (tools/content/batches/add_se1.py, 2026-11-23).\n"
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
