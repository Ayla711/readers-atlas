"""11-04 evening: places the user asked for — Rowling's Edinburgh (the Elephant House, Greyfriars Kirkyard), Woolf's
Monk's House, Carroll's Christ Church and Alice's Shop — plus Through the Looking-Glass, whose Old Sheep Shop is
Alice's Shop. Coordinates from Geograph subject locations or Commons camera locations; photos from Commons
(resized here to 800 px wide, metadata stripped). The excerpt is cut out of Project Gutenberg #12.
Usage: python3 -I add_batch7.py <app_dir> <pg_texts_dir> <photo_work_dir>"""
import importlib.util
import json
import sys
from PIL import Image

APP, TX, PW = sys.argv[1], sys.argv[2], sys.argv[3]
spec = importlib.util.spec_from_file_location("b5", __file__.replace("add_batch7.py", "add_batch5.py"))
b5 = importlib.util.module_from_spec(spec)
_argv, sys.argv = sys.argv, [sys.argv[0], APP, TX]
spec.loader.exec_module(b5)
sys.argv = _argv
prose, append, B, PROTO, PIL, L = b5.prose, b5.append, b5.B, b5.PROTO, b5.PIL, b5.L
COM = "https://commons.wikimedia.org/wiki/"
GEO = "https://www.geograph.org.uk/photo/"

cands = json.load(open(f"{PW}/candidates.json"))
PHOTOS = {  # place -> (candidate index, alt_en, alt_zh)
    "elephant-house": (0, "The red shopfront of the Elephant House on George IV Bridge", "乔治四世桥上大象咖啡馆的红色店面"),
    "greyfriars-kirkyard": (2, "Monuments along the east wall of Greyfriars Kirkyard", "灰衣修士教堂墓园东墙边的墓碑"),
    "monks-house": (0, "Monk's House, the Woolfs' weatherboarded cottage in Rodmell", "罗德梅尔的僧舍，伍尔夫夫妇住过的护墙板小屋"),
    "carroll-christ-church": (1, "Tom Quad, the great quadrangle of Christ Church, with Tom Tower", "基督教堂学院的汤姆方庭和汤姆塔"),
    "alices-shop": (5, "Alice's Shop, the small shop with the red door, on St Aldate's", "圣奥尔代茨街上红门的那家小店就是爱丽丝小店"),
}
def photo(pid):
    n, en, zh = PHOTOS[pid]
    c = cands[pid]["candidates"][n]
    im = Image.open(f"{PW}/dl/{pid}__{n}.jpg").convert("RGB")
    if im.width > 800:
        im = im.resize((800, round(im.height * 800 / im.width)), Image.LANCZOS)
    rel = f"images/places/{pid}.jpg"
    im.save(f"{APP}/{rel}", "JPEG", quality=82, optimize=True, progressive=True)  # no EXIF carried over
    return {"file": rel, "width": im.width, "height": im.height, "author": c["author"].strip(), "license": c["license"].strip(),
            "license_url": c["license_url"].strip(), "source": c["page"], "alt_en": en, "alt_zh": zh}

books = [B("through-the-looking-glass", "Through the Looking-Glass", "爱丽丝镜中奇遇", "Lewis Carroll", "刘易斯·卡罗尔", "1871", 12)]

