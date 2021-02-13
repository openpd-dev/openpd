import numpy as np

class Atom:
    def __init__(self, atom_type:str, mass) -> None:
        """
        Parameters
        ----------
        atom_type : str
            the type of atom 
        mass : float
            the mass of atom
        """        
        self._atom_type = atom_type
        self._atom_id = 0
        self._mass = mass
        self._peptide_type = None
        self._coordinate = np.zeros([3])
        self._velocity = np.zeros([3])

    def __repr__(self) -> str:
        return ('<Atom object: id %d, type %s, of peptide %s at 0x%x>'
            %(self._atom_id, self._atom_type, self._peptide_type, id(self)))

    __str__ = __repr__ 

    @property
    def atom_type(self):
        """
        atom_type gets atom_type

        Returns
        -------
        str
            the type of atom
        """        
        return self._atom_type

    @property
    def atom_id(self):
        """
        atom_id gets atom_id

        Default value: ``atom_id=0``

        Returns
        -------
        int
            the id of atom
        """        
        return self._atom_id
    
    @atom_id.setter
    def atom_id(self, atom_id:int):    
        self._atom_id = atom_id

    @property
    def mass(self):
        """
        mass gets mass

        Returns
        -------
        float
            mass of atom
        """              
        return self._mass

    @property
    def peptide_type(self):
        """
        peptide_type gets peptide_type

        Default value: ``peptide_type=None``

        Returns
        -------
        str
            type of the parent peptide
        """          
        return self._peptide_type

    @peptide_type.setter
    def peptide_type(self, peptide_type:str):  
        self._peptide_type = peptide_type
    
    @property
    def coordinate(self):
        """
        coordinate gets atom's coordinate

        The coordinate default to be ``np.array([0, 0, 0])``

        Returns
        -------
        np.ndarray
            coordinate
        """        
        return self._coordinate

    @coordinate.setter
    def coordinate(self, coordinate):
        """
        setter method to set atom's coordinate

        Parameters
        ----------
        coordinate : np.ndarry or list
            atom's coordinate

        Raises
        ------
        ValueError
            When the length of input coordinate != 3
        """           
        if len(coordinate) != 3:
            raise ValueError('Dimension of coordinate should be 3')
        for (i, j) in enumerate(coordinate):
            self._coordinate[i] = j

    @property
    def velocity(self):
        """
        velocity gets atom's velocity

        The velocity default to be ``np.array([0, 0, 0])``

        Returns
        -------
        np.ndarray
            velocity
        """    
        return self._velocity

    @velocity.setter
    def velocity(self, velocity):
        """
        setter method to set atom's velocity

        Parameters
        ----------
        velocity : np.ndarry or list
            atom's velocity

        Raises
        ------
        ValueError
            When the length of input velocity != 3
        """           
        if len(velocity) != 3:
            raise ValueError('Dimension of velocity should be 3')
        for (i, j) in enumerate(velocity):
            self._velocity[i] = j