#!/usr/bin/env python3
"""检查飞书文档 callout 的 emoji 是否被回退成 💡。

用法：
    python3 check_emoji.py draft.xml          # 检查本地 XML
    python3 check_emoji.py --doc <token>      # 检查已创建的文档（走 lark-cli fetch）

退出码：0 表示 fallback 数为 0，1 表示有回退。
"""
import argparse
import json
import re
import subprocess
import sys


def fetch_content(args):
    if args.doc:
        r = subprocess.run(
            ["lark-cli", "docs", "+fetch", "--doc", args.doc, "--format", "json"],
            capture_output=True, text=True)
        d = json.loads(r.stdout)
        return d["data"]["document"]["content"]
    return open(args.file, encoding="utf-8").read()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file", nargs="?", help="本地 XML 草稿路径")
    ap.add_argument("--doc", help="已创建文档的 token 或 URL")
    args = ap.parse_args()
    if not args.file and not args.doc:
        ap.error("需要 file 或 --doc")
    content = fetch_content(args)
    emojis = re.findall(r'<callout[^>]*emoji="([^"]*)"', content)
    if not emojis:
        print(json.dumps({"fallback_bulb": 0, "emoji": [], "note": "未找到 callout"},
                         ensure_ascii=False))
        return 0
    counts = {}
    for e in emojis:
        counts[e] = counts.get(e, 0) + 1
    fallback = counts.get("💡", 0)
    out = {"fallback_bulb": fallback,
           "emoji": sorted(counts.items(), key=lambda kv: -kv[1])}
    print(json.dumps(out, ensure_ascii=False))
    if fallback:
        print("警告：有 emoji 回退成 💡。写入时已被替换，需按 block_id 整块 block_replace。",
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
