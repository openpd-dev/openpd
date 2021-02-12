import numpy as np

class Atom(object):
    def __init__(self, atom_type:str, mass) -> None:
        """__init__ Create an Atom instance

        :param atom_type: the type of atom 
        :type atom_type: str
        :param mass: the mass of atom
        :type mass: float
        """        
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
        """atom_type property method to get atom_type

        :return: the type of atom
        :rtype: str
        """        
        return self._atom_type

    @property
    def atom_id(self):
        """atom_id property method to get atom_id

        :return: the id of atom
        :rtype: int
        """        
        return self._atom_id
    
    @atom_id.setter
    def atom_id(self, atom_id:int):
        """atom_id setter method to set atom_id

        :param atom_id: the id of atom 
        :type atom_id: int
        :return: None
        """        
        self._atom_id = atom_id

    @property
    def mass(self):
        """mass property method to get mass

        :return: mass of atom
        :rtype: float
        """        
        return self._mass

    @property
    def peptide_type(self):
        """peptide_type property method to get peptide_type

        If atom has not been added to any Peptide, peptide_type=None

        :return: type of parent peptide
        :rtype: str
        """        
        return self._peptide_type

    @peptide_type.setter
    def peptide_type(self, peptide_type:str):  
        """peptide_type setter method to set peptide_type

        :param peptide_type: the type of parent peptide
        :type peptide_type: str
        :return: None
        """          
        self._peptide_type = peptide_type
    
    @property
    def coordinate(self):
        """coordinate property method to get atom's coordinate

        The coordinate default to be np.array([0, 0, 0])

        :return: coordinate
        :rtype: np.ndarray
        """        
        return self._coordinate

    @coordinate.setter
    def coordinate(self, coordinate):
        """coordinate setter method to set atom's coordinate

        :param coordinate: atom's coordinate
        :type coordinate: np.ndarry or list
        :return: None
        """       
        if len(coordinate) != 3:
            raise ValueError('Dimension of coordinate should be 3')
        for (i, j) in enumerate(coordinate):
            self._coordinate[i] = j

    @property
    def velocity(self):
        """velocity property method to get atom's coordinate

        The velocity default to be np.array([0, 0, 0])

        :return: atom's velocity
        :rtype: np.ndarray
        """       
        return self._velocity

    @velocity.setter
    def velocity(self, velocity):
        """velocity setter method to set atom's coordinate

        :param velocity: atom's velocity
        :type velocity: np.ndarry or list
        :return: None
        """       
        if len(velocity) != 3:
            raise ValueError('Dimension of velocity should be 3')
        for (i, j) in enumerate(velocity):
            self._velocity[i] = j