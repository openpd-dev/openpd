import numpy as np
from .. import isAlmostEqual, isArrayEqual, isArrayAlmostEqual

def test_isAlmostEqual():
    a = 2
    assert isAlmostEqual(a, a+0.1*a, tolerance=0.11)
    assert isAlmostEqual(a, a+1e-6*a)
    assert not isAlmostEqual(a, a+0.2*a, tolerance=0.1)
    assert not isAlmostEqual(a, a+1e-5*a)

    b = 0
    assert isAlmostEqual(b, 1e-6)
    assert isAlmostEqual(b, 1e-5, tolerance=1e-5)

    c = -2
    assert isAlmostEqual(c, c-0.9e-6*c)
    assert isAlmostEqual(c, c-0.9e-5*c, tolerance=1e-5)

def test_isArrayEqual():
    list1 = [1, 2, 3, 4.5, 6]
    list2 = [1, 2, 3, 4.5, 6]
    list3 = [1, 2, 4, 4.5, 6]
    list4 = [1, 2, 3, 4.5, 6, 7, 8]
    list5 = [1, 2, 3, 4.5]
    assert isArrayEqual(list1, list2)
    assert isArrayEqual(np.array(list1), list2)
    assert isArrayEqual(list1, np.array(list2))
    assert isArrayEqual(np.array(list1), np.array(list2))

    assert not isArrayEqual(list1, list3)
    assert not isArrayEqual(np.array(list1), list3)
    assert not isArrayEqual(list1, np.array(list3))
    assert not isArrayEqual(np.array(list1), np.array(list3))

    assert not isArrayEqual(list1, list4)
    assert not isArrayEqual(np.array(list1), list4)
    assert not isArrayEqual(list1, np.array(list4))
    assert not isArrayEqual(np.array(list1), np.array(list4))

    assert not isArrayEqual(list1, list5)
    assert not isArrayEqual(np.array(list1), list5)
    assert not isArrayEqual(list1, np.array(list5))
    assert not isArrayEqual(np.array(list1), np.array(list5))

    list1 = ['A', 'B', 'C']
    list2 = ['A', 'B', 'C']
    list3 = ['B', 'B', 'C']
    assert isArrayEqual(list1, list2)
    assert not isArrayEqual(list1, list3)

def test_isArrayAlmostEqual():
    list1 = [0, 2, 3, 4.5, 6]
    list2 = [1e-6, 2, 3, 4.5, 6]
    list3 = [1e-4, 2, 3, 4.5, 6]
    list4 = [0.1, 2, 3, 4.5, 6]
    list5 = [0.1, 2, 3]
    assert isArrayAlmostEqual(list1, list2)
    assert isArrayAlmostEqual(np.array(list1), list2)
    assert isArrayAlmostEqual(list1, np.array(list2))
    assert isArrayAlmostEqual(np.array(list1), np.array(list2))
    
    assert not isArrayAlmostEqual(list1, list3)
    assert not isArrayAlmostEqual(np.array(list1), list3)
    assert not isArrayAlmostEqual(list1, np.array(list3))
    assert not isArrayAlmostEqual(np.array(list1), np.array(list3))
    
    assert isArrayAlmostEqual(list1, list4, 0.1)
    assert isArrayAlmostEqual(np.array(list1), list4, 0.1)
    assert isArrayAlmostEqual(list1, np.array(list4), 0.1)
    assert isArrayAlmostEqual(np.array(list1), np.array(list4), 0.1)

    assert not isArrayAlmostEqual(list1, list5)
    assert not isArrayAlmostEqual(np.array(list1), list5)
    assert not isArrayAlmostEqual(list1, np.array(list5))
    assert not isArrayAlmostEqual(np.array(list1), np.array(list5))