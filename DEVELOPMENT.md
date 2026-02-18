# Development Guide

This guide explains how to develop new TuringDB examples with our professional development setup.

## Development Environment Setup

### Prerequisites

- Python 3.13 or higher
- [uv](https://docs.astral.sh/uv/) package manager
- Git

### Initial Setup

1. **Clone and switch to dev branch:**
   ```bash
   git clone https://github.com/turing-db/turingdb-examples.git
   cd turingdb-examples
   git checkout dev
   ```

2. **Install all dependencies (including dev tools):**
   ```bash
   uv sync --group dev
   ```

3. **Set up pre-commit hooks:**
   ```bash
   uv run pre-commit install
   ```

## Development Tools

Our development environment includes:

- **pytest**: Testing framework with coverage reporting
- **ruff**: Fast linting and code formatting
- **pre-commit**: Automatic code quality checks on every commit

## Complete Development Workflow

### 1. Start Development
```bash
# Make sure you're on dev and up to date
git checkout dev
git pull origin dev

# Create feature branch (optional, for bigger changes)
git checkout -b feature/new-example
```

### 2. Develop Your Content
```bash
# Start Jupyter for notebook development
bash run_jupyter.sh

# Work on your examples, notebooks, etc.
# Save your work in Jupyter
```

### 3. Quality Checks During Development
```bash
# Run tests to make sure nothing is broken
uv run pytest

# Check code quality manually (optional)
uv run ruff check .
uv run ruff format .
```

### 4. Commit Your Changes
```bash
# Stage your changes
git add .

# Attempt commit - pre-commit will run automatically
git commit -m "Add new TuringDB example for [topic]"

# If pre-commit fails and fixes files:
git add .  # Stage the fixed files
git commit -m "Add new TuringDB example for [topic]"  # Commit again
```

### 5. Final Verification
```bash
# Run full test suite to ensure everything works
uv run pytest --cov

# Push to dev
git push origin dev
```

### 6. When Ready for Production
```bash
# Sync all production file changes from dev to main via a single PR
bash sync_to_main.sh
```

This script automatically:
- Detects which files changed on `dev` vs `main` (excluding dev-only files)
- Creates a branch off `main`, applies the changes, and opens a PR via `gh`
- Returns you to `dev` when done

Dev-only files (`DEVELOPMENT.md`, `.pre-commit-config.yaml`, `tests/`) are never synced.

## Testing

### Available Testing Commands

```bash
# Daily development
uv run pytest              # Quick check before commit

# Weekly/when adding new examples
uv run pytest --cov       # Check coverage

# When debugging issues
uv run pytest -v -s       # Verbose + see print output
```

### Writing Tests

Create test files in `tests/` directory. Test functions must start with `test_`:

```python
def test_your_example():
    from turingdb_examples.your_module import your_function
    result = your_function()
    assert result == expected_value
```

## Code Quality

### Pre-commit Hooks

Pre-commit automatically runs on every commit and will:
- Format your code with Ruff
- Fix whitespace issues
- Ensure consistent style
- Block commits until issues are resolved

### Manual Quality Checks

```bash
# Check for issues
uv run ruff check .

# Fix issues automatically
uv run ruff check --fix .

# Format code
uv run ruff format .
```

## Project Structure

```
turingdb-examples/
├── src/turingdb_examples/     # Package source code
├── tests/                     # Test files
├── examples/                  # Example notebooks and data
│   ├── notebooks/
│   │   ├── public_version/    # Production-ready examples
│   │   └── draft/             # Work-in-progress (ignored by git)
│   └── data/                  # Example datasets
├── pyproject.toml            # Dependencies and tool configuration
├── tests/README.md           # Testing documentation
└── .pre-commit-config.yaml   # Pre-commit hook configuration
```

## Branch Strategy

- **`dev` branch**: All development work, testing setup, dev tools
- **`main` branch**: Clean, production-ready examples only
- **Feature branches**: For larger changes (optional)

### Moving Examples to Production

Only stable, tested examples should be moved to `main`:

1. Develop and test thoroughly in `dev`
2. Create PR to move specific files to `main`
3. Keep development infrastructure in `dev` only

## API Keys Setup

For examples requiring API keys, create a `.env` file in the project root:

```bash
touch .env
```

Add your keys:
```env
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
MISTRAL_API_KEY=your_key_here
```

## Troubleshooting

### Pre-commit Issues

**Pre-commit blocks my commit:**
- This is normal! Pre-commit found issues and fixed them
- Run `git add .` to stage the fixed files
- Commit again - should pass this time

**Pre-commit takes too long:**
- First run installs environments (slow)
- Subsequent runs are fast

### Testing Issues

**Tests fail after changes:**
- Check import paths in your test files
- Ensure test functions start with `test_`
- Run `uv sync --group dev` to update dependencies

### Jupyter Issues

**Can't start Jupyter:**
- Use `bash run_jupyter.sh` (not system jupyter)
- Ensure you're in the project directory
- Check that dependencies are installed

## Getting Help

- Check this development guide first
- Review `tests/README.md` for testing specifics
- Ensure all tools are properly installed with `uv sync --group dev`
- Check [TuringDB documentation](https://turingdb.mintlify.app/)

---

**Happy developing!** Your professional development setup ensures high-quality, consistent code automatically. 🚀
