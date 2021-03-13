import numpy as np
from . import Force
from .. import getBond, getUnitVec
from ..unit import *
from ..unit import Quantity
from ..exceptions import RebindError

class CenterConstraintForce(Force):
    def __init__(
        self, force_id=0, force_group=0,
        origin_center=None,
        elastic_constant=100*kilojoule_permol/angstrom**2
    ) -> None:
        """
        
        Parameters
        ----------
        force_id : int, optional
            the id of force, by default 0
        force_group : int, optional
            the group of force, by default 0
        origin_center : ndarray, optional
            the origin center of CenterConstraintForce, by default None
            If None, the mass center of initial conformation will be chosen to be the ``origin_center``
        elastic_constant : int or float or Quantity, optional
            The elastic constant of the harmonic potential, by default 100*kilojoule_permol/angstrom**2
        """        
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
        """
        bindEnsemble overloads ``Force.bindEnsemble()`` to bind CenterConstraintForce to an ``Ensemble`` instance

        Parameters
        ----------
        ensemble : Ensemble
            An``Ensemble`` instance. 
            
        Raises
        ------
        AttributeError
            When self is bound multi-times
        """        
        if self._is_bound == True:
            raise RebindError('Force has been bound to %s' %(self._ensemble))
        
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
        """
        calculateMassCenter calculates the mass center of bounded ``ensemble``

        Returns
        -------
        ndarray(dtype=Quantity)
            the mass center of bounded ``ensemble``
        """        
        self._testBound()
        mass_center = np.zeros(3) * angstrom * amu
        for atom in self._atoms:
            mass_center += atom.coordinate * atom.mass
        return mass_center / self._total_mass

    def calculatePotentialEnergy(self):
        """
        calculatePotentialEnergy calculates the potential energy of ``CenterConstraintForce``

        Returns
        -------
        Quantity
            The potential energy of ``CenterConstraintForce``
        """      
        self._testBound()
        cur_center = self.calculateMassCenter()
        self._potential_energy = (
            0.5 * self._elastic_constant * getBond(
                cur_center , self._origin_center
            )**2
        )
        return self._potential_energy

    def calculateAtomForce(self, atom_id):
        """
        calculateAtomForce calculates the force acts on atom

        Parameters
        ----------
        atom_id : int
            The id of atom

        Returns
        -------
        Quantity
            the force acts on atom
        """        
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
        """
        num_atoms gets the number of atoms of ``CenterConstraintForce``

        Returns
        -------
        int
            the number of atoms
        """    
        return self._num_atoms

    @property
    def origin_center(self):
        """
        origin_center gets the origin center of ``CenterConstraintForce``

        Returns
        -------
        ndarray(dtype=Quantity)
            the origin center of ``CenterConstraintForce``
        """        
        return self._origin_center

    @property
    def potential_energy(self):
        """
        potential_energy gets the potential energy of ``CenterConstraintForce``
        
        Returns
        -------
        Quantity
            The potential energy of ``CenterConstraintForce``
        """     
        try:
            self.calculatePotentialEnergy()
            return self._potential_energy
        except:
            return self._potential_energy