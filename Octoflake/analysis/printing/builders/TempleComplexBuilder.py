from dataclasses import dataclass

from printing.builders.FlakeBuilder import FlakeBuilder
from printing.builders.OctoBuilder import OctoBuilder
from printing.builders.TowerBuilders import Tower, EvilTowerX
from printing.grid.OctoVector import OctoVector
from printing.utils import OctoConfigs
from printing.utils.OctoConfig import OctoConfig
from printing.utils.OctoUtil import X, Y, p2, f_rad, Z


@dataclass
class TempleComplexBuilder(OctoBuilder, ):

    i: int = 4
    min_i: int = 2
    center: OctoVector = OctoVector()

    def __post_init__(self):

        if self.i >= self.min_i:
            # self.add_child(Tower(self.i, self.center))
            # self.add_child(EvilTowerX(self.i, self.center + Z * (f_rad(self.i-1) ), max_subtower_i=self.i-1))
            self.add_child(EvilTowerX(self.i, self.center, max_subtower_i=self.i-1))
            # self.add_child(FlakeBuilder(self.i, self.center))
            # self.add_child(EvilTowerX(self.i, self.center))

            o = p2(self.i + 1)

            # return None

            self.add_child(TempleComplexBuilder(self.i - 1, self.min_i, self.center + X * o))
            self.add_child(TempleComplexBuilder(self.i - 1, self.min_i, self.center - X * o))
            self.add_child(TempleComplexBuilder(self.i - 1, self.min_i, self.center + Y * o))
            self.add_child(TempleComplexBuilder(self.i - 1, self.min_i, self.center - Y * o))


def build_basic_temple_complex():

    # config = OctoConfig(
    #     name="Rainbow Mk3 0.2",
    #     nozzle_width=0.2,
    #     absolute_line_width=0.36,
    #     absolute_layer_height=0.12,
    #     line_overlap=1,
    #     absolute_first_layer_height=.199,
    #     absolute_floor_height=.01,
    #     # absolute_layers_per_cell=9,
    #     target_cell_width=2.5,
    #     absolute_slit=.01
    # )
    config = OctoConfig(
        name="Rainbow Mini 0.2",
        nozzle_width=0.2,
        absolute_line_width=0.4, # (0.2 + .12) / 1.5
        absolute_layer_height=0.15,
        line_overlap=1,
        absolute_first_layer_height=.199,
        absolute_floor_height=.01,
        # absolute_layers_per_cell=4,
        target_cell_width=4,
        absolute_slit=.01
    )

    # config = OctoConfigs.config_20_rainbow_speed
    # config.absolute_layers_per_cell = 12
    config.print_derived_values()

    builder = TempleComplexBuilder(3, 1)

    builder.render(config)

    print(builder.i)

    # builder.render(config, filename="complex")

    pass


if __name__ == "__main__":
    build_basic_temple_complex()
