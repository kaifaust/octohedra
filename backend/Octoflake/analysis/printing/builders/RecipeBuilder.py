"""
RecipeBuilder - A composable fractal builder driven by recipes.

This builder unifies all fractal generation into a single recipe-based system.
Presets (flake, star, tower, flower) are just pre-defined recipes.

## Recipe Structure

A recipe has three main components:

1. **layers** - Stack of flakes positioned vertically (like Tower/Star)
   Each layer has: depth, fill_depth, z_offset (optional)

2. **depth_rules** - Per-depth branching behavior modifications
   Each rule has: depth, type (flake/solid/horizontal/vertical/skip)

3. **branches** - Spawn sub-structures at each layer (like FlowerTower)
   Each layer can have branches that spawn in horizontal directions

## Example Recipes

Simple flake (depth 3):
{
    "layers": [{"depth": 3, "fill_depth": 0}]
}

Tower (depth 4, stacking down to 1):
{
    "layers": [
        {"depth": 4, "fill_depth": 0},
        {"depth": 3, "fill_depth": 0},
        {"depth": 2, "fill_depth": 0},
        {"depth": 1, "fill_depth": 0}
    ]
}

Star (main flake + smaller flakes on top):
{
    "layers": [
        {"depth": 4, "fill_depth": 0},
        {"depth": 3, "fill_depth": 0},
        {"depth": 2, "fill_depth": 0}
    ]
}

Flower (tower with horizontal branches):
{
    "layers": [
        {"depth": 4, "fill_depth": 0, "branches": true},
        {"depth": 3, "fill_depth": 0, "branches": true},
        {"depth": 2, "fill_depth": 0, "branches": true},
        {"depth": 1, "fill_depth": 0}
    ]
}
"""

from dataclasses import dataclass, field
from typing import List, Dict, Literal, Optional, Set, Tuple

from printing.builders.OctoBuilder import OctoBuilder
from printing.grid.OctoGrid import OctoGrid
from printing.grid.OctoVector import OctoVector
from printing.utils.OctoUtil import DOWN, E, N, S, UP, W, X, Y, Z, p2


# Types of nodes that can be placed at each depth
NodeType = Literal["flake", "solid", "horizontal", "vertical", "skip"]


# Pre-defined recipes for common shapes
# These match the original Star/Tower/Flower builders
PRESET_RECIPES = {
    "flake": {
        "layers": [{"depth": 3, "fill_depth": 0}],
        "depth_rules": [],
    },
    "tower": {
        # Tower: decreasing flakes stacked vertically (matching Tower builder)
        # With base_i=3, min_iteration=1: flakes at 3, 2, 1
        "layers": [
            {"depth": 3, "fill_depth": 0},
            {"depth": 2, "fill_depth": 0},
            {"depth": 1, "fill_depth": 0},
        ],
        "depth_rules": [],
    },
    "evil_tower": {
        # Evil tower: tower with sub-towers branching in 4 directions at each level
        # Unlike flower, includes inwards so sub-branches can also branch back toward center
        "layers": [
            {"depth": 3, "fill_depth": 0, "branches": True, "branch_directions": ["outwards", "inwards", "sideways", "upwards"]},
            {"depth": 2, "fill_depth": 0, "branches": True, "branch_directions": ["outwards", "inwards", "sideways", "upwards"]},
            {"depth": 1, "fill_depth": 0},
        ],
        "depth_rules": [],
    },
    "flower": {
        # Flower: tower with horizontal branches at each layer (matching FlowerTower)
        # Outwards + sideways + upwards, but NOT inwards (prevents back-branching toward center)
        "layers": [
            {"depth": 4, "fill_depth": 0, "branches": True, "branch_directions": ["outwards", "sideways", "upwards"]},
            {"depth": 3, "fill_depth": 0, "branches": True, "branch_directions": ["outwards", "sideways", "upwards"]},
            {"depth": 2, "fill_depth": 0, "branches": True, "branch_directions": ["outwards", "sideways", "upwards"]},
            {"depth": 1, "fill_depth": 0},
        ],
        "depth_rules": [],
    },
}


