# DGB Quantum Wallet Guard 4.0.0 Candidate

![CI](https://github.com/DarekDGB/DGB-Quantum-Wallet-Guard/actions/workflows/ci.yml/badge.svg)
![Coverage 100%](https://img.shields.io/badge/coverage-100%25-brightgreen)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![Status](https://img.shields.io/badge/status-CONTROLLED--PRE--RELEASE-orange)

Author attribution: DarekDGB

Distribution version: `4.0.0`
Candidate tag: `v4.0.0`
Release status: controlled pre-release; not released and not tagged

DGB Quantum Wallet Guard (QWG) is the deterministic wallet-runtime and
transaction-safety evidence component of the DigiByte Quantum Shield. It
evaluates bounded wallet context and emits role-bound component verdict
evidence for the Shield Orchestrator.

## Authority boundary

QWG evidence is not execution authority. QWG does not:

- sign or broadcast DigiByte transactions;
- hold, derive, access, or control wallet private keys;
- change DigiByte consensus;
- approve wallet execution or spending;
- produce the final Shield receipt;
- bypass the Shield Orchestrator; or
- override AdamantineOS.

The Shield Orchestrator verifies QWG evidence and produces the only Shield
receipt AdamantineOS may consume. AdamantineOS remains the final fail-closed
policy and execution boundary. Shield `ALLOW` permits only continuation to
those independent checks.

## Shield v4 component contract

QWG uses these frozen identities:

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

The distribution-version alignment to `4.0.0` does not change these protocol
or schema identities and does not alter the historical v3 compatibility
surface.

## Signature policy and canonical order

`policy.v1` requires strict AND verification of the classical and ML-DSA
paths. Optional FN-DSA evidence may be absent. When present, it must verify and
must be last:

```text
classical-ed25519
ml-dsa
fn-dsa                    optional and last only
```

Profiles are fixed as follows:

```text
classical-ed25519 -> rfc8032-ed25519-v1
ml-dsa            -> fips204-ml-dsa-65-v1
fn-dsa            -> fips206-draft-falcon1024-v1
```

Optional FN-DSA cannot replace or rescue either required path. Present but
invalid optional evidence is fatal. The Falcon-1024 profile is draft evidence,
not final FIPS 206 proof.

## Role and key separation

The trust profile accepts only `shield_component_qwg` keys for QWG component
evidence. Algorithm, standard profile, role, key ID, key version, status, and
validity window are verifier-controlled and bound to the signature input.
Wrong-role, revoked, expired, unknown, downgraded, or mismatched evidence fails
closed.

QWG component signatures cannot be reused as Orchestrator receipt signatures
or transaction signatures because their domains, roles, and payloads differ.

## Real-crypto proof boundary

The backend-neutral adapter supports reviewed provider integrations. The
optional liboqs adapters map:

```text
ml-dsa -> ML-DSA-65
fn-dsa -> Falcon-1024
```

Default CI proves deterministic contracts, test-double behavior, KATs,
negative paths, and 100 percent statement coverage. It does not prove native
liboqs execution. The dedicated `Shield v4 Real OQS ML-DSA and Falcon-1024
Proof` workflow must execute exactly the two guarded native nodes with zero
skips, failures, or errors before a live-liboqs claim is made.

Native tests use test keys. They do not prove production key custody, HSM
assurance, provider hardening, transaction signing, or final FIPS 206
conformance.

## V4 documentation

- Contract: `docs/qwg/v4/CONTRACT.md`
- Manifest and trust profile: `docs/qwg/v4/MANIFEST.md`
- Real-crypto backend: `docs/qwg/v4/REAL_CRYPTO_BACKEND.md`
- Test matrix: `docs/qwg/v4/TEST_MATRIX.md`
- Proof pack: `docs/qwg/v4/PROOF_PACK.md`
- Release status: `docs/qwg/v4/RELEASE_STATUS_v4.0.0.md`

Tests and normative contract documents define truth. A public claim must not
exceed the evidence recorded in the proof pack and release status.

## V3 compatibility and history

The `v3.2.0` release and its documents are historical evidence. The v3
contract version `3`, schema `shield.verdict.v1`, and compatibility constant
`PACKAGE_VERSION = "3.2.0"` remain unchanged. The top-level distribution bump
does not reinterpret or rewrite v3 artifacts.

New controlled integrations should use the v4 evidence surface. Historical v3
evidence must not be accepted where trusted policy requires v4.

## Development

Install test dependencies and run the committed standard gate:

```text
python -m pip install -e ".[test]"
pytest --cov=qwg --cov-report=term-missing --cov-fail-under=100 -q
```

The two native-OQS tests are intentionally skipped in an ordinary local run.
The dedicated workflow enables them and rejects any skip.

## Release governance

`4.0.0` is the aligned distribution candidate and `v4.0.0` is only the
candidate tag name. No release decision has been authorized. Do not create or
move `v4.0.0` until all controlled V4.10 gates are complete and DarekDGB
explicitly authorizes the release action.

## License

MIT License. See `LICENSE` and `THIRD_PARTY_NOTICES.md`.

Copyright 2025 DarekDGB
