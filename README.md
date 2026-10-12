# Mindlook

> View `.xmind` mind maps in your browser — one HTML file, no install, nothing leaves your machine.

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![CI](https://github.com/caiqianha/mindlook/actions/workflows/ci.yml/badge.svg)](https://github.com/caiqianha/mindlook/actions/workflows/ci.yml)

English · [中文](#中文)

![Mindlook screenshot](docs/screenshot.png)

Try it: [caiqianha.github.io/mindlook](https://caiqianha.github.io/mindlook/) (drop in `samples/sample.xmind`).

## What

A read-only viewer for XMind files, written as a single `index.html` with zero dependencies and no build step. It unzips the file with the browser's native `DecompressionStream`, parses `content.json` (XMind 2020+) or `content.xml` (XMind 8) and lays the map out itself. A small Python CLI (`xmindview`) wraps the same page so you can open a file from the terminal or hand a self-contained HTML to someone who does not have XMind.

## Why

You get sent an `.xmind` file and only want to read it. Installing XMind, signing in, or uploading the file to a web converter is more than that deserves — and the file may be confidential.

## How to use

- **Web**: open `index.html` (or the hosted page), then drag a file in or click *Open file*. Works in Chrome 103+ / Edge 103+ / Safari 16.4+ / Firefox 113+.
- **Install as an app** (Chrome / Edge): use the browser's *Install* action. The PWA works offline and registers as a handler for `.xmind`, so double-clicking a file opens it directly.
- **CLI** (macOS / Linux, Python 3):

  ```bash
  ln -s /path/to/mindlook/xmindview ~/bin/xmindview   # or: alias xmindview='python3 -I /path/to/mindlook/xmindview.py'
  xmindview file.xmind              # render and open in the default browser
  xmindview --no-open file.xmind    # render only, print the path
  xmindview -o out.html file.xmind  # self-contained page with the data embedded; share it freely
  ```

  Without `-o` the page goes to a private temporary directory created with `mkdtemp` (mode 0700).

### Keyboard shortcuts

| Action | Keys |
|---|---|
| Search | `Ctrl/⌘ + K` or `/`; `Enter` next, `Shift + Enter` previous |
| Zoom / fit to window | `+` `−` / `0` or `F`; `Ctrl/⌘ + wheel` to zoom |
| Expand to level 1 / 2 / 3 / all | `1` `2` `3` / `A` |
| Map / outline | `O` |
| Move between topics / collapse | Arrow keys / `Space` |
| Focus a branch / back | double-click a topic / `Esc` |
| Help | `?` |

## Privacy

- The file is read with the File API and parsed in the page. There is no upload, no `fetch`, no analytics, no CDN script and no web font.
- Password-protected files are decrypted locally with WebCrypto (PBKDF2 + AES); the password never leaves the page.
- The page ships a Content-Security-Policy with `connect-src 'none'`, so the browser itself blocks any outbound request, and CI fails if a URL other than a W3C namespace identifier appears in `index.html` or `sw.js`.
- Nothing is stored except three `localStorage` preferences (language, theme, "tip dismissed").

## What is rendered

Both formats (XMind 2020+ `content.json`, XMind 8 `content.xml`) · multiple sheets · map, logic, tree, org-chart and timeline structures, per-topic · floating topics · relationships · boundaries · summaries · labels · hyperlinks · images · markers · plain and rich-text notes (bold, lists, links, images) · export to Markdown, PNG and SVG · light / dark · Chinese / English · touch and mobile.

## Limits

- Files encrypted with the pre-3.7 XMind scheme (PKCS12 key derivation) are not supported; re-save them in a current XMind.
- Fishbone and matrix layouts are approximated with the logic / tree layouts. Callouts are not rendered.
- Topic colours, fonts and themes stored in the file are ignored; Mindlook uses its own palette.
- Markers are drawn as simple glyphs (priority number, flag, star, task progress, …), not XMind's icons.
- Only `http(s)` hyperlinks are clickable; links to other topics (`xmind:#…`) and attached non-image files are not shown.
- The CLI embeds at most 20 MB of images per file; images beyond that are skipped with a notice.
- Viewing only — no editing.

## Project layout

```
index.html        the viewer (also the CLI's template)
manifest.webmanifest / sw.js / icons/   PWA: install, offline cache, .xmind file handler
xmindview.py      CLI: parse .xmind, embed the data into the page, open it
xmindview         shell wrapper (resolves symlinks, runs the CLI with python3 -I)
samples/          sample .xmind
docs/             screenshot used by this README
.github/          CI workflow and issue templates
```

MIT licensed. Mindlook is not affiliated with XMind Ltd.; XMind is a trademark of XMind Ltd.

---

## 中文

不装 XMind 也能查看 `.xmind` 思维导图。单个 HTML 文件，零依赖，文件只在浏览器本地解析，不上传。

[English](#mindlook) · 中文

![Mindlook 截图](docs/screenshot.png)

在线试用：[caiqianha.github.io/mindlook](https://caiqianha.github.io/mindlook/) ，仓库自带的 `samples/sample.xmind` 可以拿来试。

## 特点

- **零依赖、离线可用**：一个 `index.html` 就是全部，用浏览器原生接口解压，没有任何外部脚本
- **两种格式**：XMind 2020+（content.json）和 XMind 8（content.xml）
- **结构类型**：思维导图、逻辑图、树形图、组织结构图、时间轴，按文件里每个节点自己的结构设置来排布
- **完整展示**：多画布、富文本备注（加粗、列表、链接、图片）、标签、超链接、图片、标记、浮动主题、关系线、外框、概要
- **密码保护文件**：输入密码后在浏览器里本地解密（WebCrypto），XMind 8 和 2020+ 两种加密格式都支持
- **阅读工具**：搜索（⌘K）、按层级展开、双击聚焦某一分支、方向键在节点间移动、大纲视图
- **导出**：Markdown（复制或下载）、PNG、SVG
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
- 在系统里把 .xmind 文件的打开方式设为 Mindlook，之后**双击文件就直接打开**（Chrome / Edge 桌面版支持）

### 命令行（macOS / Linux，需要 Python 3）

```bash
# 加一个别名（写进 ~/.zshrc 或 ~/.bashrc）
alias xmindview='python3 -I /path/to/mindlook/xmindview.py'

xmindview 文件.xmind                 # 生成网页并用默认浏览器打开
xmindview --no-open 文件.xmind       # 只生成，打印路径
xmindview -o 输出.html 文件.xmind    # 指定输出位置（可分享给别人，单文件自带数据）
```

生成的 HTML 已内嵌导图数据和图片，拷给没有 XMind 的同事也能直接打开。

## 快捷键

| 操作 | 按键 |
|---|---|
| 搜索 | `⌘K` 或 `/`，`Enter` 下一个，`Shift+Enter` 上一个 |
| 缩放 / 适应窗口 | `+` `−` / `0` 或 `F` |
| 展开到第 1/2/3 级 / 全部 | `1` `2` `3` / `A` |
| 导图 / 大纲切换 | `O` |
| 节点间移动 / 折叠 | 方向键 / 空格 |
| 聚焦某一分支 / 返回 | 双击节点 / `Esc` |
| 帮助 | `?` |

## 已知限制

- XMind 3.7 之前的旧加密方式（PKCS12 密钥派生）不支持，需在 XMind 中重新保存
- 鱼骨图、矩阵按逻辑图/树形图近似显示；标注（callout）暂不显示
- 不沿用文件里的节点颜色和主题，统一用 Mindlook 配色
- 不支持编辑

## 项目结构

```
index.html        查看器本体（也是命令行的模板）
manifest.webmanifest / sw.js / icons/   PWA：安装、离线、.xmind 文件关联
xmindview.py      命令行：解析 .xmind，内嵌数据生成 HTML 并打开
xmindview         shell 包装
samples/          示例 .xmind 文件
docs/             README 用到的截图
```

## 许可

MIT。Mindlook 与 XMind Ltd. 无关，XMind 是 XMind Ltd. 的商标。
