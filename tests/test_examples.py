def test_imports():
    """Test that main dependencies can be imported."""
    import turingdb
    import anthropic
    import openai
    assert True  # If we get here, imports worked

def test_package_import():
    """Test that our own package can be imported."""
    import turingdb_examples
    assert turingdb_examples.__version__ == "0.1.0"

def test_turingdb():
    """Actual example tests."""
    from turingdb import TuringDB
