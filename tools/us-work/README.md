# 美国第一批核验材料

正式交付是 `packs/us/` 的五个 JSON 和 REPORT.md。这里保存生产分片、下载文本、网页证据与复现脚本，不属于网站运行数据。

从仓库根目录复现：

```sh
python3 tools/us-work/east/build.py
python3 tools/us-work/central/build.py
python3 tools/us-work/west/build.py
python3 tools/assemble_us_pack.py
python3 tools/validate_us_pack.py
python3 tools/report_us_pack.py
node tools/validate.js
```

需要联网更新独立原文副本时运行 `sh tools/us-work/shared/fetch_gutenberg.sh`。原文若更新，应重新核验逐字匹配，不能随意修改引文使测试通过。摘句保留 UTF-8 原文及 CRLF；查看器可以显示为普通换行，但数据不重排。

`shared/fresh-source-check.json` 保存最终核验所用 18 个古登堡 URL 和 SHA-256。各地区的 `evidence.json` 和脚本保存摘句锚点、原始坐标、作者死亡年份来源及 Commons 文件页许可。网页缓存仅供审核，任何缓存失败页不作为事实证据；西部部分坐标页因限流通过网页工具读取，文本证据单独缓存。

`shared/cb_2024_us_state_500k.zip` 来自美国人口普查局；`read_census_boundaries.py` 读取其中 SHP/DBF 并保留全部外环、内环及海岛。`census-states.json` 用于最终落区检查。旧 `us-states.geojson` 仅保留作初检记录，最终校验不再使用；`boundary-exceptions.json` 为空，最终没有手动州归属例外。

`shared/current-ids.json` 是实际网站数据的 ID 快照，比用户提供的英国导出更新。两者均参与查重。`shared/validation.json` 是美国包校验结果；英国 `tools/validate.js` 的成功不能代替美国包检查或正式导入。

所有内容保持 draft；后续需项目负责人导入和审稿。本目录没有第二批内容。
