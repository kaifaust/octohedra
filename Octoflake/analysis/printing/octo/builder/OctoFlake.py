from printing.octo.OctoGrid import OctoGrid


class OctoFlake:
    """Represents a generalized flake-like thing that knows how to materialize itself to an OctoGrid"""

    def __init__(self, iteration, center):
        self.iteration = iteration
        self.center = center

    def test_materialize(self):
        """
        Generate a grid containing this flake alone.

        Not suitable for combining with other grids containing other flakes.
        """
        grid = self.materialize_additive()
        return self.materialize_subtractive(grid)

    def materialize_additive(self, grid, bonus_iteration=0):
        """
        Add to the given grid every cell that this flake could conceivably need.

        Use additional private grids to do an additive/subtractive approach, and merge into the given grid.

        The OctoGrid class knows how to generate the basic Octahedron Flake, and fill and clear rectangular and
        octahedral regions. Any functionality beyond that should be in an OctoFlake subclass.
        """

        grid.make_flake(self.iteration, x = self.center[0], y = self.center[1], z = self.center[2])

        return OctoGrid()

    def materialize_subtractive(self, grid, bonus_iteration=0):
        """
        Given a grid containing potentially many flakes,
        remove any cells necessary to maintain the properties of this flake.

        The basic flake doesn't need to remove anything.
        """
        return grid
