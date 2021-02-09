from . import Force
from .. import Peptide, getBond
import numpy as np
import os

cur_dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
pdff_nonbonded_dir = os.path.join(cur_dir, '../data/pdff/nonbonded')

CONSTANT_ENERGY_VECTOR_LENGTH = 280

class PDFFNonbondedForce(Force):
    def __init__(self, cutoff_radius=12, force_id=0, force_group=0) -> None:
        super().__init__(force_id, force_group)
        self._peptides = []
        self._num_peptides = 0
        self._cutoff_radius = cutoff_radius
        self._energy_tensor = None 
        self._energy_coordinate = np.load(os.path.join(pdff_nonbonded_dir, 'coord.npy'))

    def __repr__(self) -> str:
        return ('<PDFFNonbondedForce object: %d atoms, at 0x%x>'
            %(self._num_peptides, id(self)))
    
    __str__ = __repr__

    def _addPeptide(self, peptide:Peptide):
        # Does not use deepcopy as we want it will change synchronous
        self._peptides.append(peptide)
        self._num_peptides += 1
    
    def addPeptides(self, *peptides):
        for peptide in peptides:
            self._addPeptide(peptide)

    @staticmethod
    def loadEnergyVector(peptide1:Peptide, peptide2:Peptide):
        try:
            return np.load(os.path.join(pdff_nonbonded_dir, 
                '%s-%s.npy' %(peptide1.peptide_type, peptide2.peptide_type)))
        except:
            try:
                return np.load(os.path.join(pdff_nonbonded_dir, 
                    '%s-%s.npy' %(peptide2.peptide_type, peptide1.peptide_type)))
            except:
                raise ValueError('%s-%s interaction is not contained in %s' 
                %(peptide1.peptide_type, peptide2.peptide_type, pdff_nonbonded_dir))
    
    def setEnergyTensor(self):
        if self._num_peptides < 2:
            raise AttributeError('Only %d peptides in force object, cannot form a energy tensor'
                %(self._num_peptides))
        self._energy_tensor = np.zeros([self._num_peptides, self._num_peptides, CONSTANT_ENERGY_VECTOR_LENGTH])
        # Diagonal vector will all be set to zeros, (self-self interaction is meaningless)
        for i, peptide1 in enumerate(self._peptides):
            for j, peptide2 in enumerate(self._peptides[i+1:]):
                self._energy_tensor[i, i+j+1, :] = self.loadEnergyVector(peptide1, peptide2)
                self._energy_tensor[i+j+1, i, :] = self.loadEnergyVector(peptide1, peptide2)

    # todo: calculateEnergy, calculateForce
    def calculateEnergy(self, peptide_id1, peptide_id2):
        return np.interp(getBond(self.peptides[peptide_id1].atoms[0].coordinate, self.peptides[peptide_id2].atoms[0].coordinate), 
            self._energy_coordinate, self._energy_tensor[peptide_id1, peptide_id2])

    def calculateForce(self, peptide1, peptide2):
        pass 

    @property 
    def num_peptides(self):
        return self._num_peptides

    @property
    def peptides(self):
        return self._peptides

    @property
    def cutoff_radius(self):
        return self._cutoff_radius
    
    @property
    def energy_tensor(self):
        return self._energy_tensor

    @property
    def energy_coordinate(self):
        return self._energy_coordinate