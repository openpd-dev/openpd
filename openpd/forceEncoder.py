import os
from . import System, Ensemble
from . import RIGISTERED_FORCE_FIELDS
from .unit import *
from .force import *
from .exceptions import UnsupportedForceFieldError

cur_dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
class ForceEncoder:
    def __init__(
        self, system:System, 
        force_field_name:str='pdff',
        cutoff_radius=12, derivative_width=0.0001
    ) -> None:
        self._system = system
        if not force_field_name.lower() in RIGISTERED_FORCE_FIELDS:
            raise UnsupportedForceFieldError('Force field %s is not supported by OpenPD, \n rigistered force field list: %s'
                %(force_field_name, RIGISTERED_FORCE_FIELDS))
        self._force_field_name = force_field_name
        self._force_field_folder = os.path.join(cur_dir, 'data', force_field_name)
        self._cutoff_radius = cutoff_radius
        self._derivative_width = derivative_width

    def __repr__(self) -> str:
        return ('<ForceEncoder object: encoding %s forcefield at 0x%x>' 
            %(self._force_field_name, id(self)))

    __str__ = __repr__

    def createEnsemble(self):
        self.ensemble = Ensemble(self._system)
        non_bonded_force = self._createNonBondedForce()
        bond_force = self._createBondForce()
        torsion_force = self._createTorsionForce()
        center_constraint_force = self._createCenterConstraintForce()

        self.ensemble.addForces(
            non_bonded_force, bond_force, torsion_force,
            center_constraint_force
        )

        return self.ensemble

    def _createNonBondedForce(self):
        force = PDFFNonBondedForce(
            cutoff_radius=self._cutoff_radius,
            derivative_width=self._derivative_width
        )
        return force

    def _createBondForce(self):
        force = PDFFBondForce()
        return force

    def _createTorsionForce(self):
        force = PDFFTorsionForce(
            derivative_width=self._derivative_width
        )
        return force

    def _createCenterConstraintForce(self):
        total_mass = 0 * amu
        for atom in self._system.atoms:
            total_mass += atom.mass
        elastic_constant = total_mass / amu * kilojoule_permol / angstrom**2 * 10
        force = CenterConstraintForce(
            elastic_constant = elastic_constant
        )
        return force

    @property
    def cutoff_radius(self):
        return self._cutoff_radius