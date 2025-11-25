from qwg.policies import WalletPolicy
from qwg.risk_context import RiskLevel


def test_policy_defaults_are_sane():
    p = WalletPolicy()

    # max risk – by default we tolerate up to HIGH, block on CRITICAL
    assert p.max_allowed_risk == RiskLevel.HIGH

    # ratio limits
    assert 0.0 < p.max_tx_ratio_normal <= 1.0
    assert 0.0 < p.max_tx_ratio_high <= p.max_tx_ratio_normal

    # cooldowns
    assert p.cooldown_seconds_warn > 0
    assert p.cooldown_seconds_delay >= p.cooldown_seconds_warn

    # extra auth threshold should be a positive value
    assert p.threshold_extra_auth > 0

    # full-balance tx protection ON by default
    assert p.block_full_balance_tx is True


def test_policy_can_be_customised():
    p = WalletPolicy(
        block_full_balance_tx=False,
        max_tx_ratio_normal=0.75,
        max_tx_ratio_high=0.25,
        max_allowed_risk=RiskLevel.ELEVATED,
        cooldown_seconds_warn=10,
        cooldown_seconds_delay=120,
        threshold_extra_auth=5_000.0,
    )

    assert p.block_full_balance_tx is False
    assert p.max_tx_ratio_normal == 0.75
    assert p.max_tx_ratio_high == 0.25
    assert p.max_allowed_risk == RiskLevel.ELEVATED
    assert p.cooldown_seconds_warn == 10
    assert p.cooldown_seconds_delay == 120
    assert p.threshold_extra_auth == 5_000.0
