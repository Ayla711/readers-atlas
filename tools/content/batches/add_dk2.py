"""11-24: Denmark, second pack: books of the Danish Culture Canon (2006) that selection rule v2 adds (tools/selection/dk.md).
All three are in the public domain. The quotations are cut from the Royal Danish Library's text portal (Arkiv for Dansk Litteratur,
tekster.kb.dk), read in the browser on 11-24, because this shell cannot reach kb.dk and Project Gutenberg was down for maintenance;
each is made of whole paragraphs (for Jammers Minde, the whole dateline), copied as the portal prints it. English and Chinese are our own.
- The Rector of Veilbye (Blicher, 1829): the paragraph before the body is dug up in the rector's garden. The real rector,
  Søren Jensen Quist, was beheaded in 1626; the pin is Vejlby parish near Grenaa.
- Ved Vejen (Bang, 1886): the station of the novel has no name; the book was inspired by a glimpse at Skørping station in 1883,
  so the pin is Skørping station (place type prototype). The quotation is from the opening, the stationmaster on the platform.
- Jammers Minde (Leonora Christina, completed 1674): the dateline of her preface to her children, written in the Blue Tower
  of Copenhagen Castle. The tower was pulled down in 1731–32; the pin is the article coordinates of Blåtårn.
Winter's Tales (Blixen) is still to come: its place is not found yet. No photos yet for the three places.

Usage: python3 -I tools/content/batches/add_dk2.py <app_dir> tools/content/batches/coords/add_dk2.json"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b

APP, CO = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8"))
DATE = "2026-11-24"
KB = "https://tekster.kb.dk/text/"
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
    assert not {p["id"] for p in places} & ids_in(b.data("places.js")) and {p["id"] for p in places} == set(CO)
    assert not {l["id"] for l in lines} & ids_in(b.data("lines.js"))
    for l in lines:
        assert l["book_id"] in {x["id"] for x in books} and l["place_ids"][0] in {p["id"] for p in places}, l["id"]
    assert {l["book_id"] for l in lines} == {x["id"] for x in books}
    assert {l["place_ids"][0] for l in lines} == {p["id"] for p in places}
def Q(id, book, place, loc, loc_zh, work, orig, hl_orig, en, hl_en, zh, hl_zh, note=""):
    assert "[" not in orig and "\xa0" not in orig and not re.search(r"[A-Za-zæøå]\d", orig), id   # no footnote numbers
    for text, hls in ((orig, hl_orig), (en, hl_en), (zh, hl_zh)):
        for h in hls: assert h in text, (id, h)
    return dict(id=id, book_id=book, place_ids=[place], location=loc, location_zh=loc_zh, text_orig=orig, highlight_orig=hl_orig,
                text_en=en, highlight_en=hl_en, text_zh=zh, highlight_zh=hl_zh, translation="own", status="draft",
                checked=f"Arkiv for Dansk Litteratur (tekster.kb.dk), {work}{note}, {DATE}")
b.init(APP, "", "dk", DATE)
books = [
    BK("praesten-i-vejlbye", "The Rector of Veilbye", "维尔比的牧师", "Præsten i Vejlbye", "Steen Steensen Blicher", "斯滕·斯滕森·布利克",
       "Steen Steensen Blicher", "1829", "da", ["Præsten i Vejlby", "The Parson of Veilbye", "Søren Qvist", "Erik Sørensen", "Morten Bruus", "Blicher"],
       pd=True, src=KB + "adl-texts-blich04-shoot-workid75253"),
    BK("ved-vejen", "Ved Vejen", "路边", "Ved Vejen", "Herman Bang", "赫尔曼·邦", "Herman Bang", "1886", "da",
       ["Katinka", "By the Wayside", "Katinka Bai", "Huus", "Stille Eksistenser", "Bang"], pd=True, src=KB + "adl-texts-bang01val-shoot-workid54382"),
    BK("jammers-minde", "Jammers Minde (Memoirs of Leonora Christina)", "苦难回忆", "Jammers Minde", "Leonora Christina", "莱奥诺拉·克里斯蒂娜",
       "Leonora Christina Ulfeldt", "1674", "da", ["Jammers Minde", "A Memory of Lament", "Memoirs of Leonora Christina", "Blåtårn", "Blue Tower",
       "Leonora Christina Ulfeldt"], pd=True, src=KB + "adl-texts-leonora01-shoot-workid66408"),
]
places = [
    b.ORIG("dk-vejlby", "Vejlby, near Grenaa (Djursland)", "维尔比，格雷诺附近（尤尔斯兰半岛）", *C("dk-vejlby"),
           "Parish just south-west of Grenaa on Djursland. Its rector Søren Jensen Quist was convicted of killing his farmhand and beheaded in 1626; Blicher made the case into The Rector of Veilbye (1829), told through the diary of the district judge who is to marry the rector's daughter. Vejlby Church, the parish church of the story, still stands",
           "尤尔斯兰半岛上、格雷诺西南不远的一个教区。这里的牧师索伦·延森·奎斯特被判打死了自己的长工，1626 年斩首；布利克把这桩案子写成了《维尔比的牧师》（1829），由将要娶牧师女儿的地方法官用日记讲出来。故事里的维尔比教堂至今还在"),
    b.PROTO("dk-skorping", "Skørping Station", "斯科尔平火车站", *C("dk-skorping"),
            "the small country station of Bang's Ved Vejen (1886), where the stationmaster's wife Katinka Bai lives out her quiet life. The station in the novel has no name; the book was inspired by a moment in 1883 when Bang's train passed through Skørping and he saw a pale young woman at a window, her face in her hands, watching it go",
            "邦的《路边》（1886）里那个乡下小站，站长的妻子卡廷卡·拜在这里过着无声无息的日子。小说里的车站没有名字；这本书的灵感来自 1883 年的一刻：邦的火车经过斯科尔平，他看见窗口有个脸色苍白的年轻女人，双手捧着脸，望着火车开走"),
    b.ORIG("dk-blataarn", "Site of the Blue Tower (Blåtårn), Slotsholmen, Copenhagen", "蓝塔旧址，斯洛特斯霍尔门岛，哥本哈根", *C("dk-blataarn"),
           "The Blue Tower was the great entrance tower of Copenhagen Castle and served as its prison. Leonora Christina, daughter of Christian IV, was held here from 1663 to 1685 and began Jammers Minde here. Castle and tower were pulled down in 1731–32 to make room for the first Christiansborg Palace",
           "蓝塔是哥本哈根城堡的大门塔楼，也是城堡的监狱。克里斯蒂安四世的女儿莱奥诺拉·克里斯蒂娜 1663 年到 1685 年被关在这里，《苦难回忆》就是在塔中动笔的。城堡和塔楼在 1731–32 年拆除，原地建起了第一座克里斯蒂安堡宫"),
]
lines = [
    Q("dk-pv-1", "praesten-i-vejlbye", "dk-vejlby", "The judge's diary, before the search of the garden", "法官日记：搜园子之前", "Præsten i Vejlbye",
      "Jeg drog da, tilligemed Klageren og Vidnerne, til Vejlbye med et saare beknyt Sind, mindre af Frygt for at finde den omhandlede Rømningsmand i Haugen, end af Bekymring over den Skræk og Ærgrelse, Præsten og min Kjereste derved vilde foraarsages. Underveis tænkte jeg blot paa, at lade Bagvaskeren føle Lovens hele Strænghed. Ak! du milde Himmel! der forestod mig den grueligste Opdagelse.",
      ["Vejlbye"],
      "So I drove to Vejlbye with the accuser and the witnesses, with a heavy heart, less for fear of finding the runaway in question in the garden than for worry over the fright and vexation it would cause the rector and my sweetheart. On the way I thought only of making the slanderer feel the full severity of the law. Alas! merciful heaven! the most dreadful discovery lay before me.",
      ["Vejlbye"],
      "于是我同原告和证人一道去维尔比，心里十分沉重——倒不是怕在园子里找到那个逃走的人，而是担心这会给牧师和我的心上人带来多少惊吓和烦恼。一路上我只想着，要叫那个诽谤的人尝尝法律的全部厉害。唉！慈悲的上天！等着我的，却是最可怕的发现。",
      ["维尔比"]),
    Q("dk-vv-1", "ved-vejen", "dk-skorping", "Chapter I, the opening", "第一章开头", "Ved Vejen",
      "Han fik tændt en Cigarstump og gik ud paa Perronen. Naar han gik saadan op og ned, stram i Tøjet, og Hænderne i begge Jakkelommerne, saa' man Løjtnanten endnu. Ogsaa paa Benene, de havde beholdt Rundingen fra Kavalleriet.\nFem-seks Bønderkarle var kommet og stod og skrævede i en Klump midtvejs ud for Stationsbygningen; Stationskarlen slæbte Godset frem, en enlig grønmalet Kasse, der saa' ud som den var tabt ved Kanten af Vejen.",
      ["Perronen", "Stationsbygningen"],
      "He got a cigar stub lit and went out on to the platform. When he walked up and down like that, buttoned tight, with his hands in both jacket pockets, you could still see the lieutenant in him. In his legs too: they had kept the bow of the cavalry.\nFive or six farmhands had come and stood straddle-legged in a clump halfway along, in front of the station building; the porter dragged the goods forward, a lone green-painted crate that looked as if it had been dropped at the edge of the road.",
      ["platform", "station building"],
      "他点着一截雪茄头，走到站台上。他这样走来走去，衣服扣得紧紧的，两手插在上衣口袋里，人们还看得出他当年那个中尉的样子。腿上也看得出：还留着骑兵的那道弯。\n五六个农家长工来了，叉开腿挤成一团，站在站房前面的半当中；站上的伙计把货物拖出来，是孤零零的一只绿漆木箱，看上去像是谁掉在路边上的。",
      ["站台", "站房"], note=" (second and third paragraphs)"),
    Q("dk-jm-1", "jammers-minde", "dk-blataarn", "The dateline of the preface “To my children”", "《致我的孩子们》序言的落款", "Jammers Minde",
      "Skreven i det blaa Taarn Anno 1674 den 11. Juni mit Fængsels det elfte Aar, min Fødsels-Dag, og Alders 53. Aar.",
      ["det blaa Taarn"],
      "Written in the Blue Tower, in the year 1674, the 11th of June, the eleventh year of my imprisonment, my birthday, and the 53rd year of my age.",
      ["Blue Tower"],
      "写于蓝塔，1674 年 6 月 11 日，我被囚的第十一年，我的生日，我的第五十三岁。",
      ["蓝塔"], note=" (the edition sets the dateline in four short lines; joined here)"),
]
check(books, places, lines)
if __name__ == "__main__":
    M = "11-24: second pack, Danish Culture Canon books added under selection rule v2 (tools/content/batches/add_dk2.py)"
    b.append(b.data("books.js"), books, M); b.append(b.data("places.js"), places, M); b.append(b.data("lines.js"), lines, M)
    print(len(books), "books,", len(places), "places,", len(lines), "lines")
