# IEEE RL 可复现实验训练 Skill

[English](README.en.md) | 简体中文

## Skill 名称

`ieee-rl-reproducible-training`

本仓库是该 Codex skill 的公开 GitHub 版本，用于维护可复现强化学习（Reinforcement Learning, RL）与深度强化学习（Deep Reinforcement Learning, DRL）实验工作流。建议将 Git 版本管理保留在本独立仓库中，不要把 `.git` 元数据放入 Codex 正在读取的 skills 安装目录。

## 触发语义

用于 DRL/RL 论文复现、长训练、case study、ablation、IEEE Transactions 风格绘图、实时训练监控、实验留痕、中文为主项目文档、运行结果可追溯，以及失败输出清理。

## 结构
  - `SKILL.md`
  - `agents/openai.yaml`
  - `references/ieee-plot-style.md`
  - `references/realtime-training-monitoring.md`
  - `references/reproducibility-recordkeeping.md`
  - `references/project-hygiene-cleanup.md`
  - `assets/monitor_training_template.m`
  - `assets/python_file_header_templates.md`
  - `assets/output_report_template.md`
  - `scripts/validate_run_trace.py`
  - `scripts/check_ieee_plot_manifest.py`

## `SKILL.md` frontmatter

  - `name: ieee-rl-reproducible-training`
  - `description:` 覆盖 RL/DRL paper reproduction、long training、IEEE Transactions plotting、real-time CSV/TensorBoard monitoring with optional MATLAB inspection、traceable outputs、Chinese-first documentation、cleanup of failed runs。

## 核心能力

### IEEE plotting 规范

写入 `references/ieee-plot-style.md`：
  - 面向 IEEE Transactions on Smart Grid / Power Systems。
  - 默认输出：`PDF`、`EPS`、`SVG font-embedded`、`PNG preview`。
  - SVG 要求：优先生成保留/嵌入字体信息的 SVG；若工具链无法真正嵌入字体，则使用 path-converted SVG fallback 并在 manifest 中标记 `svg_font_mode=path_fallback`。
  - 规定 Times New Roman/serif 字体、8-10 pt 字号、单栏约 3.45 in、双栏约 7.16 in、色盲友好配色、线宽、marker、legend、caption、grid、tick、linear/log axis 选择规则。
  - `reward`、`constraint violation`、`threshold sweep` 默认线性坐标；loss、gradient norm、alpha/lambda 跨数量级时才用 log，并在报告中说明。

### 实时训练监控

写入 `references/realtime-training-monitoring.md`：
  - 明确禁止 only-save-at-run-end。
  - 每个 run 实时写 `progress.csv`、`episodes.csv`、`updates.csv`，最终写 `summary.json`。
  - 每 10 episodes 或固定 step interval 输出 PowerShell/Python stdout。
  - stdout 格式包含 `[plan]`、`[progress]`、`[train]`、`[warn]` 等事件。
  - TensorBoard 作为推荐在线仪表盘；MATLAB 监控模板作为可选兼容层读取轻量 CSV，展示 reward、cost/constraint violation、alpha/lambda、fps/elapsed，不锁训练文件，不依赖 Python 进程结束。
  - checkpoint 至少包含 `latest` 与 `best`，最终保留模型、config、command、summary、manifest。

### 可复现留痕

写入 `references/reproducibility-recordkeeping.md`：
  - 项目 `README.md`、`requirements.txt`/环境说明、`output.md` 均中文为主，关键词首次出现双语。
  - `output.md` 必须包含实验假设、配置、seed、指标、图表、与论文差异、风险点、下一步建议。
  - 记录 Python、conda env、CUDA/PyTorch、GPU/CPU、seed、命令、路径、SHA256 manifest。
  - 记录项目自定义异常、处理动作和可信输出边界。

### Python 文件头模板

写入 `assets/python_file_header_templates.md`：
  - 所有 `.py` 文件开头包含中文为主总览：目的、创建日期、输入 CSV/文件、输出文件、依赖脚本/模块、运行示例、复现说明。
  - main/run/long-train 脚本额外加入佛祖 ASCII header 与：
    `May the holy Buddha watch over this code and grant it to be bug-free.`
  - 关键难懂位置详注；普通赋值和显然逻辑不写空泛注释。

### 清理纪律

写入 `references/project-hygiene-cleanup.md`：
  - 每个 stage：验证通过后直接瘦身清理。
  - 删除失败 run 输出、错误脚本、临时 plot、缓存、无解释中间文件。
  - 删除半截、废品、误导性探索文件，无需弹窗或再次征得用户同意。
  - 不删除正常多 seed、多算法、多次 validation 的成功记录。
  - 成功 run 必须用 `time + seed + script name` 或等价命名区分。
  - 失败/纠错 run 删除文件夹，只在 MD 日志中保留时间、原因、处理动作。





