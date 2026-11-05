---
name: evolver
description: "Track verified fixes, findings, corrections, decisions, failed attempts, and delivery lessons across a work cycle; distill worthwhile items into durable guards, mandatory project evolution-ledger records, planning gates, rules, skill refinements, and next-cycle inputs. Use when the user invokes $evolver, asks for a retrospective or to learn from what happened, asks to follow the conversation, close the PDCA loop, prevent recurrence, or persist lessons, or when a work cycle closes. Without explicit invocation, run one advisory check once the user's second correction in a cycle has been applied without being rejected, and one at closeout (summary, handoff, commit, release). Do not use for unresolved symptoms or broad discovery audits. 复盘、总结经验、吸取教训、下次别再犯、防止再犯、沉淀经验、落盘、固化规则、闭环。"
argument-hint: "Name the lesson, fix or correction to close, its evidence, and whether to persist now or only propose."
user-invocable: true
disable-model-invocation: false
version: 1.2.1
---

# Evolver

Close the Act stage of PDCA. Convert verified evidence from a completed cycle into the smallest durable guard that would prevent or expose the same failure class earlier.

A local fix removes today's symptom. A systemic guard changes tomorrow's default. An evolution-ledger record makes that verified change discoverable and owned. Do not confuse these three artifacts, manufacture process for a one-off issue, or institutionalize an unproven diagnosis.

## References

- Read [references/evolution-method.md](references/evolution-method.md) when classifying failed controls, selecting systemic actions, maintaining evolution ledgers, or handling multi-cause lessons.
- **Mandatory before every write or closure claim:** read [references/persistence-and-ledger.md](references/persistence-and-ledger.md) completely before creating or updating guards, evolution records, planning gates, audit statuses, project rules, or detailed cycle records. No read evidence means no write and no `已落盘` claim.

For a small lesson with one obvious guard, the method reference may be unnecessary; the persistence reference is never optional when writing.

## Invocation Modes

Determine the mode from the user's message, not merely from the fact that the skill was loaded.

### Direct mode

Use direct mode when the user:

- invokes `$evolver`;
- explicitly asks to close and persist the loop;
- asks to固化、落盘、沉淀、更新规则/测试/文档/技能, or otherwise clearly requests the durable action.

Direct mode authorizes safe local persistence within the boundary below. Execute without another confirmation unless the selected action changes architecture, schema, permissions, production/deployment state, external systems, or other material product behavior.

### Advisory mode

Use advisory mode when Evolver was selected implicitly after completed work and the user did not request persistence.

Evaluate internally whether all are true:

1. the lesson and local outcome have concrete evidence;
2. recurrence is credible, not merely imaginable;
3. a specific guard can catch the failure earlier;
4. an authoritative artifact or owner exists;
5. the expected value exceeds the maintenance and process cost.

If any condition fails, exit silently: do not write, ask, or add an Evolver section to the user's response.

If all conditions pass, do not write yet. Present only:

```text
闭环建议：<verified lesson and recurrence risk>
落盘建议：<systemic guard path + project evolution-ledger path>
确认：是否执行？（是 / 否）
```

Treat “是” or an equivalent confirmation as direct mode and persist immediately. Treat refusal as final; do not re-raise the same proposal unless new evidence materially changes it.

### Tracking mode

Use tracking mode when `$evolver` is invoked before or during a multi-step work cycle, or the user asks Evolver to follow the conversation. Until closeout, maintain a compact internal candidate register and update it after material events, not every message:

```text
Candidate ID | event/turn | confirmed fact or correction | evidence | possible failed control | status
```

Capture accepted user corrections, changed decisions, failed attempts, verified fixes, scope changes that invalidate earlier learning, and evidence that proves or disproves a candidate. Merge duplicates and mark superseded items; do not prematurely turn candidates into conclusions. Keep the register available across planning, implementation, verification, and closeout. If context compaction or a handoff is imminent, preserve it in the conversation summary or established task-state mechanism. Do not create a repository artifact merely to hold unverified candidates unless the user explicitly requests a durable running journal.

### Implicit checkpoints

Without an explicit invocation, Evolver does not track the conversation as it goes. It runs one advisory evaluation at each of two points:

1. after the user's second correction in the same cycle has been applied and the user has not rejected the result (a cycle runs from the user's goal or accepted plan to its closeout; a reply that finishes one step while the goal is still open is not a closeout);
2. at closeout: when the user or workflow begins a summary, handoff, commit, release, or the cycle ends.

