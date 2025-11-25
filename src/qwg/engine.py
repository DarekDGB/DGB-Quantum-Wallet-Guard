from .risk_context import RiskContext, RiskLevel
from .policies import WalletPolicy
from .decisions import Decision, DecisionResult


class DecisionEngine:
    """
    Core brain of DGB Quantum Wallet Guard (Layer 5).

    v0.2: simple, transparent rules + policy-aware ordering.
    Later we can plug AI / ML on top of this.
    """

    def __init__(self, policy: WalletPolicy | None = None) -> None:
        self.policy = policy or WalletPolicy()

    def evaluate_transaction(self, ctx: RiskContext) -> DecisionResult:
        p = self.policy

        # 1) Hard stop on CRITICAL risk from Sentinel or ADN
        if ctx.sentinel_level == RiskLevel.CRITICAL or ctx.adn_level == RiskLevel.CRITICAL:
            return DecisionResult(
                decision=Decision.BLOCK,
                reason="Critical chain or node risk reported by Sentinel/ADN.",
            )

        # 2) If risk is above wallet policy, delay tx
        if (
            ctx.sentinel_level.severity() > p.max_allowed_risk.severity()
            or ctx.adn_level.severity() > p.max_allowed_risk.severity()
        ):
            return DecisionResult(
                decision=Decision.DELAY,
                reason="Risk level exceeds wallet policy; transaction delayed.",
                cooldown_seconds=p.cooldown_seconds_delay,
            )

        # 3) Block full balance wipes if enabled
        if p.block_full_balance_tx and ctx.wallet_balance > 0:
            ratio = ctx.tx_amount / ctx.wallet_balance
            if ratio >= 0.99:
                return DecisionResult(
                    decision=Decision.BLOCK,
                    reason="Attempt to send ~100% of wallet balance.",
                )

        # 4) Extra auth for large absolute amounts
        #    (this should trigger BEFORE ratio-based warnings)
        if ctx.tx_amount >= p.threshold_extra_auth:
            return DecisionResult(
                decision=Decision.REQUIRE_EXTRA_AUTH,
                reason="Amount exceeds extra-auth threshold.",
                require_confirmation=True,
                require_second_factor=True,
            )

        # 5) Limit ratio based on risk level
        if ctx.wallet_balance > 0:
            ratio = ctx.tx_amount / ctx.wallet_balance

            if ctx.sentinel_level == RiskLevel.HIGH or ctx.adn_level == RiskLevel.HIGH:
                # High risk → use stricter ratio
                if ratio > p.max_tx_ratio_high:
                    return DecisionResult(
                        decision=Decision.WARN,
                        reason="Large transaction during high risk period.",
                        cooldown_seconds=p.cooldown_seconds_warn,
                        suggested_limit=p.max_tx_ratio_high * ctx.wallet_balance,
                    )
            else:
                # Normal or elevated risk
                if ratio > p.max_tx_ratio_normal:
                    return DecisionResult(
                        decision=Decision.WARN,
                        reason="Transaction exceeds normal per-tx ratio.",
                        cooldown_seconds=p.cooldown_seconds_warn,
                        suggested_limit=p.max_tx_ratio_normal * ctx.wallet_balance,
                    )

        # 6) Behaviour / device checks (very simple for v0.2)
        if ctx.behaviour_score > 1.5 or not ctx.trusted_device:
            return DecisionResult(
                decision=Decision.WARN,
                reason="Unusual behaviour or untrusted device detected.",
                cooldown_seconds=p.cooldown_seconds_warn,
            )

        # 7) Default: allow
        return DecisionResult(
            decision=Decision.ALLOW,
            reason="No policy or risk rule violated.",
        )
