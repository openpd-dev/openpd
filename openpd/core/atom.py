import numpy as np

class Atom(object):
    def __init__(self, atom_type:str, mass) -> None:
        super().__init__()
        self.atom_type = atom_type
        self.atom_id = 0
        self.mass = mass
        self.peptide_type = None
        self.coordinate = np.zeros([3])
        self.velocity = np.zeros([3])

    def __repr__(self) -> str:
        return ('<Atom object: type %s, id %d, of peptide %s at 0x%x>'
            %(self.atom_type, self.atom_id, self.peptide_type, id(self)))

    __str__ = __repr__ 

    def setAtomId(self, atom_id):
        self.atom_id = atom_id

    def setPeptideType(self, peptide_type:str):
        self.peptide_type = peptide_type
    
    def setCoordinate(self, coordinate):
        for (i, j) in enumerate(coordinate):
            self.coordinate[i] = j

    def setVelocity(self, velocity):
        for (i, j) in enumerate(velocity):
            self.velocity[i] = j