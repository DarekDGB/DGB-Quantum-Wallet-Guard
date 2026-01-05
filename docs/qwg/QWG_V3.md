# Quantum Wallet Guard (QWG) Docs — v3 (Glass-Box)

**Author:** DarekDGB  
**License:** MIT

This page documents the **QWG v3 interface contract** and how it stays **glass-box** (auditable and deterministic) while preserving the existing engine behavior.

> v3 is currently implemented as a **wrapper layer** around the existing engine logic:
> - no policy logic changes
> - no refactors required
> - strong invariants enforced by tests

---

## v3 goals

QWG v3 is designed to ensure:
- **Deterministic** decision anchoring via `context_hash`
- **Explainable** outcomes via stable `reason_id`
- **Immutable** verdict objects (no mutation after creation)
- No “black box” behavior: no hidden authority, no silent adaptation

---

## v3 outputs: QWGv3Verdict

QWG v3 returns an immutable verdict envelope:

- `schema_version`: must be `"v3"`
- `verdict_type`: `allow | deny | escalate`
- `reason_id`: stable machine-readable string identifier
- `context_hash`: deterministic SHA-256 hex digest of a stable context dict
- `reasons` (optional): additional reason IDs

### VerdictType meaning
- **allow**: execution may proceed (subject to the wallet’s higher-level gates)
- **deny**: execution must not proceed
- **escalate**: execution must not proceed until additional requirements are satisfied
  (e.g., warn/delay/extra-auth)

---

## v3 determinism: compute_context_hash(context)

QWG v3 uses a pure function that:
- accepts a **JSON-serializable dict**
- sorts keys deterministically
- uses SHA-256
- has no timestamps, randomness, or external calls

This hash anchors:
- audit trails
- regression tests
- cross-layer correlation (later)

---

## v3 adapter: to_v3_verdict(decision, context_hash)

QWG v3 wraps an existing decision-like object:
- requires `outcome` (string: `allow|deny|escalate`)
- requires `reason_id` (string)
- optionally uses `reasons` (list of strings)

Hard guarantees:
- missing required fields raise immediately (no silent “unknown”)
- no mutation (verdict is frozen/immutable)

---

## v3 wrapper entrypoint: DecisionEngine.evaluate_transaction_v3(ctx)

The v3 wrapper:
1. builds a deterministic context dict from `RiskContext` (stable keys only)
2. computes `context_hash`
3. calls the existing `evaluate_transaction(ctx)` (unchanged logic)
4. maps the result to:
   - `verdict_type`
   - stable `reason_id`
5. returns `QWGv3Verdict`

This ensures **glass-box outputs** without changing the v0.4 decision rules.

---

## Tests (proof)

QWG v3 is enforced by tests:
- verdict immutability invariant
- context_hash determinism and order independence
- wrapper returns v3 envelope with stable reason IDs

If tests fail, v3 guarantees are considered broken.

---

## Integration guidance (high-level)

- Use `evaluate_transaction_v3(ctx)` for v3 output surfaces.
- Treat `reason_id` + `context_hash` as the primary audit keys.
- Keep any future “learning” systems **non-authoritative**:
  they may observe and suggest, but must not execute or override.
