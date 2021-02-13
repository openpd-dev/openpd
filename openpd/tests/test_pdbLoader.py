from openpd.core.peptide import Peptide
import os, pytest
import numpy as np

from .. import PDBLoader, getBond
from .. import CONST_CA_CA_DISTANCE

cur_dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))

class TestPDBLoader:
    def setup(self):
        self.loader = PDBLoader(os.path.join(cur_dir, 'data/normal.pdb'))

    def teardown(self):
        self.loader = None

    def test_exceptions(self):
        with pytest.raises(ValueError):
            PDBLoader(os.path.join(cur_dir, 'data/exception.pd'))

        with pytest.raises(ValueError):
            PDBLoader(os.path.join(cur_dir, 'data/exception.pdb'))

    def test_loadSequence(self):
        assert self.loader.sequence_dict['A'] == [
            'ASN', 'LEU', 'TYR', 'ILE', 'GLN',
            'TRP', 'LEU', 'LYS', 'ASP', 'GLY'
        ]

        self.loader = PDBLoader(os.path.join(cur_dir, 'data/multiChain.pdb'))
        assert self.loader.sequence_dict['B'] == [
            'TRP', 'LEU', 'LYS'
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

        # Avoiding coordinate assigning issue when the peptide of one chain is discontinuous
        self.loader = PDBLoader(os.path.join(cur_dir, 'data/multiChain.pdb'))
        system = self.loader.createSystem(is_extract_coordinate=True)
        assert np.array_equal(system.chains[1].atoms[0].coordinate, np.array([-0.716, -0.631, -0.993]))
        assert np.array_equal(system.chains[1].atoms[2].coordinate, np.array([-1.641, -2.932, 1.963]))

    def test_guessCoordinates(self):
        system = self.loader.createSystem(is_extract_coordinate=False)

        assert getBond(system.atoms[0].coordinate, system.atoms[1].coordinate) == pytest.approx(Peptide('ASN')._ca_sc_dist)

        assert getBond(system.atoms[0].coordinate, system.atoms[2].coordinate) == pytest.approx(CONST_CA_CA_DISTANCE)
