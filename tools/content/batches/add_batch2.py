"""Batch 2 (11-03 evening): 25 books, 33 places, 37 excerpts toward the Week 1 targets.
Every excerpt is cut out of the downloaded Project Gutenberg file, never typed by hand.
Usage: python3 -I add_batch2.py <app_dir> <texts_dir>"""
import json
import re
import sys

APP, TX = sys.argv[1], sys.argv[2]
G = "https://www.gutenberg.org/ebooks/"
C = ", 2026-11-03"

def norm(s):
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = s.replace("_", "")
    s = re.sub(r"\s*--\s*", "—", s)          # Gutenberg's double hyphen is an em dash
    s = re.sub(r"(\w)- (\w)", r"\1-\2", s)    # rejoin words split by a line-wrap hyphen ("walls-- tottering" is handled above)
    return s

_cache = {}
def flat(book):
    if book not in _cache:
        raw = open(f"{TX}/{book}.txt", encoding="utf-8").read().replace("\r", "")
        paras = [norm(" ".join(p.split())) for p in re.split(r"\n\s*\n", raw)]
        _cache[book] = (raw, paras)
    return _cache[book]

def prose(book, start, end):
    """the exact text from `start` to the end of `end`, inside one paragraph"""
    for p in flat(book)[1]:
        i = p.find(start)
        if i < 0:
            continue
        j = p.find(end, i)
        assert j >= 0, (book, start, end)
        return p[i:j + len(end)]
    raise SystemExit(f"not found in {book}: {start}")

def verse(book, start, n, join_wrapped=False):
    """n non-empty lines from the first line containing `start`, indentation removed"""
    raw = flat(book)[0].split("\n")
    for i, l in enumerate(raw):
        if start in norm(l):
            out = []
            for l2 in raw[i:]:
                s = norm(l2.strip())
                if not s:
                    continue
                if join_wrapped and out and out[-1].endswith("-") and not out[-1].endswith("--"):
                    out[-1] += s            # Hopkins' printer wrapped long lines mid-word
                else:
                    out.append(s)
                if len(out) == n and not (join_wrapped and s.endswith("-")):
                    return out
    raise SystemExit(f"verse not found in {book}: {start}")

GAP = "\n…\n"

def js(v):
    return json.dumps(v, ensure_ascii=False)

def obj(d):
    return "{ " + ", ".join(f"{k}: {js(v)}" for k, v in d.items()) + " }"

def append(path, entries, marker):
    s = open(path, encoding="utf-8").read()
    i = s.rstrip().rfind("];")
    s = s[:i].rstrip() + ",\n  // —— " + marker + " ——\n" + ",\n".join("  " + obj(e) for e in entries) + "\n];\n"
    open(path, "w", encoding="utf-8").write(s)

def B(id, title, title_zh, author, author_zh, year, pg):
    return dict(id=id, title=title, title_zh=title_zh, author=author, author_zh=author_zh, year=year, orig_lang="en", public_domain=True, source_url=G + str(pg))

