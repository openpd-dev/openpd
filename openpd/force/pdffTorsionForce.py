import os
import numpy as np
from . import Force

CONSTANT_ENERGY_VECTOR_LENGTH = 280
cur_dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
pdff_torison_dir = os.path.join(cur_dir, '../data/pdff/torsion')

class PDFFTorsionForce(Force):
    def __init__(self, force_id=0, force_group=0) -> None:
        super().__init__(force_id, force_group)
        self._num_torsions = 0
        self._torsions = []
        self._torison_types = [] # This store the type of torsion like ASN-ASP
        self._energy_coordinate = np.load(os.path.join(pdff_torison_dir, 'coord.npy'))
        self._energy_array = None

    def _addTorsion(self, torsion):
        self._torsions.append(torsion)
        self._num_torsions += 1
        self._torison_types.append(
            [torsion[1].peptide_type, torsion[2].peptide_type]
        ) # The two Ca Atom's peptide_type

    def addTorsions(self, *torsions):
        for torsion in torsions:
            self._addTorsion(torsion)

    @staticmethod
    def loadEnergyVector(peptide_type1, peptide_type2):
        try:
            return np.load(os.path.join(pdff_torison_dir, 
                '%s-%s.npy' %(peptide_type1, peptide_type2)))
        except:
            try:
                return np.load(os.path.join(pdff_torison_dir, 
                    '%s-%s.npy' %(peptide_type2, peptide_type1)))
            except:
                raise ValueError('%s-%s interaction is not contained in %s' 
                %(peptide_type1, peptide_type2, pdff_torison_dir))

    def setEnergyArray(self):
        self._energy_array = np.zeros([self._num_torsions, CONSTANT_ENERGY_VECTOR_LENGTH])
        for i, torison in enumerate(self._torison_types):
            self._energy_array[i, :] = self.loadEnergyVector(torison[0], torison[1])

    # todo: calculateEnergy, calculateForce
    def calculateEnergy(self):
        pass

    def calculateForce(self):
        pass

    @property
    def num_torsions(self):
        return self._num_torsions

    @property
    def torsions(self):
        return self._torsions

    @property
    def torsion_types(self):
        return self._torison_types

    @property
    def energy_array(self):
        return self._energy_array

    @property
    def energy_coordinate(self):
        return self._energy_coordinate