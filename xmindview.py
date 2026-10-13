#!/usr/bin/env python3
"""xmindview: 把思维导图文件转成网页并在浏览器中打开。

支持 .xmind（XMind 2020+ / XMind 8，含密码保护）、FreeMind / Freeplane .mm、OPML、
Markdown（.md）和缩进文本大纲（.txt）。非 .xmind 的文件原样内嵌，由页面里的解析器处理。

用法:
  xmindview 文件.xmind [更多文件...]
  xmindview --no-open 文件.mm      # 只生成 HTML，打印路径，不打开浏览器
  xmindview -o 输出.html 文件.md    # 指定输出位置
"""
import argparse
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


def is_encrypted(zf, names):
    """清单里带 encryption-data 的就是密码保护文件（新版 manifest.json / 旧版 META-INF/manifest.xml）。"""
    for m in ("manifest.json", "META-INF/manifest.xml"):
        if m in names and b"encryption-data" in zf.read(m):
            return True
    return False


def read_source_text(path: Path) -> str:
    """非 .xmind 的文本格式：按 UTF-8 读取（去 BOM），失败时退回 GB18030，再退回替换非法字节。"""
    raw = path.read_bytes()
    for enc in ("utf-8-sig", "gb18030"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            pass
    return raw.decode("utf-8", errors="replace")


def extract(path: Path):
    """返回 (format, content, resources)。
    format 为 'json'（XMind 2020+）、'xml'（XMind 8）、'file'（密码保护，整个文件内嵌）
    或 'source'（.mm / .opml / .md / .txt 等文本格式，原文内嵌，由页面识别并解析）。
    resources 是 {zip内路径: data URI}，只包含正文引用到的图片。"""
    if path.suffix.lower() != ".xmind" and not zipfile.is_zipfile(path):
        # .mm / .opml / .md / .txt 或无扩展名的文本：原文内嵌，页面按扩展名和内容识别
        return "source", read_source_text(path), {}
    try:
        zf = zipfile.ZipFile(path)
    except zipfile.BadZipFile:
        raise SystemExit(f"错误：{path} 不是有效的 .xmind 文件（无法作为 zip 打开）")
    with zf:
        names = set(zf.namelist())
        if is_encrypted(zf, names):
            return "file", None, None
        if "content.json" in names:
            fmt, content = "json", zf.read("content.json").decode("utf-8")
        elif "content.xml" in names:
            fmt, content = "xml", zf.read("content.xml").decode("utf-8")
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
    tpl = TEMPLATE.read_text(encoding="utf-8")
    if MARK not in tpl:
        raise SystemExit(f"错误：模板 {TEMPLATE} 缺少 {MARK} 标记")
    if fmt == "file":
        # 密码保护的文件：把原文件整个嵌进网页，由浏览器在本地提示输入密码并解密
        print("提示：这是密码保护文件，打开网页后输入密码即可查看", file=sys.stderr)
        data = json.dumps({"name": path.name, "b64": base64.b64encode(path.read_bytes()).decode("ascii")})
        return tpl.replace(MARK, f"<script>window.XMIND_FILE={data};</script>")
    data = json.dumps({"name": path.name, "format": fmt, "content": content, "resources": resources}, ensure_ascii=False)
    data = data.replace("</", "<\\/")  # 防止内容里的 </script> 提前结束脚本
    return tpl.replace(MARK, f"<script>window.XMIND_DATA={data};</script>")


def open_in_browser(html_path: Path):
    if sys.platform == "darwin":
        subprocess.run(["open", str(html_path)], check=False)
    else:
        webbrowser.open(html_path.as_uri())


def main(argv):
    parser = argparse.ArgumentParser(
        prog="xmindview", description=__doc__.strip(), formatter_class=argparse.RawDescriptionHelpFormatter, add_help=True)
    parser.add_argument("files", nargs="*", metavar="文件", help="要查看的文件（.xmind / .mm / .opml / .md / .txt，可多个）")
    parser.add_argument("--no-open", action="store_true", help="只生成 HTML，打印路径，不打开浏览器")
    parser.add_argument("-o", "--output", metavar="输出.html", help="指定输出位置（只能配合单个文件）")
    if not argv[1:]:
        parser.print_help()
        return 1
    args = parser.parse_args(argv[1:])
    files = [Path(a).expanduser() for a in args.files]
    out_path = Path(args.output).expanduser() if args.output else None
    if not files:
        parser.error("请提供文件路径（.xmind / .mm / .opml / .md / .txt）")
    if out_path and len(files) > 1:
        parser.error("-o 只能配合单个文件使用")

    out_dir = None  # 未指定 -o 时，用仅当前用户可读的私有临时目录（mkdtemp 为 0700）
    for f in files:
        f = f.resolve()
        if not f.is_file():
            raise SystemExit(f"错误：文件不存在 {f}")
        html = build_html(f)
        if out_path:
            target = out_path
        else:
            if out_dir is None:
                out_dir = Path(tempfile.mkdtemp(prefix="xmindview-"))
            target = out_dir / (f.stem + ".html")
        target.write_text(html, encoding="utf-8")
        print(target)
        if not args.no_open:
            open_in_browser(target)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
