"""11-04 night: George Orwell. Nineteen Eighty-Four (1949) and Animal Farm (1945) are public domain in the UK since 2021
(Orwell died in 1950) but not yet in the US, so Project Gutenberg (US) does not carry them; the user decided to treat
them as public domain here. The excerpts could not be downloaded (Gutenberg Australia and Global Grey are blocked for
this connection), so each was read through the web reader in pieces under 125 characters from both copies and the
two compared. Coordinates from Geograph subject locations; photos from Commons.
Usage: python3 -I add_batch10.py <app_dir> <pg_texts_dir> <photo_work_dir>"""
import importlib.util, json, sys
from PIL import Image
APP, TX, PW = sys.argv[1], sys.argv[2], sys.argv[3]
spec = importlib.util.spec_from_file_location("b5", __file__.replace("add_batch10.py", "add_batch5.py"))
b5 = importlib.util.module_from_spec(spec)
_argv, sys.argv = sys.argv, [sys.argv[0], APP, TX]
spec.loader.exec_module(b5)
sys.argv = _argv
append, PROTO, PIL, D = b5.append, b5.PROTO, b5.PIL, b5.D
GEO = "https://www.geograph.org.uk/photo/"
W = "https://en.wikipedia.org/wiki/"
GAU = "https://gutenberg.net.au/ebooks01/"

cands = json.load(open(f"{PW}/candidates.json"))
PHOTOS = {
    "senate-house": (2, "Senate House, the University of London's Art Deco tower on Malet Street", "马利特街上伦敦大学参议院大楼的装饰艺术风格塔楼", None),
    "barnhill-jura": (0, "Barnhill, the farmhouse in the north of Jura", "朱拉岛北部的巴恩希尔农舍", None),
    "orwell-grave": (1, "The headstone of Eric Arthur Blair (George Orwell) in All Saints' churchyard, Sutton Courtenay", "萨顿考特尼诸圣堂墓园里埃里克·亚瑟·布莱尔（乔治·奥威尔）的墓碑", "https://creativecommons.org/publicdomain/mark/1.0/"),
    "wallington-orwell": (3, "Orwell's cottage, The Stores, at 2 Kits Lane, Wallington", "沃灵顿村基茨巷 2 号，奥威尔住过的“杂货铺”小屋", None),
}
def photo(pid):
    n, en, zh, lic_url = PHOTOS[pid]
    c = cands[pid]["candidates"][n]
    im = Image.open(f"{PW}/dl/{pid}__{n}.jpg").convert("RGB")
    if im.width > 800:
        im = im.resize((800, round(im.height * 800 / im.width)), Image.LANCZOS)
    assert im.width >= im.height, pid
    rel = f"images/places/{pid}.jpg"
    im.save(f"{APP}/{rel}", "JPEG", quality=82, optimize=True, progressive=True)
    return {"file": rel, "width": im.width, "height": im.height, "author": c["author"].strip(), "license": c["license"].strip(),
            "license_url": lic_url or c["license_url"].strip(), "source": c["page"], "alt_en": en, "alt_zh": zh}

def B(id, title, title_zh, year, url):
    return dict(id=id, title=title, title_zh=title_zh, author="George Orwell", author_zh="乔治·奥威尔", year=year, orig_lang="en",
                public_domain=True, source_url=url)
books = [B("nineteen-eighty-four", "Nineteen Eighty-Four", "一九八四", "1949", GAU + "0100021h.html"),
         B("animal-farm", "Animal Farm", "动物农场", "1945", GAU + "0100011h.html")]

