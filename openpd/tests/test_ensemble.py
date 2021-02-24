import pytest, os
import numpy as np
from .. import SequenceLoader, Ensemble, PDFFNonBondedForce, RigidBondForce, PDFFTorsionForce
from .. import isArrayEqual
from ..unit import *

cur_dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))

class TestEnsemble:
    def setup(self):
        system = SequenceLoader(os.path.join(cur_dir, 'data/testForceEncoder.json')).createSystem()
        self.ensemble = Ensemble(system)

    def teardown(self):
        self.ensemble = None

    def test_attributes(self):
        assert self.ensemble.num_forces == 0
        assert self.ensemble.forces == []

    def test_exceptions(self):
        with pytest.raises(AttributeError):
            self.ensemble.system = 1
            
        with pytest.raises(AttributeError):
            self.ensemble.num_forces = 1
        
        with pytest.raises(AttributeError):
            self.ensemble.forces = 1

    def test_addForce(self):
        non_bonded_force = PDFFNonBondedForce(self.ensemble)
        self.ensemble.addForces(non_bonded_force)
        assert self.ensemble.num_forces == 1
        assert self.ensemble.forces == [non_bonded_force]
        assert self.ensemble.forces[0].force_id == 0

    def test_addForces(self):
        non_bonded_force = PDFFNonBondedForce(self.ensemble)
        bond_force = RigidBondForce()
        self.ensemble.addForces(non_bonded_force, bond_force)

        assert self.ensemble.num_forces == 2
        assert isArrayEqual(self.ensemble.forces, [non_bonded_force, bond_force])
        assert self.ensemble.forces[0].force_id == 0
        assert self.ensemble.forces[1].force_id == 1

    def test_getForcesByGroup(self):
        non_bonded_force1 = PDFFNonBondedForce(self.ensemble)
        non_bonded_force2 = PDFFNonBondedForce(self.ensemble)
        bond_force = RigidBondForce(force_group=2)
        self.ensemble.addForces(non_bonded_force1, non_bonded_force2, bond_force)

        assert isArrayEqual(self.ensemble.getForcesByGroup(), [non_bonded_force1, non_bonded_force2])
        assert isArrayEqual(self.ensemble.getForcesByGroup([2]), [bond_force])
        assert isArrayEqual(self.ensemble.getForcesByGroup([0, 2]), self.ensemble.forces)

    def test_getNumForcesByGroup(self):
        non_bonded_force1 = PDFFNonBondedForce(self.ensemble)
        non_bonded_force2 = PDFFNonBondedForce(self.ensemble)
        bond_force = RigidBondForce(force_group=2)
        self.ensemble.addForces(non_bonded_force1, non_bonded_force2, bond_force)

        assert self.ensemble.getNumForcesByGroup() == 2
        assert self.ensemble.getNumForcesByGroup([2]) == 1
        assert self.ensemble.getNumForcesByGroup([0, 2]) == 3

    def test_calculatePotentialEnergy(self):
        force1 = PDFFNonBondedForce(cutoff_radius=12)
        force2 = PDFFTorsionForce()
        self.ensemble.addForces(force1, force2)
        
        assert (
            self.ensemble.calculatePotentialEnergy() == 
            force1.calculatePotentialEnergy() + force2.calculatePotentialEnergy()
        )

    def test_calculateAtomForce(self):
        force1 = PDFFNonBondedForce(cutoff_radius=12)
        force2 = PDFFTorsionForce()
        self.ensemble.addForces(force1, force2)
        
        assert isArrayEqual(
            self.ensemble.calculateAtomForce(1), 
            force1.calculateAtomForce(1) + force2.calculateAtomForce(1)
        )