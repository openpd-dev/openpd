from . import Integrator
from .. import Ensemble
from ..unit import *
from ..unit import Quantity

class VelocityVerletIntegrator(Integrator):
    def __init__(self, sim_interval, temperature=300) -> None:
        super().__init__(sim_interval)
        if isinstance(temperature, Quantity):
            temperature.convertTo(kelvin)
        else:
            temperature = temperature * kelvin
        self._temperature = temperature
        
    def _bindEnsemble(self, ensemble: Ensemble):
        super()._bindEnsemble(ensemble)
        self.setVelocityToTemperature(self._temperature)
        
    def step(self, num_steps):
        cur_step = 0
        mass = self._system.mass        
        self.updateAtomsForce()
        while cur_step < num_steps:
            cur_force = self._system.force
            self._system.coordinate = (
                self._system.coordinate +
                self._system.velocity * self._sim_interval +
                0.5 * self._system.force / mass * self._sim_interval**2
            )
            self.updateAtomsForce()
            self._system.velocity = (
                self._system.velocity + 
                0.5 * (
                    cur_force / mass +
                    self._system.force / mass
                ) * self._sim_interval
            )
            cur_step += 1