import pytest, os
import numpy as np
from .. import PDFFTorsionForce, SequenceLoader, Ensemble
from .. import isAlmostEqual, isArrayEqual, getTorsion, convertToNdArray
from ..unit import *
from ..exceptions import NonboundError, RebindError

cur_dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
force_field_dir = os.path.join(cur_dir, '../data/pdff/torsion')

class TestPDFFTorsionForce:
    def setup(self):
        self.force = PDFFTorsionForce()

    def teardown(self):
        self.force = None

    def test_attributes(self):
        assert self.force._derivative_width == 0.0001
        assert self.force.num_torsions == 0
        assert self.force._potential_energy == 0
        assert self.force.force_field_vector == None

    def test_exceptions(self):
        with pytest.raises(AttributeError):
            self.force.num_torsions = 1

        with pytest.raises(AttributeError):
            self.force.potential_energy = 1

        with pytest.raises(AttributeError):
            self.force.force_field_vector = 1
            
        with pytest.raises(NonboundError):
            self.force._testBound()
            
        with pytest.raises(NonboundError):
            self.force = PDFFTorsionForce()
            self.force.calculateAtomForce(1)

        with pytest.raises(RebindError):
            self.force = PDFFTorsionForce()
            system = SequenceLoader(os.path.join(cur_dir, 'data/testForceEncoder.json')).createSystem()
            ensemble = Ensemble(system)
            self.force.bindEnsemble(ensemble)
            self.force.bindEnsemble(ensemble)
            
        with pytest.raises(AttributeError):
            self.force = PDFFTorsionForce()
            system = SequenceLoader(os.path.join(cur_dir, 'data/testPDFFTorsionForceException.json')).createSystem()
            self.force.bindEnsemble(Ensemble(system))

    def test_bindEnsemble(self):
        system = SequenceLoader(os.path.join(cur_dir, 'data/testForceEncoder.json')).createSystem()
        ensemble = Ensemble(system)
        self.force.bindEnsemble(ensemble)
        
        assert self.force._is_bound == True
        assert self.force._num_torsions == 2
        assert self.force._num_atoms == 6
        assert isArrayEqual(
            self.force._torison_types,
            [
                ['ASN', 'LEU'],
                ['LEU', 'TYR']
            ]
        )

    def test_setForceFieldVector(self):
        system = SequenceLoader(os.path.join(cur_dir, 'data/testForceEncoder.json')).createSystem()
        ensemble = Ensemble(system)
        self.force.bindEnsemble(ensemble)
        
        asn_leu = np.load(os.path.join(force_field_dir, 'ASN-LEU.npz'))
        assert (
            self.force.force_field_vector[0].getEnergy(asn_leu['energy_coord'][2]) / kilojoule_permol ==
            pytest.approx(asn_leu['energy_data'][2])
        )

    def test_calculateTorsionEnergy(self):
        system = SequenceLoader(os.path.join(cur_dir, 'data/testForceEncoder.json')).createSystem()
        ensemble = Ensemble(system)
        self.force.bindEnsemble(ensemble)
        
        torsion_angle = getTorsion(
            self.force._torsions[0][0].coordinate,
            self.force._torsions[0][1].coordinate,
            self.force._torsions[0][2].coordinate,
            self.force._torsions[0][3].coordinate
        )
        assert isAlmostEqual(
            self.force.force_field_vector[0].getEnergy(torsion_angle),
            self.force.calculateTorsionEnergy(0)
        )

    def test_calculatePotentialEnergy(self):
        system = SequenceLoader(os.path.join(cur_dir, 'data/testForceEncoder.json')).createSystem()
        ensemble = Ensemble(system)
        self.force.bindEnsemble(ensemble)
        
        torsion_angle0 = getTorsion(
            self.force._torsions[0][0].coordinate,
            self.force._torsions[0][1].coordinate,
            self.force._torsions[0][2].coordinate,
            self.force._torsions[0][3].coordinate
        )
        torsion_angle1 = getTorsion(
            self.force._torsions[1][0].coordinate,
            self.force._torsions[1][1].coordinate,
            self.force._torsions[1][2].coordinate,
            self.force._torsions[1][3].coordinate
        )
        
        assert (
            self.force.calculatePotentialEnergy() == (
                self.force.force_field_vector[0].getEnergy(torsion_angle0) +
                self.force.force_field_vector[1].getEnergy(torsion_angle1)
            )
        )

    def test_calculateAtomForce(self):
        system = SequenceLoader(os.path.join(cur_dir, 'data/testPDFFTorsionForce.json')).createSystem()
        ensemble = Ensemble(system)
        self.force.bindEnsemble(ensemble)
        
        assert isArrayEqual(
            np.array([0, 0, 0]),
            convertToNdArray(self.force.calculateAtomForce(0))
        )
        
        force1 = self.force.calculateAtomForce(1)
        vec1 = system.atoms[0].coordinate - system.atoms[1].coordinate
        vec2 = system.atoms[2].coordinate - system.atoms[1].coordinate
        assert np.dot(
            convertToNdArray(vec1),
            convertToNdArray(force1)
        ) == pytest.approx(0)
        assert np.dot(
            convertToNdArray(vec2),
            convertToNdArray(force1)
        ) == pytest.approx(0)
        
        force2 = self.force.calculateAtomForce(3)
        vec1 = system.atoms[2].coordinate - system.atoms[3].coordinate
        vec2 = system.atoms[0].coordinate - system.atoms[3].coordinate
        assert np.dot(
            convertToNdArray(vec1),
            convertToNdArray(force2)
        ) == pytest.approx(0)
        assert np.dot(
            convertToNdArray(vec2),
            convertToNdArray(force2)
        ) == pytest.approx(0)
        
        v0 = convertToNdArray(force1)
        v1 = convertToNdArray(force2)
        phi = np.arccos(np.dot(v0, v1) / (np.linalg.norm(v0)*np.linalg.norm(v1)))
        assert (
            phi + abs(getTorsion(
                system.topology.torsions[0][0].coordinate,
                system.topology.torsions[0][1].coordinate,
                system.topology.torsions[0][2].coordinate,
                system.topology.torsions[0][3].coordinate,
            )) == pytest.approx(np.pi)
        )
        