from __future__ import annotations

from typing import Any, Dict, Optional


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

    - This repo does NOT import `adaptive_core` directly.
    - `adaptive_sink` can be any object that exposes either:
        * handle_event(event: dict)
        * add_event(event: dict)

    If no compatible method is found, or if anything fails, this
    function quietly returns without raising. Wallet safety first.
    """
    if adaptive_sink is None:
        return

    event: Dict[str, Any] = {
        "event_id": event_id,
        "action": action,
        "severity": severity,
        "fingerprint": fingerprint,
        "user_id": user_id,
        "extra": extra or {},
        "source": "qwg",
    }

    # Try common method names used by Adaptive Core or other sinks
    handler = getattr(adaptive_sink, "handle_event", None) or getattr(
        adaptive_sink, "add_event", None
    )
    if handler is None:
        return

    try:
        handler(event)
    except Exception:
        # Never allow adaptive plumbing to break wallet decisions.
        return
