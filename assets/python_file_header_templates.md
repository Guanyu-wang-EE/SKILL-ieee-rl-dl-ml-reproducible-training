# Python File Header Templates

Use these templates in Python files generated for RL/DRL reproduction projects guided by this skill.

## All Python Files

```python
# -*- coding: utf-8 -*-
# 中文为主总览：
# 目的：
# 创建日期：
# 输入文件/CSV：
# 输出文件：
# 依赖脚本/模块：
# 运行示例：
# 复现说明：
```

## Main / Run / Long-Training Scripts

Use the Buddha ASCII block only for large one-command long-training entry scripts such as `main.py`, `run_*.py`, `train_*.py`, or equivalent project entry points. Do not force it into small utility scripts.

```python
# 佛祖保佑 永无BUG
# May the holy Buddha watch over this code and grant it to be bug-free.
#
#                       _oo0oo_
#                      o8888888o
#                      88  .  88
#                      (| -_- |)
#                      0\  =  /0
#                    ___/`---'\___
#                  .' \\|     |// '.
#                 / \\|||  :  |||// \
#                / _||||| -:- |||||- \
#               |   | \\\  -  /// |   |
#               | \_|  ''\---/''  |_/ |
#               \  .-\__  '-'  ___/-. /
#             ___'. .'  /--.--\  `. .'___
#          .'' '<  `.___\_<|>_/___.' >' ''.
#         | | :  `- \`.;`\ _ /`;.`/ - ` : | |
#         \  \ `_.   \_ __\ /__ _/   .-` /  /
#     =====`-.____`.___ \_____/ ___.-`___.-'=====
#                       `=---='
```

## Comment Strategy

Write detailed comments only where logic is hard to audit or affects reproducibility:

- Reward/cost normalization.
- Constraint threshold definitions.
- Alpha/lambda update rules.
- Seed fixing.
- Checkpoint selection strategy.
- Any data filtering that changes reported metrics.

Do not add comments for ordinary assignments or self-evident control flow.
