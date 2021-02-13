================================
openpd.unit.BaseDimension class
================================

Overview
===========

``openpd.unit.BaseDimension`` determine the dimension of a unit. For example, a velocity unit, no matter which unit is used, has the dimension of :math:`L/T`.

.. hint:: 

    ``openpd.unit.baseDimension`` has 5 basic dimension:

    - :math:`L`: Length, SI unit: m
    - :math:`M`: Mass, SI unit: kg
    - :math:`T`: Time, SI unit: s
    - :math:`C`: Charge, SI unit: coulomb
    - :math:`Mol`: Amount of substance, SI unit: mol

.. note:: The quantity operation results will automatically turn to ``<float>`` while the results are dimensionless.


Class methods
==============
.. automodule:: openpd.unit.baseDimension
   :members:
   :undoc-members:
   :show-inheritance:

.. important::

   Read-only properties:

   - ``length_dimension``
   - ``time_dimension``
   - ``mass_dimension``
   - ``temperature_dimension``
   - ``charge_dimension``
   - ``mol_dimension``
   - ``name``

Example
=========

Instantiation
-------------

**Input**:

.. code-block:: python
    :linenos:

    import openpd.unit as unit

    velocity_dimension = unit.BaseDimension(length_dimension=1, time_dimension=-1)
    print(velocity_dimension.length_dimension)
    print(velocity_dimension.time_dimension)
    print(velocity_dimension.mass_dimension)
    print(velocity_dimension)

**Output**:

.. parsed-literal::

    1
    -1
    0
    m/s