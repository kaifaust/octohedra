import numpy as np
from euclid3 import Vector3
import math

from printing.grid.OctoVector import OctoVector


# TODO: Make this into something like "size", where it doubles up automatically
def p2(i, o=0):
    return 2 ** (i + o)


SQRT2 = math.sqrt(2)
SQRT22 = SQRT2 / 2
SQRT32 = math.sqrt(3)/2

ORIGIN = OctoVector(0, 0, 0)

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
