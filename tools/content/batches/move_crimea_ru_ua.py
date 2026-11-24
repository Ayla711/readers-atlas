"""Move the two Yalta places (and their lines) from data/ru to data/ua: Crimea is drawn as Ukraine (decision A-22).
Usage: python3 -I move.py <app_dir>"""
import os, sys
APP = sys.argv[1]
MOVE_P = ['{ id: "ru-white-dacha", ', '{ id: "ru-yalta-embankment", ']
MOVE_L = ['{ id: "co-s1", ', '{ id: "lwd-1", ']
def split(path, keys):
    keep, moved = [], []
    for ln in open(path, encoding="utf-8").read().split("\n"):
        (moved if any(ln.lstrip().startswith(k) for k in keys) else keep).append(ln)
    assert len(moved) == len(keys), (path, len(moved))
    return keep, moved
def put(path, text):
    open(path + ".new", "w", encoding="utf-8").write(text); os.replace(path + ".new", path)
def append(path, entries):
    t = open(path, encoding="utf-8").read()
    assert t.endswith("\n];\n"), path
    t = t[:-len("\n];\n")] + ",\n" + ",\n".join(e.rstrip(",") for e in entries) + "\n];\n"
    put(path, t)
def fix_commas(lines):
    # the entry before "];" must not end with a comma left over from a removed entry
    t = "\n".join(lines)
    return t.replace(",\n];", "\n];")
for kind, keys in (("places", MOVE_P), ("lines", MOVE_L)):
    keep, moved = split(os.path.join(APP, "data/ru", kind + ".js"), keys)
    if kind == "places":
        moved = [m.replace('country: "ru"', 'country: "ua"', 1) for m in moved]
        assert all('country: "ua"' in m for m in moved)
    put(os.path.join(APP, "data/ru", kind + ".js"), fix_commas(keep))
    append(os.path.join(APP, "data/ua", kind + ".js"), moved)
print("moved", MOVE_P, MOVE_L)
