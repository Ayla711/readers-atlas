"""11-24: Morocco, second pack: the five books that selection rule v2 adds (tools/selection/ma.md) and that are set in Morocco.
The Sacred Night, La Boîte à merveilles, This Blinding Absence of Light, The Alchemist (its Tangier part), Naked Lunch.
All five are in copyright, so each gets a scene note in our own words, no quotation.
Not in this pack: The Woman and the Rose (Zafzaf) is set in Torremolinos, Spain, and only ends in Morocco, so it is not counted
as a Moroccan setting (English Wikipedia, The Woman and the Rose).
Fes el Bali comes back: it went with Au Maroc in del_v2_1124.py and La Boîte à merveilles is set in it; same id, same coordinates,
same photo (moved back from _to_delete/photos_del_v2_1124/, credit row restored).
Agadir and Tazmamart have no photo yet.

Usage: python3 -I tools/content/batches/add_ma2.py <app_dir> tools/content/batches/coords/add_ma2.json"""
import json, os, re, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b

APP, CO = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8"))
b.init(APP, "", "ma", "2026-11-24")
def C(pid):
    c = CO[pid]; return c["lat"], c["lon"], c["st"], c["su"]
def BK(id, title, title_zh, title_orig, author, author_zh, author_orig, year, lang, aliases):
    return dict(id=id, title=title, title_zh=title_zh, title_orig=title_orig, author=author, author_zh=author_zh, year=year,
                orig_lang=lang, public_domain=False, source_url=None, author_orig=author_orig, aliases=aliases)

FEZ_PHOTO = {"file": "images/places/ma-fez.jpg", "width": 800, "height": 400, "author": "Hiroki Ogawa", "license": "CC BY 3.0",
             "license_url": "https://creativecommons.org/licenses/by/3.0",
             "source": "https://commons.wikimedia.org/wiki/File%3APanorama_Fes_el_Bali_Borj_Sud_Fez_morocco_-_panoramio.jpg",
             "alt_en": "Fes el Bali seen from the Borj Sud", "alt_zh": "从南堡眺望非斯老城"}
FEZ_CREDIT = "| Fes el Bali (old Fez) | Hiroki Ogawa | [CC BY 3.0](https://creativecommons.org/licenses/by/3.0) | [Commons](https://commons.wikimedia.org/wiki/File%3APanorama_Fes_el_Bali_Borj_Sud_Fez_morocco_-_panoramio.jpg) |"

