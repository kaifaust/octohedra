import math

from euclid3 import Vector3

from printing.builders.HollowFlake import HollowFlake
from printing.builders.OldOctoBuilder import OldOctoBuilder
from printing.utils.OctoUtil import p2, Z


class HollowOldOctoBuilder(OldOctoBuilder):

    def __init__(self, default_thickness = 0):
        super(HollowOldOctoBuilder, self).__init__()
        self.flakes = dict()
        self.default_thickness = default_thickness

    def make_flake(self, i, c):
        self.flakes[c] = HollowFlake(i, self.default_thickness, c)


    def simple_towerz(self, base_i, t, center=None, min_i=1, thinning=False):
        print("Making a hollow tower at", center)
        c = center if center is not None else Vector3(0, 0, p2(base_i, -1))
        for i in range(base_i, min_i - 1, -1):


            # self.flakes[tuple(c)] = HollowFlake(i, t, tuple(c))
            self.make_flake(i, tuple(c))
            # c += Z * (p2(i)-p2(i-2))
            c += Z * p2(i)
            # t = max(0, t-1)

    def evil_towerz(self, base_i, center=None, min_i=1, max_evil=math.inf, min_evil=3):
        print("wat")
        c = Vector3(*center) if center is not None else Vector3(0, 0, 0)
        for i in range(base_i, min_i - 1, -1):
            self.make_flake(i, tuple(c))
            # self.flakes[tuple(c)] = i
            if min_evil <= i <= max_evil:
                t_i = i - 1
                t_o = p2(i-1) + p2(i-2)
                t_z =  p2(t_i-1)
                print(c)
                self.simple_towerz(i - 1,1, c + (t_o, t_o, t_z))
                self.simple_towerz(i - 1,1, c + (t_o, -t_o, t_z))
                self.simple_towerz(i - 1,1, c + (-t_o, t_o, t_z))
                self.simple_towerz(i - 1,1, c + (-t_o, -t_o, t_z))
            # c += Z * (p2(i)-p2(i-2))
            c += Z * p2(i)




    def hollow_flake(self, i, c, t):
        print(f"Making a flake with center {c}")
        self.flakes[c] = HollowFlake(i,t, c)
