# TuringDB Examples

Welcome to the TuringDB Examples repository! This collection provides practical examples and tutorials for using [TuringDB](https://turingdb.mintlify.app/) in real-world scenarios.

## Quick Start

### Prerequisites

- Python 3.13 or higher
- [uv](https://docs.astral.sh/uv/) package manager

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/turing-db/turingdb-examples.git
   cd turingdb-examples
   ```

2. **Install dependencies:**
   ```bash
   uv sync
   ```

3. **Start Jupyter Lab:**
   ```bash
   uv run jupyter lab
   ```

   This will start the Jupyter server and display output like:
   ```
   [I 2024-09-26 16:30:15.123 ServerApp] Jupyter Server is running at:
   [I 2024-09-26 16:30:15.123 ServerApp] http://localhost:8888/lab?token=abc123...
   ```

   **Copy the URL** (starting with `http://localhost:8888/lab?token=...`) and paste it into your web browser to access Jupyter Lab.

4. **Open and run the example notebooks** in `examples/notebooks/public_version/`

## What's Included

### 📓 Jupyter Notebooks

Located in `examples/notebooks/public_version/`:

- **London Transport Analysis** (`london_transport_TfL.ipynb`): Demonstrates TuringDB usage with real Transport for London data
- Complete datasets included in the `data/` folder

### 🔧 What You Get

All examples work seamlessly with popular AI providers and include everything needed for data analysis and AI integration.

## Usage

1. **Run a notebook**: Navigate to any `.ipynb` file in Jupyter Lab and run the cells
2. **Modify examples**: Feel free to experiment with the code and data
3. **Add your own data**: Replace or add datasets in the `data/` folders

## API Keys Setup

Some examples may require API keys for AI services. To set them up:

1. **Create a `.env` file** in the project root directory (same level as `pyproject.toml`):
   ```bash
   touch .env
   ```

2. **Add your API keys** to the `.env` file using any text editor:
   ```bash
   # Open with your preferred editor (nano, vim, code, etc.)
   nano .env
   ```

3. **Add the following content** (replace with your actual keys):
   ```env
   # Optional: Add your API keys if needed by specific examples
   ANTHROPIC_API_KEY=your_anthropic_key_here
   OPENAI_API_KEY=your_openai_key_here
   MISTRAL_API_KEY=your_mistral_key_here
   ```

4. **Save and close** the file. The `.env` file is automatically ignored by git for security.

## Example Data

The repository includes real datasets:
- **Transport for London (TfL)**: Tube station data, routes, and sightseeing information
- All data files are located in `examples/notebooks/public_version/data/`

## Requirements

All dependencies are automatically managed and installed when you run `uv sync`. No manual package installation needed!

## Troubleshooting

### Common Issues

**Import errors**: Make sure you've run `uv sync` to install all dependencies

**Jupyter not starting**: Ensure you're using `uv run jupyter lab` and not a system-wide jupyter installation

**Missing data files**: Verify that CSV files exist in `examples/notebooks/public_version/data/`

**API errors**: Check that any required API keys are properly set in your `.env` file

### Getting Help

- Check the [TuringDB documentation](https://turingdb.mintlify.app/)

---

**Ready to dive into AI-powered data analysis?** Open those notebooks and discover what TuringDB can do for you! 🎯✨
