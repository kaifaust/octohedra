from fractions import Fraction
from unittest import TestCase

from euclid3 import Vector3
from numpy import int64

from printing.utils.HCVector import FractionVector, HCV


class TestHCV(TestCase):

    def test_individual_assignment(self):
        xyz = (1.5, 2, 3)
        x, y, z = xyz

        vector = HCV(x, y, z)

        self.assertEqual(x, vector.x)
        self.assertEqual(y, vector.y)
        self.assertEqual(z, vector.z)
        self.assertEqual(xyz, vector)

    def test_vector_assignment(self):
        tup = (1, 2, 3)
        list = [4, 5, 6]
        v3 = Vector3(7, 8, 9)

        hcv_tup = HCV(tup)
        hcv_list = HCV(list)
        hcv_v3 = HCV(v3)

        self.assertEqual(tup, hcv_tup)
        self.assertEqual(tuple(list), hcv_list)
        self.assertEqual(tuple(v3), hcv_v3)

    def test_fraction_assignment(self):
        xyz = Fraction(1, 2), Fraction(3), Fraction(6, 4)
        x, y, z = xyz
        vector = HCV(x, y, z)

        self.assertEqual(x, vector.x)
        self.assertEqual(y, vector.y)
        self.assertEqual(z, vector.z)
        self.assertEqual(xyz, vector)

    def test_string_assignment(self):
        xyz = "3.5", "-1", "0"
        x, y, z = xyz
        vector = HCV(x, y, z)

        self.assertEqual(Fraction(x), vector.x)
        self.assertEqual(Fraction(y), vector.y)
        self.assertEqual(Fraction(z), vector.z)

    def test_non_half_fractions(self):
        self.assertRaises(ValueError, HCV, 1.49999, 0, 0)

    def test_rounding(self):
        HCV(1.000000000001, 0, 0)

    def test_non_decimal_input(self):
        self.assertRaises(ValueError, HCV, "abc", 0, 0)

    def test_to_str(self):
        self.assertEqual("(1, 2, 3)", str(HCV(1, 2, 3)))
        self.assertEqual("(0.5, -0.5, 12.5)", str(HCV(1 / 2, -2 / 4, "12.5")))

    def test_add(self):
        a = HCV(1.5, 2, 3)
        b = HCV(.5, "-1/2", 5.5)

        self.assertEqual((2, 1.5, 8.5), a + b)

    def test_neg(self):
        self.assertEqual((-1, 2, -3), -HCV(1, -2, 3))

    def test_scalar_mul(self):
        vec = HCV(1, 2, 3)

        self.assertEqual((2, 4, 6), vec * 2)
        self.assertEqual((2, 4, 6), 2 * vec)

    def test_vector_mul(self):
        a = HCV(1, 2, 3)
        b = HCV(3, 2, 3)

        self.assertEqual((3, 4, 9), a * b)
        self.assertEqual((3, 4, 9), b * a)

    def test_hash(self):
        a = hash(HCV(1, 0, 0))
        print(a)

    def test_rational_input(self):
        vec1 = HCV(int64(1), 2, 3)
        vec2 = HCV(1, 2, 3)

        self.assertEqual(vec1, vec2)
        self.assertEqual(hash(vec1), hash(vec2))
