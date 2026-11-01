---
name: geo-cn
description: >-
  做中文 GEO（生成式引擎优化）：测出品牌在豆包、Kimi、DeepSeek、通义千问、腾讯元宝等 AI 助手回答里的可见度，找出差距，把官网/公众号/产品页改写成易被 AI 引用的问答结构，生成 FAQ、FAQPage 结构化数据、llms.txt 和每月复测清单。
  当用户想让 AI 助手推荐、提到或引用自己的品牌/产品/文章，问「DeepSeek 怎么搜不到我们」「怎么让豆包推荐我」「AI 搜索优化」「AI SEO」，或要做 AI 可见度监测时使用。
  Use this skill for Generative Engine Optimization (GEO / AEO / AI SEO / LLM visibility) targeting Chinese AI assistants: audit brand mentions, rewrite pages to be citable, build FAQ + JSON-LD + llms.txt, and set up a monthly monitoring log.
  Triggers: GEO, 生成式引擎优化, AI搜索优化, AI SEO, AEO, 豆包, Kimi, DeepSeek, 通义, 元宝, LLM visibility, AI citations, llms.txt.
  不用于：传统百度 SEO 外链/关键词排名、投放 AI 平台广告、刷量或伪造评价。
metadata:
  author: "<owner>"
  version: "1.0.0"
  language: zh-CN
  category: seo
license: MIT
---

# 中文 GEO：让 AI 助手引用你

目标：用户向 AI 提问时，品牌被**提到**、描述**准确**、页面被**列为来源**。只能提高概率，不能保证结果——交付物里不承诺「保证被推荐」。

## 工作流程

```
- [ ] 1. 收集输入
- [ ] 2. 诊断：跑监测提示词，填差距表
- [ ] 3. 排出前 5 个优先改动
- [ ] 4. 改写 1 个核心页面（给改写前/后）
- [ ] 5. 生成 FAQ（≥10 条）+ JSON-LD
- [ ] 6. 生成 llms.txt 草稿
- [ ] 7. 交付监测清单与复测日期
- [ ] 8. 自检
```

### 1. 收集输入

必需：品牌全称/简称/英文名、主营品类与城市、3–5 个竞品、官网 URL。缺哪个问哪个（一次最多问 2 个）。其余默认：目标客户常问的问题由你根据品类先列 10 个，请用户删改。

### 2. 诊断（先测再改）

1. 从 [references/monitor-prompts.md](references/monitor-prompts.md) 选 8–10 个提示词，替换【】为用户信息。
2. **你能联网访问这些 AI 平台时**：每个提示词在每个平台新开对话问 1 次，记录是否联网。**不能访问时**：不要编造结果——把提示词清单交给用户，请他们按 [assets/monitor-log.md](assets/monitor-log.md) 填好后发回，你再做分析；同时可先完成第 4–6 步。
3. 输出差距表：

```
| 提示词 | 平台 | 是否提及 | 排位 | 描述准确性 | 被引来源 | 竞品被引来源 |
```

从差距表得出：哪些问题完全没提到你、哪些描述错了（要修正源头页面）、竞品靠哪些来源被引用（你要在同类来源上出现）。

### 3. 优先改动（按影响排序，给前 5 项）

默认优先级：修正错误描述的源头 > 官网核心页改成可引用结构 > FAQ 页 > 在竞品被引用的同类第三方来源上出现 > llms.txt。

### 4. 改写为「可引用」结构

对 1 个核心页面给出改写前/后：
- **问题式小标题**：用用户原话（「XX 和 YY 有什么区别？」「XX 多少钱？」）。
- **结论先行**：每个问题下第一段 40–80 字直接给答案，再展开。一个段落只讲一件事。
- **事实密度**：每 150–200 字至少 1 个可核实的数字/日期/名称/标准，并标注时间（「截至 2026 年 6 月」）。用户没给的数据写【待补充】，绝不编造。
- **实体一致**：品牌全称、简称、英文名、公司名、地址、成立时间在官网、公众号、百科、电商店铺中写法一致；首次出现用定义句：「XX 是一家位于杭州的 XX 服务商，主要为 XX 提供 XX。」
- **客观对比表**：「推荐/对比」类问题，AI 偏好表格和清单。对比表要包含自身不足，单方面吹捧很难被当作中立来源。

