from . import Integrator
class BrownianIntegrator(Integrator):
    def __init__(self, sim_interval, dumpping_factor, temperature) -> None:
        super().__init__(sim_interval)
        self.dumpping_factor = dumpping_factor
        self.temperature = temperature
        self.sim_interval = sim_interval

    def step(self, num_steps):
        pass