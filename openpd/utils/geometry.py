
import numpy as np
from numpy.lib.scimath import arccos

def getBond(coord0:list, coord1:list):
    """bond Calculate the bond length from coordinate of two atoms

    :param coord0: coordinate of atom 0
    :type coord0: list
    :param coord1: coordinate of atom 1
    :type coord1: list
    :return: bond length
    :rtype: float
    """    
    coord0 = np.array(coord0)
    coord1 = np.array(coord1)

    v0 = coord0 - coord1
    
    return np.linalg.norm(v0)

def getAngle(coord0:list, coord1:list, coord2:list, is_angular=True):
    """angle Calculate the angle from the coordinate of three atoms

    :param coord0: coordinate of atom 0
    :type coord0: list
    :param coord1: coordinate of atom 1
    :type coord1: list
    :param coord2: coordinate of atom 2
    :type coord2: list
    :param is_angular: flag to wether return a angular result, defaults to True
    :type is_angular: bool, optional
    :return: angle
    :rtype: float
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

def getTorsion(coord0:list, coord1:list, coord2:list, coord3:list, is_angular=True):
    """torsion Calculate the torsion from the coordinate of four atoms
    
        Method details: 
            - https://zh.wikipedia.org/wiki/%E4%BA%8C%E9%9D%A2%E8%A7%92, 
            - https://stackoverflow.com/questions/46978451/how-to-know-if-a-dihedral-angle-is-or

    :param coord0: coordinate of atom 0
    :type coord0: list
    :param coord1: coordinate of atom 1
    :type coord1: list
    :param coord2: coordinate of atom 2
    :type coord2: list
    :param coord3: coordinate of atom 3
    :type coord3: list
    :param is_angular: flag to wether return a angular result, defaults to True
    :type is_angular: bool, optional
    :return: torsion
    :rtype: float
    """    
    coord0 = np.array(coord0)
    coord1 = np.array(coord1)
    coord2 = np.array(coord2)
    coord3 = np.array(coord3)

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