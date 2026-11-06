# ATR Skill-Security Benchmark 测试

数据集：ATR Skill-Security Benchmark，作者 Agent Threat Rules (ATR)，MIT 许可。
来源：https://huggingface.co/datasets/Agent-Threat-Rule/atr-skill-benchmark （atr-skill-benchmark.jsonl，498 条：466 良性、32 恶意）。
本目录只把样本当文本读取，**绝不执行**其中任何命令或链接。

运行：`node tests/atr/run-atr.js [--split dev|holdout|all] [--list]`

## 口径
- 判恶意：体检报告「安全风险」里出现 高危 或 中危 项。只有「提示」级（sudo、官方 curl|sh 安装、提到 .env、外部网址等）不算。
- 召回 = 判恶意的恶意样本 / 32；误报率 = 判恶意的良性样本 / 466。
- 防过拟合：按 label 分组、id 排序后奇偶交替，切成 dev（16 恶意 + 233 良性）和 holdout（16 + 233）。改规则时只看 dev 的漏报样本原文；holdout 的 32 个攻击类型互不重复，所以 holdout 召回衡量的是对没见过的攻击类型的泛化。
- 局限：部分规则类别（反弹 shell、DNS 外传等）来自通用安全常识清单，这份清单里也包含 holdout 的攻击类型，所以 holdout 并非完全盲测；holdout 的误报样本 id 在调参过程中看到过一次（但没有读其原文、没有针对它们改规则）。

## 结果（2026-11-06）
| 阶段 | 集合 | 召回 | 误报率 |
|---|---|---|---|
| 基线（改规则前） | 全部 | 16/32 = 50.0% | 90/466 = 19.31% |
| 基线 | dev / holdout | 8/16 / 8/16 | 51/233 / 39/233 |
| 第一次改完规则 | dev / holdout | 16/16 / 14/16 | 5/233 / 4/233 |
| 再按 dev 误报收窄后 | dev | 16/16 = 100% | 1/233 = 0.43% |
| 再按 dev 误报收窄后 | holdout | 14/16 = 87.5% | 2/233 = 0.86% |
| 再按 dev 误报收窄后 | 全部 | 30/32 = 93.8% | 3/466 = 0.64% |

参照：ATR 官方 hunt 模式自报召回 100%、误报 0.20%（1/466）。
仍漏：shadow-dependency（影子依赖）、evasive-10-roleplay（角色扮演式隐性注入），都属于需要语义理解的写法，正则难以泛化。
