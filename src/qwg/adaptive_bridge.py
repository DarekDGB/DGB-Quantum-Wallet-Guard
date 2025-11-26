"""
Adaptive bridge for Quantum Wallet Guard v2.

This module sends AdaptiveEvent objects into the
DigiByte Quantum Adaptive Core whenever QWG reacts
to suspicious withdrawal behaviour.

Layer name used here: "qwg".
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from adaptive_core.models import AdaptiveEvent
from adaptive_core.memory import AdaptiveMemoryWriter


def emit_adaptive_event(
    adaptive_sink: Optional[AdaptiveMemoryWriter],
    *,
    event_id: str,
    action: str,
    severity: float,
    fingerprint: str,
    user_id: Optional[str] = None,
    extra: Optional[Dict[str, Any]] = None,
) -> None:
    """
    Push a single Quantum Wallet Guard reaction into the Adaptive Core.

    Parameters
    ----------
    adaptive_sink:
        Instance of AdaptiveMemoryWriter provided by the host app.
        If None is passed, this function becomes a no-op (safe fallback).

    event_id:
        Unique or semi-unique identifier for the wallet event
        (e.g. txid, session id, or internal audit id).

    action:
        Short label describing what QWG actually did:
        - "withdrawal_delayed"
        - "cooldown_started"
        - "withdrawal_blocked"
        - "extra_verification_required"
        etc.

    severity:
        0.0–1.0 rough severity score of this reaction.

    fingerprint:
        QWG-level fingerprint of the situation – for example
        wallet fingerprint + device + policy id.

    user_id:
        Optional end-user identifier (hashed or pseudonymous).

    extra:
        Optional dictionary with structured context
        (cooldown length, rule ids, etc.).
    """
    if adaptive_sink is None:
        # Running in stand-alone mode, nothing to do
        return

    event = AdaptiveEvent(
        layer="qwg",
        anomaly_type="wallet_protection",
        action=action,
        severity=severity,
        fingerprint=fingerprint,
        metadata=extra or {},
        event_id=event_id,
    )

    adaptive_sink.write_event(event)
