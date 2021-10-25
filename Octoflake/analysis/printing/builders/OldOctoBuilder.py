from euclid3 import Vector3

import numpy as np

from printing.utils.OctoUtil import p2
from printing.builders.OctoBuilder import OctoBuilder
from printing.builders.OctoFlake import OctoFlake


class OldOctoBuilder(OctoBuilder):


    def make_flake(self, i, c: Vector3 = None):
        self.children.add(OctoFlake(i, c))

    # def materialize(self, grid=None, bonus_i=0):
    #     grid = OctoGrid() if grid is None else grid
    #
    #     for flake in self.flakes.values():
    #         flake.materialize_additive(grid)
    #
    #     for flake in self.flakes.values():
    #         flake.materialize_subtractive(grid)
    #
    #     return grid


    def stellate(self, iteration, center=None, offset=None):
        offset = 2 ** (iteration) if offset is None else offset
        center = center if center is not None else (0,0,0)
        si = iteration-2
        # self.make_flake(iteration, center)

        self.make_flake(si, (center[0] + offset, center[1], center[2] + offset))
        self.make_flake(si, (center[0] - offset, center[1], center[2] + offset))
        self.make_flake(si, (center[0], center[1]+offset, center[2] + offset))
        self.make_flake(si, (center[0], center[1]-offset, center[2] + offset))

        o2 = offset * 2
        self.make_flake(si, (center[0] + o2, center[1], center[2]))
        self.make_flake(si, (center[0] - o2, center[1], center[2] + 0))
        self.make_flake(si, (center[0], center[1] + o2, center[2] + 0))
        self.make_flake(si, (center[0], center[1] - o2, center[2] + 0))
        self.make_flake(si, (center[0], center[1], center[2] + o2))
        self.make_flake(si, (center[0], center[1], center[2] - o2))


        self.make_flake(si, (center[0] + offset, center[1] + offset, center[2]))
        self.make_flake(si, (center[0] + offset, center[1] - offset, center[2]))
        self.make_flake(si, (center[0] - offset, center[1] + offset, center[2]))
        self.make_flake(si, (center[0] - offset, center[1] - offset, center[2]))
        self.make_flake(si, (center[0], center[1], center[2] + offset))
        self.make_flake(si, (center[0], center[1], center[2] - offset))

    @staticmethod
    def stalag(grid, iteration):
        OldOctoBuilder.tower(grid, iteration, (0, 0, 2 ** iteration / 2))

    @staticmethod
    def tower_complex(grid, iteration, center=(0, 0, 0)):
        if iteration < 1:
            return
        OldOctoBuilder.tower(grid, iteration, center, full_evil=True)
        OldOctoBuilder.tower_complex(grid, iteration - 1,
                                     (center[0] + 2 ** iteration, center[1] + 2 ** iteration, center[2]))
        OldOctoBuilder.tower_complex(grid, iteration - 1,
                                     (center[0] + 2 ** iteration, center[1] - 2 ** iteration, center[2]))
        OldOctoBuilder.tower_complex(grid, iteration - 1,
                                     (center[0] - 2 ** iteration, center[1] + 2 ** iteration, center[2]))
        OldOctoBuilder.tower_complex(grid, iteration - 1,
                                     (center[0] - 2 ** iteration, center[1] - 2 ** iteration, center[2]))

    @staticmethod
    def tower(grid, iteration, center=(0, 0, 0), evil=frozenset(), full_evil=False, thin_evil=True):
        z = 0
        center = np.array(center)
        for i in range(iteration, 0, -1):
            grid.make_flake(i, center=(center[0], center[1], center[2] + z))

            if i in evil or (full_evil and iteration >= i > 1):
                exy = 2 ** (i) - 2 ** (i - 2) if not thin_evil else p2(i)
                ez = z + 2 ** (i - 2) if not thin_evil else z + p2(i, -1)
                sub_evil = full_evil
                OldOctoBuilder.tower(grid, i - 1, center + (exy, exy, ez), full_evil=sub_evil)
                OldOctoBuilder.tower(grid, i - 1, center + (exy, -exy, ez), full_evil=sub_evil)
                OldOctoBuilder.tower(grid, i - 1, center + (-exy, exy, ez), full_evil=sub_evil)
                OldOctoBuilder.tower(grid, i - 1, center + (-exy, -exy, ez), full_evil=sub_evil)

                # grid.make_flake(i-1, center +  (exy, exy, ez))
                # grid.make_flake(i-1, center +  (exy, -exy, ez))
                # grid.make_flake(i-1, center +  (-exy, exy, ez))
                # grid.make_flake(i-1, center + (-exy, -exy, ez))

            z += 2 ** i

    @staticmethod
    def fill(grid, iteration, center=(0, 0, 0)):
        offset = 2 ** (iteration - 2)
        i2 = iteration - 2
        grid.make_flake(i2, center=(center[0] + 2 * offset, center[1], center[2] + offset))
        grid.make_flake(i2, center=(center[0] - 2 * offset, center[1], center[2] + offset))
        grid.make_flake(i2, center=(center[0], center[1] + 2 * offset, center[2] + offset))
        grid.make_flake(i2, center=(center[0], center[1] - 2 * offset, center[2] + offset))
        grid.make_flake(i2, center=(center[0] + 2 * offset, center[1], center[2] - offset))
        grid.make_flake(i2, center=(center[0] - 2 * offset, center[1], center[2] - offset))
        grid.make_flake(i2, center=(center[0], center[1] + 2 * offset, center[2] - offset))
        grid.make_flake(i2, center=(center[0], center[1] - 2 * offset, center[2] - offset))
