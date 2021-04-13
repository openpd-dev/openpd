#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
file: atom.py
created time : 2021/02/03
last edit time : 2021/04/13
author : Zhenyu Wei 
version : 1.0
contact : zhenyuwei99@gmail.com
copyright : (C)Copyright 2021-2021, Zhenyu Wei and Southeast University
'''

import numpy as np

import openpd.unit as unit
from ..unit import *
from ..unit import Quantity


class Atom:
    def __init__(self, atom_type:str, mass) -> None:
        """
        Parameters
        ----------
        atom_type : str
            the type of atom 
        mass : float or Quantity
            the mass of atom. Unit default to be ``amu`` is float is provided

        Raises
        ------
        ValueError
            When the dimension of input ``mass`` is Quantity and != ``BaseDimension(mass=1)``
        """        
        self._atom_type = atom_type
        self._atom_id = 0
        if isinstance(mass, Quantity):
            mass = mass.convertTo(amu)
        else:
            mass = mass * amu
        self._mass = mass
        self._peptide_type = None
        self._peptide_id = 0
        self._coordinate = np.zeros([3]) * angstrom
        self._velocity = np.zeros([3]) * angstrom / femtosecond
        self._kinetic_energy = 0 * kilojoule_permol
        self._potential_energy = 0 * kilojoule_permol
        self._force = np.zeros([3]) * kilojoule_permol / angstrom

    def __repr__(self) -> str:
        return ('<Atom object: id %d, type %s, of peptide %s at 0x%x>'
            %(self._atom_id, self._atom_type, self._peptide_type, id(self)))

    __str__ = __repr__ 
    
    def __eq__(self, other):
        if id(self) == id(other):
            return True
        else:
            return False

    @property
    def atom_type(self):
        """
        atom_type gets atom_type

        Returns
        -------
        str
            the type of atom
        """        
        return self._atom_type

    @property
    def atom_id(self):
        """
        atom_id gets atom_id

        Default value: ``atom_id=0``

        Returns
        -------
        int
            the id of atom
        """        
        return self._atom_id
    
    @atom_id.setter
    def atom_id(self, atom_id:int):    
        self._atom_id = atom_id

    @property
    def mass(self):
        """
        mass gets mass

        Returns
        -------
        Quantity
            mass of atom
        """              
        return self._mass

    @property
    def peptide_type(self):
        """
        peptide_type gets peptide_type

        Default value: ``peptide_type=None``

        Returns
        -------
        str
            type of the parent peptide
        """          
        return self._peptide_type

    @peptide_type.setter
    def peptide_type(self, peptide_type:str):  
        self._peptide_type = peptide_type
    
    @property
    def peptide_id(self):
        """
        peptide_id gets peptide_id

        Default value: ``peptide_id=0``

        Returns
        -------
        str
            id of the parent peptide
        """          
        return self._peptide_id

    @peptide_id.setter
    def peptide_id(self, peptide_id):
        self._peptide_id = peptide_id

    @property
    def coordinate(self):
        """
        coordinate gets atom's coordinate

        The coordinate default to be ``np.array([0, 0, 0]) * angstrom``

        Returns
        -------
        np.ndarray(dtype=Quantity)
            coordinate
        """        
        return np.copy(self._coordinate)

    @coordinate.setter
    def coordinate(self, coordinate):
        """
        setter method to set atom's coordinate

        Parameters
        ----------
        coordinate : np.ndarry or list
            atom's coordinate, Unit default to be ``angstrom`` if float list or array is provided

        Raises
        ------
        ValueError
            When the length of input ``coordinate`` != 3

        ValueError
            When the dimension of input ``coordinate`` is Quantity and != ``BaseDimension(length_dimension=1)``
        """           
        if len(coordinate) != 3:
            raise ValueError('Length of coordinate vector should be 3')
        elif isinstance(coordinate[0], Quantity):
            if coordinate[0].unit.base_dimension != unit.length:
                raise ValueError(
                    'Dimension of parameter coordinate should be m instead of %s' 
                    %(coordinate[0].unit.base_dimension)
                )
            else:
                coordinate = coordinate / angstrom * angstrom
        else:
            coordinate = coordinate * angstrom

        for (i, j) in enumerate(coordinate):
            self._coordinate[i] = j
        
    @property
    def velocity(self):
        """
        velocity gets atom's velocity

        The velocity default to be ``np.array([0, 0, 0]) * angstrom / femtosecond``

        Returns
        -------
        np.ndarray(dtype=Quantity)
            velocity
        """    
        return np.copy(self._velocity)

    @velocity.setter
    def velocity(self, velocity):
        """
        setter method to set atom's velocity

        Parameters
        ----------
        velocity : np.ndarry or list
            atom's velocity, Unit default to be ``angstrom/femtosecond`` if float list or array is provided

        Raises
        ------
        ValueError
            When the length of input ``velocity`` != 3

        ValueError
            When the dimension of input ``velocity`` is Quantity and != ``BaseDimension(length_dimension=1, time_dimension=-1)``
        """           
        if len(velocity) != 3:
            raise ValueError('Length of velocity vector should be 3')
        elif isinstance(velocity[0], Quantity):
            if velocity[0].unit.base_dimension != unit.velocity:
                raise ValueError(
                    'Dimension of parameter velocity should be m/s instead of %s' 
                    %(velocity[0].unit.base_dimension)
                )
            else:
                velocity = velocity / (angstrom/femtosecond) * (angstrom/femtosecond)
        else:
            velocity = velocity * angstrom / femtosecond

        for (i, j) in enumerate(velocity):
            self._velocity[i] = j

    @property
    def force(self):
        """
        velocity gets atom's force

        The force default to be ``np.array([0, 0, 0]) * kilojoule_permol_over_angstrom``

        Returns
        -------
        np.ndarray(dtype=Quantity)
            force
        """    
        return np.copy(self._force)

    @force.setter
    def force(self, force):
        """
        setter method to set atom's force

        Parameters
        ----------
        force : np.ndarry or list
            atom's force, Unit default to be ``kilojoule_permol_over_angstrom`` if float list or array is provided

        Raises
        ------
        ValueError
            When the length of input ``force`` != 3

        ValueError
            When the dimension of input ``force`` is Quantity and != ``BaseDimension(length_dimension=-1, energy_dimension=1)``
        """           
        if len(force) != 3:
            raise ValueError('Length of velocity vector should be 3')
        elif isinstance(force[0], Quantity):
            if force[0].unit.base_dimension != unit.force:
                raise ValueError(
                    'Dimension of parameter force should be %s instead of %s' 
                    %(unit.force, force[0].unit.base_dimension)
                )
            else:
                force = force / (kilojoule_permol_over_angstrom) * (kilojoule_permol_over_angstrom)
        else:
            force = force * kilojoule_permol_over_angstrom

        for (i, j) in enumerate(force):
            self._force[i] = j

    @property
    def potential_energy(self):
        """
        potential_energy get atom's potential energy

        Returns
        -------
        Quantity
            the potential energy of atom
        """        
        return self._potential_energy

    @potential_energy.setter
    def potential_energy(self, energy):
        """
        setter method to set atom's potential energy

        Parameters
        ----------
        energy : float or Quantity
            atom's potential energy, Unit default to be ``kilojoule_permol`` if float is provided

        Raises
        ------
        ValueError
            When the dimension of input ``energy`` is Quantity and != ``BaseDimension(energy_dimension=1)``
        """           
        if isinstance(energy, Quantity):
            energy = energy.convertTo(kilojoule_permol)
        else:
            energy = energy * kilojoule_permol
        self._potential_energy = energy

    @property
    def kinetic_energy(self):
        """
        kinetic_energy get atom's kinetic energy

        Returns
        -------
        Quantity
            the kinetic energy of atom
        """    
        return self._kinetic_energy

    @kinetic_energy.setter
    def kinetic_energy(self, energy):
        """
        setter method to set atom's kinetic energy

        Parameters
        ----------
        energy : float or Quantity
            atom's kinetic energy, Unit default to be ``kilojoule_permol`` if float is provided

        Raises
        ------
        ValueError
            When the dimension of input ``energy`` is Quantity and != ``BaseDimension(energy_dimension=1)``
        """       
        if isinstance(energy, Quantity):
            energy = energy.convertTo(kilojoule_permol)
        else:
            energy = energy * kilojoule_permol
        self._kinetic_energy = energy