books = [
    BK("sacred-night", "The Sacred Night", "神圣的夜晚", "La Nuit sacrée", "Tahar Ben Jelloun", "塔哈尔·本·杰伦", "Tahar Ben Jelloun", "1987", "fr",
       ["La Nuit sacree", "Zahra", "the Consul", "Ben Jelloun", "Prix Goncourt 1987"]),
    BK("boite-a-merveilles", "La Boîte à merveilles", "奇妙的盒子", "La Boîte à merveilles", "Ahmed Sefrioui", "艾哈迈德·塞弗留伊", "Ahmed Sefrioui", "1954", "fr",
       ["The Box of Wonders", "La Boite a merveilles", "Sidi Mohammed", "Dar Chouafa", "Sefrioui"]),
    BK("blinding-absence-of-light", "This Blinding Absence of Light", "那耀眼的黑暗", "Cette aveuglante absence de lumière", "Tahar Ben Jelloun", "塔哈尔·本·杰伦", "Tahar Ben Jelloun", "2001", "fr",
       ["Cette aveuglante absence de lumiere", "Tazmamart", "Ben Jelloun"]),
    BK("the-alchemist", "The Alchemist", "牧羊少年奇幻之旅", "O Alquimista", "Paulo Coelho", "保罗·柯艾略", "Paulo Coelho", "1988", "pt",
       ["O Alquimista", "Santiago", "crystal merchant", "Coelho", "炼金术士"]),
    BK("naked-lunch", "Naked Lunch", "裸体午餐", "Naked Lunch", "William S. Burroughs", "威廉·巴勒斯", "William S. Burroughs", "1959", "en",
       ["The Naked Lunch", "Interzone", "William Lee", "Burroughs"]),
]
places = [
    b.ORIG("ma-fez", "Fes el Bali (old Fez)", "非斯老城", *C("ma-fez"),
           "The walled old city of Fez. Ahmed Sefrioui was born here in 1915, and La Boîte à merveilles (1954) is his childhood in it: a shared house in the medina called Dar Chouafa, the Koranic school, the baths, the shrines his mother takes him to",
           "非斯有城墙环绕的老城。艾哈迈德·塞弗留伊 1915 年生在这里，《奇妙的盒子》（1954）写的就是他在老城里的童年：一座叫“算命人之家”的合住院子、古兰经学堂、澡堂，还有母亲带他去的圣陵",
           photo=FEZ_PHOTO),
    b.ORIG("ma-agadir", "Agadir", "阿加迪尔", *C("ma-agadir"),
           "City on Morocco's Atlantic coast, north of the mouth of the Souss. The middle of The Sacred Night happens here: the narrator arrives after leaving her family, and is taken in by the woman who keeps the hammam and her blind brother, the Consul",
           "摩洛哥大西洋岸边的城市，在苏斯河口以北。《神圣的夜晚》的中段发生在这里：叙述者离家之后来到此地，被澡堂的女掌柜和她失明的弟弟“领事”收留"),
    b.ORIG("ma-tazmamart", "Site of Tazmamart prison", "塔兹马马特监狱旧址", *C("ma-tazmamart"),
           "Site of the secret prison on the edge of the High Atlas near Er-Rich, where 58 army officers were held after the failed coups against Hassan II, in single underground cells without light. It was closed in 1991; 30 prisoners came out alive. This Blinding Absence of Light is told by one of them. The pin is the point English Wikipedia gives for the prison; almost nothing stands there now",
           "高阿特拉斯山边缘、里什附近的秘密监狱旧址。针对哈桑二世的政变失败后，58 名军官被关在这里不见光的地下单人牢房里。监狱 1991 年关闭，活着出来的有 30 人。《那耀眼的黑暗》由其中一人讲述。图钉标的是英文维基给出的监狱位置，如今那里几乎什么都不剩"),
]
lines = [
    b.S("ma-sn-1", "sacred-night", "ma-agadir", "The Agadir chapters", "阿加迪尔的几章",
        "The narrator was raised as a son, Ahmed, because her father wanted an heir. After burying him she leaves her family and travels across Morocco to find out who she is as a woman. In Agadir the woman who sits at the door of the hammam takes her home to keep her blind brother, the Consul, company; she and the Consul become lovers. The sister's jealousy brings the narrator's uncle to Agadir to accuse her, and she kills him and goes to prison.",
        "叙述者从小被当作儿子“艾哈迈德”养大，因为父亲想要一个继承人。埋葬了父亲之后，她离开家，走遍摩洛哥，想弄清作为女人的自己是谁。在阿加迪尔，坐在澡堂门口的女掌柜把她带回家，给失明的弟弟“领事”作伴；她和领事成了情人。姐姐的嫉妒把叙述者的叔叔引到阿加迪尔来指控她，她杀了他，进了监狱。",
        ["Agadir"], ["阿加迪尔"], "https://fr.wikipedia.org/wiki/La_Nuit_sacr%C3%A9e"),
    b.S("ma-bm-1", "boite-a-merveilles", "ma-fez", "The book as a whole", "全书",
        "Sidi Mohammed, six years old and lonely, lives with his parents on the second floor of Dar Chouafa, a house in the old medina of Fez whose ground floor belongs to a fortune-teller. He tells of the neighbours on each floor, the Koranic school, and the box in which he keeps glass marbles and dried flowers, his only friends. When his father, a weaver, loses his savings and leaves the city to find work, the quiet of the house is broken until he comes back.",
        "六岁的西迪·穆罕默德很孤单，和父母住在“算命人之家”的三楼。这是非斯老城里的一座院子，底层住着一位算命的女人。他讲每层楼的邻居，讲古兰经学堂，讲那只盒子——里面收着玻璃弹珠和干花，是他仅有的朋友。当织工的父亲丢了积蓄，离城去找活干，院子里的平静被打破，直到父亲回来。",
        ["Fez"], ["非斯"], "https://fr.wikipedia.org/wiki/La_Bo%C3%AEte_%C3%A0_merveilles; https://en.wikipedia.org/wiki/Ahmed_Sefrioui"),
    b.S("ma-ba-1", "blinding-absence-of-light", "ma-tazmamart", "The novel as a whole", "全书",
        "A novel built on the testimony of a man who survived Tazmamart. The narrator is a soldier sent there after the failed coup against Hassan II; his cell is too low to stand in and has no light. The book is about how the prisoners stay alive in the dark, through prayer, through stories told from cell to cell, through memory and imagination, while one after another of them dies.",
        "这部小说以一位塔兹马马特幸存者的证词为底本。叙述者是一名军人，针对哈桑二世的政变失败后被关到这里；牢房矮得站不直，没有一点光。书里写的是囚犯怎样在黑暗里活下去：靠祈祷，靠隔着牢房讲故事，靠记忆和想象，而身边的人一个接一个死去。",
        ["Tazmamart"], ["塔兹马马特"], "https://en.wikipedia.org/wiki/This_Blinding_Absence_of_Light; https://en.wikipedia.org/wiki/Tazmamart"),
    b.S("ma-al-1", "the-alchemist", "ma-tangier", "The Tangier chapters", "丹吉尔的几章",
        "Santiago, an Andalusian shepherd, sells his sheep and crosses the strait to look for a treasure he has dreamed of at the Egyptian pyramids. On his first day in Tangier a man who offers to guide him takes all his money. He goes to work for a crystal merchant in the town, and stays until he has earned enough to join a caravan across the desert.",
        "安达卢西亚的牧羊少年圣地亚哥卖掉羊群，渡过海峡，去找梦里见到的、埋在埃及金字塔旁的宝藏。到丹吉尔的第一天，一个自称能带路的人拿走了他所有的钱。他在城里给一位水晶商人干活，攒够了钱才跟着商队走进沙漠。",
        ["Tangier"], ["丹吉尔"], "https://en.wikipedia.org/wiki/The_Alchemist_(novel)"),
    b.S("ma-nl-1", "naked-lunch", "ma-tangier", "Interzone", "“交界区”",
        "Burroughs moved to Tangier in 1954, when it was still an International Zone, and began the manuscript there that May. The book has no continuous plot; many of its episodes follow William Lee, an addict, to Interzone, an invented city with a drug market and four warring parties, modelled on the Tangier of those years. In early 1957 Allen Ginsberg and Jack Kerouac came to Tangier and helped him type and assemble the pages; Olympia Press published it in Paris in 1959.",
        "巴勒斯 1954 年搬到丹吉尔，那时这里还是国际共管区，同年 5 月他开始写这部手稿。书没有连贯的情节；许多片段跟着瘾君子威廉·李来到“交界区”——一座虚构的城市，有毒品黑市和四个互相争斗的党派，原型就是那几年的丹吉尔。1957 年初，艾伦·金斯堡和杰克·凯鲁亚克来到丹吉尔，帮他打字、整理书稿；1959 年奥林匹亚出版社在巴黎出版。",
        ["Tangier"], ["丹吉尔"], "https://en.wikipedia.org/wiki/Naked_Lunch"),
]

