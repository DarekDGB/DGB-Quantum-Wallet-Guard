from dataclasses import dataclass
from typing import List
import datetime

# Adjust these imports to match the actual QWG engine implementation.
try:
    from qwg.engine import QWGEngine
    from qwg.risk_context import RiskContext
except ImportError:
    from qwg.engine import Engine as QWGEngine  # type: ignore
    from qwg.risk_context import RiskContext  # type: ignore


@dataclass
class SweepEvent:
    step: int
    minutes_from_start: int
    wallet_id: str
    utxos_moved: int
    amount_dgb: float
    destination: str


def build_dormant_key_sweep_scenario() -> List[SweepEvent]:
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
    risk_ctx = RiskContext()
    engine = QWGEngine(risk_context=risk_ctx)
    scenario = build_dormant_key_sweep_scenario()

    print("Step | t(min) | Wallet | UTXOs | Amount (DGB) | Dest | QRS | Level | Pattern")
    print("-" * 79)

    for ev in scenario:
        ts = start_time + datetime.timedelta(minutes=ev.minutes_from_start)
        result = engine.process_sweep_event(
            wallet_id=ev.wallet_id,
            utxos_moved=ev.utxos_moved,
            amount_dgb=ev.amount_dgb,
            destination=ev.destination,
            timestamp=ts,
        )

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
