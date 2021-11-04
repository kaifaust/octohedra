from copy import copy
from dataclasses import astuple

import numpy as np
from euclid3 import *
from stl import mesh

from printing.grid.OctoCell import OctoCell
from printing.grid.OctoVector import OctoVector
from printing.grid.TetraCell import TetraCell
from printing.utils import RenderUtils
from printing.utils.OctoConfigs import config_25
from printing.utils.OctoUtil import NE, NW, SE, SW, X, Y, Z, p2


class OctoGrid:
    """
    This class only knows how to generate primitive octoflakes. okay but I wanted to try out
    this wrapping thing
    """

    def __init__(self):
        self.occ = dict()

    def merge(self, other, overwrite=False):
        self.occ = {**self.occ, **other.occ}
        return self

    def __add__(self, other):
        return self.merge(other)

    def keep_octo(self, m, center):
        to_keep = dict()
        for x, y, z in self.occ:
            i, j, k = tuple(Vector3(x, y, z) - center)
            yz = abs(j) + abs(k) <= m
            zx = abs(k) + abs(i) <= m
            if yz and zx:
                to_keep[(x, y, z)] = self.occ[(x, y, z)]

        self.occ = to_keep

    # TODO: Move this to an OctoBuilders utility file?
    def fill(self, i, f_i, center=(0, 0, 0)):

        print(f_i)
        s = p2(f_i)
        o = p2(f_i, -1)
        r = p2(i - f_i)

        print(s, o, r)

        for z in range(-r, r + 1):
            hr = r - abs(z) - 1
            for x in range(-hr, hr + 1, 2):
                for y in range(-hr, hr + 1, 2):
                    c = Vector3(*center) + (s * x, s * y, s * z)

                    # This will need to refer to the grid, duh
                    # self.make_flake(f_i, center=c)

    def insert_cell(self, center=None, x=0, y=0, z=0, strict=True):
        if center is None:
            center = OctoVector(x, y, z)
        if strict:
            center.validate()
        if center.z % 2 == 1:
            self.occ[center] = TetraCell()
        else:
            self.occ[center] = OctoCell()
        #
        #
        #
        # cell = None
        # if z % 4 == 0 and (x % 4 == 2 and y % 4 == 0 or x % 4 == 0 and y % 4 == 2):
        #     cell = OctoCell()
        # elif z % 4 == 2 and (x % 4 == 0 and y % 4 == 0 or x % 4 == 2 and y % 4 == 2):
        #     cell = OctoCell()
        # elif x % 2 == 1 and y % 2 == 1:
        #     cell = TetraCell()
        # if cell is not None:
        #     self.occ[OctoVector(x, y, z)] = cell
        # else:
        #     raise Exception(f"You tried to insert a cell at {x, y, z}")

    def render(self, config):
        mesh_data = [
            cell.render(config, center).data
            for center, cell in self.occ.items()
            ]

        if len(mesh_data) == 0:
            raise Exception("No objects to render!")

        return mesh.Mesh(np.concatenate(mesh_data), remove_empty_areas=True)

    # def render_trimesh(self, config):
    #     meshes = [
    #         cell.render_trimesh(config, center)
    #         for center, cell in self.occ.items()
    #         ]
    #
    #     # noinspection PyTypeChecker
    #     return trimesh.util.concatenate(meshes)

    def crop_bottom(self):
        self.crop(z_min=0)

    def split(self, z_split):
        above_grid = OctoGrid()
        for center in self.occ:
            if center.z >= z_split:
                above_grid.insert_cell(center)

        above_grid.crop(z_min=z_split)
        self.crop(z_max=z_split)

        return above_grid, self

    def crop(self,
             x_min=-math.inf,
             x_max=math.inf,
             y_min=-math.inf,
             y_max=math.inf,
             z_min=-math.inf,
             z_max=math.inf
             ):
        to_remove = set()
        for center, cell in self.occ.items():

            if center.z == z_min:
                cell.crop_bottom = True
            if center.z < z_min:
                to_remove.add(center)

            # tODO: Make this work again
            # if center.z == z_max:
            #     cell.crops.add(Crop.TOP)
            # if center.z > z_max:
            #     to_remove.add(center)
            # #
            # if center.x == x_min:
            #     cell.crops.add(Crop.WEST)
            # elif center.x < x_min:
            #     to_remove.add(center)
            #
            # if center.x == x_max:
            #     cell.crops.add(Crop.EAST)
            # elif center.x > x_max:
            #     to_remove.add(center)
            #
            # if center.y == y_min:
            #     cell.crops.add(Crop.SOUTH)
            # elif center.y < y_min:
            #     to_remove.add(center)
            #
            # if center.y == y_max:
            #     cell.crops.add(Crop.NORTH)
            # elif center.y > y_max:
            #     to_remove.add(center)

        for center in to_remove:
            self.occ.pop(center)

        return self

    def compute_trimming(self):
        for center, cell in self.occ.items():
            if isinstance(cell, TetraCell):
                self.trim_tetra(cell, center)
            elif isinstance(cell, OctoCell):
                self.trim_octo(cell, center)
            else:
                raise Exception("WTF are you doing bro?")

    def trim_tetra(self, cell, center):
        raise Exception("Yeah we're not doing it this way anymore")
        # c = center
        # x = center.x
        # y = center.y
        # z = center.z
        #
        # trims = set()
        #
        # flip = 1 if (x + y + z) % 4 == 3 else -1
        # o_wsw = c + -Z * flip + SW + 2 * W
        # o_ssw = (c + -Z * flip + SW + 2 * S)
        # o_ese = (c + Z * flip + SE + 2 * E)
        # o_sse = (c + Z * flip + SE + 2 * S)
        # o_wnw = (c + Z * flip + NW + 2 * W)
        # o_nnw = (c + Z * flip + NW + 2 * N)
        # o_ene = (c + -Z * flip + NE + 2 * E)
        # o_nne = (c + -Z * flip + NE + 2 * N)
        #
        # if o_wsw in self.occ or o_ssw in self.occ:
        #     trims.add(Trim.SW)
        # if o_ese in self.occ or o_sse in self.occ:
        #     trims.add(Trim.SE)
        # if o_wnw in self.occ or o_nnw in self.occ:
        #     trims.add(Trim.NW)
        # if o_ene in self.occ or o_nne in self.occ:
        #     trims.add(Trim.NE)
        #
        # cell.trims = trims

    def trim_octo(self, cell, center):
        # vc = Vector3(*center)
        vc = center
        spacing = 2

        cell.trim_ne = vc + NE * spacing in self.occ
        cell.trim_nw = vc + NW * spacing in self.occ
        cell.trim_sw = vc + SW * spacing in self.occ
        cell.trim_se = vc + SE * spacing in self.occ

        # TODO: needs the rest of these
        attic = ((vc + (Z + X) * spacing) in self.occ,
                 # and Crop.TOP not in self.occ[tuple(vc + E + Z)].crops,
                 (vc + (Z + Y) * spacing) in self.occ,
                 (vc + (Z - X) * spacing) in self.occ,
                 (vc + (Z - Y) * spacing) in self.occ,
                 (vc + 2 * Z * spacing) in self.occ
                 )

        basement = ((vc + (-Z + X) * spacing) in self.occ,
                    # and Crop.TOP not in self.occ[tuple(vc + E + Z)].crops,
                    (vc + (-Z + Y) * spacing) in self.occ,
                    (vc + (-Z - X) * spacing) in self.occ,
                    (vc + (-Z - Y) * spacing) in self.occ,
                    )

        # TODO: For vertical cropping, we need the notion of a clipped upper point

        cell.weld_up = all(attic)
        cell.weld_down = all(basement)

    def carve(self, x_min, x_max, y_min, y_max, z_min, z_max):
        """Removes all cells in a rectangular prism"""
        to_purge = set()
        for x, y, z in self.occ:
            if x_min <= x <= x_max and y_min <= y <= y_max and z_min <= z <= z_max:
                to_purge.add((x, y, z))

        for tup in to_purge:
            self.occ[tup].is_solid = True

    def full_symmetry(self, center=None):
        to_add = dict()

        for center, cell in self.occ.items():
            x, y, z = center
            to_add[(y, x, z)] = copy(cell)
            to_add[(-x, y, z)] = copy(cell)
            to_add[(y, -x, z)] = copy(cell)

        self.occ = {**self.occ, **to_add}
        return self

    def reflect_x(self):
        self.reflect(x=-1)

    def reflect_y(self):
        self.reflect(y=-1)

    def reflect_z(self):
        self.reflect(z=-1)

    def reflect(self, x=1, y=1, z=1, center_of_reflection=OctoVector()):
        rv = OctoVector(x, y, z)
        new_grid = OctoGrid()
        for center in self.occ:
            new_center = (center - center_of_reflection) * rv + center_of_reflection

            print(center, center - center_of_reflection, (center - center_of_reflection) * rv,
                  (center - center_of_reflection) * rv + center_of_reflection, new_center)

            new_grid.insert_cell(new_center)

        self.merge(new_grid)

    def four_way(self, center_of_rotation=OctoVector()):
        new_grid = OctoGrid()
        for center in self.occ:
            x, y, z = astuple(center - center_of_rotation)
            new_grid.insert_cell(OctoVector(y, x, z) + center_of_rotation)

        self.merge(new_grid)
        self.reflect_x()
        self.reflect_y()

        return self

    def six_way(self, center_of_rotation=OctoVector()):
        to_add = dict()

        new_grid = OctoGrid()
        for center, cell in self.occ.items():
            x, y, z = (center - center_of_rotation).as_tuple()
            new_grid.insert_cell(OctoVector(x, z, y) + center_of_rotation)
            new_grid.insert_cell(OctoVector(z, y, x) + center_of_rotation)
            new_grid.insert_cell(OctoVector(x, y, -z) + center_of_rotation)
            # to_add[(x, z, y)] = copy(cell)
            # to_add[(z, y, x)] = copy(cell)

            # TODO: Can we do this in one step, rather than using four_way?
            # to_add[(y, z, x)] = copy(cell)
            # to_add[(z, x, y)] = copy(cell)
            # to_add[(z, y, x)] = copy(cell)
            # to_add[(y, x, z)] = cell

        self.merge(new_grid)

        return self.four_way(center_of_rotation)

    def __str__(self):
        return str(self.occ.keys())


# def tetra_test():
#     grid = OctoGrid()
#
#     # grid.make_flake(1)
#     grid.insert_cell(center=(2, 0, 0))
#     grid.insert_cell(center=(0, 2, 0))
#     grid.insert_cell(center=(6, 0, 0))
#     grid.insert_cell(center=(2, -2, 2))
#     grid.insert_cell(center=(6, 2, 2))
#     grid.insert_cell(center=(3, 1, 1))
#     grid.insert_cell(center=(3, 1, -1))
#
#     grid.compute_trimming()
#     print(grid.occ[(3, 1, 1)].trims)
#
#     RenderUtils.render_grid(grid, config_25, z_min=None)


def reflection_test():
    grid = OctoGrid()

    grid.insert_cell(OctoVector(1, 0, 0))
    print(grid)
    grid.four_way()
    print(grid)

    RenderUtils.render_grid(grid, config_25, z_min=None)
    print("Yo")


if __name__ == "__main__":
    # tetra_test()
    reflection_test()
