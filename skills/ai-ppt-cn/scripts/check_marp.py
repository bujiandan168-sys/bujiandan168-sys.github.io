#!/usr/bin/env python3
"""Lint a Marp Markdown deck before export (stdlib only, no network).

Usage:
  python3 scripts/check_marp.py slides.md [--minutes 15]

Checks:
  ERROR  front matter missing or lacks `marp: true`
  ERROR  a slide has no speaker-notes comment (<!-- ... --> that is not a directive)
  WARN   more than 3 bullet points on a slide
  WARN   bullet longer than 20 characters (CJK counted 1 each)
  WARN   slide count far from the 1-2 minutes/slide rule when --minutes is given
  WARN   leftover 【...】 placeholders
Exit code 1 if any ERROR.
"""
import argparse
import re
import sys

DIRECTIVE = re.compile(r"<!--\s*_?(class|paginate|header|footer|backgroundColor|backgroundImage|color|theme)\s*:", re.I)
COMMENT = re.compile(r"<!--(.*?)-->", re.S)
BULLET = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+(.*)$")


def split_slides(text):
    if not text.startswith("---"):
        return None, []
    end = text.find("\n---", 3)
    if end == -1:
        return None, []
    front = text[3:end]
    body = text[end + 4:]
    slides = re.split(r"\n---[ \t]*\n", "\n" + body)
    return front, [s for s in slides if s.strip()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--minutes", type=float, default=0)
    args = ap.parse_args()
    text = open(args.path, encoding="utf-8").read()
    errors, warns = [], []

    front, slides = split_slides(text)
    if front is None:
        errors.append("缺少 front matter（文件应以 --- 开头并闭合）")
    elif not re.search(r"^\s*marp:\s*true\s*$", front, re.M):
        errors.append("front matter 缺少 `marp: true`")

    for i, s in enumerate(slides, 1):
        notes = [c for c in COMMENT.findall(s) if not DIRECTIVE.match("<!--" + c)]
        if not any(n.strip() for n in notes):
            errors.append(f"第 {i} 页没有讲稿注释 <!-- ... -->")
        bullets = [m.group(1) for line in s.splitlines() if (m := BULLET.match(line))]
        if len(bullets) > 3:
            warns.append(f"第 {i} 页有 {len(bullets)} 条要点（建议 ≤3）")
        for b in bullets:
            plain = re.sub(r"[*_`]|\[(.*?)\]\(.*?\)", r"\1", b).strip()
            if len(plain) > 20:
                warns.append(f"第 {i} 页要点过长（{len(plain)} 字）：{plain[:24]}…")
        if "【" in s:
            warns.append(f"第 {i} 页仍有【】占位符")

    n = len(slides)
    print(f"INFO 共 {n} 页")
    if args.minutes and n:
        lo, hi = args.minutes / 2, args.minutes
        if not lo <= n <= hi + 2:
            warns.append(f"{args.minutes:g} 分钟建议 {int(lo)}–{int(hi)} 页（含封面结尾可 +2），当前 {n} 页")

    for w in warns:
        print("WARN", w)
    for e in errors:
        print("ERROR", e)
    print(f"结果：{len(errors)} 个 ERROR，{len(warns)} 个 WARN")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
