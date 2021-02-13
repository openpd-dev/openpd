==============================
openpd.loader.PDBLoader class
==============================

Overview
===========

``openpd.loader.PDBLoader`` is designed to load a *.pdb* file and create a ``System`` instance. Two methods to set coordinate are supported:

- ``extractCoordinates()`` extracts the coordinate information from the input *.pdb* file.
- ``guessCoordinates()`` guesses the coordinate to form a straight peptide line.

.. seealso::

   ``guessCoordinates()`` method is talked in detail in :doc:`loader` Page
  

Class methods
==============
.. automodule:: openpd.loader.pdbLoader
   :members:
   :undoc-members:
   :show-inheritance:


Example
=========

.. seealso::

   The usage of ``PDBLoader`` is discussed in :ref:`using-pdbLoader`.