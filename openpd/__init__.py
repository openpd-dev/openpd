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

RIGISTERED_FORCE_FIELDS = [
    'pdff'
]

from openpd.utils import *

from openpd.element import Atom, Peptide, Chain, System, Topology
from openpd.loader import Loader, PDBLoader, SequenceLoader

from openpd.force import Force
from openpd.force import PDFFNonBondedForceField, PDFFNonBondedForce
from openpd.force import PDFFBondForceField, PDFFBondForce
from openpd.force import PDFFTorsionForceField, PDFFTorsionForce

from openpd.ensemble import Ensemble
from openpd.forceEncoder import ForceEncoder

from openpd.integrator import Integrator
from openpd.integrator import VerletIntegrator, LeapFrogIntegrator, VelocityVerletIntegrator
from openpd.integrator import BrownianIntegrator, MCMCIntegrator

from openpd.dumper import Dumper, LogDumper, SnapshotDumper, PDBDumper

from openpd.simulation import Simulation

from openpd.visualizer import SystemVisualizer, SnapshotVisualizer

__all__ = [
    'Atom', 'Peptide', 'Chain', 'System', 'Topology',
    'Loader', 'PDBLoader', 'SequenceLoader',
    'Force',
    'PDFFNonBondedForceField', 'PDFFNonBondedForce',
    'PDFFBondForceField', 'PDFFBondForce',
    'PDFFTorsionForceField', 'PDFFTorsionForce',
    'ForceEncoder',
    'Ensemble',
    'Integrator',
    'VerletIntegrator', 'LeapFrogIntegrator', 'VelocityVerletIntegrator',
    'BrownianIntegrator', 'MCMCIntegrator',
    'Dumper', 'LogDumper', 'SnapshotDumper', 'PDBDumper',
    'Simulation',
    'SystemVisualizer', 'SnapshotVisualizer'
]