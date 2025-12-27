import multiprocessing as mp

from octohedra.builders.RecipeBuilder import PRESET_RECIPES, get_preset_recipe

# List of available presets
AVAILABLE_PRESETS = list(PRESET_RECIPES.keys())


def _generate_in_subprocess(queue, layers, config_name, six_way, grid_depth, grid_min_depth, file_type):
    """Worker function that runs in a subprocess to generate mesh."""
    from trimesh.exchange.export import export_mesh
    from octohedra.builders.RecipeBuilder import RecipeBuilder
    from octohedra.utils import OctoConfigs

    config_map = {
        "rainbow_speed": OctoConfigs.config_20_rainbow_speed,
        "rainbow_gem": OctoConfigs.config_20_rainbow_gem,
        "quantum_gem": OctoConfigs.config_20_quantum_gem,
        "quantum_speed": OctoConfigs.config_20_quantum_Speed,
        "debug": OctoConfigs.giant_debug,
    }

    config = config_map.get(config_name, OctoConfigs.config_20_rainbow_speed)

    builder = RecipeBuilder(
        layers=layers,
        grid_depth=grid_depth,
        grid_min_depth=grid_min_depth,
    )

    grid = builder.materialize()

    if six_way:
        grid.six_way()

    grid.crop(z_min=0)
    grid.compute_trimming()

    mesh = grid.render(config)

    if file_type == "stl":
        result = export_mesh(mesh, file_obj=None, file_type="stl")
    else:
        result = export_mesh(mesh, file_obj=None, file_type="obj", include_normals=False, digits=6)

    queue.put(result)


def _run_in_subprocess(layers, config_name, six_way, grid_depth, grid_min_depth, file_type):
    """Run mesh generation in a subprocess and return the result."""
    ctx = mp.get_context("spawn")
    queue = ctx.Queue()
    proc = ctx.Process(
        target=_generate_in_subprocess,
        args=(queue, layers, config_name, six_way, grid_depth, grid_min_depth, file_type),
    )
    proc.start()
    result = queue.get()
    proc.join()
    return result


def generate_from_recipe(
    layers: list[dict],
    config_name: str = "rainbow_speed",
    six_way: bool = False,
    grid_depth: int | None = None,
    grid_min_depth: int = 2,
) -> str:
    """Generate a fractal mesh from a recipe and return as OBJ string.

    Runs in a subprocess to fully release memory after generation.
    """
    return _run_in_subprocess(layers, config_name, six_way, grid_depth, grid_min_depth, "obj")


def generate_stl_from_recipe(
    layers: list[dict],
    config_name: str = "rainbow_speed",
    six_way: bool = False,
    grid_depth: int | None = None,
    grid_min_depth: int = 2,
) -> bytes:
    """Generate a fractal mesh from a recipe and return as binary STL.

    Runs in a subprocess to fully release memory after generation.
    """
    return _run_in_subprocess(layers, config_name, six_way, grid_depth, grid_min_depth, "stl")


def generate_fractal(
    layers: list[dict] = None,
    preset: str = None,
    depth: int = 3,
    stack_height: int = 1,
    config_name: str = "rainbow_speed",
    six_way: bool = False,
    grid_depth: int | None = None,
    grid_min_depth: int = 2,
) -> str:
    """Generate a fractal mesh and return as OBJ string.

    This unified function handles both recipe-based and preset-based generation.

    Args:
        layers: List of layer configurations
        preset: Name of preset to use as base
        depth: Depth parameter for presets
        stack_height: Stack height parameter for presets
        config_name: Render config preset
        six_way: Whether to apply six-way mirroring (for star shapes)
        grid_depth: For grid structures, the expansion depth (enables 2D grid)
        grid_min_depth: For grid structures, stop expansion at this depth

    Returns:
        OBJ file content as string
    """
    apply_six_way = six_way
    apply_grid_depth = grid_depth
    apply_grid_min_depth = grid_min_depth

    # If layers not provided, get from preset
    if layers is None:
        if preset is not None:
            recipe_dict = get_preset_recipe(name=preset, depth=depth, stack_height=stack_height)
            layers = recipe_dict["layers"]
            # Get six_way from preset if not explicitly provided
            if not six_way and recipe_dict.get("six_way", False):
                apply_six_way = True
            # Get grid parameters from preset
            if apply_grid_depth is None and recipe_dict.get("grid_depth") is not None:
                apply_grid_depth = recipe_dict["grid_depth"]
                apply_grid_min_depth = recipe_dict.get("grid_min_depth", 2)
        else:
            # Default to simple flake
            layers = [{"depth": depth}]

    return generate_from_recipe(
        layers=layers,
        config_name=config_name,
        six_way=apply_six_way,
        grid_depth=apply_grid_depth,
        grid_min_depth=apply_grid_min_depth,
    )
