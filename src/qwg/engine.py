from .risk_context import RiskContext, RiskLevel
from .policies import WalletPolicy
from .decisions import Decision, DecisionResult


class DecisionEngine:
    """
    Core brain of DGB Quantum Wallet Guard (Layer 5).

    v2.0: still simple and transparent, but structured around:
      - clear severity comparisons
      - unified view of chain + node + wallet + device
      - ready for future AI / ML on top (without breaking this API)

    The behaviour remains backwards compatible with the earlier version,
    so existing tests and integrations should continue to pass.
    """

    def __init__(self, policy: WalletPolicy | None = None) -> None:
        self.policy = policy or WalletPolicy()

    # ------------------------------------------------------------------ #
    # Public API
    # ------------------------------------------------------------------ #

    def evaluate_transaction(self, ctx: RiskContext) -> DecisionResult:
        """
        Evaluate a single transaction using the combined risk context.

        The engine uses a layered approach:

        1. Absolute hard-stops (critical risk).
        2. Policy mismatch (risk higher than wallet’s tolerance).
        3. Balance / ratio rules.
        4. Large-amount extra authentication.
        5. Behaviour/device anomalies.
        6. Default allow.
        """
        p = self.policy

        # Helper variables so we don't recompute severities everywhere.
        sentinel_sev = ctx.sentinel_level.severity()
        adn_sev = ctx.adn_level.severity()
        max_chain_sev = max(sentinel_sev, adn_sev)

        # ------------------------------------------------------------------
        # 1) Hard stop on CRITICAL risk from Sentinel or ADN
        # ------------------------------------------------------------------
        if ctx.sentinel_level == RiskLevel.CRITICAL or ctx.adn_level == RiskLevel.CRITICAL:
            return DecisionResult(
                decision=Decision.BLOCK,
                reason="Critical chain or node risk reported by Sentinel/ADN.",
            )

        # If DQSN says the entire network is in extreme danger,
        # we treat it like a hard warning layer. For now we delay
        # instead of blocking, to remain conservative.
        if ctx.is_network_extremely_risky():
            return DecisionResult(
                decision=Decision.DELAY,
                reason="DQSN reports extreme network-wide risk; transaction delayed.",
                cooldown_seconds=p.cooldown_seconds_delay,
            )

        # ------------------------------------------------------------------
        # 2) If risk is above wallet policy, delay tx
        # ------------------------------------------------------------------
        if max_chain_sev > p.max_allowed_risk.severity():
            return DecisionResult(
                decision=Decision.DELAY,
                reason="Risk level exceeds wallet policy; transaction delayed.",
                cooldown_seconds=p.cooldown_seconds_delay,
            )

        # ------------------------------------------------------------------
        # 3) Balance-based rules (full wipe + ratios)
        # ------------------------------------------------------------------
        if p.block_full_balance_tx and ctx.wallet_balance > 0:
            ratio = ctx.tx_amount / ctx.wallet_balance
            if ratio >= 0.99:
                return DecisionResult(
                    decision=Decision.BLOCK,
                    reason="Attempt to send ~100% of wallet balance.",
                )

        if ctx.wallet_balance > 0:
            ratio = ctx.tx_amount / ctx.wallet_balance

            # High risk → use stricter ratio
            if max_chain_sev >= RiskLevel.HIGH.severity():
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

        # ------------------------------------------------------------------
        # 4) Extra auth for large absolute amounts
        # ------------------------------------------------------------------
        if ctx.tx_amount >= p.threshold_extra_auth:
            return DecisionResult(
                decision=Decision.REQUIRE_EXTRA_AUTH,
                reason="Amount exceeds extra-auth threshold.",
                require_confirmation=True,
                require_second_factor=True,
            )

        # ------------------------------------------------------------------
        # 5) Behaviour / device checks (kept simple for v2.0)
        # ------------------------------------------------------------------
        if ctx.behaviour_score > 1.5 or not ctx.trusted_device:
            return DecisionResult(
                decision=Decision.WARN,
                reason="Unusual behaviour or untrusted device detected.",
                cooldown_seconds=p.cooldown_seconds_warn,
            )

        # ------------------------------------------------------------------
        # 6) Default: allow
        # ------------------------------------------------------------------
        return DecisionResult(
            decision=Decision.ALLOW,
            reason="No policy or risk rule violated.",
        )
