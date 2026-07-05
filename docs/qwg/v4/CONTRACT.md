# QWG Shield v4 Component Verdict Contract

Author attribution: DarekDGB

## Status

This document defines the QWG Shield v4 component-verdict contract.

This is a parallel v4 contract. It does not modify or replace the audited v3.2 QWG deterministic contract.

V4.8E added a real ML-DSA backend adapter path for QWG component evidence. V4.8H-B adds the QWG pilot FN-DSA optional-evidence contract with authenticated `standard_profile` binding. The deterministic TEST-ONLY path remains separate and is retained only for contract and CI locking.

## Authority Boundary

QWG Shield v4 does not sign DigiByte transactions.

QWG Shield v4 does not broadcast transactions.

QWG Shield v4 does not change DigiByte consensus.

QWG Shield v4 does not approve AdamantineOS execution.

QWG Shield v4 produces cryptographically verifiable component decision evidence only.

The Shield Orchestrator verifies component evidence before producing a Shield receipt.

AdamantineOS remains the final execution boundary.

## Contract Identity

```text
component_id: qwg
component_role: shield_component_qwg
contract_version: 4
schema_version: shield.verdict.v2
canonicalization_profile: shield-v4-canon.v1
signature_policy: policy.v1
```

## Signed Payload Fields

The unsigned payload covered by `signed_payload_hash` contains:

```text
component_id
contract_version
schema_version
request_id
context_hash
freshness_nonce
not_before
not_after
decision
reason_ids
evidence_hash
evidence_families
metadata
fail_closed
canonicalization_profile
signature_policy
key_registry_version
```

The `signature_bundle` and `signed_payload_hash` fields are not part of the payload they sign.

## Canonicalization

QWG v4 uses the same Shield v4 canonicalization profile locked in the Orchestrator:

```text
shield-v4-canon.v1
```

The signed-payload hash uses this domain tag:

```text
DGB-SHIELD-V4-COMPONENT-VERDICT:shield.verdict.v2:policy.v1
```

A component-verdict signature must never verify as an Orchestrator receipt signature.

## Signature Policy

`policy.v1` requires strict AND semantics:

```text
classical-ed25519
ml-dsa
```

Optional evidence path:

```text
fn-dsa
```

ML-DSA means ML-DSA, formerly CRYSTALS-Dilithium.

FN-DSA means FN-DSA, based on Falcon.

FN-DSA is not ML-DSA and cannot satisfy the ML-DSA requirement.

FN-DSA is optional additional evidence in V4.8H-B. FN-DSA absence is allowed while the required `classical-ed25519` and `ml-dsa` paths remain valid. FN-DSA present but invalid, malformed, unsupported, unresolvable, duplicated, wrong-role, wrong-hash, wrong-domain, or profile-mismatched is fatal.

## Standard Profiles

Every signature entry carries an authenticated `standard_profile` field. QWG V4.8H-B locks these policy.v1 profiles:

```text
classical-ed25519 -> rfc8032-ed25519-v1
ml-dsa            -> fips204-ml-dsa-65-v1
fn-dsa            -> fips206-draft-falcon1024-v1
```

The FN-DSA profile is draft Falcon-1024 evidence only. Falcon-1024 is documented as NIST security level 5. ML-DSA-65 remains the required level-3 PQC path. This package makes no final FIPS 206 production claim.

The `standard_profile` value is not display-only metadata. It is bound into the real-signature message bytes and into deterministic TEST-ONLY signature material so a profile flip after signing fails closed.

## Real Backend Path

QWG V4.8E introduced an optional real backend adapter for the required `ml-dsa` path:

```text
src/qwg/v4/real_crypto_backend.py
src/qwg/v4/oqs_mldsa_backend.py
```

The OQS adapter maps Shield algorithm `ml-dsa` to OQS mechanism `ML-DSA-65`.

The adapter:

- does not vendor liboqs;
- does not add a hard `pyproject.toml` dependency;
- lazily imports `oqs` only when used;
- rejects missing or disabled OQS mechanisms;
- rejects wrong OQS mechanism selection;
- rejects malformed `b64u:` public keys or signatures;
- rejects deterministic TEST-ONLY key material at the real backend boundary;
- wraps native OQS/liboqs exceptions inside the QWG real-backend fail-closed error hierarchy;
- provides no fallback from real backend mode to deterministic TEST-ONLY signatures.

V4.8H-B extends the neutral real-crypto adapter entry shape to include `standard_profile` for all algorithms, including optional `fn-dsa`. The package does not add a live FN-DSA/Falcon backend. It locks the QWG component-side contract and signed-message bytes so a later dedicated backend can verify the same authenticated profile semantics.

Real binary signatures and public keys use this encoding shape:

```text
b64u:<unpadded-base64url-bytes>
```

This step does not add a production `classical-ed25519` backend. A production real-backend deployment must still satisfy both required policy paths.

## Freshness and Anti-Replay

Every signed QWG v4 verdict carries:

```text
request_id
freshness_nonce
not_before
not_after
```

These fields are inside the signed payload.

A verifier must reject stale, malformed, duplicate, or replayed verdicts according to the Orchestrator receipt policy and replay-state rules.

## Fail-Closed Rules

A verifier must reject:

- missing signature bundle
- missing required algorithm
- duplicate algorithm entry
- unknown algorithm
- unsupported `standard_profile`
- `standard_profile` flipped after signing
- present-invalid FN-DSA optional evidence
- present-but-unresolvable FN-DSA optional evidence
- FN-DSA attempting to replace ML-DSA or classical evidence
- wrong key id
- wrong key role
- revoked key
- invalid key window
- changed context hash
- changed request id
- changed decision
- changed reason ids
- changed evidence hash
- changed metadata
- forbidden authority metadata
- malformed canonical payload
- `null` or float values in signed fields
- missing OQS backend when real ML-DSA mode is selected
- disabled or wrong OQS ML-DSA mechanism
- malformed `b64u:` real binary material
- structurally valid but backend-invalid OQS key or signature material
- native OQS/liboqs signing, verification, mechanism-discovery, or version-discovery exception
- deterministic TEST-ONLY material at the real backend boundary

## Test-Only Cryptography Warning

The original QWG v4 pilot uses deterministic TEST-ONLY signatures for contract and CI locking.

These test signatures are not production private keys and are not production ML-DSA or FN-DSA implementations.

Production PQC adapters must satisfy the same signed payload, domain tag, key role, key version, freshness, policy, `standard_profile`, and bundle-binding rules.

The V4.8E OQS adapter is a real-backend path for QWG component evidence only. V4.8H-B adds optional FN-DSA policy and profile-binding proof only. Neither step creates transaction signing, broadcast, consensus, or final-execution authority.
