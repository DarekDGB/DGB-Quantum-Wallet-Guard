def test_packaging_imports_qwg():
    # If editable install is broken, this import will fail in CI.
    import qwg  # noqa: F401
