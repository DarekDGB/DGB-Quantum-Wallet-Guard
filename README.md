# DGB Quantum Wallet Guard --- Layer 5 v2

### Universal Wallet Security Engine for DigiByte

Welcome to **Layer 5 v2** of the DigiByte Quantum Shield Network --- the
**DGB Quantum Wallet Guard**.\
This module acts as the final wallet‑level protection layer, sitting on
top of:

1.  **Sentinel AI v2** --- chain‑level detection\
2.  **DQSN** --- network‑wide threat scoring\
3.  **ADN v2** --- node‑level autonomous protection\
4.  **DGB Wallet Guardian v2** --- wallet safety + rules\
5.  **Quantum Wallet Guard v2** ← *this repo*

Layer 5 v2 integrates **all signals** from the entire quantum shield and
makes final decisions for **every outgoing transaction**.

------------------------------------------------------------------------

## 🚀 Features in v2

-   ✔️ Advanced decision engine\
-   ✔️ Unified risk model\
-   ✔️ Wallet policies enforcement\
-   ✔️ Extra authentication triggers\
-   ✔️ Behaviour & device checks\
-   ✔️ Full test suite (pytest CI)\
-   ✔️ Clean modular architecture\
-   ✔️ Future‑proof for PQC integration (v3)

------------------------------------------------------------------------

## 📁 Project Structure

    src/qwg/
        engine.py
        risk_context.py
        policies.py
        decisions.py

    examples/
    tests/
    .github/workflows/ci.yml

------------------------------------------------------------------------

# 🧠 Core Components

## 1. `risk_context.py`

``` python
from dataclasses import dataclass
from enum import Enum
from typing import Optional
from datetime import datetime

class RiskLevel(str, Enum):
    NORMAL = "normal"
    ELEVATED = "elevated"
    HIGH = "high"
    CRITICAL = "critical"

    def severity(self) -> int:
        order = {"normal": 0, "elevated": 1, "high": 2, "critical": 3}
        return order[self.value]

@dataclass
class RiskContext:
    sentinel_level: RiskLevel = RiskLevel.NORMAL
    dqs_network_score: float = 0.0
    adn_level: RiskLevel = RiskLevel.NORMAL

    wallet_balance: float = 0.0
    tx_amount: float = 0.0

    address_age_days: Optional[int] = None
    behaviour_score: float = 1.0
    device_id: Optional[str] = None
    trusted_device: bool = True

    created_at: datetime = datetime.utcnow()
```

------------------------------------------------------------------------

## 2. `policies.py`

``` python
from dataclasses import dataclass
from .risk_context import RiskLevel

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

------------------------------------------------------------------------

## 3. `decisions.py`

``` python
from dataclasses import dataclass
from enum import Enum
from typing import Optional

class Decision(str, Enum):
    ALLOW = "allow"
    WARN = "warn"
    DELAY = "delay"
    BLOCK = "block"
    REQUIRE_EXTRA_AUTH = "require_extra_auth"

@dataclass
class DecisionResult:
    decision: Decision
    reason: str
    cooldown_seconds: int = 0
    suggested_limit: Optional[float] = None
    require_confirmation: bool = False
    require_second_factor: bool = False
```

------------------------------------------------------------------------

## 4. `engine.py`

``` python
from .risk_context import RiskContext, RiskLevel
from .policies import WalletPolicy
from .decisions import Decision, DecisionResult

class DecisionEngine:
    def __init__(self, policy: WalletPolicy | None = None) -> None:
        self.policy = policy or WalletPolicy()

    def evaluate_transaction(self, ctx: RiskContext) -> DecisionResult:
        p = self.policy

        if ctx.sentinel_level == RiskLevel.CRITICAL or ctx.adn_level == RiskLevel.CRITICAL:
            return DecisionResult(
                decision=Decision.BLOCK,
                reason="Critical chain or node risk reported by Sentinel/ADN.",
            )

        if (ctx.sentinel_level.severity() > p.max_allowed_risk.severity()
            or ctx.adn_level.severity() > p.max_allowed_risk.severity()):
            return DecisionResult(
                decision=Decision.DELAY,
                reason="Risk level exceeds wallet policy; transaction delayed.",
                cooldown_seconds=p.cooldown_seconds_delay,
            )

        if p.block_full_balance_tx and ctx.wallet_balance > 0:
            ratio = ctx.tx_amount / ctx.wallet_balance
            if ratio >= 0.99:
                return DecisionResult(
                    decision=Decision.BLOCK,
                    reason="Attempt to send ~100% of wallet balance.",
                )

        if ctx.wallet_balance > 0:
            ratio = ctx.tx_amount / ctx.wallet_balance
            if ctx.sentinel_level == RiskLevel.HIGH or ctx.adn_level == RiskLevel.HIGH:
                if ratio > p.max_tx_ratio_high:
                    return DecisionResult(
                        decision=Decision.WARN,
                        reason="Large transaction during high risk period.",
                        cooldown_seconds=p.cooldown_seconds_warn,
                        suggested_limit=p.max_tx_ratio_high * ctx.wallet_balance,
                    )
            else:
                if ratio > p.max_tx_ratio_normal:
                    return DecisionResult(
                        decision=Decision.WARN,
                        reason="Transaction exceeds normal per-tx ratio.",
                        cooldown_seconds=p.cooldown_seconds_warn,
                        suggested_limit=p.max_tx_ratio_normal * ctx.wallet_balance,
                    )

        if ctx.tx_amount >= p.threshold_extra_auth:
            return DecisionResult(
                decision=Decision.REQUIRE_EXTRA_AUTH,
                reason="Amount exceeds extra-auth threshold.",
                require_confirmation=True,
                require_second_factor=True,
            )

        if ctx.behaviour_score > 1.5 or not ctx.trusted_device:
            return DecisionResult(
                decision=Decision.WARN,
                reason="Unusual behaviour or untrusted device detected.",
                cooldown_seconds=p.cooldown_seconds_warn,
            )

        return DecisionResult(
            decision=Decision.ALLOW,
            reason="No policy or risk rule violated.",
        )
```

------------------------------------------------------------------------

# 📘 Examples (`/examples`)

## 1. Basic Usage

``` python
from qwg.engine import DecisionEngine
from qwg.risk_context import RiskContext

engine = DecisionEngine()

ctx = RiskContext(wallet_balance=1000.0, tx_amount=200.0)
result = engine.evaluate_transaction(ctx)

print(result)
```

## 2. High-Risk Scenario

``` python
ctx = RiskContext(
    wallet_balance=1000,
    tx_amount=200,
    sentinel_level=RiskLevel.HIGH,
)
```

## 3. Behaviour & Device Checks

``` python
ctx = RiskContext(
    wallet_balance=1000,
    tx_amount=50,
    behaviour_score=2.0,
    trusted_device=False,
)
```

------------------------------------------------------------------------

# 🧪 Testing (pytest)

Full test suite covering:

-   engine logic\
-   ratio rules\
-   critical chain risk\
-   extra authentication\
-   behaviour + device checks

Runs automatically in GitHub Actions.

------------------------------------------------------------------------

# 🔮 Next Milestone

After all 5 layers reach **v2 stable**, we begin:

### **🧩 Merge all layers into the Full DigiByte Quantum Shield Network (2026)**

A unified PQ-secure defence system for the entire DigiByte blockchain.

------------------------------------------------------------------------

# Made by Darek & Angel

DigiByte Quantum Shield --- protecting the future.
