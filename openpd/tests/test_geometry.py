import pytest
import numpy as np
from .. import getBond, getUnitVec, getAngle, getTorsion, isArrayEqual, isArrayAlmostEqual
from ..unit import * 
from ..unit import Quantity

def test_getBond():
    coord0 = np.array([1, 1])
    coord1 = np.array([0, 0])
    assert getBond(coord0, coord1) == pytest.approx(np.sqrt(2))

    coord0 = np.array([1, 1]) * angstrom
    coord1 = np.array([0, 0]) * angstrom
    assert getBond(coord0, coord1) == pytest.approx(np.sqrt(2) * angstrom) 

def test_getUnitVec():
    vec = np.array([1, 1])
    assert isArrayAlmostEqual(getUnitVec(vec), np.array([np.sqrt(2)/2, np.sqrt(2)/2]))

    vec = np.array([1, 1]) * angstrom
    assert isArrayAlmostEqual(getUnitVec(vec), np.array([np.sqrt(2)/2, np.sqrt(2)/2]))

    vec = [0, 0]
    assert isArrayEqual(getUnitVec(vec), [0, 0])

    vec = [0, 0] * angstrom
    assert isArrayEqual(getUnitVec(vec), [0, 0])
    assert not isinstance(getUnitVec(vec)[0], Quantity)

    coord0 = np.array([1, 1]) * angstrom
    coord1 = np.array([0, 0]) * angstrom
    assert isArrayAlmostEqual(getUnitVec(coord0-coord1), np.array([np.sqrt(2)/2, np.sqrt(2)/2]))

def test_getAngle():
    coord0 = np.array([1, 1])
    coord1 = np.array([0, 0])
    coord2 = np.array([0, 1])
    assert getAngle(coord0, coord1, coord2) == pytest.approx(np.pi/4)
    assert getAngle(coord0, coord1, coord2, is_angular=False) == pytest.approx(45)

    coord0 = np.array([1, 1]) * angstrom
    coord1 = np.array([0, 0]) * angstrom
    coord2 = np.array([0, 1]) * angstrom
    assert getAngle(coord0, coord1, coord2) == pytest.approx(np.pi/4)
    assert getAngle(coord0, coord1, coord2, is_angular=False) == pytest.approx(45)

def test_getTorsion():
    coord0 = np.array([0, 1, 1])
    coord1 = np.array([0, 0, 0])
    coord2 = np.array([1, 0, 0])
    coord3 = np.array([1, 1, 0])
    assert getTorsion(coord0, coord1, coord2, coord3) == pytest.approx(np.pi/4)
    assert getTorsion(coord0, coord1, coord2, coord3, is_angular=False) == pytest.approx(45)

    coord0 = np.array([0, 1, 1]) * angstrom
    coord1 = np.array([0, 0, 0]) * angstrom
    coord2 = np.array([1, 0, 0]) * angstrom
    coord3 = np.array([1, 1, 0]) * angstrom
    assert getTorsion(coord0, coord1, coord2, coord3) == pytest.approx(np.pi/4)
    assert getTorsion(coord0, coord1, coord2, coord3, is_angular=False) == pytest.approx(45)

    coord0 = np.array([0, 1, 1])
    coord1 = np.array([0, 0, 0])
    coord2 = np.array([1, 0, 0])
    coord3 = np.array([1, 0, -1])
    assert getTorsion(coord0, coord1, coord2, coord3) == pytest.approx(np.pi*3/4)
    assert getTorsion(coord0, coord1, coord2, coord3, is_angular=False) == pytest.approx(135)

    coord0 = np.array([0, 1, 1]) * angstrom
    coord1 = np.array([0, 0, 0]) * angstrom
    coord2 = np.array([1, 0, 0]) * angstrom
    coord3 = np.array([1, 0, -1]) * angstrom
    assert getTorsion(coord0, coord1, coord2, coord3) == pytest.approx(np.pi*3/4)
    assert getTorsion(coord0, coord1, coord2, coord3, is_angular=False) == pytest.approx(135)

    coord0 = np.array([0, 1, 1])
    coord1 = np.array([0, 0, 0])
    coord2 = np.array([1, 0, 0])
    coord3 = np.array([1, 0, 1])
    assert getTorsion(coord0, coord1, coord2, coord3) == pytest.approx(np.pi*-1/4)
    assert getTorsion(coord0, coord1, coord2, coord3, is_angular=False) == pytest.approx(-45)

    coord0 = np.array([0, 1, 1]) * angstrom
    coord1 = np.array([0, 0, 0]) * angstrom
    coord2 = np.array([1, 0, 0]) * angstrom
    coord3 = np.array([1, 0, 1]) * angstrom
    assert getTorsion(coord0, coord1, coord2, coord3) == pytest.approx(np.pi*-1/4)
    assert getTorsion(coord0, coord1, coord2, coord3, is_angular=False) == pytest.approx(-45)

    coord0 = np.array([0, 1, 1])
    coord1 = np.array([0, 0, 0])
    coord2 = np.array([1, 0, 0])
    coord3 = np.array([1, -1, 0])
    assert getTorsion(coord0, coord1, coord2, coord3) == pytest.approx(np.pi*-3/4)
    assert getTorsion(coord0, coord1, coord2, coord3, is_angular=False) == pytest.approx(-135)

    coord0 = np.array([0, 1, 1]) * angstrom
    coord1 = np.array([0, 0, 0]) * angstrom
    coord2 = np.array([1, 0, 0]) * angstrom
    coord3 = np.array([1, -1, 0]) * angstrom
    assert getTorsion(coord0, coord1, coord2, coord3) == pytest.approx(np.pi*-3/4)
    assert getTorsion(coord0, coord1, coord2, coord3, is_angular=False) == pytest.approx(-135)