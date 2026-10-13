# Changelog

All notable changes to Mindlook are recorded here. Dates are ISO (YYYY-MM-DD).

## 0.2.0 — 2026-10-13

### Added
- **New input formats**, all rendered through the same tree model as XMind: FreeMind / Freeplane `.mm` (nodes, rich-text titles and notes, built-in icons as markers, attributes as labels, folded state), OPML `.opml` (`text`, `_note`, links, checked items), Markdown `.md` (headings become levels, nested and task lists become children, paragraphs / quotes / code blocks become notes, a single leading `# title` is the root) and tab- or space-indented text outlines `.txt`. Format is detected by extension first, then by content (zip signature, `<map`, `<opml`, Markdown syntax). UTF-8 with BOM and GBK text are decoded.
- **Export menu** (`Ctrl/⌘ + E`): Markdown outline (nested `-` list, notes as indented blockquotes, labels / markers as inline tags, hyperlinks kept), plain-text outline (tab-indented), standalone SVG (shapes and text with resolved colours and fonts, connectors as paths, images embedded; no CSS variables, no `foreignObject`, no external references) and PNG at 2× (blob URL first, `data:` URL fallback for a tainted canvas, SVG fallback if PNG is impossible). Files are named after the map title; with several sheets the current one is exported; exports always contain the whole map regardless of folding or focus.
- **Search**: `Ctrl/⌘ + F` opens the in-page search (only intercepted while a map is open), `Enter` / `Shift + Enter` cycle matches and centre the current one (zooming in when the map is far out), `Esc` closes.
- **Keyboard accessibility**: topics are focusable tree items (`role="treeitem"`, `aria-level`, `aria-expanded`, `aria-selected`, roving `tabindex`); `Tab` reaches the selected or root topic, arrow keys move between parent / children / siblings, `Space` / `Enter` fold. Toolbar menus expose `aria-haspopup` / `aria-expanded`, open on the first item, support arrow-key navigation and return focus on `Esc`.
- One sample per format under `samples/` (synthetic content) and CI renders each through the CLI.

### Changed
- `xmindview` CLI accepts `.mm`, `.opml`, `.md` and `.txt` (the raw text is embedded and parsed by the page).
- PWA manifest registers file handlers for the new formats; description updated; service-worker cache bumped to `mindlook-v3`.
- Empty-state copy, help overlay (both languages) and README describe the new formats, exports and shortcuts.
- Markdown export now covers the current sheet only (previously all sheets in one document).

## 0.1.0 — 2026-10-12

- Initial release: single-file offline `.xmind` viewer (XMind 2020+ and XMind 8, password-protected files), pan / zoom, light / dark, Chinese / English, outline view, folding by level, `xmindview` CLI, PWA with offline cache and `.xmind` file handler, CI.
