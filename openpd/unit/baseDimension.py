class BaseDimension(object):
    def __init__(
            self, length_dimension=0, 
            time_dimension=0, 
            mass_dimension=0, 
            temperature_dimension=0, 
            charge_dimension = 0,
            mol_dimension=0
        ) -> None:
        super().__init__()
        self._length_dimension = length_dimension
        self._time_dimension = time_dimension
        self._mass_dimension = mass_dimension
        self._temperature_dimension = temperature_dimension
        self._charge_dimension = charge_dimension
        self._mol_dimension = mol_dimension
        self.name = ''
        if self._length_dimension != 0:
            if self._length_dimension == 1:
                self.name += 'LENGTH*'
            else:
                self.name += 'LENGTH^%d*' %self._length_dimension
        if self._time_dimension != 0:
            if self._time_dimension == 1:
                self.name += 'TIME*'
            else:
                self.name += 'TIME^%d*' %self._time_dimension
        if self._mass_dimension != 0:
            if self._mass_dimension == 1:
                self.name += 'MASS*'
            else:
                self.name += 'MASS^%d*' %self._mass_dimension
        if self._temperature_dimension != 0:
            if self._temperature_dimension == 1:
                self.name += 'TEMPERATURE*'
            else:
                self.name += 'TEMPERATURE^%d*' %self._temperature_dimension
        if self._charge_dimension != 0:
            if self._charge_dimension == 1:
                self.name += 'CHARGE*'
            else:
                self.name += 'CHARGE^%d*' %self._charge_dimension
        if self._mol_dimension != 0:
            if self._mol_dimension == 1:
                self.name += 'MOL*'
            else:
                self.name += 'MOL^%d*' %self._mol_dimension
        if self.name == '':
            self.name += 'DIMENSIONLESS'
        else:
            self.name = self.name[:-1] # Get rid of the last *

    def __repr__(self) -> str:
        return (
            '<BaseDimension object: %s at 0x%x>' 
            %(self.name, id(self))
        )

    def __str__(self) -> str:
        return self.name

    def __eq__(self, base_unit):
        if (
            self._length_dimension == base_unit.length_dimension and 
            self._time_dimension == base_unit.time_dimension and 
            self._mass_dimension == base_unit.mass_dimension and 
            self._temperature_dimension == base_unit.temperature_dimension and 
            self._charge_dimension == base_unit.charge_dimension and
            self._mol_dimension == base_unit.mol_dimension
        ):
            return True
        else:
            return False

    def __ne__(self, base_unit) -> bool:
        if (
            self._length_dimension != base_unit.length_dimension or 
            self._time_dimension != base_unit.time_dimension or
            self._mass_dimension != base_unit.mass_dimension or 
            self._temperature_dimension != base_unit.temperature_dimension or 
            self._charge_dimension != base_unit.charge_dimension or
            self._mol_dimension != base_unit.mol_dimension
        ):
            return True
        else:
            return False

    def __mul__(self, base_unit):
        return BaseDimension(
            self._length_dimension + base_unit.length_dimension,
            self._time_dimension + base_unit.time_dimension,
            self._mass_dimension + base_unit.mass_dimension,
            self._temperature_dimension + base_unit.temperature_dimension,
            self._charge_dimension + base_unit.charge_dimension,
            self._mol_dimension + base_unit.mol_dimension
        )

    def __rmul__(self, other):
        return BaseDimension(
            self._length_dimension,
            self._time_dimension,
            self._mass_dimension,
            self._temperature_dimension,
            self._charge_dimension,
            self._mol_dimension
        )

    def __truediv__(self, base_unit):
        return BaseDimension(
            self._length_dimension - base_unit.length_dimension,
            self._time_dimension - base_unit.time_dimension,
            self._mass_dimension - base_unit.mass_dimension,
            self._temperature_dimension - base_unit.temperature_dimension,
            self._charge_dimension - base_unit.charge_dimension,
            self._mol_dimension - base_unit.mol_dimension
        )

    def __rtruediv__(self, other):
        return BaseDimension(
            -self._length_dimension,
            -self._time_dimension,
            -self._mass_dimension,
            -self._temperature_dimension,
            -self._charge_dimension,
            -self._mol_dimension
        )

    def __pow__(self, value):
        return BaseDimension(
            self._length_dimension * value,
            self._time_dimension * value,
            self._mass_dimension * value,
            self._temperature_dimension * value,
            self._charge_dimension * value,
            self._mol_dimension * value
        )

    def isDimensionLess(self):
        if (
            self._length_dimension == 0 and
            self._time_dimension == 0 and
            self._mass_dimension == 0 and
            self._temperature_dimension == 0 and
            self._charge_dimension == 0 and
            self._mol_dimension == 0 
        ):
            return True
        else:
            return False

    @property
    def length_dimension(self):
        return self._length_dimension

    @property
    def time_dimension(self):
        return self._time_dimension

    @property
    def mass_dimension(self):
        return self._mass_dimension

    @property
    def temperature_dimension(self):
        return self._temperature_dimension

    @property
    def charge_dimension(self):
        return self._charge_dimension

    @property
    def mol_dimension(self):
        return self._mol_dimension
