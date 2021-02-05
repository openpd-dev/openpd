
class Simulation(object):
    def __init__(self, topology, system, integrator) -> None:
        super().__init__()
        self.topology = topology
        self.system = system
        self.integrator = integrator

    def step(self, num_steps):
        pass