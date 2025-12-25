"""
RecipeBuilder - A composable fractal builder driven by recipes.

This builder unifies all fractal generation into a single recipe-based system.
Presets (flake, tower, flower) are just pre-defined recipes.

## Recipe Structure

A recipe is a list of **layers**. Each layer corresponds to one "iteration" level
in the OG project - a recursive octahedral structure:

1. **depth** - Size (1-5), controls size and complexity
2. **shape** - How octahedra branch internally:
   - 'fractal': All 6 directions (±x, ±y, ±z) - classic fractal (default)
   - 'solid': Fill solid, no recursion
3. **spawn** - Where to create sub-structures horizontally:
   - 'out': Continue away from parent direction
   - 'in': Back toward parent
   - 'side': Perpendicular to parent
4. **bloom** - Do spawns continue the branching pattern? (recursive like Flower)
5. **echo** - Do spawns contain the full recipe at smaller scale? (like Temple Complex)

## Example Recipes

Simple flake:
{"layers": [{"depth": 3}]}

Tower (stacked layers):
{"layers": [{"depth": 4}, {"depth": 3}, {"depth": 2}, {"depth": 1}]}

Evil Tower (spawns with no bloom):
{"layers": [
    {"depth": 3, "spawn": ["out", "in", "side"]},
    {"depth": 2, "spawn": ["out", "in", "side"]},
    {"depth": 1}
]}

Flower (spawns that bloom):
{"layers": [
    {"depth": 4, "spawn": ["out", "side"], "bloom": true},
    {"depth": 3, "spawn": ["out", "side"], "bloom": true},
    {"depth": 2}
]}

Temple Complex (spawns that echo the full recipe):
{"layers": [
    {"depth": 4, "spawn": ["out", "in", "side"], "echo": true},
    {"depth": 3, "spawn": ["out", "in", "side"]},
    {"depth": 2}
]}
"""

from dataclasses import dataclass, field
from typing import Literal

from octohedra.builders.OctoBuilder import OctoBuilder
from octohedra.grid.OctoGrid import OctoGrid
from octohedra.grid.OctoVector import OctoVector
from octohedra.utils.OctoUtil import DOWN, UP, E, N, S, W, X, Y, Z, p2, f_rad

# Shape types for layers
ShapeType = Literal["fractal", "solid"]

# Spawn directions - where to create sub-structures horizontally
SpawnDirection = Literal["out", "in", "side"]

# Legacy branch styles (for backwards compatibility)
# 'waist': Sub-towers at narrower point, simple tower (no recursion) - EvilTowerX style
# 'edge': Sub-towers at outer extent, recursive branching continues - FlowerTower style
BranchStyle = Literal["waist", "edge"]


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
        # Evil tower: tower with spawns in all directions, no bloom
        # Spawns are simple towers that don't continue branching
        "layers": [
            {"depth": 3, "spawn": ["out", "in", "side"]},
            {"depth": 2, "spawn": ["out", "in", "side"]},
            {"depth": 1},
        ],
    },
    "flower": {
        # Flower: tower with blooming spawns
        # Spawns continue the branching pattern recursively
        "layers": [
            {"depth": 4, "spawn": ["out", "side"], "bloom": True},
            {"depth": 3, "spawn": ["out", "side"], "bloom": True},
            {"depth": 2, "spawn": ["out", "side"], "bloom": True},
            {"depth": 1},
        ],
    },
    "temple_complex": {
        # Temple Complex: tower with echoing spawns
        # Spawns contain the full recipe at smaller scale
        "layers": [
            {"depth": 4, "spawn": ["out", "in", "side"], "echo": True},
            {"depth": 3, "spawn": ["out", "in", "side"]},
            {"depth": 2, "spawn": ["out", "in", "side"]},
            {"depth": 1},
        ],
    },
}


