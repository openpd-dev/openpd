import pytest, os
from .. import XYZDumper
from .. import SequenceLoader, ForceEncoder, VelocityVerletIntegrator, Simulation
from ..exceptions import NonboundError

cur_dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))

class TestLogDumper:
    def setup(self):
        self.dumper = XYZDumper(
            os.path.join(cur_dir, 'output/outputXYZDumper.xyz'), 100
        )
        
    def teardown(self):
        self.dumper = None
        
    def test_attributes(self):
        assert self.dumper.dump_interval == 100

    def test_exceptions(self):
        with pytest.raises(NonboundError):
            self.dumper._test_bound()

    def test_dump(self):
        system = SequenceLoader(os.path.join(cur_dir, 'data/testSimulation.json')).createSystem()
        ensemble = ForceEncoder(system).createEnsemble()
        integrator = VelocityVerletIntegrator(1)
        simulation = Simulation(ensemble, integrator)
        self.dumper.bindSimulation(simulation)
        self.dumper.dump()