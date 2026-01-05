from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from datetime import datetime


class RiskLevel(str, Enum):
    """
    Discrete risk classification used across the Quantum Wallet Guard.

    Ordering (by severity):
        NORMAL < ELEVATED < HIGH < CRITICAL
    """
    NORMAL = "normal"
    ELEVATED = "elevated"
    HIGH = "high"
    CRITICAL = "critical"

    def severity(self) -> int:
        """
        Numeric ordering for comparisons.
        Useful for simple integer math instead of long if/else chains.
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

    This is what Sentinel AI v2, DQSN, ADN v2 and the wallet
    feed into the Quantum Wallet Guard engine.

    Layer 5 looks at this *combined* view to decide:
    - allow
    - warn / delay
    - require extra auth
    - block
    """

    # Signals from Sentinel AI v2 / chain
    sentinel_level: RiskLevel = RiskLevel.NORMAL

    # Signals from DQSN (network-wide score 0.0–1.0)
    dqs_network_score: float = 0.0

    # Signals from ADN v2 (node-local)
    adn_level: RiskLevel = RiskLevel.NORMAL

    # Wallet & transaction basics
    wallet_balance: float = 0.0
    tx_amount: float = 0.0
    address_age_days: Optional[int] = None  # how long we know this address

    # Behaviour / device
    behaviour_score: float = 1.0  # 1.0 = normal, >1.0 = risky
    device_id: Optional[str] = None
    trusted_device: bool = True

    # Metadata
    created_at: datetime = field(default_factory=datetime.utcnow)

    # ------------------------------------------------------------------ #
    # Helper methods (used by the engine, but also handy for tests)
    # ------------------------------------------------------------------ #

    def max_chain_risk(self) -> RiskLevel:
        """
        Return the worst (highest) risk level between Sentinel and ADN.
        """
        if self.sentinel_level.severity() >= self.adn_level.severity():
            return self.sentinel_level
        return self.adn_level

    def is_network_extremely_risky(self) -> bool:
        """
        Simple helper: treat very high DQSN scores as 'extreme' conditions.

        NOTE:
        - threshold is intentionally hard-coded for now to keep the
          policy object simple. We can move this into WalletPolicy later
          without breaking callers.
        """
        return self.dqs_network_score >= 0.9
