"""11-24: Finland, third pack: the three famous books held back as "place to be checked" (地点待查), hung on the nearest real
place under the rule for famous books (honest notes), scene notes in our own words (all three in copyright):
- True (Totta): no source we found names the family's city; hung at Helsinki, where Pulkkinen studied and lives
  (place type prototype, honest note).
- Meek Heritage (Hurskas kurjuus): the parishes are unnamed; hung at Hämeenkyrö in Ylä-Satakunta, Sillanpää's birthplace
  (prototype, honest note). Sillanpää died in 1964, so the novel is in copyright in Finland: a scene note.
- The Unknown Soldier: the book only (fi). Its line is at Petrozavodsk (Äänislinna), in the Russian data:
  tools/content/batches/add_ru6.py, which must run after this script.
Photos: tools/content/batches/add_photos_held_1124.py.

Usage: python3 -I tools/content/batches/add_fi3.py <app_dir> tools/content/batches/coords/add_fi3.json"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b

APP = sys.argv[1]
CO = json.load(open(sys.argv[2], encoding="utf-8")) if len(sys.argv) > 2 and sys.argv[2].endswith(".json") else {}
DATE = "2026-11-24"
def C(pid):
    c = CO[pid]; return c["lat"], c["lon"], c["st"], c["su"]
def BK(id, title, title_zh, title_orig, author, author_zh, author_orig, year, lang, aliases, pd=False, src=None):
    return dict(id=id, title=title, title_zh=title_zh, title_orig=title_orig, author=author, author_zh=author_zh, year=year,
                orig_lang=lang, public_domain=pd, source_url=src, author_orig=author_orig, aliases=aliases)
def ids_in(path): return set(re.findall(r'\{ id: "([^"]+)"', open(path, encoding="utf-8").read()))
def check(books, places, lines, ext=(), elsewhere=()):
    """ext: books already in the app (another country's books.js) that get a line here;
    elsewhere: books added here whose line goes into another country's data (another batch script)"""
    allb = set()
    for f in glob.glob(os.path.join(APP, "data", "*", "books.js")): allb |= ids_in(f)
    new = {x["id"] for x in books}
    assert not new & allb, new & allb
    assert set(ext) <= allb, set(ext) - allb
    assert not {p["id"] for p in places} & ids_in(b.data("places.js")) and {p["id"] for p in places} == set(CO)
    assert not {l["id"] for l in lines} & ids_in(b.data("lines.js"))
    bk = new | set(ext)
    for l in lines:
        assert l["book_id"] in bk and l["place_ids"][0] in {p["id"] for p in places}, l["id"]
    assert {l["book_id"] for l in lines} | set(elsewhere) == bk
    assert {l["place_ids"][0] for l in lines} == {p["id"] for p in places}
def run(books, places, lines, script):
    M = f"11-24: famous books hung on their nearest real place (tools/content/batches/{script})"
    for name, xs in (("books.js", books), ("places.js", places), ("lines.js", lines)):
        if xs: b.append(b.data(name), xs, M)
    print(len(books), "books,", len(places), "places,", len(lines), "lines")
b.init(APP, "", "fi", DATE)
books = [
    BK("true-totta", "True", "真相", "Totta", "Riikka Pulkkinen", "里卡·普尔基宁", "Riikka Pulkkinen", "2010", "fi",
       ["Totta", "Elsa", "Martti", "Eeva", "Eleonoora"]),
    BK("meek-heritage", "Meek Heritage", "虔诚的贫困", "Hurskas kurjuus", "F. E. Sillanpää", "弗兰斯·埃米尔·西兰帕", "F. E. Sillanpää",
       "1919", "fi", ["Hurskas kurjuus", "Hurskas kurjuus: Päättynyt suomalainen elämäkerta", "Juha Toivola", "Toivolan Juha"]),
    BK("unknown-soldier", "The Unknown Soldier", "无名战士", "Tuntematon sotilas", "Väinö Linna", "韦伊诺·林纳", "Väinö Linna",
       "1954", "fi", ["Tuntematon sotilas", "Unknown Soldiers", "Rokka", "Koskela", "Hietanen", "Rahikainen"]),
]
places = [
    b.PROTO("fi-helsinki", "Helsinki", "赫尔辛基", *C("fi-helsinki"),
            "the city where Elsa, Martti and their family live in Riikka Pulkkinen's True (2010). No source we found names it; the book is hung at Helsinki, where Pulkkinen studied and lives, as the nearest real place",
            "里卡·普尔基宁《真相》（2010）里埃尔莎、马尔蒂一家生活的城市。查到的资料都没有点明是哪座城市；普尔基宁在赫尔辛基读书、生活，这本书就近挂在赫尔辛基"),
    b.PROTO("fi-hameenkyro", "Hämeenkyrö", "海门屈勒", *C("fi-hameenkyro"),
            "the farming parish in north-eastern Satakunta where Juha Toivola is born in F. E. Sillanpää's Meek Heritage (1919). The parish is not named; Sillanpää was born in Hämeenkyrö, in Ylä-Satakunta, in 1888, and the book is hung there as the nearest real place",
            "弗兰斯·埃米尔·西兰帕《虔诚的贫困》（1919）里尤哈·托伊沃拉出生的那个萨塔昆塔东北部的农村教区。书里没写教区名；西兰帕 1888 年生在上萨塔昆塔的海门屈勒，这本书就近挂在这里"),
]
lines = [
    b.S("fi-tt-1", "true-totta", "fi-helsinki", "The novel as a whole", "全书",
        "Elsa, a well-known child psychologist, is dying of cancer at home. Her husband Martti, a painter of about seventy, and their daughter Eleonoora, a doctor, cannot imagine life without her. When Eleonoora's daughter Anna takes a dress from the wardrobe, it turns out to belong not to Elsa but to Eeva, the young woman who once lived with the family as Eleonoora's nanny, and with whom Martti had a long affair while Elsa was away on her scholarly trips. Eeva's story comes back, and with it the question of what memory keeps and what a lie can spare. (No source we found names the city; the book is shown at Helsinki, where Pulkkinen lives.)",
        "著名的儿童心理学家埃尔莎癌症晚期，在家里等待死亡。她的丈夫、七十岁上下的画家马尔蒂，和当医生的女儿埃莱奥诺拉，都无法想象没有她的日子。埃莱奥诺拉的女儿安娜从衣柜里拿出一条裙子，结果发现它不是埃尔莎的，而是埃娃的——这个年轻女人当年住在他们家，给小时候的埃莱奥诺拉当保姆；埃尔莎外出做学术旅行的时候，马尔蒂和她有过一段很长的私情。埃娃的故事被重新翻出来，随之而来的问题是：记忆留下了什么，一个谎言又能免去什么。（查到的资料没有点明城市；这本书挂在普尔基宁生活的赫尔辛基。）",
        ["Helsinki"], ["赫尔辛基"],
        "https://www.ahlbackagency.com/?p=17207; https://www.booksfromfinland.fi/?p=10224; https://books.apple.com/us/book/true/id447718817; https://en.wikipedia.org/wiki/Riikka_Pulkkinen"),
    b.S("fi-mh-1", "meek-heritage", "fi-hameenkyro", "The novel as a whole", "全书",
        "The life of Juha Toivola, born in 1857, a farmer's son in a parish of north-eastern Satakunta. In the famine years his drunken father loses the farm, as the better-off buy up land for bread. Juha drifts through life as a farmhand and then a crofter, poor, slow and meek, while death after death strikes his family; when he is given the vote, he does not bother to use it. In the civil war of 1918 he goes along with the Reds, for the pay and for a change from his dreary days, and after their defeat he is among the rebels the Whites put to death. (The parish is not named; Sillanpää was born in Hämeenkyrö.)",
        "尤哈·托伊沃拉的一生。他生于 1857 年，是萨塔昆塔东北部一个教区里的农家儿子。荒年里，他那酗酒的父亲丢了农庄——日子好过些的人拿面包换走了穷人的地。尤哈当过长工，后来当了佃农，贫穷、迟钝、逆来顺受，家里接二连三地死人；给了他选举权，他也懒得去投票。1918 年内战，他跟着赤卫队走了，为的是那份饷钱，也为了摆脱沉闷的日子；赤卫队失败后，他成了被白军处死的起事者之一。（书里没写教区名；西兰帕生在海门屈勒。）",
        ["Hämeenkyrö"], ["海门屈勒"],
        "https://www.gutenberg.org/ebooks/46758; https://caponeu.eu/cdp/novels/hurskas-kurjuus-paattynyt-suomalainen-elamakerta; https://en.wikipedia.org/wiki/Frans_Eemil_Sillanp%C3%A4%C3%A4"),
]
check(books, places, lines, elsewhere={"unknown-soldier"})
if __name__ == "__main__":
    run(books, places, lines, "add_fi3.py")
