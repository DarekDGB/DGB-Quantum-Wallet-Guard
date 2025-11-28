# DGB Quantum Wallet Guard — Layer 5 v2
### Post‑Quantum Wallet Defense Layer for DigiByte  
#### *Full Technical Documentation — English Version (v2)*  
Made by **Darek_DGB** & **Angel**

---

# 🛡 1. Overview

**Quantum Wallet Guard (QWG) v2** is **Layer 5** of the DigiByte 5‑Layer Quantum Shield Network.

It is the **final decision-maker** before any DigiByte wallet transaction is broadcast.  
QWG reads all risk signals from the lower layers:

| Layer | Component | Purpose |
|------|-----------|---------|
| 1 | Sentinel AI v2 | Chain anomaly detection |
| 2 | DQSN v2 | Network‑wide threat validation |
| 3 | ADN v2 | Node‑level autonomous protection |
| 4 | Guardian Wallet v2 | Wallet-side enforcement |
| 5 | **QWG v2** | Final transaction approval block/delay/warn |

Layer 5 transforms the entire multi‑layer shield into **wallet‑level protection**, ensuring DigiByte remains ultra‑secure even in future quantum threat models.

---

# ⚙️ 2. Architecture Blueprint

```
             ┌────────────────────────────────────────┐
             │         Sentinel AI v2 (Layer 1)        │
             └────────────────────────────────────────┘
                              │ alerts
                              ▼
             ┌────────────────────────────────────────┐
             │        DQSN v2 (Layer 2 – network)     │
             └────────────────────────────────────────┘
                              │ signals
                              ▼
             ┌────────────────────────────────────────┐
             │        ADN v2 (Layer 3 – node AI)      │
             └────────────────────────────────────────┘
                              │ local defense states
                              ▼
             ┌────────────────────────────────────────┐
             │   DGB Wallet Guardian v2 (Layer 4)     │
             └────────────────────────────────────────┘
                              │ enriched risk context
                              ▼
      ┌─────────────────────────────────────────────────────────┐
      │   🛡 Quantum Wallet Guard v2 (Layer 5 – THIS MODULE)    │
      └─────────────────────────────────────────────────────────┘
            │ final wallet enforcement (block/delay/warn)
            ▼
               Transaction → DigiByte blockchain
```

---

# 🧠 3. Core Responsibilities

## QWG v2 performs:

### **1. Multi-Layer Risk Fusion**
It reads and interprets:
- Sentinel AI risk level  
- ADN risk level  
- DQSN global threat score  
- Behavioural patterns  
- Device trust score  
- Wallet heuristics

---

### **2. Wallet Policy Enforcement**
Includes:
- full balance wipe protection  
- max ratio per tx  
- high‑risk ratio limits  
- extra auth triggers  
- cool‑downs in risky conditions  

---

### **3. Emitting Adaptive Events (NEW v2)**
Every block/delay/warn decision is sent as a **ThreatPacket-like AdaptiveEvent** to **Adaptive Core v2**, allowing the shield to *learn from wallet behaviour*.

---

### **4. No-Impact Safety**
The adaptive callback is **best‑effort only** — QWG never breaks wallet flow, even if Adaptive Core is offline.

---

# 📁 4. File Structure

```
src/qwg/
│   engine.py
│   risk_context.py
│   policies.py
│   decisions.py
│   adaptive_bridge.py
│   __init__.py
│
examples/
tests/
.github/workflows/ci.yml
QWG_Whitepaper_v2.md
QWG_TechSpec_v2.md
QWG_DeveloperGuide_v2.md
QWG_CodeBlueprint_v2.md
```

---

# 🔍 5. Technical Components

## 5.1 RiskContext
Carries all risk information into the decision engine.

```python
@dataclass
class RiskContext:
    sentinel_level: RiskLevel = RiskLevel.NORMAL
    dqs_network_score: float = 0.0
    adn_level: RiskLevel = RiskLevel.NORMAL

    wallet_balance: float = 0.0
    tx_amount: float = 0.0

    address_age_days: Optional[int] = None
    behaviour_score: float = 1.0
    trusted_device: bool = True

    # Adaptive Core sink
    adaptive_sink: Optional[Any] = None

    tx_id: Optional[str] = None
    wallet_fingerprint: Optional[str] = None
    user_id: Optional[str] = None
```

---

## 5.2 WalletPolicy

```python
@dataclass
class WalletPolicy:
    block_full_balance_tx: bool = True
    max_tx_ratio_normal: float = 0.5
    max_tx_ratio_high: float = 0.1
    max_allowed_risk: RiskLevel = RiskLevel.HIGH

    cooldown_seconds_warn: int = 60
    cooldown_seconds_delay: int = 300

    threshold_extra_auth: float = 10_000.0
```

---

## 5.3 Decision Engine (QWG Brain)

### Primary enforcement rules:

1. **Block** on CRITICAL Sentinel or ADN risk  
2. **Delay** transactions when risk > wallet policy  
3. **Block** full balance wipes  
4. **Extra auth** on high-value amounts  
5. **Ratio throttle** based on chain risk  
6. **Warn** on behaviour or device anomalies  
7. **Allow** only when everything is clean  

---

## 5.4 Adaptive Event Emission (v2 upgrade)

```python
emit_adaptive_event(
    adaptive_sink,
    event_id=ctx.tx_id,
    action=decision.name.lower(),
    severity=0.55–0.95,
    fingerprint=ctx.wallet_fingerprint,
    user_id=ctx.user_id,
    extra={ ... }
)
```

This allows the Adaptive Core v2 to:
- learn from wallet behaviour  
- adjust threshold sensitivity  
- detect wallet-level attack patterns  
- store ThreatPacket-like records  

---

# 🧪 6. Testing Overview

### Tests cover:
- full decision engine logic  
- high‑risk scenarios  
- ratio rules  
- device trust logic  
- adaptive event emission safety  
- integration → Adaptive Core v2  
- pytest CI automation  

Test suite runs inside GitHub Actions on every push.

---

# 📘 7. Documentation Files Included

| File | Purpose |
|------|---------|
| **QWG_Whitepaper_v2.md** | High-level conceptual overview |
| **QWG_TechSpec_v2.md** | All structures, enums, rules |
| **QWG_DeveloperGuide_v2.md** | How to integrate QWG into real wallets |
| **QWG_CodeBlueprint_v2.md** | Full blueprint for developers |

---

# ☑️ 8. v2 Upgrade Summary

### What changed in v2:
- AdaptiveBridge added  
- AdaptiveEvent model added  
- DecisionEngine now emits ThreatPacket-style events  
- Wallet behaviour added into shield intelligence  
- Better risk fusion from Sentinel/DQSN/ADN  
- Codebase modularized for merge in 2026  
- Stronger device trust model  
- Expanded test suite  
- Full CI automation  

---

# 🔮 9. Future: v3 / Merged System (2026)

Once all layers reach stable v2 readiness:

### The entire 5-layer shield merges into:

```
DigiByte Quantum Unified Shield Engine (DQ‑USE)
```

Running:
- combined inference  
- universal adaptive memory  
- shared PQC signing layer  
- multi-node protection mesh  

QWG will become the **final quantum gatekeeper** for all DigiByte wallets.

---

# 🧡 Made by DarekDGB & Angel  
### Protecting DigiByte — today, tomorrow, and in the quantum future.  
