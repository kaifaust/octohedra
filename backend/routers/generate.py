from typing import Literal, List, Optional

from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, Field

from services.octoflake_service import generate_fractal, AVAILABLE_PRESETS

router = APIRouter()

# Node types for depth rules
NodeType = Literal["flake", "solid", "horizontal", "vertical"]

# Available preset names (original artist shapes only)
PresetType = Literal["flake", "tower", "evil_tower", "flower"]

# Branch directions
BranchDirection = Literal["+x", "-x", "+y", "-y"]


class DepthRule(BaseModel):
    """A depth rule that modifies branching behavior at a specific depth."""
    depth: int = Field(..., ge=1, le=5, description="Depth level this applies to")
    type: NodeType = Field(default="flake", description="Node type at this depth")


class Layer(BaseModel):
    """A single layer in the recipe (a positioned flake)."""
    depth: int = Field(default=3, ge=1, le=5, description="Flake depth for this layer")
    fill_depth: int = Field(default=0, ge=0, le=5, description="Fill depth (0 = fractal, >0 = solid interior)")
    z_offset: Optional[int] = Field(default=None, description="Manual Z offset (auto-calculated if omitted)")
    branches: bool = Field(default=False, description="Spawn sub-structures in horizontal directions")
    branch_directions: Optional[List[BranchDirection]] = Field(
        default=None,
        description="Which directions to branch (default: all 4). Options: +x, -x, +y, -y"
    )
    branch_exclude_origin: bool = Field(
        default=True,
        description="Each sub-branch excludes direction back to its parent (symmetric orbiting)"
    )
    depth_rules: Optional[List[DepthRule]] = Field(
        default=None,
        description="Per-layer depth rules that override global rules"
    )


class GenerateRequest(BaseModel):
    """Request body for fractal generation.

    The recipe system has two main components:
    - layers: Stack of flakes positioned vertically (like Tower/Star presets)
    - depth_rules: Modify branching behavior at specific depths

    You can also use a preset as a starting point and modify from there.
    """
    # Recipe components (new format)
    layers: Optional[List[Layer]] = Field(
        default=None,
        description="List of layer configurations. Each layer is a flake at a vertical position."
    )
    depth_rules: Optional[List[DepthRule]] = Field(
        default=None,
        description="List of depth rules that modify branching behavior"
    )

    # Preset support
    preset: Optional[PresetType] = Field(
        default=None,
        description="Start from a preset recipe (flake, star, tower, hollow_tower, flower, spire, solid_core)"
    )

    # Parameters for preset-based generation
    depth: int = Field(default=3, ge=1, le=5, description="Base depth (used with presets)")
    fill_depth: int = Field(default=0, ge=0, le=3, description="Fill depth (used with presets)")
    stack_height: int = Field(default=1, ge=1, le=4, description="Stack height (used with tower-like presets)")

    # Render config
    config: str = Field(default="rainbow_speed", description="Render config preset")


class PresetInfo(BaseModel):
    """Information about a preset recipe."""
    name: str
    description: str
    layers: List[Layer]
    depth_rules: List[DepthRule]


@router.post("/generate", response_class=PlainTextResponse)
async def generate(request: GenerateRequest):
    """Generate a fractal using the unified recipe system.

    ## Recipe System

    The recipe has two main components:

    ### Layers
    Stack flakes vertically. Each layer has:
    - `depth`: Size/complexity of the flake (1-5)
    - `fill_depth`: How much to fill solid (0 = pure fractal)
    - `z_offset`: Manual positioning (optional)

    ### Depth Rules
    Modify branching at specific depths:
    - `flake`: Full 6-way branching (default)
    - `solid`: Fill solid, stop recursion
    - `horizontal`: Only X/Y directions (creates disc layers)
    - `vertical`: Only up/down (creates columns)
    - `skip`: Skip this depth, continue recursing

    ## Examples

    Simple flake:
    ```json
    {"layers": [{"depth": 3, "fill_depth": 0}]}
    ```

    Tower:
    ```json
    {"layers": [
        {"depth": 3, "fill_depth": 0},
        {"depth": 2, "fill_depth": 0},
        {"depth": 1, "fill_depth": 0}
    ]}
    ```

    Flake with horizontal branching at depth 2:
    ```json
    {
        "layers": [{"depth": 3, "fill_depth": 0}],
        "depth_rules": [{"depth": 2, "type": "horizontal"}]
    }
    ```

    Use a preset:
    ```json
    {"preset": "star", "depth": 4, "stack_height": 2}
    ```

    Customize a preset:
    ```json
    {
        "preset": "tower",
        "depth": 3,
        "depth_rules": [{"depth": 1, "type": "solid"}]
    }
    ```
    """
    # Convert Pydantic models to dicts
    layers_dicts = [layer.model_dump() for layer in request.layers] if request.layers else None
    depth_rules_dicts = [rule.model_dump() for rule in request.depth_rules] if request.depth_rules else None

    obj_content = generate_fractal(
        layers=layers_dicts,
        depth_rules=depth_rules_dicts,
        preset=request.preset,
        depth=request.depth,
        fill_depth=request.fill_depth,
        stack_height=request.stack_height,
        config_name=request.config,
    )

    return PlainTextResponse(
        content=obj_content,
        media_type="model/obj",
        headers={"Content-Disposition": "inline; filename=fractal.obj"},
    )


@router.get("/presets")
async def get_presets() -> List[str]:
    """Get list of available preset names."""
    return AVAILABLE_PRESETS


@router.get("/presets/{preset_name}")
async def get_preset(preset_name: PresetType, depth: int = 3, fill_depth: int = 0, stack_height: int = 1) -> dict:
    """Get the recipe for a preset with optional parameter adjustments.

    This allows the frontend to populate the recipe editor when a preset is selected.
    """
    from services.octoflake_service import generate_from_preset

    recipe = generate_from_preset(
        preset=preset_name,
        depth=depth,
        fill_depth=fill_depth,
        stack_height=stack_height,
    )

    return {
        "preset": preset_name,
        "layers": recipe["layers"],
        "depth_rules": recipe.get("depth_rules", []),
        "six_way": recipe.get("six_way", False),
    }
