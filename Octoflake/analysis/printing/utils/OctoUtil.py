import math

import numpy as np

from printing.grid.OctoVector import OctoVector


# TODO: Make this into something like "size", where it doubles up automatically
# The issue is that at some point we doubled the grid size so that all the octos would be on
# integer coordinates, but that meant that the radius doubled too
def p2(i, o=0):
    return 2 ** (i + o)

def octo_radius(i):
    """For an octoflake centered on the origin, gives the X (or y or x) corrdinate of the farthest octocell

    octo_radius(1) =

    """
    if i <0:
        raise ValueError("Tried to get the radius of a negative iteration.")
    if i==0:
        return 0
    else:
        return 2 ** i


def f_rad(*iterations):
    return sum([2 ** (i + 1) for i in iterations])


SQRT2 = math.sqrt(2)
SQRT22 = SQRT2 / 2
SQRT32 = math.sqrt(3) / 2

O = ORIGIN = OctoVector(0, 0, 0)

X = OctoVector(1, 0, 0)
Y = OctoVector(0, 1, 0)
Z = OctoVector(0, 0, 1)

X2 = 2 * X
Y2 = 2 * Y

E = np.array(X)
W = - E
N = np.array(Y)
S = - N
UP = np.array(Z)
DOWN = -UP

NE = N + E
NW = N + W
SW = S + W
SE = S + E

CARDINAL = np.array([E, N, W, S])
