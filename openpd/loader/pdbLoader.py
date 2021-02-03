from openpd.core import atom, peptide
import numpy as np
from numpy import pi, cos, sin
from numpy.lib.arraysetops import unique
from . import CONST_CA_SC_DISTANCE
from .. import Peptide, Chain, System, triple_letter_abbreviation

back_bone_atom = ['N', 'C', 'O', 'CA', 'H', 'H1', 'H2']
element_mass = {
            'H': 1.00800,
            'C': 12.01100,
            'N': 14.00700,
            'O': 15.9990,
            'S': 32.06000
        }

class PDBLoader(object):
    def __init__(self, pdb_file_name, end_label='ENDMDL') -> None:
        super().__init__()
        self.pdb_file_name = pdb_file_name
        self.pdb_file = open(self.pdb_file_name, 'r')
        line = self.pdb_file.readline()
        line = self._readTitleSection(line)
        line = self._readAtomSection(line, end_label)
        self._setPDBInfo()
        self.loadSequence()

    def _skipBlankLine(self, line):
        while line.startswith('\n') or line.startswith('#'):
            line = self.pdb_file.readline()
        return line

    def _skipNoAtomLine(self, line):
        while not line.startswith('ATOM'):
            line = self.pdb_file.readline()
        return line
    
    def _parseLine(self, line):
        data = line.split()
        for (i, value) in enumerate(data):
            try:
                value = float(value)
            except:
                data[i] = value
            else:
                data[i] = value
        return data
    
    @staticmethod
    def _parseAtomLine(self, line):
        data = []
        data.append(int(line[6:11]))
        data.append(line[12:16].strip())
        data.append(line[17:20].strip())
        data.append(line[21])
        data.append(int(line[22:26]))
        data.append(float(line[30:38]))
        data.append(float(line[38:46]))
        data.append(float(line[46:54]))
        return data

    def _readTitleSection(self, line):
        line = self._skipBlankLine(line)
        self._line_NoATOM = []
        while not line.startswith('ATOM'):
            self._line_NoATOM.append(line)
            line = self.pdb_file.readline()
            #self.pbc_inv = np.linalg.inv(self.pbc_diag)
        return line

    def _readAtomSection(self, line, end_label):
            line = self._skipBlankLine(line)
            line = self._skipNoAtomLine(line)
            self._raw_data = []
            self._line_ATOM = []
            while not line.startswith(end_label):
                self._raw_data.append(self._parseAtomLine(line))
                self._line_ATOM.append(line)
                line = self.pdb_file.readline()
            self._line_ATOMEND = line
            return line
    
    def _matchMass(self, atom_name):
        keys = element_mass.keys()
        atom_name = atom_name.upper()
        if len(atom_name) >= 2:
            if atom_name[0:2] in keys:
                return element_mass[atom_name[0:2]]
            elif atom_name[0] in keys:
                return element_mass[atom_name[0]]
            else:
                raise KeyError('Atom %s or Atom %s is not in element_mass %s: '
                        %(atom_name[0:2], atom_name[0], keys))
        else:
            if atom_name[0] in keys:
                return element_mass[atom_name[0]]
            else:
                raise KeyError('Atom %s is not in element_mass %s: '
                        %(atom_name[0], keys))

    def _setPDBInfo(self):
        self._num_atoms = len(self._raw_data)
        self._atom_id = np.ones([self._num_atoms, 1], int)
        self._res_id = np.ones([self._num_atoms, 1], int)
        self._mass = np.ones([self._num_atoms, 1])
        self._coord = np.ones([self._num_atoms, 3])
        self._atom_name = []
        self._res_name = []
        self._chain_name = []
        for (i, data) in enumerate(self._raw_data):
            self._atom_id[i] = int(data[0])
            self._atom_name.append(data[1])
            self._res_name.append(data[2])
            self._chain_name.append(data[3])
            self._res_id[i] = int(data[4])
            self._coord[i, :] = data[5:8]
            self._mass[i] = self._matchMass(data[1])
            self._raw_data[i].append(self._mass[i][0])
        self.num_res = np.unique(self._res_id).shape[0]
        self._num_atoms = len(self._atom_name)
        self._res_id = [np.where(unique(self._res_id)==i)[0][0] for i in self._res_id] # Sort _res_id start from 0 and increase evenly for extractCoordinate

    def loadSequence(self):
        self.sequence_dict = {}
        for chain in unique(self._chain_name):
            sequence = unique([self._res_name[i] for i, j in 
            enumerate(self._chain_name) if j==chain])
            for peptide in sequence:
                if not peptide in triple_letter_abbreviation:
                    raise ValueError('Peptide type %s is not in the standard peptide list:\n %s' 
                    %(peptide, triple_letter_abbreviation))
            self.sequence_dict[chain] = sequence

    def createSystem(self, is_extract_coordinate=True):
        self.system = System()
        for _, value in self.sequence_dict.items():
            chain = Chain()
            for peptide_type in value:
                chain.addPeptides([Peptide(peptide_type)])
            self.system.addChains([chain])
        if is_extract_coordinate:
            self.extractCoordinate()
        else:
            self.guessCoordinate()
        return self.system

    def guessCoordinate(self):
        for i, chain in enumerate(self.system.chains):
            init_point = np.random.random(3) + np.array([0, i*5, i*5])
            for j, peptide in enumerate(chain.peptides):
                ca_coord = init_point + np.array([j*CONST_CA_SC_DISTANCE, 0, 0])
                theta = np.random.rand(1)[0] * 2*pi - pi
                sc_coord = ca_coord + np.array([0, peptide.ca_sc_dist*cos(theta), peptide.ca_sc_dist*sin(theta)])
                peptide.atoms[0].coordinate = ca_coord
                peptide.atoms[1].coordinate = sc_coord

    def _extractCoordinate(self, atom_name, coord, _mass):
        coord_ca = coord[atom_name.index('CA')]
        index_sc = [i for i, j in enumerate(atom_name) if not j in back_bone_atom]
        coord_sc = np.zeros_like(coord[0, :])
        mass_sc = 0
        for index in index_sc:
            coord_sc += coord[index, :] * _mass[index, 0]
            mass_sc += _mass[index, 0]
        coord_sc /= mass_sc
        return coord_ca, coord_sc


    def extractCoordinate(self):
        peptide_id = 0
        for i, chain in enumerate(self.system.chains):
            for j, peptide in enumerate(chain.peptides):
                index = [i for i, j in enumerate(self._res_id) if j==peptide_id]
                atom_name = self._atom_name[index[0]:index[-1]+1]
                coord = self._coord[index[0]:index[-1]+1, :]
                _mass = self._mass[index[0]:index[-1]+1]
                coord_ca, coord_sc = self._extractCoordinate(atom_name, coord, _mass)
                peptide.atoms[0].coordinate = coord_ca
                peptide.atoms[1].coordinate = coord_sc
                peptide_id += 1