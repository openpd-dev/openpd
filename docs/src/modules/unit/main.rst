====================
openpd.unit package
====================

.. _package-intro:

Package introduction
======================

The ``openpd.unit`` package is designed to convert unit for both simulation and analysis conveniently. Meanwhile, ``openpd.unit`` also has the constant quantity like the Avogadro constant and the Boltzmann Constant. 

-----------------------------

.. image:: ./images/unit.svg
    :width: 550px
    :align: center

-----------------------------

As shown above, every ``unit`` exists as an instance of ``Quantity``. This is because we want to achieve that code :code:`1 * unit.nanometer` returns a ``Quantity`` while the ``Unit`` is also an attribute of ``Quantity``. If we define the ``__rmul__`` method of the ``Unit`` returning a ``Quantity`` instance, we will meet the cross import issue.

.. seealso:: :doc:`../../tutorials/howto_useunit/main` tutorial

.. _predefined-unit:

Pre-defined unit list 
======================

In OpenPD, many frequently used units have already been defined, as shown below. The user can use it with code like:

.. code-block:: python
    :linenos:

    import openpd as pd
    import openpd.unit as unit

    quantity = 1 * unit.nanometer

The import code is also discussed in :ref:`import-unit-package` . 

Meanwhile, the user can also define the custom unit by following codes in :ref:`self-defined-unit`

Base units
----------

.. table:: 
    :widths: 20 20 20 

    +----------------+--------------+-----------------+-------------+-------------+---------------------+
    |     Length     |     Mass     |      Time       | Temperature |   Charge    | Amount of substance |
    +================+==============+=================+=============+=============+=====================+
    | ``meter``      | ``kilogram`` | ``second``      | ``kelvin``  | ``coulomb`` | ``mol``             |
    +----------------+--------------+-----------------+-------------+-------------+---------------------+
    | ``decimeter``  | ``gram``     | ``millisecond`` |             | ``e``       | ``kilomol``         |
    +----------------+--------------+-----------------+-------------+-------------+---------------------+
    | ``centimeter`` | ``amu``      | ``microsecond`` |             |             |                     |
    +----------------+--------------+-----------------+-------------+-------------+---------------------+
    | ``micrometer`` | ``dalton``   | ``nanosecond``  |             |             |                     |
    +----------------+--------------+-----------------+-------------+-------------+---------------------+
    | ``nanometer``  |              | ``picosecond``  |             |             |                     |
    +----------------+--------------+-----------------+-------------+-------------+---------------------+
    | ``angstrom``   |              | ``femtosecond`` |             |             |                     |
    +----------------+--------------+-----------------+-------------+-------------+---------------------+

Mixture units
-------------

.. table:: 
    :widths: 20 20 40 20

    +-----------+----------------+------------------------+--------------+
    | Constants |     Force      |         Energy         |    Power     |
    +===========+================+========================+==============+
    | ``n_a``   | ``newton``     | ``joule``              | ``watt``     |
    +-----------+----------------+------------------------+--------------+
    | ``k_b``   | ``kilonewton`` | ``kilojoule``          | ``kilowatt`` |
    +-----------+----------------+------------------------+--------------+
    |           |                | ``kilojoule_permol``   |              |
    +-----------+----------------+------------------------+--------------+
    |           |                | ``calorie``            |              |
    +-----------+----------------+------------------------+--------------+
    |           |                | ``kilocalorie``        |              |
    +-----------+----------------+------------------------+--------------+
    |           |                | ``kilocalorie_permol`` |              |
    +-----------+----------------+------------------------+--------------+
    |           |                | ``ev``                 |              |
    +-----------+----------------+------------------------+--------------+
    |           |                | ``hartree``            |              |
    +-----------+----------------+------------------------+--------------+


Package indices
================

.. toctree::
    :maxdepth: 1

    baseDimension
    unit
    quantity