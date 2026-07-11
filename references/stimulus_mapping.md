# Stimulus Mapping

## Mapping Table

| Condition | Stage/Phase | Stimulus IDs | Participant-Facing Content | Source Paper ID | Evidence (quote/figure/table) | Implementation Mode | Asset References | Notes |
|---|---|---|---|---|---|---|---|---|
| `go` | digit | `digit_1`, `digit_2`, `digit_4-9` | White digit; press Space. | `ROBERTSON1997` | Respond to each digit except 3. | generated_text | `src/utils.py`, `config/*.yaml` | Five source sizes. |
| `no_go` | digit | `digit_3` | White 3; withhold. | `ROBERTSON1997` | Rare one-in-nine target. | generated_text | `src/utils.py`, `config/*.yaml` | 25 scored trials. |
| all | mask/response | `mask_ring`, `mask_bar_forward`, `mask_bar_backward` | White 29 mm ring with diagonal X. | `ROBERTSON1997` | 900 ms encircled-X mask. | psychopy_builtin | `config/*.yaml` | Response continues through mask. |
