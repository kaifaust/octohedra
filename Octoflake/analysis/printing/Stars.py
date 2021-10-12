from printing.octo import OctoConfigs
from printing.octo.OctoUtil import p2
from printing.octo.builder.OctoBuilder import OctoBuilder
from printing.octo.builder.OctoTowerBuilder import OctoTowerBuilder
from printing.rendering import RenderUtils

i = 5

single_builder = OctoBuilder()
single_builder.make_flake(i, (0, 0, 0))
single_mesh = single_builder.materialize()

config = OctoConfigs.config_25
config.absolute_layers_per_cell = 8
config.derive()

RenderUtils.basic_render(single_mesh, config, filename=f"{8}_single.stl")

star_builder = OctoBuilder()
star_builder.stellate(i, (0, 0, 0))
star_mesh = star_builder.materialize()

tower_builder = OctoTowerBuilder()
tower_builder.simple_tower(i, (0, 0, p2(i)-p2(i-1)))
tower_mesh = tower_builder.materialize()

flower_builder = OctoTowerBuilder()
flower_builder.flower_tower(i, center=(0, 0, p2(i) - p2(i, - 2)), min_evil=3)
flower_mesh = flower_builder.materialize()

evil_builder = OctoTowerBuilder()
evil_builder.evil_tower(i, center=(0, 0, p2(i) - p2(i, - 2)), min_evil=3)
evil_mesh = evil_builder.materialize()


config = OctoConfigs.config_25

# RenderUtils.basic_render(builder.materialize(), config)


# for layers in range(6, 7):
#     config = OctoConfigs.config_25
#     config.absolute_layers_per_cell = layers
#     config.derive()
#
#     RenderUtils.basic_render(single_mesh, config, filename=f"{layers}_single.stl")
#     RenderUtils.basic_render(star_mesh, config, filename=f"{layers}_star.stl")
#     RenderUtils.basic_render(tower_mesh, config, filename=f"{layers}_tower.stl")
#     RenderUtils.basic_render(flower_mesh, config, filename=f"{layers}_flower.stl")
#     RenderUtils.basic_render(evil_mesh, config, filename=f"{layers}_evil.stl")




# base_layers = 6
# base_i = 4
#
# for i in range(1, base_i+1):
#
#     star_builder = OctoBuilder()
#     star_builder.stellate(i, (0, 0, 0))
#     star_mesh = star_builder.materialize()
#
#     config = OctoConfigs.config_25
#     config.absolute_layers_per_cell = base_layers * p2(base_i-i)
#     config.derive()
#
#     RenderUtils.basic_render(star_mesh, config, filename=f"i_{i}_star.stl")





OctoConfigs.config_25.print_settings()
