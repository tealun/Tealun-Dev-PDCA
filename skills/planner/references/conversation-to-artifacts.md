# Conversation To Artifacts

Use this reference to guide early user discussion and convert it into durable planning documents.

## Intake Map

Capture these fields, inferring when evidence is available:

| Area | Questions | Artifact |
|---|---|---|
| Product | Who is it for, what job does it do, what pain is urgent? | PRD / core dev doc |
| Workflow | What are the main user journeys and admin journeys? | page/route map, specs |
| Platform | Web, mini program, mobile, desktop, API, internal tool? | architecture doc |
| Business | Pricing, roles, entitlements, lifecycle, operations? | specs, database model |
| Integrations | Which external APIs, webhooks, payments, auth, AI providers? | integration specs, M0 spikes |
| Data | What entities, ownership, retention, auditability, seed data? | schema, migration plan |
| Security | Auth, RBAC, tenant isolation, PII, abuse, rate limits? | security/compliance docs |
| Operations | Deployment, environments, backups, rollback, logs? | setup/deploy docs |
| Verification | How will we know the first slice works? | task gates, audit checklist |

## Discussion Rules

- Prefer "Here is what I understand; here are the 3 things blocking the planning docs" over a long questionnaire.
- Treat existing docs/code as evidence and user statements as decisions until they conflict.
- Record assumptions explicitly with an owner and expiry condition.
- Translate vague wishes into testable statements:
  - "简单后台" -> pages, roles, allowed actions, forbidden actions.
  - "安全一点" -> auth model, permission matrix, data isolation, audit logs.
  - "先跑起来" -> M1 walking skeleton with exact success path.
- For external platforms, require real evidence when behavior affects architecture: request/response samples, error codes, dashboard screenshots, callback payloads, quota/rate-limit docs.

## Understanding Card

Start substantial planning with this compact card:

```markdown
## Understanding Card

- Target users:
- Core problem:
- First-stage goal:
- Primary workflow:
- Known constraints:
- High-risk surfaces:
- Architecture-affecting unknowns:
```

Rules:

- Keep it short enough for the user to correct quickly.
- Put unclear but non-blocking details under `Assumptions`, not as questions.
- Ask for correction only where a wrong assumption would change architecture, data, compliance, or milestone order.

## Planning Ledgers

Maintain these three lists in every full planning cycle:

```markdown
## Decisions

- <confirmed fact or choice>

## Assumptions

- <reasonable default> — until <condition/user correction>

## To Verify

- <unknown fact> — owner: <M0/M1 task or evidence source>
```

Rules:

- A `Decision` can come from user confirmation, existing docs, code, or authoritative platform docs.
- An `Assumption` must be safe to proceed with and easy to revise.
- A `To Verify` item needs an evidence format: screenshot, request/response sample, command output, platform dashboard value, or production constraint.
- Do not leave `To Verify` items as chat history. Convert them into task gates.

## Blocking Question Pattern

Ask at most three questions per turn. Each question should explain what it unlocks:

```text
我只缺 3 个会影响规划的答案：
1. <question> — 决定 <architecture/data/compliance/milestone impact>
2. <question> — 决定 <impact>
3. <question> — 决定 <impact>

其他我会先按这些假设推进：
- <assumption>
```

If the user does not answer a non-critical item, continue with the stated assumption and record it.

## Confirmation Gate

Before producing the main plan or changing planning artifacts, confirm the phase contract:

```markdown
我理解：本阶段要产出 <artifact set>，完成标准是 <done_definition>，
验证方式是 <validation_method>。如果 <fail_condition>，就先停在 M0/M1 gate。
对吗？[是 / 有偏差]
```

Use this gate for:

- Creating the first full docs/database/audit plan.
- Turning a vague idea into a repo planning structure.
- Declaring readiness for M1 or implementation.
- Any planning change that affects database, auth, compliance, production, or external platform integration.

Skip or compress it only for small read-only advice.

## Artifact Set

For a serious app, aim to produce these before business coding:

1. `docs/README.md` or root `README.md`: index, reading order, maintenance rules.
2. `docs/00_core/00_01_PRD.md` or `00_01_Dev_Doc.md`: product goal, roles, architecture, stack decisions, milestone map.
3. `docs/00_core/00_02_Database_Schema.md`: schema responsibilities, entity list, isolation model, migration rules.
4. `docs/00_core/00_03_Pages_Routes.md` or API/page map: frontend routes, backend route modules, auth boundaries.
5. `docs/01_specs/`: one file per major feature/integration.
6. `docs/02_tasks/`: M0/M1 gates, implementation plan, deferred list.
7. `docs/03_compliance/`: only when PII, payments, children, health, finance, enterprise data, or regulated markets are involved.
8. `docs/99_audits/`: implementation-readiness audit before coding.
9. `database/`: baseline schema, migrations, RLS/permissions, seed data, validation scripts.

## Gate Pattern

Use this for M0/M1 task files:

```markdown
# 02_00 <Milestone Or Spike>

版本: v1 · 日期: YYYY-MM-DD · 归属: <owner/domain>
关联: <core docs/specs/audit findings>

目的: <why this gate exists>

## Checklist

| # | Item | Owner | Status | Evidence |
|---|------|-------|--------|----------|
| 1 | <fact to prove> | | ☐ | <sample/log/screenshot/link> |

## Done

- <observable condition>
- <docs updated when facts differ>

## Fail

- <condition that blocks later work>
- <fallback or decision needed>
```

## Planning Completion Criteria

The planning phase is complete when:
- A new agent can read the docs index and know where facts live.
- Unknowns are isolated into tasks, not hidden in core docs.
- Database baseline and migration policy are clear enough to execute.
- M0/M1 gates define evidence, done, and fail conditions.
- A readiness audit says what can start and what must wait.
