from euclid3 import *
from enum import Enum
import math
import numpy as np

sqrt2 = math.sqrt(2)
sqrt22 = sqrt2 / 2

tup = (1, 2, 3)

vec = Vector3(*tup)
vec2 = Vector2(1, 2)
btup = tuple(vec)
# print(vec + vec2)
print(btup)

X2 = Vector3(2, 0, 0)
Y2 = Vector3(0, 2, 0)


class OctoGrid:

    def __init__(self):
        self.occ = dict()
        self.welding = dict()
        pass

    def clear(self, iteration, center = (0,0,0)):

        r = 2 ** (iteration-1)
        # print(r)
        to_remove = []
        for x in range(-r, r + 1):
            for y in range(-r, r + 1):
                for z in range(-r, r + 1):
                    if abs(x) + abs(y) + 2 * abs(z) <= r * 2:
                        # print(x, y, z)
                        if z == 1:
                            pass
                            # print((x, y, z, r, x + y + 4 * z))
                        to_remove.append(tuple(np.array(center) + (x, y, z)))

        for remove in to_remove:
            if remove in self.occ:
                self.occ.pop(remove)
            if remove in self.welding:
                self.welding.pop(remove)



    def stellate(self, iteration, center=(0, 0, 0), offset=None):
        offset = 2 ** (iteration) if offset is None else offset
        si = iteration
        self.make_flake(si, (center[0] + offset, center[1] + offset, center[2]))
        self.make_flake(si, (center[0] + offset, center[1] - offset, center[2]))
        self.make_flake(si, (center[0] - offset, center[1] + offset, center[2]))
        self.make_flake(si, (center[0] - offset, center[1] - offset, center[2]))
        self.make_flake(si, (center[0], center[1], center[2] + offset))
        self.make_flake(si, (center[0], center[1], center[2] - offset))

    def fill(self, iteration, center=(0, 0, 0)):
        offset = 2 ** iteration / 4
        i2 = iteration - 2
        self.make_flake(i2, (center[0] + 2 * offset, center[1], center[2] + offset))
        self.make_flake(i2, (center[0] - 2 * offset, center[1], center[2] + offset))
        self.make_flake(i2, (center[0], center[1] + 2 * offset, center[2] + offset))
        self.make_flake(i2, (center[0], center[1] - 2 * offset, center[2] + offset))
        self.make_flake(i2, (center[0] + 2 * offset, center[1], center[2] - offset))
        self.make_flake(i2, (center[0] - 2 * offset, center[1], center[2] - offset))
        self.make_flake(i2, (center[0], center[1] + 2 * offset, center[2] - offset))
        self.make_flake(i2, (center[0], center[1] - 2 * offset, center[2] - offset))

    def faces(self, iteration, starting_iteration = 1000, ending_iteration=0, tetra_left=False, tetra_right=True, center=(0, 0, 0)):

        center = np.array(center)

        offset = 2 ** iteration
        si = starting_iteration
        ei = ending_iteration
        if iteration <= starting_iteration:
            self.make_flake(iteration, center)

        if iteration > ending_iteration:

            if tetra_right: self.faces(iteration-1, si, ei, False, True, center + (offset, 0, offset/2))
            if tetra_right: self.faces(iteration-1, si, ei, False, True, center + (-offset, 0, offset/2))
            if tetra_left: self.faces(iteration-1, si, ei, True, False, center + (0, offset, offset/2))
            if tetra_left: self.faces(iteration-1, si, ei, True, False, center + (0, -offset, offset/2))
            if tetra_left: self.faces(iteration-1, si, ei, True, False, center + (offset, 0, -offset/2))
            if tetra_left: self.faces(iteration-1, si, ei, True, False, center + (-offset, 0, -offset/2))
            if tetra_right: self.faces(iteration-1, si, ei, False, True, center + (0, offset, -offset/2))
            if tetra_right: self.faces(iteration-1, si, ei, False, True, center + (0, -offset, -offset/2))


    def make_flake(self, iteration, center=Vector3(0, 0, 0), is_pyramid=False, top_level = True):
        if iteration == 0:
            if tuple(center) not in self.occ:
                center_tup = tuple(center)
                if not all(map(lambda x: x == int(x), center_tup)):
                    print("Wtffff", center_tup)

                self.occ[tuple(center)] = OctoCell(is_pyramid)
            return

        i1 = iteration - 1
        o = 2 ** i1

        if tuple(center) not in self.welding:
            self.welding[tuple(center)] = is_pyramid

        self.make_flake(i1, center + Vector3(o, o, 0), is_pyramid, False)
        self.make_flake(i1, center + Vector3(o, -o, 0), is_pyramid, False)
        self.make_flake(i1, center + Vector3(-o, o, 0), is_pyramid, False)
        self.make_flake(i1, center + Vector3(-o, -o, 0), is_pyramid, False)
        self.make_flake(i1, center + Vector3(0, 0, o), is_pyramid=False, top_level=False)
        if not is_pyramid:
            self.make_flake(i1, center + Vector3(0, 0, -o), is_pyramid=False, top_level=False)

        if top_level and False:
            self.clear(iteration, center)

    def make_pyramid(self, iteration, center):
        self.make_flake(iteration, center, is_pyramid=True)

    def crop(self, x_min=None, x_max=None, y_min=None, y_max=None, z_min=None, z_max=None):

        to_remove = []
        for center, cell in self.occ.items():
            if center[2] == z_min:
                cell.is_pyramid = True
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
            if tuple(Vector3(*center) + X2) in self.occ:
                cell.trims.add(Trim.RIGHT)
            if tuple(Vector3(*center) - X2) in self.occ:
                cell.trims.add(Trim.LEFT)
            if tuple(Vector3(*center) + Y2) in self.occ:
                cell.trims.add(Trim.BACK)
            if tuple(Vector3(*center) - Y2) in self.occ:
                cell.trims.add(Trim.FRONT)

            if tuple(Vector3(*center) + X2 + Y2) in self.occ:
                if (tuple(Vector3(*center) + X2) in self.occ) != (tuple(Vector3(*center) + Y2) in self.occ):
                    cell.trims.add(Trim.BACK_RIGHT)
            if tuple(Vector3(*center) + X2 - Y2) in self.occ:
                if (tuple(Vector3(*center) + X2) in self.occ) != (tuple(Vector3(*center) - Y2) in self.occ):
                    cell.trims.add(Trim.FRONT_RIGHT)
            if tuple(Vector3(*center) - X2 + Y2) in self.occ:
                if (tuple(Vector3(*center) - X2) in self.occ) != (tuple(Vector3(*center) + Y2) in self.occ):
                    cell.trims.add(Trim.BACK_LEFT)
            if tuple(Vector3(*center) - X2 - Y2) in self.occ:
                if (tuple(Vector3(*center) - X2) in self.occ) != (tuple(Vector3(*center) - Y2) in self.occ):
                    cell.trims.add(Trim.FRONT_LEFT)

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




            new_center = ( z + 2 + y, z + x + 2*y , round(-x/2 + -y/2))
            print("new", new_center)

            to_add.add(new_center)
            to_add.add((x, y, -z))
        for center in to_add:
            if center not in self.occ:
                self.occ[center] = OctoCell(False)

        self.four_way()

    # def render_to_scad(self, cell_iteration, cell_size, overlap, slit):
    #     out = ["use <octomodules.scad>"]
    #     self.compute_trimming()
    #
    #     for center in sorted(self.occ, key=lambda x: x[2]):
    #         cell = self.occ[center]
    #         center_str = f"[{center[0] / 2 * cell_size}, {center[1] / 2 * cell_size}, {center[2] * cell_size * sqrt22}]"
    #         out.append(f"translate({center_str}) {cell.render_scad(cell_iteration, cell_size, overlap, slit)}")
    #         out.append(f"translate({center_str}) {cell.render_scad(cell_iteration, cell_size, overlap, slit)}")
    #
    #     for center, is_pyramid in self.welding.items():
    #         center_str = f"[{center[0] / 2 * cell_size}, {center[1] / 2 * cell_size}, {center[2] * cell_size * sqrt22}]"
    #         welding_size = round(4 * overlap + slit, 10)
    #         cube_str = f"translate({center_str}) "
    #         cube_str += f"translate([0, 0, {welding_size / 2}]) " if is_pyramid else "translate([0, 0, 0]) "
    #         cube_str += f"cube([{welding_size}, {welding_size}, {welding_size}], center=true);"
    #         out.append(cube_str)
    #
    #
    #     return "\n".join(out)
    #
    # def render_to_stl(self):
    #     pass


