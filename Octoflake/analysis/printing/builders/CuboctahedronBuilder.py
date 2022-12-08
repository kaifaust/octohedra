from dataclasses import dataclass

from printing.builders.FlakeBuilder import FlakeBuilder
from printing.builders.OctoBuilder import OctoBuilder
from printing.grid.OctoGrid import OctoGrid
from printing.grid.OctoVector import OctoVector
from printing.utils import OctoConfigs
from printing.utils.OctoUtil import X, Y, Z, p2


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
