import math
from fractions import Fraction
from typing import NamedTuple


class FractionVector(NamedTuple):
    x: Fraction
    y: Fraction
    z: Fraction


def convert(i) -> Fraction:
    out = Fraction(float(i)).limit_denominator()
    if out.denominator > 2:
        raise ValueError("HVC coordinates may only be integers and half-integers.")
    return out


class HCV(FractionVector):
    __slots__ = ()

    def __new__(cls, *args, **kwargs):

        if len(args) == 3:
            x, y, z = args
        elif len(args) > 0 and hasattr(args[0], '__len__') and len(args[0]) == 3:
            x, y, z = args[0]
        else:
            raise AttributeError("Didn't find enough coordinates")

        args = (convert(x), convert(y), convert(z))

        self = super().__new__(cls, *args, **kwargs)
        return self

    def __str__(self):
        return f"({float(self.x):g}, {float(self.y):g}, {float(self.z):g})"

    # def __repr__(self):
    #     return str(self)

    def __add__(self, other):
        assert hasattr(other, '__len__') and len(other) == 3
        return HCV(*map(sum, zip(self, other)))

    __radd__ = __add__

    def __neg__(self):
        return HCV(*map(Fraction.__neg__, self))

    def __mul__(self, other):
        if hasattr(other, '__len__') and len(other) == 3:
            return HCV(*map(math.prod, zip(self, other)))

        else:
            frac_other = convert(other)

            return HCV(self.x * frac_other,
                       self.y * frac_other,
                       self.z * frac_other)

    __rmul__ = __mul__
