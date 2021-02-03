import sys, os, pytest

cur_dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
openpd_dir = os.path.join(cur_dir, '../..')
sys.path.append(openpd_dir)
from openpd import Peptide, Chain, Topology

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
            self.topology.num_torsions = 1

        with pytest.raises(AttributeError):
            self.topology.torsions = 1

    def test_addChain(self):
        chain = Chain(0)
        chain.addPeptides([Peptide('ASN'), Peptide('ALA')])

        self.topology._addChain(chain)

        assert self.topology.num_atoms == 4
        assert self.topology.num_bonds == 3
        assert self.topology.num_torsions == 1

        self.topology._addChain(chain)

        assert self.topology.num_atoms == 8
        assert self.topology.num_bonds == 6
        assert self.topology.num_torsions == 2

        for i in range(50):
            self.topology._addChain(chain)
        assert self.topology.num_atoms == 4 * 52
        assert self.topology.num_bonds == 3 * 52
        assert self.topology.num_torsions == 1 * 52