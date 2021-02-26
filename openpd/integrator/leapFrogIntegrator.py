from . import Integrator

class LeapFrogIntegrator(Integrator):
    def __init__(self, sim_interval) -> None:
        super().__init__(sim_interval)