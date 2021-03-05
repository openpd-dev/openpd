======================
openpd.element package
======================

The ``openpd.element`` package is designed to represent the simulation system. Naturally, a typical protein system contains one or several chains, which consist of many peptides. And the peptides are constituted by atoms. Further, the atoms' connection will form the topology of the whole system. All **elements** described above are contained in ``openpd.element`` package.

Following this fact, the ``openpd.element`` package is designed as below:

-----------------------------

.. image:: ./images/element.svg
    :width: 700
    :align: center

-----------------------------

The ``System`` is the final model that we will use to create a ``Simulation``. Usually, the creation of a ``System`` can be automatically done by a ``loader`` in ``openpd.loader`` package.

.. seealso::

    - :doc:`../simulation` page
    - :doc:`../../tutorials/howto_createSystem/main` page
    - :doc:`../loader/main` page


.. toctree::
    :maxdepth: 1

    atom 
    peptide
    chain
    system
    topology