At each point, run the Cycle-wide Evidence Sweep over the turns and artifacts available, then apply Advisory mode: exit silently when a condition fails, otherwise present the three-line proposal. An implicit checkpoint grants no write authority, and its working list is discarded afterward; only tracking mode keeps a candidate register between events. A silent exit at the first checkpoint does not suppress the closeout checkpoint; a refused proposal is not raised again (see Advisory mode).

## Operating Boundary

Use only after concrete evidence exists from a verified fix, audit, release, incident, accepted user correction, or completed delivery cycle.

Do:

- identify the ineffective control that allowed the issue to survive;
- choose the earliest reliable and proportionate prevention or detection point;
- update a directly relevant test, gate, authoritative document, rule, or skill when authorized;
- verify that the new guard catches the target failure class;
- feed unresolved or generalizable constraints into `$planner`.

Do not:

- diagnose an unresolved symptom—route it to `$bugfixer`;
- perform broad risk discovery—route it to `$auditor`;
- replace bounded implementation—use `$tasker`;
- auto-apply architecture, schema, permission, production, deployment, or broad code changes;
- claim closure merely because a retrospective document exists.

## Entry Gate

Establish:

- `trigger` — completed fix, finding, release, incident, correction, or workflow failure;
- `evidence` — diff, test, audit item, log, screenshot, acceptance result, or outcome;
- `local_fix_status` — verified, partially verified, unresolved, or not applicable;
- `affected_path` — product or engineering path that failed;
- `recurrence_risk` — credible condition under which the failure could recur.

Separate `Confirmed`, `Inference`, and `Unknown`. Never persist an inference as a confirmed root cause. If the local symptom should be fixed but is not verified, stop evolution and route the work to `$bugfixer` or `$tasker`.

The newest user correction invalidates affected learning and downstream actions. Replace any persisted wrong statement before continuing.

## Cycle-wide Evidence Sweep

Before reconstructing lessons in direct mode or at an implicit checkpoint, build the candidate source from the whole relevant work cycle, not merely the newest exchange.

1. Define the cycle boundary at the earliest user goal, accepted plan, incident, audit, or delivery request that led to this closeout.
2. Scan every available turn inside that boundary, plus relevant diffs, tests, logs, screenshots, task state, and persisted artifacts.
3. Extract material corrections, decisions, failed attempts, verification results, recurrence risks, and invalidated assumptions into a working list (the candidate register, in tracking mode).
4. Reconcile later evidence against earlier candidates. Mark each `Confirmed`, `Inference`, `Unknown`, `Superseded`, or `Rejected`.
5. Group confirmed candidates by shared failed control and rank them by recurrence credibility, impact, breadth, and guard value.
6. Only then select what deserves persistence. Recentness is not a selection criterion.

When the full cycle is unavailable because earlier turns were truncated, compacted without a register, or occurred in another thread, do not claim a complete conversation review. Use available artifacts to reconstruct what is provable, state the coverage gap, and ask for missing history only when it could materially change the selected durable action. Never substitute the latest visible point and present it as the cycle summary.

## Persistence Preflight

Before writing anything, use tools to:

1. Resolve the project root with `git rev-parse --show-toplevel` when inside Git; otherwise use the explicit workspace root and state that Git verification is unavailable.
2. Search the project for an existing evolution ledger, including `docs/98_evolution/evolution-ledger.md`.
3. Read the existing ledger when found and preserve its schema, ID style, and ownership convention.
4. Resolve these absolute paths internally:

```text
Project root:
Systemic guard artifact:
Evolution ledger:
Closure target:
```

Resolve the evolution-record path in this order:

1. explicit user-specified ledger path;
2. existing project evolution ledger;
3. `<project-root>/docs/98_evolution/evolution-ledger.md`, creating the directory and file when absent.

Do not redirect the evolution record to a checklist, audit report, `.gitignore`, source file, chat response, or arbitrary documentation because the ledger directory is missing. Creating the standard directory is authorized in direct mode.

## Core Workflow

### 1. Reconstruct the lesson

Run the Cycle-wide Evidence Sweep first, then state internally for each shortlisted candidate:

```text
Expected control or behavior:
Observed failure:
Verified local change:
Failed earlier control:
Credible recurrence condition:
```

Reject “test more,” “communicate better,” “be careful,” “human error,” or “AI error” as root causes. Name the missing or ineffective control.

Do not select a lesson only because it is easy to write or appeared near the end. Explain internally why each persisted item outranks confirmed candidates that were not selected.

### 2. Select one primary systemic action

Choose the lowest-cost action at the earliest reliable point:

1. **Prevent** invalid state through types, schema, permissions, constraints, or simpler architecture.
2. **Detect automatically** with regression/contract tests, CI checks, static rules, monitors, or migration checks.
3. **Gate explicitly** with a planning decision, acceptance rule, review gate, deploy checklist, or audit scope.
4. **Teach the system** through authoritative docs, project instructions, or a reusable skill.
5. **Track consciously** with owner, reason, evidence needed, and revisit condition when stronger action is disproportionate.

