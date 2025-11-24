from dataclasses import dataclass
from .risk_context import RiskLevel


@dataclass
class WalletPolicy:
    """
    User / wallet-level configuration for Quantum Wallet Guard.
    These values can later be personalised in the UI.
    """

    # Block sending 100% of balance in one tx
    block_full_balance_tx: bool = True

    # Max share of balance per tx under normal risk (e.g. 0.5 = 50%)
    max_tx_ratio_normal: float = 0.5

    # Under HIGH risk, cap amount even more (e.g. 0.1 = 10%)
    max_tx_ratio_high: float = 0.1

    # Under CRITICAL risk, we block all outgoing tx
    max_allowed_risk: RiskLevel = RiskLevel.HIGH

    # Cooldown after WARN/DELAY decisions
    cooldown_seconds_warn: int = 60
    cooldown_seconds_delay: int = 300

    # When amount (in coins) exceeds this, require extra auth
    threshold_extra_auth: float = 10_000.0
