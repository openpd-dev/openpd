===================================
How to use the openpd.unit package
===================================

Introduction
=============

The ``openpd.unit`` package is designed to convert unit for both simulation and analysis conveniently. Meanwhile, ``openpd.unit`` also has the constant quantity like the Avogadro constant and the Boltzmann Constant. 

In OpenPD, every ``unit`` exists as an instance of ``Quantity`` with two attributes: ``value`` and ``unit:Unit`` . 

.. note::
    As we want to achieve that :code:`1 * unit.nanometer` returns a ``quantity`` while the ``Unit`` is an attribute of ``Quantity`` (cross import issue). We define all the basic unit as an ``Quantity`` with ``quantity.value = 1``
    

The ``quantity.unit`` is the attributes to express which unit does the ``quantity`` has. And it has two attributes ``base_dimension:BaseDimension``  and ``relative_value``. The ``base_dimension`` is used to determine the unit's basic dimension, like :math:`L`, :math:`M`, and :math:`ML/T^2`. 

.. seealso::

    - :doc:`../../modules/unit/quantity` page
    - :doc:`../../modules/unit/unit` page
    - :doc:`../../modules/unit/baseDimension` page
  
.. hint:: 

    ``openpd.unit.baseDimension`` has 5 basic dimension:

    - :math:`L`: Length, SI unit: m
    - :math:`M`: Mass, SI unit: kg
    - :math:`T`: Time, SI unit: s
    - :math:`C`: Charge, SI unit: coulomb
    - :math:`Mol`: Amount of substance, SI unit: mol

And the ``relative_value``gives the relationship between the current unit and the SI unit. For example, the ``relative_value`` of nanometer will be ``1e-9``. 

The unit package can accomplish most of the work attributes to the unit, including but not limited to: unit converting, unit multiplying, unit division.

.. seealso:: The predefined unit list can be check in :ref:`predefined-unit`

This tutorial will give many useful demo codes to demonstrate the correction and show the primary usage of this package. 

.. note:: All the code show below can be found in :file:`<openpd path>/tutorials/unit.ipynb`.

.. _import-unit-package:

Import unit package 
====================

.. code-block:: python
    :linenos:

    import openpd as pd
    import openpd.unit as unit

Usually, we recommend importing the ``openpd.unit`` as shown above, calling with the prefix ``unit`` to prevent the variable duplication. Instead of using:

.. code-block:: python
    :linenos:

    from openpd.unit import *

Constant
========

Avogadro constant
-----------------

The Avogadro constant is defined as:

.. math::

    N_a = 6.0221 \times 10^{23} mol^{-1}

So we have:

.. math::

    1\ mol \times N_a = 6.0221 \times 10^{23}

**Input**:

.. code-block:: python
    :linenos:

    # 1 mol * Na = 6.0221e23 
    quantity = unit.n_a * unit.mol

    print(type(quantity))    
    print(quantity)

**Output**:

.. parsed-literal::

    <class 'float'>
    6.0221e+23

.. hint:: The quantity operation results will automatically turn to ``<float>`` while the results are dimensionless.

And we also have:

.. math::

    \frac{6.0221 \times 10^{23}}{N_a} = 1\ mol 

**Input**:

.. code-block:: python
    :linenos:

    # 6.0221e23 / Na = 1 mol
    quantity = 6.0221e23 / unit.n_a
    
    print(type(quantity))
    print(quantity)
    print(quantity.value)
    print(quantity.unit)

**Output**:

.. parsed-literal::

    <class 'openpd.unit.quantity.Quantity'>
    1.000000e+00 mol
    1.0
    mol


Boltzmann constant
------------------
The Boltzmann constant has the dimension of Energy/Temperature as
:math:`k_B T` has dimension of energy:

.. math::

    k_B = 1.3806505 \times 10^{-23} J/K

**Input**:

.. code-block:: python
    :linenos:

    # kb * T has dimension of energy
    quantity = 1 * unit.kelvin * unit.k_b 
    
    print(type(quantity))
    print(quantity)
    print(quantity.value)
    print(quantity.unit)
    print('\n')
    
    quantity = 1 * unit.kelvin * unit.k_b / unit.joule
    
    print(type(quantity))
    print(quantity)

**Output**:

.. parsed-literal::

    <class 'openpd.unit.quantity.Quantity'>
    1.380649e-23 m^2*kg/s^2
    1.38064852e-23
    m^2*kg/s^2
    
    
    <class 'float'>
    1.38064852e-23

**Input**:

.. code-block:: python
    :linenos:

    # 300kb = 2.494 kj/mol
    quantity = 300 * unit.kelvin * unit.k_b / unit.kilojoule_permol
    
    print(type(quantity))
    print(quantity)

**Output**:

.. parsed-literal::

    <class 'float'>
    2.4943210356875993

**Input**:

.. code-block:: python
    :linenos:

    # 300kb = 0.5962 kcal/mol
    quantity = 300 * unit.kelvin * unit.k_b / unit.kilocalorie_permol
    
    print(type(quantity))
    print(quantity)

**Output**:

.. parsed-literal::

    <class 'float'>
    0.5961570352981834


Length Unit
===========

**Input**:

.. code-block:: python
    :linenos:

    quantity = 1 * unit.meter
    
    print('1m = %e cm' %(quantity/unit.centermeter))
    print('1m = %e mm' %(quantity/unit.millimeter))
    print('1m = %e um' %(quantity/unit.micrometer))
    print('1m = %e nm' %(quantity/unit.nanometer))
    print('1m = %e a' %(quantity/unit.angstrom))

**Output**:

.. parsed-literal::

    1m = 1.000000e+02 cm
    1m = 1.000000e+03 mm
    1m = 1.000000e+06 um
    1m = 1.000000e+09 nm
    1m = 1.000000e+10 a


