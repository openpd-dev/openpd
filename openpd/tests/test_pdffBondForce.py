import pytest, os, codecs, json
from .. import PDFFBondForce, SequenceLoader, Ensemble
from .. import isAlmostEqual, isArrayEqual, getBond, getUnitVec
from ..unit import *

cur_dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
force_field_dir = os.path.join(cur_dir, '../data/pdff/bond')

with codecs.open(os.path.join(force_field_dir, 'Ca-SC.json'), 'r', 'utf-8') as f:
    ca_sc_text = f.read()
with codecs.open(os.path.join(force_field_dir, 'Ca-Ca.json'), 'r', 'utf-8') as f:
    ca_ca_text = f.read()

CA_SC_JSON_FILE = json.loads(ca_sc_text)
CA_CA_JSON_FILE = json.loads(ca_ca_text)

class TestPDFFBondForce:
    def setup(self):
        self.system = SequenceLoader(os.path.join(cur_dir, 'data/testPDFFBondForce.json')).createSystem()
        self.ensemble = Ensemble(self.system)
        self.force = PDFFBondForce()

    def teardown(self):
        self.system = None
        self.ensemble = None
        self.force = None

    def test_attributes(self):
        assert self.force.num_bonds == 0
        assert self.force._potential_energy == 0
        assert self.force._force_field_vector == None

    def test_exceptions(self):
        with pytest.raises(AttributeError):
            self.force.num_bonds = 1

        with pytest.raises(AttributeError):
            self.force.potential_energy = 1

        with pytest.raises(AttributeError):
            self.force.force_field_vector = 1
        
        with pytest.raises(AttributeError):
            self.force._testBound()

        with pytest.raises(AttributeError):
            self.force.bindEnsemble(self.ensemble)
            self.force.bindEnsemble(self.ensemble)

    def test_setForceFieldVector(self):
        self.force.bindEnsemble(self.ensemble)
        assert self.force.force_field_vector.shape[0] == 3
        assert self.force.force_field_vector[0].getEnergy(2.6) == 0 * kilojoule_permol
        assert self.force.force_field_vector[1].getEnergy(3.85) == 0 * kilojoule_permol

    def test_calculateBondEnergy(self):
        self.force.bindEnsemble(self.ensemble)
        bond_length = getBond(
            self.system.topology.bonds[0][0].coordinate,
            self.system.topology.bonds[0][1].coordinate,
        ) / angstrom
        assert isAlmostEqual(
            self.force.calculateBondEnergy(0),
            0.5 * (bond_length-2.6)**2 * CA_SC_JSON_FILE["ASN"]["k"] * kilojoule_permol
        )
        assert self.force.calculateBondEnergy(1)/kilojoule_permol == pytest.approx(0)

    def test_calculatePotentialEnergy(self):
        self.force.bindEnsemble(self.ensemble)

        bond_length0 = getBond(
            self.system.topology.bonds[0][0].coordinate,
            self.system.topology.bonds[0][1].coordinate
        ) / angstrom
        energy_bond0 = 0.5 * (bond_length0-2.6)**2 * CA_SC_JSON_FILE["ASN"]["k"] * kilojoule_permol
        energy_bond1 = 0 * kilojoule_permol
        bond_length2 = getBond(
            self.system.topology.bonds[2][0].coordinate,
            self.system.topology.bonds[2][1].coordinate
        ) / angstrom
        energy_bond2 = 0.5 * (bond_length2-2.6)**2 * CA_SC_JSON_FILE["ASN"]["k"] * kilojoule_permol

        assert isAlmostEqual(
            self.force.calculatePotentialEnergy(),
            energy_bond0 + energy_bond1 + energy_bond2
        )
        assert isAlmostEqual(
            self.force.potential_energy,
            energy_bond0 + energy_bond1 + energy_bond2
        )

    def test_calculateAtomForce(self):
        self.force.bindEnsemble(self.ensemble)

        bond_length0 = getBond(
            self.system.topology.bonds[0][0].coordinate,
            self.system.topology.bonds[0][1].coordinate
        ) / angstrom
        vec0 = getUnitVec(
            self.system.topology.bonds[0][0].coordinate -
            self.system.topology.bonds[0][1].coordinate
        )
        bond_length1 = getBond(
            self.system.topology.bonds[1][0].coordinate,
            self.system.topology.bonds[1][1].coordinate
        ) / angstrom
        vec1 = getUnitVec(
            self.system.topology.bonds[1][0].coordinate -
            self.system.topology.bonds[1][1].coordinate
        )
        bond_length2 = getBond(
            self.system.topology.bonds[2][0].coordinate,
            self.system.topology.bonds[2][1].coordinate
        ) / angstrom
        vec2 = getUnitVec(
            self.system.topology.bonds[2][0].coordinate -
            self.system.topology.bonds[2][1].coordinate
        )

        assert isArrayEqual(
            self.force.calculateAtomForce(0),
            (
                0.5 * self.force.force_field_vector[0].getForce(bond_length0) * vec0 +
                0.5 * self.force.force_field_vector[1].getForce(bond_length1) * vec1   
            )
        )

        assert isArrayEqual(
            self.force.calculateAtomForce(1),
            (
                0.5 * self.force.force_field_vector[0].getForce(bond_length0) * -vec0 
            )
        )

        assert isArrayEqual(
            self.force.calculateAtomForce(2),
            (
                0.5 * self.force.force_field_vector[1].getForce(bond_length1) * -vec1 +
                0.5 * self.force.force_field_vector[2].getForce(bond_length2) * vec2
            )
        )

        assert isArrayEqual(
            self.force.calculateAtomForce(3),
            (
                0.5 * self.force.force_field_vector[2].getForce(bond_length2) * -vec2
            )
        )