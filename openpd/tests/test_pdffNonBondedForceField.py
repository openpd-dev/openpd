import pytest
import numpy as np
from .. import PDFFNonBondedForceField
from .. import findAll, findAllLambda, isArrayEqual
from ..unit import *

class TestPDFFNonBondedForceField:
    def setup(self):
        self.force_field = PDFFNonBondedForceField('ASN', 'LEU')

    def teardown(self):
        self.force_field = None

    def test_attributes(self):
        assert self.force_field.name == 'ASN-LEU'
        assert self.force_field.cutoff_radius == 12
        assert isArrayEqual(self.force_field._target_coord, np.arange(0, self.force_field._cutoff_radius+0.001, 0.001))

    def test_exceptions(self):
        with pytest.raises(AttributeError):
            self.force_field.name = 1

        with pytest.raises(AttributeError):
            self.force_field.cutoff_radius = 1
            
        with pytest.raises(ValueError):
            PDFFNonBondedForceField('ASN', 'LE')

    def test_fixInf(self):
        assert findAll(float('inf'), self.force_field._origin_data) == []

    def test_fixConverge(self):
        for i in findAllLambda(lambda x: x>12, self.force_field._origin_coord):
            assert self.force_field._origin_data[i] == 0

    def test_guessCoord(self):
        assert findAll(float('inf'), self.force_field._target_data) == []
        for i in findAllLambda(lambda x: x>12, self.force_field._target_coord):
            assert self.force_field._target_data[i] == 0
    
    def test_getEnergy(self):
        assert self.force_field._target_data[2] == pytest.approx(self.force_field.getEnergy(self.force_field._target_coord[2])/kilojoule_permol)

        assert self.force_field._origin_data[2] == pytest.approx(self.force_field.getEnergy(self.force_field._origin_coord[2])/kilojoule_permol)

    def test_getForce(self):
        sim_interval = self.force_field.derivative_width

        force =  (self.force_field.getEnergy(2-sim_interval/2) - self.force_field.getEnergy(2+sim_interval/2)) / sim_interval / angstrom
        assert self.force_field.getForce(2) / kilocalorie_permol_over_angstrom == pytest.approx(force / kilocalorie_permol_over_angstrom)
        
        self.force_field.getForce(11.9999999999)
        self.force_field.getForce(0)