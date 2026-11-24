"""Patch 2 (11-24 evening): re-read thegreatestbooks rank (D) and Goodreads count (E) for EVERY row in the 20 specs, same day, same method.
D: verify/tgb_top2000_subset_1124.txt (overall top 2000 read page by page). E: verify/gr_all_1124.txt (Goodreads autocomplete).
Row order must match verify/allrows_1124.json made from the specs before this patch (au nz eg za ng dz ma ke fi hu is tr ua ro nl be ch dk no se).
Run in tools/selection after p1_verify.py: python3 -I verify/p2_all.py"""
import sys, os, re, json, unicodedata
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import specio
f = lambda s: ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn').lower()
nz = lambda s: re.sub(r'[^a-z0-9]', '', f(s))
gr = {}
for line in open(os.path.join(HERE, 'gr_all_1124.txt'), encoding='utf-8'):
    if line.startswith('#'): continue
    i, n, t, a = line.rstrip('\n').split('|', 3); k = int(i.lstrip('M'))
    if i.startswith('M') or k not in gr: gr[k] = None if n == '-' else int(n)
tgb = []
for line in open(os.path.join(HERE, 'tgb_top2000_subset_1124.txt'), encoding='utf-8'):
    if line.startswith('#'): continue
    r, t, a = line.rstrip('\n').split('|'); tgb.append((int(r), t, a))
ALIAS = {'Belle du Seigneur': 'Her Lover', 'Fatelessness': 'Fateless or Fatelessness', 'Anna Édes': 'Édes Anna', 'Kalevala': 'The Kalevala',
         'Gysbreght van Aemstel': 'Gijsbrecht Van Aemstel', 'Fantasia: An Algerian Cavalcade': 'Fantasia', 'Children of the Alley': 'Children of Gebelawi',
         'Fairy Tales': 'Fairy Tales and Stories', 'Njáls saga': "Njal's Saga", 'The House with the Blind Glass Windows': 'House with the Blind Glass Windows',
         'Tevye the Dairyman': 'Tevye The Dairyman And The Railroad Stories', 'The Garden Party, and Other Stories': 'The Garden Party And Other Stories',
         'The Interesting Narrative': 'The Interesting Narrative of the Life of Olaudah Equiano', 'Journey to the Centre of the Earth': 'Journey to the Center of the Earth'}
FIX_D = {'The Palm-Wine Drinkard': 833, 'Out of Africa': 459}   # author spelled "Amos Tutola" / "Isak Dinesen" on the site
def surname(a):
    a = a.split('&')[0].split(',')[0].strip(); return '' if a in ('', 'Anonymous') else a.split()[-1]
def drank(title, sur):
    if title in FIX_D: return FIX_D[title]
    q = nz(ALIAS.get(title, re.sub(r'\s*\(.*?\)', '', title)))
    for r, t, a in tgb:
        if nz(t) == q and (not sur or f(sur) in f(a) or sur == 'Hippo'): return r
    return None
et = lambda n: 0 if n is None else 3 if n >= 1e6 else 2 if n >= 1e5 else 1 if n >= 1e4 else 0
dt = lambda r: 0 if r is None else 2 if r <= 500 else 1
idx = 0; changed = []
for cc in 'au nz eg za ng dz ma ke fi hu is tr ua ro nl be ch dk no se'.split():
    S = specio.load(cc)
    for j, row in enumerate(S['rows']):
        t, a, k, p, d, n = row
        if idx >= 398: break   # rows added by p1 (new canon candidates) already carry their own D/E
        g = gr.get(idx); r = drank(t, surname(a))
        q = {kk: vv for kk, vv in p.items() if kk not in ('D', 'E')}
        if dt(r): q['D'] = dt(r)
        if et(g): q['E'] = et(g)
        if q != p: changed.append((cc, t, p, q))
        if 'Goodreads' not in n:
            ev = ('D %d' % r if r else '不在 D 前 2000') + ' · ' + ('Goodreads %s' % format(g, ',') if g is not None else 'Goodreads 查不到')
            n = (n + '；' if n else '') + ev
        S['rows'][j] = (t, a, k, q, d, n); idx += 1
    specio.save(cc, S)
for c in changed: print(*c, sep=' | ')
print(len(changed), 'rows changed; rows read', idx)
