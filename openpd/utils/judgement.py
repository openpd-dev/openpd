import numpy as np

def isAlmostEqual(num1, num2, tolerance=1e-5):
    if np.abs(num1 - num2) > (np.abs(num1) if num1!=0 else 1) * tolerance :
        return False 
    else:
        return True

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
        if np.abs(element-array2[index]) > (np.abs(element) if element!=0 else 1) * tolerance:
            return False
    return True