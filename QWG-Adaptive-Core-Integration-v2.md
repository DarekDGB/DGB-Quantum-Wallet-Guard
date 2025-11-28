# QWG ↔ Adaptive Core Integration (v2)

This document shows how **DGB Quantum Wallet Guard (QWG)** can send
lightweight adaptive events into the **DigiByte Quantum Adaptive Core**.
The bridge is **optional**, **safe by default**, and never blocks wallet
decisions if the adaptive layer is offline.

---

## 1. Concept

- QWG decides what to do with a transaction: `ALLOW`, `WARN`, `DELAY`, `BLOCK`,
  `REQUIRE_EXTRA_AUTH`.
- For any **risky** decision, QWG emits a small event into the Adaptive Core,
  containing:
  - `event_id` (usually `tx_id`)
  - `action` (e.g. `"block"`, `"delay"`, `"warn"`)
  - `severity` (0.0–1.0)
  - `fingerprint` (wallet identifier)
  - `user_id` (optional)
  - risk & behaviour context (amount, balance, device trust, etc.)

On the Adaptive Core side, these events can be used to:
- reinforce learning,
- tune thresholds,
- update per-wallet risk scores,
- correlate wallet behaviour with on-chain threats.

---

## 2. Minimal Adaptive Sink Interface

QWG **does not import** `adaptive_core` directly.
Instead, it expects an object with a method like:

```python
class MyAdaptiveSink:
    def handle_event(self, event: dict) -> None:
        ...
```

or:

```python
class MyAdaptiveSink:
    def add_event(self, event: dict) -> None:
        ...
```

If no compatible method is found, or if anything fails,
**QWG ignores the adaptive path and continues normally.**

---

## 3. Wiring QWG to an Adaptive Sink

Example with a simple in-memory sink:

```python
from qwg.engine import DecisionEngine
from qwg.policies import WalletPolicy
from qwg.risk_context import RiskContext, RiskLevel


class InMemoryAdaptiveSink:
    def __init__(self) -> None:
        self.events: list[dict] = []

    def handle_event(self, event: dict) -> None:
        # In production this would forward into Adaptive Core.
        self.events.append(event)


# 1) Create policy + decision engine
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

# 4) Attach adaptive sink to the context
ctx.adaptive_sink = adaptive_sink

# 5) Ask QWG for a decision
result = engine.evaluate_transaction(ctx)

print(result.decision, result.reason)
print("Adaptive events:", adaptive_sink.events)
```

When the decision engine returns a **risky** verdict (for example `WARN`,
`DELAY` or `BLOCK`), an adaptive event is automatically emitted via
`adaptive_bridge.emit_adaptive_event(...)`. For healthy traffic (`ALLOW`),
no event is sent.

---

## 4. Using the Real Adaptive Core

In a full deployment, `adaptive_sink` would be an instance of the
**Adaptive Core interface** (from the DigiByte Quantum Adaptive Core repo),
for example:

```python
from adaptive_core.interface import AdaptiveCoreInterface
from qwg.engine import DecisionEngine
from qwg.risk_context import RiskContext, RiskLevel

adaptive = AdaptiveCoreInterface()
engine = DecisionEngine()

ctx = RiskContext(
    tx_amount=1.5,
    wallet_balance=2.0,
    sentinel_level=RiskLevel.ELEVATED,
    adn_level=RiskLevel.NORMAL,
    behaviour_score=1.0,
    trusted_device=True,
)

ctx.tx_id = "tx-123"
ctx.wallet_fingerprint = "wallet-abc"
ctx.user_id = "user-42"
ctx.adaptive_sink = adaptive

result = engine.evaluate_transaction(ctx)
```

As long as `AdaptiveCoreInterface` exposes `handle_event(event: dict)`
(or `add_event`), QWG will automatically feed it wallet-level risk signals.

---

## 5. Safety Guarantees

- If `ctx.adaptive_sink` is **missing**, no events are sent.
- If the sink object has **no compatible method**, QWG silently skips it.
- If the sink **raises an exception**, QWG catches it and continues.
- Wallet safety and user funds are **never** blocked by adaptive plumbing.

The adaptive path is **best-effort**, designed so that DigiByte wallets stay
operational even if the Adaptive Core is offline, misconfigured or under
maintenance.
