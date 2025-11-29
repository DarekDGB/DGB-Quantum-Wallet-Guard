# DGB Quantum Wallet Guard v2 (QWG v2)

### Wallet-Level Behavioural Monitoring Layer (Layer 5)

#### *Technical Documentation --- v2*

Created by **Darek (@Darek_DGB)** & **Angel**

------------------------------------------------------------------------

# 🛡 1. Overview

**Quantum Wallet Guard (QWG) v2** is **Layer 5** of the DigiByte
monitoring and behavioural‑analysis stack.

QWG does **not** modify DigiByte cryptography or protocol rules.\
Instead, it evaluates wallet‑side behaviour and multi‑layer risk context
to decide whether to:

**ALLOW · WARN · DELAY · REQUIRE AUTH · BLOCK**

This ensures users avoid high‑risk transactions even during abnormal
network or device conditions.

QWG fuses signals from all lower layers:

  Layer   Component            Purpose
  ------- -------------------- ----------------------------------
  1       Sentinel AI v2       Chain/mempool anomaly monitoring
  2       DQSN v2              Network‑wide risk scoring
  3       ADN v2               Node behaviour & anomaly context
  4       Wallet Guardian v2   Transaction‑level local rules
  5       **QWG v2**           Final behavioural enforcement

QWG converts the entire stack into **wallet‑level behavioural
protection**.

------------------------------------------------------------------------

# ⚙️ 2. Architecture Blueprint

                 Sentinel AI v2 (Layer 1)
                          │ alerts
                          ▼
                     DQSN v2 (Layer 2)
                          │ signals
                          ▼
                    ADN v2 (Layer 3)
                          │ node-risk
                          ▼
             DGB Wallet Guardian v2 (Layer 4)
                          │ tx-context
                          ▼
          🛡 Quantum Wallet Guard v2 (Layer 5 – THIS MODULE)
                          │ decision
                          ▼
         Transaction → DigiByte network (if allowed)

------------------------------------------------------------------------

# 🧠 3. Core Responsibilities

## 1. Multi‑Layer Risk Fusion

QWG reads: - Sentinel AI anomaly level\
- ADN defence level\
- DQSN global network score\
- device-trust score\
- behavioural heuristics\
- wallet‑side risk factors

## 2. Wallet Policy Enforcement

-   prevents accidental full-balance wipes\
-   ratio throttling\
-   delay/cooldown rules\
-   high-value authentication\
-   new‑address heuristics\
-   device‑trust validation

## 3. Adaptive Event Emission (Optional)

When connected, QWG sends **AdaptiveEvents** to Adaptive Core v2 for
learning.

This is *non-blocking* --- behaviour inference is optional.

## 4. Safety Guarantee

Adaptive integration is "best‑effort": - failure → ignored\
- wallet flow → never broken

------------------------------------------------------------------------

# 📁 4. File Structure

    src/qwg/
    │   engine.py
    │   risk_context.py
    │   policies.py
    │   decisions.py
    │   adaptive_bridge.py
    │   __init__.py
    │
    examples/
    tests/
    .github/workflows/ci.yml
    QWG_Whitepaper_v2.md
    QWG_TechSpec_v2.md
    QWG_DeveloperGuide_v2.md
    QWG_CodeBlueprint_v2.md

------------------------------------------------------------------------

# 🔍 5. Technical Components

## 5.1 RiskContext

``` python
@dataclass
class RiskContext:
    sentinel_level: RiskLevel = RiskLevel.NORMAL
    dqs_network_score: float = 0.0
    adn_level: RiskLevel = RiskLevel.NORMAL

    wallet_balance: float = 0.0
    tx_amount: float = 0.0

    address_age_days: Optional[int] = None
    behaviour_score: float = 1.0
    trusted_device: bool = True

    adaptive_sink: Optional[Any] = None

    tx_id: Optional[str] = None
    wallet_fingerprint: Optional[str] = None
    user_id: Optional[str] = None
```

## 5.2 WalletPolicy

``` python
@dataclass
class WalletPolicy:
    block_full_balance_tx: bool = True
    max_tx_ratio_normal: float = 0.5
    max_tx_ratio_high: float = 0.1
    max_allowed_risk: RiskLevel = RiskLevel.HIGH

    cooldown_seconds_warn: int = 60
    cooldown_seconds_delay: int = 300

    threshold_extra_auth: float = 10_000.0
```

## 5.3 Decision Engine Rules

1.  Block on CRITICAL Sentinel or ADN signal\
2.  Delay if risk \> wallet policy\
3.  Block full-balance wipes\
4.  Require auth on high-value tx\
5.  Ratio throttle by risk level\
6.  Warn on device or behavioural anomalies\
7.  Allow only when everything passes

## 5.4 Adaptive Event Emission (Optional)

``` python
emit_adaptive_event(
    adaptive_sink,
    event_id=ctx.tx_id,
    action=decision.name.lower(),
    severity=0.55,
    fingerprint=ctx.wallet_fingerprint,
    user_id=ctx.user_id,
    extra={ ... }
)
```

------------------------------------------------------------------------

# 🧪 6. Testing Overview

Covers: - decision logic\
- critical‑risk blocking\
- device‑trust anomalies\
- ratio logic\
- behavioural patterns\
- adaptive‑sink safety\
- integration points

CI runs via GitHub Actions on each commit.

------------------------------------------------------------------------

# 📘 7. Documentation Files

  File                       Purpose
  -------------------------- --------------------
  QWG_Whitepaper_v2.md       Overview
  QWG_TechSpec_v2.md         Structures & rules
  QWG_DeveloperGuide_v2.md   Integration guide
  QWG_CodeBlueprint_v2.md    Code layout

------------------------------------------------------------------------

# ☑️ 8. v2 Summary

-   added AdaptiveBridge\
-   added AdaptiveEvent model\
-   stronger device heuristics\
-   multi‑layer risk fusion\
-   modular design for 2026 merge\
-   improved decision engine\
-   expanded tests + CI

------------------------------------------------------------------------

# 🧡 9. Future (2026)

When v2 stabilises across all layers:

    DigiByte Quantum Unified Shield Engine (DQ‑USE)

QWG becomes the **final wallet gatekeeper** for all DigiByte wallets.

------------------------------------------------------------------------

# 📜 License

MIT License --- free to use, modify, and distribute.

------------------------------------------------------------------------

# 👤 Author

Created by **Darek (@Darek_DGB)**\
Developed with **Angel**, supporting DigiByte's long‑term security
vision.
