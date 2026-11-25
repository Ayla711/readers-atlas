"""11-24: Norway, second pack: books that selection rule v2 adds (tools/selection/no.md). Scene notes in our own words.
- Sophie's World: Lillesand, Hilde's home. Mysteries (public domain, 1892): the coastal town is never named; the book is hung
  at Lillesand, with which it is closely tied (local tradition: written in part at the Hotel Norge). A scene note, not a
  quotation, because no passage of the novel names a real place to highlight.
- The Alberta Trilogy: Tromsø, model of the unnamed northern town of the first volume (place type prototype).
- The Redbreast: the Royal Palace and the Palace Park, Oslo, the target of the old man's plan on 17 May.
- Out Stealing Horses: the novel names no place (a house by a lake far in the east, a summer farm by a river near the Swedish
  border); the book is shown at Trysil, where the 2019 film was shot (place type film_location), and the summary of the novel
  goes into the film place's scene text, since validate.js allows no excerpt at a film location.
  Sources: https://en.wikipedia.com/wiki/Out_Stealing_Horses_(film); https://www.finn.no/440928907 (Oktober's blurb);
  https://www.finn.no/337615832; https://www.supersummary.com/out-stealing-horses/summary/; https://www.sfanytime.com/da/movie/ut-of-stjale-hester
- The House with the Blind Glass Windows: the island community is unnamed; hung at Myre in Vesterålen, Wassmo's birthplace
  (place type prototype, honest note).
Photos: tools/content/batches/add_photos_ch_no_se_1124.py.

Usage: python3 -I tools/content/batches/add_no2.py <app_dir> tools/content/batches/coords/add_no2.json"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b

APP, CO = sys.argv[1], (json.load(open(sys.argv[2], encoding="utf-8")) if len(sys.argv) > 2 else {})
DATE = "2026-11-24"
def C(pid):
    c = CO[pid]; return c["lat"], c["lon"], c["st"], c["su"]
def BK(id, title, title_zh, title_orig, author, author_zh, author_orig, year, lang, aliases, pd=False, src=None):
    return dict(id=id, title=title, title_zh=title_zh, title_orig=title_orig, author=author, author_zh=author_zh, year=year,
                orig_lang=lang, public_domain=pd, source_url=src, author_orig=author_orig, aliases=aliases)
def ids_in(path): return set(re.findall(r'\{ id: "([^"]+)"', open(path, encoding="utf-8").read()))
def check(books, places, lines, old_places=()):
    allb = set()
    for f in glob.glob(os.path.join(APP, "data", "*", "books.js")): allb |= ids_in(f)
    assert not {x["id"] for x in books} & allb, {x["id"] for x in books} & allb
    have = ids_in(b.data("places.js"))
    assert not {p["id"] for p in places} & have and {p["id"] for p in places} == set(CO)
    assert set(old_places) <= have, set(old_places) - have
    assert not {l["id"] for l in lines} & ids_in(b.data("lines.js"))
    pl = {p["id"] for p in places} | set(old_places)
    for l in lines:
        assert l["book_id"] in {x["id"] for x in books} and l["place_ids"][0] in pl, l["id"]
    film = {p["id"]: set(p["book_ids"]) for p in places if p["place_type"] == "film_location"}
    assert {l["book_id"] for l in lines} | set().union(*film.values()) == {x["id"] for x in books}
    assert {l["place_ids"][0] for l in lines} | set(film) == pl
b.init(APP, "", "no", DATE)
books = [
    BK("alberta-trilogy", "The Alberta Trilogy", "阿尔贝塔三部曲", "Alberte-trilogien", "Cora Sandel", "科拉·桑德尔", "Cora Sandel", "1926–1939", "no",
       ["Alberte og Jakob", "Alberta and Jacob", "Alberte og friheten", "Alberta and Freedom", "Bare Alberte", "Alberta Alone", "Alberta Selmer"]),
    BK("sophies-world", "Sophie's World", "苏菲的世界", "Sofies verden", "Jostein Gaarder", "乔斯坦·贾德", "Jostein Gaarder", "1991", "no",
       ["Sofies verden", "Sophie Amundsen", "Hilde Møller Knag", "Alberto Knox", "Albert Knag"]),
    BK("the-redbreast", "The Redbreast", "知更鸟", "Rødstrupe", "Jo Nesbø", "尤·奈斯博", "Jo Nesbø", "2000", "no",
       ["Rødstrupe", "Harry Hole", "Nesbo"]),
    BK("out-stealing-horses", "Out Stealing Horses", "外出偷马", "Ut og stjæle hester", "Per Petterson", "佩尔·帕特森", "Per Petterson", "2003", "no",
       ["Ut og stjæle hester", "Trond Sander", "Lars Haug", "Jon Haug"]),
    BK("house-blind-glass-windows", "The House with the Blind Glass Windows", "盲玻璃阳台的房子", "Huset med den blinde glassveranda",
       "Herbjørg Wassmo", "赫比约格·瓦斯莫", "Herbjørg Wassmo", "1981", "no",
       ["Huset med den blinde glassveranda", "The House with the Blind Glass Porch", "Tora", "Tora trilogy", "Wassmo"]),
    BK("mysteries-hamsun", "Mysteries", "神秘", "Mysterier", "Knut Hamsun", "克努特·汉姆生", "Knut Hamsun", "1892", "no",
       ["Mysterier", "Johan Nilsen Nagel", "Nagel", "the Midget", "Minutten"], pd=True),
]
places = [
    b.ORIG("no-lillesand", "Lillesand", "利勒桑", *C("no-lillesand"),
           "Small coastal town in Sørlandet, on the Skagerrak. In Jostein Gaarder's Sophie's World (1991) it is the home of Hilde Møller Knag, to whom the strange postcards that Sophie finds are addressed, and the place her father, a UN major, comes home to. Knut Hamsun's Mysteries (1892) is closely tied to the town as well: local tradition holds that he wrote part of it at the Hotel Norge",
           "南部地区斯卡格拉克海峡边的海滨小城。乔斯坦·贾德的《苏菲的世界》（1991）里，这里是希尔德·默勒·克纳格的家——苏菲收到的那些奇怪明信片就是寄给她的；她当联合国少校的父亲最后也回到这里。克努特·汉姆生的《神秘》（1892）同这座小城也关系很深：当地传说他的一部分书稿是在诺格酒店写的"),
    b.PROTO("no-tromso", "Tromsø", "特罗姆瑟", *C("no-tromso"),
            "the small town in the far north of Norway where Alberta Selmer grows up in Cora Sandel's Alberta and Jacob (1926), the first book of the Alberta trilogy. The town is not named, but it is the Tromsø of Sandel's youth, with streets renamed and people invented; her family moved here in 1893",
            "科拉·桑德尔《阿尔贝塔与雅各布》（1926，阿尔贝塔三部曲第一部）里阿尔贝塔·塞尔默长大的那座挪威极北小城。书里没写城名，但它就是桑德尔少女时代的特罗姆瑟，只是街道改了名、人物是虚构的；她家 1893 年搬到这里"),
    b.ORIG("no-royal-palace", "The Royal Palace and the Palace Park, Oslo", "王宫与王宫公园，奥斯陆", *C("no-royal-palace"),
           "The royal residence at the top of Karl Johans gate, in its park, Slottsparken. In Jo Nesbø's The Redbreast (2000) an old man poisons a great oak in the park to clear a line of fire towards the palace balcony, where the Crown Prince is to stand on Constitution Day",
           "卡尔·约翰大街尽头的王室宫殿，周围是王宫公园。尤·奈斯博的《知更鸟》（2000）里，一个老人毒死了公园里一棵大橡树，好清出一条射向王宫阳台的射击线——宪法日那天，王储会站在那座阳台上"),
    b.P("no-trysil", "Trysil", "特吕西尔", *C("no-trysil"), "film_location",
        adaptation={"title": "Out Stealing Horses", "year": 2019, "kind": "电影"},
        scene="汉斯·彼得·莫兰 2019 年把佩尔·帕特森的《外出偷马》拍成电影，斯泰兰·斯卡斯加德演晚年的特龙；电影在挪威东部的特吕西尔乡间拍摄，另有部分在立陶宛。小说本身从不点出地名：1999 年将尽，六十七岁、失去了第二任妻子的特龙·桑德带着狗独自搬进挪威最东边一座湖边的小房子；与唯一的邻居拉尔斯·豪格重逢，唤回了 1948 年的夏天——他跟父亲住在靠近瑞典边境、一条河边的山间牧场，那是死亡与背叛的夏天：一个男孩被枪打死，父亲也为了另一个女人离开了家。摘句不能挂在影视取景地上，所以这本书通过这部电影出现在这里",
        book_ids=["out-stealing-horses"],
        scene_en="Hans Petter Moland filmed Per Petterson's Out Stealing Horses in 2019, with Stellan Skarsgård as the old Trond; it was shot in the countryside of Trysil municipality in eastern Norway, and partly in Lithuania. The novel never names its places: in late 1999 Trond Sander, sixty-seven, who has lost his second wife, moves alone with his dog to a small house by a lake far in the east of Norway; meeting his only neighbour, Lars Haug, brings back the summer of 1948, when he stayed with his father at a summer farm by a river near the Swedish border, a summer of death and betrayal in which a boy was shot dead and his father left the family for another woman. Excerpts cannot be hung on a film location, so the book is shown here through the film"),
    b.PROTO("no-myre", "Myre, Vesterålen", "米勒，韦斯特罗伦", *C("no-myre"),
            "the small coastal community in northern Norway where Tora grows up after the war in Herbjørg Wassmo's The House with the Blind Glass Windows (1981). The book does not name it; Wassmo was born in Myre in Vesterålen in 1942, and most of her books are set in northern Norway",
            "赫比约格·瓦斯莫《盲玻璃阳台的房子》（1981）里，托拉战后长大的那个挪威北部海边小地方。书里没写地名；瓦斯莫 1942 年生在韦斯特罗伦的米勒，她的大多数书都以挪威北部为背景"),
]
lines = [
    b.S("no-sw-1", "sophies-world", "no-lillesand", "The novel as a whole", "全书",
        "Fourteen-year-old Sophie Amundsen comes home from school to find questions in the mailbox, followed by typewritten pages of a course in philosophy, and strange birthday postcards meant for a girl she has never met, Hilde Møller Knag in Lillesand, sent by Hilde's father, a UN major in Lebanon. Sophie's teacher, Alberto Knox, leads her from the first philosophers to the present day, until they realise that they are characters in a book the major is writing as a fifteenth-birthday present for Hilde. On 15 June, in Lillesand, Hilde wakes to the finished ring binder and reads Sophie's story; Sophie and Alberto try to slip out of the major's mind before he comes home.",
        "十四岁的苏菲·阿蒙森放学回家，在信箱里发现几个问题，接着又收到一页页打字的哲学课讲稿，还有寄给一个她从没见过的女孩——利勒桑的希尔德·默勒·克纳格——的生日明信片，寄信人是希尔德在黎巴嫩当联合国少校的父亲。苏菲的老师艾伯特·诺克斯带她从最早的哲学家一路讲到当代，直到两人发现，他们原来是少校为希尔德十五岁生日写的一本书里的人物。6 月 15 日，希尔德在利勒桑醒来，看到那本写好的活页夹，读起苏菲的故事；苏菲和艾伯特则想趁少校回家之前，从他的脑子里溜出去。",
        ["Lillesand"], ["利勒桑"],
        "https://en.wikipedia.org/wiki/Sophie%27s_World; https://kirkusreviews.com/book-reviews/jostein-gaarder/sophies-world/print; https://ursummary.com/sophies-world-summary-jostein-gaarder/; https://litcharts.com/lit/sophie-s-world/chapter-24-the-enlightenment"),
    b.S("no-my-1", "mysteries-hamsun", "no-lillesand", "The novel as a whole", "全书",
        "One midsummer a stranger arrives in a small Norwegian coastal town: Johan Nilsen Nagel, in a loud yellow suit, carrying a violin case. He unsettles the townspeople with his odd whims and stories, defends the Midget, a poor man the town's bullies torment, and falls for Dagny. He carries poison in his pocket; the Midget, whom he befriended, secretly replaces it with water. The town is never named, but the book is closely tied to Lillesand, where local tradition says Hamsun wrote part of it at the Hotel Norge.",
        "一个仲夏，一个陌生人来到挪威一座海边小城：约翰·尼尔森·纳格尔，穿一身扎眼的黄衣服，提着一只小提琴盒。他的种种怪念头和奇谈让镇上的人不安；他替镇上恶棍们欺负的可怜人“小矮子”出头，又爱上了达格妮。他口袋里一直揣着毒药；被他当作朋友的“小矮子”偷偷把它换成了水。小城始终没有名字，但这本书同利勒桑关系很深——当地传说汉姆生有一部分书稿是在那里的诺格酒店写的。",
        ["Lillesand"], ["利勒桑"],
        "https://ebsco.com/research-starters/literature-and-writing/mysteries-knut-hamsun; https://www.ebsco.com/research-starters/literature-and-writing/mysteries-analysis-major-characters; https://www.finn.no/241102439; https://www.dagbladet.no/nyheter/pa-post-for-hamsun/66550475; https://www.klikk.no/motor/baat/raffinert-og-sjarmerende-3069675"),
    b.S("no-al-1", "alberta-trilogy", "no-tromso", "Volume one: Alberta and Jacob", "第一部：《阿尔贝塔与雅各布》",
        "A small town in the far north of Norway, early in the twentieth century. Alberta Selmer, the magistrate's daughter, and her younger brother Jacob grow up in the shadow of their parents' stifled anger, in a home kept up for show on too little money. Jacob breaks out and runs away to sea; dreamy Alberta stays, trapped by the small town's idea of what a young woman should be. In the second volume she is in Paris among the artists of Montparnasse before the First World War, and in the third she becomes a writer. (The town is not named; it is modelled on Tromsø.)",
        "二十世纪初，挪威极北的一座小城。地方法官的女儿阿尔贝塔·塞尔默和弟弟雅各布，在父母压抑的怒气里长大，家里手头拮据，却还要撑着体面。雅各布挣脱出去，跑去当了水手；爱做梦的阿尔贝塔留了下来，被小城对一个年轻女子“该是什么样”的期待困住。第二部里，她在一战前的巴黎，混在蒙帕纳斯的艺术家中间；第三部里，她成了作家。（书里没写城名，原型是特罗姆瑟。）",
        ["Tromsø"], ["特罗姆瑟"],
        "https://booksfromnorway.com/books/506-the-alberta-trilogy.pdf; https://www.finn.no/463839660; https://dannyreviews.com/h/Alberta_Jacob.html; https://lokalhistoriewiki.no/wiki/Cora_Sandel; https://fi.librarything.com/author/sandelcora; https://old.tsu.ge/data/file_db/scandinavian-studies/Per-Thomas-Andersen.pdf"),
    b.S("no-rb-1", "the-redbreast", "no-royal-palace", "The plot against the palace", "针对王宫的阴谋",
        "Two stories run side by side: Norwegian volunteers in German uniform in the trenches outside Leningrad in 1944, and Oslo in 1999–2000. Guarding the American president's motorcade at a toll barrier outside Oslo, Detective Harry Hole shoots a man he takes for an assassin, and is moved to the security service. Meanwhile an old man who has learned he is dying of cancer buys a Märklin rifle, a rare German assassination weapon, and poisons a great oak in the Palace Gardens to clear a line of fire towards the palace balcony. His target is the Crown Prince, on Constitution Day, 17 May.",
        "两条故事线并行：1944 年列宁格勒城外战壕里穿德军军服的挪威志愿兵，和 1999 至 2000 年的奥斯陆。在奥斯陆城外一个收费站为美国总统车队担任警戒时，警探哈利·霍勒开枪打了一个他以为是刺客的人，随后被调去安全局。与此同时，一个得知自己身患癌症、来日无多的老人买下一支马克林步枪——一种罕见的德国暗杀用枪，又毒死了王宫公园里的一棵大橡树，好清出一条射向王宫阳台的射击线。他的目标，是 5 月 17 日宪法日的王储。",
        ["Palace Gardens", "palace"], ["王宫公园", "王宫"],
        "https://www.supersummary.com/the-redbreast/summary/; https://www.wikipedia.org/wiki/The_Redbreast; https://www.goodreads.com/book/show/983435; https://cassiopeiapress.e-bookshelf.de/products/reading-epub/product-id/373065/title/The%2BOslo%2BTrilogy.html"),
    b.S("no-hb-1", "house-blind-glass-windows", "no-myre", "The novel as a whole", "全书",
        "A small coastal community in northern Norway in the years after the war. Tora is the child of a Norwegian mother, Ingrid, and a German soldier who died in the war, and for that she is an outsider, a “German brat”. The family lives in poverty, and her stepfather Henrik, who embodies its hunger and hardship for her, abuses her; Tora keeps silent and tries to hold on to her dignity. It is the first book of the Tora trilogy. (The book names no place; Wassmo was born in Myre in Vesterålen.)",
        "战后几年，挪威北部一个海边的小地方。托拉的母亲英格丽是挪威人，父亲是一个死于战争的德国士兵，她因此被当作外人，一个“德国崽”。一家人过得很穷，继父亨里克在她眼里就是贫穷和饥饿本身，还对她施以侵害；托拉一声不吭，努力守住自己的尊严。这是托拉三部曲的第一部。（书里没写地名；瓦斯莫生在韦斯特罗伦的米勒。）",
        ["Myre"], ["米勒"],
        "https://norla.no/en/books/624-the-house-with-the-blind-glass-windows; https://www.publishersweekly.com/9780931188503; https://www.finn.no/456585427; https://norla.no/nb/books/624; https://snl.no/Herbj%C3%B8rg_Wassmo"),
]
check(books, places, lines)
if __name__ == "__main__":
    M = "11-24: second pack, books added under selection rule v2 (tools/content/batches/add_no2.py)"
    b.append(b.data("books.js"), books, M); b.append(b.data("places.js"), places, M); b.append(b.data("lines.js"), lines, M)
    print(len(books), "books,", len(places), "places,", len(lines), "lines")