places = [
    PROTO("senate-house", "Senate House, University of London", "伦敦大学 · 参议院大楼", 51.5210, -0.1288,
          "Senate House (Geograph photo 2855085, subject location)", GEO + "2855085",
          "Usually taken as the model for the Ministry of Truth: in the Second World War it housed the Ministry of Information, where Orwell's wife Eileen worked in the Censorship Department. The Art Deco tower was built in 1932–37",
          "常被认为是“真理部”的原型：二战期间这里是英国新闻部所在地，奥威尔的妻子艾琳就在新闻部的审查处工作。这座装饰艺术风格的大楼建于 1932 至 1937 年"),
    PIL("barnhill-jura", "Barnhill, Isle of Jura", "朱拉岛 · 巴恩希尔农舍", 56.1109, -5.6927,
        "Barnhill (Geograph photo 1451233, subject location)", GEO + "1451233",
        "The farmhouse in the north of Jura where Orwell lived on and off from 1946 to January 1949 and finished Nineteen Eighty-Four. It is still let to holidaymakers, much as he left it",
        "朱拉岛北部的农舍，奥威尔 1946 年至 1949 年 1 月断断续续住在这里，在这里写完了《一九八四》。现在仍作度假屋出租，屋子基本保持他住时的样子",
        ["nineteen-eighty-four"]),
    PIL("orwell-grave", "George Orwell's grave, Sutton Courtenay", "萨顿考特尼 · 奥威尔墓", 51.6439, -1.2710,
        "Graves of Astor and Orwell, All Saints, Sutton Courtenay (Geograph photo 362296, subject location)", GEO + "362296",
        "Orwell lies in All Saints' churchyard under his real name, Eric Arthur Blair. He wanted to be buried in an English country churchyard, and David Astor, whose family owned the manor, arranged a place here",
        "奥威尔以本名埃里克·亚瑟·布莱尔葬在诸圣堂的墓园。他希望葬在英格兰乡间的教堂墓地，大卫·阿斯特的家族是这里的庄园主，由他安排了这块墓地",
        ["nineteen-eighty-four", "animal-farm"]),
    PROTO("wallington-orwell", "Wallington, Hertfordshire", "赫特福德郡 · 沃灵顿村", 51.9880, -0.1193,
          "George Orwell's plaque, Wallington (Geograph photo 6849927, subject location)", GEO + "6849927",
          "Orwell lived at The Stores, 2 Kits Lane, from 1936 to 1940, keeping a small shop and goats, and married Eileen in the parish church; the village's Manor Farm and Great Barn are taken as the models for the farm in Animal Farm",
          "奥威尔 1936 至 1940 年住在村里基茨巷 2 号的“杂货铺”，开小店、养山羊，也在村里的教堂和艾琳结婚。村里的庄园农场和大谷仓被认为是《动物农场》里那座农场的原型"),
]
for p in places:
    p["photo"] = photo(p["id"])

CHK = "Project Gutenberg Australia and Global Grey online texts, read through the web reader in short pieces and compared" + D
def L(id, book, place, loc, loc_zh, text, hl):
    for h in hl:
        assert h in text, (id, h)
    return dict(id=id, book_id=book, place_ids=[place], location=loc, location_zh=loc_zh, text_en=text, highlight_en=hl,
                translation="original", status="draft", checked=CHK)
lines = [
    L("nef-1", "nineteen-eighty-four", "london", "Part One, Chapter 1", "第一部第 1 章",
      "This, he thought with a sort of vague distaste—this was London, chief city of Airstrip One, itself the third most populous of the provinces of Oceania.",
      ["London"]),
    L("nef-2", "nineteen-eighty-four", "senate-house", "Part One, Chapter 1", "第一部第 1 章",
      "The Ministry of Truth—Minitrue, in Newspeak—was startlingly different from any other object in sight. It was an enormous pyramidal structure of glittering white concrete, soaring up, terrace after terrace, 300 metres into the air.",
      ["Ministry of Truth"]),
    L("af-1", "animal-farm", "wallington-orwell", "Chapter 1", "第 1 章",
      "Mr. Jones, of the Manor Farm, had locked the hen-houses for the night, but was too drunk to remember to shut the pop-holes.",
      ["Manor Farm"]),
]
if __name__ == "__main__":
    append(f"{APP}/data/books.js", books, "11-04 夜 奥威尔：英国 2021 年起公有领域（作者 1950 年去世），美国仍有版权；按用户决定作公有领域处理")
    append(f"{APP}/data/places.js", places, "11-04 夜 奥威尔（坐标和照片均有出处）")
    append(f"{APP}/data/lines.js", lines, "11-04 夜 奥威尔：原文无法下载，经网页阅读工具从两个在线版本分段读取并比对（草稿，待审核）")
    rows = [f"| {p['name']} | {p['photo']['author']} | [{p['photo']['license']}]({p['photo']['license_url']}) | [Commons]({p['photo']['source']}) |" for p in places]
    cr = open(f"{APP}/docs/photo-credits.md", encoding="utf-8").read().rstrip("\n") + "\n" + "\n".join(rows) + "\n"
    open(f"{APP}/docs/photo-credits.md", "w", encoding="utf-8").write(cr)
    print("\n".join(rows))
