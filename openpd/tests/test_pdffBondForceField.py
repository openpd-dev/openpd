import pytest, os
import numpy as np
from .. import PDFFBondForceField
from ..unit import *
from ..exceptions import PeptideTypeError, NotincludedInteractionError

cur_dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
force_field_dir = os.path.join(cur_dir, '../data/pdff/bond')

class TestPDFFBondForceField:
    def setup(self):
        self.force_field = PDFFBondForceField('ASN', 'ASN')
        self.ca_force_filed = PDFFBondForceField('ASN', 'ASP')

    def teardown(self):
        self.force_field = None
        self.ca_force_filed = None

    def test_attributes(self):
        assert self.force_field.name == 'ASN Ca-SC bond'
        assert self.force_field._key == 'ASN'

    def test_excpetions(self):
        with pytest.raises(AttributeError):
            self.force_field.name = 1

        with pytest.raises(PeptideTypeError):
            PDFFBondForceField('AS', 'AS')

        # not include A.npz, A can pass isStandardPeptide
        with pytest.raises(NotincludedInteractionError):
            PDFFBondForceField('A', 'A')

    def test_getEnergy(self):
        data = np.load(os.path.join(force_field_dir, 'ASN.npz'))
        assert self.force_field.getEnergy(data['energy_coord'][30]) / kilojoule_permol == pytest.approx(data['energy_data'][30])
        data = np.load(os.path.join(force_field_dir, 'CA-CA.npz'))
        assert self.ca_force_filed.getEnergy(data['energy_coord'][30]) / kilojoule_permol == pytest.approx(data['energy_data'][30])

    def test_getForce(self):
        data = np.load(os.path.join(force_field_dir, 'ASN.npz'))
        assert self.force_field.getForce(data['force_coord'][30]) / kilojoule_permol_over_angstrom == pytest.approx(data['force_data'][30])
        data = np.load(os.path.join(force_field_dir, 'CA-CA.npz'))
        assert self.ca_force_filed.getForce(data['force_coord'][30]) / kilojoule_permol_over_angstrom == pytest.approx(data['force_data'][30])


