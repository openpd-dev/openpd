import numpy as np
from . import Integrator
from ..unit import *

class VerletIntegrator(Integrator):
    def __init__(self, interval) -> None:
        """
        Parameters
        ----------
        interval : int or Quantity, optional
            the step interval of the integrator, by default ``1 * femtosecond``

        Raises
        ------
        ValueError
            When the parameter ``interval`` is ``Quantity`` and ``interval.unit.base_dimension != BaseDimension(time_dimension=1)``
        """        
        super().__init__(interval)
    
    def step(self, num_steps:int):
        cur_step = 0
        
        mass = self._system.mass
        self.updateAtomsForce()
        pre_coord = self._system.coordinate - self._system.force / mass * self._interval**2
        next_coord = self._system.coordinate
        cur_velocity = self._system.velocity
        
        while cur_step < num_steps:
            self.updateAtomsForce()
            
            next_coord = 2 * self._system.coordinate - pre_coord + self._system.force / mass * self._interval**2
            cur_velocity = (next_coord - pre_coord) / (2 * self._interval)
    
            pre_coord = self._system.coordinate
            self._system.coordinate = next_coord
            print((next_coord[1, 0]-pre_coord[1, 0]/angstrom))
            self._system.velocity = cur_velocity
            cur_step += 1
            
            
            