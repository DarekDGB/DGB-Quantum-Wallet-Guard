"""
QWG v3 Adapters

This module contains explicit, side-effect-free adapters that
translate internal QWG decision objects into v3 glass-box verdicts.

IMPORTANT:
- No decision logic lives here
- No policy evaluation lives here
- No execution authority lives here

Adapters MUST remain pure and deterministic.
"""

from qwg.v3.verdict import QWGv3Verdict, VerdictType


def to_v3_verdict(decision, context_hash: str) -> QWGv3Verdict:
    """
    Adapter: wrap an existing QWG decision object into a v3 verdict envelope.

    This function MUST NOT:
    - change decision semantics
    - infer outcomes
    - apply additional logic
    - mutate the decision

    It is a pure structural translation.
    """

    # Hard glass-box guarantees
    if not hasattr(decision, "outcome"):
        raise ValueError("Decision object missing required attribute: outcome")

    if not hasattr(decision, "reason_id"):
        raise ValueError("Decision object missing required attribute: reason_id")

    return QWGv3Verdict(
        schema_version="v3",
        verdict_type=VerdictType(decision.outcome),
        reason_id=decision.reason_id,
        context_hash=context_hash,
        reasons=getattr(decision, "reasons", None),
    )
