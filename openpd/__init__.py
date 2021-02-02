""" OpenPD is a opensource toolkit for peptides dynamics
simulation, predicting protein structure based on free-
energy tensor method.
"""

__author__ = "Zhenyu Wei"
__maintainer__ = "Zhenyu Wei" 
__email__ = "zhenyuwei99@gmail.com"
__copyright__ = "Copyright 2021-2021, Southeast University and Zhenyu Wei"
__license__ = "MIT"

triple_letter_abbreviation = [
    'ALA', 'ARG', 'ASN', 'ASP',
    'CYS', 'GLN', 'GLU', 'GLY',
    'HIS', 'ILE', 'LEU', 'LYS',
    'MET', 'PHE', 'PRO', 'SER',
    'THR', 'TRP', 'TYR', 'VAL'
]

single_letter_abbreviation = [
    'A', 'R', 'N', 'D',
    'C', 'Q', 'E', 'G',
    'H', 'I', 'L', 'K',
    'M', 'F', 'P', 'S',
    'T', 'W', 'Y', 'V'
]

from openpd.core import Topology, Atom, Peptide, Chain, System
from openpd.loader import PDBLoader, SequenceLoader

from openpd.force import PDFFNonbondedForce, PDFFTorsionForce
from openpd.forceEncoder import ForceEncoder
from openpd.ensemble import Ensemble

from openpd.integrator import BrownianIntegrator
from openpd.simulation import Simulation
from openpd.reporter import PDBReporter

__all__ = [
    'Topology', 'Atom', 'Peptide', 'Chain', 'System',
    'PDBLoader', 'SequenceLoader',
    'PDFFNonbondedForce', 'PDFFTorsionForce',
    'ForceEncoder',
    'Ensemble',
    'BrownianIntegrator',
    'Simulation',
    'PDBReporter'
]