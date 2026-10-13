# Mindlook

> Mind map viewer for `.xmind`, FreeMind / Freeplane `.mm`, OPML and Markdown — one HTML file, no install, nothing leaves your machine.

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![CI](https://github.com/caiqianha/mindlook/actions/workflows/ci.yml/badge.svg)](https://github.com/caiqianha/mindlook/actions/workflows/ci.yml)

English · [中文](#中文)

![Mindlook screenshot](docs/screenshot.png)

Try it: [caiqianha.github.io/mindlook](https://caiqianha.github.io/mindlook/) (drop in any file from `samples/`: `.xmind`, `.mm`, `.opml`, `.md`, `.txt`).

## What

A read-only mind map viewer written as a single `index.html` with zero dependencies and no build step. It opens:

- **XMind** `.xmind` — unzipped with the browser's native `DecompressionStream`; `content.json` (XMind 2020+) and `content.xml` (XMind 8), including password-protected files
- **FreeMind / Freeplane** `.mm` — nodes, rich-text titles and notes, built-in icons (mapped to markers), attributes (as labels), folded state; arrow links are ignored
- **OPML** `.opml` — `<outline text>` trees, `_note`, links, checked items
- **Markdown** `.md` — headings become levels, list items (including nested and task lists) become children, paragraphs and quotes become notes, a single leading `# title` is the root
- **Text outlines** `.txt` — one topic per line, nested by tab or space indentation

The format is picked by extension, then by sniffing the content (zip signature, `<map`, `<opml`, Markdown syntax). Every format goes through the same internal tree, so layout, search, folding and export behave identically. A small Python CLI (`xmindview`) wraps the same page so you can open a file from the terminal or hand a self-contained HTML to someone who does not have the original app.

## Why

You get sent an `.xmind` file and only want to read it. Installing XMind, signing in, or uploading the file to a web converter is more than that deserves — and the file may be confidential.

## How to use

- **Web**: open `index.html` (or the hosted page), then drag a file in or click *Open file*. Works in Chrome 103+ / Edge 103+ / Safari 16.4+ / Firefox 113+.
- **Install as an app** (Chrome / Edge): use the browser's *Install* action. The PWA works offline and registers as a handler for `.xmind`, `.mm`, `.opml`, `.md` and `.txt`, so double-clicking a file opens it directly.
- **CLI** (macOS / Linux, Python 3):

  ```bash
  ln -s /path/to/mindlook/xmindview ~/bin/xmindview   # or: alias xmindview='python3 -I /path/to/mindlook/xmindview.py'
  xmindview file.xmind              # render and open in the default browser
  xmindview --no-open notes.mm      # render only, print the path (.mm / .opml / .md / .txt work too)
  xmindview -o out.html plan.md     # self-contained page with the data embedded; share it freely
  ```

  Without `-o` the page goes to a private temporary directory created with `mkdtemp` (mode 0700).

### Export

The *Export* menu (`Ctrl/⌘ + E`) offers:

- **Markdown outline** — `-` nested list, notes as indented `>` blockquotes, labels and markers as inline `` `tags` ``, hyperlinks kept (copy to clipboard or download)
- **Plain-text outline** — tab-indented `.txt`
- **SVG** — a standalone vector file: topics as shapes and text with the colours and fonts resolved, connectors copied as paths, images embedded; no CSS variables, no `foreignObject`, no external references
- **PNG** — the same SVG rasterised at 2× (Safari falls back to a `data:` URL if the canvas is tainted; if PNG is impossible, the SVG is downloaded instead)

Downloads are named after the map title. With several sheets the current one is exported. **Exports always contain the whole map** — collapsed branches and the focused-branch view are ignored.

### Search and folding

- `Ctrl/⌘ + F` (or `Ctrl/⌘ + K`, `/`) opens the in-page search; matches are highlighted with a count, `Enter` / `Shift + Enter` move between them and centre the current one, `Esc` closes. The shortcut is only intercepted while a map is open.
- Click the dot next to a topic (or press `Space` / `Enter` on a focused topic) to fold it; the dot then shows how many topics are hidden. *Expand level* in the toolbar (or `1` `2` `3` / `A`) folds the whole map to a depth.
- Topics are focusable: `Tab` reaches the selected (or root) topic, arrow keys move to parent / child / siblings.

### Keyboard shortcuts

| Action | Keys |
|---|---|
| Search | `Ctrl/⌘ + F`, `Ctrl/⌘ + K` or `/`; `Enter` next, `Shift + Enter` previous; `Esc` closes |
| Export menu | `Ctrl/⌘ + E` |
| Zoom / fit to window | `+` `−` / `0` or `F`; `Ctrl/⌘ + wheel` to zoom |
| Collapse to level 1 / 2 / 3 / expand all | `1` `2` `3` / `A` |
| Map / outline | `O` |
| Focus / move between topics / fold | `Tab` / arrow keys / `Space` or `Enter` |
| Focus a branch / back | double-click a topic / `Esc` |
| Help | `?` |

## Privacy

- The file is read with the File API and parsed in the page (all five formats). There is no upload, no `fetch`, no analytics, no CDN script and no web font.
- Password-protected files are decrypted locally with WebCrypto (PBKDF2 + AES); the password never leaves the page.
- The page ships a Content-Security-Policy with `connect-src 'none'`, so the browser itself blocks any outbound request, and CI fails if a URL other than a W3C namespace identifier appears in `index.html` or `sw.js`.
- Nothing is stored except three `localStorage` preferences (language, theme, "tip dismissed").

## What is rendered

XMind 2020+ `content.json` and XMind 8 `content.xml` · FreeMind / Freeplane `.mm` · OPML · Markdown · text outlines · multiple sheets · map, logic, tree, org-chart and timeline structures, per-topic · floating topics · relationships · boundaries · summaries · labels · hyperlinks · images · markers · plain and rich-text notes (bold, lists, links, images) · search · folding · export to Markdown, text, SVG and PNG · light / dark · Chinese / English · touch and mobile.

## Limits

- Files encrypted with the pre-3.7 XMind scheme (PKCS12 key derivation) are not supported; re-save them in a current XMind.
- Fishbone and matrix layouts are approximated with the logic / tree layouts. Callouts are not rendered.
- Topic colours, fonts and themes stored in the file are ignored; Mindlook uses its own palette.
- Markers are drawn as simple glyphs (priority number, flag, star, task progress, …), not XMind's icons.
- Only `http(s)` hyperlinks are clickable; links to other topics (`xmind:#…`) and attached non-image files are not shown.
- The CLI embeds at most 20 MB of images per file; images beyond that are skipped with a notice.
- FreeMind arrow links, clouds and per-node fonts are ignored; Markdown tables and HTML blocks end up as notes text.
- Viewing only — no editing.

## Project layout

```
index.html        the viewer (also the CLI's template)
manifest.webmanifest / sw.js / icons/   PWA: install, offline cache, file handlers
xmindview.py      CLI: parse .xmind (or embed .mm/.opml/.md/.txt as-is), build the page, open it
xmindview         shell wrapper (resolves symlinks, runs the CLI with python3 -I)
samples/          one sample per format: .xmind, .mm, .opml, .md, .txt
docs/             screenshot used by this README
CHANGELOG.md      release notes
.github/          CI workflow and issue templates
```

MIT licensed. Mindlook is not affiliated with XMind Ltd.; XMind is a trademark of XMind Ltd.

---

## 中文

思维导图查看器：支持 `.xmind`、FreeMind / Freeplane `.mm`、OPML 和 Markdown。单个 HTML 文件，零依赖，文件只在浏览器本地解析，不上传。

[English](#mindlook) · 中文

![Mindlook 截图](docs/screenshot.png)

在线试用：[caiqianha.github.io/mindlook](https://caiqianha.github.io/mindlook/) ，仓库 `samples/` 里每种格式各有一个示例（`.xmind` `.mm` `.opml` `.md` `.txt`）可以拿来试。

## 特点

- **零依赖、离线可用**：一个 `index.html` 就是全部，用浏览器原生接口解压，没有任何外部脚本
- **五种格式**：XMind 2020+（content.json）和 XMind 8（content.xml）、FreeMind / Freeplane `.mm`（节点、富文本标题与备注、内置图标、属性、折叠状态）、OPML（`<outline text>`、`_note`、链接）、Markdown（标题分层、列表成子节点、段落与引用成备注、开头单个 `# 标题` 作为根）、缩进文本大纲 `.txt`。先按扩展名识别，再按内容嗅探，统一转成同一套节点结构
- **结构类型**：思维导图、逻辑图、树形图、组织结构图、时间轴，按文件里每个节点自己的结构设置来排布
- **完整展示**：多画布、富文本备注（加粗、列表、链接、图片）、标签、超链接、图片、标记、浮动主题、关系线、外框、概要
- **密码保护文件**：输入密码后在浏览器里本地解密（WebCrypto），XMind 8 和 2020+ 两种加密格式都支持
- **搜索与折叠**：⌘F / ⌘K 页内搜索，高亮并显示匹配数，Enter / Shift+Enter 在匹配间跳转并居中，Esc 关闭（没打开导图时不抢浏览器的 ⌘F）；点节点旁的圆点或在聚焦节点上按空格 / Enter 折叠，圆点显示隐藏的节点数；工具栏「展开层级」按深度折叠；Tab 可聚焦节点，方向键在父子、兄弟间移动
- **导出**（⌘E）：Markdown 大纲（`-` 嵌套列表、备注为缩进引用、标签与标记为行内 `` `标签` ``、保留超链接；可复制或下载）、Tab 缩进的文本大纲、独立 SVG（形状 + 文字，颜色字体已写死，无 CSS 变量、无 foreignObject、无外部引用）、PNG（2 倍分辨率；Safari 画布被污染时退回 data: URL，再不行就改下 SVG）。文件名取导图标题，多画布时导出当前画布，**始终导出完整导图**（忽略折叠与聚焦）
- **界面**：浅色 / 深色跟随系统，中英文，手机上也能用，首次使用有操作提示，按 `?` 看快捷键
- **命令行**：复制文件路径，一条命令在浏览器打开

## 使用

### 网页

双击打开 `index.html`，把 `.xmind` 文件拖进去，或点「打开文件」。
也可以部署到任何静态托管（GitHub Pages 等），用户直接访问网址即可。

需要 Chrome 103+ / Edge 103+ / Safari 16.4+ / Firefox 113+。

### 安装为应用（推荐）

用 Chrome 或 Edge 打开在线地址，点右上角「⋯」→「安装为应用」（或地址栏右侧的安装图标）。安装后：

- 可以离线使用
- 在系统里把 .xmind / .mm / .opml / .md / .txt 文件的打开方式设为 Mindlook，之后**双击文件就直接打开**（Chrome / Edge 桌面版支持）

### 命令行（macOS / Linux，需要 Python 3）

```bash
# 加一个别名（写进 ~/.zshrc 或 ~/.bashrc）
alias xmindview='python3 -I /path/to/mindlook/xmindview.py'

xmindview 文件.xmind                 # 生成网页并用默认浏览器打开
xmindview --no-open 笔记.mm          # 只生成，打印路径（.mm / .opml / .md / .txt 同样可以）
xmindview -o 输出.html 计划.md       # 指定输出位置（可分享给别人，单文件自带数据）
```

生成的 HTML 已内嵌导图数据和图片，拷给没有 XMind 的同事也能直接打开。

## 快捷键

| 操作 | 按键 |
|---|---|
| 搜索 | `⌘F`、`⌘K` 或 `/`，`Enter` 下一个，`Shift+Enter` 上一个，`Esc` 关闭 |
| 导出菜单 | `⌘E` |
| 缩放 / 适应窗口 | `+` `−` / `0` 或 `F`，`⌘ + 滚轮` 缩放 |
| 折叠到第 1/2/3 级 / 全部展开 | `1` `2` `3` / `A` |
| 导图 / 大纲切换 | `O` |
| 聚焦节点 / 节点间移动 / 折叠 | `Tab` / 方向键 / 空格或 `Enter` |
| 聚焦某一分支 / 返回 | 双击节点 / `Esc` |
| 帮助 | `?` |

Windows / Linux 上把 `⌘` 换成 `Ctrl`。

## 已知限制

- XMind 3.7 之前的旧加密方式（PKCS12 密钥派生）不支持，需在 XMind 中重新保存
- 鱼骨图、矩阵按逻辑图/树形图近似显示；标注（callout）暂不显示
- 不沿用文件里的节点颜色和主题，统一用 Mindlook 配色
- FreeMind 的箭头线、云朵和字体设置忽略；Markdown 的表格与 HTML 块作为备注文本保留
- 不支持编辑

## 项目结构

```
index.html        查看器本体（也是命令行的模板）
manifest.webmanifest / sw.js / icons/   PWA：安装、离线、文件关联
xmindview.py      命令行：解析 .xmind（.mm/.opml/.md/.txt 原文内嵌），生成 HTML 并打开
xmindview         shell 包装
samples/          每种格式一个示例：.xmind .mm .opml .md .txt
docs/             README 用到的截图
CHANGELOG.md      版本记录
```

## 许可

MIT。Mindlook 与 XMind Ltd. 无关，XMind 是 XMind Ltd. 的商标。
