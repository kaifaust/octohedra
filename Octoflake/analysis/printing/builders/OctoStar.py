from euclid3 import Vector3

from printing.utils.OctoConfigs import config_25
from printing.utils.OctoUtil import ORIGIN, p2
from printing.builders.OctoBuilder import OctoBuilder
from printing.builders.OctoFlake import OctoFlake
from printing.utils import RenderUtils


class OctoStar(OctoBuilder):

    def __init__(self):
        super().__init__()

    @classmethod
    def build_star(cls, iteration, center: Vector3 = None):
        center = center if center is not None else ORIGIN
        builder = OctoStar()

        core_flake = OctoFlake.make_flake(iteration, center)
        outer_flake = OctoFlake.make_flake(iteration - 1, center + Vector3(0, 0, p2(iteration + 1)))

        builder.children.add(core_flake)
        builder.children.add(outer_flake)
        return builder

    def materialize_additive(self, bonus_iteration=0):
        return super().materialize_additive(bonus_iteration).six_way()


def testing():
    grid = OctoStar.build_star(3).materialize()

    RenderUtils.render_grid(grid, config_25)


if __name__ == "__main__":
    testing()
