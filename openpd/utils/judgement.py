import numpy as np
from .. import TRIPLE_LETTER_ABBREVIATION, SINGLE_LETTER_ABBREVIATION
from ..exceptions import PeptideTypeError

def isAlmostEqual(num1, num2, tolerance=1e-5):
    if np.abs(num1 - num2) > (np.abs(num1) if num1!=0 else 1) * tolerance :
        return False 
    else:
        return True

def isArrayEqual(array1, array2):
    if isinstance(array1, np.ndarray):
        array1 = array1.flatten()
    if isinstance(array2, np.ndarray):
        array2 = array2.flatten()
    if len(array1) != len(array2):
        return False
    for index, element in enumerate(array1):
        if element != array2[index]:
            return False
    return True

def isArrayAlmostEqual(array1, array2, tolerance=1e-5):
    if isinstance(array1, np.ndarray):
        array1 = array1.flatten()
    if isinstance(array2, np.ndarray):
        array2 = array2.flatten()
    if len(array1) != len(array2):
        return False
    for index, element in enumerate(array1):
        if np.abs(element-array2[index]) > (np.abs(element) if element!=0 else 1) * tolerance:
            return False
    return True

def isArrayLambda(judgement, array):
    if len(array) != len(array):
        return False
    for index, element in enumerate(array):
        if not judgement(element):
            return False
    return True

def isStandardPeptide(*peptides):
    for peptide in peptides:
        peptide = peptide.upper()
        if len(peptide) == 3:
            if not peptide in TRIPLE_LETTER_ABBREVIATION:
                raise PeptideTypeError(
                    'Peptide type %s is not in the standard peptide list:\n %s' 
                    %(peptide, TRIPLE_LETTER_ABBREVIATION)
                )
        elif len(peptide) == 1:
            if not peptide in SINGLE_LETTER_ABBREVIATION:
                raise PeptideTypeError(
                    'Peptide type %s is not in the standard peptide list:\n %s' 
                    %(peptide, SINGLE_LETTER_ABBREVIATION)
                )
        else:
            raise PeptideTypeError(
                'Peptide type should be 1 or 3 letters, instead of %d letters'
                %(len(peptide))
            )
    return True