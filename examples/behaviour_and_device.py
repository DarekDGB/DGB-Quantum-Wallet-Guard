"""
Behaviour & device example:
Same amount, different behaviour / device trust.

Run with:
    python -m examples.behaviour_and_device
"""

from qwg.engine import DecisionEngine
from qwg.policies import WalletPolicy
from qwg.risk_context import RiskContext, RiskLevel


def main() -> None:
    engine = DecisionEngine(WalletPolicy())

    # Normal behaviour, trusted device
    normal = RiskContext(
        wallet_balance=5_000.0,
        tx_amount=1_000.0,
        sentinel_level=RiskLevel.NORMAL,
        adn_level=RiskLevel.NORMAL,
        behaviour_score=1.0,
        trusted_device=True,
        device_id="phone-main",
    )
    res1 = engine.evaluate_transaction(normal)
    print("[trusted_device_normal_behaviour]")
    print(f"  decision : {res1.decision.value}")
    print(f"  reason   : {res1.reason}")

    # Same tx, but on unknown / untrusted device
    untrusted = RiskContext(
        wallet_balance=5_000.0,
        tx_amount=1_000.0,
        sentinel_level=RiskLevel.NORMAL,
        adn_level=RiskLevel.NORMAL,
        behaviour_score=2.0,          # looks risky
        trusted_device=False,          # new device
        device_id="suspicious-laptop",
    )
    res2 = engine.evaluate_transaction(untrusted)
    print("\n[untrusted_device_risky_behaviour]")
    print(f"  decision : {res2.decision.value}")
    print(f"  reason   : {res2.reason}")
    if res2.cooldown_seconds:
        print(f"  cooldown : {res2.cooldown_seconds}s")


if __name__ == "__main__":
    main()
