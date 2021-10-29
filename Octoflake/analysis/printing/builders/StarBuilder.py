from euclid3 import Vector3

from printing.grid.OctoGrid import OctoGrid
from printing.grid.OctoVector import OctoVector
from printing.utils.OctoConfigs import config_25, config_3
from printing.utils.OctoUtil import ORIGIN, p2
from printing.builders.OctoBuilder import OctoBuilder
from printing.builders.FlakeBuilder import FlakeBuilder
from printing.utils import RenderUtils


class StarBuilder(OctoBuilder):

    def __init__(self, iteration, center=OctoVector(), length=1, recursive=False):
        super().__init__()
        self.center = center
        self.children.add(FlakeBuilder(iteration, center))
        if recursive:
            self.children.add(StarBuilder(iteration - 1, center + OctoVector(0, 0, p2(iteration + 1))))
        else:
            z = p2(iteration + 1)
            i = iteration - 1
            for j in range(length):
                self.children.add(FlakeBuilder(i, OctoVector(0, 0, z)))
                z += p2(i)
                i -= 1

        print(self.children)

    @classmethod
    def build_star(cls, iteration, center=OctoVector()):

        builder = StarBuilder(iteration)

        core_flake = FlakeBuilder.make_flake(iteration, center)
        outer_flake = FlakeBuilder.make_flake(iteration - 1,
                                              center + OctoVector(0, 0, p2(iteration + 1)))

        builder.children.add(core_flake)
        builder.children.add(outer_flake)
        return builder

    def materialize_additive(self, bonus_iteration=0):
        return super().materialize_additive(bonus_iteration) .six_way(self.center) # TODO: PUt
        # this back


def testing():
    i = 3
    grid = StarBuilder(i, recursive=True).materialize()

    # grid.merge(OctoStar(i-1, OctoVector(0, 0, p2(i+1))).materialize())
    # grid.six_way()
    # grid.crop(z_min=0, z_max=p2(i))

    above, below = grid.split(p2(i) + p2(i - 1))

    c = p2(i) + p2(i - 1)
    # below.crop(x_min=-c, x_max=c, y_min=-c, y_max=c)

    RenderUtils.render_grid(above, config_3, base_filename="above")
    RenderUtils.render_grid(below, config_3, base_filename="below")
    config_25.print_settings()



if __name__ == "__main__":
    testing()
