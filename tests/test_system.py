import sys, os
cur_dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
openpd_dir = os.path.join(cur_dir, '..')
sys.path.append(openpd_dir)
from openpd import Peptide, Chain, System

peptide0 = Peptide('ASN')
peptide1 = Peptide('ALA')

chain0 = Chain(0)
chain1 = Chain(2)

chain0.addPeptides([peptide1, peptide1, peptide0])
chain1.addPeptides([peptide0, peptide1, peptide0])

system = System()
system.addChains([chain0, chain1])

for atom in system.atoms:
    print(atom)

for peptide in system.peptides:
    print(peptide)

for chain in system.chains:
    print(chain)

for bond in system.topology.bonds:
    print(bond)
print(system)