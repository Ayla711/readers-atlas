"""Download the candidate thumbnails listed in urls.tsv (960 px thumb first, then the original). Usage: python3 -I dl_here.py <work_dir>"""
import csv, os, re, sys, time, urllib.request, urllib.error
W = sys.argv[1]; os.makedirs(f"{W}/dl", exist_ok=True)
UA = "ReadersAtlasPrototype/0.1 (educational, low volume)"
def get(u):
    with urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": UA}), timeout=60) as r:
        return r.read()
for p, n, u in csv.reader(open(f"{W}/urls.tsv"), delimiter="\t"):
    f = f"{W}/dl/{p}__{n}.jpg"
    if os.path.exists(f) and os.path.getsize(f) > 2000:
        continue
    m = re.match(r"https://upload\.wikimedia\.org/wikipedia/commons/(\w)/(\w\w)/(.+)$", u)
    tries = [f"https://upload.wikimedia.org/wikipedia/commons/thumb/{m.group(1)}/{m.group(2)}/{m.group(3)}/960px-{m.group(3)}", u] if m else [u]
    for t in tries:
        ok = False
        for i in range(4):
            try:
                open(f, "wb").write(get(t)); ok = True; break
            except urllib.error.HTTPError as e:
                if e.code in (400, 404): break
                print(f, e.code, flush=True); time.sleep(8 * (i + 1))
            except Exception as e:
                print(f, e, flush=True); time.sleep(5)
        if ok: break
    print(os.path.basename(f), os.path.getsize(f) if os.path.exists(f) else 0, flush=True)
    time.sleep(3)
