# 🛡 Quantum Wallet Guard — Historical Quantum-Style Attack Scenario

### Scenario ID: QWG-SIM-001 — Dormant Key Sweep

Author: **DarekDGB**
Status: **Historical design scenario; executable prototype retired**
Layer: **5 — Conceptual behavioural wallet analysis**

> **Control notice:** This v2 document is historical and non-authoritative.
> The executable QWG-SIM-001 dormant-sweep prototype is formally retired and
> is not part of the current API. Neither this document nor QWG grants wallet
> action, execution, signing, broadcast or DigiByte consensus authority.

---

## 1. Scenario Overview

**Purpose:**
Document a hypothetical quantum-style key-sweep pattern for threat modelling:

- many long-dormant UTXOs
- controlled through multiple wallets
- moved within a short time window
- consolidated into a few aggregation addresses

This scenario is documentation only. It does not run against the current QWG
implementation, and it is not evidence that QWG detects this pattern. No real
keys, UTXOs or RPC connections are involved.

---

## 2. Threat Model

The historical design models a future attacker who might be able to:

- derive private keys from exposed public keys through a future cryptographic
  break or another compromise
- sweep funds from old addresses whose public keys have been on-chain for years
- coordinate several transfers into a small set of receiving addresses

Potential indicators include:

- sudden activation of long-dormant wallets
- large UTXO counts per transaction
- strong destination clustering
- behaviour unlike the affected wallets' established history

Behavioural analysis cannot prove that a quantum attack occurred and does not
replace post-quantum cryptography.

---

## 3. Scenario Setup

### 3.1 Wallet Set

The conceptual dataset uses three logical wallets:

- **Wallet A** — 30 UTXOs, last activity more than five years ago
- **Wallet B** — 20 UTXOs, last activity more than three years ago
- **Wallet C** — 10 UTXOs, last activity more than two years ago

The scenario assumes long-exposed public keys, no activity in the previous
twelve months, and non-dust balances. These assumptions are synthetic and are
not loaded by any current runtime.

### 3.2 Time Window

The design places six hypothetical transfers in a 30-minute window and uses two
aggregation addresses, **X1** and **X2**.

---

## 4. Event Timeline

| Step | Time | Source wallet | UTXOs moved | Total value (DGB) | Destination |
|---:|---:|---|---:|---:|---|
| 1 | 0 min | A | 10 | 12,000 | X1 |
| 2 | 5 min | B | 8 | 9,500 | X1 |
| 3 | 9 min | C | 5 | 4,200 | X2 |
| 4 | 14 min | A | 10 | 11,700 | X1 |
| 5 | 20 min | B | 7 | 8,900 | X2 |
| 6 | 27 min | C | 5 | 4,000 | X1 |

The threat-modelling pattern combines time clustering, destination clustering,
dormant sources and high aggregate value. The table is a design fixture in
this document only.

---

## 5. Historical Analytics Proposal

The retired design proposed deriving features such as:

- time since an address last moved funds
- time since a public key first appeared on-chain
- UTXO count and transferred value
- rolling-window value
- receiving-address concentration
- deviation from historical wallet behaviour

It also proposed three illustrative components:

1. **Dormancy Shock Score (DSS)** — dormant or old keys moving meaningful
   value.
2. **Sweep Pattern Score (SPS)** — related wallets moving many UTXOs in a
   short window toward clustered destinations.
3. **Profile Deviation Score (PDS)** — behaviour differing from the source
   wallet's history.

The historical document represented a proposed combined score as:

```text
QRS = w1 * DSS + w2 * SPS + w3 * PDS
```

The current QWG engine does not implement these features, component scores,
weights or multi-wallet aggregation. They must not be treated as an API or a
tested scoring contract.

---

## 6. Illustrative Desired Behaviour

The values below are retained only to explain the original design intent. They
were not produced by the current QWG runtime and are not test evidence.

| After step | DSS | SPS | PDS | Illustrative QRS | Illustrative level |
|---:|---:|---:|---:|---:|---|
| 1 | 70 | 40 | 90 | 80 | MEDIUM |
| 2 | 80 | 65 | 95 | 88 | HIGH |
| 3 | 85 | 75 | 95 | 92 | CRITICAL |

The original design also used example alert text and a payload containing the
wallets, destinations, time window and total value. Those examples describe a
possible future evidence format only. They do not demonstrate that an alert
was emitted, that another component received it, or that any wallet or node
action occurred.

Any future consumer would remain responsible for independently validating the
evidence and applying its own fail-closed policy. A label or score alone cannot
freeze funds, reject a transaction, sign, broadcast or alter consensus.

---

## 7. Outcome Status

QWG-SIM-001 did not validate dormant-key-sweep detection. Its executable
prototype and associated test depended on a runtime contract that is not part
of the current implementation, so both are formally retired.

The document preserves only these threat-modelling requirements for possible
future work:

1. distinguish dormant-source activation from ordinary wallet activity
2. evaluate coordinated timing and destination concentration
3. explain every derived feature and threshold
4. separate evidence generation from wallet or node authority
5. prove behaviour with implemented tests before making capability claims

---

## 8. Future Implementation Gate

Before this scenario could become executable evidence, a future controlled
change would need to provide and verify:

- an explicit event and state model
- deterministic feature and scoring definitions
- validation and fail-closed error handling
- unit, integration and adversarial tests
- documented false-positive and false-negative limits
- clear separation from signing, broadcasting, consensus and final wallet
  action authority

Until that gate is completed, QWG-SIM-001 remains a historical,
non-authoritative threat-analysis document only.

