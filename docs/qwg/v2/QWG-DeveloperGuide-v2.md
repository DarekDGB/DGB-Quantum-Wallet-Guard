# 🛡 QWG Developer Guide — v2

Author: **DarekDGB (@Darek_DGB)**  
AI Engineering Assistant: **Angel**  
Status: **v2 – Developer Integration Guide**  
License: **MIT**

---

# 1. Introduction

The Quantum Wallet Guard (QWG) Developer Guide explains how to:

- integrate QWG into a DigiByte-aware application  
- feed events into the engine  
- interpret QRS (Quantum-Style Risk Score)  
- react to HIGH and CRITICAL classifications  
- run simulations and tests  
- connect QWG to Guardian Wallet v2, ADN v2 and Adaptive Core  

QWG is **non-invasive**: it does not modify consensus or digisignature behaviour.  
It provides **behaviour-based quantum-era risk analysis** on wallet activity.

---

# 2. Installation & Requirements

QWG is a pure Python package.  
Requirements:

- Python ≥ 3.10  
- pytest (for tests)  
- DigiByte data feed (your own app or node RPC)  

Clone the repository:

```
git clone https://github.com/DarekDGB/DigiByte-Quantum-Wallet-Guard
cd DigiByte-Quantum-Wallet-Guard
```

Run tests:

```
pytest -q
```

---

# 3. Core Components (Developer View)

### 3.1 QWGEngine
Main engine responsible for:

- timing analysis  
- UTXO pattern evaluation  
- QRS computation  
- pattern signature detection  
- policy enforcement  

### 3.2 RiskContext
State container for:

- timestamps  
- wallet relationships  
- previous flagged events  
- entropy signals  

### 3.3 Policies
Defines:

- thresholds: LOW, ELEVATED, HIGH, CRITICAL  
- pattern rules: DORMANT_KEY_SWEEP, MULTI_WALLET_DRAIN  

### 3.4 Decisions
Structured response with:

```
qrs_score: int
risk_level: str
pattern: Optional[str]
details: dict
```

---

# 4. Basic Integration Example

Minimal developer usage:

```python
from qwg.engine import QWGEngine
from qwg.risk_context import RiskContext

ctx = RiskContext()
engine = QWGEngine(risk_context=ctx)

result = engine.process_sweep_event(
    wallet_id="A",
    utxos_moved=5,
    amount_dgb=4200,
    destination="X1",
    timestamp=datetime.utcnow()
)

print(result.qrs_score, result.risk_level, result.pattern)
```

---

# 5. Event Types

QWG accepts structured *wallet behaviour events*.  
The core event model includes:

- **wallet_id**  
- **utxos_moved**  
- **amount_dgb**  
- **destination**  
- **timestamp**  

Developers transforming DigiByte RPC calls into QWG events must:

- ensure timestamp accuracy  
- correctly track per-wallet identifiers  
- preserve UTXO counts  

---

# 6. Pattern Detection Logic

### 6.1 Dormant Key Sweep
Triggered when dormant wallets move in rapid succession toward clustering destinations.

Developer checklist:

- map each event to wallet_id  
- track timing between events  
- maintain consistent timestamps  
- respect cross-wallet relationships  

### 6.2 Multi-Wallet Drain
Triggered when many active wallets drain simultaneously.

Checklist:

- maintain event ordering  
- detect window bursts  
- track destination entropy  

---

# 7. Deep Integration (Guardian Wallet, ADN, Adaptive Core)

### 7.1 Guardian Wallet v2
Guardian Wallet should:

- show warnings on HIGH  
- enforce delays on CRITICAL  
- require additional verification on CRITICAL  

QWG → Guardian flow:

```
QWG DecisionResult
       ↓
Guardian UX → warning, friction, or lock
```

### 7.2 ADN v2 (Autonomous Defense Node)
ADN can use QWG results to:

- lockdown RPC endpoints  
- throttle transactions  
- isolate node behaviour  

### 7.3 Adaptive Core
Adaptive Core learns from:

- DecisionResults  
- timing sequences  
- cluster labels  
- repeated attack scenarios  

Updates may change policies dynamically.

---

# 8. Running Simulation Scenarios

From repo root:

```
python examples/dormant_key_sweep_scenario.py
```

You will see:

- step-by-step event evaluation  
- evolving QRS  
- final CRITICAL risk  

This demonstrates real attack behaviour.

---

# 9. Writing Your Own QWG Scenarios

To create your own:

1. Create a dataclass representing your event  
2. Build a list of events in order  
3. Feed them into QWGEngine sequentially  
4. Log QRS and patterns  

Example template:

```python
events = [
    SweepEvent(1, 0,  "A", 10, 12000, "X1"),
    SweepEvent(2, 6,  "B", 7,  9000,  "X1"),
    SweepEvent(3, 12, "C", 5,  4200,  "X2")
]
```

---

# 10. Testing & CI

Tests included:

```
tests/test_engine.py
tests/test_policies.py
tests/test_decisions.py
tests/test_dormant_key_sweep.py
tests/test_adaptive_bridge.py
```

Run:

```
pytest -q
```

---

# 11. Deployment Recommendations

- Use staging/testnet before production  
- Store DecisionResult logs for auditing  
- Integrate Guardian Wallet for user-facing actions  
- Connect to ADN for node defence  
- Feed anonymised results into Adaptive Core  

---

# 12. Best Practices for Integrators

- Always maintain strict timestamp ordering  
- Never skip events — QWG relies on sequence integrity  
- Consider per-user or per-platform RiskContext isolation  
- Log all high-risk decisions  
- Merge with DQSN and Sentinel signals where possible  

---

# 13. Roadmap for Developers

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

**@Darek_DGB** on X  
