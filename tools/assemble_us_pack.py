#!/usr/bin/env python3
"""Merge independently researched batch-one fragments; do not import into the app."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / 'tools/us-work'
OUT = ROOT / 'packs/us'


def write(name, data):
    (OUT / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main():
    OUT.mkdir(exist_ok=True)
    for name in ['books', 'places', 'lines', 'photos']:
        merged = {} if name == 'photos' else []
        for region in ['east', 'central', 'west']:
            part = json.loads((WORK / region / (name + '.json')).read_text(encoding='utf-8'))
            if name == 'photos':
                assert not merged.keys() & part.keys(), 'duplicate photo/place across fragments'
                merged.update(part)
            else:
                merged.extend(part)
        if name != 'photos':
            ids = [row['id'] for row in merged]
            assert len(ids) == len(set(ids)), f'duplicate {name} across fragments'
        write(name + '.json', merged)
    write('pack.json', {
        'country': 'us', 'country_name': 'United States', 'country_name_zh': '美国',
        'region_scheme': 'state', 'produced_by': 'Codex', 'produced_at': '2026-11-09',
        'notes': '第一批：30 本书；50 州及华盛顿特区覆盖。所有摘句与场景说明为 draft，等待导入和人工审核；未开始第二批。坐标、原文截取和照片许可核验记录见 tools/us-work/，范围与选题说明见 REPORT.md。'
    })
    print('Assembled', OUT)


if __name__ == '__main__':
    main()
