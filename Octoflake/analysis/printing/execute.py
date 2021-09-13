from OctoConfig import OctoConfig
from OctoGrid import OctoGrid
from StlRenderer import StlRenderer
from OctoBuilder import OctoBuilder

from stl import Mode

TEST_FILE_NAME = "/Users/silver/Desktop/derp.stl"

# config15 = OctoConfig(
#     nozzle=0.4,
#     nozzle_width_multiplier=1.5,
#     line_layer_ratio=2,
#     first_layer_multiplier=0.5)
#
# config1 = OctoConfig(
#     nozzle=0.4,
#     nozzle_width_multiplier=1,
#     line_layer_ratio=2,
#     first_layer_multiplier=1.5)
#
# config2 = OctoConfig(
#     nozzle=0.4,
#     nozzle_width_multiplier=7/4,
#     line_layer_ratio=2,
#     first_layer_multiplier=0.5)


config25 = OctoConfig(
    nozzle=0.25,
    nozzle_width_multiplier=.35/.25,
    line_layer_ratio=2,
    first_layer_multiplier=0.5)


config = config25
# config = config15

grid = OctoGrid()

iteration = 4

OctoBuilder.stalag(grid, iteration)
# grid.make_flake(iteration)
# grid.make_flake(iteration - 1, center=(0, 0, 2 ** (iteration)))
# grid.make_flake(iteration - 2, center=(0, 0, 2 ** (iteration) +2 ** (iteration-1) ))

# grid.stellate(iteration-1, offset=2 ** iteration)


grid.compute_trimming()
grid.crop(z_min=0)

grid.compute_trimming()

print(len(grid.occ.items()))

renderer = StlRenderer()

# flake = renderer.render(grid, cell_size, overlap, slit,pyramid_floor= 0)

for layers in range(5, 6):
    iteration = 5
    filename = f"/Users/silver/Desktop/derp_{layers=}_{iteration=}.stl"
    config.layers_per_cell = layers
    config.derive()

    flake = renderer.render_with_config(grid, config)
    flake.save(filename, mode=Mode.BINARY)

# levels = 4
# filename = f"/Users/silver/Desktop/derp_{levels}.stl"
# config.layers_per_cell = levels
#
#
# flake = renderer.render_with_config(grid, config)
# flake.save(filename, mode=Mode.BINARY)
