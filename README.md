# 🛡️ Quantum Wallet Guard (QWG)
### *User-Side Transaction Vetting, PQC Verification & Behavioural Defence Layer*
**Architecture by @DarekDGB — MIT Licensed**

---

## 🚀 Purpose

**Quantum Wallet Guard (QWG)** is the **user-side defensive engine** of the DigiByte Quantum Shield.  
It is the final intelligent checkpoint before any wallet action occurs.

Where:

- **DQSN v2** measures network entropy & health  
- **Sentinel AI v2** detects anomalies  
- **ADN v2** produces defence playbooks  

**QWG** evaluates *user transactions and wallet behaviour* in real time.

It performs:

- PQC-ready signature verification  
- heuristic & behavioural transaction analysis  
- runtime defence logic  
- integration with Guardian Wallet  
- network threat response based on ADN signals  

QWG is **your last line of defence before funds leave the wallet**.

---

# 🛡️ Position in the 5-Layer DigiByte Quantum Shield

```
 ┌───────────────────────────────────────────────┐
 │              Guardian Wallet                  │
 │   User warnings • Hardening policies          │
 └───────────────────────────────────────────────┘
                     ▲
                     │  (structured warnings & prompts)
 ┌───────────────────────────────────────────────┐
 │       QWG — Quantum Wallet Guard              │
 │ Runtime Guard • PQC Verification • Behaviour  │
 └───────────────────────────────────────────────┘
                     ▲
                     │  (defence playbook outputs)
 ┌───────────────────────────────────────────────┐
 │                ADN v2                         │
 │ Defence Tactics • Scenario Routing            │
 └───────────────────────────────────────────────┘
                     ▲
                     │  (threat signals)
 ┌───────────────────────────────────────────────┐
 │             Sentinel AI v2                    │
 │ Telemetry Analytics & Anomaly Detection       │
 └───────────────────────────────────────────────┘
                     ▲
                     │  (entropy & network metrics)
 ┌───────────────────────────────────────────────┐
 │                  DQSN v2                      │
 │ Network Health • Node Metrics • Chain Signals │
 └───────────────────────────────────────────────┘
```

QWG is the **shield that stands directly between the user and danger**.

---

# 🎯 Core Mission

### ✓ PQC Signature Verification  
QWG includes PQC-ready adapters for:

- Falcon  
- Dilithium  

ensuring future-proof DigiByte transaction validation.

### ✓ Transaction Behaviour Analysis  
Detects anomalies such as:

- draining UTXOs  
- large sends to unseen addresses  
- suspicious fee patterns  
- abnormal timing (bot-like actions)  

### ✓ Runtime Defence Logic  
Guards the wallet continuously:

- intercepts dangerous actions  
- delays or blocks unsafe behaviour  
- triggers Guardian Wallet warnings  

### ✓ ADN Signal Integration  
If ADN detects a network threat:

- reorg attacks  
- propagation anomalies  
- hashpower surges  

QWG adjusts its behaviour accordingly:

- warns users  
- recommends delaying sends  
- increases verification strictness  

### ✓ Zero-Trust Protection  
QWG assumes:

- the OS may be compromised  
- clipboard may be hijacked  
- malware may be active  
- user may be manipulated  

Therefore:

**QWG protects by default.**

---

# 🧠 Threat Model (User-Side Focus)

QWG protects against:

### **1. Human Error**
- sending to wrong address  
- sending too much  
- accepting abnormal fees  

### **2. Malware / Phishing**
- clipboard hijacking  
- auto-withdrawal scripts  
- infected environment behaviour  

### **3. Quantum Threats (Future)**
- invalid ECDSA signatures  
- PQC forgery attempts  
- mixed-signature anomalies  

### **4. Network-Level Attacks**
Triggered by ADN signals:

- reorg risk  
- partition/eclipse detection  
- mempool flooding  
- timing manipulation  

### **5. Social Engineering**
- fake addresses  
- last-minute swap of recipient  
- unusual withdrawal behaviour  

---

# 🧩 Internal Architecture (Reference)

```
qwg/
│
├── pqc/
│     ├── verifier.py
│     ├── falcon_adapter.py
│     ├── dilithium_adapter.py
│
├── analysis/
│     ├── behavior_engine.py
│     ├── tx_pattern.py
│     └── fee_sanity.py
│
├── defence/
│     ├── guard_runtime.py
│     ├── rule_engine.py
│     └── adn_integration.py
│
├── outputs/
│     ├── guardian_bridge.py
│     └── warnings.py
│
└── utils/
      ├── types.py
      ├── config.py
      └── logging.py
```

Each module is modular, extendable, and clean — ready for DigiByte Core developers.

---

# 📡 Data Flow Overview

```
[User attempts a transaction]
              │
              ▼
      ┌───────────────────────┐
      │   QWG Runtime Guard   │
      └───────────────────────┘
              │
   ┌──────────┼───────────┐
   ▼          ▼           ▼
[Behaviour] [PQC]   [ADN Signal]
[Analysis] [Verify] [Integration]
   │          │           │
   └──────────┼───────────┘
              ▼
     [Decision & Warning Engine]
              ▼
      [Guardian Wallet Prompt]
```

QWG always explains **why** it warns the user.

---

# 🔐 PQC Architecture

QWG contains:

- PQC signature validator  
- abstraction layer for signing scheme upgrades  
- ready adapters (Falcon/Dilithium)  
- fallback ECDSA behaviour for current DGB  

This ensures:

- DigiByte is ready for quantum migration  
- wallets remain upgrade-proof  
- hybrid signatures are supported in future  

---

# 🛡️ Design Principles

1. **Protect the user by default**  
2. **Fail-safe — block or warn, never silently allow**  
3. **Explainable decisions**  
4. **Deterministic behaviour**  
5. **Zero-trust model**  
6. **Composability** — extendable rules  
7. **Interoperability with Guardian Wallet & ADN**  

---

# ⚙️ Code Status

QWG includes:

- full PQC scaffolding  
- runtime guard logic  
- behavioural analysis framework  
- rule engine  
- warning output system  
- structured architecture  
- CI tests for import stability  

This repository is **architecture-complete** and ready for developer expansion.

---

# 🧪 Tests

Includes:

- structure tests  
- runtime import validation  
- behavioural engine skeleton tests  
- PQC verifier stubs  

More simulations can be added by contributors.

---

# 🤝 Contribution Policy

See `CONTRIBUTING.md` for full rules.

Summary:

- ✓ improvements welcome  
- ✓ new defence logic  
- ✓ stronger rules  
- ✗ no removal of architecture  
- ✗ no consensus changes  
- ✗ no UI logic (handled by Guardian Wallet)  

---

# 📜 License

MIT License  
© 2025 **DarekDGB**

This architecture is free to use with mandatory attribution.
