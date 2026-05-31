from __future__ import annotations

from dataclasses import dataclass

import pytest

from qwg.adapters import to_v3_verdict
from qwg.adaptive_bridge import emit_adaptive_event
from qwg.decisions import Decision, DecisionResult
from qwg.engine import DecisionEngine
from qwg.risk_context import RiskContext, RiskLevel


class ThreatPacketSink:
    def __init__(self) -> None:
        self.packets: list[dict] = []

    def receive_threat_packet(self, packet: dict) -> None:
        self.packets.append(packet)


class RaisingThreatPacketSink:
    def receive_threat_packet(self, packet: dict) -> None:
        raise RuntimeError("boom")


class RaisingEventSink:
    def handle_event(self, event: dict) -> None:
        raise RuntimeError("boom")


class AddEventSink:
    def __init__(self) -> None:
        self.events: list[dict] = []

    def add_event(self, event: dict) -> None:
        self.events.append(event)


class EngineThreatSink:
    def __init__(self) -> None:
        self.packets: list[dict] = []

    def receive_threat_packet(self, packet: dict) -> None:
        self.packets.append(packet)


class ExplodingContext(RiskContext):
    @property
    def tx_amount(self) -> float:  # type: ignore[override]
        raise RuntimeError("unsafe context")

    @tx_amount.setter
    def tx_amount(self, value: float) -> None:  # pragma: no cover - dataclass init hook
        pass


def test_to_v3_verdict_rejects_missing_outcome() -> None:
    @dataclass
    class MissingOutcome:
        reason_id: str = "REASON"

    with pytest.raises(ValueError, match="outcome"):
        to_v3_verdict(MissingOutcome(), "0" * 64)


def test_to_v3_verdict_rejects_missing_reason_id() -> None:
    @dataclass
    class MissingReason:
        outcome: str = "allow"

    with pytest.raises(ValueError, match="reason_id"):
        to_v3_verdict(MissingReason(), "0" * 64)


def test_emit_adaptive_event_noops_for_none_sink() -> None:
    emit_adaptive_event(
        adaptive_sink=None,
        event_id="tx-none",
        action="warn",
        severity=0.1,
        fingerprint="wallet-none",
    )


def test_emit_adaptive_event_prefers_threat_packet_path() -> None:
    sink = ThreatPacketSink()

    emit_adaptive_event(
        adaptive_sink=sink,
        event_id="tx-1",
        action="block",
        severity=0.9,
        fingerprint="wallet-1",
        user_id="user-1",
        extra={
            "threat_type": "wallet_block",
            "description": "blocked",
            "timestamp": "2026-01-01T00:00:00Z",
            "node_id": "node-1",
            "wallet_id": "wallet-override",
            "tx_id": "tx-override",
            "block_height": 123,
        },
    )

    assert sink.packets == [
        {
            "source_layer": "quantum_wallet_guard",
            "threat_type": "wallet_block",
            "severity": 1,
            "description": "blocked",
            "timestamp": "2026-01-01T00:00:00Z",
            "node_id": "node-1",
            "wallet_id": "wallet-override",
            "tx_id": "tx-override",
            "block_height": 123,
        }
    ]


def test_emit_adaptive_event_returns_safely_when_threat_packet_sink_raises() -> None:
    emit_adaptive_event(
        adaptive_sink=RaisingThreatPacketSink(),
        event_id="tx-raise",
        action="block",
        severity=1.0,
        fingerprint="wallet-raise",
    )


def test_emit_adaptive_event_returns_safely_when_event_handler_raises() -> None:
    emit_adaptive_event(
        adaptive_sink=RaisingEventSink(),
        event_id="tx-handler-raise",
        action="warn",
        severity=0.5,
        fingerprint="wallet-handler-raise",
    )


