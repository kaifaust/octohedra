from enum import Enum
from pathlib import Path

import numpy as np
from euclid3 import Vector3
from stl import Mesh

from printing.grid.GridCell import GridCell, seal_belt, stitch_belts
from printing.utils import OctoConfigs, RenderUtils
from printing.utils.OctoConfig import OctoConfig
from printing.utils.OctoUtil import CARDINAL, DOWN, E, N, S, SQRT22, UP, W, p2


def auto_str(cls):
    def __str__(self):
        return '%s(%s)' % (
            type(self).__name__,
            ', '.join('%s=%s' % item for item in vars(self).items())
            )

    cls.__str__ = __str__
    cls.__repr__ = __str__
    return cls


@auto_str
class Foo(object):
    def __init__(self, value_1, value_2):
        self.attribute_1 = value_1
        self.attribute_2 = value_2


class Crop(Enum):
    TOP = 1
    BOTTOM = 2
    EAST = 3
    NORTH = 4
    WEST = 5
    SOUTH = 6
    NONE = 7


class Trim(Enum):
    # TOP = 1  # Unused
    # BOTTOM = 2
    # FRONT = 3
    # BACK = 4
    # LEFT = 5
    # RIGHT = 6

    NE = 7
    NW = 8
    SW = 9
    SE = 10


