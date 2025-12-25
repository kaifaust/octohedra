from typing import Literal

from fastapi import APIRouter
from fastapi.responses import PlainTextResponse, Response
from pydantic import BaseModel, Field

from services.octohedra_service import AVAILABLE_PRESETS, generate_fractal, generate_stl_from_recipe

router = APIRouter()

# Shape types for layers - how octahedra branch
# - fractal: branch in all 6 directions (±x, ±y, ±z) - classic fractal
# - solid: fill solid (no fractal recursion)
LayerShape = Literal["fractal", "solid"]

# Available preset names (original artist shapes only)
PresetType = Literal["flake", "tower", "evil_tower", "flower", "temple_complex"]

# Branch directions (relative to parent direction)
# - outwards: away from parent (if came from +x, go -x, +y, -y)
# - inwards: back toward parent (if came from +x, go +x)
# - sideways: perpendicular to parent (if came from +x, go +y, -y)
# - upwards: continue building central stack (+z)
BranchDirection = Literal["outwards", "inwards", "sideways", "upwards"]

# Branch styles - how sub-structures are built (geometry)
# - waist: Sub-towers at waist (narrower point) - EvilTowerX style
# - edge: Sub-towers at edge (full extent) - FlowerTower style
BranchStyle = Literal["waist", "edge"]

# Spawn directions - where sub-structures appear horizontally
SpawnDirection = Literal["out", "in", "side"]

class Layer(BaseModel):
    """A single layer in the recipe - the fundamental building block.

    In the OG project, this corresponds to one 'iteration' level in a tower.

    New generative model:
    - size: How big this layer is (1-5)
    - spawn: Where to create sub-structures horizontally (out/in/side)
    - bloom: Do spawns continue the branching pattern? (recursive like Flower)
    - echo: Do spawns contain the full recipe at smaller scale? (like Temple Complex)
    """
    # Size of this layer (1-5)
    depth: int = Field(default=3, ge=1, le=5, description="Iteration size (1-5), controls size and complexity")

    # Shape - how octahedra branch internally
    shape: LayerShape | None = Field(
        default=None,
        description="How octahedra branch at each level. Default: 'fractal'"
    )

    # Spawn - where to create sub-structures (new unified model)
    spawn: list[SpawnDirection] | None = Field(
        default=None,
        description="Where to spawn sub-structures: 'out' (away), 'in' (toward parent), 'side' (perpendicular)"
    )

    # Bloom - spawns continue the branching pattern recursively (like Flower)
    bloom: bool = Field(
        default=False,
        description="Do spawns continue the branching pattern? (recursive like Flower)"
    )

    # Echo - spawns contain the full recipe at smaller scale (like Temple Complex)
    echo: bool = Field(
        default=False,
        description="Do spawns contain the full recipe at reduced scale? (like Temple Complex)"
    )

    # Legacy fields for backwards compatibility
    branch_directions: list[BranchDirection] | None = Field(
        default=None,
        description="[DEPRECATED] Use 'spawn' instead. Which directions to spawn sub-towers"
    )
    branch_style: BranchStyle | None = Field(
        default=None,
        description="[DEPRECATED] Use 'bloom' instead. Where sub-structures attach"
    )


class GenerateRequest(BaseModel):
    """Request body for fractal generation.

    The recipe system uses layers as the fundamental building block.
    Each layer is a recursive octahedral structure with a specific shape.
    """
    # Recipe: list of layers
    layers: list[Layer] | None = Field(
        default=None,
        description="List of layer configurations. Each layer has a depth, shape, and attach point."
    )

    # Preset support
    preset: PresetType | None = Field(
        default=None,
        description="Start from a preset recipe (flake, tower, evil_tower, flower, temple_complex)"
    )

    # Parameters for preset-based generation
    depth: int = Field(default=3, ge=1, le=5, description="Base depth (used with presets)")
    stack_height: int = Field(default=1, ge=1, le=4, description="Stack height (used with tower-like presets)")

    # Six-way mirroring (for star-like shapes)
    six_way: bool = Field(default=False, description="Apply six-way mirroring")

    # Legacy grid expansion - prefer using 'echo' in layers instead
    grid_depth: int | None = Field(default=None, ge=2, le=5, description="[DEPRECATED] Use 'echo' in layers. Grid expansion depth")
    grid_min_depth: int = Field(default=2, ge=1, le=4, description="[DEPRECATED] Use 'echo' in layers. Stop grid expansion at this depth")

    # Render config
    config: str = Field(default="rainbow_speed", description="Render config preset")


