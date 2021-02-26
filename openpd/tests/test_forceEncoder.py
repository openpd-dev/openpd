import pytest, os
import numpy as np
from .. import CONST_CA_CA_DISTANCE, ForceEncoder, SequenceLoader, Ensemble
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
        self.encoder.ensemble = Ensemble(self.encoder._system)
        force = self.encoder._createNonBondedForce()
        force.bindEnsemble(self.encoder.ensemble)
        
        origin_coord = np.load(os.path.join(cur_dir, '../data/pdff/nonbonded/coord.npy'))
        asn_leu_energy_vector = np.load(os.path.join(cur_dir, '../data/pdff/nonbonded/ASN-LEU.npy'))
        assert force.force_field_matrix[0, 1].getEnergy(origin_coord[50]) == pytest.approx(asn_leu_energy_vector[50], 1e-3)

        asn_tyr_energy_vector = np.load(os.path.join(cur_dir, '../data/pdff/nonbonded/ASN-TYR.npy'))
        assert force.force_field_matrix[0, 2].getEnergy(origin_coord[50]) == pytest.approx(asn_tyr_energy_vector[50], 1e-3)

    def test_createBondForce(self):
        force = self.encoder._createBondForce()
        assert force.num_bonds == 5
        assert len(force.bond_length) == 5
        assert force.bonds[0][0] == self.encoder._system.atoms[0]
        assert force.bonds[0][1] == self.encoder._system.atoms[1]
        assert force.bond_length[0] == 5
        assert force.bond_length[1] == CONST_CA_CA_DISTANCE

    def test_createTorsionForce(self):
        self.encoder.ensemble = Ensemble(self.encoder._system)
        force = self.encoder._createTorsionForce()
        force.bindEnsemble(self.encoder.ensemble)
        
        origin_coord = np.load(os.path.join(cur_dir, '../data/pdff/torsion/coord.npy'))
        asn_leu_energy_vector = np.load(os.path.join(cur_dir, '../data/pdff/torsion/ASN-LEU.npy'))
        assert force.force_field_vector[0].getEnergy(origin_coord[50]) == pytest.approx(asn_leu_energy_vector[50], 1e-3)
        
        leu_tyr_energy_vector = np.load(os.path.join(cur_dir, '../data/pdff/torsion/LEU-TYR.npy'))
        assert force.force_field_vector[1].getEnergy(origin_coord[50]) == pytest.approx(leu_tyr_energy_vector[50], 1e-3)
        
    def test_createEnsemble(self):
        ensemble = self.encoder.createEnsemble()
        assert ensemble.getNumForcesByGroup([0]) == 2
        assert ensemble.getNumForcesByGroup([1]) == 0