# QWG Shield v4 Real Crypto Backend Contract

Author attribution: DarekDGB

## Status

This document locks the QWG Shield v4 real-crypto backend boundary for component verdict evidence.

V4.8E introduces a deployment-controlled real ML-DSA adapter path for QWG. V4.8H-B extends the neutral real-crypto signature-entry contract with authenticated `standard_profile` binding and optional FN-DSA draft-profile evidence semantics. These steps do not replace the deterministic TEST-ONLY signature path used by contract tests. They do not make QWG a transaction signer, broadcaster, consensus layer, wallet custody layer, or AdamantineOS final authority.

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

- `classical-ed25519` - required classical signature path;
- `ml-dsa` - required PQC path; ML-DSA was formerly CRYSTALS-Dilithium;
- `fn-dsa` - optional evidence path based on Falcon.

`fn-dsa` is not ML-DSA. It must never override failure of the required `classical-ed25519` or `ml-dsa` paths.

## Standard profile lock

Every real signature entry carries `standard_profile`, and that value is part of the message signed by the backend.

V4.8H-B allows these profiles:

```text
classical-ed25519 -> rfc8032-ed25519-v1
ml-dsa            -> fips204-ml-dsa-65-v1
fn-dsa            -> fips206-draft-falcon1024-v1
```

`fips206-draft-falcon1024-v1` means FN-DSA draft-profile evidence based on Falcon-1024. It is optional QWG hybrid evidence only. It is not final FIPS 206 proof. Future final-profile support must add a separate profile, KATs, registry keys, docs, and tests instead of reinterpreting draft signatures.

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
standard_profile: fips204-ml-dsa-65-v1
```

The mechanism is deliberately locked for this backend. A caller cannot silently swap `ML-DSA-44`, `ML-DSA-87`, Falcon/FN-DSA, or another mechanism behind the Shield policy name.

## CI proof levels and gated real-liboqs job

Default package CI proves the QWG real-backend adapter interface, binary-material parsing, authenticated `standard_profile` binding, fail-closed exception hierarchy, and component evidence wiring with deterministic backends. That default CI does not claim to execute live liboqs ML-DSA or live FN-DSA/Falcon.

Live liboqs ML-DSA proof is optional and gated so QWG does not gain a hard OQS/liboqs dependency. The dedicated job must set `SHIELD_V4_REAL_OQS=1`, install `oqs`/liboqs, write a JUnit report, disable default coverage addopts for the focused gated job, and run the not-skipped guard:

```text
SHIELD_V4_REAL_OQS=1 python -m pytest \
  tests/test_v48g_real_oqs_mldsa_backend.py \
  --override-ini addopts='' \
  --junitxml=.artifacts/v48g-real-oqs.xml
python scripts/assert_real_oqs_junit_not_skipped.py .artifacts/v48g-real-oqs.xml
```

The guard fails if the real-OQS job collects zero tests, skips any testcase, or records any failure/error. A public claim that live liboqs ML-DSA verified through QWG requires that gated job to pass with `skipped == 0`; release-grade real-backend proof remains a V4.10 release gate.

## V4.8H-E OQS Falcon-1024 mapping

V4.8H-E adds an optional OQS Falcon-1024 backend for live FN-DSA draft-profile evidence:

```text
src/qwg/v4/oqs_falcon_backend.py
tests/test_v48h_e_oqs_falcon_backend.py
tests/test_v48h_e_real_oqs_falcon_backend.py
```

The backend mapping is locked as:

```text
Shield algorithm: fn-dsa
standard_profile: fips206-draft-falcon1024-v1
OQS mechanism:    Falcon-1024
```

This backend is optional evidence only. It does not make FN-DSA required, does not let FN-DSA rescue failed or missing `classical-ed25519` or `ml-dsa`, does not sign transactions, does not broadcast, and does not change DigiByte consensus. It is draft Falcon-1024 profile evidence only, not a final FIPS 206 production claim.

## Frozen real-signature input

Every real QWG component-verdict signature signs the exact byte string:

```text
DGB-SHIELD-V4-REAL-CRYPTO-SIGNATURE-INPUT
<domain_tag>
<signed_payload_hash>
<algorithm>
<standard_profile>
<key_id>
<key_version>
```

Rules:

- UTF-8 encoding only;
- line separator is LF (`\n`);
- no trailing newline;
- `domain_tag` must be `DGB-SHIELD-V4-COMPONENT-VERDICT:shield.verdict.v2:policy.v1`;
- `signed_payload_hash` must be lowercase SHA-256 hex;
- `algorithm`, `standard_profile`, `key_id`, and `key_version` must match QWG policy and the QWG trust-profile entry;
- unsupported `standard_profile` values fail closed;
- a `standard_profile` flip after signing fails signature verification.

The `signed_payload_hash` is already computed over the domain-separated canonical QWG verdict payload. The real-signature input binds that hash to the concrete signature entry so signatures cannot be spliced across algorithms, profiles, keys, roles, or bundles.

## FN-DSA optional evidence behavior

For V4.8H-B, QWG may include `fn-dsa` as optional evidence over the same `signed_payload_hash` used by the required signatures.

Decision rules:

- required `classical-ed25519 + ml-dsa` still use AND semantics;
- FN-DSA absent is allowed;
- FN-DSA present and valid is recorded as optional evidence;
- FN-DSA present but invalid is DENY;
- FN-DSA present but no active QWG `fn-dsa` trust-profile key is DENY;
- unsupported FN-DSA `standard_profile` is DENY;
- duplicate FN-DSA entries are DENY;
- valid FN-DSA cannot rescue failed or missing `classical-ed25519` or `ml-dsa`.

V4.8H-B locks the QWG component contract, KAT, and verifier behavior. V4.8H-E adds the gated live Falcon-1024 backend path without changing the signed-message format.

V4.8H-E extends the dedicated PQC workflow so it sets both `SHIELD_V4_REAL_OQS=1` and `SHIELD_V4_REAL_OQS_FALCON=1`, then runs the ML-DSA proof and the Falcon-1024 proof in the same guarded JUnit report:

```text
python -m pytest --override-ini addopts='' \
  tests/test_v48g_real_oqs_mldsa_backend.py \
  tests/test_v48h_e_real_oqs_falcon_backend.py \
  -q --junitxml=shield-v4-real-oqs-results.xml
python scripts/assert_real_oqs_junit_not_skipped.py shield-v4-real-oqs-results.xml
```

A public live Falcon-1024 claim requires that dedicated workflow to finish green with `skipped == 0`, `failures == 0`, and `errors == 0` for the guarded report.

## Binary encoding lock

Real ML-DSA, FN-DSA/Falcon-1024, and other real signatures/public keys are binary. QWG real backend adapters use explicit unpadded base64url encoding with the prefix:

```text
b64u:<unpadded-base64url-bytes>
```

Rules:

- real binary signatures use `b64u:`;
- real public keys use `b64u:` in the QWG trust profile;
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

Shield v4 `policy.v1` still requires both:

```text
classical-ed25519
ml-dsa
```

A production real-backend deployment must satisfy both required paths. This QWG OQS adapter alone does not downgrade policy.v1 and does not allow ML-DSA or FN-DSA to replace the required classical path.

## Third-party attribution

When a real backend is selected, repository-level attribution belongs in:

```text
THIRD_PARTY_NOTICES.md
```

The notice identifies the backend family, clarifies that no third-party PQC source is vendored unless explicitly stated, and keeps author attribution as DarekDGB.