class Trim(Enum):
    TOP = 1  # Unused
    BOTTOM = 2
    FRONT = 3
    BACK = 4
    LEFT = 5
    RIGHT = 6

    FRONT_LEFT = 7
    FRONT_RIGHT = 8
    BACK_LEFT = 9
    BACK_RIGHT = 10


class OctoCell:

    def __init__(self, is_pyramid=False):
        self.is_pyramid = is_pyramid
        self.trims = set()

    def render_scad(self, iteration, size, overlap, slit):
        rounding = 10
        size = round(size + 2 * overlap, rounding)
        trim = round(overlap + slit / 2, rounding)
        overlap = round(overlap, rounding)
        slit = round(slit, rounding)

        trim_front = trim if Trim.FRONT in self.trims else 0
        trim_back = trim if Trim.BACK in self.trims else 0
        trim_left = trim if Trim.LEFT in self.trims else 0
        trim_right = trim if Trim.RIGHT in self.trims else 0
        trim_bottom = round(sqrt2 * overlap, rounding)

        kern_front_left = trim if Trim.FRONT_LEFT in self.trims else 0
        kern_front_right = trim if Trim.FRONT_RIGHT in self.trims else 0
        kern_back_left = trim if Trim.BACK_LEFT in self.trims else 0
        kern_back_right = trim if Trim.BACK_RIGHT in self.trims else 0

        is_pyramid = str(self.is_pyramid).lower()

        return f"octahedron({iteration=}, {size=}, {overlap=}, {slit=},\n" \
               f"    {trim_front=}, {trim_back=}, {trim_left=}, {trim_right=}, {trim_bottom=},\n" + \
               f"    {kern_front_left=}, {kern_front_right=}, {kern_back_left=}, {kern_back_right=}, {is_pyramid=!s});"
        # return f"octahedron({iteration=}, {size=});"#, {size=}, {overlap=}, {slit=},{is_pyramid=!s});\n" \
        #        # f"    {trim_front=}, {trim_back=}, {trim_left=}, {trim_right=}, {trim_bottom=},\n" + \
        #        # f"    {kern_front_left=}, {kern_front_right=}, {kern_back_left=}, {kern_back_right=}, {is_pyramid=!s});"

    def __str__(self):
        return f"Octahedron({self.trims})"

    def __repr__(self):
        return self.__str__()


