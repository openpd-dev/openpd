import math
import multiprocessing as mp
import numpy as np
import openpd.unit as unit
from .. import Ensemble
from ..unit import *
from ..unit import Quantity
from ..exceptions import NonboundError, RebindError, DismatchedDimensionError

class Integrator:
    def __init__(self, sim_interval=1) -> None:
        """
        Parameters
        ----------
        sim_interval : int or Quantity, optional
            the step sim_interval of the integrator, by default ``1 * femtosecond``

        Raises
        ------
        ValueError
            When the parameter ``sim_interval`` is ``Quantity`` and ``sim_interval.unit.base_dimension != BaseDimension(time_dimension=1)``
        """        
        if isinstance(sim_interval, Quantity):
            sim_interval.convertTo(femtosecond)
        else:
            sim_interval = sim_interval * femtosecond
        
        self._sim_interval = sim_interval
        self._is_bound = False # This will turn to True in Simulation.__init__()
        self._ensemble = None

    def __repr__(self):
        return (
            '<Integrator object: step sim_interval %s at 0x%x>'
            %(self._sim_interval, id(self))
        )

    __str__ = __repr__
    
    def _bindEnsemble(self, ensemble:Ensemble):
        """
        _bindEnsemble binds integrator to an ``Ensemble`` instance
        
        This will only called by ``Simulation`` instance

        Parameters
        ----------
        ensemble : Ensemble
            target ``Ensemble``

        Raises
        ------
        openpd.exceptions.RebindError
            When bind ``Integrator`` multi-times
        """        
        if self._is_bound:
            raise RebindError('This integrator has been bonded, can not be bound again!')
        self._ensemble = ensemble
        self._system = ensemble.system
        self._is_bound = True

    def _testBound(self):
        if not self._is_bound:
            raise NonboundError('Integrator has not been bound to any Simulation instance')

    def setVelocityToTemperature(self, temperature):
        """
        setVelocityToTemperature sets atoms' velocity to meet the temperature requirement

        Parameters
        ----------
        temperature : int or float or Quantity
            target temperature, Unit default to be ``kelvin`` if ``int`` or ``float`` is provided

        Raises
        ------
        AttributeError
            When ``self`` has not been bound to any ``Simulation`` instance

        ValueError
            When the dimension of input ``temperature`` is Quantity and != ``BaseDimension(temperature_dimension=1)``
        """        
        self._testBound()
        if isinstance(temperature, Quantity):
            if temperature.unit.base_dimension != unit.temperature:
                raise DismatchedDimensionError(
                    'Dimension of parameter temperature should be s instead of %s' 
                    %(temperature.unit.base_dimension)
                )
            else:
                temperature = temperature / kelvin * kelvin
        else:
            temperature = temperature * kelvin

        for atom in self._system.atoms:
            width = (3 * k_b * temperature / atom.mass).sqrt()
            atom.velocity = np.random.rand(3) * 2 * width - width
        
        # Rescale temperature
        scale = self.calculateTemperature() / temperature
        for atom in self._system.atoms:
            atom.velocity /= np.sqrt(scale)
        

    def calculateKineticEnergy(self):
        """
        calculateKineticEnergy returns the kinetic energy of all atoms

        Returns
        -------
        Quantity
            Kinetic energy of all atoms

        Raises
        ------
        AttributeError
            When ``self`` has not been bound to any ``Simulation`` instance
        """        
        self._testBound()
        
        kinetic_energy = 0
        for atom in self._system.atoms:
            kinetic_energy += atom.mass * (atom.velocity**2).sum() / 2
        return kinetic_energy.convertTo(kilojoule_permol)

    def calculateTemperature(self):
        """
        calculateTemperature returns the temperature of the Simulation System

        Returns
        -------
        Quantity
            Temperature of Simulation System

        Raises
        ------
        AttributeError
            When ``self`` has not been bound to any ``Simulation`` instance
        """     
        self._testBound()
        kinetic_energy = self.calculateKineticEnergy()
        return kinetic_energy * 2 / 3 / self._system.num_atoms / k_b
        
    def updateForce(self, force_group=[0]):
        """
        updateForce updates the force acts on all ``Atom``

        This method needs to be overloaded for all subclass
        """  
        num_processes = mp.cpu_count() if self._system.num_atoms > mp.cpu_count() else self._system.num_atoms
        atom_ranges = np.array_split([atom.atom_id for atom in self._system.atoms], num_processes)

        jobs = []
        manager = mp.Manager()
        return_dict = manager.dict()
        for atom_range in atom_ranges:            
            jobs.append(mp.Process(
                target=self._calculateAtomForce,
                args=(atom_range, force_group, return_dict)
            ))
            jobs[-1].start()
        [p.join() for p in jobs]
        for atom in self._system.atoms:
            atom.force = return_dict[atom.atom_id]

    def _calculateAtomForce(self, atom_range, force_group, return_dict):
        for atom_id in atom_range:
            return_dict[atom_id] = self._ensemble.calculateAtomForce(atom_id, force_group)

    def step(self, num_steps:int):
        """
        step iteratively integrate ``system`` based on the forces in ``ensemble``

        This method needs to be overloaded for all subclass

        Parameters
        ----------
        num_steps : int
            the number of steps that integrator will integrate

        Raises
        ------
        NotImplementedError
            When the subclass does not overload this method
        """        
        raise NotImplementedError('step() method has not been overloaded yet!')

    @property
    def sim_interval(self):
        """
        sim_interval gets the step sim_interval of ``self``

        Returns
        -------
        Quantity
            the step sim_interval of ``self``
        """        
        return self._sim_interval

    @sim_interval.setter
    def sim_interval(self, sim_interval):
        """
        setter method to set the step sim_interval of ``self``

        Parameters
        ----------
        sim_interval : int or float or Quantity
            the step sim_interval of the integrator, Unit default to be ``femtosecond`` if ``int`` or ``float`` is provided

        Raises
        ------
        ValueError
            When the dimension of input ``sim_interval`` is Quantity and != ``BaseDimension(time_dimension=1)``
        """        
        if isinstance(sim_interval, Quantity):
            if sim_interval.unit.base_dimension != unit.time:
                raise DismatchedDimensionError(
                    'Dimension of parameter sim_interval should be s instead of %s' 
                    %(sim_interval.unit.base_dimension)
                )
            else:
                sim_interval = sim_interval / femtosecond * femtosecond
        else:
            sim_interval = sim_interval * femtosecond
        self._sim_interval = sim_interval 

    @property
    def ensemble(self):
        """
        system gets the ``ensemble`` that bound to ``self``

        Returns
        -------
        System
            the ``ensemble`` that bound to ``self``
        """
        self._testBound()
        return self._ensemble