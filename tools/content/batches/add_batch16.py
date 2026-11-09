"""11-05: coverage check, category 4 — The Lord of the Rings (BBC Big Read no. 1). Still in copyright: a scene note in our
own words only. Places: Moseley Bog (the woods Tolkien acknowledged behind his ancient forests) and 20 Northmoor Road,
Oxford, where he wrote The Hobbit and almost all of The Lord of the Rings; the Wolvercote grave now links the new book too.
Facts from Wikipedia and the Historic England listing (via British Listed Buildings); photos from Commons.
Usage: python3 -I add_batch16.py <app_dir> <pg_texts_dir> <photo_work_dir>"""
import importlib.util, json, re, sys
from PIL import Image
APP, TX, PW = sys.argv[1], sys.argv[2], sys.argv[3]
spec = importlib.util.spec_from_file_location("b5", __file__.replace("add_batch16.py", "add_batch5.py"))
b5 = importlib.util.module_from_spec(spec)
_argv, sys.argv = sys.argv, [sys.argv[0], APP, TX]
spec.loader.exec_module(b5)
sys.argv = _argv
b5.D = ", 2026-11-05"
append, PROTO, PIL, W = b5.append, b5.PROTO, b5.PIL, b5.W

books = [dict(id="lord-of-the-rings", title="The Lord of the Rings", title_zh="魔戒", author="J. R. R. Tolkien", author_zh="托尔金", year="1954–1955",
              orig_lang="en", public_domain=False, source_url=None,
              aliases=["指环王", "The Fellowship of the Ring", "The Two Towers", "The Return of the King"])]
places = [
    PROTO("moseley-bog", "Moseley Bog, Birmingham", "伯明翰 · 莫斯利沼泽", 52.4360, -1.8630, "Moseley Bog (Wikipedia)", W + "Moseley_Bog",
          "Tolkien lived nearby as a boy and later called the countryside here 'a kind of lost paradise'. He acknowledged these old woods as an inspiration for the ancient forests of The Hobbit and The Lord of the Rings. Now a nature reserve run by the Wildlife Trust for Birmingham and the Black Country",
          "托尔金小时候就住在附近，后来说这一带是“一种失落的乐园”。他承认，《霍比特人》和《魔戒》里那些古老的森林，灵感来自这片老树林。现在是自然保护区，由伯明翰与黑乡野生动物信托管理"),
    PIL("northmoor-road-20", "20 Northmoor Road, Oxford", "牛津 · 北沼路 20 号", 51.7711, -1.2602,
        "20 Northmoor Road (British Listed Buildings, Grade II)", "https://britishlistedbuildings.co.uk/101391361-20-northmoor-road-oxford",
        "Tolkien's home from 1930 to 1947. The listing says he wrote the whole of The Hobbit and almost all of The Lord of the Rings in this house. It is a private house, listed Grade II since 2004, with a blue plaque",
        "托尔金 1930 至 1947 年的家。文物登录说明里写着，他在这座房子里写了《霍比特人》的全部和《魔戒》的几乎全部。现在是私宅，2004 年列为二级保护建筑，墙上有蓝色纪念牌",
        ["the-hobbit", "lord-of-the-rings"]),
]
lines = [dict(id="lotr-s1", kind="scene", book_id="lord-of-the-rings", place_ids=["moseley-bog"],
              location="Book 1, Chapter 6, The Old Forest", location_zh="第一卷第 6 章《老林子》",
              text_en="To shake off the Black Riders, Frodo and his friends cut through the Old Forest. The trees seem to close in and herd them along, until Old Man Willow traps Merry and Pippin; Tom Bombadil comes singing along the river and sets them free.",
              text_zh="为了甩掉黑骑手，佛罗多和伙伴们抄近路穿过老林子。树木仿佛围拢过来，把他们往一个方向赶；柳树老头困住了梅里和皮平，汤姆·邦巴迪尔唱着歌沿河而来，把他们救了出来。",
              highlight_en=["Old Forest"], highlight_zh=["老林子"], status="draft")]

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

def link_grave():
    path = f"{APP}/data/places.js"
    s = open(path, encoding="utf-8").read()
    m = re.search(r'(\{ id: "tolkien-grave".*?book_ids: )(\[[^\]]*\])', s)
    ids = json.loads(m.group(2))
    if "lord-of-the-rings" not in ids:
        ids.append("lord-of-the-rings")
    s = s[:m.start(2)] + json.dumps(ids, ensure_ascii=False) + s[m.end(2):]
    open(path, "w", encoding="utf-8").write(s)

if __name__ == "__main__":
    append(f"{APP}/data/books.js", books, "11-05 覆盖面复核第四批：《魔戒》（有版权，只写场景说明）")
    append(f"{APP}/data/places.js", places, "11-05 覆盖面复核第四批：《魔戒》（坐标和照片均有出处）")
    append(f"{APP}/data/lines.js", lines, "11-05 覆盖面复核第四批：《魔戒》场景说明（草稿，待审核）")
    link_grave()
    rows = [f"| {p['name']} | {p['photo']['author']} | [{p['photo']['license']}]({p['photo']['license_url']}) | [Commons]({p['photo']['source']}) |" for p in places]
    cr = open(f"{APP}/docs/photo-credits.md", encoding="utf-8").read().rstrip("\n") + "\n" + "\n".join(rows) + "\n"
    open(f"{APP}/docs/photo-credits.md", "w", encoding="utf-8").write(cr)
    print("ok")
