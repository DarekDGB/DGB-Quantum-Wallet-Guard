# DigiByte Quantum Wallet Guard  
## Code Blueprint — Version 2  
**Author:** DarekDGB  
**License:** MIT

---

# 1. Module Layout

QWG follows a clean, modular structure:

```
qwg/
  engine.py
  risk_context.py
  policies.py
  decisions.py
```

---

# 2. Engine Overview

The `DecisionEngine` evaluates a `RiskContext` and produces a `DecisionResult`.

High‑level algorithm:

```
if critical risk → BLOCK
elif risk > tolerance → DELAY
elif ~100% balance wipe → BLOCK
elif large ratio → WARN
elif tx >= threshold_extra_auth → REQUIRE_EXTRA_AUTH
elif behaviour anomaly → WARN
else → ALLOW
```

This order must be preserved across all languages.

---

# 3. Core Files

## 3.1 risk_context.py

Contains:

- RiskLevel enum  
- RiskContext dataclass  
- severity ordering  
- behaviour score model  

## 3.2 policies.py

Policy class controlling:

- balance wipe protection  
- ratio limits  
- cooldowns  
- allowed risk threshold  
- extra‑auth trigger levels  

## 3.3 decisions.py

Stable public API strings:

```
allow
warn
delay
block
require_extra_auth
```

## 3.4 engine.py

Implements the evaluation logic using the ordered rule list.

---

# 4. Example Integration

```python
from qwg.engine import DecisionEngine
from qwg.risk_context import RiskContext, RiskLevel

engine = DecisionEngine()

ctx = RiskContext(
    wallet_balance=1500,
    tx_amount=900,
    sentinel_level=RiskLevel.ELEVATED
)

print(engine.evaluate_transaction(ctx))
```

---

# 5. Multi‑Language Porting Guide

When porting to Rust, C++, Kotlin, JS:

- preserve evaluation order  
- preserve enum string values  
- preserve WalletPolicy defaults  
- return DecisionResult in the same structure  

---

# 6. Merge Preparation

In 2026, QWG v2 will integrate with Layers 1–4 into a unified Quantum Shield Network SDK.

The merge will include:

- unified RiskContext pipeline  
- shared config  
- shared engine entrypoint  

---

# 7. Final Notes

QWG v2 is designed to be lightweight, deterministic, and ready for future PQC integration.

Authored by **DarekDGB**.
