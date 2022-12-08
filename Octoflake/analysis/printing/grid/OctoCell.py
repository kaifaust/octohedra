from dataclasses import dataclass
from pathlib import Path
from typing import Set

import numpy as np

from printing.grid.GridCell import GridCell, belts_to_trimesh
from printing.grid.OctoVector import OctoVector
from printing.utils import OctoConfigs, RenderUtils
from printing.utils.OctoConfig import RenderConfig
from printing.utils.OctoUtil import CARDINAL, DOWN, E, N, NE, NW, S, SE, SQRT22, SW, UP, W, X, Y, Z


@dataclass
class OctoCell(GridCell):
    weld_up: bool = False
    weld_down: bool = False
    clip_point_up: bool = False

    crop_top: bool = False
    crop_bottom: bool = False
    crop_east: bool = False
    crop_west: bool = False
    crop_north: bool = False
    crop_south: bool = False

    trim_ne: bool = False
    trim_nw: bool = False
    trim_sw: bool = False
    trim_se: bool = False

    def trim(self, center: OctoVector, occ=Set[OctoVector]):
        vc = center
        spacing = 2

        self.trim_ne = vc + NE * spacing in occ
        self.trim_nw = vc + NW * spacing in occ
        self.trim_sw = vc + SW * spacing in occ
        self.trim_se = vc + SE * spacing in occ

        # TODO: needs the rest of these
        attic = ((vc + (Z + X) * spacing) in occ,
                 # and Crop.TOP not in self.occ[tuple(vc + E + Z)].crops,
                 (vc + (Z + Y) * spacing) in occ,
                 (vc + (Z - X) * spacing) in occ,
                 (vc + (Z - Y) * spacing) in occ,
                 (vc + 2 * Z * spacing) in occ
                 )

        basement = ((vc + (-Z + X) * spacing) in occ,
                    # and Crop.TOP not in self.occ[tuple(vc + E + Z)].crops,
                    (vc + (-Z + Y) * spacing) in occ,
                    (vc + (-Z - X) * spacing) in occ,
                    (vc + (-Z - Y) * spacing) in occ,
                    )

        # TODO: For vertical cropping, we need the notion of a clipped upper point
        # TODO: Need to mak e

        self.clip_point_up = not any(attic)

        self.weld_up = all(attic)
        self.weld_down = all(basement)

    def render(self, config: RenderConfig, center=OctoVector(), sharp=False, flower_mode=True):

        overlap = config.overlap

        oversize = config.cell_size + overlap
        slit = config.slit

        trim = (overlap + slit / 2) / 2
        weld = overlap + slit / 2

        top = oversize / 2 * UP
        bottom = oversize / 2 * DOWN

        top_belt = overlap / 2 * (CARDINAL + DOWN) + top

        if self.clip_point_up:
            # top_belt = (3 * config.layer_height) * (CARDINAL + DOWN) + top
            # top_belt = (overlap / 2 + 1.5 * config.layer_height) * (CARDINAL + DOWN) + top
            top_belt = (1.25 * config.line_width) * (CARDINAL + DOWN) + top

        bottom_belt = overlap / 2 * (CARDINAL + UP) + bottom

        static_equator_belt = CARDINAL * oversize / 2
        equator_belt = CARDINAL * oversize / 2
        equator_upper_belt = equator_belt + trim * (-CARDINAL + UP)
        equator_lower_belt = equator_belt + trim * (-CARDINAL + DOWN)

        pyramid_bottom_belt = equator_belt + config.first_layer_height * DOWN \
                              - config.layer_height * (0.5) * DOWN

        flange = config.floor_height
        # TODO: Why these factors of sqrt2
        flange_scooch = trim / 2 - flange * SQRT22 / 2
        upper_flange_belt = equator_belt + flange * (UP - CARDINAL)
        lower_flange_belt = equator_belt + flange * (UP - CARDINAL)

        top_welding_upper_belt = top + weld * CARDINAL + 0.01 * UP
        top_welding_lower_belt = top + weld * (CARDINAL + DOWN)

        down_welding_upper_belt = bottom + weld * (CARDINAL + UP)
        down_welding_lower_belt = bottom + weld * CARDINAL + overlap / 2 * UP

        upper_belts = []
        if not self.crop_top:

            if self.weld_up:
                upper_belts.append(top_welding_upper_belt)
                upper_belts.append(top_welding_lower_belt)
            else:
                upper_belts.append(top_belt)
            if not sharp:
                upper_belts.append(equator_upper_belt)

        lower_belts = []
        if not self.crop_bottom:
            if not sharp:
                lower_belts.append(equator_lower_belt)
            if self.weld_down:
                lower_belts.append(down_welding_upper_belt)
                lower_belts.append(down_welding_lower_belt)
            lower_belts.append(bottom_belt)
        # else:

        # lower_belts.append(pyramid_bottom_belt)

        # For the old style
        # lower_belts = []
        # if not self.crop_bottom:
        #     if not sharp:
        #         lower_belts.append(equator_lower_belt)
        #     if self.weld_down:
        #         lower_belts.append(down_welding_upper_belt)
        #         lower_belts.append(down_welding_lower_belt)
        #     lower_belts.append(bottom_belt)

        if self.trim_ne:
            equator_belt[0] -= (N + E) * trim / 2
            equator_belt[1] -= (N + E) * trim / 2
            upper_flange_belt[0] -= (N + E) * flange_scooch
            upper_flange_belt[1] -= (N + E) * flange_scooch
        if self.trim_nw:
            equator_belt[1] -= (N + W) * trim / 2
            equator_belt[2] -= (N + W) * trim / 2
            upper_flange_belt[1] -= (N + W) * flange_scooch
            upper_flange_belt[2] -= (N + W) * flange_scooch
        if self.trim_sw:
            equator_belt[2] -= (S + W) * trim / 2
            equator_belt[3] -= (S + W) * trim / 2
            upper_flange_belt[2] -= (S + W) * flange_scooch
            upper_flange_belt[3] -= (S + W) * flange_scooch
        if self.trim_se:
            equator_belt[3] -= (S + E) * trim / 2
            equator_belt[0] -= (S + E) * trim / 2
            upper_flange_belt[3] -= (S + E) * flange_scooch
            upper_flange_belt[0] -= (S + E) * flange_scooch

        belts = np.array(upper_belts + [equator_belt] + lower_belts)
        # print(belts)

        for belt in belts:
            if self.crop_east:
                belt[0][0] = 0
                belt[0][1] = 0
            if self.crop_north:
                belt[1][0] = 0
                belt[1][1] = 0
            if self.crop_west:
                belt[2][0] = 0
                belt[2][1] = 0
            if self.crop_south:
                belt[3][0] = 0
                belt[3][1] = 0

        mesh = belts_to_trimesh(belts)
        if self.crop_bottom and flange > 0:
            # mesh += belts_to_trimesh(np.array([lower_flange_belt, pyramid_bottom_belt]))
            mesh += belts_to_trimesh(np.array([lower_flange_belt, static_equator_belt,
                                               pyramid_bottom_belt]))
            pass

        return mesh


def test_basic_render():
    config = OctoConfigs.default
    config.absolute_layers_per_cell = 3
    # config.absolute_overlap = 1

    config.print_settings()

    filename = Path.home() / "Desktop" / "derp.stl"

    cell1 = OctoCell(
            # crop_bottom=True
            # trim_se=True,
            weld_up=True,
            # weld_down=True,
            )

    # belts_to_trimesh

    cell2 = OctoCell(

            )

    cells = (cell1, cell2)

    RenderUtils.save_mesh(cell1.render(config))

    # RenderUtils.save_mesh(*[cell.render(config, OctoVector(4 * i, 0, 0)) for i, cell in
    #                           enumerate(cells)])


def testing():
    print("Doing some testing, I'm sure")
    test_basic_render()


if __name__ == "__main__":
    testing()
