from dataclasses import dataclass
from typing import NamedTuple

from bidict import bidict
from euclid3 import Vector3

from printing.builders.OctoBuilder import OctoBuilder
from printing.grid.OctoGrid import OctoGrid
from printing.grid.OctoVector import OctoVector
from printing.utils import OctoConfigs, RenderUtils
from printing.utils.OctoConfig import OctoConfig
from printing.utils.OctoUtil import p2


# UNE = (1, 1, 1)
# UNW = (-1, 1, 1)
# USW = (-1, -1, 1)
# USE = (1, -1, 1)
# DNE = (1, 1, -1)
# DNW = (-1, 1, -1)
# DSW = (-1, -1, -1)
# DSE = (1, -1, -1)
# UNE = (OctoVector(1, 0, 0), OctoVector(0, 1, 0), OctoVector(0, 0, 1))
# UNW = (OctoVector(0, 1, 0), OctoVector(-1, 0, 0), OctoVector(0, 0, 1))
# USW = (OctoVector(-1, 0, 0), OctoVector(0, -1, 0), OctoVector(0, 0, 1))
# USE = (OctoVector(0, -1, 0), OctoVector(1, 0, 0), OctoVector(0, 0, 1))
# DNE = (OctoVector(0, 1, 0), OctoVector(1, 0, 0), OctoVector(0, 0, -1))
# DNW = (OctoVector(-1, 0, 0), OctoVector(0, 1, 0), OctoVector(0, 0, -1))
# DSW = (OctoVector(0, -1, 0), OctoVector(-1, 0, 0), OctoVector(0, 0, -1))
# DSE = (OctoVector(1, 0, 0), OctoVector(0, -1, 0), OctoVector(0, 0, -1))


class Orientation(NamedTuple):
    x: OctoVector
    y: OctoVector
    z: OctoVector


UNE = Orientation(OctoVector(1, 0, 0), OctoVector(0, 1, 0), OctoVector(0, 0, 1))
UNW = Orientation(OctoVector(0, 1, 0), OctoVector(-1, 0, 0), OctoVector(0, 0, 1))
USW = Orientation(OctoVector(-1, 0, 0), OctoVector(0, -1, 0), OctoVector(0, 0, 1))
USE = Orientation(OctoVector(0, -1, 0), OctoVector(1, 0, 0), OctoVector(0, 0, 1))
DNE = Orientation(OctoVector(0, 1, 0), OctoVector(1, 0, 0), OctoVector(0, 0, -1))
DNW = Orientation(OctoVector(-1, 0, 0), OctoVector(0, 1, 0), OctoVector(0, 0, -1))
DSW = Orientation(OctoVector(0, -1, 0), OctoVector(-1, 0, 0), OctoVector(0, 0, -1))
DSE = Orientation(OctoVector(1, 0, 0), OctoVector(0, -1, 0), OctoVector(0, 0, -1))

LEFT_LOOKUP = bidict({
    UNE: UNW,
    UNW: USW,
    USW: USE,
    USE: UNE,
    DNE: DSE,
    DNW: DNE,
    DSW: DNW,
    DSE: DSW
})

FLIP_LOOKUP = bidict({
    UNE: DNE,
    UNW: DNW,
    USW: DSW,
    USE: DSE,
})


def flip_z(self):
    if self in FLIP_LOOKUP:
        return FLIP_LOOKUP[self]
    else:
        return FLIP_LOOKUP.inverse[self]


def turn_right(self):
    return LEFT_LOOKUP.inverse[self]


def turn_left(self):
    return LEFT_LOOKUP[self]


