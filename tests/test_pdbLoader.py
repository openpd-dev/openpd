import sys, os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
cur_dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
openpd_dir = os.path.join(cur_dir, '..')
sys.path.append(openpd_dir)

from openpd import PDBLoader

loader = PDBLoader(os.path.join(cur_dir, 'sequence.pdb'))

system = loader.createSystem(is_extract_coordinate=True)
for peptide in system.peptides:
    print(peptide)

for atom in system.atoms:
    pass
    #print(atom.coordinate)

for chain in system.chains:
    print(chain)

print(system)
print(system.topology)

coord = system.coordinate
fig = plt.figure()
ax = Axes3D(fig)
color = []
for peptide in system.peptides:
    color.extend(['navy', 'brown'])
ax.scatter(coord[:, 0], coord[:, 1], coord[:, 2], c=color)
for bond in system.topology.bonds:
    ax.plot([bond[0].coordinate[0], bond[1].coordinate[0]],
            [bond[0].coordinate[1], bond[1].coordinate[1]],
            [bond[0].coordinate[2], bond[1].coordinate[2]], c='teal')
plt.show()