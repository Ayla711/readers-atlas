"""11-04 night: Virginia Woolf's other homes, as the user asked — Talland House (St Ives), 46 Gordon Square
(Bloomsbury), Hogarth House (Richmond) — plus To the Lighthouse, so that Talland House has its book. The Woolf and
Carroll pilgrimage places are linked to both of the author's books now in the list; Monk's House gains where her
ashes lie. Coordinates from Commons camera locations; photos from Commons (one cropped to landscape, marked as such).
Usage: python3 -I add_batch8.py <app_dir> <pg_texts_dir> <photo_work_dir>"""
import importlib.util
import json
import re
import sys
from PIL import Image

APP, TX, PW = sys.argv[1], sys.argv[2], sys.argv[3]
spec = importlib.util.spec_from_file_location("b5", __file__.replace("add_batch8.py", "add_batch5.py"))
b5 = importlib.util.module_from_spec(spec)
_argv, sys.argv = sys.argv, [sys.argv[0], APP, TX]
spec.loader.exec_module(b5)
sys.argv = _argv
append, PIL, D = b5.append, b5.PIL, b5.D
COM = "https://commons.wikimedia.org/wiki/"
WOOLF = ["mrs-dalloway", "to-the-lighthouse"]

cands = json.load(open(f"{PW}/candidates.json"))
PHOTOS = {  # place -> (candidate index, alt_en, alt_zh, crop box or None, author override)
    "talland-house": (1, "Talland House around 1882, when the Stephens first rented it", "1882 年前后的塔兰德宅，斯蒂芬一家刚租下它的时候", None, "Unknown photographer"),
    "gordon-square-46": (6, "The front of 46 Gordon Square, with the door and a blue plaque", "戈登广场 46 号的正门和门边的蓝牌", (0, 645, 960, 1365), None),
    "hogarth-house": (1, "The blue plaque on Hogarth House: Leonard and Virginia Woolf lived here 1915–1924 and founded the Hogarth Press 1917", "霍加斯宅门口的蓝牌：伍尔夫夫妇 1915—1924 年住在这里，1917 年创办霍加斯出版社", None, None),
}
def photo(pid):
    n, en, zh, crop, author = PHOTOS[pid]
    c = cands[pid]["candidates"][n]
    im = Image.open(f"{PW}/dl/{pid}__{n}.jpg").convert("RGB")
    if crop:
        im = im.crop(crop)
    if im.width > 800:
        im = im.resize((800, round(im.height * 800 / im.width)), Image.LANCZOS)
    assert im.width >= im.height, pid
    rel = f"images/places/{pid}.jpg"
    im.save(f"{APP}/{rel}", "JPEG", quality=82, optimize=True, progressive=True)  # no EXIF carried over
    ph = {"file": rel, "width": im.width, "height": im.height, "author": author or c["author"].strip(), "license": c["license"].strip(),
          "license_url": c["license_url"].strip(), "source": c["page"], "alt_en": en, "alt_zh": zh}
    if crop:
        ph["cropped"] = True
    return ph

books = [dict(id="to-the-lighthouse", title="To the Lighthouse", title_zh="到灯塔去", author="Virginia Woolf", author_zh="伍尔夫", year="1927",
              orig_lang="en", public_domain=True, source_url="https://standardebooks.org/ebooks/virginia-woolf/to-the-lighthouse")]

