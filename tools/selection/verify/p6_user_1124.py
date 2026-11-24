"""Patch 6 (11-24, after the user's answers): no cap on numbers; the Danish culture canon (12 works, unranked) counts as a top-10 list
(A1 = 4 for every canon work); Finland gets two more sources found in the re-check of Runeberg; the books still at zero evidence
after the re-check are marked for deletion (the user: 复核完确定 0 分的可以删掉).
Finland sources: Rasmus Bäckgren, Kaanonit kohtaavat (pro gradu, University of Helsinki 2016, core.ac.uk/download/43337077.pdf), which
reproduces (a) the 'market canon' of Juhani Niemi, Suomalaisten suosikkikirjat (cumulative print runs from publishers, 1983 and 1997),
ranked 1-16, and (b) the upper-secondary teaching canon of Juha Rikama's dissertation (teacher surveys 1980, 1990, 2000-01).
Run in tools/selection: python3 -I verify/p6_user_1124.py, then build all."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import specio
DEL = {'au':['Waltzing Matilda'],'be':['Pedigree','A Dog of Flanders'],'ch':['Reveries of the Solitary Walker','Derborence','Jürg Jenatsch','The Prisoner of Chillon','Manfred','The Final Problem','Lucerne','On the Lake','Stranger in the Village'],
 'dk':['Peder Paars','The Diary of a Parish Clerk','Tine','Letters Written in Sweden, Norway, and Denmark'],'dz':['Nuptials','Au soleil'],'is':["Grettir's Saga"],'ke':['Weep Not, Child','The Flame Trees of Thika','The Man-Eaters of Tsavo'],
 'ma':['The Travels (Rihla)','The Voices of Marrakesh','Southern Mail','Au Maroc'],'ng':['Efuru'],'no':['Terje Vigen','Garman & Worse','The Lottery Ticket',"Babette's Feast",'Letters Written in Sweden, Norway, and Denmark'],
 'ro':['Memories of My Boyhood','Solenoid','Tristia','The Carpathian Castle'],'se':['Jerusalem'],'tr':['Written After Swimming from Sestos to Abydos'],'ua':['The Fountain of Bakhchisaray'],'za':['Mhudi']}
RECHECK = {  # what the second re-check looked at, for the notes
 ('be','Pedigree'): '复核：Espace Nord 2023 目录里没有《家世》（只有西默农的另两本）',
 ('ro','Memories of My Boyhood'): '复核：2025 年 9 年级课程大纲只点作者克良格，不点书名',
 ('is',"Grettir's Saga"): '复核：冰岛课程只要求读“至少三部萨迦”，不点名',
 ('ng','Efuru'): '复核：不在非洲百部（thegreatestbooks 第 254 号书单全表）',
 ('za','Mhudi'): '复核：不在非洲百部，也不在南非 31 本书单',
 ('dk','The Diary of a Parish Clerk'): '复核：丹麦中学正典只列作家布利克，不列书名；正典里布利克的书是《维尔比牧师》',
 ('dk','Tine'): '复核：丹麦中学正典只列作家邦，不列书名；文化正典里邦的书是《路边》',
}
specs = {}
S_ = lambda cc: specs.setdefault(cc, specio.load(cc))
for cc, ts in DEL.items():
    S = S_(cc)
    for t in ts:
        row = next(r for r in S['rows'] if r[0] == t)
        n = row[5] + ('；' + RECHECK[(cc, t)] if (cc, t) in RECHECK else '')
        specio.setrow(S, t, dec='删除（零项，用户同意删）', note=n)
# Denmark: the whole canon counts as a top-10 list
S = S_('dk')
for j, (t, a, k, p, d, n) in enumerate(S['rows']):
    if p.get('A1') == 3: S['rows'][j] = (t, a, k, {**p, 'A1': 4}, d, n)
S['sources']['A1'] += '；11-24 用户定：正典只有 12 部、不分名次，整份按“前 10”算（每本 A1 记 4）'
# Finland: market canon (A2) and teaching canon (B)
S = S_('fi')
src = dict(S['sources']); keys = list(src); i = keys.index('A1') + 1
S['sources'] = {k: src[k] for k in keys[:i]} | {'A2': '芬兰“市场正典”：尼耶米《芬兰人最爱的书》按出版社报的累计印数排名（1983、1997），第 1–16 名 — 转引自赫尔辛基大学硕士论文 Bäckgren《Kaanonit kohtaavat》（2016）'} | {k: src[k] for k in keys[i:]}
S['sources']['B'] = '芬兰高中文学课全班共读书目：里卡马博士论文（2004）三次教师调查（1980、1990、2000–01）— 转引自同一篇论文；前 5 名和 2000–01 年第 11、14 名有名次'
A2 = {'The Tales of Ensign Stål': 4, 'Seven Brothers': 4, 'Kalevala': 4, 'The Unknown Soldier': 4, 'Under the North Star': 4, 'Meek Heritage': 3}
B = {'Seven Brothers': 2, 'The Unknown Soldier': 2, 'Kalevala': 2, 'Under the North Star': 2, 'Meek Heritage': 2}
for t in set(A2) | set(B):
    row = next(r for r in S['rows'] if r[0] == t)
    p = dict(row[3])
    if t in A2: p['A2'] = A2[t]
    if t in B: p['B'] = B[t]
    specio.setrow(S, t, pts=p)
specio.setrow(S, 'The Tales of Ensign Stål', note='市场正典第 1 名（累计印数约 120 万）；高中共读书目里没有，论文说它的教学已移到初中；不在 D 前 2000 · Goodreads 825')
specio.setrow(S, 'Meek Heritage', note='即《虔诚的贫困》（Hurskas kurjuus）；市场正典第 16 名、高中共读第 5 名；不在 D 前 2000 · Goodreads 566')
NEW = [
 ('The Railroad (Rautatie)', 'Juhani Aho', '本国', {'A2': 4}, '', '市场正典第 5 名；萨沃乡间一对老夫妇去看火车，地点待查；不在 D 前 2000 · Goodreads 1,187'),
 ('Heath Cobblers (Nummisuutarit)', 'Aleksis Kivi', '本国', {'A2': 4}, '', '基维第二本；剧本，市场正典第 7 名；村子是虚构的，地点待查；不在 D 前 2000 · Goodreads 353'),
 ("The Surgeon's Stories (Välskärin kertomuksia)", 'Zacharias Topelius', '本国', {'A2': 4}, '', '市场正典第 9 名；历史小说，地点待查；不在 D 前 2000 · Goodreads 61（第 2 卷）'),
 ('The Thinker of Havukka-aho (Havukka-ahon ajattelija)', 'Veikko Huovinen', '本国', {'A2': 4}, '', '市场正典第 10 名；凯努林区，地点待查；不在 D 前 2000 · Goodreads 1,156'),
 ('The Red Line (Punainen viiva)', 'Ilmari Kianto', '本国', {'A2': 3, 'B': 2}, '', '市场正典第 12 名、高中共读第 3 名；1907 年首次议会选举，地点待查；不在 D 前 2000 · Goodreads 1,330'),
 ('Juha', 'Juhani Aho', '本国', {'B': 2}, '', '阿霍第二本；高中共读第 4 名；Goodreads 没查到单独条目'),
 ('The Betrothal (Kihlaus)', 'Aleksis Kivi', '本国', {'A2': 3}, '', '市场正典第 11 名；独幕剧；Goodreads 48'),
 ('Borrowing Matches (Tulitikkuja lainaamassa)', 'Maiju Lassila', '本国', {'A2': 3}, '', '市场正典第 13 名；不在 D 前 2000 · Goodreads 348'),
 ('The Maid Silja (Nuorena nukkunut)', 'F. E. Sillanpää', '本国', {'A2': 3}, '', '西兰帕第二本；市场正典第 14 名；不在 D 前 2000 · Goodreads 686'),
]
for r in NEW:
    if not any(x[0] == r[0] for x in S['rows']): S['rows'].append(r)
for cc, S in specs.items(): specio.save(cc, S)
print('ok', sorted(specs))
