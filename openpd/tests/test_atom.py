import pytest
import numpy as np

from .. import Atom, isArrayEqual
from ..unit import *
from ..unit import Quantity

class TestAtom:
    def setup(self):
        self.atom = Atom('Ca', 12)

    def teardown(self):
        self.atom = None
        
    def test_attributes(self):
        assert self.atom.atom_type == 'Ca'

        assert self.atom.atom_id == 0
        self.atom.atom_id = 1
        assert self.atom.atom_id == 1

        assert self.atom.mass == 12

        assert self.atom.peptide_type == None
        self.atom.peptide_type = 'ASN'
        assert self.atom.peptide_type == 'ASN'

        assert isArrayEqual(self.atom._coordinate, np.zeros([3]))
        self.atom.coordinate = [1, 1, 1] * angstrom
        assert isArrayEqual(self.atom._coordinate, np.ones([3]))
        assert self.atom.coordinate[0] == angstrom
        assert isinstance(self.atom.velocity[0], Quantity)

        assert isArrayEqual(self.atom.velocity, np.zeros([3]))
        self.atom.velocity = [1, 1, 1]  * angstrom / femtosecond
        assert isArrayEqual(self.atom.velocity, np.ones([3]))
        assert self.atom.velocity[0] == angstrom / femtosecond
        assert isinstance(self.atom.velocity[0], Quantity)

    def test_exceptions(self):
        with pytest.raises(AttributeError):
            self.atom.atom_type = 1
        
        with pytest.raises(AttributeError):
            self.atom.mass = 1

        with pytest.raises(ValueError):
            self.atom.coordinate = [2, 2]
        
        with pytest.raises(ValueError):
            self.atom.coordinate = np.array([2, 2])

        with pytest.raises(ValueError):
            self.atom.coordinate = [2, 2, 2] * angstrom / second

        with pytest.raises(ValueError):
            self.atom.coordinate = [2, 2]
        
        with pytest.raises(ValueError):
            self.atom.velocity = np.array([2, 2])

        with pytest.raises(ValueError):
            self.atom.velocity = [2, 2, 2] * angstrom 
