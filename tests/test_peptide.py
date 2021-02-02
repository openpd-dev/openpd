import sys
sys.path.append('/Users/zhenyuwei/Programs/openpd/')
from openpd import Peptide

peptide = Peptide('ASN')
print(peptide)

print(peptide.ca_sc_dist)

for atom in peptide.atoms:
    print(atom.mass)