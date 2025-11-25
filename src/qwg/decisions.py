from dataclasses import dataclass
from enum import Enum
from typing import Optional


class Decision(str, Enum):
    """
    Final outcome type produced by the Quantum Wallet Guard engine.
    Each enum value represents a wallet action.
    """
    ALLOW = "allow"
    WARN = "warn"
    DELAY = "delay"
    BLOCK = "block"
    REQUIRE_EXTRA_AUTH = "require_extra_auth"


@dataclass
class DecisionResult:
    """
    Structured response returned by the DecisionEngine.

    Fields:
    - decision: enum describing the outcome
    - reason: human-readable explanation
    - cooldown_seconds: optional delay time for WARN/DELAY
    - suggested_limit: safe maximum amount (if provided)
    - require_confirmation: whether UI should show confirm popup
    - require_second_factor: whether 2FA is required
    """

    decision: Decision
    reason: str

    cooldown_seconds: Optional[int] = None
    suggested_limit: Optional[float] = None

    require_confirmation: bool = False
    require_second_factor: bool = False
