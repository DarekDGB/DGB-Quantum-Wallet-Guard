import pytest

from qwg.v3.context_hash import compute_context_hash


def test_compute_context_hash_rejects_non_dict():
    with pytest.raises(TypeError, match="context must be a dict"):
        compute_context_hash("not-a-dict")  # type: ignore[arg-type]
