from . import Integrator

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

    def _integrate(self):
        # equal to self.step(1)
        pass
    
    def step(self, num_steps:int):
        pass