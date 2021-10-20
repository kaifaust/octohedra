import numpy as np
from euclid3 import Vector3
import math


def p2(i, o=0):
    return 2 ** (i + o)


SQRT2 = math.sqrt(2)
SQRT22 = SQRT2 / 2
SQRT32 = math.sqrt(3)/2

X = Vector3(1, 0, 0)
Y = Vector3(0, 1, 0)
Z = Vector3(0, 0, 1)

X2 = Vector3(2, 0, 0)
Y2 = Vector3(0, 2, 0)

E = np.array((1, 0, 0))
N = np.array((0, 1, 0))
W = np.array((-1, 0, 0))
S = np.array((0, -1, 0))

NE = N + E
NW = N + W
SW = S + W
SE = S + E

CARDINAL = np.array([E, N, W, S])
UP = np.array((0, 0, 1))
DOWN = np.array((0, 0, -1))
