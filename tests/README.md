# Skill 体检 · 规则测试集

用真实 SKILL.md 校准工具站（index.html）里的体检规则，统计误报和漏报。

运行：`node tests/run.js`（加 `--dump` 打印每个样本的命中项）。脚本直接抽出 index.html 里的体检代码执行，测的就是线上那一份规则。

## 样本构成
| 目录 | 数量 | 说明 |
|---|---|---|
| samples/ | 43 | 公开仓库的真实 SKILL.md，原样复制，仅用于规则测试 |
| synthetic/ | 9 | 故意写坏的样本（远程脚本、eval、提示注入、模板化描述等），防止修误报时把真问题放过 |
| ../skills/ | 9 | 本仓库自家 Skill |
| local/ | 13 | 不可再分发的样本（专有许可或未声明许可），只在本地跑，不提交（见 .gitignore） |

## 来源与许可
| 前缀 | 来源 | 提交 | 许可 |
|---|---|---|---|
| anthropics__ | https://github.com/anthropics/skills （ca45fc4） | 15 个 Apache-2.0 的 Skill | Apache-2.0，见 samples/LICENSES/Apache-2.0-anthropics.txt |
| mattpocock__ | https://github.com/mattpocock/skills （4ae2317） | 13 个 | MIT，见 samples/LICENSES/MIT-mattpocock.txt |
| obra__ | https://github.com/obra/superpowers （22f0b46） | 15 个 | MIT，见 samples/LICENSES/MIT-obra.txt |
| local/anthropics__ | anthropics/skills 的 docx、pdf、pptx、xlsx | 不提交 | 专有许可 |
| local/vercel__ | https://github.com/vercel-labs/agent-skills （1a2c79d） | 不提交 | 仓库未声明许可 |

## 标注
expected.json 记录每个样本「应该命中」的检测项，由人工逐条复核。标注原则：
- 英文 description 只要写了 Use when / use for / triggers on / whenever 等触发条件，就不算缺触发语句；「没举用户原话」只对中文描述提示。
- `disable-model-invocation: true` 的 Skill 由用户手动调用，不检查触发语句。
- 散文里的 eval（如 "an eval (prompt tuning…"）不算动态执行，只认 `eval(` 和 shell 的 `eval "$…"`。
- description 里用引号列出的套话（例如「要去掉的赋能、助力」）不算注水。
- name 与文件夹不一致按规范判为严重，即使是 Vercel 官方仓库。

注意：标注和规则修复由同一人完成，100% 只说明规则符合当前标注，不代表没有其他误报；欢迎提 issue 补充反例。
