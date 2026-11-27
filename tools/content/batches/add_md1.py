"""11-26: Moldova, the 5 books the user chose: the top 5 of the 2013 UNIMEDIA/Cartier poll of the best Bessarabian novels
of the last 50 years (tools/selection/md.md). Moldova opens with this batch. All five are in copyright, so the lines are
scene notes in our own words. Places, with the reason for each:
- Mana (Orhei): Din calidor is Paul Goma's own childhood in this village, in the teachers' house of its school, with the
  calidor (veranda) of the title.
- The other four novels are set in villages the authors invented, so under the rule for famous books each is hung at the
  author's native village, with an honest note:
  - Unțești (Ungheni) for The Tale of the Red Rooster: its village, Ponoare, is not a real place we could find.
  - Mălăiești (left bank of the Dniester) for Broken Flight: the action begins and ends on the bank of the Dniester; the
    village is not named in the sources we read.
  - Horodiște (Dondușeni) for The Burden of Our Kindness: Ciutura is invented and lies in the Soroca plain, like Horodiște.
  - Codreanca, formerly Cobâlca (Strășeni), for The Chronicle of the Chicken Thieves: Găinari is invented.
The map of Moldova (data/md/geo.js) is built from geoBoundaries MDA ADM1 (UNHCR, OCHA FISS; CC BY 3.0 IGO): 32 districts,
the municipalities of Chișinău, Bălți and Bender, Gagauzia and Transnistria. Natural Earth's admin-1 for Moldova lacks
Dubăsari and splits Transnistria into odd pieces.
Usage: python3 -I tools/content/batches/add_md1.py <app_dir> tools/content/batches/coords/add_md1.json"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b

APP, CO = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8"))
DATE = "2026-11-26"
b.init(APP, "", "md", DATE)
def C(pid):
    c = CO[pid]; return c["lat"], c["lon"], c["st"], c["su"]
def BK(id, title, title_zh, title_orig, author, author_zh, year, aliases):
    return dict(id=id, title=title, title_zh=title_zh, title_orig=title_orig, author=author, author_zh=author_zh, year=year,
                orig_lang="ro", public_domain=False, source_url=None, aliases=aliases)

books = [
    BK("povestea-cu-cocosul-rosu", "The Tale of the Red Rooster", "红公鸡的故事", "Povestea cu cocoșul roșu", "Vasile Vasilache",
       "瓦西列·瓦西拉凯", "1966", ["Povestea cu cocoșul roșu", "Povestea cu cucoșul roșu", "Serafim", "Ponoare"]),
    BK("zbor-frant", "Broken Flight", "折翼", "Zbor frânt", "Vladimir Beșleagă", "弗拉基米尔·贝什利亚格", "1966",
       ["Zbor frânt", "Zbor frînt", "Isai"]),
    BK("povara-bunatatii-noastre", "The Burden of Our Kindness", "我们善良的重负", "Povara bunătății noastre", "Ion Druță",
       "伊翁·德鲁策", "1970", ["Povara bunătății noastre", "Balade din câmpie", "Ciutura", "Onache Cărăbuș"]),
    BK("din-calidor", "From the Porch: A Bessarabian Childhood", "从门廊：一个比萨拉比亚的童年", "Din calidor. O copilărie basarabeană",
       "Paul Goma", "保罗·戈马", "1987", ["Din calidor", "Le Calidor", "My Childhood at the Gate of Unrest", "Mana"]),
    BK("hronicul-gainarilor", "The Chronicle of the Chicken Thieves", "偷鸡贼编年史", "Hronicul Găinarilor", "Aureliu Busuioc",
       "奥雷利乌·布苏约克", "2006", ["Hronicul Găinarilor", "Găinari"]),
]

places = [
    b.ORIG("md-mana", "Mana, Orhei", "奥尔海伊的马纳村", *C("md-mana"),
        "A village of Seliște commune, Orhei district, where Paul Goma was born in 1935. His parents taught at the village school, which his father built with the villagers, with the teachers' home and its calidor, a long veranda, on one side; Din calidor recalls his childhood here",
        "奥尔海伊区塞利什泰乡的一个村子，保罗·戈马 1935 年生在这里。他的父母是村里学校的教师，学校是他父亲和村民一起盖的，一侧是教师住处和它的“卡利多尔”——一条长长的廊子；《从门廊》写的就是他在这里的童年"),
    b.ORIG("md-untesti", "Unțești, Ungheni", "温格尼区的温采什蒂村", *C("md-untesti"),
        "The village in Ungheni district where Vasile Vasilache was born in 1926 and went to primary school. The Tale of the Red Rooster is set in an invented village, Ponoare; it is hung here, at its author's native village, under the rule for famous books",
        "温格尼区的一个村子，瓦西列·瓦西拉凯 1926 年生在这里，并在这里读完小学。《红公鸡的故事》发生在虚构的村子波诺阿雷；按“名著不漏”的规则，挂在作者的家乡"),
    b.ORIG("md-malaiesti", "Mălăiești", "梅勒耶什蒂", *C("md-malaiesti"),
        "A large village on the left bank of the Dniester, in Grigoriopol district (Transnistria), first recorded in 1541, where Vladimir Beșleagă was born in 1931. Broken Flight begins and ends on the bank of the Dniester, in a village the sources we read do not name; it is hung at its author's native village under the rule for famous books",
        "德涅斯特河左岸格里戈里奥波尔区（德涅斯特河左岸地区）的一个大村，1541 年首见于文献，弗拉基米尔·贝什利亚格 1931 年生在这里。《折翼》从德涅斯特河岸开始，也在河岸结束，我们读到的资料没有写出村名；按“名著不漏”的规则，挂在作者的家乡"),
    b.ORIG("md-horodiste", "Horodiște, Dondușeni", "顿杜谢尼区的霍罗迪什泰村", *C("md-horodiste"),
        "A village of the Soroca plain, between two tributaries of the Răut, where Ion Druță was born in 1928 and lived until he was eleven; he wrote a memoir named after it. Ciutura, the village of The Burden of Our Kindness, is invented and lies in the same Soroca plain; critics hold that Druță's villages, whatever their names, are one and the same",
        "索罗卡平原上的一个村子，在勒乌特河的两条支流之间，伊翁·德鲁策 1928 年生在这里，在这里住到 11 岁，还以它为名写过一本回忆录。《我们善良的重负》里的丘图拉村是虚构的，也在索罗卡平原；评论家认为，德鲁策笔下的村子不管叫什么名字，都是同一个村子"),
    b.ORIG("md-codreanca", "Codreanca (Cobâlca), Strășeni", "斯特雷谢尼区的科德良卡（旧名科贝尔卡）", *C("md-codreanca"),
        "A village of Strășeni district, formerly called Cobâlca, where Aureliu Busuioc was born in 1928. Găinari, the village of The Chronicle of the Chicken Thieves, is invented; the novel is hung at its author's native village under the rule for famous books",
        "斯特雷谢尼区的一个村子，旧名科贝尔卡，奥雷利乌·布苏约克 1928 年生在这里。《偷鸡贼编年史》里的盖纳里村是虚构的；按“名著不漏”的规则，挂在作者的家乡"),
]

lines = [
    b.S("md-dc-1", "din-calidor", "md-mana", "The novel as a whole", "全书",
        "Din calidor is Paul Goma's Bessarabian childhood in Mana, told by the boy Paul from the calidor, the veranda of the teachers' house at the village school his father had built. The child's world of village characters, games and his parents is broken into by history: the Soviet occupation of 1940, his father's deportation to Siberia, the burning of Romanian books, flight and return. The family left for Transylvania in March 1944. The book appeared first in French, as Le Calidor, in 1987, and then in Romanian.",
        "《从门廊》是保罗·戈马在马纳的比萨拉比亚童年，由小男孩保罗在“卡利多尔”——父亲盖的村校旁教师住处的长廊——上讲出来。孩子眼中的世界有村里形形色色的人物、游戏和父母，却一次次被历史打断：1940 年的苏联占领、父亲被流放西伯利亚、罗马尼亚文书籍被焚烧、逃难又回来。1944 年 3 月一家人逃往特兰西瓦尼亚。这本书先以法文《卡利多尔》在 1987 年出版，之后才有罗马尼亚文版。",
        ["Mana"], ["马纳"],
        "https://old.bncreanga.md/pdf/Paul_Goma.pdf; https://www.diacronia.ro/indexing/details/A6787/pdf; https://www.diacronia.ro/indexing/details/A6893/pdf; https://en.wikipedia.org/wiki/Paul_Goma"),
    b.S("md-cr-1", "povestea-cu-cocosul-rosu", "md-untesti", "The novel as a whole", "全书",
        "Serafim, a young and rather bewildered peasant, goes to the fair to buy a cow and comes home with Bălan, a white bullock, which turns out to have a rich inner life of its own; around them the village of Ponoare, in the time of the collective farm, gossips, quarrels and makes up. The novel turns a folk tale of foolish bargains, in the manner of Creangă's Dănilă Prepeleac, into a parable of village life; its first part appeared in 1966, and the second, in 1971, was harshly attacked by the critics. Vasile Vasilache was born in Unțești.",
        "年轻、有点糊涂的农民塞拉菲姆去集市买奶牛，牵回来的却是一头白色小公牛巴兰，而这头牛自有丰富的内心世界；他们周围，是集体农庄时代的波诺阿雷村，家长里短、吵了又和。小说把一个傻人做亏本买卖的民间故事——像克良格笔下的达尼勒·普雷佩亚克那样——写成了一则乡村生活的寓言；第一部 1966 年出版，1971 年的第二部遭到评论家猛烈抨击。瓦西列·瓦西拉凯生在温采什蒂。",
        ["Unțești"], ["温采什蒂"],
        "https://www.moldpres.md/rom/cultura/cronica-arhivelor-25; https://www.cyberculture.ro/2015/06/26/carte-audio-povestea-cu-cocosul-rosu-vasile-vasilache/; https://ibn.idsi.md/sites/default/files/imag_file/Povestea%20lui%20Vasile%20Vasilache_poveste%20existentiala%20a%20romanului.pdf; https://ro.wikipedia.org/wiki/Vasile_Vasilache_(scriitor)"),
    b.S("md-zf-1", "zbor-frant", "md-malaiesti", "The novel as a whole", "全书",
        "Years afterwards, when the villagers ask Isai whether it is true that he went over to the Germans on the other bank in the summer the front stopped on the Dniester, he sometimes smiles, sometimes gets angry and walks away. The novel tells that summer: Isai tears himself out of the Germans' hands and throws himself into the Dniester to cross back to his own bank, the leap that gives the book its title. The action begins on the bank of the Dniester and ends there, with Isai and a boy walking home along the river. Vladimir Beșleagă was born in Mălăiești, a village on the Dniester.",
        "多年以后，村里人问伊萨伊：那年夏天前线停在德涅斯特河上，他是不是投奔了对岸的德国人？他有时笑笑，有时发火走开。小说讲的就是那个夏天：伊萨伊从德国人手里挣脱，纵身跳进德涅斯特河，要游回自己这边的岸——书名说的正是这一跃。故事从德涅斯特河岸开始，也在河岸结束：伊萨伊和一个男孩沿着河走回家。弗拉基米尔·贝什利亚格生在德涅斯特河边的梅勒耶什蒂。",
        ["Mălăiești"], ["梅勒耶什蒂"],
        "https://www.diacronia.ro/indexing/details/A6945/pdf; https://bibliopolis.hasdeu.md/index.php/bibliopolis/article/download/1214/1107/3483; https://ro.wikipedia.org/wiki/Mălăiești,_Stînga_Nistrului"),
    b.S("md-pb-1", "povara-bunatatii-noastre", "md-horodiste", "The novel as a whole", "全书",
        "The Burden of Our Kindness follows Ciutura, an invented village of the Soroca plain, from the start of the twentieth century into the 1950s, through the life of the peasant Onache Cărăbuș, whose fate meets the dramatic history of Bessarabia; the critic Valeriu Cristea called Ciutura a village stronger than history. Its first part, Ballads of the Plain, appeared in 1963 and the whole in 1970; that year the head of the Moldavian Communist Party wrote to warn the Lenin Prize committee against it. Ion Druță was born in Horodiște, in the same Soroca plain.",
        "《我们善良的重负》写索罗卡平原上一个虚构的村子丘图拉，从 20 世纪初写到 50 年代，主线是农民奥纳凯·克勒布什的一生，他的命运和比萨拉比亚动荡的历史交织在一起；评论家瓦列留·克里斯泰亚说，丘图拉是“一个比历史更强大的村子”。第一部《平原歌谣》1963 年出版，全书 1970 年出版；就在那一年，摩尔达维亚共产党第一书记写信给列宁奖评委会，警告这部小说有颠覆性。伊翁·德鲁策生在同一片索罗卡平原上的霍罗迪什泰。",
        ["Horodiște"], ["霍罗迪什泰"],
        "https://bibsadoveanusoroca.wordpress.com/2026/09/03/ion-druta-izvor-nesecat-al-bunatatii-2/; https://www.arborinstitute.eu/ion-druta-ambiguitatea-ideologica-a-literaturii/; https://www.diacronia.ro/indexing/details/A5414/pdf; https://www.cuzanet.ro/documentar/ion-druta-un-amestec-de-admiratie-si-controversa.html"),
    b.S("md-hg-1", "hronicul-gainarilor", "md-codreanca", "The novel as a whole", "全书",
        "The Chronicle of the Chicken Thieves is a parody of the history of Bessarabia over two centuries, told as the chronicle of an invented village, Găinari, founded in 1812, the year of the Russian annexation, by chicken thieves driven out of another village. Generation after generation the family passes on its vices and survives every change of regime, down to 1970, when the 'new chicken thieves' have become a perfect social and political class. The National Theatre Mihai Eminescu in Chișinău has staged it. Aureliu Busuioc was born in Cobâlca, now Codreanca.",
        "《偷鸡贼编年史》借一个虚构村子盖纳里的编年史，戏仿两百年来的比萨拉比亚历史：这个村子由被别的村子赶出来的偷鸡贼在 1812 年——俄国吞并比萨拉比亚的那一年——建立。一代又一代，这一家把恶习传下去，挺过每一次政权更替，一直到 1970 年，“新偷鸡贼”已经成了一个完美的社会和政治阶层。基希讷乌的米哈伊·爱明内斯库国家剧院把它搬上了舞台。奥雷利乌·布苏约克生在科贝尔卡，也就是今天的科德良卡。",
        ["Codreanca"], ["科德良卡"],
        "https://unimedia.info/ro/news/f009b5a23d6f09ed/in-ochii-tai-fermecatori-hronicul-gainarilor-si-krum-spectacole-difuzate-online-gratuit-de-teatrul-national-mihai-eminescu.html; https://www.goodreads.com/book/show/17375973-hronicul-g-inarilor; https://dialogica.asm.md/arhivarevistei/Metaliteratura/2010,%20nr.1-4%20(23-24).pdf; https://ro.wikipedia.org/wiki/Codreanca,_Strășeni"),
]

def ids_in(path): return set(re.findall(r'\{ id: "([^"]+)"', open(path, encoding="utf-8").read()))
all_books = set()
for f in glob.glob(os.path.join(APP, "data", "*", "books.js")):
    all_books |= ids_in(f)
new_b, new_p = {x["id"] for x in books}, {x["id"] for x in places}
assert len(books) == 5 and not new_b & all_books, new_b & all_books
assert new_p == set(CO), new_p ^ set(CO)
for l in lines:
    assert l["book_id"] in new_b and l["place_ids"][0] in new_p, l["id"]
assert {l["book_id"] for l in lines} == new_b and {l["place_ids"][0] for l in lines} == new_p

HEAD = "// Moldova, hand-written content (tools/content/batches/add_md1.py, 2026-11-26).\n"
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
