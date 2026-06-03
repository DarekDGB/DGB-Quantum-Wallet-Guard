# 🛡️ DGB Quantum Wallet Guard v3.2.0

![CI](https://github.com/DarekDGB/DGB-Quantum-Wallet-Guard/actions/workflows/ci.yml/badge.svg)
![Coverage 100%](https://img.shields.io/badge/coverage-100%25-brightgreen)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/status-ORCHESTRATOR--BOUNDARY--LOCKED-critical)

**Deterministic Wallet Runtime Guard • Transaction / Key Safety Evidence**  
**Architecture & Implementation by @DarekDGB — MIT Licensed**

---

## Purpose

**DGB Quantum Wallet Guard v3.2.0** is the deterministic wallet-runtime safety layer of the **DigiByte Quantum Shield**.

QWG evaluates wallet runtime context, transaction safety context, and quantum/post-quantum risk indicators before wallet execution continues.

QWG may produce evidence for:

- unsafe transaction context
- weak or mismatched wallet runtime posture
- quantum-risk escalation
- unsafe signing-path conditions
- defensive wallet lockdown conditions
- Shield Orchestrator aggregation

QWG does **not**:

- sign transactions
- broadcast transactions
- hold, derive, or access private keys
- modify DigiByte consensus
- approve AdamantineOS execution directly
- override the Shield Orchestrator
- act as final execution authority

QWG is a **wallet safety evidence component**.

---

## Position in the DigiByte Quantum Shield

```text
┌───────────────────────────────────────────────┐
│              AdamantineOS                     │
│   Consumes only Shield Orchestrator receipt   │
└───────────────────────────────────────────────┘
                       ▲
                       │ deterministic receipt only
┌───────────────────────────────────────────────┐
│          Shield Orchestrator v3               │
│   Final Shield aggregation + receipt boundary │
└───────────────────────────────────────────────┘
                       ▲
                       │ component verdict evidence
┌───────────────────────────────────────────────┐
│        Quantum Wallet Guard v3                │
│   Wallet runtime / transaction safety gate    │
└───────────────────────────────────────────────┘
                       ▲
                       │ wallet + tx + risk context
┌───────────────────────────────────────────────┐
│        Wallet Runtime / Signing Flow          │
│   Local context only — no key custody in QWG  │
└───────────────────────────────────────────────┘
```

QWG evaluates wallet safety evidence.

The Shield Orchestrator is the final Shield receipt boundary for AdamantineOS handoff.

---

## Core Mission

### Deterministic Wallet Safety Evaluation

QWG converts validated wallet runtime and transaction safety context into deterministic verdict evidence.

Same valid input must always produce the same output.

### Fail-Closed by Default

QWG must reject unsafe input conditions, including:

- malformed wallet context
- malformed transaction context
- unsupported contract versions
- unknown strict fields
- duplicate or conflicting authority claims
- unsafe numeric values
- oversized payloads
- unserialisable data
- ambiguity affecting authority or auditability

### Evidence Only

QWG output is not final execution authority.

QWG verdict data must be treated as component evidence for Shield orchestration.

Raw QWG output must not be consumed by AdamantineOS as final signing, execution, or approval authority.

---

## v3.2.0 Manifest / Verdict Lock

QWG v3.2.0 includes the Shield manifest / registry / canonical verdict lock required before AdamantineOS integration.

The v3.2.0 lock enforces:

- component identity discipline
- contract version discipline
- stable reason ID registration
- stable evidence-family registration
- deterministic canonical verdict data
- fail-closed rejection of malformed verdict inputs
- Orchestrator-first handoff assumptions

QWG remains evidence-only.

It cannot:

- sign
- broadcast
- hold keys
- expand authority
- override the Shield Orchestrator
- approve AdamantineOS execution directly

See:

- `docs/v3/MANIFEST.md`
- `docs/v3/REASON_IDS.md`
- `docs/v3/EVIDENCE_FAMILIES.md`
- `docs/v3/TEST_MATRIX.md`
- `docs/v3/PROOF_PACK.md`

---

## Repository Layout

```text
DGB-Quantum-Wallet-Guard/
├─ README.md
├─ LICENSE
├─ CHANGELOG.md
├─ SECURITY.md
├─ docs/
│  └─ v3/
│     ├─ EVIDENCE_FAMILIES.md
│     ├─ MANIFEST.md
│     ├─ PROOF_PACK.md
│     ├─ REASON_IDS.md
│     └─ TEST_MATRIX.md
├─ tests/
│  └─ test_v3_2_manifest_verdict_lock.py
└─ src/
   └─ qwg/
      └─ contracts/
         ├─ __init__.py
         └─ v3_2_lock.py
```

---

## Tests & Security Guarantees

Security and regression tests enforce:

- deterministic wallet-safety behavior
- fail-closed behavior
- strict manifest discipline
- stable reason IDs
- stable evidence families
- canonical verdict lock behavior
- no hidden authority
- no silent fallback
- no key custody
- no Orchestrator bypass assumption

Tests define truth.

No release is locked unless CI proves the contract surface.

---

## v3.2.0 Status

QWG is aligned with the Shield v3.2.0 integration-boundary track:

- package metadata set to `3.2.0`
- manifest / reason ID / evidence-family docs are present
- v3.2.0 verdict lock tests are present
- deterministic contract behavior is preserved
- no consensus authority is added
- no signing, broadcasting, key custody, or hidden execution authority is added
- AdamantineOS must consume Shield through the Orchestrator receipt only

Do **not** tag v3.2.0 until the final roadmap checklist, fresh ZIP audit, CI proof, and Red Team report are complete.

---

## Shield v3 Invariants

QWG follows the Shield v3 baseline invariants:

- **Deny-by-default** — anything not explicitly allowed is rejected.
- **Fail-closed** — invalid, ambiguous, partial, or unsafe input is rejected.
- **Deterministic execution** — same valid input must produce the same output.
- **No silent fallback** — failures must surface as explicit reasoned rejections.
- **No key custody** — QWG never holds, derives, signs with, or accesses private keys.
- **Evidence-only output** — QWG evidence does not approve execution.
- **Orchestrator-first handoff** — AdamantineOS receives Shield state only through the deterministic Orchestrator receipt.

Any violation of these invariants is a security defect.

---

## Documentation

- Manifest: `docs/v3/MANIFEST.md`
- Reason IDs: `docs/v3/REASON_IDS.md`
- Evidence Families: `docs/v3/EVIDENCE_FAMILIES.md`
- Test Matrix: `docs/v3/TEST_MATRIX.md`
- Proof Pack: `docs/v3/PROOF_PACK.md`

---

## Contribution Policy

Rules:

- No consensus-touching behavior.
- No signing or broadcasting behavior.
- No private-key custody behavior.
- No AdamantineOS direct execution approval.
- Deterministic wallet-safety evidence only.
- Tests required for contract changes.
- No bypass of the Shield Orchestrator receipt boundary.

---

## License

MIT License  
© 2025 **DarekDGB**
