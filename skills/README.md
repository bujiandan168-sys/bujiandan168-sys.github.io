<div align="center">

# zh-skills · 中文内容创作 Agent Skills

**小红书 · 抖音/视频号 · 公众号 · 中文 GEO · 中文 PPT · X 热帖编译**

[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-spec%20compliant-4b32c3)](https://agentskills.io/specification)
[![Skills](https://img.shields.io/badge/skills-6-blue)](#技能一览)
[![Version](https://img.shields.io/badge/version-1.0.0-green)](#更新日志)
[![Language](https://img.shields.io/badge/lang-简体中文-red)](#)
[![skills.sh](https://img.shields.io/badge/install-npx%20skills%20add-black)](https://skills.sh)
[![License](https://img.shields.io/badge/license-MIT-green)](../LICENSE)

[English](#english) · [安装](#安装) · [示例](#示例提示词) · [更新日志](#更新日志)

</div>

面向中文创作者与小商家的 6 个 Agent Skills。每个技能都是一个遵循 [Agent Skills 开放规范](https://agentskills.io/specification) 的文件夹：带 YAML 头信息的 `SKILL.md`，加上按需加载的 `references/`、`assets/`、`scripts/` 和用于评测的 `evals/evals.json`。

与通用「写作提示词」的区别：
- **平台硬规则内置**：小红书标题 ≤20 字、正文 ≤1000 字；公众号标题 ≤64 字、摘要 ≤120 字；X 中文按加权字符（汉字计 2）≤280——均已核对官方来源。
- **合规自检**：《广告法》绝对化用语与疗效用语、小红书站外导流、微信诱导分享、AI 生成内容标识。
- **离线校验脚本**：每个技能附带纯 Python 标准库脚本，交付前自动检查字数、违规词、格式（不联网、不写文件）。
- **不编造**：素材缺失处统一标【待补充】，不虚构体验、数据和评价。

## 技能一览

| 技能 | 做什么 | 关键自检 |
|---|---|---|
| [`xiaohongshu-viral`](./xiaohongshu-viral/SKILL.md) | 小红书笔记：选题、5 个标题、封面字、正文、标签、发布建议 | 标题 ≤20 / 正文 ≤1000、导流信息、广告法用语 |
| [`douyin-script`](./douyin-script/SKILL.md) | 抖音/视频号/快手口播：3 秒钩子、按时长校准的口播、分镜表、SRT 字幕 | 语速 3.5–5 字/秒、单一 CTA、AI 内容声明 |
| [`geo-cn`](./geo-cn/SKILL.md) | 中文 GEO：豆包/Kimi/DeepSeek/通义/元宝可见度诊断、可引用改写、FAQ + JSON-LD、llms.txt、月度监测 | JSON-LD 校验、不编造测试结果 |
| [`wechat-article`](./wechat-article/SKILL.md) | 公众号长文：标题、摘要、大纲、Markdown 正文、文末转化 | 标题 ≤64 / 摘要 ≤120、诱导分享 |
| [`ai-ppt-cn`](./ai-ppt-cn/SKILL.md) | 中文 PPT：主线、结论式标题、每页讲稿，交付 Marp Markdown，可导出 PPTX/PDF | 每页 ≤3 要点、讲稿完整、页数匹配时长 |
| [`x-thread-en2cn`](./x-thread-en2cn/SKILL.md) | 英文 X 热帖编译为中文帖（即刻/微博/X 中文串/小红书/公众号） | 出处完整、引用 ≤2 句、X 加权字数 |
| [`short-drama-cn`](./short-drama-cn/SKILL.md) | AI 短剧/漫剧：创意→人物卡→分集大纲→分场剧本→分镜→即梦/可灵提示词 | 角色一致性、每集钩子、合规自检 |

## 目录结构

```
zh-skills/
├── README.md
├── LICENSE                     # 待作者选择
└── skills/
    ├── xiaohongshu-viral/
    │   ├── SKILL.md
    │   ├── references/         # 标题公式、示例、广告合规速查
    │   ├── scripts/check_copy.py
    │   └── evals/evals.json
    ├── douyin-script/          # + assets/storyboard-template.md
    ├── geo-cn/                 # + assets/ (FAQ、llms.txt、监测表) + scripts/check_faq_jsonld.py
    ├── wechat-article/
    ├── ai-ppt-cn/              # + assets/marp-template.md + scripts/check_marp.py
    └── x-thread-en2cn/         # + scripts/x_weighted_len.py
```

## 安装

### 方式一：skills CLI（推荐）

```bash
# 安装全部技能（CLI 会让你选择目标工具）
npx skills add bujiandan168-sys/bujiandan168-sys.github.io

# 只装一个技能到 Claude Code
npx skills add bujiandan168-sys/bujiandan168-sys.github.io --skill xiaohongshu-viral -a claude-code

# 全局安装（所有项目可用）
npx skills add bujiandan168-sys/bujiandan168-sys.github.io -g
```

skills CLI 需要较新的 Node.js（以 [skills CLI 文档](https://github.com/vercel-labs/skills) 为准）。

### 方式二：手动复制

**Claude Code**

```bash
# 全局
mkdir -p ~/.claude/skills && cp -r skills/* ~/.claude/skills/
# 仅当前项目
mkdir -p .claude/skills && cp -r skills/* .claude/skills/
```

**Codex / Cursor / Gemini CLI / GitHub Copilot / OpenCode 等（通用目录）**

```bash
mkdir -p .agents/skills && cp -r skills/* .agents/skills/
```

**Trae / Qwen Code / Windsurf / CodeBuddy / 通义灵码**：分别复制到 `.trae/skills/`、`.qwen/skills/`、`.windsurf/skills/`、`.codebuddy/skills/`、`.lingma/skills/`。

各工具的技能目录可能随版本变化，以其官方文档或 [skills CLI 的支持列表](https://github.com/vercel-labs/skills/blob/main/docs/agents.md) 为准。安装后新开会话即可生效。

## 兼容性

| 项目 | 说明 |
|---|---|
| 规范 | Agent Skills 开放规范；全部技能通过 `skills-ref validate` |
| 已知支持的工具 | Claude Code、Codex、Cursor、Gemini CLI、GitHub Copilot、OpenCode、Trae / Trae CN、Qwen Code、Kimi Code CLI、Windsurf、CodeBuddy、通义灵码等（见 skills CLI 支持列表） |
| 校验脚本 | Python 3.8+，仅标准库；无 Python 时技能会改用人工清单 |
| `ai-ppt-cn` 导出 | Node.js（`npx`）+ Chrome / Edge / Firefox 之一；可编辑 PPTX 另需 LibreOffice |
| 网络 | 技能本身不需要联网；`geo-cn` 的实测步骤需要能访问各 AI 平台（无法访问时会请你回传结果） |

## 示例提示词

技能会根据 `description` 自动触发，直接说需求即可：

- 「帮我给这款手冲咖啡壶写一篇小红书种草笔记，价格 299，我是个人号」
- 「写一条 45 秒的抖音口播，宣传我们社区洗衣店，我自己出镜」
- 「问 DeepSeek 杭州团餐推荐从来不提我们，帮我做 GEO」
- 「把这份季度数据写成公众号复盘文章，读者是同行老板」
- 「把这份会议纪要做成 10 页汇报 PPT，输出 Marp」
- 「把这条英文 thread 编译成即刻长帖」

也可以点名：「用 xiaohongshu-viral 技能写……」

## 评测

每个技能的 `evals/evals.json` 含 3–4 条真实场景提示词和可判定的断言，格式遵循 [Evaluating skills](https://agentskills.io/skill-creation/evaluating-skills)。建议每个用例分别在「装技能 / 不装技能」两种条件下各跑一次，对比断言通过率。

## 校验与安全

```bash
pip install skills-ref
for d in skills/*/; do agentskills validate "$d"; done   # 或 skills-ref validate
```

- 所有脚本仅使用 Python 标准库，只读取你传入的本地文本，不联网、不写文件、不调用子进程。
- 技能正文没有隐藏指令；`geo-cn` 明确拒绝生成「给 AI 看的隐藏文字」。

## 注意事项

- 技能会提示广告法、平台规则与版权要求，但**发布前请自行核对**，本合集不构成法律意见。平台规则会变化，文中平台限制的核对日期为 2026-11。
- 技能不编造数据与体验；【待补充】处请替换为真实信息。
- GEO 只能提高被 AI 引用的概率，无法保证结果。

## 更新日志

### v1.0.0（2026-11-01）

- 6 个技能全部按 Agent Skills 规范重写：`name`/目录一致，`description` 写清「做什么 + 何时用」并含中英文触发词，新增 `metadata.author` / `metadata.version`。
- 仓库改为 `skills/<name>/` 布局（与 anthropics/skills、marketingskills 一致）。
- 正文改为「检查清单 + 默认值 + 交付模板 + 自检步骤」，新增「Gotchas / 常见坑」，长内容移入 `references/`、`assets/`，并写明何时读取。
- 平台限制全部重新核对官方来源；修正公众号摘要上限（120 字，原写 54 字）。
- 新增离线校验脚本：`check_copy.py`（小红书/公众号/抖音）、`check_faq_jsonld.py`、`check_marp.py`、`x_weighted_len.py`。
- 新增每个技能的 `evals/evals.json`。

## 许可证

MIT，见仓库根目录 [LICENSE](../LICENSE)。可免费使用、修改、转载，保留版权声明即可。

## 贡献

欢迎 Issue / PR。新增技能请保持：文件夹名与 `name` 一致（小写字母、数字、连字符），`description` ≤1024 字符并写清「做什么 + 何时用」，`SKILL.md` ≤500 行，附 `evals/evals.json`，提交前运行 `skills-ref validate`。

---

## English

**zh-skills** is a pack of 7 [Agent Skills](https://agentskills.io) for Chinese-language content work. Skill bodies are in Simplified Chinese; descriptions are bilingual so agents and directory search match both Chinese and English queries.

| Skill | What it does |
|---|---|
| `xiaohongshu-viral` | Ready-to-post Xiaohongshu (RedNote) notes: titles ≤20 chars, body ≤1000 chars, hashtags, ad-law check |
| `douyin-script` | Douyin / WeChat Channels / Kuaishou voice-over scripts with hook, shot list and SRT subtitles |
| `geo-cn` | Generative Engine Optimization for Chinese AI assistants (Doubao, Kimi, DeepSeek, Qwen, Yuanbao): audit, rewrite, FAQ + JSON-LD, llms.txt |
| `wechat-article` | Long-form WeChat Official Account articles: title ≤64, digest ≤120, outline, Markdown body |
| `ai-ppt-cn` | Chinese slide decks as Marp Markdown with speaker notes, exportable to PPTX/PDF |
| `x-thread-en2cn` | Adapt English X/Twitter threads into Chinese posts with attribution and X weighted-length checks |
| `short-drama-cn` | Chinese AI short-drama/comic-drama writing: character cards, episode outline, scenes, shot list, video-model prompts, consistency and compliance checks |

**Install**

```bash
npx skills add bujiandan168-sys/bujiandan168-sys.github.io            # all skills, pick your agent
npx skills add bujiandan168-sys/bujiandan168-sys.github.io --skill geo-cn -a claude-code
# or copy manually
cp -r skills/* ~/.claude/skills/            # Claude Code
cp -r skills/* .agents/skills/              # Codex, Cursor, Gemini CLI, Copilot, OpenCode…
```

**Example prompts**: "write a xiaohongshu post for my coffee shop's new latte", "turn this English thread into a Chinese Jike post", "make a 10-slide Chinese status deck in Marp from these notes".

Every skill ships offline, stdlib-only validation scripts and `evals/evals.json` test cases. All skills pass `skills-ref validate`. Platform limits were verified against official sources in Nov 2026; platform rules change, so double-check before publishing. Not legal advice.

**Changelog**: v1.0.0 (2026-11-01) — spec-compliant rewrite, `skills/` layout, gotchas, scripts, evals.
