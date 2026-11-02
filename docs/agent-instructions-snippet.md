# 让 Agent 真的调用技能：项目指令片段

English version: [below](#english-snippet).

## 为什么需要这一段

装好技能不等于 Agent 会用。如果项目指令里没有写任何触发条件，Agent 会按自己的习惯干活，技能可能装了一整个开发周期都没被调用过。

在项目指令里加一节，逐个写清每个技能在什么时候必须调用，并要求每个会话的第一条回复先说明哪些技能可用，技能才会真正进入工作流程。

把下面的片段复制到你项目的 Agent 指令文件里即可：

- Claude Code：`CLAUDE.md`
- Codex、Cursor、OpenCode 等：`AGENTS.md`（Claude Code 也可以在 `CLAUDE.md` 里写一行 `@AGENTS.md` 共用同一份）
- Gemini：`GEMINI.md`

中英文选一个，和你项目指令的语言一致就行。片段里的台账路径 `docs/98_evolution/evolution-ledger.md` 是 evolver 的默认位置，项目另有约定时改成你的路径。

## 中文片段

```markdown
## 配套技能：要调用，不要只“照着精神做”

本项目使用 Tealun Skills（planner、tasker、bugfixer、auditor、evolver、explainer）。触发条件满足时，通过技能工具调用对应技能（或读取它的 SKILL.md 并按步骤执行）；只按“大意”去做不算调用。每个会话的第一条回复，先说明这六个技能里哪些可用；缺哪个就直说。

- **planner：任何规划意图，不论大小。** 功能、页面、URL 或站点结构调整、数据或 schema 变更、重构、发布、路线图、文档体系或流程。在写代码或内容之前调用，先把决定写进对应文档。
- **tasker：任何对文件或状态的改动。** 动手前写清完成定义和一个可执行的检查；收尾时给出证据（命令输出、截图），不要只给描述。只读的问答不需要。
- **bugfixer：用户说有问题或“还是不对”、截图里能看到缺陷、或者某个检查失败时。** 先复现或直接观察，证明原因，只修这个原因，再验证最初的症状已经消失。
- **auditor：推送安全、部署、URL 参数或共享状态相关的改动之前，发布之前，以及任何审计请求。**
- **evolver：用户报告的问题修好并验证之后、同一周期内第二次被纠正之后、以及每个工作周期结束时。** 把经验和对应的防线记到 `docs/98_evolution/evolution-ledger.md`。
- **explainer：用户看不懂要改的地方，或想知道项目由哪几块组成、某个按钮点了之后发生什么、改一处会牵连哪里、AI 刚才改了什么时。** 只读，不改代码；白话说明写进 `docs/explainer/`，每条结论附文件路径。tasker 或 bugfixer 动手前先用它确认要改的地方；功能完成或审计之后用它刷新项目地图。
```

## English snippet

```markdown
## Companion skills: invoke them, do not just follow their spirit

This project uses the Tealun Skills (planner, tasker, bugfixer, auditor, evolver, explainer). When a trigger below applies, invoke the matching skill through the skill tool (or read its SKILL.md and follow it). Following the general idea without invoking it does not count. In the first reply of every session, state which of the six skills are available; if one is missing, say so.

- **planner: every planning intent, whatever its size.** A feature, a page, a URL or site-structure change, a data or schema change, a refactor, a release, a roadmap, a doc system or process. Invoke it before writing code or content, and record the decisions in the relevant doc first.
- **tasker: every change to files or state.** Set the done definition and an executable check before editing; finish with evidence (command output, screenshots), not a description. Read-only answers are exempt.
- **bugfixer: when the user says something is wrong or still wrong, a screenshot shows a defect, or a check fails.** Reproduce or observe first, prove the cause, fix only that, and verify the original symptom.
- **auditor: before pushing changes to security, deployment, URL parameters or shared state, before a release, and on any audit request.**
- **evolver: after a verified fix of a user-reported problem, after a second correction in a cycle, and at the close of each work cycle.** Record the lesson and its guard in `docs/98_evolution/evolution-ledger.md`.
- **explainer: when the user cannot follow the code about to change, or asks what the project is made of, what happens after a click, what a change would affect, or what the AI just changed.** Read-only; it writes plain-language pages with file paths under `docs/explainer/`. Use it before tasker or bugfixer change an area the user does not understand, and refresh the project map after a feature or an audit.
```

## 云端会话里没有技能怎么办：把技能放进项目

同步脚本和插件安装的都是本机或账号级的技能。在云端会话、CI 或别人的机器上，这些技能可能根本不存在，会话里只看得到项目自带的技能。解决办法是把技能固定版本复制进项目仓库。

做法：

1. 把某个提交的完整内容复制到项目里，例如 `skills/tealun/upstream/`：

   ```bash
   git clone --depth 1 https://github.com/tealun/Tealun-Skills.git /tmp/tealun-skills
   mkdir -p skills/tealun
   rm -rf skills/tealun/upstream
   cp -R /tmp/tealun-skills skills/tealun/upstream
   rm -rf skills/tealun/upstream/.git
   git -C /tmp/tealun-skills rev-parse HEAD   # 记下这个提交号
   ```

2. 在 `skills/tealun/UPSTREAM.md` 里记下来源仓库、提交号、日期和许可证（MIT），并写明：不要在项目里直接改这些文件，要更新就从新的提交整体替换目录，同时更新这张表。
3. 在上面的指令片段里加一句，告诉 Agent 去哪里找：

   ```markdown
   The skills are vendored at `skills/tealun/upstream/` (pinned commit in `skills/tealun/UPSTREAM.md`). If the skill tool does not list them, read those copies. Do not edit them in place.
   ```

   中文：`技能的固定副本在 skills/tealun/upstream/（提交号见 skills/tealun/UPSTREAM.md）。技能工具里看不到时，直接读这些副本。不要在项目里直接修改它们。`

只用 Claude Code 的项目，也可以把需要的技能目录复制到项目的 `.claude/skills/<技能名>/`，Claude Code 打开项目时会把它们当作项目技能加载。

复制进项目的代价是版本不会自动更新，需要你定期从上游替换。所以只在确实需要的场景（云端会话、多人协作、CI）这样做。
