import matplotlib.pyplot as plt
import numpy as np

class SnapshotVisualizer:
    def __init__(self, pds_file, figsize=[15, 10]) -> None:
        if not pds_file.endswith('.pds'):
            raise ValueError('The snapshot file should endwith .pds!')
        self._pds_file = pds_file
        self._figsize = figsize
        self._atom_info = []
        self._atom_coord = []
        self._bond_info = []
        self._frame_vec = []
        self._sim_time_vec = []
        self._num_frames = 0
        self.readPDSFile()
        
    def __repr__(self) -> str:
        return (
            '<SnapshotVisualizer object: visualize %s at 0x%x>'
            %(self._pds_file, id(self))
        )
        
    __str__ = __repr__
        
    def _skipBlankOrCommentLine(self, line):
        while line.startswith('#') or line.startswith('\n'):
            line = self._io.readline()
        return line
    
    def _readFrameLine(self, line):
        res = []
        while line.startswith('FRAME'):
            res.append(int(line.split()[1]))
            line = self._io.readline()
        return line, res
    
    def _readSimTimeLine(self, line):
        res = []
        while line.startswith('SIMTIME'):
            res.append(float(line.split()[1]))
            line = self._io.readline()
        return line, res
    
    @staticmethod
    def _parseAtomLine(line):
        data = line.split()
        res = []
        res.append(int(data[1])) # atom id
        res.append(data[2]) # atom type
        res.append(int(data[3])) # peptide id
        res.append(data[4]) # peptide type
        res.append(int(data[5])) # chain id
        res.append(np.array([
            float(data[6]), float(data[7]), float(data[8])
        ])) # coordinate as an ndarray
        return res
    
    def _readAtomLine(self, line):
        res = []
        coord = []
        while line.startswith('ATOM'):
            data = self._parseAtomLine(line)
            res.append(data)
            coord.append(data[-1])
            line = self._io.readline()
        return line, res, coord
    
    def _readBondLine(self, line):
        res = []
        while line.startswith('BOND'):
            res.append(
                np.array(
                    [float(i) for i in line.split()[2:]]
                )
            )
            line = self._io.readline()
        return line, res
    
    def _skipEndFrameLine(self, line):
        while line.startswith('ENDFRAME'):
            line = self._io.readline()
        return line
    
    def _readSingleFrame(self, line):
        line = self._skipBlankOrCommentLine(line)
        line, frame = self._readFrameLine(line)
        line, sim_time = self._readSimTimeLine(line)
        line, atom_info, atom_coord = self._readAtomLine(line)
        line, bond_info = self._readBondLine(line)
        line = self._skipEndFrameLine(line)
        self._frame_vec.extend(frame)
        self._sim_time_vec.extend(sim_time)
        self._atom_info.append(atom_info)
        self._atom_coord.append(atom_coord)
        self._bond_info.append(bond_info)
        if self._num_frames == 0:
            self._num_atoms = len(self._atom_info[0])
            self._num_bonds = len(self._bond_info[0])
        self._num_frames += 1
        return line
    
    def readPDSFile(self):
        self._io = open(self._pds_file, 'r')
        line = self._io.readline()
        while line:
            line = self._readSingleFrame(line)
        self._io.close()
        
    def on_close_event(self, event):
        self._break=True
        
    def show(
        self, pause_time=0.1, atom_size=150, bond_width=3  
    ):
        self._break = False
        fig = plt.figure(figsize=self._figsize)
        fig.canvas.mpl_connect('close_event', self.on_close_event)
        ax = fig.add_subplot(111, projection='3d')
        plt.ion()
        while not self._break:
            for frame in range(self._num_frames):
                if self._break:
                    break
                plt.cla()
                for atom in self._atom_info[frame]:
                    if atom[1] == 'CA':
                        ax.scatter3D(
                            atom[-1][0], atom[-1][1], atom[-1][2], 
                            '.', c='navy', s=atom_size, edgecolors='face'
                        )
                    elif atom[1] == 'SC':
                        ax.scatter3D(
                            atom[-1][0], atom[-1][1], atom[-1][2], 
                            '.', c='brown', s=atom_size, edgecolors='face'
                        )
                for bond in self._bond_info[frame]:
                    ax.plot3D(
                        [bond[0], bond[3]],
                        [bond[1], bond[4]],
                        [bond[2], bond[5]],
                        c='teal', lw=bond_width
                    )
                plt.pause(pause_time)
        
    @property
    def pds_file(self):
        return self._pds_file
    
    @property
    def num_frames(self):
        return self._num_frames
    
    @property
    def num_atoms(self):
        return self._num_atoms
    
    @property
    def num_bonds(self):
        return self._num_bonds