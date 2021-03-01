import os
import numpy as np
from scipy.interpolate import interp1d
from . import Force
from .. import getBond, getUnitVec, findAll
from ..unit import *
from ..unit import Quantity

cur_dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
force_field_dir = os.path.join(cur_dir, '../data/pdff/nonbonded')

class PDFFNonBondedForceField:
    def __init__(
        self, peptide_type1, peptide_type2, 
        cutoff_radius=12, derivative_width=0.0001
    ):
        """
        Parameters
        ----------
        peptide_type1 : str
            The type of peptide 1
        peptide_type2 : str
            The type of peptide 1
        cutoff_radius : int or Quantity, optional
            the cutoff radius, by default 12
        derivative_width : float, optional
            the derivative width for the calculation of force, by default 0.0001
            
        Raises
        ------
        ValueError
            When the interaction is not contained in the force field folder
        """        
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
                
        self._origin_coord = np.load(os.path.join(force_field_dir, 'coord.npy'))

        if isinstance(cutoff_radius, Quantity):
            cutoff_radius = cutoff_radius.convertTo(angstrom) / angstrom
        self._cutoff_radius = cutoff_radius
        self._derivative_width = derivative_width

        self._target_coord = np.arange(0, self._cutoff_radius+0.001, 0.001)
        
        self._fixInf()
        self._fixConverge()
        self._guessData()
        self._setEnergyInterpolate()
        self._setForceInterpolate()

    def __repr__(self) -> str:
        return (
            '<PDFFNonBondedForceField object: %s force field at 0x%x>'
            %(self._name, id(self))
        )

    __str__ = __repr__
        
    def _fixInf(self):
        inf_index = findAll(float('inf'), self._origin_data)
        self.k = (self._origin_data[inf_index[-1]+1] - self._origin_data[inf_index[-1]+2]) / (self._origin_coord[inf_index[-1]+1] - self._origin_coord[inf_index[-1]+2])
        for i, j in enumerate(inf_index):
            index = inf_index[-(i+1)]
            self._origin_data[index] =  self.k * (self._origin_coord[index] - self._origin_coord[index+1]) + self._origin_data[index+1]
    
    def _fixConverge(self):
        zero_index = [i for i, j in enumerate(self._origin_data) if self._origin_coord[i]>self._cutoff_radius]
        for index in zero_index:
            self._origin_data[index] = 0
    
    def _guessData(self):
        self._target_data = np.zeros_like(self._target_coord)
        f = interp1d(self._origin_coord, self._origin_data, kind='cubic')
        for i, coord in enumerate(self._target_coord):
            if coord < self._origin_coord[0]:
                self._target_data[i] = self.k * (coord - self._origin_coord[0]) + self._origin_data[0]
            elif coord < self._cutoff_radius:
                self._target_data[i] = f(coord)
        
    def _setEnergyInterpolate(self):
        self._energy_interp = interp1d(self._target_coord, self._target_data, kind='cubic')

    def _setForceInterpolate(self):
        coord = np.arange(0, self._cutoff_radius, self._derivative_width)
        force_coord = coord[:-1] + self._derivative_width * 0.5
        force_data = (self._energy_interp(coord[1:]) - self._energy_interp(coord[:-1])) / self._derivative_width

        self._force_interp = interp1d(force_coord, -force_data, kind='cubic')

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
        if isinstance(coord, Quantity):
            coord = coord.convertTo(angstrom) / angstrom
        if coord <= self._cutoff_radius:
            return self._energy_interp(coord) * kilojoule_permol
        else:
            return 0 * kilojoule_permol

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
        if isinstance(coord, Quantity):
            coord = coord.convertTo(angstrom) / angstrom
        if coord <= self._cutoff_radius:
            return self._force_interp(coord) * kilojoule_permol_over_angstrom
        else:
            return 0 * kilojoule_permol_over_angstrom
        
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
    def cutoff_radius(self):
        """
        cutoff_radius gets the cutoff radius of force field

        Returns
        -------
        Quantity
            the cutoff radius of force field
        """        
        return self._cutoff_radius * angstrom

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

