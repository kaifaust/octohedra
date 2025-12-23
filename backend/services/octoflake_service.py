from typing import List, Dict, Optional

from trimesh.exchange.export import export_mesh

from printing.builders.RecipeBuilder import RecipeBuilder, get_preset_recipe, PRESET_RECIPES
from printing.utils import OctoConfigs

CONFIG_MAP = {
    "rainbow_speed": OctoConfigs.config_20_rainbow_speed,
    "rainbow_gem": OctoConfigs.config_20_rainbow_gem,
    "quantum_gem": OctoConfigs.config_20_quantum_gem,
    "quantum_speed": OctoConfigs.config_20_quantum_Speed,
    "debug": OctoConfigs.giant_debug,
}

# List of available presets
AVAILABLE_PRESETS = list(PRESET_RECIPES.keys())


def _build_mesh(
    layers: List[Dict],
    depth_rules: List[Dict] = None,
    config_name: str = "rainbow_speed",
    six_way: bool = False,
):
    """Build a fractal mesh from a recipe.

    Args:
        layers: List of layer configurations, each with depth and fill_depth
        depth_rules: List of depth rule overrides
        config_name: Render config preset
        six_way: Whether to apply six-way mirroring (for star shapes)

    Returns:
        Trimesh mesh object
    """
    config = CONFIG_MAP.get(config_name, OctoConfigs.config_20_rainbow_speed)

    builder = RecipeBuilder(
        layers=layers,
        depth_rules=depth_rules or [],
    )

    grid = builder.materialize()

    # Apply six-way mirroring if requested (for star preset)
    if six_way:
        grid.six_way()

    grid.crop(z_min=0)
    grid.compute_trimming()

    return grid.render(config)


def generate_from_recipe(
    layers: List[Dict],
    depth_rules: List[Dict] = None,
    config_name: str = "rainbow_speed",
    six_way: bool = False,
) -> str:
    """Generate a fractal mesh from a recipe and return as OBJ string.

    Args:
        layers: List of layer configurations, each with depth and fill_depth
        depth_rules: List of depth rule overrides
        config_name: Render config preset
        six_way: Whether to apply six-way mirroring (for star shapes)

    Returns:
        OBJ file content as string
    """
    mesh = _build_mesh(layers, depth_rules, config_name, six_way)

    obj_content = export_mesh(
        mesh,
        file_obj=None,
        file_type="obj",
        include_normals=False,
        digits=6,
    )
    return obj_content


def generate_stl_from_recipe(
    layers: List[Dict],
    depth_rules: List[Dict] = None,
    config_name: str = "rainbow_speed",
    six_way: bool = False,
) -> bytes:
    """Generate a fractal mesh from a recipe and return as binary STL.

    Args:
        layers: List of layer configurations, each with depth and fill_depth
        depth_rules: List of depth rule overrides
        config_name: Render config preset
        six_way: Whether to apply six-way mirroring (for star shapes)

    Returns:
        Binary STL file content
    """
    mesh = _build_mesh(layers, depth_rules, config_name, six_way)

    stl_content = export_mesh(
        mesh,
        file_obj=None,
        file_type="stl",
    )
    return stl_content


def generate_from_preset(
    preset: str,
    depth: int = 3,
    fill_depth: int = 0,
    stack_height: int = 1,
    config_name: str = "rainbow_speed",
) -> Dict:
    """Get a preset recipe with optional parameter adjustments.

    Args:
        preset: Name of preset (flake, star, tower, hollow_tower, flower, spire, solid_core)
        depth: Base depth for the preset
        fill_depth: Fill depth (for solid interiors)
        stack_height: Number of stacked layers (for tower-like shapes)
        config_name: Render config preset

    Returns:
        Recipe dictionary that can be used for generation
    """
    return get_preset_recipe(preset, depth=depth, fill_depth=fill_depth, stack_height=stack_height)


def generate_fractal(
    layers: List[Dict] = None,
    depth_rules: List[Dict] = None,
    preset: str = None,
    depth: int = 3,
    fill_depth: int = 0,
    stack_height: int = 1,
    config_name: str = "rainbow_speed",
    six_way: bool = False,
    # Legacy parameters (for backwards compatibility)
    shape: str = None,
    recipe: List[Dict] = None,
) -> str:
    """Generate a fractal mesh and return as OBJ string.

    This unified function handles both recipe-based and preset-based generation.

    Args:
        layers: List of layer configurations (new format)
        depth_rules: List of depth rule overrides (new format)
        preset: Name of preset to use as base
        depth: Depth parameter for presets
        fill_depth: Fill depth parameter for presets
        stack_height: Stack height parameter for presets
        config_name: Render config preset
        six_way: Whether to apply six-way mirroring (for star shapes)

        # Legacy parameters
        shape: Old shape parameter (maps to preset)
        recipe: Old recipe parameter (maps to depth_rules)

    Returns:
        OBJ file content as string
    """
    # Handle legacy parameters
    if shape is not None and preset is None:
        preset = shape
    if recipe is not None and depth_rules is None:
        depth_rules = recipe

    # Track whether to apply six_way
    apply_six_way = six_way

    # If layers not provided, get from preset
    if layers is None:
        if preset is not None:
            recipe_dict = get_preset_recipe(preset, depth=depth, fill_depth=fill_depth, stack_height=stack_height)
            layers = recipe_dict["layers"]
            # Merge preset depth_rules with any provided rules
            preset_rules = recipe_dict.get("depth_rules", [])
            if depth_rules:
                # User rules override preset rules
                rule_map = {r["depth"]: r for r in preset_rules}
                for r in depth_rules:
                    rule_map[r["depth"]] = r
                depth_rules = list(rule_map.values())
            else:
                depth_rules = preset_rules
            # Get six_way from preset if not explicitly provided
            if not six_way and recipe_dict.get("six_way", False):
                apply_six_way = True
        else:
            # Default to simple flake
            layers = [{"depth": depth, "fill_depth": fill_depth}]

    return generate_from_recipe(
        layers=layers,
        depth_rules=depth_rules,
        config_name=config_name,
        six_way=apply_six_way,
    )
