import sys, os
cur_dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
openpd_dir = os.path.join(cur_dir, '..')
sys.path.append(openpd_dir)

from openpd import Peptide

peptide = Peptide('ASN')
print(peptide.peptide_type)


for atom in peptide.atoms:
    print(atom.mass)