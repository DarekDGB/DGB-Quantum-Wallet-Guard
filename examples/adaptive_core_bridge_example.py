from __future__ import annotations

from qwg.engine import DecisionEngine
from qwg.policies import WalletPolicy
from qwg.risk_context import RiskContext, RiskLevel


class InMemoryAdaptiveSink:
    """
    Minimal example sink that collects adaptive events in memory.

    In production this would be replaced with the real
    DigiByte Quantum Adaptive Core interface.
    """

    def __init__(self) -> None:
        self.events: list[dict] = []

    def handle_event(self, event: dict) -> None:
        # In a real deployment, forward into Adaptive Core here.
        self.events.append(event)


def main() -> None:
    # 1) Create wallet policy + decision engine
    policy = WalletPolicy()
    engine = DecisionEngine(policy=policy)

    # 2) Create adaptive sink instance
    adaptive_sink = InMemoryAdaptiveSink()

    # 3) Build risk context for a transaction
    ctx = RiskContext(
        tx_amount=1.5,
        wallet_balance=2.0,
        sentinel_level=RiskLevel.ELEVATED,
        adn_level=RiskLevel.NORMAL,
        behaviour_score=1.0,
        trusted_device=True,
    )

    # Optional metadata used by the adaptive bridge
    ctx.tx_id = "tx-123"
    ctx.wallet_fingerprint = "wallet-abc"
    ctx.user_id = "user-42"

    # Attach adaptive sink to the context → this enables the bridge
    ctx.adaptive_sink = adaptive_sink

    # 4) Ask QWG for a decision
    result = engine.evaluate_transaction(ctx)

    print("Decision:", result.decision, "-", result.reason)
    print("Adaptive events emitted:")
    for e in adaptive_sink.events:
        print(e)


if __name__ == "__main__":
    main()
