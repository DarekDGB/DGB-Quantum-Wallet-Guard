"""
High-risk network scenario:
Sentinel / ADN signal elevated or critical risk.

Run with:
    python -m examples.high_risk_scenario
"""

from qwg.engine import DecisionEngine
from qwg.policies import WalletPolicy
from qwg.risk_context import RiskContext, RiskLevel


def main() -> None:
    engine = DecisionEngine(WalletPolicy())

    # Elevated risk → still allowed, but may warn/limit
    elevated = RiskContext(
        wallet_balance=2_000.0,
        tx_amount=200.0,
        sentinel_level=RiskLevel.ELEVATED,
        adn_level=RiskLevel.NORMAL,
    )
    res1 = engine.evaluate_transaction(elevated)
    print("[elevated_risk]")
    print(f"  decision : {res1.decision.value}")
    print(f"  reason   : {res1.reason}")

    # High risk → stricter ratio rules
    high = RiskContext(
        wallet_balance=2_000.0,
        tx_amount=600.0,
        sentinel_level=RiskLevel.HIGH,
        adn_level=RiskLevel.NORMAL,
    )
    res2 = engine.evaluate_transaction(high)
    print("\n[high_risk_large_tx]")
    print(f"  decision : {res2.decision.value}")
    print(f"  reason   : {res2.reason}")
    if res2.suggested_limit is not None:
        print(f"  suggested_limit : {res2.suggested_limit}")

    # Critical risk → block everything
    critical = RiskContext(
        wallet_balance=2_000.0,
        tx_amount=50.0,
        sentinel_level=RiskLevel.CRITICAL,
        adn_level=RiskLevel.NORMAL,
    )
    res3 = engine.evaluate_transaction(critical)
    print("\n[critical_risk_any_tx]")
    print(f"  decision : {res3.decision.value}")
    print(f"  reason   : {res3.reason}")


if __name__ == "__main__":
    main()
