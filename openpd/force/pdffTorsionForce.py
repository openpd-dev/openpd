import os
import numpy as np
from numpy import pi, floor
from scipy.interpolate import interp1d
from . import Force
from .. import getTorsion, getNormVec
from ..unit import *

cur_dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
force_field_dir = os.path.join(cur_dir, '../data/pdff/torsion')

class PDFFTorsionForceField:
    def __init__(
        self, peptide_type1, peptide_type2, 
        derivative_width=0.0001
    ): 
        try:
            self._name = peptide_type1 + '-' + peptide_type2
            self._origin_data = np.load(os.path.join(force_field_dir, self._name + '.npy'))
        except:
            try:
                self._name = peptide_type2 + '-' + peptide_type1
                self._origin_data = np.load(os.path.join(force_field_dir, self._name + '.npy'))
            except:
                raise ValueError(
                    '%s-%s interaction is not contained in %s' 
                    %(peptide_type1, peptide_type2, force_field_dir)    
                )
                
        self._derivative_width = derivative_width
        
        self._origin_coord = np.load(os.path.join(force_field_dir, 'coord.npy'))
        self._target_coord = np.arange(-pi, pi+0.001, 0.001)
        self._guessData()
        self._setEnergyInterpolate()
        self._setForceInterpolate()
    
    def __repr__(self) -> str:
        return (
            '<PDFFTorsionForce object: %s force field at 0x%x>'
            %(self._name, id(self))
        )

    __str__ = __repr__

    def _guessData(self):
        f = interp1d(self._origin_coord, self._origin_data, kind='cubic')
        self._target_data = f(self._target_coord)

    def _setEnergyInterpolate(self):
        self._energy_interp = interp1d(self._target_coord, self._target_data, kind='cubic')
        
    def _setForceInterpolate(self):
        coord = np.arange(-pi, pi, self._derivative_width)
        force_coord = coord[:-1] + self._derivative_width * 0.5
        force_data = (self._energy_interp(coord[1:]) - self._energy_interp(coord[:-1])) / self._derivative_width

        self._force_interp = interp1d(force_coord, -force_data, kind='cubic')
        
    def getEnergy(self, coord):
        return self._energy_interp(coord) * kilojoule_permol
    
    def getForce(self, coord):
        return self._force_interp(coord) * kilojoule_permol_over_angstrom

    @property
    def name(self):
        """
        name gets the name of force field

        Returns
        -------
        str
            the name of force field
        """        
        return self._name

    @property
    def derivative_width(self):
        """
        derivative_width gets the derivative width for the calculation of force

        Returns
        -------
        float
            the derivative width for the calculation of force
        """        
        return self._derivative_width

