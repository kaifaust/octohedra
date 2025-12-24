from dataclasses import dataclass, field
from functools import reduce

from octohedra.grid.OctoGrid import OctoGrid
from octohedra.utils import OctoConfigs, RenderUtils


@dataclass
class OctoBuilder:
    """Represents a generalized flake-like thing that knows how to materialize itself to an
    OctoGrid

    The lifecycle is:

        - init() is called with all your parameters and shit
        - populate() is called in post_init, which is when you set up your children
        - You should be done at this point (exception would be negative stuff, but we ain't dealt
        with that shit yet




    """
    # name: ClassVar[str] = "Base Builder"
    children: list = field(default_factory=list, repr=False, init=False)

    def __post_init__(self):
        self.populate()

    def __iadd__(self, other):
        self.add_child(other)
        return self

    def __str__(self):
        return self.__class__.__name__

        # return str(self.children)

    def add_child(self, child):

        self.children.append(child)
        return self

    @classmethod
    def builder(cls):
        return OctoBuilder()

    def render(self,
               config=OctoConfigs.default,
               filename="Octo",
               base_path=None,
               **filename_details):
        """Generate and save this shape"""
        grid = self.materialize()
        RenderUtils.render_grid(grid, config, filename, base_path, **filename_details)

    def populate(self):
        """
        Actually write down who your kids are. This is the method you should probably override
        """
        pass

    def materialize(self):
        """
        Generate a grid containing this flake alone.

        Call this on the root of your tree of OctoBuilders. You shouldn't need to override this.
        """
        grid = self.materialize_additive()
        self.materialize_subtractive(grid)
        return grid

    def materialize_additive(self, bonus_iteration=0):
        """
        Add to the given grid every cell that this flake could conceivably need.

        Use additional private grids to do an additive/subtractive approach, and merge into the
        given grid.

        The OctoGrid class knows how to generate the basic Octahedron Flake, and fill and clear
        rectangular and
        octahedral regions. Any functionality beyond that should be in an Octohedra subclass.
        """
        self.populate()

        if len(self.children) == 0:
            return OctoGrid()
        sub_grids = [child.materialize_additive() for child in self.children]

        return reduce(OctoGrid.merge, sub_grids)

    def materialize_subtractive(self, grid: OctoGrid, bonus_iteration=0):
        """
        Given a grid containing potentially many flakes,
        remove any cells necessary to maintain the properties of this flake.

        The basic flake doesn't need to remove anything.
        """

        for child in self.children:
            child.materialize_subtractive(grid)

        return grid
