# Testing Guide for TuringDB Examples

## Daily Testing Commands

```bash
# Daily development
uv run pytest              # Quick check before commit

# Weekly/when adding new examples  
uv run pytest --cov       # Check coverage

# When debugging issues
uv run pytest -v -s       # Verbose + see print output
```

## Test Structure

- `test_examples.py` - Tests for basic imports and package functionality
- Add new test files as `test_*.py` for each major example

## Writing Tests

Test functions must start with `test_` and should test functions from `src/turingdb_examples/`:

```python
def test_your_example():
    from turingdb_examples.your_module import your_function
    result = your_function()
    assert result == expected_value
```

## Coverage Reports

Coverage reports are generated in:
- Terminal output (with `--cov`)
- HTML format in `htmlcov/` directory (with `--cov-report=html`)

## Additional pytest Options

- `uv run pytest tests/specific_test.py` - Run only one test file
- `uv run pytest -k "test_name"` - Run tests matching pattern
- `uv run pytest --tb=short` - Shorter error messages
- `uv run pytest --maxfail=1` - Stop after first failure