"""
QWG v3 Context Hash

Provides a deterministic, side-effect-free hashing function
for decision contexts.

IMPORTANT:
- No timestamps
- No randomness
- No network calls
- Pure function only
"""

import hashlib
import json
from typing import Any, Dict


def compute_context_hash(context: Dict[str, Any]) -> str:
    """
    Compute a deterministic hash for a given decision context.

    Rules:
    - Input must be JSON-serializable
    - Keys are sorted
    - No implicit mutation
    """

    if not isinstance(context, dict):
        raise TypeError("context must be a dict")

    payload = json.dumps(
        context,
        sort_keys=True,
        separators=(",", ":"),
    )

    return hashlib.sha256(payload.encode("utf-8")).hexdigest()
