from dataclasses import dataclass

from octohedra.builders.FlakeBuilder import FlakeBuilder
from octohedra.builders.OctoBuilder import OctoBuilder
from octohedra.grid.OctoGrid import OctoGrid
from octohedra.grid.OctoVector import OctoVector
from octohedra.utils import OctoConfigs
from octohedra.utils.OctoUtil import X, Y, Z, p2


@dataclass
class CuboctahedronBuilder(OctoBuilder):
    iteration: int = 0
    center: OctoVector = OctoVector()

    def materialize_additive(self, bonus_iteration=0):
        i = self.iteration
        d = p2(i, 1)
        grid = OctoGrid()
        grid += FlakeBuilder(i).materialize_additive()
        grid += FlakeBuilder(i, center=Z * 2 * d).materialize_additive()
        grid += FlakeBuilder(i, center=X * d + Z * d).materialize_additive()
        grid += FlakeBuilder(i, center=-X * d + Z * d).materialize_additive()
        grid += FlakeBuilder(i, center=Y * d + Z * d).materialize_additive()
        grid += FlakeBuilder(i, center=-Y * d + Z * d).materialize_additive()
        grid = grid.crop(-d, d, -d, d, 0, 2 * d)

        return grid


def test():
    builder = CuboctahedronBuilder(iteration=3)
    builder.render(config=OctoConfigs.default, filename="Cuboctahedron")


if __name__ == "__main__":
    test()
