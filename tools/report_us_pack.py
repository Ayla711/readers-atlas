#!/usr/bin/env python3
"""Generate an explicit first-batch inventory and canonical deferral report."""
import collections
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / 'packs/us'
WORK = ROOT / 'tools/us-work'


def read(p):
    return json.loads(p.read_text(encoding='utf-8'))


def norm(s):
    return re.sub(r'[^a-z0-9]', '', re.sub(r'^(the|a|an)\s+', '', s.lower()))


def main():
    books, places, lines = [read(PACK/(f+'.json')) for f in ['books', 'places', 'lines']]
    photos = read(PACK/'photos.json')
    canon = read(ROOT/'tools/canon-us.json')
    result = read(WORK/'shared/validation.json')
    authors = {b['author'] for b in books}
    ca = {a['name']: a for a in canon['authors']}
    counts = collections.Counter(l['book_id'] for l in lines)
    title_keys = {(norm(b['title']), b['author']) for b in books}
    states = result['state_places']
    death = {}
    photo_evidence = {}
    for region in ['central', 'west', 'east']:
        ev = read(WORK/region/'evidence.json')
        photo_evidence.update(ev.get('photos', {}))
        for key in ['books', 'copyright']:
            for bid, value in ev.get(key, {}).items():
                if not isinstance(value, dict):
                    continue
                if any(k in value for k in ['death_year', 'author_death', 'author_death_year']):
                    death[bid] = (value.get('death_year', value.get('author_death', value.get('author_death_year'))), value.get('author_source', value.get('source', '')))
    report = [
        '# 美国内容包 · 第一批交付报告', '', '日期：2026-11-09。依据 `content-pack-spec.md` v1.1 与 `us-brief.md`。', '',
        '## 交付范围', '',
        f'- {len(books)} 本书，{len(authors)} 位作者，{len(places)} 个地点，{len(lines)} 条内容：{result["quotations"]} 条公有领域摘句、{result["scenes"]} 条原创场景说明。',
        f'- 覆盖 {result["states_covered"]}/51 个一级区：50 州和华盛顿特区。州归属不写入地点 JSON，留给导入器按坐标分配。',
        f'- {len(photos)} 张照片清单；所有朝圣地均配 Commons 文件。未收影视取景地；其 20 处目标属于第三批。',
        '- 五个 JSON 均为 UTF-8。全部内容为 `draft`。本次未导入网站，未修改现有 `data/`，未开始第二批。',
        '- 英文摘句以脚本从实际下载的古登堡文本截取，保留原标点与 CRLF 换行，不重排文字。`text_zh` 为本次自译，等待人工审核；`translation: original` 表示英文为原作。',
        '', '## 自查结果及导入边界', '',
        '- `node tools/validate.js`：现有英国网站数据通过，0 errors。该工具固定读取英国 `data/*.js` 与英国边界，不能把此结果冒称为美国包通过导入。',
        f'- `python3 tools/validate_us_pack.py`：{len(result["errors"])} errors；检查批次规模、必填字段、全局 ID、引用、高亮、语言、版权分流、原文逐字匹配、照片完整性及州覆盖。机器结果位于 `tools/us-work/shared/validation.json`。',
        '- 独立重新下载 18 份古登堡全文后，40 条摘句全部逐字匹配，未依赖生成脚本自己的判断。下载 URL 与 SHA-256 见 `tools/us-work/shared/fresh-source-check.json`。',
        '- 同时对照 `packs/existing-ids.json` 与实时 `data/*.js` 快照查重。后者有 161 本书、259 个地点、212 条内容，较交付的英国快照新增条目也纳入冲突检查。美国 Oxford 使用 `oxford-mississippi`。',
        '- 英国寿命加 70 年口径采用任务规定的 1955 年去世截止线。海明威、福克纳、斯坦贝克、赫斯顿、怀尔德、弗罗斯特等仍只写场景说明，即使美国古登堡有全文也不引用。规则参考 [英国政府版权期限说明](https://www.gov.uk/copyright/how-long-copyright-lasts)。',
        '- 坐标从公开页面的十进制度数或度分秒换算后保留四位小数；整数末尾的零不影响 JSON 数值精度。城市、河流及山地的代表点用途逐条注明，不伪称精确场景地址。',
        '- 州边界独立检查最终使用 [美国人口普查局 2024 年 1:500,000 州界](https://www2.census.gov/geo/tiger/GENZ2024/shp/cb_2024_us_state_500k.zip)。69 个地点全部落入其预期州／DC，没有手动落区例外。较粗的初检边界曾漏掉 Nantucket、Sullivan’s Island 和 Honolulu；精细官方边界已全部解决，未为了通过检查移动正确坐标。Honolulu 使用有公开出处的市政厅陆地点作为城市代表，不声称小说场景发生于该楼。',
        '- 阿拉斯加使用 Wrangell 的实际美国地点；没有把加拿大育空或克朗代克写入美国。',
        '- Commons 页面已核对允许许可，照片只交文件标题及双语说明。导入器仍需重新查许可、下载与生成署名。',
        '', '## 书目、作者与版权依据', '',
        '“一级／二级”指作者在外部名单中的等级；书不一定本身上榜。书单命中和其余书目的推迟原因见后文。', '',
        '| 书名 / ID | 作者 | 名单 | 版权处理 | 内容数 |', '|---|---|---|---|---|'
    ]
    for b in books:
        tier = f"一级作者" if ca.get(b['author'], {}).get('tier') == 1 else '二级作者' if b['author'] in ca else '名单外补充'
        yr, url = death.get(b['id'], (None, ''))
        desc = ('公有领域' if b['public_domain'] else '仅场景说明')
        if yr:
            desc += f'；[去世于 {yr}]({url})' if url else f'；去世于 {yr}'
        elif b['author'] == 'Alice Walker':
            desc += '；在世作者'
        report.append(f"| {b['title_zh']} / `{b['id']}` | {b['author']} | {tier} | {desc} | {counts[b['id']]} |")
    report += ['', '## 照片许可核验', '', '| 地点 | Commons 文件页 | 已核实许可 |', '|---|---|---|']
    for pid, photo in photos.items():
        ev = photo_evidence[pid]
        report.append(f'| `{pid}` | [{photo["commons_file"]}]({ev["file_page"]}) | {ev["license"]} |')
    report += ['', 'Brunswick 配图为约 1905 年的历史明信片，双语说明已明确，不代表建筑当前外观。', '', '## 每州地点数量', '', '| 一级区 | 数量 | 地点 ID |', '|---|---:|---|']
    for state, ids in sorted(states.items()):
        report.append(f'| {state} | {len(ids)} | ' + '、'.join(f'`{x}`' for x in ids) + ' |')
    report += ['', '## 选题调整与名单外依据', '',
        '- 第一批以全国覆盖为优先约束；以名单中的一级作者为主体，加入确有地方关联的旅行文学。多数故居与其余经典本批暂缓，不视为已完成或永久排除。',
        '- John Muir《Travels in Alaska》补阿拉斯加和太平洋西北；作者有 [NPS John Muir National Historic Site](https://www.nps.gov/jomu/index.htm) 公共纪念地。',
        '- Owen Wister《The Virginian》补怀俄明；[Medicine Bow Museum](https://travelwyoming.com/listing/medicine-bow-museum/735/) 的公开文学纪念资料支持选题。',
        '- Hamlin Garland《Main-Travelled Roads》补南达科他；[美国诗人学会作者介绍](https://poets.org/poet/hamlin-garland) 记录其文学经历与普利策奖。地点摘自作者序言而非虚构短篇正文，已明确标注。',
        '- George Alfred Townsend《The Entailed Hat》补特拉华；[特拉华州档案馆文学研究](https://archivesfiles.delaware.gov/ebooks/GATHs_Literary_Work_and_Folk.pdf) 第 37 页讨论此书的地方文学地位。',
        '- Charles W. Chesnutt《The Marrow of Tradition》补北卡罗来纳；依据 [北卡州文化资源部门作家纪念牌资料](https://www.dncr.nc.gov/blog/2023/12/29/charles-w-chesnutt-1858-1932-i-32)，并核验虚构 Wellington 与 Wilmington 的关系。',
        '- 《飘》《Look Homeward, Angel》本轮未找到满足指定 Gutenberg 下载流程的可用文本，暂缓；不以记忆引文代替。《大地》主要情节在中国，未用美国故居冒充小说发生地。',
        '- 印第安纳 Indianapolis 的摘句是人物说明自己的来处，并非当地正在发生的场景；地点说明已明确。城市规模清单和作者序言属于真实地点提及，但文学展示优先级可在人工审核时降低。',
        '', '## 外部名单完整去向', '',
        f'名单含 {len(canon["authors"])} 位作者、{len(canon["sites"])} 处故居、{len(canon["big_read"])} 条书单来源记录；去重后为 {len({(b["title"],b["author"]) for b in canon["big_read"]})} 部作品。同书被两份书单收录时，下表合并出处。', '',
        '### 作者', '', '| 作者 | 级别 | 本批处理／暂缓原因 |', '|---|---|---|'
    ]
    for a in canon['authors']:
        if a['name'] in authors:
            reason = '已收：' + '、'.join(b['title_zh'] for b in books if b['author'] == a['name'])
        elif a['tier'] == 1:
            reason = '暂缓：第一批 30 本及全国覆盖额度；后续须补作品与故居，尚未完成逐条来源核验。'
        else:
            reason = '暂缓：二级候选，第一批优先一级作者与缺州覆盖；等待导入反馈后再选。'
        report.append(f'| {a["name"]} | {a["tier"]} | {reason} |')
    report += ['', '### 上榜书', '', '| 作品 | 作者 | 出处 | 本批处理／暂缓原因 |', '|---|---|---|---|']
    listed = {}
    for b in canon['big_read']:
        listed.setdefault((b['title'], b['author']), []).append(b['src']+(f' #{b["rank"]}' if b['rank'] else ''))
    existing = read(ROOT/'packs/existing-ids.json')['books']
    for (title, author), sources in listed.items():
        if (norm(title), author) in title_keys:
            reason = '本批已收。'
        elif any(norm(b['title']) == norm(title) and b['author'] == author for b in existing):
            reason = '英国包已有同书，按全局单书约定不重复新增；以后只扩地点引用。'
        elif title == 'Gone with the Wind':
            reason = '暂缓：本轮未取得满足指定下载流程的古登堡原文；不是版权判定为否。'
        elif author in authors:
            reason = '暂缓：本批已选该作者其他作品或只选部分上榜作品，优先满足 30 本与缺州覆盖。'
        else:
            reason = '暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。'
        report.append(f'| {title} | {author} | {", ".join(sources)} | {reason} |')
    report += ['', '### 故居名单', '',
        '同一城市的原著地点不等于已收该城的作家故居。例如 Hannibal 城市点不计作 Twain Boyhood Home；Oxford 城市原型不计作 Rowan Oak。', '',
        '| 名单地点 | 州 | 本批处理／暂缓原因 |', '|---|---|---|']
    # Map actual retained pilgrimage entries to canonical names by explicit identifying words.
    for site in canon['sites']:
        candidates = [p for p in places if (p['place_type'] == 'pilgrimage' and
                      (('Stowe' in site['name'] and 'stowe' in p['id'] and
                        (('Brunswick' in site['name'] and 'brunswick' in p['id']) or ('Hartford' in site['name'] and 'hartford' in p['id']))) or
                       ('Frost Stone House' in site['name'] and 'frost' in p['id'] and 'stone' in p['id']))) or
                      ('Orchard House' in site['name'] and p['id'] == 'concord-orchard-house')]
        if candidates:
            reason = '已收：' + '、'.join('`'+p['id']+'`（'+p['place_type']+'）' for p in candidates)
        elif site.get('status') in ['private', 'not open', "scholars' retreat"]:
            reason = '暂缓：私人／非普通开放场所，需进一步核验访问说明和自由许可实地照片；本批不引导造访。'
        else:
            reason = '暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。'
        report.append(f'| {site["name"]} | {site["state"]} | {reason} |')
    report += ['', '## 复现与审核文件', '',
        '1. 三组 `tools/us-work/{east,central,west}/build.py` 从已下载的文本及截取锚点生成分片；同目录 `evidence.json` 保存原始坐标、版权依据及原文证据，`notes.md` 记录内容判断。',
        '2. `python3 tools/assemble_us_pack.py` 合并五个 JSON。',
        '3. `python3 tools/validate_us_pack.py` 独立校验美国包，并输出逐州机器结果。',
        '4. `python3 tools/report_us_pack.py` 重建本报告。',
        '5. `node tools/validate.js` 检查现有网站数据；正式导入工具准备好后再执行导入和项目负责人的内容审核。',
        '', '接下来等待第一批的导入与审核反馈，再决定第二批；本交付不宣称已完成名单的全面覆盖。', ''
    ]
    (PACK/'REPORT.md').write_text('\n'.join(report), encoding='utf-8')
    print('Wrote', PACK/'REPORT.md')


if __name__ == '__main__':
    main()
