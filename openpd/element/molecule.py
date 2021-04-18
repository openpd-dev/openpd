#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
file: molecule.py
created time : 2021/04/14
last edit time : 2021/04/15
author : Zhenyu Wei 
version : 1.0
contact : zhenyuwei99@gmail.com
copyright : (C)Copyright 2021-2021, Zhenyu Wei and Southeast University
'''

from copy import deepcopy
from . import Atom
from ..exceptions import *


class Molecule:
    def __init__(self, molecule_name: str) -> None:
        self._molecule_name = molecule_name
        self._molecule_id = 0
        self._parent_chain = None

        self._atoms = []
        self._num_atoms = 0

    def __repr__(self) -> str:
        return ('<Molecule object: id %d, name %s, of chain %d of 0x%x>' 
            %(self._molecule_id, self._molecule_name, self._chain_id, id(self)))

    __str__ = __repr__

    def _addAtom(self, atom: Atom):
        if self._parent_chain != None:
            raise ModifiedBoundMoleculeError(
                'Molecule has been bound to Chain %d, cannot add more atoms!'
                %(self._parent_chain.chain_id)
            )
        self._atoms.append(deepcopy(atom))
        self._atoms[-1].atom_id = self._num_atoms
        self._num_atoms += 1
        self._atoms[-1].parent_molecule = self  # This should be the last due to the ModifiedBoundMoleculeError

    def addAtoms(self, *atoms):
        for atom in atoms:
            self._addAtom(atom)

    @property
    def molecule_name(self):
        return self._molecule_name

    @property
    def molecule_id(self):
        return self._molecule_id

    @molecule_id.setter
    def molecule_id(self, molecule_id: int):
        self._molecule_id = molecule_id

    @property
    def parent_chain(self):
        """
        chain_id gets the id of parent chain

        Returns
        -------
        int
            the id of parent chain
        """
        return self._parent_chain

    @parent_chain.setter
    def parent_chain(self, chain):
        self._parent_chain = chain

    @property
    def chain_id(self):
        if self._parent_chain == None:
            raise NonboundError(
                'Molecule has not been bound to any chain'
            )     
        return self._parent_chain.chain_id
    
    @property 
    def atoms(self):
        """
        atoms gets a ``list`` contain all atoms in the peptide

        Returns
        -------
        list(Atom)
            list contain all atoms in the peptide
        """    
        return self._atoms

    @property
    def num_atoms(self):
        """
        num_atoms gets the number of atoms in the peptide

        Returns
        -------
        int
            the number of atoms in the peptide
        """        
        return self._num_atoms