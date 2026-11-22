"""Aozora Bunko texts for content batches (11-22). Gutenberg was down for maintenance, and Japanese originals live on
Aozora Bunko anyway. fetch() downloads a work by its number and writes two files into <dir>: <n>.raw.txt, the file as
Aozora publishes it (Shift_JIS, decoded), and <n>.txt, a clean copy that the cuts are taken from:

- the title block, the notes on notation and the colophon (底本：…) are dropped;
- ruby readings (《…》) and their start marks (｜) are dropped;
- an editor's note number (一五［＃「一五」は行右小書き］, or ［＃行右小書き］一五［＃行右小書き終わり］) is dropped;
- a character outside JIS X 0208 (※［＃「…」、第3水準1-15-39］ or …、U+6424…) becomes that character;
- Aozora's spelled-out repetition marks (／＼, ／″＼) become the marks themselves (〱, 〲);
- any other editor note (［＃…］, layout) is dropped.

Nothing else is changed. cut() refuses a passage that still holds a ※ (an unresolved character).

    python3 -I aozora.py <dir> <work number> [<work number> …]     # download
"""
import csv, html, io, re, sys, urllib.request, zipfile

LIST = "https://www.aozora.gr.jp/index_pages/list_person_all_extended_utf8.zip"
_rows = {}

def _catalogue(d):
    if not _rows:
        try:
            z = zipfile.ZipFile(f"{d}/list.zip")
        except FileNotFoundError:
            open(f"{d}/list.zip", "wb").write(urllib.request.urlopen(LIST, timeout=60).read())
            z = zipfile.ZipFile(f"{d}/list.zip")
        for r in list(csv.reader(io.TextIOWrapper(z.open(z.namelist()[0]), encoding="utf-8-sig")))[1:]:
            _rows.setdefault(r[0].lstrip("0"), r)
    return _rows

def card(d, n):
    """the work's page on Aozora Bunko (its 図書カード)"""
    return _catalogue(d)[str(n)][13]

def _jis(m):
    note = m.group(1)
    u = re.search(r"U\+([0-9A-Fa-f]{4,5})", note)
    if u:
        return chr(int(u.group(1), 16))
    j = re.search(r"第[34]水準(\d)-(\d+)-(\d+)", note)
    if j:
        plane, row, cell = map(int, j.groups())
        bs = bytes([0xA0 + row, 0xA0 + cell]) if plane == 1 else bytes([0x8F, 0xA0 + row, 0xA0 + cell])
        return bs.decode("euc_jis_2004")
    return "※"

def clean(t):
    t = re.sub(r"※［＃([^］]*)］", _jis, t)
    t = re.sub(r"([一二三四五六七八九〇]+)［＃「\1」は行右小書き］", "", t)
    t = re.sub(r"［＃行右小書き］[一二三四五六七八九〇]+［＃行右小書き終わり］", "", t)
    t = re.sub(r"《[^》]*》", "", t)
    t = t.replace("｜", "")
    t = t.replace("／″＼", "〲").replace("／＼", "〱")
    t = re.sub(r"［＃[^］]*］", "", t)
    return t

def fetch(d, n):
    r = _catalogue(d)[str(n)]
    url = r[45]
    if not url.endswith(".zip"):
        raise SystemExit(f"Aozora #{n} has no text file of its own ({url})")
    zz = zipfile.ZipFile(io.BytesIO(urllib.request.urlopen(url, timeout=60).read()))
    raw = zz.read([x for x in zz.namelist() if x.endswith(".txt")][0]).decode("shift_jis", errors="replace").replace("\r", "")
    open(f"{d}/{n}.raw.txt", "w", encoding="utf-8").write(raw)
    parts = re.split(r"\n-{20,}\n", raw)
    t = parts[0].split("\n")[0] + "\n\n" + "\n-----\n".join(parts[2:]) if len(parts) >= 3 else raw
    t = re.split(r"\n底本：", t)[0]
    open(f"{d}/{n}.txt", "w", encoding="utf-8").write(clean(t))

_texts = {}
def text(d, n):
    if n not in _texts:
        _texts[n] = open(f"{d}/{n}.txt", encoding="utf-8").read()
    return _texts[n]

def cut(d, n, start, end, after=None):
    """the exact text from `start` to the end of `end`, inside one paragraph; `after` picks a later occurrence"""
    t = text(d, n)
    i = t.find(start, t.find(after) if after else 0)
    assert i >= 0, (n, start)
    j = t.find(end, i)
    assert j >= 0, (n, start, end)
    s = t[i:j + len(end)]
    assert "\n" not in s, (n, start, "crosses a paragraph: cut it in two")
    assert "※" not in s, (n, start, "holds an unresolved character")
    return s

if __name__ == "__main__":
    for n in sys.argv[2:]:
        fetch(sys.argv[1], n)
        print(n, card(sys.argv[1], n))
