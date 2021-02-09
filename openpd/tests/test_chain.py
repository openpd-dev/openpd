import pytest

from .. import Peptide, Chain

class TestChain:
    def setup(self):
        self.chain = Chain(0)

    def teardown(self):
        self.chain = None

    def test_attributes(self):
        assert self.chain.chain_id == 0
        self.chain.chain_id = 1
        assert self.chain.chain_id == 1

        assert self.chain.peptides == []

        assert self.chain.atoms == []

        assert self.chain.num_atoms == 0

        assert self.chain.num_peptides == 0

    def test_exceptions(self):
        with pytest.raises(AttributeError):
            self.chain.num_peptides = 1

        with pytest.raises(AttributeError):
            self.chain.peptides = 1

        with pytest.raises(AttributeError):
            self.chain.num_atoms = 1

        with pytest.raises(AttributeError):
            self.chain.atoms = 1

    def test_addPeptide(self):
        peptide = Peptide('ASN')
        self.chain.addPeptides(peptide)
        
        assert self.chain.num_peptides == 1
        assert self.chain.num_atoms == 2
        assert self.chain.peptides[0].chain_id == 0

    def test_addPeptides(self):
        peptide1 = Peptide('ASN')
        peptide2 = Peptide('ALA')
        self.chain.addPeptides(peptide1, peptide2)

        assert self.chain.num_peptides == 2
        assert self.chain.num_atoms == 4
        for id, peptide in enumerate(self.chain.peptides):
            assert peptide.chain_id == 0
            assert peptide.peptide_id == id

        for i in range(50):
            self.chain.addPeptides(peptide1, peptide2)
            assert self.chain.num_peptides == 2 + (i+1) * 2
            assert self.chain.num_atoms == 4 + (i+1) * 4
            for peptide in self.chain.peptides[-2:]:
                assert peptide.chain_id == 0