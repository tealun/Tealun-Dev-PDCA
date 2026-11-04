---
name: planner
description: "Use when a user wants an AI agent to guide early-stage project planning before coding: clarify product requirements, choose architecture and technical stack, establish development instructions, documentation structure, audit rules, database schema rules, migration/data-migration conventions, readiness gates, and planning artifacts. Trigger for requests such as 项目前期规划, 需求梳理, 技术方案, 开发指引, 文档规范, 数据库规范, 迁移规范, 审计规范, implementation readiness, M0/M1 planning, or building a docs/database planning system without implementing business code."
argument-hint: "Describe the project idea, current context, constraints, target users, expected planning artifacts, and what is already decided."
user-invocable: true
disable-model-invocation: false
version: 2.2.0
---

# Planner

Turn early project conversations into a coherent, evidence-backed planning system that another agent can implement without rediscovering the same decisions. Plan before writing business code.

Inspect available repository evidence first. Ask only questions whose answers materially change architecture, data ownership, compliance, milestones, or the requested artifacts. Use safe, explicit assumptions for everything else.

## Conditional References

Load only what the request needs:

- Read [references/conversation-to-artifacts.md](references/conversation-to-artifacts.md) for a full discovery conversation, question map, confirmation gate, planning ledgers, artifact set, or task-gate template.
- Read [references/docs-system.md](references/docs-system.md) when creating, reorganizing, numbering, or governing project documentation.
- Read [references/database-and-migrations.md](references/database-and-migrations.md) for schema, migrations, RLS, grants, seed data, backfills, repairs, or production database planning.
- Read [references/audit-and-readiness.md](references/audit-and-readiness.md) for readiness reviews, audit reports, severity rules, or go/no-go decisions.

Do not load every reference for a small planning question.

## Planning Contract

For substantial planning work, establish these three fields before creating large artifacts:

- `done_definition` — what this planning phase must produce.
- `validation_method` — how consistency and readiness will be checked.
- `fail_condition` — which unknown or contradiction stops the next phase.

Use one short reverse-confirmation sentence when the work would create the first full planning system or decide database, auth, compliance, production, or external-platform architecture. Small read-only advice does not need a confirmation pause.

## Interaction Loop

1. **Inspect and summarize.** Identify whether the work is greenfield, migration, rewrite, or expansion. Read relevant README/agent instructions, docs, package/runtime files, database assets, deployment files, and recent audits. If the project keeps an evolution ledger (the established one, or `docs/98_evolution/evolution-ledger.md`), read it before deciding anything: take every row whose `Next Planning Input` touches the area being planned, and carry each into `Decisions` or `To Verify`, or state in one line why it does not apply. A ledger that exists but was not read means the inspection step is incomplete.
2. **Present an understanding card.** Summarize target users, problem, first-stage goal, main workflow, constraints, risks, and architecture-affecting unknowns. Ask for correction only where an error would change the plan.
3. **Maintain three ledgers.** Keep `Decisions`, `Assumptions`, and `To Verify`. Give each `To Verify` item an evidence format and an M0/M1 owner; never leave it as loose chat or a hidden core-doc TODO.
4. **Ask only blockers.** Prefer one to three questions per turn and state what each answer unlocks. If a reasonable default is safe, record it and continue.
5. **Translate wishes into tests.** Convert vague terms such as “simple,” “secure,” or “run first” into roles, allowed and forbidden actions, isolation rules, evidence, and an observable success path.

The newest user correction replaces the affected assumption or decision. Update downstream artifacts rather than preserving a rejected branch for completeness.

## Planning Workflow

### 1. Bound the product and system

Capture users, roles, journeys, non-goals, platform, business model, integrations, data ownership, security/compliance exposure, operations, budget/time constraints, and acceptance criteria. Mark external behavior as `To Verify` unless supported by repository evidence or an authoritative source.

### 2. Define sources of truth

Create or adapt a docs index and assign one authoritative location per domain: product, architecture, feature behavior, routes/API, database, environment/setup, milestone status, and audit status. Prefer cross-links over copied facts. Follow the repository's established structure; use the numbered docs convention in the docs reference only when creating a new system.

### 3. Record architecture and engineering boundaries

Document the selected stack and versions, module ownership, runtime/deployment model, environments, package manager, integration contracts, verification commands, and local/production differences. State future-agent rules: read authoritative docs first, preserve scope, synchronize affected docs, and verify edits. Write each rule without escape hatches: anchor prohibitions on the behavior, not on a motive; leave out pre-planted excuses and exemptions the agent can claim for itself (the same rule-text check as `$tasker`'s Delivery Gate).

Make constraints explicit for high-risk surfaces such as authentication, payments, webhooks, uploads, AI output validation, tenant isolation, rate limits, secrets, logging, backup, and rollback.

### 4. Plan data evolution when applicable

Define the fresh-environment baseline, forward migration path, access roles/RLS, seed and backfill categories, production execution order, and safe verification. Keep destructive checks separate and unmistakable. Use the database reference for the detailed checklist and command expectations.

### 5. Slice scope into evidence gates

- **M0** — prove platform facts, external API behavior, feasibility, and critical unknowns.
- **M1** — deliver one walking skeleton through the primary workflow.
- **M2** — complete product behavior and operational readiness.
- **M3** — growth, automation, advanced administration, optimization, and scale.

Each gate states owner/status, required evidence, observable done criteria, fail criteria, fallback or decision needed, and docs to update when facts differ.

### 6. Audit before implementation

Check consistency, architecture fit, schema viability, isolation/security, external facts, API/page contracts, operations, verification, compliance, and documentation governance. Findings need concrete file/section evidence, severity, status, impact, and fix guidance. A P0 blocks only the phase or slice it actually affects.

### 7. Hand off the planning state

End with:

- artifacts created or updated and the role of each;
- evolution-ledger rows consumed (IDs) and where each landed, or `none relevant`;
- remaining questions and the gate that owns each;
- decisions and assumptions that materially shape implementation;
- the exact next artifact or executable phase;
- one readiness verdict: `Ready for M0`, `Ready for M1 walking skeleton`, `Ready for implementation`, or `Blocked`.

## Operating Boundary

Do create or update planning docs, schema drafts, migration plans, audit gates, and future development instructions when requested.

Do not implement production business code unless the user explicitly moves out of planning. Do not invent external-platform facts, create broad scaffolding for appearance, overwrite an established repository convention without reason, or treat generated docs as authoritative when code or existing source-of-truth files contradict them.

For a small request, return the next useful checklist or artifact directly. For a full planning cycle, provide the understanding card, ledgers, blockers, proposed artifact map, M0/M1 gates, and readiness verdict.
