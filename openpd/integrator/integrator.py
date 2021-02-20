import numpy as np

import openpd.unit as unit
from .. import System, Ensemble
from ..unit import *
from ..unit import Quantity

class Integrator:
    def __init__(self, interval=1) -> None:
        """
        Parameters
        ----------
        interval : int or Quantity, optional
            the step interval of the integrator, by default ``1 * femtosecond``

        Raises
        ------
        ValueError
            When the parameter ``interval`` is ``Quantity`` and ``interval.unit.base_dimension != BaseDimension(time_dimension=1)``
        """        
        if isinstance(interval, Quantity):
            if interval.unit.base_dimension != unit.time:
                raise ValueError(
                    'Dimension of parameter interval should be s instead of %s' 
                    %(interval.unit.base_dimension)
                )
            else:
                interval = interval / femtosecond * femtosecond
        else:
            interval = interval * femtosecond
        
        self._interval = interval
        self._is_bound = False # This will turn to True in Simulation.__init__()

    def __repr__(self):
        return (
            '<Integrator object: step interval %s at 0x%x>'
            %(self._interval, id(self))
        )

    __str__ = __repr__

    def _testBound(self):
        if not self._is_bound:
            raise AttributeError('Integrator has not been bound to any Simulation instance')

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
            if temperature.unit.base_dimension != unit.time:
                raise ValueError(
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
        calculateKineticEnergy returns the kinetic energy of the ``self.system``

        Returns
        -------
        Quantity
            Kinetic energy of ``self.system``

        Raises
        ------
        AttributeError
            When ``self`` has not been bound to any ``Simulation`` instance
        """        
        self._testBound()
        
        kinetic_energy = 0
        for atom in self.system.atoms:
            kinetic_energy += atom.mass * (atom.velocity**2).sum() / 2
        return kinetic_energy.convertTo(kilojoule_permol)

    def calculateTemperature(self):
        """
        calculateTemperature returns the temperature of the ``self.system``

        Returns
        -------
        Quantity
            Temperature of ``self.system``

        Raises
        ------
        AttributeError
            When ``self`` has not been bound to any ``Simulation`` instance
        """     
        self._testBound()
        kinetic_energy = self.calculateKineticEnergy()
        return kinetic_energy * 2 / 3 / self._system.num_atoms / k_b

    def _bindTo(self, system:System, ensemble:Ensemble):
        if self._is_bound:
            raise AttributeError('This integrator has been bonded, can not be bound again!')
        self._system = system
        self._ensemble = ensemble
        self._is_bound = True

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
    def interval(self):
        """
        interval gets the step interval of ``self``

        Returns
        -------
        Quantity
            the step interval of ``self``
        """        
        return self._interval

    @interval.setter
    def interval(self, interval):
        """
        setter method to set the step interval of ``self``

        Parameters
        ----------
        interval : int or float or Quantity
            the step interval of the integrator, Unit default to be ``femtosecond`` if ``int`` or ``float`` is provided

        Raises
        ------
        ValueError
            When the dimension of input ``interval`` is Quantity and != ``BaseDimension(time_dimension=1)``
        """        
        if isinstance(interval, Quantity):
            if interval.unit.base_dimension != unit.time:
                raise ValueError(
                    'Dimension of parameter interval should be s instead of %s' 
                    %(interval.unit.base_dimension)
                )
            else:
                interval = interval / femtosecond * femtosecond
        else:
            interval = interval * femtosecond
        self._interval = interval 
    
    @property
    def system(self):
        """
        system gets the ``system`` that bound to ``self``

        Returns
        -------
        System
            the ``system`` that bound to ``self``
        """        
        self._testBound()
        return self._system

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