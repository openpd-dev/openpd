import pytest, os
import numpy as np
from .. import CONST_CA_CA_DISTANCE, ForceEncoder, SequenceLoader
from .. import isArrayEqual, isAlmostEqual, findFirstLambda

cur_dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))


class TestForceEncoder:

    def setup(self):
        self.system = SequenceLoader(os.path.join(cur_dir, 'data/testForceEncoder.json')).createSystem()
        self.encoder = ForceEncoder(self.system)

    def teardown(self):
        self.encoder = None

    def test_attributes(self):
        pass

    def test_exceptions(self):
        with pytest.raises(ValueError):
            ForceEncoder(self.system, 'a')

    def test_createNonBondedForce(self):
        force = self.encoder._createNonBondedForce()
        origin_coord = np.load(os.path.join(cur_dir, '../data/pdff/nonbonded/coord.npy'))
       
        assert force.num_peptides == 3

        assert isArrayEqual(force.energy_coordinate, np.linspace(0, 30, 601))

        asn_leu_energy_vector = np.load(os.path.join(cur_dir, '../data/pdff/nonbonded/ASN-LEU.npy'))
        assert isAlmostEqual(
            asn_leu_energy_vector[findFirstLambda(lambda x: x<2.05 and x >1.95, origin_coord)], 
            force.energy_matrix[0, 1](origin_coord[findFirstLambda(lambda x: x<2.05 and x >1.95, origin_coord)]), 1e-3
        )

        asn_tyr_energy_vector = np.load(os.path.join(cur_dir, '../data/pdff/nonbonded/ASN-TYR.npy'))
        assert isAlmostEqual(
            asn_tyr_energy_vector[findFirstLambda(lambda x: x<2.05 and x >1.95, origin_coord)], 
            force.energy_matrix[0, 2](origin_coord[findFirstLambda(lambda x: x<2.05 and x >1.95, origin_coord)]), 1e-3
        )

    def test_createBondForce(self):
        force = self.encoder._createBondForce()
        assert force.num_bonds == 5
        assert len(force.bond_length) == 5
        assert force.bonds[0][0] == self.encoder.system.atoms[0]
        assert force.bonds[0][1] == self.encoder.system.atoms[1]
        assert force.bond_length[0] == 5
        assert force.bond_length[1] == CONST_CA_CA_DISTANCE

    # def test_createTorsionForce(self):
    #     force = self.encoder._createTorsionForce()
    #     assert force.num_torsions == 2
    #     assert len(force.torsion_types) == 2
    #     assert isArrayEqual(force.torsion_types[0], ['ASN', 'LEU'])

    #     energy_coordinate = np.load(os.path.join(cur_dir, '../data/pdff/torsion/coord.npy'))
    #     assert isArrayEqual(force.energy_coordinate, energy_coordinate)

    #     asn_leu_energy_vector = np.load(os.path.join(cur_dir, '../data/pdff/torsion/ASN-LEU.npy'))
    #     assert isArrayEqual(force.energy_array[0, :], asn_leu_energy_vector)

    #     leu_tyr_energy_vector = np.load(os.path.join(cur_dir, '../data/pdff/torsion/LEU-TYR.npy'))
    #     assert isArrayEqual(force.energy_array[1, :], leu_tyr_energy_vector)

    # def test_createEnsemble(self):
    #     ensemble = self.encoder.createEnsemble()
    #     assert ensemble.getNumForcesByGroup([0]) == 3
    #     assert ensemble.getNumForcesByGroup([1]) == 0

    # todo: test_calculateEnergy, test_calculateForce
    def test_calculateEnergy(self):
        pass

    def test_calculateForce(self):
        pass
