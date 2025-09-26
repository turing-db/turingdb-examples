def test_imports():
    """Test that main dependencies can be imported."""
    assert True


def test_turingdb_example_version():
    """Test that our own package can be imported."""
    import turingdb_examples

    assert turingdb_examples.__version__ == "0.1.0"


def test_basic_turingdb_example():
    """Test our basic example functions."""
    from turingdb_examples.basic_turingdb_example import (
        hello_turingdb,
        create_turingdb_client,
    )

    # Test the hello function
    result = hello_turingdb()
    assert result == "Hello from TuringDB Examples!"

    # Test client creation
    client = create_turingdb_client()
    assert client is not None