Prefer prevention and automatic detection over reminders. Add multiple layers only when consequence and recurrence risk justify them.

### 3. Define the two-artifact action contract

For closure beyond `Corrected`, distinguish:

- **Systemic Guard:** the test, rule, checklist, constraint, monitor, or other control that prevents or detects recurrence.
- **Evolution Record:** the project-ledger row that records evidence, root cause, guard, verification, closure level, and next-cycle input.

Changing a guard does not substitute for writing the evolution record. Writing the evolution record does not prove the guard works.

For every action identify:

- authoritative artifact or execution surface;
- owner;
- protected invariant;
- observable guard verification;
- rollback/removal condition when relevant.

When the guard is written text (a rule, checklist, instruction, or skill change), remove escape hatches before writing it: anchor each prohibition on the behavior, not on a motive (“do not do X in order to Y” leaves “that was not my aim” as an exit); delete pre-planted excuses (“users rarely need…”, “usually fine to…”); add no exemption the agent can claim for itself. This is the same rule-text check as `$tasker`'s Delivery Gate.

Preserve existing repository conventions and one source of truth. Ask for a decision only when evidence cannot safely determine architecture, schema, permissions, production behavior, or domain intent.

### 4. Apply within authorization

In direct mode, safe local persistence is limited to directly relevant non-production tests, documentation, checklists, planning gates, project rules, skills, and the established evolution ledger. Advisory mode must receive confirmation first. Use `$tasker` for broader implementation.

When later evidence verifies the guard of an existing open ledger row, upgrade that row in place as the persistence reference describes instead of appending a new one. For ledger writes, prefer `scripts/append_evolution_ledger.py` so directory creation, schema checks, escaping, duplicate-ID rejection, and read-back are deterministic. If the script cannot be used, follow the persistence reference exactly; do not silently invent another destination.

Every persistence claim requires an actual write and read-back verification. No verified write means `待确认` or `未落盘`, never `已落盘`. Do not commit, push, deploy, migrate, or contact external systems unless separately requested.

### 5. Prove both paths

Verify:

```text
original trigger → local fix → symptom no longer present
same failure class → new guard → prevented or detected earlier
verified guard → project evolution ledger → record exists at the resolved path
```

Use a realistic regression case when possible. A document edit alone does not prove prevention, and a green build does not prove the guard detects the target failure.

Assign the highest proven level:

- `Corrected` — local symptom is verified fixed.
- `Guarded` — a repeatable control catches the same failure class.
- `Institutionalized` — the guard is verified, its source of truth and ownership align, and the evolution record is written and read back from the resolved project ledger.
- `Fed forward` — the lesson is also linked into the next planning cycle.

The PDCA loop is closed only at `Institutionalized` or `Fed forward`.

Hard ceilings:

- No realistic guard execution or verification → at most `Corrected`.
- No evolution-ledger update → at most `Guarded`; never claim `已落盘`, `Institutionalized`, or `Fed forward`.
- A document edit alone is not guard verification.

### 6. Feed the next cycle

Route unresolved or generalizable lessons to `$planner` as a confirmed decision, assumption to verify, M0 spike, M1 acceptance gate, non-goal, protected invariant, or architecture/data/security/operations/compliance constraint. Do not leave durable lessons only in chat.

## Cross-Skill Loop

```text
planner → tasker → auditor → bugfixer → evolver
   ↑                                      |
   └──────────────────────────────────────┘
```

`evolver` may follow a successful release or process review directly when no defect exists.

## Output Contract

After persistence or a direct-mode closeout, return no more than six short lines and distinguish the guard from the ledger:

```text
闭环：<Corrected | Guarded | Institutionalized | Fed forward>
结论：<one verified lesson>
防线：<已写入/未写入 + absolute path + guard verification>
台账：<已追加/未追加 + absolute path + row read-back result>
验证：<target failure-class check and result>
待办：<only when a material action remains>
```

Omit `待办` when empty. Never use the generic phrase `已落盘` unless the project evolution ledger was actually updated and read back. If cycle coverage is incomplete and material, append it briefly to `结论` or `待办`; never imply a full-history sweep. In advisory mode, use only the three-line proposal from Invocation Modes; when evolution is not worthwhile, emit nothing. Keep detailed cards, taxonomies, and evidence walkthroughs internal or in the persisted artifact unless the user requests detail. Never claim closure without guard verification.

---

Part of Tealun Dev PDCA by Tealun · https://github.com/tealun/tealun-dev-pdca · MIT
