# 🛡 QWG Code Blueprint — v2

Author: **DarekDGB**
Status: **v2 – Historical code snapshot**
License: **MIT**

> **Control notice:** This v2 document is historical and non-authoritative.
> The executable QWG-SIM-001 dormant-sweep prototype is formally retired and
> is not part of the current API. Neither this document nor QWG grants wallet
> action, execution, signing, broadcast or DigiByte consensus authority.

---

## 1. Purpose of This Document

This blueprint preserves a **historical v2-oriented snapshot** of selected
Quantum Wallet Guard (QWG) files. It is not a complete or authoritative map of
the current repository; current source, manifests and tests take precedence.

It explains:

- the intended role of selected v2 modules
- the historical relationships between those components
- the example and test structure recorded at that time
- corrected retirement boundaries for QWG-SIM-001

Do not use this snapshot to infer that a listed path or capability remains in a
later release.

---

## 2. Historical Top-Level Layout Snapshot

The following list is retained to show the v2-oriented structure covered by
this document. It is intentionally not a complete current inventory.

```text
.github/workflows/
    ci.yml

examples/
    adaptive_core_bridge_example.py
    basic_usage.py
    behaviour_and_device.py
    high_risk_scenario.py

src/qwg/
    __init__.py
    adaptive_bridge.py
    decisions.py
    engine.py
    policies.py
    risk_context.py

tests/
    test_adaptive_bridge.py
    test_decisions.py
    test_engine.py
    test_policies.py

QWG-Adaptive-Core-Integration-v2.md
QWG-CodeBlueprint-v2.md
QWG-DeveloperGuide-v2.md
QWG-QuantumAttackScenario-1.md
QWG-TechSpec-v2.md
QWG_Whitepaper_v2.md
LICENSE
README.md
```

---

## 3. Core Engine Modules (`src/qwg/`)

### 3.1 `__init__.py`

- Exposes the public API for `qwg` as a package.
- Re-exports:
  - `DecisionEngine`
  - `RiskContext`
  - `RiskLevel`
  - `WalletPolicy`
  - `Decision` and `DecisionResult`

Integration code may choose between:

```python
from qwg import DecisionEngine, RiskContext
# or
from qwg.engine import DecisionEngine
from qwg.risk_context import RiskContext
```

---

### 3.2 `engine.py`

**Role:** Policy-driven transaction decision engine for QWG.

Key responsibilities:

- Accepts a transaction-scoped `RiskContext` snapshot.
- Evaluates the ordered rules configured by `WalletPolicy`.
- Returns a `DecisionResult` containing the decision, stable reason, and any
  cooldown, suggested limit or extra-authentication flags.
- Can emit a best-effort Adaptive Core event when the supplied context has a
  compatible adaptive sink.
- Provides a deterministic v3 verdict wrapper without changing the underlying
  v2 decision logic.

Typical flow inside:

1. Inspect Sentinel and ADN risk levels.
2. Apply the configured wallet-risk ceiling.
3. Check full-balance, extra-authentication and transaction-ratio rules.
4. Check behaviour and trusted-device signals.
5. Return a structured result from `decisions.py`.
6. Optionally emit the decision through `adaptive_bridge.py`.

Extension points:

- Add new rules only with matching policy fields and tests.
- Keep rule ordering and stable reason identifiers explicit.

The retired multi-wallet sweep-event API is not part of the current codebase.

---

### 3.3 `risk_context.py`

**Role:** Holds the security-signal snapshot for one transaction decision.

It carries, for example:

- Sentinel and ADN risk levels
- the DQSN network score
- wallet balance and transaction amount
- address age, behaviour score and trusted-device state
- optional metadata used by integrations

The current class does not maintain sweep history, wallet graphs or
destination-clustering state.

Extension points:

- add security signals only with deterministic handling and tests
- preserve the existing defaults and serialisable v3 context surface

---

### 3.4 `policies.py`

**Role:** Encodes QWG’s **policy rules** and thresholds.

Defines `WalletPolicy`, including:

- full-balance protection
- normal-risk and high-risk transaction-ratio limits
- the maximum permitted external risk level
- warning and delay cooldowns
- behaviour and trusted-device controls
- the extra-authentication amount threshold.

Typical usage:

```python
policy = WalletPolicy(max_tx_ratio_normal=0.25)
engine = DecisionEngine(policy=policy)
```

This file is the primary target for:

- explicit wallet-level configuration
- reviewed changes to the decision thresholds

---

### 3.5 `decisions.py`

**Role:** Defines the structured **results** returned by QWG.

`Decision` provides `ALLOW`, `WARN`, `DELAY`, `BLOCK` and
`REQUIRE_EXTRA_AUTH`. `DecisionResult` carries:

- `decision`
- `reason` and optional stable `reason_id`
- optional `cooldown_seconds` and `suggested_limit`
- confirmation and second-factor flags.

By keeping this in a single module:

- logs and integrations are consistent
- tests can assert against a stable interface
- developers can serialise decisions into JSON easily.

Example:

```python
result.decision
result.reason_id
result.cooldown_seconds
```

---

### 3.6 `adaptive_bridge.py`

**Role:** Connects QWG to the **Adaptive Core**.

Responsibilities:

- serialising selected decisions into a generic event or
  ThreatPacket-shaped dictionary
- accepting a caller-supplied sink without importing Adaptive Core
- failing quietly so optional telemetry cannot break wallet decisions.

