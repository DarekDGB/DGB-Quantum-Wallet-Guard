from dataclasses import dataclass
from .risk_context import RiskLevel


@dataclass
class WalletPolicy:
    """
    User / wallet-level configuration for Quantum Wallet Guard.

    These are *reference defaults* for DigiByte wallets.
    Wallets and users can override them in their own UI.
    """

    # 1) Hard risk ceiling
    # Only when risk goes ABOVE this level we DELAY.
    # So with CRITICAL we allow NORMAL/ELEVATED/HIGH to be handled
    # by the ratio / behaviour rules instead of auto-delay.
    max_allowed_risk: RiskLevel = RiskLevel.CRITICAL

    # 2) Full-balance protection
    # Block sending (almost) 100% of the wallet in one tx.
    block_full_balance_tx: bool = True

    # 3) Ratio limits
    # Under NORMAL / ELEVATED risk, max share of balance per tx (e.g. 0.25 = 25%)
    max_tx_ratio_normal: float = 0.25

    # Under HIGH risk, cap amount even more (e.g. 0.10 = 10%)
    max_tx_ratio_high: float = 0.10

    # 4) Cooldowns after WARN / DELAY decisions
    cooldown_seconds_warn: int = 60
    cooldown_seconds_delay: int = 300

    # 5) Extra authentication threshold
    # When absolute amount (in DGB) exceeds this, require extra auth
    # even if ratios look safe.
    threshold_extra_auth: float = 10_000.0

    # 6) Optional future daily limit (not yet enforced in engine)
    daily_limit_amount: float = 50_000.0
