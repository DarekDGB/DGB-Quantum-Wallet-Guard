# Quantum Wallet Guard (QWG) Docs — v2

**Author:** DarekDGB  
**License:** MIT

This page documents the **v2-era** QWG concepts and interfaces as they existed before the v3 “glass-box” wrapper work.

> **Important:** QWG v2 docs are kept for historical/reference purposes.  
> QWG v3 is the current direction and should be used for new integrations.

---

## What “v2” means here

In the QWG repo, “v2” refers to:
- v2-era **naming** and **event semantics** (e.g., “Adaptive Core v2” wording)
- Risk context descriptions referencing **Sentinel/DQSN/ADN v2**
- Adaptive event payloads that include human-readable fields like `description`

This does **not** mean the engine is opaque — it means the documentation and event semantics were not yet upgraded to the **v3 glass-box contract**.

---

## Core components (v2)

### 1) RiskContext
A snapshot of wallet + environment signals used for evaluating a transaction:
- Sentinel signal (risk level)
- DQSN network score
- ADN node-local risk level
- Wallet balance / tx amount
- Device trust & behavior score

### 2) DecisionEngine
Evaluates a `RiskContext` against a `WalletPolicy` and produces a `DecisionResult`:
- `ALLOW`
- `WARN`
- `DELAY`
- `REQUIRE_EXTRA_AUTH`
- `BLOCK`

### 3) Adaptive Bridge (v2 semantics)
When QWG blocks/delays/warns, it may emit an AdaptiveEvent (best-effort) that includes:
- a high-level `threat_type`
- a human-readable `description`
- supporting context fields

---

## Status

- This doc is **frozen**.
- New work should reference: **QWG v3 Docs**.
