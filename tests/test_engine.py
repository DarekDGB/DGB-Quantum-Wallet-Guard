import datetime

from qwg.engine import DecisionEngine
from qwg.policies import WalletPolicy
from qwg.risk_context import RiskContext, RiskLevel
from qwg.decisions import Decision


# ------------------------------------------------------------
# Helper for building a complete RiskContext
# ------------------------------------------------------------
def make_ctx(**overrides) -> RiskContext:
    base = dict(
        sentinel_level=RiskLevel.NORMAL,
        dqs_network_score=0.0,
        adn_level=RiskLevel.NORMAL,
        wallet_balance=1000.0,
        tx_amount=10.0,
        address_age_days=30,
        behaviour_score=1.0,
        device_id="device-1",
        trusted_device=True,
        created_at=datetime.datetime.utcnow(),
    )
    base.update(overrides)
    return RiskContext(**base)


# ------------------------------------------------------------
# Your original tests (kept exactly as they were)
# ------------------------------------------------------------

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


# ------------------------------------------------------------
# New advanced v2 tests
# ------------------------------------------------------------

def test_allow_small_tx_normal_risk():
    engine = DecisionEngine()
    ctx = make_ctx(wallet_balance=1000.0, tx_amount=10.0)
    result = engine.evaluate_transaction(ctx)
    assert result.decision is Decision.ALLOW


def test_delay_when_risk_above_policy():
    policy = WalletPolicy(max_allowed_risk=RiskLevel.ELEVATED)
    engine = DecisionEngine(policy=policy)

    ctx = make_ctx(sentinel_level=RiskLevel.HIGH)
    result = engine.evaluate_transaction(ctx)

    assert result.decision is Decision.DELAY
    assert result.cooldown_seconds == policy.cooldown_seconds_delay


def test_warn_on_large_ratio_normal_risk():
    engine = DecisionEngine()
    ctx = make_ctx(wallet_balance=1000.0, tx_amount=800.0)  # 80%
    result = engine.evaluate_transaction(ctx)

    assert result.decision is Decision.WARN
    assert result.suggested_limit == engine.policy.max_tx_ratio_normal * 1000.0


def test_warn_on_large_ratio_high_risk_stricter():
    engine = DecisionEngine()
    ctx = make_ctx(
        wallet_balance=1000.0,
        tx_amount=200.0,  # 20%
        sentinel_level=RiskLevel.HIGH,
    )
    result = engine.evaluate_transaction(ctx)

    assert result.decision is Decision.WARN
    assert result.suggested_limit == engine.policy.max_tx_ratio_high * 1000.0


def test_require_extra_auth_for_big_amount():
    policy = WalletPolicy(threshold_extra_auth=5000.0)
    engine = DecisionEngine(policy=policy)

    ctx = make_ctx(wallet_balance=10000.0, tx_amount=7000.0)
    result = engine.evaluate_transaction(ctx)

    assert result.decision is Decision.REQUIRE_EXTRA_AUTH
    assert result.require_confirmation is True
    assert result.require_second_factor is True


def test_warn_on_untrusted_device():
    engine = DecisionEngine()
    ctx = make_ctx(trusted_device=False)
    result = engine.evaluate_transaction(ctx)
    assert result.decision is Decision.WARN


def test_warn_on_high_behaviour_score():
    engine = DecisionEngine()
    ctx = make_ctx(behaviour_score=2.0)
    result = engine.evaluate_transaction(ctx)
    assert result.decision is Decision.WARN
