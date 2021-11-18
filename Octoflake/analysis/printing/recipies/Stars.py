from printing.builders.OldOctoBuilder import OldOctoBuilder
from printing.utils import OctoConfigs, RenderUtils
from printing.utils.OctoUtil import p2

# i = 6

# single_builder = OctoBuilder()
# single_builder.make_flake(i, (0, 0, 0))
# single_mesh = single_builder.materialize()
#
# config = OctoConfigs.config_25
# config.absolute_layers_per_cell = 8
# config.derive()
#
# # RenderUtils.basic_render(single_mesh, config, filename=f"{8}_single.stl")
#
# star_builder = OctoBuilder()
# star_builder.stellate(i, (0, 0, 0))
# star_mesh = star_builder.materialize()
#
# # RenderUtils.basic_render(single_mesh, config, filename=f"{8}_single.stl")
#
# tower_builder = OctoTowerBuilder()
# tower_builder.simple_tower(i, (0, 0, p2(i)-p2(i-1)))
# tower_mesh = tower_builder.materialize()
#
# flower_builder = OctoTowerBuilder()
# flower_builder.flower_tower(i, center=(0, 0, p2(i) - p2(i, - 2)), min_evil=3)
# flower_mesh = flower_builder.materialize()
#
# evil_builder = OctoTowerBuilder()
# evil_builder.evil_tower(i, center=(0, 0, p2(i) - p2(i, - 2)), min_evil=3)
# evil_mesh = evil_builder.materialize()
#
#
# config = OctoConfigs.config_25

# RenderUtils.basic_render(builder.materialize(), config)


# for i in range(3, 6):
#     for layers in range(5, 9):
#         config = OctoConfigs.config_25
#         config.absolute_layers_per_cell = layers
#         config.derive()
#
#         single_builder = OctoBuilder()
#         single_builder.make_flake(i, (0, 0, 0))
#         single_mesh = single_builder.materialize()
#
#         # RenderUtils.basic_render(single_mesh, config, filename=f"{8}_single.stl")
#
#         star_builder = OctoBuilder()
#         star_builder.stellate(i, (0, 0, 0))
#         star_mesh = star_builder.materialize()
#
#         # RenderUtils.basic_render(single_mesh, config, filename=f"{8}_single.stl")
#
#         tower_builder = OctoTowerBuilder()
#         tower_builder.simple_tower(i, (0, 0, p2(i)-p2(i-1)))
#         tower_mesh = tower_builder.materialize()
#
#         flower_builder = OctoTowerBuilder()
#         flower_builder.flower_tower(i, center=(0, 0, p2(i) - p2(i, - 2)), min_evil=3)
#         flower_mesh = flower_builder.materialize()
#
#         evil_builder = OctoTowerBuilder()
#         evil_builder.evil_tower(i, center=(0, 0, p2(i) - p2(i, - 2)), min_evil=3)
#         evil_mesh = evil_builder.materialize()
#
#         RenderUtils.basic_render(single_mesh, config, filename=f"{i}_{layers}_single.stl")
#         RenderUtils.basic_render(star_mesh, config, filename=f"{i}_{layers}_star.stl")
#         RenderUtils.basic_render(tower_mesh, config, filename=f"{i}_{layers}_tower.stl")
#         RenderUtils.basic_render(flower_mesh, config, filename=f"{i}_{layers}_flower.stl")
#         RenderUtils.basic_render(evil_mesh, config, filename=f"{i}_{layers}_evil.stl")


base_layers = 4
base_i = 5

for i in range(3, base_i+1):

    star_builder = OldOctoBuilder()
    star_builder.stellate(i, (0, 0, 0))
    star_grid = star_builder.materialize()

    config = OctoConfigs.config_25
    config.absolute_layers_per_cell = base_layers * p2(base_i-i)
    config.derive()

    RenderUtils.render_grid(star_grid, config, base_filename=f"i_{i}_star.stl")

exit()

i = 4

# tower_builder = OctoTowerBuilder()
# tower_builder.simple_tower(i, (0, 0, 0))

def temple_complex(i, x, y, min_i = 1):

    if i < min_i:
        pass

    else:
        tower_builder.simple_tower(i, (x, y, 0))
        temple_complex(i-1, x + p2(i), y + p2(i), min_i=min_i)
        temple_complex(i-1, x + p2(i), y - p2(i), min_i=min_i)
        temple_complex(i-1, x - p2(i), y + p2(i), min_i=min_i)
        temple_complex(i-1, x -  p2(i), y - p2(i), min_i=min_i)


temple_complex(i, 0, 0)

# tower_builder.simple_tower(i - 1, (p2(i), p2(i), 0))
# tower_builder.simple_tower(i - 1, (p2(i), -p2(i), 0))
# tower_builder.simple_tower(i - 1, (-p2(i), p2(i), 0))
# tower_builder.simple_tower(i - 1, (-p2(i), -p2(i), 0))

tower_mesh = tower_builder.materialize()
for layers in range(5, 9):

    config = OctoConfigs.config_25
    config.absolute_layers_per_cell = layers
    config.derive()

    RenderUtils.render_grid(tower_mesh, config, base_filename=f"{layers}_temple_complex.stl")

OctoConfigs.config_25.print_settings()
