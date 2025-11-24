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
        """
        Numeric ordering for comparisons:
        NORMAL < ELEVATED < HIGH < CRITICAL
        """
        order = {
            "normal": 0,
            "elevated": 1,
            "high": 2,
            "critical": 3,
        }
        return order[self.value]


@dataclass
class RiskContext:
    """
    Snapshot of all security signals for a single transaction.
    This is what Sentinel AI, DQSN, ADN v2 and the wallet feed
    into the Quantum Wallet Guard engine.
    """

    # Signals from Sentinel AI v2 / chain
    sentinel_level: RiskLevel = RiskLevel.NORMAL

    # Signals from DQSN (network-wide)
    dqs_network_score: float = 0.0  # 0.0–1.0

    # Signals from ADN v2 (node-local)
    adn_level: RiskLevel = RiskLevel.NORMAL

    # Wallet & transaction basics
    wallet_balance: float = 0.0
    tx_amount: float = 0.0
    address_age_days: Optional[int] = None

    # Behaviour / device
    behaviour_score: float = 1.0  # 1.0 = normal, >1 = risky
    device_id: Optional[str] = None
    trusted_device: bool = True

    # Metadata
    created_at: datetime = datetime.utcnow()
