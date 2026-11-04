# Tasker v1.7.0 — Workspace Identity Safety

## Added

- A mandatory `target_identity` field for M/L acceptance gates.
- A Workspace Identity Gate before the first mutation or any cross-repository switch.
- Explicit resolution of ambiguous phrases such as “this project” and “the other project.”
- Wrong-workspace containment that freezes writes and inventories all touched repositories.
- Recovery authorization separated from diagnosis: rollback, revert, move, or cherry-pick requires the user to confirm the concrete project mapping and action.
- Verification that every changed path belongs to the confirmed target and that discovery-only sibling repositories remained untouched.
- Early triggering when the agent merely suspects project-context leakage, before it decides to switch repositories.
- A Post-Error Restraint Gate: detecting a wrong target permits read-only containment, never immediate rollback or compensating writes.

## Incident Class Prevented

An agent starts in repository A, discovers repository B from feature clues, mutates B without confirming the switch, then misreads a correction about “this/other project” and rolls back valid work. Version 1.7.0 stops both transitions at an explicit identity gate.
