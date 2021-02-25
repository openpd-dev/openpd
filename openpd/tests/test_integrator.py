import pytest, os

from .. import Integrator, SequenceLoader, ForceEncoder
from ..unit import *

cur_dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))

class TestIntegrator:
    def setup(self):
        self.integrator = Integrator(1)
        system = SequenceLoader(os.path.join(cur_dir, 'data/testForceEncoder.json')).createSystem()
        ensemble = ForceEncoder(system).createEnsemble()
        self.integrator._bindEnsemble(ensemble)

    def teardown(self):
        self.integrator = None

    def test_attributes(self):
        assert self.integrator.interval == 1 * femtosecond
        assert self.integrator._is_bound == True

    def test_exception(self):
        with pytest.raises(AttributeError):
            self.integrator.ensemble = 1

        with pytest.raises(ValueError):
            Integrator(1*kilogram)

        with pytest.raises(ValueError):
            self.integrator.interval = 1 * kilogram

    def test_testBound(self):
        integrator = Integrator(1)
        with pytest.raises(AttributeError):
            integrator._testBound()

    def test_calculateKineticEnergy(self):
        assert self.integrator.calculateKineticEnergy()  == 0 * kilojoule_permol

    def test_calculateTemperature(self):
        assert self.integrator.calculateTemperature()  == 0 * kelvin

    def test_setVelocityToTemperature(self):
        self.integrator.setVelocityToTemperature(300)
        assert self.integrator.calculateTemperature() == 300 * kelvin

        self.integrator.setVelocityToTemperature(298)
        assert self.integrator.calculateTemperature() == 298 * kelvin

    def test_step(self):
        with pytest.raises(NotImplementedError):
            self.integrator.step(100)