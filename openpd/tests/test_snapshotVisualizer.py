import pytest, os
from .. import SnapshotVisualizer

cur_dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))

class TestSnapshotVisualizer:
    def setup(self):
        self.visualizer = SnapshotVisualizer(
            os.path.join(cur_dir, 'data/test_snapshotVisualizer.pds')
        )
    
    def teardown(self):
        self.visualizer = None
    
    def test_attributes(self):
        assert self.visualizer._pds_file == os.path.join(cur_dir, 'data/test_snapshotVisualizer.pds')
    
    def test_exceptions(self):
        with pytest.raises(AttributeError):
            self.visualizer.num_frames = 1
            
        with pytest.raises(AttributeError):
            self.visualizer.num_atoms = 1
        
        with pytest.raises(AttributeError):
            self.visualizer.num_bonds = 1
            
        with pytest.raises(ValueError):
            SnapshotVisualizer('a.ps')
    
    def test_readPDSFile(self):
        assert self.visualizer.num_frames == 11
        assert self.visualizer.num_atoms == 6
        assert self.visualizer.num_bonds == 5
        
        assert len(self.visualizer._atom_info) == 11
        assert len(self.visualizer._atom_info[-1]) == 6
        
        assert len(self.visualizer._bond_info) == 11
        assert len(self.visualizer._bond_info[-1]) == 5
        
        assert self.visualizer._sim_time_vec[-1] == 0.0002
        assert self.visualizer._frame_vec[-1] == 10
        
        