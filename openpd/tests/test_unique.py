import numpy as np
from .. import isArrayEqual
from .. import uniqueList, mergeSameNeighbor

def test_uniqueList():
    goal = [1, 2, 3, 4, 4, 4, 1, 2]
    assert isArrayEqual(uniqueList(goal), [1, 2, 3, 4])
    assert not isArrayEqual(uniqueList(goal), [1, 2, 3, 4, 1])
    assert isArrayEqual(uniqueList(np.array(goal)), [1, 2, 3, 4])

    goal = [4, 2, 3, 4, 4, 4, 1, 2]
    assert isArrayEqual(uniqueList(goal), [4, 2, 3, 1])
    assert isArrayEqual(uniqueList(np.array(goal)), [4, 2, 3, 1])

    goal = ['C', 'A', 'B', 'A', 'A']
    assert isArrayEqual(uniqueList(goal), ['C', 'A', 'B'])
    assert not isArrayEqual(uniqueList(goal), ['C', 'A', 'B', 'A'])

def test_mergeSameNeighbor():
    goal = [1, 1, 1, 3, 4, 2, 5, 1, 1, 2, 2]
    assert isArrayEqual(mergeSameNeighbor(goal), [1, 3, 4, 2, 5, 1, 2])
    assert isArrayEqual(mergeSameNeighbor(np.array(goal)), [1, 3, 4, 2, 5, 1, 2])
    assert not isArrayEqual(mergeSameNeighbor(goal), [1, 3, 4, 2, 5])
    assert not isArrayEqual(mergeSameNeighbor(np.array(goal)), [1, 3, 4, 2, 5])

    goal = ['ASN', 'ASN', 'LEU', 'LEU', 'ASN']
    assert isArrayEqual(mergeSameNeighbor(goal), ['ASN', 'LEU', 'ASN'])
    assert not isArrayEqual(mergeSameNeighbor(goal), ['ASN', 'LEU'])

    