def ids_in(path): return set(re.findall(r'\{ id: "([^"]+)"', open(path, encoding="utf-8").read()))
import glob
all_books = set()
for f in glob.glob(os.path.join(APP, "data", "*", "books.js")): all_books |= ids_in(f)
assert not {x["id"] for x in books} & all_books, {x["id"] for x in books} & all_books
old_places = ids_in(b.data("places.js"))
assert not {p["id"] for p in places} & old_places and {p["id"] for p in places} == set(CO)
assert not {l["id"] for l in lines} & ids_in(b.data("lines.js"))
for l in lines:
    assert l["book_id"] in {x["id"] for x in books} and l["place_ids"][0] in ({p["id"] for p in places} | old_places), l["id"]
assert {l["book_id"] for l in lines} == {x["id"] for x in books}

if __name__ == "__main__":
    M = "11-24: second pack, five books added under selection rule v2 (tools/content/batches/add_ma2.py)"
    b.append(b.data("books.js"), books, M)
    b.append(b.data("places.js"), places, M)
    b.append(b.data("lines.js"), lines, M)
    src = os.path.join(APP, "_to_delete", "photos_del_v2_1124", "ma-fez.jpg"); dst = os.path.join(APP, "images", "places", "ma-fez.jpg")
    if not os.path.exists(dst): shutil.copyfile(src, dst)
    cred = os.path.join(APP, "docs", "photo-credits.md"); t = open(cred, encoding="utf-8").read()
    if FEZ_CREDIT not in t:
        open(cred + ".new", "w", encoding="utf-8").write(t.rstrip("\n") + "\n" + FEZ_CREDIT + "\n"); os.replace(cred + ".new", cred)
    print(len(books), "books,", len(places), "places,", len(lines), "lines")
