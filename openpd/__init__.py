""" OpenPD is a opensource toolkit for peptides dynamics
simulation, predicting protein structure based on free-
energy tensor method.
"""

__author__ = "Zhenyu Wei"
__maintainer__ = "Zhenyu Wei" 
__email__ = "zhenyuwei99@gmail.com"
__copyright__ = "Copyright 2021-2021, Southeast University and Zhenyu Wei"
__license__ = "GPLv3"

CONST_CA_CA_DISTANCE = 3.85

TRIPLE_LETTER_ABBREVIATION = [
    'ALA', 'ARG', 'ASN', 'ASP',
    'CYS', 'GLN', 'GLU', 'GLY',
    'HIS', 'ILE', 'LEU', 'LYS',
    'MET', 'PHE', 'PRO', 'SER',
    'THR', 'TRP', 'TYR', 'VAL'
]

SINGLE_LETTER_ABBREVIATION = [
    'A', 'R', 'N', 'D',
    'C', 'Q', 'E', 'G',
    'H', 'I', 'L', 'K',
    'M', 'F', 'P', 'S',
    'T', 'W', 'Y', 'V'
]

rigistered_force_filed_list = [
    'pdff'
]

from openpd.utils import *

from openpd.core import Topology, Atom, Peptide, Chain, System
from openpd.loader import Loader, PDBLoader, SequenceLoader

from openpd.force import Force, RigidBondForce
from openpd.force import PDFFNonBondedForceField, PDFFNonbondedForce
from openpd.force import PDFFTorsionForceField, PDFFTorsionForce

from openpd.ensemble import Ensemble
from openpd.forceEncoder import ForceEncoder
from openpd.integrator import BrownianIntegrator
from openpd.simulation import Simulation
from openpd.dumper import PDBDumper

from openpd.visualizer import SystemVisualizer

__all__ = [
    'Topology', 'Atom', 'Peptide', 'Chain', 'System',
    'PDBLoader', 'SequenceLoader',
    'Force', 'RigidBondForce', 
    'PDFFNonBondedForceField', 'PDFFNonbondedForce',
    'PDFFTorsionForceField', 'PDFFTorsionForce',
    'ForceEncoder',
    'Ensemble',
    'BrownianIntegrator',
    'Simulation',
    'PDBDumper',
    'SystemVisualizer'
]