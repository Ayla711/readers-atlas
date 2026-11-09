# tools/checks — 页面检查（Playwright，无头 Chromium）

每项都以仓库目录为参数：`python3 -I tools/checks/<脚本> "$PWD"`。改了地图、标签、样式后全跑一遍；`run_all.sh` 按快慢排好了顺序。

| 脚本 | 查什么 | 时间 |
|---|---|---|
| `check_labels.py` | 地图标签、圆点、地图元素、侧栏之间不重叠（map-layers.md 3、3.2、10） | 1 分钟 |
| `check_cjk.py` | 中文界面下没有漏翻的英文、没有中英混排错误 | 1 分钟 |
| `check_contrast.py` | 14 个视图 × 中英文，文字对比度 ≥ 4.5:1（大字 3:1），按 CSS 背景算 | 2 分钟 |
| `check_contrast_pixels.py` | 地图上压着海/陆的文字，按真实像素算对比度 | 1 分钟 |
| `check_wave.py` | WAVE 风格的无障碍规则：空按钮/标签/标题、表单标签、ARIA、小字、焦点等 | 2 分钟 |
| `check_name_dots.py` | 地名不压别的地点的圆点、地名互不重叠，两种窗口尺寸、每个视图 | 8 分钟 |
| `flags_check_slow.py` / `flags_check_zh_slow.py` | 旅行小旗与地名、圆点不重叠（英 / 中） | 各 5 分钟 |

数据校验另见 `node tools/validate.js [国家]`、`node tools/check_coverage.js`。
