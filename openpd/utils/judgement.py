import numpy as np

def isArrayEqual(array1, array2):
    if len(array1) != len(array2):
        return False
    for index, element in enumerate(array1):
        if element != array2[index]:
            return False
    return True

def isArrayAlmostEqual(array1, array2, tolerance=1e-5):
    if len(array1) != len(array2):
        return False
    for index, element in enumerate(array1):
        if np.abs(element-array2[index]) > tolerance:
            return False
    return True