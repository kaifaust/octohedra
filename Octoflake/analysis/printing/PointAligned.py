# from printing.octo.builder.OctoFlake import OctoFlakeBuilder
import functools
import random
from pathlib import Path

from euclid3 import Vector3

from printing.octo import OctoConfigs
from printing.octo.OctoCell import Crop
from printing.octo.OctoGrid import OctoGrid
from printing.octo.OctoUtil import p2, E, N, W, S, UP, DOWN
from printing.octo.builder.OldOctoBuilder import OldOctoBuilder

builder = OldOctoBuilder()

# builder.make_flake(2)

# grid = builder.materialize()


grid = OctoGrid()


# i = 4
# grid.make_flake(i, cell_scale=i-2)
# grid.make_flake(i-1, Vector3(0, 0, p2(i)), cell_scale=i-3)
# grid.make_flake(i-2, Vector3(0, 0, p2(i)+p2(i-1)))

# i = 4
# grid.make_flake(i, cell_scale=0, overwrite=True)
# grid.make_flake(i-1, Vector3(0, 0, p2(i)), cell_scale=1, overwrite=True)
# grid.make_flake(i-2, Vector3(0, 0, p2(i)+p2(i-1)), cell_scale=2, overwrite=True)


# grid.make_flake(5)


# def random_scale_flake(grid, iteration, center=None):
#     center = center if center is not None else Vector3(0, 0, 0)
#
#     # if iteration == 0:
#     #     self.insert_cell(center, cell_scale=0, is_subcell=cell_scale>0)
#     #     return
#     if iteration == 0 or random.randint(1, 6) == 1:
#         # print("Inserting real cell at", center)
#         grid.insert_cell(center, cell_scale=iteration, overwrite=True)
#         return
#     else:
#         # print("inserting dummy at", center)
#         grid.insert_cell(center, iteration, is_dummy=True)
#
#     i1 = iteration - 1
#     o = p2(i1)
#
#     for direction in (E, N, W, S, UP, DOWN):
#         random_scale_flake(grid, i1, center=center + o * direction)
#
#
# def save_rand_flake(i, name=None):
#     name = f"derp_{random.randint(0, 100)}" if name is None else name
#     grid = OctoGrid()
#     random_scale_flake(grid, 3)
#     grid.compute_trimming()
#     grid.crop(z_min=0)
#
#     config = OctoConfigs.config_25
#     config.absolute_layers_per_cell = 10
#     config.derive()
#
#     grid.render(config).save(Path.home() / "Desktop"/f"{name}.stl")
#
#
# for n in range(10):
#     save_rand_flake(3, f"derp_{n}")


def multi_scale_tower(base_i, base_scale):
    z = 0
    for i in range(base_i, 0, -1):
        grid.make_flake(i, Vector3(0, 0, z), cell_scale=max(0, base_scale - (base_i - i)), overwrite=True)

        z += p2(i)


def face_flake(i, center=None, scale_ne=0, scale_nw=0, scale_sw=0, scale_se=0):
    ne_grid = OctoGrid()
    ne_grid.make_flake(i, center, scale_ne)
    ne_grid.crop(x_min=0, y_min=0)
    print(ne_grid.occ.keys())

    nw_grid = OctoGrid()
    nw_grid.make_flake(i, center, scale_nw)
    nw_grid.crop(x_max=0, y_min=0)
    print(nw_grid.occ.keys())

    sw_grid = OctoGrid()
    sw_grid.make_flake(i, center, scale_sw)
    sw_grid.crop(x_max=0, y_max=0)
    print(ne_grid.occ.keys())

    se_grid = OctoGrid()
    se_grid.make_flake(i, center, scale_se)
    se_grid.crop(x_min=0, y_max=0)
    print(se_grid.occ.keys())

    # sw_grid = OctoGrid().make_flake(i, center, scale_sw)
    # [tuple(center)].crops.update({Crop.SOUTH, Crop.WEST})

    # se_grid = OctoGrid().make_flake(i, center, scale_se)
    # ne_grid[tuple(center)].crops.update({Crop.SOUTH, Crop.WEST})

    return [ne_grid, nw_grid, sw_grid, se_grid]



# i = 1
# center = Vector3(0, 0, 0)
# scale_ne = 1
# scale_nw = 0
#
# ne_grid = OctoGrid()
# ne_grid.make_flake(i, center, scale_ne)
# ne_grid.crop(x_min=0, y_min=0)
# print(ne_grid.occ)
#
# nw_grid = OctoGrid()
# nw_grid.make_flake(i, center, scale_nw)
# nw_grid.crop(x_max=0, y_min=0)
# print(nw_grid.occ)
#
#
# grid = ne_grid.merge(nw_grid)
#
# for center, cells in grid.occ.items():
#     print(center, cells)
#
#
# exit()


#
#
# center = center if center is not None else Vector3(0, 0, 0)
#
# i1 = i - 1
# o = p2(i1)
#
# if i == -1:
#     return
#
# if i == 0:
#     grid.insert_cell(center)
#
# if i == scale_ne:
#     grid.insert_cell(center, i)
#     grid.occ[tuple(center)].crops.update({Crop.WEST, Crop.SOUTH})
#     # face_flake()
#
#
#
#
# for direction in (E, N, W, S, UP, DOWN):
#     face_flake(grid, i1, center + o * direction, scale_ne, scale_nw, scale_sw, scale_se)


# def gradient_flake(i, top_i):


# def face_flake(i, )

i = 5

# grid.make_flake(i)

grids = face_flake(i, scale_ne=3, scale_nw=2, scale_sw=1, scale_se=0)


grid = functools.reduce(OctoGrid.merge, grids)
grid.crop(z_min=0)

config = OctoConfigs.config_25
# config = OctoConfigs.render_testing
config.absolute_layers_per_cell = 16
config.derive()


grid.compute_trimming()
mesh = grid.render(config)

mesh.save(Path.home() / "Desktop" / f"derp.stl")

# grid.insert_cell(center=Vector3(0, 0, 0), cell_scale=i, overwrite=True)
# grid.occ[(0, 0, 0)].crops.update({Crop.EAST, Crop.BOTTOM})

# multi_scale_tower(4, 3)
#

# random_scale_flake(grid, 3)

# grid.six_way()
# grid.make_flake(1)

# print(grid.occ)




# config = OctoConfigs.render_testing
# config.print_settings()
# config.print_derived_values()
