from copy import deepcopy
from . import Peptide

class Chain(object):
    def __init__(self, chain_id=0):
        super().__init__()
        self.chain_id = chain_id
        self.peptides = []
        self.num_atoms = 0
        self.num_peptides = 0

    def __repr__(self) -> str:
        return ('<Chain object: id %d at 0x%x>' 
            %(self.chain_id, id(self)))

    __str__ = __repr__

    def _addPeptide(self, peptide:Peptide):
        self.peptides.append(deepcopy(peptide))
        self.peptides[-1].setChainId(self.chain_id)
        self.peptides[-1].setPeptideId(self.num_peptides)
        for atom in self.peptides[-1].getAtoms():
            atom.setAtomId(self.num_atoms)
            self.num_atoms += 1
        self.num_peptides += 1

    def addPeptides(self, peptide_vec):
        for peptide in peptide_vec:
            self._addPeptide(peptide)
    
    def setChainId(self, chain_id):
        self.chain_id = chain_id

    def getAtoms(self):
        atoms = []
        for peptide in self.peptides:
            atoms.extend(peptide.getAtoms())
        return atoms

    def getPeptides(self):
        return self.peptides