---
name: ai-ppt-cn
description: >-
  把资料或想法做成中文演示文稿：一句话主线、逐页大纲（标题即结论）、每页 ≤3 个要点、每页口语讲稿，交付可直接导出 PPTX/PDF 的 Marp Markdown，并附导出命令与自检。
  当用户要做 PPT、幻灯片、汇报、述职、路演/融资 deck、培训课件、方案提案、项目复盘，或要把文档、会议纪要、报告转成幻灯片，或要求输出 Marp / Markdown 幻灯片 / pptx 时使用。
  Use this skill to turn notes, reports or ideas into a Chinese slide deck — storyline, slide-by-slide outline, speaker notes — delivered as Marp Markdown that exports to PowerPoint (PPTX) or PDF.
  Triggers: PPT, 幻灯片, 演示文稿, 汇报, 路演, 课件, deck, slides, Marp, pptx, presentation, pitch deck, speaker notes.
  不用于：编辑已有 .pptx 文件的格式/动画、设计海报或单张图片。
metadata:
  author: "<owner>"
  version: "1.0.0"
  language: zh-CN
  category: productivity
license: MIT
---

# 中文 PPT：大纲 → 成稿

把一份资料或一个想法，变成一页一个观点、带讲稿的演示文稿，以 Marp Markdown 交付。

## 工作流程

```
- [ ] 1. 补齐输入（最多问 2 个问题）
- [ ] 2. 写一句话主线
- [ ] 3. 选结构 → 出页面大纲表（先给用户确认）
- [ ] 4. 逐页成稿 + 讲稿，写入 Marp 模板
- [ ] 5. 自检（脚本 + 清单），修到通过
- [ ] 6. 交付 Marp 文件 + 导出说明
```

### 1. 补齐输入

最多问 2 个，优先：**听众是谁、听完要做什么决定**；**讲多久**。未说明时默认：内部工作汇报、15 分钟、10–12 页、16:9。

### 2. 一句话主线

写出「听众看完应记住的一句话」。所有页面标题按顺序读下来，应当就是这句话的展开。

### 3. 结构与大纲

默认结构（按场景选 1 个）：

| 场景 | 结构 |
|---|---|
| 工作汇报（默认） | 结论先行 → 关键数据 → 进展 → 问题与原因 → 下一步 → 需要的支持 |
| 商业路演 | 痛点 → 方案 → 产品演示 → 市场规模 → 商业模式 → 竞争 → 团队 → 数据牵引 → 融资用途 |
| 方案提案 | 客户目标 → 现状诊断 → 方案总览 → 分模块细节 → 排期 → 报价 → 为什么选我们 |
| 培训课件 | 学习目标 → 为什么重要 → 知识点 ×3（讲解+案例+练习）→ 总结 → 测验 |
| 项目复盘 | 目标 vs 结果 → 时间线 → 做对了什么 → 问题根因 → 改进行动 |

大纲表：

```
| 页码 | 页面标题（=结论句） | 核心要点（≤3） | 版式 | 素材/图表 |
```

**标题写成结论**：❌「Q3 销售情况」✅「Q3 销售额同比增长 18%，主要来自新渠道」。

先把大纲交给用户确认；用户已说「直接出完整稿」时，大纲和成稿一起交付。

### 4. 逐页成稿

- 一页一个观点；要点 ≤3 条，每条 ≤20 字。
- 能用图不用字：趋势→折线，对比→柱状，占比→条形（饼图 ≤5 类），流程→箭头。图表给出数据表和图表类型，由用户出图。
- 数据页写清单位、时间、来源；用户没给的数字写【待补充】，不编。
- 中文排版：中文与英文/数字之间加空格；标点用全角。
- **讲稿**：每页 80–200 字口语，写在该页的 `<!-- ... -->` 注释里（导出 PPTX 时成为演讲者备注）。结构：一句承上 → 解释「为什么」→ 一句启下。总讲稿字数 ≈ 时长（分钟）× 200–250 字。

从 [assets/marp-template.md](assets/marp-template.md) 复制 front matter 和版式（封面 `lead`、大字观点 `big`、左右对比 `cols`、三栏卡片 `cards`、图表页、结尾页），不要从零写 CSS。

### 5. 自检（必须执行）

```bash
python3 scripts/check_marp.py slides.md --minutes <时长>
```

检查 `marp: true`、每页是否有讲稿、要点数量与长度、页数与时长是否匹配、残留占位符。ERROR 必须改；无 Python 时按「交付前清单」人工核对。

### 6. 交付模板

~~~markdown
## 主线
<一句话>

## 页面大纲
<大纲表>

## Marp 源文件（保存为 slides.md）
```markdown
<完整 Marp Markdown>
```

## 导出
npx @marp-team/marp-cli@latest slides.md --pptx      # PowerPoint
npx @marp-team/marp-cli@latest slides.md --pdf       # PDF
<如有本地图片，加 --allow-local-files>

## 配图与待补充
- 第 N 页：<图表类型 + 数据>
- 需用户补充：…
~~~

## Gotchas / 常见坑

- **默认导出的 PPTX 文字不可编辑**：Marp CLI 的 `--pptx` 把每页渲染成背景图片（演讲者备注会保留）。用户要在 PowerPoint 里改字，需要 `--pptx --pptx-editable`——这是**实验性**功能，需额外安装 LibreOffice Impress，复杂样式可能报错或走样，且**不保留演讲者备注**。交付时必须把这个取舍告诉用户。
- **导出 PDF/PPTX 需要浏览器**：Marp CLI 转 PDF、PPTX、图片需要本机装有 Chrome、Edge 或 Firefox 之一；需要 Node.js（`npx` 方式）。
- **本地图片默认不加载**：出于安全原因，浏览器转换默认不读本地文件，图片会缺失；用 `--allow-local-files`（只对可信的 Markdown 使用）。
- **中文字体取决于导出机器**：模板的 `font-family` 依次回退 Noto Sans SC / 思源黑体 / 苹方 / 微软雅黑；导出机器一个都没装时中文会显示为方框或被替换字体。
- **分页符 `---` 必须独占一行，且上一行留空**：紧跟在文字行下面的 `---` 会被 Markdown 解析成二级标题（setext 标题），而不是分页。
- **讲稿注释不要以指令名开头**：`<!-- _class: big -->`、`<!-- paginate: false -->` 这类是 Marp 指令，不会成为讲稿；讲稿写在单独的注释里。

## 交付前清单

- [ ] 页面标题串起来就是完整故事，且每个标题是结论句
- [ ] 每页 ≤3 个要点、每条 ≤20 字
- [ ] 每页都有讲稿注释；总讲稿字数与时长匹配
- [ ] 数据有单位、时间、来源；无编造数字
- [ ] front matter 含 `marp: true`，`---` 分页独占一行
- [ ] 已告知 PPTX 默认不可编辑及 `--pptx-editable` 的限制

## 参考文件（按需读取）

- [assets/marp-template.md](assets/marp-template.md)：写 Marp 源文件时必用，包含主题样式与 6 种版式。
- [references/example-milktea-q3.md](references/example-milktea-q3.md)：做经营/工作汇报类、想对齐大纲与讲稿颗粒度时读。
