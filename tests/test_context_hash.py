from qwg.v3.context_hash import compute_context_hash


def test_context_hash_is_deterministic():
    context = {
        "sentinel": "normal",
        "amount": 100,
        "device": "abc123",
    }

    h1 = compute_context_hash(context)
    h2 = compute_context_hash(context)

    assert h1 == h2


def test_context_hash_order_independent():
    context_a = {
        "a": 1,
        "b": 2,
    }

    context_b = {
        "b": 2,
        "a": 1,
    }

    assert compute_context_hash(context_a) == compute_context_hash(context_b)
