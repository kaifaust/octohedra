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
PresetType = Literal["flake", "tower", "evil_tower", "flower"]

# Branch directions (relative to parent direction)
# - outwards: away from parent (if came from +x, go -x, +y, -y)
# - inwards: back toward parent (if came from +x, go +x)
# - sideways: perpendicular to parent (if came from +x, go +y, -y)
# - upwards: continue building central stack (+z)
BranchDirection = Literal["outwards", "inwards", "sideways", "upwards"]

class Layer(BaseModel):
    """A single layer in the recipe - the fundamental building block."""
    depth: int = Field(default=3, ge=1, le=5, description="Recursion depth (1-5), controls size and complexity")
    shape: LayerShape | None = Field(
        default=None,
        description="How octahedra branch at each level. Default: 'fractal'"
    )
    attach_next_at: int | None = Field(
        default=None, ge=1, le=5,
        description="Next layer attaches at this depth level (default: top)"
    )
    branch_directions: list[BranchDirection] | None = Field(
        default=None,
        description="Which directions to spawn sub-towers (empty/null = no branching)"
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
        description="Start from a preset recipe (flake, tower, evil_tower, flower)"
    )

    # Parameters for preset-based generation
    depth: int = Field(default=3, ge=1, le=5, description="Base depth (used with presets)")
    stack_height: int = Field(default=1, ge=1, le=4, description="Stack height (used with tower-like presets)")

    # Six-way mirroring (for star-like shapes)
    six_way: bool = Field(default=False, description="Apply six-way mirroring")

    # Render config
    config: str = Field(default="rainbow_speed", description="Render config preset")


@router.post("/generate", response_class=PlainTextResponse)
async def generate(request: GenerateRequest):
    """Generate a fractal using the recipe system.

    ## Recipe System

    Each layer is a recursive octahedral structure with:
    - `depth`: Size/complexity (1-5). Higher = more detail and larger.
    - `shape`: How octahedra branch at each level:
      - `fractal`: All 6 directions (±x, ±y, ±z) - classic fractal
      - `solid`: Fill solid, no recursion
    - `attach_next_at`: Which depth level the next layer attaches to
    - `branch_directions`: Spawn sub-structures in these directions

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

    Use a preset:
    ```json
    {"preset": "tower", "depth": 4, "stack_height": 3}
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
    if layers_dicts is None:
        if request.preset is not None:
            recipe_dict = get_preset_recipe(
                request.preset,
                depth=request.depth,
                stack_height=request.stack_height
            )
            layers_dicts = recipe_dict["layers"]
            six_way = six_way or recipe_dict.get("six_way", False)
        else:
            layers_dicts = [{"depth": request.depth}]

    stl_content = generate_stl_from_recipe(
        layers=layers_dicts,
        config_name=request.config,
        six_way=six_way,
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

    return {
        "preset": preset_name,
        "layers": recipe["layers"],
        "six_way": recipe.get("six_way", False),
    }
