from __future__ import annotations

import hashlib
import random
from statistics import mean, median, stdev
from typing import Any


DIGITS = tuple(range(1, 10))
FONT_POINTS = (48, 72, 94, 100, 120)
FONT_HEIGHTS_DEG = (1.37, 2.06, 2.63, 2.75, 3.32)


class TrialPlan(str):
    def __new__(cls, *, digit: int, font_points: int, font_height_deg: float,
                is_practice: bool, trial_index_in_block: int) -> "TrialPlan":
        condition = "no_go" if int(digit) == 3 else "go"
        obj = str.__new__(cls, condition)
        obj.condition = condition
        obj.digit = int(digit)
        obj.font_points = int(font_points)
        obj.font_height_deg = float(font_height_deg)
        obj.is_practice = bool(is_practice)
        obj.trial_index_in_block = int(trial_index_in_block)
        return obj

    def to_dict(self) -> dict[str, Any]:
        return {
            "condition": self.condition,
            "condition_id": f"{self.condition}_digit_{self.digit}_size_{self.font_points}",
            "digit": self.digit,
            "font_points": self.font_points,
            "font_height_deg": self.font_height_deg,
            "is_practice": self.is_practice,
            "trial_index_in_block": self.trial_index_in_block,
        }


def _stable_seed(base_seed: int, *parts: object) -> int:
    payload = "|".join([str(base_seed), *(str(part) for part in parts)])
    return int.from_bytes(hashlib.blake2b(payload.encode("utf-8"), digest_size=8).digest(), "big")


def generate_trial_plans(*, repetitions_per_digit: int, seed: int, block_idx: int,
                         is_practice: bool) -> list[TrialPlan]:
    repetitions = int(repetitions_per_digit)
    if repetitions <= 0:
        raise ValueError("repetitions_per_digit must be positive")
    records: list[dict[str, Any]] = []
    for digit in DIGITS:
        for index in range(repetitions):
            size_index = (index + digit - 1) % len(FONT_POINTS)
            records.append({
                "digit": digit,
                "font_points": FONT_POINTS[size_index],
                "font_height_deg": FONT_HEIGHTS_DEG[size_index],
            })
    rng = random.Random(_stable_seed(seed, "sart", block_idx, "practice" if is_practice else "scored"))
    rng.shuffle(records)
    return [TrialPlan(**record, is_practice=is_practice, trial_index_in_block=index)
            for index, record in enumerate(records)]


def summarize_trials(rows: list[dict[str, Any]]) -> dict[str, Any]:
    scored = [row for row in rows if not bool(row.get("is_practice"))]
    go_rows = [row for row in scored if row.get("condition") == "go"]
    no_go_rows = [row for row in scored if row.get("condition") == "no_go"]
    correct_rts = [float(row["response_rt"]) for row in go_rows
                   if bool(row.get("correct")) and isinstance(row.get("response_rt"), (int, float))]
    return {
        "trials": len(scored),
        "go_hit_rate": sum(bool(row.get("correct")) for row in go_rows) / len(go_rows) if go_rows else 0.0,
        "commission_error_rate": sum(bool(row.get("false_alarm")) for row in no_go_rows) / len(no_go_rows) if no_go_rows else 0.0,
        "omission_error_rate": sum(bool(row.get("omission")) for row in go_rows) / len(go_rows) if go_rows else 0.0,
        "mean_go_rt": mean(correct_rts) if correct_rts else None,
        "median_go_rt": median(correct_rts) if correct_rts else None,
        "go_rt_sd": stdev(correct_rts) if len(correct_rts) > 1 else None,
    }
