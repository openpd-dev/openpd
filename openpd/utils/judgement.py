import numpy as np

def isArrayEqual(array1, array2):
    for index, element in enumerate(array1):
        if element != array2[index]:
            return False
    return True