# DigiByte Quantum Wallet Guard  
## Developer Guide — Version 2  
**Author:** DarekDGB  
**License:** MIT

---

# 1. Introduction

This guide explains how developers integrate QWG into DigiByte wallets, services, and node‑based systems.

QWG provides the final decision on whether a transaction should be:

- allowed  
- warned  
- delayed  
- blocked  
- or require extra authentication  

---

# 2. Quick Start

```python
from qwg.engine import DecisionEngine
from qwg.risk_context import RiskContext, RiskLevel

engine = DecisionEngine()

ctx = RiskContext(wallet_balance=1000, tx_amount=200)
result = engine.evaluate_transaction(ctx)
print(result.decision, result.reason)
```

---

# 3. Feeding Risk Signals

Typical pipeline:

```
Wallet UI → Build tx → Gather signals → Create RiskContext → QWG DecisionEngine
```

Recommended fields:

- wallet_balance  
- tx_amount  
- sentinel_level  
- adn_level  
- behaviour_score  
- trusted_device  

---

# 4. Handling Decisions

| Decision | Required Wallet Action |
|----------|------------------------|
| ALLOW | Sign + broadcast |
| WARN | Show warning, suggest safer limit |
| DELAY | Enforce cooldown timer |
| BLOCK | Do not sign — show reason |
| REQUIRE_EXTRA_AUTH | Trigger 2FA or hardware approval |

Example:

```python
if result.decision is Decision.WARN:
    show_warning(result.reason)
```

---

# 5. Custom Policies

```python
strict = WalletPolicy(
    max_tx_ratio_normal=0.3,
    threshold_extra_auth=2000.0,
    max_allowed_risk=RiskLevel.ELEVATED,
)
engine = DecisionEngine(strict)
```

Policies allow wallet differentiation:

- retail wallets  
- institutional custodians  
- exchanges  
- mobile/desktop clients  

---

# 6. Testing Your Integration

QWG ships a comprehensive pytest suite validating:

- decision logic  
- warning conditions  
- extra‑auth triggers  
- behaviour/device models  

Wallets should include their own tests simulating real‑world scenarios.

---

# 7. Logging & Observability

Wallets should log:

- input RiskContext (sanitized)  
- output DecisionResult  
- user actions after decision  

This enables tuning and anomaly detection.

---

# 8. Merge Roadmap (2026)

After all 5 layers reach v2:

- Integrate into a unified Quantum Shield Network SDK  
- Provide stable API bindings for Rust, C++, JS  
- Add PQC upgrade pathways  

---

# 9. Credits

Designed and authored by **DarekDGB** as part of the DigiByte Quantum Shield Network.
