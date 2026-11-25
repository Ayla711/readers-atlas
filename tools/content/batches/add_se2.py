"""11-24: Sweden, second pack: books that selection rule v2 adds (tools/selection/se.md). All in copyright: scene notes in
our own words.
- The Laughing Policeman: the bus terminus on Norra Stationsgatan, Stockholm. The Christmas Oratorio: Sunne.
- Flowering Nettle: Martinson's own childhood in Blekinge; hung at Jämshög, the parish where he was born (place type
  prototype, honest note). City of My Dreams: Södermalm.
Photos: tools/content/batches/add_photos_ch_no_se_1124.py.

Usage: python3 -I tools/content/batches/add_se2.py <app_dir> tools/content/batches/coords/add_se2.json"""
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
    assert {l["book_id"] for l in lines} == {x["id"] for x in books}
    assert {l["place_ids"][0] for l in lines} == pl
b.init(APP, "", "se", DATE)
books = [
    BK("laughing-policeman", "The Laughing Policeman", "大笑的警察", "Den skrattande polisen", "Maj Sjöwall and Per Wahlöö", "马伊·舍瓦尔、佩尔·瓦勒",
       "Maj Sjöwall och Per Wahlöö", "1968", "sv", ["Den skrattande polisen", "Martin Beck", "Åke Stenström", "Kollberg", "Sjowall Wahloo"]),
    BK("christmas-oratorio", "The Christmas Oratorio", "圣诞清唱剧", "Juloratoriet", "Göran Tunström", "约兰·通斯特伦", "Göran Tunström", "1983", "sv",
       ["Juloratoriet", "Sidner Nordensson", "Aron Nordensson", "Solveig", "Tunstrom"]),
    BK("flowering-nettle", "Flowering Nettle", "荨麻开花", "Nässlorna blomma", "Harry Martinson", "哈里·马丁松", "Harry Martinson", "1935", "sv",
       ["Nässlorna blomma", "Martin Tomasson", "Martinson"]),
    BK("city-of-my-dreams", "City of My Dreams", "我梦中的城市", "Mina drömmars stad", "Per Anders Fogelström", "佩尔·安德斯·福格尔斯特伦",
       "Per Anders Fogelström", "1960", "sv", ["Mina drömmars stad", "Henning Nilsson", "Stockholm series", "Fogelstrom"]),
]
places = [
    b.ORIG("se-norra-stationsgatan", "Norra Stationsgatan, Stockholm", "北车站街，斯德哥尔摩", *C("se-norra-stationsgatan"),
           "Street along the northern edge of Stockholm, at the city limit with Solna. In Sjöwall and Wahlöö's The Laughing Policeman (1968) a double-decker bus approaching its terminus here is found with everyone aboard shot dead or wounded",
           "斯德哥尔摩北缘、紧挨着与索尔纳交界处的一条街。舍瓦尔和瓦勒的《大笑的警察》（1968）里，一辆快到这里终点站的双层公交车被发现时，车上的人全部中枪，非死即伤"),
    b.ORIG("se-sunne", "Sunne", "松讷", *C("se-sunne"),
           "Small town in Värmland where Göran Tunström grew up, the son of a priest. The Christmas Oratorio (1983) opens here, as the town gathers once again to perform Bach's Christmas Oratorio",
           "韦姆兰的小城，约兰·通斯特伦作为牧师的儿子在这里长大。《圣诞清唱剧》（1983）在这里开篇：全城的人又一次聚到一起，演唱巴赫的《圣诞清唱剧》"),
    b.PROTO("se-jamshog", "Jämshög, Blekinge", "耶姆舍格，布莱金厄", *C("se-jamshog"),
            "the Blekinge countryside of Harry Martinson's Flowering Nettle (1935), where the parish orphan Martin is boarded out from farm to farm in the 1910s. Martin is Martinson's alter ego and the book tells his own childhood; Martinson was born in the parish of Jämshög in 1904",
            "哈里·马丁松《荨麻开花》（1935）里的布莱金厄乡间——1910 年代，教区孤儿马丁被一家家农庄轮流寄养。马丁就是马丁松的化身，这本书写的是他自己的童年；马丁松 1904 年生在耶姆舍格教区"),
    b.ORIG("se-sodermalm", "Södermalm, Stockholm", "南岛，斯德哥尔摩", *C("se-sodermalm"),
           "The hilly island south of Stockholm's old town, once its poor working-class quarter. Per Anders Fogelström's City of My Dreams (1960), first of his five Stockholm novels, follows working people on Södermalm from 1860 to 1880",
           "斯德哥尔摩老城南边多山的岛，从前是穷苦工人聚居的街区。佩尔·安德斯·福格尔斯特伦的《我梦中的城市》（1960）是他五部斯德哥尔摩小说的第一部，写的是 1860 到 1880 年间南岛上的劳动者"),
]
lines = [
    b.S("se-lp-1", "laughing-policeman", "se-norra-stationsgatan", "The opening", "开篇",
        "A cold, rainy night in Stockholm. A double-decker bus heading for its terminus on Norra Stationsgatan, a few metres from the city limit with Solna, is found with its passengers gunned down by a sub-machine gun: eight are dead and one is wounded. One of the dead is the young detective Åke Stenström, off duty but carrying a pistol, sitting next to a young nurse. Why was he on the bus? Martin Beck and Kollberg come to suspect that the massacre was meant to hide its true target, Stenström himself, who had been quietly investigating the unsolved murder of a Portuguese woman sixteen years before. Beck, a man who rarely laughs, laughs only in the book's last line.",
        "斯德哥尔摩一个又冷又湿的夜晚。一辆开往北车站街终点站的双层公交车——那里离斯德哥尔摩与索尔纳的市界只有几米——被发现时，车上乘客已遭冲锋枪扫射：八人死亡，一人受伤。死者中有年轻的警探奥克·斯滕斯特伦，他当时不在班上，却带着手枪，坐在一个年轻护士旁边。他为什么会在这辆车上？马丁·贝克和科尔贝里渐渐怀疑，这场屠杀是为了掩盖真正的目标——斯滕斯特伦本人：他一直在私下调查十六年前一桩没破的葡萄牙女子谋杀案。很少笑的贝克，直到全书最后一句才笑了出来。",
        ["Norra Stationsgatan"], ["北车站街"],
        "https://www.randomhousebooks.com/books/168101; https://en.wikipedia.org/wiki/The_Laughing_Policeman_(novel); https://www.goodreads.com/book/show/927672; https://pma.knigogid.ru/books/295973-the-laughing-policeman/toread; https://www.salomonssonagency.se/books/den-skrattande-polisen/; https://supersummary.com/the-laughing-policeman/summary"),
    b.S("se-co-1", "christmas-oratorio", "se-sunne", "The novel as a whole", "全书",
        "In Sunne the people gather once again to perform Bach's Christmas Oratorio, and from there the story spreads across three generations, from the 1930s to the 1980s, moving between Värmland and its opposite on the globe, New Zealand. It begins with a catastrophe: Solveig Nordensson, on her way to church to sing, is trampled to death by a herd of cows. Her husband Aron and their son Sidner each shut themselves in their own grief, the loss breaking one and ruining the other, and Sidner searches for a balance between unavoidable sorrow and the healing power of love.",
        "松讷的人们又一次聚到一起，演唱巴赫的《圣诞清唱剧》；故事从这里铺展开去，横跨三代人，从 1930 年代写到 1980 年代，在韦姆兰和地球另一边的新西兰之间来回。一切始于一场灾祸：索尔薇格·努登松在去教堂唱歌的路上，被一群牛踩死了。她的丈夫阿龙和儿子西德纳各自困在自己的悲痛里，这场灾祸击垮了一个，毁了另一个；西德纳则在无法回避的哀伤和爱的疗愈之间寻找平衡。",
        ["Sunne"], ["松讷"],
        "https://bookbeat.com/no/book/juloratoriet-11054; https://www.dagbladet.no/kultur/en-vidtfavnende-fabel/65405919; https://www.norden.org/no/node/5105; https://en.wikipedia.org/wiki/G%C3%B6ran_Tunstr%C3%B6m"),
    b.S("se-fn-1", "flowering-nettle", "se-jamshog", "The novel as a whole", "全书",
        "Blekinge, mostly in the 1910s. Little Martin's father dies, and his mother leaves her children for a new life in California. Martin becomes a parish child, boarded out on one farm after another, a loveless, bleak life lit by his marvellous dreams. Told in the third person from the child's point of view, it is Martinson's own childhood, hardly changed. (Martinson was born in the parish of Jämshög.)",
        "布莱金厄，主要是 1910 年代。小马丁的父亲死了，母亲丢下孩子们去加利福尼亚开始新生活。马丁成了教区的孩子，被一家家农庄轮流寄养，日子冷漠而凄苦，只有他那些奇妙的梦给它照进一点光。小说用第三人称、从孩子的眼光讲述，写的几乎就是马丁松自己的童年。（马丁松生在耶姆舍格教区。）",
        ["Jämshög"], ["耶姆舍格"],
        "https://en.wikipedia.org/wiki/Flowering_Nettle; https://www.goodreads.com/book/show/18074295; https://www.nobelprize.org/nobel_prizes/literature/laureates/1974/martinson-article.html; https://snl.no/Harry_Martinson; https://dbnl.org/tekst/_die004197401_01/_die004197401_01_0131.php; https://en.wikipedia.org/wiki/Harry_Martinson"),
    b.S("se-cd-1", "city-of-my-dreams", "se-sodermalm", "The novel as a whole", "全书",
        "Stockholm, 1860. Henning Nilsson, come from the countryside to find work, gazes at the city that will become his home. Like hundreds of other young men he goes down to Slussen to work in the harbour, and among the poor of Södermalm, often underpaid and overworked, he still finds friendship and love. The novel follows a group of working people on Södermalm until 1880, as Stockholm begins to grow from a provincial town into a city; four more novels follow Henning's family to 1968.",
        "1860 年的斯德哥尔摩。从乡下来找活干的亨宁·尼尔松，望着这座将成为他的家的城市。他像成百上千的年轻人一样，下到闸口去港口干活；在南岛的穷人中间，常被少付工钱、又被累得半死，他还是找到了友谊和爱情。小说跟着南岛上的一群劳动者一直写到 1880 年，斯德哥尔摩也在这些年里开始从一座外省小城长成大城市；之后还有四部小说，把亨宁一家的故事写到 1968 年。",
        ["Södermalm"], ["南岛"],
        "https://www.nordinagency.se/portfolio-item/city-of-my-dreams-2/; https://en.wikipedia.org/wiki/City_of_My_Dreams; https://stockholmskallan.stockholm.se/postfiles/UTB/ArtiklarDirektPress/Hamnar_dirpress_aug_2010.pdf; https://bankersreadbookstoo.blogspot.com/2024/08/the-city-of-my-dreams.html; https://stockholmskallan.stockholm.se/postfiles/SMF/SD/SSMB_0026272_01.pdf"),
]
check(books, places, lines)
if __name__ == "__main__":
    M = "11-24: second pack, books added under selection rule v2 (tools/content/batches/add_se2.py)"
    b.append(b.data("books.js"), books, M); b.append(b.data("places.js"), places, M); b.append(b.data("lines.js"), lines, M)
    print(len(books), "books,", len(places), "places,", len(lines), "lines")
