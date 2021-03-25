import pytest, os
import numpy as np
from .. import PDFFNonBondedForceField, PDFFNonBondedForce, SequenceLoader, Ensemble
from .. import isAlmostEqual, isArrayEqual, isArrayAlmostEqual, getBond, getUnitVec
from ..unit import *
from ..exceptions import NonboundError, RebindError

cur_dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
force_field_dir = os.path.join(cur_dir, '../data/pdff/nonbonded')

class TestPDFFNonBondedForce:
    def setup(self):
        self.system = SequenceLoader(os.path.join(cur_dir, 'data/testForceEncoder.json')).createSystem()
        self.ensemble = Ensemble(self.system)
        self.force = PDFFNonBondedForce()

    def teardown(self):
        self.force = None

    def test_attributes(self):
        assert self.force.cutoff_radius == 12
        assert self.force.num_peptides == 0
        assert self.force.potential_energy == 0
        assert self.force.force_field_matrix == None

    def test_exceptions(self):
        with pytest.raises(AttributeError):
            self.force.cutoff_radius = 1

        with pytest.raises(AttributeError):
            self.force.num_peptides = 1
        
        with pytest.raises(AttributeError):
            self.force.potential_energy = 1

        with pytest.raises(AttributeError):
            self.force.force_field_matrix = 1

        with pytest.raises(AttributeError):
            system = SequenceLoader(os.path.join(cur_dir, 'data/testPDFFNonBondedForceException.json')).createSystem()
            self.force.bindEnsemble(Ensemble(system))

        with pytest.raises(NonboundError):
            self.force = PDFFNonBondedForce()
            self.force.calculateAtomForce(1)
            
        with pytest.raises(RebindError):
            system = SequenceLoader(os.path.join(cur_dir, 'data/testForceEncoder.json')).createSystem()
            self.force.bindEnsemble(self.ensemble)
            self.force.bindEnsemble(self.ensemble)

    def test_setForceFieldMatrix(self):
        self.force.bindEnsemble(self.ensemble)
        
        asn_leu_potential_data = np.load(os.path.join(force_field_dir, 'ASN-LEU.npz'))

        assert self.force.force_field_matrix[0, 0] == 0
        assert self.force.force_field_matrix[1, 0].getEnergy(2) == self.force.force_field_matrix[0, 1].getEnergy(2)

        assert (
            self.force.force_field_matrix[0, 1].getEnergy(asn_leu_potential_data['energy_coord'][50]) ==
             pytest.approx(asn_leu_potential_data['energy_data'][50], 1e-3)
        )

    def test_calculatePairEnergy(self):
        self.force.bindEnsemble(self.ensemble)
        
        asn_leu_force_field = PDFFNonBondedForceField('ASN', 'LEU')
        bond_length = getBond(
            self.force._peptides[0].atoms[1].coordinate, 
            self.force._peptides[1].atoms[1].coordinate, 
        )  / angstrom
        assert isAlmostEqual(
            self.force.calculatePairEnergy(0, 1), asn_leu_force_field.getEnergy(bond_length)
        ) 

        asn_tyr_force_field = PDFFNonBondedForceField('ASN', 'TYR')
        bond_length = getBond(
            self.force._peptides[0].atoms[1].coordinate, 
            self.force._peptides[2].atoms[1].coordinate, 
        )  / angstrom
        assert isAlmostEqual(
            self.force.calculatePairEnergy(0, 2), asn_tyr_force_field.getEnergy(bond_length)
        ) 

    def test_calculatePotentialEnergy(self):
        self.force.bindEnsemble(self.ensemble)
        
        asn_leu_force_field = PDFFNonBondedForceField('ASN', 'LEU')
        asn_tyr_force_field = PDFFNonBondedForceField('ASN', 'TYR')
        leu_tyr_force_field = PDFFNonBondedForceField('LEU', 'TYR')

        bond01 = getBond(
            self.force._peptides[0].atoms[1].coordinate, 
            self.force._peptides[1].atoms[1].coordinate, 
        )  / angstrom
        bond02 = getBond(
            self.force._peptides[0].atoms[1].coordinate, 
            self.force._peptides[2].atoms[1].coordinate, 
        )  / angstrom
        bond12 = getBond(
            self.force._peptides[1].atoms[1].coordinate, 
            self.force._peptides[2].atoms[1].coordinate, 
        )  / angstrom

        assert isAlmostEqual(
            self.force.calculatePotentialEnergy(),
            asn_tyr_force_field.getEnergy(bond02) 
        ) 
        assert isAlmostEqual(
            self.force.potential_energy,
            asn_tyr_force_field.getEnergy(bond02)
        ) 

        self.force._is_scale_14 = False

        assert isAlmostEqual(
            self.force.calculatePotentialEnergy(),
            (
                asn_leu_force_field.getEnergy(bond01) +
                asn_tyr_force_field.getEnergy(bond02) + 
                leu_tyr_force_field.getEnergy(bond12)
            )
        ) 
        assert isAlmostEqual(
            self.force.potential_energy,
            (
                asn_leu_force_field.getEnergy(bond01) +
                asn_tyr_force_field.getEnergy(bond02) + 
                leu_tyr_force_field.getEnergy(bond12)
            )
        ) 
        
    def test_calculateAtomForce(self):
        self.force.bindEnsemble(self.ensemble)
        
        system = self.force._ensemble.system

        assert isArrayEqual(self.force.calculateAtomForce(atom_id=0), [0, 0, 0])

        asn_leu_force_field = PDFFNonBondedForceField('ASN', 'LEU')
        asn_tyr_force_field = PDFFNonBondedForceField('ASN', 'TYR')

        bond13 = getBond(system.atoms[1].coordinate, system.atoms[3].coordinate)/angstrom
        if bond13 <= 12:
            force13 = asn_leu_force_field.getForce(bond13) * getUnitVec(system.atoms[3].coordinate - system.atoms[1].coordinate) * 0.5
        else:
            force13 = np.zeros([3]) * kilocalorie_permol_over_angstrom
        
        bond15 = getBond(system.atoms[1].coordinate, system.atoms[5].coordinate)/angstrom
        if bond15 <= 12:
            force15 = asn_tyr_force_field.getForce(bond15) * getUnitVec(system.atoms[5].coordinate - system.atoms[1].coordinate) * 0.5
        else:
            force15 = np.zeros([3]) * kilocalorie_permol_over_angstrom

        assert isArrayAlmostEqual(self.force.calculateAtomForce(atom_id=1), force15)

        self.force._is_scale_14 = False
        force = (force13+force15) 
        assert isArrayAlmostEqual(self.force.calculateAtomForce(atom_id=1), force)