def get_preset_recipe(name: str, depth: int = 3, stack_height: int = 1) -> dict:
    """Get a preset recipe, optionally adjusting parameters.

    Args:
        name: Preset name
        depth: Base depth (size) of the layers
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
        # Evil tower: tower with spawns in all directions, no bloom
        layers = []
        min_depth = max(1, depth - stack_height)
        for d in range(depth, min_depth - 1, -1):
            layer = {"depth": d}
            # All layers except the smallest get spawns
            if d > min_depth:
                layer["spawn"] = ["out", "in", "side"]
            layers.append(layer)
        return {"layers": layers}

    elif name == "flower":
        # Flower: tower with blooming spawns
        layers = []
        min_depth = max(1, depth - stack_height - 1)
        for d in range(depth, min_depth - 1, -1):
            layer = {"depth": d}
            # All layers except the smallest get blooming spawns
            if d > min_depth:
                layer["spawn"] = ["out", "side"]
                layer["bloom"] = True
            layers.append(layer)
        return {"layers": layers}

    elif name == "temple_complex":
        # Temple Complex: tower with echoing spawns on first layer
        # The echo makes spawns contain the full recipe at smaller scale
        layers = []
        min_depth = max(1, depth - stack_height)
        for i, d in enumerate(range(depth, min_depth - 1, -1)):
            layer = {"depth": d}
            # All layers except the smallest get spawns
            if d > min_depth:
                layer["spawn"] = ["out", "in", "side"]
                # Only the first layer echoes (recursive self-replication)
                if i == 0:
                    layer["echo"] = True
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
    how it branches. Layers are stacked vertically.

    New generative model:
    - spawn: Where to create sub-structures (out/in/side)
    - bloom: Do spawns continue branching? (like Flower)
    - echo: Do spawns contain full recipe at smaller scale? (like Temple Complex)
    """

    # Recipe parameters
    layers: list[dict] = field(default_factory=list)
    center: OctoVector = field(default_factory=OctoVector)

    # For spawn recursion: the direction we came from (to compute relative directions)
    origin_dir: tuple[int, int] | None = None

    # Echo recursion depth tracking (internal)
    _echo_depth: int = 0  # How many levels of echo recursion we're in
    _echo_max_depth: int = 4  # Maximum echo recursion depth (prevents infinite recursion)

    # Legacy: Grid expansion (deprecated - use echo instead)
    grid_depth: int | None = None
    grid_min_depth: int = 2

    # Legacy parameters (for backwards compatibility)
    max_depth: int = 3
    depth_rules: list[dict] = field(default_factory=list)

    # Horizontal direction tuples for spawning
    ALL_HORIZ_DIRS = {(1, 0), (-1, 0), (0, 1), (0, -1)}

    def __post_init__(self):
        if not self.layers and self.grid_depth is None:
            # No layers specified AND not in grid mode - create default single flake
            self.layers = [{"depth": self.max_depth}]

    def _compute_spawn_directions(
        self,
        spawn: list[str],
        origin_dir: tuple[int, int] | None,
    ) -> set[tuple[int, int]]:
        """
        Compute spawn directions based on spawn options and origin direction.

        Args:
            spawn: List of spawn directions: 'out', 'in', 'side'
            origin_dir: The direction we came from (e.g., (1, 0) if we spawned from +x)
                       None for the root level (all horizontal directions are valid)

        Returns:
            Set of (dx, dy) tuples representing spawn directions
        """
        result = set()

        # If no origin, we're at the root - use all horizontal directions for 'out'
        if origin_dir is None:
            if "out" in spawn:
                result.update(self.ALL_HORIZ_DIRS)
            return result

        ox, oy = origin_dir

        for d in spawn:
            if d == "out":
                # Continue away from parent (same direction we traveled)
                result.add((ox, oy))
            elif d == "in":
                # Back toward parent (opposite direction)
                result.add((-ox, -oy))
            elif d == "side":
                # Perpendicular to origin direction
                if ox != 0:
                    result.add((0, 1))
                    result.add((0, -1))
                else:
                    result.add((1, 0))
                    result.add((-1, 0))

        return result

    def _compute_branch_directions(
        self,
        directions: list[str],
        origin_dir: tuple[int, int] | None,
    ) -> set[tuple[int, int]]:
        """
        [LEGACY] Compute branch directions based on semantic options and origin direction.
        Use _compute_spawn_directions instead for new code.
        """
        result = set()

        if origin_dir is None:
            if "outwards" in directions:
                result.update(self.ALL_HORIZ_DIRS)
            return result

        ox, oy = origin_dir

        for d in directions:
            if d == "outwards":
                result.add((ox, oy))
            elif d == "inwards":
                result.add((-ox, -oy))
            elif d == "sideways":
                if ox != 0:
                    result.add((0, 1))
                    result.add((0, -1))
                else:
                    result.add((1, 0))
                    result.add((-1, 0))

        return result

    def materialize_additive(self, bonus_iteration=0):
        """Build the complete structure from layers.

        Handles the new spawn/bloom/echo model:
        - spawn: Where to create sub-structures (out/in/side)
        - bloom: Do spawns continue branching? (like Flower)
        - echo: Do spawns contain full recipe at smaller scale? (like Temple Complex)
        """
        combined_grid = OctoGrid()

        # Legacy: Handle grid_depth for backwards compatibility
        # New code should use 'echo' in layers instead
        if self.grid_depth is not None and self.grid_depth < self.grid_min_depth:
            return combined_grid

        if self.grid_depth is not None and self.grid_depth >= self.grid_min_depth:
            # Build tower at this grid node using legacy logic
            tower_layers = []
            max_subtower_depth = self.grid_depth - 1
            for d in range(self.grid_depth, 0, -1):
                layer = {"depth": d}
                if 1 <= d <= max_subtower_depth:
                    layer["spawn"] = ["out", "in", "side"]  # Use new spawn syntax
                tower_layers.append(layer)

            tower_builder = RecipeBuilder(
                layers=tower_layers,
                center=self.center,
                grid_depth=None,
            )
            tower_grid = tower_builder.materialize_additive()
            combined_grid = OctoGrid.merge(combined_grid, tower_grid)

            # Expand grid in 4 horizontal directions
            grid_offset = p2(self.grid_depth + 1)
            for dx, dy in self.ALL_HORIZ_DIRS:
                sub_center = self.center + OctoVector(grid_offset * dx, grid_offset * dy, 0)
                sub_builder = RecipeBuilder(
                    layers=[],
                    center=sub_center,
                    grid_depth=self.grid_depth - 1,
                    grid_min_depth=self.grid_min_depth,
                )
                sub_grid = sub_builder.materialize_additive()
                combined_grid = OctoGrid.merge(combined_grid, sub_grid)

            return combined_grid

        # Standard layer building with spawn/bloom/echo
        current_z = 0
        prev_layer = None

        for layer_idx, layer in enumerate(self.layers):
            layer_depth = layer.get("depth", 3)
            layer_shape = layer.get("shape", "fractal")

            # New spawn model
            layer_spawn = layer.get("spawn")
            layer_bloom = layer.get("bloom", False)
            layer_echo = layer.get("echo", False)
            has_spawns = bool(layer_spawn)

            # Legacy: branch_directions for backwards compatibility
            layer_branch_dirs = layer.get("branch_directions")
            has_legacy_branches = bool(layer_branch_dirs)

            # Calculate z position based on previous layer
            if prev_layer is not None:
                attach_at = prev_layer.get("attach_next_at")
                prev_depth = prev_layer.get("depth", 3)
                if attach_at is not None:
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
            combined_grid = OctoGrid.merge(combined_grid, layer_grid)

            # Handle spawns (new model)
            if has_spawns:
                i = layer_depth
                if i >= 2:  # Need at least depth 2 for sub-structures
                    spawn_dirs = self._compute_spawn_directions(layer_spawn, self.origin_dir)

                    if layer_echo:
                        # Echo: spawns contain the full recipe at smaller scale
                        # This creates Temple Complex-like recursive self-similarity
                        if self._echo_depth < self._echo_max_depth:
                            # Use edge-style positioning for echo (at outer extent)
                            horiz_offset = p2(i + 1)

                            for dx, dy in spawn_dirs:
                                spawn_center = self.center + OctoVector(
                                    horiz_offset * dx,
                                    horiz_offset * dy,
                                    0  # Echo starts at ground level
                                )

                                # Scale down the recipe for the echo
                                # Each layer depth is reduced by 1
                                echo_layers = []
                                for orig_layer in self.layers:
                                    new_depth = orig_layer.get("depth", 3) - 1
                                    if new_depth >= 1:
                                        echo_layer = {"depth": new_depth}
                                        if orig_layer.get("spawn"):
                                            echo_layer["spawn"] = orig_layer["spawn"].copy()
                                        if orig_layer.get("bloom"):
                                            echo_layer["bloom"] = True
                                        if orig_layer.get("echo"):
                                            echo_layer["echo"] = True
                                        if orig_layer.get("shape"):
                                            echo_layer["shape"] = orig_layer["shape"]
                                        echo_layers.append(echo_layer)

                                if echo_layers:
                                    echo_builder = RecipeBuilder(
                                        layers=echo_layers,
                                        center=spawn_center,
                                        origin_dir=(dx, dy),
                                        _echo_depth=self._echo_depth + 1,
                                        _echo_max_depth=self._echo_max_depth,
                                    )
                                    echo_grid = echo_builder.materialize_additive()
                                    combined_grid = OctoGrid.merge(combined_grid, echo_grid)

                    elif layer_bloom:
                        # Bloom: spawns continue the branching pattern (like Flower)
                        horiz_offset = p2(i + 1)
                        sub_base_depth = i - 1
                        z_drop = -p2(sub_base_depth + 1)
                        after_layer_z = layer_z + p2(i + 1)

                        for dx, dy in spawn_dirs:
                            spawn_center = self.center + OctoVector(
                                horiz_offset * dx,
                                horiz_offset * dy,
                                after_layer_z + z_drop
                            )

                            # Build from depth (i-1) down, continuing the bloom pattern
                            sub_layers = []
                            for d in range(sub_base_depth, 0, -1):
                                sub_layer = {"depth": d}
                                if d > 1:
                                    sub_layer["spawn"] = layer_spawn.copy()
                                    sub_layer["bloom"] = True
                                sub_layers.append(sub_layer)

                            if sub_layers:
                                sub_builder = RecipeBuilder(
                                    layers=sub_layers,
                                    center=spawn_center,
                                    origin_dir=(dx, dy),
                                )
                                sub_grid = sub_builder.materialize_additive()
                                combined_grid = OctoGrid.merge(combined_grid, sub_grid)

                    else:
                        # No bloom, no echo: simple tower spawns (like Evil Tower)
                        horiz_offset = f_rad(i) - f_rad(i - 2)
                        sub_tower_z = layer_z

                        for dx, dy in spawn_dirs:
                            sub_base_depth = i - 1
                            tower_z_offset = f_rad(sub_base_depth - 1) if sub_base_depth >= 1 else 0

                            spawn_center = self.center + OctoVector(
                                horiz_offset * dx,
                                horiz_offset * dy,
                                sub_tower_z + tower_z_offset
                            )

                            # Simple tower: no further branching
                            sub_layers = []
                            for d in range(sub_base_depth, 0, -1):
                                sub_layers.append({"depth": d})

                            if sub_layers:
                                sub_builder = RecipeBuilder(
                                    layers=sub_layers,
                                    center=spawn_center,
                                    origin_dir=(dx, dy),
                                )
                                sub_grid = sub_builder.materialize_additive()
                                combined_grid = OctoGrid.merge(combined_grid, sub_grid)

            # Legacy: Handle branch_directions for backwards compatibility
            elif has_legacy_branches:
                include_upwards = "upwards" in layer_branch_dirs
                branch_style = layer.get("branch_style", "waist")
                current_dirs = self._compute_branch_directions(layer_branch_dirs, self.origin_dir)

                i = layer_depth
                if i >= 2:
                    if branch_style == "waist":
                        horiz_offset = f_rad(i) - f_rad(i - 2)
                        sub_tower_z = layer_z

                        for dx, dy in current_dirs:
                            sub_base_depth = i - 1
                            tower_z_offset = f_rad(sub_base_depth - 1) if sub_base_depth >= 1 else 0

                            branch_center = self.center + OctoVector(
                                horiz_offset * dx,
                                horiz_offset * dy,
                                sub_tower_z + tower_z_offset
                            )

                            sub_layers = []
                            for d in range(sub_base_depth, 0, -1):
                                sub_layers.append({"depth": d})

                            if sub_layers:
                                sub_builder = RecipeBuilder(
                                    layers=sub_layers,
                                    center=branch_center,
                                    origin_dir=(dx, dy),
                                )
                                sub_grid = sub_builder.materialize_additive()
                                combined_grid = OctoGrid.merge(combined_grid, sub_grid)

                    elif branch_style == "edge":
                        horiz_offset = p2(i + 1)
                        sub_base_depth = i - 1
                        z_drop = -p2(sub_base_depth + 1)
                        after_layer_z = layer_z + p2(i + 1)

                        for dx, dy in current_dirs:
                            branch_center = self.center + OctoVector(
                                horiz_offset * dx,
                                horiz_offset * dy,
                                after_layer_z + z_drop
                            )

                            sub_layers = []
                            for d in range(sub_base_depth, 0, -1):
                                sub_layer = {"depth": d}
                                if d > 1:
                                    sub_layer["branch_directions"] = layer_branch_dirs.copy()
                                    sub_layer["branch_style"] = "edge"
                                sub_layers.append(sub_layer)

                            if sub_layers:
                                sub_builder = RecipeBuilder(
                                    layers=sub_layers,
                                    center=branch_center,
                                    origin_dir=(dx, dy),
                                )
                                sub_grid = sub_builder.materialize_additive()
                                combined_grid = OctoGrid.merge(combined_grid, sub_grid)

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
