from enum import Enum, auto
from bidict import bidict
from euclid3 import Vector3

from printing.builders.OctoBuilder import OctoBuilder
from printing.grid.OctoGrid import OctoGrid
from printing.utils import RenderUtils
from printing.utils.OctoUtil import Z, p2

# UNE = (1, 1, 1)
# UNW = (-1, 1, 1)
# USW = (-1, -1, 1)
# USE = (1, -1, 1)
# DNE = (1, 1, -1)
# DNW = (-1, 1, -1)
# DSW = (-1, -1, -1)
# DSE = (1, -1, -1)
UNE = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
UNW = ((0, 1, 0), (-1, 0, 0), (0, 0, 1))
USW = ((-1, 0, 0), (0, -1, 0), (0, 0, 1))
USE = ((0, -1, 0), (1, 0 , 0), (0, 0, 1))
DNE = ((0, 1, 0), (1, 0, 0), (0, 0, -1))
DNW = ((-1, 0, 0), (0, 1, 0), (0, 0, -1))
DSW = ((0, -1, 0), (-1, 0, 0), (0, 0, -1))
DSE = ((1, 0, 0), (0, -1, 0), (0, 0, -1))

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

def flip_z(v):


    return FLIP_LOOKUP[v] if v in FLIP_LOOKUP else FLIP_LOOKUP.inverse[v]


def turn_right(v):
    return LEFT_LOOKUP.inverse[v]


def turn_left(v: Vector3):
    return LEFT_LOOKUP[v]


class OctoSectorBuilder(OctoBuilder):

    def __init__(self, iteration, base_i=0, orientation=UNE, center=None):
        super().__init__()
        self.orientation = orientation
        self.iteration = iteration
        self.center = Vector3(0, 0, 0) if center is None else center

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

        self.materialize_sector(grid, i - 1, i-1, center + o * ox, orientation)
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
        ov = orientation

        ox = Vector3(*orientation[0])
        oy = Vector3(*orientation[1])
        oz = Vector3(*orientation[2])


        self.materialize_sector(grid, i - 1, base_i, center +  o* ox, orientation)
        self.materialize_sector(grid, i - 1, base_i, center + o * oy, orientation)

        self.materialize_sector(grid, i - 1, base_i, center + o * oz, orientation)
        self.materialize_sector(grid, i - 1, base_i, center + o * oz, flip_z(orientation))
        #
        self.materialize_sector(grid, i - 1, base_i, center + o * oy, turn_right(orientation))
        self.materialize_sector(grid, i - 1, base_i, center + o * ox, turn_left(orientation))




    def fill_sector(self, grid: OctoGrid, iteration, center, orientation):

        ox = Vector3(*orientation[0])
        oy = Vector3(*orientation[1])
        oz = Vector3(*orientation[2])

        iteration += 1

        points = [ox *x + oy * y + oz * z + center
                  for x in range(0, p2(iteration) + 1)
                  for y in range(0, p2(iteration) + 1)
                  for z in range(0, p2(iteration) + 1)
                  if x + y + z < p2(iteration) + 1
                  ]

        for point in points:
            grid.insert_cell(center=point)

    @classmethod
    def build_solid_sector(cls, iteration):
        pass



def test_fill_sector():
    grid = OctoGrid()
    builder = OctoSectorBuilder(4, 2)
    i = 5


    builder.detailed_core_sector(grid, i, Vector3(0,0,0), UNE)
    builder.detailed_core_sector(grid, i, Vector3(0, 0, 0), UNW)
    builder.detailed_core_sector(grid, i, Vector3(0, 0, 0), USE)
    builder.detailed_core_sector(grid, i, Vector3(0, 0, 0), USW)

    grid.compute_trimming()

    RenderUtils.render_grid(grid, z_min=0, filename="detailed_core.stl")


# builder.detailed_core_sector_v2(grid, i, Vector3(0,0,0), UNE)
#     builder.detailed_core_sector_v2(grid, i, Vector3(0, 0, 0), UNW)
#     builder.detailed_core_sector_v2(grid, i, Vector3(0, 0, 0), USE)
#     builder.detailed_core_sector_v2(grid, i, Vector3(0, 0, 0), USW)


    # builder.materialize_sector(grid, 4, 0, Vector3(0, 0, 0), USW)
    # builder.materialize_sector(grid, 4, 1, Vector3(0, 0, 0), UNE)
    # builder.materialize_sector(grid, 4, 2, Vector3(0, 0, 0), UNW)
    # builder.materialize_sector(grid, 4, 3, Vector3(0, 0, 0), USE)



    # builder.materialize_sector(grid, 4, 2, Vector3(0, 0, 0), DSW)
    # builder.materialize_sector(grid, 4, 0, Vector3(0, 0, 0), DNE)
    # builder.materialize_sector(grid, 4, 3, Vector3(0, 0, 0), DNW)
    # builder.materialize_sector(grid, 4, 1, Vector3(0, 0, 0), DSE)

    # builder.fill_sector(grid, i, Vector3(0, 0, 0), USW)
    # builder.fill_sector(grid, i, Vector3(0, 0, 0), USE)
    # builder.fill_sector(grid, i, Vector3(0, 0, 0), UNW)
    # builder.fill_sector(grid, i, Vector3(0, 0, 0), UNE)
    # builder.fill_sector(grid, i, Vector3(0, 0, 0), DSW)
    # builder.fill_sector(grid, i, Vector3(0, 0, 0), DSE)
    # builder.fill_sector(grid, i, Vector3(0, 0, 0), DNW)
    # builder.fill_sector(grid, i, Vector3(0, 0, 0), DNE)



def test_materialize_sector():
    grid = OctoGrid()
    builder = OctoSectorBuilder(4, 2)

    builder.materialize_sector(grid, 4, 3, Vector3(0, 0, 0), UNE)

    RenderUtils.render_grid(grid)


if __name__ == "__main__":
    test_fill_sector()
    # test_materialize_sector()
