from printing.octo.OctoGrid import OctoGrid


class OctoBuilder:
    """Represents a generalized flake-like thing that knows how to materialize itself to an OctoGrid"""

    def __init__(self):
        self.children = set()

    def materialize(self):
        """
        Generate a grid containing this flake alone.

        Call this on the root of your tree of octobuilders
        """

        grid = OctoGrid()

        self.materialize_additive(grid)
        self.materialize_subtractive(grid)
        return grid


    def materialize_additive(self, grid, bonus_iteration=0):
        """
        Add to the given grid every cell that this flake could conceivably need.

        Use additional private grids to do an additive/subtractive approach, and merge into the given grid.

        The OctoGrid class knows how to generate the basic Octahedron Flake, and fill and clear rectangular and
        octahedral regions. Any functionality beyond that should be in an OctoFlake subclass.
        """



        for child in self.children:
            child.materialize_additive(grid)

        return grid

    def materialize_subtractive(self, grid, bonus_iteration=0):
        """
        Given a grid containing potentially many flakes,
        remove any cells necessary to maintain the properties of this flake.

        The basic flake doesn't need to remove anything.
        """



        for child in self.children:
            child.materialize_subtractive(grid)

        return grid
