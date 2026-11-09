"""Agatha Christie: excerpts from two early books (published 1922 and 1924, on Project Gutenberg), three
pilgrimage places, and scene notes (own words) for three later books still in copyright.
Usage: python3 -I add_christie.py <app_dir> <texts_dir> <coords_json>"""
import importlib.util
import json
import sys

APP, TX, CJ = sys.argv[1], sys.argv[2], sys.argv[3]
spec = importlib.util.spec_from_file_location("b2", __file__.replace("add_christie.py", "add_batch2.py"))
b2 = importlib.util.module_from_spec(spec)
_argv, sys.argv = sys.argv, [sys.argv[0], APP, TX]
spec.loader.exec_module(b2)
sys.argv = _argv
prose, append, L = b2.prose, b2.append, b2.L
coords = {c["id"]: c for c in json.load(open(CJ))}
G = "https://www.gutenberg.org/ebooks/"
CHRISTIE = ["secret-adversary", "poirot-investigates", "and-then-there-were-none", "dead-mans-folly", "four-fifty-from-paddington"]

def B(id, title, title_zh, year, pg=None):
    # Christie died in 1976: in copyright in the UK until the end of 2046 (spec R-4); the 1920s books are
    # public domain in the US, which is why Project Gutenberg has them
    return dict(id=id, title=title, title_zh=title_zh, author="Agatha Christie", author_zh="阿加莎·克里斯蒂", year=year,
                orig_lang="en", public_domain=False, source_url=G + str(pg) if pg else None)

books = [
    B("secret-adversary", "The Secret Adversary", "秘密对手", "1922", 1155),
    B("poirot-investigates", "Poirot Investigates", "首相绑架案", "1924", 61262),
    B("and-then-there-were-none", "And Then There Were None", "无人生还", "1939"),
    B("dead-mans-folly", "Dead Man's Folly", "古屋疑云", "1956"),
    B("four-fifty-from-paddington", "4.50 from Paddington", "命案目睹记", "1957"),
]

def place(id, name, name_zh, **kw):
    c = coords[id]
    assert c["lat"] is not None, id
    d = dict(id=id, name=name, name_zh=name_zh, lat=round(c["lat"], 4), lon=round(c["lon"], 4), place_type=kw.pop("type", "original"))
    d.update(kw)
    d["coord_checked"] = f'{c["source_title"]} — {c["source_url"]}, 2026-11-03'
    return d

places = [
    place("dover-street", "Dover Street, Mayfair", "梅费尔 · 多佛街"),
    place("piccadilly-circus", "Piccadilly Circus", "皮卡迪利广场"),
    place("soho", "Soho", "苏豪区"),
    place("holyhead", "Holyhead", "霍利黑德", city=True),
    place("torquay", "Torquay", "托基", type="pilgrimage", city=True,
          note="阿加莎·克里斯蒂 1890 年生于托基，在家族宅子 Ashfield 长大", note_en="Agatha Christie was born in Torquay in 1890 and grew up at the family home, Ashfield",
          book_ids=CHRISTIE),
    place("greenway", "Greenway", "格林威庄园", type="pilgrimage",
          note="克里斯蒂 1938 年起在达特河畔的度假屋，现属英国国民信托", note_en="Christie's holiday home on the River Dart from 1938, now owned by the National Trust",
          book_ids=CHRISTIE),
    place("cholsey-church", "St Mary's Church, Cholsey", "乔尔西 · 圣玛丽教堂", type="pilgrimage",
          note="克里斯蒂安葬在这座教堂的墓地，离她在沃灵福德的家不远", note_en="Christie is buried in the churchyard here, near her home at Winterbrook, Wallingford",
          book_ids=CHRISTIE),
    place("burgh-island", "Burgh Island", "伯格岛", type="prototype",
          prototype_of="常被认为是《无人生还》里士兵岛的原型；克里斯蒂曾住岛上的酒店", prototype_of_en="Usually named as the model for Soldier Island in And Then There Were None; Christie stayed at its hotel"),
]

def S(id, book, pid, loc, loc_zh, en, zh, hl_en, hl_zh):
    for h in hl_en: assert h in en, (id, h)
    for h in hl_zh: assert h in zh, (id, h)
    return dict(id=id, kind="scene", book_id=book, place_ids=[pid], location=loc, location_zh=loc_zh,
                text_en=en, text_zh=zh, highlight_en=hl_en, highlight_zh=hl_zh, status="draft")

