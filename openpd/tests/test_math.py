import numpy as np
from .. import gcd

def test_gcd():
    a = [1, 2, 3]
    assert gcd(*a) == 1
    
    b = np.array([2, 4, 16])
    assert gcd(*b) == 2