from dataclasses import dataclass
from enum import Enum
from typing import Optional


class Decision(str, Enum):
    """
    High-level decision taken by the Quantum Wallet Guard.

    The string values are **public API** – they appear in logs,
    telemetry and can be used by UIs. Do NOT change lightly.
    """

    ALLOW = "allow"
    WARN = "warn"
    DELAY = "delay"
    BLOCK = "block"
    REQUIRE_EXTRA_AUTH = "require_extra_auth"


@dataclass
class DecisionResult:
    """
    Result returned by the DecisionEngine.

    Fields:
      - decision            – one of the Decision enum values
      - reason              – human/machine readable explanation
      - cooldown_seconds    – optional delay before user can retry
      - suggested_limit     – optional safer amount the wallet may propose
      - require_confirmation – show extra confirmation dialog
      - require_second_factor – require 2FA / extra auth step
    """

    decision: Decision
    reason: str
    cooldown_seconds: Optional[int] = None
    suggested_limit: Optional[float] = None
    require_confirmation: bool = False
    require_second_factor: bool = False
