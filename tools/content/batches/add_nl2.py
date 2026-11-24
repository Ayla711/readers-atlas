"""11-24: the Netherlands, second pack: books that selection rule v2 adds (tools/selection/nl.md), as far as their places are found.
All four new books are in copyright: scene notes in our own words. The Goldfinch is already in the app (us); it gets a second
scene here, for the Amsterdam chapters that open and close the novel.
- The Evenings (Amsterdam, the last ten days of 1946), Turkish Delight (the sculptor's Amsterdam studio), The Goldfinch: Amsterdam.
- The Darkroom of Damocles: Voorschoten, where Osewoudt keeps his tobacco shop.
- The Discovery of Heaven: the Westerbork radio observatory, built near the site of the wartime camp.
Not added yet: Out of Mind (Hersenschimmen) is set near Gloucester, Massachusetts, outside the Netherlands; whether to hang it
there is the user's call. No photos yet.

Usage: python3 -I tools/content/batches/add_nl2.py <app_dir> tools/content/batches/coords/add_nl2.json"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b

APP, CO = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8"))
DATE = "2026-11-24"
EXT = {"goldfinch"}  # books already in the app (another country's books.js) that get a line here
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
b.init(APP, "", "nl", DATE)
books = [
    BK("the-evenings", "The Evenings", "晚间", "De avonden", "Gerard Reve", "赫拉德·雷弗", "Gerard Reve", "1947", "nl",
       ["De avonden", "De Avonden", "Frits van Egters", "Simon van het Reve"]),
    BK("darkroom-of-damocles", "The Darkroom of Damocles", "达摩克利斯的暗室", "De donkere kamer van Damokles", "Willem Frederik Hermans",
       "威廉·弗雷德里克·赫尔曼斯", "Willem Frederik Hermans", "1958", "nl",
       ["De donkere kamer van Damokles", "De donkere kamer van Damocles", "Henri Osewoudt", "Dorbeck", "W. F. Hermans"]),
    BK("discovery-of-heaven", "The Discovery of Heaven", "天堂的发现", "De ontdekking van de hemel", "Harry Mulisch", "哈里·穆里施",
       "Harry Mulisch", "1992", "nl", ["De ontdekking van de hemel", "Max Delius", "Onno Quist", "Quinten Quist", "Ada Brons"]),
    BK("turkish-delight", "Turkish Delight", "土耳其软糖", "Turks fruit", "Jan Wolkers", "扬·沃尔克斯", "Jan Wolkers", "1969", "nl",
       ["Turks fruit", "Turks Fruit", "Olga"]),
]
places = [
    b.ORIG("nl-amsterdam", "Amsterdam", "阿姆斯特丹", *C("nl-amsterdam"),
           "Capital of the Netherlands. Gerard Reve's The Evenings (1947) follows a young office clerk in Amsterdam through the last ten evenings of 1946; Jan Wolkers' Turkish Delight (1969) is a sculptor's love story told mostly from his Amsterdam studio; and Donna Tartt's The Goldfinch (2013) opens and closes in an Amsterdam hotel at Christmas",
           "荷兰首都。赫拉德·雷弗的《晚间》（1947）跟着阿姆斯特丹一个年轻小职员走过 1946 年最后十个晚上；扬·沃尔克斯的《土耳其软糖》（1969）是一个雕塑家的爱情故事，大半发生在他阿姆斯特丹的工作室里；唐娜·塔特的《金翅雀》（2013）则在圣诞时节阿姆斯特丹的一家旅馆里开头，也在那里收尾"),
    b.ORIG("nl-voorschoten", "Voorschoten", "福尔斯霍滕", *C("nl-voorschoten"),
           "Village between Leiden and The Hague. In Willem Frederik Hermans' The Darkroom of Damocles (1958) Henri Osewoudt keeps the tobacco shop here when the war begins, and it is here that he meets his double Dorbeck",
           "莱顿和海牙之间的小镇。威廉·弗雷德里克·赫尔曼斯的《达摩克利斯的暗室》（1958）里，战争爆发时亨利·奥瑟沃特在这里开着一家烟草店，也是在这里遇见了他的替身多尔贝克"),
    b.ORIG("nl-westerbork-telescope", "Westerbork Synthesis Radio Telescope", "韦斯特博克综合孔径射电望远镜", *C("nl-westerbork-telescope"),
           "Radio telescope in the Drenthe countryside, next to the site of Camp Westerbork, the wartime camp through which the Jews of the Netherlands were deported. In Harry Mulisch's The Discovery of Heaven (1992) the astronomer Max Delius becomes chief astronomer of the observatory built here",
           "德伦特乡间的射电望远镜，紧挨着韦斯特博克营旧址——二战时荷兰犹太人就是经由这座营地被遣送出去的。哈里·穆里施的《天堂的发现》（1992）里，天文学家马克斯·德利乌斯当上了建在这里的天文台的首席天文学家"),
]
lines = [
    b.S("nl-ev-1", "the-evenings", "nl-amsterdam", "The novel as a whole", "全书",
        "Sunday 22 December 1946, in Amsterdam (“our town” in the opening sentence): on the first floor of Schilderskade 66, Frits van Egters, a twenty-three-year-old office clerk who still lives with his parents, wakes before it is light. The ten chapters follow him through the last ten days of the year, one day each and above all its evening: dinners with parents he finds irritating and embarrassing, visits to friends, his fixation on time passing, decay and illness, and the dreams with which most chapters close. The book ends in the early hours of New Year's Day, 1947.",
        "1946 年 12 月 22 日，星期天，阿姆斯特丹（开篇第一句里叫“我们的城市”）：画家码头 66 号二楼，二十三岁、还和父母住在一起的小职员弗里茨·范·埃格特斯在天亮之前醒来。全书十章，跟着他走过这一年的最后十天，一章一天，写的主要是晚上：和让他心烦又难堪的父母吃饭，去朋友家串门，他对时光流逝、衰败和疾病的执念，还有大多数章节结尾的那些梦。小说在 1947 年元旦凌晨结束。",
        ["Amsterdam"], ["阿姆斯特丹"],
        "https://en.wikipedia.org/wiki/The_Evenings; https://canon2015.literairecanon.be/en/works/de-avonden; https://www.letterenfonds.nl/en/books/the-evenings; https://dbnl.org/tekst/_bzz001198901_01/_bzz001198901_01_0032.php; https://www.themodernnovel.org/europe/w-europe/netherlands/reve/avonden"),
    b.S("nl-td-1", "turkish-delight", "nl-amsterdam", "The novel as a whole", "全书",
        "The nameless narrator, a young Amsterdam sculptor, tells of his wild love for Olga, whom he married against the wishes of her well-off parents. Most of it happens in his studio, which is also his home, where Olga often posed for him. Olga has left him, and he tries to forget her with one woman after another. Then her mother tells him that Olga is in hospital with a brain tumour. For half a year he visits her several times a week, reads to her and brings her Turkish delight, the only sweet she still dares to eat; when she dies she is holding on to the bright red wig he gave her.",
        "无名的叙述者是阿姆斯特丹一个年轻的雕塑家，他讲述自己对奥尔加的狂热爱情——他不顾她那富裕的父母反对娶了她。故事大多发生在他那间既是工作室又是住处的屋子里，奥尔加常在那里给他当模特。奥尔加离开了他，他靠一个又一个女人来忘掉她。后来奥尔加的母亲告诉他，奥尔加得了脑瘤住进了医院。半年里他每周去看她好几次，给她读书，给她带土耳其软糖——那是她唯一还敢吃的甜食；她死的时候，还紧紧按着他送的那顶火红的假发。",
        ["Amsterdam"], ["阿姆斯特丹"],
        "https://dbnl.org/tekst/anbe001lexi01_01/lvlw00684.php; https://maken.wikiwijs.nl/bestanden/782889/Turks%20fruit.docx; https://www.letterenfonds.nl/en/books/turkish-delight/print; https://bookbeat.com/nl/book/turks-fruit-1292458"),
    b.S("nl-gf-1", "goldfinch", "nl-amsterdam", "The opening and the last part", "开篇与最后一部",
        "The novel opens and closes in Amsterdam at Christmas. Theo Decker, now an adult, is shut in his hotel room, a canal house, sick and frightened, unable to read the Dutch papers that report a killing. He has come with his old friend Boris to recover Carel Fabritius's The Goldfinch, the small painting he carried out of the bombed museum in New York as a boy. The deal goes wrong: in a shoot-out Theo kills a man and Boris is wounded, and Theo waits alone in the hotel for days, until Boris turns up at Christmas, having told the authorities about the thieves.",
        "小说在圣诞时节的阿姆斯特丹开头，也在那里收尾。已经成年的西奥·德克尔把自己关在旅馆房间里——那是一座运河边的老房子——病着，又怕得要命，看不懂报道一桩命案的荷兰报纸。他是和老朋友鲍里斯一起来的，要追回卡雷尔·法布里蒂乌斯的《金翅雀》——少年时他从纽约那座被炸的博物馆里带出来的那幅小画。交易出了岔子：枪战中西奥打死了一个人，鲍里斯受了伤，西奥一个人在旅馆里等了好几天，直到圣诞节鲍里斯才出现——他已经把那伙窃贼报告给了当局。",
        ["Amsterdam"], ["阿姆斯特丹"],
        "https://en.wikipedia.org/wiki/The_Goldfinch_(novel); https://www.gradesaver.com/the-goldfinch/study-guide/summary-chapter-11; https://www.gradesaver.com/the-goldfinch/study-guide/summary; https://cliffsnotes-v1.prod.webpr.hmhco.com/literature/g/the-goldfinch/book-summary; https://ursummary.com/the-goldfinch-summary-chapter-by-chapter-donna-tartt/; https://www.goodreads.com/topic/show/1637236-1-14-the-goldfinch-part-i"),
    b.S("nl-dd-1", "darkroom-of-damocles", "nl-voorschoten", "The novel as a whole", "全书",
        "Henri Osewoudt has married Ria and taken over the tobacco shop in Voorschoten, where he lives with her and with his mother, who has left a psychiatric hospital. On the first day of the war, 10 May 1940, he meets Lieutenant Dorbeck, who looks exactly like him except that Dorbeck's hair is black. Dorbeck asks him to develop a roll of film and draws him into the resistance. The only thing that could prove to the world that Dorbeck exists is a photograph of him, and in the end even that photograph turns out not to exist.",
        "亨利·奥瑟沃特娶了里娅，接手了福尔斯霍滕的那家烟草店，和她以及刚从精神病院出来的母亲住在一起。1940 年 5 月 10 日，战争的第一天，他遇见了多尔贝克中尉——除了一头黑发，长得和他一模一样。多尔贝克请他冲洗一卷胶卷，把他拉进了抵抗运动。能向世人证明多尔贝克存在的唯一东西是一张他的照片，可到最后，连这张照片也被证明并不存在。",
        ["Voorschoten"], ["福尔斯霍滕"],
        "https://dbnl.org/tekst/anbe001lexi01_01/lvlw00284.php; https://dbnl.org/tekst/jans037over01_01/jans037over01_01_0001.php; https://app.thestorygraph.com/books/debf44ae-5592-4e99-8f4e-6ede8165c972; https://bookbeat.com/bg/book/de-donkere-kamer-van-damokles-723198"),
    b.S("nl-dh-1", "discovery-of-heaven", "nl-westerbork-telescope", "The observatory at Westerbork", "韦斯特博克的天文台",
        "Max Delius's Jewish mother was deported to Auschwitz, and his father was executed after the war as a collaborator. In the 1960s Max, an astronomer, accepts the post of chief astronomer at the great observatory that the Dutch government builds at Westerbork, in rural Drenthe, a place with a shameful history: the camp from which the Jews of the Netherlands were deported. Behind the story, an angel in heaven has arranged the meeting of Max and Ada Brons so that their son Quinten can bring the tablets of the Ten Commandments back to heaven; Quinten's search ends in Jerusalem.",
        "马克斯·德利乌斯的犹太母亲被遣送到奥斯维辛，父亲战后作为通敌者被处决。1960 年代，天文学家马克斯接受了一个职位：去荷兰政府在德伦特乡间韦斯特博克建造的大型天文台当首席天文学家——这个地方有一段可耻的历史：荷兰犹太人正是从这里的营地被遣送出去的。故事背后，天堂里的一位天使安排了马克斯和阿达·布龙斯的相遇，好让他们的儿子昆滕把刻着十诫的石板送回天堂；昆滕的寻找最后在耶路撒冷结束。",
        ["Westerbork"], ["韦斯特博克"],
        "https://www.nybooks.com/?p=19083; https://www.wikipedia.com/wiki/The_Discovery_of_Heaven; https://letterenfonds.nl/en/books/the-discovery-of-heaven; https://studenttheses.universiteitleiden.nl/access/item%3A2606264/view; https://dbnl.org/tekst/_gid001199301_01/_gid001199301_01_0078.php"),
]
check(books, places, lines)
if __name__ == "__main__":
    M = "11-24: second pack, books added under selection rule v2 (tools/content/batches/add_nl2.py)"
    b.append(b.data("books.js"), books, M); b.append(b.data("places.js"), places, M); b.append(b.data("lines.js"), lines, M)
    print(len(books), "books,", len(places), "places,", len(lines), "lines")
