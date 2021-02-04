from openpd.core.peptide import Peptide
import os, pytest
import numpy as np

from .. import PDBLoader, bond
from ..loader import CONST_CA_SC_DISTANCE

cur_dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))

class TestPDBLoader:
    def setup(self):
        self.loader = PDBLoader(os.path.join(cur_dir, 'data/normal.pdb'))

    def teardown(self):
        self.loader = None

    def test_exceptions(self):
        with pytest.raises(ValueError):
            PDBLoader(os.path.join(cur_dir, 'data/exception.pdb'))

    def test_loadSequence(self):
        assert self.loader.sequence_dict['A'] == [
                'ASN', 'LEU', 'TYR', 'ILE', 'GLN',
                'TRP', 'LEU', 'LYS', 'ASP', 'GLY'
            ]

    def test_createSystem(self):
        system = self.loader.createSystem()

        assert system.num_atoms == 20
        assert system.num_peptides == 10
        assert system.num_chains == 1

        assert system.topology.num_atoms == 20
        assert system.topology.num_bonds == 19
        assert system.topology.num_angles == 18
        assert system.topology.num_torsions == 9

    def test_extractCoordinates(self):
        system = self.loader.createSystem(is_extract_coordinate=True)
        assert np.array_equal(system.atoms[0].coordinate, np.array([-8.608, 3.135, -1.618]))

        assert np.array_equal(system.atoms[2].coordinate, np.array([-4.923, 4.002, -2.452]))

    def test_guessCoordinates(self):
        system = self.loader.createSystem(is_extract_coordinate=False)

        assert bond(system.atoms[0].coordinate, system.atoms[1].coordinate) == pytest.approx(Peptide('ASN')._ca_sc_dist)

        assert bond(system.atoms[0].coordinate, system.atoms[2].coordinate) == pytest.approx(CONST_CA_SC_DISTANCE)
