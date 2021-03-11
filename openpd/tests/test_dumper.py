import pytest, os
from .. import Dumper
from .. import SequenceLoader, ForceEncoder, VelocityVerletIntegrator, Simulation
from ..exceptions import NonboundError, RebindError

cur_dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))

class TestDumper:
    def setup(self):
        self.dumper = Dumper(
            os.path.join(cur_dir, 'output/outputDumper.log'), 100
        )
        
    def teardown(self):
        self.dumper = None
        
    def test_attributes(self):
        self.dumper.dump_interval == 100
        self.dumper._is_bound == False
    
    def test_exceptions(self):
        with pytest.raises(AttributeError):
            self.dumper.dump_interval = 1
    
    def test_testBound(self):
        with pytest.raises(NonboundError):
            self.dumper._test_bound()
            
    def test_bindSimulation(self):
        system = SequenceLoader(os.path.join(cur_dir, 'data/testSimulation.json')).createSystem()
        ensemble = ForceEncoder(system).createEnsemble()
        integrator = VelocityVerletIntegrator(1)
        simulation = Simulation(ensemble, integrator)
        self.dumper.bindSimulation(simulation)
        assert self.dumper._is_bound == True
        
        with pytest.raises(RebindError):
            self.dumper.bindSimulation(simulation)
            
    def test_dump(self):
        system = SequenceLoader(os.path.join(cur_dir, 'data/testSimulation.json')).createSystem()
        ensemble = ForceEncoder(system).createEnsemble()
        integrator = VelocityVerletIntegrator(1)
        simulation = Simulation(ensemble, integrator)
        self.dumper.bindSimulation(simulation)
        with pytest.raises(NotImplementedError):
            self.dumper.dump()
    
    