import pytest, os
from .. import LogDumper
from .. import SequenceLoader, ForceEncoder, VelocityVerletIntegrator, Simulation

cur_dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))

class TestLogDumper:
    def setup(self):
        self.dumper = LogDumper(
            os.path.join(cur_dir, 'data/outputLogDumper.log'), 100, 
            get_steps=True,
            get_elapsed_time=True,
            get_kinetic_energy=True
        )
        
    def teardown(self):
        self.dumper = None
        
    def test_attributes(self):
        assert self.dumper.dump_interval == 100
        
    def test_exceptions(self):
        with pytest.raises(AttributeError):
            self.dumper._test_bound()
            
    def test_setTitle(self):
        dumper = LogDumper(
            os.path.join(cur_dir, 'data/outputLogDumper.log'), 
            100, get_steps=True
        )
        dumper._setTitle()
        assert dumper.title == 'Steps     '
        
        dumper = LogDumper(
            os.path.join(cur_dir, 'data/outputLogDumper.log'), 
            100, get_steps=True, get_kinetic_energy=True
        )
        dumper._setTitle()
        assert dumper.title == 'Steps     Kinetic Energy (kj/mol)  '
        
    def test_dump(self):
        self.dumper = LogDumper(
            os.path.join(cur_dir, 'data/outputLogDumper.log'), 100,
            get_steps=True,
            get_elapsed_time=True,
            get_remain_time=True,
            get_simulation_time=True,
            get_temperature=True,
            get_potential_energy=True, get_kinetic_energy=True, 
            get_nonbonded_energy=True, get_torsion_energy=True,
            get_total_energy=True 
        )
        system = SequenceLoader(os.path.join(cur_dir, 'data/testSimulation.json')).createSystem()
        ensemble = ForceEncoder(system).createEnsemble()
        integrator = VelocityVerletIntegrator(1)
        simulation = Simulation(ensemble, integrator)
        self.dumper.bindSimulation(simulation)
        self.dumper.dump()