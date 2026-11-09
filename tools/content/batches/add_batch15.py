"""11-05: coverage check, category 3 — nine writers' houses missing for writers already in the database (Dickens, Hardy,
Johnson, Kipling, Wordsworth, Burns, Barrie, Dylan Thomas, C. S. Lewis). Each links every book of its writer.
Facts from Wikipedia, British Listed Buildings, Undiscovered Scotland, the Dylan Thomas Birthplace site and the Irish News;
coordinates from those pages or the photo's Geograph / Commons location; photos from Commons.
Usage: python3 -I add_batch15.py <app_dir> <pg_texts_dir> <photo_work_dir>"""
import importlib.util, json, sys
from PIL import Image
APP, TX, PW = sys.argv[1], sys.argv[2], sys.argv[3]
spec = importlib.util.spec_from_file_location("b5", __file__.replace("add_batch15.py", "add_batch5.py"))
b5 = importlib.util.module_from_spec(spec)
_argv, sys.argv = sys.argv, [sys.argv[0], APP, TX]
spec.loader.exec_module(b5)
sys.argv = _argv
b5.D = ", 2026-11-05"
append, PIL, W = b5.append, b5.PIL, b5.W

DICKENS = ["bleak-house", "pickwick-papers", "david-copperfield", "hard-times", "great-expectations", "oliver-twist", "christmas-carol"]
places = [
    PIL("dickens-birthplace", "Charles Dickens Birthplace Museum, Portsmouth", "朴茨茅斯 · 狄更斯出生地博物馆", 50.8070, -1.0872,
        "Charles Dickens Birthplace Museum (Wikipedia)", W + "Charles_Dickens_Birthplace_Museum",
        "Dickens was born in this house in Landport, Portsmouth, in 1812. The city has owned it since 1904; the rooms were restored in the 1960s, and it is run by Portsmouth Museums",
        "狄更斯 1812 年生在朴茨茅斯兰德港的这座房子里。1904 年起归市政府所有，1960 年代按当年的样子修复了室内，现由朴茨茅斯博物馆管理",
        DICKENS),
    PIL("max-gate", "Max Gate, Dorchester", "多切斯特 · 马克斯门", 50.7081, -2.4200, "Max Gate (Wikipedia)", W + "Max_Gate",
        "Hardy designed the house himself and his father and brother built it. He lived here from 1885 until his death in 1928 and wrote Tess of the d'Urbervilles, Jude the Obscure, The Mayor of Casterbridge and much of his poetry here. His sister Kate left it to the National Trust in 1940",
        "哈代自己设计了这座房子，由他的父亲和弟弟施工。他 1885 年住进来，直到 1928 年去世，在这里写了《德伯家的苔丝》《无名的裘德》《卡斯特桥市长》和大量的诗。1940 年他的妹妹凯特把房子留给了国民信托",
        ["tess", "return-of-the-native", "far-from-the-madding-crowd"]),
    PIL("johnson-birthplace", "Samuel Johnson Birthplace Museum, Lichfield", "利奇菲尔德 · 约翰逊出生地博物馆", 52.6835, -1.8279,
        "Samuel Johnson Birthplace Museum (Wikipedia)", W + "Samuel_Johnson_Birthplace_Museum",
        "Johnson's father Michael, a bookseller, built the house in 1707 as his shop and home, and Johnson was born here on 18 September 1709. It stands on the corner of Market Street and Breadmarket Street, across from the market square, and has been a museum since 1901",
        "约翰逊的父亲迈克尔是书商，1707 年盖了这座房子，楼下开书店、楼上住家；约翰逊 1709 年 9 月 18 日生在这里。房子在市场街和面包市场街的拐角，对着集市广场，1901 年起是博物馆",
        ["journey-western-islands", "life-of-johnson"]),
    PIL("batemans", "Bateman's, Burwash", "伯沃什 · 贝特曼庄园", 50.9893, 0.3793, "Bateman's (Wikipedia)", W + "Bateman%27s",
        "The Kiplings bought Bateman's in 1902 and he lived here until his death in 1936. Puck of Pook's Hill is named after the hill you can see from the house, and If— was written here too. Under his widow Caroline's will it passed to the National Trust in 1939",
        "吉卜林夫妇 1902 年买下贝特曼庄园，他在这里一直住到 1936 年去世。《普克山的帕克》就是以从屋里望得见的那座小山命名的，《如果》也是在这里写的。1939 年按他遗孀卡罗琳的遗嘱归国民信托",
        ["puck-of-pooks-hill"]),
    PIL("rydal-mount", "Rydal Mount", "赖德尔山庄", 0, 0, "", "",
        "Wordsworth's home from 1813 until his death in 1850. His great-great-granddaughter Mary Henderson bought it in 1969 and opened it to the public in 1970; the Wordsworth Trust bought it in 2026",
        "华兹华斯 1813 年搬来，在这里一直住到 1850 年去世。他的玄孙女玛丽·亨德森 1969 年买下这里，1970 年对外开放；2026 年华兹华斯基金会买下了它",
        ["wordsworth-poems"]),
    PIL("burns-house-dumfries", "Robert Burns House, Dumfries", "邓弗里斯 · 彭斯故居", 55.0661, -3.6080,
        "24 Burns Street, Robert Burns House (British Listed Buildings, Category A)", "https://britishlistedbuildings.co.uk/200362606-24-burns-street-robert-burns-house-dumfries",
        "Burns lived in this house, now 24 Burns Street, from 1793 until his death in 1796. It is now a museum",
        "彭斯 1793 年搬进这座房子（今伯恩斯街 24 号），一直住到 1796 年去世。现在是博物馆",
        ["burns-highlands"]),
    PIL("barrie-birthplace", "J. M. Barrie's Birthplace, Kirriemuir", "基里缪尔 · 巴里出生地", 0, 0, "", "",
        "Barrie was born at 9 Brechin Road on 9 May 1860, the ninth of ten children in a weaver's family. At seven he put on his first play in the wash-house behind it, which is said to have given him the Wendy House in Peter Pan. Cared for by the National Trust for Scotland",
        "巴里 1860 年 5 月 9 日生在布里金路 9 号，是织布工家里十个孩子中的第九个。七岁时，他在屋后的洗衣房里排演了自己的第一出戏，据说《彼得·潘》里的温迪小屋就是从这里来的。现由苏格兰国民信托管理",
        ["peter-pan-kensington"]),
    PIL("dylan-thomas-birthplace", "Dylan Thomas Birthplace, 5 Cwmdonkin Drive, Swansea", "斯旺西 · 迪伦·托马斯出生地", 0, 0, "", "",
        "Dylan Thomas was born in the front bedroom of this house in the Uplands in 1914 and lived here until his parents moved out in 1937. It has been restored to how it was in 1914 and opens to visitors",
        "迪伦·托马斯 1914 年生在斯旺西高地区这座房子的前卧室，一直住到 1937 年父母搬走。房子已按 1914 年的样子修复，对外开放",
        ["under-milk-wood"]),
    PIL("cs-lewis-square", "C. S. Lewis Square, Belfast", "贝尔法斯特 · C. S. 刘易斯广场", 0, 0, "", "",
        "A square in east Belfast, where Lewis grew up, at the meeting of the Connswater and Comber Greenways. It opened on 22 November 2016, the 53rd anniversary of his death, with seven sculptures by Maurice Harron of characters from The Lion, the Witch and the Wardrobe",
        "贝尔法斯特东区的一个广场，在康斯沃特绿道和科默绿道交会处；刘易斯就在东区长大。广场 2016 年 11 月 22 日落成，正是他去世 53 周年，广场上有莫里斯·哈伦雕的七座《狮子、女巫和魔衣橱》人物雕像",
        ["lion-witch-wardrobe"]),
]

