import numpy as np
from euclid3 import *

from printing.octo.OctoCell import OctoCell, Trim, Crop
from printing.octo.OctoUtil import X, Y, Z, Y2, X2, p2


class OctoGrid:
    """This class only knows how to generate primitive octoflakes."""

    def __init__(self):
        self.occ = dict()
        self.welding = dict()
        pass

    def merge(self, other):
        self.occ = {**self.occ, **other.occ}
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
            hr = r - abs(z) -1
            for x in range(-hr, hr + 1, 2):
                for y in range(-hr, hr + 1, 2):
                    c = Vector3(*center) + (s * x, s * y, s * z)

                    self.make_flake(f_i, center=c)


    def make_flake(self, iteration, x=0, y=0, z=0, center=None):
        center = center if center is not None else Vector3(x, y, z)
        x, y, z = center
        if iteration == 0:
            if tuple(center) not in self.occ:
                center_tup = tuple(center)
                # forprint(center_tup)
                # if not all(map(lambda q: q == int(q), center_tup)):
                #     print("Wtffff", center_tup)

                self.occ[tuple(center)] = OctoCell()
            return

        i1 = iteration - 1
        o = 2 ** i1

        if tuple(center) not in self.welding:
            self.welding[tuple(center)] = True

        self.make_flake(i1, center=center + Vector3(o, o, 0))
        self.make_flake(i1, center=center + Vector3(o, -o, 0))
        self.make_flake(i1, center=center + Vector3(-o, o, 0))
        self.make_flake(i1, center=center + Vector3(-o, -o, 0))
        self.make_flake(i1, center=center + Vector3(0, 0, o))
        self.make_flake(i1, center=center + Vector3(0, 0, -o))

    def crop(self, x_min=None, x_max=None, y_min=None, y_max=None, z_min=None, z_max=None):

        to_remove = []
        for center, cell in self.occ.items():
            if center[2] == z_min:
                cell.is_pyramid = True
                cell.crops.add(Crop.UP)
            if center[2] < z_min:
                to_remove.append(center)

        for center in to_remove:
            self.occ.pop(center)

        weld_to_remove = []
        for center in self.welding:
            if center[2] == z_min:
                self.welding[center] = True
            if center[2] < z_min:
                weld_to_remove.append(center)

        for center in weld_to_remove:
            self.welding.pop(center)

    def compute_trimming(self):
        for center, cell in self.occ.items():

            vc = Vector3(*center)

            if tuple(vc + X2) in self.occ:
                cell.trims.add(Trim.RIGHT)
            if tuple(vc - X2) in self.occ:
                cell.trims.add(Trim.LEFT)
            if tuple(vc + Y2) in self.occ:
                cell.trims.add(Trim.BACK)
            if tuple(vc - Y2) in self.occ:
                cell.trims.add(Trim.FRONT)

            attic = (tuple(vc + X + Y + Z) in self.occ,
                     tuple(vc + X - Y + Z) in self.occ,
                     tuple(vc - X + Y + Z) in self.occ,
                     tuple(vc - X - Y + Z) in self.occ,
                     )

            basement = (tuple(vc + X + Y - Z) in self.occ,
                        tuple(vc + X - Y - Z) in self.occ,
                        tuple(vc - X + Y - Z) in self.occ,
                        tuple(vc - X - Y - Z) in self.occ,
                        )

            cell.weld_up = all(attic)
            # cell.weld_down = all(basement) or True
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
        to_add = set()
        for x, y, z in self.occ:
            # print("old", x, y, z)
            # new_center = (x, y, z)
            # new_center = (x, y, z)
            # new_center = (x, y, z)
            # print("new", new_center)

            to_add.add((-x, y, z))
            to_add.add((x, -y, z))
            to_add.add((-x, -y, z))
        for center in to_add:
            if center not in self.occ:
                self.occ[center] = OctoCell(False)

    def six_way(self):
        to_add = set()
        for x, y, z in self.occ:
            print("old", x, y, z)

            new_center = (z + 2 + y, z + x + 2 * y, round(-x / 2 + -y / 2))
            print("new", new_center)

            to_add.add(new_center)
            to_add.add((x, y, -z))
        for center in to_add:
            if center not in self.occ:
                self.occ[center] = OctoCell(False)

        self.four_way()
