import pytest, os

from .. import VerletIntegrator, SequenceLoader, ForceEncoder
from ..unit import *

cur_dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))

class TestVerletIntegrator:
    def setup(self):
        self.integrator = VerletIntegrator(1)
        system = SequenceLoader(os.path.join(cur_dir, 'data/testForceEncoder.json')).createSystem()
        ensemble = ForceEncoder(system).createEnsemble()
        self.integrator._bindEnsemble(ensemble)

    def teardown(self):
        self.integrator = None

    def test_attributes(self):
        assert self.integrator.sim_interval == 1 * femtosecond
        assert self.integrator._is_bound == True

    def test_exceptions(self):
        with pytest.raises(ValueError):
            VerletIntegrator(1*kilogram)

        with pytest.raises(ValueError):
            self.integrator.sim_interval = 1 * kilogram

    def test_step(self):
        self.integrator.step(100)