places = [
    PIL("elephant-house", "The Elephant House, George IV Bridge", "乔治四世桥 · 大象咖啡馆", 55.9474, -3.1918,
        "The Elephant House, 21 George IV Bridge (The Scotsman); the café is across the street from where the Commons photo 'The Elephant House october 2023' was taken (camera 55.94739, -3.19159)",
        COM + "File:The_Elephant_House_october_2023.jpg",
        "A café at 21 George IV Bridge where J. K. Rowling wrote in the back room, looking out to the castle, while working on the early Harry Potter books. She has said she had been writing the series for years before she first came here, so it is not its birthplace, though 'I did write in there'. Closed after a fire in 2021, it reopened in 2026",
        "乔治四世桥 21 号的咖啡馆。罗琳写早期几本《哈利·波特》时常坐在后屋写作，窗外就是爱丁堡城堡。她说过，自己开始写这套书比第一次来这里早好几年，所以这里算不上“诞生地”，但她确实在这里写过。2021 年因火灾停业，2026 年重新开张",
        ["harry-potter-1"]),
    PIL("greyfriars-kirkyard", "Greyfriars Kirkyard", "灰衣修士教堂墓园", 55.9467, -3.1922,
        "Greyfriars Kirkyard (Commons photo 'Greyfriars Kirkyard Memorials', camera location inside the kirkyard 55.9467, -3.19222)",
        COM + "File:Greyfriars_Kirkyard_Memorials.jpg",
        "The Old Town graveyard, in use since the late 16th century, where Rowling often walked while writing. Its graves include Thomas Riddell (died 1806) and the poet William McGonagall, often taken as the sources of the names Tom Riddle and Professor McGonagall; Rowling has said she may have picked up the name Riddle without realising",
        "老城的墓园，16 世纪末开始使用，罗琳写作期间常来这里散步。墓园里葬着 1806 年去世的托马斯·里德尔和诗人威廉·麦戈纳格尔，常被认为是汤姆·里德尔和麦格教授这两个名字的来源；罗琳说过，里德尔这个名字可能是她无意中记下的",
        ["harry-potter-1", "harry-potter-2"]),
    PIL("monks-house", "Monk's House, Rodmell", "罗德梅尔 · 僧舍（伍尔夫故居）", 50.8386, 0.0166,
        "Monk's House, Rodmell (Geograph photo 3940379, subject location; Wikipedia gives 50.8387, 0.0165)", GEO + "3940379",
        "The cottage Virginia and Leonard Woolf bought in 1919 and lived in full-time from 1940; many of her novels took shape in the writing lodge at the end of the garden. The National Trust has run it as a writer's house museum since 1980",
        "伍尔夫和丈夫伦纳德 1919 年买下的乡间小屋，1940 年起长住；她的许多小说是在花园尽头的写作小屋里成形的。1980 年起由国民信托作为作家故居开放参观",
        ["mrs-dalloway"]),
    PIL("carroll-christ-church", "Christ Church, Lewis Carroll's college", "牛津 · 卡罗尔任教的基督教堂学院", 51.7499, -1.2560,
        "Mercury fountain at the centre of Tom Quad (Geograph photo 187947, subject location)", GEO + "187947",
        "Carroll came up to Christ Church in 1851 and stayed on as a Student of the college, teaching mathematics from 1855 to 1881; Alice Liddell was a daughter of the Dean, Henry Liddell. The marker is in Tom Quad, the great quadrangle",
        "卡罗尔 1851 年进入基督教堂学院读书，之后留在学院，1855 至 1881 年担任数学讲师；爱丽丝·利德尔是院长亨利·利德尔的女儿。标记放在学院的大方庭汤姆方庭",
        ["alice-in-wonderland", "through-the-looking-glass"]),
    PROTO("alices-shop", "Alice's Shop, St Aldate's", "圣奥尔代茨街 · 爱丽丝小店", 51.7489, -1.2567,
          "Alice's Shop, 83 St Aldate's (Geograph photo 8084523, subject location SP 51410 05841)", GEO + "8084523",
          "The model for the Old Sheep Shop in chapter 5 of Through the Looking-Glass; Tenniel's illustration shows this shop. Alice Liddell, the Dean's daughter from Christ Church across the road, used to buy sweets here; it now sells Alice gifts",
          "《爱丽丝镜中奇遇》第 5 章老羊开的那家小店的原型，坦尼尔的插图画的就是这家店。对面基督教堂学院院长的女儿爱丽丝·利德尔当年常来这里买糖；现在是一家卖爱丽丝纪念品的小店"),
]
for p in places:
    p["photo"] = photo(p["id"])

lines = [
    L("ttlg-1", "through-the-looking-glass", "alices-shop", "Chapter 5, Wool and Water", "第 5 章《羊毛和水》",
      prose(12, "She looked at the Queen, who seemed to have suddenly wrapped herself up", "a great pair of spectacles."), ["little dark shop"], 12),
]

if __name__ == "__main__":
    append(f"{APP}/data/books.js", books, "11-04 晚 用户补充：《爱丽丝镜中奇遇》（爱丽丝小店是书里老羊小店的原型）")
    append(f"{APP}/data/places.js", places, "11-04 晚 用户补充：罗琳的爱丁堡、伍尔夫故居、卡罗尔的牛津（坐标和照片均有出处）")
    append(f"{APP}/data/lines.js", lines, "11-04 晚 用户补充：《爱丽丝镜中奇遇》老羊小店")
    rows = []
    for p in places:
        ph = p["photo"]
        rows.append(f"| {p['name']} | {ph['author']} | [{ph['license']}]({ph['license_url']}) | [Commons]({ph['source']}) |")
    cr = open(f"{APP}/docs/photo-credits.md", encoding="utf-8").read().rstrip("\n") + "\n" + "\n".join(rows) + "\n"
    open(f"{APP}/docs/photo-credits.md", "w", encoding="utf-8").write(cr)
    print("\n".join(rows))
    print(lines[0]["text_en"])
