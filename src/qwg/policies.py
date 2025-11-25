from dataclasses import dataclass
from .risk_context import RiskLevel


@dataclass
class WalletPolicy:
    """
    User / wallet-level configuration for Quantum Wallet Guard.

    These values define how strict the wallet should be under
    different risk conditions. They can later be exposed in the UI
    so power-users can tune them.
    """

    # 1) Balance protection
    # ------------------------------------------------------------------
    # Block sending ~100% of balance in one transaction
    block_full_balance_tx: bool = True

    # Max share of balance per tx under NORMAL / ELEVATED risk
    # Example: 0.5 = 50% of the wallet balance in a single tx
    max_tx_ratio_normal: float = 0.5

    # Under HIGH risk, cap amount even more strictly
    # Example: 0.1 = 10% of the wallet balance in a single tx
    max_tx_ratio_high: float = 0.1

    # 2) Global risk tolerance
    # ------------------------------------------------------------------
    # By default we tolerate up to HIGH.
    # If Sentinel or ADN reports CRITICAL, we block all outgoing tx.
    max_allowed_risk: RiskLevel = RiskLevel.HIGH

    # 3) Cooldowns after WARN / DELAY decisions
    # ------------------------------------------------------------------
    # Short cooldown after a WARN (user sees a warning but may proceed)
    cooldown_seconds_warn: int = 60

    # Longer cooldown when we DELAY a transaction because of risk
    cooldown_seconds_delay: int = 300

    # 4) Behaviour & device thresholds
    # ------------------------------------------------------------------
    # Behaviour score above this value is considered suspicious.
    # (RiskContext.behaviour_score: 1.0 = normal, >1.0 = riskier)
    max_behaviour_score: float = 1.5

    # If True, untrusted devices will trigger a warning decision.
    require_trusted_device: bool = True

    # 5) Extra authentication threshold
    # ------------------------------------------------------------------
    # When tx amount (in coins) exceeds this, we require extra auth
    # such as 2FA / biometric confirmation.
    threshold_extra_auth: float = 10_000.0
