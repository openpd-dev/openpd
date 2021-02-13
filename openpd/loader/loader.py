import numpy as np
from numpy import pi, cos, sin
from .. import CONST_CA_CA_DISTANCE

class Loader:
    def __init__(self, input_file_path, input_file_suffix) -> None:
        """
        Parameters
        ----------
        input_file_path : str
            the path of input file
        input_file_suffix : str
            the suffix of input file, like ``input_file_suffix='pdb'``

        Raises
        ------
        ValueError
            When the input file's suffix does not match ``input_file_suffix``
        """        
        if not input_file_path.endswith('.'+input_file_suffix):
            raise ValueError(
                'A .%s file is required instead of %s' 
                %(input_file_suffix, input_file_path)
        )
        self.input_file_path = input_file_path

    def loadSequence(self):
        """
        _loadSequence loads the input file and set ``self.sequence_dict``

        Raises
        ------
        NotImplementedError
            When the subclass does not overload this method
        """        
        raise NotImplementedError('_loadSequence() method has not been overloaded yet!')

    def guessCoordinates(self):
        """
        guessCoordinates generates coord for ``self.system`` by guessing mode.
        """        
        for i, chain in enumerate(self.system.chains):
            init_point = np.random.random(3) + np.array([0, i*5, i*5])
            for j, peptide in enumerate(chain.peptides):
                ca_coord = init_point + np.array([j*CONST_CA_CA_DISTANCE, 0, 0])
                theta = np.random.rand(1)[0] * 2*pi - pi
                sc_coord = ca_coord + np.array([0, peptide._ca_sc_dist*cos(theta), peptide._ca_sc_dist*sin(theta)])
                peptide.atoms[0].coordinate = ca_coord
                peptide.atoms[1].coordinate = sc_coord

    def createSystem(self):
        """
        createSystem creates and returns a ``System`` instance

        Raises
        ------
        NotImplementedError
            When the subclass does not overload this method
        """        
        self.loadSequence()
        raise NotImplementedError('createSystem() method has not been overloaded yet!')
