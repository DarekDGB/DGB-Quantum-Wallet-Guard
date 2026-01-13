# Quantum Wallet Guard (QWG) — v3 (Glass-Box Contract)

**Author:** DarekDGB  
**Status:** v3 contract surface is deterministic + test-locked  
**Scope of truth:** `qwg.v3/*`

---

## v3 goals

QWG v3 provides a **glass-box**, **deterministic**, **auditable** output surface.

It guarantees:
- same inputs → same outputs
- stable reason identifiers
- canonical, reproducible context hashing
- zero hidden authority

---

## v3 outputs: QWGv3Verdict

The v3 surface returns a stable structure:

- `verdict_type` (ALLOW / WARN / DENY)
- `reason_id` (stable, regression-locked)
- `context_hash` (canonical hash of request context)

Verdict meaning:
- **ALLOW** – safe to proceed
- **WARN** – elevated risk
- **DENY** – execution must not proceed

---

## Deterministic hashing

Function:
```
compute_context_hash(context: dict) -> str
```

Rules:
- deterministic
- no timestamps
- no randomness
- canonical serialization
- fail-fast on invalid input types

---

## Verdict adapter

Function:
```
to_v3_verdict(decision, context_hash) -> QWGv3Verdict
```

Rules:
- explicit mapping
- no side effects
- no authority escalation

---

## Engine wrapper entrypoint

Function:
```
DecisionEngine.evaluate_transaction_v3(ctx)
```

Responsibilities:
- evaluate legacy engine behavior
- compute deterministic context_hash
- return v3 verdict

Non-responsibilities:
- no signing
- no network I/O
- no state mutation

---

## Adaptive Core boundary

Adaptive Core integration:
- is optional
- is a side-effect only
- must not influence verdict or context_hash

The v3 verdict is authoritative.

---

## Tests

CI enforces coverage on the v3 surface:

```
pytest --cov=qwg.v3 --cov-report=term-missing --cov-fail-under=90 -q
```

Current state:
- `qwg.v3.context_hash`: 100%
- `qwg.v3.verdict`: 100%

---
© 2025 DarekDGB