def tower(grid, iteration, center=(0, 0, 0)):
    z = center[2]
    for i in range(iteration, 0, -1):
        print(i)
        grid.make_flake(i, (center[0], center[1], center[2] + z))
        z += 2 ** i


def tower_complex(grid, iteration, center=(0, 0, 0)):
    if iteration < 3:
        return
    tower(grid, iteration, center)
    tower_complex(grid, iteration - 1, (center[0] + 2 ** iteration, center[1] + 2 ** iteration, center[2]))
    tower_complex(grid, iteration - 1, (center[0] + 2 ** iteration, center[1] - 2 ** iteration, center[2]))
    tower_complex(grid, iteration - 1, (center[0] - 2 ** iteration, center[1] + 2 ** iteration, center[2]))
    tower_complex(grid, iteration - 1, (center[0] - 2 ** iteration, center[1] - 2 ** iteration, center[2]))


# grid = OctoGrid()
#
# iteration = 5
# cell_iteration = 0
# spacing = 1.5 * (2 ** cell_iteration)
# slit = .1
# overlap = 0.3 * sqrt22 * sqrt22 + .001
# grid.make_flake(iteration, (0, 0, 0))
# # grid.stellate(iteration-2, offset=2 ** iteration)
#
# # tower_complex(grid, 4)
# grid.crop(z_min=0)


# ################################################ Robin's lamp
# taper = 2 ** (iteration-2)
# cyl_top = (2/4 * 2 ** (iteration) - taper) * sqrt22 * spacing
# cyl_bot = ( 3/4*  2 ** (iteration) - taper) * sqrt22 * spacing
# cyl_radius = (1+ 2 ** (iteration - 3)) * spacing * sqrt2
#
# print(cyl_radius)
#
# rendered += f"\n translate([0, 0, {-cyl_bot}]) cylinder({ cyl_top + cyl_bot}, r= {cyl_radius}, $fn=200 );"
# rendered += f"\ntranslate([0, 0, {cyl_top}]) cylinder({ taper * sqrt22 * spacing}, {cyl_radius}, 0, $fn=200 );"


# rendered = grid.render_to_scad(cell_iteration, spacing, overlap, slit)
#
# with open("render.scad", "w") as render_file:
#     render_file.writelines(rendered)
#
# subprocess.call(["OpenSCAD", "-o", os.path.expanduser("~/Desktop/render_bin.stl"),
#                  "--enable=lazy-union",
#                  "--export-format", "binstl",
#                  "render.scad"])
