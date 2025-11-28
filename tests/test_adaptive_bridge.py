# tests/test_adaptive_bridge.py

from __future__ import annotations

from typing import Any, Dict, Optional

from qwg.adaptive_bridge import emit_adaptive_event


class DummyAdaptiveSink:
    """
    Minimal fake sink used to verify that QWG emits adaptive events
    without raising and with the expected shape.
    """

    def __init__(self) -> None:
        self.events: list[Dict[str, Any]] = []

    def handle_event(self, event: Dict[str, Any]) -> None:
        self.events.append(event)


def test_emit_adaptive_event_sends_event_to_sink() -> None:
    sink = DummyAdaptiveSink()

    emit_adaptive_event(
        adaptive_sink=sink,
        event_id="tx-123",
        action="block",
        severity=0.9,
        fingerprint="wallet-abc",
        user_id="user-1",
        extra={"reason": "test"},
    )

    # One event should be recorded
    assert len(sink.events) == 1
    evt = sink.events[0]

    assert evt["event_id"] == "tx-123"
    assert evt["action"] == "block"
    assert evt["severity"] == 0.9
    assert evt["fingerprint"] == "wallet-abc"
    assert evt["user_id"] == "user-1"
    assert evt["extra"]["reason"] == "test"
    assert evt["source"] == "qwg"


def test_emit_adaptive_event_safe_on_missing_handler() -> None:
    class NoHandlerSink:
        pass

    # Should not raise even though sink has no handle_event/add_event
    sink = NoHandlerSink()
    emit_adaptive_event(
        adaptive_sink=sink,
        event_id="tx-999",
        action="warn",
        severity=0.5,
        fingerprint="wallet-x",
    )

    # Nothing to assert – success is "no exception"
