"""Add books, places and excerpts for the five regions that had no excerpts (spec 6.5).
Every excerpt below was copied from the source edition named in `checked`.
Usage: python3 -I add_regions.py <app_dir>"""
import json
import re
import sys

APP = sys.argv[1]
G = "https://www.gutenberg.org/ebooks/"

def js(v):
    return json.dumps(v, ensure_ascii=False)

def obj(d):
    return "{ " + ", ".join(f"{k}: {js(v)}" for k, v in d.items()) + " }"

def append(path, entries, marker):
    s = open(path, encoding="utf-8").read()
    i = s.rstrip().rfind("];")
    block = ",\n  // —— " + marker + " ——\n" + ",\n".join("  " + obj(e) for e in entries) + "\n"
    head = s[:i].rstrip()
    s = head + block + "];\n"
    open(path, "w", encoding="utf-8").write(s)

# ---------- books ----------
books_path = f"{APP}/data/books.js"
s = open(books_path, encoding="utf-8").read()
SOURCE_URL = {
    "canterbury-tales": G + "22120", "richard-ii": G + "1512", "macbeth": G + "1533",
    "elegy-churchyard": G + "15409", "life-of-johnson": G + "1564", "blake-songs": G + "1934",
    "burns-highlands": G + "1279", "wordsworth-poems": G + "9622", "to-autumn": G + "23684",
    "persuasion": G + "105", "wuthering-heights": G + "768", "bleak-house": G + "1023",
    "edinburgh-notes": G + "382", "study-in-scarlet": G + "244", "dracula": G + "345",
    "mrs-dalloway": G + "71865",
    "tower-of-london-soseki": "https://www.aozora.gr.jp/cards/000148/card1076.html",
    "saying-goodbye-cambridge": "https://zh.wikisource.org/wiki/%E5%86%8D%E5%88%A5%E5%BA%B7%E6%A9%8B",
}
for bid, url in SOURCE_URL.items():
    pat = re.compile(r'(\{ id: "' + re.escape(bid) + r'",.*?source_url: )"[^"]*"')
    s, n = pat.subn(lambda m: m.group(1) + js(url), s, count=1)
    assert n == 1, bid
# Wordsworth's entry now covers three poems from two collections
s = s.replace('title: "Tintern Abbey; Composed upon Westminster Bridge", title_zh: "廷特恩修道院；威斯敏斯特桥上", author: "William Wordsworth", author_zh: "华兹华斯", year: "1798；1807"',
              'title: "Lyrical Ballads; Poems, in Two Volumes", title_zh: "抒情歌谣集；两卷本诗集", author: "William Wordsworth", author_zh: "华兹华斯", year: "1798；1807"')
open(books_path, "w", encoding="utf-8").write(s)

append(books_path, [
    {"id": "marmion", "title": "Marmion", "title_zh": "玛米恩", "author": "Walter Scott", "author_zh": "司各特", "year": "1808", "orig_lang": "en", "public_domain": True, "source_url": G + "4010"},
    {"id": "north-and-south", "title": "North and South", "title_zh": "南方与北方", "author": "Elizabeth Gaskell", "author_zh": "盖斯凯尔", "year": "1855", "orig_lang": "en", "public_domain": True, "source_url": G + "4276"},
    {"id": "the-rainbow", "title": "The Rainbow", "title_zh": "虹", "author": "D. H. Lawrence", "author_zh": "劳伦斯", "year": "1915", "orig_lang": "en", "public_domain": True, "source_url": G + "28948"},
    {"id": "shropshire-lad", "title": "A Shropshire Lad", "title_zh": "什罗普郡少年", "author": "A. E. Housman", "author_zh": "豪斯曼", "year": "1896", "orig_lang": "en", "public_domain": True, "source_url": G + "5720"},
    {"id": "irish-sketch-book", "title": "The Irish Sketch Book", "title_zh": "爱尔兰札记", "author": "William Makepeace Thackeray", "author_zh": "萨克雷", "year": "1843", "orig_lang": "en", "public_domain": True, "source_url": G + "42890"},
], "11-03 补空白大区：东北、西北、东米德兰兹、西米德兰兹、北爱尔兰")

