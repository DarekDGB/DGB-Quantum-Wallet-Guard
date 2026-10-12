# QWG Shield v4.0.0 Release Status

Status: CONTROLLED PRE-RELEASE
Release decision: NOT YET AUTHORIZED
Distribution version: 4.0.0
Candidate tag: v4.0.0
Tag created: no
Author attribution: DarekDGB

## Current state

V4.10-E1 aligned the QWG distribution and release pack to the coordinated
Shield `4.0.0` candidate. Its post-commit gate is verified at
`ad728421c5a8866a0c914bec927009fab39c04bb`.

V4.10-I2 prepares QWG's final native evidence workflow with immutable provider
sources, exact-node JUnit enforcement, and retained proof artifacts. It awaits
the QWG post-commit workflow, artifact, and fresh-ZIP gate. It does not announce
a release and does not authorize a tag.

The candidate preserves the frozen v3 compatibility surface and all v4
protocol identities. The E1 change was release truth, documentation, and
regression locking. I2 changes native proof infrastructure and evidence
documentation. Neither changes runtime cryptographic behavior, schemas,
fixtures, or authority.

## Candidate controls

- Required classical Ed25519 and ML-DSA paths remain strict AND.
- Optional FN-DSA/Falcon-1024 remains optional-last draft evidence.
- Optional evidence cannot replace or rescue either required path.
- Canonical signature order is enforced before trust or crypto work.
- Trust remains role-separated to `shield_component_qwg`.
- Shared component and FN-DSA KAT fixture bytes remain frozen.
- Standard CI requires 100 percent QWG statement coverage.
- Dedicated real-OQS proof requires exactly two native nodes with zero skips,
  failures, or errors.

The exact policy order is `classical-ed25519`, `ml-dsa`, then optional
`fn-dsa` under `fips206-draft-falcon1024-v1`. Optional FN-DSA cannot replace
or rescue either required path and is not final FIPS 206 proof.

## Authority boundary

QWG does not sign or broadcast transactions, hold wallet keys, change DigiByte
consensus, approve execution, produce the final Shield receipt, bypass the
Shield Orchestrator, or override AdamantineOS.

AdamantineOS remains the final fail-closed policy and execution boundary.

## Remaining roadmap gates

V4.10-A through H: verified for their recorded source snapshots.
V4.10-I1: Orchestrator and its path-initialization FIX1 verified at
`ad36f5a3050557c2ea8dd8f228a97a85d5313818`.
V4.10-I2: QWG package prepared; both final-commit workflows, retained exact
two-node native artifact, fresh source ZIP, and QWG H-row refresh pending.
V4.10-I3 through I7: subsequent repositories not started.
V4.10-J: final negative matrix and adversarial audit pending.
V4.10-K: final hashes, attribution, and fresh-ZIP lock pending.
V4.10-L: final release decision pending.

## Release rule

Do not create or move `v4.0.0`. A green repository, a candidate version, or a
completed V4.10-E1 package is not release authorization. Only an explicit
DarekDGB decision after the complete V4.10 roadmap may authorize the tag.
