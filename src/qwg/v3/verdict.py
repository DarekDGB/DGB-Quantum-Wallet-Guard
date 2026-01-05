from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


class VerdictType(str, Enum):
    """
    Explicit verdict types for QWG v3.

    NOTE:
    - These are outcomes, not scores.
    - Execution authority lives elsewhere.
    """
    ALLOW = "allow"
    DENY = "deny"
    ESCALATE = "escalate"


@dataclass(frozen=True)
class QWGv3Verdict:
    """
    Glass-box verdict envelope for Quantum Wallet Guard v3.

    This object:
    - is immutable
    - carries an explicit verdict
    - always includes a reason_id
    - is safe to log, audit, and test
    """

    schema_version: str            # always "v3"
    verdict_type: VerdictType
    reason_id: str                 # stable machine-readable ID
    context_hash: str              # deterministic identifier
    reasons: Optional[List[str]] = None
