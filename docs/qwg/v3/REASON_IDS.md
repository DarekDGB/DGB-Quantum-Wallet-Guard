# DGB Quantum Wallet Guard - v3.2.0 Historical Reason IDs

Author attribution: DarekDGB
Status: frozen v3 compatibility registry

Every emitted v3 reason ID was required to be declared and test-covered for the
historical v3.2.0 release. Unknown reason IDs fail closed.

- `QWG_OK_POSTURE_ALLOW`
- `QWG_ESCALATE_QUANTUM_POSTURE`
- `QWG_DENY_KEY_RISK`
- `QWG_ERROR_INVALID_VERDICT`
- `QWG_ERROR_CONTEXT_HASH_MISMATCH`

The `4.0.0` distribution candidate does not rename or reinterpret these v3
compatibility identifiers.
