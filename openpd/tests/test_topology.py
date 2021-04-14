import pytest

from .. import Atom, Topology

class TestTopology:
    def setup(self):
        self.topology = Topology()

    def teardown(self):
        self.topology = None

    def test_attributes(self):
        assert self.topology.num_atoms == 0
        assert self.topology.atoms == []

        assert self.topology.num_bonds == 0
        assert self.topology.bonds == []

        assert self.topology.num_torsions == 0
        assert self.topology.torsions == []

    def test_exceptions(self):
        with pytest.raises(AttributeError):
            self.topology.num_atoms = 1

        with pytest.raises(AttributeError):
            self.topology.atoms = 1

        with pytest.raises(AttributeError):
            self.topology.num_bonds = 1
        
        with pytest.raises(AttributeError):
            self.topology.bonds = 1

        with pytest.raises(AttributeError):
            self.topology.num_angles = 1
        
        with pytest.raises(AttributeError):
            self.topology.angles = 1
        
        with pytest.raises(AttributeError):
            self.topology.num_torsions = 1

        with pytest.raises(AttributeError):
            self.topology.torsions = 1
            
    def test_addAtom(self):
        atom1 = Atom('CA', 12)
        self.topology.addAtom(atom1)

        assert self.topology.num_atoms == 1
        assert self.topology.atoms == [atom1]

    def test_addBond(self):
        atom1 = Atom('CA', 12)
        atom2 = Atom('CA', 12)
        self.topology.addBond(atom1, atom2)

        assert self.topology.num_bonds == 1
        assert self.topology.bonds[0][0] == atom1
        assert self.topology.bonds[0][1] == atom2

    def test_addAngle(self):
        atom1 = Atom('CA', 12)
        atom2 = Atom('CA', 12)
        atom3 = Atom('CA', 12)
        self.topology.addAngle(atom1, atom2, atom3)

        assert self.topology.num_angles == 1
        assert self.topology.angles[0][0] == atom1
        assert self.topology.angles[0][1] == atom2
        assert self.topology.angles[0][2] == atom3

    def test_addTorsion(self):
        atom1 = Atom('CA', 12)
        atom2 = Atom('CA', 12)
        atom3 = Atom('CA', 12)
        atom4 = Atom('CA', 12)
        self.topology.addTorsion(atom1, atom2, atom3, atom4)

        assert self.topology.num_torsions == 1
        assert self.topology.torsions[0][0] == atom1
        assert self.topology.torsions[0][1] == atom2
        assert self.topology.torsions[0][2] == atom3
        assert self.topology.torsions[0][3] == atom4