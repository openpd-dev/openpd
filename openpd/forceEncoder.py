import numpy as np
import os
from . import System
from . import PDFFNonbondedForce, PDFFTorsionForce

cur_dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))

class ForceEncoder(object):
    def __init__(self, system:System) -> None:
        super().__init__()
        self.system = system
        self.forces = []

    def createEnsemble(self):
        for chain in self.system.chains:
            pass