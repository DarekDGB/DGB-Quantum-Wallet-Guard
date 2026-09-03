# QWG Shield v4 Proof Pack

Status: V4.10-E1 controlled `4.0.0` release candidate; not released or tagged
Author attribution: DarekDGB

## Authenticated source

```text
repository: DGB-Quantum-Wallet-Guard
commit: 636d9baa1f2d09803edcfcc626fdf17094ac26ae
git tree: fd31cffd1acf9fee229c0fa0bb810185ce8c2bd0
fresh ZIP: DGB-Quantum-Wallet-Guard-main(20260812-060639).zip
fresh ZIP SHA-256: f7993882663b67bd7ce4432fb90bd234131f238b247e37ec6495eec0a508dd83
archive inventory: 81 files, 17 directories, 98 entries
```

The archive comment matches the authenticated commit. Full CRC reading, root,
path, traversal, and backslash checks passed before modification.

## Version alignment

The distribution candidate is `4.0.0`; the candidate tag name is `v4.0.0`.
No v4 tag is created or authorized by this document.

Frozen protocol and compatibility identities remain:

```text
v3 contract: 3
v3 package compatibility field: 3.2.0
v3 schema: shield.verdict.v1
v4 contract: 4
v4 schema: shield.verdict.v2
v4 canonicalization: shield-v4-canon.v1
v4 policy: policy.v1
v4 signature bundle: shield.signature_bundle.v1
v4 key registry: shield.key_registry.v1
v4 role: shield_component_qwg
```

## Signature evidence

| Path | Requirement | Profile | Evidence |
|---|---|---|---|
| `classical-ed25519` | required first | `rfc8032-ed25519-v1` | deterministic contract and negative tests |
| `ml-dsa` | required second | `fips204-ml-dsa-65-v1` | deterministic contract plus guarded ML-DSA-65 node |
| `fn-dsa` | optional last | `fips206-draft-falcon1024-v1` | deterministic contract plus guarded Falcon-1024 node |

Both required paths use strict AND semantics. Optional FN-DSA cannot replace or
rescue either required path. Present-invalid optional evidence is fatal.
Falcon-1024 remains draft evidence, not final FIPS 206 proof.

The producer emits canonical order without mutating caller input. The verifier
rejects noncanonical received order before trust lookup or cryptographic
verification.

## Frozen KAT evidence

```text
tests/fixtures/v4/component_verdict_policy_v1_kat.json
SHA-256: 176d9d8f7d16be456f2bf783c3031b65c46fd5f9efed1aba89d216b98406b0ff

tests/fixtures/v4/fn_dsa_signed_message_draft_profile_kat.json
SHA-256: b799b963cb46ccf579a0380cffeecd81f99fa616267e6d69fec4f2bf06e9f6ef
```

These bytes remain unchanged by V4.10-E1.

## Test evidence

Authenticated pre-E1 baseline:

```text
Python: 3.12.13
standard collection: 165 passed, 2 approved native-OQS skips
QWG statements in coverage baseline: 1,029
coverage requirement: 100 percent
```

Candidate-package evidence:

```text
Python: 3.11.15
standard suite: 175 passed, 2 approved native-OQS skips
QWG statements: 1,029 / 1,029
statement coverage: 100 percent
V4.10-E1 release-pack lock: 10 passed
```

The required post-commit proof is:

1. standard Python 3.11 CI green with 100 percent QWG statement coverage;
2. dedicated real-OQS workflow green;
3. guarded JUnit tests=2, skipped=0, failures=0, errors=0; and
4. fresh post-commit ZIP exact-scope verification.

The screenshot or workflow page is evidence of remote status. No persisted
JUnit archive SHA-256 is claimed.

## Authority proof

No path grants transaction signing, broadcast, consensus, key custody,
Orchestrator-receipt authority, AdamantineOS bypass, or final execution
authority. QWG signs or verifies only its component verdict evidence.
AdamantineOS remains the final fail-closed policy and execution boundary.

## Residuals

- Native workflows fetch liboqs and liboqs-python from floating default
  branches.
- Workflow actions retain mutable major tags.
- Standard CI enforces statement, not branch, coverage.
- Native provider tests use test keys and do not prove production custody or
  HSM assurance.
- FN-DSA/Falcon-1024 is a draft-profile path.

These residuals remain visible release inputs.

## Tag rule

Do not create or move `v4.0.0` based on this proof pack. Only an explicit
DarekDGB release decision after the complete V4.10 roadmap may authorize that
action.
