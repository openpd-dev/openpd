==========================
openpd.unit.Quantity class
==========================

Overview
===========

``openpd.unit.Quantity`` is designed to represent a physical quantity (value with unit), having two attributes:

- ``value``: the value of physical quantity
- ``unit``: the unit of physical quantity

.. note:: All the predefined units are all ``Quantity`` instances.

The math operations are full defined for ``Quantity``, including:

- ``__eq__``
- ``__add__``, ``__radd__``, ``__iadd__``
- ``__sub__``, ``__rsub__``, ``__isub__``
- ``__mul__``, ``__rmul__``, ``__imul__``
- ``__truediv__``, ``__rtruediv__``, ``__itruediv__``

Class methods
==============
.. automodule:: openpd.unit.quantity
   :members:
   :undoc-members:
   :show-inheritance:

Example
========

Instantiation
--------------

**Input**:

.. code-block:: python
    :linenos:

    import openpd.unit as unit

    length_dimension = unit.BaseDimension(length_dimension=1)
    nanometer = unit.Quantity(1, unit.Unit(length_dimension, 1e-9))

    print(nanometer.value)
    print(nanometer.unit)

**Output**:

.. parsed-literal::

    1
    m

Math operations
-----------------

**Input**:

.. code-block:: python
    :linenos:

    import openpd.unit as unit

    meter = 2 * unit.meter
    newton = 3 * unit.newton
    joule = 1 * unit.joule

    print(meter*newton)
    print(joule)
    print(meter*newton == 6*joule)

**Output**:

.. parsed-literal::

    6.000000e+00 m^2*kg/s^2
    1.000000e+00 m^2*kg/s^2
    True