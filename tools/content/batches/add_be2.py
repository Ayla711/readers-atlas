"""11-24: Belgium, second pack: books that selection rule v2 adds (tools/selection/be.md), as far as their places are found.
- Of Reynaert the Fox (c. 1250, public domain): a quotation from Dutch Wikisource, Vanden Vos Reynaerde/Deel V: in his lie
  about a plot against the king, the bear goes to Flanders and comes "in Waes, int soete lant". Place: the Waasland.
  orig_lang is "nl" because the app's language list has no Middle Dutch.
- Scene notes in our own words (in copyright): Cheese (Antwerp); Chapel Road (Ter-Muren and the Kapellekensbaan in
  Erembodegem, Aalst); La Comtesse des digues (Weert on the Scheldt); The Angel Maker (Wolfheim is invented; the
  Drielandenpunt on the Vaalserberg beside it is real and in the book); Austerlitz, already in the app (cz), gets the
  opening scene in Antwerp Centraal station.
Not added: The Misfortunates (Reetveerdegem is invented); Malpertuis (the town is not named, and no source found places the
house in Ghent); Happe-Chair (the novel's places, le Culot, la Californie, Saut-du-Leu, are local names not identified
with a real place in any source found). No photos yet.

Usage: python3 -I tools/content/batches/add_be2.py <app_dir> tools/content/batches/coords/add_be2.json <wikisource_root>"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b
import wikisource as ws

APP, CO, WSR = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8")), sys.argv[3]
DATE = "2026-11-24"
WS = "https://nl.wikisource.org/wiki/"
EXT = {"cz-austerlitz"}  # books already in the app (another country's books.js) that get a line here
def C(pid):
    c = CO[pid]; return c["lat"], c["lon"], c["st"], c["su"]
def BK(id, title, title_zh, title_orig, author, author_zh, author_orig, year, lang, aliases, pd=False, src=None):
    return dict(id=id, title=title, title_zh=title_zh, title_orig=title_orig, author=author, author_zh=author_zh, year=year,
                orig_lang=lang, public_domain=pd, source_url=src, author_orig=author_orig, aliases=aliases)
def ids_in(path): return set(re.findall(r'\{ id: "([^"]+)"', open(path, encoding="utf-8").read()))
def check(books, places, lines):
    allb = set()
    for f in glob.glob(os.path.join(APP, "data", "*", "books.js")): allb |= ids_in(f)
    assert not {x["id"] for x in books} & allb, {x["id"] for x in books} & allb
    assert EXT <= allb, EXT - allb
    assert not {p["id"] for p in places} & ids_in(b.data("places.js")) and {p["id"] for p in places} == set(CO)
    assert not {l["id"] for l in lines} & ids_in(b.data("lines.js"))
    bk = {x["id"] for x in books} | EXT
    for l in lines:
        assert l["book_id"] in bk and l["place_ids"][0] in {p["id"] for p in places}, l["id"]
    assert {l["book_id"] for l in lines} == bk
    assert {l["place_ids"][0] for l in lines} == {p["id"] for p in places}
def Q(id, book, place, loc, loc_zh, title, orig, hl_orig, en, hl_en, zh, hl_zh):
    assert "[" not in orig and "\xa0" not in orig, id
    assert orig.count("\n") == en.count("\n") == zh.count("\n"), id  # verse: one line of translation for each line
    for text, hls in ((orig, hl_orig), (en, hl_en), (zh, hl_zh)):
        for h in hls: assert h in text, (id, h)
    return dict(id=id, book_id=book, place_ids=[place], location=loc, location_zh=loc_zh, text_orig=orig, highlight_orig=hl_orig,
                text_en=en, highlight_en=hl_en, text_zh=zh, highlight_zh=hl_zh, translation="own", status="draft",
                checked=f"Dutch Wikisource, {title}, {DATE}")
b.init(APP, "", "be", DATE)
T_RE = "Vanden Vos Reynaerde/Deel V"
books = [
    BK("reynaert", "Of Reynaert the Fox", "列那狐", "Van den vos Reynaerde", "Willem die Madocke maecte", "威廉（《马多克》的作者）",
       "Willem die Madocke maecte", "c. 1250", "nl",
       ["Van den vos Reynaerde", "Vanden Vos Reynaerde", "Van den vos Reinaerde", "Reynard the Fox", "Reinaert", "Reynaert", "Kriekeputte"],
       pd=True, src=WS + "Vanden_Vos_Reynaerde"),
    BK("kaas", "Cheese", "奶酪", "Kaas", "Willem Elsschot", "威廉·埃尔斯霍特", "Willem Elsschot", "1933", "nl",
       ["Kaas", "Frans Laarmans", "Laarmans", "Edam", "Elsschot"]),
    BK("chapel-road", "Chapel Road", "小教堂路", "De Kapellekensbaan", "Louis Paul Boon", "路易·保罗·博恩", "Louis Paul Boon", "1953", "nl",
       ["De Kapellekensbaan", "Kapellekensbaan", "Ondineke", "Ondine", "Boontje", "Ter-Muren", "L. P. Boon"]),
    BK("comtesse-des-digues", "La Comtesse des digues", "堤坝伯爵夫人", "La Comtesse des digues", "Marie Gevers", "玛丽·热韦尔",
       "Marie Gevers", "1931", "fr", ["The Countess of the Dikes", "Suzanne Briat", "dijkgraaf", "Gevers"]),
    BK("angel-maker", "The Angel Maker", "天使制造者", "De engelenmaker", "Stefan Brijs", "斯特凡·布赖斯", "Stefan Brijs", "2005", "nl",
       ["De engelenmaker", "Victor Hoppe", "Wolfheim", "Brijs"]),
]
places = [
    b.ORIG("be-waasland", "Waasland", "瓦斯兰", *C("be-waasland"),
           "The “land of Waes” between Ghent and Antwerp. Of Reynaert the Fox (c. 1250) names real places of this corner of Flanders, and the Waasland plays a large part in Reynaert's great lie: condemned to the gallows, the fox saves himself with a story of a plot against King Noble hatched in Waes, “the sweet land”, and of a treasure hidden at Kriekeputte",
           "根特和安特卫普之间的“瓦斯之地”。《列那狐》（约 1250 年）写到了佛兰德这一带的许多真实地名，瓦斯兰在列那那个弥天大谎里分量很重：被判上绞架的狐狸编了一个故事来救自己的命——有人在“甜美的”瓦斯密谋杀害狮王诺布尔，还有一笔财宝藏在克里克普特"),
    b.ORIG("be-antwerp", "Antwerp", "安特卫普", *C("be-antwerp"),
           "Belgium's great port on the Scheldt, where Willem Elsschot was born and died. In Cheese (1933) Frans Laarmans, a clerk at an Antwerp shipyard company, becomes the agent for Dutch Edam and has to find a place to store it",
           "斯海尔德河上的比利时大港，威廉·埃尔斯霍特生于斯、卒于斯。《奶酪》（1933）里，安特卫普一家造船公司的小职员弗兰斯·拉尔曼斯当上了荷兰埃丹奶酪的代理商，还得给这批奶酪找个地方堆放"),
    b.ORIG("be-ter-muren", "Ter-Muren and the Kapellekensbaan, Erembodegem (Aalst)", "特尔穆伦与小教堂路，埃伦博德海姆（阿尔斯特）", *C("be-ter-muren"),
           "Hamlet in Erembodegem, on the edge of Aalst, where the Kapellekensbaan runs past the chapel of Our Lady of Ter Muren. Louis Paul Boon lived here for the last twenty-five years of his life; the chapel is a setting of De Kapellekensbaan (1953), and since 2024 Frans De Vree's statue of its heroine Ondineke stands on the Kapellekensbaan again",
           "阿尔斯特城边埃伦博德海姆的一个小村落，小教堂路从特尔穆伦圣母小教堂旁经过。路易·保罗·博恩人生的最后二十五年就住在这里；这座小教堂是《小教堂路》（1953）里的地点，2024 年起，弗兰斯·德·弗雷雕的女主人公翁迪内克像又回到了小教堂路边"),
    b.ORIG("be-weert", "Weert, Bornem", "韦尔特，博尔内姆", *C("be-weert"),
           "Village on the Scheldt in Klein-Brabant, its polders guarded by dikes and flooded more than once. Marie Gevers' first novel, La Comtesse des digues (1931), is set here: a year in the life of Suzanne Briat, the dike-reeve's daughter",
           "小布拉班特斯海尔德河边的村子，圩田靠堤坝守护，不止一次被水淹没。玛丽·热韦尔的第一部小说《堤坝伯爵夫人》（1931）就发生在这里，写的是堤坝总管的女儿苏珊娜·布里亚一年的生活"),
    b.ORIG("be-vaalserberg", "Drielandenpunt, Vaalserberg", "三国交界点，瓦尔瑟山", *C("be-vaalserberg"),
           "The hill where Belgium, Germany and the Netherlands meet. Wolfheim, the village of Stefan Brijs' The Angel Maker (2005), is invented and lies near the three-country point; the Drielandenpunt on the Vaalserberg is where the teacher secretly takes the triplets, and where the villagers walk the Way of the Cross at the end",
           "比利时、德国和荷兰三国交界的山丘。斯特凡·布赖斯《天使制造者》（2005）里的沃尔夫海姆村是虚构的，就在三国交界点附近；瓦尔瑟山上的三国交界点，是女教师偷偷带三胞胎去的地方，也是结尾村民们走苦路的地方"),
    b.ORIG("be-antwerpen-centraal", "Antwerpen-Centraal station", "安特卫普中央车站", *C("be-antwerpen-centraal"),
           "Antwerp's domed main station, beside the zoo. W. G. Sebald's Austerlitz (2001) opens here: in 1967 the narrator first meets Jacques Austerlitz in the waiting room, the Salle des pas perdus",
           "安特卫普带穹顶的中央车站，紧挨着动物园。塞巴尔德的《奥斯特利茨》（2001）从这里开始：1967 年，叙述者在候车大厅“失落脚步之厅”里第一次遇见雅克·奥斯特利茨"),
]
RE = ws.block(os.path.join(WSR, "nl"), T_RE, "Daer maecte hi hem te Vlaendren waert", "Ende quamen teene dorpe, hiet Hijfte.")
lines = [
    Q("be-re-1", "reynaert", "be-waasland", "Part V: Reynaert's lie about a plot against the king", "第五部分：列那编造的谋反故事", T_RE,
      RE, ["Waes"],
      "Then he set out for Flanders\nand came into Waes, the sweet land,\nwhere he found my father.\nMy father sent for Grimbeert the wise\nand Isengrim the grey;\nTibeert the cat made the fifth;\nand they came to a village called Hijfte.",
      ["Waes"],
      "于是他动身前往佛兰德，\n来到瓦斯，那甜美的地方，\n在那里找到了我父亲。\n我父亲请来聪明的格林贝尔特，\n还有灰毛的伊森格林，\n猫儿蒂贝尔特是第五个；\n他们来到一个叫海夫特的村子。",
      ["瓦斯"]),
    b.S("be-ka-1", "kaas", "be-antwerp", "The novel as a whole", "全书",
        "Antwerp. At his mother's funeral Frans Laarmans, a clerk at the General Marine and Shipbuilding Company, meets a highly placed friend of his brother's, and is soon general agent for Belgium and Luxembourg of a Dutch firm selling full-fat Edam. He takes unpaid sick leave from the office and puts all his care into every part of the new trade, the desk, the typewriter, the paperwork, except selling. Ten thousand cheeses arrive in 370 crates and go into the cellars of a warehouse; in the end he goes back to his old office, the cheese still in store.",
        "安特卫普。母亲的葬礼上，“通用海运造船公司”的小职员弗兰斯·拉尔曼斯结识了哥哥的一位有地位的朋友，没多久就当上了一家荷兰全脂埃丹奶酪公司在比利时和卢森堡的总代理。他向公司请了无薪病假，把心思花在新生意的每一样上——写字台、打字机、各种单据——唯独不花在推销上。一万个奶酪装在 370 只箱子里运到，进了仓库的地窖；到最后，他又回到了原来的办公室，奶酪还堆在仓库里。",
        ["Antwerp"], ["安特卫普"],
        "https://dbnl.org/tekst/_voo013200601_01/_voo013200601_01_0017.php; https://maken.wikiwijs.nl/bestanden/703770/Kaas.docx; https://www.goodreads.com/book/show/800279; https://bookbeat.com/it/book/kaas-1113599; https://www.publishersweekly.com/9781862074811; https://www.librarything.com/work/176319"),
    b.S("be-cr-1", "chapel-road", "be-ter-muren", "The novel as a whole", "全书",
        "Boon's “first illegal novel” is built of three layers. Printed in italics is the story of Ondineke, a working-class girl of Ter-Muren, a hamlet at the end of the Kapellekensbaan, the chapel lane that runs along the long wall of a blanket factory into the town of Aalst. It follows Ondine and her husband Oscar from the rise of Flemish socialism at the end of the nineteenth century to the Second World War, as Ondine gives in to the lure of a better, bourgeois life. Between its pieces the writer “Boontje” talks over the novel and the world after the war with his friends in his house on the Kapellekensbaan, and a third layer retells the tale of Reynaert the fox.",
        "博恩这部“第一部非法小说”由三层叙事搭成。用斜体印的是翁迪内克的故事：她是特尔穆伦一个工人家的女孩——特尔穆伦是小教堂路尽头的小村落，这条小路沿着一家毯子厂的长墙通往阿尔斯特城里。故事跟着翁迪内和她的丈夫奥斯卡，从十九世纪末佛兰德社会主义兴起一直写到第二次世界大战，翁迪内一步步屈从于更好的、资产阶级生活的诱惑。在这些片段之间，作家“小博恩”和朋友们在他小教堂路上的家里谈论这部小说和战后的世界；第三层则重讲列那狐的故事。",
        ["Kapellekensbaan", "Ter-Muren"], ["小教堂路", "特尔穆伦"],
        "https://dbnl.org/tekst/anbe001lexi01_01/lvlw00049.php; https://dbnl.org/tekst/_tir001198801_01/_tir001198801_01_0011.php; https://dbnl.org/tekst/_sep001198601_01/_sep001198601_01_0043.php; https://dbnl.org/tekst/_lit003200101_01/_lit003200101_01_0031.php; https://nl.wikipedia.org/wiki/De_Kapellekensbaan"),
    b.S("be-cd-1", "comtesse-des-digues", "be-weert", "The novel as a whole", "全书",
        "Flanders between the wars, in the village of Weert on the Scheldt, where dikes protect the polders and the river is king. Suzanne Briat, an only child, loses her father Jules, the dike-reeve (dijkgraaf, the “count of the dikes”), who chaired the council that inspects and keeps up the dikes. She knows the work well, but no woman has ever held the post. Over one year, pressed by her aunt to marry, she is drawn to Triphon, a strong, handsome worker kept from her by class, and to Max Larix, an untidy outsider who loves nature and sings; the book closes with his love song.",
        "两次大战之间的佛兰德，斯海尔德河边的韦尔特村，堤坝守护着圩田，大河就是这里的王。独生女苏珊娜·布里亚失去了父亲朱尔——他是堤坝总管（dijkgraaf，“堤坝伯爵”），主持负责巡查和养护堤坝的委员会。苏珊娜对这份工作很熟，可还从没有女人担任过这个职位。一年当中，姑妈催她嫁人，她先是被特里丰吸引——一个强壮英俊的工人，却因阶级之隔可望而不可即；后来又被马克斯·拉里克斯吸引——一个邋遢、热爱自然、爱唱歌的外来人。全书以他的情歌作结。",
        ["Weert"], ["韦尔特"],
        "https://www.espacenord.com/wp-content/uploads/2021/06/dp_comtesse_des_digues_def_def.pdf; https://orbi.umons.ac.be/bitstream/20.500.12907/44106/1/4_lievois_gravet.pdf; https://is.muni.cz/el/phil/podzim2015/FJ0B622/59300538/Partie_III_chapitre_4.pdf; https://www.universalis.fr/encyclopedie/marie-gevers/"),
    b.S("be-am-1", "angel-maker", "be-vaalserberg", "The novel as a whole", "全书",
        "On 13 October 1984, after almost twenty years away, Doctor Victor Hoppe returns to Wolfheim, the village near the three-country point where his father was the doctor, with newborn identical triplets, Michael, Gabriel and Raphael. The villagers are suspicious; slowly it emerges that all three boys are seriously ill, and that Hoppe, who wanted to outdo God, has made them by cloning himself. While he is away at a medical fair, the boys' teacher Charlotte Maenhout secretly takes them on an outing to the Drielandenpunt on the Vaalserberg, which ends in a fiasco. At the end, while the villagers follow the Way of the Cross on the Vaalserberg, Hoppe nails himself to a cross.",
        "1984 年 10 月 13 日，离开将近二十年之后，维克托·霍普医生回到三国交界点附近的沃尔夫海姆村——他父亲当年就是这里的医生。他带回一组刚出生的同卵三胞胎：米迦勒、加百列和拉斐尔。村民们满腹狐疑；渐渐地人们发现，三个孩子都病得很重，而一心要“跟上帝比个高低”的霍普，是用克隆自己的办法造出了他们。趁他去参加医学博览会，孩子们的女教师夏洛特·门豪特偷偷带他们去瓦尔瑟山上的三国交界点游玩，结果一败涂地。结尾，村民们在瓦尔瑟山上走苦路的时候，霍普把自己钉上了十字架。",
        ["Vaalserberg"], ["瓦尔瑟山"],
        "https://dbnl.org/tekst/anbe001lexi01_01/lvlw00077.php; https://dbnl.org/tekst/_ons003200601_01/_ons003200601_01_0067.php; https://neerlandistiek.nl/2024/03/het-eerste-kwart-stefan-brijs-de-engelenmaker; https://maken.wikiwijs.nl/bestanden/666049/leesverslag%20De%20Engelenmaker.docx; https://maken.wikiwijs.nl/bestanden/672486/De%20Engelenmaker%20Stefan%20de%20Brijs%20bookreport.docx"),
    b.S("be-au-1", "cz-austerlitz", "be-antwerpen-centraal", "The opening", "开篇",
        "Summer 1967. The narrator, on one of his journeys from England to Belgium, arrives in Antwerp feeling unwell, spends an afternoon in the Nocturama of the zoo beside the station, and then walks into the great hall of the Centraal Station under its dome sixty metres high. In the waiting room, the Salle des pas perdus, one traveller is not staring into space but sketching and taking notes: Jacques Austerlitz, an architectural historian. Their talk continues in the station buffet under its great clock, about the station as a show of Belgium's colonial confidence and about the history of fortification. It is the first of the meetings, over some thirty years, in which Austerlitz slowly tells his story.",
        "1967 年夏天。叙述者又一次从英国到比利时旅行，到安特卫普时身体不适，在车站旁边动物园的夜行动物馆里待了一个下午，然后走进中央车站那座穹顶高六十米的大厅。在候车大厅“失落脚步之厅”里，有一个旅客没有呆呆地望着前方，而是在画速写、记笔记——他就是建筑史学者雅克·奥斯特利茨。两人在车站餐厅那座大钟下面接着聊：聊这座车站如何炫耀比利时的殖民自信，聊要塞的历史。这是两人前后三十来年一次次会面的开始，奥斯特利茨在这些会面里慢慢讲出了自己的身世。",
        ["Centraal Station"], ["中央车站"],
        "https://press.uchicago.edu/Misc/Chicago/795409.html; https://www.supersummary.com/austerlitz/pages-21-50-summary; https://www.lrb.co.uk/v33/n19/james-wood/sent-east; https://kosmopolis.cccb.org/en/?p=1684; https://en.wikipedia.org/wiki/Austerlitz_(novel)"),
]
check(books, places, lines)
if __name__ == "__main__":
    M = "11-24: second pack, books added under selection rule v2 (tools/content/batches/add_be2.py)"
    b.append(b.data("books.js"), books, M); b.append(b.data("places.js"), places, M); b.append(b.data("lines.js"), lines, M)
    print(len(books), "books,", len(places), "places,", len(lines), "lines")
