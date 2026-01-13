# 🔐 DGB Quantum Wallet Guard (QWG)

[![CI](https://github.com/DarekDGB/DGB-Quantum-Wallet-Guard/actions/workflows/ci.yml/badge.svg)](https://github.com/DarekDGB/DGB-Quantum-Wallet-Guard/actions)
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![Status](https://img.shields.io/badge/status-QWG%20v3%20locked-success.svg)](#)

**Author:** DarekDGB  
**License:** MIT  
**Status:** QWG v3 complete — glass-box, deterministic, test-locked

---

## Overview

**Quantum Wallet Guard (QWG)** is a **deterministic, policy-driven wallet defense layer** designed to protect cryptocurrency wallets from high-risk transactions, abnormal behavior, and hostile runtime conditions.

QWG follows a strict **glass-box security philosophy**:

> Every decision is explicit, deterministic, auditable, and enforced by tests.  
> No opaque models. No hidden authority. No silent behavior changes.

---

## What QWG Is (and Is Not)

### QWG **is**
- A wallet-side **decision and enforcement policy engine**
- Deterministic and explainable by construction
- Safe to audit, reason about, and integrate with higher layers
- Designed for long-term security stability

### QWG **is not**
- An autonomous AI
- A black-box risk scorer
- A signing or execution authority
- A component that can move funds

QWG **never signs transactions** and **never executes transfers**.  
It only evaluates risk and returns **explicit verdicts**.

---

## QWG v3 — Glass-Box Contract

QWG v3 introduces a **strict, test-backed contract surface** without changing the underlying decision behavior.

### Core guarantees
- Deterministic `context_hash`
- Stable `reason_id` identifiers
- Immutable verdict objects
- No authority creep
- Fail-closed semantics

All guarantees are enforced by CI with **100% coverage on the v3 surface**.

---

## Architecture Position

```
┌──────────────────────────────┐
│        Wallet Runtime        │
│  (UI / UX / User Approval)   │
└──────────────▲───────────────┘
               │ verdict
┌──────────────┴───────────────┐
│        QWG v3 Contract       │
│  Deterministic verdict gate  │
│  (ALLOW / DENY / ESCALATE)   │
└──────────────▲───────────────┘
               │ risk context
┌──────────────┴───────────────┐
│     Legacy Decision Engine   │
│   (policies, scoring, rules) │
└──────────────────────────────┘
```

QWG v3 is the **authoritative verdict surface**.  
Legacy logic may evolve, but **must not violate the v3 contract**.

---

## v3 Verdict Output

QWG v3 returns an immutable verdict envelope:

- `schema_version = "v3"`
- `verdict_type`: `allow | deny | escalate`
- `reason_id`: stable machine-readable identifier
- `context_hash`: deterministic SHA-256 hash
- `reasons` (optional): additional reason identifiers

### Verdict semantics
- **allow** → execution may proceed (subject to wallet rules)
- **deny** → execution must not proceed
- **escalate** → execution pauses for warnings, delays, or extra authentication

---

## Determinism & Auditability

QWG v3 anchors decisions using a **pure hashing function**:

- JSON-serializable input
- Sorted keys
- No timestamps
- No randomness
- No network calls

This guarantees:
- reproducible outcomes
- reliable regression testing
- clean audit trails

---

## Repository Layout

```
src/qwg/
├─ v3/                    # authoritative contract surface
│  ├─ context_hash.py
│  └─ verdict.py
├─ engine.py              # legacy decision logic
├─ adapters.py            # v3 adapters
└─ ...                    # internal helpers
```

Only `qwg.v3` is coverage-gated and contract-locked.

---

## Documentation

- **QWG v3 (authoritative):** `docs/qwg/v3/QWG_V3.md`
- **QWG v2 (legacy reference):** `docs/qwg/v2/`
- **Docs index:** `docs/qwg/README.md`
- **Security policy:** `SECURITY.md`

---

## Testing & CI

This repository enforces:
- deterministic behavior tests
- reason_id stability
- immutability invariants
- type safety & fail-fast guards
- **100% coverage on `qwg.v3`**

If CI fails, the security contract is considered broken.

---

## Security

See **`SECURITY.md`** for vulnerability disclosure and security guarantees.

---

## License

MIT License © 2026 **DarekDGB**