def test_emit_adaptive_event_supports_add_event_fallback() -> None:
    sink = AddEventSink()

    emit_adaptive_event(
        adaptive_sink=sink,
        event_id="tx-add",
        action="warn",
        severity=0.5,
        fingerprint="wallet-add",
    )

    assert len(sink.events) == 1
    assert sink.events[0]["event_id"] == "tx-add"
    assert sink.events[0]["source"] == "qwg"


def test_engine_emits_adaptive_packet_with_context_details() -> None:
    sink = EngineThreatSink()
    ctx = RiskContext(
        sentinel_level=RiskLevel.CRITICAL,
        wallet_balance=1000.0,
        tx_amount=10.0,
        behaviour_score=1.2,
        trusted_device=False,
    )
    ctx.adaptive_sink = sink  # type: ignore[attr-defined]
    ctx.tx_id = "tx-engine"  # type: ignore[attr-defined]
    ctx.wallet_fingerprint = "wallet-engine"  # type: ignore[attr-defined]
    ctx.user_id = "user-engine"  # type: ignore[attr-defined]

    result = DecisionEngine().evaluate_transaction(ctx)

    assert result.decision is Decision.BLOCK
    assert len(sink.packets) == 1
    packet = sink.packets[0]
    assert packet["threat_type"] == "wallet_block"
    assert packet["wallet_id"] == "wallet-engine"
    assert packet["tx_id"] == "tx-engine"
    assert "Critical chain or node risk" in packet["description"]


def test_engine_emit_adaptive_never_breaks_wallet_decision() -> None:
    ctx = ExplodingContext(sentinel_level=RiskLevel.CRITICAL)
    ctx.adaptive_sink = object()  # type: ignore[attr-defined]

    result = DecisionEngine().evaluate_transaction(ctx)

    assert result.decision is Decision.BLOCK
    assert result.reason_id == "QWG_V3_CRITICAL_CHAIN_OR_NODE_RISK"


@pytest.mark.parametrize(
    ("reason", "expected"),
    [
        ("Critical chain or node risk reported by Sentinel/ADN.", "QWG_V3_CRITICAL_CHAIN_OR_NODE_RISK"),
        ("Risk level exceeds wallet policy; transaction delayed.", "QWG_V3_POLICY_MAX_RISK_EXCEEDED"),
        ("Attempt to send ~100% of wallet balance.", "QWG_V3_FULL_BALANCE_WIPE_ATTEMPT"),
        ("Amount exceeds extra-auth threshold.", "QWG_V3_EXTRA_AUTH_THRESHOLD_EXCEEDED"),
        ("Large transaction during high risk period.", "QWG_V3_RATIO_EXCEEDS_HIGH_RISK_LIMIT"),
        ("Transaction exceeds normal per-tx ratio.", "QWG_V3_RATIO_EXCEEDS_NORMAL_LIMIT"),
        ("Unusual behaviour or untrusted device detected.", "QWG_V3_BEHAVIOUR_OR_DEVICE_RISK"),
        ("No policy or risk rule violated.", "QWG_V3_HEALTHY_ALLOW"),
        ("something else", "QWG_V3_UNCLASSIFIED_REASON"),
    ],
)
def test_reason_id_fallback_mapping_is_stable(reason: str, expected: str) -> None:
    result = DecisionResult(decision=Decision.ALLOW, reason=reason)

    assert DecisionEngine()._map_reason_id_fallback(result) == expected


def test_risk_context_helper_methods_cover_both_paths() -> None:
    sentinel_worse = RiskContext(sentinel_level=RiskLevel.HIGH, adn_level=RiskLevel.ELEVATED)
    adn_worse = RiskContext(sentinel_level=RiskLevel.NORMAL, adn_level=RiskLevel.CRITICAL)
    risky_network = RiskContext(dqs_network_score=0.9)
    normal_network = RiskContext(dqs_network_score=0.89)

    assert sentinel_worse.max_chain_risk() is RiskLevel.HIGH
    assert adn_worse.max_chain_risk() is RiskLevel.CRITICAL
    assert risky_network.is_network_extremely_risky() is True
    assert normal_network.is_network_extremely_risky() is False
