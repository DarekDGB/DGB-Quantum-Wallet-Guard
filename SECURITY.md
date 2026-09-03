# Security Policy - DGB Quantum Wallet Guard

Repository: `DGB-Quantum-Wallet-Guard`
Component: QWG
Maintainer: DarekDGB
License: MIT

## Supported surfaces

| Surface | Status |
|---|---|
| Distribution `4.0.0` / candidate `v4.0.0` | Controlled pre-release; security-maintained; not released or tagged |
| Shield v3.2.0 compatibility surface | Historical release; compatibility-maintained |
| Older archived behavior | Unsupported unless an issue affects a maintained surface |

The distribution-version alignment does not change frozen v3 or v4 protocol
and schema identities. Historical material is non-authoritative for new v4
security claims.

## Security model

QWG is a deterministic, fail-closed wallet-safety evidence component. It
validates bounded wallet and transaction context and emits role-bound evidence
for the Shield Orchestrator.

QWG does not:

- alter DigiByte consensus;
- sign or broadcast transactions;
- hold, derive, or access wallet private keys;
- approve spending or execution;
- create the final Shield receipt;
- bypass the Shield Orchestrator; or
- override AdamantineOS.

AdamantineOS remains the final fail-closed policy and execution boundary.
Shield `ALLOW` is evidence that may continue to independent downstream checks,
not execution authority.

## Frozen v4 identities

The maintained v4 surface uses:

```text
component_id: qwg
component_role: shield_component_qwg
contract_version: 4
schema_version: shield.verdict.v2
canonicalization_profile: shield-v4-canon.v1
signature_policy: policy.v1
signature_bundle_schema: shield.signature_bundle.v1
key_registry_schema: shield.key_registry.v1
```

Distribution version `4.0.0` is not a protocol identifier.

## Required and optional algorithms

`policy.v1` requires both paths in this order:

```text
classical-ed25519
ml-dsa
```

Optional `fn-dsa` may appear only last under
`fips206-draft-falcon1024-v1`. It may be absent. If present, it must verify
and cannot replace or rescue a missing or failed required path. The Falcon-1024
profile is draft evidence, not final FIPS 206 proof.

A verifier must reject reordered, duplicated, unknown, wrong-profile,
wrong-role, revoked, expired, mismatched, or downgraded evidence before any
authority inference.

## Role and key separation

QWG evidence uses only role `shield_component_qwg`. Trust entries bind role,
algorithm, profile, key ID, key version, validity window, status, and public
key. QWG component evidence cannot be reused as Orchestrator receipt evidence
or transaction-signing authority.

Private signing material belongs outside QWG's evidence-verification boundary.
The repository's deterministic signature material is TEST-ONLY.

## Real-backend evidence

The backend-neutral adapter and optional liboqs adapters preserve fail-closed
behavior. There is no silent fallback from a selected real backend to
TEST-ONLY signatures.

Standard CI proves interface behavior, KATs, negative paths, and 100 percent
statement coverage. The dedicated real-OQS workflow proves the exact native
ML-DSA-65 and Falcon-1024 test nodes with a no-skip JUnit guard. Neither proof
establishes production key custody, HSM assurance, provider hardening,
transaction signing, or final FIPS 206 conformance.

## Required negative behavior

The v4 surface must reject:

- missing or invalid required signatures;
- reordered, duplicated, unsupported, or unknown algorithms;
- optional evidence placed before or between required paths;
- required-path rescue attempts;
- role, key, profile, domain, context, payload-hash, or policy mismatch;
- revoked, expired, not-yet-valid, or unknown trust entries;
- malformed canonical payloads or binary material;
- native backend exceptions or non-boolean verifier results;
- deterministic TEST-ONLY material at a real-backend boundary; and
- forbidden transaction, broadcast, consensus, custody, bypass, or final-
  authority metadata.

Tests and normative contract documents define truth.

## Reporting a vulnerability

Do not disclose a suspected security issue publicly first. Use a private GitHub
security advisory when available, or contact `@DarekDGB`.

Include the affected commit or tag, reproduction steps, expected and actual
behavior, security impact, and whether the issue affects v3 compatibility, v4
evidence, or both.

## Release governance

Distribution `4.0.0` is a controlled candidate. No `v4.0.0` tag may be
created or moved before all V4.10 gates and explicit DarekDGB authorization.
Green CI and aligned metadata do not themselves authorize a release.

## Final security rule

Reject any change that weakens determinism, fail-closed behavior, canonical
bundle order, required signature policy, QWG role separation, no-key-custody
behavior, or the evidence-only authority boundary.

Copyright 2025 DarekDGB