@auto_str
class OctoCell(GridCell):
    """
    Represents an abstract octahedron within an OctoGrid. It's size is relative to its
    coordinates in the grid, not its physical size.
    """

    def __init__(self, crops=None, trims=None, weld_up=False, weld_down=False, clip_point_up=False):
        super().__init__()
        self.crops = set() if crops is None else crops
        self.trims = set() if trims is None else trims
        self.weld_up = weld_up
        self.weld_down = weld_down
        self.clip_point_up = clip_point_up

    def __copy__(self):
        return OctoCell(self.crops.copy())

    def render(self, config: OctoConfig, center=None):
        center = Vector3(*center)/2 if center is not None else Vector3(0, 0, 0)

        overlap = config.overlap

        oversize = config.cell_size + overlap

        slit = config.slit

        trim = (overlap + slit / 2) / 2
        weld = overlap + slit / 2

        top = oversize / 2 * UP
        bottom = oversize / 2 * DOWN

        # top_belt = top + overlap  * (CARDINAL + DOWN)
        top_belt = top + overlap / 2.5 * (CARDINAL + DOWN)
        bottom_belt = bottom + overlap / 2 * (CARDINAL + UP)

        equator_belt = CARDINAL * oversize / 2
        equator_upper_belt = equator_belt + trim * (UP - CARDINAL)
        equator_lower_belt = equator_belt + trim * (DOWN - CARDINAL)

        flange = config.floor_height
        upper_flange_belt = equator_belt + flange * SQRT22 * (UP - CARDINAL)
        lower_flange_belt = equator_belt + flange * SQRT22 * (UP - CARDINAL)

        # print(config.cell_size, oversize, equator_belt)

        # print(equator_belt)

        upper_belts = []
        lower_belts = []

        if Crop.TOP in self.crops:
            pass


        elif self.weld_up:
            top_welding_upper_belt = top + weld * (CARDINAL + UP)
            top_welding_lower_belt = top + weld * (CARDINAL + DOWN)

            upper_belts = [top_welding_upper_belt, top_welding_lower_belt, equator_upper_belt]
        else:
            upper_belts = [top_belt, equator_upper_belt]
            # upper_belts = [pointy_belt, top_belt, equator_upper_belt]

        if Crop.BOTTOM in self.crops:

            upper_belts.append(upper_flange_belt)
            upper_belts.append(lower_flange_belt)



        elif self.weld_down:
            down_welding_upper_belt = bottom + weld * (CARDINAL + UP)
            down_welding_lower_belt = bottom + weld * CARDINAL + overlap / 2 * ( UP)
            lower_belts = [equator_lower_belt, down_welding_upper_belt, down_welding_lower_belt]
        else:
            lower_belts = [equator_lower_belt, bottom_belt]

        flange_scooch = trim / 2 - flange * SQRT22 / 2



        if Trim.NE in self.trims:  # or self.cell_scale>0:
            if Crop.BOTTOM not in self.crops:
                equator_belt[0] -= (N + E) * trim / 2
                equator_belt[1] -= (N + E) * trim / 2
            upper_flange_belt[0] -= (N + E) * flange_scooch
            upper_flange_belt[1] -= (N + E) * flange_scooch

        if Trim.NW in self.trims:  # or self.cell_scale>0:
            if Crop.BOTTOM not in self.crops:
                equator_belt[1] -= (N + W) * trim / 2
                equator_belt[2] -= (N + W) * trim / 2
            upper_flange_belt[1] -= (N + W) * flange_scooch
            upper_flange_belt[2] -= (N + W) * flange_scooch
        if Trim.SW in self.trims:  # or self.cell_scale>0:
            if Crop.BOTTOM not in self.crops:
                equator_belt[2] -= (S + W) * trim / 2
                equator_belt[3] -= (S + W) * trim / 2
            upper_flange_belt[2] -= (S + W) * flange_scooch
            upper_flange_belt[3] -= (S + W) * flange_scooch
            # TODO: Moving the belts back to upright (Do I care?)
            lower_flange_belt[2] += (S + W) * flange * SQRT22 / 2
            lower_flange_belt[3] += (S + W) * flange * SQRT22 / 2
        if Trim.SE in self.trims:  # or self.cell_scale>0:
            if Crop.BOTTOM not in self.crops:
                equator_belt[3] -= (S + E) * trim / 2
                equator_belt[0] -= (S + E) * trim / 2
            upper_flange_belt[3] -= (S + E) * flange_scooch
            upper_flange_belt[0] -= (S + E) * flange_scooch

        belts = np.array(upper_belts + [equator_belt] + lower_belts)

        for belt in belts:
            if Crop.EAST in self.crops:
                belt[0][0] = 0
                belt[0][1] = 0
            if Crop.NORTH in self.crops:
                belt[1][0] = 0
                belt[1][1] = 0
            if Crop.WEST in self.crops:
                belt[2][0] = 0
                belt[2][1] = 0
            if Crop.SOUTH in self.crops:
                belt[3][0] = 0
                belt[3][1] = 0

        faces = [seal_belt(belts[0])]
        for i in range(len(belts) - 1):
            faces.append(stitch_belts(belts[i], belts[i + 1]))

        faces.append(seal_belt(belts[-1], is_bottom=True))

        # Make the faces into a mesh
        face_array = np.concatenate(faces)
        octo = Mesh(np.zeros(face_array.shape[0], dtype=Mesh.dtype))
        octo.vectors = face_array
        octo.update_normals()
        octo.translate(Vector3(*center) * config.cell_size / 2)  # /SQRT2)

        # Todo, scale

        return octo


def test_basic_render():
    config = OctoConfigs.config_25
    config.absolute_layers_per_cell = 8
    config.absolute_overlap = 1
    config.derive()
    config.print_settings()

    filename = Path.home() / "Desktop" / "derp.stl"

    cell1 = OctoCell(
            # crops={Crop.BOTTOM},
            trims={Trim.SW},
            # weld_up=True,
            weld_down=True,
            )

    cell2 = OctoCell(

            )

    cells = (cell1,cell2)

    RenderUtils.save_meshes(*[cell.render(config, Vector3(4 * i, 0, 0)) for i, cell in enumerate(cells)])



def testing():
    print("Doing some testing, I'm sure")
    test_basic_render()


if __name__ == "__main__":
    testing()

    # def __str__(self):
    #     return f"Octahedron({self.trims})"
    #
    # def __repr__(self):
    #     return self.__str__()
