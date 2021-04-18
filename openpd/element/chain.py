#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
file: chain.py
created time : 2021/01/17
last edit time : 2021/04/14
author : Zhenyu Wei 
version : 1.0
contact : zhenyuwei99@gmail.com
copyright : (C)Copyright 2021-2021, Zhenyu Wei and Southeast University
'''

from copy import deepcopy
from . import Molecule

class Chain:
    def __init__(self, chain_id=0):
        """
        __init__ 

        Parameters
        ----------
        chain_id : int, optional
            the id of chain, by default 0
        """        
        self._chain_id = chain_id
        self._molecules = []
        self._num_atoms = 0
        self._num_molecules = 0

    def __repr__(self) -> str:
        return ('<Chain object: id %d, with %d molecules, at 0x%x>' 
            %(self._chain_id, self._num_molecules, id(self)))

    __str__ = __repr__

    def _addMolecule(self, molecule: Molecule):
        self._molecules.append(deepcopy(molecule))
        self._molecules[-1].molecule_id = self._num_molecules
        for atom in self._molecules[-1].atoms:
            atom.atom_id = self._num_atoms
            self._num_atoms += 1
        self._num_molecules += 1
        self._molecules[-1].parent_chain = self

    def addMolecules(self, *molecules):
        """
        addPeptides adds molecules to the Chain

        Parameters
        ----------
        *molecules : 
            one or serval Molecule instance
        """        
        for molecule in molecules:
            self._addMolecule(molecule)
    
    @property
    def chain_id(self):
        """
        chain_id gets chain_id

        Returns
        -------
        int
            the id of chain
        """        
        return self._chain_id

    @chain_id.setter
    def chain_id(self, chain_id:int):
        self._chain_id = chain_id

    @property
    def num_atoms(self):
        """
        num_atoms gets the number of atoms in the chain

        Returns
        -------
        int
            the number of atoms in the chain
        """        
        return self._num_atoms

    @property
    def atoms(self):
        """
        atoms gets a ``list`` contain all atoms in the chain

        Returns
        -------
        list(Atom)
            list contain all atoms in the chain
        """    
        atoms = []
        for molecule in self._molecules:
            atoms.extend(molecule.atoms)
        return atoms

    @property 
    def num_molecules(self):
        """
        num_molecules gets the number of molecules in the chain

        Returns
        -------
        int
            the number of molecules in the chain
        """       
        return self._num_molecules

    @property
    def molecules(self):
        """
        molecules gets a ``list`` contain all molecules in the chain

        Returns
        -------
        list(Molecule)
            list contain all molecules in the chain
        """    
        return self._molecules