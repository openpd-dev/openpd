import os, pickle
import numpy as np
from numpy import pi, floor
from scipy.interpolate import interp1d
from . import Force
from .. import getTorsion, getNormVec, isStandardPeptide
from ..unit import *
from ..exceptions import RebindError, NotincludedInteractionError

cur_dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
force_field_dir = os.path.join(cur_dir, '../data/pdff/torsion')

class PDFFTorsionForceField:
    def __init__(
        self, peptide_type1, peptide_type2
    ): 
        """
        Parameters
        ----------
        peptide_type1 : str
            The type of peptide 1
        peptide_type2 : str
        derivative_width : float, optional
            the derivative width for the calculation of force, by default 0.0001

        Raises
        ------
        openpd.exceptions.NotincludedInteractionError
            When the interaction is not contained in the force field folder
        """      
        isStandardPeptide(peptide_type1, peptide_type2)  
        try:
            self._name = peptide_type1 + '-' + peptide_type2
            self._origin_data = np.load(os.path.join(force_field_dir, self._name + '.npz'))
        except:
            try:
                self._name = peptide_type2 + '-' + peptide_type1
                self._origin_data = np.load(os.path.join(force_field_dir, self._name + '.npz'))
            except:
                raise NotincludedInteractionError(
                    '%s-%s interaction is not contained in %s' 
                    %(peptide_type1, peptide_type2, force_field_dir)    
                )
                
        self._setEnergyInterpolate()
        self._setForceInterpolate()
    
    def __repr__(self) -> str:
        return (
            '<PDFFTorsionForce object: %s force field at 0x%x>'
            %(self._name, id(self))
        )

    __str__ = __repr__

    def _setEnergyInterpolate(self):
        coord = np.array(self._origin_data['energy_coord'])
        coord[0] = -np.pi - 0.000001
        coord[-1] = np.pi + 0.000001
        self._energy_interp = interp1d(
            coord, 
            self._origin_data['energy_data'], kind='cubic'
        )

    def _setForceInterpolate(self):
        coord = np.array(self._origin_data['force_coord'])
        coord[0] = -np.pi - 0.000001
        coord[-1] = np.pi + 0.000001
        self._force_interp = interp1d(
            coord, 
            self._origin_data['force_data'], kind='cubic'
        )
        
    def getEnergy(self, coord):
        """
        getEnergy calculates the energy in specific coordinate

        Parameters
        ----------
        coord : float or list or np.ndarray
            The coordinate of the wanted energy

        Returns
        -------
        float or np.ndarry
            The energy in giving coordinate
        """        
        return self._energy_interp(coord) * kilojoule_permol
    
    def getForce(self, coord):
        """
        getForce calculates the force in specific coordinate

        Parameters
        ----------
        coord : float or list or np.ndarray
            The coordinate of the wanted force

        Returns
        -------
        float or np.ndarry
            The force in giving coordinate
        """        
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

class PDFFTorsionForce(Force):
    def __init__(
        self, force_id=0, force_group=0
    ) -> None:
        """
        Parameters
        ----------
        force_id : int, optional
            the id of force, by default 0
        force_group : int, optional
            the group of force, by default 0
        derivative_width : float, optional
            the derivative width used to calculate force, by default 0.0001
        """        
        super().__init__(force_id, force_group)
        
        self._num_torsions = 0
        self._potential_energy = 0
        self._force_field_vector = None
        
    def __repr__(self) -> str:
        return ('<PDFFTorsionForce object: %d torsions, at 0x%x>'
            %(self._num_torsions, id(self)))
    
    __str__ = __repr__
        
    def bindEnsemble(self, ensemble):
        """
        bindEnsemble overloads ``Force.bindEnsemble()`` to bind ``PDFFTorsionForce`` to an ``Ensemble`` instance
        
        Then, all the information needed will be extracted from ``ensemble`` and ``self.setEnergyVector()`` will be called to set ``self._energy_vector``

        Parameters
        ----------
        ensemble : Ensemble
            An``Ensemble`` instance. 
            
        Raises
        ------
        openpd.exceptions.RebindError
            When ``self`` is bound multi-times
        """        
        if self._is_bound == True:
            raise RebindError('Force has been bound to %s' %(self._ensemble))
        
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
            ]) # Parent Molecule of 2 Ca Atom
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

    def calculateTorsionEnergy(self, torsion_id):
        """
        calculateTorsionEnergy calculates the potential energy of specifc torsion

        Parameters
        ----------
        torsion_id : id
            the id of torsion

        Returns
        -------
        Quantity
            The potential energy of specifc torsion
        """        
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
        """
        calculatePotentialEnergy calculates the potential energy of all torsions

        Returns
        -------
        Quantity
            The potential energy of all torsions
        """        
        self._testBound()
        self._potential_energy = 0
        for torsion_id in range(self._num_torsions):
            self._potential_energy += self.calculateTorsionEnergy(torsion_id)
        return self._potential_energy 

    def calculateAtomForce(self, atom_id):
        """
        calculateAtomForce calculates the force acts on atom

        Parameters
        ----------
        atom_id : int
            The id of atom

        Returns
        -------
        Quantity
            the force acts on atom
        """        
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
                force += 0.5 * self.force_field_vector[torsion_id].getForce(torsion_angle) * vec 
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
                force += 0.5 * self.force_field_vector[torsion_id].getForce(torsion_angle) * vec 
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
                force += 0.5 * self.force_field_vector[torsion_id].getForce(torsion_angle) * vec 
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
        """
        num_torsions gets the number of torsions of ``PDFFTorsionForce``

        Returns
        -------
        int
            the number of torsions
        """      
        return self._num_torsions

    @property
    def potential_energy(self):
        """
        potential_energy gets the potential energy of all torsions
        
        Returns
        -------
        Quantity
            The potential energy of all torsions 
        """        
        try:
            self.calculatePotentialEnergy()
            return self._potential_energy
        except:
            return self._potential_energy

    @property
    def force_field_vector(self):
        """
        force_field_vector gets the force field vector

        Returns
        -------
        np.ndarray(dtype=PDFFTorsionForceField)
            force field vector
        """      
        return self._force_field_vector