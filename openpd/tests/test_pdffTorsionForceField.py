from openpd.utils.judgement import isAlmostEqual
import pytest, os
import numpy as np
from numpy import pi
from .. import PDFFTorsionForceField
from .. import isArrayEqual
from ..unit import *

cur_dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
force_field_dir = os.path.join(cur_dir, '../data/pdff/torsion')

class TestPDFFTorsionForceField:
    def setup(self):
        self.force_field = PDFFTorsionForceField('ASN', 'LEU')

    def teardown(self):
        pass

    def test_attributes(self):
        assert self.force_field.name == 'ASN-LEU'
        assert isArrayEqual(self.force_field._target_coord, np.arange(-pi, pi+0.001, 0.001))
        assert self.force_field.derivative_width == 0.0001

    def test_exceptions(self):
        with pytest.raises(AttributeError):
            self.force_field.name = 1
            
        with pytest.raises(AttributeError):
            self.force_field.derivative_width = 1

    def test_getEnergy(self):
        asn_leu_force_field = np.load(os.path.join(force_field_dir, 'ASN-LEU.npy'))
        coord = np.load(os.path.join(force_field_dir, 'coord.npy'))
        assert (
            self.force_field.getEnergy(coord[2]) / kilojoule_permol ==
            pytest.approx(asn_leu_force_field[2])
        )
        
    def test_getForce(self):
        coord = np.load(os.path.join(force_field_dir, 'coord.npy'))
        assert isAlmostEqual(
            self.force_field.getForce(coord[2]),
            - (
                self.force_field.getEnergy(coord[2]+0.5*self.force_field.derivative_width) - 
                self.force_field.getEnergy(coord[2]-0.5*self.force_field.derivative_width)
            ) / self.force_field.derivative_width / angstrom
        )