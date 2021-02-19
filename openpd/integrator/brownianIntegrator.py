from . import Integrator
class BrownianIntegrator(Integrator):
    def __init__(self, interval, dumpping_factor, temperature) -> None:
        super().__init__(interval)
        self.dumpping_factor = dumpping_factor
        self.temperature = temperature
        self.interval = interval

    def step(self, num_steps):
        pass