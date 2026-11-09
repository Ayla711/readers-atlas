"""Batch 3 (11-03 night): bring every region to at least 5 excerpts.
Reuses the extraction helpers from add_batch2 (excerpts are cut from the Gutenberg files, never typed).
Coordinates come from coords/new13.json (sourced, see coord_checked).
Usage: python3 -I add_batch3.py <app_dir> <texts_dir> <coords_json>"""
import json
import sys

sys.argv = sys.argv[:3] + sys.argv[4:] if len(sys.argv) > 4 else sys.argv
APP, TX, CJ = sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None
import importlib.util
spec = importlib.util.spec_from_file_location("b2", __file__.replace("add_batch3.py", "add_batch2.py"))
b2 = importlib.util.module_from_spec(spec)
sys_argv = sys.argv
sys.argv = [sys_argv[0], APP, TX]
spec.loader.exec_module(b2)      # defines helpers; its __main__ block does not run
sys.argv = sys_argv
prose, verse, GAP, append, B, L = b2.prose, b2.verse, b2.GAP, b2.append, b2.B, b2.L

coords = {c["id"]: c for c in json.load(open(CJ))}

def place(id, name, name_zh, **kw):
    c = coords[id]
    assert c["lat"] is not None, id
    d = dict(id=id, name=name, name_zh=name_zh, lat=round(c["lat"], 4), lon=round(c["lon"], 4), place_type=kw.pop("type", "original"))
    d.update(kw)
    d["coord_checked"] = f'{c["source_title"]} — {c["source_url"]}, 2026-11-03'
    return d

def proto(id, name, name_zh, zh, en, **kw):
    return place(id, name, name_zh, type="prototype", prototype_of=zh, prototype_of_en=en, **kw)

books = [
    B("sylvias-lovers", "Sylvia's Lovers", "西尔维娅的恋人", "Elizabeth Gaskell", "盖斯凯尔", "1863", 4537),
    B("mary-barton", "Mary Barton", "玛丽·巴顿", "Elizabeth Gaskell", "盖斯凯尔", "1848", 2153),
    B("agnes-grey", "Agnes Grey", "艾格妮丝·格雷", "Anne Brontë", "安妮·勃朗特", "1847", 767),
    B("mrs-tiggy-winkle", "The Tale of Mrs. Tiggy-Winkle", "温迪琪·温克太太的故事", "Beatrix Potter", "波特", "1905", 15137),
    B("lavengro", "Lavengro", "拉文格罗", "George Borrow", "博罗", "1851", 20198),
    B("glens-of-antrim", "Songs of the Glens of Antrim", "安特里姆山谷之歌", "Moira O'Neill", "莫伊拉·奥尼尔", "1900", 53075),
]

places = [
    place("norham-castle", "Norham Castle", "诺勒姆城堡"),
    place("housesteads", "Hadrian's Wall at Housesteads", "哈德良长城 · 豪斯斯特兹", city=False),
    place("tynemouth-priory", "Tynemouth Priory", "泰恩茅斯修道院"),
    place("corrymeela", "Corrymeela, near Ballycastle", "巴利卡斯尔 · 科里米拉"),
    place("carrickfergus-castle", "Carrickfergus Castle", "卡里克弗格斯城堡"),
    place("glenarm", "Glenarm and the Antrim coast road", "格莱纳姆 · 安特里姆海岸公路"),
    proto("whitby", "Whitby", "惠特比", "《西尔维娅的恋人》里 Monkshaven 的原型", "The model for Monkshaven in Sylvia's Lovers", city=True),
    proto("scarborough", "Scarborough", "斯卡伯勒", "常被认为是《艾格妮丝·格雷》结尾海滨小城的原型，安妮·勃朗特葬于此", "Usually taken as the seaside town at the end of Agnes Grey; Anne Brontë is buried here", city=True),
    place("little-town", "Little Town, Newlands Valley", "纽兰兹谷 · 小镇农场"),
    place("greenheys", "Greenheys, Manchester", "曼彻斯特 · 格林海斯"),
    place("great-white-horse", "The Great White Horse, Ipswich", "伊普斯威奇 · 大白马客栈"),
    place("norwich", "Norwich", "诺里奇", city=True),
    place("bala", "Bala and Llyn Tegid", "巴拉 · 泰吉德湖", city=True),
]
for p in places:
    if p.get("city") is False:
        del p["city"]

