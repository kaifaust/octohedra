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
4. **branch_directions** - Spawn sub-structures in these directions:
   - 'outwards': Continue away from parent direction
   - 'inwards': Back toward parent
   - 'sideways': Perpendicular to parent
   - 'upwards': Continue building central stack (+z)
5. **branch_style** - How sub-structures are built:
   - 'evil': Sub-towers at waist, simple tower (no further branching) - EvilTowerX style
   - 'flower': Sub-towers at edge, recursive branching continues - FlowerTower style

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
from octohedra.utils.OctoUtil import DOWN, UP, E, N, S, W, X, Y, Z, p2, f_rad

# Shape types for layers
ShapeType = Literal["fractal", "solid"]

# Branch styles - determines geometry of sub-structures
BranchStyle = Literal["evil", "flower"]


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
        # Uses "evil" branch style: sub-towers at waist, simple towers (no further branching)
        "layers": [
            {"depth": 3, "branch_directions": ["outwards", "inwards", "sideways", "upwards"], "branch_style": "evil"},
            {"depth": 2, "branch_directions": ["outwards", "inwards", "sideways", "upwards"], "branch_style": "evil"},
            {"depth": 1},
        ],
    },
    "flower": {
        # Flower: tower with horizontal branches at each layer
        # Uses "flower" branch style: sub-towers at edge, recursive branching continues
        # Note: flower uses outwards+sideways (excludes direction we came from in recursive branches)
        "layers": [
            {"depth": 4, "branch_directions": ["outwards", "sideways", "upwards"], "branch_style": "flower"},
            {"depth": 3, "branch_directions": ["outwards", "sideways", "upwards"], "branch_style": "flower"},
            {"depth": 2, "branch_directions": ["outwards", "sideways", "upwards"], "branch_style": "flower"},
            {"depth": 1},
        ],
    },
    "temple_complex": {
        # Temple Complex: Evil tower with grid expansion
        # Each grid node gets an evil tower, recursively expanding in 4 directions
        # Uses "evil" branch style for the tower at each grid node
        "layers": [
            {"depth": 4, "branch_directions": ["outwards", "inwards", "sideways", "upwards"], "branch_style": "evil"},
            {"depth": 3, "branch_directions": ["outwards", "inwards", "sideways", "upwards"], "branch_style": "evil"},
            {"depth": 2, "branch_directions": ["outwards", "inwards", "sideways", "upwards"], "branch_style": "evil"},
            {"depth": 1},
        ],
        "grid_depth": 4,  # Controls grid recursion depth
        "grid_min_depth": 2,  # Stop grid expansion at this depth
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
        # Uses "evil" branch style - sub-towers at waist, simple towers
        layers = []
        min_depth = max(1, depth - stack_height)
        for d in range(depth, min_depth - 1, -1):
            layer = {"depth": d}
            # All layers except the smallest get branches
            if d > min_depth:
                layer["branch_directions"] = ["outwards", "inwards", "sideways", "upwards"]
                layer["branch_style"] = "evil"
            layers.append(layer)
        return {"layers": layers}

    elif name == "flower":
        # Flower: tower with branches at each layer (except the last)
        # Uses "flower" branch style - sub-towers at edge, recursive branching
        layers = []
        min_depth = max(1, depth - stack_height - 1)
        for d in range(depth, min_depth - 1, -1):
            layer = {"depth": d}
            # All layers except the smallest get branches
            if d > min_depth:
                layer["branch_directions"] = ["outwards", "sideways", "upwards"]
                layer["branch_style"] = "flower"
            layers.append(layer)
        return {"layers": layers}

    elif name == "temple_complex":
        # Temple Complex: Evil tower layers with grid expansion
        # depth controls base layer depth, stack_height controls grid recursion
        grid_depth = max(2, min(5, depth + 1))  # Grid recursion depth
        grid_min_depth = max(1, grid_depth - stack_height - 1)  # Stop expansion at this depth

        # Build evil tower layers scaled to depth
        # Uses "evil" branch style - sub-towers at waist, simple towers
        layers = []
        min_layer_depth = max(1, depth - stack_height)
        for d in range(depth, min_layer_depth - 1, -1):
            layer = {"depth": d}
            # All layers except the smallest get branches
            if d > min_layer_depth:
                layer["branch_directions"] = ["outwards", "inwards", "sideways", "upwards"]
                layer["branch_style"] = "evil"
            layers.append(layer)

        return {
            "layers": layers,
            "grid_depth": grid_depth,
            "grid_min_depth": grid_min_depth,
        }

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

    For city-like structures, grid_depth and grid_min_depth control 2D grid expansion:
    - At each grid node, the layers are built as a tower
    - The grid recursively expands in 4 horizontal directions
    - Each expansion level uses a smaller grid_depth
    """

    # Recipe parameters
    layers: list[dict] = field(default_factory=list)
    center: OctoVector = field(default_factory=OctoVector)

    # Grid expansion for city-like structures
    grid_depth: int | None = None  # Current grid expansion depth (None = no grid)
    grid_min_depth: int = 2  # Stop grid expansion at this depth

    # For branch recursion: the direction we came from (to compute relative directions)
    origin_dir: tuple[int, int] | None = None

    # Legacy parameters (for backwards compatibility)
    max_depth: int = 3
    depth_rules: list[dict] = field(default_factory=list)  # Deprecated

    # Horizontal direction tuples for branching
    ALL_HORIZ_DIRS = {(1, 0), (-1, 0), (0, 1), (0, -1)}

    def __post_init__(self):
        if not self.layers and self.grid_depth is None:
            # No layers specified AND not in grid mode - create default single flake
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

        # If in grid mode but below minimum depth, return empty grid
        # This matches TempleComplexBuilder behavior where i < min_i creates nothing
        if self.grid_depth is not None and self.grid_depth < self.grid_min_depth:
            return combined_grid

        # Handle city-style grid expansion (matches TempleComplexBuilder)
        if self.grid_depth is not None and self.grid_depth >= self.grid_min_depth:
            # Build EvilTowerX-style tower at this grid node
            # Tower layers go from grid_depth down to 1
            # TempleComplexBuilder uses max_subtower_i = grid_depth - 1
            # This means: top layer (grid_depth) has NO branches, all others do
            tower_layers = []
            max_subtower_depth = self.grid_depth - 1
            for d in range(self.grid_depth, 0, -1):
                layer = {"depth": d}
                # Branches on layers where min_subtower_i <= d <= max_subtower_i
                # min_subtower_i defaults to 1, max is grid_depth - 1
                if 1 <= d <= max_subtower_depth:
                    layer["branch_directions"] = ["outwards", "inwards", "sideways", "upwards"]
                    layer["branch_style"] = "evil"  # Grid uses evil-style towers
                tower_layers.append(layer)

            tower_builder = RecipeBuilder(
                layers=tower_layers,
                center=self.center,
                grid_depth=None,  # Don't recurse grid in tower
            )
            tower_grid = tower_builder.materialize_additive()
            combined_grid = OctoGrid.merge(combined_grid, tower_grid)

            # Expand grid in 4 horizontal directions
            # Each sub-grid node will build its own tower based on (grid_depth - 1)
            grid_offset = p2(self.grid_depth + 1)
            for dx, dy in self.ALL_HORIZ_DIRS:
                sub_center = self.center + OctoVector(grid_offset * dx, grid_offset * dy, 0)
                sub_builder = RecipeBuilder(
                    layers=[],  # Empty - tower is derived from grid_depth
                    center=sub_center,
                    grid_depth=self.grid_depth - 1,
                    grid_min_depth=self.grid_min_depth,
                )
                sub_grid = sub_builder.materialize_additive()
                combined_grid = OctoGrid.merge(combined_grid, sub_grid)

            return combined_grid

        # Standard tower/flake building (no grid expansion)
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

            # Handle branches based on branch_style
            if has_branches:
                # Check if upwards is included (controls whether central stack continues)
                include_upwards = "upwards" in layer_branch_dirs
                branch_style = layer.get("branch_style", "evil")  # Default to evil for backwards compat

                # Compute which horizontal directions to branch based on origin
                current_dirs = self._compute_branch_directions(layer_branch_dirs, self.origin_dir)

                i = layer_depth
                if i >= 2:  # Need at least depth 2 for sub-towers
                    if branch_style == "evil":
                        # EvilTowerX geometry: sub-towers at horizontal offset from layer center
                        # Offset = f_rad(i) - f_rad(i-2) = 2^(i+1) - 2^(i-1)
                        # This places sub-towers at the "waist" of the current flake
                        horiz_offset = f_rad(i) - f_rad(i - 2)

                        # Sub-towers start at the same Z as current layer center
                        sub_tower_z = layer_z

                        for dx, dy in current_dirs:
                            # Sub-tower base depth
                            sub_base_depth = i - 1

                            # TowerX adds f_rad(base_i - 1) to the Z position for first flake
                            tower_z_offset = f_rad(sub_base_depth - 1) if sub_base_depth >= 1 else 0

                            branch_center = self.center + OctoVector(
                                horiz_offset * dx,
                                horiz_offset * dy,
                                sub_tower_z + tower_z_offset
                            )

                            sub_origin = (dx, dy)

                            # Evil style: simple tower (no further branching)
                            sub_layers = []
                            for d in range(sub_base_depth, 0, -1):
                                sub_layers.append({"depth": d})

                            if sub_layers:
                                sub_builder = RecipeBuilder(
                                    layers=sub_layers,
                                    center=branch_center,
                                    origin_dir=sub_origin,
                                )
                                sub_grid = sub_builder.materialize_additive()
                                combined_grid = OctoGrid.merge(combined_grid, sub_grid)

                    elif branch_style == "flower":
                        # FlowerTower geometry: sub-towers at edge of layer
                        # horiz_offset = p2(i + 1) = f_rad(i)
                        # z_offset = -p2(t_i + 1) = -f_rad(i-1) where t_i = i-1
                        horiz_offset = p2(i + 1)
                        sub_base_depth = i - 1
                        z_drop = -p2(sub_base_depth + 1)  # = -f_rad(sub_base_depth)

                        # The branch position is relative to where we are AFTER the layer
                        # (c += Z * p2(i+1) happens, then we spawn at c + offset)
                        after_layer_z = layer_z + p2(i + 1)

                        for dx, dy in current_dirs:
                            branch_center = self.center + OctoVector(
                                horiz_offset * dx,
                                horiz_offset * dy,
                                after_layer_z + z_drop
                            )

                            sub_origin = (dx, dy)

                            # Flower style: recursive - remaining layers continue branching
                            # Build from depth (i-1) down, with same branch pattern
                            sub_layers = []
                            for d in range(sub_base_depth, 0, -1):
                                sub_layer = {"depth": d}
                                # Continue the flower pattern (with branches) for all except last
                                if d > 1:
                                    sub_layer["branch_directions"] = layer_branch_dirs.copy()
                                    sub_layer["branch_style"] = "flower"
                                sub_layers.append(sub_layer)

                            if sub_layers:
                                sub_builder = RecipeBuilder(
                                    layers=sub_layers,
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