books = [
    B("pride-and-prejudice", "Pride and Prejudice", "傲慢与偏见", "Jane Austen", "奥斯汀", "1813", 1342),
    B("emma", "Emma", "爱玛", "Jane Austen", "奥斯汀", "1815", 158),
    B("northanger-abbey", "Northanger Abbey", "诺桑觉寺", "Jane Austen", "奥斯汀", "1817", 121),
    B("pickwick-papers", "The Pickwick Papers", "匹克威克外传", "Charles Dickens", "狄更斯", "1836–1837", 580),
    B("david-copperfield", "David Copperfield", "大卫·科波菲尔", "Charles Dickens", "狄更斯", "1850", 766),
    B("hard-times", "Hard Times", "艰难时世", "Charles Dickens", "狄更斯", "1854", 786),
    B("great-expectations", "Great Expectations", "远大前程", "Charles Dickens", "狄更斯", "1861", 1400),
    B("cranford", "Cranford", "克兰福德", "Elizabeth Gaskell", "盖斯凯尔", "1853", 394),
    B("mill-on-the-floss", "The Mill on the Floss", "弗洛斯河上的磨坊", "George Eliot", "乔治·艾略特", "1860", 6688),
    B("tess", "Tess of the d'Urbervilles", "德伯家的苔丝", "Thomas Hardy", "哈代", "1891", 110),
    B("hound-of-the-baskervilles", "The Hound of the Baskervilles", "巴斯克维尔的猎犬", "Arthur Conan Doyle", "柯南·道尔", "1902", 2852),
    B("kidnapped", "Kidnapped", "绑架", "Robert Louis Stevenson", "史蒂文森", "1886", 421),
    B("three-men-in-a-boat", "Three Men in a Boat", "三怪客泛舟记", "Jerome K. Jerome", "杰罗姆", "1889", 308),
    B("sons-and-lovers", "Sons and Lovers", "儿子与情人", "D. H. Lawrence", "劳伦斯", "1913", 217),
    B("merry-adventures-robin-hood", "The Merry Adventures of Robin Hood", "罗宾汉的快乐冒险", "Howard Pyle", "派尔", "1883", 10148),
    B("journey-western-islands", "A Journey to the Western Islands of Scotland", "苏格兰西部群岛旅行记", "Samuel Johnson", "约翰逊", "1775", 2064),
    B("king-lear", "King Lear", "李尔王", "William Shakespeare", "莎士比亚", "1606", 1532),
    B("lady-of-the-lake", "The Lady of the Lake", "湖上夫人", "Walter Scott", "司各特", "1810", 3011),
    B("arnold-new-poems", "New Poems", "新诗集", "Matthew Arnold", "阿诺德", "1867", 54985),
    B("hopkins-poems", "Poems", "霍普金斯诗集", "Gerard Manley Hopkins", "霍普金斯", "1918", 22403),
    B("grantchester", "The Old Vicarage, Grantchester", "格兰切斯特的老牧师住宅", "Rupert Brooke", "布鲁克", "1912", 262),
    B("old-wives-tale", "The Old Wives' Tale", "老妇谭", "Arnold Bennett", "本涅特", "1908", 5247),
    B("puck-of-pooks-hill", "Puck of Pook's Hill", "普克山的帕克", "Rudyard Kipling", "吉卜林", "1906", 26027),
    B("wild-wales", "Wild Wales", "狂野的威尔士", "George Borrow", "博罗", "1862", 648),
    B("lorna-doone", "Lorna Doone", "洛娜·杜恩", "R. D. Blackmore", "布莱克莫尔", "1869", 17460),
]

def P(id, name, name_zh, lat, lon, **kw):
    return dict(id=id, name=name, name_zh=name_zh, lat=lat, lon=lon, place_type=kw.pop("type", "original"), **kw)

def PROTO(id, name, name_zh, lat, lon, zh, en, **kw):
    return P(id, name, name_zh, lat, lon, type="prototype", prototype_of=zh, prototype_of_en=en, **kw)

