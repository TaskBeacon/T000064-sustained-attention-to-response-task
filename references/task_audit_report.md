# Task Audit Report

Task: `T000064-sustained-attention-to-response-task`

Verdict: no critical or serious findings after repair.

## Findings

- [Moderate, repaired] QA's initial 80 ms simulated RT exceeded its scaled response phases, making every scored go trial an omission. QA now uses 10 ms and exact forced IDs for one go omission and one digit-3 false alarm, covering hit, omission, false alarm, and correct rejection.
- [Low, accepted adaptation] Font sizes are exactly balanced within each digit rather than only randomly assigned, removing size-by-digit imbalance while preserving all source sizes.

## PsyFlow Ownership

| Concern | Owner |
|---|---|
| trial_id | PsyFlow `next_trial_id()` |
| condition schedule | task-local seeded exact planner + BlockUnit |
| randomness | task-local stable seed |
| response capture | StimUnit across digit and mask |
| trigger emission | StimUnit trigger runtime |
| timing/deadline | config + PsyFlow |
| phase data/context | `set_trial_context` + `to_dict` |
| stimulus construction | config + StimBank rebuild for digit size |
| responder integration | standard responder plugin |

## Residual Risk

- The 250 ms exposure requires a calibrated display for precise behavioral deployment.
- Visual mask geometry must be checked in both PsychoPy and browser renderers.
