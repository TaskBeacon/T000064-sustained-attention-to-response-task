# Parameter Mapping

## Mapping Table

| Parameter ID | Config Path | Implemented Value | Source Paper ID | Evidence (quote/figure/table) | Decision Type | Notes |
|---|---|---:|---|---|---|---|
| `digit_set` | planner | 1-9 | `ROBERTSON1997` | Digits 1-9; withhold to rare target 3 | direct | 3 is one ninth. |
| `scored_trials` | `task.total_trials` | 225 | `ROBERTSON1997` | 25 presentations of each digit | direct | One continuous block. |
| `practice_trials` | `task.practice_repetitions_per_digit` | 18 | `ROBERTSON1997` replication protocol | 18 trials including two 3s | direct | Each digit twice. |
| `digit_duration` | `timing.digit_duration` | 0.25 s | `ROBERTSON1997` | Digit shown 250 ms | direct | Response remains open. |
| `mask_duration` | `timing.mask_duration` | 0.90 s | `ROBERTSON1997` | Mask shown 900 ms | direct | Fixed 1150 ms onset interval. |
| `font_sizes` | `task.font_points` | 48,72,94,100,120 | `ROBERTSON1997` | Five randomly assigned Symbol sizes | direct | Mapped to 12-29 mm heights. |
| `mask_size` | mask primitives | 29 mm / 3.32 deg | `ROBERTSON1997` | 29 mm diameter encircled diagonal cross | direct conversion | At 50 cm. |
| `size_balance` | planner | each digit x each size five times | local adaptation | Source assigned sizes randomly | adapted | Removes size-digit imbalance. |