@router.post("/generate", response_class=PlainTextResponse)
async def generate(request: GenerateRequest):
    """Generate a fractal using the recipe system.

    ## Layer Model

    Each layer describes a recursive octahedral structure:
    - `depth`: Size (1-5). Higher = larger and more complex.
    - `shape`: How octahedra branch internally ('fractal' or 'solid')
    - `spawn`: Where to create sub-structures ('out', 'in', 'side')
    - `bloom`: Do spawns continue branching? (recursive like Flower)
    - `echo`: Do spawns contain full recipe at smaller scale? (like Temple Complex)

    ## Examples

    Simple flake:
    ```json
    {"layers": [{"depth": 3}]}
    ```

    Tower (stacked layers):
    ```json
    {"layers": [
        {"depth": 3},
        {"depth": 2},
        {"depth": 1}
    ]}
    ```

    Evil Tower (tower with spawns, no bloom):
    ```json
    {"layers": [
        {"depth": 3, "spawn": ["out", "in", "side"]},
        {"depth": 2, "spawn": ["out", "in", "side"]},
        {"depth": 1}
    ]}
    ```

    Flower (tower with blooming spawns):
    ```json
    {"layers": [
        {"depth": 4, "spawn": ["out", "side"], "bloom": true},
        {"depth": 3, "spawn": ["out", "side"], "bloom": true},
        {"depth": 2}
    ]}
    ```

    Temple Complex (tower with echoing spawns):
    ```json
    {"layers": [
        {"depth": 4, "spawn": ["out", "in", "side"], "echo": true},
        {"depth": 3, "spawn": ["out", "in", "side"]},
        {"depth": 2}
    ]}
    ```
    """
    # Convert Pydantic models to dicts
    layers_dicts = [layer.model_dump() for layer in request.layers] if request.layers else None

    obj_content = generate_fractal(
        layers=layers_dicts,
        preset=request.preset,
        depth=request.depth,
        stack_height=request.stack_height,
        config_name=request.config,
        six_way=request.six_way,
        grid_depth=request.grid_depth,
        grid_min_depth=request.grid_min_depth,
    )

    return PlainTextResponse(
        content=obj_content,
        media_type="model/obj",
        headers={"Content-Disposition": "inline; filename=fractal.obj"},
    )


@router.post("/generate/stl")
async def generate_stl(request: GenerateRequest):
    """Generate a fractal as binary STL (for 3D printing).

    Same parameters as /generate, but returns binary STL instead of OBJ.
    """
    from services.octohedra_service import get_preset_recipe

    # Convert Pydantic models to dicts
    layers_dicts = [layer.model_dump() for layer in request.layers] if request.layers else None

    # Resolve layers from preset if needed
    six_way = request.six_way
    grid_depth = request.grid_depth
    grid_min_depth = request.grid_min_depth
    if layers_dicts is None:
        if request.preset is not None:
            recipe_dict = get_preset_recipe(
                request.preset,
                depth=request.depth,
                stack_height=request.stack_height
            )
            layers_dicts = recipe_dict["layers"]
            six_way = six_way or recipe_dict.get("six_way", False)
            # Get grid parameters from preset
            if grid_depth is None and recipe_dict.get("grid_depth") is not None:
                grid_depth = recipe_dict["grid_depth"]
                grid_min_depth = recipe_dict.get("grid_min_depth", 2)
        else:
            layers_dicts = [{"depth": request.depth}]

    stl_content = generate_stl_from_recipe(
        layers=layers_dicts,
        config_name=request.config,
        six_way=six_way,
        grid_depth=grid_depth,
        grid_min_depth=grid_min_depth,
    )

    return Response(
        content=stl_content,
        media_type="model/stl",
        headers={"Content-Disposition": "attachment; filename=octohedra.stl"},
    )


@router.get("/presets")
async def get_presets() -> list[str]:
    """Get list of available preset names."""
    return AVAILABLE_PRESETS


@router.get("/presets/{preset_name}")
async def get_preset(preset_name: PresetType, depth: int = 3, stack_height: int = 1) -> dict:
    """Get the recipe for a preset with optional parameter adjustments.

    This allows the frontend to populate the recipe editor when a preset is selected.
    """
    from octohedra.builders.RecipeBuilder import get_preset_recipe

    recipe = get_preset_recipe(
        name=preset_name,
        depth=depth,
        stack_height=stack_height,
    )

    result = {
        "preset": preset_name,
        "layers": recipe["layers"],
        "six_way": recipe.get("six_way", False),
    }

    # Include grid parameters if present in the recipe
    if recipe.get("grid_depth") is not None:
        result["grid_depth"] = recipe["grid_depth"]
        result["grid_min_depth"] = recipe.get("grid_min_depth", 2)

    return result
