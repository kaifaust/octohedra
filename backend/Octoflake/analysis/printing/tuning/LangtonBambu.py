from printing.builders.FlakeBuilder import FlakeBuilder
from printing.builders.StarBuilder import StarBuilder
from printing.builders.TowerBuilders import FlowerTowerX, FlowerTower, EvilTowerX
from printing.utils.OctoConfig import OctoConfig
from printing.utils.OctoUtil import octo_radius, Z


def gem_tuning():
    # config = OctoConfig(
    #     name="Rainbow Gem",
    #     nozzle_width=0.2,
    #     absolute_line_width=0.3,
    #     absolute_layer_height=0.15,
    #     line_overlap=1,
    #     absolute_first_layer_height= .2249, #.1799,
    #     absolute_floor_height=.01,
    #     absolute_layers_per_cell=6, # prev was 16
    #     # target_cell_width=1.75,
    #     # target_cell_width=1,
    #     absolute_slit=.001
    # )

    # config = OctoConfig(
    #     name="Rainbow Mk3 0.3",
    #     nozzle_width=0.3,
    #     absolute_line_width=0.4,
    #     absolute_layer_height=0.15,
    #     line_overlap=1,
    #     absolute_first_layer_height=.2249,
    #     absolute_floor_height=.01,
    #     # absolute_layers_per_cell=8,
    #     target_cell_width=2.5,
    #     absolute_slit=.001
    # )

    config = OctoConfig(
        name="Bambu 0.4",
        nozzle_width=0.4,
        absolute_line_width=0.42, # (0.2 + .12) / 1.5
        absolute_layer_height=0.16,
        line_overlap=1,
        absolute_first_layer_height=.1999,
        # solid_layers=2,
        # absolute_floor_height=.01,
        # absolute_layers_per_cell=9,
        target_cell_width=3,
        absolute_slit=.01
    )

    config.print_settings()
    config.print_derived_values()



    # for layer_count in (4, 8, 12, 16):
    #     config.absolute_layers_per_cell = layer_count
    # FlowerTower(base_i=2).render(config,
    #                   # layers=config.layers_per_cell,
    #                   # overlap=overlap,
    #                   # width=config.line_width,
    #                   filename="Flower 2")

    # exit()

    StarBuilder(5, length=3).render(config,filename="Flake")

gem_tuning()
