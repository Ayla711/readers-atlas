"""Find freely licensed photo candidates on Wikimedia Commons for pilgrimage and film places.
Uses the ordinary search and file pages (the API is rate-limited for this connection), slowly.
Writes photos/candidates.json and photos/thumbs/<place>__<n>.jpg.
Usage: python3 -I photo_candidates.py <work_dir> [place_id ...]"""
import html
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

WORK = sys.argv[1]
ONLY = set(sys.argv[2:])
UA = "ReadersAtlasPrototype/0.1 (https://claude.ai/code; educational literary atlas prototype, low volume)"
QUERIES = {
    "poets-corner": "Poets' Corner Westminster Abbey",
    "shakespeare-birthplace": "Shakespeare's Birthplace Henley Street",
    "dove-cottage": "Dove Cottage Grasmere",
    "keats-house": "Keats House Hampstead",
    "chawton": "Jane Austen's House Chawton",
    "bronte-parsonage": "Bronte Parsonage Museum Haworth",
    "dickens-museum": "Charles Dickens Museum Doughty Street",
    "sherlock-museum": "Sherlock Holmes Museum",
    "xu-zhimo-stone": "Xu Zhimo stone King's College",
    "lao-she-plaque": "Lao She plaque St James's Gardens",
    "torquay": "Torquay harbour",
    "greenway": "Greenway House Devon",
    "cholsey-church": "St Mary's Church Cholsey",
    "st-martins-theatre": "St Martin's Theatre West Street",
    "cuckmere-cottages": "Coastguard Cottages Cuckmere Haven",
    "leadenhall-market": "Leadenhall Market",
    "christ-church": "Christ Church Oxford Great Hall staircase",
    "alnwick-castle": "Alnwick Castle",
    "glenfinnan": "Glenfinnan Viaduct",
    "dyrham-park": "Dyrham Park house",
    "chalcot-crescent": "Chalcot Crescent",
    "doune-castle": "Doune Castle",
}
OK_LICENSE = re.compile(r"^(CC BY(-SA)? [0-9.]+( [a-z]+)?|CC0|Public domain|PD|Attribution|CC BY(-SA)?)", re.I)

def get(url, binary=False, tries=3):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=40) as r:
                data = r.read()
            time.sleep(1.2)
            return data if binary else data.decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(25); continue
            if e.code == 404:
                return None
            time.sleep(3)
        except Exception:
            time.sleep(3)
    return None

def text(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s or ""))).strip()

def file_info(title):
    page = get("https://commons.wikimedia.org/wiki/" + urllib.parse.quote(title.replace(" ", "_")))
    if not page:
        return None
    page = page.replace("&#95;", "_")
    lic = re.search(r'class="licensetpl_short"[^>]*>(.*?)</span>', page, re.S)
    lic_url = re.search(r'class="licensetpl_link"[^>]*>(.*?)</span>', page, re.S)
    aut = re.search(r'id="fileinfotpl_aut"[^>]*>.*?</td>\s*<td[^>]*>(.*?)</td>', page, re.S)
    orig = re.search(r'<div class="fullImageLink"[^>]*>\s*<a href="(https://upload\.wikimedia\.org/[^"]+)"', page)
    dims = re.search(r'([\d,]+) × ([\d,]+) pixels', page)
    desc = re.search(r'class="description[^"]*"[^>]*>(.*?)</div>', page, re.S)
    return {
        "title": title,
        "page": "https://commons.wikimedia.org/wiki/" + urllib.parse.quote(title.replace(" ", "_")),
        "license": text(lic.group(1)) if lic else "",
        "license_url": text(lic_url.group(1)) if lic_url else "",
        "author": text(aut.group(1))[:120] if aut else "",
        "original": orig.group(1).split("?")[0] if orig else "",
        "w": int(dims.group(1).replace(",", "")) if dims else 0,
        "h": int(dims.group(2).replace(",", "")) if dims else 0,
        "desc": text(desc.group(1))[:160] if desc else "",
    }

def thumb_url(orig, width=960):
    m = re.match(r"https://upload\.wikimedia\.org/wikipedia/commons/(\w)/(\w\w)/(.+)$", orig)
    if not m:
        return None
    a, ab, name = m.groups()
    return f"https://upload.wikimedia.org/wikipedia/commons/thumb/{a}/{ab}/{name}/{width}px-{name}"

def main():
    os.makedirs(f"{WORK}/thumbs", exist_ok=True)
    out_path = f"{WORK}/candidates.json"
    out = json.load(open(out_path)) if os.path.exists(out_path) else {}
    for pid, q in QUERIES.items():
        if (ONLY and pid not in ONLY) or (not ONLY and pid in out):
            continue
        res = get("https://commons.wikimedia.org/w/index.php?" + urllib.parse.urlencode(
            {"search": q, "title": "Special:Search", "ns6": 1, "fulltext": 1, "limit": 14}))
        titles = []
        for t in re.findall(r'data-serp-pos="\d+"[^>]*title="(File:[^"]+)"|<a href="/wiki/(File:[^"]+)" title="File:[^"]+"', res or ""):
            t = t[0] or urllib.parse.unquote(t[1]).replace("_", " ")
            t = html.unescape(t)
            if t not in titles and re.search(r"\.(jpe?g|png)$", t, re.I):
                titles.append(t)
        cands = []
        for t in titles[:9]:
            info = file_info(t)
            if not info or not OK_LICENSE.search(info["license"]) or re.search(r"\bNC\b|\bND\b", info["license"]):
                continue
            if info["w"] and info["w"] < 900:
                continue
            tu = thumb_url(info["original"], 960 if info["w"] >= 960 else info["w"])
            data = get(tu, binary=True) if tu else None
            if not data:
                continue
            fn = f"{WORK}/thumbs/{pid}__{len(cands)}.jpg"
            open(fn, "wb").write(data)
            info["thumb"] = fn
            cands.append(info)
            if len(cands) == 4:
                break
        out[pid] = {"query": q, "candidates": cands}
        json.dump(out, open(out_path, "w"), ensure_ascii=False, indent=1)
        print(pid, len(titles), "found,", len(cands), "usable", flush=True)

main()
