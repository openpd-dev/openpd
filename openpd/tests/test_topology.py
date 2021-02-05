import pytest

from .. import Peptide, Chain, Topology
from .. import CONST_CA_CA_DISTANCE

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

    def test_addChain(self):
        chain = Chain(0)
        chain.addPeptides(Peptide('ASN'), Peptide('ALA'), Peptide('ASN'))

        self.topology._addChain(chain)

        assert self.topology.num_atoms == 6
        assert self.topology.atoms == chain.atoms
        assert self.topology.num_bonds == 5
        assert self.topology.bonds[0][2] == chain.peptides[0].ca_sc_dist
        assert self.topology.bonds[1][2] == CONST_CA_CA_DISTANCE
        assert self.topology.num_angles == 4
        assert self.topology.num_torsions == 2

        self.topology._addChain(chain)

        assert self.topology.num_atoms == 12
        assert self.topology.num_bonds == 10
        assert self.topology.num_angles == 8
        assert self.topology.num_torsions == 4

        for i in range(50):
            self.topology._addChain(chain)
            assert self.topology.num_atoms == 12 + (i+1) * 6
            assert self.topology.num_bonds == 10 + (i+1) * 5
            assert self.topology.num_angles == 8 + (i+1) * 4
            assert self.topology.num_torsions == 4 + (i+1) * 2