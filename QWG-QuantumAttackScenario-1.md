# 🛡 Quantum Wallet Guard — Quantum-Style Attack Scenario Report  
### Scenario ID: QWG-SIM-001 — Dormant Key Sweep

Status: **Simulation-only, no mainnet impact**  
Layer: **5 — Quantum-Style Behavioural Wallet Analysis**

---

## 1. Scenario Overview

**Goal:**  
Validate that **Quantum Wallet Guard (QWG)** can detect a *quantum-style key sweep* pattern:

- many long-dormant UTXOs  
- from multiple wallets  
- moved within a short time window  
- consolidated into a few aggregation addresses  

This scenario runs entirely in **simulation mode**.  
No real keys, UTXOs, or RPC connections are required.

---

## 2. Threat Model

We model a future attacker with the ability to:

- derive private keys from exposed public keys (e.g. via quantum or hybrid side-channel),  
- sweep funds from old addresses whose public keys have been on-chain for years,  
- coordinate multiple sweeps into a small set of receiving addresses.

Key characteristics of such an attack:

- sudden activation of long-dormant wallets,  
- large UTXO counts per transaction,  
- strong destination clustering,  
- behaviour totally unlike normal user flows.

QWG does **not** replace post-quantum signatures.  
It acts as a **behavioural early-warning system** for quantum-assisted theft.

---

## 3. Scenario Setup

### 3.1 Wallet Set

We simulate three logical wallets:

- **Wallet A** — 30 UTXOs, last activity > 5 years ago  
- **Wallet B** — 20 UTXOs, last activity > 3 years ago  
- **Wallet C** — 10 UTXOs, last activity > 2 years ago  

All have:

- long-exposed public keys on-chain,  
- no activity in the last 12 months,  
- non-dust balances.

### 3.2 Time Window

We simulate a **30-minute window** during which almost all UTXOs from A, B, C are swept and consolidated into two aggregation addresses:

- **X1**, **X2**

---

## 4. Event Timeline

| Step | Time (t) | Source Wallet | UTXOs Moved | Total Value (DGB) | Destination |
|------|----------|--------------|-------------|-------------------|-------------|
| 1 | t = 0 min   | A            | 10          | 12,000            | X1          |
| 2 | t = 5 min   | B            | 8           | 9,500             | X1          |
| 3 | t = 9 min   | C            | 5           | 4,200             | X2          |
| 4 | t = 14 min  | A            | 10          | 11,700            | X1          |
| 5 | t = 20 min  | B            | 7           | 8,900             | X2          |
| 6 | t = 27 min  | C            | 5           | 4,000             | X1          |

Pattern:

- high time clustering (all events within 30 minutes),  
- high destination clustering (only X1 and X2),  
- all sources previously dormant for years,  
- high aggregate value.

---

## 5. QWG Analysis Flow

QWG receives each transaction as a **behavioural event** and computes features.

### 5.1 Input Features

For each event QWG derives metrics such as:

- `address_age` — time since last activity,  
- `key_exposure_age` — time since public key first appeared on-chain,  
- `utxo_count_moved`,  
- `value_dgb`,  
- `rolling_window_value` (e.g. 30 minutes),  
- `destination_concentration` (entropy of receiving addresses),  
- `profile_deviation` (distance from historical behaviour of the source wallet).

These are passed into the QWG **risk engine**.

### 5.2 Internal Scores

QWG tracks three key components:

1. **Dormancy Shock Score (DSS)**  
   - high when dormant / old keys suddenly move meaningful value.

2. **Sweep Pattern Score (SPS)**  
   - high when many UTXOs from related wallets are moved within a short time window,  
   - extra weight for strong destination clustering.

3. **Profile Deviation Score (PDS)**  
   - high when the behaviour is unlike any previous profile for that wallet.

A combined **Quantum-Style Risk Score (QRS)** is computed (0–100):

```text
QRS = w1 * DSS + w2 * SPS + w3 * PDS
```

Weights are configurable in `src/qwg/policies.py` or `risk_context.py`.

---

## 6. Detection Behaviour

### 6.1 Early Phase (Steps 1–3)

After the first three sweeps:

- three long-dormant wallets were activated,  
- large UTXO bundles moved,  
- destinations X1, X2 dominate.

Example intermediate scores:

| After Step | DSS | SPS | PDS | QRS (0–100) | QWG Risk Level |
|------------|-----|-----|-----|-------------|----------------|
| 1          | 70  | 40  | 90  | 80          | MEDIUM         |
| 2          | 80  | 65  | 95  | 88          | HIGH           |
| 3          | 85  | 75  | 95  | 92          | CRITICAL       |

At this point QWG flags:

```text
pattern = "DORMANT_KEY_SWEEP"
risk_level = CRITICAL
```

and emits an alert.

Example log line:

```text
[QWG][ALERT] pattern="DORMANT_KEY_SWEEP" wallets=[A,B,C] dests=[X1,X2] qrs=92 level=CRITICAL
```

### 6.2 Escalation to ADN v2 & Wallet Guardian v2

QWG sends a structured event to:

- **ADN v2** — to raise chain / node risk,  
- **Wallet Guardian v2** — so any further spending attempts from the affected keys can be frozen or rejected.

Example JSON payload:

```json
{
  "event_type": "DORMANT_KEY_SWEEP",
  "risk_level": "CRITICAL",
  "qrs_score": 92,
  "source_wallets": ["A", "B", "C"],
  "destinations": ["X1", "X2"],
  "time_window_minutes": 30,
  "total_value_dgb": 50500
}
```

ADN v2 can propagate this to the rest of the shield.  
Wallet Guardian v2 can enforce freezes for addresses / wallets related to A, B, C.

### 6.3 Late Phase (Steps 4–6)

During later sweeps:

- QRS remains near maximum,  
- QWG continues to log each extension of the attack,  
- the pattern footprint grows for later analysis.

Example log:

```text
[QWG][PERSIST] pattern="DORMANT_KEY_SWEEP" wallets=[A,B,C] additional_utxos=22 added_value=24600 qrs=97
```

All events are exported to the Adaptive Core for replay and training.

---

## 7. Outcome Summary

In scenario **QWG-SIM-001**, Quantum Wallet Guard:

1. Detected sudden activation of long-dormant wallets with old exposed keys.  
2. Recognised coordinated multi-wallet UTXO sweeps into a small set of destinations.  
3. Raised **Quantum-Style Risk Score (QRS)** to CRITICAL early in the sequence.  
4. Emitted alerts to **ADN v2** and **Wallet Guardian v2** for protective action.  
5. Exported pattern details suitable for Adaptive Core learning and future pattern matching.

This validates that QWG can serve as a **behavioural early-warning layer** for quantum-style attacks, even before any on-chain PQC upgrade.

---

## 8. Testnet Integration Notes

When integrated into DigiByte testnet:

- QWG should subscribe to a transaction / UTXO event feed,  
- the configuration for QRS thresholds must be tuned to chain statistics,  
- alerts from QWG should be wired into:

  - ADN v2 (risk escalation),  
  - Wallet Guardian v2 (freeze / reject),  
  - Adaptive Core (learning stream).

This scenario QWG-SIM-001 can be replayed using either:

- synthetic events in unit / integration tests (see `tests/`),  
- or a dedicated simulation script that feeds mock transactions into `src/qwg/engine.py`.

It is the **canonical v1 quantum-style attack scenario** for QWG v2.
