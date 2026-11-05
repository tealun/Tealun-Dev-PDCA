# Docs System

Use this reference to create or reorganize the project documentation system.

## Directory Convention

Default structure:

```text
docs/
  README.md
  00_core/
  01_specs/
  02_tasks/
  03_compliance/
  88_planning/
  99_audits/
  design/
```

Meanings:

- `00_core/`: stable facts that future implementation must obey: product, architecture, routes/API, database, AI/integrations, setup.
- `01_specs/`: feature-level requirements and acceptance criteria.
- `02_tasks/`: milestone gates, execution plans, deferred items, spike results.
- `03_compliance/`: privacy, data protection, legal, SDK inventory, regulated-domain obligations.
- `88_planning/`: roadmap, deployment, operations, business planning, disaster recovery.
- `99_audits/`: readiness and quality audits. The latest audit is the status source.
- `design/`: design handoff, images, prototypes, UI references.

## Numbering

- Numbered docs use `NN_MM_Title_With_Underscores.md`.
- Use `_` between numeric prefixes and words or letters. Prefer `00_core`, `01_specs`, `99_audits`, and `99_01_readiness.md`; avoid `00-core`, `01-specs`, and `99-audits` in new projects.
- Audit docs use `99_NN_<short_topic>.md`.
- Deferred audit items live in one `99_9999_deferred.md`.
- Keep filenames short and sortable.

## Source-Of-Truth Rules

- Define one source of truth per domain.
- If docs conflict with code in an existing project, code behavior wins and docs must be updated.
- If multiple docs need the same detail, put the detail in the authoritative doc and link from the others.
- Avoid "current status" claims in indexes when they will go stale; link to latest audit/task status instead.
- Use repository-relative paths in docs.

Recommended domain ownership:

| Domain | Source |
|---|---|
| Product goals and roles | `00_core/00_01_PRD.md` or `00_01_Dev_Doc.md` |
| Tech stack and architecture | `00_core/00_01_*` |
| Database schema | `database/schema.sql` plus `00_core/00_02_Database_Schema.md` |
| API/routes/pages | `00_core/00_03_Pages_Routes.md` or `01_specs/01_02_Api_Spec.md` |
| Environment/setup | `00_core/00_05_Setup_Guide.md` |
| Feature behavior | relevant `01_specs/` file |
| Milestone readiness | `02_tasks/` |
| Audit status | latest `99_audits/` report |

## Maintenance Rules

Add these rules to the docs index or project agent instructions:

- Changing database structure requires updating `database/schema.sql`, migration files, and database docs.
- Changing routes/pages/API contracts requires updating route/API docs.
- Changing AI prompts/models requires updating AI docs and configuration source.
- Changing environment, deployment, or production operations requires updating setup/deployment docs.
- Adding a major feature requires updating PRD/core docs and adding a task/spec when needed.
- Completing a task requires updating task status and, for risky work, landing an audit or verification note.

## Planning Doc Quality Bar

Good planning docs are:
- Concrete enough that an agent can execute without re-asking the same questions.
- Explicit about unresolved facts.
- Cross-linked instead of duplicated.
- Versioned or dated where project state matters.
- Clear about "must", "should", and "later".

Bad planning docs:
- Mix product vision, schema, todos, bugs, and deployment in one document.
- Keep "TODO: verify" in core docs without a task gate.
- List APIs without auth/permission boundaries.
- Describe database tables without ownership, indexes, deletion, and migration strategy.
