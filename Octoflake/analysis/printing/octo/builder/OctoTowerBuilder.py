import math
from enum import Enum

from euclid3 import Vector3
from printing.octo.OctoUtil import Z, p2

from printing.octo import OctoConfigs
from printing.octo.OctoGrid import OctoGrid
from printing.rendering.RenderUtils import basic_render

INF = 100


class Growth(Enum):
    NW = 1  # Unused
    NE = 2
    SE = 3
    SW = 4

    @staticmethod
    def ALL():
        return {
            Growth.NW: (-1, 1),
            Growth.NE: (1, 1),
            Growth.SE: (1, -1),
            Growth.SW: (-1, -1),
        }


# class OctoTowerConfig:
#
#     def __init__(self,
#                  base_i,
#                  min_i=0,
#                  center=None,
#                  max_evil=math.inf,
#                  min_evil=1
#                  ):
#         self.base_i = base_i
#         self.min_i = min_i
#         self.center = center
#         self.max_evil = max_evil
#         self.min_evil = min_evil


class OctoTowerBuilder:

    def __init__(self):
        self.flakes = dict()
        self.sub_towers = dict()

    def raw_flake(self, i, center):
        self.flakes[tuple(center)] = i

    def simple_tower(self, base_i, center=None, min_i=1):

        c = center if center is not None else Vector3(0, 0, 0)
        for i in range(base_i, min_i - 1, -1):
            self.flakes[tuple(c)] = i
            c += Z * p2(i)

    def tower(self, config):
        pass

    def evil_tower(self, base_i, center=None, min_i=1, max_evil=math.inf, min_evil=1):
        c = center if center is not None else Vector3(0, 0, 0)
        for i in range(base_i, min_i - 1, -1):
            self.flakes[tuple(c)] = i
            c += Z * p2(i)
            if min_evil <= i <= max_evil:
                t_i = i - 1
                t_o = p2(i)
                t_z = -p2(t_i)
                self.simple_tower(i - 1, c + (t_o, t_o, t_z), min_i)
                self.simple_tower(i - 1, c + (t_o, -t_o, t_z), min_i)
                self.simple_tower(i - 1, c + (-t_o, t_o, t_z), min_i)
                self.simple_tower(i - 1, c + (-t_o, -t_o, t_z), min_i)

    def flower_tower(self, base_i, growth_dirs=None, center=None, min_i=1, max_evil=math.inf, min_evil=3):
        all_dirs = {(1, 1), (1, -1), (-1, 1), (-1, -1)}
        growth_dirs = growth_dirs if growth_dirs is not None else all_dirs.copy()
        print("Making a flower tower that grows in: ", growth_dirs)
        c = center if center is not None else Vector3(0, 0, 0)
        for i in range(base_i, min_i - 1, -1):
            self.flakes[tuple(c)] = i
            c += Z * p2(i)
            if min_evil <= i <= max_evil:
                t_i = i - 1
                t_o = p2(i)
                t_z = -p2(t_i)
                for x, y in growth_dirs:
                    # print(x, y)
                    next_dirs = all_dirs.copy()
                    next_dirs.remove((-x, -y))
                    next_dirs={(x, y)}
                    print(next_dirs)

                    self.flower_tower(i-1, next_dirs, c + (t_o * x, t_o * y, t_z))
                    # self.flower_tower(i-1, c + (t_o, -t_o, t_z))
                    # self.flower_tower(i-1, c + (-t_o, t_o, t_z))
                    # self.flower_tower(i-1, c + (-t_o, -t_o, t_z))

            # if i in evil or (full_evil and iteration >= i > 1):
            #     exy = 2 ** (i) - 2 ** (i - 2) if not thin_evil else p2(i)
            #     ez = z + 2 ** (i - 2) if not thin_evil else z +  p2(i, -1)
            #     sub_evil = full_evil
            #     OctoBuilder.tower(grid, i - 1, center + (exy, exy, ez), full_evil=sub_evil)
            #     OctoBuilder.tower(grid, i - 1, center + (exy, -exy, ez), full_evil=sub_evil)
            #     OctoBuilder.tower(grid, i - 1, center + (-exy, exy, ez), full_evil=sub_evil)
            #     OctoBuilder.tower(grid, i - 1, center + (-exy, -exy, ez), full_evil=sub_evil)

            # grid.make_flake(i-1, center +  (exy, exy, ez))
            # grid.make_flake(i-1, center +  (exy, -exy, ez))
            # grid.make_flake(i-1, center +  (-exy, exy, ez))
            # grid.make_flake(i-1, center + (-exy, -exy, ez))

    def materialize(self, grid: OctoGrid = None):
        grid = grid if grid is not None else OctoGrid()

        for center, i in self.flakes.items():
            grid.make_flake(i, center=center)
        for tower in self.sub_towers.values():
            tower.materialize(grid)
        return grid


def test():
    tower = OctoTowerBuilder()
    i = 3
    # tower.evil_tower(i, center=(0, 0, p2(i) - p2(i, - 2)), min_evil=3, min_i=2)
    tower.flower_tower(i, center=(0, 0, p2(i) - p2(i, - 2)), min_evil=3)
    # tower.simple_tower(i, center=(0, 0, p2(i) - p2(i, - 2)))
    grid = OctoGrid()
    tower.materialize(grid)
    config = OctoConfigs.config_25
    basic_render(grid, config=config)
    config.print_settings()


if __name__ == "__main__":
    test()
