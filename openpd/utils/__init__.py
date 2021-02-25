__author__ = "Zhenyu Wei"
__maintainer__ = "Zhenyu Wei" 
__email__ = "zhenyuwei99@gmail.com"
__copyright__ = "Copyright 2021-2021, Southeast University and Zhenyu Wei"
__license__ = "GPLv3"

from .judgement import isAlmostEqual, isArrayEqual, isArrayAlmostEqual, isArrayLambda
from .geometry import convertToNdArray, getBond, getUnitVec, getNormVec, getAngle, getTorsion
from .unique import uniqueList, mergeSameNeighbor
from .locate import findFirst, findFirstLambda, findAll, findAllLambda, binarySearch
from .math import gcd

__all__ = [
    'isAlmostEqual', 'isArrayEqual', 'isArrayAlmostEqual', 'isArrayLambda',
    'convertToNdArray', 'getBond', 'getUnitVec', 'getNormVec', 'getAngle', 'getTorsion',
    'uniqueList', 'mergeSameNeighbor',
    'findFirst', 'findFirstLambda', 'findAll', 'findAllLambda', 'binarySearch',
    'gcd'
]