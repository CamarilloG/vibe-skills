#!/usr/bin/env python3
"""统计飞书文档里的原生组件数量，用于交付前核对。

用法：
    python3 count_blocks.py draft.xml        # 本地 XML
    python3 count_blocks.py --doc <token>    # 已创建的文档
"""
import argparse
import json
import subprocess

TAGS = ["<grid", "<callout", "<html5-block", "<whiteboard", "<table", "<colgroup",
        "<img", "<source", "<li", "<h1", "<h2"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file", nargs="?")
    ap.add_argument("--doc")
    args = ap.parse_args()
    if args.doc:
        r = subprocess.run(["lark-cli", "docs", "+fetch", "--doc", args.doc, "--format", "json"],
                           capture_output=True, text=True)
        d = json.loads(r.stdout)
        content = d["data"]["document"]["content"]
        rev = d["data"]["document"].get("revision_id")
    else:
        content = open(args.file, encoding="utf-8").read()
        rev = None
    out = {t.strip("<"): content.count(t) for t in TAGS}
    out["_chars"] = len(content)
    if rev is not None:
        out["_revision"] = rev
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
