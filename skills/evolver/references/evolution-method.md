# Evolution Method

Use this reference for root-cause classification, systemic-action selection, or multi-item evolution work.

## Evolution Card and Ledgers

Begin with a cycle-wide candidate register when work spans multiple turns:

```text
Candidate ID | event/turn | fact/correction | evidence | possible failed control | status
```

Populate it from the earliest relevant goal through verification, including later evidence that supersedes or rejects earlier candidates. Use `Confirmed`, `Inference`, `Unknown`, `Superseded`, or `Rejected`. Merge repeated symptoms by shared failed control. Do not rank by conversational recency.

For shortlisted confirmed candidates, capture internally:

```text
Trigger:
Current fix status:
Recurrence risk:
Failed control:
Evolution goal:
Protected invariants:
Systemic guard:
Evolution ledger:
```

Maintain only when the cycle needs them:

- `Lessons` — verified learning and evidence.
- `Systemic Actions` — durable change, owner, and verification.
- `Next-cycle Inputs` — decisions, spikes, gates, and constraints for Planner.

Use this compact learning statement:

```text
We expected <control or behavior>.
Instead <observed failure> happened.
The verified local fix changed <causal component>.
The earlier control failed because <specific missing/ineffective control>.
Without a systemic action, recurrence is credible when <condition>.
```

## Failed-Control Classes

| Primary class | Signal | Earliest useful control |
|---|---|---|
| Planning gap | requirement, role, data rule, or external fact was undecided | decision, M0 spike, acceptance criterion |
| Execution gap | scope drift, incomplete action, unsupported completion claim, or wrong persistence surface | task contract, path preflight, confirmation boundary, evidence rule |
| Design/contract gap | UI, API, schema, permission, or ownership contract was ambiguous | spec, interface contract, schema rule |
| Test gap | known correct behavior lacked executable coverage | regression, integration, contract, or E2E test |
| Audit gap | relevant risk dimension or critical path was not inspected | audit scope, detector, checklist, severity rule |
| Documentation drift | implementation and source of truth diverged | ownership and documentation-sync rule |
| Runtime/operations gap | deployment, config, migration, monitoring, or rollback control was absent | runbook, delivery gate, health check, alert |
| Skill/agent gap | repeated intent or workflow failure by agents | trigger, boundary, procedure, or validation update |

Choose one primary class and only contributing classes that change the action. A person or model making a mistake is the trigger; the root cause is the control that failed to prevent, detect, or contain it.

## Action Selection Tests

For each candidate action ask:

1. Would it have prevented or detected the original failure earlier?
2. Is it attached to the authoritative artifact or execution path?
3. Can it be verified repeatedly rather than trusted as prose?
4. Is its maintenance cost proportionate to recurrence likelihood and impact?
5. Does it protect already accepted behavior and avoid unrelated scope?
6. Will the verified lesson be discoverable in the established project evolution ledger?

Reject actions that only restate the lesson, duplicate an existing control, create ceremony without a testable effect, or confuse guard placement with ledger placement.

## Multi-Item Prioritization

Group lessons by shared failed control, not by incident chronology. Prefer one guard that covers a verified class of failures over several reminders. Keep independent risks separate when they need different owners or verification.

Order actions by:

1. severe and credible recurrence;
2. earliest reliable prevention/detection;
3. prerequisites for other guards;
4. low-cost improvements with broad proven coverage;
5. explicitly deferred items with revisit conditions.

Before selecting, compare every confirmed candidate from the cycle. Record internally why omitted candidates are duplicate, superseded, weakly evidenced, low recurrence, already guarded, or disproportionate to persist. This prevents the last visible lesson from becoming the default merely because it is convenient.

## Closure Calibration

- `Corrected` requires proof of the local outcome.
- `Guarded` requires a repeatable control and a target failure case.
- `Institutionalized` additionally requires authoritative placement and ownership plus a verified project evolution-ledger record.
- `Fed forward` additionally requires a linked next-cycle decision or gate.

Do not skip levels based on intention. Without a ledger update, closure is at most `Guarded`. If runtime access or realistic test data is unavailable, name the verification gap and report the lower proven level.
