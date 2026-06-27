# QWG Shield v4 Manifest

Author attribution: DarekDGB

## Component

```text
name: DGB Quantum Wallet Guard
component_id: qwg
component_role: shield_component_qwg
contract_version: 4
schema_version: shield.verdict.v2
```

## Purpose

QWG Shield v4 emits cryptographically verifiable component verdict evidence for the Shield Orchestrator.

QWG remains an evidence producer, not a transaction signer, broadcaster, consensus layer, wallet custody layer, or AdamantineOS override layer.

## Frozen Profiles

```text
canonicalization_profile: shield-v4-canon.v1
signature_policy: policy.v1
signature_bundle_schema: shield.signature_bundle.v1
key_registry_schema: shield.key_registry.v1
```

## Required Signature Paths

```text
classical-ed25519
ml-dsa
```

Both required paths must verify for policy.v1.

V4.8E adds a real OQS-backed adapter for the `ml-dsa` path only. It does not weaken the requirement for `classical-ed25519`.

## Optional Signature Path

```text
fn-dsa
```

FN-DSA may provide additional evidence, but it never overrides a failed required path.

## Algorithm Naming

ML-DSA is the NIST-standardized name for the signature direction formerly known as CRYSTALS-Dilithium.

FN-DSA is based on Falcon.

FN-DSA and ML-DSA are separate signature directions.

## Trust Profile

The QWG v4 trust profile requires:

```text
role
key_id
key_version
algorithm
not_before
not_after
status
public_key
```

The only valid QWG role in this component package is:

```text
shield_component_qwg
```

A revoked key, unknown key, wrong role, wrong algorithm, invalid validity window, malformed real binary key, or deterministic TEST-ONLY key in real backend mode fails closed.

## Real Backend Files

V4.8E adds:

```text
src/qwg/v4/real_crypto_backend.py
src/qwg/v4/oqs_mldsa_backend.py
docs/qwg/v4/REAL_CRYPTO_BACKEND.md
THIRD_PARTY_NOTICES.md
```

The OQS adapter maps:

```text
Shield algorithm: ml-dsa
OQS mechanism:    ML-DSA-65
```

It lazily imports `oqs` only when used and does not add a hard dependency to `pyproject.toml`.

## Current Implementation Status

V4.4 provided:

- a parallel `qwg.v4` package;
- canonical component-verdict signed payload construction;
- deterministic TEST-ONLY signature entries;
- strict signature-bundle validation;
- QWG role-bound trust profile validation;
- negative tests for tampering, context mismatch, and missing signatures.

V4.8E adds:

- a backend-neutral real crypto adapter for QWG component verdict evidence;
- strict `b64u:<unpadded-base64url-bytes>` real binary material encoding;
- a lazy OQS/liboqs ML-DSA backend mapped to `ML-DSA-65`;
- tests proving OQS missing, disabled, wrong mechanism, malformed binary material, native OQS/liboqs exceptions, and TEST-ONLY material all fail closed.

V4.8G adds:

- strict `isinstance(verified, bool)` enforcement for generic and OQS verifier returns;
- a gated live liboqs ML-DSA proof test in `tests/test_v48g_real_oqs_mldsa_backend.py`;
- a not-skipped JUnit guard in `scripts/assert_real_oqs_junit_not_skipped.py`;
- documentation that default CI proves the interface contract and fail-closed behavior, while live liboqs proof requires `SHIELD_V4_REAL_OQS=1` plus installed `oqs`/liboqs.


## V4.8G-R4 Audit Cleanup

V4.8G-R4 closes the audit cleanup items for component canonicalization drift by adding:

- QWG real-crypto adapter parity now matches the later component ports;
- the shared frozen component-verdict KAT fixture in `tests/fixtures/v4/component_verdict_policy_v1_kat.json`;
- a KAT lock test that must reproduce signed payload hash `a3881f27444ce73de875a15c8b413785a4fec4f4c03baaa6f8ee2fbf839736ae`;
- explicit proof that null and float mutations of the KAT payload fail before signing.

The KAT is TEST-ONLY deterministic evidence. It is not production key material and does not claim live liboqs execution.
