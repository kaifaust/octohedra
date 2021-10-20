from pathlib import Path

from stl import Mode, Mesh
import numpy as np

from printing.utils import OctoConfigs


def render_grid(grid,
                config=OctoConfigs.config_25,
                filename="derp.stl",
                base_path=None,
                z_min=0,  # Set to None to not crop
                mode=Mode.BINARY):
    if z_min is not None:
        grid.crop(z_min=z_min)
    grid.compute_trimming()



    print(f"Rendering a grid with {len(grid.occ)} octos.")
    print(f"Using {config}.")
    mesh = grid.render(config)
    save_meshes(mesh, filename=filename, base_path=base_path, mode=mode)


def save_meshes(*meshes, filename="derp.stl", base_path=None, mode=Mode.BINARY):
    mesh_data = [mesh.data for mesh in meshes]
    mesh = Mesh(np.concatenate(mesh_data))
    base_path = base_path if base_path is not None else Path.home() / "Desktop"
    path = base_path / filename
    print(f"Saving mesh as {path}")
    mesh.save(path, mode=mode)
    print(f"Done!")
