# Changelog

## v3.0.0 — Shield v3 Stabilisation

### Changed

- Bumped package version from `0.0.0` to `3.0.0`.
- Raised CI coverage gate from `qwg.v3` at 90% to full `qwg` package at 100%.
- Updated README, SECURITY, and v3 documentation to reflect the full-package v3.0.0 stabilisation standard.
- Added `py.typed` package marker for typed package consumers.

### Added

- Added coverage-lock tests for adapter fail-fast guards.
- Added coverage-lock tests for Adaptive Core bridge paths:
  - `None` sink no-op
  - direct `receive_threat_packet` path
  - `add_event` fallback path
  - defensive exception-swallowing paths
- Added coverage-lock tests for engine Adaptive Core emission and fail-safe behavior.
- Added coverage-lock tests for reason ID fallback mapping.
- Added coverage-lock tests for `RiskContext` helper methods.

### Security

- Locked optional Adaptive Core plumbing so it remains unable to break wallet decisions.
- Confirmed QWG remains a decision/verdict layer only, with no signing, broadcasting, or fund-movement authority.

