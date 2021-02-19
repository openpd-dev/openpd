from . import Integrator

class LeapFrogIntegrator(Integrator):
    def __init__(self, interval) -> None:
        super().__init__(interval)