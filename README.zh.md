# awesome-skill-generate

英文首页请见 [README.md](./README.md)。

`awesome-skill-generate` 是一个把 notebook、教程和领域流程沉淀成可复用 skill 的仓库。

这个仓库的目标不是“总结 notebook”，而是让 Agent 能把 notebook 转成：

- 可触发
- 可执行
- 可验证
- 可审查

的 skill。

## 整体流程

```text
Notebook / Tutorial / Workflow
            |
            v
   skill-authoring
            |
            v
Generated Skill Directory
(SKILL.md + references + acceptance)
            |
            v
 skill-quality-scorer
            |
            v
Score Report + Validation + Acceptance
```

## 为什么需要这个仓库

这个仓库的目标是把 `notebook -> skill` 这件事做得更稳定，而不是让 Agent 只会复述 notebook。

它要求 Agent：

- 先从 notebook 提炼稳定任务
- 再检查真实源码、`inspect.signature(...)`、`help(...)`、`-h/--help`
- 特别检查 `method`、`recipe`、`backend`、`mode` 这类多分支参数
- 生成带有 `SKILL.md`、`references/`、`assets/acceptance.json` 的 skill
- 再使用 reviewer 视角做质量审查和必要的实证验证

## 快速开始

1. 在 Codex 或 Claude Code 中打开本仓库。
2. 选择一个要转换的 notebook。
3. 要求 Agent 使用 `skill-authoring`，输出到 `examples/generated-skills/<skill-name>/`。
4. 要求 Agent 使用 `skill-quality-scorer` 审查结果。
5. 运行 validate、acceptance 和测试。

示例请求：

```text
请使用当前仓库里的 skill-authoring，把 /absolute/path/to/notebook.ipynb 转成一个可复用的 skill。

要求：
1. 输出到 examples/generated-skills/<skill-name>/
2. 不要只是总结 notebook
3. 要检查真实源码、inspect.signature、help 或 -h/--help
4. 要检查 method、recipe、backend、mode 这类多分支参数
5. 生成完成后，再用 skill-quality-scorer 做一次审查
6. 在当前目录生成评分报告
7. 最后运行 validate 和 acceptance
```

## 两个核心 meta-skill

- [`skills/skill-authoring/`](./skills/skill-authoring/SKILL.md)
  负责把 notebook 转成可复用 skill。
- [`skills/skill-quality-scorer/`](./skills/skill-quality-scorer/SKILL.md)
  负责审查和打分，并在合适时从 reviewer 视角运行数据。

## 教程

English:

- [Codex Tutorial](./codex-tutorial-en.md)
- [Claude Code Tutorial](./claude-code-tutorial-en.md)

中文：

- [Codex 中文教程](./codex-tutorial-zh.md)
- [Claude Code 中文教程](./claude-code-tutorial-zh.md)

## 仓库结构

```text
awesome-skill-generate/
├── README.md
├── README.zh.md
├── codex-tutorial-en.md
├── codex-tutorial-zh.md
├── claude-code-tutorial-en.md
├── claude-code-tutorial-zh.md
├── skills/
│   ├── skill-authoring/
│   └── skill-quality-scorer/
├── examples/
│   └── generated-skills/
├── scripts/
└── tests/
```

## 示例

当前仓库附带一个 notebook-derived 示例 skill：

- [`examples/generated-skills/dynamo-preprocess/`](./examples/generated-skills/dynamo-preprocess/SKILL.md)

来源 notebook：

- `/Users/fernandozeng/Desktop/analysis/dynamo-release/docs/tutorials/notebooks/100_tutorial_preprocess.ipynb`

评分报告示例：

- [`dynamo-preprocess-score-report-2026-03-18.md`](./dynamo-preprocess-score-report-2026-03-18.md)

## 常用命令

校验 skill：

```bash
python3 scripts/validate_skills.py --root all
```

运行 acceptance：

```bash
python3 scripts/run_skill_acceptance.py --root all
```

运行测试：

```bash
python3 -m unittest discover -s tests -v
```

检查 Python 接口：

```bash
python3 scripts/inspect_python_interface.py dynamo.preprocessing:Preprocessor --pretty
```

## 原则

- skill 不是 notebook 摘要
- 源码优先于教程记忆
- 多分支参数必须做覆盖检查
- 需要实证时，评分不能只看文本
