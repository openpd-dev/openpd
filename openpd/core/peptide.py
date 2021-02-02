import numpy as np
import json, codecs, os
from copy import deepcopy
from . import Atom
from .. import triple_letter_abbreviation

cur_dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
template_dir = os.path.join(cur_dir, '../data/template/')

class Peptide(object):
    def __init__(self, peptide_type:str, peptide_id=0, chain_id=0): 
        super().__init__()
        if not peptide_type.upper() in triple_letter_abbreviation:
            raise ValueError('Peptide type %s is not in the standard peptide list:\n %s' 
                %(peptide_type, triple_letter_abbreviation))
        self.peptide_type = peptide_type
        self.peptide_id = peptide_id
        self.chain_id = chain_id

        # Reading template json file of corresponding peptide in data/topology folder
        template_file = os.path.join(template_dir, self.peptide_type+'.json')
        with codecs.open(template_file, 'r', 'utf-8') as f:
            template_text = f.read()
        self.template_dict = json.loads(template_text)
        self.ca_sc_dist = self.template_dict['ca_sc_dist']
        
        # Adding atoms as template file
        self.atoms = []
        self.num_atoms = 0
        for (atom_type, info) in list(self.template_dict['parent_atoms'].items()):
            self._addAtom(Atom(atom_type, info['mass']))

    def __repr__(self) -> str:
        return ('<Peptide object: type %s, id %d, of chain %d of 0x%x>' 
            %(self.peptide_type, self.peptide_id, self.chain_id, id(self)))

    __str__ = __repr__

    def _addAtom(self, atom:Atom):
        self.atoms.append(deepcopy(atom))
        self.atoms[-1].setPeptideType(self.peptide_type)
        self.atoms[-1].setAtomId(self.num_atoms)
        self.num_atoms += 1
    
    def addAtoms(self, atom_vec):
        for atom in atom_vec:
            self._addAtom(atom)

    def setPeptideId(self, peptide_id):
        self.peptide_id = peptide_id

    def setChainId(self, chain_id):
        self.chain_id = chain_id

    def getPeptideId(self):
        return self.peptide_id

    def getChainId(self):
        return self.chain_id
    
    def getAtoms(self):
        return self.atoms
