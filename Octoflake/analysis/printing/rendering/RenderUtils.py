from pathlib import Path

from stl import Mode

from printing.octo.OctoConfig import OctoConfig
from printing.rendering.StlRenderer import StlRenderer


def basic_render(grid, config=None, filename="derp.stl", base_path=None, z_min=0, mode=Mode.BINARY):
    grid.compute_trimming()
    grid.crop(z_min=z_min)

    config = config if config is not None else OctoConfig()
    renderer = StlRenderer()
    base_path = base_path if base_path is not None else Path.home() / "Desktop"

    path = base_path / filename

    print(f"Rendering a grid with {len(grid.occ)} octos.")
    print(f"Using {config}.")
    mesh = renderer.render(config, grid)

    print(f"Saving as {path}")
    mesh.save(path, mode=mode)

    print(f"Done!")
