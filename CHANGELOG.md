# Changelog - DGB Quantum Wallet Guard

All notable changes to this repository are documented here.

Tests and normative contract documents define truth. Release notes do not
grant authority or replace the controlled release gates.

## 4.0.0 Candidate - Unreleased

Status: controlled pre-release. Candidate tag: `v4.0.0`. Tag created: no.

### Added

- Added the parallel Shield v4 component-verdict, signature-bundle, and QWG
  trust-profile surfaces.
- Added required classical Ed25519 and ML-DSA evidence under `policy.v1`.
- Added optional-last FN-DSA/Falcon-1024 draft-profile evidence with strict
  no-rescue behavior.
- Added deterministic shared KATs, real-backend adapters, and guarded native
  liboqs ML-DSA/Falcon-1024 proof nodes.
- Added the v4 proof pack, release-status record, and release-pack lock tests.

### Changed

- Aligned package metadata and active public documentation to the `4.0.0`
  candidate.
- Preserved every v3 protocol, schema, and compatibility identity unchanged.
- Historicized the old v3.2.0 pending-tag wording without rewriting release
  history.
- Aligned the contract, manifest, test matrix, and real-backend documentation
  with canonical bundle order and current evidence.

### Security

- Required canonical order: `classical-ed25519`, `ml-dsa`, then optional
  `fn-dsa`.
- Required both classical and ML-DSA paths; optional FN-DSA cannot replace or
  rescue a required path.
- Preserved QWG-only role and key separation.
- Preserved no transaction signing, no broadcast, no key custody, no consensus
  change, no Orchestrator bypass, and no final authority.

### Release gate

This entry does not announce a release. Remaining V4.10 component, verifier,
compatibility, full-system, adversarial, hash, attribution, fresh-ZIP, and
release-decision gates remain controlling. Only DarekDGB may authorize creation
or movement of the `v4.0.0` tag.

## v3.2.0 - Manifest / Verdict / Orchestrator Boundary Hardening

The `v3.2.0` release and its documents are historical evidence. The checklist
below records the pre-release controls that governed that release.

### Added

- Added the Shield v3.2.0 manifest, registries, and canonical verdict lock.
- Added stable reason ID and evidence-family documentation.
- Added v3.2.0 proof-pack and test-matrix documentation.
- Added Orchestrator-first handoff language for AdamantineOS integration.

### Changed

- Set package metadata to `3.2.0` for that historical release.
- Clarified that raw QWG output was evidence, not final signing, execution, or
  approval authority.

### Historical release gate

The controlled v3.2.0 process required green CI, complete registry and proof
documents, a fresh-ZIP audit, authorized bypass review, and no unresolved
critical or high finding.

## v3.1.0 - Shield Hardening Baseline

- Hardened the Shield v3 contract and regression coverage.
- Preserved deterministic, fail-closed wallet-safety behavior.

## v3.0.0 - Stable Shield v3 Baseline

- Added the stable QWG v3 deterministic wallet-safety contract.

Copyright 2025 DarekDGB
