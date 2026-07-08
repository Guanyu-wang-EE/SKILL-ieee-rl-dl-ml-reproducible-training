# IEEE RL/DL/ML Reproducible Training 技能

<p align="right"><a href="README.md">English</a> | <strong>简体中文</strong></p>

本仓库是一个 RL/DRL/DL/ML 可复现训练技能的 Git 源镜像。它把长时间学习实验收束为可审计的研究包：实时记录、无损断点续训 checkpoint 契约、适用时的训练/评估证据分离、长训练 TensorBoard 监控、适用时的同 tier 原始奖励对比、IEEE 风格图件、产物清单与最终质量门。

仓库文档保留在这里。精简的安装运行副本只应包含技能本身执行所需文件。

对于 non-RL、affine-only、DL-only 或 paper-style numerical reproduction，只复用 recordkeeping、IEEE figure、manifest、cleanup 与 final-audit 部分；RL-only 产物只有在项目明确定义时才要求。

## 目录

- [用途](#用途)
- [仓库地图](#仓库地图)
- [如何使用该技能](#如何使用该技能)
- [核心契约](#核心契约)
- [参考文件索引](#参考文件索引)
- [脚本索引](#脚本索引)
- [资产索引](#资产索引)
- [预期项目产物](#预期项目产物)
- [生成项目 README 契约](#生成项目-readme-契约)
- [验证命令](#验证命令)
- [维护说明](#维护说明)
- [语言一致性](#语言一致性)

## 用途

当 RL/DRL/DL/ML 实验的科学结论必须能够从命令追踪到最终报告时使用该技能。它特别适合多智能体强化学习、智能电网仿真、约束强化学习、监督/深度学习 baseline、无人值守长训练、训练后产物打包，以及组会或论文证据审计。

该技能有意保持严格。缺失数据是一种结果，不是编造图件、指标、基线或完成声明的理由。

## 仓库地图

| 路径 | 作用 |
|---|---|
| [`SKILL.md`](SKILL.md) | 入口、硬门、路由表与最小工作流 |
| [`references/`](references/) | 按任务加载的具体规则 |
| [`scripts/`](scripts/) | 确定性验证器与审计辅助脚本 |
| [`assets/`](assets/) | 模板与可复用输出辅助文件 |
| [`agents/`](agents/) | 可选界面元数据 |
| [`README.md`](README.md) | 英文仓库导航 |
| [`README_zh.md`](README_zh.md) | 简体中文仓库导航 |

## 如何使用该技能

1. 先阅读 [`SKILL.md`](SKILL.md)。
2. 按其中 `Reference Routing` 表只加载相关参考文件。
3. 对当前产物运行匹配的确定性脚本。
4. 在任何 final 或 complete 声明前，加载 [`references/final-quality-gates.md`](references/final-quality-gates.md)，并运行相关审计命令。

不要默认加载所有参考文件。该技能的结构是精简入口路由器加聚焦参考文件。

## 核心契约

- 没有冒烟测试、资源检查、实时日志、checkpoint 与 TensorBoard 仪表盘计划，不得开始长训练。
- 长训练只有在用户明确要求或项目计划授权时才使用 subagents；子代理只作为有边界的审查、监控与护栏，科学决策、补丁、停止运行、清理与最终声明由主 agent 负责。
- 长训练一旦打开 subagents，就保持为只读监控，直到最终收口、明确停止，或其负责的产物切片已不再相关；主 agent 等待报告时继续推进非破坏性监控。
- 只有 checkpoint 保存完整训练状态时，才允许称为 full resume / 无损断点续训：policy/actor、critic/value、target networks、optimizers、schedulers/noise/entropy-temperature state、适用时的 replay buffer、RNG states、episode/global-step cursor、best metric state、config hash、git commit 与 resume command。
- 只保存 actor 或 model 的 checkpoint 只能标为 warm start、fine-tuning 或 continuation run，不能标为无损 full resume。
- 不得把 RL-only 产物强加给 non-RL、affine-only、DL-only 或 paper-style numerical reproduction 项目。
- 训练记录与评估记录未分离前，不得声明完成。
- 科学 gate 失败后不得推进阶段；必须使用五循环调试规则并记录证据，再标记 `BLOCKED`。
- 对代码、实验、绘图、报告或指标定义的实质修改，必须运行三轮 reviewer-driven 收口循环；未解决的 P0/P1 发现会阻塞完成声明。
- 重要代码/设计发现必须使用 `Symptom`、`Source`、`Consequence`、`Remedy`；图件/表格/指标审查必须检查数据粒度、分组键、指标方向、归一化与重复计数风险。
- 编辑生成的 Python 实验文件前，必须加载 [`assets/python_file_header_templates.md`](assets/python_file_header_templates.md)；直接使用中文 overview header 字段，不输出字面量 `# 中文为主总览：` 行。
- Buddha ASCII 只用于入口脚本；重要或创新代码块需要简洁中文注释。
- 最终完成前，必须核对 stage contract、报告声明、图轴/legend/文字与实际输出文件。
- Git 提交保留 source/tests/docs/CSV/JSON/figures/gates/reports/manifests/lightweight evidence；排除 raw inputs、logs、caches 与大体积 solver caches，除非明确作为归档证据。
- 不得把不同方法各自的 shaped training-objective reward 当作性能证据直接互比。
- 训练后奖励比较必须使用同 tier 原始环境奖励差值，例如同一尺度的环境 `step()` reward 或 `eval_episodes.csv:reward`。
- 项目根 `README.md` 必须是导航页，用相对链接索引报告、图件、表格、代码、配置、运行记录、验证日志、清单、审计与缺失产物说明。
- 最终报告必须包含风险边界、缺失产物说明、artifact index、SHA256 manifest、适用时的 reviewer-loop 证据与质量门证据。
- 失败、中断、冒烟、短测、pilot 或不可行运行不得混入有效性能均值。
- 清理只可自动删除可复现临时缓存；logs、checkpoints、CSV、manifests、生成图件与实验输出必须有明确 disposable contract 或用户授权后才能删除。

## 参考文件索引

| 参考文件 | 何时加载 |
|---|---|
| [`references/realtime-training-monitoring.md`](references/realtime-training-monitoring.md) | 规划或审计长训练、subagent 审查/监控/护栏、实时 CSV/JSONL/stdout 记录、TensorBoard、full-resume checkpoint、科学 gate、五循环调试、坏 run 处理 |
| [`references/reproducibility-recordkeeping.md`](references/reproducibility-recordkeeping.md) | 撰写或审计项目 `README.md`、`requirements.txt`、`output.md`、运行记录、Python 头注释与复现说明 |
| [`references/post-training-reporting.md`](references/post-training-reporting.md) | 生成报告、图件、表格、artifact index、reproducibility manifest、PPT index、colleague briefing、缺失产物说明 |
| [`references/ieee-plot-style.md`](references/ieee-plot-style.md) | 创建或审查 IEEE 风格图件、caption、SVG/PDF/PNG 导出、figure manifest |
| [`references/final-quality-gates.md`](references/final-quality-gates.md) | 在声明 run、报告、产物包或项目完成前进行最终审计；代码/测试/debug 补丁变化时也覆盖收口审查 |
| [`references/project-hygiene-cleanup.md`](references/project-hygiene-cleanup.md) | 清理或排除失败、误导、半成品或垃圾产物，同时保留可信成功运行 |

## 脚本索引

| 脚本 | 作用 |
|---|---|
| [`scripts/validate_run_trace.py`](scripts/validate_run_trace.py) | 验证 run 文件夹中的训练记录、progress schema、checkpoint 与可选评估产物 |
| [`scripts/check_ieee_plot_manifest.py`](scripts/check_ieee_plot_manifest.py) | 检查 figure manifest、导出覆盖率与 IEEE 图件包一致性 |
| [`scripts/audit_reproducible_training_project.py`](scripts/audit_reproducible_training_project.py) | 执行最终 smoke/semantic audit：根 README 导航、技能合规矩阵、raw reward 对比列、shaped reward claim 失败、高风险 claim 警告、报告、图件、表格、TensorBoard events、manifest、artifact index、生成代码头注释 |

## 资产索引

| 资产 | 作用 |
|---|---|
| [`assets/python_file_header_templates.md`](assets/python_file_header_templates.md) | 中文优先 Python 文件头与入口脚本佛头模板 |
| [`assets/output_report_template.md`](assets/output_report_template.md) | 结构化 `output.md` 报告模板 |
| [`assets/monitor_training_template.m`](assets/monitor_training_template.m) | MATLAB CSV 监控模板，用作备选实时监督 |

## 预期项目产物

### 运行记录

| 产物 | 要求 |
|---|---|
| `config.json`, `run_command.txt`, `git_commit.txt` | 可复现启动上下文 |
| `stdout.log`, `progress.csv`, `episodes.csv`, `updates.csv` | 实时训练与诊断记录 |
| `tensorboard/` 或 `tb/` event files | 长训练必需的仪表盘证据 |
| `checkpoints/latest`, `checkpoints/best` | 可恢复模型来源；声明 full resume 时必须包含完整训练状态 |
| `summary.json`, `diagnostic.json` 或 `gate_debug_report.md` | 最终状态、gate/debug 证据、中止原因 |

### 评估记录

| 产物 | 要求 |
|---|---|
| `eval_config.json`, `eval_command.txt` | 评估设置与精确命令 |
| `eval_episodes.csv`, `eval_summary.json` | 测试 seed、checkpoint 来源、policy 模式、feasible rate 与评估指标 |

### 训练后产物包

| 产物 | 要求 |
|---|---|
| 根 `README.md` 或结果 `index.md` | 导航页，不能只是简介或 changelog |
| 主报告、summary、风险报告、debug/change log | 中文优先技术证据，并清晰标注 claim boundary |
| `figures/`, figure README, `figure_quality_audit.md`, `figure_quality_audit.csv` | IEEE 风格图件与质量证据 |
| `tables/`, `algorithm_comparison_summary.csv`, `same_tier_raw_reward_delta.csv`, run/eval/constraint summaries | 机器可读汇总 |
| `reproducibility_manifest.json`, `artifact_index.csv` | SHA256/字节数清单与人类可读产物索引 |
| `ppt_index.md` 或 `colleague_briefing.md` | 幻灯片映射、takeaway、claim boundary 与产物路径 |
| `skill_compliance_audit.md`, 使用时的 `completion_audit.md` | Gate 矩阵与最终就绪证据 |
| `missing_figures.md`, `missing_tables.md` | 明确缺失列、上游产物与所需 instrumentation |

### 原始奖励对比表

`algorithm_comparison_summary.csv` 必须包含：

```text
algorithm, tier, seed_count, raw_reward_source, raw_env_reward_mean, raw_env_reward_std, delta_vs_same_tier_baseline, shaped_reward_used_for_claim
```

性能行中的 `shaped_reward_used_for_claim` 必须为 `false`。若为 `true`，最终审计失败。

## 生成项目 README 契约

每个使用该技能的 RL/DRL/DL/ML 复现实验项目，其根 `README.md` 必须是导航页，并使用 GitHub 可用的相对链接。它必须索引：

- 子目录 README，例如 `figures/README.md` 或 TensorBoard event README；
- 报告：index、正式报告、summary、PPT index、colleague briefing、risk report、debug/change log；
- 图件：figures 目录、figure README、figure quality audit、missing figures 说明；
- 表格：tables 目录、algorithm comparison、run summary、evaluation summary、constraint violation summary、artifact index；
- 代码：`src/`、`scripts/`、训练入口、评估入口、训练后产物生成脚本；
- 配置：`commands/configs/` 或项目实际 config 目录；
- 运行记录：`runs/`、`progress.csv`、`stdout.log`、checkpoints、TensorBoard event 目录；
- 复现与审计：manifest、artifact index、validation logs、skill compliance audit、completion audit；
- 缺失产物：`missing_figures.md`、`missing_tables.md`。

如果某类产物未生成，README 必须写明 `NOT AVAILABLE: <reason>`，或链接相应缺失产物说明。不得静默省略该类别。

## 验证命令

根据当前审查产物运行对应检查：

```bash
python path/to/quick_validate.py .
python scripts/validate_run_trace.py path/to/run-folder
python scripts/check_ieee_plot_manifest.py path/to/figure_manifest.json
python scripts/audit_reproducible_training_project.py --project-root path/to/repo --results-dir path/to/results
python -m py_compile scripts/validate_run_trace.py scripts/check_ieee_plot_manifest.py scripts/audit_reproducible_training_project.py
```

`audit_reproducible_training_project.py` 返回 `PASS`、`WARN` 或 `FAIL`。`FAIL` 表示最终交付 gate 缺失或科学口径不安全；`WARN` 表示历史债或高风险 claim 文本需要复查。

## 维护说明

- 保持 [`SKILL.md`](SKILL.md) 精简，并把细节路由到 references。
- 当某项要求可机器检查时，同步更新 reference 文件与 audit 脚本。
- 仅把仓库文档保留在该 Git 镜像中，不要放进精简安装运行副本。
- 修改脚本后执行验证，并在发布前删除生成缓存。
- 在同一提交中同步更新 [`README.md`](README.md) 与 [`README_zh.md`](README_zh.md)。

## 语言一致性

[`README.md`](README.md) 是本文档的英文对应版本。两份 README 应拥有相同章节、声明、质量门、命令与维护预期。
