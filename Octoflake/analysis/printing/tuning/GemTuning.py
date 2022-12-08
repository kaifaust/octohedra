from printing.builders.FlakeBuilder import FlakeBuilder
from printing.builders.TowerBuilders import FlowerTower
from printing.utils.OctoConfig import OctoConfig


def gem_tuning():
    config = OctoConfig(
        name="Rainbow Gem",
        nozzle_width=0.2,
        absolute_line_width=0.35,
        absolute_layer_height=-.12,
        line_overlap=1,
        absolute_first_layer_height=.1999,
        absolute_floor_height=.01,
        # absolute_layers_per_cell=8,
        target_cell_width=2,
        absolute_slit=.001
    )

    config.print_settings()
    config.print_derived_values()

    i = 2

    # FlowerTowerX().render(config,
    #                       # layers=layers,
    #                       # overlap=overlap,
    #                       width=config.line_width,
    #                       filename="Flower")

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
