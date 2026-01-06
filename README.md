# 🔐 DGB Quantum Wallet Guard (QWG)

[![CI](https://github.com/DarekDGB/DGB-Quantum-Wallet-Guard/actions/workflows/ci.yml/badge.svg)](https://github.com/DarekDGB/DGB-Quantum-Wallet-Guard/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![Status](https://img.shields.io/badge/status-QWG%20v3%20complete-success.svg)](#)

**Author:** DarekDGB  
**License:** MIT  
**Status:** QWG v3 complete — glass-box, deterministic, test-enforced

---

## Overview

**Quantum Wallet Guard (QWG)** is a **deterministic, policy-driven wallet defense layer** designed to protect cryptocurrency wallets from high-risk transactions, abnormal behavior, and hostile operating conditions.

QWG is built with a strict **glass-box security philosophy**:

> Every decision is explicit, deterministic, auditable, and enforced by tests.  
> No opaque models. No hidden authority. No silent behavior changes.

---

## What QWG Is (and Is Not)

### QWG **is**
- A wallet-side **decision engine**
- A **policy-enforcing defense layer**
- Deterministic and explainable by construction
- Safe to audit, reason about, and integrate

### QWG **is not**
- An autonomous AI
- A black-box risk scorer
- A signing or execution authority
- A system that can move funds

QWG never signs transactions and never executes transfers.  
It only **evaluates risk and returns explicit verdicts**.

---

## QWG v3 — Glass-Box Contract

QWG v3 introduces a **strict, test-backed contract** without changing the underlying decision logic.

### Core guarantees
- **Deterministic context hashing** (`context_hash`)
- **Explicit reason identifiers** (`reason_id`)
- **Immutable verdict objects**
- **No authority creep**
- **Fail-closed behavior**

All guarantees are enforced by unit tests and CI.

---

## v3 Verdict Output

QWG v3 returns an immutable verdict envelope:

- `schema_version = "v3"`
- `verdict_type`: `allow | deny | escalate`
- `reason_id`: stable machine-readable identifier
- `context_hash`: deterministic SHA-256 hash
- `reasons` (optional): additional reason IDs

### Verdict semantics
- **allow** → execution may proceed (subject to higher-level wallet gates)
- **deny** → execution must not proceed
- **escalate** → execution must pause for warnings, delays, or extra authentication

---

## Determinism & Auditability

QWG v3 uses a **pure hashing function** to anchor decisions:

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

## Documentation

- **QWG v3 (authoritative):** `docs/qwg/v3/QWG_V3.md`
- **QWG v2 (legacy reference):** `docs/qwg/v2/`
- **Docs index:** `docs/qwg/README.md`

> Only v3 documentation reflects current security guarantees.

---

## Testing & CI

This repository includes:
- decision-path tests (allow / deny / escalate)
- reason_id stability tests
- immutability invariants
- determinism invariants
- packaging import smoke test
- CI enforcing editable install via `pyproject.toml`

If tests fail, glass-box guarantees are considered broken.

---

## Security

Please see **`SECURITY.md`** for responsible vulnerability disclosure guidelines.

---

## License

MIT License © DarekDGB
