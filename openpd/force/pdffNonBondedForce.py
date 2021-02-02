'''
Author: your name
Date: 2021-01-31 21:40:12
LastEditTime: 2021-01-31 21:40:13
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: /openpd/openpd/force/nonbondedforce.py
'''
from . import Force
from .. import Atom
import numpy as np
import os

cur_dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
pdff_nonbonded_dir = os.path.join(cur_dir, '../data/pdff/nonbonded')

class PDFFNonbondedForce(Force):
    def __init__(self, force_id, force_group=0) -> None:
        super().__init__(force_id, force_group)
        self.atoms = []
        self.num_atoms = 0

    def __repr__(self) -> str:
        return ('<PDFFNonbondedForce object: %d atoms, at 0x%x>'
            %(self.num_atoms, id(self)))
    
    __str__ = __repr__

    def _addAtom(self, atom:Atom):
        self.particles.append(atom.atom)
        self.num_particels += 1
    
    def addAtoms(self, atom_vec):
        for atom in atom_vec:
            self._addAtom(atom)