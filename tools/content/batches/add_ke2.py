"""11-24: Kenya, second pack: the three books that selection rule v2 adds (tools/selection/ke.md).
A Grain of Wheat, The River and the Source, Coming to Birth. All in copyright: scene notes in our own words.
Thabai, the village of A Grain of Wheat, is invented; it is a version of Ngũgĩ's own village Kamiriithu, by Limuru
(EBSCO Research Starters, 'A Grain of Wheat: Analysis of Setting'), so the book hangs at Limuru. Limuru comes back with the
same id, coordinates and photo it had before del_v2_1124.py.
The River and the Source begins in Yimbo and moves to Sakwa; neither has coordinates on Wikipedia. Both lie in today's
Bondo sub-county of Siaya (wards of Bondo Constituency), so the book hangs at Bondo town. No photo yet for Bondo or Nairobi.

Usage: python3 -I tools/content/batches/add_ke2.py <app_dir> tools/content/batches/coords/add_ke2.json"""
import glob, json, os, re, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b

APP, CO = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8"))
DATE = "2026-11-24"
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
    oldp = ids_in(b.data("places.js"))
    assert not {p["id"] for p in places} & oldp and {p["id"] for p in places} == set(CO)
    assert not {l["id"] for l in lines} & ids_in(b.data("lines.js"))
    for l in lines:
        assert l["book_id"] in {x["id"] for x in books} and l["place_ids"][0] in {p["id"] for p in places}, l["id"]
    assert {l["book_id"] for l in lines} == {x["id"] for x in books}
    assert {l["place_ids"][0] for l in lines} == {p["id"] for p in places}
def restore_photo(pid, row):
    src = os.path.join(APP, "_to_delete", "photos_del_v2_1124", pid + ".jpg"); dst = os.path.join(APP, "images", "places", pid + ".jpg")
    if not os.path.exists(dst): shutil.copyfile(src, dst)
    cred = os.path.join(APP, "docs", "photo-credits.md"); t = open(cred, encoding="utf-8").read()
    if row not in t:
        open(cred + ".new", "w", encoding="utf-8").write(t.rstrip("\n") + "\n" + row + "\n"); os.replace(cred + ".new", cred)
b.init(APP, "", "ke", DATE)
LIMURU_PHOTO = {"file": "images/places/ke-limuru.jpg", "width": 800, "height": 600, "author": "Mekami", "license": "CC BY-SA 4.0",
                "license_url": "https://creativecommons.org/licenses/by-sa/4.0", "source": "https://commons.wikimedia.org/wiki/File%3ALimuru_tea_farms.jpg",
                "alt_en": "Tea fields on the hills at Limuru", "alt_zh": "利穆鲁山坡上的茶园"}
