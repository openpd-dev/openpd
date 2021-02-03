from . import Chain

class Topology(object):
    def __init__(self) -> None:
        super().__init__()
        self._atoms = []
        self._bonds = []
        self._torsions = []
        self._num_atoms = 0
        self._num_bonds = 0
        self._num_torsions = 0
    
    def __repr__(self) -> str:
        return ('<Topology object: %d atoms, %d bonds, %d torsions at 0x%x>'
            %(self._num_atoms, self._num_bonds, self._num_torsions, id(self)))

    __str__ = __repr__

    def addChain(self, chain:Chain):
        for i, peptide in enumerate(chain.peptides[:-1]):
            self._bonds.append([peptide.atoms[0], peptide.atoms[1]]) # Ca-Sc bond
            self._bonds.append([peptide.atoms[0], chain.peptides[i+1].atoms[0]]) # Ca- Ca bond
            self._num_bonds += 2
            self._torsions.append([peptide.atoms[1], peptide.atoms[0], chain.peptides[i+1].atoms[0], chain.peptides[i+1].atoms[1]])
            self._num_torsions += 1
        self._bonds.append([chain.peptides[-1].atoms[0], chain.peptides[-1].atoms[1]]) 
        self._num_bonds += 1
        self._atoms.extend(chain.atoms)
        self._num_atoms += chain.num_atoms

    @property
    def num_atoms(self):
        return self._num_atoms

    @property
    def atoms(self):
        return self._atoms

    @property
    def num_bonds(self):
        return self._num_bonds

    @property
    def bonds(self):
        return self._bonds

    @property
    def num_torsions(self):
        return self._num_torsions

    @property
    def torsions(self):
        return self._torsions

    

    
