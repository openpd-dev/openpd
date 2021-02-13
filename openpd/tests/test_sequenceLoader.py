import os, pytest

from .. import SequenceLoader, Peptide, getBond
from .. import CONST_CA_CA_DISTANCE

cur_dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))

class TestSequenceLoader:
    def setup(self):
        pass

    def teardown(self):
        self.loader = None

    def test_exceptions(self):
        with pytest.raises(ValueError):
            SequenceLoader(os.path.join(cur_dir, 'data/tripleNormal.jsn'), is_single_letter=True)

        # Having wrong single abbreviation in input file
        with pytest.raises(ValueError):
            SequenceLoader(os.path.join(cur_dir, 'data/singleException.json'), is_single_letter=True)
        
        # Using single letter abbrivaition file without specifying is_single_letter=True
        with pytest.raises(ValueError):
            SequenceLoader(os.path.join(cur_dir, 'data/singleNormal.json'), is_single_letter=False)

        # Having wrong triple abbreviation in input file
        with pytest.raises(ValueError):
            SequenceLoader(os.path.join(cur_dir, 'data/tripleException.json'), is_single_letter=True)

        # Using triple letter abbrivaition file with specifying is_single_letter=True
        with pytest.raises(ValueError):
            SequenceLoader(os.path.join(cur_dir, 'data/tripleNormal.json'), is_single_letter=True)

    def test_loadSequence(self):
        loader = SequenceLoader(os.path.join(cur_dir, 'data/singleNormal.json'), is_single_letter=True)
        assert loader.sequence_dict['Chain 1'] == ['ALA', 'ALA', 'ILE', 'ASN', 'ALA']
        assert loader.sequence_dict['Chain 2'] == ['ILE', 'ASN', 'ALA', 'ILE']

        loader = SequenceLoader(os.path.join(cur_dir, 'data/tripleNormal.json'), is_single_letter=False)
        assert loader.sequence_dict['Chain 1'] == [
            "ASN", "ALA", "ASN", "ALA", "ALA", 
            "ASN", "ALA", "ASN", "ALA", "ALA"
        ]
        assert loader.sequence_dict['Chain 2'] == [
            "ASN", "ALA", "ASN", "ALA", "ALA"]

    def test_CreateSystem(self):
        loader = SequenceLoader(os.path.join(cur_dir, 'data/singleNormal.json'), is_single_letter=True)
        system = loader.createSystem()
        assert system.topology.num_atoms == 18
        assert system.topology.num_bonds == 9 + 7
        assert system.topology.num_angles == 8 + 6
        assert system.topology.num_torsions == 4 + 3

        loader = SequenceLoader(os.path.join(cur_dir, 'data/tripleNormal.json'), is_single_letter=False)
        system = loader.createSystem()
        assert system.topology.num_atoms == 30
        assert system.topology.num_bonds == 19 + 9
        assert system.topology.num_angles == 18 + 8
        assert system.topology.num_torsions == 9 + 4

    def test_guessCoordinates(self):
        loader = SequenceLoader(os.path.join(cur_dir, 'data/singleNormal.json'), is_single_letter=True)
        system = loader.createSystem()

        assert getBond(system.atoms[0].coordinate, system.atoms[1].coordinate) == pytest.approx(Peptide('ALA')._ca_sc_dist)

        assert getBond(system.atoms[0].coordinate, system.atoms[2].coordinate) == pytest.approx(CONST_CA_CA_DISTANCE)

        loader = SequenceLoader(os.path.join(cur_dir, 'data/tripleNormal.json'), is_single_letter=False)
        system = loader.createSystem()

        assert getBond(system.atoms[0].coordinate, system.atoms[1].coordinate) == pytest.approx(Peptide('ALA')._ca_sc_dist)

        assert getBond(system.atoms[0].coordinate, system.atoms[2].coordinate) == pytest.approx(CONST_CA_CA_DISTANCE)

