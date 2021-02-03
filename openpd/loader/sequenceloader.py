from . import CONST_CA_SC_DISTANCE
import json, codecs
import numpy as np
from numpy import pi, cos, sin
from .. import Peptide, Chain, System, single_letter_abbreviation, triple_letter_abbreviation

class SequenceLoader(object):
    def __init__(self, sequence_file, is_single_letter=False) -> None:
        super().__init__()
        self.sequence_file = sequence_file
        self.is_single_letter = is_single_letter
        self.loadSequence()

    def loadSequence(self):
        with codecs.open(self.sequence_file, 'r', 'utf-8') as f:
            self.sequence_text = f.read()
        self.sequence_dict = json.loads(self.sequence_text)
        if self.is_single_letter:
            # Change input peptide type into triple letter abbreviation
            for key, value in self.sequence_dict.items():
                if key.upper().startswith('CHAIN'):
                    for i, peptide_type in enumerate(value):
                        if not peptide_type.upper() in single_letter_abbreviation:
                            raise ValueError('Peptide type %s is not in the standard peptide list:\n %s' 
                                 %(peptide_type, single_letter_abbreviation))
                        else:
                            self.sequence_dict[key][i] = triple_letter_abbreviation[single_letter_abbreviation==peptide_type.upper()]

    def createSystem(self):
        self.system = System()
        for key, value in self.sequence_dict.items():
            if key.upper().startswith('CHAIN'):
                chain = Chain()
                for peptide_type in value:
                    chain.addPeptides([Peptide(peptide_type)])
                self.system.addChains([chain])
        self.guessCoordinate()
        return self.system

    def guessCoordinate(self):
        for i, chain in enumerate(self.system.chains):
            init_point = np.random.random(3) + np.array([0, i*5, i*5])
            for i, peptide in enumerate(chain.peptides):
                ca_coord = init_point + np.array([i*CONST_CA_SC_DISTANCE, 0, 0])
                theta = np.random.rand(1)[0] * 2*pi - pi
                sc_coord = ca_coord + np.array([0, peptide._ca_sc_dist*cos(theta), peptide._ca_sc_dist*sin(theta)])
                peptide.atoms[0].coordinate = ca_coord
                peptide.atoms[1].coordinate = sc_coord