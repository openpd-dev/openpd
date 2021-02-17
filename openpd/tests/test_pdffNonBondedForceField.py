import pytest
import numpy as np
from .. import PDFFNonBondedForceField
from .. import findFirstLambda, findAll, findAllLambda, isAlmostEqual, isArrayEqual

class TestPDFFNonBondedForceField:
    def setup(self):
        self.force_field = PDFFNonBondedForceField('ASN', 'LEU')

    def teardown(self):
        pass

    def test_attributes(self):
        assert self.force_field.name == 'ASN-LEU'
        assert isArrayEqual(self.force_field.target_coord, np.linspace(0, 30, 601))
        assert self.force_field.cutoff_radius == 12

    def test_exceptions(self):
        with pytest.raises(AttributeError):
            self.force_field.name = 1
        
        with pytest.raises(AttributeError):
            self.force_field.target_coord = 1

        with pytest.raises(AttributeError):
            self.force_field.cutoff_radius = 1

    def test_fixInf(self):
        assert findAll(float('inf'), self.force_field._origin_data) == []

    def test_fixConverge(self):
        for i in findAllLambda(lambda x: x>12, self.force_field._origin_coord):
            assert self.force_field._origin_data[i] == 0

    def test_guessCoord(self):
        assert findAll(float('inf'), self.force_field.target_data) == []
        for i in findAllLambda(lambda x: x>12, self.force_field.target_coord):
            assert self.force_field.target_data[i] == 0
    
    def test_getInterpolate(self):
        f = self.force_field.getInterpolate()
        assert self.force_field.target_data[findFirstLambda(lambda x: x<2.01 and x >1.99, self.force_field.target_coord)] == pytest.approx(f(2))

        assert isAlmostEqual(
            self.force_field._origin_data[findFirstLambda(lambda x: x<2.05 and x >1.95, self.force_field._origin_coord)], 
            f(self.force_field._origin_coord[findFirstLambda(lambda x: x<2.05 and x >1.95, self.force_field._origin_coord)]), 1e-3
        )