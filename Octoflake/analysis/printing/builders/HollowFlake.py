from printing.grid.OctoGrid import OctoGrid
from printing.utils.OctoUtil import p2
from printing.builders.OctoBuilder import OctoBuilder


class HollowFlake(OctoBuilder):

    def __init__(self, iteration, thickness_iteration=0, center=(0, 0, 0)):
        super(HollowFlake, self).__init__()
        self.iteration = iteration
        self.thickness_iteration = thickness_iteration
        self.center = center

    def materialize_additive(self):
        grid = OctoGrid()
        grid.fill(self.iteration, self.thickness_iteration, self.center)

        return grid

    def materialize_subtractive(self, grid):
        t = p2(self.iteration) - 2 * p2(self.thickness_iteration)
        grid.clear_octo(t, center=self.center)

    def __repr__(self):
        return f"HollowFlake({self.iteration}, {self.center}, {self.thickness_iteration})"
