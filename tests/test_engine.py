from qwg.engine import DecisionEngine
from qwg.policies import WalletPolicy
from qwg.risk_context import RiskContext, RiskLevel
from qwg.decisions import Decision


def test_allow_normal_tx():
    engine = DecisionEngine(WalletPolicy())
    ctx = RiskContext(
        wallet_balance=1000.0,
        tx_amount=100.0,
        sentinel_level=RiskLevel.NORMAL,
        adn_level=RiskLevel.NORMAL,
    )
    result = engine.evaluate_transaction(ctx)
    assert result.decision == Decision.ALLOW


def test_block_full_balance_wipe():
    engine = DecisionEngine(WalletPolicy())
    ctx = RiskContext(
        wallet_balance=1000.0,
        tx_amount=999.0,
    )
    result = engine.evaluate_transaction(ctx)
    assert result.decision == Decision.BLOCK


def test_block_on_critical_risk():
    engine = DecisionEngine(WalletPolicy())
    ctx = RiskContext(
        wallet_balance=1000.0,
        tx_amount=10.0,
        sentinel_level=RiskLevel.CRITICAL,
    )
    result = engine.evaluate_transaction(ctx)
    assert result.decision == Decision.BLOCK
