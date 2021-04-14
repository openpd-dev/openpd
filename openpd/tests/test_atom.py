#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
file: test_atom.py
created time : 2021/02/04
last edit time : 2021/04/14
author : Zhenyu Wei 
version : 1.0
contact : zhenyuwei99@gmail.com
copyright : (C)Copyright 2021-2021, Zhenyu Wei and Southeast University
'''

import pytest
import numpy as np

from .. import Atom, Molecule, Chain, isArrayEqual
from ..unit import *
from ..unit import Quantity
from ..exceptions import *

class TestAtom:
    def setup(self):
        self.atom = Atom('Ca', 12)

    def teardown(self):
        self.atom = None
        
    def test_attributes(self):
        assert self.atom.atom_type == 'Ca'

        assert self.atom.atom_id == 0
        self.atom.atom_id = 1
        assert self.atom.atom_id == 1

        assert self.atom.mass == 12
        assert isinstance(self.atom.mass, Quantity)
        assert self.atom.mass == 12 * amu

        molecule = Molecule('CLA')
        molecule.molecule_id = 1
        self.atom.parent_molecule = molecule
        assert id(self.atom.parent_molecule) == id(molecule)
        assert self.atom.molecule_id == 1
        assert self.atom.molecule_name == 'CLA'
        # Test of coordinate
        assert isArrayEqual(self.atom._coordinate, np.zeros([3]))
        self.atom.coordinate = [1, 1, 1]
        assert isArrayEqual(self.atom._coordinate, np.ones([3])*angstrom)
        assert self.atom.coordinate[0] == angstrom
        assert isinstance(self.atom.coordinate[0], Quantity)

        # Test of velocity
        assert isArrayEqual(self.atom.velocity, np.zeros([3]))
        self.atom.velocity = [1, 1, 1] 
        assert isArrayEqual(self.atom.velocity, np.ones([3]) * angstrom / femtosecond)
        assert self.atom.velocity[0] == angstrom / femtosecond
        assert isinstance(self.atom.velocity[0], Quantity)

        # Test of potential energy
        assert self.atom.potential_energy == 0 * kilojoule_permol
        self.atom.potential_energy = 1
        assert self.atom.potential_energy == 1 * kilojoule_permol
        self.atom.potential_energy = 1 * kilocalorie_permol
        assert self.atom.potential_energy == 4.184 * kilojoule_permol

        # Test of kinetic energy
        assert self.atom.kinetic_energy == 0 * kilojoule_permol
        self.atom.kinetic_energy = 1
        assert self.atom.kinetic_energy == 1 * kilojoule_permol
        self.atom.kinetic_energy = 1 * kilocalorie_permol
        assert self.atom.kinetic_energy == 4.184 * kilojoule_permol

        # Test of force
        assert isArrayEqual(self.atom.force, np.zeros([3]))
        self.atom.force = [1, 1, 1] 
        assert isArrayEqual(self.atom.force, np.ones([3]) * kilojoule_permol_over_angstrom)
        assert self.atom.force[0] == kilojoule_permol_over_angstrom
        assert isinstance(self.atom.force[0], Quantity)

    def test_exceptions(self):
        with pytest.raises(AttributeError):
            self.atom.atom_type = 1
        
        with pytest.raises(AttributeError):
            self.atom.mass = 1

        with pytest.raises(NonboundError):
            self.atom.molecule_name 

        with pytest.raises(NonboundError):
            self.atom.molecule_id

        with pytest.raises(EditBoundAttributeError):
            molecule = Molecule('CLA')
            molecule.addAtoms(self.atom)
            chain = Chain(0)
            chain.addMolecules(molecule)
            chain.molecules[0].atoms[0].atom_id = 1

        with pytest.raises(ValueError):
            self.atom.coordinate = [2, 2]
        
        with pytest.raises(ValueError):
            self.atom.coordinate = np.array([2, 2])

        with pytest.raises(ValueError):
            self.atom.coordinate = [2, 2, 2] * angstrom / second

        with pytest.raises(ValueError):
            self.atom.coordinate = [2, 2]
        
        with pytest.raises(ValueError):
            self.atom.velocity = np.array([2, 2])

        with pytest.raises(ValueError):
            self.atom.velocity = [2, 2, 2] * angstrom 