lines = [
    L("mar-3", "marmion", "norham-castle", "Canto I, stanza I", "第一章第 1 节",
      "\n".join(verse(4010, "Day set on Norham's castled steep", 3) if False else verse(4010, "DAY set on Norham's castled steep", 3)).replace("DAY set", "Day set", 1),
      ["Norham's castled steep", "Tweed", "Cheviot"], 4010),
    L("mar-4", "marmion", "tynemouth-priory", "Canto II, stanza VIII", "第二章第 8 节",
      "\n".join(verse(4010, "And now the vessel skirts the strand", 6)), ["Northumberland", "Tynemouth's priory and bay"], 4010),
    L("puck-2", "puck-of-pooks-hill", "housesteads", "On the Great Wall", "《在长城上》",
      prose(26027, "'Just when you think you are at the world's end", "And that is the Wall!'"), ["the Wall"], 26027),
    L("gl-1", "glens-of-antrim", "corrymeela", "Corrymeela", "《科里米拉》",
      "\n".join(verse(53075, "Over here in England I'm helpin' wi' the hay", 4)), ["Corrymeela"], 53075),
    L("isb-3", "irish-sketch-book", "carrickfergus-castle", "Belfast to the Causeway", "《从贝尔法斯特到巨人堤》一章",
      prose(42890, "Carrickfergus rejoices in a real romantic-looking castle", "famous as a background for a picture."), ["Carrickfergus"], 42890),
    L("isb-4", "irish-sketch-book", "glenarm", "Belfast to the Causeway", "《从贝尔法斯特到巨人堤》一章",
      prose(42890, "If the road from Larne to Glenarm is beautiful", "this noble line of coast-scenery."), ["Glenarm", "Cushendall"], 42890),
    L("syl-1", "sylvias-lovers", "whitby", "Chapter I", "第 1 章",
      prose(4537, "On the north-eastern shores of England there is a town called Monkshaven", "fifteen thousand inhabitants."), ["Monkshaven"], 4537),
    L("ag-1", "agnes-grey", "scarborough", "Chapter XXIV, The Sands", "第 24 章《沙滩》",
      prose(767, "when my foot was on the sands", "surmounted by green swelling hills,"), ["sands", "bay"], 767),
    L("tig-1", "mrs-tiggy-winkle", "little-town", "Opening", "开篇",
      prose(15137, "Once upon a time there was a little girl called Lucie", "a farm called Little-town."), ["Little-town"], 15137),
    L("mb-1", "mary-barton", "greenheys", "Chapter I", "第 1 章",
      prose(2153, "There are some fields near Manchester", "a little village about two miles distant."), ["Manchester", "Green Heys Fields"], 2153),
    L("pick-3", "pickwick-papers", "great-white-horse", "Chapter XXII", "第 22 章",
      prose(580, "stands an inn known far and wide by the appellation of the Great White Horse", "distantly resembling an insane cart-horse,"), ["Great White Horse"], 580),
    L("lav-1", "lavengro", "norwich", "Chapter XIV", "第 14 章",
      prose(20198, "A fine old city, truly, is that", "the fair and fertile valley in which it stands."), ["fine old city"], 20198),
    L("wwa-3", "wild-wales", "bala", "Chapter L", "第 50 章",
      prose(648, "three or four thousand inhabitants, situated near the northern end of an oblong valley", "are occupied by Llyn Tegid."), ["Llyn Tegid"], 648),
]

if __name__ == "__main__":
    append(f"{APP}/data/books.js", books, "11-03 夜 第三批：薄弱大区补到每区 ≥ 5 条")
    append(f"{APP}/data/places.js", places, "11-03 夜 第三批（坐标均有出处）")
    append(f"{APP}/data/lines.js", lines, "11-03 夜 第三批（均从古登堡原文摘录）")
    print(len(books), "books,", len(places), "places,", len(lines), "excerpts")
    for l in lines:
        print(f"{l['id']:8}", l["text_en"].replace("\n", " / ")[:150])
