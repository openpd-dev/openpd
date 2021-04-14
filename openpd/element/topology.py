#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
file: topology.py
created time : 2021/02/03
last edit time : 2021/04/13
author : Zhenyu Wei 
version : 1.0
contact : zhenyuwei99@gmail.com
copyright : (C)Copyright 2021-2021, Zhenyu Wei and Southeast University
'''

from . import Atom, Chain

class Topology:
    def __init__(self) -> None:
        self._atoms = []
        self._bonds = []
        self._angles = []
        self._torsions = []
        self._num_atoms = 0
        self._num_bonds = 0
        self._num_angles = 0
        self._num_torsions = 0
    
    def __repr__(self) -> str:
        return ('<Topology object: %d atoms, %d bonds, %d angles, %d torsions at 0x%x>'
            %(self._num_atoms, self._num_bonds, self._num_angles, self._num_torsions, id(self)))

    __str__ = __repr__
    
    def addAtom(self, atom: Atom):
        self._atoms.append(atom)
        self._num_atoms += 1

    def addBond(self, atom1: Atom, atom2: Atom):
        self._bonds.append([atom1, atom2])
        self._num_bonds += 1

    def addAngle(self, atom1: Atom, atom2: Atom, atom3: Atom):
        self._angles.append([atom1, atom2, atom3])
        self._num_angles += 1
    
    def addTorsion(self, atom1: Atom, atom2: Atom, atom3: Atom, atom4: Atom):
        self._torsions.append([atom1, atom2, atom3, atom4])
        self._num_torsions += 1

    @property
    def num_atoms(self):
        """
        num_atoms gets the number of atoms in the topology

        Returns
        -------
        int
            the number of atoms in the topology
        """
        return self._num_atoms

    @property
    def atoms(self):
        """
        atoms gets a ``list`` contain all atoms in the topology

        Returns
        -------
        list(Atom)
            list contain all atoms in the topology
        """ 
        return self._atoms

    @property
    def num_bonds(self):
        """
        num_bonds gets the number of bonds in the topology

        Returns
        -------
        int
            the number of bonds in the topology
        """  
        return self._num_bonds

    @property
    def bonds(self):
        """
        bonds gets a ``list`` contain all bonds in the topology

        a bond is also a list of atom like [atom1, atom2]

        Returns
        -------
        list(list(Atom))
            list contain all bonds in the topology
        """
        return self._bonds

    @property
    def num_angles(self):
        """
        num_angles gets the number of angles in the topology

        Returns
        -------
        int
            the number of angles in the topology
        """  
        return self._num_angles

    @property
    def angles(self):
        """
        angles gets a ``list`` contain all angles in the topology

        an angle is also a list of atom like [atom1, atom2, atom3] for :math:`\\angle 123` 

        Returns
        -------
        list(list(Atom))
            list contain all angles in the topology
        """
        return self._angles

    @property
    def num_torsions(self):
        """
        num_torsions gets the number of torsions in the topology

        Returns
        -------
        int
            the number of torsions in the topology
        """  
        return self._num_torsions

    @property
    def torsions(self):
        """
        torison gets a ``list`` contain all torsions in the topology

        a torsion is also a list of atom like [atom1, atom2, atom3, atom4] for :math:`^2\\angle 1234` 

        Returns
        -------
        list(list(Atom))
            list contain all torsions in the topology
        """
        return self._torsions

    

    
