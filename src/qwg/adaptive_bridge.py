from __future__ import annotations

from typing import Any, Dict, Optional
from datetime import datetime


def emit_adaptive_event(
    adaptive_sink: Any,
    event_id: str,
    action: str,
    severity: float,
    fingerprint: str,
    user_id: Optional[str] = None,
    extra: Optional[Dict[str, Any]] = None,
) -> None:
    """
    Thin, dependency-free bridge from QWG → Adaptive Core.

    This bridge is deliberately defensive:

      - This repo does NOT import `adaptive_core` directly.
      - `adaptive_sink` can be any object that exposes one of:
            * handle_event(event: dict)
            * add_event(event: dict)
            * receive_threat_packet(packet: dict | object)

      - If no compatible method is found, or if anything fails,
        this function returns quietly. Wallet safety first.

    v2 behaviour:

      - Still emits the original generic `event` dict used by QWG.
      - Additionally, if `adaptive_sink` exposes `receive_threat_packet`,
        we send a ThreatPacket-shaped dict so the Adaptive Core v2 can
        store it in ThreatMemory and include it in immune reports.
    """
    if adaptive_sink is None:
        return

    extra = extra or {}

    # ------------------------------------------------------------------ #
    # 1) Original generic event payload (backwards compatible)
    # ------------------------------------------------------------------ #
    event: Dict[str, Any] = {
        "event_id": event_id,
        "action": action,
        "severity": severity,
        "fingerprint": fingerprint,
        "user_id": user_id,
        "extra": extra,
        "source": "qwg",
    }

    # ------------------------------------------------------------------ #
    # 2) ThreatPacket-shaped payload for Adaptive Core v2
    # ------------------------------------------------------------------ #
    # We do NOT import ThreatPacket directly – we just mirror its fields
    # so any adaptive core can wrap this dict into a real ThreatPacket.
    now_iso = datetime.utcnow().isoformat() + "Z"

    threat_packet: Dict[str, Any] = {
        "source_layer": "quantum_wallet_guard",
        "threat_type": extra.get("threat_type", action or "wallet_guard_event"),
        "severity": int(round(severity)),
        "description": extra.get(
            "description",
            f"QWG action={action}, fingerprint={fingerprint}",
        ),
        "timestamp": extra.get("timestamp", now_iso),
        "node_id": extra.get("node_id"),
        "wallet_id": extra.get("wallet_id", user_id),
        "tx_id": extra.get("tx_id"),
        "block_height": extra.get("block_height"),
    }

    # ------------------------------------------------------------------ #
    # 3) Prefer direct ThreatPacket path if available
    # ------------------------------------------------------------------ #
    try:
        receive_tp = getattr(adaptive_sink, "receive_threat_packet", None)
        if callable(receive_tp):
            receive_tp(threat_packet)
            return
    except Exception:
        # Never allow adaptive plumbing to break wallet decisions.
        return

    # ------------------------------------------------------------------ #
    # 4) Fallback: old generic event handlers (v1 compatibility)
    # ------------------------------------------------------------------ #
    handler = getattr(adaptive_sink, "handle_event", None) or getattr(
        adaptive_sink, "add_event", None
    )
    if handler is None:
        return

    try:
        handler(event)
    except Exception:
        # Again: wallet safety first.
        return
