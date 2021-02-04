import pytest
import numpy as np

from .. import Atom, isArrayEqual

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
        self.atom.coordinate = [1, 1, 1]
        assert isArrayEqual(self.atom._coordinate, np.ones([3]))

        assert isArrayEqual(self.atom.velocity, np.zeros([3]))
        self.atom.velocity = [1, 1, 1]
        assert isArrayEqual(self.atom.velocity, np.ones([3]))

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
            self.atom.coordinate = [2, 2]
        
        with pytest.raises(ValueError):
            self.atom.coordinate = np.array([2, 2])

