# Recovery Protocol

Read this file after two failures of the same approach, when progress stalls, or before reporting `Blocked`.

## Strategy Reset

Before the next attempt:

1. Capture the exact failure signal and its artifact.
2. List prior attempts and identify their shared assumption or mechanism.
3. Re-check prerequisites using source code, raw responses, logs, official specifications, or direct environment inspection.
4. Form at least two competing explanations, including one that contradicts the leading assumption.
5. Choose a materially different next action and define its success and failure observations before running it.
6. Prefer an observation that eliminates multiple explanations over another speculative mutation.

Changing a timeout, renaming a variable, or rerunning with minor flags is not a distinct strategy unless it tests a different hypothesis. If no distinct mutation strategy remains, continue with safe read-only probes while they can reduce uncertainty. Stop only when no relevant in-scope observation remains or a concrete external blocker prevents it.

## Retreat Rules

- `execute` failure → `plan`: redesign from new evidence.
- incomplete `verify` → `execute`: fill the evidence gap.
- rejected `confirm` → `clarify`: normalize the corrected contract.
- no suitable tool → `clarify`: state the missing capability or authority.

Every retreat states why the previous stage is no longer valid. The main retry and retreat caps remain authoritative.

## Wrong-Workspace Containment

Enter containment as soon as the agent suspects context crossed projects; do not wait for proof or a user complaint. Suspicion includes incompatible product vocabulary, attachments that do not match the workspace, a feature found only in a sibling repository, ambiguous “this/other/previous project” language, or a required write outside the confirmed root.

When triggered:

1. Stop all writes across every involved repository.
2. Capture read-only state for each repository: absolute root, branch/HEAD, clean or dirty state, commits created during the task, and uncommitted paths touched by the agent.
3. Translate ambiguous references into explicit candidates, for example `“this project” = A?` and `“other project” = B?`. Do not infer which mapping the user meant from anger, recency, or feature similarity.
4. Ask the user to confirm both the intended target and the disposition of each artifact: keep, revert uncommitted edits, revert a commit, cherry-pick, or leave untouched. Until answered, do not take the apparently obvious recovery action.
5. Perform only the confirmed recovery. Re-check every repository afterward and report exact remaining state.

Never use a destructive recovery command merely because the agent believes it caused the changes. Existing dirty work may belong to the user, and an apparently wrong repository may actually be the intended sibling project. Containment is automatic; rollback is not.

The first response after detecting a possible wrong target must be deliberately non-executive: freeze, inventory, map, ask. Do not combine the diagnosis and recovery in one tool sequence.

## Blocked Report

Use `Blocked` only when a dependency, authority, input, environment, destructive-risk decision, or exhausted relevant observability prevents meaningful progress. Lack of a confirmed root cause, one or more failed fixes, or reluctance to speculate is not itself a blocker while additional safe diagnostics exist. Report:

- Exact blocker and current evidence.
- Attempts made and why each failed.
- Explanations ruled out and what remains plausible.
- Smallest external action or decision needed.
- First command or step to run after resumption.
- Current artifacts and scope state.

Do not replace this with a vague request for the user to “try manually.”

## Repeated Cause Safeguards

| Cause | Safeguard |
|---|---|
| `hallucination` | require tool evidence and immediate read-back |
| `omission` | list relevant files and dependencies before acting |
| `misread` | quote the exact evidence before interpreting it |
| `tool-failure` | check return codes and distinguish environment failure from task failure |
| `user-ambiguity` | state the assumption and obtain confirmation |
| `logic-flaw` | write competing hypotheses and test the causal chain |
| `wrong-target` | freeze writes, inventory every touched repository, make path mappings explicit, and require recovery confirmation |

