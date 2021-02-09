import pytest, os
import numpy as np
from .. import Atom, RigidBondForce, SequenceLoader

cur_dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))

class TestRigidBondForce:
    def setup(self):
        self.force = RigidBondForce()
        self.system = SequenceLoader(os.path.join(cur_dir, 'data/testForceEncoder.json')).createSystem()

    def teardown(self):
        self.force = None

    def test_attributes(self):
        assert self.force.num_bonds == 0
        assert self.force.bonds == []
        assert self.force.bond_length == []

    def test_exceptions(self):
        with pytest.raises(AttributeError):
            self.force.num_bonds = 1
        
        with pytest.raises(AttributeError):
            self.force.bonds = 1

        with pytest.raises(AttributeError):
            self.force.bond_length = 1

        with pytest.raises(ValueError):
            self.force.addBonds([Atom('CA', 12), Atom('CS', 13)])

    def test_addBond(self):
        atom1 = Atom('CA', 12)
        atom2 = Atom('CS', 13)
        self.force.addBonds([atom1, atom2, 1])
        assert self.force.num_bonds == 1
        assert self.force.bonds == [[atom1, atom2]]
        assert self.force.bond_length == [1]

    def test_addBonds(self):
        atom1 = Atom('CA', 12)
        atom2 = Atom('CS', 13)
        self.force.addBonds([atom1, atom2, 1], [atom2, atom1, 10])
        assert self.force.num_bonds == 2
        assert self.force.bonds == [[atom1, atom2], [atom2, atom1]]
        assert self.force.bond_length == [1, 10]

        self.force.addBonds([atom1, atom2, 1], [atom2, atom1, 10])
        assert self.force.num_bonds == 4
        assert self.force.bonds[-2:] == [[atom1, atom2], [atom2, atom1]]
        assert self.force.bond_length[-2:] == [1, 10]
