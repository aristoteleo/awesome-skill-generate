<div align="center">

<img src="https://raw.githubusercontent.com/Starlitnightly/ImageStore/main/omicverse_img/Gemini_Generated_Image_9hq7de9hq7de9hq7.png" >


# awesome-skill-generate

### 让 Agent 生成的 skill，真正变得可用。

把 notebook、教程和一次性 workflow，变成可复用、可审查、可评分的 agent skill。

[![GitHub stars](https://img.shields.io/github/stars/aristoteleo/awesome-skill-generate?style=flat-square)](https://github.com/aristoteleo/awesome-skill-generate/stargazers)
[![GitHub last commit](https://img.shields.io/github/last-commit/aristoteleo/awesome-skill-generate?style=flat-square)](https://github.com/aristoteleo/awesome-skill-generate/commits/main)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue?style=flat-square)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/tests-unittest-green?style=flat-square)](./tests)
[![Meta Skills](https://img.shields.io/badge/meta--skills-2-orange?style=flat-square)](./skills)
[![Notebook to Skill](https://img.shields.io/badge/notebook-%3E-skill-7c3aed?style=flat-square)](./README.md)
[![Source Grounded](https://img.shields.io/badge/source-grounded-0f766e?style=flat-square)](./skills/skill-authoring/SKILL.md)
[![Empirical Scoring](https://img.shields.io/badge/empirical-scoring-b45309?style=flat-square)](./skills/skill-quality-scorer/SKILL.md)

[快速开始](#快速开始) · [查看示例 Skill](./examples/generated-skills/dynamo-preprocess/SKILL.md) · [查看评分报告](./dynamo-preprocess-score-report-2026-03-18.md) · [Codex 中文教程](./codex-tutorial-zh.md) · [Claude Code 中文教程](./claude-code-tutorial-zh.md) · [English README](./README.md)

[快速开始](#快速开始) · [教程](#教程) · [一眼看懂](#一眼看懂) · [对比基准快照](#对比基准快照) · [贡献](#贡献)

</div>

---

> [!WARNING]
> 默认 Agent 已经会生成 skill。问题是，大多数 skill 并不好用。这个仓库的目标，就是修这个问题。

## 为什么这件事值得做

如果你正在把知识、流程、教程和 notebook 变成 AI 产品、内部自动化、Agent workflow 或可复用能力，那么这个仓库的意义在于：

它能把：

- notebook
- prompt
- transcript
- 一次性 demo

变成：

- 可复用 skill
- 可审查 artifact
- 可评分交付物
- 可标准化的 agent 工作单元

## 默认 Agent 已经会生成 skill 了，但大多数并不好用

常见问题很稳定：

- 只是复述 notebook，而不是提炼稳定任务
- 只写 notebook 跑到的那条分支
- 不检查真实源码、`inspect.signature(...)`、`help(...)` 或 `-h/--help`
- 没有 reviewer 侧的实证执行证据
- notebook 事实、源码事实、验证事实全堆在一起，后续难维护

`awesome-skill-generate` 的目标，就是系统性修复这些问题。

## 为什么它值得用

<table>
  <tr>
    <td width="33%"><strong>有源码依据</strong><br/><br/>生成 skill 前，先看真实源码、<code>inspect.signature(...)</code>、<code>help(...)</code>、<code>-h/--help</code>，避免把 notebook 局部路径误当成真实接口。</td>
    <td width="33%"><strong>覆盖多分支参数</strong><br/><br/>会特别检查 <code>method</code>、<code>recipe</code>、<code>backend</code>、<code>mode</code> 等关键分支参数，减少功能遗漏。</td>
    <td width="33%"><strong>评分有实证</strong><br/><br/>对于数据敏感 workflow，scorer 不只看文档，而会在 reviewer 视角补做必要的执行验证。</td>
  </tr>
</table>

<table>
  <tr>
    <td width="33%"><strong>产物结构清晰</strong><br/><br/>输出不是一份堆满信息的大文档，而是 <code>SKILL.md</code>、<code>references/</code>、<code>assets/</code>、可选 <code>scripts/</code> 的组合。</td>
    <td width="33%"><strong>对人类可见</strong><br/><br/>会生成带命令、证据、分数、残余风险的评分报告，并且每个维度分数下都有简短理由。</td>
    <td width="33%"><strong>试图制定标准</strong><br/><br/>这个仓库强调 capability-first 命名、环境无关的 skill 内容，以及显式的“拆成多个 skill 还是保留一个”的判断。</td>
  </tr>
</table>


## 快速开始

> [!TIP]
> 如果你想最快看到价值，建议先拿一个稳定任务明确的 notebook 做一次完整的 `生成 -> 打分 -> 看报告` 闭环，再考虑批量化。


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
5. 如果 notebook 里混了多个独立任务，要拆成多个 skill，或者明确说明为什么保留成一个 skill 更合理
6. 不要把本地绝对源码路径、python 解释器路径或本地环境名写进 SKILL.md 或 references
7. 对长时运行或 GPU-heavy 步骤，除非明确要求 full run，否则只做 representative smoke 验证
8. 生成完成后，再用 skill-quality-scorer 做一次审查
9. 在当前目录生成评分报告，并且每个维度分数下面都写简短理由
10. 最后运行 validate 和 acceptance
```

## 教程

**English**

- [Codex Tutorial](./codex-tutorial-en.md)
- [Claude Code Tutorial](./claude-code-tutorial-en.md)

**中文**

- [Codex 中文教程](./codex-tutorial-zh.md)
- [Claude Code 中文教程](./claude-code-tutorial-zh.md)

## 一眼看懂

```text
Notebook / Tutorial / Workflow
            |
            v
   skill-authoring
            |
            v
Generated Skill Directory
(SKILL.md + references + assets)
            |
            v
 skill-quality-scorer
            |
            v
Score Report + Validation + Acceptance
```

## 默认 Agent 生成物 vs 本仓库

| 维度 | 默认 Agent 风格产物 | `awesome-skill-generate` |
| --- | --- | --- |
| 目标 | 总结 notebook | 生成可复用 skill |
| API 处理 | 只写 notebook 用到的部分 | 检查 live source、signature、help、分支 |
| 验证 | 很弱或缺失 | 显式 validation 和 acceptance |
| 数据工作流 | 往往只做文本审查 | 必要时做 reviewer 侧实证执行 |
| 产物结构 | 一份大文档 | `SKILL.md` + `references/` + `assets/` + 可选 `scripts/` |
| 人类信任 | 靠感觉 | 靠报告和证据 |
| 可维护性 | 漂移快 | 可追踪、可更新 |

## 对比基准快照

当前仓库中的实测样例：

<div align="center">

[![加权分数](https://img.shields.io/badge/weighted%20score-95%2F100-111827?style=for-the-badge)](./dynamo-preprocess-score-report-2026-03-18.md)
[![评分结论](https://img.shields.io/badge/verdict-pass-15803d?style=for-the-badge)](./dynamo-preprocess-score-report-2026-03-18.md)
[![执行清晰度](https://img.shields.io/badge/execution%20clarity-5%2F5-1d4ed8?style=for-the-badge)](./dynamo-preprocess-score-report-2026-03-18.md)
[![实证可执行性](https://img.shields.io/badge/empirical%20executability-5%2F5-b45309?style=for-the-badge)](./dynamo-preprocess-score-report-2026-03-18.md)

[![有源码依据](https://img.shields.io/badge/source-grounded-0f766e?style=flat-square)](./skills/skill-authoring/SKILL.md)
[![覆盖多分支](https://img.shields.io/badge/branch-aware-7c2d12?style=flat-square)](./examples/generated-skills/dynamo-preprocess/references/source-grounding.md)
[![带证据报告](https://img.shields.io/badge/report-backed-7e22ce?style=flat-square)](./dynamo-preprocess-score-report-2026-03-18.md)

</div>

> [!NOTE]
> 这里展示的 benchmark 基于仓库当前的 `dynamo-preprocess` 示例 skill，以及对应的评分报告。

- 生成 skill：[`examples/generated-skills/dynamo-preprocess/`](./examples/generated-skills/dynamo-preprocess/SKILL.md)
- 评分报告：[`dynamo-preprocess-score-report-2026-03-18.md`](./dynamo-preprocess-score-report-2026-03-18.md)
- 加权分数：`95/100`
- 结论：`pass`

> [!IMPORTANT]
> 下方“默认 Agent”基线是基于 rubric 失败模式构造的说明性画像，不是一个单独版本化的 benchmark artifact。它的作用是帮助读者理解这个仓库试图消除哪些失败模式。

下方对比基线的含义：

- 一个典型的“默认 Agent 生成结果”
- 它主要是 notebook 总结，不做完整 source-grounding，也不做 reviewer 侧实证验证
- 这是基于 rubric 失败模式构造的说明性画像，不是一个单独版本化的 benchmark artifact

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

## 我们想制定什么标准

这个仓库不只是一个 prompt 集合。它试图把 skill 生成做成可审计、可比较、可标准化的流程。

我们希望推动这样的标准：

1. skill 必须定义稳定能力，而不是照抄教程标题、示例数据集名或物种名。
2. 如果 notebook 里混了多个可以独立触发的任务，生成器应该优先拆成多个 skill；只有共享边界非常强时才保留成一个。
3. skill 必须有 trigger contract、execution spine、validation contract。
4. 具体 API 或 CLI 描述，应该有 live source、signature、help 或 CLI help 依据。
5. 多分支参数必须做覆盖检查，不能只从 notebook 单条路径推断。
6. 可复用 skill 内容应该保持环境无关；本地 review 配置不应进入 `SKILL.md` 或 `references/`。
7. 生成文档应优先使用 repo-relative path 或 import path，而不是机器相关的绝对路径。
8. 对长时运行或 GPU-heavy workflow，默认应在有限评审预算内做 representative smoke，而不是默认要求完整昂贵复现。
9. 对数据工作流，必要时必须有 reviewer 侧执行证据。
10. 产物结构应该清晰：`SKILL.md`、`references/`、`assets/`，必要时加 `scripts/`。
11. 评分报告应该对人类可见，并包含命令、证据、残余风险，以及每个维度分数下的简短理由。
12. 质量判断应该依赖 rubric，而不是凭感觉。



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

## 贡献

欢迎各种形式的贡献。不管是发布新的 skill、改进生成器、优化 scorer、完善 benchmark 叙事，还是直接贡献代码，都欢迎查看 GitHub Issues 并参与进来。

## 许可证

本项目采用 [BSD 2-Clause](./LICENSE) 许可证。

## 版权

Copyright © 2026 [Qiu Lab](https://www.devo-evo.com).
