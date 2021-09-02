from OctoConfig import OctoConfig
from OctoGrid import OctoGrid
from StlRenderer import StlRenderer

from stl import Mode

TEST_FILE_NAME = "/Users/silver/Desktop/derp.stl"

config = OctoConfig(
    nozzle=0.4,
    nozzle_width_multiplier=1.5,
    line_layer_ratio=2,
    first_layer_multiplier=0.5)

print(config)

grid = OctoGrid()

iteration = 3

# tower(grid, iteration)
grid.make_flake(iteration)
grid.make_flake(iteration - 1, center=(0, 0, 2 ** (iteration)))

# grid.stellate(iteration-1, offset=2 ** iteration)


grid.compute_trimming()
grid.crop(z_min=2 ** (iteration - 1))

grid.compute_trimming()

print(len(grid.occ.items()))

renderer = StlRenderer()

# flake = renderer.render(grid, cell_size, overlap, slit,pyramid_floor= 0)

for levels in range(5, 10):
    filename = f"/Users/silver/Desktop/derp_{levels}.stl"
    config.layers_per_cell = levels
    config.derive()

    flake = renderer.render_with_config(grid, config)
    flake.save(filename, mode=Mode.BINARY)
