import pytest, os
import numpy as np
from .. import PDFFBondForce, SequenceLoader, Ensemble
from .. import isAlmostEqual, isArrayEqual, getBond, getUnitVec
from ..unit import *
from ..exceptions import NonboundError, RebindError

cur_dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
force_field_dir = os.path.join(cur_dir, '../data/pdff/bond')

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
        
        with pytest.raises(NonboundError):
            self.force._testBound()

        with pytest.raises(RebindError):
            self.force.bindEnsemble(self.ensemble)
            self.force.bindEnsemble(self.ensemble)

    def test_setForceFieldVector(self):
        self.force.bindEnsemble(self.ensemble)
        assert self.force.force_field_vector.shape[0] == 3
        asn_potential = np.load(os.path.join(force_field_dir, 'ASN.npz'))
        assert self.force.force_field_vector[0].getEnergy(asn_potential['energy_coord'][10])/kilojoule_permol == pytest.approx(asn_potential['energy_data'][10])
        ca_potential = np.load(os.path.join(force_field_dir, 'CA-CA.npz'))
        assert self.force.force_field_vector[1].getEnergy(ca_potential['energy_coord'][10])/kilojoule_permol == pytest.approx(ca_potential['energy_data'][10])

    def test_calculateBondEnergy(self):
        self.force.bindEnsemble(self.ensemble)
        bond_length0 = getBond(
            self.system.topology.bonds[0][0].coordinate,
            self.system.topology.bonds[0][1].coordinate,
        ) / angstrom
        assert isAlmostEqual(
            self.force.calculateBondEnergy(0),
            self.force.force_field_vector[0].getEnergy(bond_length0)
        )
        bond_length1 = getBond(
            self.system.topology.bonds[1][0].coordinate,
            self.system.topology.bonds[1][1].coordinate
        ) / angstrom
        assert isAlmostEqual(
            self.force.calculateBondEnergy(1),
            self.force.force_field_vector[1].getEnergy(bond_length1)
        )

    def test_calculatePotentialEnergy(self):
        self.force.bindEnsemble(self.ensemble)

        bond_length0 = getBond(
            self.system.topology.bonds[0][0].coordinate,
            self.system.topology.bonds[0][1].coordinate
        ) / angstrom
        energy_bond0 = self.force.force_field_vector[0].getEnergy(bond_length0)
        bond_length1 = getBond(
            self.system.topology.bonds[1][0].coordinate,
            self.system.topology.bonds[1][1].coordinate
        ) / angstrom
        energy_bond1 = self.force.force_field_vector[1].getEnergy(bond_length1)
        bond_length2 = getBond(
            self.system.topology.bonds[2][0].coordinate,
            self.system.topology.bonds[2][1].coordinate
        ) / angstrom
        energy_bond2 = self.force.force_field_vector[2].getEnergy(bond_length2)

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
            self.force.calculateAtomForce(0), (
                0.5 * self.force.force_field_vector[0].getForce(bond_length0) * vec0 +
                0.5 * self.force.force_field_vector[1].getForce(bond_length1) * vec1   
            )
        )

        assert isArrayEqual(
            self.force.calculateAtomForce(1), (
                0.5 * self.force.force_field_vector[0].getForce(bond_length0) * -vec0 
            )
        )

        assert isArrayEqual(
            self.force.calculateAtomForce(2), (
                0.5 * self.force.force_field_vector[1].getForce(bond_length1) * -vec1 +
                0.5 * self.force.force_field_vector[2].getForce(bond_length2) * vec2
            )
        )

        assert isArrayEqual(
            self.force.calculateAtomForce(3), (
                0.5 * self.force.force_field_vector[2].getForce(bond_length2) * -vec2
            )
        )