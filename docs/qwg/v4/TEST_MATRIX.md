# QWG Shield v4 Test Matrix

Author attribution: DarekDGB

## Scope

This matrix covers the QWG Shield v4 component-verdict contract, the V4.8E real ML-DSA pilot backend path, and the V4.8H-B QWG FN-DSA optional-evidence pilot.

The goal is to prove QWG can produce and verify v4 component evidence while keeping TEST-ONLY deterministic signatures separate from real backend mode. FN-DSA is optional additional evidence only; it cannot rescue any failed required signature path.

## Positive Tests

| Test | Expected result |
|---|---|
| build unsigned QWG v4 payload | deterministic payload with `contract_version: 4` |
| add required classical + ML-DSA test signatures | signed envelope validates under TEST-ONLY verifier |
| validate with matching context hash | verification summary returned |
| verify required role | `shield_component_qwg` only |
| build real crypto signature input | frozen QWG component domain bytes with authenticated `standard_profile` |
| build real ML-DSA signature entry through backend adapter | `b64u:` signature entry produced with `fips204-ml-dsa-65-v1` |
| verify real ML-DSA signature entry through backend adapter | verification returns true |
| FN-DSA absent with required signatures valid | accepted under V4.8H policy |
| FN-DSA present and valid with required signatures valid | accepted and recorded as optional evidence |
| FN-DSA signed-message KAT | `fn-dsa`, `fips206-draft-falcon1024-v1`, and component domain bytes match fixture |
| lazy OQS fake backend exposes version | backend metadata includes locked mechanism |
| gated live liboqs ML-DSA proof | skipped by default; passes only in a dedicated `SHIELD_V4_REAL_OQS=1` job with `skipped == 0` |
| shared frozen component-verdict KAT vector | canonical JSON, domain-separated bytes, and signed payload hash match the shared V4.8G-R4 fixture |

## Negative Tests

| Test | Expected result |
|---|---|
| tampered signature | fail closed |
| changed context hash after signing | fail closed |
| missing ML-DSA required signature | fail closed |
| FN-DSA valid but ML-DSA invalid | fail closed |
| FN-DSA valid but classical invalid | fail closed |
| FN-DSA present invalid | fail closed |
| FN-DSA present with no registry key | fail closed |
| FN-DSA duplicate entry | fail closed |
| FN-DSA wrong key role | fail closed |
| FN-DSA wrong domain tag | fail closed |
| FN-DSA wrong signed payload hash | fail closed |
| FN-DSA unsupported `standard_profile` | fail closed |
| FN-DSA `standard_profile` flipped after signing | fail closed |
| duplicate algorithm entry | fail closed |
| unsupported algorithm | fail closed |
| wrong domain tag | fail closed |
| wrong signed payload hash | fail closed |
| revoked key | fail closed |
| artifact outside key validity window | fail closed |
| forbidden authority metadata | fail closed |
| null in signed payload | fail closed |
| float in signed payload | fail closed |
| KAT payload mutated with null or float | fail closed before signing |
| duplicate JSON key while parsing | fail closed |
| verifier callback raises native exception | fail closed |
| verifier callback returns non-bool | fail closed |
| real backend missing required algorithm support | fail closed |
| real backend receives TEST-ONLY key id or public key | fail closed |
| real backend receives TEST-ONLY private key reference | fail closed |
| real backend emits malformed non-`b64u:` signature | fail closed |
| malformed real `b64u:` public key | fail closed |
| malformed real `b64u:` signature | fail closed |
| OQS import missing when backend selected | fail closed |
| OQS `ML-DSA-65` mechanism disabled | fail closed |
| wrong OQS mechanism requested | fail closed |
| OQS backend asked to sign or verify non-`ml-dsa` algorithm | fail closed |
| native OQS version or mechanism discovery exception | fail closed through QWG backend error hierarchy |
| native OQS sign exception on backend-invalid key material | fail closed through QWG backend error hierarchy |
| native OQS verify exception on structurally valid but backend-invalid key/signature bytes | fail closed through QWG backend error hierarchy |
| empty OQS message, secret key, or signature bytes | fail closed |
| live liboqs wrong-length public key | fail closed through QWG backend error hierarchy in the gated real-OQS job |
| live liboqs tampered signature | verify returns false in the gated real-OQS job |
| real-OQS job import-skips or collects no tests | guard fails the dedicated job |

## Required CI Gate

```text
pytest --cov=qwg --cov-report=term-missing --cov-fail-under=100 -q
```

## Optional Real-OQS CI Gate

This gate is not part of default CI and must not create a hard OQS/liboqs dependency. It is required before any public claim that live liboqs ML-DSA verified through QWG:

```text
SHIELD_V4_REAL_OQS=1 python -m pytest \
  tests/test_v48g_real_oqs_mldsa_backend.py \
  --override-ini addopts='' \
  --junitxml=.artifacts/v48g-real-oqs.xml
python scripts/assert_real_oqs_junit_not_skipped.py .artifacts/v48g-real-oqs.xml
```

No final FN-DSA/FIPS 206 public claim is made by V4.8H-B or V4.8H-E. V4.8H-E adds the dedicated gated Falcon-1024 proof path and still requires the not-skipped guard before any public live-Falcon claim.

## V4.8G-R4 Audit Cleanup Checks

The component test suite now includes a shared frozen component-verdict KAT fixture:

```text
tests/fixtures/v4/component_verdict_policy_v1_kat.json
```

Every component repo must reproduce this signed payload hash exactly:

```text
a3881f27444ce73de875a15c8b413785a4fec4f4c03baaa6f8ee2fbf839736ae
```

The KAT is TEST-ONLY deterministic canonicalization evidence only. It does not sign transactions, broadcast, change DigiByte consensus, or claim live liboqs execution.

## V4.8H-B FN-DSA KAT

QWG V4.8H-B adds this component signed-message KAT:

```text
tests/fixtures/v4/fn_dsa_signed_message_draft_profile_kat.json
```

The KAT locks the exact `build_real_crypto_signature_input` bytes for:

```text
algorithm: fn-dsa
standard_profile: fips206-draft-falcon1024-v1
domain: DGB-SHIELD-V4-COMPONENT-VERDICT:shield.verdict.v2:policy.v1
```

The KAT is TEST-ONLY message-construction evidence. It is not production key material, not production FN-DSA, and not final FIPS 206 proof.

## V4.8H-E Full Hybrid and Live-Falcon Checks

V4.8H-E adds these checks:

```text
tests/test_v48h_e_oqs_falcon_backend.py
tests/test_v48h_e_real_oqs_falcon_backend.py
```

The deterministic backend-contract test proves Falcon-1024 adapter wiring, `b64u:` binary material parsing, wrong-algorithm denial, disabled-mechanism denial, native exception fail-closed handling, and `standard_profile` binding.

The real-liboqs test is gated and must be run only by the dedicated PQC workflow with:

```text
SHIELD_V4_REAL_OQS=1
SHIELD_V4_REAL_OQS_FALCON=1
```

A live Falcon-1024 claim requires the dedicated PQC workflow JUnit guard to report `skipped == 0`, `failures == 0`, and `errors == 0`. FN-DSA remains optional evidence and is not final FIPS 206 proof.

## Authority Boundary

Passing these tests proves only the QWG v4 component-verdict contract, QWG real ML-DSA adapter boundary, and QWG FN-DSA optional-evidence policy behavior.

It does not grant transaction-signing authority, broadcast authority, DigiByte consensus authority, Shield Orchestrator final receipt authority, or AdamantineOS final authority.
