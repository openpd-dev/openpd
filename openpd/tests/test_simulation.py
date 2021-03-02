import pytest, os

from .. import SequenceLoader, ForceEncoder, VelocityVerletIntegrator, Simulation, LogDumper, SnapshotDumper
from ..unit import *

cur_dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))

class TestSimulation:
    def setup(self):
        self.system = SequenceLoader(os.path.join(cur_dir, 'data/testSimulation.json')).createSystem()
        self.ensemble = ForceEncoder(self.system).createEnsemble()
        self.integrator = VelocityVerletIntegrator(1, temperature=300)
        self.simulation = Simulation(self.ensemble, self.integrator)
        
    def teardown(self):
        self.system = None
        self.ensemble = None
        self.integrator = None
        self.simulation = None
        
    def test_attributes(self):
        assert self.simulation.num_dumpers == 0
        assert self.simulation.dumpers == []
        assert self.simulation._dumper_intervals == []
        assert self.simulation.cur_step == 0
        assert self.simulation.target_step == 0
        assert self.simulation.remain_step == 0
        
    def test_exceptions(self):
        with pytest.raises(AttributeError):
            self.simulation.num_dumpers = 1
            
        with pytest.raises(AttributeError):
            self.simulation.dumpers = 1
            
        with pytest.raises(AttributeError):
            self.simulation.cur_step = 1
            
        with pytest.raises(AttributeError):
            self.simulation.target_step = 1
        
        with pytest.raises(AttributeError):
            self.simulation.remain_step = 1
            
    def test_addDumper(self):
        dumper = LogDumper(os.path.join(cur_dir, 'output/outputSimulation.log'), 10)
        self.simulation._addDumper(dumper)
        assert self.simulation.num_dumpers == 1
        assert self.simulation.dumpers[0] == dumper
        
    def test_addDumpers(self):
        dumper1 = LogDumper(os.path.join(cur_dir, 'output/outputSimulation.log'), 10)
        dumper2 = LogDumper(os.path.join(cur_dir, 'output/outputSimulation.log'), 20)
        self.simulation.addDumpers(dumper1, dumper2)
        assert self.simulation.num_dumpers == 2
        assert self.simulation._gcd_interval == 10
        
    def test_dump(self):
        log_dumper = LogDumper(
            os.path.join(cur_dir, 'output/outputSimulation.log'), 20,
            get_steps=True, get_simulation_time=True,
            get_elapsed_time=True, get_remain_time=True,
            get_kinetic_energy=True, get_potential_energy=True
        )
        snapshot_dumper = SnapshotDumper(
            os.path.join(cur_dir, 'output/outputSimulation.pds'), 20
        )
        self.simulation.addDumpers(log_dumper, snapshot_dumper)
        self.simulation._integrator._sim_interval = 0.1 * femtosecond
        self.simulation.step(30)

    def test_minimizeEnergy(self):
        with pytest.raises(ValueError):
            self.simulation.minimizeEnergy('aa')

        cur_energy = self.simulation._ensemble.calculatePotentialEnergy()
        self.simulation.minimizeEnergy('gd', max_iteration=10)
        assert cur_energy > self.simulation._ensemble.calculatePotentialEnergy()

        cur_energy = self.simulation._ensemble.calculatePotentialEnergy()
        self.simulation.minimizeEnergy('sd', max_iteration=2)
        assert cur_energy > self.simulation._ensemble.calculatePotentialEnergy()