LIMURU_CREDIT = "| Limuru | Mekami | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0) | [Commons](https://commons.wikimedia.org/wiki/File%3ALimuru_tea_farms.jpg) |"
books = [
    BK("grain-of-wheat", "A Grain of Wheat", "一粒麦种", "A Grain of Wheat", "Ngũgĩ wa Thiong'o", "恩古吉·瓦·提安哥", "Ngũgĩ wa Thiong'o", "1967", "en",
       ["Thabai", "Mugo", "Kihika", "Gikonyo", "Mumbi", "Uhuru", "Ngugi", "James Ngugi"]),
    BK("river-and-the-source", "The River and the Source", "河与源", "The River and the Source", "Margaret A. Ogola", "玛格丽特·奥戈拉", "Margaret A. Ogola", "1994", "en",
       ["Akoko", "Nyabera", "Awiti", "Wandia", "Yimbo", "Sakwa", "Aluor", "Ogola"]),
    BK("coming-to-birth", "Coming to Birth", "诞生", "Coming to Birth", "Marjorie Oludhe Macgoye", "玛乔丽·奥卢德·麦戈耶", "Marjorie Oludhe Macgoye", "1986", "en",
       ["Paulina", "Martin Were", "Macgoye", "Sinclair Prize"]),
]
places = [
    b.ORIG("ke-limuru", "Limuru", "利穆鲁", *C("ke-limuru"),
           "Town in the Kikuyu highlands north-west of Nairobi. Ngũgĩ wa Thiong'o was born in 1938 at Kamiriithu, close by. Thabai, the village of A Grain of Wheat, is an invented one modelled on Kamiriithu, so the book hangs here; he wrote it as a student at Leeds",
           "内罗毕西北基库尤高地上的小镇。恩古吉·瓦·提安哥 1938 年出生在附近的卡米里图。《一粒麦种》里的塔拜村是虚构的，以卡米里图为原型，所以这本书挂在这里；书是他在利兹读书时写的",
           photo=LIMURU_PHOTO),
    b.ORIG("ke-bondo", "Bondo, Siaya County", "邦多，锡亚亚郡", *C("ke-bondo"),
           "Town in Luo country near Lake Victoria. The River and the Source opens in Yimbo, where Akoko is born a chief's daughter, and moves to Sakwa, where she marries; both are in today's Bondo sub-county, and neither has a point of its own on the map, so the book hangs at the town",
           "维多利亚湖附近卢奥人地区的小镇。《河与源》从因博开始，阿科科作为酋长的女儿生在那里，后来嫁到萨夸；两处今天都属邦多县，地图上都找不到自己的坐标，所以这本书挂在镇上"),
    b.ORIG("ke-nairobi", "Nairobi", "内罗毕", *C("ke-nairobi"),
           "Capital of Kenya. In Coming to Birth the sixteen-year-old Paulina comes here from her village in western Kenya to join her husband Martin; the book follows her through the city's years before and after independence. The pin is the city's own point",
           "肯尼亚首都。《诞生》里，十六岁的保利娜从肯尼亚西部的村子来到这里，和丈夫马丁团聚；全书跟着她走过这座城市独立前后的岁月。图钉标的是城市本身的位置"),
]
lines = [
    b.S("ke-gw-1", "grain-of-wheat", "ke-limuru", "The novel as a whole", "全书",
        "The days before Uhuru, Kenya's independence, in 1963, in the Gikuyu village of Thabai. The village wants to honour Kihika, a forest fighter hanged during the Emergency, and asks Mugo, a quiet man it takes for a hero of the detention camps, to speak. Mugo is the one who betrayed Kihika. Around him are Gikonyo, back from the camps, and his wife Mumbi, Kihika's sister, who bore a child to the collaborator Karanja while he was away. On the day itself Mugo confesses before the crowd.",
        "1963 年肯尼亚独立（“乌呼鲁”）前的几天，基库尤村庄塔拜。村里人要纪念紧急状态时期被绞死的丛林战士基希卡，请沉默寡言的穆戈来讲话——大家以为他是拘留营里的英雄。出卖基希卡的正是穆戈。他身边是从拘留营回来的吉孔约，和吉孔约的妻子、基希卡的妹妹蒙比；吉孔约不在的时候，她给通敌的卡兰贾生了一个孩子。独立那天，穆戈当众认了罪。",
        ["Thabai"], ["塔拜"], "https://en.wikipedia.org/wiki/A_Grain_of_Wheat; https://www.ebsco.com/research-starters/literature-and-writing/grain-wheat-analysis-setting"),
    b.S("ke-rs-1", "river-and-the-source", "ke-bondo", "Part one: Akoko", "第一部：阿科科",
        "The novel follows four generations of Kenyan women over about a hundred years. It begins around 1870 with the birth of Akoko, first daughter after seven sons of the chief of Yimbo. She marries into Sakwa; when her husband and sons are dead she goes back to Yimbo, and then with her daughter Nyabera to the Catholic mission at Aluor. From there the story passes to Nyabera's daughter Awiti and to Wandia, in a changed country.",
        "小说写了四代肯尼亚女人、大约一百年的事。开头是 1870 年前后阿科科出生——因博酋长有了七个儿子之后的第一个女儿。她嫁到萨夸；丈夫和儿子们死后，她回到因博，又带着女儿尼亚贝拉去了阿卢奥尔的天主教传教站。故事从那里传到尼亚贝拉的女儿阿维蒂，再到万迪娅，国家已经变了样。",
        ["Yimbo"], ["因博"], "https://www.gradesaver.com/the-river-and-the-source/study-guide/summary; https://www.advance-africa.com/The-River-and-the-Source.html; https://en.wikipedia.org/wiki/Margaret_Ogola"),
    b.S("ke-cb-1", "coming-to-birth", "ke-nairobi", "The novel as a whole", "全书",
        "At sixteen Paulina leaves her village in western Kenya for Nairobi, to join her new husband Martin Were. She loses one pregnancy after another and the marriage wears thin; she moves to Kisumu, where she teaches and sews and has a child by a married man. The novel sets her slow growth into a person of her own beside the country's passage out of colonial rule, and brings her back to Nairobi and to Martin.",
        "十六岁的保利娜离开肯尼亚西部的村子去内罗毕，和新婚丈夫马丁·韦雷团聚。她一次次流产，婚姻渐渐磨薄；她搬到基苏木，教书、做裁缝，和一个有妇之夫生了孩子。小说把她慢慢长成一个独立的人的过程，和这个国家走出殖民统治的过程并排来写，最后让她回到内罗毕，回到马丁身边。",
        ["Nairobi"], ["内罗毕"], "https://kirkusreviews.com/book-reviews/marjorie-oludhe-macgoye/coming-to-birth/print; https://newlinesmag.com/first-person/end-of-colonial-kenya-reflected-in-its-own-literature/; https://en.wikipedia.org/wiki/Marjorie_Oludhe_Macgoye"),
]
check(books, places, lines)
if __name__ == "__main__":
    M = "11-24: second pack, three books added under selection rule v2 (tools/content/batches/add_ke2.py)"
    b.append(b.data("books.js"), books, M); b.append(b.data("places.js"), places, M); b.append(b.data("lines.js"), lines, M)
    restore_photo("ke-limuru", LIMURU_CREDIT)
    print(len(books), "books,", len(places), "places,", len(lines), "lines")
