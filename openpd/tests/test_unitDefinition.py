import pytest
from ..unit import *

def test_constants():
    # Avogadro Constant
    assert mol * n_a == 6.0221e23
    assert 6.0221e23 / n_a == 1 * mol

    # Boltzmann Constant
    assert 300 * kelvin * k_b / kilojoule_permol == pytest.approx(2.494321)
    assert 300 * kelvin * k_b / kilocalorie_permol == pytest.approx(0.596157)
    assert 300 * kelvin * k_b / ev == pytest.approx(0.02585199)
    assert 300 * kelvin * k_b / hartree == pytest.approx(9.500431e-04)

def test_length():
    assert meter / decimeter == pytest.approx(10)
    assert meter / centermeter == pytest.approx(100)
    assert meter / millimeter == pytest.approx(1000)
    assert meter / micrometer == pytest.approx(1e6)
    assert meter / nanometer == pytest.approx(1e9)
    assert meter / angstrom == pytest.approx(1e10)

def test_mass():
    assert kilogram / gram == pytest.approx(1e3)
    assert kilogram / amu == pytest.approx(1/1.66053904e-27)
    assert kilogram / dalton == pytest.approx(1/1.66053904e-27)

    assert gram / kilogram == pytest.approx(1e-3)
    assert amu / kilogram == pytest.approx(1.66053904e-27)
    assert dalton / kilogram == pytest.approx(1.66053904e-27)

def test_time():
    assert second / millisecond == pytest.approx(1e3)
    assert second / microsecond == pytest.approx(1e6)
    assert second / nanosecond == pytest.approx(1e9)
    assert second / picosecond == pytest.approx(1e12)
    assert second / femtosecond == pytest.approx(1e15)

def test_temperature():
    assert kelvin / kelvin == 1

def test_charge():
    assert coulomb / e == pytest.approx(1/1.602176634e-19)

def test_mol():
    assert kilomol / mol == pytest.approx(1e3)

def test_force():
    assert newton / newton == 1

def test_energy():
    assert joule / kilojoule == pytest.approx(1e-3)
    assert joule / joule_permol == pytest.approx(6.0221e23)
    assert joule / kilojoule_permol == pytest.approx(6.0221e20)

    assert joule / calorie == pytest.approx(1/4.184)
    assert joule / kilocalorie == pytest.approx(1/4.184e3)
    assert joule / calorie_premol == pytest.approx(6.0221e23/4.184)
    assert joule / kilocalorie_permol == pytest.approx(6.0221e23/4.184e3)
    
    assert joule / ev == pytest.approx(1/1.60217662e-19)
    assert joule / hartree == pytest.approx(1/4.3597447222071e-18)

def test_power():
    assert watt / kilowatt == pytest.approx(1e-3)

def test_mixture():
    assert newton * meter == joule
    assert joule / (n_a * mol) == joule_permol
    assert joule / second == watt
    assert kilojoule / second == kilowatt
    assert kilojoule == joule * 1000
    assert angstrom == meter * 1e-10
    assert not angstrom == meter * 1e-9
    assert millisecond == second / 1e3