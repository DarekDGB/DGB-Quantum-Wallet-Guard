# DGB Quantum Wallet Guard

**DGB Quantum Wallet Guard** is a universal security engine and SDK for DigiByte wallets.  
It connects to **Sentinel AI v2**, **DQSN**, and **ADN v2** to evaluate every transaction and enforce
quantum-aware rules, limits, cooldowns, warnings and blocks.

---

## 🚀 Purpose

As DigiByte moves toward post-quantum security, wallets must become intelligent and reactive.  
DGB Quantum Wallet Guard provides a unified protection layer any DigiByte wallet can integrate with.

This SDK ensures:

- Transaction evaluation based on global + local risk  
- Protection from quantum-related anomalies  
- Behavioural checks and full-balance protection  
- Cool-downs, throttled sending, and forced confirmation steps  
- Seamless integration with Layers 1–4 of the Quantum Shield Network

---

## 🧠 Architecture (Layer 5)

DGB Quantum Wallet Guard integrates with the first four layers:

1. **Sentinel AI v2** – detection  
2. **DQSN** – network scoring  
3. **ADN v2** – node defence  
4. **DGB Wallet Guardian** – personal wallet logic  
5. **DGB Quantum Wallet Guard** – *universal SDK for all wallets*

This repository implements **Layer 5** of the DigiByte Quantum Shield Network.

---

## 📦 Features (v0.1 Roadmap)

- `RiskContext` model (Sentinel/DQSN/ADN signals)  
- `DecisionEngine` returning ALLOW / WARN / DELAY / BLOCK / REQUIRE_EXTRA_AUTH  
- User-policy rules (send limits, frequency, cooldowns)  
- Behaviour model (normal send size & patterns)  
- Device fingerprint module  
- Pluggable API for **any** DigiByte wallet

---

## 📂 Project Structure

```
/src
  /qwg
    __init__.py
    engine.py
    risk_context.py
    decisions.py
    policies.py
/tests
  test_engine.py
/examples
  basic_usage.py
LICENSE
README.md
```

---

## 🧩 Basic Usage

```python
from qwg import DecisionEngine, WalletPolicy, RiskContext, RiskLevel

policy = WalletPolicy()
engine = DecisionEngine(policy=policy)

ctx = RiskContext(
    wallet_balance=10_000.0,
    tx_amount=4_000.0,
    sentinel_level=RiskLevel.NORMAL,
    adn_level=RiskLevel.NORMAL,
)

result = engine.evaluate_transaction(ctx)
print(result.decision, result.reason)
```

---

## ⚙️ License

MIT License — open source, free for all DigiByte developers.

---

## 🌐 Vision

To provide DigiByte with a future-proof, intelligent wallet protection layer that completes the Quantum Shield Network and prepares the ecosystem for full PQC migration.

---

© 2025 DarekDGB – Open-source protection for DigiByte
