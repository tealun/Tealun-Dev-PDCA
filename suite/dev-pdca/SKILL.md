---
name: dev-pdca
display_name: "开发闭环 dev-pdca"
display_name_en: "Dev PDCA Loop"
description_zh: "让 AI 写代码，不再“说做完了，其实没做到”。dev-pdca 用 PDCA 闭环约束 AI 的开发全过程，五个技能自动接力：【Plan · planner】动手前先定需求、架构和 M0–M3 阶段门槛，决策、假设、待验证项分别记账，不边做边猜。【Do · tasker】每次改动先写完成标准和可执行的检查，有副作用的操作先确认；做完必须拿出命令输出、截图等证据，而不是一句“看起来没问题”。【Check · auditor】按风险自动选择快速、标准或深度审计，只报告经过验证、有证据的问题，并标明严重性、置信度和验证缺口。【Check · bugfixer】先复现，用证据证明原因再动手，只修最小的因果链；修完验证原始症状确实消失，再补一条“撤掉修复就会失败”的回归测试。【Act · evolver】把验证过的教训固化成测试、规则和演进台账，下一轮规划自动带上，同样的坑不踩第二次。检查失败自动转修复，修好回到执行；同一轮被纠正两次，自动开始复盘。直接说“做一次审计”“修复这个报错”即可自动分派，也可点名调用。"
description_en: "Stop AI agents saying “done” when it isn't. dev-pdca runs development as a PDCA loop of five skills that hand work to each other: [Plan · planner] sets requirements, architecture and M0–M3 gates before code, tracking decisions, assumptions and open questions. [Do · tasker] defines done and an executable check before each change, confirms side effects, and closes with evidence, not “looks fine”. [Check · auditor] scales the audit to risk and reports only verified findings, with severity, confidence and gaps. [Check · bugfixer] reproduces, proves the cause, fixes the smallest causal chain, verifies the symptom is gone, and adds a regression test that fails without the fix. [Act · evolver] turns verified lessons into tests, rules and a ledger for the next plan. A failed check routes to bugfixer and back; a second correction starts a retrospective. Just say “audit this” or “fix this error”."
examples_zh:
  - "我想实现一个这样的项目，帮我梳理需求和计划，我们先一起讨论出一个框架"
  - "接口返回还是报 500，你要着重从后端服务器交互上找问题并修复"
  - "把这次修好的问题复盘一下，固化成规则，防止再犯"
examples_en:
  - "I want to build a project like this. Help me sort out the requirements and plan, and let's agree on a framework first"
  - "The API still returns 500. Focus on the backend server interactions, find the cause and fix it"
  - "Run a retrospective on this fix and turn the lesson into a rule so it doesn't recur"
author: Tealun
category: developer
description: "PDCA development loop for AI coding agents: one entry that routes to five evidence-first sub-skills. Plan = planner, Do = tasker, Check = auditor (and bugfixer when a check fails), Act = evolver. Use for software development work: project planning, requirements, architecture, M0/M1; implementing or changing code and docs with verification; bugs, errors, 500s, regressions, wrong-looking screenshots, 'still wrong'; audits, code review, security or release checks; retrospectives, preventing recurrence, persisting lessons. 开发闭环（PDCA）：项目规划、需求梳理、技术方案；任务执行、代码实现；修 bug、报错、还是不对、CI 失败、上传或审核被拒；审计、代码评审、安全检查；复盘、防止复发、经验固化。Once active, keep its routing rules for the rest of the session."
argument-hint: "Optional: name a stage or skill, then the task. e.g. 审计 当前项目 / 修复 这个 500 报错 / planner M0 计划"
user-invocable: true
version: 1.0.1
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

- **To bugfixer, immediately**: a post-change check fails, including CI or an external platform rejecting an upload, publish or review; the user says the result is still wrong or rejects it; a concrete runtime symptom appears; a previous repair missed its predicted outcome. Fallback: after roughly four substantive unresolved diagnostic exchanges with at least one concrete failure. Do not count greetings, confirmations, status checks or tool polling. After the symptom is verified gone, resume the interrupted sub-skill.
- **To auditor**: before pushing changes that touch auth, permissions, tenant isolation, payments, sensitive data, uploads, webhooks, database schema, deployment, URL parameters or shared state; before a release; on any audit request. Ordinary implementation does not become a full audit by default.
- **Evolver, silent tracking**: start tracking after a second accepted correction, a failed attempt that changes the approach, a third work phase, three material candidates, or when closeout, commit or release begins. At an implicit closeout, exit silently if nothing durable is worthwhile; otherwise propose one action and wait for confirmation. Explicit requests authorize safe local writes.
- **Back to planner**: when execution or audit exposes an unplanned decision about scope, architecture or data.

## Closing a cycle

A cycle is closed when the Do result has evidence, the Check found no open blocking issue, and Act either recorded a guard or stated that none was worthwhile. Report which stages ran, the evidence for each, and any stage skipped with its reason.
