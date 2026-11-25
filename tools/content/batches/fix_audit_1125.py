"""11-25 audit fixes. Each change is made once in the batch script and once in the data (or tool), so the two stay
the same.
- Robben Island (flagged offshore_island) sits 8.3 km off the simplified South African outline: validate.js now
  lets a flagged island sit up to 10 km off (was 6).
- The Secret Adversary, Poirot Investigates, The Waste Land and Winnie-the-Pooh (1922-1926, quoted from Project
  Gutenberg) are marked public_domain: true, going by US public domain.
- Lincoln Cathedral, the real-life setting of Anya Seton's Katherine, was not linked to the book: book_ids added.
Usage: python3 -I fix_audit_1125.py <app_dir>"""
import os, sys
APP = sys.argv[1]
B = "tools/content/batches/"
T = {
 "tools/validate.js": [
  ("are flagged in the data and may sit up to 6 km off", "are flagged in the data and may sit up to 10 km off"),
  ("const limit = p.offshore_island ? 6 :", "const limit = p.offshore_island ? 10 :"),
 ],
 B + "add_ca1.py": [("4 km for rough_coast, 6 km for offshore_island", "4 km for rough_coast, 10 km for offshore_island (6 before 11-25)")],
 B + "add_christie.py": [
  ("is why Project Gutenberg has them\n", "is why Project Gutenberg has them; from 11-25 those two are marked public domain (US)\n"),
  ('orig_lang="en", public_domain=False, source_url=G + str(pg) if pg else None)',
   'orig_lang="en", public_domain=id in ("secret-adversary", "poirot-investigates"),\n                source_url=G + str(pg) if pg else None)'),
 ],
 B + "add_batch5.py": [('"1922", 1321, pd=False),', '"1922", 1321),')],
 B + "add_batch11.py": [
  ("The Waste Land and marked public_domain: false;", "The Waste Land (marked public_domain: false at first, true from 11-25);"),
  ('"1926", 67098, pd=False),', '"1926", 67098),'),
 ],
 B + "add_batch18.py": [
  ('她和女儿琼·博福特合葬在这里，墓在天使唱诗堂的南侧"),', '她和女儿琼·博福特合葬在这里，墓在天使唱诗堂的南侧",\n          book_ids=["katherine-seton"]),'),
 ],
 "data/uk/places.js": [
  ('on the south side of the Angel Choir", coord_checked', 'on the south side of the Angel Choir", book_ids: ["katherine-seton"], coord_checked'),
 ],
}
for bid in ["secret-adversary", "poirot-investigates", "the-waste-land", "winnie-the-pooh"]:
    T.setdefault("data/uk/books.js", []).append(("BOOK:" + bid, None))

for rel, pairs in T.items():
    path = os.path.join(APP, rel)
    s = open(path, encoding="utf-8").read()
    for old, new in pairs:
        if old.startswith("BOOK:"):
            bid = old[5:]
            rows = s.split("\n")
            hit = [i for i, r in enumerate(rows) if r.startswith('  { id: "%s",' % bid)]
            assert len(hit) == 1 and rows[hit[0]].count("public_domain: false") == 1, bid
            rows[hit[0]] = rows[hit[0]].replace("public_domain: false", "public_domain: true")
            s = "\n".join(rows)
            continue
        assert s.count(old) == 1, (rel, old[:60], s.count(old))
        s = s.replace(old, new)
    tmp = path + ".new"
    open(tmp, "w", encoding="utf-8").write(s)
    os.replace(tmp, path)
    print("ok", rel)
