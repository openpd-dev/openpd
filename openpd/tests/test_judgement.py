import pytest
import numpy as np
from .. import isAlmostEqual, isArrayEqual, isArrayAlmostEqual, isArrayLambda, isStandardPeptide
from ..exceptions import PeptideTypeError

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

    list1 = np.ones([3, 3, 3])
    list2 = np.ones([3, 3, 3])
    assert isArrayEqual(list1, list2)
    list2[1, 1, 1] = 0
    assert not isArrayEqual(list1, list2)

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

    list1 = np.ones([3, 3, 3])
    list2 = np.ones([3, 3, 3])
    assert isArrayAlmostEqual(list1, list2)
    list2[1, 1, 1] = 1 + 1e-6
    assert isArrayAlmostEqual(list1, list2)
    assert not isArrayAlmostEqual(list1, list2, 1e-7)

def test_isArrayLambda():
    a = [1, 2, 3, 4, 5]
    assert isArrayLambda(lambda x:x>0, a)
    assert not isArrayLambda(lambda x:x<3, a)

    a = np.array([1, 2, 3, 4, 5])
    assert isArrayLambda(lambda x:x>0, a)
    assert not isArrayLambda(lambda x:x<3, a)

def test_isStandardPeptide():
    assert isStandardPeptide('ASN')
    assert isStandardPeptide('ASN', 'ASP')

    assert isStandardPeptide('A')
    assert isStandardPeptide('A', 'S')

    assert isStandardPeptide('ASN', 'A', 'ASP')
    assert isStandardPeptide('A', 'LEU', 'A')

    with pytest.raises(PeptideTypeError):
        isStandardPeptide('ASS')

    with pytest.raises(PeptideTypeError):
        isStandardPeptide('ASN', 'ASS')

    with pytest.raises(PeptideTypeError):
        isStandardPeptide('Z')

    with pytest.raises(PeptideTypeError):
        isStandardPeptide('A', 'Z')

    with pytest.raises(PeptideTypeError):
        isStandardPeptide('ASN', 'Z')

    with pytest.raises(PeptideTypeError):
        isStandardPeptide('A', 'ASZ')
    
    with pytest.raises(PeptideTypeError):
        isStandardPeptide('AS')

    with pytest.raises(PeptideTypeError):
        isStandardPeptide('ASN', 'AS')

    # lower case

    assert isStandardPeptide('asN')
    assert isStandardPeptide('asn', 'AsP')

    assert isStandardPeptide('a')
    assert isStandardPeptide('a', 's')

    assert isStandardPeptide('ASN', 'a', 'ASP')
    assert isStandardPeptide('a', 'LeU', 'a')

    with pytest.raises(PeptideTypeError):
        isStandardPeptide('ASs')

    with pytest.raises(PeptideTypeError):
        isStandardPeptide('ASn', 'AsS')

    with pytest.raises(PeptideTypeError):
        isStandardPeptide('z')

    with pytest.raises(PeptideTypeError):
        isStandardPeptide('a', 'z')

    with pytest.raises(PeptideTypeError):
        isStandardPeptide('ASN', 'z')

    with pytest.raises(PeptideTypeError):
        isStandardPeptide('A', 'AsZ')
    
    with pytest.raises(PeptideTypeError):
        isStandardPeptide('As')

    with pytest.raises(PeptideTypeError):
        isStandardPeptide('asN', 'aS')