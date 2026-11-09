#!/usr/bin/env python3
"""Validate the batch-one pack without modifying the UK application data.

Usage: python3 tools/validate_us_pack.py [packs/us]
Source downloads and official Census state-boundary data are in tools/us-work.
The official importer remains the authority for final region assignment/licences.
"""
import collections
import hashlib
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
PACK = ROOT / (sys.argv[1] if len(sys.argv) > 1 else 'packs/us')
WORK = ROOT / 'tools/us-work'
errors = []


def check(condition, message):
    if not condition:
        errors.append(message)


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def required(obj, fields, label):
    for field in fields:
        check(field in obj and obj[field] not in (None, '', []), f'{label}: missing {field}')


def in_ring(x, y, ring):
    inside = False
    for a, b in zip(ring, ring[1:] + ring[:1]):
        if (a[1] > y) != (b[1] > y) and x < (b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0]:
            inside = not inside
    return inside


def in_geometry(x, y, geometry):
    polygons = [geometry['coordinates']] if geometry['type'] == 'Polygon' else geometry['coordinates']
    return any(in_ring(x, y, rings[0]) and not any(in_ring(x, y, hole) for hole in rings[1:]) for rings in polygons)


def validate():
    meta = read(PACK / 'pack.json')
    books, places, lines = [read(PACK / (k + '.json')) for k in ('books', 'places', 'lines')]
    photos = read(PACK / 'photos.json')
    required(meta, ['country', 'country_name', 'country_name_zh', 'region_scheme', 'produced_by', 'produced_at', 'notes'], 'pack')
    check(meta['country'] == 'us' and meta['region_scheme'] == 'state', 'pack: country/scheme')
    occupied = set()
    for old_path in [ROOT/'packs/existing-ids.json', WORK/'shared/current-ids.json']:
        old = read(old_path)
        for key in ['books', 'places', 'line_ids']:
            occupied.update(x['id'] if isinstance(x, dict) else x for x in old[key])
    all_ids = []
    for label, rows in [('book', books), ('place', places), ('line', lines)]:
        for row in rows:
            ident = row.get('id', '')
            check(bool(re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', ident)), f'{label}: invalid id {ident}')
            check(ident not in occupied, f'{label}: occupied id {ident}')
            all_ids.append(ident)
    check(len(all_ids) == len(set(all_ids)), 'duplicate global ids inside pack')
    book_map = {b['id']: b for b in books}
    place_map = {p['id']: p for p in places}
    check(len(books) == 30, f'batch: expected 30 books, got {len(books)}')
    check(60 <= len(places) <= 80, f'batch: expected 60–80 places, got {len(places)}')
    check(len(lines) == 60, f'batch: expected 60 lines, got {len(lines)}')
    for b in books:
        required(b, ['title', 'title_zh', 'author', 'author_zh', 'year', 'orig_lang', 'source_url'], b['id'])
        check(isinstance(b.get('public_domain'), bool), f"{b['id']}: public_domain boolean")
        check(b.get('orig_lang') == 'en', f"{b['id']}: non-English requires extra review")
    copyright_evidence = {}
    expected_states = {}
    coordinate_evidence = {}
    photo_evidence = {}
    for region in ['east', 'central', 'west']:
        ev = read(WORK/region/'evidence.json')
        photo_evidence.update(ev.get('photos', {}))
        expected_states.update(ev.get('state_by_place', {}))
        for pid, value in ev.get('coordinates', ev.get('places', {})).items():
            coordinate_evidence[pid] = value
            if value.get('state'):
                expected_states[pid] = value['state']
        for key in ['books', 'copyright']:
            for bid, value in ev.get(key, {}).items():
                if isinstance(value, dict) and any(k in value for k in ['death_year', 'author_death', 'author_death_year']):
                    copyright_evidence[bid] = value
    for b in books:
        ev = copyright_evidence.get(b['id'], {})
        check(bool(ev), f"{b['id']}: missing copyright evidence")
        year = ev.get('death_year', ev.get('author_death', ev.get('author_death_year')))
        check(b['public_domain'] == (isinstance(year, int) and year <= 1955), f"{b['id']}: copyright mismatch with death evidence")
        check(bool(ev.get('author_source', ev.get('source'))), f"{b['id']}: copyright source absent")
    linked_places = set()
    for p in places:
        label = p['id']
        required(p, ['name', 'name_zh', 'lat', 'lon', 'place_type', 'note', 'note_en', 'coord_checked', 'fact_source'], label)
        check(p.get('place_type') in ['original', 'prototype', 'pilgrimage', 'film_location'], f'{label}: invalid type')
        check(' — https://' in p.get('coord_checked', ''), f'{label}: coordinate source format')
        check('state' not in p and 'region' not in p, f'{label}: region must be importer assigned')
        ev = coordinate_evidence.get(label, {})
        check(bool(ev), f'{label}: coordinate evidence absent')
        if 'source_lat' in ev:
            lat, lon = ev['source_lat'], ev['source_lon']
        else:
            raw = ev.get('raw', ev.get('raw_coordinates', ''))
            nums = re.findall(r'-?\d+(?:\.\d+)?', raw)
            check(len(nums) == 2, f'{label}: could not parse coordinate evidence')
            if len(nums) == 2:
                lat, lon = map(float, nums)
                if 'coordinates' in raw:
                    lat, lon = lon, lat
            else:
                lat, lon = 0, 0
        check(abs(p['lat']-lat) <= 0.000050001 and abs(p['lon']-lon) <= 0.000050001, f'{label}: coordinate changed from published source')
        for field, limit in [('lat', 90), ('lon', 180)]:
            value = p.get(field)
            check(isinstance(value, (int, float)) and abs(value) <= limit, f'{label}: invalid {field}')
            check(round(value, 4) == value, f'{label}: {field} more than 4 decimal places')
        if p['place_type'] == 'prototype':
            required(p, ['prototype_of', 'prototype_of_en'], label)
        if p['place_type'] in ['pilgrimage', 'film_location']:
            required(p, ['book_ids'], label)
            check(label in photos, f'{label}: required photo absent')
            linked_places.add(label)
        if p['place_type'] == 'film_location':
            required(p, ['adaptation', 'scene', 'scene_en'], label)
            required(p.get('adaptation', {}), ['title', 'year', 'kind'], label)
        for bid in p.get('book_ids', []):
            check(bid in book_map, f'{label}: dangling book {bid}')
    counts = collections.Counter()
    quoted = 0
    source_cache = {}
    fresh_evidence = {}
    for line in lines:
        label = line['id']
        bid = line.get('book_id')
        required(line, ['book_id', 'place_ids', 'location', 'location_zh', 'text_en', 'text_zh', 'status'], label)
        check(bid in book_map, f'{label}: unknown book {bid}')
        counts[bid] += 1
        check(line.get('status') == 'draft', f'{label}: must be draft')
        for pid in line.get('place_ids', []):
            check(pid in place_map, f'{label}: dangling place {pid}')
            check(place_map.get(pid, {}).get('place_type') != 'film_location', f'{label}: quote/scene points to film location')
            linked_places.add(pid)
        for field, text_field in [('highlight_en', 'text_en'), ('highlight_zh', 'text_zh')]:
            for term in line.get(field, []):
                check(term in line.get(text_field, ''), f'{label}: missing highlight {term}')
        if not book_map.get(bid, {}).get('public_domain'):
            check(line.get('kind') == 'scene', f'{label}: copyrighted quotation')
        if line.get('kind') == 'scene':
            required(line, ['fact_source'], label)
            check('source' not in line and 'text_orig' not in line, f'{label}: scene has quote-only fields')
        else:
            check('kind' not in line, f'{label}: invalid kind')
            required(line, ['source', 'translation'], label)
            source = line.get('source', {})
            check(source.get('kind') == 'gutenberg', f'{label}: expected downloaded Gutenberg source')
            gid = source.get('id')
            if gid not in source_cache:
                fresh = WORK/'shared/fresh-gutenberg'/f'pg{gid}.txt'
                matching = [fresh] if fresh.exists() else []
                check(bool(matching), f'{label}: missing independent fresh source download pg{gid}.txt')
                source_cache[gid] = [f.read_bytes().decode('utf-8-sig') for f in matching]
                if matching:
                    fresh_evidence[gid] = {'url': f'https://www.gutenberg.org/cache/epub/{gid}/pg{gid}.txt',
                                           'sha256': hashlib.sha256(fresh.read_bytes()).hexdigest()}
            fragments = line.get('text_en', '').split('…')
            check(any(all(part in src for part in fragments) for src in source_cache[gid]), f'{label}: quotation not verbatim in cached pg{gid}.txt')
            quoted += 1
    for bid in book_map:
        check(1 <= counts[bid] <= 10, f'{bid}: must have 1–10 lines, got {counts[bid]}')
    check(set(place_map) <= linked_places, 'unlinked places: ' + ', '.join(sorted(set(place_map)-linked_places)))
    for pid, photo in photos.items():
        check(pid in place_map, f'photo: unknown place {pid}')
        required(photo, ['commons_file', 'alt_en', 'alt_zh'], f'photo {pid}')
        check(photo.get('commons_file', '').startswith('File:'), f'photo {pid}: Commons title missing File:')
        ev = photo_evidence.get(pid, {})
        check(bool(ev.get('file_page')), f'photo {pid}: verified file-page evidence missing')
        check(bool(re.fullmatch(r'(CC BY(?:-SA)? [0-9.]+|CC0|Public domain)', ev.get('license', ''))), f'photo {pid}: licence evidence invalid')
    english = {'title', 'author', 'name', 'note_en', 'prototype_of_en', 'scene_en', 'location', 'text_en', 'alt_en'}
    for row in books + places + lines + list(photos.values()):
        for key in english & row.keys():
            check(not re.search(r'[\u3040-\u30ff\u3400-\u9fff]', str(row[key])), f"{row.get('id', 'photo')}: CJK in {key}")
    boundary = read(WORK/'shared/census-states.json')
    features = boundary['states']
    territories = {'PR', 'VI', 'GU', 'MP', 'AS'}
    states = {f['name']: [] for f in features if f['abbr'] not in territories}
    state_abbreviations = {f['name']: f['abbr'] for f in features}
    unresolved = []
    for p in places:
        matches = []
        x, y = p['lon'], p['lat']
        for f in features:
            a, b, c, d = f['bbox']
            if a <= x <= c and b <= y <= d and sum(in_ring(x, y, ring) for ring in f['rings']) % 2:
                matches.append(f['name'])
        if len(matches) == 1 and matches[0] in states:
            states[matches[0]].append(p['id'])
            check(expected_states.get(p['id']) == state_abbreviations[matches[0]], f"{p['id']}: polygon state differs from source evidence")
        else:
            unresolved.append({'id': p['id'], 'matches': matches})
    for item in unresolved:
        check(False, f"{item['id']}: unresolved Census state boundary {item['matches']}")
    for state, ids in states.items():
        check(bool(ids), f'coverage: no place in {state}')
    result = {'books': len(books), 'places': len(places), 'lines': len(lines), 'quotations': quoted,
              'scenes': len(lines)-quoted, 'photos': len(photos), 'states_covered': sum(bool(v) for v in states.values()),
              'state_places': states, 'boundary_source': boundary['source'], 'boundary_unresolved': unresolved, 'errors': errors}
    (WORK/'shared/fresh-source-check.json').write_text(json.dumps(fresh_evidence, indent=2)+'\n', encoding='utf-8')
    (WORK/'shared/validation.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ['state_places']}, ensure_ascii=False, indent=2))
    return bool(errors)


if __name__ == '__main__':
    sys.exit(validate())
