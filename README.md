# The Reader's Atlas · 读者地图（原型）

笔记本网页版原型，从英国开始，暂无后端。

## 怎么打开

双击 `index.html` 即可，不需要安装，也不需要本地服务器。大区地图和数据都在本地文件里，离线也能用。需要联网的只有两样：字体（Fraunces、Inter、IBM Plex Mono、Caveat、思源宋体，来自 Google Fonts，离线时退回系统字体），和放大后的街道底图（来自 OpenFreeMap，离线时不显示，地图照常可用）。

## 能做什么

- 开场动画：旋转的地球展开成平面世界地图，标题浮现，停在世界首页。点击、按键或滚轮可跳过；同一次浏览会话只播一次；系统开启“减少动画”时不播放。测试时可在网址后加 `?intro=1` 强制播放，`?intro=0` 关闭。
- 语言：默认英文，右上角按钮切换中文，选择会被记住。界面文字都在 `js/i18n.js`。
- 世界首页：不带路由打开时，整张世界地图铺满窗口，中间是标题，侧栏收起。点英国进入英国全景；点右边缘的 “Explore” 标签或两指向左轻扫打开侧栏，点侧栏左边缘的 › 或向右轻扫收起。网址：首页不带 `#`，英国全景是 `#/uk`。
- 地图：世界底图 + 英国 12 个大区（ITL1 分区）。滚轮缩放、拖动平移，点大区放大，点标记看摘句。
- 放大后的细节（只看不点）：进入大区后，郡和伦敦 33 个自治市的边界以虚线显示并标出名字；继续放大，大区的底色逐渐变淡，下面的复古街道底图显出来——泰晤士河等河流、湖泊、公园、铁路、主次干道，再放大是小街、建筑、街名和街区名。底图由 `js/basemap.js` 绘制（MapLibre GL + OpenFreeMap 矢量瓦片，免费无需密钥），配色沿用设计系统的地图色，和 SVG 地图逐像素对齐；切换中文时底图地名也会换成中文（有中文名的地方）。
- 标签优先级：可点击的地点名和标记点最优先；郡名其次，会避开地点名；底图自己的城镇名、街名等最后，只要会和前两者重叠就不画（例如 Whitby Abbey 旁不会再出现第二个 “Whitby”）。
- 海岸线：放大到街道底图出现后，海岸线只用底图（OpenStreetMap）那一条；大区和郡只画内陆边界，大区底色画在底图海水下面，由真实海岸线裁齐。离线时保持原来的样子。详细规则见 `docs/map-layers.md`。
- 四种地点：原著地点（实心圆）、原型地（空心圆）、作家朝圣（星）、影视取景（方块）。左下角图例同时是筛选。
- 摘句：英文版检索和显示，非现代英语原作可切换看原文，地名高亮。
- 搜索：书名、作者、地点，中英文都可以。输入时地图同步高亮：结果所在的地点被圈出，其他标记变淡，用方向键或鼠标指到哪条结果，它的地点就闪动并标出名字。也可以搜作者。
- 打开一本书或一位作者后，地图只显示相关的地点（原著地点、原型地、作家朝圣、影视取景都算），左上角的标签可以切换成显示全部；鼠标指到右侧列表里的地点，地图上对应的标记会闪动并标出名字。
- 链接：每个页面都有自己的网址，如 `index.html#/place/whitby-abbey`、`#/book/persuasion`、`#/author/jane-austen`、`#/region/TLI`，可以收藏或发给别人；浏览器后退键可回到上一个视图。
- 我的旅行：收藏地点、标记去过、加入行程（带日期），统计去过的地点和覆盖的大区。
- 我的书单：想读 / 已读，每本书可以写笔记。
- 个人数据存在浏览器 localStorage 里，换浏览器或清除网站数据会丢失。

## 文件结构

```
index.html          页面
css/style.css       样式
js/data.js          按需加载一个国家的数据文件（data/<国家>/…），国家之间排队、互不干扰（11-09，R-3）
js/app.js           全部交互逻辑（无第三方库）
js/store.js         个人数据（心愿单、去过、行程、书架、收藏、笔记、偏好）唯一的读写入口；导出 / 导入（11-09，R-6、R-7）
js/i18n.js          界面文字（英文 / 中文）
js/journal-store.js 旅行日志的存储（文字走 store.js 的同一后端，照片在 IndexedDB）
js/intro.js         开场动画
js/basemap.js       放大后的复古街道底图（只做视觉，不可点击）
js/vendor/          MapLibre GL 4.7.1（BSD-3 许可，见 maplibre-gl.LICENSE.txt）
data/countries.js   国家列表（代码、中英文名、一级区划叫法、视图范围、数据文件），由 tools/build_countries.py 从 tools/countries.json 生成
data/world-geo.js   世界各国轮廓，由 tools/build_geo.py 生成，不要手改
data/intro-geo.js   开场动画用的精简世界轮廓，由 tools/build_intro_geo.py 生成
data/uk/geo.js      英国的 12 个大区和 232 个单元，由 tools/build_geo.py 生成，不要手改
data/us/geo.js      美国 50 州 + DC（内容文件暂空，countries.js 里未开放）
data/uk/books.js    书目
data/uk/places.js   地点（country、place_type、adaptation 等字段）
data/uk/lines.js    摘句（text_en、text_orig、highlight_en、highlight_orig、place_ids）
images/places/      地点照片（800 px 宽，来自 Wikimedia Commons；署名见 docs/photo-credits.md）
tools/countries.json  国家配置（数据来源的真身）；tools/build_countries.py 生成 data/countries.js
tools/build_geo.py  重新生成 data/<国家>/geo.js 和 data/world-geo.js 的脚本：`python3 -I tools/build_geo.py <admin1> <admin0> uk data/uk/geo.js`，`… world data/world-geo.js`
tools/build_intro_geo.py  重新生成 data/intro-geo.js 的脚本
tools/validate.js   数据校验：`node tools/validate.js [国家代码]`，默认 uk
tools/checks/       页面检查脚本（标签重叠、圆点、对比度、无障碍、中文字符、旅行小旗），见其 README；`tools/checks/run_all.sh` 全跑
tools/content/      内容制作：`batchlib.py`（手写批次的共用函数）、`batches/`（英国各批次原件）、`photos/`（Commons 照片流水线），见其 README
cache/pg/           古登堡原文缓存（不进 git；内容脚本和导入校验用）
docs/week1-uk-spec.md  Week 1 规格说明（执行与验收对照）
docs/map-layers.md  地图分层、标签优先级、海岸线和缩放级别规则
docs/photo-credits.md  地点照片的作者、许可证和原图链接
docs/travel-journal-spec.md  旅行日志与照片的需求（等后端阶段再实现）
docs/plan-week2-5.md  Week 2–5 计划：多国家重构、Supabase 最小后端、数据包导入、演示路线（11-08）
docs/content-pack-spec.md  交给其他 AI 的内容数据包格式（11-08）
packs/               内容数据包：uk/ 是英国样例包，us-brief.md 是美国包的任务说明，existing-ids.json 是已占用的 id
tools/canon-us.json  美国的外部选题名单（tools/build_canon_us.py 生成）
```

