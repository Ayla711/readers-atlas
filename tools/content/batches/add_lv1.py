"""11-26: Latvia, the 7 books the user chose (the Latvian works in the Top 21 of the 2014 "Lielā lasīšana" reader vote;
tools/selection/lv.md). Latvia opens with this batch. The Kitten's Mill (1913) is out of copyright, but its tale names no
place and no free text of it was found, so it has no line, only Skalbe's memorial museum. The others are in copyright and
get scene notes in our own words. Clearers of Fate has no line either: the Nārbuļi farm of the novels has no real place;
the television series made from them was filmed in Liezēre parish (film location). Places, with the reason for each:
- Saulrieti, Vecpiebalga parish (pilgrimage): Skalbe's summer house, now the Kārlis Skalbe memorial museum.
- Ragaciems (pilgrimage): Ziedonis was born in Ragaciems in 1933 and is buried in its cemetery.
- Ložmetējkalns: the second part of Blizzard of Souls gives the Christmas Battles of 1916–17 particular attention; the
  Christmas Battles Museum (Mangaļi), where the film's battle scenes were shot, stands in this battlefield.
- Grīziņkalns, Riga: Bille's childhood passes in a narrow flat of a Vārnu Street courtyard house in Grīziņkalns.
- Sakstagals (A-24): The Child of Man is set on an unnamed Latgale farmstead; Klīdzējs grew up nearby and went to the
  Sakstagals school, now named after him.
- Lejasciems: Sakse's birthplace, where on a Midsummer eve the night violets gave her the first of the flower tales.
- Liezēre (film location, television series): the series was filmed at the "Kalna Jaunzemji" farm in Liezēre parish; the
  pin is the parish centre, as the farm has no published coordinates.
The map of Latvia (data/lv/geo.js) is built from geoBoundaries LVA ADM1 (Geoportal of Latvia, 2021, CC BY 4.0), the 43
units of the 2021 reform, with Varakļāni merged into Madona (1 July 2025): 35 municipalities and 7 state cities.
Usage: python3 -I tools/content/batches/add_lv1.py <app_dir> tools/content/batches/coords/add_lv1.json"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b

APP, CO = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8"))
DATE = "2026-11-26"
b.init(APP, "", "lv", DATE)
def C(pid):
    c = CO[pid]; return c["lat"], c["lon"], c["st"], c["su"]
def BK(id, title, title_zh, title_orig, author, author_zh, year, aliases, pd=False):
    return dict(id=id, title=title, title_zh=title_zh, title_orig=title_orig, author=author, author_zh=author_zh, year=year,
                orig_lang="lv", public_domain=pd, source_url=None, aliases=aliases)

books = [
    BK("kakisa-dzirnavas", "The Kitten's Mill", "小猫的磨坊", "Kaķīša dzirnavas", "Kārlis Skalbe", "卡尔利斯·斯卡尔贝", "1913",
       ["Kaķīša dzirnavas", "Ziemas pasakas", "Puss's Water Mill"], pd=True),
    BK("liktena-lidumnieki", "Clearers of Fate", "命运的开拓者", "Likteņa līdumnieki", "Vladimirs Kaijaks", "弗拉季米尔斯·凯亚克斯", "1999",
       ["Likteņa līdumnieki", "Enijas bize", "Zem Marsa debesīm", "Nārbuļu dēli", "Mantinieki", "Nārbuļi"]),
    BK("epifanijas", "Epiphanies", "顿悟", "Epifānijas", "Imants Ziedonis", "伊曼茨·齐耶多尼斯", "1971", ["Epifānijas"]),
    BK("dveselu-putenis", "Blizzard of Souls", "灵魂的暴风雪", "Dvēseļu putenis", "Aleksandrs Grīns", "亚历山大斯·格林斯", "1933",
       ["Dvēseļu putenis", "The Rifleman", "Artūrs Vanags"]),
    BK("bille", "Bille", "比勒", "Bille", "Vizma Belševica", "维兹玛·贝尔舍维察", "1992", ["Bille", "Bille un karš", "Billes skaistā jaunība"]),
    BK("cilveka-berns", "The Child of Man", "人之子", "Cilvēka bērns", "Jānis Klīdzējs", "亚尼斯·克利杰伊斯", "1956",
       ["Cilvēka bērns", "Cylvāka bārns", "Boņuks"]),
    BK("pasakas-par-ziediem", "Fairy Tales about Flowers", "花的童话", "Pasakas par ziediem", "Anna Sakse", "安娜·萨克塞", "1966",
       ["Pasakas par ziediem", "Naktsvijole"]),
]

places = [
    b.PIL("lv-saulrieti", "Saulrieti, Vecpiebalga", "韦茨皮耶巴尔加的绍尔列蒂", *C("lv-saulrieti"),
        "Kārlis Skalbe's summer house in Vecpiebalga parish, the parish where he was born in 1879; it is now his memorial museum, and his grave is nearby. His fairy tale The Kitten's Mill, from the collection Ziemas pasakas (1913), named in the Latvian Cultural Canon, won the phone vote of the 2014 Big Read as the nation's favourite book",
        "卡尔利斯·斯卡尔贝在韦茨皮耶巴尔加乡的夏日别墅，他 1879 年就生在这个乡；别墅如今是他的纪念馆，他的墓就在附近。他的童话《小猫的磨坊》收在被列入拉脱维亚文化正典的《冬天的童话》（1913）里，2014 年“大阅读”电话投票中当选全国最喜爱的书",
        ["kakisa-dzirnavas"]),
    b.PIL("lv-ragaciems", "Ragaciems", "拉加齐姆斯", *C("lv-ragaciems"),
        "The fishing village on the Gulf of Riga where Imants Ziedonis was born in 1933 into a fisherman's family; he was buried in the Ragaciems cemetery in 2013. His Epiphanies came first in the internet vote of the 2014 Big Read",
        "里加湾边的渔村，伊曼茨·齐耶多尼斯 1933 年生在这里的一个渔民家庭；2013 年他安葬在拉加齐姆斯公墓。他的《顿悟》在 2014 年“大阅读”的网络投票中排第一",
        ["epifanijas"]),
    b.ORIG("lv-lozmetejkalns", "Ložmetējkalns", "机枪山", *C("lv-lozmetejkalns"),
        "Machine-Gun Hill in Valgunde parish, a sand ridge south of Lake Babīte fortified by the German army; the Latvian riflemen and Siberian rifle divisions took it in the Christmas Battles of January 1917. The Christmas Battles Museum at Mangaļi, where the battle scenes of the 2019 film of Blizzard of Souls were shot, stands in the same battlefield",
        "瓦尔贡德乡的“机枪山”，巴比泰湖以南的一道沙岗，德军在这里修了坚固的防线；1917 年 1 月的圣诞战役中，拉脱维亚步兵和西伯利亚步兵师攻下了它。2019 年电影《灵魂的暴风雪》的战斗场面在附近曼加利的圣诞战役博物馆拍摄，就在同一片战场上"),
    b.ORIG("lv-grizinkalns", "Grīziņkalns, Riga", "里加的格里津卡尔恩斯", *C("lv-grizinkalns"),
        "A working-class neighbourhood of Riga, long called 'Latvian Riga'. Vizma Belševica lived here as a child, and Bille's childhood passes in a narrow flat of a courtyard house on Vārnu Street; the 2018 film was shot in that house and courtyard, which now carry a plaque with Bille's portrait",
        "里加的工人街区，很早就被叫作“拉脱维亚人的里加”。维兹玛·贝尔舍维察小时候住在这里，比勒的童年就在瓦尔努街一座院内小楼的狭窄公寓里度过；2018 年的电影就在那座楼和院子里拍摄，楼上如今挂着一块印有比勒画像的牌子"),
    b.ORIG("lv-sakstagals", "Sakstagals", "萨克斯塔加尔斯", *C("lv-sakstagals"),
        "A Latgale village 14 km from Rēzekne. Jānis Klīdzējs spent his childhood between two family farms in the nearby parishes of Viļāni and Kantinieki and from 1923 walked 5 km to the Sakstagals primary school, which now bears his name. The farmstead of The Child of Man is not named, so the novel is pinned here",
        "拉特加莱的一个村子，距雷泽克内 14 公里。亚尼斯·克利杰伊斯的童年在附近维利亚尼乡和坎蒂涅基乡的两处家族农庄之间度过，1923 年起每天走 5 公里到萨克斯塔加尔斯小学上学，这所学校如今以他命名。《人之子》里的农庄没有名字，所以挂在这里"),
    b.ORIG("lv-lejasciems", "Lejasciems", "莱亚斯齐姆斯", *C("lv-lejasciems"),
        "A village in eastern Vidzeme where the Tirza meets the Gauja, Anna Sakse's birthplace (1905). On a Midsummer eve, on her way to her parents here, the scent of flowering night violets gave her the first of her flower tales, 'Naktsvijole' (The Night Violet)",
        "维泽梅东部蒂尔扎河汇入高亚河处的村子，安娜·萨克塞 1905 年生在这里。一个仲夏节前夜，她回这里看望父母，路上开着的夜紫罗兰的香气，让她写出了第一篇花的童话《夜紫罗兰》"),
    b.P("lv-liezere", "Liezēre", "列泽雷", *C("lv-liezere"), "film_location",
        adaptation={"title": "Likteņa līdumnieki", "year": 2003, "kind": "电视剧"},
        scene="拉脱维亚电视台 2003—2008 年播出的电视剧《命运的开拓者》改编自弗拉季米尔斯·凯亚克斯的四部长篇，在马多纳区列泽雷乡的“卡尔纳·亚翁泽姆吉”农庄拍摄（图钉在乡中心，农庄本身没有公开坐标）。故事追随纳尔布利一家：1885 年，男爵夫人把被人引诱的侍女卡特丽娜嫁出去，陪嫁一块地，此后一家四代经历了 20 世纪拉脱维亚的全部风云，一直写到 1995 年。剧本由凯亚克斯的妻子玛拉·斯维雷执笔，导演是维尔日尼亚·莱伊尼亚，这部剧成了拉脱维亚电视台历来最受欢迎的电视剧。",
        book_ids=["liktena-lidumnieki"],
        scene_en="The Latvian Television series Clearers of Fate (2003–2008), made from Vladimirs Kaijaks's four novels, was filmed at the 'Kalna Jaunzemji' farm in Liezēre parish, Madona Municipality (the pin is the parish centre; the farm has no published coordinates). It follows the Nārbuļi family from 1885, when a baroness marries off her seduced chambermaid Katrīna and gives her land as a dowry, through four generations and all the turns of Latvia's twentieth century to 1995. The script was by Kaijaks's wife Māra Svīre and the director Virdžīnija Lejiņa; it became Latvian Television's most popular series ever."),
]

lines = [
    b.S("lv-ep-1", "epifanijas", "lv-ragaciems", "Revelation", "显现",
        "Epiphanies are the three books of lyrical and ironic miniatures in prose (1971, 1974, 1994) that Imants Ziedonis wrote in the countryside, where he wanted to put down his roots; from 1969 to 1974 he built himself a reed-thatched country house at Murjāņi, now a summer residence of his museum. The word, he explained, comes from the Greek for shining forth, a revelation, and his epiphanies, he wrote, are born of boredom and weariness, of the blindness and deafness around us. The first two books are named in the Latvian Cultural Canon. Ziedonis was born in Ragaciems and lies in its cemetery.",
        "《顿悟》是伊曼茨·齐耶多尼斯在他想扎根的乡间写的三本抒情而带讽刺的散文小品（1971、1974、1994）；1969 到 1974 年他在穆里亚尼给自己盖了一座芦苇顶的乡间小屋，如今是他的博物馆的夏季馆舍。他解释说，这个词来自希腊语，意思是“照亮、显现”；他写道，他的顿悟生于无聊和厌倦，生于我们周围的盲、聋、哑和庸俗。前两本被列入拉脱维亚文化正典。齐耶多尼斯生在拉加齐姆斯，也葬在这里的公墓。",
        ["Ragaciems"], ["拉加齐姆斯"],
        "https://en.wikipedia.org/wiki/Imants_Ziedonis; https://lv.wikipedia.org/wiki/Imants_Ziedonis; https://www.vestnesis.lv/ta/id/155; https://kulturaskanons.lv/archive/imants-ziedonis/"),
    b.S("lv-dp-1", "dveselu-putenis", "lv-lozmetejkalns", "Part Two: the Christmas Battles", "第二部：圣诞战役",
        "Artūrs Vanags, son of a Zemgale farming family, joins the Latvian riflemen after German soldiers kill his mother in the family's yard. The second part of the novel follows the rifle regiments from the Ķekava front to the Tīreļpurvs bog and gives particular attention to the Christmas Battles of December 1916 and January 1917, in which his brother Edgars falls; it ends with the retreat from Riga in 1917. Aleksandrs Grīns himself fought in the Christmas Battles in the machine-gun team of the 4th Vidzeme Latvian Rifle Regiment. In those battles the riflemen and Siberian divisions took Ložmetējkalns.",
        "泽姆加莱一户农家的儿子阿尔图尔斯·瓦纳格斯，在德军士兵于自家院子里杀害母亲之后，参加了拉脱维亚步兵。小说第二部随步兵团从凯卡瓦前线打到蒂雷尔沼泽，着力描写 1916 年 12 月到 1917 年 1 月的圣诞战役，他的哥哥埃德加斯就死在这场战役里；这一部以 1917 年撤出里加结束。亚历山大斯·格林斯本人就在第 4 维泽梅拉脱维亚步兵团的机枪队里打过圣诞战役。在这场战役中，拉脱维亚步兵和西伯利亚步兵师攻下了机枪山。",
        ["Ložmetējkalns"], ["机枪山"],
        "https://enciklopedija.lv/skirklis/55356-Dvēseļu-putenis; https://enciklopedija.lv/skirklis/33399-Ziemassvētku-kaujas; https://www.dveseluputenis.lv/lv/laika-skala/notikums/85/ziemassvetku-kauju-sakums/; https://lv.wikipedia.org/wiki/Ložmetējkalns"),
    b.S("lv-bi-1", "bille", "lv-grizinkalns", "The Grīziņkalns republic", "格里津卡尔恩斯共和国",
        "The first book of Vizma Belševica's semi-autobiographical trilogy follows Bille from the age of five until she starts school, in the 1930s. Her childhood is poor: it passes in the 'Grīziņkalns republic', in a narrow flat of a courtyard house on Vārnu Street, with summers in the countryside at her father's sister's near Ugāle. Across the trilogy Bille is saved from the greyness of life by the world of books and by her own creative work. Belševica herself grew up in Grīziņkalns.",
        "维兹玛·贝尔舍维察这部半自传三部曲的第一本，写比勒从五岁到上学这几年，时间是 20 世纪 30 年代。她的童年很穷：在“格里津卡尔恩斯共和国”里，瓦尔努街一座院内小楼的狭窄公寓里度过，夏天去乌加莱一带的姑姑家过。在整部三部曲里，让比勒从灰暗的生活里得救的，是书的世界和她自己的创作。贝尔舍维察本人就是在格里津卡尔恩斯长大的。",
        ["Grīziņkalns"], ["格里津卡尔恩斯"],
        "https://enciklopedija.lv/skirklis/106300-“Bille”; https://www.lsm.lv/raksts/kultura/kino-foto-un-tv/billei-uzfilmetas-divas-tresdalas-epizozu.a199607/; https://lv.wikipedia.org/wiki/Vizma_Belševica"),
    b.S("lv-cb-1", "cilveka-berns", "lv-sakstagals", "Boņuks", "博纽克斯",
        "The Child of Man pictures life on a Latgale farmstead in the 1920s through the seven-year-old Boņuks (Bonifācijs Pavulāns), and largely retells Jānis Klīdzējs's own childhood. Klīdzējs grew up between the family farms of Kurpnieki in Viļāni parish and Upmaļi in Kantinieki parish, and from 1923 went to the Sakstagals primary school 5 km away, now the Jānis Klīdzējs school. Jānis Streičs's 1991 film of the novel was the first feature film made in Latgalian and Latvia's first entry for the Academy Award for foreign-language film. The farmstead of the novel is not named, so it is pinned here.",
        "《人之子》借七岁的博纽克斯（博尼法齐斯·帕武兰斯）的眼睛，写 20 世纪 20 年代拉特加莱一个农家院里的生活，很大程度上就是亚尼斯·克利杰伊斯自己的童年。克利杰伊斯在维利亚尼乡的库尔普涅基和坎蒂涅基乡的乌普马利两处家族农庄之间长大，1923 年起到 5 公里外的萨克斯塔加尔斯小学上学，这所学校如今叫亚尼斯·克利杰伊斯学校。1991 年亚尼斯·斯特赖奇斯据小说拍的电影，是第一部用拉特加莱语拍的故事片，也是拉脱维亚第一次报送奥斯卡外语片奖的影片。小说里的农庄没有名字，所以挂在这里。",
        ["Sakstagals"], ["萨克斯塔加尔斯"],
        "https://lv.wikipedia.org/wiki/Cilvēka_bērns; https://lv.wikipedia.org/wiki/Jānis_Klīdzējs; https://lv.wikipedia.org/wiki/Sakstagals; https://lvportals.lv/dienaskartiba/285747-filmai-cilveka-berns-25-gadu-jubileja-restaureta-versija-2017"),
    b.S("lv-pz-1", "pasakas-par-ziediem", "lv-lejasciems", "The Night Violet", "夜紫罗兰",
        "Anna Sakse's book of fairy tales about flowers began, as Saulcerīte Viese recalls in her introduction, on a Midsummer eve, when the young writer was travelling to her parents in Lejasciems, lost her way in the forest from the station, and met the scent of flowering night violets, fine pale flowers on frail stems; so the first tale, 'Naktsvijole', was born. Tales of the balsam, the bleeding heart and the gladiolus followed, and watercolours by Kārlis Sūniņš gave the impulse to gather them into a book (1966).",
        "安娜·萨克塞这本关于花的童话集，据萨乌尔采丽特·维埃塞在序言里所写，开始于一个仲夏节前夜：年轻的作家回莱亚斯齐姆斯看望父母，从车站出来在林子里迷了路，迎面飘来正在开放的夜紫罗兰的香气——细长的茎上开着纤弱苍白的花；第一篇童话《夜紫罗兰》就这样诞生了。后来又有了凤仙花、荷包牡丹、唐菖蒲的故事，卡尔利斯·苏尼什的水彩画促成了把它们编成一本书（1966）。",
        ["Lejasciems"], ["莱亚斯齐姆斯"],
        "https://www.vestnesis.lv/ta/id/100422; https://lv.wikipedia.org/wiki/Anna_Sakse"),
]

def ids_in(path): return set(re.findall(r'\{ id: "([^"]+)"', open(path, encoding="utf-8").read()))
all_books = set()
for f in glob.glob(os.path.join(APP, "data", "*", "books.js")):
    all_books |= ids_in(f)
new_b, new_p = {x["id"] for x in books}, {x["id"] for x in places}
assert len(books) == 7 and len(new_b) == 7
assert not new_b & all_books, new_b & all_books
assert new_p == set(CO), new_p ^ set(CO)
line_places = {p["id"] for p in places if p["place_type"] != "film_location"}
for l in lines:
    assert l["book_id"] in new_b and l["place_ids"][0] in line_places, l["id"]
linked = {l["book_id"] for l in lines} | {x for p in places for x in p.get("book_ids", [])}
assert linked == new_b, new_b ^ linked
assert {l["place_ids"][0] for l in lines} | {p["id"] for p in places if p.get("book_ids")} == new_p

HEAD = "// Latvia, hand-written content (tools/content/batches/add_lv1.py, 2026-11-26).\n"
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
