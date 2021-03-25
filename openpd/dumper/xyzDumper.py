#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
file: xyzDumper.py
created time : 2021/03/17
last edit time : 2021/03/17
author : Zhenyu Wei 
version : 1.0
contact : zhenyuwei99@gmail.com
copyright : (C)Copyright 2021-2021, Zhenyu Wei and Southeast University
'''

from . import Dumper
from ..unit import *

class XYZDumper(Dumper):
    def __init__(self, output_file, dump_interval: int, is_overwrite=True) -> None:
        if not output_file.endswith('.xyz'):
            raise ValueError('The XYZ file should endwith .xyz!')
        super().__init__(output_file, dump_interval, is_overwrite=is_overwrite)
        self.cur_frame = 0
    
    def __repr__(self):
        if self._is_bound:
            return (
                '<XYZDumper object: dump every %d step(s), binding with simulation at 0x%x>'
                %(self._dump_interval, id(self._simulation))
            )
        else:
            return (
                '<XYZDumper object: unbounded!>'
            )
            
    __str__ = __repr__
        
    def _setTitle(self):
        if self._is_bound:   
            self.title = (
                '%d\n.xyz file created by OpenPD at %s' 
                %(self._simulation._ensemble._system.num_atoms, self._simulation._start_time)
            )
            
        else:
            self.title = ''

    def bindSimulation(self, simulation):
        super().bindSimulation(simulation)
        self._setTitle()
        # io = open(self._output_file, 'a')
        # print(self.title, file=io)
        # io.close()

    def dump(self):
        io = open(self._output_file, 'a')
        self._test_bound()
        self._dumpNumAtom(io)
        self._dumpFrame(io)
        self._dumpXYZ(io)
        self.cur_frame += 1
        io.close()

    def _dumpNumAtom(self, io):
        info = '%d' %self._simulation._ensemble._system.num_atoms
        print(info, file=io)

    def _dumpFrame(self, io):
        info = 'Frame %d' %self.cur_frame
        print(info, file=io)

    def _dumpXYZ(self, io):
        info = ''
        for atom in self._simulation._ensemble._system.atoms:
            coord = atom.coordinate / angstrom
            info += (
                '{:<5}{:<13}{:<13}{:<13}\n'
            ).format(
                atom.atom_type, '%.6f' %coord[0], '%.6f' %coord[1], '%.6f' %coord[2]
            )
        print(info[:-1], file=io) # Get rid of the final \n