from . import Integrator
from ..unit import *
from ..unit import Quantity

class VelocityVerletIntegrator(Integrator):
    def __init__(self, interval, temperature=300) -> None:
        super().__init__(interval)
        if isinstance(temperature, Quantity):
            temperature.convertTo(kelvin)
        else:
            temperature = temperature * kelvin
        self._temperature = temperature
        
    def step(self, num_steps):
        cur_step = 0
        
        mass = self._system.mass
        self.setVelocityToTemperature(self._temperature)
        
        self.updateAtomsForce()
        while cur_step < num_steps:
            cur_force = self._system.force
            self._system.coordinate = (
                self._system.coordinate +
                self._system.velocity * self._interval +
                0.5 * self._system.force / mass * self._interval**2
            )
            self.updateAtomsForce()
            self._system.velocity = (
                self._system.velocity + 
                0.5 * (
                    cur_force / mass +
                    self._system.force / mass
                ) * self._interval
            )
            cur_step += 1