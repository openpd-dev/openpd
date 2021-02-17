import pytest, os
import numpy as np
from .. import PDFFNonBondedForceField, PDFFNonbondedForce, Peptide
from .. import isArrayEqual, isAlmostEqual, findFirstLambda, findAllLambda

cur_dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
force_field_dir = os.path.join(cur_dir, '../data/pdff/nonbonded')

class TestPDFFNonBondedForce:
    def setup(self):
        self.force = PDFFNonbondedForce()

    def teardown(self):
        self.force = None

    def test_attributes(self):
        assert self.force.num_peptides == 0
        assert self.force.peptides == []

        assert self.force.cutoff_radius == 12

        assert self.force.energy_matrix == None

        energy_coordinate = np.linspace(0, 30, 601)
        assert isArrayEqual(self.force.energy_coordinate, energy_coordinate)

    def test_exceptions(self):
        with pytest.raises(AttributeError):
            self.force.num_peptides = 1

        with pytest.raises(AttributeError):
            self.force.peptides = 1
        
        with pytest.raises(AttributeError):
            self.force.cutoff_radius = 1

        with pytest.raises(AttributeError):
            self.force.energy_matrix = 1
        
        with pytest.raises(AttributeError):
            self.force.energy_coordinate = 1

        self.force._addPeptide(Peptide('ASN'))
        with pytest.raises(AttributeError):
            self.force.setEnergyTensor()

    def test_loadForceField(self):
        force_field = self.force.loadForceField('ASN', 'ASP')
        origin_data = np.load(os.path.join(force_field_dir, 'ASN-ASP.npy'))
        origin_coord = np.load(os.path.join(force_field_dir, 'coord.npy'))

        assert force_field.target_data[findFirstLambda(lambda x: x<2.01 and x >1.99, force_field.target_coord)] == pytest.approx(force_field.getInterpolate()(2))
        assert isAlmostEqual(
            origin_data[findFirstLambda(lambda x: x<5.05 and x >4.95, origin_coord)],
            force_field.getInterpolate()(origin_coord[findFirstLambda(lambda x: x<5.05 and x >4.95, origin_coord)]), 5e-2
        )

        for i in findAllLambda(lambda x: x>12, force_field.target_coord):
            assert force_field.target_data[i] == 0

        # Test reverse order
        force_field = self.force.loadForceField('ASP', 'ASN')
        origin_data = np.load(os.path.join(force_field_dir, 'ASN-ASP.npy'))

        assert force_field.target_data[findFirstLambda(lambda x: x<2.01 and x >1.99, force_field.target_coord)] == pytest.approx(force_field.getInterpolate()(2))
        assert isAlmostEqual(
            force_field.getInterpolate()(origin_coord[findFirstLambda(lambda x: x<5.05 and x >4.95, origin_coord)]), 
            origin_data[findFirstLambda(lambda x: x<5.05 and x >4.95, origin_coord)], 5e-2
        )

        for i in findAllLambda(lambda x: x>12, force_field.target_coord):
            assert force_field.target_data[i] == 0

        with pytest.raises(ValueError):
            self.force.loadForceField(Peptide('ASN'), Peptide('ALA'))

    def test_addPeptide(self):
        self.force._addPeptide(Peptide('ASN'))

        assert self.force.num_peptides == 1

    def test_setEnergyMatrix(self):
        self.force._addPeptide(Peptide('ASN'))

        with pytest.raises(AttributeError):
            self.force.setEnergyMatrix()

        self.force._addPeptide(Peptide('LEU'))
        self.force._addPeptide(Peptide('TYR'))
        self.force.setEnergyMatrix()
        asn_leu_energy_vector = np.load(os.path.join(force_field_dir, 'ASN-LEU.npy'))
        origin_coord = np.load(os.path.join(force_field_dir, 'coord.npy'))

        assert self.force.energy_matrix[0, 0](19) == pytest.approx(0)
        assert self.force.energy_matrix[1, 0](2) == self.force.energy_matrix[0][1](2)
        assert isAlmostEqual(
            self.force.energy_matrix[0, 1](origin_coord[findFirstLambda(lambda x: x<3.05 and x >2.95, origin_coord)]), 
            asn_leu_energy_vector[findFirstLambda(lambda x: x<3.05 and x >2.95, origin_coord)], 1e-2
        )

        self.force._addPeptide(Peptide('ASN'))
        self.force._addPeptide(Peptide('LEU'))
        self.force._addPeptide(Peptide('TYR'))
        self.force.setEnergyMatrix()

        assert self.force.energy_matrix[4, 4](19) == pytest.approx(0)
        assert self.force.energy_matrix[4, 3](2) == self.force.energy_matrix[3][4](2)
        assert isAlmostEqual(
            self.force.energy_matrix[3, 4](origin_coord[findFirstLambda(lambda x: x<3.05 and x >2.95, origin_coord)]), 
            asn_leu_energy_vector[findFirstLambda(lambda x: x<3.05 and x >2.95, origin_coord)], 1e-2
        )

    def test_addPeptides(self):
        self.force.addPeptides(Peptide('ASN'), Peptide('LEU'))

        assert self.force.num_peptides == 2

        self.force.addPeptides(Peptide('TYR'), Peptide('LEU'))
        asn_leu_energy_vector = np.load(os.path.join(force_field_dir, 'ASN-LEU.npy'))
        leu_leu_energy_vector = np.load(os.path.join(force_field_dir, 'LEU-LEU.npy'))

        assert self.force.num_peptides == 4
        self.force.setEnergyMatrix()

    # todo: test_calculateEnergy
    def test_calculateEnergy(self):
        peptide1 = Peptide('ASN', 0)
        peptide1.atoms[1].coordinate = [3, 1, 1]
        peptide2 = Peptide('ASP', 1)
        peptide2.atoms[1].coordinate = [0, 0, 0]
        peptide3 = Peptide('ASN', 2)
        peptide3.atoms[1].coordinate = [6, 1, 1]
        self.force.addPeptides(peptide1, peptide2, peptide3)
        self.force.setEnergyMatrix()
        asn_asp_force_field = PDFFNonBondedForceField('ASN', 'ASP', np.linspace(0, 30, 601))
        asn_asn_force_field = PDFFNonBondedForceField('ASN', 'ASN', np.linspace(0, 30, 601))
        assert self.force.calculateEnergy(0, 1) == pytest.approx(asn_asp_force_field.getInterpolate()(np.sqrt(11)))
        assert self.force.calculateEnergy(0, 2) == pytest.approx(asn_asn_force_field.getInterpolate()(3))

    def test_calculateTotalEnergy(self):
        peptide1 = Peptide('ASN', 0)
        peptide1.atoms[1].coordinate = [3, 1, 1]
        peptide2 = Peptide('ASP', 1)
        peptide2.atoms[1].coordinate = [0, 0, 0]
        peptide3 = Peptide('ASN', 2)
        peptide3.atoms[1].coordinate = [6, 1, 1]
        self.force.addPeptides(peptide1, peptide2, peptide3)
        self.force.setEnergyMatrix()
        asn_asp_force_field = PDFFNonBondedForceField('ASN', 'ASP', np.linspace(0, 30, 601))
        asn_asn_force_field = PDFFNonBondedForceField('ASN', 'ASN', np.linspace(0, 30, 601))
        assert self.force.calculateTotalEnergy() == pytest.approx(
            asn_asp_force_field.getInterpolate()(np.sqrt(11)) +
            asn_asn_force_field.getInterpolate()(3) + 
            asn_asp_force_field.getInterpolate()(np.sqrt(38))
        )
        assert self.force.total_energy == pytest.approx(
            asn_asp_force_field.getInterpolate()(np.sqrt(11)) +
            asn_asn_force_field.getInterpolate()(3) + 
            asn_asp_force_field.getInterpolate()(np.sqrt(38))
        )

    # todo: test_calculateForce
    def test_calculateForce(self):
        peptide1 = Peptide('ASN', 0)
        peptide1.atoms[1].coordinate = [3.3, 0, 0]
        peptide2 = Peptide('ASP', 1)
        peptide2.atoms[1].coordinate = [0, 0, 0]
        self.force.addPeptides(peptide1, peptide2)
        self.force.setEnergyMatrix()
        assert self.force.calculateForce(0, 1).value < 0

        peptide1.atoms[1].coordinate = [2.3, 0, 0]
        assert self.force.calculateForce(0, 1).value > 0
