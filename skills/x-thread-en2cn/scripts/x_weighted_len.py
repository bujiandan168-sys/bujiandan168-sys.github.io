#!/usr/bin/env python3
"""Count X (Twitter) weighted length for each post in a Chinese thread.

Stdlib only, offline. Implements the twitter-text v3 weighting documented at
https://docs.x.com/fundamentals/counting-characters : Latin/common punctuation
weigh 1, CJK and other characters weigh 2, every URL counts 23, limit 280.
Emoji ZWJ sequences are counted per code point, so the result can be slightly
HIGHER than X's own count (safe side).

Usage:
  python3 scripts/x_weighted_len.py thread.txt
  cat thread.txt | python3 scripts/x_weighted_len.py -

Posts are split on lines that start with "1/", "2/" ... ; without numbering,
blank-line-separated blocks are treated as posts. Exit 1 if any post > 280.
"""
import re
import sys

LIMIT = 280
URL = re.compile(r"https?://\S+", re.I)
LIGHT = [(0x0000, 0x10FF), (0x2000, 0x200D), (0x2010, 0x201F), (0x2032, 0x2037)]


def weight(text):
    total = 0
    for m in URL.finditer(text):
        total += 23
    text = URL.sub("", text)
    for ch in text:
        cp = ord(ch)
        total += 1 if any(lo <= cp <= hi for lo, hi in LIGHT) else 2
    return total


def split_posts(text):
    parts = re.split(r"(?m)^(?=\s*\d+\s*/)", text)
    parts = [p.strip() for p in parts if p.strip()]
    if len(parts) <= 1:
        parts = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    return parts


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    src = sys.stdin.read() if sys.argv[1] == "-" else open(sys.argv[1], encoding="utf-8").read()
    bad = 0
    for i, post in enumerate(split_posts(src), 1):
        w = weight(post)
        flag = "OK  " if w <= LIMIT else "OVER"
        bad += w > LIMIT
        print(f"{flag} 第 {i} 条：{w}/{LIMIT}  {post[:18].replace(chr(10), ' ')}…")
    print(f"结果：{bad} 条超长")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
