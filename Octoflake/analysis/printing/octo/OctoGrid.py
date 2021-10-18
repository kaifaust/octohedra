from collections import defaultdict
from copy import copy

import numpy as np
from euclid3 import *
from multimap import MultiMap, MutableMultiMap
from stl import mesh

from printing.octo.OctoCell import OctoCell, Trim, Crop
from printing.octo.OctoUtil import X, Y, Z, Y2, X2, p2, E, DOWN, UP, S, W, N, NE, SE, SW, NW


class OctoGrid:
    """This class only knows how to generate primitive octoflakes."""

    def __init__(self):
        self.occ = defaultdict(set)



    def merge(self, other):
        keys = set(self.occ).union(other.occ)

        new_occ = defaultdict(set)
        for key in keys:
            new_occ[key] = self.occ[key].union(other.occ[key])




        self.occ = new_occ
        return self

    def __add__(self, other):
        return self.merge(other)

    # def clear(self, iteration, center=(0, 0, 0)):
    #
    #     r = 2 ** (iteration - 1)
    #     # print(r)
    #     to_remove = []
    #     for x in range(-r, r + 1):
    #         for y in range(-r, r + 1):
    #             for z in range(-r, r + 1):
    #                 if abs(x) + abs(y) + 2 * abs(z) <= r * 2:
    #                     # print(x, y, z)
    #                     if z == 1:
    #                         pass
    #                         # print((x, y, z, r, x + y + 4 * z))
    #                     to_remove.append(tuple(np.array(center) + (x, y, z)))
    #
    #     for remove in to_remove:
    #         if remove in self.occ:
    #             self.occ.pop(remove)
    #         if remove in self.welding:
    #             self.welding.pop(remove)

    # TODO: Move to OctoBuilder
    # def stellate(self, iteration, center=(0, 0, 0), offset=None):
    #     offset = 2 ** (iteration) if offset is None else offset
    #     si = iteration
    #     self.make_flake(si, (center[0] + offset, center[1] + offset, center[2]))
    #     self.make_flake(si, (center[0] + offset, center[1] - offset, center[2]))
    #     self.make_flake(si, (center[0] - offset, center[1] + offset, center[2]))
    #     self.make_flake(si, (center[0] - offset, center[1] - offset, center[2]))
    #     self.make_flake(si, (center[0], center[1], center[2] + offset))
    #     self.make_flake(si, (center[0], center[1], center[2] - offset))
    #
    # def fill(self, iteration, center=(0, 0, 0)):
    #     offset = 2 ** iteration / 4
    #     i2 = iteration - 2
    #     self.make_flake(i2, (center[0] + 2 * offset, center[1], center[2] + offset))
    #     self.make_flake(i2, (center[0] - 2 * offset, center[1], center[2] + offset))
    #     self.make_flake(i2, (center[0], center[1] + 2 * offset, center[2] + offset))
    #     self.make_flake(i2, (center[0], center[1] - 2 * offset, center[2] + offset))
    #     self.make_flake(i2, (center[0] + 2 * offset, center[1], center[2] - offset))
    #     self.make_flake(i2, (center[0] - 2 * offset, center[1], center[2] - offset))
    #     self.make_flake(i2, (center[0], center[1] + 2 * offset, center[2] - offset))
    #     self.make_flake(i2, (center[0], center[1] - 2 * offset, center[2] - offset))

    # TODO: This should be moved to a higher level octobuilder
    def faces(self, iteration, starting_iteration=1000, ending_iteration=0, tetra_left=False, tetra_right=True,
              center=(0, 0, 0)):

        center = np.array(center)

        offset = 2 ** iteration
        si = starting_iteration
        ei = ending_iteration
        if iteration <= starting_iteration:
            self.make_flake(iteration, center=center)

        if iteration > ending_iteration:

            if tetra_right: self.faces(iteration - 1, si, ei, False, True, center + (offset, 0, offset / 2))
            if tetra_right: self.faces(iteration - 1, si, ei, False, True, center + (-offset, 0, offset / 2))
            if tetra_left: self.faces(iteration - 1, si, ei, True, False, center + (0, offset, offset / 2))
            if tetra_left: self.faces(iteration - 1, si, ei, True, False, center + (0, -offset, offset / 2))
            if tetra_left: self.faces(iteration - 1, si, ei, True, False, center + (offset, 0, -offset / 2))
            if tetra_left: self.faces(iteration - 1, si, ei, True, False, center + (-offset, 0, -offset / 2))
            if tetra_right: self.faces(iteration - 1, si, ei, False, True, center + (0, offset, -offset / 2))
            if tetra_right: self.faces(iteration - 1, si, ei, False, True, center + (0, -offset, -offset / 2))

    def clear_octo(self, m, x=0, y=0, z=0, center=None):
        print(f"Clearing everything in an octo of size {m} centered at {center}")
        for i in range(-m, m + 1):
            for j in range(-m, m + 1):
                for k in range(-m, m + 1):

                    yz = abs(j) + abs(k) <= m
                    zx = abs(k) + abs(i) <= m

                    if yz and zx:
                        c = tuple(Vector3(i, j, k) + center)
                        # print(c)
                        # print(self.occ.pop(tuple(c), None))
                        # self.occ[c] = OctoCell()
                        # c = (i, j, k)
                        if c in self.occ:
                            # print(f"removing {c}")
                            self.occ.pop(c)

    def keep_octo(self, m, center):
        to_keep = dict()
        for x, y, z in self.occ:
            i, j, k = tuple(Vector3(x, y, z) - center)
            yz = abs(j) + abs(k) <= m
            zx = abs(k) + abs(i) <= m
            if yz and zx:
                to_keep[(x, y, z)] = self.occ[(x, y, z)]

        self.occ = to_keep

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

                    self.make_flake(f_i, center=c)

    def make_flake(self, iteration, center: Vector3 = None, cell_scale=0, overwrite=False):
        # print(iteration, center, cell_scale)
        center = center if center is not None else Vector3(0, 0, 0)

        # if iteration == 0:
        #     self.insert_cell(center, cell_scale=0, is_subcell=cell_scale>0)
        #     return
        if iteration == -1:
            return
        if iteration == cell_scale:
            # print("Inserting real cell at", center)
            self.insert_cell(center, cell_scale, overwrite=overwrite)
        elif iteration> cell_scale:
            # print("inserting dummy at", center)
            self.insert_cell(center, iteration, is_dummy=True)
        elif iteration==0:
            self.insert_cell(center, iteration, is_dummy=True)

        i1 = iteration - 1
        o = p2(i1)

        for direction in (E, N, W, S, UP, DOWN):
            self.make_flake(i1, center=center + o * direction, cell_scale=cell_scale)

        return self

    def insert_cell(self, center: Vector3, cell_scale=0, is_subcell=False, overwrite=False, is_dummy=False):


        m = p2(cell_scale)

        is_clear = True
        for i in range(-m, m + 1):
            for j in range(-m, m + 1):
                for k in range(-m, m + 1):

                    xy = abs(i) + abs(j) <= m
                    yz = abs(j) + abs(k) <= m
                    zx = abs(k) + abs(i) <= m

                    if yz and zx and xy:
                        c = tuple(Vector3(i, j, k) + center)
                        if c in self.occ:
                            for cell in self.occ[c]:
                                if not cell.is_dummy:
                                    is_clear = False


        # if cell_scale == 2:
        #     print(is_clear, overwrite)
        if is_clear or overwrite:
            self.occ[tuple(center)].add(OctoCell(cell_scale=cell_scale, center=center, is_subcell=is_subcell,
                                               is_dummy=is_dummy))



        # if cell_scale == 0:
        #     return

        # r = p2(cell_scale)
        # for z in range(-r, r + 1):
        #     hr = r - abs(z) - 1
        #     for x in range(-hr, hr + 1, 2):
        #         for y in range(-hr, hr + 1, 2):
        #             c = Vector3(*center) + (x, y, z)
        #             self.occ[tuple(c)] = OctoCell(is_dummy=True)

    def render(self, config):
        mesh_data = [

            cell.render(config, center).data
            for center, cells in self.occ.items()
            for cell in cells
            if not cell.is_dummy]

        # print(mesh_data)

        # for center, cell in self.occ.items():
        #     print(center, cell.is_dummy)

        # for center, cell in grid.occ.items():
        #     center = np.array(center) * (config.cell_size / 2, config.cell_size / 2, config.cell_size * sqrt22)
        #     meshes.append(
        #         self.neo_trimmed_octo(cell, config.cell_size, config.overlap, config.slit, center))

        return mesh.Mesh(np.concatenate(mesh_data))

    def crop(self, x_min=-math.inf, x_max=math.inf, y_min=-math.inf, y_max=math.inf, z_min=-math.inf, z_max=math.inf):



        to_remove = set()
        for center, cells in self.occ.items():
            for cell in cells:
                x, y, z = center
                if center[2] == z_min:
                    cell.crops.add(Crop.BOTTOM)
                if center[2] < z_min:
                    to_remove.add(center)

                if center[2] == z_max:
                    cell.crops.add(Crop.TOP)
                if center[2] > z_max:
                    to_remove.add(center)
                #
                if x == x_min:
                    cell.crops.add(Crop.WEST)
                elif x < x_min:
                    to_remove.add(center)

                if x == x_max:
                    cell.crops.add(Crop.EAST)
                elif x > x_max:
                    to_remove.add(center)

                if y == y_min:
                    cell.crops.add(Crop.SOUTH)
                elif y < y_min:
                    to_remove.add(center)

                if y == y_max:
                    cell.crops.add(Crop.NORTH)
                elif y > y_max:
                    to_remove.add(center)

            # if center[2] == z_min:
            #     cell.crops.add(Crop.TOP)
            # if center[2] < z_min:
            #     to_remove.append(center)
            #
            # if center[2] == z_min:
            #     cell.crops.add(Crop.TOP)
            # if center[2] < z_min:
            #     to_remove.append(center)
            #
            # if center[2] == z_min:
            #     cell.crops.add(Crop.TOP)
            # if center[2] < z_min:
            #     to_remove.append(center)

        for center in to_remove:
            self.occ.pop(center)

        return self

    def compute_trimming(self):
        for center, cells in self.occ.items():
            for cell in cells:

                vc = Vector3(*center)

                spacing = p2(cell.cell_scale)

                if tuple(vc + NE * spacing) in self.occ:
                    cell.trims.add(Trim.NE)
                if tuple(vc + NW * spacing) in self.occ:
                    cell.trims.add(Trim.NW)
                if tuple(vc + SW * spacing) in self.occ:
                    cell.trims.add(Trim.SW)
                if tuple(vc + SE * spacing) in self.occ:
                    cell.trims.add(Trim.SE)

                # TODO: needs the rest of these
                attic = (tuple(vc + E + Z) in self.occ , # and Crop.TOP not in self.occ[tuple(vc + E + Z)].crops,
                         tuple(vc + N + Z) in self.occ,
                         tuple(vc + W + Z) in self.occ,
                         tuple(vc + S + Z) in self.occ,
                         )

                basement = (tuple(vc + X + Y - Z) in self.occ,
                            tuple(vc + X - Y - Z) in self.occ,
                            tuple(vc - X + Y - Z) in self.occ,
                            tuple(vc - X - Y - Z) in self.occ,
                            )

                cell.weld_up = all(attic)

                cell.point_down = False
                cell.point_up = False

            # cell.point_up = not any(attic) or tuple(vc + 2 * Z) in self.occ

    def carve(self, x_min, x_max, y_min, y_max, z_min, z_max):
        to_purge = set()
        for x, y, z in self.occ:
            if x_min <= x <= x_max and y_min <= y <= y_max and z_min <= z <= z_max:
                to_purge.add((x, y, z))

        for tup in to_purge:
            self.occ[tup].is_solid = True

    # TODO
    def four_way(self):
        to_add = dict()

        for center, cell in self.occ.items():
            # print("old", x, y, z)
            x, y, z = center

            # to_add[(x, y, z)] = copy(cell)
            to_add[(y, x, z)] = copy(cell)
            to_add[(-x, y, z)] = copy(cell)
            to_add[(y, -x, z)] = copy(cell)

            # to_add[(y, x, z)] = cell

            # new_center = (z + 2 + y, z + x + 2 * y, round(-x / 2 + -y / 2))
            # print("new", new_center)

            # to_add.add(new_center)
            # to_add.add((x, y, -z))

        for center in to_add:
            if center not in self.occ:
                self.occ[center] = OctoCell(False)
        self.occ = {**self.occ, **to_add}

    def six_way(self):
        to_add = dict()

        for center, cell in self.occ.items():
            # print("old", x, y, z)
            x, y, z = center

            # to_add[(x, y, z)] = copy(cell)
            to_add[(x, z, y)] = copy(cell)
            to_add[(z, y, x)] = copy(cell)
            # to_add[(y, z, x)] = copy(cell)
            # to_add[(z, x, y)] = copy(cell)
            # to_add[(z, y, x)] = copy(cell)
            # to_add[(y, x, z)] = cell

            # new_center = (z + 2 + y, z + x + 2 * y, round(-x / 2 + -y / 2))
            # print("new", new_center)

            # to_add.add(new_center)
            # to_add.add((x, y, -z))

        for center in to_add:
            if center not in self.occ:
                self.occ[center] = OctoCell(False)
        self.occ = {**self.occ, **to_add}
        self.four_way()