places = [
    PIL("talland-house", "Talland House, St Ives", "圣艾夫斯 · 塔兰德宅", 50.2084, -5.4792,
        "Talland House (Commons photo 'Talland House, St Ives, Cornwall - May 2022', camera location 50.20842, -5.47912)",
        COM + "File:Talland_House,_St_Ives,_Cornwall_-_May_2022.jpg",
        "The house above Porthminster Bay that Leslie Stephen rented for the family's summers, with Godrevy Lighthouse across the bay. Virginia spent three months here every summer for the first 13 years of her life; the family did not come back after 1894. Those summers lie behind To the Lighthouse",
        "莱斯利·斯蒂芬租下的海边别墅，俯瞰波斯明斯特湾，对岸就是戈德雷维灯塔。伍尔夫出生后的头 13 年，全家每年夏天都在这里住三个月；1894 年以后再没回来。这些夏天后来写进了《到灯塔去》",
        ["to-the-lighthouse"]),
    PIL("gordon-square-46", "46 Gordon Square, Bloomsbury", "布卢姆斯伯里 · 戈登广场 46 号", 51.5244, -0.1300,
        "46 Gordon Square (Commons photo '46 Gordon Square Bloomsbury Camden London, WC1H 0PD', taken in front of the house, camera location 51.52442, -0.13018)",
        COM + "File:46_Gordon_Square_Bloomsbury_Camden_London,_WC1H_0PD.jpg",
        "After their father's death in 1904 the Stephen siblings left Kensington for this house; the Thursday Evenings that Virginia and Vanessa held here for Thoby's Cambridge friends made it the first centre of the Bloomsbury Group. Virginia moved to Fitzroy Square after Vanessa married; Keynes later lived here",
        "1904 年父亲去世后，斯蒂芬家的兄妹从肯辛顿搬进这栋房子。弗吉尼亚和姐姐瓦妮莎在这里办“周四晚会”，招待哥哥索比的剑桥朋友，这里成了布卢姆斯伯里文化圈最早的聚会地。瓦妮莎结婚后，弗吉尼亚搬去了菲茨罗伊广场；后来凯恩斯住在这里",
        WOOLF),
    PIL("hogarth-house", "Hogarth House, Richmond", "里士满 · 霍加斯宅", 51.4604, -0.3008,
        "Hogarth House, 34 Paradise Road (English Heritage blue plaques); position from the Commons photo 'LEONARD and VIRGINIA WOOLF - Hogarth House 34 Paradise Road Richmond TW9 1SE', camera location 51.460448, -0.300786",
        COM + "File:LEONARD_and_VIRGINIA_WOOLF_-_Hogarth_House_34_Paradise_Road_Richmond_TW9_1SE.jpg",
        "Leonard and Virginia Woolf lived here from 1915 to 1924, and in 1917 set up the Hogarth Press on the dining-room table, naming it after the house; a blue plaque records both",
        "伍尔夫夫妇 1915 至 1924 年住在这里；1917 年在餐厅的桌子上办起了出版社，以这座房子命名为霍加斯出版社。门口的蓝牌记着这两件事",
        WOOLF),
]
for p in places:
    p["photo"] = photo(p["id"])

def edit_place(s, pid, fn):
    m = re.search(r'^  \{ id: "' + re.escape(pid) + r'",.*$', s, re.M)
    assert m, pid
    return s[:m.start()] + fn(m.group(0)) + s[m.end():]

if __name__ == "__main__":
    append(f"{APP}/data/books.js", books, "11-04 夜 用户补充：《到灯塔去》（塔兰德宅的书）")
    s = open(f"{APP}/data/places.js", encoding="utf-8").read()
    def monks(e):
        e = e.replace('book_ids: ["mrs-dalloway"]', 'book_ids: ["mrs-dalloway", "to-the-lighthouse"]')
        e = e.replace("1980 年起由国民信托作为作家故居开放参观", "她去世后，伦纳德把她的骨灰葬在花园的榆树下。1980 年起由国民信托作为作家故居开放参观")
        e = e.replace("The National Trust has run it as a writer's house museum since 1980", "Leonard buried her ashes under an elm in the garden. The National Trust has run it as a writer's house museum since 1980")
        assert e.count("to-the-lighthouse") == 1 and "榆树" in e and "elm" in e
        return e
    s = edit_place(s, "monks-house", monks)
    for pid in ["daresbury", "carroll-grave", "carroll-christ-church"]:
        def carroll(e):
            if "through-the-looking-glass" in e:
                return e
            assert e.count('book_ids: ["alice-in-wonderland"]') == 1, pid
            return e.replace('book_ids: ["alice-in-wonderland"]', 'book_ids: ["alice-in-wonderland", "through-the-looking-glass"]')
        s = edit_place(s, pid, carroll)
    open(f"{APP}/data/places.js", "w", encoding="utf-8").write(s)
    append(f"{APP}/data/places.js", places, "11-04 夜 用户补充：伍尔夫的另外三处旧居（坐标和照片均有出处）")
    rows = []
    for p in places:
        ph = p["photo"]
        note = " (cropped to landscape)" if ph.get("cropped") else ""
        rows.append(f"| {p['name']} | {ph['author']}{note} | [{ph['license']}]({ph['license_url']}) | [Commons]({ph['source']}) |")
    cr = open(f"{APP}/docs/photo-credits.md", encoding="utf-8").read().rstrip("\n") + "\n" + "\n".join(rows) + "\n"
    open(f"{APP}/docs/photo-credits.md", "w", encoding="utf-8").write(cr)
    print("\n".join(rows))
