from copy import deepcopy
from . import Peptide

class Chain:
    def __init__(self, chain_id=0):
        """
        __init__ 

        Parameters
        ----------
        chain_id : int, optional
            the id of chain, by default 0
        """        
        self._chain_id = chain_id
        self._peptides = []
        self._num_atoms = 0
        self._num_peptides = 0

    def __repr__(self) -> str:
        return ('<Chain object: id %d, with %d peptides, at 0x%x>' 
            %(self._chain_id, self._num_peptides, id(self)))

    __str__ = __repr__

    def _addPeptide(self, peptide:Peptide):
        self._peptides.append(deepcopy(peptide))
        self._peptides[-1].chain_id = self._chain_id
        self._peptides[-1].peptide_id = self._num_peptides
        for atom in self._peptides[-1].atoms:
            atom.atom_id = self._num_atoms
            self._num_atoms += 1
        self._num_peptides += 1

    def addPeptides(self, *peptides):
        """
        addPeptides adds peptides to the Chain

        Parameters
        ----------
        *peptides : 
            one or serval Peptide instance
        """        
        for peptide in peptides:
            self._addPeptide(peptide)
    
    @property
    def chain_id(self):
        """
        chain_id gets chain_id

        Returns
        -------
        int
            the id of chain
        """        
        return self._chain_id

    @chain_id.setter
    def chain_id(self, chain_id:int):
        self._chain_id = chain_id

    @property
    def num_atoms(self):
        """
        num_atoms gets the number of atoms in the chain

        Returns
        -------
        int
            the number of atoms in the chain
        """        
        return self._num_atoms

    @property
    def atoms(self):
        """
        atoms gets a ``list`` contain all atoms in the chain

        Returns
        -------
        list(Atom)
            list contain all atoms in the chain
        """    
        atoms = []
        for peptide in self._peptides:
            atoms.extend(peptide.atoms)
        return atoms

    @property 
    def num_peptides(self):
        """
        num_peptides gets the number of peptides in the chain

        Returns
        -------
        int
            the number of peptides in the chain
        """       
        return self._num_peptides

    @property
    def peptides(self):
        """
        peptides gets a ``list`` contain all peptide in the chain

        Returns
        -------
        list(Peptide)
            list contain all peptides in the chain
        """    
        return self._peptides