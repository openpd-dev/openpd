import sys, os
cur_dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
openpd_dir = os.path.join(cur_dir, '..')
sys.path.append(openpd_dir)

from openpd import Peptide, Chain

chain = Chain(1)
peptide0 = Peptide('ASN')
peptide1 = Peptide('ALA')

chain.addPeptides([peptide0, peptide1, peptide0])

print(chain)

for atom in chain.atoms:
    print(atom)

for peptide in chain.peptides:
    print(peptide)