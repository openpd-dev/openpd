import datetime
import numpy as np
from . import Ensemble, Integrator, Dumper
from . import gcd
from .unit import *

ENERGY_MINIMIZATION_METHODS = [
    'gd', 'gradient descent',
    'sd', 'steepest descent',
    'cg', 'conjugate gradient'
]

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
        
    def dump(self):
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
                self.dump()

    def minimizeEnergy(
        self, method='gd', max_iteration:int=1000,
        energy_tolerance=1e-7,
        alpha=0.001, alpha_range=list(np.arange(-0.01, 0.01+0.0001, 0.0001))
    ):
        if not method.lower() in ENERGY_MINIMIZATION_METHODS:
            raise ValueError(
                '%s method is not support. Choose from \n %s'
                %(method, ENERGY_MINIMIZATION_METHODS)
            )
        self._max_iteration = max_iteration
        self._energy_tolerance = energy_tolerance
        self._alpha = alpha # gd
        self._alpha_range = alpha_range # sd
        print('Start energy minimization:')
        print(
            'Initial potential energy: %.5f kj/mol' 
            %(self._ensemble.calculatePotentialEnergy()/kilojoule_permol)
        )
        if method.lower() == 'gd' or method.lower() == 'gradient descent':
            self._gradientDescentMinimizer()
        elif method.lower() == 'sd' or method.lower() == 'steepest descent':
            self._steepDescentMinimizer()
        elif method.lower() == 'cg' or method.lower() == 'conjugrate gradient':
            self._conjugateGradientMinimizer()

    def _gradientDescentMinimizer(self):
        cur_iteration = 0
        pre_energy = self._ensemble.calculatePotentialEnergy()
        while cur_iteration < self._max_iteration:
            for atom in self._ensemble.system.topology.atoms:
                atom.force = self._ensemble.calculateAtomForce(atom.atom_id)
                atom.coordinate += self._alpha * atom.force / kilojoule_permol_over_angstrom
            cur_energy = self._ensemble.calculatePotentialEnergy()
            energy_error = np.abs((cur_energy - pre_energy) * 2 / (cur_energy + pre_energy))
            if energy_error < self._energy_tolerance:
                print('Penultimate potential energy: %.5f kj/mol' %(pre_energy/kilojoule_permol))
                print('Final potential energy: %.5f kj/mol' %(cur_energy/kilojoule_permol))
                print('Energy error: %s < %e' %(energy_error, self._energy_tolerance))
                return None
            cur_iteration += 1
        print('Max number of iterations %d has achieved.' %(self._max_iteration))
        print(
            'Final potential energy: %.5f kj/mol' 
            %(self._ensemble.calculatePotentialEnergy()/kilojoule_permol)
        )
    
    def _steepDescentMinimizer(self):
        cur_iteration = 0
        pre_energy = self._ensemble.calculatePotentialEnergy()
        while cur_iteration < self._max_iteration:
            # Update force
            for atom in self._ensemble.system.topology.atoms:
                atom.force = self._ensemble.calculateAtomForce(atom.atom_id)
            # Search minima
            energy_range = []
            cur_coord = self._ensemble.system.coordinate
            for alpha in self._alpha_range:
                self._ensemble.system.coordinate = (
                    cur_coord + self._ensemble.system.force /
                    kilocalorie_permol_over_angstrom * alpha
                )
                energy_range.append(self._ensemble.calculatePotentialEnergy()/kilojoule_permol)
            target_alpha = self._alpha_range[energy_range.index(min(energy_range))]
            # Update
            self._ensemble.system.coordinate = (
                cur_coord + self._ensemble.system.force / 
                kilocalorie_permol_over_angstrom * target_alpha
            )
            cur_energy = self._ensemble.calculatePotentialEnergy()
            # Calculate Error
            energy_error = np.abs((cur_energy - pre_energy) * 2 / (cur_energy + pre_energy))
            if energy_error < self._energy_tolerance:
                print('Penultimate potential energy: %.5f kj/mol' %(pre_energy/kilojoule_permol))
                print('Final potential energy: %.5f kj/mol' %(cur_energy/kilojoule_permol))
                print('Energy error: %s < %e' %(energy_error, self._energy_tolerance))
                return None
            cur_iteration += 1
        print('Max number of iterations %d has achieved.' %(self._max_iteration))
        print(
            'Final potential energy: %.5f kj/mol' 
            %(self._ensemble.calculatePotentialEnergy()/kilojoule_permol)
        )

    def _conjugateGradientMinimizer(self):
        pass
        
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