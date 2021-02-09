from .force import *

class Ensemble(object):
    def __init__(self) -> None:
        super().__init__()
        self._forces = []
        self._num_forces = 0

    # note: transits force directly to ensemble
    def _addForce(self, force:Force):
        self._forces.append(force)
        self._forces[-1].force_id = self._num_forces
        self._num_forces += 1

    def addForces(self, *forces):
        for force in forces:
            self._addForce(force)

    def calculateEnergy(self, force_group=[0]):
        energy = 0
        for force in self.getForcesByGroup(force_group):
            energy += force.calculateEnergy()
        return energy

    def calculateForce(self):
        pass

    @property
    def forces(self):
        return self._forces

    @property
    def num_forces(self):
        return self._num_forces

    def getForcesByGroup(self, force_group=[0]):
        return [force for force in self._forces if force.force_group in force_group]
 
    def getNumForcesByGroup(self, force_group=[0]):
        return len(self.getForcesByGroup(force_group))