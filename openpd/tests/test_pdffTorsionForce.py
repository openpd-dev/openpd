import pytest, os
import numpy as np
from .. import PDFFTorsionForce, Peptide
from .. import isArrayEqual

cur_dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
force_field_dir = os.path.join(cur_dir, '../data/pdff/torsion')

class TestPDFFTorsionForce:
    def setup(self):
        self.force = PDFFTorsionForce()

    def teardown(self):
        self.force = None

    def test_attributes(self):
        energy_coordinate = np.load(os.path.join(force_field_dir, 'coord.npy'))

        assert self.force.force_id == 0
        assert self.force.force_group == 0
        assert self.force.num_torsions == 0
        assert self.force.torsions == []
        assert self.force.torsion_types == []
        assert self.force.energy_array == None
        assert isArrayEqual(self.force.energy_coordinate, energy_coordinate)

    def test_exceptions(self):
        with pytest.raises(AttributeError):
            self.force.num_torsions = 1
        
        with pytest.raises(AttributeError):
            self.force.torsions = 1

        with pytest.raises(AttributeError):
            self.force.torsion_types = 1

        with pytest.raises(AttributeError):
            self.force.energy_array = 1

        with pytest.raises(AttributeError):
            self.force.energy_coordinate = 1

    def test_loadForceField(self):
        asn_leu_energy = np.load(os.path.join(force_field_dir, 'ASN-LEU.npy'))
        #assert isArrayEqual(self.force.loadEnergyVector('ASN', 'LEU'), asn_leu_energy)
        #assert isArrayEqual(self.force.loadEnergyVector('LEU', 'ASN'), asn_leu_energy)

        with pytest.raises(ValueError):
            self.force.loadForceField('AS', 'AS')

    def test_addTorsion(self):
        peptide1 = Peptide('ASN')
        peptide2 = Peptide('LEU')
        torsion = [peptide1.atoms[1], peptide1.atoms[0], peptide2.atoms[0], peptide2.atoms[1]]
        self.force._addTorsion(torsion)
        
        assert self.force.num_torsions == 1
        assert isArrayEqual(self.force.torsion_types[0], ['ASN', 'LEU'])

    def test_addTorsions(self):
        peptide1 = Peptide('ASN')
        peptide2 = Peptide('LEU')
        torsion1 = [peptide1.atoms[1], peptide1.atoms[0], peptide2.atoms[0], peptide2.atoms[1]]
        peptide1 = Peptide('ASN')
        peptide2 = Peptide('LEU')
        torsion2 = [peptide2.atoms[1], peptide2.atoms[0], peptide1.atoms[0], peptide1.atoms[1]]

        self.force.addTorsions(torsion1, torsion2)
        assert self.force.num_torsions == 2
        assert isArrayEqual(self.force.torsion_types[0], ['ASN', 'LEU'])
        assert isArrayEqual(self.force.torsion_types[1], ['LEU', 'ASN'])

        self.force.addTorsions(torsion2, torsion1)
        assert self.force.num_torsions == 4
        assert isArrayEqual(self.force.torsion_types[2], ['LEU', 'ASN'])
        assert isArrayEqual(self.force.torsion_types[3], ['ASN', 'LEU'])

    def test_setEnergyVector(self):
        peptide1 = Peptide('ASN')
        peptide2 = Peptide('LEU')
        torsion1 = [peptide1.atoms[1], peptide1.atoms[0], peptide2.atoms[0], peptide2.atoms[1]]
        peptide1 = Peptide('ASN')
        peptide2 = Peptide('LEU')
        torsion2 = [peptide2.atoms[1], peptide2.atoms[0], peptide1.atoms[0], peptide1.atoms[1]]
        asn_leu_energy = np.load(os.path.join(force_field_dir, 'ASN-LEU.npy'))

        self.force.addTorsions(torsion1)
        self.force.setEnergyVector()

        self.force.addTorsions(torsion2)
        self.force.setEnergyVector()


    # todo: test_calculateEnergy
    def test_calculateEnergy(self):
        pass

    # todo: test_calculateForce
    def test_calculateForce(self):
        pass
