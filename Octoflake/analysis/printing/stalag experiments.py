from printing.octo import OctoConfigs
from printing.octo.OctoGrid import OctoGrid
from printing.octo.builder.OctoBuilder import OctoBuilder
from printing.rendering import RenderUtils

TEST_FILE_NAME = "/Users/silver/Desktop/derp.stl"

################### # Set up the grid and populate it

grid = OctoGrid()

iteration = 4


OctoBuilder.stalag(grid, iteration)


config = OctoConfigs.config_8_thin

RenderUtils.basic_render(grid, config, f"derp.stl")

config.print_settings()



# def quad_tower(grid, i, contact=-2):
#     # grid.make_flake(i, z=2 ** i - 2 ** (i + contact))
#     # z = 2 ** i - 2 ** (i + contact) + 2 ** (i-2)
#     # s = 2 ** (i-1) +2 ** (i-2)
#     # OctoBuilder.tower(grid, i-1, (s, s, z))
#     # OctoBuilder.tower(grid, i-1, (s, -s, z))
#     # OctoBuilder.tower(grid, i-1, (-s, s, z))
#     # OctoBuilder.tower(grid, i-1, (-s, -s, z))
#
#     cz = p2(i) - p2(i, contact)
#     grid.make_flake(i, z=cz)
#
#     sz = cz + p2(i)
#     s = p2(i)
#
#     tz = sz + p2(i)  # - p2(i-1)
#
#     si = i - 1
#
#     # OctoBuilder.tower(grid, si, (0, 0, z + p2(i, -1)), full_evil=True, thin_evil=False)
#     grid.make_flake(i, s, s, sz)
#     grid.make_flake(i, s, -s, sz)
#     grid.make_flake(i, -s, s, sz)
#     grid.make_flake(i, -s, -s, sz)
#
#     OctoBuilder.tower(grid, i, (s, s, tz), full_evil=True)
#     OctoBuilder.tower(grid, i, (s, -s, tz), full_evil=True)
#     OctoBuilder.tower(grid, i, (-s, s, tz), full_evil=True)
#     OctoBuilder.tower(grid, i, (-s, -s, tz), full_evil=True)


# quad_tower(grid, iteration, contact=-1)




# OctoBuilder.tower(grid, iteration, center=(0, 0, 2 ** iteration - 2 ** (iteration - 2)), full_evil=True)
# OctoBuilder.stalag(grid, iteration)
# grid.make_flake(iteration)
# grid.make_flake(iteration - 1, center=(0, 0, 2 ** (iteration)))
# grid.make_flake(iteration - 2, center=(0, 0, 2 ** (iteration) +2 ** (iteration-1) ))
#
# grid.make_flake(iteration)
# OctoBuilder.stellate(grid, iteration-1, offset=2 ** iteration)


################## # Do the post-processing of the grid




# grid.compute_trimming()
# grid.crop(z_min=0)

# grid.compute_trimming()

# print(len(grid.occ.items()))
#
################### # Set up the rendering config
