# IEEE RL Reproducible Training 技能

<p align="right"><a href="README.md">English</a> | <strong>简体中文</strong></p>

一个可复现强化学习训练技能，用于可追踪实验、训练/测试记录分离、IEEE 风格图件与最终产物审计。

本仓库是该技能的 Git 源镜像。仓库文档保留在这里；安装后的运行副本应保持精简，只包含执行所需文件。

## 功能范围

- 为长训练定义实时 CSV、JSONL、stdout 与 checkpoint 记录。
- 区分训练证据、评估证据与训练后报告。
- 通过专用参考文件和脚本路由图件风格、报告包、清单、清理与最终审计。

## 使用场景

当任务与 SKILL.md 中的描述匹配时使用该技能。先阅读 SKILL.md，再按照其中的路由表打开 references、scripts、assets 或索引资源。

典型使用场景：

- 长训练前运行冒烟测试，并创建唯一输出目录。
- 训练期间写入实时记录，训练后运行独立评估。
- 在声称完成前生成报告、图件、清单、风险说明与最终质量门证据。

## 仓库内容

- `agents/`
- `assets/`
- `references/`
- `scripts/`
- `SKILL.md`

## 运行契约

- 不得编造指标、图件、基线或完成声明。
- 保持训练记录与评估记录分离。
- 保留成功运行记录，并标记失败产物，不静默混合。

## 验证与复查

- 修改技能发现元数据前，先检查 SKILL.md frontmatter。
- 保持 Hard Gates、Reference Routing 与 Verification 和仓库实际文件一致。
- 如果存在 references/final-quality-gates.md，在任何最终、就绪、发布、提交或完成声明前使用它。
- 如果存在技能专用审计脚本，修改路由文件或确定性辅助程序后运行它。

## 维护说明

- 保持 SKILL.md 作为入口和路由器。
- 如果技能包含参考文件，将详细领域材料保存在 references/ 中。
- 将确定性辅助程序放在 scripts/ 或 tools/ 中，并在修改后验证。
- 同步更新 README.md 与 README_zh.md，确保两种语言描述相同的范围与质量门。
- 不要把仅属于仓库的文档移动到安装后的运行副本。

## 语言一致性

README.md 是本文档的英文对应版本。任一 README 变更时，应在同一个提交中同步更新另一种语言版本。
