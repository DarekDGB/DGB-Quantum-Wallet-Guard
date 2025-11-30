# 🛡 DigiByte Quantum Wallet Guard (QWG) — v2

**Layer‑5: Quantum‑Era Wallet Behaviour Guard for DigiByte**

QWG (Quantum Wallet Guard) is the fifth defensive layer in the DigiByte
Quantum Shield stack. It sits *around* DigiByte wallets and watches how
funds move over time, looking for quantum‑style key sweeps, automated
drain patterns, and abnormal behaviour that normal wallet software
cannot see.

QWG does **not** change DigiByte consensus or cryptography.  
It is a Python risk‑analysis engine that can be integrated into
exchanges, custodial systems, enterprise wallets or power‑user tooling
to score withdrawal flows and trigger extra protection when risk rises.

---

## 🎯 High‑Level Goals

QWG is designed to:

- Detect **dormant key sweep patterns** (many long‑silent wallets moving
  at once toward a few aggregation points)
- Flag **automated wallet drains** and abnormal withdrawal bursts
- Highlight **entropy‑weak signing patterns** (timing, rhythm, volume)
- Provide a **Quantum‑Style Risk Score (QRS)** per wallet / session
- Expose a clean Python API that DigiByte or any other chain can plug
  into without touching consensus rules

---

## 🧱 How QWG Fits Into the 5‑Layer Shield

The full stack looks like this:

1. **Sentinel AI v2** – monitors node, mempool and chain behaviour  
2. **DQSN v2** – aggregates risk across many nodes (network‑wide view)  
3. **ADN v2** – autonomous local defense node (lockdowns, throttling)  
4. **Guardian Wallet v2** – user‑facing wallet guard & UX enforcement  
5. **Quantum Wallet Guard v2 (QWG)** – deep pattern analysis on wallet
   flows and quantum‑style attack patterns

Above all of this sits the **Adaptive Core**, which learns from every
layer and can update policies over time.

QWG is the specialist that focuses on **“what is the wallet really
doing?”** over many steps, not just a single transaction.

---

## 🧠 Core Concepts

### Quantum‑Style Risk Score (QRS)

- Integer 0–100
- Derived from timing, volume, UTXO structure, repetition,
  cross‑wallet correlations and policy rules
- Mapped to levels: `LOW`, `ELEVATED`, `HIGH`, `CRITICAL`

### RiskContext

- Long‑lived object that tracks:
  - wallet history
  - burst patterns
  - device / session flags (if provided by the integrator)
  - links to Sentinel / Guardian signals via Adaptive Bridge

### Engine

The `QWGEngine` consumes structured events and returns a decision:

- QRS score
- risk level
- detected pattern tags (e.g. `DORMANT_KEY_SWEEP`)

---

## 📂 Repository Layout (current v2 structure)

```text
.github/workflows/
    ci.yml                         # GitHub Actions: lint + tests

examples/
    adaptive_core_bridge_example.py  # how QWG talks to Adaptive Core
    basic_usage.py                   # minimal engine + RiskContext demo
    behaviour_and_device.py          # shows behaviour / device signals
    dormant_key_sweep_scenario.py    # QWG‑SIM‑001 scenario (doc‑linked)
    high_risk_scenario.py            # generic high‑risk pattern demo

src/qwg/
    __init__.py
    adaptive_bridge.py             # connector into the Adaptive Core
    decisions.py                   # decision objects & helpers
    engine.py                      # QWGEngine – main risk engine
    policies.py                    # threshold and pattern policies
    risk_context.py                # RiskContext – long‑lived state

tests/
    test_adaptive_bridge.py
    test_decisions.py
    test_dormant_key_sweep.py      # asserts QRS escalation for SIM‑001
    test_engine.py
    test_policies.py

QWG-Adaptive-Core-Integration-v2.md  # how QWG plugs into Adaptive Core
QWG-CodeBlueprint-v2.md              # file‑by‑file blueprint of engine
QWG-DeveloperGuide-v2.md             # how to integrate and extend
QWG-QuantumAttackScenario-1.md       # dormant key sweep scenario spec
QWG-TechSpec-v2.md                   # technical API + data structures
QWG_Whitepaper_v2.md                 # high‑level narrative & rationale
LICENSE
README.md
```

This README is focused on giving Jared / other engineers a **fast
overview** of what lives where and how everything fits together.

---

## ▶️ Running the Example Scenarios

From the repo root:

```bash
python examples/basic_usage.py
python examples/dormant_key_sweep_scenario.py
python examples/high_risk_scenario.py
```

The dormant key sweep scenario (`QWG‑SIM‑001`) is aligned with the
specification in `QWG-QuantumAttackScenario-1.md`. It feeds a synthetic
multi‑wallet “sweep” into `QWGEngine` so you can see:

- how QRS evolves step‑by‑step
- when risk level reaches `CRITICAL`
- which pattern tags are attached

This gives integrators a **concrete feel** for how quantum‑style attack
detection would behave in production.

---

## 🧪 Running the Test Suite

```bash
pytest -q
```

The tests cover:

- core engine wiring (`test_engine.py`)
- policies & thresholds (`test_policies.py`)
- decision objects (`test_decisions.py`)
- adaptive bridge behaviour (`test_adaptive_bridge.py`)
- the dormant key sweep scenario (`test_dormant_key_sweep.py`)

When all tests are green, QWG v2 is in a consistent state and safe to
run in a testnet / staging environment.

---

## 🔌 Integration Philosophy

QWG is intentionally:

- **chain‑agnostic** – built for DigiByte first, but other UTXO chains
  can reuse it by feeding their own events
- **non‑invasive** – no consensus changes, no cryptography replacement
- **observable** – every decision can be logged, explained, and tuned
- **adaptive‑ready** – the Adaptive Core can adjust policies over time
  based on attack data and operator feedback

For DigiByte specifically, QWG is meant to sit next to:

- DigiDollar oracle / stability infrastructure  
- exchanges running DigiByte custodial wallets  
- high‑value cold‑to‑hot migration flows  

and give them another **line of intelligence** before funds actually
move.

---

## 🧾 Status

- Version: **v2 – reference implementation**
- Stability: **experimental but structured for real‑world testing**
- Intended next step: **testnet / staging deployments** where QWG
  observes real DigiByte flows and Adaptive Core starts learning.

---

## 📜 License

MIT – free to use, modify and extend for DigiByte and any other
blockchain project that wants additional quantum‑era wallet protection.

---

## 👤 Credits

- **Architecture & Vision:** @DarekDGB  
- **AI Engineering Assistance:** “Angel” 

If you are reading this as a DigiByte core dev, integrator or security
researcher and want to experiment with QWG in a controlled environment,
reach out to **@Darek_DGB** on X.