Mass Unit
=========

The atomic mass unit (AMU), or dalton is defined as:

.. math::

    1\ dalton = 1.660539 \times 10^{−27} kg

**Input**:

.. code-block:: python
    :linenos:

    quantity = 1 * unit.dalton
    
    print(quantity == 1*unit.amu)
    print('1 dalton = %e kg' %(quantity/unit.kilogram))
    print('1 dalton = %e g' %(quantity/unit.gram))

**Output**:

.. parsed-literal::

    True
    1 dalton = 1.660539e-27 kg
    1 dalton = 1.660539e-24 g


Time Unit
=========

**Input**:

.. code-block:: python
    :linenos:

    quantity = 1 * unit.second
    
    print('1s = %e ms' %(quantity/unit.millisecond))
    print('1s = %e us' %(quantity/unit.microsecond))
    print('1s = %e ns' %(quantity/unit.nanosecond))
    print('1s = %e ps' %(quantity/unit.picosecond))
    print('1s = %e fs' %(quantity/unit.femtosecond))

**Output**:

.. parsed-literal::

    1s = 1.000000e+03 ms
    1s = 1.000000e+06 us
    1s = 1.000000e+09 ns
    1s = 1.000000e+12 ps
    1s = 1.000000e+15 fs


Charge Unit
===========

The standard charge unit is coulomb and its relationship with electron
charge is:

.. math::

       1 e = 1.60217662 \times 10^{-19} C

**Input**:

.. code-block:: python
    :linenos:

    quantity = 1. * unit.e
    
    print('1e = %e C' %(quantity/unit.coulomb))

**Output**:

.. parsed-literal::

    1e = 1.602177e-19 C


Unit Mixture
============
``openpd.unit`` also support the multiple and division of ``units`` as shown below:

**Input**:

.. code-block:: python
    :linenos:

    # Energy = Force * Length
    print(1*unit.meter*unit.newton)
    print(1*unit.joule)
    print(1*unit.meter*unit.newton == 1*unit.joule)

**Output**:

.. parsed-literal::

    1.000000e+00 m^2*kg/s^2
    1.000000e+00 m^2*kg/s^2
    True

**Input**:

.. code-block:: python
    :linenos:

    # Power = Energy / Time
    print(1*unit.joule/unit.second)
    print(1*unit.watt)
    print(1*unit.joule/unit.second == 1*unit.watt)

**Output**:

.. parsed-literal::

    1.000000e+00 m^2*kg/s^3
    1.000000e+00 m^2*kg/s^3
    True

.. _self-defined-unit:

Self-defined Unit
============================

In OpenPD, users can also define the ``unit`` by themselves, as shown below.

Define a Basic Unit
--------------------

**Input**:

.. code-block:: python
    :linenos:

    # Define a nanometer
    length_dimension = unit.BaseDimension(length_dimension=1)
    relative_value = 1e-9
    nanometer = unit.Quantity(1, unit.Unit(length_dimension, relative_value))

    print(nanometer==unit.nanometer)

**Output**:

.. parsed-literal::

    True

Define a Mixture Unit
----------------------

**Input**:

.. code-block:: python
    :linenos:

    # Define kj
    # Energy dimension: M L^2 / T^2
    energy_dimension = unit.BaseDimension(
        mass_dimension=1, length_dimension=2, time_dimension=-2
    )
    relative_value = 1e3
    kilojoule = unit.Quantity(1, unit.Unit(energy_dimension, relative_value))

    print(kilojoule==unit.kilojoule)

**Output**:

.. parsed-literal::

    True

Define a constant Unit
-------------------------
.. note:: 

    The definition of constants is different from other units. The constants always have the ``quantity.relative_value=1`` and ``quantity.value`` corresponds to the real value of their definition, as we treat them as the criterion of the corresponding dimension. As the existence of such dimension is used as a unit converter, such as :math:`Energy/Temperature`, the constants themselves are better choices for the criterions than the simple operation of SI units. 

**Input**:

.. code-block:: python
    :linenos:

    # Define k_b
    temperature_dimension = unit.BaseDimension(temperature_dimension=1)
    energy_dimension = unit.BaseDimension(
        mass_dimension=1, length_dimension=2, time_dimension=-2
    )
    k_b = unit.Quantity(
        1.38064852e-23, unit.Unit(energy_dimension/temperature_dimension, 1)
    )

    print(k_b==unit.k_b)

**Output**:

.. parsed-literal::

    True


Suppose we define the Avogadro constant unit with ``value=1`` and compared it with ``openpd.unit.n_a``: 

**Input**:

.. code-block:: python
    :linenos:

    mol_dimension = unit.BaseDimension(mol_dimension=1)
    n_a = unit.Quantity(1, unit.Unit(1/mol_dimension, 6.0221e23))

    a = 6.0221e23/n_a
    b = 6.0221e23/unit.n_a

    print('This is a:')
    print(a)
    print(a.value)
    print(a.unit.relative_value)

    print('\nThis is b:')
    print(b)
    print(b.value)
    print(b.unit.relative_value)

**Output**:

.. parsed-literal::

    This is a:
    1.000000e+00 mol
    6.0221e+23
    1.6605503063715315e-24

    This is b:
    1.000000e+00 mol
    1.0
    1.0

If we define the ``quantity.value=1`` and ``quantity.unit.relative_value=6.0221e23``, we found the final result, which is defined by ``quantity.value*quantity.unit.relative_value``, is the same, while the  ``quantity.value=6.0221e+23`` is misleading. As these constants are all defined as converters from a unit to another, it is reasonable to define them as their corresponding unit's criterion instead  of the SI one.