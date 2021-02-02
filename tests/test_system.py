from os import system
import sys
sys.path.append('/Users/zhenyuwei/Programs/openpd/')
from openpd import Peptide, Chain, System

peptide0 = Peptide('ASN')
peptide1 = Peptide('ALA')

chain0 = Chain(0)
chain1 = Chain(2)

chain0.addPeptides([peptide1, peptide1, peptide0])
chain1.addPeptides([peptide0, peptide1, peptide0])

system = System()
system.addChains([chain0, chain1])

for atom in system.getAtoms():
    print(atom)

for peptide in system.getPeptides():
    print(peptide)

for chain in system.getChains():
    print(chain)

for bond in system.topology.bonds:
    print(bond)
print(system)