@dataclass
class OctoSectorBuilder(OctoBuilder):
    center: OctoVector = OctoVector()
    iteration: int = 1
    interior_i: int = 0
    surface_i: int = 0
    orientation: Orientation = USE

    # def __post_init__(self):
    #     if

    # def __init__(self, iteration, base_i=0, orientation=UNE, center=None):
    #     super().__init__()
    #     self.orientation = orientation
    #     self.iteration = iteration
    #     self.center = Vector3(0, 0, 0) if center is None else center

    def materialize_additive(self, bonus_iteration=0):
        grid = OctoGrid()
        self.materialize_sector(grid, self.iteration, self.interior_i)
        return grid

    def detailed_core_sector_v2(self, grid, i, center, orientation):
        o = p2(i)

        ox = Vector3(*orientation[0])
        oy = Vector3(*orientation[1])
        oz = Vector3(*orientation[2])

        self.detailed_core_sector(grid, i - 1, center + o * ox, orientation)
        self.detailed_core_sector(grid, i - 1, center + o * oy, orientation)

        self.detailed_core_sector(grid, i - 1, center + o * oz, orientation)
        self.materialize_sector(grid, i - 1, 0, center + o * oz, flip_z(orientation))
        #
        self.materialize_sector(grid, i - 1, 0, center + o * oy, turn_right(orientation))
        self.materialize_sector(grid, i - 1, 0, center + o * ox, turn_left(orientation))

    def detailed_core_sector(self, grid, i, center, orientation):
        o = p2(i)

        ox = Vector3(*orientation[0])
        oy = Vector3(*orientation[1])
        oz = Vector3(*orientation[2])

        self.materialize_sector(grid, i - 1, i - 1, center + o * ox, orientation)
        self.materialize_sector(grid, i - 1, i - 1, center + o * oy, orientation)

        self.materialize_sector(grid, i - 1, i - 1, center + o * oz, orientation)
        self.materialize_sector(grid, i - 1, 0, center + o * oz, flip_z(orientation))
        #
        self.materialize_sector(grid, i - 1, 0, center + o * oy, turn_right(orientation))
        self.materialize_sector(grid, i - 1, 0, center + o * ox, turn_left(orientation))

    def materialize_sector(self, grid, i, base_i, center, orientation):
        if i == base_i:

            self.fill_sector(grid, i, center, orientation)
            return

        o = p2(i)
        ox, oy, oz = orientation

        self.materialize_sector(grid, i - 1, base_i, center + o * ox, orientation)
        self.materialize_sector(grid, i - 1, base_i, center + o * oy, orientation)

        self.materialize_sector(grid, i - 1, base_i, center + o * oz, orientation)
        self.materialize_sector(grid, i - 1, base_i, center + o * oz, flip_z(orientation))
        #
        self.materialize_sector(grid, i - 1, base_i, center + o * oy, turn_right(orientation))
        self.materialize_sector(grid, i - 1, base_i, center + o * ox, turn_left(orientation))

    def fill_sector(self, grid: OctoGrid, iteration, center, orientation):

        ox, oy, oz = orientation

        # iteration += 1

        octo_points = [ox * x + oy * y + oz * z + center
                       for x in range(0, p2(iteration) + 1)
                       for y in range(0, p2(iteration) + 1)
                       for z in range(0, p2(iteration) + 1)
                       if x + y + z < p2(iteration) + 0
                       ]

        for point in octo_points:
            grid.insert_cell(center=point, octo_only=True, strict=False)

        # TODO: Keep trying manual infill
        # tetra_points = [ox * x + oy * y + oz * z + center
        #                 for x in range(0, p2(iteration) + 1)
        #                 for y in range(0, p2(iteration) + 1)
        #                 for z in range(0, p2(iteration) + 1)
        #                 if x + y + z == p2(iteration) - 1
        #                 ]
        #
        # print(tetra_points)
        # for point in tetra_points:
        #     grid.insert_cell(center=point, tetra_only=True)

    @classmethod
    def build_solid_sector(cls, iteration):
        pass


def test_fill_sector():
    grid = OctoGrid()
    builder = OctoSectorBuilder()
    grid1 = builder.materialize_sector(3, 0, OctoVector(), USE)

    # builder.detailed_core_sector(grid, i, Vector3(0, 0, 0), Orientation.UNE)
    # builder.detailed_core_sector(grid, i, Vector3(0, 0, 0), Orientation.UNW)
    # builder.detailed_core_sector(grid, i, Vector3(0, 0, 0), Orientation.USE)
    # builder.detailed_core_sector(grid, i, Vector3(0, 0, 0), Orientation.USW)

    grid.compute_trimming()

    RenderUtils.render_grid(grid,
                            z_min=0,
                            filename="detailed_core.stl",
                            config=OctoConfigs.config_2)




def multi(i, sectors, name, config):
    builder = OctoSectorBuilder()
    grid = OctoGrid()
    for base_i, orientation in sectors:
        sector_grid = OctoGrid()
        builder.materialize_sector(grid, i, base_i, OctoVector(), orientation)
        # builder.materialize_sector(sector_grid, i, base_i, OctoVector(), orientation
        # RenderUtils.render_grid(sector_grid, config, base_filename="sector1", base_i=base_i)
    grid.crop_bottom()
    grid.compute_trimming()
    RenderUtils.render_grid(grid, config, filename=name)


def make_multi_scale():
    config = OctoConfig(
        name="Rainbow Gem",
        nozzle_width=0.2,
        absolute_line_width=0.3,
        absolute_layer_height=0.15,
        line_overlap=1,
        absolute_first_layer_height= .2249, #.1799,
        absolute_floor_height=.01,
        absolute_layers_per_cell=16, # prev was 16
        absolute_slit=.001
    )


    for i, layers in ((3, 6),):
        config.absolute_layers_per_cell = layers
        config.print_settings()
        config.print_derived_values()

        # bs = base_sectors = [(0, UNE), (1, UNW), (2, USW), (3, USE)]
        # bs = base_sectors = [(0, UNE), (2, USW)]
        bs = base_sectors = [(0, UNE)]
        multi(i, base_sectors, f"InOrder_CCW", config)
        # multi(i, [(0, UNE), (3, UNW), (2, USW), (1, USE)], f"InOrder_CW", config)

    exit()
    builder = OctoSectorBuilder()



def test_materialize_sector():
    pass
    grid = OctoGrid()
    builder = OctoSectorBuilder(4, 2)

    builder.materialize_sector(grid, i=1, base_i=1, center=Vector3(0, 0, 0),orientation= UNE)

    RenderUtils.render_grid(grid)


if __name__ == "__main__":
    # make_multi_scale()
    test_materialize_sector()
