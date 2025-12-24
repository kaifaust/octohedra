"""
RecipeBuilder - A composable fractal builder driven by recipes.

This builder unifies all fractal generation into a single recipe-based system.
Presets (flake, tower, flower) are just pre-defined recipes.

## Recipe Structure

A recipe is a list of **layers**. Each layer is a recursive octahedral structure:

1. **depth** - Recursion depth (1-5), controls size and complexity
2. **shape** - How octahedra branch at each level:
   - 'fractal': All 6 directions (±x, ±y, ±z) - classic fractal (default)
   - 'solid': Fill solid, no recursion
3. **attach_next_at** - Which depth level the next layer attaches to (default: top)
4. **branch_directions** - Spawn sub-structures in these directions

## Example Recipes

Simple flake (depth 3):
{
    "layers": [{"depth": 3}]
}

Tower (depth 4, stacking down to 1):
{
    "layers": [
        {"depth": 4},
        {"depth": 3},
        {"depth": 2},
        {"depth": 1}
    ]
}
"""

from dataclasses import dataclass, field
from typing import Literal

from octohedra.builders.OctoBuilder import OctoBuilder
from octohedra.grid.OctoGrid import OctoGrid
from octohedra.grid.OctoVector import OctoVector
from octohedra.utils.OctoUtil import DOWN, UP, E, N, S, W, Z, p2

# Shape types for layers
ShapeType = Literal["fractal", "solid"]


# Pre-defined recipes for common shapes
PRESET_RECIPES = {
    "flake": {
        "layers": [{"depth": 3}],
    },
    "tower": {
        # Tower: decreasing flakes stacked vertically
        "layers": [
            {"depth": 3},
            {"depth": 2},
            {"depth": 1},
        ],
    },
    "evil_tower": {
        # Evil tower: tower with sub-towers branching in 4 directions at each level
        "layers": [
            {"depth": 3, "branch_directions": ["outwards", "inwards", "sideways", "upwards"]},
            {"depth": 2, "branch_directions": ["outwards", "inwards", "sideways", "upwards"]},
            {"depth": 1},
        ],
    },
    "flower": {
        # Flower: tower with horizontal branches at each layer
        "layers": [
            {"depth": 4, "branch_directions": ["outwards", "sideways", "upwards"]},
            {"depth": 3, "branch_directions": ["outwards", "sideways", "upwards"]},
            {"depth": 2, "branch_directions": ["outwards", "sideways", "upwards"]},
            {"depth": 1},
        ],
    },
}


def get_preset_recipe(name: str, depth: int = 3, stack_height: int = 1) -> dict:
    """Get a preset recipe, optionally adjusting parameters.

    Args:
        name: Preset name
        depth: Base depth (complexity) of the shape
        stack_height: Number of additional layers for tower-like shapes
    """
    if name not in PRESET_RECIPES:
        name = "flake"

    if name == "flake":
        return {
            "layers": [{"depth": depth}],
        }

    elif name == "tower":
        # Tower: flakes from depth down to (depth - stack_height)
        layers = []
        min_depth = max(1, depth - stack_height)
        for d in range(depth, min_depth - 1, -1):
            layers.append({"depth": d})
        return {"layers": layers}

    elif name == "evil_tower":
        # Evil tower: tower with sub-towers branching in 4 directions at each level
        layers = []
        min_depth = max(1, depth - stack_height)
        for d in range(depth, min_depth - 1, -1):
            layer = {"depth": d}
            # All layers except the smallest get branches
            if d > min_depth:
                layer["branch_directions"] = ["outwards", "inwards", "sideways", "upwards"]
            layers.append(layer)
        return {"layers": layers}

    elif name == "flower":
        # Flower: tower with branches at each layer (except the last)
        layers = []
        min_depth = max(1, depth - stack_height - 1)
        for d in range(depth, min_depth - 1, -1):
            layer = {"depth": d}
            # All layers except the smallest get branches
            if d > min_depth:
                layer["branch_directions"] = ["outwards", "sideways", "upwards"]
            layers.append(layer)
        return {"layers": layers}

    # Fallback
    return {
        "layers": [{"depth": depth}],
    }


