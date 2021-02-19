from . import Integrator

class VerletIntegrator(Integrator):
    def __init__(self, interval) -> None:
        super().__init__(interval)