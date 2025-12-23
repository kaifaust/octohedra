"""
RecipeBuilder - A composable fractal builder driven by recipes.

This builder unifies all fractal generation into a single recipe-based system.
Presets (flake, tower, flower) are just pre-defined recipes.

## Recipe Structure

A recipe is a list of **layers**. Each layer is a recursive octahedral structure:

1. **depth** - Recursion depth (1-5), controls size and complexity
2. **shape** - How octahedra branch at each level:
   - 'full': All 6 directions (±x, ±y, ±z) - classic fractal (default)
   - 'horizontal': Only horizontal (±x, ±y) - creates disc layers
   - 'vertical': Only vertical (±z) - creates column structures
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

Horizontal layer on top of full flake:
{
    "layers": [
        {"depth": 3, "shape": "full"},
        {"depth": 2, "shape": "horizontal"}
    ]
}
"""

from dataclasses import dataclass, field
from typing import List, Dict, Literal, Optional, Set, Tuple

from printing.builders.OctoBuilder import OctoBuilder
from printing.grid.OctoGrid import OctoGrid
from printing.grid.OctoVector import OctoVector
from printing.utils.OctoUtil import DOWN, E, N, S, UP, W, X, Y, Z, p2


# Shape types for layers
ShapeType = Literal["full", "horizontal", "vertical", "solid"]


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


def get_preset_recipe(name: str, depth: int = 3, stack_height: int = 1) -> Dict:
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
    layers: List[Dict] = field(default_factory=list)
    center: OctoVector = field(default_factory=OctoVector)

    # For branch recursion: the direction we came from (to compute relative directions)
    origin_dir: Optional[Tuple[int, int]] = None

    # Legacy parameters (for backwards compatibility)
    max_depth: int = 3
    depth_rules: List[Dict] = field(default_factory=list)  # Deprecated

    # Direction sets for different shapes
    HORIZONTAL = [E, N, W, S]
    VERTICAL = [UP, DOWN]
    ALL_DIRS = [E, N, W, S, UP, DOWN]

    # Horizontal direction tuples for branching
    ALL_HORIZ_DIRS = {(1, 0), (-1, 0), (0, 1), (0, -1)}

    def __post_init__(self):
        if not self.layers:
            # No layers specified, create default single flake
            self.layers = [{"depth": self.max_depth}]

    def _compute_branch_directions(
        self,
        directions: List[str],
        origin_dir: Optional[Tuple[int, int]],
    ) -> Set[Tuple[int, int]]:
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

    def _get_directions_for_shape(self, shape: str) -> list:
        """Get the branching directions for a shape type."""
        if shape == "horizontal":
            return [E, N, W, S]
        elif shape == "vertical":
            return [UP, DOWN]
        else:  # 'full' is the default
            return [E, N, W, S, UP, DOWN]

    def _get_tip_positions(self, depth: int, shape: str, center: OctoVector) -> List[OctoVector]:
        """Get the tip positions (outermost cell centers) for a layer.

        For a fractal of given depth and shape, returns the positions of all
        the outermost octahedra (the "tips" where the next layer could grow from).
        """
        if depth <= 0:
            return [center]

        if shape == "solid":
            # For solid, tips are at the corners of the bounding octahedron
            # These are at manhattan distance = radius - 1 from center
            radius = p2(depth + 1) - 1
            tips = []
            # The 6 cardinal tips
            for direction in [E, N, W, S, UP, DOWN]:
                tip_pos = center + OctoVector(*(direction * (radius - 1)))
                tips.append(tip_pos)
            return tips

        # For fractal shapes, recursively find tips
        directions = self._get_directions_for_shape(shape)

        # At depth 1, the tips are the cells placed at depth 0
        if depth == 1:
            tips = []
            for direction in directions:
                tip_pos = center + OctoVector(*(p2(0) * 2 * direction))
                tips.append(tip_pos)
            return tips

        # For deeper fractals, recurse to find all tips
        tips = []
        for direction in directions:
            next_center = center + OctoVector(*(p2(depth - 1) * 2 * direction))
            sub_tips = self._get_tip_positions(depth - 1, shape, next_center)
            tips.extend(sub_tips)

        return tips

    def materialize_additive(self, bonus_iteration=0):
        """Build the complete structure from layers."""
        combined_grid = OctoGrid()
        current_z = 0
        prev_layer = None  # Track previous layer for attach_next_at
        prev_tips = None  # Track tip positions from previous layer

        for layer_idx, layer in enumerate(self.layers):
            layer_depth = layer.get("depth", 3)
            layer_shape = layer.get("shape", "full")
            grow_from = layer.get("grow_from", "center")
            # Branching is enabled if branch_directions is present and non-empty
            layer_branch_dirs = layer.get("branch_directions")
            has_branches = bool(layer_branch_dirs)

            # Determine build centers and layer_z based on grow_from
            if grow_from == "tips" and prev_tips is not None and len(prev_tips) > 0:
                # Build from each tip of the previous layer
                build_centers = prev_tips
                # For tips mode, layer_z is based on max tip z
                layer_z = max(tip.z for tip in prev_tips)
            else:
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
                build_centers = [layer_center]

            # Build this layer's structure from each build center
            layer_grid = OctoGrid()
            all_tips = []

            for build_center in build_centers:
                self._build_layer_recursive(layer_grid, layer_depth, layer_shape, build_center)
                # Collect tips from this build center
                tips = self._get_tip_positions(layer_depth, layer_shape, build_center)
                all_tips.extend(tips)

            # Merge into combined grid
            combined_grid = OctoGrid.merge(combined_grid, layer_grid)

            # Store tips for potential use by next layer
            prev_tips = all_tips

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

        # Get directions based on shape
        directions = self._get_directions_for_shape(shape)

        # Recurse into each direction
        for direction in directions:
            next_center = center + p2(depth - 1) * 2 * direction
            self._build_layer_recursive(grid, depth - 1, shape, next_center)


def generate_from_recipe(
    recipe: Dict,
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
    from printing.utils import OctoConfigs

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

    # Test 3: Horizontal layer on full flake
    print("Testing horizontal layer...")
    builder = RecipeBuilder(
        layers=[
            {"depth": 3, "shape": "full"},
            {"depth": 2, "shape": "horizontal"},
        ],
    )
    builder.render(config=OctoConfigs.config_20_rainbow_speed, filename="Recipe_horizontal")

    # Test 4: Flower (tower with branches)
    print("Testing flower...")
    recipe = get_preset_recipe("flower", depth=4, stack_height=2)
    builder = RecipeBuilder(layers=recipe["layers"])
    builder.render(config=OctoConfigs.config_20_rainbow_speed, filename="Recipe_flower")

    # Test 5: Solid layer
    print("Testing solid...")
    builder = RecipeBuilder(
        layers=[{"depth": 3, "shape": "solid"}],
    )
    builder.render(config=OctoConfigs.config_20_rainbow_speed, filename="Recipe_solid")

    print("All tests complete!")


if __name__ == "__main__":
    test_recipe()
