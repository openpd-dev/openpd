import pytest

from .. import Atom, Peptide

class TestPeptide:
    def setup(self):
        self.peptide = Peptide('ASN')
    
    def teardown(self):
        self.peptide = None

    def test_attributes(self):
        assert self.peptide.peptide_type == 'ASN'
        
        assert self.peptide.peptide_id == 0
        self.peptide.peptide_id = 1
        assert self.peptide.peptide_id == 1

        assert self.peptide.chain_id == 0
        self.peptide.chain_id = 1
        assert self.peptide.chain_id == 1

        assert self.peptide.num_atoms == 2

        assert self.peptide.atoms[0].atom_type == 'CA'
        assert self.peptide.atoms[1].atom_type == 'SC'

    def test_exceptions(self):
        with pytest.raises(ValueError):
            Peptide('AN')

        with pytest.raises(AttributeError):
            self.peptide.peptide_type = 1

        with pytest.raises(AttributeError):
            self.peptide.atoms = 1

        with pytest.raises(AttributeError):
            self.peptide.num_atoms = 1

    def test_addAtom(self):
        atom = Atom('CA', 12)
        self.peptide.addAtoms(atom)
        assert self.peptide.num_atoms == 3
        assert self.peptide.atoms[0].peptide_type == 'ASN'

    def test_addAtoms(self):
        atom = Atom('CA', 12)
        self.peptide.addAtoms(*[atom, atom, atom])
        assert self.peptide.num_atoms == 5
        for atom in self.peptide.atoms:
            assert atom.peptide_type == 'ASN'

        for i in range(50):
            self.peptide.addAtoms(atom, atom, atom)
            assert self.peptide.num_atoms == 5 + (i+1) * 3
            for atom in self.peptide.atoms[-3:]:
                assert atom.peptide_type == 'ASN'


    