---
name: dev-pdca
display_name: "开发闭环 dev-pdca"
display_name_en: "Dev PDCA Loop"
description_zh: "用 PDCA 方法让 AI 高效、有效地做开发：规划（planner）、执行（tasker）、审计（auditor）、修复（bugfixer）、复盘（evolver）五个技能一包装齐，环环相扣，每一步都要拿出证据。直接说要做的事即可自动分派，也可点名调用。"
description_en: "A PDCA development loop for AI agents: plan (planner), do (tasker), audit (auditor), fix (bugfixer) and learn (evolver), five evidence-first skills in one package that hand off to each other. Say what you need and it routes automatically, or name a stage directly."
description: "PDCA development loop for AI coding agents: one entry that routes to five evidence-first sub-skills. Plan = planner, Do = tasker, Check = auditor (and bugfixer when a check fails), Act = evolver. Use for software development work: project planning, requirements, architecture, M0/M1; implementing or changing code and docs with verification; bugs, errors, 500s, regressions, wrong-looking screenshots, 'still wrong'; audits, code review, security or release checks; retrospectives, preventing recurrence, persisting lessons. 开发闭环（PDCA）：项目规划、需求梳理、技术方案；任务执行、代码实现；修 bug、报错、还是不对；审计、代码评审、安全检查；复盘、防止复发、经验固化。Once active, keep its routing rules for the rest of the session."
argument-hint: "Optional: name a stage or skill, then the task. e.g. 审计 当前项目 / 修复 这个 500 报错 / planner M0 计划"
user-invocable: true
version: 1.0.0
---

# dev-pdca

One entry for the Tealun Skills suite. It runs software work as a PDCA loop and hands each stage to the sub-skill that owns it. This file only routes; the sub-skills do the work.

| Stage | Sub-skill | Owns |
| --- | --- | --- |
| Plan | `planner` | requirements, architecture, documentation and readiness gates before coding |
| Do | `tasker` | any change to files or state, with a done-definition and executable checks |
| Check | `auditor` | evidence-backed review of risk before merge, release or on request |
| Check → fix | `bugfixer` | a failed check or reported symptom: reproduce, prove the cause, fix, guard |
| Act | `evolver` | turn verified lessons into durable guards, ledger records and next-cycle inputs |

## Loading a sub-skill

1. Resolve the file: `./<name>/SKILL.md` (suite package layout) first, then `../<name>/SKILL.md` (repository or plugin layout, where the skills are siblings).
2. Read the whole file and follow it as written. Files it mentions are relative to that sub-skill's own folder. In the suite package its supporting files sit directly beside its `SKILL.md`; if a path such as `references/x.md` does not resolve, look for `x.md` in the same folder.
3. Inside a sub-skill, `$planner`, `$tasker`, `$bugfixer`, `$auditor` and `$evolver` mean: load that sub-skill the same way.
4. Never act from memory of a sub-skill or from its "spirit". If the file cannot be read, say which one is missing, then continue with the minimum it would require: state the done-definition, gather evidence, verify, report gaps.

Run one sub-skill at a time. When one hands off to another, carry the scope, target identity, done-definition and protected invariants across, then return to the earliest stage the handoff invalidated.

## Routing

### Explicit requests

A named stage, skill or action wins. Match aliases in any language:

- **planner**: 规划, 项目规划, 需求梳理, 技术方案, 架构, 开发指引, 文档规范, 数据库规范, 迁移规范, M0/M1, plan, roadmap, architecture, readiness.
- **tasker**: 执行, 实现, 改, 做完, 拆解任务, implement, change, build, do this task, workflow.
- **bugfixer**: 修复, 修 bug, 报错, 500, 回归, 还是不对, 复现, fix, bug, error, regression, still wrong, broken.
- **auditor**: 审计, 代码评审, review, 检查漏洞, 安全检查, 发布前检查, audit, security review, release check.
- **evolver**: 复盘, 防止复发, 经验固化, 落盘, 规则, 台账, retro, lessons, prevent recurrence, close the loop.

Invocation forms: `/dev-pdca 审计 当前项目`, `/dev-pdca bugfixer 这个 500 报错`, or plain language such as "用 auditor 做一次审计".

Bare `/dev-pdca` with no task: print the five sub-skills as one line each (stage, name, when to use), then stop.

### Unnamed requests

- Planning intent of any size (feature, page, URL or site structure, data or schema change, refactor, release, roadmap, documentation system) → `planner` before any code.
- Any change to files or state → `tasker`. Read-only questions need no sub-skill.
- Concrete failure evidence (error, log, screenshot, failing check, reproduction steps) → `bugfixer`.
- "Is there a problem here?" with no failure evidence → `auditor`. With failure evidence → `bugfixer`.
- A verified fix, finding or decision worth keeping → `evolver`.

## Session rules

These stay in force for the whole session once this skill is active. They replace the cold-start triggers each sub-skill carries when installed on its own.

- **To bugfixer, immediately**: a post-change check fails; the user says the result is still wrong or rejects it; a concrete runtime symptom appears; a previous repair missed its predicted outcome. Fallback: after roughly four substantive unresolved diagnostic exchanges with at least one concrete failure. Do not count greetings, confirmations, status checks or tool polling. After the symptom is verified gone, resume the interrupted sub-skill.
- **To auditor**: before pushing changes that touch auth, permissions, tenant isolation, payments, sensitive data, uploads, webhooks, database schema, deployment, URL parameters or shared state; before a release; on any audit request. Ordinary implementation does not become a full audit by default.
- **Evolver, silent tracking**: start tracking after a second accepted correction, a failed attempt that changes the approach, a third work phase, three material candidates, or when closeout, commit or release begins. At an implicit closeout, exit silently if nothing durable is worthwhile; otherwise propose one action and wait for confirmation. Explicit requests authorize safe local writes.
- **Back to planner**: when execution or audit exposes an unplanned decision about scope, architecture or data.

## Closing a cycle

A cycle is closed when the Do result has evidence, the Check found no open blocking issue, and Act either recorded a guard or stated that none was worthwhile. Report which stages ran, the evidence for each, and any stage skipped with its reason.
