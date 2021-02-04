import pytest
import numpy as np
from .. import getBond, getAngle, getTorsion

def test_getBond():
    coord0 = np.array([1, 1])
    coord1 = np.array([0, 0])
    assert getBond(coord0, coord1) == pytest.approx(np.sqrt(2))

def test_getAngle():
    coord0 = np.array([1, 1])
    coord1 = np.array([0, 0])
    coord2 = np.array([0, 1])
    assert getAngle(coord0, coord1, coord2) == pytest.approx(np.pi/4)
    assert getAngle(coord0, coord1, coord2, is_angular=False) == pytest.approx(45)

def test_getTorsion():
    coord0 = np.array([0, 1, 1])
    coord1 = np.array([0, 0, 0])
    coord2 = np.array([1, 0, 0])
    coord3 = np.array([1, 1, 0])
    assert getTorsion(coord0, coord1, coord2, coord3) == pytest.approx(np.pi/4)
    assert getTorsion(coord0, coord1, coord2, coord3, is_angular=False) == pytest.approx(45)

    coord0 = np.array([0, 1, 1])
    coord1 = np.array([0, 0, 0])
    coord2 = np.array([1, 0, 0])
    coord3 = np.array([1, 0, -1])
    assert getTorsion(coord0, coord1, coord2, coord3) == pytest.approx(np.pi*3/4)
    assert getTorsion(coord0, coord1, coord2, coord3, is_angular=False) == pytest.approx(135)

    coord0 = np.array([0, 1, 1])
    coord1 = np.array([0, 0, 0])
    coord2 = np.array([1, 0, 0])
    coord3 = np.array([1, 0, 1])
    assert getTorsion(coord0, coord1, coord2, coord3) == pytest.approx(np.pi*-1/4)
    assert getTorsion(coord0, coord1, coord2, coord3, is_angular=False) == pytest.approx(-45)

    coord0 = np.array([0, 1, 1])
    coord1 = np.array([0, 0, 0])
    coord2 = np.array([1, 0, 0])
    coord3 = np.array([1, -1, 0])
    assert getTorsion(coord0, coord1, coord2, coord3) == pytest.approx(np.pi*-3/4)
    assert getTorsion(coord0, coord1, coord2, coord3, is_angular=False) == pytest.approx(-135)