@dataclass
class RecipeBuilder(OctoBuilder):
    """
    A builder that constructs fractals from recipes.

    Each layer is a recursive octahedral structure with a shape that determines
    how it branches. Layers are stacked vertically, with attach points controlling
    where each layer connects to the previous one.
    """

    # Recipe parameters
    layers: list[dict] = field(default_factory=list)
    center: OctoVector = field(default_factory=OctoVector)

    # For branch recursion: the direction we came from (to compute relative directions)
    origin_dir: tuple[int, int] | None = None

    # Legacy parameters (for backwards compatibility)
    max_depth: int = 3
    depth_rules: list[dict] = field(default_factory=list)  # Deprecated

    # Horizontal direction tuples for branching
    ALL_HORIZ_DIRS = {(1, 0), (-1, 0), (0, 1), (0, -1)}

    def __post_init__(self):
        if not self.layers:
            # No layers specified, create default single flake
            self.layers = [{"depth": self.max_depth}]

    def _compute_branch_directions(
        self,
        directions: list[str],
        origin_dir: tuple[int, int] | None,
    ) -> set[tuple[int, int]]:
        """
        Compute branch directions based on semantic options and origin direction.

        Args:
            directions: List of semantic directions like 'outwards', 'inwards', 'sideways', 'upwards'
            origin_dir: The direction we came from (e.g., (1, 0) if we branched from +x)
                       None for the root level (all horizontal directions are valid)

        Returns:
            Set of (dx, dy) tuples representing allowed horizontal branch directions
        """
        result = set()

        # If no origin, we're at the root - use all horizontal directions
        if origin_dir is None:
            # At root, 'outwards' means all 4 directions
            if "outwards" in directions:
                result.update(self.ALL_HORIZ_DIRS)
            return result

        ox, oy = origin_dir

        for d in directions:
            if d == "outwards":
                # Continue away from parent (same direction we traveled to get here)
                result.add((ox, oy))
            elif d == "inwards":
                # Back toward parent (opposite of direction we traveled)
                result.add((-ox, -oy))
            elif d == "sideways":
                # Perpendicular to origin direction
                if ox != 0:
                    result.add((0, 1))
                    result.add((0, -1))
                else:
                    result.add((1, 0))
                    result.add((-1, 0))
            # 'upwards' is handled separately (controls +z continuation)

        return result

    def materialize_additive(self, bonus_iteration=0):
        """Build the complete structure from layers."""
        combined_grid = OctoGrid()
        current_z = 0
        prev_layer = None  # Track previous layer for attach_next_at

        for layer_idx, layer in enumerate(self.layers):
            layer_depth = layer.get("depth", 3)
            layer_shape = layer.get("shape", "fractal")
            # Branching is enabled if branch_directions is present and non-empty
            layer_branch_dirs = layer.get("branch_directions")
            has_branches = bool(layer_branch_dirs)

            # Calculate z position based on previous layer's attach_next_at
            if prev_layer is not None:
                attach_at = prev_layer.get("attach_next_at")
                prev_depth = prev_layer.get("depth", 3)
                if attach_at is not None:
                    # Attach at a specific depth level of the previous layer
                    prev_layer_center_z = current_z - p2(prev_depth + 1)
                    layer_z = prev_layer_center_z + p2(attach_at + 1)
                else:
                    layer_z = current_z
            else:
                layer_z = current_z

            layer_center = self.center + Z * layer_z

            # Build this layer's structure
            layer_grid = OctoGrid()
            self._build_layer_recursive(layer_grid, layer_depth, layer_shape, layer_center)

            # Merge into combined grid
            combined_grid = OctoGrid.merge(combined_grid, layer_grid)

            # Handle branches
            if has_branches:
                # Get remaining layers for sub-structures
                remaining_layers = self.layers[layer_idx + 1:]
                if remaining_layers:
                    # Check if upwards is included (controls whether central stack continues)
                    include_upwards = "upwards" in layer_branch_dirs

                    # Compute which horizontal directions to branch based on origin
                    current_dirs = self._compute_branch_directions(layer_branch_dirs, self.origin_dir)

                    # Spawn sub-structures in computed horizontal directions
                    branch_offset = p2(layer_depth + 1)
                    branch_z_offset = layer_z + p2(layer_depth + 1) - p2(layer_depth)

                    for dx, dy in current_dirs:
                        # Calculate branch position
                        branch_center = self.center + OctoVector(
                            branch_offset * dx,
                            branch_offset * dy,
                            branch_z_offset
                        )

                        # The sub-builder's origin is the direction we're branching
                        sub_origin = (dx, dy)

                        # Build sub-structure with remaining layers
                        sub_builder = RecipeBuilder(
                            layers=remaining_layers,
                            center=branch_center,
                            origin_dir=sub_origin,
                        )
                        sub_grid = sub_builder.materialize_additive()
                        combined_grid = OctoGrid.merge(combined_grid, sub_grid)

                    # If upwards is excluded, skip remaining layers at center
                    if not include_upwards:
                        break

            # Move up for next layer
            current_z = layer_z + p2(layer_depth + 1)
            prev_layer = layer

        return combined_grid

    def _build_layer_recursive(self, grid: OctoGrid, depth: int, shape: str, center: OctoVector):
        """Recursively build a layer with the given shape applied uniformly."""
        if depth <= 0:
            grid.insert_cell(center)
            return

        # Handle solid shape - fill the entire region
        # The radius should match the extent of an equivalent "full" fractal
        # A depth-N fractal extends to p2(depth+1) - 2 from center
        # But fill uses strict < so we need radius = p2(depth+1) - 1 to include that extent
        if shape == "solid":
            radius = p2(depth + 1) - 1
            grid.fill(radius, center)
            return

        # For 'fractal' shape, branch in all 6 cardinal directions
        # (solid is already handled above)
        for direction in [E, N, W, S, UP, DOWN]:
            next_center = center + p2(depth - 1) * 2 * direction
            self._build_layer_recursive(grid, depth - 1, shape, next_center)


