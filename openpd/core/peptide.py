import json, codecs, os
from copy import deepcopy
from . import Atom
from .. import TRIPLE_LETTER_ABBREVIATION

cur_dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
template_dir = os.path.join(cur_dir, '../data/template/')

class Peptide(object):
    def __init__(self, peptide_type:str, peptide_id=0, chain_id=0): 
        super().__init__()
        if not peptide_type.upper() in TRIPLE_LETTER_ABBREVIATION:
            raise ValueError('Peptide type %s is not in the standard peptide list:\n %s' 
                %(peptide_type, TRIPLE_LETTER_ABBREVIATION))
        self._peptide_type = peptide_type
        self._peptide_id = peptide_id
        self._chain_id = chain_id

        # Reading template json file of corresponding peptide in data/topology folder
        template_file = os.path.join(template_dir, self._peptide_type+'.json')
        with codecs.open(template_file, 'r', 'utf-8') as f:
            template_text = f.read()
        self._template_dict = json.loads(template_text)
        self._ca_sc_dist = self._template_dict['ca_sc_dist']
        
        # Adding atoms as template file
        self._atoms = []
        self._num_atoms = 0
        for (atom_type, info) in list(self._template_dict['parent_atoms'].items()):
            self._addAtom(Atom(atom_type, info['mass']))

    def __repr__(self) -> str:
        return ('<Peptide object: type %s, id %d, of chain %d of 0x%x>' 
            %(self._peptide_type, self._peptide_id, self._chain_id, id(self)))

    __str__ = __repr__

    def _addAtom(self, atom:Atom):
        self._atoms.append(deepcopy(atom))
        self._atoms[-1].peptide_type = self._peptide_type
        self._atoms[-1].atom_id = self._num_atoms
        self._num_atoms += 1
    
    def addAtoms(self, *atoms):
        for atom in atoms:
            self._addAtom(atom)

    @property
    def peptide_type(self):
        return self._peptide_type

    @property
    def peptide_id(self):
        return self._peptide_id
    
    @peptide_id.setter
    def peptide_id(self, peptide_id:int):
        self._peptide_id = peptide_id

    @property
    def chain_id(self):
        return self._chain_id

    @chain_id.setter
    def chain_id(self, chain_id:int):
        self._chain_id = chain_id
    
    @property 
    def atoms(self):
        return self._atoms

    @property
    def num_atoms(self):
        return self._num_atoms

    @property
    def ca_sc_dist(self):
        return self._ca_sc_dist