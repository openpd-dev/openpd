
import numpy as np
from numpy.lib.scimath import arccos
from . import isArrayLambda

def getBond(coord0, coord1):
    """
    getBond calculates the bond length from coordinate of two atoms

    Parameters
    ----------
    coord0 : list or np.ndarray
        coordinate of atom 0
    coord1 : list or np.ndarray
        coordinate of atom 1

    Returns
    -------
    float or Quantity
        bond length
    """    
    coord0 = np.array(coord0)
    coord1 = np.array(coord1)

    v0 = coord0 - coord1
    
    return np.linalg.norm(v0)

def getNormVec(vec):
    vec = np.array(vec)
    if isArrayLambda(lambda x:x==0, vec):
        return np.float64(vec / (vec + 1))
    else:
        return np.float64(vec / np.linalg.norm(vec))

def getAngle(coord0, coord1, coord2, is_angular=True):
    """
    getAngle calculates the angle from the coordinate of three atoms

    Parameters
    ----------
    coord0 : list or np.ndarray
        coordinate of atom 0
    coord1 : list or np.ndarray
        coordinate of atom 1
    coord2 : list or np.ndarray
        coordinate of atom 2
    is_angular : bool, optional
        flag to wether return a angular result, by default True

    Returns
    -------
    float
        angle
    """    
    coord0 = np.array(coord0)
    coord1 = np.array(coord1)
    coord2 = np.array(coord2)

    v0 = coord0 - coord1
    v1 = coord2 - coord1

    cos_phi = np.dot(v0, v1) / (np.linalg.norm(v0)*np.linalg.norm(v1))

    if is_angular:
        return arccos(cos_phi)
    else:
        return arccos(cos_phi) / np.pi * 180

def getTorsion(coord0, coord1, coord2, coord3, is_angular=True):
    """
    getTorsion calculates the torsion from the coordinate of four atoms

    Method details: 
        - https://zh.wikipedia.org/wiki/%E4%BA%8C%E9%9D%A2%E8%A7%92, 
        - https://stackoverflow.com/questions/46978451/how-to-know-if-a-dihedral-angle-is-or

    Parameters
    ----------
    coord0 : list or np.ndarray
        coordinate of atom 0
    coord1 : list or np.ndarray
        coordinate of atom 1
    coord2 : list or np.ndarray
        coordinate of atom 2
    coord3 : list or np.ndarray
        coordinate of atom 3
    is_angular : bool, optional
        flag to wether return a angular result, by default True

    Returns
    -------
    float
        torsion angle
    """    
    coord0 = getNormVec(coord0)
    coord1 = getNormVec(coord1)
    coord2 = getNormVec(coord2)
    coord3 = getNormVec(coord3)

    v0 = coord0 - coord1
    v1 = coord2 - coord1
    v2 = coord3 - coord2
    
    # Calculate the vertical vector of each plane
    # Note the order of cross product
    na = np.cross(v1, v0)
    nb = np.cross(v1, v2)

    # Note that we delete the absolute value  
    cos_phi = np.dot(na, nb) / (np.linalg.norm(na)*np.linalg.norm(nb))

    # Sign of angle
    omega = np.dot(v0, np.cross(v1, v2))
    sign = omega / np.abs(omega)

    if is_angular:
        return sign * arccos(cos_phi)
    else:
        return sign * arccos(cos_phi) / np.pi * 180