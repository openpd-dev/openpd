#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
file: exceptions.py
created time : 2021/03/11
last edit time : 2021/04/14
author : Zhenyu Wei 
version : 1.0
contact : zhenyuwei99@gmail.com
copyright : (C)Copyright 2021-2021, Zhenyu Wei and Southeast University
'''

class NonboundError(Exception):
    """
    NonboundError related to the binding action 
    Used in:
    - openpd.force
    - openpd.integrator 
    - openpd.dumper
    - openpd.element.atom
    - openpd.element.molecule
    """    
    pass

class RebindError(Exception):
    """
    NonboundError related to the rebinding error contained in openpd.force, openpd.integrator, and openpd.dumper package
    """ 
    pass

class ModifiedBoundMoleculeError(Exception):
    """
    ModifiedBoundMoleculeError raises when edited the attribute of a bound instance
    Used in:
    - openpd.element.molecule
    """

class PeptideTypeError(Exception):
    """
    PeptideTypeError related to the peptide type error
    Used in
    - openpd.element.peptide 
    - openpd.loader
    - openpd.force package
    """ 
    pass

class UnsupportedForceFieldError(Exception):
    """
    UnsupportedForceFieldError related to the unsupported force field error contained in openpd.forceEncoder module
    """ 
    pass

class NotincludedInteractionError(Exception):
    """
    NotincludedInteractionError related to the interaction is not included error contained in openpd.force package
    """ 
    pass

class DismatchedDimensionError(Exception):
    """
    DismatchedDimensionError related to the dismatched dimension error contained in openpd.unit package and openpd.integrator.integrator module
    """ 
    pass

class DividingZeroError(Exception):
    """
    DividingZeroError related to the dividing zero error contained in openpd.unit.quantity module
    """
    pass