class PDFFTorsionForce(Force):
    def __init__(
        self, force_id=0, force_group=0,
        derivative_width=0.0001
    ) -> None:
        super().__init__(force_id, force_group)
        self._derivative_width = derivative_width
        
        self._num_torsions = 0
        self._potential_energy = 0
        self._force_field_vector = None
        
    def __repr__(self) -> str:
        return ('<PDFFTorsionForce object: %d torsions, at 0x%x>'
            %(self._num_torsions, id(self)))
    
    __str__ = __repr__
        
    def bindEnsemble(self, ensemble):
        if self._is_bound == True:
            raise AttributeError('Force has been bound to %s' %(self._ensemble))
        
        self._is_bound = True
        self._ensemble = ensemble
        
        self._num_atoms = self._ensemble.system.topology.num_atoms
        self._atoms = self._ensemble.system.topology.atoms
        self._num_torsions = ensemble.system.topology.num_torsions
        self._torsions = ensemble.system.topology.torsions
        self._torison_types = [] # This store the type of torsion like ASN-ASP
        for torsion in self._torsions:
            self._torison_types.append([
                torsion[1].peptide_type, 
                torsion[2].peptide_type
            ]) # Parent Peptide of 2 Ca Atom
        self._setForceFieldVector()

    def _setForceFieldVector(self):
        if self._num_torsions < 1:
            raise AttributeError(
                'Only %d torsion in force object, cannot form force field vector'
                %(self._num_torsions)
            )
        self._force_field_vector = np.zeros(self._num_torsions, dtype=PDFFTorsionForceField)
        for i, torison_type in enumerate(self._torison_types):
            self._force_field_vector[i] = PDFFTorsionForceField(
                torison_type[0], torison_type[1]
            )

    # todo: calculateEnergy, calculateForce
    def calculateTorsionEnergy(self, torsion_id):
        self._testBound()
        return self._force_field_vector[torsion_id].getEnergy(
            getTorsion(
                self._torsions[torsion_id][0].coordinate, 
                self._torsions[torsion_id][1].coordinate, 
                self._torsions[torsion_id][2].coordinate, 
                self._torsions[torsion_id][3].coordinate
            )
        )

    def calculatePotentialEnergy(self):
        self._testBound()
        self._potential_energy = 0
        for torsion_id in range(self._num_torsions):
            self._potential_energy += self.calculateTorsionEnergy(torsion_id)
        return self._potential_energy 

    def calculateAtomForce(self, atom_id):
        self._testBound()
        # fixme: Need to multiple 0.5 to each force?
        target_atom = self._atoms[atom_id]
        if target_atom.atom_type == 'CA':
            # CA has no interaction in PDFF
            return np.zeros(3) * kilojoule_permol_over_angstrom
        else:
            force = np.zeros(3) * kilojoule_permol_over_angstrom

            if atom_id == 1:
                # First SC
                torsion_id = 0
                vec = getNormVec(
                    self._torsions[torsion_id][0].coordinate,
                    self._torsions[torsion_id][1].coordinate,
                    self._torsions[torsion_id][2].coordinate
                )
                torsion_angle = getTorsion(
                    self._torsions[torsion_id][0].coordinate, 
                    self._torsions[torsion_id][1].coordinate, 
                    self._torsions[torsion_id][2].coordinate, 
                    self._torsions[torsion_id][3].coordinate
                )
                force += self.force_field_vector[torsion_id].getForce(torsion_angle) * vec
            elif atom_id == self._num_atoms - 1:
                # Last SC
                torsion_id = self._num_torsions - 1
                vec = getNormVec(
                    self._torsions[torsion_id][3].coordinate,
                    self._torsions[torsion_id][2].coordinate,
                    self._torsions[torsion_id][1].coordinate
                )
                torsion_angle = getTorsion(
                    self._torsions[torsion_id][0].coordinate, 
                    self._torsions[torsion_id][1].coordinate, 
                    self._torsions[torsion_id][2].coordinate, 
                    self._torsions[torsion_id][3].coordinate
                )
                force += self.force_field_vector[torsion_id].getForce(torsion_angle) * vec 
            else:
                # Other SC
                torsion_id = int(floor(atom_id/2)) - 1 
                # Atom 3 equals to the second SC and corelated to 0 torsion and 1 torsion
                # Atom 5 equals to the third SC and corelated to 1 torsion and 2 torsion
                vec = getNormVec(
                    self._torsions[torsion_id][0].coordinate,
                    self._torsions[torsion_id][1].coordinate,
                    self._torsions[torsion_id][2].coordinate
                )
                torsion_angle = getTorsion(
                    self._torsions[torsion_id][0].coordinate, 
                    self._torsions[torsion_id][1].coordinate, 
                    self._torsions[torsion_id][2].coordinate, 
                    self._torsions[torsion_id][3].coordinate
                )
                force += self.force_field_vector[torsion_id].getForce(torsion_angle) * vec
                
                torsion_id += 1 # Next torsion
                vec = getNormVec(
                    self._torsions[torsion_id][3].coordinate,
                    self._torsions[torsion_id][2].coordinate,
                    self._torsions[torsion_id][1].coordinate
                )
                torsion_angle = getTorsion(
                    self._torsions[torsion_id][0].coordinate, 
                    self._torsions[torsion_id][1].coordinate, 
                    self._torsions[torsion_id][2].coordinate, 
                    self._torsions[torsion_id][3].coordinate
                )
                force += 0.5 * self.force_field_vector[torsion_id].getForce(torsion_angle) * vec 
                
            return force

    @property
    def num_torsions(self):
        return self._num_torsions

    @property
    def potential_energy(self):
        try:
            self.calculatePotentialEnergy()
            return self._potential_energy
        except:
            return self._potential_energy

    @property
    def force_field_vector(self):
        return self._force_field_vector