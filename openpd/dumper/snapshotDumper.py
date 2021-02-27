from . import Dumper
from ..unit import *

class SnapshotDumper(Dumper):
    def __init__(self, output_file, dump_interval) -> None:
        if not output_file.endswith('.pds'):
            raise ValueError('The snapshot file should endwith .pds!')
        super().__init__(output_file, dump_interval)
        self.cur_frame = 0
        
    def _setTitle(self):
        if self._is_bound:   
            self.title = '# OpenPD snapshot file created at %s' %self._simulation._start_time
        else:
            self.title = ''
        
    def bindSimulation(self, simulation):
        super().bindSimulation(simulation)
        self._setTitle()
        io = open(self._output_file, 'a')
        print(self.title, file=io)
        io.close()
        
    def dump(self):
        io = open(self._output_file, 'a')
        self._test_bound()
        self._dumpFrame(io)
        self._dumpSimulationTime(io)
        self._dumpAtom(io)
        self._dumpBond(io)
        self._dumpEndFrame(io)
        self.cur_frame += 1
        io.close()
    
    def _dumpFrame(self, io):
        info = 'FRAME %d' %self.cur_frame
        print(info, file=io)
        
    def _dumpSimulationTime(self, io):
        info = 'SIMTIME %.6f NS' %(
            self._simulation._cur_step * self._simulation._integrator.sim_interval / nanosecond
        )
        print(info, file=io)
        
    def _dumpAtom(self, io):
        info = ''
        for chain in self._simulation._ensemble._system.chains:
            for peptide in chain.peptides:
                for atom in peptide.atoms:
                    coord = atom.coordinate / angstrom
                    info += (
                        'ATOM {:<6}{:<5}{:<6}{:<6}{:<6}{:<13}{:<13}{:<13}\n'
                    ).format(
                        atom.atom_id, atom.atom_type, peptide.peptide_id, atom.peptide_type, chain.chain_id,
                        '%.6f' %coord[0], '%.6f' %coord[1], '%.6f' %coord[2]
                    )
        print(info[:-1], file=io) # Get rid of the final \n
        
    def _dumpBond(self, io):
        info = ''
        for i, bond in enumerate(self._simulation._ensemble._system.topology.bonds):
            coord0 = bond[0].coordinate / angstrom
            coord1 = bond[1].coordinate / angstrom
            info += (
                'BOND {:<6}{:<13}{:<13}{:<13}{:<13}{:<13}{:<13}\n'
            ).format(
                i, '%.6f' %coord0[0], '%.6f' %coord0[1], '%.6f' %coord0[2],
                '%.6f' %coord1[0], '%.6f' %coord1[1], '%.6f' %coord1[2]
            )
        print(info[:-1], file=io) # Get rid of the final \n
        
    def _dumpEndFrame(self, io):
        info = 'ENDFRAME'
        print(info, file=io)