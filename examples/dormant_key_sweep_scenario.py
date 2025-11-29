# QWG Dormant Key Sweep Example Script

Save this as **`examples/dormant_key_sweep_scenario.py`** in your QWG repo.

```python
"""Dormant key sweep scenario example for Quantum Wallet Guard (QWG).

This example feeds a synthetic "dormant key sweep" pattern into the QWG
engine so developers can see how the Quantum-Style Risk Score (QRS)
evolves and when the engine marks the pattern as CRITICAL.

NOTE:
- This is a simulation only.
- Adjust imports / class names if your engine API differs slightly.
"""

from dataclasses import dataclass
from typing import List
import datetime

# --- IMPORTS ---------------------------------------------------------------
# Adjust these imports to match your actual engine / risk context API.

try:
    # Option 1: engine exposed as QWGEngine + RiskContext
    from qwg.engine import QWGEngine
    from qwg.risk_context import RiskContext
except ImportError:
    try:
        # Option 2: engine exposed as Engine
        from qwg.engine import Engine as QWGEngine  # type: ignore
        from qwg.risk_context import RiskContext  # type: ignore
    except ImportError as e:
        raise SystemExit(
            "Could not import QWGEngine / RiskContext.\n"
            "Please open examples/dormant_key_sweep_scenario.py and\n"
            "update the imports at the top to match your code.\n"
            f"Original error: {e}"
        )


@dataclass
class SweepEvent:
    step: int
    minutes_from_start: int
    wallet_id: str
    utxos_moved: int
    amount_dgb: float
    destination: str


def build_dormant_key_sweep_scenario() -> List[SweepEvent]:
    """Scenario QWG-SIM-001 â aligned with QWG-QuantumAttackScenario-1.md."""
    return [
        SweepEvent(1, 0,  "A", 10, 12000, "X1"),
        SweepEvent(2, 5,  "B", 8,  9500,  "X1"),
        SweepEvent(3, 9,  "C", 5,  4200,  "X2"),
        SweepEvent(4, 14, "A", 10, 11700, "X1"),
        SweepEvent(5, 20, "B", 7,  8900,  "X2"),
        SweepEvent(6, 27, "C", 5,  4000,  "X1"),
    ]


def main() -> None:
    start_time = datetime.datetime.utcnow()

    # Initialise risk context and engine. Adjust if your engine requires config.
    risk_ctx = RiskContext()
    engine = QWGEngine(risk_context=risk_ctx)

    scenario = build_dormant_key_sweep_scenario()

    print(
        "Step | t(min) | Wallet | UTXOs | Amount (DGB) | Dest | QRS | Level | Pattern"
    )
    print("-" * 79)

    for ev in scenario:
        ts = start_time + datetime.timedelta(minutes=ev.minutes_from_start)

        # The exact API may differ â adapt this call to match your engine.
        result = engine.process_sweep_event(
            wallet_id=ev.wallet_id,
            utxos_moved=ev.utxos_moved,
            amount_dgb=ev.amount_dgb,
            destination=ev.destination,
            timestamp=ts,
        )

        # We expect the engine to return an object with:
        #   .qrs_score (0â100)
        #   .risk_level (e.g. "LOW"/"MEDIUM"/"HIGH"/"CRITICAL")
        #   .pattern (e.g. "DORMANT_KEY_SWEEP" or None)
        qrs = getattr(result, "qrs_score", None)
        level = getattr(result, "risk_level", "?")
        pattern = getattr(result, "pattern", "")

        print(
            f"{ev.step:>4} | {ev.minutes_from_start:>5}   | {ev.wallet_id:<6} | "
            f"{ev.utxos_moved:>5} | {ev.amount_dgb:>12.0f} | {ev.destination:<4} | "
            f"{qrs if qrs is not None else '??':>3} | {level:<8} | {pattern}"
        )


if __name__ == "__main__":
    main()
```
