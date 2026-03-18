# Codex 使用教程

这份教程面向 Codex 用户，目标是让 Codex 使用 `awesome-skill-generate` 从 notebook 生成 skill。

## 你需要准备什么

至少准备三样东西：

1. notebook 路径
2. 相关源码或运行环境
3. 输出目录

推荐输出目录：

- `examples/generated-skills/<skill-name>/`

不要输出到：

- `skills/<skill-name>/`

因为 `skills/` 放的是这个仓库自己的 meta-skills。

## 最小提示词

```text
请使用当前仓库里的 skill-authoring，把 /绝对路径/your.ipynb 转成一个可复用的 skill。

要求：
1. 输出到 examples/generated-skills/<skill-name>/
2. 不要只是总结 notebook，要提炼成另一个 Agent 可执行的 skill
3. 要检查真实源码、inspect.signature、help 或 -h/--help
4. 要特别检查 method、recipe、backend、mode 这类多分支参数
5. 生成完成后，再用 skill-quality-scorer 做一次审查
6. reviewer 在打分时要尽量使用数据验证 skill 的可执行性
7. 最后运行 validate 和 acceptance
```

## 推荐提示词

```text
请在当前仓库中，使用 awesome-skill-generate 的能力，把下面这个 notebook 转成一个可复用的 skill：

输入 notebook：
/absolute/path/to/your-notebook.ipynb

输出目录：
examples/generated-skills/your-skill-name/

要求：
1. 使用 skill-authoring 的方式生成 skill
2. 不要把结果放到仓库自己的 skills/ 目录
3. 先从 notebook 中提炼稳定任务，而不是照抄 notebook 标题
4. 先检查真实接口，包括源码、inspect.signature、help 或 CLI 的 -h/--help
5. 对 method、recipe、backend、mode、provider、*_method 等多分支参数做检查
6. 生成的 skill 至少要包含：
   - SKILL.md
   - references/source-notebook-map.md
   - references/source-grounding.md（如果 skill 里写到了具体函数、参数、命令）
   - assets/acceptance.json
7. 生成后使用 skill-quality-scorer 审查
8. scorer 打分时请自己运行代表性数据，而不只是看文档
9. 把评分结果写成当前目录下的 Markdown 报告，文件名用 `<skill-name>-score-report-YYYY-MM-DD.md`
10. 最后运行：
   - python3 scripts/validate_skills.py --root examples
   - python3 scripts/run_skill_acceptance.py --root examples
   - python3 -m unittest discover -s tests -v
```

## 你应该期待 Codex 做什么

一个合格的 Codex 运行流程应包括：

1. 读取 notebook
2. 读取相关源码
3. 确定稳定任务
4. 写出 skill 文件结构
5. 写 `SKILL.md`
6. 写 `references/`
7. 写 `assets/acceptance.json`
8. 用 scorer 审查
9. 用 reviewer 角度跑代表性数据
10. 生成 score report

## 你该如何验收

重点看下面几件事：

- 它是不是只在复述 notebook
- 它有没有检查真实接口
- 它有没有检查分支参数
- 它有没有把输出目录放对
- 它打分时是否真的跑了数据
- 它有没有给出当前目录下的 score report

## 一个真实例子

```text
请使用当前仓库里的 skill-authoring，把 /Users/fernandozeng/Desktop/analysis/dynamo-release/docs/tutorials/notebooks/100_tutorial_preprocess.ipynb 转成一个可复用的 skill。

Python环境请你使用 conda 下的 omictest 环境。

要求：
1. 输出到 examples/generated-skills/dynamo-preprocess/
2. 不要只是总结 notebook，要提炼成另一个 Agent 可执行的 skill
3. 要检查真实源码、inspect.signature、help 或 -h/--help
4. 要特别检查 method、recipe、backend、mode 这类多分支参数
5. 生成完成后，再用 skill-quality-scorer 做一次审查
6. scorer 打分时请自己使用 synthetic 或 notebook 相邻数据验证 skill
7. 最后运行 validate 和 acceptance
```

## 常用命令

```bash
python3 scripts/validate_skills.py --root examples
python3 scripts/run_skill_acceptance.py --root examples
python3 -m unittest discover -s tests -v
```
