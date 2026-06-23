# QWG Shield v4 Real Crypto Backend Contract

Author attribution: DarekDGB

## Status

This document locks the QWG Shield v4 real-crypto backend boundary for component verdict evidence.

V4.8E introduces a deployment-controlled real ML-DSA adapter path for QWG. It does not replace the deterministic TEST-ONLY signature path used by contract tests. It does not make QWG a transaction signer, broadcaster, consensus layer, wallet custody layer, or AdamantineOS final authority.

## Non-authority lock

QWG Shield v4 cryptography proves QWG component decision evidence only.

QWG still must not:

- sign DigiByte transactions;
- broadcast transactions;
- change DigiByte consensus;
- grant final execution approval;
- bypass the Shield Orchestrator;
- bypass AdamantineOS.

The Shield Orchestrator verifies QWG component evidence before producing a Shield receipt. AdamantineOS remains the final execution boundary.

## Algorithm lock

Shield v4 policy `policy.v1` uses these names:

- `classical-ed25519` — required classical signature path;
- `ml-dsa` — required PQC path; ML-DSA was formerly CRYSTALS-Dilithium;
- `fn-dsa` — optional evidence path based on Falcon.

`fn-dsa` is not ML-DSA. It must never override failure of the required `classical-ed25519` or `ml-dsa` paths.

## Backend model

QWG exposes a backend-neutral adapter contract in:

```text
src/qwg/v4/real_crypto_backend.py
```

The neutral adapter does not require a specific PQC library. Real deployments may connect liboqs, an HSM, a FIPS-validated module, or another reviewed backend through the same interface.

The optional OQS ML-DSA backend lives in:

```text
src/qwg/v4/oqs_mldsa_backend.py
```

It lazily imports `oqs` only when used, so normal CI and non-OQS deployments do not silently depend on local machine crypto state. If OQS is missing, disabled, lacks the locked mechanism, or raises a native backend exception, the adapter wraps that failure inside the QWG real-backend fail-closed error hierarchy.

## OQS ML-DSA mapping

For Shield v4 `policy.v1`, the optional OQS backend maps:

```text
Shield algorithm: ml-dsa
OQS mechanism:    ML-DSA-65
```

The mechanism is deliberately locked for this backend. A caller cannot silently swap `ML-DSA-44`, `ML-DSA-87`, Falcon/FN-DSA, or another mechanism behind the Shield policy name.

## Frozen real-signature input

Every real QWG component-verdict signature signs the exact byte string:

```text
DGB-SHIELD-V4-REAL-CRYPTO-SIGNATURE-INPUT
<domain_tag>
<signed_payload_hash>
<algorithm>
<key_id>
<key_version>
```

Rules:

- UTF-8 encoding only;
- line separator is LF (`\n`);
- no trailing newline;
- `domain_tag` must be `DGB-SHIELD-V4-COMPONENT-VERDICT:shield.verdict.v2:policy.v1`;
- `signed_payload_hash` must be lowercase SHA-256 hex;
- `algorithm`, `key_id`, and `key_version` must match the QWG trust-profile entry.

The `signed_payload_hash` is already computed over the domain-separated canonical QWG verdict payload. The real-signature input binds that hash to the concrete signature entry so signatures cannot be spliced across algorithms, keys, roles, or bundles.

## Binary encoding lock

Real ML-DSA signatures and public keys are binary. QWG real backend adapters use explicit unpadded base64url encoding with the prefix:

```text
b64u:<unpadded-base64url-bytes>
```

Rules:

- real binary signatures use `b64u:`;
- real OQS public keys use `b64u:` in the QWG trust profile;
- padding characters (`=`) are rejected;
- malformed base64url is rejected before calling a crypto backend;
- structurally valid base64url that decodes to backend-invalid key or signature lengths must fail closed through `QwgV4RealCryptoBackendError`;
- historical 64-character deterministic test digests remain test fixtures only.

## Test-only material rejection

The real-crypto adapter must reject deterministic test material before calling a production backend.

Rejected examples include:

- key ids beginning with `test-`;
- public keys containing `TEST-ONLY`;
- private key references containing `test-only` or beginning with `test-`.

There is no automatic fallback from real backend mode to TEST-ONLY deterministic signatures.

## Policy status

This step adds the real ML-DSA path for QWG. Shield v4 `policy.v1` still requires both:

```text
classical-ed25519
ml-dsa
```

A production real-backend deployment must satisfy both required paths. This QWG OQS adapter alone does not downgrade policy.v1 and does not allow ML-DSA to replace the required classical path.

## Third-party attribution

When a real backend is selected, repository-level attribution belongs in:

```text
THIRD_PARTY_NOTICES.md
```

The notice identifies the backend family, clarifies that no third-party PQC source is vendored unless explicitly stated, and keeps author attribution as DarekDGB.
