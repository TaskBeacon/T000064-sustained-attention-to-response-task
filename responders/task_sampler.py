from __future__ import annotations

import random as _random
from dataclasses import dataclass, field
from typing import Any

from psyflow.sim.contracts import Action, Feedback, Observation, SessionInfo


@dataclass
class TaskSamplerResponder:
    continue_key: str = "space"
    go_hit_rate: float = 0.97
    no_go_withhold_rate: float = 0.85
    rt_mean_s: float = 0.42
    rt_sd_s: float = 0.08
    forced_omission_trials: list[int] = field(default_factory=list)
    forced_false_alarm_trials: list[int] = field(default_factory=list)

    def __post_init__(self) -> None: self._rng: Any = None
    def start_session(self, session: SessionInfo, rng: Any) -> None: self._rng = rng
    def on_feedback(self, fb: Feedback) -> None: return None
    def end_session(self) -> None: self._rng = None
    def _draw(self) -> float: return float(self._rng.random()) if hasattr(self._rng, "random") else _random.random()
    def _rt(self) -> float:
        if hasattr(self._rng, "normal"): return max(0.005, float(self._rng.normal(self.rt_mean_s, self.rt_sd_s)))
        if hasattr(self._rng, "gauss"): return max(0.005, float(self._rng.gauss(self.rt_mean_s, self.rt_sd_s)))
        return self.rt_mean_s

    def act(self, obs: Observation) -> Action:
        keys = [str(key) for key in list(obs.valid_keys or [])]
        if not keys: return Action(key=None, rt_s=None)
        factors = dict(getattr(obs, "task_factors", {}) or {})
        stage = str(factors.get("stage", getattr(obs, "phase", "")))
        if any(token in stage for token in ("instruction", "summary", "good_bye", "practice_intro")):
            return Action(key=self.continue_key if self.continue_key in keys else keys[0], rt_s=0.2)
        if stage not in {"digit", "mask_response"}: return Action(key=None, rt_s=None)
        trial_id = int(getattr(obs, "trial_id", -1)) if str(getattr(obs, "trial_id", "")).isdigit() else -1
        condition = str(factors.get("condition", "go"))
        if condition == "go":
            respond = trial_id not in set(self.forced_omission_trials) and self._draw() <= self.go_hit_rate
        else:
            respond = trial_id in set(self.forced_false_alarm_trials) or self._draw() > self.no_go_withhold_rate
        return Action(key=keys[0], rt_s=self._rt()) if respond else Action(key=None, rt_s=None)
