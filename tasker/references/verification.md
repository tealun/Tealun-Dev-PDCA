# Verification Protocol

Read this file for every `M/L` task. It defines how Tasker proves outcomes without turning checks into ceremony.

## Evidence Model

Build an Evidence Ledger:

```text
Action → Artifact → Observation → Requirement → Verdict
```

- **Action** proves execution occurred.
- **Artifact** is the inspectable result of that action.
- **Observation** is what the artifact demonstrates. Write what was actually seen: an output excerpt, a value, or read-back text. A bare label such as “pass”, “OK”, or “no issue” is not an observation.
- **Requirement** is the acceptance item supported by that observation.
- **Verdict** states whether coverage is sufficient.

A changed file or successful command does not automatically prove correctness. Missing coverage means retreat or use an accurate non-confirmed verdict.

For diagnostic work, use a hypothesis ledger before mutation:

```text
Observed fact → candidate cause → predicted distinguishing evidence → check → result
```

Do not convert correlation, code proximity, familiar failure patterns, or a plausible explanation into a root-cause claim. Root-cause evidence must connect the symptom to the causal link and show that changing or controlling that link changes the outcome as predicted.

## Outcome Path

When an effect crosses components, trace the shortest causal path:

```text
input or original failure → changed component → downstream effect → observable outcome
```

For `M`, trace the main success and relevant failure path. For `L`, include critical recovery and external-boundary paths.

### Compact Execution Trace

Use this only as a sequencing example; adapt every check to the actual task:

```text
requirement → prevent expired-session login failures
validation  → relevant auth tests + repeated login exercise
change      → guard the invalid session state + add a regression test
evidence    → tests pass + expired session returns the expected response
invariant   → normal login still succeeds
verdict     → Confirmed, with confidence based on evidence quality
```

## Evidence Quality

Accept evidence only when it is current, relevant, produced from the intended target/environment, and observes the requested behavior or a defensible proxy.

Reject or downgrade evidence when:

- A file changed but behavior was not exercised.
- A command passed while running zero relevant checks.
- Tests do not cover the changed or failing path.
- A build is used to prove business behavior.
- Text search is used to prove runtime correctness.
- A service starts but the requested workflow is not exercised.
- Results come from stale artifacts, the wrong directory, branch, target, or environment.
- Only the happy path was checked when the task concerns an edge or failure case.

## Preserved Invariants

Identify behavior that must remain unchanged and validate it in proportion to risk. Typical invariants include public API compatibility, normal-path behavior, data shape, permissions, performance boundaries, and rollback viability.

For repository work, workspace identity is an invariant. Verification must show that:

- every changed path resolves under the confirmed `target_identity`;
- the reported branch/HEAD belongs to that target;
- no sibling or discovery-only repository was mutated;
- any intentional cross-repository artifact was separately authorized.

`git status` from one repository is insufficient when more than one repository was inspected or touched. Record status for every involved root.

If a cross-project signal occurred, verification must also include the user's explicit target confirmation. Repository similarity, successful tests, or finding the expected feature cannot substitute for that confirmation.

## Implementation Review

Answer with concrete observations:

1. **Plan alignment** — did actual changes stay within confirmed scope?
   - Confirm the repository/path identity as well as the feature scope.
2. **Contract safety** — did interfaces, schemas, configuration, or callers change, and were consumers checked?
3. **Boundary behavior** — were relevant empty, invalid, failure, timeout, concurrency, and rollback paths considered?
4. **Fix quality** — was the cause removed or only the symptom contained? If mitigation was necessary, state its limits and follow-up.

Unsupported answers are verification gaps, not completed checklist items.

## Symmetric Close Check

Mirror the Acceptance Gate:

| Before execution | Before close |
|---|---|
| `done_definition` | requirement coverage and verdict |
| `validation_method` | actual command or observation and result |
| `fail_condition` | failure prevented, reproduced, or explicitly untested |
| expected artifact | actual artifact and location |
| `scope_boundary` | changed surfaces and invariant checks |

If a required row lacks evidence and progress is possible, return to `execute`.

## Depth

| Level | Reads | Checks | Outcome evidence | Boundaries |
|---|---|---|---|---|
| `M` | related imports/config | build plus relevant tests | ledger plus main outcome path | obvious failures and invariants |
| `L` | full affected module and tests | full suite plus static analysis and external anchor | full ledger and critical paths | exhaustive inputs, recovery, rollback |

## Tool-Call Audit

At `verify`, list executive tool calls and their artifacts. This proves execution occurred; use the ledger to prove requirements were satisfied.