# coordinates: Wikipedia for Bateman's (Pook's Hill), Erraid, Cooling church, Iffley Lock, Badgworthy Water;
# Natural Earth populated places for Bath, Brighton, Oxford, Dover (city centres adjusted to the historic core);
# the rest are well-known landmarks, still to be checked in the coordinate pass (spec 6.5)
places = [
    PROTO("chatsworth", "Chatsworth House", "查茨沃斯庄园", 53.2275, -1.6115, "常被认为是《傲慢与偏见》彭伯里庄园的原型", "Widely held to be a model for Pemberley in Pride and Prejudice"),
    P("brighton", "Brighton", "布莱顿", 50.8225, -0.1372, city=True),
    P("box-hill", "Box Hill", "博克斯山", 51.2560, -0.3100),
    P("bath", "Bath", "巴斯", 51.3811, -2.3590, city=True),
    P("beechen-cliff", "Beechen Cliff, Bath", "巴斯 · 比琴崖", 51.3757, -2.3576),
    P("bath-pump-room", "The Pump Room, Bath", "巴斯 · 大泵房", 51.3813, -2.3597),
    P("rochester-castle", "Rochester Castle", "罗切斯特城堡", 51.3896, 0.5014),
    P("great-yarmouth", "Great Yarmouth", "大雅茅斯", 52.6083, 1.7305, city=True),
    PROTO("preston", "Preston", "普雷斯顿", 53.7632, -2.7031, "常被认为是《艰难时世》焦煤镇的原型", "Often named as the model for Coketown in Hard Times", city=True),
    PROTO("cooling-church", "St James' Church, Cooling", "库林 · 圣詹姆斯教堂", 51.4553, 0.5264, "《远大前程》开篇沼地墓园的原型", "The model for the marsh churchyard where Great Expectations opens"),
    PROTO("knutsford", "Knutsford", "纳茨福德", 53.3025, -2.3708, "《克兰福德》的原型，盖斯凯尔在这里长大", "The model for Cranford, where Gaskell grew up", city=True),
    PROTO("gainsborough", "Gainsborough", "盖恩斯伯勒", 53.3994, -0.7763, "《弗洛斯河上的磨坊》圣奥格镇的原型", "The model for St Ogg's in The Mill on the Floss", city=True),
    P("blackmore-vale", "Blackmore Vale", "布莱克莫尔谷", 50.9667, -2.3167),
    P("stonehenge", "Stonehenge", "巨石阵", 51.1789, -1.8262),
    P("dartmoor", "Dartmoor", "达特穆尔高原", 50.5700, -3.9200),
    P("erraid", "Erraid", "埃雷德岛", 56.2900, -6.3600, offshore_island=True),
    P("queensferry", "South Queensferry", "南昆斯费里", 55.9895, -3.3960),
    P("hampton-court", "Hampton Court maze", "汉普顿宫迷宫", 51.4065, -0.3378),
    P("marlow", "Marlow", "马洛", 51.5710, -0.7769, city=True),
    P("iffley-lock", "Iffley Lock", "伊夫利船闸", 51.7285, -1.2403),
    PROTO("eastwood", "Eastwood", "伊斯特伍德", 53.0186, -1.3049, "劳伦斯的出生地，《儿子与情人》里 Bestwood 的原型", "Lawrence's birthplace, the model for Bestwood in Sons and Lovers", city=True),
    P("sherwood-forest", "Sherwood Forest", "舍伍德森林", 53.2045, -1.0726),
    P("iona", "Iona", "艾奥纳岛", 56.3346, -6.3925, offshore_island=True),
    P("loch-ness", "Loch Ness", "尼斯湖", 57.3000, -4.4500),
    P("shakespeare-cliff", "Shakespeare Cliff, Dover", "多佛尔 · 莎士比亚崖", 51.1100, 1.2918),
    P("dover", "Dover", "多佛尔", 51.1279, 1.3134, city=True),
    P("grantchester", "Grantchester", "格兰切斯特", 52.1797, 0.0962),
    P("loch-katrine", "Loch Katrine", "卡特琳湖", 56.2500, -4.5000),
    P("oxford", "Oxford", "牛津", 51.7520, -1.2577, city=True),
    P("elwy-valley", "Elwy valley", "埃尔威河谷", 53.2400, -3.4800),
    PROTO("burslem", "Burslem", "伯斯勒姆", 53.0450, -2.1990, "本涅特《老妇谭》里 Bursley 的原型", "The model for Bursley in The Old Wives' Tale", city=True),
    P("pooks-hill", "Pook's Hill, Burwash", "伯沃什 · 普克山", 50.9893, 0.3793),
    P("snowdon", "Snowdon", "斯诺登山", 53.0685, -4.0763),
    P("llangollen", "Llangollen", "兰戈伦", 52.9700, -3.1700, city=True),
    P("doone-valley", "Doone Valley, Badgworthy Water", "杜恩谷 · 巴奇沃西溪", 51.1975, -3.7255),
]

def L(id, book_id, place, loc, loc_zh, text, hl, pg):
    for h in hl:
        assert h in text, (id, h)
    return dict(id=id, book_id=book_id, place_ids=[place], location=loc, location_zh=loc_zh, text_en=text,
                highlight_en=hl, translation="original", status="draft", checked=f"Project Gutenberg #{pg}{C}")

def caps(s, word, fixed):
    """display small caps at the start of a chapter or poem, e.g. "IN the first place" -> "In the first place" """
    return s.replace(word, fixed, 1)

