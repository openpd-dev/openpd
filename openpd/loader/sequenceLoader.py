import json, codecs
from . import Loader
from .. import Peptide, Chain, System
from .. import SINGLE_LETTER_ABBREVIATION, TRIPLE_LETTER_ABBREVIATION, findFirst

class SequenceLoader(Loader):
    def __init__(self, input_file_path, is_single_letter=False) -> None:
        """
        Parameters
        ----------
        input_file_path : str
            The path of the input *.json* file
        is_single_letter : bool, optional
            The flag of wether the *.json* file is writened in single letter abbreviation, by default False
        """        
        super().__init__(input_file_path, 'json')
        self.is_single_letter = is_single_letter
        self.loadSequence()

    def loadSequence(self):
        """
        loadSequence overloads Loader.loadsequence()

        Raises
        ------
        ValueError
            When the peptide type is not in the standard peptide list.
        """     
        with codecs.open(self.input_file_path, 'r', 'utf-8') as f:
            self.sequence_text = f.read()
        self.sequence_dict = json.loads(self.sequence_text)
        if self.is_single_letter:
            # Change input peptide type into triple letter abbreviation
            for key, value in self.sequence_dict.items():
                if key.upper().startswith('CHAIN'):
                    for i, peptide_type in enumerate(value):
                        if not peptide_type.upper() in SINGLE_LETTER_ABBREVIATION:
                            raise ValueError('Peptide type %s is not in the standard peptide list:\n %s' 
                                 %(peptide_type, SINGLE_LETTER_ABBREVIATION))
                        else:
                            self.sequence_dict[key][i] = TRIPLE_LETTER_ABBREVIATION[findFirst(peptide_type.upper(), SINGLE_LETTER_ABBREVIATION)]
        else:
            for key, value in self.sequence_dict.items():
                if key.upper().startswith('CHAIN'):
                    for i, peptide_type in enumerate(value):
                        if peptide_type in SINGLE_LETTER_ABBREVIATION:
                            raise ValueError('Peptide type %s is a single letter abbreviation, try to use loader=SequenceLoader(file, is_single_letter=True)' 
                                %(peptide_type))
                        if not peptide_type in TRIPLE_LETTER_ABBREVIATION:
                            raise ValueError('Peptide type %s is not in the standard peptide list:\n %s' 
                                 %(peptide_type, SINGLE_LETTER_ABBREVIATION))

    def createSystem(self):
        """
        createSystem creates and returns a ``System`` instance

        Returns
        -------
        System
            A ``System`` instance that has the same topology and peptide sequence with input *.pdb* file
        """
        self.system = System()
        for key, value in self.sequence_dict.items():
            if key.upper().startswith('CHAIN'):
                chain = Chain()
                for peptide_type in value:
                    chain.addPeptides(Peptide(peptide_type))
                self.system.addChains(chain)
        self.guessCoordinates()
        return self.system