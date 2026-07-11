from __future__ import annotations

from functools import partial
from typing import Any

from psyflow import StimUnit, next_trial_id, set_trial_context

from .utils import TrialPlan


def _context(*, trial_id: int, block_id: str, condition_id: str, phase: str,
             deadline_s: float, valid_keys: list[str], task_factors: dict[str, Any],
             stim_id: str) -> dict[str, Any]:
    return {"trial_id": trial_id, "phase": phase, "deadline_s": deadline_s,
            "valid_keys": valid_keys, "block_id": block_id, "condition_id": condition_id,
            "task_factors": task_factors, "stim_id": stim_id}


def _mask(stim_bank) -> list[Any]:
    return [stim_bank.get("mask_ring"), stim_bank.get("mask_bar_forward"), stim_bank.get("mask_bar_backward")]


def run_trial(win, kb, settings, condition, stim_bank, trigger_runtime, block_id=None, block_idx=None):
    if not isinstance(condition, TrialPlan):
        raise TypeError("SART trials require a preplanned TrialPlan")
    plan = condition.to_dict()
    trial_id = next_trial_id()
    block_id_value = str(block_id or "block_0")
    response_key = str(settings.response_key)
    keys = [response_key]
    factors = {**plan, "correct_key": response_key if plan["condition"] == "go" else None}
    trial_data: dict[str, Any] = {"trial_id": trial_id, "block_id": block_id_value,
                                  "block_idx": int(block_idx or 0), **plan}
    make_unit = partial(StimUnit, win=win, kb=kb, runtime=trigger_runtime)

    digit_duration = float(settings.digit_duration)
    digit_stim = stim_bank.rebuild("digit", text=str(plan["digit"]), height=float(plan["font_height_deg"]))
    digit = make_unit(unit_label="digit").add_stim(digit_stim)
    set_trial_context(digit, **_context(
        trial_id=trial_id, block_id=block_id_value, condition_id=plan["condition_id"],
        phase="digit", deadline_s=digit_duration, valid_keys=keys,
        task_factors={**factors, "stage": "digit"}, stim_id=f"digit_{plan['digit']}",
    ))
    digit.capture_response(
        keys=keys,
        correct_keys=keys if plan["condition"] == "go" else [],
        duration=digit_duration,
        onset_trigger=settings.triggers.get(f"digit_{plan['condition']}"),
        response_trigger={response_key: settings.triggers.get("go_response" if plan["condition"] == "go" else "commission_error")},
        terminate_on_response=False,
    ).to_dict(trial_data)
    digit_response = digit.get_state("response", None)
    digit_rt = digit.get_state("rt", None)

    mask_duration = float(settings.mask_duration)
    mask_response = None
    mask_rt = None
    if digit_response is None:
        mask = make_unit(unit_label="mask_response").add_stim(*_mask(stim_bank))
        set_trial_context(mask, **_context(
            trial_id=trial_id, block_id=block_id_value, condition_id=plan["condition_id"],
            phase="mask_response", deadline_s=mask_duration, valid_keys=keys,
            task_factors={**factors, "stage": "mask_response"}, stim_id="encircled_x_mask",
        ))
        mask.capture_response(
            keys=keys,
            correct_keys=keys if plan["condition"] == "go" else [],
            duration=mask_duration,
            onset_trigger=settings.triggers.get("mask"),
            response_trigger={response_key: settings.triggers.get("go_response" if plan["condition"] == "go" else "commission_error")},
            timeout_trigger=settings.triggers.get("omission_error") if plan["condition"] == "go" else None,
            terminate_on_response=False,
        ).to_dict(trial_data)
        mask_response = mask.get_state("response", None)
        mask_rt = mask.get_state("rt", None)
    else:
        mask_hold = make_unit(unit_label="mask_hold").add_stim(*_mask(stim_bank))
        set_trial_context(mask_hold, **_context(
            trial_id=trial_id, block_id=block_id_value, condition_id=plan["condition_id"],
            phase="mask_hold", deadline_s=mask_duration, valid_keys=[],
            task_factors={**factors, "stage": "mask_hold"}, stim_id="encircled_x_mask",
        ))
        mask_hold.show(duration=mask_duration, onset_trigger=settings.triggers.get("mask")).to_dict(trial_data)

    response = digit_response if digit_response is not None else mask_response
    response_rt = float(digit_rt) if isinstance(digit_rt, (int, float)) else (
        digit_duration + float(mask_rt) if isinstance(mask_rt, (int, float)) else None)
    false_alarm = plan["condition"] == "no_go" and response is not None
    omission = plan["condition"] == "go" and response is None
    correct = not false_alarm and not omission
    outcome = "hit" if plan["condition"] == "go" and correct else (
        "omission" if omission else ("false_alarm" if false_alarm else "correct_rejection"))
    trial_data.update({"response_key": str(response) if response is not None else "",
                       "response_rt": response_rt, "false_alarm": false_alarm,
                       "omission": omission, "correct": correct, "outcome": outcome})
    return trial_data
