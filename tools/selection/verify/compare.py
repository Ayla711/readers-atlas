import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json, re, unicodedata, specio
L = json.load(open('verify/allrows_1124.json'))
gr = {}
for line in open('verify/gr_all_1124.txt'):
    if line.startswith('#'): continue
    i, n, t, a = line.rstrip('\n').split('|', 3)
    k = int(i.lstrip('M'))
    if i.startswith('M') or k not in gr: gr[k] = None if n == '-' else int(n)
f = lambda s: ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn').lower()
nz = lambda s: re.sub(r'[^a-z0-9]', '', f(s))
tgb = []
for line in open('verify/tgb_top2000_subset_1124.txt'):
    if line.startswith('#'): continue
    r, t, a = line.rstrip('\n').split('|'); tgb.append((int(r), t, a))
ALIAS = {'Belle du Seigneur': 'Her Lover', 'Fatelessness': 'Fateless or Fatelessness', 'Anna Édes': 'Édes Anna', 'Kalevala': 'The Kalevala',
         'Gysbreght van Aemstel': 'Gijsbrecht Van Aemstel', 'Fantasia: An Algerian Cavalcade': 'Fantasia', 'Children of the Alley': 'Children of Gebelawi',
         'Fairy Tales': 'Fairy Tales and Stories', 'Cheese': 'Cheese', 'Of Reynaert the Fox': 'Reynard the Fox', 'Njáls saga': "Njal's Saga",
         'The House with the Blind Glass Windows': 'House with the Blind Glass Windows', 'Tevye the Dairyman': 'Tevye The Dairyman And The Railroad Stories',
         'The Garden Party, and Other Stories': 'The Garden Party And Other Stories', 'The Interesting Narrative': 'The Interesting Narrative of the Life of Olaudah Equiano',
         'Journey to the Centre of the Earth': 'Journey to the Center of the Earth', 'Poems': 'Poems'}
def drank(title, sur):
    q = nz(ALIAS.get(title, re.sub(r'\s*\(.*?\)', '', title)))
    for r, t, a in tgb:
        if nz(t) == q and (not sur or f(sur) in f(a) or sur in ('', 'Hippo')): return r
    return None
def etier(n): return 0 if n is None else 3 if n >= 1e6 else 2 if n >= 1e5 else 1 if n >= 1e4 else 0
def dtier(r): return 0 if r is None else 2 if r <= 500 else 1
out = []
idx = 0
for cc in 'au nz eg za ng dz ma ke fi hu is tr ua ro nl be ch dk no se'.split():
    S = specio.load(cc)
    for row in S['rows']:
        t, a, k, p, d, n = row
        sur = L[idx][4]
        g = gr.get(idx); r = drank(t, sur)
        e_new, d_new = etier(g), dtier(r)
        if p.get('E', 0) != e_new or p.get('D', 0) != d_new:
            out.append((cc, t, p.get('D', 0), d_new, r, p.get('E', 0), e_new, g))
        idx += 1
for o in out: print('%s | %s | D %s->%s (%s) | E %s->%s (%s)' % o)
print(len(out))
