"""11-23: the Netherlands, first pack: 12 new books, 13 places. Multatuli's Lauriergracht, Hildebrand's Haarlemmerhout,
Dumas at the Gevangenpoort, the Hero of Haarlem at Spaarndam, Anne Frank's Prinsengracht, Mulisch's Haarlem, Chevalier's
Delft, Camus's Amsterdam, Burton's Golden Bend, and three writers' places: Vondel's park, Spinoza's last house and
Couperus's street in The Hague; Erasmus (The Praise of Folly, from the Swiss pack) gets his statue in Rotterdam.

Quotations (4 lines) are cut from Dutch, French and English Wikisource pages (tools/content/wikisource.py); translations
of the Dutch and French are our own drafts (translation: "own"). Books in copyright, and PD books whose text we did not
reach, have scene notes in our own words or hang on a writer's place. What a cut changes, named in `checked`:
hard-wrapped lines are re-flowed, doubled spaces written as one; the Camera Obscura cut is one sentence from the middle
of a paragraph.

Coordinates are those of the place's Dutch Wikipedia article (cache/nl/coords.json); the Erasmus statue has none of its
own, so its pin is the Laurenskerk, in front of which it stands.

Usage: python3 -I add_nl1.py <app_dir> <coords.json> <wikisource_root>"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b
import wikisource as ws

APP, CO, WSR = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8")), sys.argv[3]
DATE = "2026-11-23"
b.init(APP, "", "nl", DATE)
W = b.W
NLW = "https://nl.wikipedia.org/wiki/"

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

T_MH, T_CO = "Max Havelaar/EERSTE HOOFDSTUK", "Camera Obscura/Een onaangenaam mens in de Haarlemmerhout"
T_TN, T_HB = "La Tulipe noire/I", "Hans Brinker, or The Silver Skates/Friends in Need"
EXIST = {"praise-of-folly"}

books = [
    BK("max-havelaar", "Max Havelaar", "马格斯·哈弗拉尔", "Max Havelaar, of de koffi-veilingen der Nederlandsche Handel-Maatschappy",
       "Multatuli", "穆尔塔图里", "Multatuli", "1860", src=ws.url("nl", "Max Havelaar"),
       aliases=["Batavus Droogstoppel", "Lauriergracht", "Lebak", "Eduard Douwes Dekker", "Last & Co"]),
    BK("camera-obscura", "Camera Obscura", "暗箱", "Camera Obscura", "Hildebrand (Nicolaas Beets)", "希尔德布兰德（尼古拉斯·贝茨）", "Hildebrand",
       "1839", src=ws.url("nl", "Camera Obscura"), aliases=["Hildebrand", "Nicolaas Beets", "Nurks", "Haarlemmerhout"]),
    BK("black-tulip", "The Black Tulip", "黑郁金香", "La Tulipe noire", "Alexandre Dumas", "大仲马", "Alexandre Dumas", "1850", lang="fr",
       src=ws.url("fr", "La Tulipe noire"), aliases=["La Tulipe noire", "Cornelius van Baerle", "Rosa", "De Witt", "Haarlem"]),
    BK("hans-brinker", "Hans Brinker, or The Silver Skates", "银冰鞋", "Hans Brinker, or The Silver Skates", "Mary Mapes Dodge", "玛丽·梅普斯·道奇",
       "Mary Mapes Dodge", "1865", lang="en", src=ws.url("en", "Hans Brinker, or The Silver Skates"),
       aliases=["The Silver Skates", "Hans Brinker", "Gretel", "The Hero of Haarlem", "Hansje Brinker", "汉斯·布林克"]),
    BK("gijsbrecht", "Gysbreght van Aemstel", "阿姆斯特尔的海斯布雷赫特", "Gysbreght van Aemstel", "Joost van den Vondel", "冯德尔",
       "Joost van den Vondel", "1637", aliases=["Gijsbrecht van Aemstel", "Vondel", "Badeloch"]),
    BK("diary-of-anne-frank", "The Diary of a Young Girl", "安妮日记", "Het Achterhuis", "Anne Frank", "安妮·弗兰克", "Anne Frank", "1947", pd=False,
       aliases=["Het Achterhuis", "Diary of Anne Frank", "Kitty", "Secret Annex", "Prinsengracht 263"]),
    BK("the-assault", "The Assault", "袭击", "De aanslag", "Harry Mulisch", "哈里·穆里施", "Harry Mulisch", "1982", pd=False,
       aliases=["De aanslag", "Anton Steenwijk", "Fake Ploeg", "Haarlem"]),
    BK("girl-with-a-pearl-earring", "Girl with a Pearl Earring", "戴珍珠耳环的少女", "Girl with a Pearl Earring", "Tracy Chevalier", "特蕾西·雪佛兰",
       "Tracy Chevalier", "1999", lang="en", pd=False, aliases=["Griet", "Vermeer", "Delft"]),
    BK("the-fall-camus", "The Fall", "堕落", "La Chute", "Albert Camus", "加缪", "Albert Camus", "1956", lang="fr", pd=False,
       aliases=["La Chute", "Clamence", "Mexico City", "Amsterdam"]),
    BK("the-miniaturist", "The Miniaturist", "微缩模型师", "The Miniaturist", "Jessie Burton", "杰西·伯顿", "Jessie Burton", "2014", lang="en", pd=False,
       aliases=["Nella Oortman", "Johannes Brandt", "Herengracht", "Golden Bend", "Het huis aan de Gouden Bocht"]),
    BK("eline-vere", "Eline Vere", "埃莉娜·维尔", "Eline Vere", "Louis Couperus", "路易·库佩鲁斯", "Louis Couperus", "1889", aliases=["Couperus", "Den Haag", "Betsy", "Henk van Raat"]),
    BK("ethics-spinoza", "Ethics", "伦理学", "Ethica, ordine geometrico demonstrata", "Baruch Spinoza", "斯宾诺莎", "Benedictus de Spinoza", "1677",
       lang="la", aliases=["Ethica", "Spinoza", "Opera Posthuma"]),
]

places = [
    ORIG("nl-lauriergracht", "Lauriergracht, Amsterdam", "劳里尔运河，阿姆斯特丹",
         "Canal in the Jordaan, Amsterdam. Max Havelaar opens with the coffee broker Batavus Droogstoppel telling us he lives at Lauriergracht No. 37; beside the front door of No. 37 there now hangs a sign with the name of his fictional firm, 'Last & Co'",
         "阿姆斯特丹约旦区的一条运河。《马格斯·哈弗拉尔》开篇，咖啡经纪人巴达维斯·德罗赫斯托佩尔告诉读者，他住在劳里尔运河 37 号；如今 37 号门边挂着一块牌子，写着他那家虚构的经纪行的名字“拉斯特公司”"),
    ORIG("nl-haarlemmerhout", "Haarlemmerhout, Haarlem", "哈勒姆林苑，哈勒姆",
         "The oldest city wood in the Netherlands, at Haarlem. In Camera Obscura, Hildebrand has to spend a Sunday in July here with his tiresome cousin Nurks from Amsterdam. The Hildebrand monument, a fountain with figures from the book and Beets himself, has stood in the wood since 1962; it was restored with durable replicas on 13 September 2014, Beets's 200th birthday",
         "荷兰最古老的城市森林，在哈勒姆。《暗箱》里，希尔德布兰德不得不陪着从阿姆斯特丹来的讨厌表兄努尔克斯在这里过一个七月的星期天。林中的希尔德布兰德纪念喷泉自 1962 年起立在这里，雕像是书中的人物和贝茨本人；2014 年 9 月 13 日，贝茨两百周年诞辰那天，雕像以耐久材料的复制品修复一新"),
    ORIG("nl-gevangenpoort", "Gevangenpoort, The Hague", "监狱门，海牙",
         "Medieval gatehouse prison by the Binnenhof in The Hague, a museum since 1882. Its most famous prisoner was Cornelis de Witt; on 20 August 1672 he and his brother Johan were lynched by the mob in front of its door. The Black Tulip opens with the crowd running towards the prison that day; Dumas calls it the Buytenhof, after the square it stands on",
         "海牙国会大厦旁的中世纪城门监狱，1882 年起成为博物馆。这里最有名的囚犯是科内利斯·德·维特：1672 年 8 月 20 日，他和弟弟约翰在监狱门前被暴民私刑处死。《黑郁金香》开篇就是那天涌向这座监狱的人群；大仲马用它所在的广场名把它叫作“比顿霍夫”"),
    ORIG("nl-spaarndam", "Spaarndam (the Hero of Haarlem)", "斯帕伦丹（哈勒姆的英雄）",
         "Village at the mouth of the Spaarne on the IJ, half of it in the municipality of Haarlem. On the IJdijk stands a little statue of 'The Hero of Haarlem (Hansje Brinker)', the boy from an American book who saved the land by putting his finger in a hole in the dike; the local tourist office put it there. In Hans Brinker the story is read aloud in an English schoolroom",
         "斯帕讷河注入艾湖处的村庄，一半属于哈勒姆市。艾堤上立着一尊小雕像《哈勒姆的英雄（汉斯·布林克）》——这个来自一本美国书的男孩把手指塞进堤上的洞，救了整片土地；雕像是当地旅游局立的。在《银冰鞋》里，这个故事是在英国的一间教室里被朗读出来的"),
    ORIG("nl-anne-frank", "Anne Frank House, Amsterdam", "安妮·弗兰克之家，阿姆斯特丹",
         "Prinsengracht 263, where Otto Frank's businesses had their offices from 1 December 1940 and where the Frank family hid in the annex behind from 6 July 1942. The museum around it opened on 3 May 1960; the Westertoren beside it plays an important part in Anne's diary",
         "王子运河 263 号。1940 年 12 月 1 日起，奥托·弗兰克的公司在这里办公；1942 年 7 月 6 日起，弗兰克一家躲进了后面的密室。围绕它建起的博物馆 1960 年 5 月 3 日开放；旁边的西教堂钟楼在安妮的日记里占有重要的位置"),
    ORIG("nl-haarlem", "Haarlem", "哈勒姆",
         "City in North Holland. The Assault begins in 1945 on a quay at the edge of Haarlem, where the Steenwijk family lives; years later Anton comes back to the empty plot, where a monument to the attack now stands",
         "北荷兰省的城市。《袭击》的故事从 1945 年哈勒姆城边一条河岸街开始，施泰恩韦克一家就住在那里；多年以后，安东回到那块空地，那里已经立起了纪念那次袭击的碑"),
    ORIG("nl-delft", "Markt, Delft", "德尔夫特集市广场",
         "The market square at the heart of Delft, the city of the painter Johannes Vermeer. Girl with a Pearl Earring is set in Delft in 1664, where the young Griet goes to work in Vermeer's house",
         "德尔夫特城中心的集市广场，这是画家维米尔的城市。《戴珍珠耳环的少女》的故事发生在 1664 年的德尔夫特，年轻的格里特到维米尔家去做女仆"),
    ORIG("nl-wallen", "De Wallen, Amsterdam", "红灯区（德瓦伦），阿姆斯特丹",
         "Amsterdam's red-light district, in the oldest part of the city between the Zeedijk and Nieuwmarkt and the Warmoesstraat. Camus's The Fall is told night after night in a bar here called Mexico City, which its narrator places in the last circle of Amsterdam's canals",
         "阿姆斯特丹的红灯区，在城里最古老的一片，夹在海堤街、新市场和瓦尔莫斯街之间。加缪的《堕落》就是一夜又一夜在这里一家叫“墨西哥城”的酒吧里讲出来的，叙述者说这里是阿姆斯特丹运河一圈圈环线的最后一圈"),
    ORIG("nl-herengracht", "Golden Bend, Herengracht, Amsterdam", "绅士运河黄金弯，阿姆斯特丹",
         "The stretch of the Herengracht in Amsterdam known as the Golden Bend (Gouden Bocht). In The Miniaturist the merchant Johannes Brandt's house stands here; the Dutch translation is called Het huis aan de Gouden Bocht. The novel was inspired by Petronella Oortman's doll's house in the Rijksmuseum",
         "阿姆斯特丹绅士运河上被称作“黄金弯”的一段。《微缩模型师》里，商人约翰内斯·勃兰特的宅子就在这里，荷兰文译本的书名就叫《黄金弯上的房子》。小说的灵感来自国家博物馆里佩特罗内拉·奥尔特曼的玩偶屋"),
    PIL("nl-vondelpark", "Vondelpark, Amsterdam", "冯德尔公园，阿姆斯特丹",
        "Amsterdam's city park, first opened on 15 June 1865 as the New Park. It took Vondel's name through the architect Pierre Cuypers, who had campaigned since 1862 for a statue of the poet and designed the pedestal of the Vondel monument, unveiled here in October 1867. Vondel's Gysbreght van Aemstel, written for the opening of Amsterdam's first stone theatre, was first staged on 3 January 1638; from 1641 it was played in Amsterdam almost every year, at first as a Christmas play and from the 19th century at New Year, a custom that lasted until 1968",
        "阿姆斯特丹的城市公园，1865 年 6 月 15 日首次开放，当时叫“新公园”。它得名冯德尔，要归功于建筑师皮埃尔·奎珀斯：他从 1862 年起就奔走为这位诗人立像，还设计了 1867 年 10 月在园中揭幕的冯德尔纪念像的基座。冯德尔的《阿姆斯特尔的海斯布雷赫特》是为阿姆斯特丹第一座石砌剧院的开幕而写的，1638 年 1 月 3 日首演；从 1641 年起，它几乎每年都在阿姆斯特丹上演，起初是圣诞戏，19 世纪起改为新年首演，这个传统一直延续到 1968 年",
        ["gijsbrecht"]),
    PIL("nl-spinozahuis", "Domus Spinozana, The Hague", "斯宾诺莎故居，海牙",
        "Paviljoensgracht 72, The Hague, the house of Hendrik van der Spyk, where Spinoza lodged in the last years of his life and died in 1677. His Ethics, which he had held back from print, was published by his friends in Amsterdam in the year of his death",
        "海牙帕维永运河 72 号，亨德里克·范·德·斯派克的房子。斯宾诺莎生命的最后几年寄住在这里，1677 年在此去世。他一直没有付印的《伦理学》，在他去世那年由朋友们在阿姆斯特丹出版",
        ["ethics-spinoza"]),
    PIL("nl-archipelbuurt", "Archipelbuurt (Couperus's Surinamestraat), The Hague", "群岛区（库佩鲁斯的苏里南街），海牙",
        "Quarter of The Hague where Couperus's father had a house built at Surinamestraat 20 in 1883; on its first floor Louis Couperus wrote his first novel, Eline Vere (1889), the story of a young woman of Hague society who lives with her sister Betsy and Betsy's husband Henk van Raat. A bust of Couperus has stood at the start of the street since 1963",
        "海牙的一个街区。1883 年，库佩鲁斯的父亲在苏里南街 20 号盖了一座房子，路易·库佩鲁斯就在它的二楼写出了第一部小说《埃莉娜·维尔》（1889）——写一个海牙上流社会的年轻女子，和姐姐贝特西、姐夫亨克·范·拉特住在一起。街口自 1963 年起立着一尊库佩鲁斯的胸像",
        ["eline-vere"]),
    PIL("nl-erasmus", "Erasmus statue, Laurenskerk, Rotterdam", "伊拉斯谟像，圣劳伦斯教堂，鹿特丹",
        "Hendrick de Keyser's bronze Erasmus, unveiled on 30 April 1622 and the oldest statue in the Netherlands, shows him reading a book. It first stood on the Grote Markt and since 1964 has stood on the square in front of the Laurenskerk. Erasmus was born in Rotterdam around 1466, though he lived there for only four years",
        "亨德里克·德·凯泽塑造的伊拉斯谟铜像，1622 年 4 月 30 日揭幕，是荷兰最古老的雕像，表现他正在读书。它起初立在大集市广场，1964 年起移到圣劳伦斯教堂前的广场上。伊拉斯谟约 1466 年生于鹿特丹，不过他在这里只住过四年",
        ["praise-of-folly"]),
]

_tn = raw(T_TN, "Le 20 août 1672,", "grand pensionnaire de Hollande.", "fr")
lines = [
    Q("nl-mh-1", "max-havelaar", "nl-lauriergracht", "Chapter 1, opening", "第一章开头", T_MH,
      raw(T_MH, "Ik ben makelaar in koffi,", "of als ge wat anders zyt."), ["Lauriergracht"],
      "I am a coffee broker, and live on the Lauriergracht, No. 37. It is not my habit to write novels, or such things, and so it was a long time before I brought myself to order a couple of extra reams of paper and begin the work which you, dear reader, have just taken in hand, and which you must read whether you are a coffee broker or whether you are something else.",
      ["Lauriergracht"],
      "我是咖啡经纪人，住在劳里尔运河 37 号。写小说或者诸如此类的东西，不是我的习惯；所以我拖了好久，才下决心多订了几令纸，动手写这部作品——亲爱的读者，你刚刚把它拿在手里，不管你是咖啡经纪人，还是干别的什么的，你都非读不可。",
      ["劳里尔运河"]),
    Q("nl-co-1", "camera-obscura", "nl-haarlemmerhout", "'An Unpleasant Man in the Haarlemmerhout'", "《哈勒姆林苑里一个讨厌的人》", T_CO,
      raw(T_CO, "Maar de steen uit Amsterdam", "komt alleen in den Hout."), ["den Hout"],
      "But the stone from Amsterdam shattered all those delights, and the whole plan had to be put off, under the thought, dreadful to us, of sitting the whole day in the Hout; for a respectable Amsterdammer comes only to the Hout.",
      ["the Hout"],
      "可是从阿姆斯特丹捎来的那块石头把这一切美事都砸碎了，整个计划只好推迟，我们还得面对一个可怕的念头：要在林苑里坐上一整天；因为一个体面的阿姆斯特丹人只到林苑来。",
      ["林苑"], note=" (one sentence from the middle of a paragraph; the cousin's letter came tied to a stone)"),
    Q("nl-tn-1", "black-tulip", "nl-gevangenpoort", "Chapter 1, opening", "第一章开头", T_TN, _tn, ["la Haye", "Buytenhof"],
      "On 20 August 1672 the city of The Hague, so lively, so white, so trim that one would think every day was Sunday; the city of The Hague, with its shady park, with its great trees leaning over its Gothic houses, with the broad mirrors of its canals in which its steeples with their almost oriental domes are reflected; the city of The Hague, capital of the Seven United Provinces, was swelling all its arteries with a black and red flood of hurried, breathless, anxious citizens, who ran, knife at the belt, musket on the shoulder or stick in hand, towards the Buytenhof, a formidable prison whose barred windows are still shown today, and where, since the charge of murder brought against him by the surgeon Tychelaer, Cornelius de Witt, brother of the former Grand Pensionary of Holland, had lain languishing.",
      ["The Hague", "Buytenhof"],
      "1672 年 8 月 20 日，海牙城——这座城那么生气勃勃、那么洁白、那么俏丽，让人觉得天天都是星期日；海牙城，有它绿荫浓密的林苑，有它那些俯向哥特式房屋的大树，有它那些宽阔如镜的运河，映出一座座几乎带着东方风味的圆顶钟楼；海牙城，七省联合共和国的首都——这一天，它的每一条血管都涨满了黑红色的人流：市民们匆忙、喘息、不安，腰里别着刀，肩上扛着火枪，或是手里拿着棍子，向比顿霍夫奔去。那是一座森严的监狱，至今人们还会指给你看它那些装着铁栅的窗户；自从外科医生蒂克拉尔控告他谋杀以来，荷兰前大议长的哥哥科内利乌斯·德·维特就一直被关在里面受苦。",
      ["海牙", "比顿霍夫"], site="French"),
    EN("nl-hb-1", "hans-brinker", "nl-spaarndam", "Chapter 18, 'Friends in Need': the schoolroom reading of 'The Hero of Haarlem'",
       "第十八章《患难之交》：课堂上朗读的《哈勒姆的英雄》", T_HB,
       flow(raw(T_HB, "Quick as a flash, he saw his duty.", "shall not be drowned while I am here!", "en")),
       ["Haarlem"],
       "他一下子就明白了自己该做什么。他扔掉花，爬上堤坡，一直爬到那个洞跟前。几乎还没意识到，他那胖乎乎的小手指就已经塞了进去。水不流了！啊！他想着，孩子气地得意一笑，这下那些发怒的水只好待在外头了！只要我在这儿，哈勒姆就淹不了！",
       ["哈勒姆"], note=" (the page's line ends joined, doubled spaces written as one)"),
]
lines += [
    S("nl-af-s1", "diary-of-anne-frank", "nl-anne-frank", "Throughout", "全书",
      "Anne Frank is given a red-checked diary for her thirteenth birthday on 12 June 1942 and writes it as letters to 'Kitty'. On 6 July 1942 the family goes into hiding in the secret annex behind her father's business at Prinsengracht 263, where they stay for two years until they are discovered on 4 August 1944.",
      "1942 年 6 月 12 日，安妮·弗兰克十三岁生日那天得到一本红格子日记本，她把日记写成给“基蒂”的信。1942 年 7 月 6 日，全家躲进了父亲公司所在的王子运河 263 号后面的密室，在那里藏了两年，直到 1944 年 8 月 4 日被发现。",
      ["Prinsengracht 263"], ["王子运河 263 号"], NLW + "Het_Achterhuis_(dagboek)"),
    S("nl-assault-s1", "the-assault", "nl-haarlem", "Opening", "开篇",
      "Near the end of the war, in 1945, Fake Ploeg, a Dutch Nazi working for the police, is shot outside the neighbours' house on a quay at the edge of Haarlem. The neighbours drag the body in front of the Steenwijks' house; the Germans burn it down and execute Anton's parents. Years later Anton comes back to the empty plot, where a monument to the attack now stands.",
      "战争快结束时的 1945 年，替警察做事的荷兰纳粹党人法克·普洛赫在哈勒姆城边一条河岸街上、邻居家门前被枪杀。邻居把尸体拖到了施泰恩韦克家门口；德国人烧了他们的房子，处决了安东的父母。多年以后，安东回到那块空地，那里已经立起了纪念那次袭击的碑。",
      ["Haarlem"], ["哈勒姆"], NLW + "De_aanslag_(roman)"),
    S("nl-pearl-s1", "girl-with-a-pearl-earring", "nl-delft", "Throughout", "全书",
      "In 1664, sixteen-year-old Griet has to leave her family home in Delft after her father, a tile painter, is blinded in an accident, and she is found a place as a maid in the household of the painter Johannes Vermeer.",
      "1664 年，做瓷砖画匠的父亲在一次事故中失明，十六岁的格里特不得不离开德尔夫特的家，到画家约翰内斯·维米尔家里做女仆。",
      ["Delft"], ["德尔夫特"], W + "Girl_with_a_Pearl_Earring_(novel)"),
    S("nl-fall-s1", "the-fall-camus", "nl-wallen", "Throughout", "全书",
      "Night after night in a bar called Mexico City, in Amsterdam's red-light district, Jean-Baptiste Clamence, once a respected Paris defence lawyer, makes his confession to a stranger from Paris. He likens the city's concentric canals to the circles of hell, and says the quarter they are sitting in is the last circle.",
      "在阿姆斯特丹红灯区一家叫“墨西哥城”的酒吧里，曾是巴黎名律师的让-巴蒂斯特·克拉芒斯一夜又一夜地向一个同样来自巴黎的陌生人忏悔。他把这座城一圈圈的同心运河比作地狱的一层层，说他们坐着的这一片就是最后一层。",
      ["red-light district"], ["红灯区"], W + "The_Fall_(Camus_novel)"),
    S("nl-mini-s1", "the-miniaturist", "nl-herengracht", "Throughout", "全书",
      "On an October day in 1686, eighteen-year-old Nella Oortman from Assendelft comes to the Herengracht house of her new husband, the merchant Johannes Brandt. He gives her a cabinet house, a replica of their home, and the miniaturist she hires to furnish it begins to send pieces that seem to foretell what will happen.",
      "1686 年十月的一天，来自阿森德尔夫特的十八岁的内拉·奥尔特曼来到新婚丈夫、商人约翰内斯·勃兰特在绅士运河上的宅子。他送给她一座柜式玩偶屋，是他们这座宅子的复制品；她雇来布置玩偶屋的微缩模型师开始寄来一件件物件，仿佛在预示将要发生的事。",
      ["Herengracht"], ["绅士运河"], "https://www.bookbrowse.com/excerpts/index.cfm/book_number/3104/the-miniaturist"),
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

HEAD = "// The Netherlands, hand-written content (tools/content/batches/add_nl1.py, 2026-11-23).\n"
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
