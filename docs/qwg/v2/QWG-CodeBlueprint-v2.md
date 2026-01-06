# 🛡 QWG Code Blueprint — v2

Author: **DarekDGB (@Darek_DGB)**  
AI Engineering Assistant: **Angel**  
Status: **v2 – Code-Level Blueprint**  
License: **MIT**

---

## 1. Purpose of This Document

This blueprint gives DigiByte core developers, security engineers and integrators a
**file-by-file view** of the Quantum Wallet Guard (QWG) codebase.

It explains:

- what each module does  
- how components depend on each other  
- where to extend or hook into the system  
- how examples and tests are structured  

If you are reviewing the project for testnet or integration, this is the
map of the entire Layer-5 engine.

---

## 2. Top-Level Layout

```text
.github/workflows/
    ci.yml

examples/
    adaptive_core_bridge_example.py
    basic_usage.py
    behaviour_and_device.py
    dormant_key_sweep_scenario.py
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
    test_dormant_key_sweep.py
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
- Typically re-exports:
  - `QWGEngine`
  - `RiskContext`
  - key enums / decision types

Integration code may choose between:

```python
from qwg import QWGEngine, RiskContext
# or
from qwg.engine import QWGEngine
from qwg.risk_context import RiskContext
```

---

### 3.2 `engine.py`

**Role:** Central risk engine for QWG.

Key responsibilities:

- Accepts structured events (e.g. sweep-like wallet movements).  
- Calls into `RiskContext` to read/update state.  
- Evaluates policies defined in `policies.py`.  
- Produces a `Decision` / `DecisionResult` with:
  - `qrs_score`
  - `risk_level`
  - `pattern` (e.g. `DORMANT_KEY_SWEEP`)
  - optional `details`.

Typical flow inside:

1. Normalise event data.  
2. Update context (timing, history, wallet links).  
3. Compute raw metrics (timing bursts, clustering, etc.).  
4. Call policy helpers to derive scores and pattern tags.  
5. Convert to final decision object from `decisions.py`.  
6. Optionally pass event + decision to `adaptive_bridge.py`.

Extension points:

- Add new engine methods for additional event types.  
- Add new scoring factors and include them in QRS.  

---

### 3.3 `risk_context.py`

**Role:** Holds **state across multiple events**.

Tracks, for example:

- last timestamp per wallet  
- global and per-wallet event history  
- correlation information (e.g. sets of related wallets)  
- previously flagged patterns / warnings  

This object is intentionally separate from the engine so that:

- one context can be reused across many calls  
- environments (exchange, wallet app) can decide scoping:
  - per user
  - per session
  - per cluster of wallets

Extension points:

- add additional fields to track new styles of patterns  
- extend context to store cross-chain or cross-service data  

---

### 3.4 `policies.py`

**Role:** Encodes QWG’s **policy rules** and thresholds.

Contains logic for:

- mapping raw metrics → QRS (0–100)  
- deriving `LOW / ELEVATED / HIGH / CRITICAL` boundaries  
- tagging patterns such as:
  - `DORMANT_KEY_SWEEP`
  - `MULTI_WALLET_DRAIN` (if present)
- combining multiple signals into a final policy decision.

Typical usage (internally):

```python
score, level, pattern = evaluate_policies(context, metrics)
```

This file is the primary target for:

- Adaptive Core adjustments  
- human operator tuning  
- adding new pattern definitions  

---

### 3.5 `decisions.py`

**Role:** Defines the structured **results** returned by QWG.

Common fields:

- `qrs_score: int` — Quantum-Style Risk Score (0–100).  
- `risk_level: str` — `LOW`, `ELEVATED`, `HIGH`, `CRITICAL`.  
- `pattern: Optional[str]` — pattern tag if matched.  
- `details: dict` — optional extra metrics or debug info.

By keeping this in a single module:

- logs and integrations are consistent  
- tests can assert against a stable interface  
- developers can serialise decisions into JSON easily.

Example:

```python
result.qrs_score   # 92
result.risk_level  # "CRITICAL"
result.pattern     # "DORMANT_KEY_SWEEP"
```

---

### 3.6 `adaptive_bridge.py`

**Role:** Connects QWG to the **Adaptive Core**.

Responsibilities:

- serialising selected events + decisions into a format suitable for
  Adaptive Core ingestion  
- possibly receiving updated thresholds or policy parameters in future
  versions  
- defining event types that Adaptive Core expects (e.g. schema-like).

In v2, this file formulates the “bridge contract” between:

- local, per-instance QWG engines  
- the network-wide learning / adaptation layer.

Extension points:

- plug in message queues or pub/sub for larger deployments  
- encrypt or sign outgoing data if used over open networks  

---

## 4. Examples (`examples/`)

These scripts are **self-contained demonstrations** of QWG behaviour.
They are meant for:

- human understanding  
- initial integration testing  
- regression scenarios  

### 4.1 `basic_usage.py`

Shows:

- how to initialise `RiskContext` and `QWGEngine`  
- how to feed a simple event  
- how to print `qrs_score`, `risk_level`, `pattern`.

Ideal starting point for new developers.

---

### 4.2 `behaviour_and_device.py`

Demonstrates:

- how session / device information could be attached to events  
- how RiskContext can be extended to track extra context (e.g. device
  fingerprints, app IDs)  
- how this influences QRS and pattern tagging.

This is a template for integration with Guardian Wallet v2 or
device-aware infrastructure.

---

### 4.3 `high_risk_scenario.py`

Shows a synthetic scenario where behaviour escalates quickly to
`HIGH` or `CRITICAL`.

Useful for:

- validating end-to-end wiring  
- showing integrators what “bad” flows look like in logs.  

---

### 4.4 `adaptive_core_bridge_example.py`

Demonstrates how:

- QWG decisions can be passed through `adaptive_bridge.py`  
- payloads might be sent to Adaptive Core  
- identifiers and risk labels can be carried across.

This is a concrete reference for any system that wants to actually wire
QWG + Adaptive Core.

---

### 4.5 `dormant_key_sweep_scenario.py`

Implements **QWG-SIM-001**, the **Dormant Key Sweep** scenario described
in `QWG-QuantumAttackScenario-1.md`.

Key points:

- multiple wallets (`A`, `B`, `C`)  
- many UTXOs  
- aggregation to `X1`, `X2`  
- timeline in minutes from a start time  
- expected QRS escalation into `CRITICAL`.

Developers can run:

```bash
python examples/dormant_key_sweep_scenario.py
```

and observe:

- when the pattern is detected  
- how `qrs_score` moves with each event  
- how logs would look in a real system.

---

## 5. Tests (`tests/`)

The tests guarantee that the core behaviour of QWG remains stable as
code evolves.

### 5.1 `test_engine.py`

- Validates engine wiring and main execution paths.  
- Ensures basic QRS calculation works end-to-end.  
- Guards against breaking changes in engine signatures.

---

### 5.2 `test_policies.py`

- Checks that policy boundaries for `LOW`, `ELEVATED`, `HIGH`,
  `CRITICAL` are honoured.  
- Confirms that pattern tags are assigned correctly based on synthetic
  inputs.  

When updating `policies.py`, this file must pass green.

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

### 5.5 `test_dormant_key_sweep.py`

- Implements the test for QWG-SIM-001 scenario.  
- Feeds a sequence of events equivalent to the example scenario.  
- Asserts that:
  - QRS reaches a high range (e.g. ≥90), or  
  - risk level is `CRITICAL`,  
  - pattern is correctly tagged.

This test is a key indicator that the dormant key sweep detection logic
has not degraded.

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

Technical details:

- QRS computation  
- core APIs  
- data models  
- pattern definitions  
- integration flows  

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

Canonical specification for the **Dormant Key Sweep** scenario:

- timeline  
- wallets and destinations  
- value distribution  
- rationale for its structure  

This file is the reference behind the example + test.

---

## 8. Extension Points

Developers who want to extend QWG can focus on:

- `policies.py` for new pattern definitions  
- `risk_context.py` for additional state tracking  
- `adaptive_bridge.py` for richer integration  
- new examples and tests for emerging scenarios  

Any changes should:

- keep `decisions.py` stable as a public contract  
- maintain a clear, explainable path from raw events to QRS  
- preserve test coverage and CI green status.

---

## 9. Conclusion

This blueprint shows how each part of QWG v2 fits into the overall
architecture.

For deeper explanation of concepts and design choices, see:

- `QWG_Whitepaper_v2.md`  
- `QWG-TechSpec-v2.md`  
- `QWG-DeveloperGuide-v2.md`  
- `QWG-Adaptive-Core-Integration-v2.md`  

For practical understanding, run:

```bash
python examples/dormant_key_sweep_scenario.py
pytest -q
```

For questions or collaboration:

**@Darek_DGB** on X.
