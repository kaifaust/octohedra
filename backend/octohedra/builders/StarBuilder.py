from trimesh.exchange.export import export_mesh

from octohedra.builders.FlakeBuilder import FlakeBuilder
from octohedra.builders.OctoBuilder import OctoBuilder
from octohedra.config import OUTPUT_DIR
from octohedra.grid.OctoVector import OctoVector

# from octohedra.grid.Renderer import Renderer
from octohedra.utils import OctoConfigs, RenderUtils

# from octohedra.utils.OctoConfigs import config_25
from octohedra.utils.OctoUtil import p2


class StarBuilder(OctoBuilder):

    def __init__(self, iteration, center=OctoVector(), length=1, recursive=False):
        super().__init__()
        self.center = center
        self.add_child(FlakeBuilder(iteration, center, scale=0))
        if recursive:
            self.add_child(StarBuilder(iteration - 1,
                                       center + OctoVector(0, 0, p2(iteration + 1))))
        else:
            z = p2(iteration + 1)
            i = iteration - 1
            for j in range(length):
                # self.add_child(FlakeBuilder(i, OctoVector(0, 0, z), scale=1-j))
                self.add_child(FlakeBuilder(i, OctoVector(0, 0, z), scale=0))
                z += p2(i + 1)
                i -= 1

    # @classmethod
    # def build_star(cls, iteration, center=OctoVector()):
    #
    #     builder = StarBuilder(iteration)
    #
    #     core_flake = FlakeBuilder.make_flake(iteration, center)
    #     outer_flake = FlakeBuilder.make_flake(iteration - 1,
    #                                           center + OctoVector(0, 0, p2(iteration + 1)))
    #
    #     builder.children.add(core_flake)
    #     builder.children.add(outer_flake)
    #     return builder

    def materialize_additive(self, bonus_iteration=0):
        return super().materialize_additive(bonus_iteration).six_way(self.center)  # TODO: PUt
        # this back


def testing_recursive():
    i = 4
    grid = StarBuilder(i, recursive=True).materialize()

    # grid.merge(OctoStar(i-1, OctoVector(0, 0, p2(i+1))).materialize())
    # grid.six_way()
    # grid.crop(z_min=0, z_max=p2(i))

    above, below = grid.split(p2(i) + p2(i - 1))

    c = p2(i) + p2(i - 1)
    # below.crop(x_min=-c, x_max=c, y_min=-c, y_max=c)

    RenderUtils.render_grid(above, config_3, filename="above")
    RenderUtils.render_grid(below, config_3, filename="below")
    config_25.print_settings()


def testing():
    i = 4
    config = OctoConfigs.config_20_rainbow_quality
    # config = OctoConfigs.config_20_quantum_quality_mini
    # config = OctoConfigs.config_20_rainbow_balance
    # config = OctoConfigs.config_20_rainbow_speed
    # config.absolute_layer_height = .05
    # config.target_overlap_cell_ratio = 2
    # config.absolute_overlap = 4 * config.line_width
    # config.derive()
    # config.absolute_layers_per_cell = 16
    grid = StarBuilder(i, length=1).render(config)
    config.print_settings()
    config.print_derived_values()
    exit()
    grid.crop_bottom()
    grid.compute_trimming()

    mesh = Renderer().render(grid, config=config)
    config.print_settings()

    filename = str(OUTPUT_DIR / "derp.obj")

    export_mesh(mesh, filename, include_normals=False)

    with open(filename, "a") as f:
        f.write("\n")


if __name__ == "__main__":
    # testing_recursive()
    testing()
