# 🛡 QWG Technical Specification — v2

## 1. Overview
Quantum Wallet Guard (QWG) is the Layer‑5 behavioural risk engine in the DigiByte Quantum Shield. 
It evaluates wallet activity, timing, UTXO structure, and cross‑wallet correlations to produce a Quantum‑Style Risk Score (QRS).

## 2. Core Modules
### 2.1 QWGEngine (engine.py)
- Entry point for all analysis.
- Methods:
  - `process_sweep_event(...)`
  - `evaluate_timing(...)`
  - `compute_qrs(...)`
- Outputs Decision object.

### 2.2 RiskContext (risk_context.py)
Tracks:
- event history
- timing deltas
- entropy
- wallet relationships

### 2.3 Policies (policies.py)
Defines thresholds:
- LOW: 0‑24
- ELEVATED: 25‑49
- HIGH: 50‑89
- CRITICAL: 90‑100

Pattern policies:
- DORMANT_KEY_SWEEP
- MULTI_WALLET_DRAIN

### 2.4 Decisions (decisions.py)
Object fields:
- qrs_score: int
- risk_level: str
- pattern: str | None

### 2.5 Adaptive Bridge (adaptive_bridge.py)
Optional integration:
- send policy updates
- receive global signals
- unify with Adaptive Core behaviour

## 3. Data Structures

### SweepEvent (example usage)
```
wallet_id: str
utxos_moved: int
amount_dgb: float
destination: str
timestamp: datetime
```

### DecisionResult
```
qrs_score: int
risk_level: str
pattern: Optional[str]
details: dict
```

## 4. QRS Calculation Logic
Inputs:
- timing burst intensity
- UTXO fragmentation
- destination clustering
- multi-wallet coordination
- prior flagged events
- external risk signals

Process:
1. Calculate timing anomaly score  
2. Evaluate UTXO structure  
3. Detect pattern signatures  
4. Apply policy thresholds  
5. Produce final DecisionResult  

## 5. Pattern Detection

### 5.1 DORMANT_KEY_SWEEP
Triggered when:
- multiple long‑inactive wallets move within a short window
- amounts fall within correlated ranges
- destinations cluster to 1–2 aggregation addresses
- sequence acceleration is present

### 5.2 MULTI_WALLET_DRAIN
Triggered when:
- many active wallets drain simultaneously
- destination diversity drops
- amounts appear tightly correlated

## 6. Integration Flow
1. Instantiate RiskContext  
2. Instantiate QWGEngine(risk_context)  
3. Feed events sequentially  
4. Parse DecisionResult  
5. If risk == CRITICAL:  
   - Guardian Wallet triggers friction  
   - ADN v2 may lockdown  
   - DQSN v2 may escalate network‑wide score  

## 7. Example Event Flow
Included in:
- examples/dormant_key_sweep_scenario.py  
- tests/test_dormant_key_sweep.py  

File demonstrates:
- QRS evolution
- CRITICAL escalation
- pattern detection tag

## 8. Test Coverage
### Covered:
- engine logic  
- policies thresholds  
- decision object behaviour  
- dormant key sweep scenario  

### Command:
```
pytest -q
```

## 9. Performance Expectations
- Single event eval < 3 ms  
- Context memory < 1 MB typical  
- Suitable for exchanges and Guardian Wallet integrations  

## 10. Roadmap
- more pattern signatures  
- PQC‑specific heuristics  
- adaptive policy tuning  
- deeper Sentinel/DQSN integration  

## 11. Licensing
MIT — free for DigiByte ecosystem and all chains.
