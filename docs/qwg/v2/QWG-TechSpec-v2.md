# 🛡 QWG Technical Specification — v2

Author: **DarekDGB**

> **Control notice:** This v2 specification is historical and
> non-authoritative. The executable QWG-SIM-001 dormant-sweep prototype is
> formally retired and is not part of the current API. Neither this document
> nor QWG grants wallet action, execution, signing, broadcast or DigiByte
> consensus authority.

## 1. Overview

Quantum Wallet Guard (QWG) is a transaction-policy decision component in the
DigiByte Quantum Shield. It evaluates a caller-supplied `RiskContext` and
returns a structured decision. It does not sign or broadcast transactions,
change DigiByte consensus, or grant execution authority.

The earlier dormant-key-sweep design is formally retired as an executable
scenario. It remains documentation-only threat analysis and is not a current
runtime capability.

## 2. Core Modules

### 2.1 DecisionEngine (`engine.py`)

- Entry point for transaction-policy evaluation.
- Public methods:
  - `evaluate_transaction(ctx)`
  - `evaluate_transaction_v3(ctx)`
- Returns `DecisionResult` for the v2 path and a deterministic verdict envelope
  for the v3 wrapper.

### 2.2 RiskContext (`risk_context.py`)

Carries a transaction-scoped snapshot of:

- Sentinel and ADN risk levels
- DQSN network score
- wallet balance and transaction amount
- address age
- behaviour score and device-trust data
- optional integration metadata

It does not maintain multi-wallet sweep history or destination-clustering
state.

### 2.3 Policies (`policies.py`)

`WalletPolicy` defines:

- full-balance protection
- normal-risk and high-risk transaction-ratio limits
- maximum allowed external risk
- warning and delay cooldowns
- behaviour and trusted-device controls
- extra-authentication amount threshold

### 2.4 Decisions (`decisions.py`)

`Decision` values:

- `ALLOW`
- `WARN`
- `DELAY`
- `BLOCK`
- `REQUIRE_EXTRA_AUTH`

`DecisionResult` carries the decision, reason, optional stable reason ID,
cooldown, suggested limit, and extra-authentication flags.

### 2.5 Adaptive Bridge (`adaptive_bridge.py`)

Optional integration that emits a generic event or ThreatPacket-shaped
dictionary to a caller-supplied sink. The bridge does not import Adaptive Core,
and failures in optional telemetry do not change the wallet decision.

## 3. Data Structures

### RiskContext

```text
sentinel_level: RiskLevel
dqs_network_score: float
adn_level: RiskLevel
wallet_balance: float
tx_amount: float
address_age_days: int | None
behaviour_score: float
device_id: str | None
trusted_device: bool
```

### DecisionResult

```text
decision: Decision
reason: str
reason_id: str | None
cooldown_seconds: int | None
suggested_limit: float | None
require_confirmation: bool
require_second_factor: bool
```

## 4. Decision Evaluation Order

1. Block on critical Sentinel or ADN risk.
2. Delay when external risk exceeds wallet policy.
3. Block a configured near-full-balance send.
4. Require extra authentication above the configured amount.
5. Apply transaction-to-balance ratio limits.
6. Warn on configured behaviour or device risk.
7. Otherwise allow.

This ordered rule set is the current v2 decision contract. It does not compute
a multi-wallet Quantum-Style Risk Score or assign dormant-sweep pattern labels.

## 5. Retired Dormant-Key-Sweep Design

QWG-SIM-001 described a hypothetical sequence of long-dormant wallets moving
funds to clustered destinations. The proposed multi-event analytics runtime was
never implemented in the current engine. Its former example and test are
formally retired and must not be cited as coverage, runtime behaviour or proof
of attack detection.

The scenario document may still be used as a conceptual threat-analysis input
for future design work. A future implementation would require a separately
reviewed data contract, runtime, tests and evidence.

## 6. Integration Flow

1. Construct and validate a transaction-scoped `RiskContext`.
2. Instantiate `DecisionEngine`, optionally with an explicit `WalletPolicy`.
3. Call `evaluate_transaction(ctx)`.
4. Interpret the returned `DecisionResult` under the integrator's own policy.
5. Keep transaction signing, broadcast and final execution authority outside
   QWG.

## 7. Current Example Flow

The maintained basic example is:

```text
python -m examples.basic_usage
```

It demonstrates ordinary transaction-context evaluation. No maintained example
implements the retired dormant-key-sweep design.

## 8. Test Coverage

Current v2-facing coverage includes engine rules, policy configuration,
decision objects and Adaptive Core bridge behaviour. The retired design
scenario is not an executed test surface.

Run:

```text
pytest -q
```

## 9. Performance Expectations

No latency or memory service-level guarantee is defined by this specification.
Integrators must benchmark the exact release, Python runtime and deployment
environment they intend to use.

## 10. Roadmap

- reviewed transaction-context schemas
- additional deterministic policy rules
- deeper Sentinel and DQSN signal integration
- separately specified behavioural analytics where justified by implemented
  code and tests

Roadmap items are proposals, not current capabilities.

## 11. Licensing

MIT — free for the DigiByte ecosystem and all chains.

