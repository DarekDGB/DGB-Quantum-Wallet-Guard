from qwg.engine import DecisionEngine
from qwg.risk_context import RiskContext, RiskLevel
from qwg.policies import WalletPolicy


def test_decision_result_includes_reason_id_for_critical_block():
    engine = DecisionEngine()
    ctx = RiskContext(
        sentinel_level=RiskLevel.CRITICAL,
        wallet_balance=1000.0,
        tx_amount=10.0,
    )
    result = engine.evaluate_transaction(ctx)
    assert result.reason_id == "QWG_V3_CRITICAL_CHAIN_OR_NODE_RISK"


def test_decision_result_includes_reason_id_for_extra_auth():
    policy = WalletPolicy()
    policy.threshold_extra_auth = 5.0
    engine = DecisionEngine(policy=policy)

    ctx = RiskContext(
        wallet_balance=1000.0,
        tx_amount=10.0,
    )
    result = engine.evaluate_transaction(ctx)
    assert result.reason_id == "QWG_V3_EXTRA_AUTH_THRESHOLD_EXCEEDED"
