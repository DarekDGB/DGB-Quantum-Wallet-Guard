# Changelog — DGB Quantum Wallet Guard

All notable changes to this repository are documented here.

The format follows a simple release-note style suitable for Shield component audit and release review.

---

## v3.2.0 — Manifest / Verdict / Orchestrator Boundary Hardening

### Added

- Added Shield v3.2.0 manifest / registry / canonical verdict lock.
- Added deterministic component identity discipline for QWG.
- Added stable reason ID registry documentation.
- Added stable evidence-family registry documentation.
- Added v3.2.0 proof-pack documentation.
- Added v3.2.0 test matrix documentation.
- Added v3.2.0 manifest/verdict lock tests.
- Added Orchestrator-first handoff language for AdamantineOS integration.

### Changed

- Updated package metadata to `3.2.0`.
- Updated README to make v3.2.0 the current integration-boundary hardening surface.
- Updated security policy to state that QWG verdicts are evidence only.
- Clarified that AdamantineOS must consume Shield decisions through the deterministic Shield Orchestrator receipt only.
- Clarified that raw QWG output is not final signing, execution, or approval authority.

### Security

- Reinforced fail-closed handling for malformed or unsafe verdict data.
- Reinforced no-key-custody boundary.
- Reinforced no signing, no broadcasting, no consensus modification, and no hidden authority.
- Reinforced that Shield `ALLOW` only permits AdamantineOS to continue its own checks.
- Locked v3.2.0 release readiness behind final roadmap checklist, CI proof, fresh ZIP audit, and Red Team report.

### Release Gate

Do **not** tag v3.2.0 until:

- roadmap checklist is complete
- tests pass locally or in CI
- coverage gate remains satisfied
- manifest / reason ID / evidence-family docs are aligned
- verdict boundary tests pass
- Orchestrator receipt boundary is respected
- final fresh ZIP audit is complete
- Red Team report is complete
- no docs-vs-tests mismatch remains

---

## v3.1.0 — Shield Hardening Baseline

### Added

- Hardened Shield v3 contract behavior.
- Strengthened regression coverage.
- Preserved deterministic wallet-safety behavior.
- Preserved fail-closed safety expectations.

### Security

- No consensus authority added.
- No signing authority added.
- No broadcasting authority added.
- No private-key custody added.

---

## v3.0.0 — Stable Shield v3 Baseline

### Added

- Stable QWG v3 baseline.
- Deterministic wallet safety contract behavior.
- Fail-closed wallet guard behavior.
- CI coverage gate for release confidence.

---

## Notes

Tests define truth.

Documentation must not claim behavior that tests do not enforce.

© 2025 DarekDGB
