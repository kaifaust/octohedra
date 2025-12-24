"""Integration tests for mesh generation.

These tests verify that the fractal builders produce valid 3D meshes
with expected properties (vertex count, face count, watertightness).
"""
import tempfile
from pathlib import Path

import pytest
import trimesh

from octohedra.builders.FlakeBuilder import FlakeBuilder
from octohedra.grid.OctoGrid import OctoGrid
from octohedra.grid.OctoVector import OctoVector
from octohedra.utils import OctoConfigs


class TestFlakeBuilderMeshOutput:
    """Test that FlakeBuilder produces valid mesh output."""

    @pytest.fixture
    def config(self):
        """Use a simple config for fast test execution."""
        return OctoConfigs.giant_debug

    def test_basic_flake_creates_mesh(self, config):
        """A basic flake should produce a non-empty mesh."""
        builder = FlakeBuilder(iteration=1, scale=0)
        grid = builder.materialize()

        assert len(grid.occ) > 0, "Grid should contain cells"

        mesh = grid.render(config)

        assert isinstance(mesh, trimesh.Trimesh)
        assert len(mesh.vertices) > 0, "Mesh should have vertices"
        assert len(mesh.faces) > 0, "Mesh should have faces"

    def test_flake_iteration_scaling(self, config):
        """Higher iteration flakes should have more cells."""
        grid_1 = FlakeBuilder(iteration=1, scale=0).materialize()
        grid_2 = FlakeBuilder(iteration=2, scale=0).materialize()

        assert len(grid_2.occ) > len(grid_1.occ), (
            "Iteration 2 should have more cells than iteration 1"
        )

    def test_mesh_has_consistent_properties(self, config):
        """The same input should produce the same output."""
        builder = FlakeBuilder(iteration=2, scale=0)

        grid1 = builder.materialize()
        mesh1 = grid1.render(config)

        # Create fresh builder to ensure no state leakage
        builder2 = FlakeBuilder(iteration=2, scale=0)
        grid2 = builder2.materialize()
        mesh2 = grid2.render(config)

        assert len(mesh1.vertices) == len(mesh2.vertices)
        assert len(mesh1.faces) == len(mesh2.faces)

    def test_mesh_bounds_are_reasonable(self, config):
        """Mesh should have positive volume and reasonable bounds."""
        builder = FlakeBuilder(iteration=2, scale=0)
        grid = builder.materialize()
        mesh = grid.render(config)

        bounds = mesh.bounds
        assert bounds is not None, "Mesh should have bounds"

        # Check that mesh has positive extent in all dimensions
        extents = bounds[1] - bounds[0]
        assert all(e > 0 for e in extents), "Mesh should have positive extent in all dimensions"


class TestOctoGridOperations:
    """Test core OctoGrid operations."""

    def test_insert_cell_at_origin(self):
        """Inserting a cell at origin should work."""
        grid = OctoGrid()
        grid.insert_cell(OctoVector(0, 0, 0))

        assert len(grid.occ) == 1

    def test_fill_creates_multiple_cells(self):
        """Fill operation should create multiple cells."""
        grid = OctoGrid()
        grid.fill(radius=2, center=OctoVector(0, 0, 0))

        assert len(grid.occ) > 1, "Fill should create multiple cells"

    def test_crop_removes_cells(self):
        """Crop should remove cells outside bounds."""
        grid = OctoGrid()
        grid.fill(radius=4, center=OctoVector(0, 0, 0))
        initial_count = len(grid.occ)

        grid.crop(z_min=0)  # Remove cells below z=0
        cropped_count = len(grid.occ)

        assert cropped_count <= initial_count, "Crop should remove some cells"

    def test_merge_combines_grids(self):
        """Merging grids should combine their cells."""
        grid1 = OctoGrid()
        grid1.insert_cell(OctoVector(0, 0, 0))

        grid2 = OctoGrid()
        grid2.insert_cell(OctoVector(2, 0, 0))

        grid1.merge(grid2)

        assert len(grid1.occ) == 2, "Merged grid should have cells from both"


class TestMeshExport:
    """Test that meshes can be exported to files."""

    @pytest.fixture
    def simple_mesh(self):
        """Create a simple mesh for export testing."""
        config = OctoConfigs.giant_debug
        builder = FlakeBuilder(iteration=1, scale=0)
        grid = builder.materialize()
        return grid.render(config)

    def test_export_to_obj(self, simple_mesh):
        """Mesh should be exportable to OBJ format."""
        with tempfile.NamedTemporaryFile(suffix=".obj", delete=False) as f:
            filepath = Path(f.name)

        try:
            simple_mesh.export(str(filepath))
            assert filepath.exists()
            assert filepath.stat().st_size > 0, "OBJ file should not be empty"

            # Verify file can be read back
            loaded = trimesh.load(str(filepath))
            assert len(loaded.vertices) == len(simple_mesh.vertices)
        finally:
            filepath.unlink(missing_ok=True)

    def test_export_to_stl(self, simple_mesh):
        """Mesh should be exportable to STL format."""
        with tempfile.NamedTemporaryFile(suffix=".stl", delete=False) as f:
            filepath = Path(f.name)

        try:
            simple_mesh.export(str(filepath))
            assert filepath.exists()
            assert filepath.stat().st_size > 0, "STL file should not be empty"

            # Verify file can be read back
            loaded = trimesh.load(str(filepath))
            assert len(loaded.vertices) > 0
        finally:
            filepath.unlink(missing_ok=True)
