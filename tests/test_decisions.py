from qwg.decisions import Decision, DecisionResult


def test_decision_enum_values_are_stable():
    # These strings become part of the public API / logs – don't change lightly.
    assert Decision.ALLOW.value == "allow"
    assert Decision.WARN.value == "warn"
    assert Decision.DELAY.value == "delay"
    assert Decision.BLOCK.value == "block"
    assert Decision.REQUIRE_EXTRA_AUTH.value == "require_extra_auth"


def test_decision_result_defaults():
    r = DecisionResult(
        decision=Decision.ALLOW,
        reason="ok",
    )

    assert r.decision is Decision.ALLOW
    assert r.reason == "ok"
    assert r.cooldown_seconds is None or r.cooldown_seconds == 0
    assert r.suggested_limit is None
    assert r.require_confirmation is False
    assert r.require_second_factor is False


def test_decision_result_with_all_flags():
    r = DecisionResult(
        decision=Decision.REQUIRE_EXTRA_AUTH,
        reason="Big tx",
        cooldown_seconds=300,
        suggested_limit=1_000.0,
        require_confirmation=True,
        require_second_factor=True,
    )

    assert r.decision is Decision.REQUIRE_EXTRA_AUTH
    assert r.reason == "Big tx"
    assert r.cooldown_seconds == 300
    assert r.suggested_limit == 1_000.0
    assert r.require_confirmation is True
    assert r.require_second_factor is True
