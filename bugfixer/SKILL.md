---
name: bugfixer
description: "Use for full-stack development-time bug fixing when the user reports broken behavior, UI regressions, screenshots that look wrong, console errors, API 400/401/500 failures, persistence problems, incorrect statistics, deployment/runtime failures, CI failures, an external platform rejecting an upload, publish or review, repeated correction, a failed post-change check, or a prior fix that missed the cause. Activate immediately on explicit failure evidence or 'still wrong' feedback, and when diagnosis inside another workflow stalls on a concrete unresolved failure. Reproduce or directly observe the symptom, collect runtime evidence, test competing hypotheses with discriminating checks, isolate the proven responsible layer, make the smallest safe fix, verify the original user-visible outcome, and lock it with a regression test that fails without the fix when the project has a test harness. Do not stop at plausible explanations or close merely because one attempted fix failed."
argument-hint: "Describe the symptom, screenshot/log/error, expected behavior, affected environment, and any recent change."
user-invocable: true
disable-model-invocation: false
version: 1.7.0
---

# Bugfixer

Repair concrete development defects from the user-visible symptom to the smallest proven cause. Preserve the latest product intent, change only the causal chain, and verify that the reported symptom is gone.

When the newest user message corrects the direction, treat the mismatch with that corrected intent as the current bug. Stop extending the rejected direction and protect everything the user already approved.

## Discussion-aware Activation

Enter Bugfixer immediately when an explicit symptom, failing check after a change (including CI, or an external platform rejecting an upload, publish or review), runtime error, or user feedback such as “still wrong” appears during another workflow. Do not wait for the user to invoke the skill or for a turn threshold.