def generate_from_recipe(
    recipe: dict,
    config=None,
) -> OctoGrid:
    """
    Generate a fractal grid from a recipe dictionary.

    Args:
        recipe: Recipe dictionary with layers
        config: Optional render config

    Returns:
        OctoGrid containing the generated fractal
    """
    builder = RecipeBuilder(
        layers=recipe.get("layers", []),
    )
    return builder.materialize()


def test_recipe():
    """Test the RecipeBuilder with various configurations."""
    from octohedra.utils import OctoConfigs

    # Test 1: Simple flake (default)
    print("Testing simple flake...")
    builder = RecipeBuilder(
        layers=[{"depth": 3}],
    )
    builder.render(config=OctoConfigs.config_20_rainbow_speed, filename="Recipe_flake")

    # Test 2: Tower-like (multiple stacked layers)
    print("Testing tower...")
    recipe = get_preset_recipe("tower", depth=4, stack_height=3)
    builder = RecipeBuilder(layers=recipe["layers"])
    builder.render(config=OctoConfigs.config_20_rainbow_speed, filename="Recipe_tower")

    # Test 3: Flower (tower with branches)
    print("Testing flower...")
    recipe = get_preset_recipe("flower", depth=4, stack_height=2)
    builder = RecipeBuilder(layers=recipe["layers"])
    builder.render(config=OctoConfigs.config_20_rainbow_speed, filename="Recipe_flower")

    # Test 4: Solid layer
    print("Testing solid...")
    builder = RecipeBuilder(
        layers=[{"depth": 3, "shape": "solid"}],
    )
    builder.render(config=OctoConfigs.config_20_rainbow_speed, filename="Recipe_solid")

    print("All tests complete!")


if __name__ == "__main__":
    test_recipe()
