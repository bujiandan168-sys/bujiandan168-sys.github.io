---
name: grill-me-cn
description: >-
  动笔前先追问：用户给出写作/选题/方案的模糊想法时，一次只问一个问题，逐个追问受众、目的、素材、红线，直到足够具体再交给写作类 skill。
  当用户说「帮我写个…」但信息很少，或说「先帮我想清楚」「拷问我」「grill me」时使用。
  Use this skill to interrogate a vague idea one question at a time before writing.
  Triggers: 追问, 想清楚, 拷问我, grill me, 选题, 需求不清.
  不用于：需求已很具体的直接生成任务。
metadata:
  author: "<owner>"
  version: "0.1.0"
  language: zh-CN
---

# 动笔前先拷问（grill-me-cn）

## 流程
1. 用一句话复述用户想法，请用户确认。
2. 一次只问一个问题，按顺序：谁看？看完要做什么？你手里有什么真实素材/数据？最不想出现什么？成功怎么衡量？
3. 每个问题附你的推荐答案，用户回「行」即可通过。
4. 能从上下文或文件里查到的，不问，直接查。
5. 5 个问题答完（或用户说「够了」），输出「一页纸简报」：受众、目标、核心观点、素材清单、红线。
6. 询问下一步交给哪个 skill（xiaohongshu-viral、douyin-script、wechat-article 等）。

## Gotchas
- 不要一次抛出多个问题。
- 不要在追问阶段开始写正文。
- 用户明确说「直接写」就跳过追问，只列出你做的假设。
