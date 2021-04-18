import pytest

from .. import Atom, Molecule, Chain

class TestChain:
    def setup(self):
        self.chain = Chain(0)

    def teardown(self):
        self.chain = None

    def test_attributes(self):
        assert self.chain.chain_id == 0
        self.chain.chain_id = 1

        assert self.chain.chain_id == 1

        assert self.chain.molecules == []

        assert self.chain.atoms == []

        assert self.chain.num_atoms == 0

        assert self.chain.num_molecules == 0

    def test_exceptions(self):
        with pytest.raises(AttributeError):
            self.chain.num_molecules = 1

        with pytest.raises(AttributeError):
            self.chain.molecules = 1

        with pytest.raises(AttributeError):
            self.chain.num_atoms = 1

        with pytest.raises(AttributeError):
            self.chain.atoms = 1

    def test_addMolecule(self):
        molecule = Molecule('ASN')
        self.chain.addMolecules(molecule)
        
        assert self.chain.num_molecules == 1
        assert self.chain.num_atoms == 0
        assert self.chain.molecules[0].chain_id == 0

    def test_addMolecule(self):
        molecule1 = Molecule('ASN')
        molecule2 = Molecule('ASP')
        self.chain.addMolecules(molecule1, molecule2)

        assert self.chain.num_molecules == 2
        assert self.chain.num_atoms == 0

        self.chain = Chain(0)
        atom1 = Atom('CA', 12)
        atom2 = Atom('SC', 192)
        molecule1.addAtoms(atom1, atom2)
        molecule2.addAtoms(atom1, atom2)
        self.chain.addMolecules(molecule1, molecule2)

        assert self.chain.num_molecules == 2
        assert self.chain.num_atoms == 4
        assert self.chain.atoms[0].molecule_id == 0
        assert self.chain.atoms[3].molecule_id == 1

        for i, molecule in enumerate(self.chain.molecules):
            assert molecule.chain_id == 0
            assert molecule.molecule_id == i

        for i in range(50):
            self.chain.addMolecules(molecule1, molecule2)
            assert self.chain.num_molecules == 2 + (i+1) * 2
            assert self.chain.num_atoms == 4 + (i+1) * 4
            for molecule in self.chain.molecules[-2:]:
                assert molecule.chain_id == 0