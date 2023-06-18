from printing.builders.FlakeBuilder import FlakeBuilder
from printing.builders.TowerBuilders import FlowerTowerX, FlowerTower, EvilTowerX
from printing.utils.OctoConfig import OctoConfig

raspberry_gold = OctoConfig(
    name="Raspberry Gold Gem",
    nozzle_width=0.2,
    absolute_line_width=0.25,
    absolute_layer_height=0.12,
    line_overlap=1,
    absolute_first_layer_height=.199,
    absolute_floor_height=.01,
    absolute_layers_per_cell=12,
    # target_cell_width=1.75,
    absolute_slit=.001
)

def gem_tuning():




    FlowerTower(base_i=2).render(raspberry_gold, filename="Sparkle")



    FlakeBuilder(3).render(raspberry_gold,filename="Flake")

    EvilTowerX(base_i= 4, display_base=False).render(raspberry_gold,
                          # layers=layers,
                          # overlap=overlap,
                          # width=config.line_width,
                          filename="Evil")

    # EvilTowerX(base_i= 3, display_base=False).render(config,
    #                       # layers=layers,
    #                       # overlap=overlap,
    #                       width=config.line_width,
    #                       filename="Evil")

    exit()

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
