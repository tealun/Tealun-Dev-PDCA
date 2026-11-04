# Persistence and Evolution Ledger

Read this reference completely before every Evolver write or closure claim.

## Non-Substitution Rule

Evolver persists two different things:

1. a **Systemic Guard** in its authoritative execution surface;
2. an **Evolution Record** in the project's evolution ledger.

A test, checklist, `.gitignore`, project rule, or source edit may be the guard, but none is the evolution ledger. A ledger row records the evolution, but does not prove that the guard works.

## Persistence Boundary

Prefer existing repository conventions. Direct-mode persistence (explicit `$evolver`, a clear persistence request, or confirmation of an advisory proposal) is limited to directly relevant local, non-production artifacts such as:

- an established retrospective or continuous-improvement record;
- a focused regression test or check when the requested evolution includes implementation;
- authoritative documentation, project instructions, checklists, or planning gates;
- the established project evolution ledger, or `docs/98_evolution/evolution-ledger.md` when none exists.

Implicit activation alone is not write authorization. In advisory mode, propose one artifact and guard, then wait for confirmation. Do not silently apply architecture, schema, permission, production, deployment, broad workflow, or external-system changes. Record the proposed action and route its execution through `$tasker` when it exceeds the request.

If one material uncertainty, write restriction, missing workspace, or source-of-truth conflict blocks persistence, do not write a speculative record. Return that single blocker; after confirmation, persist without repeating the retrospective.

## Guard and Ledger Placement

Place the systemic guard in the earliest authoritative test, rule, checklist, gate, constraint, or execution surface.

Separately resolve the evolution record in this order:

1. explicit user-specified ledger path;
2. existing project evolution ledger discovered by search;
3. `<project-root>/docs/98_evolution/evolution-ledger.md`.

Read an existing ledger before appending. Preserve its schema and ID convention. If no ledger exists, create the standard directory and file in direct mode. Absence is not a reason to write the record elsewhere or skip it.

Suggested fallback:

```text
docs/98_evolution/
  evolution-ledger.md
  cycles/
    <date-or-cycle>-<topic>.md
```

Keep evolution records separate from audit reports. Link the source audit item rather than copying it.

## Minimum Ledger Schema

```markdown
| ID | Trigger/Evidence | Root Cause | Local Fix | Systemic Action | Guard Verification | Closure Level | Next Planning Input |
|---|---|---|---|---|---|---|---|
```

Entries must distinguish confirmed evidence from inference, link their source where practical, use a unique ID, escape `|`, and remain concise.

Prefer `scripts/append_evolution_ledger.py` for deterministic creation, schema validation, duplicate-ID rejection, append, and read-back.

### Upgrading an open row

Rows at `Corrected` or `Guarded` are open. When later evidence verifies the guard of an existing row (the guard caught the failure class, or the planned verification ran), edit that row in place: update `Guard Verification` with the new evidence and date, and raise `Closure Level`. Do not append a second row for the same lesson. Read the row back after editing and run the ledger check the project uses (for example `scripts/check_ledger.py`).

The candidate register is a working source, not automatically a durable ledger. Persist only selected, verified lessons. When the user explicitly requests a running journal, place it in an existing task-state convention or a clearly labeled draft artifact, retain source turn/artifact references, and keep unverified candidates out of authoritative rules until closeout.

## Audit and Status Coordination

When an audit finding triggered evolution:

- update its status only after the relevant action is verified and document edits are in scope;
- distinguish `Fixed locally` from `Guarded against recurrence`;
- link deferred systemic work to the original finding and evidence;
- do not rewrite the audit's original observation to make the later action appear inevitable.

## Write Verification

After persistence:

1. read back every changed guard artifact;
2. run the guard or the narrowest relevant validation;
3. read back the exact evolution-ledger row;
4. confirm the row's schema, unique ID, links, evidence, and closure level;
5. ensure the statement does not promote inference to fact;
6. inspect the worktree for unintended changes;
7. report absolute guard and ledger paths separately.

No verified ledger write means `台账：未追加`; closure cannot exceed `Guarded`. No guard execution or proof means closure cannot exceed `Corrected` unless the evolution is purely a planning feed-forward with independently verified ownership and gate placement.
