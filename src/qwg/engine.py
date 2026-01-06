from __future__ import annotations

from .risk_context import RiskContext, RiskLevel
from .policies import WalletPolicy
from .decisions import Decision, DecisionResult
from .adaptive_bridge import emit_adaptive_event

from qwg.adapters import to_v3_verdict
from qwg.v3.context_hash import compute_context_hash


class DecisionEngine:
    """
    Core brain of DGB Quantum Wallet Guard (Layer 5).

    v0.4:
      - simple, transparent rules + policy-aware ordering
      - emits AdaptiveEvent records to the Adaptive Core
        whenever a risky wallet action is blocked / delayed / warned.
      - v2: enriches events with threat_type + description so
        Adaptive Core v2 can store them as ThreatPackets and use
        them inside the immune reports.

    v3 (wrapper only):
      - adds a side-effect-free wrapper that returns a v3 glass-box verdict
      - does NOT change decision logic or policy behavior
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

            # threat_type label used by Adaptive Core v2 (via adaptive_bridge)
            threat_type = f"wallet_{decision.name.lower()}"

            emit_adaptive_event(
                adaptive_sink=adaptive_sink,
                event_id=tx_id,
                action=decision.name.lower(),  # "block", "delay", "warn", ...
                severity=severity,
                fingerprint=fingerprint,
                user_id=user_id,
                extra={
                    # High-level semantics for Adaptive Core v2
                    "threat_type": threat_type,
                    "description": reason,
                    "tx_id": tx_id,
                    "wallet_id": fingerprint,
                    # Risk context for deeper analysis
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
    # v3 helpers (pure, deterministic)
    # ------------------------------------------------------------------ #

    def _build_v3_context(self, ctx: RiskContext) -> dict:
        """
        Build a deterministic, JSON-serializable context dict for v3 hashing.

        IMPORTANT:
        - no timestamps
        - no randomness
        - no network lookups
        - stable keys only
        """
        return {
            "sentinel_level": getattr(ctx.sentinel_level, "value", str(ctx.sentinel_level)),
            "dqs_network_score": float(getattr(ctx, "dqs_network_score", 0.0)),
            "adn_level": getattr(ctx.adn_level, "value", str(ctx.adn_level)),
            "wallet_balance": float(getattr(ctx, "wallet_balance", 0.0)),
            "tx_amount": float(getattr(ctx, "tx_amount", 0.0)),
            "address_age_days": getattr(ctx, "address_age_days", None),
            "behaviour_score": float(getattr(ctx, "behaviour_score", 1.0)),
            "device_id": getattr(ctx, "device_id", None),
            "trusted_device": bool(getattr(ctx, "trusted_device", True)),
        }

    def _map_reason_id_fallback(self, result: DecisionResult) -> str:
        """
        Fallback mapping for v3 reason_id (compat only).

        This should only be used if an older DecisionResult has no reason_id.
        """
        reason = getattr(result, "reason", "") or ""

        if "Critical chain or node risk" in reason:
            return "QWG_V3_CRITICAL_CHAIN_OR_NODE_RISK"
        if "Risk level exceeds wallet policy" in reason:
            return "QWG_V3_POLICY_MAX_RISK_EXCEEDED"
        if "Attempt to send ~100% of wallet balance" in reason:
            return "QWG_V3_FULL_BALANCE_WIPE_ATTEMPT"
        if "Amount exceeds extra-auth threshold" in reason:
            return "QWG_V3_EXTRA_AUTH_THRESHOLD_EXCEEDED"
        if "Large transaction during high risk period" in reason:
            return "QWG_V3_RATIO_EXCEEDS_HIGH_RISK_LIMIT"
        if "Transaction exceeds normal per-tx ratio" in reason:
            return "QWG_V3_RATIO_EXCEEDS_NORMAL_LIMIT"
        if "Unusual behaviour or untrusted device" in reason:
            return "QWG_V3_BEHAVIOUR_OR_DEVICE_RISK"
        if "No policy or risk rule violated" in reason:
            return "QWG_V3_HEALTHY_ALLOW"

        return "QWG_V3_UNCLASSIFIED_REASON"

    def _map_outcome(self, decision: Decision) -> str:
        """
        Map internal Decision into v3 outcome string for the verdict envelope.
        """
        if decision == Decision.ALLOW:
            return "allow"
        if decision == Decision.BLOCK:
            return "deny"
        return "escalate"

    # ------------------------------------------------------------------ #
    # Public API (v0.4)
    # ------------------------------------------------------------------ #

    def evaluate_transaction(self, ctx: RiskContext) -> DecisionResult:
        p = self.policy

        # 1) Hard stop on CRITICAL risk from Sentinel or ADN
        if ctx.sentinel_level == RiskLevel.CRITICAL or ctx.adn_level == RiskLevel.CRITICAL:
            reason = "Critical chain or node risk reported by Sentinel/ADN."
            result = DecisionResult(
                decision=Decision.BLOCK,
                reason=reason,
                reason_id="QWG_V3_CRITICAL_CHAIN_OR_NODE_RISK",
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
                reason_id="QWG_V3_POLICY_MAX_RISK_EXCEEDED",
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
                    reason_id="QWG_V3_FULL_BALANCE_WIPE_ATTEMPT",
                )
                self._emit_adaptive(ctx, Decision.BLOCK, reason, severity=0.9)
                return result

        # 4) Extra auth for large absolute amounts
        if ctx.tx_amount >= p.threshold_extra_auth:
            reason = "Amount exceeds extra-auth threshold."
            result = DecisionResult(
                decision=Decision.REQUIRE_EXTRA_AUTH,
                reason=reason,
                reason_id="QWG_V3_EXTRA_AUTH_THRESHOLD_EXCEEDED",
                require_confirmation=True,
                require_second_factor=True,
            )
            self._emit_adaptive(ctx, Decision.REQUIRE_EXTRA_AUTH, reason, severity=0.7)
            return result

        # 5) Limit ratio based on risk level
        if ctx.wallet_balance > 0:
            ratio = ctx.tx_amount / ctx.wallet_balance

            if ctx.sentinel_level == RiskLevel.HIGH or ctx.adn_level == RiskLevel.HIGH:
                if ratio > p.max_tx_ratio_high:
                    reason = "Large transaction during high risk period."
                    result = DecisionResult(
                        decision=Decision.WARN,
                        reason=reason,
                        reason_id="QWG_V3_RATIO_EXCEEDS_HIGH_RISK_LIMIT",
                        cooldown_seconds=p.cooldown_seconds_warn,
                        suggested_limit=p.max_tx_ratio_high * ctx.wallet_balance,
                    )
                    self._emit_adaptive(ctx, Decision.WARN, reason, severity=0.65)
                    return result
            else:
                if ratio > p.max_tx_ratio_normal:
                    reason = "Transaction exceeds normal per-tx ratio."
                    result = DecisionResult(
                        decision=Decision.WARN,
                        reason=reason,
                        reason_id="QWG_V3_RATIO_EXCEEDS_NORMAL_LIMIT",
                        cooldown_seconds=p.cooldown_seconds_warn,
                        suggested_limit=p.max_tx_ratio_normal * ctx.wallet_balance,
                    )
                    self._emit_adaptive(ctx, Decision.WARN, reason, severity=0.55)
                    return result

        # 6) Behaviour / device checks
        if ctx.behaviour_score > 1.5 or not ctx.trusted_device:
            reason = "Unusual behaviour or untrusted device detected."
            result = DecisionResult(
                decision=Decision.WARN,
                reason=reason,
                reason_id="QWG_V3_BEHAVIOUR_OR_DEVICE_RISK",
                cooldown_seconds=p.cooldown_seconds_warn,
            )
            self._emit_adaptive(ctx, Decision.WARN, reason, severity=0.6)
            return result

        # 7) Default: allow
        return DecisionResult(
            decision=Decision.ALLOW,
            reason="No policy or risk rule violated.",
            reason_id="QWG_V3_HEALTHY_ALLOW",
        )

    # ------------------------------------------------------------------ #
    # Public API (v3 wrapper)
    # ------------------------------------------------------------------ #

    def evaluate_transaction_v3(self, ctx: RiskContext):
        """
        v3 wrapper around evaluate_transaction().

        IMPORTANT:
        - does NOT change decision logic
        - returns deterministic, glass-box verdict envelope
        """
        v3_context = self._build_v3_context(ctx)
        context_hash = compute_context_hash(v3_context)

        result = self.evaluate_transaction(ctx)

        class _DecisionLike:
            def __init__(self, outcome: str, reason_id: str):
                self.outcome = outcome
                self.reason_id = reason_id
                self.reasons = None

        reason_id = result.reason_id or self._map_reason_id_fallback(result)

        decision_like = _DecisionLike(
            outcome=self._map_outcome(result.decision),
            reason_id=reason_id,
        )

        return to_v3_verdict(decision_like, context_hash)
