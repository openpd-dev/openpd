======================
openpd.core.Atom class
======================

Introduction
============

``openpd.core.Atom`` is designed to store atoms' information, as the most fundamental class of ``openpd.core`` package.

The ``openpd.core.Atom`` is defined by two parameter:

- The name of atom;
- The mass of atom;

These two parameter are the determinative identification of atom in OpenPD. 

.. note::

   Meanwhile, the peptide type also affects the interaction of atoms in PDFF.  However, this can be determined only after create a ``Peptide`` instance. So, the user will hardly have an opportunity and need to create a ``Atom`` instance by themselves as this work has been accomplished when creating a ``Peptide`` instance.

.. seealso::

   - :doc:`../../pdff/overview`
   - :doc:`peptide`

Class methods
==============

.. automodule:: openpd.core.atom
   :members:
   :undoc-members:
   :show-inheritance:

.. important::

   Read-only properties:

   - ``atom_type``
   - ``mass``

   Editable properties:

   - ``atom_id``
   - ``peptide_type``
   - ``coordinate``
   - ``velocity``
   - ``potential_energy``
   - ``kinetic_energy``
   - ``force``

Examples
==============

Instantiation
--------------

**Input**:

.. code-block:: python
   :linenos:

   import openpd as pd

   atom = pd.Atom('Ca', 12)
   
   print(atom)
   print(atom.atom_type)
   print(atom.mass)
   print(atom.coordinate)
   print(atom.velocity)

   print(atom.peptide_type)
   atom.peptide_type = 'TYR'
   print(atom.peptide_type)

   atom.coordinate = np.array([1, 2, 3])
   print(atom.coordinate)

**Output**:

.. parsed-literal::

   <Atom object: id 0, type Ca, of peptide None at 0x7fb09fbd2bd0>
   Ca
   12
   [0. 0. 0.]
   [0. 0. 0.]
   None
   TYR
   [1. 2. 3.]