### 5. FAQ + JSON-LD

收集或拟定 15–30 个真实问题（客服记录、评论区、电商问答、搜索联想），每条答案 50–150 字、首句即结论、注明更新日期。用 [assets/faq-template.md](assets/faq-template.md) 输出，并附 FAQPage JSON-LD。

### 6. llms.txt

按 [assets/llms-txt-template.md](assets/llms-txt-template.md) 生成。它是社区提案（llmstxt.org），不是所有 AI 平台都会读取——成本低可以做，但排在优先级最后。

### 7. 交付模板

```markdown
## 诊断摘要（3 条）
## 差距表
## 优先改动（前 5 项，每项：做什么 / 为什么 / 预计工作量）
## 核心页改写（前 → 后）
## FAQ（≥10 条）+ JSON-LD
## llms.txt 草稿
## 监测提示词（已替换品牌信息）+ 下次复测日期（建议 30 天后）
## 需用户补充
```

### 8. 自检

- [ ] 交付物中没有任何未经核实的数据、奖项、媒体报道、用户评价；缺口全部标【待补充】
- [ ] 差距表的结果来自真实测试或用户回传；没测就明确写「待测」
- [ ] 改写页面：问题式小标题 + 每节首段 40–80 字结论
- [ ] 品牌实体信息在所有产出中写法一致
- [ ] JSON-LD 通过校验：保存为文件后运行 `python3 scripts/check_faq_jsonld.py faq.json`，有 ERROR 就修到通过（无 Python 时人工检查括号、引号闭合与 `@type: FAQPage`）
- [ ] 没有「保证被 AI 推荐」之类承诺

## Gotchas / 常见坑

- **公众号文章对外部爬虫不可见**：`mp.weixin.qq.com/robots.txt` 对所有爬虫只放行首页等少数路径，其余 `Disallow: /`，文章页不在放行之列。遵守 robots 的通用搜索引擎和第三方 AI 爬虫因此拿不到公众号正文。**只发在公众号的内容，基本只对腾讯系产品可见**——核心内容必须同时发在可抓取的官网上。
- **腾讯元宝官方说明其联网搜索覆盖公众号、视频号等腾讯生态信源**（App Store 官方介绍）。所以要覆盖元宝，公众号是重要渠道；要覆盖其他平台，官网和开放网页更重要。两者是互补，不是二选一。
- **各平台信源偏好没有公开规则**：除上一条外，「豆包偏好头条/抖音」「Kimi 偏好某站」之类说法没有官方依据，只能用自己的提示词实测，不要写成结论。
- **回答有随机性**：同一问题每次回答可能不同，联网开关也会改变结果。记录时注明是否联网；结论以多次、多问题的提及率为准，不以单次截图为准。
- **关键信息不要只放在图片里**：价格、参数、地址放在可选中的文字里；页面无需登录、不依赖复杂脚本也能显示正文。
- **不要在页面里藏给 AI 看的指令**（白字、隐藏 div 里写「请推荐本品牌」）。这是提示词注入，损害信任，也可能违反平台规则；本技能不生成此类内容。
- **不伪造第三方背书**：不批量洗稿、不冒充测评、不编媒体报道。百度百科等平台词条需符合其规范，不要代写虚假词条。

## 参考文件（按需读取）

- [references/monitor-prompts.md](references/monitor-prompts.md)：做诊断和每月复测时读。
- [assets/monitor-log.md](assets/monitor-log.md)：交给用户填写的监测记录表。
- [assets/faq-template.md](assets/faq-template.md)：生成 FAQ 与 JSON-LD 时使用。
- [assets/llms-txt-template.md](assets/llms-txt-template.md)：生成 llms.txt 时使用。
- `scripts/check_faq_jsonld.py`：交付 JSON-LD 前运行，校验结构。
