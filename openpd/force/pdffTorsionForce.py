import os
import numpy as np
from numpy import pi 
from scipy.interpolate import interp1d
from . import Force
from .. import getTorsion
from ..unit import *

cur_dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
force_field_dir = os.path.join(cur_dir, '../data/pdff/torsion')

class PDFFTorsionForceField:
    def __init__(
        self, peptide_type1, peptide_type2, 
        target_coord=np.linspace(-pi, pi, 600)
    ): 
        self._name = peptide_type1 + '-' + peptide_type2
        self._target_coord = target_coord

        self._origin_coord = np.load(os.path.join(force_field_dir, 'coord.npy'))
        self._origin_data = np.load(os.path.join(force_field_dir, self._name + '.npy'))
        self.guessData()

    def guessData(self):
        f = interp1d(self._origin_coord, self._origin_data, kind='cubic')
        self._target_data = f(self._target_coord)

    def getInterpolate(self):
        return interp1d(self._target_coord, self._target_data, kind='cubic')

    @property
    def name(self):
        return self._name

    @property
    def target_coord(self):
        return self._target_coord

    @property
    def target_data(self):
        return self._target_data

class PDFFTorsionForce(Force):
    def __init__(self, force_id=0, force_group=0) -> None:
        super().__init__(force_id, force_group)
        self._num_torsions = 0
        self._torsions = []
        self._torison_types = [] # This store the type of torsion like ASN-ASP
        self._energy_coordinate = np.load(os.path.join(force_field_dir, 'coord.npy'))
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

    def loadForceField(self, peptide_type1, peptide_type2):
        try:
            return PDFFTorsionForceField(peptide_type1, peptide_type2, self._energy_coordinate)
        except:
            try:
                return PDFFTorsionForceField(peptide_type2, peptide_type1, self._energy_coordinate)
            except:
                raise ValueError(
                    '%s-%s interaction is not contained in %s' 
                    %(peptide_type1, peptide_type2, force_field_dir)    
                )

    def setEnergyVector(self):
        if self._num_torsions < 1:
            raise AttributeError(
                'Only %d torsions in force object, cannot form a energy matrix'
                %(self._num_torsions)
            )
        self._energy_vector = np.zeros(self._num_torsions, dtype=interp1d)
        for i, torison_type in enumerate(self._torison_types):
            self._energy_vector[i] = self.loadForceField(torison_type[0], torison_type[1]).getInterpolate()

    # todo: calculateEnergy, calculateForce
    def calculateEnergy(self, torsion_id):
        return self._energy_vector[torsion_id](
            getTorsion(
                self.torsions[0].coordinate, 
                self.torsions[1].coordinate, 
                self.torsions[2].coordinate, 
                self.torsions[3].coordinate
            )
        ) * kilojoule_permol

    def calculateForce(self, torsion_id, derivative_width=0.0001):
        torsion_angle = getTorsion(
                self.torsions[0].coordinate, 
                self.torsions[1].coordinate, 
                self.torsions[2].coordinate, 
                self.torsions[3].coordinate
        )
        # Fixme: The unit derivation of torsion energy
        return (
            -(self._energy_vector[torsion_id](torsion_angle+derivative_width)
            - self._energy_vector[torsion_id](torsion_angle-derivative_width)) / (2*derivative_width)
            * kilojoule_permol / angstrom
        )

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