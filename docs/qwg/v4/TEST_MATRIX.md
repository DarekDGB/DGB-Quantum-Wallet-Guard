# QWG Shield v4 Test Matrix

Author attribution: DarekDGB

## Scope

This matrix covers the QWG Shield v4 component-verdict contract and the V4.8E real ML-DSA pilot backend path.

The goal is to prove QWG can produce and verify v4 component evidence while keeping TEST-ONLY deterministic signatures separate from real backend mode.

## Positive Tests

| Test | Expected result |
|---|---|
| build unsigned QWG v4 payload | deterministic payload with `contract_version: 4` |
| add required classical + ML-DSA test signatures | signed envelope validates under TEST-ONLY verifier |
| validate with matching context hash | verification summary returned |
| verify required role | `shield_component_qwg` only |
| build real crypto signature input | frozen QWG component domain bytes |
| build real ML-DSA signature entry through backend adapter | `b64u:` signature entry produced |
| verify real ML-DSA signature entry through backend adapter | verification returns true |
| lazy OQS fake backend exposes version | backend metadata includes locked mechanism |
| gated live liboqs ML-DSA proof | skipped by default; passes only in a dedicated `SHIELD_V4_REAL_OQS=1` job with `skipped == 0` |

## Negative Tests

| Test | Expected result |
|---|---|
| tampered signature | fail closed |
| changed context hash after signing | fail closed |
| missing ML-DSA required signature | fail closed |
| duplicate algorithm entry | fail closed |
| unsupported algorithm | fail closed |
| wrong domain tag | fail closed |
| wrong signed payload hash | fail closed |
| revoked key | fail closed |
| artifact outside key validity window | fail closed |
| forbidden authority metadata | fail closed |
| null in signed payload | fail closed |
| float in signed payload | fail closed |
| duplicate JSON key while parsing | fail closed |
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

This gate is not part of default CI and must not create a hard OQS/liboqs dependency. It is
required before any public claim that live liboqs ML-DSA verified through QWG:

```text
SHIELD_V4_REAL_OQS=1 python -m pytest \
  tests/test_v48g_real_oqs_mldsa_backend.py \
  --override-ini addopts='' \
  --junitxml=.artifacts/v48g-real-oqs.xml
python scripts/assert_real_oqs_junit_not_skipped.py .artifacts/v48g-real-oqs.xml
```

## Authority Boundary

Passing these tests proves only the QWG v4 component-verdict contract and QWG real ML-DSA adapter boundary.

It does not grant transaction-signing authority, broadcast authority, DigiByte consensus authority, Shield Orchestrator final receipt authority, or AdamantineOS final authority.
