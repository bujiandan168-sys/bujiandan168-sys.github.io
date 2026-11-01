#!/usr/bin/env python3
"""Validate a FAQPage JSON-LD block offline (stdlib only, no network).

Usage:
  python3 scripts/check_faq_jsonld.py faq.json
  cat faq.json | python3 scripts/check_faq_jsonld.py -

Checks: valid JSON, @type FAQPage, each Question has name + acceptedAnswer.text,
no leftover 【】 placeholders, answers 20-300 chars. Exit 1 on any ERROR.
"""
import json
import sys


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    src = sys.stdin.read() if sys.argv[1] == "-" else open(sys.argv[1], encoding="utf-8").read()
    errors, warns = [], []
    try:
        data = json.loads(src)
    except json.JSONDecodeError as exc:
        print(f"ERROR 不是合法 JSON：第 {exc.lineno} 行第 {exc.colno} 列 {exc.msg}")
        return 1
    if data.get("@context") not in ("https://schema.org", "http://schema.org", "https://schema.org/"):
        errors.append("@context 应为 https://schema.org")
    if data.get("@type") != "FAQPage":
        errors.append("@type 应为 FAQPage")
    items = data.get("mainEntity") or []
    if not items:
        errors.append("mainEntity 为空")
    for i, q in enumerate(items, 1):
        if q.get("@type") != "Question":
            errors.append(f"第 {i} 条 @type 应为 Question")
        name = (q.get("name") or "").strip()
        ans = ((q.get("acceptedAnswer") or {}).get("text") or "").strip()
        if not name:
            errors.append(f"第 {i} 条缺少 name（问题）")
        if not ans:
            errors.append(f"第 {i} 条缺少 acceptedAnswer.text")
        elif not 20 <= len(ans) <= 300:
            warns.append(f"第 {i} 条答案 {len(ans)} 字，建议 50-150 字")
        if "【" in name + ans:
            warns.append(f"第 {i} 条仍有【】占位符")
    for w in warns:
        print("WARN", w)
    for e in errors:
        print("ERROR", e)
    print(f"共 {len(items)} 条问答；{len(errors)} 个 ERROR，{len(warns)} 个 WARN")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
