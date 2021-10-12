from euclid3 import Vector3
import math


def p2(i, o=0):
    return 2 ** (i + o)


SQRT2 = math.sqrt(2)
SQRT22 = SQRT2 / 2

X = Vector3(1, 0, 0)
Y = Vector3(0, 1, 0)
Z = Vector3(0, 0, 1)

X2 = Vector3(2, 0, 0)
Y2 = Vector3(0, 2, 0)
