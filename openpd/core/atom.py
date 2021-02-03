import numpy as np

class Atom(object):
    def __init__(self, atom_type:str, mass) -> None:
        super().__init__()
        self._atom_type = atom_type
        self._atom_id = 0
        self._mass = mass
        self._peptide_type = None
        self._coordinate = np.zeros([3])
        self._velocity = np.zeros([3])

    def __repr__(self) -> str:
        return ('<Atom object: type %s, id %d, of peptide %s at 0x%x>'
            %(self._atom_type, self._atom_id, self._peptide_type, id(self)))

    __str__ = __repr__ 

    @property
    def atom_type(self):
        return self._atom_type

    @property
    def atom_id(self):
        return self._atom_id
    
    @atom_id.setter
    def atom_id(self, atom_id:int):
        self._atom_id = atom_id

    @property
    def mass(self):
        return self._mass

    @property
    def peptide_type(self):
        return self._peptide_type

    @peptide_type.setter
    def peptide_type(self, peptide_type:str):
        self._peptide_type = peptide_type
    
    @property
    def coordinate(self):
        return self._coordinate

    @coordinate.setter
    def coordinate(self, coordinate):
        for (i, j) in enumerate(coordinate):
            self._coordinate[i] = j

    @property
    def velocity(self):
        return self._velocity

    @velocity.setter
    def velocity(self, velocity):
        for (i, j) in enumerate(velocity):
            self._velocity[i] = j