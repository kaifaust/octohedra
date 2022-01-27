import numbers
from dataclasses import astuple, dataclass

import numpy as np


def validate(i):
    try:
        int_i = int(i)
    except TypeError:
        raise ValueError("OctoVector coordinates may only be integers.")
    else:
        if i != int_i:
            raise ValueError("OctoVector coordinates may only be integers.")
        return int_i


@dataclass(frozen=True)
class OctoVector:
    x: numbers.Integral = 0
    y: numbers.Integral = 0
    z: numbers.Integral = 0

    def validate(self):
        for coordinate in self:
            if coordinate != int(coordinate):
                raise ValueError("OctoVector coordinates may only be integers in strict mode.")

    def __repr__(self):
        return f"OctoVector({float(self.x):g}, {float(self.y):g}, {float(self.z):g})"

    __str__ = __repr__

    def __add__(self, other):
        if isinstance(other, OctoVector):
            return OctoVector(self.x + other.x, self.y + other.y, self.z + other.z)
        elif hasattr(other, '__len__') and len(other) == 3:
            return OctoVector(self.x + other[0], self.y + other[1], self.z + other[2])
        else:
            raise TypeError(f"Tried to add {other} to an OctoVector but I don't know how.")

    __radd__ = __add__

    def __sub__(self, other):
        if isinstance(other, OctoVector):
            return OctoVector(self.x - other.x, self.y - other.y, self.z - other.z)
        elif hasattr(other, '__len__') and len(other) == 3:
            return OctoVector(self.x - other[0], self.y - other[1], self.z - other[2])
        else:
            raise TypeError(f"Tried to subtract {other} from an OctoVector, but I don't know "
                            f"how.")

    def __rsub__(self, other):
        if isinstance(other, OctoVector):
            return OctoVector(self.x - other.x, self.y - other.y, self.z - other.z)
        elif hasattr(other, '__len__') and len(other) == 3:
            return OctoVector(self.x - other[0], self.y - other[1], self.z - other[2])
        else:
            raise AttributeError(f"Tried to subtract {other} from an OctoVector, but I don't know "
                                 f"how.")

    def __neg__(self):
        return OctoVector(-self.x, -self.y, -self.z)

    def __mul__(self, other):
        if isinstance(other, OctoVector):
            return OctoVector(self.x * other.x, self.y * other.y, self.z * other.z)
        elif hasattr(other, '__len__') and len(other) == 3:
            return OctoVector(self.x * other[0], self.y * other[1], self.z * other[2])
        elif isinstance(other, numbers.Number):
            return OctoVector(self.x * other, self.y * other, self.z * other)
        # elif isinstance(other, numbers.Number):
        #     raise ValueError("OctoVector coordinates may only be integers.")
        else:
            raise TypeError(f"Tried to multiply an OctoVector by {other} but I don't know how.")

    __rmul__ = __mul__

    def as_np(self):
        return np.array((self.x, self.y, self.z))

    def as_tuple(self):
        return astuple(self)

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
    print(vec)
    # print(vec + vec2)

    print(OctoVector(x=100, y=0, z=0) + OctoVector(0, 0, 0))

    x, y, z, = vec
    print(x, y, z)
    print(vec[2])

    d = dict()
    d[vec2] = False

    print(vec)
