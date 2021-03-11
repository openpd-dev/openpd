import pytest
import numpy as np
from .. import PDFFNonBondedForceField
from ..unit import *
from ..exceptions import PeptideTypeError

class TestPDFFNonBondedForceField:
    def setup(self):
        self.force_field = PDFFNonBondedForceField('ASN', 'LEU')

    def teardown(self):
        self.force_field = None

    def test_attributes(self):
        assert self.force_field.name == 'ASN-LEU'
        assert self.force_field.cutoff_radius == 12
        
    def test_exceptions(self):
        with pytest.raises(AttributeError):
            self.force_field.name = 1

        with pytest.raises(AttributeError):
            self.force_field.cutoff_radius = 1
            
        with pytest.raises(PeptideTypeError):
            PDFFNonBondedForceField('ASN', 'LE')

        # not include ASN-A, A can pass isStandardPeptide
        with pytest.raises(ValueError):
            PDFFNonBondedForceField('ASN', 'A')

        with pytest.raises(ValueError):
            PDFFNonBondedForceField('ASN', 'LEU', cutoff_radius=32)

        with pytest.raises(ValueError):
            PDFFNonBondedForceField('ASN', 'LEU', cutoff_radius=3.1*nanometer)
    
    def test_getEnergy(self):
        assert (
            self.force_field._origin_data['energy_data'][20] ==
            pytest.approx(self.force_field.getEnergy(self.force_field._origin_data['energy_coord'][20])/kilojoule_permol)
        )
        self.force_field.getEnergy(0)
        self.force_field.getEnergy(11.999999999999999999999)
        assert self.force_field.getEnergy(20) == 0 * kilojoule_permol
        assert self.force_field.getEnergy(2 * nanometer) == 0

    def test_getForce(self):
        assert (
            self.force_field._origin_data['force_data'][20] ==
            pytest.approx(self.force_field.getForce(self.force_field._origin_data['force_coord'][20])/kilojoule_permol_over_angstrom)
        )

        sim_interval = 0.001
        force =  (self.force_field.getEnergy(2-sim_interval/2) - self.force_field.getEnergy(2+sim_interval/2)) / sim_interval / angstrom
        assert self.force_field.getForce(2) / kilocalorie_permol_over_angstrom == pytest.approx(force / kilocalorie_permol_over_angstrom)
        
        self.force_field.getForce(11.999999999999999999999)
        self.force_field.getForce(0)

        assert self.force_field.getForce(14) == 0
        assert self.force_field.getForce(1.4 * nanometer) == 0 * kilojoule_permol_over_angstrom