"""
Basic example: normal vs suspicious transaction.

Run with:
    python -m examples.basic_usage
"""

from qwg.engine import DecisionEngine
from qwg.policies import WalletPolicy
from qwg.risk_context import RiskContext, RiskLevel


def show_result(label: str, ctx: RiskContext, engine: DecisionEngine) -> None:
    result = engine.evaluate_transaction(ctx)
    print(f"\n[{label}]")
    print(f"  decision : {result.decision.value}")
    print(f"  reason   : {result.reason}")
    if result.cooldown_seconds:
        print(f"  cooldown : {result.cooldown_seconds}s")
    if result.suggested_limit is not None:
        print(f"  suggested_limit : {result.suggested_limit}")
    if result.require_confirmation or result.require_second_factor:
        print("  extra_auth : confirmation="
              f"{result.require_confirmation}, "
              f"second_factor={result.require_second_factor}")


def main() -> None:
    policy = WalletPolicy()
    engine = DecisionEngine(policy=policy)

    # Normal small transaction
    normal_ctx = RiskContext(
        wallet_balance=1_000.0,
        tx_amount=50.0,
        sentinel_level=RiskLevel.NORMAL,
        adn_level=RiskLevel.NORMAL,
    )
    show_result("normal_tx", normal_ctx, engine)

    # Suspicious large transaction (50% of balance)
    big_ctx = RiskContext(
        wallet_balance=1_000.0,
        tx_amount=500.0,
        sentinel_level=RiskLevel.NORMAL,
        adn_level=RiskLevel.NORMAL,
    )
    show_result("large_tx", big_ctx, engine)


if __name__ == "__main__":
    main()
