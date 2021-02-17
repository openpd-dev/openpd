import pytest, os
import numpy as np
from numpy import pi
from .. import PDFFTorsionForceField
from .. import findFirstLambda, findAll, findAllLambda, isAlmostEqual, isArrayEqual

cur_dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
force_field_dir = os.path.join(cur_dir, '../data/pdff/torsion')

class TestPDFFTorsionForce:
    def setup(self):
        self.force_field = PDFFTorsionForceField('ASN', 'LEU')

    def teardown(self):
        pass

    def test_attributes(self):
        assert self.force_field.name == 'ASN-LEU'
        assert isArrayEqual(self.force_field.target_coord, np.linspace(-pi, pi, 600))

    def test_exceptions(self):
        with pytest.raises(AttributeError):
            self.force_field.name = 1
        
        with pytest.raises(AttributeError):
            self.force_field.target_coord = 1

        with pytest.raises(AttributeError):
            self.force_field.target_data = 1