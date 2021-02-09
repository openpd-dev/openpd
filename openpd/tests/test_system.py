import pytest
import numpy as np

from .. import Peptide, Chain, System

class TestSystem:
    def setup(self):
        self.system = System()

    def teardown(self):
        self.system = None

    def test_attributes(self):
        assert self.system.num_atoms == 0
        assert self.system.atoms == []

        assert self.system.num_peptides == 0
        assert self.system.peptides == []

        assert self.system.num_chains == 0
        assert self.system.chains == []

        assert self.system.topology.num_atoms == 0
        assert self.system.topology.num_bonds == 0
        assert self.system.topology.num_angles == 0
        assert self.system.topology.num_torsions == 0

        assert len(self.system.coordinate) == 0

    def test_exceptions(self):
        with pytest.raises(AttributeError):
            self.system.num_atoms = 1
        
        with pytest.raises(AttributeError):
            self.system.atoms = 1

        with pytest.raises(AttributeError):
            self.system.num_peptides = 1
        
        with pytest.raises(AttributeError):
            self.system.num_peptides = 1
        
        with pytest.raises(AttributeError):
            self.system.peptides = 1

        with pytest.raises(AttributeError):
            self.system.num_chains = 1
        
        with pytest.raises(AttributeError):
            self.system.chains = 1

        with pytest.raises(AttributeError):
            self.system.topology = 1
        
        with pytest.raises(ValueError):
            self.system.coordinate = np.array([1, 1, 1])

    def test_addChain(self):
        peptide0 = Peptide('ASN')
        peptide1 = Peptide('ALA')

        chain = Chain(0)
        chain.addPeptides(peptide1, peptide1, peptide0)
        
        self.system.addChains(chain)

        assert self.system.num_atoms == 6
        assert self.system.num_peptides == 3
        assert self.system.num_chains == 1

        assert self.system.chains[0].chain_id == 0
        for peptide in self.system.chains[0].peptides:
            assert peptide.chain_id == 0
        assert self.system.topology.num_atoms == 6
        assert self.system.topology.num_bonds == 5
        assert self.system.topology.num_angles == 4
        assert self.system.topology.num_torsions == 2

    def test_addChains(self):
        peptide0 = Peptide('ASN')
        peptide1 = Peptide('ALA')

        chain0 = Chain(0)
        chain1 = Chain(2)

        chain0.addPeptides(peptide1, peptide1, peptide0)
        chain1.addPeptides(peptide0, peptide1, peptide0)

        self.system.addChains(chain0, chain1)

        assert self.system.num_atoms == 12
        assert self.system.num_peptides == 6
        assert self.system.num_chains == 2

        assert self.system.chains[0].chain_id == 0
        for peptide in self.system.chains[0].peptides:
            assert peptide.chain_id == 0
        assert self.system.chains[1].chain_id == 1
        for peptide in self.system.chains[1].peptides:
            assert peptide.chain_id == 1

        assert self.system.topology.num_atoms == 12
        assert self.system.topology.num_bonds == 10
        assert self.system.topology.num_angles == 8
        assert self.system.topology.num_torsions == 4

        for i in range(50):
            self.system.addChains(chain0)
            for peptide in self.system.chains[-1].peptides:
                assert peptide.chain_id == i + 2

            assert self.system.topology.num_atoms == 12 + (i+1) * 6
            assert self.system.topology.num_bonds == 10 + (i+1) * 5
            assert self.system.topology.num_angles == 8 + (i+1) * 4
            assert self.system.topology.num_torsions == 4 + (i+1) * 2