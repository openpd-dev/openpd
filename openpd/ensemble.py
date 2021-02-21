from .force import *
from . import System

# note: Ensemble contains all force for a simulation, creating from a System. When call _addForce(), Ensemble will call force.bindEnsemble to bind and activate the Force
class Ensemble:   
    def __init__(self, system:System) -> None:
        self._system = system
        self._forces = []
        self._num_forces = 0      

    # note: transits force directly to ensemble
    def _addForce(self, force:Force):
        force.bindEnsemble(self)
        self._forces.append(force)
        self._forces[-1].force_id = self._num_forces
        self._num_forces += 1

    def addForces(self, *forces):
        for force in forces:
            self._addForce(force)
    
    def calculatePotentialEnergy(self, force_group=[0]):
        potential_energy = 0
        for force in self.getForcesByGroup(force_group):
            potential_energy += force.calculatePotentialEnergy()
        return potential_energy

    def getForcesByGroup(self, force_group=[0]):
        return [force for force in self._forces if force.force_group in force_group]
 
    def getNumForcesByGroup(self, force_group=[0]):
        return len(self.getForcesByGroup(force_group))
    
    @property
    def system(self):
        return self._system

    @property
    def forces(self):
        return self._forces

    @property
    def num_forces(self):
        return self._num_forces