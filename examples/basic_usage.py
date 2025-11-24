"""
Basic example of using DGB Quantum Wallet Guard (Layer 5).

This is how a DigiByte wallet would call the engine
before broadcasting a transaction.
"""

from qwg import DecisionEngine, WalletPolicy, RiskContext, RiskLevel


def main() -> None:
    # 1) Load or define wallet policy
    policy = WalletPolicy()

    # 2) Create engine
    engine = DecisionEngine(policy=policy)

    # 3) Build risk context for a transaction
    ctx = RiskContext(
        wallet_balance=10_000.0,   # total DGB balance
        tx_amount=4_000.0,         # amount we want to send
        sentinel_level=RiskLevel.NORMAL,
        adn_level=RiskLevel.NORMAL,
        dqs_network_score=0.1,
        behaviour_score=1.0,
        trusted_device=True,
    )

    # 4) Ask engine for a decision
    result = engine.evaluate_transaction(ctx)

    print("Decision:", result.decision.value)
    print("Reason:", result.reason)
    if result.suggested_limit is not None:
        print("Suggested limit:", result.suggested_limit)
    if result.cooldown_seconds:
        print("Cooldown (s):", result.cooldown_seconds)


if __name__ == "__main__":
    main()