def get_preset_recipe(name: str, depth: int = 3, fill_depth: int = 0, stack_height: int = 1) -> Dict:
    """Get a preset recipe, optionally adjusting parameters.

    Args:
        name: Preset name
        depth: Base depth (complexity) of the shape
        fill_depth: How much to fill solid (0 = fractal)
        stack_height: Number of additional layers for tower-like shapes
    """
    if name not in PRESET_RECIPES:
        name = "flake"

    if name == "flake":
        return {
            "layers": [{"depth": depth, "fill_depth": fill_depth}],
            "depth_rules": [],
        }

    elif name == "tower":
        # Tower: flakes from depth down to (depth - stack_height)
        # Matches Tower(base_i=depth, min_iteration=depth-stack_height)
        layers = []
        min_depth = max(1, depth - stack_height)
        for d in range(depth, min_depth - 1, -1):
            layers.append({"depth": d, "fill_depth": fill_depth})
        return {"layers": layers, "depth_rules": []}

    elif name == "evil_tower":
        # Evil tower: tower with sub-towers branching in 4 directions at each level
        # Matches EvilTower(base_i=depth, min_i=1)
        # Includes inwards so sub-branches can also branch back toward center
        layers = []
        min_depth = max(1, depth - stack_height)
        for d in range(depth, min_depth - 1, -1):
            has_branches = d > min_depth
            layer = {
                "depth": d,
                "fill_depth": fill_depth,
                "branches": has_branches,
            }
            if has_branches:
                layer["branch_directions"] = ["outwards", "inwards", "sideways", "upwards"]
            layers.append(layer)
        return {"layers": layers, "depth_rules": []}

    elif name == "flower":
        # Flower: tower with branches at each layer (except the last)
        # Matches FlowerTower(base_i=depth, min_i=1)
        # Outwards + sideways + upwards, but NOT inwards (prevents back-branching)
        layers = []
        min_depth = max(1, depth - stack_height - 1)
        for d in range(depth, min_depth - 1, -1):
            # All layers except the smallest get branches
            has_branches = d > min_depth
            layer = {
                "depth": d,
                "fill_depth": fill_depth,
                "branches": has_branches,
            }
            if has_branches:
                layer["branch_directions"] = ["outwards", "sideways", "upwards"]
            layers.append(layer)
        return {"layers": layers, "depth_rules": []}

    # Fallback
    return {
        "layers": [{"depth": depth, "fill_depth": fill_depth}],
        "depth_rules": [],
    }


