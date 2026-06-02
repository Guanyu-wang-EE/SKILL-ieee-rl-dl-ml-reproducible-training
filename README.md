skill 名称：`ieee-rl-reproducible-training`

触发语义：用于 DRL/RL 论文复现、长训练、case study、ablation、IEEE Transactions 风格绘图、实时训练监控、实验留痕、中文为主项目文档、运行结果可追溯、失败输出清理。

结构：
  - `SKILL.md`
  - `agents/openai.yaml`
  - `references/ieee-plot-style.md`
  - `references/realtime-training-monitoring.md`
  - `references/reproducibility-recordkeeping.md`
  - `references/project-hygiene-cleanup.md`
  - `references/early-stop-risk-gates.md`
  - `assets/monitor_training_template.m`
  - `assets/python_file_header_templates.md`
  - `assets/output_report_template.md`
  - `scripts/validate_run_trace.py`
  - `scripts/check_ieee_plot_manifest.py`

- `SKILL.md` frontmatter：
  - `name: ieee-rl-reproducible-training`
  - `description:` 覆盖 RL/DRL paper reproduction、long training、IEEE Transactions plotting、real-time CSV/MATLAB monitoring、traceable outputs、Chinese-first documentation、cleanup of failed runs。

- IEEE plotting 规范写入 `references/ieee-plot-style.md`：
  - 面向 IEEE Transactions on Smart Grid / Power Systems。
  - 默认输出：`PDF`、`EPS`、`SVG font-embedded`、`PNG preview`。
  - SVG 要求：优先生成保留/嵌入字体信息的 SVG；若工具链无法真正嵌入字体，则使用 path-converted SVG fallback 并在 manifest 中标记 `svg_font_mode=path_fallback`。
  - 规定 Times New Roman/serif 字体、8-10 pt 字号、单栏约 3.45 in、双栏约 7.16 in、色盲友好配色、线宽、marker、legend、caption、grid、tick、linear/log axis 选择规则。
  - `reward`、`constraint violation`、`threshold sweep` 默认线性坐标；loss、gradient norm、alpha/lambda 跨数量级时才用 log，并在报告中说明。

- 实时训练监控写入 `references/realtime-training-monitoring.md`：
  - 明确禁止 only-save-at-run-end。
  - 每个 run 实时写 `progress.csv`、`episodes.csv`、`updates.csv`，最终写 `summary.json`。
  - 每 10 episodes 或固定 step interval 输出 PowerShell/Python stdout。
  - stdout 格式固定为 `[plan]`、`[progress]`、`[train]`、`[warn]`、`[stop]`。
  - MATLAB 监控模板读取轻量 CSV，展示 reward、cost/constraint violation、alpha/lambda、fps/elapsed，不锁训练文件，不依赖 Python 进程结束。
  - checkpoint 至少包含 `latest` 与 `best`，最终保留模型、config、command、summary、manifest。

- 可复现留痕写入 `references/reproducibility-recordkeeping.md`：
  - 项目 `README.md`、`requirements.txt`/环境说明、`output.md` 均中文为主，关键词首次出现双语。
  - `output.md` 必须包含实验假设、配置、seed、指标、图表、与论文差异、风险点、下一步建议。
  - 记录 Python、conda env、CUDA/PyTorch、GPU/CPU、seed、命令、路径、SHA256 manifest。
  - 结果明显异常时及时停止，记录原因，不继续污染总结果。

- Python 文件头模板写入 `assets/python_file_header_templates.md`：
  - 所有 `.py` 文件开头包含中文为主总览：目的、创建日期、输入 CSV/文件、输出文件、依赖脚本/模块、运行示例、复现说明。
  - main/run/long-train 脚本额外加入佛祖 ASCII header 与：
    `May the holy Buddha watch over this code and grant it to be bug-free.`
  - 关键难懂位置详注；普通赋值和显然逻辑不写空泛注释。