lines = [
    L("sa-1", "secret-adversary", "dover-street", "Chapter I", "第 1 章",
      "\n".join([prose(1155, "\"TOMMY, old thing!\"", "old thing!\"").replace("TOMMY", "Tommy", 1), prose(1155, "\"Tuppence, old bean!\"", "old bean!\""),
                 prose(1155, "The two young people greeted each other affectionately", "the Dover Street Tube exit in doing so.")]),
      ["Dover Street Tube"], 1155),
    L("sa-2", "secret-adversary", "piccadilly-circus", "Chapter III", "第 3 章",
      prose(1155, "\"All in good time. What an awful place Piccadilly Circus is.", "if they killed the five-pound notes!\""), ["Piccadilly Circus"], 1155),
    L("sa-3", "secret-adversary", "soho", "Chapter VII", "第 7 章",
      prose(1155, "Then he walked up Shaftesbury Avenue", "the maze of mean streets round Soho."), ["Shaftesbury Avenue", "Soho"], 1155),
    L("sa-4", "secret-adversary", "holyhead", "Chapter XX", "第 20 章",
      prose(1155, "However, Tommy had plenty of time to cool down before they reached Holyhead", "as they alighted at their destination."), ["Holyhead"], 1155),
    L("pi-1", "poirot-investigates", "brighton", "Jewel Robbery at the Grand Metropolitan", "《大都会饭店珠宝劫案》",
      prose(61262, "Saturday evening saw us dining at the Grand Metropolitan", "seemed to be at Brighton."), ["Grand Metropolitan", "Brighton"], 61262),
    L("pi-2", "poirot-investigates", "dover", "The Kidnapped Prime Minister", "《首相绑架案》",
      prose(61262, "On arriving at Dover Poirot's behaviour", "clutched desperately at my arm."), ["Dover"], 61262),
    S("tn-s1", "and-then-there-were-none", "burgh-island", "Chapters 1–2", "第 1–2 章",
      "Ten strangers, each lured by a letter from an unknown host, are taken by boat to Soldier Island off the Devon coast and left there; one by one, they begin to die.",
      "十个素不相识的人各自收到一位陌生主人的来信，被小船送上德文郡海边的士兵岛，随后被困在岛上，一个接一个地死去。",
      ["Soldier Island"], ["士兵岛"]),
    S("dmf-s1", "dead-mans-folly", "greenway", "Nasse House", "纳斯庄园",
      "Poirot is called to Nasse House in Devon, where a murder hunt staged as a game at the fête turns into a real murder; the house and its boathouse are modelled on Christie's own Greenway.",
      "波洛被请到德文郡的纳斯庄园，游园会上作为游戏安排的“寻找凶手”变成了真正的命案；纳斯庄园和它的船屋就是照着克里斯蒂自己的格林威写的。",
      ["Nasse House", "Greenway"], ["纳斯庄园", "格林威"]),
    S("fp-s1", "four-fifty-from-paddington", "paddington-station", "Chapter 1", "第 1 章",
      "On the 4.50 from Paddington, Mrs McGillicuddy looks out as another train runs alongside, and sees a man strangling a woman in one of its carriages.",
      "麦克吉利克迪太太坐上 4 点 50 分从帕丁顿开出的火车，一列火车并行驶过时，她看见对面车厢里一个男人正在掐死一个女人。",
      ["4.50 from Paddington"], ["帕丁顿"]),
]

if __name__ == "__main__":
    append(f"{APP}/data/books.js", books, "11-03 夜 阿加莎·克里斯蒂（英国 2046 年底前受版权保护；1920 年代的书在美国已进入公有领域）")
    append(f"{APP}/data/places.js", places, "11-03 夜 阿加莎·克里斯蒂（坐标均有出处）")
    append(f"{APP}/data/lines.js", lines, "11-03 夜 阿加莎·克里斯蒂：早期作品为古登堡原文摘句，后期作品为场景说明（kind: scene）")
    print(len(books), "books,", len(places), "places,", len(lines), "entries")
    for l in lines:
        print(f"{l['id']:7}", l["text_en"].replace("\n", " / ")[:140])
