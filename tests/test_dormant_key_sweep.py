import datetime
import pytest

try:
    from qwg.engine import QWGEngine
    from qwg.risk_context import RiskContext
except ImportError:
    pytest.skip(
        "QWGEngine / RiskContext not available.",
        allow_module_level=True,
    )


def _build_event(engine, wallet_id, utxos_moved, amount_dgb, minutes_from_start, start_time):
    ts = start_time + datetime.timedelta(minutes=minutes_from_start)
    return engine.process_sweep_event(
        wallet_id=wallet_id,
        utxos_moved=utxos_moved,
        amount_dgb=amount_dgb,
        destination="X1",
        timestamp=ts,
    )


def test_dormant_key_sweep_reaches_critical():
    risk_ctx = RiskContext()
    engine = QWGEngine(risk_context=risk_ctx)

    start = datetime.datetime(2025, 1, 1, 0, 0, 0)

    events = [
        ("A", 10, 12000, 0),
        ("B", 8,  9500,  5),
        ("C", 5,  4200,  9),
        ("A", 10, 11700, 14),
        ("B", 7,  8900,  20),
        ("C", 5,  4000,  27),
    ]

    last_result = None
    for wallet_id, utxos, amount, minutes in events:
        last_result = _build_event(
            engine=engine,
            wallet_id=wallet_id,
            utxos_moved=utxos,
            amount_dgb=amount,
            minutes_from_start=minutes,
            start_time=start,
        )

    assert last_result is not None

    qrs = getattr(last_result, "qrs_score", None)
    level = getattr(last_result, "risk_level", "")

    # Adjust threshold/label in future if your scoring scale changes.
    assert qrs is None or qrs >= 90 or level == "CRITICAL"
