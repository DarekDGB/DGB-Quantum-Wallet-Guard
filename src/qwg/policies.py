from dataclasses import dataclass
from .risk_context import RiskLevel


@dataclass
class WalletPolicy:
    """
    Wallet-level safety policy for DGB Quantum Wallet Guard (Layer 5).

    These values are **sane defaults** for most DigiByte users.
    Wallets, exchanges and custodians can override them to be stricter
    or looser depending on their own risk appetite.

    Fields map directly to the logic in DecisionEngine:
      - max_allowed_risk       → how much chain / node risk we tolerate
      - max_tx_ratio_normal    → max % of balance per tx at normal risk
      - max_tx_ratio_high      → max % of balance per tx at high risk
      - cooldown_seconds_delay → how long to delay when risk > policy
      - cooldown_seconds_warn  → cooldown for warnings / soft limits
      - threshold_extra_auth   → amount that triggers extra auth
      - block_full_balance_tx  → hard block on ~100% balance wipes
    """

    # 0) How much chain / node risk do we tolerate?
    # NORMAL < ELEVATED < HIGH < CRITICAL
    # We choose ELEVATED (stricter than HIGH) for strong protection.
    max_allowed_risk: RiskLevel = RiskLevel.ELEVATED

    # 1) Per-transaction balance ratio limits
    # Example with balance = 1000 DGB:
    #   - normal: max 250 DGB
    #   - high:   max 100 DGB
    max_tx_ratio_normal: float = 0.25  # 25% of balance under normal risk
    max_tx_ratio_high: float = 0.10    # 10% of balance when risk is HIGH+

    # 2) Cooldowns (in seconds)
    cooldown_seconds_warn: int = 60    # 1 minute cooldown after WARN
    cooldown_seconds_delay: int = 300  # 5 minutes delay when risk > policy

    # 3) Extra authentication threshold (absolute amount in DGB)
    # Any tx >= this value will require extra auth (2FA / extra confirmation).
    threshold_extra_auth: float = 10_000.0

    # 4) Hard block on sending ~100% of wallet balance in one tx
    block_full_balance_tx: bool = True
