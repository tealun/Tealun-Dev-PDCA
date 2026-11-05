# Audit And Readiness

Use this reference to audit planning artifacts before implementation begins.

## Readiness Verdicts

Use one of:

- `Ready for M0`: enough context to run fact-finding spikes.
- `Ready for M1 walking skeleton`: core assumptions are proven; build one vertical path only.
- `Ready for implementation`: specs, schema, operations, and verification are coherent.
- `Blocked`: a P0 unknown or contradiction prevents safe coding.

Verdicts must be actionable. Always pair the verdict with:

- `Can start now`: exact phase or slice.
- `Must wait`: blocked phase or module.
- `Evidence needed`: shortest list of facts that would change the verdict.
- `Next artifact`: the next doc, task gate, schema draft, or audit to create.

## Severity

| Severity | Meaning |
|---|---|
| P0 | Must resolve before the next phase; current plan may fail, leak data, or force rework. |
| P1 | Resolve before coding the affected module. |
| P2 | Can defer, but record ownership and trigger condition. |

## Planning Audit Dimensions

Audit these dimensions, adapting to project shape:

1. Product clarity: users, jobs, roles, non-goals, success metrics.
2. Architecture fit: stack, runtime lifecycle, module boundaries, deployment target.
3. External facts: platform APIs, payments, auth, webhooks, AI providers, quotas, callback payloads.
4. Security: auth, RBAC, tenant/user isolation, PII, rate limits, raw body/webhook validation, log redaction.
5. Database: schema baseline, migrations, RLS/permissions, indexes, lifecycle, seed/backfill/repair.
6. API/page contracts: route map, request/response, error codes, auth boundaries, pagination.
7. Compliance: privacy notice, consent, retention, children/education/finance/health/enterprise obligations if applicable.
8. Operations: environments, secrets, deployment, backup, rollback, monitoring, health checks.
9. Verification: tests, migration checks, acceptance criteria, M0/M1 done/fail gates.
10. Documentation governance: source-of-truth map, no duplicated drifting facts, docs sync rules.

## Report Template

```markdown
# 99_NN — <Topic> — <Date>

## Scope

- Project phase: <idea/M0/M1/pre-implementation>
- Reviewed artifacts: <files>
- Verdict: <Ready for M0/M1/implementation/Blocked>

## Summary

- P0: <n>
- P1: <n>
- P2: <n>
- Main risk: <one sentence>

## P0 — Must Resolve

| ID | Status | Title | Evidence | Impact | Recommendation |
|---|---|---|---|---|---|
| A-P0-1 | Open | <issue> | <file/section> | <risk> | <fix> |

## P1 — Resolve Before Module Coding

...

## P2 — Deferred

...

## Gates

- Can start now: <M0/M1/specific slice>
- Must wait: <blocked slice>
- Evidence needed: <list>

## Doc Updates Needed

- <file and required update>
```

## Go/No-Go Rules

- If an external platform behavior is unverified and affects identity, payment, permissions, or data shape, block implementation of that path and create an M0 spike.
- If public access and tenant/user isolation conflict, treat as P0.
- If runtime/database versions are already EOL or near EOL for a new project, treat as P0/P1 depending on deployment timeline.
- If schema docs define tables but not ownership/isolation/constraints, treat as P1.
- If API docs omit auth or permission boundaries, treat as P1.
- If production migration instructions are not copy-pasteable for the user's actual environment, treat as P1.
- If docs duplicate facts across multiple sources, define a single source before implementation.

## Go/No-Go Confirmation

Before telling the user a project can move from planning into M1 or implementation, run this check:

```markdown
## Readiness Gate

- Done definition:
- Validation method:
- Fail condition:
- P0 unknowns:
- P1 before-module items:
- Verdict:
```

Rules:

- If any P0 unknown exists, verdict cannot be `Ready for implementation`.
- If a P0 unknown affects only one integration, allow unrelated M0/M1 work and clearly name the blocked slice.
- If validation depends on user-provided evidence, say exactly what evidence is needed.
- Do not claim readiness from prose alone; anchor it to docs, task gates, schema files, platform evidence, or audit findings.

## Verification Discipline

- Verify planning claims against files when a repo exists.
- Do not trust status headers; check the actual content and related code/docs.
- For every finding, include concrete evidence: file, section, command output, or missing artifact.
- When a finding is fixed or deferred, update its status in the audit file and move deferred items into the deferred file.
