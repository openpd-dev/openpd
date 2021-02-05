import sys, os
cur_dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
openpd_dir = os.path.join(cur_dir, '..')
sys.path.append(openpd_dir)
from openpd import SequenceLoader, SystemVisualizer

loader = SequenceLoader(os.path.join(cur_dir, 'sequence.json'), is_single_letter=False)
print(loader.sequence_dict)
system = loader.createSystem()

for peptide in system.peptides:
    print(peptide)

for chain in system.chains:
    print(chain)

print(system)
print(system.topology)


visualizer = SystemVisualizer(system, figsize=[15, 10])
#visualizer.setGrid(True)
print(visualizer)
visualizer.show()