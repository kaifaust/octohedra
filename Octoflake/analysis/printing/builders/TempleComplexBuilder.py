from dataclasses import dataclass

from printing.builders.OctoBuilder import OctoBuilder
from printing.builders.TowerBuilders import Tower
from printing.grid.OctoVector import OctoVector
from printing.utils import OctoConfigs
from printing.utils.OctoUtil import X, Y, p2


@dataclass
class TempleComplexBuilder(OctoBuilder, ):

    i: int = 4
    min_i: int = 2
    center: OctoVector = OctoVector()

    def __post_init__(self):

        if self.i >= self.min_i:
            self.add_child(Tower(self.i, self.center))

            o = p2(self.i + 1)

            self.add_child(TempleComplexBuilder(self.i - 1, self.min_i, self.center + X * o))
            self.add_child(TempleComplexBuilder(self.i - 1, self.min_i, self.center - X * o))
            self.add_child(TempleComplexBuilder(self.i - 1, self.min_i, self.center + Y * o))
            self.add_child(TempleComplexBuilder(self.i - 1, self.min_i, self.center - Y * o))


def build_basic_temple_complex():
    config = OctoConfigs.config_20_rainbow_speed
    config.absolute_layers_per_cell = 12
    config.print_derived_values()

    builder = TempleComplexBuilder(5, 1)

    builder.render(config)

    print(builder.i)

    # builder.render(config, filename="complex")

    pass


if __name__ == "__main__":
    build_basic_temple_complex()
