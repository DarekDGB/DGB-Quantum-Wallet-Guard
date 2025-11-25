# DigiByte Quantum Wallet Guard  
## Technical Specification — Version 2  
**Author:** DarekDGB  
**License:** MIT  
**Status:** Stable v2 (pre‑merge)

---

## 1. Purpose

The Quantum Wallet Guard (QWG) is Layer 5 of the DigiByte Quantum Shield Network.  
It provides final transaction‑level security by combining signals from:

- Sentinel AI v2 (Layer 1)  
- DQSN (Layer 2)  
- ADN v2 (Layer 3)  
- DGB Wallet Guardian v2 (Layer 4)

QWG enforces deterministic rules ensuring safe wallet behaviour under normal and high‑risk conditions.

---

## 2. Architecture

```
Sentinel AI v2 ─┐
                ├──► RiskContext → DecisionEngine → DecisionResult
       DQSN ────┤
       ADN v2 ──┘
```

QWG does not replace lower layers — it consumes their signals.

---

## 3. Core Types

### 3.1 RiskLevel

```python
class RiskLevel(str, Enum):
    NORMAL = "normal"
    ELEVATED = "elevated"
    HIGH = "high"
    CRITICAL = "critical"
```

Ordered severity: NORMAL < ELEVATED < HIGH < CRITICAL.

### 3.2 RiskContext

Central structure aggregating chain, network, node, and wallet signals.

- sentinel_level  
- dqs_network_score  
- adn_level  
- wallet_balance  
- tx_amount  
- behaviour_score  
- trusted_device  
- device_id  
- created_at  

### 3.3 WalletPolicy

Defines configurable transaction safety rules:

- block_full_balance_tx  
- max_tx_ratio_normal  
- max_tx_ratio_high  
- max_allowed_risk  
- cooldown_seconds_warn  
- cooldown_seconds_delay  
- threshold_extra_auth  

### 3.4 Decision & DecisionResult

Public API:

```
allow, warn, delay, block, require_extra_auth
```

DecisionResult encapsulates:

- decision  
- reason  
- suggested_limit  
- cooldown_seconds  
- require_confirmation  
- require_second_factor  

---

## 4. Engine Behaviour

Evaluation order (highest‑priority rules first):

1. **CRITICAL chain/node risk → BLOCK**  
2. **Risk exceeds wallet tolerance → DELAY**  
3. **~100% balance wipe → BLOCK**  
4. **Large ratio (normal/high risk) → WARN**  
5. **High absolute amount → REQUIRE_EXTRA_AUTH**  
6. **Behaviour/device anomalies → WARN**  
7. **Else → ALLOW**

---

## 5. Integration

QWG is fully deterministic and designed for:

- Desktop wallets  
- Mobile wallets  
- Node RPC services  
- Exchanges using DigiByte hot/cold wallets  

Wallets must enforce decisions strictly.

---

## 6. Test Requirements

The v2 test suite validates:

- Enum stability  
- Policy defaults  
- Engine logic  
- High‑risk scenarios  
- Extra authentication flow  

Any implementation in Rust, C++, or JS must reproduce identical outputs.

---

## 7. Merge Roadmap (2026)

After all layers reach v2:

- Merge Layers 1–5 into one DigiByte Quantum Shield Network SDK.  
- Provide unified risk API.  
- Add PQC migration hooks.

---

## 8. Conclusion

QWG v2 defines stable wallet‑level protection rules for the entire DigiByte ecosystem.
