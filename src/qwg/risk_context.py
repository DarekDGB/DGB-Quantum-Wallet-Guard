from dataclasses import dataclass
from enum import Enum
from typing import Optional
from datetime import datetime


class RiskLevel(str, Enum):
    NORMAL = "normal"
    ELEVATED = "elevated"
    HIGH = "high"
    CRITICAL = "critical"

    def severity(self) -> int:
        order = {
            "normal": 0,
            "elevated": 1,
            "high": 2,
            "critical": 3,
        }
        return order[self.value]
