#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
file: pdffHydroFieldForce.py
created time : 2021/04/07
last edit time : 2021/04/07
author : Zhenyu Wei 
version : 1.0
contact : zhenyuwei99@gmail.com
copyright : (C)Copyright 2021-2021, Zhenyu Wei and Southeast University
'''

import os, json, codecs
import numpy as np
from .. import Force
from .. import getBond
from ..unit import *
from ..unit import Quantity
from ..exceptions import *

cur_dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
force_field_dir = os.path.join(cur_dir, '../data/pdff/hydrofield')

class PDFFNonBondedForceField:
    def __init__(self, atom_type: str) -> None:
        self._atom_type = atom_type

    def __repr__(self) -> str:
        return (
            '<PDFFNonBondedForceField object: %s atom at 0x%x>'
            %(self._atom_type, id(self))
        )

    __str__ = __repr__

    @staticmethod
    def _getEnergyExperssion(paramters: dict):
        expression = 'lambda r: '
        terms = []
        gaussian_term = lambda h, mu, sigma: '%.5f * np.exp(-((r-%.5f)/%.5f)**2)' %(h, mu, sigma)
        switching_term = lambda zeta, r_s: '1 / (1 + np.exp(-%.5f * (r - %.5f)))' %(zeta, r_s)
        for key, value in paramters.items():
            if key.lower().startswith('gaussian'):
                terms.append(gaussian_term(value['h'], value['mu'], value['sigma']))
            elif key.lower().startswith('switching'):
                terms.append(switching_term(value['zeta'], value['r_s']))
        for i, j in enumerate(terms):
            if i != len(terms)-1:
                expression += j + ' + '
            else:
                expression += j
        return eval(expression + ' - 1') # g(r) - 1

    @staticmethod
    def _getForceExperssion(paramters: dict):
        expression = 'lambda r: '
        terms = []
        gaussian_term = lambda h, mu, sigma: '2 * %.5f * (r - %.5f) / %.5f**2 * np.exp(- (r - %.5f)**2 / %.5f**2)' %(h, mu, sigma, mu, sigma)
        switching_term = lambda zeta, r_s: '- %.5f * np.exp(-%.5f*(r-%.5f)) / (1 + np.exp(-%.5f*(r-%.5f)))**2' %(zeta, zeta, r_s, zeta, r_s)
        for key, value in paramters.items():
            if key.lower().startswith('gaussian'):
                terms.append(gaussian_term(value['h'], value['mu'], value['sigma']))
            elif key.lower().startswith('switching'):
                terms.append(switching_term(value['zeta'], value['r_s']))
        for i, j in enumerate(terms):
            if i != len(terms)-1:
                expression += j + ' + '
            else:
                expression += j

        return eval(expression)

    def getEnergy(self):
        pass

    def getForce(self):
        pass

class PDFFHydroFieldForce(Force):
    def __init__(self, force_id, force_group) -> None:
        super().__init__(force_id, force_group)

    def bindEnsemble(self, ensemble):
        if self._is_bound == True:
            raise RebindError('Force has been bound to %s' %(self._ensemble))
        
        self._is_bound = True
        self._ensemble = ensemble
        self._num_peptides = self._ensemble.system.num_peptides
        self._peptides = self._ensemble.system.peptides
        self._num_atoms = self._ensemble.system.num_atoms
        self._atoms = self._ensemble.system.atoms

    def _setForceFieldVector(self):
        pass