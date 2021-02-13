=========================
openpd.unit.Unit class
=========================

Overview
===========

``openpd.Unit`` has two attributes:

- ``base_dimension`` determines the dimension of ``Unit``.
- ``relative_value`` determines the relative value to the basic unit (usually SI unit) with ``base_dimension``.

The ``Unit`` has already covered all the information for a unit. However, as we talked in :ref:`package-intro`, the predefined units are all the instances of ``Quantity`` due to the cross import issue.

Class methods
==============

.. automodule:: openpd.unit.unit
   :members:
   :undoc-members:
   :show-inheritance:

.. important::

   Read-only properties:

   - ``unit_name``
   - ``base_dimension``
   - ``relative_value``

Example
=========

Instantiation
-------------

**Input**:

.. code-block:: python
    :linenos:

    import openpd.unit as unit

    length_dimension = unit.BaseDimension(length_dimension=1)
    unit_nanometer = unit.Unit(length_dimension, 1e-9)

    print(unit_nanometer.unit_name)
    print(unit_nanometer.relative_value)

**Output**:

.. parsed-literal::

    m
    1e-09
