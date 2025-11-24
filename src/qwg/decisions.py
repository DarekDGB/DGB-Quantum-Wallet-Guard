from dataclasses import dataclass
from enum import Enum
from typing import Optional


class Decision(str, Enum):
    ALLOW = "allow"
    WARN = "warn"
    DELAY = "delay"
    BLOCK = "block"
    REQUIRE_EXTRA_AUTH = "require_extra_auth"


@dataclass
class DecisionResult:
    decision: Decision
    reason: str
    cooldown_seconds: int = 0
    require_confirmation: bool = False
    require_second_factor: bool = False
    suggested_limit: Optional[float] = None
