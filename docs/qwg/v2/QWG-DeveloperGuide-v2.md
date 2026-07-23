# 🛡 QWG Developer Guide — v2

Author: **DarekDGB**
Status: **v2 – Historical developer guide**
License: **MIT**

> **Control notice:** This v2 document is historical and non-authoritative.
> The executable QWG-SIM-001 dormant-sweep prototype is formally retired and
> is not part of the current API. Neither this document nor QWG grants wallet
> action, execution, signing, broadcast or DigiByte consensus authority.

---

# 1. Introduction

The Quantum Wallet Guard (QWG) Developer Guide explains how to:

- integrate QWG into a DigiByte-aware application
- evaluate a transaction-scoped risk context
- interpret `DecisionResult` values
- handle warnings, delays, blocks and extra-authentication requests
- review the examples and tests named by this historical guide
- connect QWG to Guardian Wallet v2, ADN v2 and Adaptive Core

QWG is **non-invasive**: it does not modify consensus or DigiByte signature
behaviour, sign transactions or broadcast transactions. It evaluates supplied
wallet, transaction, device and external-risk signals under local policy.

---

# 2. Installation & Requirements

QWG is a pure Python package.
Requirements:

- Python ≥ 3.11
- pytest (for tests)
- an integration-specific source for validated `RiskContext` values

Clone the repository:

```
git clone https://github.com/DarekDGB/DGB-Quantum-Wallet-Guard
cd DGB-Quantum-Wallet-Guard
```

Run tests:

```
pytest -q
```

---

# 3. Core Components (Developer View)

### 3.1 DecisionEngine
Main engine responsible for applying ordered wallet-policy rules to a
transaction-scoped `RiskContext` and returning a `DecisionResult`.

### 3.2 RiskContext
Transaction snapshot containing:

- Sentinel and ADN risk levels
- DQSN network score
- wallet balance and transaction amount
- address age, behaviour score and device-trust signals

### 3.3 Policies
Defines wallet-level limits, including transaction ratios, maximum external
risk, cooldowns, full-balance protection and the extra-authentication amount.

### 3.4 Decisions
Structured response with:

```
decision: Decision
reason: str
reason_id: Optional[str]
cooldown_seconds: Optional[int]
suggested_limit: Optional[float]
require_confirmation: bool
require_second_factor: bool
```

---

# 4. Basic Integration Example

Minimal developer usage:

```python
from qwg.engine import DecisionEngine
from qwg.risk_context import RiskContext, RiskLevel

ctx = RiskContext(
    wallet_balance=1_000.0,
    tx_amount=50.0,
    sentinel_level=RiskLevel.NORMAL,
    adn_level=RiskLevel.NORMAL,
)
engine = DecisionEngine()

result = engine.evaluate_transaction(ctx)

print(result.decision.value, result.reason, result.reason_id)
```

---

# 5. Transaction Context Inputs

QWG accepts a `RiskContext` supplied by the integrating application. Core
inputs include:

- **sentinel_level** and **adn_level**
- **dqs_network_score**
- **wallet_balance** and **tx_amount**
- **address_age_days**
- **behaviour_score** and **trusted_device**

The integration is responsible for validating and supplying these values.
The current v2 runtime does not accept a multi-wallet sweep-event model.

---

# 6. Decision Logic and Retired Design Scenario

### 6.1 Current decision rules

`DecisionEngine.evaluate_transaction(...)` checks external critical risk,
policy-risk limits, near-full-balance sends, extra-authentication thresholds,
transaction-to-balance ratios, behaviour score and device trust. Rule order is
part of the observable behaviour and is covered by the current test suite.

### 6.2 Retired dormant-key-sweep design

The earlier QWG-SIM-001 design proposed multi-wallet event sequencing,
destination clustering and a `DORMANT_KEY_SWEEP` label. The proposed API is
not part of the current runtime. Its former example and test are formally
retired and must not be used as implementation, coverage or validation
evidence. The scenario document is
retained only as conceptual, historical threat analysis.

---

# 7. Deep Integration (Guardian Wallet, ADN, Adaptive Core)

### 7.1 Guardian Wallet v2
An integrating wallet can present the returned `ALLOW`, `WARN`, `DELAY`,
`BLOCK` or `REQUIRE_EXTRA_AUTH` decision and its reason. The wallet remains
responsible for validating the evidence and deciding whether any action is
appropriate.

QWG → Guardian flow:

```
QWG DecisionResult
       ↓
Guardian policy → independently authorised UX or wallet action
```

### 7.2 ADN v2 (Autonomous Defense Node)
An ADN integration may consume QWG evidence under its own policy. A
`DecisionResult` does not authorise an RPC lockdown, throttling, isolation or
any other node action.

### 7.3 Adaptive Core
The optional bridge can emit a best-effort decision event or
ThreatPacket-shaped dictionary to a caller-supplied sink. The current bridge
does not produce dormant-sweep timing sequences, cluster labels or scenario
training data. Any learning or policy update is outside this component and
requires explicit validation by the integrating system.

---

# 8. Running Current Examples

From the repository root, run the maintained basic example:

```
python -m examples.basic_usage
```

The retired dormant-key-sweep scenario is not runnable and is not evidence of
real attack detection.

---

# 9. Writing Your Own QWG Scenarios

To create your own:

1. Build explicit `RiskContext` values for the policy paths under review.
2. Evaluate each context with `DecisionEngine`.
3. Assert the exact decision and stable reason identifier.
4. Keep synthetic demonstrations separate from production claims.

Example template:

```python
contexts = [
    RiskContext(wallet_balance=1_000.0, tx_amount=50.0),
    RiskContext(wallet_balance=1_000.0, tx_amount=999.0),
]
results = [DecisionEngine().evaluate_transaction(ctx) for ctx in contexts]
```

---

# 10. Testing & CI

Tests included:

```
tests/test_engine.py
tests/test_policies.py
tests/test_decisions.py
tests/test_adaptive_bridge.py
```

Run:

```
pytest -q
```

---

# 11. Deployment Preconditions

- Verify the exact release, tests and controlled evidence under review.
- Validate every integration input and fail closed on malformed evidence.
- Keep final wallet, node, signing and broadcast authority in the integrating
  component.
- Treat optional Adaptive Core emission as telemetry, not execution authority.
- Complete independent staging and security review before production use.

---

# 12. Best Practices for Integrators

- Validate every value used to construct `RiskContext`.
- Treat `DecisionResult` as evidence for an integrating policy, not as
  transaction-signing or broadcast authority.
- Log non-allow decisions and stable reason identifiers.
- Merge with DQSN and Sentinel signals where possible

---

# 13. Roadmap for Developers

The following items are historical proposals, not implemented capabilities:

- JSON schema for QWG events
- WebSocket real-time interface
- Enterprise multi-wallet monitoring module
- PQC-aware heuristics
- Multi-chain support (Litecoin, Dogecoin, Bitcoin)
- Adaptive Core dynamic policy injection

---

# 14. License

MIT — free for all chains, free for DigiByte ecosystem.

---

# 15. Contact

For technical questions, integration help, or contributions:

**DarekDGB**

