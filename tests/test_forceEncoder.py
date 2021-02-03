import sys, os
cur_dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
openpd_dir = os.path.join(cur_dir, '..')
sys.path.append(openpd_dir)

from openpd import PDBLoader, ForceEncoder

loader = PDBLoader(os.path.join(cur_dir, 'sequence.pdb'))

system = loader.createSystem(is_extract_coordinate=True)

force_encoder = ForceEncoder(system)

print(force_encoder)