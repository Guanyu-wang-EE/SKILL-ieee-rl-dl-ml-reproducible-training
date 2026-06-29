# 实验目标

说明实验假设、复现目标、算法、环境、seed、steps、metrics、项目判据，以及 train/test evaluation 的边界。

# 配置

- 算法：
- 环境：
- Seed：
- 训练步数：
- 测试 seed：
- Policy 模式：deterministic / stochastic
- 加载 checkpoint：best / latest / other
- Python / PyTorch / CUDA：
- CPU / GPU：
- Conda env / requirements：
- 训练命令：
- 测试命令：
- 输出目录：
- SHA256 manifest：

# 运行摘要

记录每个阶段做了什么、为什么继续/中断/完成、哪些输出可信、哪些输出被保留、排除，或在授权清理时删除。引用 `plan_summary.json`、训练 run 文件夹、evaluation 文件夹和关键 stdout 事件。

# Train/Test 结果

分开汇报训练指标和测试指标。测试部分必须说明 `eval_config.json`、`eval_command.txt`、`eval_episodes.csv`、`eval_summary.json` 的路径、测试 seed、policy 模式、checkpoint 来源和 feasible rate。

# IEEE 图

列出 PNG/PDF/SVG 图、数据源、生成命令、SHA256、font family、DPI、SVG 字体模式、SVG backend、字体嵌入检查状态、SVG vector geometry 检查状态、figure quality audit 路径。若生成 EPS，再列为期刊增强项。说明图中 hypothesis、metric、threshold、seed 数，以及线性/对数坐标选择理由。

# 图片质量与汇报入口

说明 `figures*/README.md`、`figure_quality_audit.md`、`figure_quality_audit.csv`、`missing_figures.md` 的路径。列出 PPT 优先使用的 PDF 图、每张图能证明什么、不能证明什么，以及必须同步讲的风险图。

# Threshold Summary

引用 `threshold_summary.csv`，至少说明 `algo, seed_count, threshold, reward_mean, reward_std, cv_mean, feasible_rate`。

# 与论文对比

对照目标论文或 case study 的主要指标、趋势、约束违反 (constraint violation)、消融实验 (ablation study) 结果和差异。

# 异常与处理

记录项目自定义异常、数值错误、环境错误、日志/CSV 异常等事件及处理动作。

# 专家风险判断

说明结果可信度、边界条件、不可比因素、环境版本风险、seed 数不足风险、统计不确定性、测试策略风险、后续验证需求。

# 下一步建议

给出下一轮训练、参数扫描、threshold sweep、更多 seed、绘图改进、清理动作或收尾理由。
