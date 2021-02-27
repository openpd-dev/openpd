import pytest, os
from .. import SnapshotDumper
from .. import SequenceLoader, ForceEncoder, VelocityVerletIntegrator, Simulation

cur_dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))

class TestSnapshotDumper:
    def setup(self):
        self.dumper = SnapshotDumper(
            os.path.join(cur_dir, 'data/outputSnapshotDumper.pds'), 100
        )
    
    def test_attributes(self):
        assert self.dumper.dump_interval == 100
    
    def test_exceptions(self):
        with pytest.raises(AttributeError):
            self.dumper._test_bound()
            
        with pytest.raises(ValueError):
            self.dumper = SnapshotDumper(
            os.path.join(cur_dir, 'data/outputSnapshotDumper.sp'), 100
        )
            
    def test_dump(self):
        system = SequenceLoader(os.path.join(cur_dir, 'data/testSimulation.json')).createSystem()
        ensemble = ForceEncoder(system).createEnsemble()
        integrator = VelocityVerletIntegrator(1)
        simulation = Simulation(ensemble, integrator)
        self.dumper.bindSimulation(simulation)
        self.dumper.dump()
    
    