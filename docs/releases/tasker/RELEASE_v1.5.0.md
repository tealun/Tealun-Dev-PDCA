# Tasker v1.5.0 — Verifiable Outcome Execution

Tasker now distinguishes executing an action from proving the user's intended outcome.

## Added

- Evidence Ledger: `Action → Artifact → Observation → Requirement → Verdict`
- Outcome Path for cross-component M/L tasks
- Completion verdicts: `Confirmed`, `Likely`, `Partially verified`, `Not verified`, `Blocked`
- M/L confidence levels: `High`, `Medium`, `Low`
- Preserved-invariant checks for bounded and high-risk changes
- Evidence acceptance and rejection rules
- Symmetric pre-execution and pre-close acceptance checks

## Preserved

- The seven-stage Tasker state machine
- S/M/L sizing and confirmation policy
- Zero-Tool Zero-Progress, PTV, and Tool-Call Audit
- Lightweight handling for S-level tasks

## Behavioral Change

A tool call or changed artifact proves that execution occurred, not that the requested outcome is correct. `verify` must connect observations to each acceptance requirement, and `close` must report an evidence-calibrated verdict.
