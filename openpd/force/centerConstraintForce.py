import numpy as np
from . import Force
from .. import getBond, getUnitVec
from ..unit import *
from ..unit import Quantity

class CenterConstraintForce(Force):
    def __init__(
        self, force_id=0, force_group=0,
        origin_center=None,
        elastic_constant=100*kilojoule_permol/angstrom**2
    ) -> None:
        super().__init__(force_id, force_group)

        # origin_center == None means extract current center coord as the origin point
        # This can be only done after or during calling bindEnsemble
        self._is_extract_center = False
        if origin_center == None:
            self._is_extract_center = True
        elif isinstance(origin_center[0], Quantity):
            origin_center = np.array([i.convertTo(angstrom) for i in origin_center])
        else:
            origin_center = np.array(origin_center * angstrom)
        self._origin_center = origin_center

        if isinstance(elastic_constant, Quantity):
            elastic_constant = elastic_constant.convertTo(kilojoule_permol/angstrom**2)
        else:
            elastic_constant = elastic_constant * kilojoule_permol/angstrom**2
        self._elastic_constant = elastic_constant
        self._num_atoms = 0
        self._potential_energy = 0

    def __repr__(self) -> str:
        return (
            '<CenterConstraintForce object: centered at (%.3f, %.3f, %.3f) A, at 0x%x>'
            %(
                self._origin_center[0]/angstrom, 
                self._origin_center[1]/angstrom, 
                self._origin_center[2]/angstrom, id(self)
            )
        )
    
    __str__ = __repr__

    def bindEnsemble(self, ensemble):
        if self._is_bound == True:
            raise AttributeError('Force has been bound to %s' %(self._ensemble))
        
        self._is_bound = True
        self._ensemble = ensemble
        self._num_atoms = self._ensemble.system.topology.num_atoms
        self._atoms = self._ensemble.system.topology.atoms
        self._total_mass = 0 * amu
        for atom in self._atoms:
            self._total_mass += atom.mass
        if self._is_extract_center:
            self._origin_center = self.calculateMassCenter()
    
    def calculateMassCenter(self):
        self._testBound()
        mass_center = np.zeros(3) * angstrom * amu
        for atom in self._atoms:
            mass_center += atom.coordinate * atom.mass
        return mass_center / self._total_mass

    def calculatePotentialEnergy(self):
        self._testBound()
        cur_center = self.calculateMassCenter()
        self._potential_energy = (
            0.5 * self._elastic_constant * getBond(
                cur_center , self._origin_center
            )**2
        )
        return self._potential_energy

    def calculateAtomForce(self, atom_id):
        self._testBound()
        atom = self._atoms[atom_id]
        cur_center = self.calculateMassCenter()
        force = (
            self._elastic_constant * getBond(
                cur_center, self._origin_center
            ) * atom.mass / self._total_mass
        )
        vec = getUnitVec(self._origin_center - cur_center)
        return force * vec

    @property
    def num_atoms(self):
        return self._num_atoms

    @property
    def origin_center(self):
        return self._origin_center

    @property
    def potential_energy(self):
        try:
            self.calculatePotentialEnergy()
            return self._potential_energy
        except:
            return self._potential_energy