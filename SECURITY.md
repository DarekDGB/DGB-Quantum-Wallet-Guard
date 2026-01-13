# 🔐 Security Policy — Quantum Wallet Guard (QWG)

**Repository:** DGB-Quantum-Wallet-Guard  
**Maintainer:** DarekDGB  
**License:** MIT

---

## Security model

QWG is a **local wallet defense layer** that produces **deterministic, auditable verdicts**.

It does NOT:
- modify blockchain consensus
- sign transactions
- broadcast network messages

All effects are local.

---

## Contract surface

Authoritative v3 surface:
- `qwg.v3.context_hash`
- `qwg.v3.verdict`

These modules must remain:
- deterministic
- side-effect free
- coverage-gated

---

## Non-negotiable invariants

1. Determinism (same inputs → same outputs)
2. No hidden authority
3. Stable reason identifiers
4. Fail-fast on invalid input
5. Optional integrations must not affect verdicts

---

## Testing & CI

CI enforces:

```
pytest --cov=qwg.v3 --cov-fail-under=90 -q
```

Security-sensitive changes require tests.

---

## Vulnerability reporting

- Prefer GitHub Security Advisories
- Or contact **@DarekDGB** on GitHub

Please include reproduction steps and impact assessment.

---

## Out of scope

- DigiByte consensus vulnerabilities
- mining or protocol attacks
- unrelated UI issues

---

## Disclaimer

Software is provided **as-is**, without warranty.

---
© 2025 DarekDGB
