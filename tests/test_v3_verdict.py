import pytest

from qwg.adapters import to_v3_verdict
from qwg.v3.verdict import VerdictType


class DummyDecision:
    """
    Minimal stand-in for an existing QWG decision object.

    This avoids touching real engine logic and keeps the test
    focused on the v3 envelope invariant only.
    """
    def __init__(self):
        self.outcome = "deny"
        self.reason_id = "TEST_REASON_ID"
        self.reasons = ["test_reason"]


def test_v3_verdict_is_immutable():
    decision = DummyDecision()
    context_hash = "deadbeef" * 8  # deterministic placeholder

    verdict = to_v3_verdict(decision, context_hash)

    # Basic correctness
    assert verdict.schema_version == "v3"
    assert verdict.verdict_type == VerdictType.DENY
    assert verdict.reason_id == "TEST_REASON_ID"
    assert verdict.context_hash == context_hash

    # Glass-box invariant: verdict must be immutable
    with pytest.raises(Exception):
        verdict.reason_id = "MUTATE"
