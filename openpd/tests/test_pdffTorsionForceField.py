from openpd.utils.judgement import isAlmostEqual
import pytest, os
import numpy as np
from numpy import pi
from .. import PDFFTorsionForceField
from .. import isArrayEqual
from ..unit import *
from ..exceptions import PeptideTypeError, NotincludedInteractionError

cur_dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
force_field_dir = os.path.join(cur_dir, '../data/pdff/torsion')

class TestPDFFTorsionForceField:
    def setup(self):
        self.force_field = PDFFTorsionForceField('ASN', 'LEU')

    def teardown(self):
        pass

    def test_attributes(self):
        assert self.force_field.name == 'ASN-LEU'

    def test_exceptions(self):
        with pytest.raises(AttributeError):
            self.force_field.name = 1

        with pytest.raises(PeptideTypeError):
            PDFFTorsionForceField('ASN', 'LU')

        # not include A-A, A can pass isStandardPeptide
        with pytest.raises(NotincludedInteractionError):
            PDFFTorsionForceField('A', 'A')

    def test_getEnergy(self):
        asn_leu = np.load(os.path.join(force_field_dir, 'ASN-LEU.npz'))
        assert (
            self.force_field.getEnergy(asn_leu['energy_coord'][2]) / kilojoule_permol ==
            pytest.approx(asn_leu['energy_data'][2])
        )
        self.force_field.getEnergy(np.pi)
        self.force_field.getEnergy(-np.pi)
        
    def test_getForce(self):
        asn_leu = np.load(os.path.join(force_field_dir, 'ASN-LEU.npz'))
        assert isAlmostEqual(
            self.force_field.getForce(asn_leu['force_coord'][300]),
            asn_leu['force_data'][300]
        )
        
        self.force_field.getForce(np.pi)
        self.force_field.getForce(-np.pi)