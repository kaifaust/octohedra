import itertools
import math
from dataclasses import astuple, dataclass, field
from fractions import Fraction

import numpy as np
from euclid3 import Vector3


def validate(i):
    if i != int(i):
        raise ValueError("OctoVector coordinates may only be integers.")
    return int(i)


@dataclass(frozen=True)
class OctoVector:
    x: int = 0
    y: int = 0
    z: int = 0
    # strict: bool = field(init=)



    # def __post_init__(self):
    #     validate(self.x)
    #     validate(self.y)
    #     validate(self.z)

    def validate(self):
        for coordinate in self:
            if coordinate != int(coordinate):
                raise ValueError("OctoVector coordinates may only be integers in strict mode.")



    # __slots__ = ()

    # def __new__(cls, x, y, z):
    #
    #     self = super().__new__(cls, validate(x), validate(y), validate(z))
    #     return self
    #
    # def __str__(self):
    #     return f"({float(self.x):g}, {float(self.y):g}, {float(self.z):g})"

    def __add__(self, other):
        if isinstance(other, OctoVector):
            return OctoVector(self.x + other.x, self.y + other.y, self.z + other.z)
        elif hasattr(other, '__len__') and len(other) == 3:
            return OctoVector(self.x + other[0], self.y + other[1], self.z + other[2])
        else:
            raise AttributeError(f"Tried to add {other} to an OctoVector but I don't know how.")

    __radd__ = __add__

    def __sub__(self, other):
        if isinstance(other, OctoVector):
            return OctoVector(self.x - other.x, self.y - other.y, self.z - other.z)
        elif hasattr(other, '__len__') and len(other) == 3:
            return OctoVector(self.x - other[0], self.y - other[1], self.z - other[2])
        else:
            raise AttributeError(f"Tried to subtract {other} from an OctoVector, but I don't know "
                                 f"how.")

    def __rsub__(self, other):
        if isinstance(other, OctoVector):
            return OctoVector(*map(math.prod, zip(astuple(self), astuple(other))))
        elif hasattr(other, '__len__') and len(other) == 3:
            return OctoVector(*map(math.prod, zip(astuple(self), other)))
        else:
            raise AttributeError(f"Tried to subtract {other} from an OctoVector, but I don't know"
                                 f" how.")

    def __neg__(self):
        return OctoVector(-self.x, -self.y, -self.z)

    def __mul__(self, other):
        # if isinstance(other, OctoVector):
        #     return OctoVector(*map(math.prod, zip(astuple(self), astuple(other))))
        if hasattr(other, '__len__') and len(other) == 3:
            return OctoVector(*map(math.prod, zip(astuple(self), other)))
        else:


            return OctoVector(self.x * other,
                              self.y * other,
                              self.z * other)

    def to_np(self):
        return np.array((self.x, self.y, self.z))

    def as_tuple(self):
        return astuple(self)

    __rmul__ = __mul__

    def __iter__(self):
        return self.as_tuple().__iter__()

    def __getitem__(self, item):
        return self.as_tuple()[item]

    def __len__(self):
        return len(self.as_tuple())


if __name__ == "__main__":
    vec = OctoVector(1, 2, 3)
    vec2 = OctoVector(-1, 2, 3)
    print(vec * 5)
    print(vec * Vector3(2, 3, 5))
    # print(vec + vec2)

    print(OctoVector(x=100, y=0, z=0) + OctoVector(0, 0, 0))

    x, y, z, = vec
    print(x, y, z)
    print(vec[2])

    d = dict()
    d[vec2] = False

    print(d[vec * (-1, 1, 1.0)])

    print(vec)