In v2, this file formulates the “bridge contract” between:

- local, per-instance QWG engines
- the network-wide learning / adaptation layer.

Extension points:

- plug in message queues or pub/sub for larger deployments
- encrypt or sign outgoing data if used over open networks

---

## 4. Examples (`examples/`)

The historical snapshot included scripts intended for:

- human understanding
- initial integration testing
- regression scenarios

### 4.1 `basic_usage.py`

Shows:

- how to initialise `RiskContext` and `DecisionEngine`
- how to evaluate a transaction-scoped context
- how to print the returned decision and reason.

Ideal starting point for new developers.

---

### 4.2 `behaviour_and_device.py`

Demonstrates:

- how behaviour and trusted-device signals can be supplied in `RiskContext`
- how those inputs affect an ordered policy decision.

This is a template for integration with Guardian Wallet v2 or
device-aware infrastructure.

---

### 4.3 `high_risk_scenario.py`

Shows synthetic high-risk transaction context and the resulting policy
decision.

Useful for:

- validating end-to-end wiring
- showing integrators what “bad” flows look like in logs.

---

### 4.4 `adaptive_core_bridge_example.py`

Demonstrates how:

- QWG decisions can be passed through `adaptive_bridge.py`
- payloads might be sent to Adaptive Core
- identifiers and decision evidence can be carried across.

The example is illustrative. Any real integration must validate the current
bridge contract and keep Adaptive Core failures from changing wallet policy.

---

### 4.5 Retired QWG-SIM-001 artifact

The earlier dormant-key-sweep executable was based on a proposed
multi-event analytics API that was never implemented. It is formally retired
and is not part of the current examples. `QWG-QuantumAttackScenario-1.md`
remains only as a conceptual, historical threat-analysis document; it is not
an executable demonstration or evidence of detection behaviour.

---

## 5. Tests (`tests/`)

The selected tests recorded here exercise v2-oriented behaviour. Only the
actual test suite for a specific release can establish that release's tested
surface.

### 5.1 `test_engine.py`

- Validates engine wiring and main execution paths.
- Exercises ordered `DecisionEngine` rules and returned decisions.
- Guards against breaking changes in engine signatures.

---

### 5.2 `test_policies.py`

- Checks wallet-policy defaults and configured thresholds.
- Confirms the policy object exposes the values used by the engine.

Any policy change requires the relevant tests for that release to pass.

---

### 5.3 `test_decisions.py`

- Verifies behaviour of the decision classes / objects.
- Ensures defaults, equality semantics (if any), and fields remain
  consistent.

This is important so external integrators can rely on a stable decision
API.

---

### 5.4 `test_adaptive_bridge.py`

- Validates the format and handling in `adaptive_bridge.py`.
- Ensures outgoing payloads contain the required fields.
- Prevents accidental changes to the Adaptive Core contract.

---

### 5.5 Retired QWG-SIM-001 test

The former scenario test depended on the same nonexistent sweep-event API and
did not execute a current runtime path. It is formally retired and must not be
cited as coverage or proof of dormant-key-sweep detection. Any future
implementation requires a separately reviewed runtime contract and real tests.

---

## 6. CI Workflow (`.github/workflows/ci.yml`)

The CI file:

- installs dependencies
- runs the test suite via `pytest`
- can be extended later to run linting / type-checking.

Any pull request or commit should show **green CI** before being
considered for merge or testnet experimentation.

---

## 7. Documentation Files

### 7.1 `QWG_Whitepaper_v2.md`

High-level narrative:

- motivation
- threat model
- role in the 5-layer shield
- relationship to PQC
- roadmap and limitations

### 7.2 `QWG-TechSpec-v2.md`

Historical technical details, corrected to distinguish the implemented
transaction-decision API from the retired behavioural-analytics proposal.

### 7.3 `QWG-DeveloperGuide-v2.md`

Developer-focused:

- installation
- integration patterns
- example usage
- best practices
- deployment recommendations

### 7.4 `QWG-Adaptive-Core-Integration-v2.md`

Describes how:

- QWG produces data for Adaptive Core
- events and decisions are serialised and transported
- feedback from Adaptive Core might tune policies.

### 7.5 `QWG-QuantumAttackScenario-1.md`

Historical threat-analysis description for the retired **Dormant Key Sweep**
design scenario:

- timeline
- wallets and destinations
- value distribution
- rationale for its structure

This file is documentation only. It does not describe an implemented runtime,
and no maintained example or test is derived from it.

---

## 8. Extension Points

Developers who want to extend QWG can focus on:

- `policies.py` for reviewed wallet-policy changes
- `risk_context.py` for additional transaction-scoped signals
- `adaptive_bridge.py` for richer integration
- new examples and tests for emerging scenarios

Any changes should:

- keep `decisions.py` stable as a public contract
- maintain a clear, explainable path from context inputs to decisions
- preserve test coverage and CI green status.

---

## 9. Conclusion

This blueprint preserves a partial historical view of QWG v2. It must not be
used as a substitute for inspecting the source and tests of the release under
review.

For deeper explanation of concepts and design choices, see:

- `QWG_Whitepaper_v2.md`
- `QWG-TechSpec-v2.md`
- `QWG-DeveloperGuide-v2.md`
- `QWG-Adaptive-Core-Integration-v2.md`

Before running an example or test command, confirm the path and prerequisites
against the release under review.

Author and project contact: **DarekDGB**.

