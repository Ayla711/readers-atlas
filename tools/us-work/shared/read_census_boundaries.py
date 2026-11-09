#!/usr/bin/env python3
"""Read Census Polygon SHP/DBF using only the standard library.

Preserve all rings; the audit uses the even/odd polygon rule (islands and holes).
This is an audit artifact, not application geometry or a general shapefile library.
"""
import hashlib
import json
import struct
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
archive = HERE/'cb_2024_us_state_500k.zip'
with zipfile.ZipFile(archive) as z:
    dbf = z.read(next(n for n in z.namelist() if n.endswith('.dbf')))
    shp = z.read(next(n for n in z.namelist() if n.endswith('.shp')))
count, header_size, record_size = struct.unpack_from('<IHH', dbf, 4)
fields = []
offset = 32
while dbf[offset] != 13:
    fields.append((dbf[offset:offset+11].split(b'\0')[0].decode('ascii'), dbf[offset+16]))
    offset += 32
records = []
for i in range(count):
    offset = header_size + i*record_size
    assert dbf[offset] == 32, 'unexpected deleted DBF record'
    offset += 1
    row = {}
    for name, length in fields:
        row[name] = dbf[offset:offset+length].decode('utf-8').strip()
        offset += length
    records.append(row)
assert struct.unpack_from('>I', shp)[0] == 9994
assert struct.unpack_from('<I', shp, 32)[0] == 5, 'expected Polygon shape file'
states = []
offset = 100
for row in records:
    recno, words = struct.unpack_from('>II', shp, offset)
    assert recno == len(states)+1
    body = shp[offset+8:offset+8+words*2]
    assert struct.unpack_from('<I', body)[0] == 5
    bbox = struct.unpack_from('<4d', body, 4)
    parts, points = struct.unpack_from('<II', body, 36)
    starts = list(struct.unpack_from('<'+'I'*parts, body, 44)) + [points]
    xy = [list(struct.unpack_from('<2d', body, 44+4*parts+j*16)) for j in range(points)]
    rings = [xy[a:b] for a,b in zip(starts, starts[1:])]
    assert all(len(r) >= 4 and r[0] == r[-1] for r in rings)
    states.append({'name': row['NAME'], 'abbr': row['STUSPS'], 'bbox': bbox, 'rings': rings})
    offset += 8+words*2
assert offset == len(shp)
result = {'source': 'https://www2.census.gov/geo/tiger/GENZ2024/shp/cb_2024_us_state_500k.zip',
          'sha256': hashlib.sha256(archive.read_bytes()).hexdigest(), 'scale': '1:500,000', 'states': states}
(HERE/'census-states.json').write_text(json.dumps(result, separators=(',', ':'))+'\n', encoding='utf-8')
print(f'Parsed {len(states)} state/territory records, {sum(len(s["rings"]) for s in states)} rings.')
