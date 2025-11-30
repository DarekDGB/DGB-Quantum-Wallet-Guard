# 🛡 DigiByte Quantum Wallet Guard (QWG) — v2

QWG (Quantum Wallet Guard) is Layer‑5 of the DigiByte Quantum Shield Network.
It monitors wallet activity in real time and detects high‑risk patterns,
including quantum‑style key sweep behaviour.

## 🚀 Purpose
QWG prevents:
- quantum‑style key‑sweep attacks
- automated wallet drains
- abnormal signing behaviour
- suspicious multi‑wallet sequences
- entropy‑weak transaction patterns

## 🧠 Core Components
- **QWGEngine** — computes Quantum‑Style Risk Score (QRS)
- **RiskContext** — timing, entropy, behaviour
- **Policies** — LOW → ELEVATED → HIGH → CRITICAL
- **Decisions** — final classification & actions
- **Adaptive Bridge** — connects to Adaptive Core (Layer‑6)

## 📂 Repository Structure
src/qwg/
    engine.py
    decisions.py
    policies.py
    risk_context.py
    adaptive_bridge.py

examples/
    dormant_key_sweep_scenario.py

tests/
    test_dormant_key_sweep.py

docs/
    QWG_Whitepaper_v2.md
    QWG_TechSpec_v2.md
    QWG_DeveloperGuide_v2.md
    QWG_CodeBlueprint_v2.md

## ▶️ Running Example Scenario
python examples/dormant_key_sweep_scenario.py

## 🧪 Running Tests
pytest -q

## 🔗 Layer Position
1. Sentinel AI v2
2. DQSN v2
3. ADN v2
4. Guardian Wallet v2
5. **Quantum Wallet Guard v2**

Adaptive Core (v1) learns from all previous layers.

## 📜 License
MIT

## 👤 Author
DarekDGB
