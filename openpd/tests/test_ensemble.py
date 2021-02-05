import pytest, os
import numpy as np
from .. import Ensemble, PDFFNonbondedForce, RigidBondForce
from .. import isArrayEqual

cur_dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))

class TestEnsemble:
    def setup(self):
        self.ensemble = Ensemble()

    def teardown(self):
        self.ensemble = None

    def test_attributes(self):
        assert self.ensemble.num_forces == 0
        assert self.ensemble.forces == []

    def test_exceptions(self):
        with pytest.raises(AttributeError):
            self.ensemble.num_forces = 1
        
        with pytest.raises(AttributeError):
            self.ensemble.forces = 1

    def test_addForce(self):
        non_bonded_force = PDFFNonbondedForce()
        self.ensemble.addForces(non_bonded_force)
        assert self.ensemble.num_forces == 1
        assert self.ensemble.forces == [non_bonded_force]
        assert self.ensemble.forces[0].force_id == 0

    def test_addForces(self):
        non_bonded_force = PDFFNonbondedForce()
        bond_force = RigidBondForce()
        self.ensemble.addForces(non_bonded_force, bond_force)

        assert self.ensemble.num_forces == 2
        assert isArrayEqual(self.ensemble.forces, [non_bonded_force, bond_force])
        assert self.ensemble.forces[0].force_id == 0
        assert self.ensemble.forces[1].force_id == 1

    def test_getForcesByGroup(self):
        non_bonded_force1 = PDFFNonbondedForce()
        non_bonded_force2 = PDFFNonbondedForce()
        bond_force = RigidBondForce(force_group=2)
        self.ensemble.addForces(non_bonded_force1, non_bonded_force2, bond_force)

        assert isArrayEqual(self.ensemble.getForcesByGroup(), [non_bonded_force1, non_bonded_force2])
        assert isArrayEqual(self.ensemble.getForcesByGroup([2]), [bond_force])
        assert isArrayEqual(self.ensemble.getForcesByGroup([0, 2]), self.ensemble.forces)

    def test_getNumForcesByGroup(self):
        non_bonded_force1 = PDFFNonbondedForce()
        non_bonded_force2 = PDFFNonbondedForce()
        bond_force = RigidBondForce(force_group=2)
        self.ensemble.addForces(non_bonded_force1, non_bonded_force2, bond_force)

        assert self.ensemble.getNumForcesByGroup() == 2
        assert self.ensemble.getNumForcesByGroup([2]) == 1
        assert self.ensemble.getNumForcesByGroup([0, 2]) == 3

    # todo: test_calculateEnergy
    def test_calculateEnergy(self):
        pass

    # todo: test_calculateForce
    def test_calculateForce(self):
        pass