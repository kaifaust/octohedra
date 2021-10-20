from stl import Mode

from printing.builders.HollowOctoBuilder import HollowOldOctoBuilder
from printing.builders.OldOctoBuilder import OldOctoBuilder
from printing.grid.OctoGrid import OctoGrid
from printing.grid.OctoCell import Trim
from printing.utils.OctoUtil import p2
from printing.utils import OctoConfigs, RenderUtils

TEST_FILE = f"/Users/silver/Desktop/hollow.stl"

grid = OctoGrid()

# grid.occ[(-1, -1, 0)] = OctoCell()
# grid.occ[(1, 1, 0)] = OctoCell()
# grid.occ[(0, 0, 1)] = OctoCell()
# renderer = StlRenderer()
# config = OctoConfig(10, 3, 1)
# mesh = renderer.render(grid, config)
# mesh.save(f"/Users/silver/Desktop/hollow.stl")
# exit()

# print(renderer.welding_cube(1))


# renderer = StlRenderer()
#
# cell = OctoCell(
#     is_pyramid=False,
#     is_solid=False,
#     trims={Trim.FRONT, Trim.LEFT},
#     weld_up=True,
#     weld_down=True,
#     point_up=False,
#     point_down=False
# )
#
# mesh = renderer.neo_trimmed_octo(cell, 100, 10, 1)
# mesh.save(TEST_FILE)
# exit()

i = 4

# def hollow(i, center=None):


c = (0, 0, p2(i, -1) - p2(i, -2))


def filled_flake(i, center):
    grid.make_flake(i, center=center)
    OldOctoBuilder.fill(grid, i, center)


i1 = i - 1
o = p2(i1)
center = c
# filled_flake(i, c)
# filled_flake(i1, center=center + Vector3(o, o, 0))
# filled_flake(i1, center=center + Vector3(o, -o, 0))
# filled_flake(i1, center=center + Vector3(-o, o, 0))
# filled_flake(i1, center=center + Vector3(-o, -o, 0))
# filled_flake(i1, center=center + Vector3(0, 0, o))
# filled_flake(i1, center=center + Vector3(0, 0, -o))




# grid.fill(2, 10)




# builder = HollowOctoBuilder()

# builder.hollow_flake(i, c)
# builder.simple_tower(i)

# builder.materialize(grid)


# flake = HollowFlake(3, c, 1)
# RenderUtils.basic_render(HollowFlake(3, c, 0).materialize(), config_8, filename="30.stl")
# RenderUtils.basic_render(HollowFlake(3, c, 1).materialize(), config_8, filename="31.stl")
# RenderUtils.basic_render(HollowFlake(3, c, 2).materialize(), config_8, filename="32.stl")
# RenderUtils.basic_render(grid, config_8)
# RenderUtils.basic_render(grid, config_8)
# grid = flake.materialize()



builder = HollowOldOctoBuilder()

# builder.hollow_flake(4, c, 1)

# builder.simple_tower(5, 2, center= (0, 0, 0))

builder.default_thickness = 0
# builder.stellate(3)
i = 6
builder.evil_towerz(i, center=(0, 0, p2(i-2)))


# for c, flake in builder.flakes.items():
#     print(c, flake)

grid = builder.materialize()



# grid.keep_octo(p2(i), center=c)
# grid.clear_octo(p2(i-1) +  p2(i, -2), center=c)

print(len(grid.occ))

c = int(p2(i, -2) - 1)
print(c)

# for x in range(-c, c + 1):
#     for y in range(-c, c + 1):
#         for z in range(0, p2(i) + p2(i, -1)):
#             center = (x, y, z)
#             rect = z < p2(i) - p2(i, -1)
#             tri = abs(x) + abs(y) + (z - p2(i) + c + 3) < c
#             # if (rect or tri):
#             #     grid.occ[center] = OctoCell()
#             if center in grid.occ and (rect or tri):
#                 grid.occ.pop(center)


config = OctoConfigs.config_transparent_04
config.absolute_layers_per_cell = 5
config.derive()
RenderUtils.render_grid(grid, config, f"derp.stl")



# for layers in range(3, 7):
#     config.absolute_layers_per_cell = layers
#     config.derive()
#     RenderUtils.basic_render(grid, config, f"derp_{layers}.stl")


config.print_settings()
config.print_derived_values()


exit()

grid.crop(z_min=0)  # - 2 ** (i-1))

# grid.occ.pop((1, 1, 0))
# grid.occ.pop((1, -1, 0))
# grid.occ.pop((-1, 1, 0))
# grid.occ.pop((-1, -1, 0))
# grid.occ.pop((0, 0, 1))
# grid.occ.pop((0, 0, -1))

grid.compute_trimming()

# grid.carve(-2, 2, -2, 2, -100, 4)


# print(grid.occ)

for center, cell in grid.occ.items():
    x, y, z = center

    if cell.weld_down:
        print(x, y, z, cell)

#


# to_kill = list(filter(lambda x: x[2] < 1, grid.occ.keys()))
#
# # print(to_kill)
# #
# for key in to_kill:
#     grid.occ.pop(key)
#
#
# # grid.occ.pop((0, 0, 3))
#
# print(grid.occ.keys())
#
# for key in [(2, 2, 1), (2, -2, 1), (-2, 2, 1), (-2, -2, 1)]:
#     grid.occ.pop(key)



flake.save(TEST_FILE, mode=Mode.BINARY)
#


trims = {
    Trim.FRONT,
    Trim.BACK,
    Trim.LEFT,
    Trim.RIGHT
}
