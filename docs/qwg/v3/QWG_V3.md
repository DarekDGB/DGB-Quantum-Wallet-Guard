# Quantum Wallet Guard (QWG) — v3.1.0 Foundation Hardening Contract

**Author:** DarekDGB  
**Status:** v3.1.0 foundation-hardening surface is deterministic, auditable, and full-package test-locked  
**Scope of truth:** `qwg` package, with `qwg.v3/*` as the authoritative verdict surface

---

## Purpose

Quantum Wallet Guard is the wallet-side Shield layer that evaluates wallet and transaction risk before a wallet proceeds.

QWG does **not** sign, broadcast, or move funds. It returns explicit, deterministic decisions and v3 verdict envelopes that downstream wallet code can enforce.

---

## v3.1.0 foundation-hardening goals

QWG v3.1.0 foundation hardening preserves the Shield Contract v3 surface while strengthening release discipline, timestamp handling, documentation alignment, and full-package proof gates:

- deterministic context hashing
- immutable v3 verdict envelope
- stable reason identifiers
- explicit allow / deny / escalate semantics
- optional Adaptive Core bridge that cannot affect wallet verdicts
- full-package 100% coverage gate
- no hidden authority
- no silent behavior changes

---

## v3 verdict output

The authoritative v3 wrapper returns `QWGv3Verdict`:

- `schema_version = "v3"`
- `verdict_type = allow | deny | escalate`
- `reason_id = stable machine-readable reason identifier`
- `context_hash = deterministic SHA-256 context hash`
- `reasons = optional extra reason identifiers`

Verdict meaning:

- **allow** — no QWG policy or risk rule was violated
- **deny** — the wallet action must not proceed
- **escalate** — the wallet action requires warning, delay, or extra authentication

---

## Deterministic context hashing

Function:

```python
compute_context_hash(context: dict) -> str
```

Rules:

- input must be a dictionary
- keys are sorted before hashing
- compact JSON separators are used
- no timestamps
- no randomness
- no network calls
- same input always produces the same hash

---

## Verdict adapter

Function:

```python
to_v3_verdict(decision, context_hash) -> QWGv3Verdict
```

Rules:

- adapter is structural only
- no policy evaluation
- no decision logic
- no execution authority
- missing required decision attributes fail fast

---

## Engine wrapper entrypoint

Function:

```python
DecisionEngine.evaluate_transaction_v3(ctx)
```

Responsibilities:

- build deterministic v3 context
- compute context hash
- evaluate existing QWG policy engine
- map internal decisions into v3 verdict semantics
- return an immutable verdict envelope

Non-responsibilities:

- no signing
- no network I/O
- no fund movement
- no autonomous execution

---

## Adaptive Core boundary

Adaptive Core integration is optional and best-effort only.

It may emit threat/event information outward, but it must never:

- change the QWG decision
- change the v3 verdict
- change the context hash
- raise into wallet decision flow
- become an execution authority

---

## CI / test lock

The v3.1.0 foundation-hardening gate covers the full package, not only `qwg.v3`:

```bash
pytest --cov=qwg --cov-report=term-missing --cov-fail-under=100 -q
```

Required state:

- all tests pass
- total package coverage is 100%
- every source module reports 100% coverage
- security-sensitive branches have explicit tests

---

## Current v3.1.0 status

- `pyproject.toml` version: `3.1.0`
- full `qwg` package coverage gate: `100%`
- package typing marker: `src/qwg/py.typed`
- later manifest / verdict / receipt / proof-pack hardening: promoted to the next Shield roadmap phase

---

© 2025 DarekDGB
