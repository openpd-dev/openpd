import pytest
import numpy as np

from .. import Atom, Molecule, Chain, System

class TestSystem:
    def setup(self):
        self.system = System()

    def teardown(self):
        self.system = None

    def test_attributes(self):
        assert self.system.num_atoms == 0
        assert self.system.atoms == []

        assert self.system.num_molecules == 0
        assert self.system.molecules == []

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
            self.system.num_molecules = 1
        
        with pytest.raises(AttributeError):
            self.system.molecules = 1

        with pytest.raises(AttributeError):
            self.system.num_chains = 1
        
        with pytest.raises(AttributeError):
            self.system.chains = 1

        with pytest.raises(AttributeError):
            self.system.topology = 1
        
        with pytest.raises(ValueError):
            self.system.coordinate = np.array([1, 1, 1])

    def test_addChain(self):
        molecule0 = Molecule('ASN')
        molecule1 = Molecule('ASP')

        atom1 = Atom('CA', 12)
        atom2 = Atom('SC', 192)
        molecule0.addAtoms(atom1, atom2)
        molecule1.addAtoms(atom1, atom2)

        chain = Chain(0)
        chain.addMolecules(molecule1, molecule0, molecule1)

        assert chain.num_molecules == 3
        assert chain.num_atoms == 6
        
        self.system.addChains(chain)

        assert self.system.num_atoms == 6
        assert self.system.num_molecules == 3
        assert self.system.num_chains == 1

        assert self.system.chains[0].chain_id == 0
        for molecule in self.system.chains[0].molecules:
            assert molecule.chain_id == 0

    def test_addChains(self):
        molecule0 = Molecule('ASN')
        molecule1 = Molecule('ASP')

        atom1 = Atom('CA', 12)
        atom2 = Atom('SC', 192)
        molecule0.addAtoms(atom1, atom2)
        molecule1.addAtoms(atom1, atom2)

        chain0 = Chain(0)
        chain1 = Chain(2)

        chain0.addMolecules(molecule1, molecule1, molecule0)
        chain1.addMolecules(molecule0, molecule1, molecule0)

        self.system.addChains(chain0, chain1)

        assert self.system.num_atoms == 12
        assert self.system.num_molecules == 6
        assert self.system.num_chains == 2

        assert self.system.chains[0].chain_id == 0
        for molecule in self.system.chains[0].molecules:
            assert molecule.chain_id == 0
        assert self.system.chains[1].chain_id == 1
        for molecule in self.system.chains[1].molecules:
            assert molecule.chain_id == 1

        for i in range(50):
            self.system.addChains(chain0)
            for molecule in self.system.chains[-1].molecules:
                assert molecule.chain_id == i + 2