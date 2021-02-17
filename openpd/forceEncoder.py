"""
    ForceEncoder is used to create several necessary and only necessary force
"""

import numpy as np
import os
from . import System, Ensemble
from .force import *
from . import rigistered_force_filed_list, CONST_CA_CA_DISTANCE

cur_dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
class ForceEncoder(object):
    def __init__(self, system:System, force_field_name:str='pdff', is_rigid_bond=True, cutoff_radius=12) -> None:
        super().__init__()
        self._system = system
        if not force_field_name.lower() in rigistered_force_filed_list:
            raise ValueError('Force field %s is not supported by OpenPD, \n rigistered force field list: %s'
                %(force_field_name, rigistered_force_filed_list))
        self._force_field_name = force_field_name
        self._force_field_folder = os.path.join(cur_dir, 'data', force_field_name)
        self._cutoff_radius = cutoff_radius

    def __repr__(self) -> str:
        return ('<ForceEncoder object: encoding %s forcefield at 0x%x>' 
            %(self._force_field_name, id(self)))

    __str__ = __repr__

    def createEnsemble(self):
        self.ensemble = Ensemble()
        non_bonded_force = self._createNonBondedForce()
        bond_force = self._createBondForce()
        torsion_force =  PDFFTorsionForce()#self._createTorsionForce()

        self.ensemble.addForces(non_bonded_force, bond_force, torsion_force)

        return self.ensemble

    def _createNonBondedForce(self):
        force = PDFFNonbondedForce(self._cutoff_radius)
        force.addPeptides(*self.system.peptides)
        force.setEnergyMatrix()
        return force

    def _createBondForce(self):
        force = RigidBondForce()
        force.addBonds(*self.system.topology.bonds)
        return force

    def _createTorsionForce(self):
        force = PDFFTorsionForce()
        force.addTorsions(*self.system.topology.torsions)
        force.setEnergyVector()
        return force

    @property
    def system(self):
        return self._system

    @property
    def cutoff_radius(self):
        return self._cutoff_radius