__author__ = "Zhenyu Wei"
__maintainer__ = "Zhenyu Wei" 
__email__ = "zhenyuwei99@gmail.com"
__copyright__ = "Copyright 2021-2021, Southeast University and Zhenyu Wei"
__license__ = "MIT"

CONST_CA_SC_DISTANCE = 3.85

from .pdbLoader import PDBLoader
from .sequenceLoader import SequenceLoader

__all__ = ['PDBLoader', 'SequenceLoader']