lines = [
    L("pp-1", "pride-and-prejudice", "chatsworth", "Chapter 43", "第 43 章",
      prose(1342, "the eye was instantly caught by Pemberley House", "backed by a ridge of high woody hills;"), ["Pemberley House"], 1342),
    L("pp-2", "pride-and-prejudice", "brighton", "Chapter 41", "第 41 章",
      prose(1342, "In Lydia's imagination, a visit to Brighton", "covered with officers."), ["Brighton"], 1342),
    L("emma-1", "emma", "box-hill", "Volume III, Chapter VII", "第三卷第 7 章",
      prose(158, "They had a very fine day for Box Hill;", "in favour of a pleasant party."), ["Box Hill"], 158),
    L("na-1", "northanger-abbey", "bath", "Chapter 2", "第 2 章",
      prose(121, "They arrived at Bath.", "conducted them to the hotel."), ["Bath"], 121),
    L("na-2", "northanger-abbey", "beechen-cliff", "Chapter 14", "第 14 章",
      prose(121, "They determined on walking round Beechen Cliff", "from almost every opening in Bath."), ["Beechen Cliff", "Bath"], 121),
    L("pick-1", "pickwick-papers", "rochester-castle", "Chapter II", "第 2 章",
      prose(580, "'Magnificent ruin!' said Mr. Augustus Snodgrass", "came in sight of the fine old castle.") + GAP
      + prose(580, "'Ah! fine place,' said the stranger", "old cathedral too—"), ["fine old castle"], 580),
    L("pick-2", "pickwick-papers", "bath-pump-room", "Chapter XXXVI", "第 36 章",
      prose(580, "The Great Pump Room is a spacious saloon", "and a statue of Nash,"), ["Great Pump Room"], 580),
    L("dc-1", "david-copperfield", "great-yarmouth", "Chapter 3", "第 3 章",
      prose(766, "it was well known (I suppose to those", "the finest place in the universe."), ["Yarmouth"], 766),
    L("dc-2", "david-copperfield", "canterbury-cathedral", "Chapter 13", "第 13 章",
      prose(766, "I have associated it, ever since, with the sunny street of Canterbury", "with the rooks sailing round the towers."), ["Canterbury", "Cathedral"], 766),
    L("ht-1", "hard-times", "preston", "Book the First, Chapter V", "第一部第 5 章",
      caps(prose(786, "COKETOWN, to which Messrs. Bounderby", "was a triumph of fact;"), "COKETOWN", "Coketown") + GAP
      + prose(786, "It was a town of red brick", "like the painted face of a savage."), ["Coketown"], 786),
    L("ge-1", "great-expectations", "cooling-church", "Chapter I", "第 1 章",
      prose(1400, "Ours was the marsh country", "twenty miles of the sea.") + GAP
      + prose(1400, "At such a time I found out for certain", "was the churchyard;"), ["marsh country", "churchyard"], 1400),
    L("cran-1", "cranford", "knutsford", "Chapter I", "第 1 章",
      caps(prose(394, "IN the first place, Cranford", "above a certain rent are women."), "IN the", "In the"), ["Cranford"], 394),
    L("mof-1", "mill-on-the-floss", "gainsborough", "Book I, Chapter I", "第一部第 1 章",
      prose(6688, "A wide plain, where the broadening Floss", "with an impetuous embrace.") + GAP
      + prose(6688, "the town of St Ogg's, which shows", "the broad gables of its wharves"), ["Floss", "St Ogg's"], 6688),
    L("tess-1", "tess", "blackmore-vale", "Chapter II", "第 2 章",
      prose(110, "The village of Marlott lay amid", "within a four hours' journey from London."), ["Vale of Blakemore, or Blackmoor"], 110),
    L("tess-2", "tess", "stonehenge", "Chapter LVIII", "第 58 章",
      "\n".join([prose(110, "\"It is Stonehenge!\"", "said Clare."), prose(110, "\"The heathen temple, you mean?\"", "you mean?\""),
                 prose(110, "\"Yes. Older than the centuries", "older than the d'Urbervilles!")]), ["Stonehenge"], 110),
    L("hound-1", "hound-of-the-baskervilles", "dartmoor", "Chapter 6", "第 6 章",
      prose(2852, "behind the peaceful and sunlit countryside", "the jagged and sinister hills."), ["moor"], 2852),
    L("kid-1", "kidnapped", "erraid", "Chapter XIII", "第 13 章",
      prose(421, "The reef on which we had struck", "lay low and black upon the larboard."), ["Mull", "Earraid"], 421),
    L("kid-2", "kidnapped", "queensferry", "Chapter V", "第 5 章",
      prose(421, "The town of Queensferry lies farther west", "gone north with passengers."), ["Queensferry"], 421),
    L("jwi-1", "journey-western-islands", "iona", "Inch Kenneth", "《因奇肯尼思》一节",
      prose(2064, "We were now treading that illustrious Island", "the blessings of religion.") + GAP
      + prose(2064, "That man is little to be envied", "among the ruins of Iona!"), ["illustrious Island", "Iona"], 2064),
    L("jwi-2", "journey-western-islands", "loch-ness", "Lough Ness", "《尼斯湖》一节",
      prose(2064, "On the right the limpid waters of Lough Ness", "by a gentle agitation."), ["Lough Ness"], 2064),
    L("lear-1", "king-lear", "shakespeare-cliff", "Act IV, Scene I", "第四幕第一场",
      "Dost thou know Dover?\nEDGAR. Ay, master.\nGLOUCESTER. " + "\n".join(verse(1532, "There is a cliff, whose high", 2)), ["Dover", "cliff"], 1532),
    L("lol-1", "lady-of-the-lake", "loch-katrine", "Canto I, stanza XIV", "第一章第 14 节",
      "\n".join(verse(3011, "Where, gleaming with the setting sun", 4)), ["Loch Katrine"], 3011),
    L("tmb-1", "three-men-in-a-boat", "hampton-court", "Chapter VI", "第 6 章",
      prose(308, "Harris asked me if I'd ever been in the maze", "hardly worth the twopence charged for admission."), ["maze at Hampton Court"], 308),
    L("tmb-2", "three-men-in-a-boat", "marlow", "Chapter XIII", "第 13 章",
      prose(308, "Marlow is one of the pleasantest river centres", "to be found in it, nevertheless"), ["Marlow"], 308),
    L("tmb-3", "three-men-in-a-boat", "iffley-lock", "Chapter XVIII", "第 18 章",
      prose(308, "Iffley Lock and Mill, a mile before you reach Oxford", "rather disappointing, after the pictures."), ["Iffley Lock", "Oxford"], 308),
    L("sal-1", "sons-and-lovers", "eastwood", "Part One, Chapter I", "第一部第 1 章",
      prose(217, "\"The Bottoms\" succeeded to \"Hell Row\".", "in the little gin-pits two fields away."), ["The Bottoms", "Hell Row"], 217),
    L("rh-1", "merry-adventures-robin-hood", "sherwood-forest", "Prologue", "序",
      caps(prose(10148, "IN MERRY ENGLAND in the time of old", "whose name was Robin Hood."), "IN MERRY ENGLAND", "In merry England"),
      ["Sherwood Forest", "Nottingham Town"], 10148),
    L("arn-1", "arnold-new-poems", "dover", "Dover Beach", "《多佛海滩》",
      "\n".join(verse(54985, "The sea is calm to-night.", 5)), ["straits", "cliffs of England"], 54985),
    L("arn-2", "arnold-new-poems", "oxford", "Thyrsis", "《塞西斯》",
      "\n".join(verse(54985, "And that sweet city with her dreaming spires", 2)), ["sweet city with her dreaming spires"], 54985),
    L("hop-1", "hopkins-poems", "oxford", "Duns Scotus's Oxford", "《邓斯·司各脱的牛津》",
      caps("\n".join(verse(22403, "TOWERY city and branchy", 2, join_wrapped=True)), "TOWERY", "Towery"), ["Towery city", "river-rounded"], 22403),
    L("hop-2", "hopkins-poems", "elwy-valley", "In the Valley of the Elwy", "《在埃尔威河谷》",
      "\n".join(verse(22403, "Lovely the woods, waters, meadows", 2)), ["Wales"], 22403),
    L("gr-1", "grantchester", "grantchester", "Closing section", "后半部分至结尾",
      "\n".join(verse(262, "Ah God! to see the branches stir", 2)) + GAP + "\n".join(verse(262, "Stands the Church clock at ten to three?", 2)),
      ["Grantchester"], 262),
    L("owt-1", "old-wives-tale", "burslem", "Book I, Chapter I", "第一部第 1 章",
      prose(5247, "Bursley has the honours of antiquity", "absolutely sure in its conceit."), ["Bursley", "Five Towns"], 5247),
    L("puck-1", "puck-of-pooks-hill", "pooks-hill", "Weland's Sword", "《韦兰之剑》",
      prose(26027, "right under one of my oldest hills in Old England?", "plain as the nose on my face."), ["Pook's Hill"], 26027),
    L("wwa-1", "wild-wales", "llangollen", "Chapter VI", "第 6 章",
      prose(648, "Llangollen is a small town or large village", "on the southern side of the Dee."), ["Llangollen", "Dee"], 648),
    L("wwa-2", "wild-wales", "snowdon", "Chapter XXIX", "第 29 章",
      prose(648, "Snowdon or Eryri is no single hill", "the highest point of Southern Britain."), ["Snowdon", "Y Wyddfa"], 648),
    L("ld-1", "lorna-doone", "doone-valley", "Chapter VII", "第 7 章",
      prose(17460, "For Bagworthy water ran out of Doone valley", "from the mouth of it."), ["Bagworthy water", "Doone valley"], 17460),
]

if __name__ == "__main__":
    append(f"{APP}/data/books.js", books, "11-03 晚 第二批：补到 Week 1 目标")
    append(f"{APP}/data/places.js", places, "11-03 晚 第二批")
    append(f"{APP}/data/lines.js", lines, "11-03 晚 第二批（均从古登堡原文摘录）")
    print(len(books), "books,", len(places), "places,", len(lines), "excerpts")
    for l in lines:
        print(f"{l['id']:8}", l["text_en"].replace("\n", " / ")[:150])
