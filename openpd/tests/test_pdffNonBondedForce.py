import pytest, os
import numpy as np
from .. import PDFFNonbondedForce, Peptide, isArrayEqual
from ..force.pdffNonBondedForce import CONSTANT_ENERGY_VECTOR_LENGTH

cur_dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
force_field_dir = os.path.join(cur_dir, '../data/pdff/nonbonded')

class TestNonBondedForce:
    def setup(self):
        self.force = PDFFNonbondedForce()

    def teardown(self):
        self.force = None

    def test_attributes(self):
        assert self.force.num_peptides == 0
        assert self.force.peptides == []

        assert self.force.cutoff_radius == 12

        assert self.force.energy_tensor == None

        energy_coordinate = np.load(os.path.join(force_field_dir, 'coord.npy'))
        assert isArrayEqual(self.force.energy_coordinate, energy_coordinate)

    def test_exceptions(self):
        with pytest.raises(AttributeError):
            self.force.num_peptides = 1

        with pytest.raises(AttributeError):
            self.force.peptides = 1
        
        with pytest.raises(AttributeError):
            self.force.cutoff_radius = 1

        with pytest.raises(AttributeError):
            self.force.energy_tensor = 1
        
        with pytest.raises(AttributeError):
            self.force.energy_coordinate = 1

        self.force._addPeptide(Peptide('ASN'))
        with pytest.raises(AttributeError):
            self.force.setEnergyTensor()

    def test_loadEnergyVector(self):
        energy_vector = np.load(os.path.join(force_field_dir, 'ASN-ASP.npy'))

        assert energy_vector.shape[0] == CONSTANT_ENERGY_VECTOR_LENGTH

        assert isArrayEqual(self.force.loadEnergyVector(Peptide('ASN'), Peptide('ASP')), 
            energy_vector)

        assert isArrayEqual(self.force.loadEnergyVector(Peptide('ASP'), Peptide('ASN')), 
            energy_vector)

        with pytest.raises(ValueError):
            self.force.loadEnergyVector(Peptide('ASN'), Peptide('ALA'))

    def test_addPeptide(self):
        self.force._addPeptide(Peptide('ASN'))

        assert self.force.num_peptides == 1

    def test_setEnergyTensor(self):
        self.force._addPeptide(Peptide('ASN'))
        self.force._addPeptide(Peptide('LEU'))
        self.force._addPeptide(Peptide('TYR'))
        self.force.setEnergyTensor()
        asn_leu_energy_vector = np.load(os.path.join(force_field_dir, 'ASN-LEU.npy'))

        assert self.force.energy_tensor.shape[0] == 3
        assert self.force.energy_tensor.shape[1] == 3
        assert self.force.energy_tensor.shape[2] == CONSTANT_ENERGY_VECTOR_LENGTH
        assert isArrayEqual(self.force.energy_tensor[0, 0, :], np.zeros(CONSTANT_ENERGY_VECTOR_LENGTH))
        assert isArrayEqual(self.force.energy_tensor[1, 2, :], self.force.energy_tensor[2, 1, :])
        assert isArrayEqual(self.force.energy_tensor[0, 1, :], asn_leu_energy_vector)

        self.force._addPeptide(Peptide('ASN'))
        self.force._addPeptide(Peptide('LEU'))
        self.force._addPeptide(Peptide('TYR'))
        self.force.setEnergyTensor()
        asn_leu_energy_vector = np.load(os.path.join(force_field_dir, 'ASN-LEU.npy'))

        assert self.force.energy_tensor.shape[0] == 6
        assert self.force.energy_tensor.shape[1] == 6
        assert self.force.energy_tensor.shape[2] == CONSTANT_ENERGY_VECTOR_LENGTH
        assert isArrayEqual(self.force.energy_tensor[3, 3, :], np.zeros(CONSTANT_ENERGY_VECTOR_LENGTH))
        assert isArrayEqual(self.force.energy_tensor[4, 5, :], self.force.energy_tensor[5, 4, :])
        assert isArrayEqual(self.force.energy_tensor[3, 4, :], asn_leu_energy_vector)

    def test_addPeptides(self):
        self.force.addPeptides(Peptide('ASN'), Peptide('LEU'))

        assert self.force.num_peptides == 2

        self.force.addPeptides(Peptide('TYR'), Peptide('LEU'))
        asn_leu_energy_vector = np.load(os.path.join(force_field_dir, 'ASN-LEU.npy'))
        leu_leu_energy_vector = np.load(os.path.join(force_field_dir, 'LEU-LEU.npy'))

        assert self.force.num_peptides == 4
        self.force.setEnergyTensor()
        assert isArrayEqual(self.force.energy_tensor[3, 3, :], np.zeros(CONSTANT_ENERGY_VECTOR_LENGTH))
        assert isArrayEqual(self.force.energy_tensor[0, 3, :], asn_leu_energy_vector)
        assert isArrayEqual(self.force.energy_tensor[3, 1, :], leu_leu_energy_vector)

    # todo: test_calculateEnergy
    def test_calculateEnergy(self):
        peptide1 = Peptide('ASN', 0)
        peptide1.atoms[0].coordinate = [2, 1, 1]
        peptide2 = Peptide('ASP', 1)
        peptide2.atoms[0].coordinate = [0, 0, 0]
        self.force.addPeptides(peptide1, peptide2)
        self.force.setEnergyTensor()
        # print(self.force.calculateEnergy(0, 1))

    # todo: test_calculateForce
    def test_calculateForce(self):
        pass
