import pytest, os
import numpy as np
from .. import ForceEncoder, SequenceLoader, Ensemble
from .. import isArrayEqual
from ..unit import *

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

        asn_tyr_potential = np.load(os.path.join(cur_dir, '../data/pdff/nonbonded/ASN-TYR.npz'))
        assert force.force_field_matrix[0, 2].getEnergy(asn_tyr_potential['energy_coord'][50]) == pytest.approx(asn_tyr_potential['energy_data'][50], 1e-3)

    def test_createBondForce(self):
        self.encoder.ensemble = Ensemble(self.encoder._system)
        force = self.encoder._createBondForce()
        force.bindEnsemble(self.encoder.ensemble)
        assert force._num_bonds == 5
        data = np.load(os.path.join(cur_dir, '../data/pdff/bond/ASN.npz'))
        assert force.force_field_vector[0].getEnergy(data['energy_coord'][30])/kilojoule_permol == pytest.approx(data['energy_data'][30])
        data = np.load(os.path.join(cur_dir, '../data/pdff/bond/CA-CA.npz'))
        assert force.force_field_vector[1].getEnergy(data['energy_coord'][30])/kilojoule_permol == pytest.approx(data['energy_data'][30])


    def test_createTorsionForce(self):
        self.encoder.ensemble = Ensemble(self.encoder._system)
        force = self.encoder._createTorsionForce()
        force.bindEnsemble(self.encoder.ensemble)
        
        origin_coord = np.load(os.path.join(cur_dir, '../data/pdff/torsion/coord.npy'))
        asn_leu_energy_vector = np.load(os.path.join(cur_dir, '../data/pdff/torsion/ASN-LEU.npy'))
        assert force.force_field_vector[0].getEnergy(origin_coord[50]) == pytest.approx(asn_leu_energy_vector[50], 1e-3)
        
        leu_tyr_energy_vector = np.load(os.path.join(cur_dir, '../data/pdff/torsion/LEU-TYR.npy'))
        assert force.force_field_vector[1].getEnergy(origin_coord[50]) == pytest.approx(leu_tyr_energy_vector[50], 1e-3)

    def test_createCenterConstraintForce(self):
        self.encoder.ensemble = Ensemble(self.encoder._system)
        force = self.encoder._createCenterConstraintForce()
        force.bindEnsemble(self.encoder.ensemble)
        assert force.num_atoms == 6
        assert not isArrayEqual(
            force.origin_center,
            np.zeros(3) * angstrom
        )
        
    def test_createEnsemble(self):
        ensemble = self.encoder.createEnsemble()
        assert ensemble.getNumForcesByGroup([0]) == 4
        assert ensemble.getNumForcesByGroup([1]) == 0