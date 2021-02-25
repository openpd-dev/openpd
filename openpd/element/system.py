import numpy as np
from copy import deepcopy

from . import Chain, Topology
from .. import isArrayEqual

class System:
    def __init__(self) -> None:
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

    def addChains(self, *chains):
        """
        addChains adds chains to the System

        Parameters
        ----------
        *chains : 
            one or serval Chain instance
        """  
        for chain in chains:
            self._addChain(chain)
        self._cooridnate_shape = list(self.coordinate.shape)

    @property
    def num_atoms(self):
        """
        num_atoms gets the number of atoms in the system

        Returns
        -------
        int
            the number of atoms in the system
        """   
        return self._num_atoms

    @property
    def atoms(self):
        """
        atoms gets a ``list`` contain all atoms in the system

        Returns
        -------
        list(Atom)
            list contain all atoms in the system
        """    
        atoms = []
        for chain in self._chains:
            atoms.extend(chain.atoms)
        return atoms
        
    @property
    def num_peptides(self):
        """
        num_peptides gets the number of peptides in the system

        Returns
        -------
        int
            the number of peptides in the system
        """       
        return self._num_peptides
    
    @property
    def peptides(self):
        """
        peptides gets a ``list`` contain all peptide in the system

        Returns
        -------
        list(Peptide)
            list contain all peptides in the system
        """    
        peptides = []
        for chain in self._chains:
            peptides.extend(chain.peptides)
        return peptides

    @property
    def num_chains(self):
        """
        num_chains gets the number of chains in the system

        Returns
        -------
        int
            the number of chains in the system
        """ 
        return self._num_chains
    
    @property
    def chains(self):
        """
        chains gets a ``list`` contain all peptide in the system

        Returns
        -------
        list(Chain)
            list contain all chains in the system
        """   
        return self._chains

    @property
    def topology(self):
        """
        topology gets the topology of the system

        Returns
        -------
        Topology
            the topology of the system
        """        
        return self._topology

    @property
    def coordinate(self):
        """
        coordinate gets the coordinate of all atoms in the system

        Returns
        -------
        np.ndarray
            the coordinate of all atoms in the system
        """        
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
