# Evidence and Reporting

Use this reference before accepting findings or writing an audit report.

## Evidence State Machine

Every candidate follows:

```text
Candidate → Context inspected → Reproduced or statically proven
          → Severity calibrated → Accepted or rejected → Reported
```

For each accepted finding record:

- trigger, reachable context, and affected baseline;
- expected invariant and actual behavior;
- reproduction or concrete static proof;
- impact and affected scope;
- file/line or configuration location;
- command/inspection method and observed result;
- conclusion type, severity, confidence, and remaining assumptions.

## Conclusion, Severity, and Confidence

Conclusion types:

- `Confirmed` — reproduced or directly proven through a reachable path.
- `Likely` — strong static evidence; runtime confirmation unavailable.
- `Exposure` — risky surface exists; exploit/failure path not established.
- `Verification gap` — important property could not be checked.
- `N/A` — relevant surface does not exist.

Severity and confidence are independent:

- `P0` — immediate material risk such as exploitable security failure, data loss/corruption, critical outage, or broken core invariant.
- `P1` — should be fixed before the affected release/module; meaningful correctness, safety-net, operability, or maintainability risk.
- `P2` — bounded improvement with low immediate impact.
- Confidence: `High | Medium | Low`.

Do not inflate structural smells to P0. Missing coverage is normally a verification gap or P1 safety-net issue, not proof of broken behavior.

## Rejection and Downgrade Rules

Reject or downgrade when evidence is only:

- a keyword match without surrounding context or reachability;
- an unused dangerous function or inactive configuration;
- a scanner/advisory without resolved-version and usage checks;
- generated, example, fixture, vendored, or stale-commit content;
- a missing test used to assert the underlying feature is broken;
- a label from a tool or prior report without reproduction on this baseline.

Record rejected high-signal candidates when doing so explains why a scary match is not a finding.

## Compact Report Template

```markdown
# <Audit title>

## Scope
- Baseline: <branch@HEAD or non-Git snapshot>; worktree <state>
- Included: <paths/changes>
- Depth and reason: <quick|standard|deep>
- Evidence limits: <none or list>

## Verdict
- P0: <n> | P1: <n> | P2: <n>
- Main risk: <one sentence>

## Critical Paths
- <path>: <Healthy|At risk|Broken|Not verified> — <evidence>

## Confirmed Strengths
- <control worth preserving>

## Findings
| ID | Severity | Type / Confidence | Status | Finding | Path / Dimension | Evidence | Remediation |
|---|---|---|---|---|---|---|---|

## Verification Gaps
- <property, reason, evidence needed>

## Coverage
- 1 Architecture: <result>
- ...
- 12 Deploy & Ops: <result>

## Evidence Log
- Accepted: <candidate → proof>
- Rejected: <candidate → reason>
```

Use existing repository naming/status conventions first. If a new system is explicitly requested, default to `docs/99_audits/99_NN_<short_topic>.md` and keep one `99_9999_deferred.md`. Status values may be `Open`, `Fixed`, `Deferred`, or `Declined`; a deferred entry records its source report, ID, reason, and revisit condition.

## Acceptance Checks

Before delivery verify:

- all file/line references match the baseline;
- every accepted finding has proof and calibrated impact;
- severity and confidence are separate;
- applicable dimensions have a result or named gap;
- required critical paths have health or a blocker;
- strengths and evidence limits are explicit;
- checks did not leave unintended worktree changes;
- report edits, commits, pushes, deployments, and fixes stayed within user authorization.
