# art

Fractal geometry generators and other tech-art experiments.

## Octoflake

The main project - a fractal geometry generator that creates 3D-printable octahedral/snowflake structures.

### Setup

Requires Python 3.11+ and [Poetry](https://python-poetry.org/docs/#installation).

```bash
cd Octoflake/analysis
poetry install
```

### Usage

Generate sample fractal meshes:

```bash
poetry run python -m printing.builders.FlakeBuilder
```

Output files (`.obj`, `.stl`) are saved to `Octoflake/analysis/output/`.

To customize the output directory, set the `OCTOFLAKE_OUTPUT_DIR` environment variable:

```bash
OCTOFLAKE_OUTPUT_DIR=/path/to/output poetry run python -m printing.builders.FlakeBuilder
```

### Development

Run tests:

```bash
poetry run pytest
```

Run tests with coverage:

```bash
poetry run pytest --cov
```

Lint code:

```bash
poetry run ruff check printing/
```

Set up pre-commit hooks (optional):

```bash
poetry run pre-commit install
```

### Project Structure

```text
Octoflake/analysis/
├── printing/
│   ├── builders/      # Shape builders (FlakeBuilder, StarBuilder, etc.)
│   ├── grid/          # Grid data structures
│   ├── gcode/         # G-code generation for direct printing
│   ├── recipies/      # Pre-configured shape recipes
│   ├── tests/         # Test suite
│   ├── utils/         # Configuration and utilities
│   └── config.py      # Output path configuration
├── output/            # Generated files (git-ignored)
└── pyproject.toml     # Poetry dependencies and tool config
```
