"""
Output path configuration for the Octohedra project.

Set the OCTOHEDRA_OUTPUT_DIR environment variable to customize output location,
or it defaults to ./output/ relative to the octohedra package.
"""
import os
from pathlib import Path


def get_output_dir() -> Path:
    """
    Returns the output directory for generated files.

    Priority:
    1. OCTOHEDRA_OUTPUT_DIR environment variable
    2. ./output/ relative to the octohedra package
    """
    if env_path := os.environ.get("OCTOHEDRA_OUTPUT_DIR"):
        path = Path(env_path)
    else:
        # Default: output/ directory next to the octohedra package
        path = Path(__file__).parent.parent / "output"

    path.mkdir(parents=True, exist_ok=True)
    return path


OUTPUT_DIR = get_output_dir()
