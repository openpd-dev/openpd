from . import Chain

class Topology(object):
    def __init__(self) -> None:
        super().__init__()
        self.atoms = []
        self.bonds = []
        self.torsions = []
        self.num_atoms = 0
        self.num_bonds = 0
        self.num_torsions = 0
    
    def __repr__(self) -> str:
        return ('<Topology object: %d atoms, %d bonds, %d torsions at 0x%x>'
            %(self.num_atoms, self.num_bonds, self.num_torsions, id(self)))

    def addChain(self, chain:Chain):
        for i, peptide in enumerate(chain.peptides[:-1]):
            self.bonds.append([peptide.atoms[0], peptide.atoms[1]]) # Ca-Sc bond
            self.bonds.append([peptide.atoms[0], chain.peptides[i+1].atoms[0]]) # Ca- Ca bond
            self.num_bonds += 2
            self.torsions.append([peptide.atoms[1], peptide.atoms[0], chain.peptides[i+1].atoms[0], chain.peptides[i+1].atoms[1]])
            self.num_torsions += 1
        self.bonds.append([chain.peptides[-1].atoms[0], chain.peptides[-1].atoms[1]]) 
        self.num_bonds += 1
        self.atoms.extend(chain.getAtoms())
        self.num_atoms += chain.num_atoms
