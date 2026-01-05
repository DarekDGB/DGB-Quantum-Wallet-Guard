from qwg.engine import DecisionEngine
from qwg.risk_context import RiskContext


def test_engine_evaluate_transaction_v3_returns_glass_box_verdict():
    engine = DecisionEngine()

    # "Healthy allow" default context (should not trigger any rules)
    ctx = RiskContext(
        wallet_balance=1000.0,
        tx_amount=1.0,
        trusted_device=True,
        behaviour_score=1.0,
    )

    verdict = engine.evaluate_transaction_v3(ctx)

    # Glass-box envelope invariants
    assert verdict.schema_version == "v3"
    assert verdict.verdict_type.value in ("allow", "deny", "escalate")
    assert isinstance(verdict.reason_id, str) and len(verdict.reason_id) > 0
    assert isinstance(verdict.context_hash, str) and len(verdict.context_hash) == 64

    # For this healthy context, it should be an allow with the known stable reason_id
    assert verdict.verdict_type.value == "allow"
    assert verdict.reason_id == "QWG_V3_HEALTHY_ALLOW"