# ---------- places ----------
append(f"{APP}/data/places.js", [
    {"id": "lindisfarne", "name": "Lindisfarne (Holy Island)", "name_zh": "林迪斯法恩（圣岛）", "lat": 55.6690, "lon": -1.8000, "place_type": "original"},
    {"id": "bamburgh-castle", "name": "Bamburgh Castle", "name_zh": "班堡城堡", "lat": 55.6090, "lon": -1.7099, "place_type": "original"},
    {"id": "glencoyne-bay", "name": "Glencoyne Bay, Ullswater", "name_zh": "阿尔斯沃特湖 · 格伦科因湾", "lat": 54.5590, "lon": -2.9430, "place_type": "prototype",
     "prototype_of": "华兹华斯兄妹 1802 年 4 月看见湖岸水仙的地方", "prototype_of_en": "Where William and Dorothy Wordsworth saw the daffodils in April 1802"},
    {"id": "manchester", "name": "Manchester", "name_zh": "曼彻斯特", "lat": 53.4808, "lon": -2.2426, "place_type": "prototype", "city": True,
     "prototype_of": "《南方与北方》里的工业城 Milton 的原型", "prototype_of_en": "The model for Milton, the mill town of North and South"},
    {"id": "erewash-cossall", "name": "Erewash valley near Cossall", "name_zh": "埃瑞瓦什河谷 · 科索尔附近", "lat": 52.9690, "lon": -1.2960, "place_type": "original"},
    {"id": "bredon-hill", "name": "Bredon Hill", "name_zh": "布雷登山", "lat": 52.0600, "lon": -2.0640, "place_type": "original"},
    {"id": "wenlock-edge", "name": "Wenlock Edge", "name_zh": "温洛克岭", "lat": 52.5530, "lon": -2.6400, "place_type": "original"},
    {"id": "clun", "name": "Clun", "name_zh": "克伦", "lat": 52.4220, "lon": -3.0300, "place_type": "original"},
    {"id": "ludlow", "name": "Ludlow", "name_zh": "拉德洛", "lat": 52.3675, "lon": -2.7190, "place_type": "original", "city": True},
    {"id": "giants-causeway", "name": "Giant's Causeway", "name_zh": "巨人堤", "lat": 55.2408, "lon": -6.5116, "place_type": "original"},
    {"id": "belfast", "name": "Belfast", "name_zh": "贝尔法斯特", "lat": 54.5973, "lon": -5.9301, "place_type": "original", "city": True},
], "11-03 补空白大区")

