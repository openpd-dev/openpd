import os
import numpy as np
from scipy.interpolate import interp1d
from . import Force
from .. import Peptide
from .. import getBond, findAll
from ..unit import *

cur_dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
force_field_dir = os.path.join(cur_dir, '../data/pdff/nonbonded')

class PDFFNonBondedForceField:
    def __init__(
        self, peptide_type1, peptide_type2, 
        target_coord=np.linspace(0, 30, 601), cutoff_radius=12
    ):
        self._name = peptide_type1 + '-' + peptide_type2
        self._target_coord = target_coord
        self._cutoff_radius = cutoff_radius
        
        self._origin_coord = np.load(os.path.join(force_field_dir, 'coord.npy'))
        self._origin_data = np.load(os.path.join(force_field_dir, self._name + '.npy'))
        self.fixInf()
        self.fixConverge()
        self.guessData()
        
    def fixInf(self):
        inf_index = findAll(float('inf'), self._origin_data)
        self.k = (self._origin_data[inf_index[-1]+1] - self._origin_data[inf_index[-1]+2]) / (self._origin_coord[inf_index[-1]+1] - self._origin_coord[inf_index[-1]+2])
        for i, j in enumerate(inf_index):
            index = inf_index[-(i+1)]
            self._origin_data[index] =  self.k * (self._origin_coord[index] - self._origin_coord[index+1]) + self._origin_data[index+1]
    
    def fixConverge(self):
        zero_index = [i for i, j in enumerate(self._origin_data) if self._origin_coord[i]>self._cutoff_radius]
        for index in zero_index:
            self._origin_data[index] = 0
    
    def guessData(self):
        self._target_data = np.zeros_like(self._target_coord)
        f = interp1d(self._origin_coord, self._origin_data, kind='cubic')
        for i, coord in enumerate(self._target_coord):
            if coord < self._origin_coord[0]:
                self._target_data[i] = self.k * (coord - self._origin_coord[0]) + self._origin_data[0]
            elif coord < self._cutoff_radius:
                self._target_data[i] = f(coord)
        
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

    @property
    def cutoff_radius(self):
        return self._cutoff_radius

class PDFFNonbondedForce(Force):
    def __init__(self, cutoff_radius=12, force_id=0, force_group=0) -> None:
        super().__init__(force_id, force_group)
        self._peptides = []
        self._num_peptides = 0
        self._cutoff_radius = cutoff_radius
        self._energy_matrix = None 
        self._energy_coordinate = np.linspace(0, 30, 601)

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

    def loadForceField(self, peptide_type1, peptide_type2):
        try:
            return PDFFNonBondedForceField(peptide_type1, peptide_type2, self._energy_coordinate, cutoff_radius=self._cutoff_radius)
        except:
            try:
                return PDFFNonBondedForceField(peptide_type2, peptide_type1, self._energy_coordinate, cutoff_radius=self._cutoff_radius)
            except:
                raise ValueError(
                    '%s-%s interaction is not contained in %s' 
                    %(peptide_type1, peptide_type2, force_field_dir)    
                )
    
    def setEnergyMatrix(self):
        if self._num_peptides < 2:
            raise AttributeError(
                'Only %d peptides in force object, cannot form a energy matrix'
                %(self._num_peptides)
            )
        self._energy_matrix = np.zeros([self._num_peptides, self._num_peptides], dtype=interp1d)
        # self._energy_matrix = [[0 for i in range(self._num_peptides)] for j in range(self._num_peptides)]
        # Diagonal vector will all be set to zeros, (self-self interaction is meaningless)
        for i, peptide1 in enumerate(self._peptides):
            self._energy_matrix[i, i] = interp1d(self._energy_coordinate, np.zeros_like(self._energy_coordinate), kind='linear')
            for j, peptide2 in enumerate(self._peptides[i+1:]):
                self._energy_matrix[i, i+j+1] = self.loadForceField(peptide1.peptide_type, peptide2.peptide_type).getInterpolate()
                self._energy_matrix[i+j+1, i] = self.loadForceField(peptide1.peptide_type, peptide2.peptide_type).getInterpolate()

    def calculateEnergy(self, peptide_id1, peptide_id2):
        return self._energy_matrix[peptide_id1, peptide_id2](
            getBond(
                self.peptides[peptide_id1].atoms[1].coordinate, self.peptides[peptide_id2].atoms[1].coordinate
            )
        ) * kilojoule_permol

    def calculateTotalEnergy(self):
        self._total_energy = 0
        for i in range(self._num_peptides):
            for j in range(i+1, self._num_peptides):
                self._total_energy += self.calculateEnergy(i, j)
        return self._total_energy

    def calculateForce(self, peptide_id1, peptide_id2, derivative_width=0.0001):
        bond_length = getBond(
                self.peptides[peptide_id1].atoms[1].coordinate, self.peptides[peptide_id2].atoms[1].coordinate
            )
        return (
            -(self._energy_matrix[peptide_id1, peptide_id2](bond_length+derivative_width)
            - self._energy_matrix[peptide_id1, peptide_id2](bond_length-derivative_width)) / (2*derivative_width)
            * kilojoule_permol / angstrom
        )

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
    def energy_matrix(self):
        return self._energy_matrix

    @property
    def energy_coordinate(self):
        return self._energy_coordinate
    
    @property
    def total_energy(self):
        self.calculateTotalEnergy()
        return self._total_energy