"""11-04 night: Godrevy Lighthouse as the real-life model for the lighthouse in To the Lighthouse, with one excerpt.
The text could not be downloaded here (Standard Ebooks and the other copies are blocked for this connection), so the
sentence was read from the Standard Ebooks single-page text through the web reader in pieces under 125 characters,
each piece read twice and the overlaps checked. Photo and coordinates from Commons / Geograph.
Usage: python3 -I add_batch9.py <app_dir> <pg_texts_dir> <photo_work_dir>"""
import importlib.util, json, sys
from PIL import Image
APP, TX, PW = sys.argv[1], sys.argv[2], sys.argv[3]
spec = importlib.util.spec_from_file_location("b5", __file__.replace("add_batch9.py", "add_batch5.py"))
b5 = importlib.util.module_from_spec(spec)
_argv, sys.argv = sys.argv, [sys.argv[0], APP, TX]
spec.loader.exec_module(b5)
sys.argv = _argv
append, PROTO, D = b5.append, b5.PROTO, b5.D

c = json.load(open(f"{PW}/candidates.json"))["godrevy"]["candidates"][4]
im = Image.open(f"{PW}/dl/godrevy__4.jpg").convert("RGB")
if im.width > 800:
    im = im.resize((800, round(im.height * 800 / im.width)), Image.LANCZOS)
im.save(f"{APP}/images/places/godrevy.jpg", "JPEG", quality=82, optimize=True, progressive=True)
photo = {"file": "images/places/godrevy.jpg", "width": im.width, "height": im.height, "author": c["author"].strip(), "license": c["license"].strip(),
         "license_url": c["license_url"].strip(), "source": c["page"], "alt_en": "Godrevy Lighthouse on its island in St Ives Bay",
         "alt_zh": "圣艾夫斯湾小岛上的戈德雷维灯塔"}
place = PROTO("godrevy", "Godrevy Lighthouse", "戈德雷维灯塔", 50.2425, -5.4004,
              "Godrevy Lighthouse, Godrevy Island (Geograph photo 407138, subject location)", "https://www.geograph.org.uk/photo/407138",
              "The lighthouse on its rock in St Ives Bay that the Stephen children looked out to from Talland House. The novel moves the Ramsays to the Isle of Skye, but its lighthouse is usually traced to Godrevy",
              "圣艾夫斯湾小岛上的灯塔，斯蒂芬家的孩子们在塔兰德宅就能望见它。小说把拉姆齐一家搬到了斯凯岛，但书里的灯塔通常被认为来自戈德雷维",
              offshore_island=True)
place["photo"] = photo
text = ("For the great plateful of blue water was before her; the hoary Lighthouse, distant, austere, in the midst; "
        "and on the right, as far as the eye could see, fading and falling, in soft low pleats, the green sand dunes with the wild "
        "flowing grasses on them, which always seemed to be running away into some moon country, uninhabited of men.")
line = dict(id="ttl-1", book_id="to-the-lighthouse", place_ids=["godrevy"], location="The Window, section 1", location_zh="第一部《窗》第 1 节",
            text_en=text, highlight_en=["hoary Lighthouse"], translation="original", status="draft",
            checked="Standard Ebooks, To the Lighthouse (single-page text, read in pieces through the web reader and cross-checked)" + D)
if __name__ == "__main__":
    append(f"{APP}/data/places.js", [place], "11-04 夜 用户补充：戈德雷维灯塔（《到灯塔去》的灯塔原型）")
    append(f"{APP}/data/lines.js", [line], "11-04 夜 用户补充：《到灯塔去》第一部")
    row = f"| {place['name']} | {photo['author']} | [{photo['license']}]({photo['license_url']}) | [Commons]({photo['source']}) |"
    cr = open(f"{APP}/docs/photo-credits.md", encoding="utf-8").read().rstrip("\n") + "\n" + row + "\n"
    open(f"{APP}/docs/photo-credits.md", "w", encoding="utf-8").write(cr)
    print(row)
