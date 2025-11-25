# DigiByte Quantum Shield Network  
## DGB Quantum Wallet Guard — Layer 5 v2 Whitepaper

**Author:** Darek (@Darek_DGB)  
**Module:** DGB Quantum Wallet Guard (QWG) — Layer 5 v2  
**License:** MIT  
**Status:** Reference implementation, open-source

---

## 1. Vision and Role in the Stack

The DigiByte Quantum Shield Network is a 5‑layer security mesh designed to protect
DigiByte from emerging quantum and advanced attack vectors.

High‑level architecture:

```text
┌───────────────────────────────┐
│   Sentinel AI v2 (Layer 1)   │  Chain-level anomaly detection
└──────────────┬────────────────┘
               │ signals
┌──────────────▼────────────────┐
│     DQSN (Layer 2)            │  Network-wide threat scoring
└──────────────┬────────────────┘
               │ scores
┌──────────────▼────────────────┐
│     ADN v2 (Layer 3)          │  Node-local autonomous defense
└──────────────┬────────────────┘
               │ defense state
┌──────────────▼────────────────┐
│ DGB Wallet Guardian v2 (L4)   │  Local wallet risk rules
└──────────────┬────────────────┘
               │ consolidated risk
┌──────────────▼────────────────┐
│  Quantum Wallet Guard v2 (L5) │  Final decision for every tx
└───────────────────────────────┘
```

**Quantum Wallet Guard (QWG) v2** is the *final decision layer*.  
It connects all security signals and determines whether a transaction should:

- be **allowed**
- be **warned** with limits
- be **delayed**
- trigger **extra authentication**
- be **blocked completely**

---

## 2. Threat Model

QWG does not replace the lower layers — it *consumes* them.
Its focus is **wallet-level and user-level risk**, including:

- Sudden full-balance wipes
- Large transfers in high network risk periods
- Compromised or untrusted devices
- Abnormal behaviour patterns (behaviour score)
- High-value transactions that should require 2FA / extra auth
- Elevated or critical chain risk signalled by Sentinel AI v2 and ADN v2

The design assumes that **on-chain quantum attacks** will first be detectable as
anomalies in entropy, nonce reuse, mempool patterns, reorgs, or difficulty shifts.
These are covered at Layers 1–3. Layer 5 focuses on **how the wallet reacts**.

---

## 3. Design Goals

1. **Deterministic and auditable**  
   Security behaviour must be easy to reason about, debug, and verify.

2. **Configurable, not magical**  
   Policies are explicit (`WalletPolicy`) and can be tuned per wallet or use case.

3. **Composable with other layers**  
   Risk context is explicit (`RiskContext`) and can accept future signals
   from new detection engines or PQC migrations.

4. **Safe-by-default behaviour**  
   Defaults favour protection: block full balance wipes, limit ratios,
   require extra auth for big transfers.

5. **Lightweight, language-agnostic reference**  
   This Python reference implementation can be re‑implemented in C++, Rust,
   or any JVM/JS language while keeping semantics identical.

---

## 4. Data Model Overview

### 4.1 RiskLevel

```python
class RiskLevel(str, Enum):
    NORMAL = "normal"
    ELEVATED = "elevated"
    HIGH = "high"
    CRITICAL = "critical"

    def severity(self) -> int:
        order = {"normal": 0, "elevated": 1, "high": 2, "critical": 3}
        return order[self.value]
```

### 4.2 RiskContext

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
    device_id: Optional[str] = None
    trusted_device: bool = True

    created_at: datetime = datetime.utcnow()
```

### 4.3 WalletPolicy

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

### 4.4 Decisions

```python
class Decision(str, Enum):
    ALLOW = "allow"
    WARN = "warn"
    DELAY = "delay"
    BLOCK = "block"
    REQUIRE_EXTRA_AUTH = "require_extra_auth"
```

Combined with:

```python
@dataclass
class DecisionResult:
    decision: Decision
    reason: str
    cooldown_seconds: Optional[int] = None
    suggested_limit: Optional[float] = None
    require_confirmation: bool = False
    require_second_factor: bool = False
```

---

## 5. Decision Engine

The `DecisionEngine` evaluates a `RiskContext` under a `WalletPolicy`
and returns a `DecisionResult`.

High‑level flow:

```text
1. Check CRITICAL chain or node risk  → BLOCK
2. Check if risk exceeds wallet policy → DELAY
3. Block full-balance wipes (≈100%)   → BLOCK
4. Enforce per‑tx ratios (normal vs HIGH) → WARN + suggested limit
5. Trigger extra auth for large amount → REQUIRE_EXTRA_AUTH
6. React to behaviour / device issues  → WARN
7. Otherwise                            → ALLOW
```

---

## 6. Integration and Roadmap

See the Technical Spec and Developer Guide for implementation details.

Planned for **2026**: merge all five layers into a unified DigiByte
Quantum Shield SDK with PQC support and multi‑language bindings.
