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

V4.8H-B keeps FN-DSA optional for QWG. Absence is allowed. Presence is fatal if the FN-DSA entry is invalid, malformed, unsupported, duplicated, wrong-role, wrong-hash, wrong-domain, or has no matching active QWG trust-profile key.

## Algorithm Naming

ML-DSA is the NIST-standardized name for the signature direction formerly known as CRYSTALS-Dilithium.

FN-DSA is based on Falcon.

FN-DSA and ML-DSA are separate signature directions.

Shield v4 uses the algorithm identifier `fn-dsa`, not the Q-ID `pqc-` prefix.

## Standard Profiles

QWG V4.8H-B locks these `standard_profile` values into signature entries and real-signature message bytes:

```text
classical-ed25519 -> rfc8032-ed25519-v1
ml-dsa            -> fips204-ml-dsa-65-v1
fn-dsa            -> fips206-draft-falcon1024-v1
```

`fips206-draft-falcon1024-v1` means draft Falcon-1024 evidence only. It is not a final FIPS 206 production proof. The profile field is authenticated so a later profile flip or downgrade attempt fails closed.

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

The trust profile preserves the `(role, algorithm)` model. FN-DSA uses the QWG role plus `algorithm: fn-dsa`; the algorithm is not folded into the role name.

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

V4.8H-B extends `real_crypto_backend.py`, `signing.py`, and `trust_profile.py` so all signature entries include authenticated `standard_profile` and optional FN-DSA evidence follows the same bundle semantics as the Orchestrator.

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

## V4.8H-B FN-DSA Pilot

V4.8H-B adds:

- authenticated `standard_profile` in QWG signature entries;
- `standard_profile` binding inside `build_real_crypto_signature_input`;
- Falcon-1024 draft profile locking for optional `fn-dsa` evidence;
- shared component FN-DSA signed-message KAT fixture in `tests/fixtures/v4/fn_dsa_signed_message_draft_profile_kat.json`;
- tests proving FN-DSA absence is allowed, valid FN-DSA is recorded, present-invalid FN-DSA is fatal, and FN-DSA cannot rescue failed or missing required signatures.

V4.8H-B does not claim final FIPS 206 compliance. V4.8H-E adds the gated live Falcon-1024 backend path while keeping FN-DSA optional and draft-profile only.

## V4.8H-E Final Hybrid Evidence Lock

V4.8H-E adds:

- the optional OQS Falcon-1024 backend in `src/qwg/v4/oqs_falcon_backend.py`;
- deterministic backend-contract tests in `tests/test_v48h_e_oqs_falcon_backend.py`;
- a gated real-liboqs Falcon-1024 proof test in `tests/test_v48h_e_real_oqs_falcon_backend.py`;
- a dedicated PQC workflow that runs both live ML-DSA and live Falcon-1024 proofs with the not-skipped JUnit guard.

The H-E lock keeps FN-DSA optional. It does not upgrade FN-DSA to required policy, does not claim final FIPS 206 support, and does not let Falcon/FN-DSA override required `classical-ed25519` or `ml-dsa` failures.