- 清理纪律写入 `references/project-hygiene-cleanup.md`：
  - 每个 stage：验证通过后再瘦身清理。
  - 删除失败 run 输出、错误脚本、临时 plot、缓存、无解释中间文件。
  - 不删除正常多 seed、多算法、多次 validation 的成功记录。
  - 成功 run 必须用 `time + seed + script name` 或等价命名区分。
  - 失败/纠错 run 删除文件夹，只在 MD 日志中保留时间、原因、处理动作。

- 早停与风险门控写入 `references/early-stop-risk-gates.md`：
  - NaN/Inf、OOM、alpha/lambda 爆炸、constraint violation 长期不下降、reward 崩塌、环境交互异常、CSV 不更新、fps 异常时触发停机或人工复核。
  - 停机后删除污染输出，仅保留 MD 事件记录。

## Interfaces And Validation

- `scripts/validate_run_trace.py`：
  - 检查 run 文件夹是否包含 `config.json`、`run_command.txt`、`progress.csv`、`episodes.csv`、`updates.csv`、`summary.json`、checkpoint。
  - 检查 CSV 必要列、时间戳、seed/algo/env/step 一致性、是否存在 NaN/Inf。
  - 输出 pass/fail 与缺失项。

- `scripts/check_ieee_plot_manifest.py`：
  - 检查 figure manifest 是否记录 PDF/EPS/SVG/PNG、数据源、生成命令、SHA256、时间。
  - 检查 SVG 字体模式字段：`embedded` 或 `path_fallback`。
  - 检查图文件实际存在且哈希匹配。

- `assets/monitor_training_template.m`：
  - MATLAB 脚本读取 `progress.csv`，循环刷新曲线。
  - 默认布局 2x2：reward、constraint violation、alpha/lambda、fps。
  - 图面干净，适合训练中实时监督，不承担最终 IEEE 出图职责。

- `assets/output_report_template.md`：
  - 中文为主模板，章节固定为：实验目标、配置、运行摘要、IEEE 图、与论文对比、异常与处理、专家风险判断、下一步建议。


**C. 风险点与验证检查**

主要风险：

- IEEE 风格被误解成“好看”而非“论文可发表”：需要硬性尺寸、字体、线宽、导出规范。
- log axis 被滥用：必须由数量级跨度和论文解释需求决定。
- 只保存最终结果：这是本次已经踩过的坑，skill 必须强约束实时 CSV 与 stdout。
- MATLAB 监控过重：必须只读轻量 CSV，不干扰训练，不锁文件。
- 清理过度：失败污染要删，但正常多 seed 成功 run 不能删。
- 文档写成“还没长训”的语气：要按真实状态写，计划、进行中、已完成要分清。
- 佛祖 header 只应放在 main/run 类大型长训脚本，不要求所有小工具脚本都放。
- skill 过长：核心 `SKILL.md` 过大反而降低可用性，细节必须分流到 references。

最终验证清单：

- `SKILL.md` 英文、concise、scientific，frontmatter 只有 `name` 和 `description`。
- description 覆盖 IEEE plots、RL/DRL reproduction、long training、monitoring、traceability、cleanup。
- references 覆盖配色、字体、字号、坐标、图例、导出、caption、manifest。
- monitoring 覆盖“不 run 结束才落盘”、MATLAB `.m`、CSV、stdout interval、输出字段、风险日志。
- recordkeeping 覆盖中文 README、requirements、output.md、环境、seed、命令、SHA256、专家分析。
- script header 覆盖中文总览、日期、CSV 依赖、py 依赖、concise 注释。
- main/run 脚本覆盖佛祖 ASCII 与英文祝语。
- cleanup 覆盖失败输出删除、MD 留痕、成功多 run 保留、时间+seed+脚本命名。
- 有 `validate_run_trace.py` 或等价检查脚本思路，确保 trace 文件和 manifest 不缺。
- 创建后用 skill-creator 的 `quick_validate.py` 验证。

