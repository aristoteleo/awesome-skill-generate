# awesome-skill-generate

`awesome-skill-generate` 是一个把 notebook、教程和领域流程沉淀成可复用 skill 的仓库。

这个仓库的目标不是“总结 notebook”，而是让 Agent 能把 notebook 转成：

- 可触发
- 可执行
- 可验证
- 可审查

的 skill。

## 一张图看懂

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

## 仓库结构

```text
awesome-skill-generate/
├── README.md
├── .gitignore
├── codex-tutorial-zh.md
├── claude-code-tutorial-zh.md
├── scripts/
│   ├── inspect_python_interface.py
│   ├── run_skill_acceptance.py
│   └── validate_skills.py
├── skills/
│   ├── skill-authoring/
│   └── skill-quality-scorer/
├── examples/
│   └── generated-skills/
│       └── dynamo-preprocess/
└── tests/
```

## 两个核心 meta-skill

- `skills/skill-authoring/`
  负责把 notebook 转成 skill。
- `skills/skill-quality-scorer/`
  负责给 skill 打分，并要求 reviewer 自己运行数据做实证评分，而不是只看文档。

## 仓库能做什么

- 从 `ipynb` 提炼稳定任务
- 检查真实源码、`inspect.signature(...)`、`help(...)`、`-h/--help`
- 检查 `method`、`recipe`、`backend`、`mode` 等多分支参数
- 生成 skill 目录结构
- 审查 skill 的结构质量
- 用 reviewer 侧的数据执行证据给 skill 打分
- 输出用户可见的 score report

## 推荐工作流

1. 选定一个 notebook。
2. 使用 `skill-authoring` 生成 skill。
3. 输出到 `examples/generated-skills/<skill-name>/` 或你自己的输出目录。
4. 使用 `skill-quality-scorer` 审查 skill。
5. scorer 自己运行代表性数据，对 skill 做实证评分。
6. 在当前目录生成一个用户可见的 score report。
7. 运行 validate、acceptance 和测试。

## 常用命令

```bash
python3 scripts/validate_skills.py --root all
python3 scripts/run_skill_acceptance.py --root all
python3 -m unittest discover -s tests -v
```

接口检查示例：

```bash
python3 scripts/inspect_python_interface.py dynamo.preprocessing:Preprocessor --pretty
```

## 教程

- Codex：`codex-tutorial-zh.md`
- Claude Code：`claude-code-tutorial-zh.md`

## 示例

当前仓库附带一个 notebook-derived 示例 skill：

- `examples/generated-skills/dynamo-preprocess/`

它来自：

- `/Users/fernandozeng/Desktop/analysis/dynamo-release/docs/tutorials/notebooks/100_tutorial_preprocess.ipynb`

## 原则

- skill 不是 notebook 摘要
- 源码优先于教程记忆
- 分支参数必须做覆盖检查
- 评分不能只看文字，还要看 reviewer 是否真的拿数据跑过
