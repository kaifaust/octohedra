from copy import copy
from dataclasses import astuple
from functools import wraps

import trimesh
from euclid3 import *
from trimesh import transformations, util

from printing.grid.GridCell import GridCell
from printing.grid.OctoCell import OctoCell
from printing.grid.OctoVector import OctoVector
from printing.grid.TetraCell import TetraCell
from printing.utils import OctoConfigs, RenderUtils
from printing.utils.OctoConfig import RenderConfig

DEFAULT_GRID = "default"


def dispatch(method):
    @wraps(method)
    def wrapper(*args, grids=None, **kwargs):
        self = args[0]
        args = args[1:]
        grids = self.subgrids.keys() if grids is None else grids
        for grid in self.get_grids():
            if grid.name in grids:
                method(self=grid, *args, **kwargs)

    return wrapper


class OctoGrid:
    """
    This class only knows how to generate primitive octoflakes. okay but I wanted to try out
    this wrapping thing
    """

    def __init__(self, name="Body"):
        self.name = name
        self.occ = dict()
        self.subgrids = dict()
        self.cache = dict()

    def add_subgrid(self, name):
        self.subgrids[name] = OctoGrid(name)

    def get_subgrid(self, name):
        return self.subgrids[name]

    def get_grids(self):
        return {self.name: self} | self.subgrids

    def merge(self, other):
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

    def render(self, config=OctoConfigs.default, rotate=True, grid=DEFAULT_GRID):
        render_config = config.derive_render_config()
        cells = [self.render_cell(cell, center, render_config) for center, cell in self.occ.items()]

        if len(cells) > 0:
            cell_meshes = util.concatenate(cells)
        else:
            cell_meshes = trimesh.Trimesh()

        if rotate:
            angle = math.radians(45)
            rot = transformations.rotation_matrix(angle, (0, 0, 1))
            cell_meshes.apply_transform(rot)

        return cell_meshes.process()

    def render_cell(self, cell: GridCell, center: OctoVector, config: RenderConfig):
        if astuple(cell) not in self.cache:
            self.cache[astuple(cell)] = cell.render(config)

        cell_mesh = self.cache[astuple(cell)].copy()

        return cell_mesh.apply_translation(center.as_np() * (config.cell_size / 4))

    # @dispatch
    def insert_cell(self,
                    center: OctoVector = None,
                    x=0,
                    y=0,
                    z=0,
                    strict=False,
                    octo_only=False,
                    tetra_only=False):

        if center is None:
            center = OctoVector(x, y, z)
        # print("Inserting a cell at:", center)
        if strict:
            center.validate()
        else:
            self.occ[center] = OctoCell()

        valid_even_z = (center.x % 4 == 2 and center.y % 4 == 0) \
                       or (center.x % 4 == 0 and center.y % 4 == 2)

        valid_odd_z = (center.x % 4 == 0 and center.y % 4 == 0) \
                      or (center.x % 4 == 2 and center.y % 4 == 2)

        if center.z % 4 == 0 and valid_even_z or center.z % 4 == 2 and valid_odd_z:
            if not tetra_only:
                self.occ[center] = OctoCell()
        elif center.z % 2 == 1 and abs(center.x) % 2 == 1 and abs(center.y) % 2 == 1:
            if not octo_only:
                self.occ[center] = TetraCell()

    # TODO: Move this to an OctoBuilders utility file?
    def fill(self, radius, center, clear=False):

        # print("Radius:", radius)

        points = [center + OctoVector(x, y, z)
                  for x in range(-radius, radius + 1)
                  for y in range(-radius, radius + 1)
                  for z in range(-radius, radius + 1)
                  if abs(x) + abs(y) + abs(z) < radius
                  ]

        for point in points:
            if not clear:
                self.insert_cell(center=point)
            else:
                self.occ.pop(point)

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
            if center.z == z_max:
                cell.crop_top = True
            if center.z > z_max:
                to_remove.add(center)

            if center.x == x_min:
                cell.crop_west = True
            elif center.x < x_min:
                to_remove.add(center)
            #
            if center.x == x_max:
                cell.crop_east = True
            elif center.x > x_max:
                to_remove.add(center)
            #
            if center.y == y_min:
                cell.crop_south = True
            elif center.y < y_min:
                to_remove.add(center)
            #
            if center.y == y_max:
                cell.crop_north = True
            elif center.y > y_max:
                to_remove.add(center)

        for center in to_remove:
            self.occ.pop(center)

        return self

    def compute_trimming(self):
        centers = set(self.occ.keys())
        for center, cell in self.occ.items():
            cell.trim(center, centers)

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

    def __repr__(self):
        return f"OctoGrid({self.name})({str(list(self.occ.keys()))})"

    def __str__(self):
        return "Octogrid " + str(list(self.occ.keys()))


def reflection_test():
    grid = OctoGrid()

    grid.insert_cell(OctoVector(1, 0, 0))
    print(grid)
    grid.four_way()
    print(grid)

    RenderUtils.render_grid(grid, config_25, z_min=None)
    print("Yo")


def decorator_test():
    grid = OctoGrid("Body")
    grid.add_subgrid("Modifier1")
    grid.add_subgrid("Modifier2")

    print(grid.get_grids())
    # grid.insert_cell(x=2)
    # print(grid.get_grids())
    # grid.insert_cell(y=2, grids="Modifier1")
    # print(grid.get_grids())
    # grid.insert_cell(y=-2, grids=("Body", "Modifier2"))
    # print(grid.get_grids())

    # grid.insert_cell(x=2)
    #
    # print(grid.occ)
    # print()


if __name__ == "__main__":
    # tetra_test()
    # reflection_test()
    decorator_test()