COORDS = json.load(open(f"{PW}/coords.json", encoding="utf-8"))
for p in places:
    if p["id"] in COORDS:
        la, lo, st, su = COORDS[p["id"]]
        p["lat"], p["lon"], p["coord_checked"] = la, lo, f"{st} — {su}{b5.D}"
    assert p["lat"] and p["coord_checked"].split(" — ")[1].startswith("http"), p["id"]

PHOTOS = json.load(open(f"{PW}/choice.json", encoding="utf-8"))
cands = json.load(open(f"{PW}/candidates.json"))
for p in places:
    n, en, zh, crop = PHOTOS[p["id"]]
    c = cands[p["id"]]["candidates"][n]
    im = Image.open(f"{PW}/dl/{p['id']}__{n}.jpg").convert("RGB")
    if crop:
        x0, y0, x1, y1 = crop
        im = im.crop((round(x0 * im.width), round(y0 * im.height), round(x1 * im.width), round(y1 * im.height)))
    if im.width > 800:
        im = im.resize((800, round(im.height * 800 / im.width)), Image.LANCZOS)
    assert im.width >= im.height, p["id"]
    rel = f"images/places/{p['id']}.jpg"
    im.save(f"{APP}/{rel}", "JPEG", quality=82, optimize=True, progressive=True)
    p["photo"] = {"file": rel, "width": im.width, "height": im.height, "author": c["author"].strip() or "Unknown author", "license": c["license"].strip(),
                  "license_url": c["license_url"].strip(), "source": c["page"], "alt_en": en, "alt_zh": zh}
    if crop:
        p["photo"]["cropped"] = True

if __name__ == "__main__":
    append(f"{APP}/data/places.js", places, "11-05 覆盖面复核第三批：已有作家缺的 9 处故居（坐标和照片均有出处）")
    rows = [f"| {p['name']} | {p['photo']['author']} | [{p['photo']['license']}]({p['photo']['license_url']}) | [Commons]({p['photo']['source']}) |" for p in places]
    cr = open(f"{APP}/docs/photo-credits.md", encoding="utf-8").read().rstrip("\n") + "\n" + "\n".join(rows) + "\n"
    open(f"{APP}/docs/photo-credits.md", "w", encoding="utf-8").write(cr)
    print(len(places), "places")
