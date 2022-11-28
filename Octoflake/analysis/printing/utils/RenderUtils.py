from pathlib import Path

from trimesh.exchange.export import export_mesh

from printing.utils import OctoConfigs


# TODO: Make system for tuning along various axes
def render_grid(grid,
                config=OctoConfigs.default,
                filename="derp",
                dir=None,
                z_min=0,  # Set to None to not crop
                **filename_details):
    if z_min is not None:
        grid.crop(z_min=z_min)
    grid.compute_trimming()

    print(f"Rendering a grid with {len(grid.occ)} octos, using config: {config}.")

    save_mesh(grid.render(config),
              filename=filename + "_" + config.name,
              path=dir,
              **filename_details)


# TODO: Strip off extension if included in the filename
def save_mesh(mesh,
              filename="derp",
              path=None,
              **filename_details):
    default_path = Path.home() / "Desktop" / "shapes"
    path = path if path is not None else default_path
    if not path.exists():
        path.mkdir()
    if filename_details:
        details = "_".join([f"{key}={value:g}" for key, value in filename_details.items()])
        filename += "_" + details
    filename += ".obj"

    # print(filename, filename)

    path = path / filename
    print(f"Saving mesh as {path}")

    filename = str(path)
    with open(filename, "w") as f:
        print(export_mesh(mesh,
                          file_obj=None,
                          file_type="obj",
                          include_normals=False,
                          digits=6),
              file=f)
        f.write("\n")  # Add trailing newline

    print(f"Done!")
