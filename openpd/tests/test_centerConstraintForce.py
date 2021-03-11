import pytest, os
import numpy as np
from .. import CenterConstraintForce, SequenceLoader, Ensemble
from .. import isArrayEqual, getBond, getUnitVec
from ..unit import *
from ..exceptions import NonboundError, RebindError

cur_dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))

class TestCenterConstraintForce:
    def setup(self):
        self.system = SequenceLoader(os.path.join(cur_dir, 'data/testCenterConstraintForce.json')).createSystem()
        self.ensemble = Ensemble(self.system)
        self.force = CenterConstraintForce(origin_center=[0, 0, 0])        

    def teardown(self):
        self.system = None
        self.ensemble = None
        self.force = None

    def test_attributes(self):
        assert self.force.num_atoms == 0
        assert isArrayEqual(
            self.force.origin_center,
            np.zeros([3]) * angstrom
        )
        assert self.force.potential_energy == 0
        assert self.force._elastic_constant == 100 * kilojoule_permol / angstrom**2

    def test_exceptions(self):
        with pytest.raises(AttributeError):
            self.force.num_atoms = 1

        with pytest.raises(AttributeError):
            self.force.origin_center = 1
        
        with pytest.raises(AttributeError):
            self.force.potential_energy = 1
        
        with pytest.raises(NonboundError):
            self.force._testBound()

        with pytest.raises(RebindError):
            self.force.bindEnsemble(self.ensemble)
            self.force.bindEnsemble(self.ensemble)

    def test_calculateMassCenter(self):
        self.force.bindEnsemble(self.ensemble)
        mass_center = np.zeros(3) * angstrom * amu
        total_mass = 0 * amu
        for atom in self.system.topology.atoms:
            mass_center += atom.mass * atom.coordinate
            total_mass += atom.mass
        mass_center /= total_mass
        assert isArrayEqual(
            self.force.calculateMassCenter(),
            mass_center
        )

    def test_calculatePotentialEnergy(self):
        self.force.bindEnsemble(self.ensemble)
        cur_center = np.zeros(3) * angstrom * amu
        total_mass = 0 * amu
        for atom in self.system.topology.atoms:
            cur_center += atom.mass * atom.coordinate
            total_mass += atom.mass
        cur_center /= total_mass
        assert (
            self.force.calculatePotentialEnergy() == 
            0.5 * 100 * kilojoule_permol / angstrom**2 * getBond(
                cur_center, self.force.origin_center
            )**2
        )

    def test_calculateAtomForce(self):
        self.force.bindEnsemble(self.ensemble)
        cur_center = np.zeros(3) * angstrom * amu
        total_mass = 0 * amu
        for atom in self.system.topology.atoms:
            cur_center += atom.mass * atom.coordinate
            total_mass += atom.mass
        cur_center /= total_mass
        atom0 = self.system.atoms[0]
        force0 = (
            100 * kilojoule_permol / angstrom**2 * getBond(
                cur_center, self.force.origin_center
            ) * atom0.mass / total_mass
        )
        vec0 = getUnitVec(self.force.origin_center - cur_center)
        assert isArrayEqual(
            self.force.calculateAtomForce(0),
            force0 * vec0
        )