@dataclass
class RecipeBuilder(OctoBuilder):
    """
    A builder that constructs fractals from recipes.

    Recipes can define:
    - layers: Stack of flakes at different depths/positions
    - depth_rules: Modify branching behavior at specific depths
    - branches: Layers can spawn sub-structures horizontally (like FlowerTower)

    This unified approach replaces the separate Star/Tower/Flower builders
    while allowing the same (and more) flexibility.
    """

    # Recipe parameters
    layers: List[Dict] = field(default_factory=list)
    depth_rules: List[Dict] = field(default_factory=list)
    center: OctoVector = field(default_factory=OctoVector)

    # For branch recursion: the direction we came from (to compute relative directions)
    origin_dir: Optional[Tuple[int, int]] = None

    # Legacy parameters (for backwards compatibility)
    max_depth: int = 3
    recipe: Optional[List[Dict]] = None  # Old format: list of depth rules

    # Direction sets for different branching patterns
    HORIZONTAL = [E, N, W, S]
    VERTICAL = [UP, DOWN]
    ALL_DIRS = [E, N, W, S, UP, DOWN]

    # Horizontal direction tuples for branching
    ALL_HORIZ_DIRS = {(1, 0), (-1, 0), (0, 1), (0, -1)}

    def __post_init__(self):
        # Convert legacy recipe format to new format
        if self.recipe is not None and not self.layers:
            # Old format: recipe is just depth_rules
            self.depth_rules = self.recipe
            self.layers = [{"depth": self.max_depth, "fill_depth": 0}]
        elif not self.layers:
            # No layers specified, create default single flake
            self.layers = [{"depth": self.max_depth, "fill_depth": 0}]

        # Build lookup for depth rules
        self._depth_rule_map = {r.get("depth"): r for r in self.depth_rules}

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

    def _get_rule_for_depth(self, depth: int, layer_rules: Optional[List[Dict]] = None) -> Dict:
        """Get the depth rule for a given depth, checking layer-specific rules first."""
        # Check layer-specific rules first
        if layer_rules:
            for rule in layer_rules:
                if rule.get("depth") == depth:
                    return rule
        # Fall back to global rules
        return self._depth_rule_map.get(depth, {"depth": depth, "type": "flake"})

    def _get_directions_for_type(self, node_type: str) -> list:
        """Get the branching directions for a node type."""
        if node_type == "horizontal":
            return [E, N, W, S]
        elif node_type == "vertical":
            return [UP, DOWN]
        else:  # flake is the default
            return [E, N, W, S, UP, DOWN]

    def materialize_additive(self, bonus_iteration=0):
        """Build the complete structure from layers."""
        combined_grid = OctoGrid()
        current_z = 0
        prev_layer = None  # Track previous layer for attach_next_at

        for layer_idx, layer in enumerate(self.layers):
            layer_depth = layer.get("depth", 3)
            layer_fill = layer.get("fill_depth", 0)
            has_branches = layer.get("branches", False)
            layer_rules = layer.get("depth_rules")  # Per-layer depth rules

            # Calculate z position based on previous layer's attach_next_at
            if prev_layer is not None:
                attach_at = prev_layer.get("attach_next_at")
                prev_depth = prev_layer.get("depth", 3)
                if attach_at is not None:
                    # Attach at a specific depth level of the previous layer
                    # The position of depth A in the previous layer is p2(A + 1) from prev layer's center
                    # prev layer center was at (current_z - p2(prev_depth + 1))
                    prev_layer_center_z = current_z - p2(prev_depth + 1)
                    layer_z = prev_layer_center_z + p2(attach_at + 1)
                else:
                    layer_z = current_z
            else:
                layer_z = current_z

            layer_center = self.center + Z * layer_z

            # Build this layer's flake with depth rules applied
            layer_grid = OctoGrid()
            self._build_flake_recursive(layer_grid, layer_depth, layer_fill, layer_center, layer_rules)

            # Merge into combined grid
            combined_grid = OctoGrid.merge(combined_grid, layer_grid)

            # Handle branches
            if has_branches:
                # Get remaining layers for sub-structures
                remaining_layers = self.layers[layer_idx + 1:]
                if remaining_layers:
                    # Get branch directions (semantic: outwards, inwards, sideways, upwards)
                    layer_branch_dirs = layer.get("branch_directions")

                    # Default directions if not specified
                    if layer_branch_dirs is None:
                        layer_branch_dirs = ["outwards", "sideways", "upwards"]

                    # Check if upwards is included (controls whether central stack continues)
                    include_upwards = "upwards" in layer_branch_dirs

                    # Compute which horizontal directions to branch based on origin
                    current_dirs = self._compute_branch_directions(layer_branch_dirs, self.origin_dir)

                    # Spawn sub-structures in computed horizontal directions
                    branch_offset = p2(layer_depth + 1)
                    branch_z_offset = current_z + p2(layer_depth + 1) - p2(layer_depth)

                    for dx, dy in current_dirs:
                        # Calculate branch position
                        branch_center = self.center + OctoVector(
                            branch_offset * dx,
                            branch_offset * dy,
                            branch_z_offset
                        )

                        # The sub-builder's origin is the direction we're branching
                        # (from the sub-builder's perspective, this is where it came from)
                        sub_origin = (dx, dy)

                        # Build sub-structure with remaining layers
                        sub_builder = RecipeBuilder(
                            layers=remaining_layers,
                            depth_rules=self.depth_rules,
                            center=branch_center,
                            origin_dir=sub_origin,
                        )
                        sub_grid = sub_builder.materialize_additive()
                        combined_grid = OctoGrid.merge(combined_grid, sub_grid)

                    # If upwards is excluded, skip remaining layers at center
                    if not include_upwards:
                        break

            # Move up for next layer (from where this layer was placed)
            current_z = layer_z + p2(layer_depth + 1)
            prev_layer = layer

        return combined_grid

    def _build_flake_recursive(self, grid: OctoGrid, depth: int, fill_depth: int, center: OctoVector, layer_rules: Optional[List[Dict]] = None):
        """Recursively build a flake, applying depth rules."""
        if depth <= 0:
            grid.insert_cell(center)
            return

        # Check for fill_depth (like FlakeBuilder's scale parameter)
        if depth <= fill_depth:
            radius = p2(depth + 1)
            grid.fill(radius, center)
            return

        # Check depth rules for special behavior (layer-specific rules take priority)
        rule = self._get_rule_for_depth(depth, layer_rules)
        node_type = rule.get("type", "flake")

        # Handle solid fill - fills the entire region at this depth
        if node_type == "solid":
            radius = p2(depth + 1)
            grid.fill(radius, center)
            return

        # Handle skip - continue recursing without placing at this depth
        if node_type == "skip":
            for direction in self.ALL_DIRS:
                next_center = center + p2(depth - 1) * 2 * direction
                self._build_flake_recursive(grid, depth - 1, fill_depth, next_center, layer_rules)
            return

        # Get directions based on node type (horizontal, vertical, or all)
        directions = self._get_directions_for_type(node_type)

        # Recurse into each direction
        for direction in directions:
            next_center = center + p2(depth - 1) * 2 * direction
            self._build_flake_recursive(grid, depth - 1, fill_depth, next_center, layer_rules)


