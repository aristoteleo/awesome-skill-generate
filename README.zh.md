# awesome-skill-generate

英文首页请见 [README.md](./README.md)。

`awesome-skill-generate` 是一个把 notebook、教程和领域流程沉淀成可复用 skill 的仓库。

这个仓库的目标不是“总结 notebook”，而是把 `notebook -> executable skill` 做成一套更可靠的方法。

## 为什么需要这个仓库

默认情况下，Agent 生成 skill 很容易出现这些问题：

- 只是复述 notebook，而不是提炼稳定任务
- 只写 notebook 跑到的那一条分支
- 不检查真实源码、`inspect.signature(...)`、`help(...)` 或 `-h/--help`
- 验证很弱，没有 reviewer 侧的执行证据
- notebook 事实、源码事实、验证事实全混在一起，后续很难维护

`awesome-skill-generate` 的目标，就是系统性修复这些问题。

## 为什么它是 Awesome

这个仓库要求 Agent 生成的 skill 具备下面这些性质：

- 可触发
- 可执行
- 可验证
- 可审查
- 有源码依据
- 能覆盖多分支参数
- 能产出带证据的评分报告

落到具体要求上，就是 Agent 需要：

- 先从 notebook 提炼稳定任务
- 再检查真实源码、`inspect.signature(...)`、`help(...)`、`-h/--help`
- 特别检查 `method`、`recipe`、`backend`、`mode` 这类多分支参数
- 生成带有 `SKILL.md`、`references/`、`assets/acceptance.json` 的 skill
- 在需要时，让 scorer 从 reviewer 视角做实证执行检查
- 输出人类可见的 score report，而不是只给一句“通过”

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

## 对比基准快照

当前仓库中的实测样例：

- 生成 skill：[`examples/generated-skills/dynamo-preprocess/`](./examples/generated-skills/dynamo-preprocess/SKILL.md)
- 评分报告：[`dynamo-preprocess-score-report-2026-03-18.md`](./dynamo-preprocess-score-report-2026-03-18.md)
- 加权分数：`95/100`
- 结论：`pass`

下面的对比基线含义是：

- 一个典型的“默认 Agent 生成结果”
- 它主要是 notebook 总结，不做完整 source-grounding，也不做 reviewer 侧实证验证
- 这个基线是基于 rubric 失败模式构造的说明性画像，不是一个单独版本化的 benchmark artifact

### 总分对比

```text
默认 Agent 生成 skill      38/100  [########------------]
awesome-skill-generate    95/100  [###################-]
```

### 各维度对比

```text
维度                       默认 Agent    本仓库样例
Trigger Precision          3/5  ###--    5/5  #####
Execution Clarity          2/5  ##---    5/5  #####
Validation Strength        1/5  #----    4/5  ####-
Empirical Executability    1/5  #----    5/5  #####
Context Efficiency         3/5  ###--    4/5  ####-
Reusability                2/5  ##---    5/5  #####
Resource Partitioning      2/5  ##---    5/5  #####
Compatibility Robustness   1/5  #----    5/5  #####
Maintainability            2/5  ##---    5/5  #####
```

### 这个对比真正说明了什么

真正有价值的提升，不是文案更好看，而是四件事：

- 用真实源码和接口来约束 skill，而不是只靠 notebook 记忆
- 对 `method` / `recipe` / `backend` 这类分支参数做覆盖检查
- 对数据工作流要求 reviewer 侧的实证执行证据
- 把 skill 拆成可维护的结构，而不是把所有内容塞进一个文档

## 我们想为 Skill 生成制定什么标准

这个仓库不只是一个 prompt 集合。它试图把 skill 生成这件事做成可审计、可比较、可标准化的流程。

我们想推动的标准包括：

1. skill 必须定义稳定任务，而不是照抄教程标题。
2. skill 必须有 trigger contract、execution spine、validation contract。
3. 任何具体 API 或 CLI 描述，都应该有 live source、signature、help 或 CLI help 依据。
4. 多分支参数必须做覆盖检查，不能只根据 notebook 的单条路径推断。
5. 对数据工作流，必要时必须有 reviewer 侧的执行证据。
6. 产物结构应该清晰：`SKILL.md`、`references/`、`assets/`，必要时加 `scripts/`。
7. 评分报告应该对人类可见，并包含命令、证据和残余风险。
8. 质量判断应该依赖 rubric，而不是主观感觉。

如果越来越多生成出来的 skill 都符合这些规则，那么 skill 生成就不再只是 prompt craft，而会更像一门工程 discipline。

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
