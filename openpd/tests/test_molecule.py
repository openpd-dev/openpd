#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
file: test_molecule.py
created time : 2021/04/14
last edit time : 2021/04/14
author : Zhenyu Wei 
version : 1.0
contact : zhenyuwei99@gmail.com
copyright : (C)Copyright 2021-2021, Zhenyu Wei and Southeast University
'''
import pytest
from .. import Atom, Molecule, Chain
from ..exceptions import *

class TestPeptide:
    def setup(self):
        self.molecule = Molecule('ASN')
        atom1 = Atom('CA', 12)
        atom2 = Atom('SC', 192)
        self.molecule.addAtoms(atom1, atom2)
    
    def teardown(self):
        self.molecule = None

    def test_attributes(self):
        assert self.molecule.molecule_name == 'ASN'
        
        assert self.molecule.molecule_id == 0
        self.molecule.molecule_id = 1
        assert self.molecule.molecule_id == 1
        for atom in self.molecule.atoms:
            assert atom.molecule_id == 1

        assert self.molecule.num_atoms == 2

        assert self.molecule.atoms[0].atom_type == 'CA'
        assert self.molecule.atoms[1].atom_type == 'SC'

    def test_exceptions(self):
        with pytest.raises(AttributeError):
            self.molecule.molecule_name = 1

        with pytest.raises(AttributeError):
            self.molecule.atoms = 1

        with pytest.raises(AttributeError):
            self.molecule.num_atoms = 1

        with pytest.raises(NonboundError):
            self.molecule.chain_id

        with pytest.raises(ModifiedBoundMoleculeError):
            chain = Chain(0)
            chain.addMolecules(self.molecule)
            chain.molecules[0].addAtoms(1)

    def test_addAtom(self):
        atom = Atom('CA', 12)
        self.molecule.addAtoms(atom)
        assert self.molecule.num_atoms == 3
        assert self.molecule.atoms[0].molecule_name == 'ASN'

    def test_addAtoms(self):
        atom = Atom('CA', 12)
        self.molecule.addAtoms(*[atom, atom, atom])
        assert self.molecule.num_atoms == 5
        for atom in self.molecule.atoms:
            assert atom.molecule_name == 'ASN'

        for i in range(50):
            self.molecule.addAtoms(atom, atom, atom)
            assert self.molecule.num_atoms == 5 + (i+1) * 3
            for atom in self.molecule.atoms[-3:]:
                assert atom.molecule_name == 'ASN'


    