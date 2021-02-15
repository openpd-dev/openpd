import pytest
from ..unit import BaseDimension, Unit

class TestUnit:
    def setup(self):
        self.unit = Unit(BaseDimension(length_dimension=1), 1e-10)

    def teardown(self):
        self.unit = None

    def test_attributes(self):
        assert self.unit.unit_name == 'm'
        assert self.unit.base_dimension == BaseDimension(length_dimension=1)
        assert self.unit.relative_value == 1e-10

    def test_exceptions(self):
        with pytest.raises(AttributeError):
            self.unit.unit_name = 1
        
        with pytest.raises(AttributeError):
            self.unit.base_dimension = 1

        with pytest.raises(AttributeError):
            self.unit.relative_value = 1        

    def test_isDimensionLess(self):
        assert not self.unit.isDimensionLess()
        assert BaseDimension().isDimensionLess()

    def test_setRelativeValueToOne(self):
        self.unit.setRelativeValueToOne()
        assert self.unit.relative_value == 1

    def test_add(self):
        angstrom = Unit(BaseDimension(length_dimension=1), 1e-10)
        gram = Unit(BaseDimension(mass_dimension=1), 1e-3)
        assert angstrom + angstrom == angstrom
        assert 1 + angstrom == angstrom
        assert angstrom + 1 == angstrom

        with pytest.raises(ValueError):
            gram + angstrom

    def test_sub(self):
        angstrom = Unit(BaseDimension(length_dimension=1), 1e-10)
        gram = Unit(BaseDimension(mass_dimension=1), 1e-3)
        assert angstrom - angstrom == angstrom
        assert 1 - angstrom == angstrom
        assert angstrom - 1 == angstrom

        with pytest.raises(ValueError):
            gram - angstrom

    def test_mul(self):
        angstrom = Unit(BaseDimension(length_dimension=1), 1e-10)
        angstrom_square = Unit(BaseDimension(length_dimension=2), 1e-20)
        assert angstrom * 1 == angstrom
        assert 1 * angstrom == angstrom
        assert angstrom * angstrom == angstrom_square

    def test_div(self):
        angstrom_reciprocal = Unit(BaseDimension(length_dimension=-1), 1e10)
        angstrom = Unit(BaseDimension(length_dimension=1), 1e-10)
        angstrom_square = Unit(BaseDimension(length_dimension=2), 1e-20)
        assert angstrom / 1 == angstrom
        assert 1 / angstrom == angstrom_reciprocal
        assert angstrom_square / angstrom == angstrom
        assert angstrom / angstrom_square == angstrom_reciprocal
        assert (angstrom / angstrom).isDimensionLess()

    def test_pow(self):
        constant = Unit(BaseDimension(), 1)
        angstrom_reciprocal = Unit(BaseDimension(length_dimension=-1), 1e10)
        angstrom = Unit(BaseDimension(length_dimension=1), 1e-10)
        angstrom_square = Unit(BaseDimension(length_dimension=2), 1e-20)
        assert angstrom_square == angstrom**2
        assert angstrom == angstrom**1
        assert constant == angstrom**0
        assert angstrom_reciprocal == angstrom**-1