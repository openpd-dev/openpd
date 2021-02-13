import numpy as np
from copy import deepcopy
from . import BaseDimension, Unit
from .. import isAlmostEqual

class Quantity:
    def __init__(self, value, unit:Unit) -> None:
        """
        Parameters
        ----------
        value : int or float
            the value of quantity
        unit : Unit
            the unit of quantity
        """        
        self.value = value
        self.unit = unit

    def isDimensionLess(self):
        """
        isDimensionLess judges wether ``self`` is dimensionless

        Returns
        -------
        bool
            - True, the quantity is dimensionless
            - False, the quantity isn't dimensionless
        """      
        if self.unit.isDimensionLess():
            return True
        else:
            return False

    # If the unit is dimensionless, just return the absolute value
    def judgeAndReturn(self):
        """
        judgeAndReturn returns different value depends on the result of ``self.isDimensionLess()``

        Returns
        -------
        int or float or Quantity
            - If ``self.isDiemsionLess() == True``, return the ``self.value * self.unit.relative_value``
            - If ``self.isDiemsionLess() == False``, return ``deepcopy(self)``
        """        
        if self.isDimensionLess():
            return self.value * self.unit.relative_value
        else:
            return deepcopy(self)

    def __repr__(self) -> str:
        return (
            '<Quantity object: %e %s at 0x%x>' 
            %(self.value*self.unit.relative_value, self.unit.base_dimension, id(self))
        )

    def __str__(self) -> str:
        return (
            '%e %s' %(self.value*self.unit.relative_value, self.unit.base_dimension)
        )

    def __eq__(self, other) -> bool:
        if isinstance(other, Quantity):
            if (
                isAlmostEqual(other.value * other.unit.relative_value, self.value * self.unit.relative_value) and 
                other.unit.base_dimension == self.unit.base_dimension
            ):
                return True
            else:
                return False
        # Value judgement, without relative value like 10*angstrom == 10
        else:
            if other == self.value:
                return True
            else:
                return False

    def __add__(self, other):
        if isinstance(other, Quantity):
            return Quantity(
                self.value + other.value * (other.unit.relative_value / self.unit.relative_value) ,
                self.unit + other.unit # Test wether the base dimension is same Or the dimension will be changed in the next step
            ).judgeAndReturn()
        elif isinstance(other, list):
            res = []
            for value in other:
                res.append(self+value)
            return res
        elif isinstance(other, np.ndarray):
            res = []
            for value in other:
                res.append(self+value)
            return np.array(res)
        else:
            return Quantity(
                self.value + other,
                self.unit
            ).judgeAndReturn()

    __iadd__ = __add__
    
    def __radd__(self, other):
        if isinstance(other, Quantity):
            return Quantity(
                other.value + self.value * (self.unit.relative_value / other.unit.relative_value) ,
                other.unit + self.unit
            ).judgeAndReturn()
        elif isinstance(other, list):
            res = []
            for value in other:
                res.append(self+value)
            return res
        elif isinstance(other, np.ndarray):
            res = []
            for value in other:
                res.append(self+value)
            return np.array(res)
        else:
            return Quantity(
                self.value + other,
                self.unit
            ).judgeAndReturn()

    def __sub__(self, other):
        if isinstance(other, Quantity):
            return Quantity(
                self.value - other.value * (other.unit.relative_value / self.unit.relative_value) ,
                self.unit - other.unit
            ).judgeAndReturn()
        elif isinstance(other, list):
            res = []
            for value in other:
                res.append(self - value)
            return res
        elif isinstance(other, np.ndarray):
            res = []
            for value in other:
                res.append(self - value)
            return np.array(res)
        else:
            return Quantity(
                self.value - other,
                self.unit
            ).judgeAndReturn()

    __isub__ = __sub__

    def __rsub__(self, other):
        if isinstance(other, Quantity):
            return Quantity(
                other.value - self.value * (self.unit.relative_value / other.unit.relative_value),
                other.unit - self.unit 
            ).judgeAndReturn()
        elif isinstance(other, list):
            res = []
            for value in other:
                res.append(value - self)
            return res
        elif isinstance(other, np.ndarray):
            res = []
            for value in other:
                print(type(value))
                res.append(value - self)
            return np.array(res)
        else:
            return Quantity(
                other - self.value,
                self.unit
            ).judgeAndReturn()

    def __mul__(self, other):
        if isinstance(other, Quantity):
            return Quantity(
                self.value * other.value,
                self.unit * other.unit
            ).judgeAndReturn()
        elif isinstance(other, list):
            res = []
            for value in other:
                res.append(self * value)
            return res
        elif isinstance(other, np.ndarray):
            res = []
            for value in other:
                res.append(self * value)
            return np.array(res)
        else:
            return Quantity(
                self.value * other,
                1 * self.unit
            ).judgeAndReturn()

    __imul__ = __mul__
    __rmul__ = __mul__
    
    def __truediv__(self, other):
        if isinstance(other, Quantity):
            if other.value == 0:
                raise ValueError('Dividing 0: Nan')
            return Quantity(
                self.value / other.value,
                self.unit / other.unit
            ).judgeAndReturn()
        elif isinstance(other, list):
            res = []
            for value in other:
                res.append(self/value)
            return res
        elif isinstance(other, np.ndarray):
            res = []
            for value in other:
                res.append(self/value)
            return np.array(res)
        else:
            if other == 0:
                raise ValueError('Dividing 0: Nan')
            return Quantity(
                self.value / other,
                self.unit
            ).judgeAndReturn()

    __itruediv__ = __truediv__

    def __rtruediv__(self, other):
        if self.value == 0:
            raise ValueError('Dividing 0: Nan')
        elif isinstance(other, Quantity):
            return Quantity(
                other.value / self.value,
                other.unit / self.unit
            ).judgeAndReturn()
        elif isinstance(other, list):
            res = []
            for value in other:
                res.append(value/self)
            return res
        elif isinstance(other, np.ndarray):
            res = []
            for value in other:
                res.append(value/self)
            return np.array(res)
        else:
            return Quantity(
                other / self.value,
                1 / self.unit
            ).judgeAndReturn()

    def __pow__(self, value):
        res = Quantity(1, Unit(BaseDimension(), 1)) # result of **0
        if value > 0:
            for _ in range(value):
                res *= self
        elif value < 0:
            for _ in range(abs(value)):
                res /= self
        return res.judgeAndReturn()