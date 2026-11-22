"""Wikisource texts for content batches (11-22, while Project Gutenberg was down for maintenance).
fetch() saves a rendered page (https://<lang>.wikisource.org/wiki/<title>) as <dir>/<title>.html, "/" written "__";
text() reads the page's own text out of it:

- only the article body (mw-parser-output) is read; navigation, headers and footers are not;
- ruby readings (<rt>, <rp>), footnote marks (<sup class="reference">), page numbers and edit links are dropped;
- tables of contents, style and script are dropped;
- block ends (p, div, br, li, table rows, headings, dd) become line ends.

Nothing inside the text is changed. cut() takes a passage from one line; if an edition prints its own glosses in the
running text (〔…〕, （＊ママ）), the batch names each one it drops and cut() checks that it was there.

Wikimedia limits the rate of requests: fetch() waits between pages and backs off on HTTP 429.

    python3 -I wikisource.py <dir> <lang> <title> [<title> …]     # download
"""
import html, os, re, sys, time, urllib.parse, urllib.request
from html.parser import HTMLParser

UA = {"User-Agent": "ReadersAtlas/1.0 (course project; github.com/Ayla711/readers-atlas)"}

def url(lang, title):
    return f"https://{lang}.wikisource.org/wiki/" + urllib.parse.quote(title.replace(" ", "_"), safe="/:()'")

def _file(d, title):
    return os.path.join(d, title.replace("/", "__") + ".html")

def fetch(d, lang, title, wait=3):
    for k in range(6):
        try:
            s = urllib.request.urlopen(urllib.request.Request(url(lang, title), headers=UA), timeout=60).read().decode("utf-8")
            break
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(8 * (k + 1))
                continue
            raise
    else:
        raise SystemExit(f"rate limited: {title}")
    open(_file(d, title), "w", encoding="utf-8").write(s)
    time.sleep(wait)

BLOCK = {"p", "div", "br", "li", "tr", "h1", "h2", "h3", "h4", "h5", "h6", "dd", "dt", "table", "blockquote", "center"}
SKIP_TAGS = {"rt", "rp", "style", "script", "noscript"}
VOID = {"br", "img", "hr", "meta", "link", "input", "wbr", "source", "col", "area", "param", "track", "embed", "base"}
SKIP_CLASSES = ("reference", "pagenum", "ws-pagenum", "mw-editsection", "toc", "ws-noexport", "noprint", "mw-cite-backlink",
                "references", "reflist", "navbox", "ws-summary")

class _Text(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self.stack, self.skip, self.inside = [], [], 0, 0
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = a.get("class") or ""
        if tag == "div" and "mw-parser-output" in cls.split():
            self.inside += 1
            self.stack.append((tag, "body"))
            return
        drop = tag in SKIP_TAGS or any(c in cls.split() for c in SKIP_CLASSES) or a.get("id") == "toc"
        if tag in VOID:
            if tag == "br" and self.inside and not self.skip:
                self.out.append("\n")
            return
        self.stack.append((tag, "skip" if drop else ""))
        if drop:
            self.skip += 1
    def handle_endtag(self, tag):
        if tag in VOID or not any(t == tag for t, _ in self.stack):
            return
        while self.stack:
            t, kind = self.stack.pop()
            if kind == "skip":
                self.skip -= 1
            if kind == "body":
                self.inside -= 1
            if t in BLOCK and self.inside and not self.skip:
                self.out.append("\n")
            if t == tag:
                break
    def handle_data(self, data):
        if self.inside and not self.skip:
            self.out.append(data)

_texts = {}
def text(d, title):
    if title not in _texts:
        p = _Text()
        p.feed(open(_file(d, title), encoding="utf-8").read())
        t = "".join(p.out).replace("\r", "")
        t = "\n".join(l.strip(" \t") for l in t.split("\n"))
        _texts[title] = re.sub(r"\n{2,}", "\n", t)
    return _texts[title]

def cut(d, title, start, end, drop=(), after=None):
    """the exact text from `start` to the end of `end`, inside one line; each string in `drop` (an edition's own gloss
    printed in the running text) must be inside the passage, and is taken out"""
    t = text(d, title)
    i = t.find(start, t.find(after) if after else 0)
    assert i >= 0, (title, start)
    j = t.find(end, i)
    assert j >= 0, (title, start, end)
    s = t[i:j + len(end)]
    assert "\n" not in s, (title, start, "crosses a line: cut it in two")
    for g in drop:
        assert g in s, (title, start, g)
        s = s.replace(g, "")
    return s

def block(d, title, start, end, drop=(), number=None, after=None):
    """the exact text from `start` to the end of `end` across lines (verse, an exchange of poems); each line's leading
    indent is taken off, and an editor's poem number at the head of a line (number=r"\\d{4}　") too"""
    t = text(d, title)
    i = t.find(start, t.find(after) if after else 0)
    assert i >= 0, (title, start)
    j = t.find(end, i)
    assert j >= 0, (title, start, end)
    s = t[i:j + len(end)]
    for g in drop:
        assert g in s, (title, start, g)
        s = s.replace(g, "")
    out = []
    for l in s.split("\n"):
        l = l.lstrip(" 　\t")
        if number:
            l = re.sub("^" + number, "", l)
        out.append(l)
    return "\n".join(out)

if __name__ == "__main__":
    d, lang = sys.argv[1], sys.argv[2]
    os.makedirs(d, exist_ok=True)
    for title in sys.argv[3:]:
        fetch(d, lang, title)
        print(title, len(text(d, title)), "chars")
