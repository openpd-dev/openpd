from .. import uniqueList

class BaseDimension:
    def __init__(
            self, length_dimension=0, 
            time_dimension=0, 
            mass_dimension=0, 
            temperature_dimension=0, 
            charge_dimension = 0,
            mol_dimension=0
        ) -> None:
        """
        Parameters
        ----------
        length_dimension : int, optional
            dimension of length, by default 0
        time_dimension : int, optional
            dimension of time, by default 0
        mass_dimension : int, optional
            dimension of mass, by default 0
        temperature_dimension : int, optional
            dimension of temperature, by default 0
        charge_dimension : int, optional
            dimension of charge, by default 0
        mol_dimension : int, optional
            dimension of amount of substance, by default 0
        """        
        self._length_dimension = length_dimension
        self._time_dimension = time_dimension
        self._mass_dimension = mass_dimension
        self._temperature_dimension = temperature_dimension
        self._charge_dimension = charge_dimension
        self._mol_dimension = mol_dimension
        self._dimension_list = [
            self._length_dimension,
            self._time_dimension,
            self._mass_dimension,
            self._temperature_dimension,
            self._charge_dimension,
            self._mol_dimension
        ]
        # The name of base dimension will be replaced with the name of its corresponding SI Unit
        # Like m for length and kg for mass
        self._dimension_name = [
            'm',
            's',
            'kg',
            'k',
            'c',
            'mol'
        ]
        self._generateDimensionName()

    def _generateDimensionName(self):
        self._name = ''
        if uniqueList(self._dimension_list) == [0]:
            return None # self._name = '' 
        else:
            zipped = zip(self._dimension_list, self._dimension_name)
            sort_zipped = sorted(zipped, key=lambda x:(x[0]*-1, x[1]))
            res = zip(*sort_zipped)
            dimensions, names = [list(x) for x in res]
 
            for i, dimension in enumerate(dimensions):
                if i > 1 and dimension < 0 and dimensions[i-1] >= 0:
                    if self._name != '':
                        self._name = self._name[:-1] + '/' # Change the final * to /
                    else:
                        self._name = '1/'
                if dimension > 1:
                    self._name += names[i] + '^%d*' %dimension
                elif dimension == 1:
                    self._name += names[i] + '*'
                elif dimension == 0:
                    pass
                elif dimension == -1:
                    self._name += names[i] + '*'
                elif dimension < -1:
                    self._name += names[i] + '^%d*' %(-dimension)

            self._name = self._name[:-1] # Get rid of the last *

    def __repr__(self) -> str:
        return (
            '<BaseDimension object: %s at 0x%x>' 
            %(self._name, id(self))
        )

    def __str__(self) -> str:
        return self._name

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
        """
        isDimensionLess judges wether ``self`` is a dimensionless

        Returns
        -------
        [type]
            [description]
        """        
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
        """
        length_dimension gets the dimension of length

        Returns
        -------
        int
            dimension of length
        """        
        return self._length_dimension

    @property
    def time_dimension(self):
        """
        time_dimension gets the dimension of time

        Returns
        -------
        int
            dimension of time
        """   
        return self._time_dimension

    @property
    def mass_dimension(self):
        """
        mass_dimension gets the dimension of mass

        Returns
        -------
        int
            dimension of mass
        """   
        return self._mass_dimension

    @property
    def temperature_dimension(self):
        """
        temperature_dimension gets the dimension of temperature

        Returns
        -------
        int
            dimension of temperature
        """   
        return self._temperature_dimension

    @property
    def charge_dimension(self):
        """
        charge_dimension gets the dimension of charge

        Returns
        -------
        int
            dimension of charge
        """   
        return self._charge_dimension

    @property
    def mol_dimension(self):
        """
        mol_dimension gets the dimension of amount of substance

        Returns
        -------
        int
            dimension of amount of substance
        """   
        return self._mol_dimension

    @property
    def name(self):
        """
        name gets the name of ``self``

        The name of ``BaseDimension`` is consist with SI unit. 
        For example, ``BaseDimension(length_dimension=1, time_dimension=-1)`` has name 'm/s'

        Returns
        -------
        str
            name of BaseDimension
        """   
        return self._name
