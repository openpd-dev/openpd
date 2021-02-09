class BrownianIntegrator:
    def __init__(self, dumpping_factor, temperature, interval) -> None:
        self.dumpping_factor = dumpping_factor
        self.temperature = temperature
        self.interval = interval

    def step(self, num_steps):
        pass