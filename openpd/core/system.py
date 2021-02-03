import numpy as np
from copy import deepcopy

from . import Chain, Topology
from .. import isArrayEqual

class System(object):
    def __init__(self) -> None:
        super().__init__()
        self._chains = []
        self._topology = Topology()
    
        self._num_atoms = 0
        self._num_peptides = 0
        self._num_chains = 0
        self._cooridnate_shape = list(self.coordinate.shape)

    def __repr__(self) -> str:
        return ('<System object: %d chains, %d peptides, %d atoms at 0x0x%x>' 
            %(self._num_chains, self._num_peptides, self._num_atoms, id(self)))

    __str__ = __repr__
        
    def _addChain(self, chain:Chain):
        self._chains.append(deepcopy(chain))
        self._chains[-1].chain_id = self._num_chains
        for peptide in self._chains[-1].peptides:
            peptide.chain_id = self._num_chains
            peptide.peptide_id = self._num_peptides
            self._num_peptides += 1
        for atom in self._chains[-1].atoms:
            atom.atom_id = self._num_atoms
            self._num_atoms += 1
        self._num_chains += 1
        self._topology._addChain(self._chains[-1])

    def addChains(self, chain_vec):
        for chain in chain_vec:
            self._addChain(chain)
        self._cooridnate_shape = list(self.coordinate.shape)

    @property
    def num_atoms(self):
        return self._num_atoms

    @property
    def atoms(self):
        atoms = []
        for chain in self._chains:
            atoms.extend(chain.atoms)
        return atoms
        
    @property
    def num_peptides(self):
        return self._num_peptides
    
    @property
    def peptides(self):
        peptides = []
        for chain in self._chains:
            peptides.extend(chain.peptides)
        return peptides

    @property
    def num_chains(self):
        return self._num_chains
    
    @property
    def chains(self):
        return self._chains

    @property
    def topology(self):
        return self._topology

    @property
    def coordinate(self):
        coord = []
        for atom in self.atoms:
            coord.append(atom.coordinate)
        return np.array(coord)

    @coordinate.setter
    def coordinate(self, coord):
        coord = np.array(coord)
        if not isArrayEqual(coord.shape, self._cooridnate_shape):
            raise ValueError('Dimension of input %s is different from dimension of coordinate matrix %s' 
                %(coord.shape, self._cooridnate_shape))

        for i, atom in enumerate(self.atoms):
            atom.coordinate = coord[i, :]
