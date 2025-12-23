"""Tests for HCVector (Half-integer Coordinate Vector)."""
from fractions import Fraction

import pytest
from euclid3 import Vector3
from numpy import int64

from printing.utils.HCVector import HCV


class TestHCVAssignment:
    """Tests for HCV constructor and assignment."""

    def test_individual_assignment(self):
        """HCV should accept individual x, y, z values."""
        xyz = (1.5, 2, 3)
        x, y, z = xyz

        vector = HCV(x, y, z)

        assert vector.x == x
        assert vector.y == y
        assert vector.z == z
        assert xyz == vector

    def test_vector_assignment(self):
        """HCV should accept tuples, lists, and Vector3."""
        tup = (1, 2, 3)
        lst = [4, 5, 6]
        v3 = Vector3(7, 8, 9)

        hcv_tup = HCV(tup)
        hcv_list = HCV(lst)
        hcv_v3 = HCV(v3)

        assert tup == hcv_tup
        assert tuple(lst) == hcv_list
        assert tuple(v3) == hcv_v3

    def test_fraction_assignment(self):
        """HCV should accept Fraction values."""
        xyz = Fraction(1, 2), Fraction(3), Fraction(6, 4)
        x, y, z = xyz
        vector = HCV(x, y, z)

        assert vector.x == x
        assert vector.y == y
        assert vector.z == z
        assert xyz == vector

    def test_string_assignment(self):
        """HCV should accept string representations of numbers."""
        xyz = "3.5", "-1", "0"
        x, y, z = xyz
        vector = HCV(x, y, z)

        assert vector.x == Fraction(x)
        assert vector.y == Fraction(y)
        assert vector.z == Fraction(z)

    def test_rational_input(self):
        """HCV should handle numpy int64 types correctly."""
        vec1 = HCV(int64(1), 2, 3)
        vec2 = HCV(1, 2, 3)

        assert vec1 == vec2
        assert hash(vec1) == hash(vec2)


class TestHCVValidation:
    """Tests for HCV input validation."""

    def test_non_half_fractions_raises(self):
        """HCV should reject values that aren't half-integers."""
        with pytest.raises(ValueError):
            HCV(1.49999, 0, 0)

    def test_rounding_accepted(self):
        """HCV should accept values very close to valid half-integers."""
        HCV(1.000000000001, 0, 0)  # Should not raise

    def test_non_decimal_input_raises(self):
        """HCV should reject non-numeric strings."""
        with pytest.raises(ValueError):
            HCV("abc", 0, 0)


class TestHCVOperations:
    """Tests for HCV arithmetic operations."""

    def test_to_str(self):
        """HCV should have readable string representation."""
        assert str(HCV(1, 2, 3)) == "(1, 2, 3)"
        assert str(HCV(1 / 2, -2 / 4, "12.5")) == "(0.5, -0.5, 12.5)"

    def test_add(self):
        """HCV addition should work correctly."""
        a = HCV(1.5, 2, 3)
        b = HCV(0.5, -0.5, 5.5)

        assert (2, 1.5, 8.5) == a + b

    def test_neg(self):
        """HCV negation should work correctly."""
        assert (-1, 2, -3) == -HCV(1, -2, 3)

    def test_scalar_mul(self):
        """HCV scalar multiplication should work from both sides."""
        vec = HCV(1, 2, 3)

        assert (2, 4, 6) == vec * 2
        assert (2, 4, 6) == 2 * vec

    def test_vector_mul(self):
        """HCV element-wise multiplication should work correctly."""
        a = HCV(1, 2, 3)
        b = HCV(3, 2, 3)

        assert (3, 4, 9) == a * b
        assert (3, 4, 9) == b * a

    def test_hash(self):
        """HCV should be hashable."""
        h = hash(HCV(1, 0, 0))
        assert isinstance(h, int)
