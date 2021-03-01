import pytest
import numpy as np
from .. import PDFFBondForceField
from .. import isAlmostEqual
from ..unit import *

class TestPDFFBondForceField:
    def setup(self):
        self.force_field = PDFFBondForceField('ASN', 'ASN')

    def teardown(self):
        self.force_field = None

    def test_attributes(self):
        assert self.force_field.name == 'ASN Ca-SC bond'
        assert self.force_field._key == 'ASN'

    def test_excpetions(self):
        with pytest.raises(AttributeError):
            self.force_field.name = 1

        with pytest.raises(ValueError):
            PDFFBondForceField('AS', 'AS')

    def test_getEnergy(self):
        assert self.force_field.getEnergy(2.6) == 0 * kilojoule_permol
        assert isAlmostEqual(
            self.force_field.getEnergy(4),
            0.5 * (4-2.6)**2 * 100 * kilojoule_permol
        )

    def test_getForce(self):
        assert self.force_field.getForce(2.6) == 0 * kilojoule_permol_over_angstrom
        assert isAlmostEqual(
            self.force_field.getForce(4),
            - 100 * (4-2.6) * kilojoule_permol_over_angstrom
        )

