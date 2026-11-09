"""11-05: two BBC Big Read titles the user picked — A Tale of Two Cities (#63) and Black Beauty (#58). Both public domain:
excerpts cut out of the downloaded Project Gutenberg files (#98, #271) and hung on places already on the map (Dover, Soho,
London Bridge). New place: Anna Sewell's birthplace in Great Yarmouth. Dickens's two museums now link the new book.
Usage: python3 -I add_batch17.py <app_dir> <pg_texts_dir> <photo_work_dir>"""
import importlib.util, json, re, sys
from PIL import Image
APP, TX, PW = sys.argv[1], sys.argv[2], sys.argv[3]
spec = importlib.util.spec_from_file_location("b5", __file__.replace("add_batch17.py", "add_batch5.py"))
b5 = importlib.util.module_from_spec(spec)
_argv, sys.argv = sys.argv, [sys.argv[0], APP, TX]
spec.loader.exec_module(b5)
sys.argv = _argv
b5.D = ", 2026-11-05"
append, prose, B, PIL, L, W = b5.append, b5.prose, b5.B, b5.PIL, b5.L, b5.W
COM = "https://commons.wikimedia.org/wiki/"

books = [
    B("tale-of-two-cities", "A Tale of Two Cities", "双城记", "Charles Dickens", "狄更斯", "1859", 98),
    B("black-beauty", "Black Beauty", "黑骏马", "Anna Sewell", "安娜·休厄尔", "1877", 271),
]
cands = json.load(open(f"{PW}/candidates.json"))
c0 = cands["anna-sewell-house"]["candidates"][0]
places = [
    PIL("anna-sewell-house", "Anna Sewell's House, Great Yarmouth", "大雅茅斯 · 安娜·休厄尔故居", 52.6105, 1.7271,
        "Anna Sewell's House, Church Plain, Great Yarmouth (Commons photo by Colin Smith, object location)", c0["page"],
        "Anna Sewell was born at 26 Church Plain on 30 March 1820. She wrote Black Beauty much later, between 1871 and 1877, at her home in Old Catton near Norwich, and died in 1878, a few months after it came out. The Redwings Horse Sanctuary leases the house and opened it to visitors in 2022",
        "安娜·休厄尔 1820 年 3 月 30 日生在教堂广场 26 号。《黑骏马》是她多年以后在诺里奇附近老卡顿的家里写的，从 1871 年写到 1877 年；书出版几个月后，她于 1878 年去世。现在这座房子由红翼马匹救助站租用，2022 年起对外开放",
        ["black-beauty"]),
]
n, en, zh = 0, "Anna Sewell's House on Church Plain, Great Yarmouth", "大雅茅斯教堂广场上的安娜·休厄尔故居"
im = Image.open(f"{PW}/dl/anna-sewell-house__{n}.jpg").convert("RGB")
if im.width > 800:
    im = im.resize((800, round(im.height * 800 / im.width)), Image.LANCZOS)
rel = "images/places/anna-sewell-house.jpg"
im.save(f"{APP}/{rel}", "JPEG", quality=82, optimize=True, progressive=True)
places[0]["photo"] = {"file": rel, "width": im.width, "height": im.height, "author": c0["author"].strip(), "license": c0["license"].strip(),
                      "license_url": c0["license_url"].strip(), "source": c0["page"], "alt_en": en, "alt_zh": zh}

lines = [
    L("ttc-1", "tale-of-two-cities", "dover", "Book 1, Chapter 4, The Preparation", "第一卷第 4 章《准备》",
      prose(98, "When the mail got successfully to Dover", "an adventurous traveller upon."), ["Dover"], 98),
    L("ttc-2", "tale-of-two-cities", "soho", "Book 2, Chapter 6, Hundreds of People", "第二卷第 6 章《成百上千的人》",
      prose(98, "The quiet lodgings of Doctor Manette", "on his way to dine with the Doctor."), ["Soho-square"], 98),
    L("bb-1", "black-beauty", "london-bridge", "Chapter 35, Jerry Barker", "第 35 章《杰里·巴克》",
      prose(271, "In and out, in and out we went", "eight minutes to twelve o'clock."), ["London Bridge"], 271),
]

def link_dickens():
    path = f"{APP}/data/places.js"
    s = open(path, encoding="utf-8").read()
    for pid in ["dickens-museum", "dickens-birthplace"]:
        m = re.search(r'(\{ id: "' + pid + r'".*?book_ids: )(\[[^\]]*\])', s)
        ids = json.loads(m.group(2))
        if "tale-of-two-cities" not in ids:
            ids.append("tale-of-two-cities")
        s = s[:m.start(2)] + json.dumps(ids, ensure_ascii=False) + s[m.end(2):]
    open(path, "w", encoding="utf-8").write(s)

if __name__ == "__main__":
    append(f"{APP}/data/books.js", books, "11-05 Big Read：《双城记》《黑骏马》（古登堡原文）")
    append(f"{APP}/data/places.js", places, "11-05 Big Read：安娜·休厄尔故居（坐标和照片均有出处）")
    append(f"{APP}/data/lines.js", lines, "11-05 Big Read：《双城记》《黑骏马》古登堡原文摘句（草稿，待审核）")
    link_dickens()
    p = places[0]
    row = f"| {p['name']} | {p['photo']['author']} | [{p['photo']['license']}]({p['photo']['license_url']}) | [Commons]({p['photo']['source']}) |"
    cr = open(f"{APP}/docs/photo-credits.md", encoding="utf-8").read().rstrip("\n") + "\n" + row + "\n"
    open(f"{APP}/docs/photo-credits.md", "w", encoding="utf-8").write(cr)
    for l in lines:
        print(l["id"], "|", l["text_en"])
