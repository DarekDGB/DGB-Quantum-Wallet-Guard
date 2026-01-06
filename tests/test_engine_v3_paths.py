from qwg.engine import DecisionEngine
from qwg.risk_context import RiskContext, RiskLevel
from qwg.policies import WalletPolicy


def test_v3_wrapper_denies_on_critical_risk():
    engine = DecisionEngine()

    ctx = RiskContext(
        sentinel_level=RiskLevel.CRITICAL,
        wallet_balance=1000.0,
        tx_amount=10.0,
        trusted_device=True,
        behaviour_score=1.0,
    )

    verdict = engine.evaluate_transaction_v3(ctx)

    assert verdict.schema_version == "v3"
    assert verdict.verdict_type.value == "deny"
    assert verdict.reason_id == "QWG_V3_CRITICAL_CHAIN_OR_NODE_RISK"
    assert isinstance(verdict.context_hash, str) and len(verdict.context_hash) == 64


def test_v3_wrapper_escalates_on_extra_auth_threshold():
    # Make the threshold small to force the path deterministically
    policy = WalletPolicy()
    policy.threshold_extra_auth = 5.0

    engine = DecisionEngine(policy=policy)

    ctx = RiskContext(
        wallet_balance=1000.0,
        tx_amount=10.0,  # exceeds threshold_extra_auth
        trusted_device=True,
        behaviour_score=1.0,
    )

    verdict = engine.evaluate_transaction_v3(ctx)

    assert verdict.schema_version == "v3"
    assert verdict.verdict_type.value == "escalate"
    assert verdict.reason_id == "QWG_V3_EXTRA_AUTH_THRESHOLD_EXCEEDED"
    assert isinstance(verdict.context_hash, str) and len(verdict.context_hash) == 64
