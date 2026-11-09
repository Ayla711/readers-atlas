"""Add English fields to places.js and bilingual locations to lines.js.
Usage: python3 -I add_english.py <app_dir>"""
import re
import sys

APP = sys.argv[1]

PLACE_EN = {
    "stoke-poges": ("prototype_of_en", "The country churchyard of Gray's Elegy"),
    "st-cross-winchester": ("prototype_of_en", "Where Keats walked before writing To Autumn"),
    "top-withens": ("prototype_of_en", "Widely held to be the model for Wuthering Heights"),
    "poets-corner": ("note_en", "Chaucer is buried here, and Poets' Corner grew up around his tomb"),
    "shakespeare-birthplace": ("note_en", "Henley Street, Stratford-upon-Avon"),
    "dove-cottage": ("note_en", "Wordsworth's home"),
    "keats-house": ("note_en", "Keats's home"),
    "chawton": ("note_en", "Where Austen did her later writing"),
    "bronte-parsonage": ("note_en", "Home of the Brontë sisters"),
    "dickens-museum": ("note_en", "48 Doughty Street"),
    "sherlock-museum": ("note_en", "It carries the 221B Baker Street door number"),
    "xu-zhimo-stone": ("note_en", "A stone carved with lines from Saying Goodbye to Cambridge Again"),
    "lao-she-plaque": ("note_en", "Put up by English Heritage in 2003"),
    "cuckmere-cottages": ("scene_en", "Robbie and Cecilia's seaside cottage in the ending"),
    "leadenhall-market": ("scene_en", "Diagon Alley and the entrance to the Leaky Cauldron"),
    "christ-church": ("scene_en", "The staircase where first-years walk up to the Great Hall"),
    "alnwick-castle": ("scene_en", "Hogwarts exteriors and the flying lesson"),
    "glenfinnan": ("scene_en", "The Hogwarts Express crossing the viaduct"),
    "dyrham-park": ("scene_en", "Darlington Hall's exterior and drive"),
    "chalcot-crescent": ("scene_en", "The Browns' house at 32 Windsor Gardens"),
    "doune-castle": ("scene_en", "Castle Leoch, seat of Clan MacKenzie"),
}

LINE_LOC = {
    "ct-1": ("General Prologue", "总引"),
    "ct-2": ("General Prologue", "总引"),
    "r2-1": ("Act 2, Scene 1 (set at Ely House)", "第二幕第一场（剧情设在伊利府）"),
    "mac-1": ("Act 1, Scene 6 (before Macbeth's castle at Inverness)", "第一幕第六场（麦克白的因弗内斯城堡前）"),
    "mac-2": ("Act 4, Scene 1", "第四幕第一场"),
    "gray-1": ("Stanza 1", "第 1 节"),
    "bos-1": ("20 September 1777", "1777 年 9 月 20 日"),
    "blake-1": ("London (Songs of Experience)", "《伦敦》（《经验之歌》）"),
    "blake-2": ("Holy Thursday (Songs of Innocence)", "《圣星期四》（《天真之歌》）"),
    "burns-1": ("Stanza 1", "第 1 节"),
    "ww-1": ("Composed upon Westminster Bridge", "《威斯敏斯特桥上》"),
    "ww-2": ("Tintern Abbey, opening lines", "《廷特恩修道院》，开篇"),
    "keats-1": ("Stanza 1", "第 1 节"),
    "pers-1": ("Volume I, Chapter 11", "第一卷第 11 章"),
    "wh-1": ("Chapter 1", "第 1 章"),
    "wh-2": ("Chapter 34 (closing lines)", "第 34 章（结尾）"),
    "bh-1": ("Chapter 1", "第 1 章"),
    "bh-2": ("Chapter 1", "第 1 章"),
    "edi-1": ("Chapter 1", "第 1 章"),
    "sis-1": ("Part I, Chapter 1", "第一部第 1 章"),
    "sis-2": ("Part I, Chapter 1", "第一部第 1 章"),
    "dra-1": ("Chapter 6 (Mina's journal)", "第 6 章（Mina 的日记）"),
    "sos-1": ("Opening", "开篇"),
    "dal-1": ("Opening", "开篇"),
    "dal-2": ("Opening", "开篇"),
    "xu-1": ("Stanza 1", "第 1 节"),
    "xu-2": ("Stanza 2", "第 2 节"),
}

# ---- places: one object per line; insert the English field before the closing brace
path = f"{APP}/data/places.js"
src = open(path, encoding="utf-8").read().splitlines()
done = set()
for i, line in enumerate(src):
    m = re.search(r'\{ id: "([^"]+)"', line)
    if m and m.group(1) in PLACE_EN:
        key, val = PLACE_EN[m.group(1)]
        val = val.replace('"', '\\"')
        if key == "scene_en":
            line = line.replace('}, scene:', ' }, scene:', 1)
        line = re.sub(r"\s*\},?\s*$", lambda mm: f', {key}: "{val}" ' + ("}," if mm.group(0).strip().endswith(",") else "}"), line)
        # adaptation kind in English
        line = line.replace('kind: "电影" }', 'kind: "电影", kind_en: "film" }').replace('kind: "电视剧" }', 'kind: "电视剧", kind_en: "TV series" }')
        src[i] = line
        done.add(m.group(1))
missing = set(PLACE_EN) - done
assert not missing, missing
open(path, "w", encoding="utf-8").write("\n".join(src) + "\n")

# ---- lines: replace location with English and add location_zh
path = f"{APP}/data/lines.js"
text = open(path, encoding="utf-8").read()
count = 0
for lid, (en, zh) in LINE_LOC.items():
    pat = re.compile(r'(\{ id: "' + re.escape(lid) + r'",.*?location: )"[^"]*"', re.S)
    text, n = pat.subn(lambda m: m.group(1) + '"' + en.replace('"', '\\"') + '", location_zh: "' + zh + '"', text, count=1)
    count += n
assert count == len(LINE_LOC), count
text = text.replace("// translation：", "// location 为英文，location_zh 为中文。\n// translation：")
open(path, "w", encoding="utf-8").write(text)
print("places updated:", len(done), "lines updated:", count)