# ---------- lines ----------
C = ", 2026-11-03"
L = lambda **k: dict(k, translation="original", status="draft")
append(f"{APP}/data/lines.js", [
    L(id="mar-1", book_id="marmion", place_ids=["lindisfarne"], location="Canto II, stanzas VIII–IX", location_zh="第二章第 8–9 节",
      text_en="And reached the Holy Island's bay.\n…\nThe tide did now its floodmark gain,\nAnd girdled in the saint's domain:\nFor, with the flow and ebb, its style\nVaries from continent to isle;\nDry-shod, o'er sands, twice every day,\nThe pilgrims to the shrine find way;",
      highlight_en=["Holy Island"], checked="Project Gutenberg #4010" + C),
    L(id="mar-2", book_id="marmion", place_ids=["bamburgh-castle"], location="Canto II, stanza VIII", location_zh="第二章第 8 节",
      text_en="Thy tower, proud Bamborough, marked they there,\nKing Ida's castle, huge and square,\nFrom its tall rock look grimly down,\nAnd on the swelling ocean frown;",
      highlight_en=["Bamborough"], checked="Project Gutenberg #4010" + C),
    L(id="ww-3", book_id="wordsworth-poems", place_ids=["glencoyne-bay"], location="I wandered lonely as a Cloud (Poems, in Two Volumes, 1807)", location_zh="《我好似一朵流云》（1807 年《两卷本诗集》）",
      text_en="I wandered lonely as a Cloud\nThat floats on high o'er Vales and Hills,\nWhen all at once I saw a crowd\nA host of dancing Daffodills;\nAlong the Lake, beneath the trees,\nTen thousand dancing in the breeze.",
      highlight_en=["Lake", "Daffodills"], checked="Project Gutenberg #8824 (1807 edition)" + C),
    L(id="ns-1", book_id="north-and-south", place_ids=["manchester"], location="Chapter VII", location_zh="第 7 章",
      text_en="For several miles before they reached Milton, they saw a deep lead-coloured cloud hanging over the horizon in the direction in which it lay.",
      highlight_en=["Milton"], checked="Project Gutenberg #4276" + C),
    L(id="rb-1", book_id="the-rainbow", place_ids=["erewash-cossall"], location="Chapter I", location_zh="第 1 章",
      text_en="The Brangwens had lived for generations on the Marsh Farm, in the meadows where the Erewash twisted sluggishly through alder trees, separating Derbyshire from Nottinghamshire.",
      highlight_en=["Erewash", "Derbyshire", "Nottinghamshire"], checked="Project Gutenberg #28948" + C),
    L(id="sl-1", book_id="shropshire-lad", place_ids=["bredon-hill"], location="XXI, Bredon Hill", location_zh="第 21 首《布雷登山》",
      text_en="In summertime on Bredon\nThe bells they sound so clear;\nRound both the shires they ring them\nIn steeples far and near,",
      highlight_en=["Bredon"], checked="Project Gutenberg #5720" + C),
    L(id="sl-2", book_id="shropshire-lad", place_ids=["wenlock-edge"], location="XXXI", location_zh="第 31 首",
      text_en="On Wenlock Edge the wood's in trouble;\nHis forest fleece the Wrekin heaves;\nThe gale, it plies the saplings double,\nAnd thick on Severn snow the leaves.",
      highlight_en=["Wenlock Edge", "Wrekin", "Severn"], checked="Project Gutenberg #5720" + C),
    L(id="sl-3", book_id="shropshire-lad", place_ids=["clun"], location="L", location_zh="第 50 首",
      text_en="Clunton and Clunbury,\nClungunford and Clun,\nAre the quietest places\nUnder the sun.",
      highlight_en=["Clunton and Clunbury", "Clungunford and Clun"], checked="Project Gutenberg #5720" + C),
    L(id="sl-4", book_id="shropshire-lad", place_ids=["ludlow"], location="XXIII", location_zh="第 23 首",
      text_en="The lads in their hundreds to Ludlow come in for the fair,",
      highlight_en=["Ludlow"], checked="Project Gutenberg #5720" + C),
    L(id="bos-2", book_id="life-of-johnson", place_ids=["giants-causeway"], location="1779", location_zh="1779 年",
      text_en="BOSWELL. 'Is not the Giant's-Causeway worth seeing?' JOHNSON. 'Worth seeing? yes; but not worth going to see.'",
      highlight_en=["Giant's-Causeway"], checked="Project Gutenberg #1564" + C),
    L(id="isb-1", book_id="irish-sketch-book", place_ids=["belfast"], location="Newry, Armagh, Belfast", location_zh="《纽里、阿马、贝尔法斯特》一章",
      text_en="the town of Belfast seemed to me really to be as neat, prosperous, and handsome a city as need be seen;",
      highlight_en=["Belfast"], checked="Project Gutenberg #42890" + C),
    L(id="isb-2", book_id="irish-sketch-book", place_ids=["giants-causeway"], location="Belfast to the Causeway", location_zh="《从贝尔法斯特到巨人堤》一章",
      text_en="The road to the Causeway is bleak, wild, and hilly.\n…\nSee, yonder are the black rocks stretching to Portrush; how leaden and grey the sea looks! how grey and leaden the sky!",
      highlight_en=["Causeway", "Portrush"], checked="Project Gutenberg #42890" + C),
], "11-03 补空白大区（均从原文摘录）")
print("done")
