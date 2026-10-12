# QWG Shield v4 Real Crypto Backend

Status: controlled `4.0.0` release candidate; not released or tagged
Author attribution: DarekDGB

## Boundary

The QWG real-backend path signs and verifies QWG component verdict evidence
only. It does not sign or broadcast DigiByte transactions, hold wallet keys,
change consensus, create the final Shield receipt, bypass the Orchestrator, or
grant AdamantineOS final authority.

## Algorithms and profiles

```text
classical-ed25519 -> rfc8032-ed25519-v1       required
ml-dsa            -> fips204-ml-dsa-65-v1    required
fn-dsa            -> fips206-draft-falcon1024-v1 optional-last
```

Optional FN-DSA cannot replace or rescue either required path. Falcon-1024 is
draft-profile evidence, not final FIPS 206 proof.

## Provider mappings

The backend-neutral adapter is
`src/qwg/v4/real_crypto_backend.py`. Optional liboqs adapters map:

```text
ml-dsa -> ML-DSA-65
fn-dsa -> Falcon-1024
```

Providers are imported only when selected. No hard liboqs dependency is added.
A missing provider, disabled or wrong mechanism, native exception, or
non-boolean verifier result fails closed.

## Frozen signature input

Every real QWG signature signs these LF-separated fields with no terminal LF:

```text
DGB-SHIELD-V4-REAL-CRYPTO-SIGNATURE-INPUT
<domain_tag>
<signed_payload_hash>
<algorithm>
<standard_profile>
<key_id>
<key_version>
```

The domain is
`DGB-SHIELD-V4-COMPONENT-VERDICT:shield.verdict.v2:policy.v1`. Algorithm,
profile, role-resolved key ID, key version, and payload hash must match the
verifier-controlled QWG trust entry.

## Binary material

Real keys and signatures use strict unpadded
`b64u:<base64url-bytes>` encoding. Padding, malformed alphabet, empty bytes,
wrong length, or backend-invalid material fails closed.

Deterministic test IDs, TEST-ONLY public keys, and test-only private references
are rejected at the real-backend boundary. There is no automatic fallback to
test signatures.

## Dedicated native proof

Default CI proves interface and fail-closed behavior but not native liboqs
execution. The dedicated workflow enables both guarded nodes:

```text
tests/test_v48g_real_oqs_mldsa_backend.py::test_v48g_real_oqs_mldsa65_qwg_backend_round_trip_and_negatives
tests/test_v48h_e_real_oqs_falcon_backend.py::test_v48h_e_real_oqs_falcon1024_backend_round_trip_and_negatives
```

Its JUnit guard requires tests=2, skipped=0, failures=0, and errors=0. The exact
mode checks actual testcase outcomes, consistent counters, and one-to-one
membership in the complete node list above. A green
native proof uses test keys and does not establish production custody, HSM
assurance, transaction signing, provider hardening, or final FIPS 206
conformance.

## V4.10-I2 immutable sources and retained evidence

```text
liboqs: 0.16.0
liboqs commit: 5a1a854b0dc9f2141bdc771c555ee60c37950183
liboqs-python: 0.16.0
liboqs-python commit: c6378cd5c8db74c0adf34ddcfbb96ee9c99f8061
native proof CPython: 3.11.15
pytest: 8.4.2
runner label: ubuntu-24.04
```

Checkout, Python setup, and artifact upload actions use immutable commits.
The workflow checks each fetched source HEAD, builds a shared Release liboqs
outside the repository, and builds/installs a wheel from the pinned wrapper
checkout without dependency resolution during those wheel operations.

`OQS_INSTALL_PATH` and `LD_LIBRARY_PATH` are initialized in a shell step after
runner startup through `GITHUB_ENV`. The workflow explicitly loads the expected
native library before importing `oqs`, compares library handles, checks both
mechanisms and versions, and verifies installed wrapper modules against the
pinned source. A wrong provider or identity fails the job.

The retained artifact is named
`shield-v4-real-oqs-<repository-commit>-<run-attempt>`. It contains the exact
collection, JUnit report, verbose pytest output, guard output, environment and
provider identities, native build/install logs, CMake cache, Python package
inventory, wrapper wheel, source-archive hashes, and `SHA256SUMS`.
Missing evidence fails the guard or upload step. Failure-run artifacts remain
diagnostic and cannot be promoted to successful proof.

Retention is 90 days; preserve the verified archive externally before expiry.
The native shared library is hashed, not retained. Source archive streams are
hashed, not retained. The runner image, apt packages, and transitive build
dependencies are not fully immutable, so this is source identity and execution
evidence rather than a bit-reproducible native-binary claim.

The hosted QWG I2 proof remains pending until the delivered package is committed
and its successful exact-commit artifact and fresh source ZIP are verified.

## Third-party attribution

Provider-family notices belong in `THIRD_PARTY_NOTICES.md`. No third-party
PQC source is vendored unless that notice explicitly says otherwise. First-
party author attribution remains DarekDGB.
