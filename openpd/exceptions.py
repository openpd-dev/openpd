class NonboundError(Exception):
    """
    NonboundError related to the binding action contained in openpd.force, openpd.integrator, and openpd.dumper package
    """    
    pass

class RebindError(Exception):
    """
    NonboundError related to the rebinding error contained in openpd.force, openpd.integrator, and openpd.dumper package
    """ 
    pass

class PeptideTypeError(Exception):
    """
    PeptideTypeError related to the peptide type error contained in openpd.element.peptide module, openpd.loader, and openpd.force package
    """ 
    pass

class UnsupportedForceFieldError(Exception):
    """
    UnsupportedForceFieldError related to the unsupported force field error contained in openpd.forceEncoder module
    """ 
    pass

class NotincludedInteractionError(Exception):
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