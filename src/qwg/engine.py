from __future__ import annotations

from .risk_context import RiskContext, RiskLevel
from .policies import WalletPolicy
from .decisions import Decision, DecisionResult
from .adaptive_bridge import emit_adaptive_event


class DecisionEngine:
    """
    Core brain of DGB Quantum Wallet Guard (Layer 5).

    v0.3:
      - simple, transparent rules + policy-aware ordering
      - emits AdaptiveEvent records to the Adaptive Core
        whenever a risky wallet action is blocked / delayed / warned.
    """

    def __init__(self, policy: WalletPolicy | None = None) -> None:
        self.policy = policy or WalletPolicy()

    # ------------------------------------------------------------------ #
    # Internal helper – send event to Adaptive Core (if configured)
    # ------------------------------------------------------------------ #

    def _emit_adaptive(
        self,
        ctx: RiskContext,
        decision: Decision,
        reason: str,
        severity: float,
    ) -> None:
        """
        Send a lightweight AdaptiveEvent into the Adaptive Core.

        This is best-effort:
        - if ctx has no adaptive_sink, nothing happens
        - we never raise inside this helper
        """
        adaptive_sink = getattr(ctx, "adaptive_sink", None)
        if adaptive_sink is None:
            return

        try:
            tx_id = getattr(ctx, "tx_id", "unknown-tx")
            fingerprint = getattr(ctx, "wallet_fingerprint", "unknown-wallet")
            user_id = getattr(ctx, "user_id", None)

            emit_adaptive_event(
                adaptive_sink=adaptive_sink,
                event_id=tx_id,
                action=decision.name.lower(),  # "block", "delay", "warn", ...
                severity=severity,
                fingerprint=fingerprint,
                user_id=user_id,
                extra={
                    "reason": reason,
                    "sentinel_level": getattr(
                        ctx.sentinel_level, "name", str(ctx.sentinel_level)
                    ),
                    "adn_level": getattr(
                        ctx.adn_level, "name", str(ctx.adn_level)
                    ),
                    "tx_amount": ctx.tx_amount,
                    "wallet_balance": ctx.wallet_balance,
                    "behaviour_score": getattr(ctx, "behaviour_score", None),
                    "trusted_device": getattr(ctx, "trusted_device", None),
                },
            )
        except Exception:
            # Adaptive path must never break wallet decisions.
            return

    # ------------------------------------------------------------------ #
    # Public API
    # ------------------------------------------------------------------ #

    def evaluate_transaction(self, ctx: RiskContext) -> DecisionResult:
        p = self.policy

        # 1) Hard stop on CRITICAL risk from Sentinel or ADN
        if ctx.sentinel_level == RiskLevel.CRITICAL or ctx.adn_level == RiskLevel.CRITICAL:
            reason = "Critical chain or node risk reported by Sentinel/ADN."
            result = DecisionResult(
                decision=Decision.BLOCK,
                reason=reason,
            )
            self._emit_adaptive(ctx, Decision.BLOCK, reason, severity=0.95)
            return result

        # 2) If risk is above wallet policy, delay tx
        if (
            ctx.sentinel_level.severity() > p.max_allowed_risk.severity()
            or ctx.adn_level.severity() > p.max_allowed_risk.severity()
        ):
            reason = "Risk level exceeds wallet policy; transaction delayed."
            result = DecisionResult(
                decision=Decision.DELAY,
                reason=reason,
                cooldown_seconds=p.cooldown_seconds_delay,
            )
            self._emit_adaptive(ctx, Decision.DELAY, reason, severity=0.75)
            return result

        # 3) Block full balance wipes if enabled
        if p.block_full_balance_tx and ctx.wallet_balance > 0:
            ratio = ctx.tx_amount / ctx.wallet_balance
            if ratio >= 0.99:
                reason = "Attempt to send ~100% of wallet balance."
                result = DecisionResult(
                    decision=Decision.BLOCK,
                    reason=reason,
                )
                self._emit_adaptive(ctx, Decision.BLOCK, reason, severity=0.9)
                return result

        # 4) Extra auth for large absolute amounts
        #    (this should trigger BEFORE ratio-based warnings)
        if ctx.tx_amount >= p.threshold_extra_auth:
            reason = "Amount exceeds extra-auth threshold."
            result = DecisionResult(
                decision=Decision.REQUIRE_EXTRA_AUTH,
                reason=reason,
                require_confirmation=True,
                require_second_factor=True,
            )
            self._emit_adaptive(ctx, Decision.REQUIRE_EXTRA_AUTH, reason, severity=0.7)
            return result

        # 5) Limit ratio based on risk level
        if ctx.wallet_balance > 0:
            ratio = ctx.tx_amount / ctx.wallet_balance

            if ctx.sentinel_level == RiskLevel.HIGH or ctx.adn_level == RiskLevel.HIGH:
                # High risk → use stricter ratio
                if ratio > p.max_tx_ratio_high:
                    reason = "Large transaction during high risk period."
                    result = DecisionResult(
                        decision=Decision.WARN,
                        reason=reason,
                        cooldown_seconds=p.cooldown_seconds_warn,
                        suggested_limit=p.max_tx_ratio_high * ctx.wallet_balance,
                    )
                    self._emit_adaptive(ctx, Decision.WARN, reason, severity=0.65)
                    return result
            else:
                # Normal or elevated risk
                if ratio > p.max_tx_ratio_normal:
                    reason = "Transaction exceeds normal per-tx ratio."
                    result = DecisionResult(
                        decision=Decision.WARN,
                        reason=reason,
                        cooldown_seconds=p.cooldown_seconds_warn,
                        suggested_limit=p.max_tx_ratio_normal * ctx.wallet_balance,
                    )
                    self._emit_adaptive(ctx, Decision.WARN, reason, severity=0.55)
                    return result

        # 6) Behaviour / device checks (very simple for v0.2)
        if ctx.behaviour_score > 1.5 or not ctx.trusted_device:
            reason = "Unusual behaviour or untrusted device detected."
            result = DecisionResult(
                decision=Decision.WARN,
                reason=reason,
                cooldown_seconds=p.cooldown_seconds_warn,
            )
            self._emit_adaptive(ctx, Decision.WARN, reason, severity=0.6)
            return result

        # 7) Default: allow  (no adaptive event – considered "healthy" traffic)
        return DecisionResult(
            decision=Decision.ALLOW,
            reason="No policy or risk rule violated.",
        )
