import pytest, os, codecs, json
from .. import PDFFBondForceField
from .. import isAlmostEqual
from ..unit import *

cur_dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
force_field_dir = os.path.join(cur_dir, '../data/pdff/bond')

with codecs.open(os.path.join(force_field_dir, 'Ca-SC.json'), 'r', 'utf-8') as f:
    ca_sc_text = f.read()
with codecs.open(os.path.join(force_field_dir, 'Ca-Ca.json'), 'r', 'utf-8') as f:
    ca_ca_text = f.read()

CA_SC_JSON_FILE = json.loads(ca_sc_text)
CA_CA_JSON_FILE = json.loads(ca_ca_text)

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
            0.5 * (4-2.6)**2 * CA_SC_JSON_FILE["ASN"]["k"] * kilojoule_permol
        )

    def test_getForce(self):
        assert self.force_field.getForce(2.6) == 0 * kilojoule_permol_over_angstrom
        assert isAlmostEqual(
            self.force_field.getForce(4),
            - CA_SC_JSON_FILE["ASN"]["k"] * (4-2.6) * kilojoule_permol_over_angstrom
        )

