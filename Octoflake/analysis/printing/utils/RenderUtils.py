import math
from pathlib import Path

from stl import Mode, Mesh
import numpy as np

from printing.utils import OctoConfigs


def render_4_8_layers(grid,
                      config=OctoConfigs.config_25,
                      filename="derp",
                      base_path=None,
                      z_min=0,  # Set to None to not crop
                      mode=Mode.BINARY):
    layer_heights = list(range(4, 9))
    render_at_layer_heights(grid, layer_heights, config, filename, base_path, z_min, mode)


def render_at_pow2_layers(grid,
                          config=OctoConfigs.config_25,
                          filename="derp",
                          base_path=None,
                          z_min=0,  # Set to None to not crop
                          mode=Mode.BINARY):
    layer_heights = [2 ** pow for pow in range(2, 6)]
    render_at_layer_heights(grid, layer_heights, config, filename, base_path, z_min, mode)


def render_at_layer_heights(grid, layers,
                            config=OctoConfigs.config_25,
                            filename="derp",
                            base_path=None,
                            z_min=0,  # Set to None to not crop
                            mode=Mode.BINARY):
    print("Rendering a grid at layers per cell counts:", layers)
    if not hasattr(layers, '__len__'):
        print("wat")
        layers = (layers,)

    for layer_count in layers:
        config.absolute_layers_per_cell = layer_count
        print(layer_count)
        config.derive()
        render_grid(grid, config, filename + f"_layers_{layer_count}", base_path, z_min, mode)


def render_grid(grid,
                config=OctoConfigs.config_25,
                base_filename="derp",
                base_path=None,
                z_min=0,  # Set to None to not crop
                mode=Mode.BINARY,
                translation=(0, 0, 0),
                **filename_details):
    if z_min is not None:
        grid.crop(z_min=z_min)
    grid.compute_trimming()

    print(f"Rendering a grid with {len(grid.occ)} octos.")
    print(f"Using config: {config}.")
    mesh = grid.render(config)


    save_meshes(mesh,
                base_filename=base_filename,
                base_path=base_path,
                mode=mode,
                translation=translation,
                **filename_details)


def save_meshes(*meshes,
                base_filename="derp",
                base_path=None,
                mode=Mode.BINARY,
                translation=(0, 0, 0),
                **filename_details):
    mesh_data = np.concatenate([mesh.data for mesh in meshes])
    # rounded = mesh_data.astype(np.float)


    mesh = Mesh(mesh_data)



    # mesh.rotate(np.array([0, 0, 1]), math.radians(45))
    mesh.translate(translation)

    base_path = base_path if base_path is not None else Path.home() / "Desktop" / "shapes"
    if not base_path.exists():
        base_path.mkdir()
    filename = base_filename.split(".")[0] + \
               "_" + \
               "_".join([f"{key}={value:.3}" for key, value in filename_details.items()]) + \
               ".stl"

    path = base_path / filename
    print(f"Saving mesh as {path}")
    mesh.save(path, mode=mode)
    print(f"Done!")
