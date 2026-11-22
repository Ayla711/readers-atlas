"""Small edits to the data files, which keep one entry per line (11-22)."""
import json
import re

def drop_entries(path, ids):
    """remove whole one-line entries by id; every id must be found"""
    rows = open(path, encoding="utf-8").read().split("\n")
    out, gone = [], set()
    for r in rows:
        m = re.match(r'  \{ id: "([^"]+)"', r)
        if m and m.group(1) in ids:
            gone.add(m.group(1))
            continue
        out.append(r)
    assert gone == set(ids), set(ids) - gone
    s = "\n".join(out)
    s = re.sub(r",(\s*\n\];)", r"\1", s)                                  # the entry now last carries no comma
    s = re.sub(r"\n  // —— [^\n]* ——\n(?=\];|  // ——)", "\n", s)         # a batch marker left with nothing under it
    open(path, "w", encoding="utf-8").write(s)

def set_source(path, book_id, url):
    """fill a book's source_url, which must be null"""
    s = open(path, encoding="utf-8").read()
    pat = re.compile(r'(  \{ id: "' + re.escape(book_id) + r'",[^\n]*?source_url: )null')
    s, k = pat.subn(lambda m: m.group(1) + json.dumps(url, ensure_ascii=False), s)
    assert k == 1, book_id
    open(path, "w", encoding="utf-8").write(s)

def ids(path):
    return set(re.findall(r'  \{ id: "([^"]+)"', open(path, encoding="utf-8").read()))
