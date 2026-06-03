# DGB Quantum Wallet Guard — Shield v3.2.0 Manifest

Author attribution: DarekDGB

## Component Identity

- `component_id`: `qwg`
- `contract_version`: `3`
- `package_version`: `3.2.0`
- `output_schema_version`: `shield.verdict.v1`

## Supported Decisions

- `ALLOW`
- `ESCALATE`
- `DENY`
- `ERROR`
- `SKIPPED`

## Reason ID Registry

- `QWG_OK_POSTURE_ALLOW`
- `QWG_ESCALATE_QUANTUM_POSTURE`
- `QWG_DENY_KEY_RISK`
- `QWG_ERROR_INVALID_VERDICT`
- `QWG_ERROR_CONTEXT_HASH_MISMATCH`

## Evidence Family Registry

- `wallet_posture`
- `quantum_risk_context`
- `key_age_context`
- `dormancy_context`

## Authority Boundary

This component is evidence-only. It does not sign, broadcast, hold keys, expand authority, override the Orchestrator, or approve AdamantineOS execution directly.

## Orchestrator Role

The component verdict is input evidence only. Final Shield outcome must be produced by the Shield Orchestrator deterministic receipt.

## AdamantineOS Visibility

AdamantineOS must not consume this component directly. AdamantineOS consumes Shield only through one deterministic Orchestrator receipt.
