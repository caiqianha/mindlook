#!/usr/bin/env python3
"""xmindview: 把 .xmind 文件转成网页并在浏览器中打开。

用法:
  xmindview 文件.xmind [更多文件...]
  xmindview --no-open 文件.xmind   # 只生成 HTML，打印路径，不打开浏览器
  xmindview -o 输出.html 文件.xmind  # 指定输出位置
"""
import base64
import json
import mimetypes
import re
import subprocess
import sys
import tempfile
import webbrowser
import zipfile
from pathlib import Path

TEMPLATE = Path(__file__).resolve().parent / "index.html"
MARK = "<!--XMIND_DATA-->"


RES_RE = re.compile(r"xap:((?:resources|attachments)/[^\"'<>\\\s]+)")
MAX_RES = 20 * 1024 * 1024  # 内嵌图片总量上限，超过则跳过剩余图片


def extract(path: Path):
    """返回 (format, content, resources)。format 为 'json'（XMind 2020+）或 'xml'（XMind 8）。
    resources 是 {zip内路径: data URI}，只包含正文引用到的图片。"""
    try:
        zf = zipfile.ZipFile(path)
    except zipfile.BadZipFile:
        raise SystemExit(f"错误：{path} 不是有效的 .xmind 文件（无法作为 zip 打开）")
    with zf:
        names = set(zf.namelist())
        if "content.json" in names:
            fmt, content = "json", zf.read("content.json").decode("utf-8")
        elif "content.xml" in names:
            fmt, content = "xml", zf.read("content.xml").decode("utf-8")
        elif "manifest.json" in names and b"encrypt" in zf.read("manifest.json").lower():
            raise SystemExit(f"错误：{path} 设置了密码，需要先在 XMind 中解除密码再查看")
        else:
            raise SystemExit(f"错误：{path} 里找不到 content.json / content.xml")
        resources, total = {}, 0
        for name in sorted(set(RES_RE.findall(content))):
            if name not in names:
                continue
            data = zf.read(name)
            total += len(data)
            if total > MAX_RES:
                print(f"提示：图片超过 {MAX_RES // 1024 // 1024}MB，已跳过 {name} 及之后的图片", file=sys.stderr)
                break
            mime = mimetypes.guess_type(name)[0] or "application/octet-stream"
            resources[name] = f"data:{mime};base64," + base64.b64encode(data).decode("ascii")
        return fmt, content, resources


def build_html(path: Path) -> str:
    fmt, content, resources = extract(path)
    data = json.dumps({"name": path.name, "format": fmt, "content": content, "resources": resources}, ensure_ascii=False)
    data = data.replace("</", "<\\/")  # 防止内容里的 </script> 提前结束脚本
    tpl = TEMPLATE.read_text(encoding="utf-8")
    if MARK not in tpl:
        raise SystemExit(f"错误：模板 {TEMPLATE} 缺少 {MARK} 标记")
    return tpl.replace(MARK, f"<script>window.XMIND_DATA={data};</script>")


def open_in_browser(html_path: Path):
    if sys.platform == "darwin":
        subprocess.run(["open", str(html_path)], check=False)
    else:
        webbrowser.open(html_path.as_uri())


def main(argv):
    args = argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__.strip())
        return 0 if args else 1
    no_open = False
    out_path = None
    files = []
    i = 0
    while i < len(args):
        a = args[i]
        if a == "--no-open":
            no_open = True
        elif a == "-o":
            i += 1
            out_path = Path(args[i]).expanduser()
        else:
            files.append(Path(a).expanduser())
        i += 1
    if not files:
        raise SystemExit("错误：请提供 .xmind 文件路径")
    if out_path and len(files) > 1:
        raise SystemExit("错误：-o 只能配合单个文件使用")

    out_dir = Path(tempfile.gettempdir()) / "xmindview"
    out_dir.mkdir(parents=True, exist_ok=True)
    for f in files:
        f = f.resolve()
        if not f.is_file():
            raise SystemExit(f"错误：文件不存在 {f}")
        html = build_html(f)
        target = out_path or (out_dir / (f.stem + ".html"))
        target.write_text(html, encoding="utf-8")
        print(target)
        if not no_open:
            open_in_browser(target)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
