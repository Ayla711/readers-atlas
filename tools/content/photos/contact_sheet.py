"""Contact sheets of photo candidates: one row per place, up to 4 thumbnails with index and license.
Usage: python3 -I contact_sheet.py <work_dir> <places_per_sheet>"""
import json
import sys
from PIL import Image, ImageDraw, ImageFont

WORK, PER = sys.argv[1], int(sys.argv[2])
d = json.load(open(f"{WORK}/candidates.json"))
TW, TH, PAD, LABEL = 300, 200, 8, 34
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 13)
    big = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
except OSError:
    font = big = ImageFont.load_default()
ids = list(d)
for s in range(0, len(ids), PER):
    group = ids[s:s + PER]
    W = PAD + 4 * (TW + PAD)
    H = len(group) * (TH + LABEL + 26 + PAD) + PAD
    sheet = Image.new("RGB", (W, H), "white")
    dr = ImageDraw.Draw(sheet)
    y = PAD
    for pid in group:
        dr.text((PAD, y), pid, fill="black", font=big)
        y += 22
        for i, c in enumerate(d[pid]["candidates"]):
            im = Image.open(c["thumb"]).convert("RGB")
            im.thumbnail((TW, TH))
            x = PAD + i * (TW + PAD)
            sheet.paste(im, (x, y))
            dr.text((x, y + TH + 2), f"[{i}] {c['license']}", fill="black", font=font)
            dr.text((x, y + TH + 17), c["title"][5:45], fill="#555", font=font)
        if not d[pid]["candidates"]:
            dr.text((PAD, y + 80), "(no usable candidates)", fill="red", font=big)
        y += TH + LABEL + PAD
    out = f"{WORK}/sheet_{s // PER + 1}.jpg"
    sheet.save(out, quality=80)
    print(out, group)
