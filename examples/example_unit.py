import sys, os
cur_dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
openpd_dir = os.path.join(cur_dir, '..')
sys.path.append(openpd_dir)

import openpd.unit as unit
import numpy as np

print(300*unit.kelvin*unit.k_b/unit.kilojoule_permol)

print([300, 400, 500]*unit.kelvin*unit.k_b/unit.kilojoule_permol)

print(np.array([300, 400, 500])*unit.kelvin*unit.k_b/unit.kilojoule_permol)

print(1*unit.meter*unit.newton)
print(1*unit.joule)
print(1*unit.meter*unit.newton == 1*unit.joule)