from printing.builders.FlakeBuilder import FlakeBuilder
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
        name="Rainbow Mini 0.2",
        nozzle_width=0.2,
        absolute_line_width=0.351, # (0.2 + .12) / 1.5
        absolute_layer_height=0.15,
        line_overlap=1,
        absolute_first_layer_height=.1499,
        absolute_floor_height=.01,
        # absolute_layers_per_cell=9,
        target_cell_width=3,
        absolute_slit=.01
    )

    config.print_settings()
    config.print_derived_values()



    # for layer_count in (4, 8, 12, 16):
    #     config.absolute_layers_per_cell = layer_count
    FlowerTower(base_i=2).render(config,
                      # layers=config.layers_per_cell,
                      # overlap=overlap,
                      # width=config.line_width,
                      filename="Flower 2")

    exit()

    # FlakeBuilder(5).render(config,filename="Flake")

    # i = 5
    # fb = FlakeBuilder(i-1)
    # print(fb.children)
    # fb.add_child(FlakeBuilder(5, center=octo_radius(i+1) * Z))
    # print(fb.children)
    # fb.render(config,"Flake With Base", i=i)
    # exit()



    EvilTowerX(base_i= 4, display_base=False).render(config,
                          # layers=layers,
                          # overlap=overlap,
                          # width=config.line_width,
                          filename="Evil")

    # EvilTowerX(base_i= 3, display_base=False).render(config,
    #                       # layers=layers,
    #                       # overlap=overlap,
    #                       width=config.line_width,
    #                       filename="Evil")

    # exit()

    FlakeBuilder(i).render(config)

    FlowerTower(i, elevate_base=True).render(config,
                                             # layers=layers,
                                             # overlap=overlap,
                                             # width=width,
                                             filename="Flower")

    exit()
    for width in (.2, .25, .30, .35):
        config.absolute_line_width = width

        FlowerTower(i, elevate_base=True).render(config,
                                                 # layers=layers,
                                                 # overlap=overlap,
                                                 width=width,
                                                 filename="Flower")


if __name__ == "__main__":
    gem_tuning()
