import os
import numpy as np
from scipy.interpolate import interp1d
from . import Force
from .. import getBond, getUnitVec, isStandardPeptide
from ..unit import *
from ..unit import Quantity
from ..exceptions import RebindError, NotincludedInteractionError

cur_dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
force_field_dir = os.path.join(cur_dir, '../data/pdff/bond')

class PDFFBondForceField:
    def __init__(
        self, peptide_type1, peptide_type2,
    ):
        """
        Parameters
        ----------
        peptide_type1 : str
            The type of peptide 1
        peptide_type2 : str
            The type of peptide 2
            
        Raises
        ------
        openpd.exceptions.PeptideTypeError
            When the peptide type is not in the standard peptide list
            
        openpd.exceptions.NotincludedInteractionError
            When the interaction is not contained in the force field folder
        """    
        isStandardPeptide(peptide_type1, peptide_type2)
        if peptide_type1 == peptide_type2:
            self._key = peptide_type1
            self._name = peptide_type1 + ' Ca-SC bond'
        else:
            self._key = 'CA-CA'
            self._name = peptide_type1 + ' Ca - ' + peptide_type2 + ' Ca bond'
        try:
            self._origin_data = np.load(os.path.join(force_field_dir, self._key + '.npz'))
        except:
            raise NotincludedInteractionError(
                '%s is not contained in PDFF Bond Force Field' 
                %(self._name)    
            ) 
        self._setEnergyInterp()
        self._setForceInterp()

    def __repr__(self) -> str:
        return (
            '<PDFFBondForceField object: %s force field at 0x%x>'
            %(self._name, id(self))
        )

    __str__ = __repr__

    def _setEnergyInterp(self):
        self._energy_interp = interp1d(
            self._origin_data['energy_coord'], 
            self._origin_data['energy_data'], kind='cubic'
        )

    def _setForceInterp(self):
        self._force_interp = interp1d(
            self._origin_data['force_coord'], 
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
        if isinstance(coord, Quantity):
            coord = coord.convertTo(angstrom) / angstrom
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
        if isinstance(coord, Quantity):
            coord = coord.convertTo(angstrom) / angstrom
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

class PDFFBondForce(Force):
    def __init__(
        self, force_id=0, force_group=0,
        derivative_width=0.0001
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
        self._derivative_width = derivative_width
        
        self._num_bonds = 0
        self._potential_energy = 0
        self._force_field_vector = None

    def __repr__(self) -> str:
        return ('<PDFFBondForce object: %d bonds, at 0x%x>'
            %(self._num_bonds, id(self)))
    
    __str__ = __repr__
        
    def bindEnsemble(self, ensemble):
        """
        bindEnsemble overloads ``Force.bindEnsemble()`` to bind ``PDFFBondForce`` to an ``Ensemble`` instance
        
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
        self._num_bonds = ensemble.system.topology.num_bonds
        self._bonds = ensemble.system.topology.bonds
        self._bond_types = [] # This store the type of torsion like ASN-ASP
        for bond in self._bonds:
            self._bond_types.append([
                bond[0].peptide_type,
                bond[1].peptide_type
            ]) # Peptide type of two atoms, if the same, Ca-SC, not Ca-Ca
        self._setForceFieldVector()

    def _setForceFieldVector(self):
        self._testBound()
        if self._num_bonds < 1:
            raise AttributeError(
                'Only %d bond in force object, cannot form force field vector'
                %(self._num_bonds)
            )
        self._force_field_vector = np.zeros(self._num_bonds, dtype=PDFFBondForceField)
        for i, bond_type in enumerate(self._bond_types):
            self._force_field_vector[i] = PDFFBondForceField(
                bond_type[0], bond_type[1]
            )

    def calculateBondEnergy(self, bond_id):
        """
        calculateBondEnergy calculates the potential energy of specific bond

        Parameters
        ----------
        bond_id
            the id of torsion

        Returns
        -------
        Quantity
            The potential energy of specific bond
        """   
        self._testBound()
        bond_length = getBond(
            self._bonds[bond_id][0].coordinate,
            self._bonds[bond_id][1].coordinate
        )
        return self._force_field_vector[bond_id].getEnergy(bond_length)

    def calculatePotentialEnergy(self):
        """
        calculatePotentialEnergy calculates the potential energy of all bonds

        Returns
        -------
        Quantity
            The potential energy of all bonds
        """        
        self._testBound()
        self._potential_energy = 0
        for bond_id in range(self._num_bonds):
            self._potential_energy += self.calculateBondEnergy(bond_id)
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
        atom = self._atoms[atom_id]
        num_bonds = 0
        if atom.atom_type == 'CA':
            if atom.atom_id == 0 or atom.atom_id == self._num_atoms - 1:
                num_bonds = 2
            else:
                num_bonds = 3
        else:
            num_bonds = 1
        bond_info = []
        for bond_id, bond in enumerate(self._bonds):
            if atom in bond:
                bond_info.append(
                    [bond_id, bond, [0, 1] if bond[0]==atom else [1, 0]]
                ) # Locate the position of current in bond
                if len(bond_info) == num_bonds:
                    break
        force = np.zeros(3) * kilocalorie_permol_over_angstrom
        for info in bond_info:
            vec = getUnitVec(
                info[1][info[2][0]].coordinate -
                info[1][info[2][1]].coordinate
            )
            bond_length = getBond(
                info[1][info[2][0]].coordinate, 
                info[1][info[2][1]].coordinate
            )
            force += 0.5 * self._force_field_vector[info[0]].getForce(bond_length) * vec
        return force

    @property
    def num_bonds(self):
        """
        num_bonds gets the number of bonds of ``PDFFBondForce``

        Returns
        -------
        int
            the number of bonds
        """     
        return self._num_bonds

    @property
    def potential_energy(self):
        """
        potential_energy gets the potential energy of all bonds
        
        Returns
        -------
        Quantity
            The potential energy of all bonds 
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