from enum import Enum
from pathlib import Path

from euclid3 import Vector3

import numpy as np
from stl import Mesh

from printing.octo import OctoConfigs
from printing.octo.OctoConfig import OctoConfig
from printing.octo.OctoUtil import E, N, W, S, CARDINAL, UP, DOWN, p2, SQRT22, SQRT2
from printing.rendering.RenderUtils import seal_belt, stitch_belts


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
class OctoCell:
    """
    Represents an abstract octahedron within an OctoGrid. It's size is relative to its coordinates in the grid,
    not its physical size.





    """

    def __init__(self,
                 cell_scale=0,
                 center=None,
                 is_pyramid=False,  # TODO: Deprecate
                 crops=None,
                 is_solid=False,
                 trims=None,
                 weld_up=False,
                 weld_down=False,
                 point_up=False,
                 point_down=False,
                 is_point_aligned=False,
                 is_dummy = False,
                 is_subcell = False
                 ):

        self.cell_scale = cell_scale
        self.center = center if center is not None else Vector3(0, 0, 0)
        self.is_pyramid = is_pyramid
        self.crops = crops if crops is not None else set()
        self.is_solid = is_solid
        self.trims = trims if trims is not None else set()
        self.weld_up = weld_up
        self.weld_down = weld_down
        self.point_up = point_up
        self.point_down = point_down
        self.is_point_aligned = is_point_aligned
        self.is_dummy = is_dummy
        self.is_subcell = is_subcell



        if self.is_pyramid:
            self.crops.add(Crop.BOTTOM)

    def __copy__(self):
        return OctoCell(cell_scale=self.cell_scale)


    def render(self, config: OctoConfig, center):

        if self.is_dummy:
            print("Not rendering because I'm a dummy")
            return Mesh()



        overlap = config.overlap

        oversize = config.cell_size * p2(self.cell_scale) + overlap

        slit = config.slit if not self.is_subcell else 0

        trim = (overlap + slit / 2)/2
        weld = overlap + slit / 2

        top = oversize / 2 * UP
        bottom = oversize / 2 * DOWN

        top_belt = top + overlap/2 * (CARDINAL + DOWN)
        bottom_belt = bottom + overlap/2 * (CARDINAL + UP)

        equator_belt = CARDINAL * oversize / 2
        equator_upper_belt = equator_belt + trim * (UP - CARDINAL)
        equator_lower_belt = equator_belt + trim * (DOWN - CARDINAL)

        # print(config.cell_size, oversize, equator_belt)

        # print(equator_belt)

        upper_belts = []
        lower_belts = []

        if Crop.TOP in self.crops:
            pass
        elif self.is_solid:
            upper_belts = [np.copy(equator_belt) + UP * oversize]
        elif self.weld_up:
            top_welding_upper_belt = top + weld * (CARDINAL + UP)
            top_welding_lower_belt = top + weld * (CARDINAL + DOWN)

            upper_belts = [top_welding_upper_belt, top_welding_lower_belt, equator_upper_belt]
        else:
            upper_belts = [top_belt, equator_upper_belt]

        if Crop.BOTTOM in self.crops:
            pass
        elif self.is_solid:
            equator_belt += DOWN * oversize
        elif self.weld_down:
            down_welding_upper_belt = bottom + weld * (CARDINAL + UP)
            down_welding_lower_belt = bottom + weld * CARDINAL

            lower_belts = [equator_lower_belt, down_welding_upper_belt, down_welding_lower_belt]
        else:
            lower_belts = [equator_lower_belt, bottom_belt]

        # upper_belts = [top_upper_belt, top_lower_belt, equator_upper_belt]
        # lower_belts = [equator_lower_belt, bottom_upper_belt, bottom_lower_belt]

        # belts = [equator_belt, equator_upper_belt, equator_lower_belt, top_upper_belt, top_lower_belt,
        #          bottom_upper_belt, bottom_lower_belt, up_welding_belt_top, up_welding_belt_bottom, down_welding_belt_top,
        #          down_welding_belt_bottom]
        # upper_belts = [equator_upper_belt, top_upper_belt, top_lower_belt, up_welding_belt_top, up_welding_belt_bottom]
        # lower_belts = [equator_lower_belt, bottom_upper_belt, bottom_lower_belt, down_welding_belt_top,
        #                down_welding_belt_bottom]

        # if Crop.TOP in self.crops:
        #     upper_belts = []
        # if Crop.BOTTOM in self.crops:
        #     lower_belts = []

        if not self.is_solid and Crop.TOP not in self.crops and Crop.BOTTOM not in self.crops:
            if Trim.NE in self.trims:# or self.cell_scale>0:
                equator_belt[0] -= (N + E) * trim/2
                equator_belt[1] -= (N + E) * trim/2
            if Trim.NW in self.trims:# or self.cell_scale>0:
                equator_belt[1] -= (N + W) * trim/2
                equator_belt[2] -= (N + W) * trim/2
            if Trim.SW in self.trims:# or self.cell_scale>0:
                equator_belt[2] -= (S + W) * trim/2
                equator_belt[3] -= (S + W) * trim/2
            if Trim.SE in self.trims:# or self.cell_scale>0:
                equator_belt[3] -= (S + E) * trim/2
                equator_belt[0] -= (S + E) * trim/2

        # if Crop.UP in self.crops:
        #     for belt in upper_belts:
        #         belt[:, 2] = 0
        #
        # if Crop.DOWN in self.crops:
        #     for belt in lower_belts:
        #         belt[:, 2] = 0

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

        # belts = np.array(upper_belts + [equator_belt] + lower_belts)

        # belts = [top_belt, equator_belt]

        faces = [seal_belt(belts[0])]
        for i in range(len(belts) - 1):
            faces.append(stitch_belts(belts[i], belts[i + 1]))

        faces.append(seal_belt(belts[-1], is_bottom=True))

        # faces.append(seal_belt(top_upper_belt))
        # faces.append(stitch_belts(top_upper_belt, top_lower_belt))
        # faces.append(stitch_belts(top_lower_belt, equator_upper_belt))
        # faces.append(stitch_belts(equator_upper_belt, equator_belt))
        # faces.append(stitch_belts(equator_belt, equator_lower_belt))
        # faces.append(stitch_belts(equator_lower_belt, bottom_upper_belt))
        # faces.append(stitch_belts(bottom_upper_belt, bottom_lower_belt))

        # faces.append(seal_belt(bottom_lower_belt, is_bottom=True))

        # if self.is_solid:
        #     faces.append(seal_belt(top_solid_belt))
        #     faces.append(stitch_belts(top_solid_belt, bottom_solid_belt))
        #     faces.append(seal_belt(bottom_solid_belt, bottom=True))
        # elif self.is_pyramid:
        #     if self.point_up:
        #         faces.append(stitch_belt_to_point(top, equator_belt))
        #         faces.append(seal_belt(equator_belt, bottom=True))
        #     else:
        #         faces.append(seal_belt(top_belt))
        #         faces.append(stitch_belts(top_belt, equator_belt))
        #         faces.append(seal_belt(equator_belt, bottom=True))
        # else:  # Is a complete octo
        #     if Trim.FRONT in cell.trims:
        #         equator_belt[: 2, 1] = equator_top_belt[0, 1]
        #     if Trim.BACK in cell.trims:
        #         equator_belt[2:, 1] = equator_top_belt[2, 1]
        #     if Trim.RIGHT in cell.trims:
        #         equator_belt[1: 3, 0] = equator_top_belt[1, 0]
        #     if Trim.LEFT in cell.trims:
        #         equator_belt[3, 0] = equator_top_belt[0, 0]
        #         equator_belt[0, 0] = equator_top_belt[0, 0]
        #
        #     # Top half
        #     if cell.weld_up:
        #         faces.append(seal_belt(up_welding_belt_top))
        #         faces.append(stitch_belts(up_welding_belt_top, up_welding_belt_bottom))
        #         faces.append(stitch_belts(up_welding_belt_bottom, equator_top_belt))
        #         faces.append(stitch_belts(equator_top_belt, equator_belt))
        #         faces.append(stitch_belts(equator_belt, equator_bottom_belt))
        #     elif cell.point_up:
        #         faces.append(stitch_belt_to_point(top, equator_top_belt))
        #         faces.append(stitch_belts(equator_top_belt, equator_belt))
        #         faces.append(stitch_belts(equator_belt, equator_bottom_belt))
        #     else:  # snipped top
        #         faces.append(seal_belt(top_belt))
        #         faces.append(stitch_belts(top_belt, equator_top_belt))
        #         faces.append(stitch_belts(equator_top_belt, equator_belt))
        #         faces.append(stitch_belts(equator_belt, equator_bottom_belt))
        #
        #     # Bottom half
        #     if cell.weld_down:
        #         faces.append(stitch_belts(equator_bottom_belt, down_welding_belt_top))
        #         # faces.append(self.seal_belt(down_welding_belt_top))
        #         faces.append(stitch_belts(down_welding_belt_top, down_welding_belt_bottom))
        #         # faces.append(self.seal_belt(down_welding_belt_bottom, bottom=True))
        #         faces.append(stitch_belt_to_point(cropped_bottom, down_welding_belt_bottom, bottom=True))
        #
        #
        #     elif cell.point_down:
        #         faces.append(stitch_belt_to_point(bottom, equator_bottom_belt, bottom=True))
        #     else:  # Snipped bottom
        #         faces.append(stitch_belts(equator_bottom_belt, bottom_belt))
        #         faces.append(seal_belt(bottom_belt, bottom=True))
        #
        # if Crop.UP in cell.crops:
        #     pass

        # Make the faces into a mesh
        face_array = np.concatenate(faces)
        octo = Mesh(np.zeros(face_array.shape[0], dtype=Mesh.dtype))
        octo.vectors = face_array
        octo.update_normals()
        octo.translate(Vector3(*center) * config.cell_size/2) #/SQRT2)

        # Todo, scale

        return octo


def test_basic_render():
    cell = OctoCell(
        crops={Crop.WEST},
        # trims={Trim.SW},
        weld_up=True,
        weld_down=True,

        is_point_aligned=True)
    config = OctoConfigs.config_25
    cell.render(config).save(Path.home() / "Desktop" / "derp.stl")


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