def generate_from_recipe(
    recipe: Dict,
    config=None,
) -> OctoGrid:
    """
    Generate a fractal grid from a recipe dictionary.

    Args:
        recipe: Recipe dictionary with layers and depth_rules
        config: Optional render config

    Returns:
        OctoGrid containing the generated fractal
    """
    builder = RecipeBuilder(
        layers=recipe.get("layers", []),
        depth_rules=recipe.get("depth_rules", []),
    )
    return builder.materialize()


def test_recipe():
    """Test the RecipeBuilder with various configurations."""
    from printing.utils import OctoConfigs

    # Test 1: Simple flake (default)
    print("Testing simple flake...")
    builder = RecipeBuilder(
        layers=[{"depth": 3, "fill_depth": 0}],
    )
    builder.render(config=OctoConfigs.config_20_rainbow_speed, filename="Recipe_flake")

    # Test 2: Tower-like (multiple stacked layers)
    print("Testing tower...")
    recipe = get_preset_recipe("tower", depth=4, stack_height=3)
    builder = RecipeBuilder(
        layers=recipe["layers"],
        depth_rules=recipe["depth_rules"],
    )
    builder.render(config=OctoConfigs.config_20_rainbow_speed, filename="Recipe_tower")

    # Test 3: Star-like (main flake + smaller on top)
    print("Testing star...")
    recipe = get_preset_recipe("star", depth=4, stack_height=2)
    builder = RecipeBuilder(
        layers=recipe["layers"],
        depth_rules=recipe["depth_rules"],
    )
    builder.render(config=OctoConfigs.config_20_rainbow_speed, filename="Recipe_star")

    # Test 4: Flower (tower with branches)
    print("Testing flower...")
    recipe = get_preset_recipe("flower", depth=4, stack_height=2)
    builder = RecipeBuilder(
        layers=recipe["layers"],
        depth_rules=recipe["depth_rules"],
    )
    builder.render(config=OctoConfigs.config_20_rainbow_speed, filename="Recipe_flower")

    # Test 5: With solid core
    print("Testing with solid core...")
    builder = RecipeBuilder(
        layers=[{"depth": 3, "fill_depth": 0}],
        depth_rules=[{"depth": 1, "type": "solid"}],
    )
    builder.render(config=OctoConfigs.config_20_rainbow_speed, filename="Recipe_solid_core")

    print("All tests complete!")


if __name__ == "__main__":
    test_recipe()
