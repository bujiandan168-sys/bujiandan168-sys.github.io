#!/usr/bin/env python3
"""Offline self-check for Chinese marketing copy (Xiaohongshu / WeChat / Douyin).

Pure standard library. Reads local text only; makes no network calls and
writes nothing to disk.

Usage:
  python3 scripts/check_copy.py --platform xhs --title "标题" --body-file note.txt
  python3 scripts/check_copy.py --platform wechat --title "标题" --digest "摘要"
  python3 scripts/check_copy.py --platform douyin --body-file script.txt --seconds 45
  echo "正文" | python3 scripts/check_copy.py --platform xhs --title "标题" --body-file -

Exit code 0 = no blocking issue, 1 = at least one ERROR, 2 = bad arguments.
"""
import argparse
import re
import sys

# Platform hard limits verified 2026-11 (see SKILL.md "Gotchas" for sources).
LIMITS = {
    "xhs": {"title": 20, "body": 1000},
    "wechat": {"title": 64, "digest": 120},
    "douyin": {},
}

# Absolute / superlative terms (Advertising Law art. 9(3)) and medical-claim
# terms (art. 17). Heuristic list: a hit means "review this", not "illegal".
ABSOLUTE_TERMS = [
    "最好", "最佳", "最强", "最便宜", "最低价", "最高级", "最优", "最先进",
    "第一", "No.1", "NO.1", "顶级", "极品", "首选", "国家级", "世界级",
    "全网最低", "100%", "百分百", "绝对", "永久", "万能", "王牌",
]
MEDICAL_TERMS = [
    "治疗", "治愈", "根治", "药到病除", "消炎", "祛痘", "祛斑", "减肥",
    "降血压", "降血糖", "防癌", "抗癌", "排毒", "疗效", "处方",
]
INDUCE_SHARE = ["转发到", "分享到朋友圈", "集赞", "转发后", "不转不是", "必转"]

CONTACT_PATTERNS = [
    (re.compile(r"1[3-9]\d{9}"), "疑似手机号"),
    (re.compile(r"https?://\S+|www\.\S+", re.I), "外部链接"),
    (re.compile(r"(微信|vx|VX|v信|wx|WX|薇信|威信)\s*[:：号]?\s*[A-Za-z][-_A-Za-z0-9]{5,19}"), "疑似微信号"),
    (re.compile(r"二维码|扫码"), "二维码/扫码字样"),
    (re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"), "邮箱"),
]


def read_text(value, path):
    if path == "-":
        return sys.stdin.read()
    if path:
        with open(path, encoding="utf-8") as fh:
            return fh.read()
    return value or ""


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--platform", choices=sorted(LIMITS), required=True)
    ap.add_argument("--title", default="")
    ap.add_argument("--digest", default="", help="WeChat summary (摘要)")
    ap.add_argument("--body", default="")
    ap.add_argument("--body-file", default="", help="path to body text, or - for stdin")
    ap.add_argument("--seconds", type=float, default=0, help="Douyin target duration")
    args = ap.parse_args()

    try:
        body = read_text(args.body, args.body_file)
    except OSError as exc:
        print(f"ERROR 读取正文失败: {exc}")
        return 2

    errors, warns = [], []
    lim = LIMITS[args.platform]

    for field, text in (("title", args.title), ("digest", args.digest), ("body", body)):
        if field in lim and text:
            n = len(text.strip())
            if n > lim[field]:
                errors.append(f"{field} 长度 {n} 超过上限 {lim[field]}")
            else:
                print(f"OK   {field} 长度 {n}/{lim[field]}")

    if args.platform == "xhs" and args.title and len(args.title.strip()) > 18:
        warns.append("标题 >18 字：部分机型两行显示会挤，建议 ≤18 字")

    if args.platform == "douyin" and args.seconds:
        chars = len(re.sub(r"\s", "", body))
        rate = chars / args.seconds if args.seconds else 0
        print(f"INFO 口播 {chars} 字 / {args.seconds:g} 秒 = {rate:.1f} 字/秒")
        if rate > 5.0:
            warns.append("语速 >5 字/秒，念不完，删字或加时长")
        elif rate < 3.5:
            warns.append("语速 <3.5 字/秒，节奏偏慢，可加信息点或缩短时长")

    full = "\n".join([args.title, args.digest, body])
    for term in ABSOLUTE_TERMS:
        if term in full:
            warns.append(f"绝对化用语「{term}」：改写，或确认属于可证实的事实/自我比较")
    for term in MEDICAL_TERMS:
        if term in full:
            warns.append(f"医疗/功效用语「{term}」：非医疗类商品不得使用")
    if args.platform == "wechat":
        for term in INDUCE_SHARE:
            if term in full:
                errors.append(f"疑似诱导分享「{term}」：微信平台禁止")
    if args.platform in ("xhs", "douyin"):
        # XHS: verified hard rule (交易导流违规管理细则). Douyin: flagged for review.
        sink = errors if args.platform == "xhs" else warns
        for pat, label in CONTACT_PATTERNS:
            for m in pat.finditer(full):
                sink.append(f"{label}「{m.group(0)}」：疑似站外导流，删除或改用平台组件")
    if "【待补充" in full:
        warns.append("仍有【待补充】占位，发布前替换为真实信息")

    for w in warns:
        print(f"WARN {w}")
    for e in errors:
        print(f"ERROR {e}")
    print(f"结果：{len(errors)} 个 ERROR，{len(warns)} 个 WARN")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
