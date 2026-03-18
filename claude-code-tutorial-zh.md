# Claude Code 使用教程

这份教程面向 Claude Code 用户，目标是让 Claude Code 使用 `awesome-skill-generate` 从 notebook 生成 skill。

## 使用思路

Claude Code 在这个仓库里的角色，和 Codex 很接近：

- 用 `skill-authoring` 生成 skill
- 用 `skill-quality-scorer` 审查 skill
- 在评分阶段自己运行代表性数据
- 生成当前目录下的 score report

## 推荐任务描述

你给 Claude Code 的任务最好包含下面几部分：

- notebook 路径
- 输出目录
- Python 环境
- 源码检查要求
- 分支覆盖要求
- scorer 侧数据执行要求

## 推荐提示词模板

```text
请在当前仓库里，使用 awesome-skill-generate 的两个核心 meta-skills 完成以下任务：

1. 使用 skill-authoring，把 /absolute/path/to/notebook.ipynb 转成一个可复用 skill
2. 输出到 examples/generated-skills/your-skill-name/
3. 检查真实源码、inspect.signature、help 或 CLI 帮助
4. 检查 method、recipe、backend、mode 等分支参数
5. 使用 skill-quality-scorer 对生成结果打分
6. scorer 不要只看文档，要自己用代表性数据验证 skill 的可执行性
7. 把评分报告写到当前目录，文件名为 `<skill-name>-score-report-YYYY-MM-DD.md`
8. 最后运行 validate、acceptance 和测试
```

## Claude Code 应该输出什么

理想输出包括：

- 生成好的 skill 目录
- reviewer 侧数据执行证据
- 当前目录下的评分报告
- 简洁的风险说明

## 你应该重点检查什么

- skill 是否真的可触发
- skill 是否真的可执行
- scorer 是否真的跑了数据
- score report 是否有真实命令和输出

## Claude Code 示例

```text
请使用当前仓库里的 skill-authoring，把 /Users/fernandozeng/Desktop/analysis/dynamo-release/docs/tutorials/notebooks/100_tutorial_preprocess.ipynb 转成一个可复用的 skill。

Python环境请你使用 conda 下的 omictest 环境。

要求：
1. 输出到 examples/generated-skills/dynamo-preprocess/
2. 不要只是总结 notebook，要提炼成另一个 Agent 可执行的 skill
3. 要检查真实源码、inspect.signature、help 或 -h/--help
4. 要特别检查 method、recipe、backend、mode 这类多分支参数
5. 生成完成后，再用 skill-quality-scorer 做一次审查
6. scorer 打分时请自己使用数据验证 skill
7. 最后运行 validate 和 acceptance
```

## 常用命令

```bash
python3 scripts/validate_skills.py --root all
python3 scripts/run_skill_acceptance.py --root all
python3 -m unittest discover -s tests -v
```
