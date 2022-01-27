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
        radius = p2(self.iteration + 1)
        grid.fill(radius, self.center)

        return grid

    def materialize_subtractive(self, grid):
        radius = p2(self.iteration) - 2 * p2(self.thickness_iteration)
        grid.fill(radius, self.center, clear=True)

    def __repr__(self):
        return f"HollowFlake({self.iteration}, {self.center}, {self.thickness_iteration})"




if __name__=="__main__":



    flake = HollowFlake()
