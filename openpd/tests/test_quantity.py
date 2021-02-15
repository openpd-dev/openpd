from openpd.unit.baseDimension import BaseDimension
import pytest
import numpy as np

from ..unit import *
from .. import isArrayEqual

class TestQuantity:
    def setup(self):
        pass

    def teardown(self):
        pass

    def test_attributes(self):
        quantity = 1 * angstrom
        assert quantity.value == 1
        assert quantity.unit == angstrom.unit

        quantity = np.array([1, 2, 3]) * angstrom
        assert quantity[0].value == 1
        assert quantity[0].unit == angstrom.unit

        quantity = [1, 2, 3, 4] * angstrom
        assert quantity[0].value == 1
        assert quantity[0].unit == angstrom.unit

    def test_exceptions(self):
        pass

    def test_eq(self):
        assert 1 * nanometer == 10 * angstrom
        assert not 1 * nanometer == 1 * nanosecond

        assert 1 * nanometer == 1
        assert 1 * nanometer != 10

    def test_add(self):
        # __add__
        quantity = np.array([1, 2, 3, 4]) * angstrom
        quantity = quantity + 1
        assert quantity[0] == 2 * angstrom
        assert quantity[-1] == 5 * angstrom
        assert isArrayEqual(quantity, np.array([1, 2, 3, 4]) * angstrom + 1 * angstrom)

        quantity = np.array([1, 2, 3, 4]) * angstrom
        quantity = quantity + 1 * nanometer
        assert quantity[0] == 11 * angstrom
        assert quantity[-1] == 14 * angstrom

        quantity = np.array([1, 2, 3, 4]) * angstrom
        quantity = quantity + [1, 2, 3, 4]
        assert quantity[0] == 2 * angstrom
        assert quantity[-1] == 8 * angstrom
        assert isArrayEqual(quantity, np.array([1, 2, 3, 4]) * angstrom + [1, 2, 3, 4] * angstrom)

        quantity = np.array([1, 2, 3, 4]) * angstrom
        quantity = quantity + [1, 2, 3, 4] * nanometer
        assert quantity[0] == 11 * angstrom
        assert quantity[-1] == 44 * angstrom

        quantity = np.array([1, 2, 3, 4]) * angstrom
        quantity = quantity + np.array([1, 2, 3, 4])
        assert quantity[0] == 2 * angstrom
        assert quantity[-1] == 8 * angstrom
        assert isArrayEqual(quantity, np.array([1, 2, 3, 4]) * angstrom + [1, 2, 3, 4] * angstrom)

        quantity = np.array([1, 2, 3, 4]) * angstrom
        quantity = quantity + np.array([1, 2, 3, 4]) * nanometer
        assert quantity[0] == 11 * angstrom
        assert quantity[-1] == 44 * angstrom

        # __iadd__
        quantity = np.array([1, 2, 3, 4]) * angstrom
        quantity += 1
        assert quantity[0] == 2 * angstrom
        assert quantity[-1] == 5 * angstrom

        quantity = np.array([1, 2, 3, 4]) * angstrom
        quantity += 1 * nanometer
        assert quantity[0] == 11 * angstrom
        assert quantity[-1] == 14 * angstrom

        quantity = np.array([1, 2, 3, 4]) * angstrom
        quantity += [1, 2, 3, 4]
        assert quantity[0] == 2 * angstrom
        assert quantity[-1] == 8 * angstrom
        assert isArrayEqual(quantity, np.array([1, 2, 3, 4]) * angstrom + [1, 2, 3, 4] * angstrom)

        quantity = np.array([1, 2, 3, 4]) * angstrom
        quantity += [1, 2, 3, 4] * nanometer
        assert quantity[0] == 11 * angstrom
        assert quantity[-1] == 44 * angstrom

        quantity = np.array([1, 2, 3, 4]) * angstrom
        quantity += np.array([1, 2, 3, 4])
        assert quantity[0] == 2 * angstrom
        assert quantity[-1] == 8 * angstrom
        assert isArrayEqual(quantity, np.array([1, 2, 3, 4]) * angstrom + [1, 2, 3, 4] * angstrom)

        quantity = np.array([1, 2, 3, 4]) * angstrom
        quantity += np.array([1, 2, 3, 4]) * nanometer
        assert quantity[0] == 11 * angstrom
        assert quantity[-1] == 44 * angstrom
        
        # __radd__
        quantity = np.array([1, 2, 3, 4]) * angstrom
        quantity = 1 + quantity
        assert quantity[0] == 2 * angstrom
        assert quantity[-1] == 5 * angstrom
        assert isArrayEqual(quantity, 1 * angstrom + np.array([1, 2, 3, 4]) * angstrom)

        quantity = np.array([1, 2, 3, 4]) * angstrom
        quantity = 1 * nanometer + quantity
        assert quantity[0] == 11 * angstrom
        assert quantity[-1] == 14 * angstrom

        quantity = np.array([1, 2, 3, 4]) * angstrom
        quantity = [1, 2, 3, 4] + quantity
        assert quantity[0] == 2 * angstrom
        assert quantity[-1] == 8 * angstrom
        assert isArrayEqual(quantity, np.array([1, 2, 3, 4]) * angstrom + [1, 2, 3, 4] * angstrom)

        quantity = np.array([1, 2, 3, 4]) * angstrom
        quantity = [1, 2, 3, 4] * nanometer + quantity
        assert quantity[0] == 11 * angstrom
        assert quantity[-1] == 44 * angstrom

        quantity = np.array([1, 2, 3, 4]) * angstrom
        quantity = np.array([1, 2, 3, 4]) + quantity
        assert quantity[0] == 2 * angstrom
        assert quantity[-1] == 8 * angstrom
        assert isArrayEqual(quantity, np.array([1, 2, 3, 4]) * angstrom + [1, 2, 3, 4] * angstrom)

        quantity = np.array([1, 2, 3, 4]) * angstrom
        quantity = np.array([1, 2, 3, 4]) * nanometer + quantity
        assert quantity[0] == 11 * angstrom
        assert quantity[-1] == 44 * angstrom

        # Different unit
        quantity1 = np.array([1, 2]) * angstrom
        quantity2 = np.array([2, 1]) * second
        with pytest.raises(ValueError):
            quantity1 + quantity2

    def test_sub(self):
        # __sub__
        quantity = np.array([1, 2, 3, 4]) * angstrom
        quantity = quantity - 1
        assert quantity[0] == 0 * angstrom
        assert quantity[-1] == 3 * angstrom
        assert isArrayEqual(quantity, np.array([1, 2, 3, 4]) * angstrom - 1 * angstrom)

        quantity = np.array([1, 2, 3, 4]) * angstrom
        quantity = quantity - 1 * nanometer
        assert quantity[0] == -9 * angstrom
        assert quantity[-1] == -6 * angstrom

        quantity = np.array([1, 2, 3, 4]) * angstrom
        quantity = quantity - [1, 2, 3, 4]
        assert quantity[0] == 0 * angstrom
        assert quantity[-1] == 0 * angstrom
        assert isArrayEqual(quantity, np.array([1, 2, 3, 4]) * angstrom - [1, 2, 3, 4] * angstrom)

        quantity = np.array([1, 2, 3, 4]) * angstrom
        quantity = quantity - [1, 2, 3, 4] * nanometer
        assert quantity[0] == -9 * angstrom
        assert quantity[-1] == -36 * angstrom

        quantity = np.array([1, 2, 3, 4]) * angstrom
        quantity = quantity - np.array([1, 2, 3, 4])
        assert quantity[0] == 0 * angstrom
        assert quantity[-1] == 0 * angstrom
        assert isArrayEqual(quantity, np.array([1, 2, 3, 4]) * angstrom - np.array([1, 2, 3, 4]) * angstrom)

        quantity = np.array([1, 2, 3, 4]) * angstrom
        quantity = quantity - np.array([1, 2, 3, 4]) * nanometer
        assert quantity[0] == -9 * angstrom
        assert quantity[-1] == -36 * angstrom

        # __isub__
        quantity = np.array([1, 2, 3, 4]) * angstrom
        quantity -= 1
        assert quantity[0] == 0 * angstrom
        assert quantity[-1] == 3 * angstrom
        assert isArrayEqual(quantity, np.array([1, 2, 3, 4]) * angstrom - 1 * angstrom)

        quantity = np.array([1, 2, 3, 4]) * angstrom
        quantity -= 1 * nanometer
        assert quantity[0] == -9 * angstrom
        assert quantity[-1] == -6 * angstrom

        quantity = np.array([1, 2, 3, 4]) * angstrom
        quantity -= [1, 2, 3, 4]
        assert quantity[0] == 0 * angstrom
        assert quantity[-1] == 0 * angstrom
        assert isArrayEqual(quantity, np.array([1, 2, 3, 4]) * angstrom - [1, 2, 3, 4] * angstrom)

        quantity = np.array([1, 2, 3, 4]) * angstrom
        quantity = quantity - [1, 2, 3, 4] * nanometer
        assert quantity[0] == -9 * angstrom
        assert quantity[-1] == -36 * angstrom

        quantity = np.array([1, 2, 3, 4]) * angstrom
        quantity -= np.array([1, 2, 3, 4])
        assert quantity[0] == 0 * angstrom
        assert quantity[-1] == 0 * angstrom
        assert isArrayEqual(quantity, np.array([1, 2, 3, 4]) * angstrom - np.array([1, 2, 3, 4]) * angstrom)

        quantity = np.array([1, 2, 3, 4]) * angstrom
        quantity -= np.array([1, 2, 3, 4]) * nanometer
        assert quantity[0] == -9 * angstrom
        assert quantity[-1] == -36 * angstrom
        
        # __rsub__
        quantity = np.array([1, 2, 3, 4]) * angstrom
        quantity = 1 - quantity 
        assert quantity[0] == 0 * angstrom
        assert quantity[-1] == -3 * angstrom
        assert isArrayEqual(quantity, 1 * angstrom - np.array([1, 2, 3, 4]) * angstrom)

        quantity = np.array([1, 2, 3, 4]) * angstrom
        quantity = 1 * nanometer - quantity
        assert quantity[0] == 9 * angstrom
        assert quantity[-1] == 6 * angstrom

        quantity = np.array([1, 2, 3, 4]) * angstrom
        quantity = [1, 2, 3, 4] - quantity
        assert quantity[0] == 0 * angstrom
        assert quantity[-1] == 0 * angstrom
        assert isArrayEqual(quantity, [1, 2, 3, 4] * angstrom - np.array([1, 2, 3, 4]) * angstrom)

        quantity = np.array([1, 2, 3, 4]) * angstrom
        quantity = [1, 2, 3, 4] * nanometer - quantity
        assert quantity[0] == 9 * angstrom
        assert quantity[-1] == 36 * angstrom

        quantity = np.array([1, 2, 3, 4]) * angstrom
        quantity = np.array([1, 2, 3, 4]) - quantity
        assert quantity[0] == 0 * angstrom
        assert quantity[-1] == 0 * angstrom
        assert isArrayEqual(quantity, np.array([1, 2, 3, 4]) * angstrom - np.array([1, 2, 3, 4]) * angstrom)

        quantity = np.array([1, 2, 3, 4]) * angstrom
        quantity = np.array([1, 2, 3, 4]) * nanometer - quantity
        assert quantity[0] == 9 * angstrom
        assert quantity[-1] == 36 * angstrom

        # Different unit
        quantity1 = np.array([1, 2]) * angstrom
        quantity2 = np.array([2, 1]) * second
        with pytest.raises(ValueError):
            quantity1 - quantity2

    def test_mul(self):
        # __mul__
        quantity = np.array([1, 2, 3, 4]) * angstrom
        quantity = quantity * 2
        assert quantity[0] == 2 * angstrom
        assert quantity[-1] == 8 * angstrom
        assert isArrayEqual(quantity, np.array([1, 2, 3, 4]) * angstrom * 2)

        quantity = np.array([1, 2, 3, 4]) * angstrom
        quantity = quantity * [1, 2, 3, 4]
        assert quantity[0] == 1 * angstrom
        assert quantity[-1] == 16 * angstrom

        # __imul__
        quantity = np.array([1, 2, 3, 4]) * angstrom
        quantity *= 2
        assert quantity[0] == 2 * angstrom
        assert quantity[-1] == 8 * angstrom
        assert isArrayEqual(quantity, np.array([1, 2, 3, 4]) * angstrom * 2)

        quantity = np.array([1, 2, 3, 4]) * angstrom
        quantity *= [1, 2, 3, 4]
        assert quantity[0] == 1 * angstrom
        assert quantity[-1] == 16 * angstrom

        # __rmul__
        quantity = np.array([1, 2, 3, 4]) * angstrom
        quantity = 2 * quantity
        assert quantity[0] == 2 * angstrom
        assert quantity[-1] == 8 * angstrom
        assert isArrayEqual(quantity, 2 * np.array([1, 2, 3, 4]) * angstrom)

        quantity = np.array([1, 2, 3, 4]) * angstrom
        quantity = [1, 2, 3, 4] * quantity
        assert quantity[0] == 1 * angstrom
        assert quantity[-1] == 16 * angstrom

        # dot
        quantity = np.array([1, 2, 3, 4]) * angstrom
        quantity = quantity.dot(np.array([1, 2, 3, 4]))
        assert quantity == 1 + 4 + 9 + 16 * angstrom

        # mixture
        quantity1 = 1 * nanometer
        quantity2 = 1 * nanosecond
        quantity = quantity1 * quantity2
        assert quantity.value == 1
        assert quantity.unit.base_dimension == BaseDimension(length_dimension=1, time_dimension=1)
        assert quantity.unit.relative_value == 1e-18

    def test_div(self):
        # __div__
        quantity = np.array([1, 2, 3, 4]) * angstrom
        quantity = quantity / 2
        assert quantity[0] == 0.5 * angstrom
        assert quantity[-1] == 2 * angstrom
        assert isArrayEqual(quantity, np.array([1, 2, 3, 4]) * angstrom / 2)

        quantity = np.array([1, 2, 3, 4]) * angstrom
        quantity = quantity / [1, 2, 3, 4]
        assert quantity[0] == 1 * angstrom
        assert quantity[-1] == 1 * angstrom

        # __idiv__
        quantity = np.array([1, 2, 3, 4]) * angstrom
        quantity /= 2
        assert quantity[0] == 0.5 * angstrom
        assert quantity[-1] == 2 * angstrom
        assert isArrayEqual(quantity, np.array([1, 2, 3, 4]) * angstrom / 2)

        quantity = np.array([1, 2, 3, 4]) * angstrom
        quantity /= [1, 2, 3, 4]
        assert quantity[0] == 1 * angstrom
        assert quantity[-1] == 1 * angstrom

        # __rdiv__
        quantity = np.array([1, 2, 3, 4]) * angstrom
        quantity = 2 / quantity
        assert quantity[0] == 2 * angstrom**-1
        assert quantity[-1] == 0.5 * angstrom**-1
        assert isArrayEqual(quantity, 2 / (np.array([1, 2, 3, 4]) * angstrom))

        quantity = np.array([1, 2, 3, 4]) * angstrom
        quantity = [1, 2, 3, 4] / quantity
        assert quantity[0] == 1 * angstrom**-1
        assert quantity[-1] == 1 * angstrom**-1

        # mixture
        quantity1 = 1 * nanometer
        quantity2 = 1 * nanosecond
        quantity = quantity1 / quantity2
        assert quantity.value == 1
        assert quantity.unit.base_dimension == BaseDimension(length_dimension=1, time_dimension=-1)
        assert quantity.unit.relative_value == 1

        quantity = quantity1 / quantity1
        assert quantity == 1

        # divide 0
        with pytest.raises(ValueError):
            quantity = 1 * nanometer
            quantity / 0

        with pytest.raises(ValueError):
            quantity = 0 * nanometer
            1 / quantity

        with pytest.raises(ValueError):
            quantity1 = 0 * nanometer
            quantity2 = 1 * second
            quantity2 / quantity1

    def test_pow(self):
        quantity = np.array([1, 2, 3, 4]) * angstrom
        quantity = quantity**2
        assert quantity[0] == 1 * angstrom**2
        assert quantity[-1] == 16 * angstrom**2

        quantity = np.array([1, 2, 3, 4]) * angstrom
        quantity = quantity**0
        assert quantity[0] == 1
        assert quantity[-1] == 1

        quantity = np.array([1, 2, 3, 4]) * angstrom
        quantity = quantity**-2
        assert quantity[0] == 1  * angstrom**-2
        assert quantity[-1] == 1/16 * angstrom**-2


