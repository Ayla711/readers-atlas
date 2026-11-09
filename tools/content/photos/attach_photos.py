"""Attach chosen photos to places that are already in data/<country>/places.js.
Usage: python3 -I attach_photos.py <app_dir> <country> <work_dir>
<work_dir>/choice.json: {"<place id>": [<candidate index>, "alt text (en)", "alt text (zh)", crop or null], ...}
    crop: [x0, y0, x1, y1] as fractions of the image, or null.
Reads <work_dir>/candidates.json and dl/<id>__<n>.jpg (from find_photos.py + dl_here.py), writes images/places/<id>.jpg
(800 px wide, JPEG q82), inserts the photo object into the place record and appends the credit rows to
docs/photo-credits.md."""
import json, re, sys
from PIL import Image
APP, COUNTRY, PW = sys.argv[1], sys.argv[2], sys.argv[3]
choice = json.load(open(f"{PW}/choice.json", encoding="utf-8"))
cands = json.load(open(f"{PW}/candidates.json", encoding="utf-8"))
pp = f"{APP}/data/{COUNTRY}/places.js"
s = open(pp, encoding="utf-8").read()
rows = []
for pid, (n, en, zh, crop) in choice.items():
    c = cands[pid]["candidates"][n]
    im = Image.open(f"{PW}/dl/{pid}__{n}.jpg").convert("RGB")
    if crop:
        x0, y0, x1, y1 = crop
        im = im.crop((round(x0 * im.width), round(y0 * im.height), round(x1 * im.width), round(y1 * im.height)))
    if im.width > 800:
        im = im.resize((800, round(im.height * 800 / im.width)), Image.LANCZOS)
    assert im.width >= im.height, f"{pid}: portrait images are not used"
    rel = f"images/places/{pid}.jpg"
    im.save(f"{APP}/{rel}", "JPEG", quality=82, optimize=True, progressive=True)
    photo = {"file": rel, "width": im.width, "height": im.height, "author": c["author"].strip() or "Unknown author", "license": c["license"].strip(),
             "license_url": c["license_url"].strip(), "source": c["page"], "alt_en": en, "alt_zh": zh}
    if crop:
        photo["cropped"] = True
    m = re.search(r'(\{ id: "' + re.escape(pid) + r'".*?)( \},?\n)', s)
    assert m, f"{pid}: not in {pp}"
    assert "photo:" not in m.group(1), f"{pid}: already has a photo"
    s = s[:m.end(1)] + ", photo: " + json.dumps(photo, ensure_ascii=False) + s[m.end(1):]
    name = re.search(r'name: "([^"]*)"', m.group(1)).group(1)
    rows.append(f"| {name} | {photo['author']} | [{photo['license']}]({photo['license_url']}) | [Commons]({photo['source']}) |")
open(pp, "w", encoding="utf-8").write(s)
with open(f"{APP}/docs/photo-credits.md", "a", encoding="utf-8") as fh:
    fh.write("\n".join(rows) + "\n")
print(len(rows), "photos attached")
