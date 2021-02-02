import sys
sys.path.append('/Users/zhenyuwei/Programs/openpd/')
from openpd import Peptide, Chain

chain = Chain(1)
peptide0 = Peptide('ASN')
peptide1 = Peptide('ALA')

chain.addPeptides([peptide0, peptide1, peptide0])

print(chain)

for atom in chain.getAtoms():
    print(atom)

for peptide in chain.getPeptides():
    print(peptide)