What counts as “still wrong”: the user reports that delivered behavior is broken or does not do what was already agreed (“还是不对”, “doesn't work”, “same error”, a screenshot of the old symptom). A correction that changes or refines what was asked (wording, punctuation, style, naming, a different file inside the confirmed target, or scope) is a requirement change, not a defect: it stays with the surrounding workflow, which retreats to `clarify` or `plan` and reworks. When a message mixes both, the defect part comes here.

If reproduction or direct observation shows the agreed result is actually in place (no defect), stop: report what you observed, with the command output, and hand back to the surrounding workflow without editing. When the report conflicts with an instruction the user gave earlier, quote both and ask which one stands; that is input no tool can obtain. If the symptom is less explicit, this is the fallback threshold, and the only definition of it in the suite (Tasker and dev-pdca refer here): activate on the fourth diagnostic exchange that ends with the same concrete failure still unresolved. One diagnostic exchange is an assistant attempt to explain or change the failing behavior, followed by a user message or check result showing the failure remains. Greetings, status requests, tool polling, repeated confirmations, and unrelated discussion are not exchanges. Without a concrete failure, no count starts.

When Tasker encounters these signals, preserve its task contract and route the defect investigation here. Bugfixer owns diagnosis and repair until the original observable outcome passes; then return control to the surrounding workflow for its remaining acceptance checks.

## Conditional References

Load only the detail required by the symptom:

- Read [references/full-stack-debugging.md](references/full-stack-debugging.md) when the failure may cross layers, the responsible layer is unclear, or a previous fix regressed.
- Read [references/frontend.md](references/frontend.md) for screenshots, layout, interaction, theming, role/view, or client-state defects.
- Read [references/backend-data.md](references/backend-data.md) for API, auth, persistence, storage, metrics, database, or migration defects.
- Read [references/runtime-deploy.md](references/runtime-deploy.md) for production-only behavior, configuration boundaries, CI, deploy sync, process managers, reverse proxies, or stale versions.

Load multiple references only when the observed causal path actually crosses those boundaries.

## Repair Contract

### 1. Capture the symptom

- Record what the user observes, what should happen, where it happens, and what changed recently.
- Treat screenshots, exact logs, HTTP responses, stack traces, and backend errors as evidence.
- Prefer runtime sources over examples, docs, comments, or assumptions.
- If the user corrects the target, restate the corrected outcome and rejected direction before editing.

### 2. Define acceptance

Use an observable result such as “the drawer no longer blocks content,” “the value persists after reload,” or “the route is registered in the running service.” Add the narrowest executable check that can prove it: syntax, typecheck, targeted test, request, log observation, migration inspection, or visual comparison.

### 3. Localize before editing

Identify the first layer that can explain the evidence:

- UI/layout — markup, styles, safe areas, conditional rendering, design tokens.
- Client — handlers, state, cache, navigation, request construction, response mapping.
- Contract — route, method, auth boundary, DTO/schema, status and response shape.
- Backend/data — service, repository, transaction, ownership, database/storage, metrics.
- Runtime — environment, build artifact, migration order, process, proxy, deployed version.
- Product intent — accepted structure, forbidden controls, role-specific behavior, wording.

Trace only far enough to prove the causal chain. If a link is assumed, mark it unverified.

### 3a. Prove the diagnosis

Before a causal edit, maintain a compact diagnostic ledger:

```text
Observation | Candidate cause | Predicted evidence | Discriminating check | Result | Status
```

- Derive candidates from observed code paths, runtime state, logs, requests, data, or reproducible behavior—not familiarity or narrative plausibility.
- Keep at least two competing candidates when the responsible link is not directly observed; include one outside the initially suspected layer when evidence permits.
- Choose the cheapest check whose possible outcomes distinguish candidates. Merely rereading the same code or rerunning the same failing action is not a discriminating check.
- Mark a candidate `proven` only when its predicted evidence is observed and a targeted intervention changes the symptom as predicted. Otherwise keep it `plausible`, `weakened`, or `rejected`.
- Do not edit production code solely to discover whether an unsupported guess is true when a log, breakpoint, request capture, query, focused test, temporary instrumentation, or direct state inspection can decide first.

### 4. Patch the smallest causal chain

- Preserve user-confirmed behavior and unrelated dirty-worktree changes.
- Do not redesign, audit, rename, refactor, or add features unless the repair requires it.
- Respect explicit protected surfaces such as “change A, do not change C.”
- Keep database assets in the database boundary and private/runtime values out of tracked examples.
- If the required repair materially expands scope, explain why before proceeding.

### 5. Verify the reported outcome

- Run the narrowest check that exercises the symptom, then broaden with blast radius.
- Read the first real failing command, line, and exit reason before naming a cause.
- A green build proves buildability, not visual, auth, metric, persistence, or deployment correctness.
- Report exact unverified gaps and required restart, migration, deploy, or user visual confirmation.
- Do not say “fixed” until evidence matches the original or corrected symptom.

### 5a. Lock the fix with a regression guard

After the original symptom is verified gone, make the fix hard to lose:

- When the project has a test harness (unit, integration, end-to-end, contract, or a check script that CI or the documented pre-commit gate runs), add the narrowest automated test that reproduces the original symptom and passes only with the fix. Assert the user-visible outcome or the proven causal link, not an implementation detail that a harmless refactor would break.
- When no harness covers the failing layer, add the closest executable guard the project already runs—a schema or config validation, a lint rule, a smoke script, a startup assertion—or state why none is proportionate.
- When feasible, prove the guard bites with a mutation check: temporarily revert or disable only the fix, run the new test and record that it fails for the expected reason, restore the fix, and record that it passes. Revert only the fix's own hunks (a reverse patch of the fix, or a stash limited to files that hold no other uncommitted work); never leave the revert in place and never touch unrelated work.
- Keep it proportionate. Do not build a new test framework, add dependencies, or broaden scope just to host one test. Skip with a stated reason when there is no harness, the defect lives only in an environment tests cannot reach, or the user declines; report the skip as an unguarded gap.
- A guard that passes with and without the fix is not a guard. Rework it or report it as unverified.

### 6. Continue after a missed fix

A failed repair is new diagnostic evidence, not a reason to stop.

1. Revert or isolate only the agent's disproven change when safe and authorized; preserve unrelated user work.
2. Record exactly which prediction failed and which candidates it weakens or rejects.
3. Inspect the next unobserved link in the causal path and run a materially different discriminating check.
4. Load [references/full-stack-debugging.md](references/full-stack-debugging.md) and expand one boundary outward when two attempts shared the same assumption or layer.
5. Continue while an in-scope observation, inspection, instrumentation, or test can reduce uncertainty.

Never close with “the fix missed the root cause, so I will stop guessing” while meaningful diagnostics remain. Stop only for a concrete blocker: missing authority, inaccessible environment/data, unavailable required input, destructive-risk decision, or exhausted relevant observability. State the blocker and the exact next observation needed. Uncertainty by itself is not a blocker.

## Fast Triage

Use status codes as evidence:

- `400` — compare request shape, content type, enums, and validation schema.
- `401` — check missing/expired auth and public/private route boundaries.
- `403` — check authenticated identity, owner/tenant role, and permission rules.
- `404` — distinguish wrong method/path, missing resource, absent route, stale build, and wrong proxy target.
- `500` — read server logs; inspect nulls, constraints, migrations, storage, and unhandled branches.

When an old protected route returns `401` but a new related route returns `404`, the service and auth layer are live while the new route is absent from the running target. Check deployment version, route registration, build output, and proxy target before changing the client.

For generated artifacts that remain stale or wrong after a fix, compare the source record, stored file/object, metadata or version marker, regeneration trigger, direct/static URL path, and download/preview endpoint before changing render code again. If output semantics changed, require artifact versioning, invalidation, or regeneration plus a regression for old artifacts.

## User Corrections

When the user says a fix is wrong or incomplete:

1. Stop defending the prior implementation.
2. Classify the divergence: intent, visual fidelity, data flow, persistence, contract, runtime, or verification.
3. Restate the corrected target and protected accepted behavior.
4. Remove the rejected direction before adding anything new.
5. Re-check code and runtime facts instead of defending the prior explanation.
6. Search for stale rejected labels, paths, controls, keys, endpoints, or private values after editing.

If a narrow edit caused encoding, line-ending, or whole-file churn, restore the prior content and reapply only the intended change. Stay calm and evidence-led when the user is frustrated.

## Verification Depth

- Small UI change — syntax plus targeted component/page inspection and visual acceptance.
- Client/contract change — client check plus affected server contract test or typecheck.
- Persistence/metrics change — exercise write, readback, reload, identity rules, and affected tests.
- Database/migration change — inspect schema authority, migration state, build/tests, and safe-target checks.
- Runtime/deploy change — verify external behavior after build/restart and compare expected running version.
- User-correction change — scan for the rejected variant and prove only the corrected behavior remains.

## Closeout

Report concisely:

1. Cause and repair.
2. Files or modules changed.
3. Checks and observed results.
4. Regression guard: the test or check added, and the mutation-check result (fails without the fix, passes with it), or the stated reason it was skipped.
5. Remaining restart, migration, deployment, or user confirmation.

Commit or push only when explicitly requested.
