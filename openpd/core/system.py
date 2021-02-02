import numpy as np
from copy import deepcopy
from . import Chain, Topology


class System(object):
    def __init__(self) -> None:
        super().__init__()
        self.chains = []
        self.topology = Topology()
    
        self.num_atoms = 0
        self.num_peptides = 0
        self.num_chains = 0

    def __repr__(self) -> str:
        return ('<System object: %d chains, %d peptides, %d atoms at 0x0x%x>' 
            %(self.num_chains, self.num_peptides, self.num_atoms, id(self)))
        
    def _addChain(self, chain:Chain):
        self.chains.append(deepcopy(chain))
        self.chains[-1].setChainId(self.num_chains) 
        for peptide in self.chains[-1].getPeptides():
            peptide.setChainId(self.num_chains)
            peptide.setPeptideId(self.num_peptides)
            self.num_peptides += 1
        for atom in self.chains[-1].getAtoms():
            atom.setAtomId(self.num_atoms)
            self.num_atoms += 1
        self.num_chains += 1
        self.topology.addChain(self.chains[-1])

    def addChains(self, chain_vec):
        for chain in chain_vec:
            self._addChain(chain)

    def getAtoms(self):
        atoms = []
        for chain in self.chains:
            atoms.extend(chain.getAtoms())
        return atoms
        
    def getPeptides(self):
        peptides = []
        for chain in self.chains:
            peptides.extend(chain.getPeptides())
        return peptides

    def getChains(self):
        return self.chains

    def getTopology(self):
        return self.topology

    def getCoordinate(self):
        coord = []
        for atom in self.getAtoms():
            coord.append(atom.coordinate)
        return np.array(coord)
