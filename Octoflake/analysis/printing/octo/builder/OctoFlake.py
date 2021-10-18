from euclid3 import Vector3

from printing.octo.builder.OctoBuilder import OctoBuilder


class OctoFlake(OctoBuilder):
    def __init__(self, iteration, center: Vector3 = None, cell_scale=0):
        super().__init__()
        self.iteration = iteration
        self.center = center if center is not None else Vector3(0, 0, 0)
        self.cell_scale = cell_scale

    def materialize_additive(self, grid, bonus_iteration=0):
        grid.make_flake(self.iteration, self.center, self.cell_scale)

#
#
#
# class OctoFlakeBuilder(OctoBuilder):
#
#
#     def __init__(self, iteration, center:Vector3 = None, size = 1):
#         super.__init__()
#         self.iteration = iteration
#         self.center = center if center is not None else Vector3(0,0,0)
#         self.size = size
#
#
#
#
#
#     # def materialize_additive(self, grid=None, bonus_iteration=0):
#     #     grid = grid if grid is not None else OctoGrid()
#     #
#     #     OctoFlakeBuilder.make_flake(self.iteration, self.center, grid, bonus_iteration)
#
#
#     def make_flake(self, iteration, center, grid, cell_scale):
#
#         if iteration == cell_scale:
#             self.children.add(OctahedronBuilder.)
#             grid.make_flake(iteration, center)