class PDFFNonBondedForce(Force):
    def __init__(
        self, force_id=0, force_group=0,
        cutoff_radius=12, derivative_width=0.0001,
    ) -> None:
        """
        Parameters
        ----------
        force_id : int, optional
            the id of force, by default 0
        force_group : int, optional
            the group of force, by default 0
        cutoff_radius : int, optional
            the cutoff radius, by default ``12 * angstrom``
        derivative_width : float, optional
            the derivative width used to calculate force, by default 0.0001
        """        
        super().__init__(force_id, force_group)
        
        if isinstance(cutoff_radius, Quantity):
            cutoff_radius = cutoff_radius.convertTo(angstrom)
        else:
            cutoff_radius = cutoff_radius * angstrom
        self._cutoff_radius = cutoff_radius
        self._derivative_width = derivative_width
        
        self._num_atoms = 0
        self._num_peptides = 0
        self._potential_energy = 0
        self._force_field_matrix = None
          
    def __repr__(self) -> str:
        return ('<PDFFNonBondedForce object: %d peptides, at 0x%x>'
            %(self._num_peptides, id(self)))
    
    __str__ = __repr__
    
    def bindEnsemble(self, ensemble):
        """
        bindEnsemble overloads ``Force.bindEnsemble()`` to bind PDFFNonBondedForce to an ``Ensemble`` instance
        
        Then, ``self.setEnergyMatrix()`` will be called to set ``self._energy_matrix``, and all the information needed will be extracted from ``ensemble``

        Parameters
        ----------
        ensemble : Ensemble
            An``Ensemble`` instance. 
            
        Raises
        ------
        AttributeError
            When self is bound multi-times
        """        
        if self._is_bound == True:
            raise AttributeError('Force has been bound to %s' %(self._ensemble))
        
        self._is_bound = True
        self._ensemble = ensemble
        self._num_peptides = self._ensemble.system.num_peptides
        self._peptides = self._ensemble.system.peptides
        self._num_atoms = self._ensemble.system.num_atoms
        self._atoms = self._ensemble.system.atoms
        self._setForceFieldMatrix()
    
    def _setForceFieldMatrix(self):
        """
        _setForceFieldMatrix set the ``self.force_field_matrix``

        Raises
        ------
        AttributeError
            When the number of peptides is less than 2
        """        
        if self._num_peptides < 2:
            raise AttributeError(
                'Only %d peptides in force object, cannot form force field matrix'
                %(self._num_peptides)
            )
        self._force_field_matrix = np.zeros([self._num_peptides, self._num_peptides], dtype=PDFFNonBondedForceField)
        for i, peptide1 in enumerate(self._peptides):
            for j, peptide2 in enumerate(self._peptides[i+1:]):
                force_field =  PDFFNonBondedForceField(
                    peptide1.peptide_type, peptide2.peptide_type, 
                    cutoff_radius=self._cutoff_radius,
                    derivative_width=self._derivative_width
                )

                self._force_field_matrix[i, i+j+1] = force_field
                self._force_field_matrix[i+j+1, i] = force_field

    def calculatePairEnergy(self, peptide_id1, peptide_id2):
        """
        calculatePairEnergy calculates the potential energy between two peptides

        Parameters
        ----------
        peptide_id1 : int
            the id of peptide 1
        peptide_id2 : int
            the id of peptide 2

        Returns
        -------
        Quantity
            The potential energy between two peptides
        """        
        self._testBound()
        return self._force_field_matrix[peptide_id1, peptide_id2].getEnergy(
            getBond(
                self._peptides[peptide_id1].atoms[1].coordinate, self._peptides[peptide_id2].atoms[1].coordinate
            ) 
        )

    def calculatePotentialEnergy(self):
        """
        calculatePotentialEnergy calculates the potential energy of all peptides

        Returns
        -------
        Quantity
            The potential energy of all peptides
        """        
        self._testBound()
        self._potential_energy = 0
        for i in range(self._num_peptides):
            for j in range(i+1, self._num_peptides):
                self._potential_energy += self.calculatePairEnergy(i, j)
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
        
        target_atom = self._atoms[atom_id]
        if target_atom.atom_type == 'CA':
            # CA has no interaction in PDFF
            return np.zeros(3) * kilojoule_permol_over_angstrom
        elif target_atom.atom_type == 'SC':
            force = np.zeros(3) * kilojoule_permol_over_angstrom
            target_peptide_id = int((target_atom.atom_id - 1) / 2)
            # All SC atoms
            for peptide_id, atom in enumerate(self._atoms[1::2]):
                bond_length = getBond(target_atom.coordinate, atom.coordinate)
                if(
                    atom.atom_id != target_atom.atom_id and 
                    bond_length <= self._cutoff_radius
                ):
                    vec = getUnitVec(atom.coordinate - target_atom.coordinate)
                    single_force = self._force_field_matrix[target_peptide_id, peptide_id].getForce(bond_length) 
                    force += single_force * vec
            return force

    @property
    def cutoff_radius(self):
        """
        cutoff_radius gets the cutoff radius of force field

        Returns
        -------
        Quantity
            the cutoff radius of force field
        """             
        return self._cutoff_radius

    @property
    def num_peptides(self):
        """
        num_peptides gets the number of peptides of ``PDFFNonBondedForce``

        Returns
        -------
        int
            the number of peptides
        """        
        return self._num_peptides

    @property
    def potential_energy(self):
        """
        potential_energy gets the potential energy of all peptides
        
        Returns
        -------
        Quantity
            The potential energy of all peptides 
        """        
        try:
            self.calculatePotentialEnergy()
            return self._potential_energy
        except:
            return self._potential_energy
    
    @property
    def force_field_matrix(self):
        """
        force_field_matrix gets the force field matrix

        Returns
        -------
        np.ndarray(dtype=PDFFNonBondedForceField)
            force field matrix
        """        
        return self._force_field_matrix