import datetime
from . import Ensemble, Integrator, Dumper
from . import gcd
from .unit import *

class Simulation:
    def __init__(self, ensemble:Ensemble, integrator:Integrator) -> None:
        self._ensemble = ensemble
        self._integrator = integrator
        self._integrator._bindEnsemble(self._ensemble)
        self._num_dumpers = 0
        self._dumpers = []
        self._dumper_intervals = []
        self._cur_step = 0
        self._target_step = 0
        self._remain_step = 0
        self._start_time = datetime.datetime.now().replace(microsecond=0)
        self._cur_time = datetime.datetime.now().replace(microsecond=0)
        self._elapsed_time = self._cur_time - self._start_time
        self._remain_time = datetime.timedelta(seconds=0)
        
    def _addDumper(self, dumper:Dumper):
        self._num_dumpers += 1
        self._dumpers.append(dumper)
        self._dumper_intervals.append(dumper.dump_interval)
        self._dumpers[-1].bindSimulation(self)
        
    def addDumpers(self, *dumpers):
        for dumper in dumpers:
            self._addDumper(dumper)
        self._gcd_interval = gcd(*self._dumper_intervals)
        self._start_time = datetime.datetime.now().replace(microsecond=0) # Update start time
        
    def _dump(self):
        self._cur_time = datetime.datetime.now().replace(microsecond=0)
        self._elapsed_time = self._cur_time - self._start_time
        self._sim_velocity = (
            self.cur_step / (self._elapsed_time.total_seconds() + 0.001)
        ) # Step / second
        self._remain_time = datetime.timedelta(seconds=int(round(self._remain_step/self._sim_velocity)))
        
        for i, dumper in enumerate(self._dumpers):
            if self._cur_step % self._dumper_intervals[i] == 0:
                dumper.dump()
            
    def step(self, num_steps):
        self._target_step += num_steps
        self._remain_step = num_steps
        # Dump 0 Step
        for dumper in self._dumpers:
            dumper.dump()
        while self._cur_step < self._target_step:
            if self._remain_step < self._gcd_interval:
                # Dump Last Step
                self._integrator.step(self._gcd_interval)
                self._cur_step += self._remain_step
                self._remain_step = 0
                for dumper in self._dumpers:
                    dumper.dump()
            else:
                self._integrator.step(self._gcd_interval)
                self._cur_step += self._gcd_interval
                self._remain_step -= self._gcd_interval
                self._dump()
        
    @property
    def num_dumpers(self):
        return self._num_dumpers
        
    @property
    def dumpers(self):
        return self._dumpers
                
    @property
    def cur_step(self):
        return self._cur_step
    
    @property
    def target_step(self):
        return self._target_step
    
    @property
    def remain_step(self):
        return self._remain_step