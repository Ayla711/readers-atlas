"""Shared helpers for hand-written content batches (tools/content/batches/*.py used these through add_batch2/5).
Every excerpt is cut from a downloaded Project Gutenberg text, never typed; every place carries the source of its
coordinates. Set the paths first:

    import batchlib as b
    b.init(app_dir="…/readers_atlas", tx_dir="…/cache/pg", country="uk", date="2026-11-09")
    text = b.prose(1342, "It is a truth universally acknowledged", "in want of a wife.")
    b.append(b.data("places.js"), [b.ORIG(...)], "11-09 batch note")

Gutenberg texts: download https://www.gutenberg.org/cache/epub/<n>/pg<n>.txt to <tx_dir>/<n>.txt.
"""
import json
import re

APP = TX = COUNTRY = None
D = ""
G = "https://www.gutenberg.org/ebooks/"
W = "https://en.wikipedia.org/wiki/"

def init(app_dir, tx_dir, country="uk", date=""):
    """app_dir: the repo root; tx_dir: folder of Gutenberg texts; date: appended to coord_checked / checked"""
    global APP, TX, COUNTRY, D
    APP, TX, COUNTRY, D = app_dir, tx_dir, country, (", " + date if date else "")
    _cache.clear()

def data(name):
    """path of a data file of the current country: data("places.js") -> <app>/data/<country>/places.js"""
    return f"{APP}/data/{COUNTRY}/{name}"

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


def paras(book, *pairs):
    """adjacent paragraphs, each cut with prose(), joined with a newline (spec 6.6)"""
    return "\n".join(prose(book, a, b) for a, b in pairs)

def verse_lines(book, start, n):
    """n non-empty lines from the line containing `start`; indentation and the editor's line numbers removed"""
    raw = flat(book)[0].split("\n")
    for i, l in enumerate(raw):
        if start in norm(l):
            out = []
            for l2 in raw[i:]:
                s = re.sub(r"\s+\d+\s*$", "", norm(l2.strip())).strip()
                if s:
                    out.append(s)
                if len(out) == n:
                    return "\n".join(out)
    raise SystemExit(f"not found in {book}: {start}")

def B(id, title, title_zh, author, author_zh, year, pg, pd=True):
    return dict(id=id, title=title, title_zh=title_zh, author=author, author_zh=author_zh, year=year, orig_lang="en",
                public_domain=pd, source_url=G + str(pg))

def P(id, name, name_zh, lat, lon, st, su, type, **kw):
    d = dict(id=id, country=COUNTRY, name=name, name_zh=name_zh, lat=lat, lon=lon, place_type=type)
    d.update(kw)
    d["coord_checked"] = f"{st} — {su}{D}"
    return d

def ORIG(id, name, name_zh, lat, lon, st, su, en, zh, **kw):
    return P(id, name, name_zh, lat, lon, st, su, "original", note=zh, note_en=en, **kw)

def PROTO(id, name, name_zh, lat, lon, st, su, en, zh, **kw):
    return P(id, name, name_zh, lat, lon, st, su, "prototype", prototype_of=zh, prototype_of_en=en, **kw)

def PIL(id, name, name_zh, lat, lon, st, su, en, zh, book_ids, **kw):
    return P(id, name, name_zh, lat, lon, st, su, "pilgrimage", note=zh, book_ids=book_ids, note_en=en, **kw)

def L(id, book_id, place, loc, loc_zh, text, hl, pg):
    for h in hl:
        assert h in text, (id, h)
    return dict(id=id, book_id=book_id, place_ids=[place], location=loc, location_zh=loc_zh, text_en=text,
                highlight_en=hl, translation="original", status="draft", checked=f"Project Gutenberg #{pg}{D}")


def S(id, book_id, place, loc, loc_zh, en, zh, hl_en, hl_zh, src):
    """a scene note for a book still in copyright: no quotation, a description in both languages"""
    for h in hl_en:
        assert h in en, (id, h)
    for h in hl_zh:
        assert h in zh, (id, h)
    return dict(id=id, kind="scene", book_id=book_id, place_ids=[place], location=loc, location_zh=loc_zh, text_en=en, text_zh=zh,
                highlight_en=hl_en, highlight_zh=hl_zh, status="draft", fact_source=src)
