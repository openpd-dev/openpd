from . import Integrator

class VelocityVerletIntegrator(Integrator):
    def __init__(self, interval) -> None:
        super().__init__(interval)