## 地图分层与标签（摘要）

改地图相关代码前先看 `docs/map-layers.md`。最要紧的三条：

1. **能点的在最上面。** 图层从下到上依次是：街道底图（只看）→ SVG 大区、郡界、郡名 → 地点标记和地点名 → 框饰和按钮。
2. **标签让位顺序：** 地点名和标记点 > 郡 / 自治市名 > 大区名（只在英国全景，自动避让：在自己区域里找空位，放不下时先缩小字号、再拆成两行）> 底图标签。底图通过一组看不见的“占位”文字知道地点名、标记点、郡名在哪里，碰上就不画。
3. **海岸线只有一条。** 有街道瓦片时，被两个不同区域共用的线段才画成边界；只属于一个区域的线段是海岸线，交给底图。

## 检查数据

每次改完 `data/` 里的文件，运行：

```
node tools/validate.js
```

它会检查 id、引用、高亮词、坐标和必填字段，并列出与本周内容目标的差距。有错误时会逐条列出。

## 加一本书的步骤

1. 在 `data/uk/books.js` 加一条书目（`title`/`author` 只写英文，`title_zh`/`author_zh` 为中文；原作不是英文时，原文书名和作者名写在 `title_orig`/`author_orig`，只用于搜索）。
2. 在 `data/uk/places.js` 加它涉及的地点（每个地点带 `country: "uk"`）（已有的地点直接复用 id）。`name` 为英文、`name_zh` 为中文；说明文字同样成对填写：`note`/`note_en`、`prototype_of`/`prototype_of_en`、`scene`/`scene_en`。坐标要先查到公开出处（维基百科等），把出处写进 `coord_checked`。大区由坐标自动判断。
3. 在 `data/uk/lines.js` 加摘句，`place_ids` 指向地点，`highlight_en` 写要高亮的词。外语原作同时填 `text_orig` 和 `highlight_orig`。`location` 为英文，`location_zh` 为中文。
4. 摘句从公有领域全文复制，不凭记忆录入；书中不相邻的部分之间单独一行 `…`。受版权保护的书不录原文，改写一两句自己的话的场景说明：加 `kind: "scene"`，同时填 `text_en` 和 `text_zh`（页面不会标出它是场景说明）。规则见 `docs/week1-uk-spec.md` 第 6.6 节。
5. 想给地点配照片：只用 Wikimedia Commons 或 Geograph 上许可证为 CC BY、CC BY-SA、CC0 或公有领域的照片（不用 Google 地图或电影截图），缩到 800 px 宽放进 `images/places/<id>.jpg`，在地点上加 `photo` 字段（作者、许可证、许可证链接、原图链接、中英文说明），再重新生成 `docs/photo-credits.md`。
6. 运行 `node tools/validate.js`，然后把 `index.html` 里改过的文件的版本号（`?v=9` 一类）加一，免得浏览器用缓存的旧数据。

## 已知限制

- 种子数据的摘句全部是草稿（`status: "draft"`），英译标为 `own` 的是原型阶段自译，需要审核。
- 地点坐标已全部对照公开坐标核对（出处在每个地点的 `coord_checked`）；高地、达特穆尔等面状地点取其中有代表性的一点。
- 世界其他国家只显示底图，点击会提示第 3–4 周开放。
- 地图边界数据来自 Natural Earth（公有领域）。街道底图：OpenFreeMap © OpenMapTiles，数据 © OpenStreetMap 贡献者，地图右下角有署名。
- 底图需要浏览器支持 WebGL；不支持时只显示大区地图。

## 版本控制与上线（11-09 起）

仓库在 GitHub（私有，演示前转公开给 Pages 用）。第一次：

```sh
cd ~/Documents/readers_atlas
git init -b main
git add -A && git commit -m "The Reader's Atlas: UK version, multi-country data layer"
git remote add origin git@github.com:<你的账号>/readers-atlas.git
git push -u origin main
```

以后每批改动一个 commit。GitHub Pages：仓库 Settings → Pages → Source 选 `main` / 根目录，几分钟后地址是 `https://<账号>.github.io/readers-atlas/`。本地双击 `index.html` 仍然能用。`_to_delete/`、`cache/` 不进 git（见 `.gitignore`）。
