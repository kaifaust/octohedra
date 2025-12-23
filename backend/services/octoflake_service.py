from trimesh.exchange.export import export_mesh

from printing.builders.FlakeBuilder import FlakeBuilder
from printing.utils import OctoConfigs

CONFIG_MAP = {
    "rainbow_speed": OctoConfigs.config_20_rainbow_speed,
    "rainbow_gem": OctoConfigs.config_20_rainbow_gem,
    "quantum_gem": OctoConfigs.config_20_quantum_gem,
    "quantum_speed": OctoConfigs.config_20_quantum_Speed,
    "debug": OctoConfigs.giant_debug,
}


def generate_fractal(iteration: int, scale: int, config_name: str) -> str:
    """Generate a fractal mesh and return as OBJ string."""
    config = CONFIG_MAP.get(config_name, OctoConfigs.config_20_rainbow_speed)

    builder = FlakeBuilder(iteration=iteration, scale=scale)
    grid = builder.materialize()
    grid.crop(z_min=0)
    grid.compute_trimming()

    mesh = grid.render(config)

    obj_content = export_mesh(
        mesh,
        file_obj=None,
        file_type="obj",
        include_normals=False,
        digits=6,
    )
    return obj_content
