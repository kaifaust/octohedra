from euclid3 import *
from enum import Enum
import math
import subprocess
import os
import random


class OctoGridGenerator:

    def __init__(self):
        self.occ = dict()
        self.welding = dict()
        pass

    def stellate(self, iteration, center=(0, 0, 0), offset=None):
        offset = 2 ** (iteration) if offset is None else offset
        si = iteration
        self.make_flake(si, (center[0] + offset, center[1] + offset, center[2]))
        self.make_flake(si, (center[0] + offset, center[1] - offset, center[2]))
        self.make_flake(si, (center[0] - offset, center[1] + offset, center[2]))
        self.make_flake(si, (center[0] - offset, center[1] - offset, center[2]))
        self.make_flake(si, (center[0], center[1], center[2] + offset))
        self.make_flake(si, (center[0], center[1], center[2] - offset))

    def fill(self, iteration, center=(0, 0, 0)):
        offset = 2 ** iteration / 4
        i2 = iteration - 2
        self.make_flake(i2, (center[0] + 2 * offset, center[1], center[2] + offset))
        self.make_flake(i2, (center[0] - 2 * offset, center[1], center[2] + offset))
        self.make_flake(i2, (center[0], center[1] + 2 * offset, center[2] + offset))
        self.make_flake(i2, (center[0], center[1] - 2 * offset, center[2] + offset))
        self.make_flake(i2, (center[0] + 2 * offset, center[1], center[2] - offset))
        self.make_flake(i2, (center[0] - 2 * offset, center[1], center[2] - offset))
        self.make_flake(i2, (center[0], center[1] + 2 * offset, center[2] - offset))
        self.make_flake(i2, (center[0], center[1] - 2 * offset, center[2] - offset))

    def make_flake(self, iteration, center=Vector3(0, 0, 0), is_pyramid=True):
        if iteration == 0:
            if tuple(center) not in self.occ:
                self.occ[tuple(center)] = is_pyramid
            return

        i1 = iteration - 1
        o = 2 ** i1

        if tuple(center) not in self.welding:
            self.welding[tuple(center)] = is_pyramid

        self.make_flake(i1, center + Vector3(o, o, 0), is_pyramid)
        self.make_flake(i1, center + Vector3(o, -o, 0), is_pyramid)
        self.make_flake(i1, center + Vector3(-o, o, 0), is_pyramid)
        self.make_flake(i1, center + Vector3(-o, -o, 0), is_pyramid)
        self.make_flake(i1, center + Vector3(0, 0, o), is_pyramid=False)
        if not is_pyramid:
            self.make_flake(i1, center + Vector3(0, 0, -o), is_pyramid=False)

    def make_pyramid(self, iteration, center):
        self.make_flake(iteration, center, is_pyramid=True)

    def crop(self, x_min=None, x_max=None, y_min=None, y_max=None, z_min=None, z_max=None):

        to_remove = []
        for center, cell in self.occ.items():
            if center[2] == z_min:
                cell.is_pyramid = True
            if center[2] < z_min:
                to_remove.append(center)

        for center in to_remove:
            self.occ.pop(center)

        weld_to_remove = []
        for center in self.welding:
            if center[2] == z_min:
                self.welding[center] = True
            if center[2] < z_min:
                weld_to_remove.append(center)

        for center in weld_to_remove:
            self.welding.pop(center)
