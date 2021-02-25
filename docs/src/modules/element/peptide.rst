=============================
openpd.element.Peptide class
=============================

Introduction
============

``openpd.element.Peptide`` is designed to represent the peptides of protein. When the user creates an instance of ``Peptide``, only the type of peptide is needed, like ``"ASN"``. Both single and triple letter abbreviation is supported. 

However, the peptide type must be included in the standard peptide list shown below:

.. code-block:: python 
   :linenos:

   TRIPLE_LETTER_ABBREVIATION = [
      'ALA', 'ARG', 'ASN', 'ASP',
      'CYS', 'GLN', 'GLU', 'GLY',
      'HIS', 'ILE', 'LEU', 'LYS',
      'MET', 'PHE', 'PRO', 'SER',
      'THR', 'TRP', 'TYR', 'VAL'
   ]

   SINGLE_LETTER_ABBREVIATION = [
      'A', 'R', 'N', 'D',
      'C', 'Q', 'E', 'G',
      'H', 'I', 'L', 'K',
      'M', 'F', 'P', 'S',
      'T', 'W', 'Y', 'V'
   ]

After specifying the peptide type, the attributes of ``Peptide`` will be automatically set up by searching the template *.json* file like:

.. code-block:: json
   :linenos:

   {
      "name": "TYR",
      "parent_atoms": {
         "CA": {"mass": 12}, 
         "SC": {"mass": 192}
      },
      "ca_sc_dist": 5
   }

, all of which are stored in ``<openpd source code folder>/openpd/data/template``.

Class methods
==============

.. automodule:: openpd.element.peptide
   :members:
   :undoc-members:
   :show-inheritance:

.. note::
   
   The ``atom_id`` of added ``atom`` will be changed to follow the adding order and the ``peptide_type`` will be set to the ``peptide_type`` of current ``peptide``. 

.. important::

   Read-only properties:

   - ``peptide_type``
   - ``num_atoms``
   - ``atoms``
   - ``ca_sc_dist``

   Editable properties:

   - ``peptide_id``
   - ``chain_id``

Examples
=========

Instantiation
--------------

**Input**:

.. code-block:: python
   :linenos:

   import openpd as pd

   peptide = pd.Peptide('TYR')

   print(peptide.peptide_id)
   for atom in peptide.atoms:
      print(atom, atom.mass)
   print(peptide.num_atoms)


**Output**:

.. parsed-literal::

   0
   <Atom object: id 0, type CA, of peptide TYR at 0x7fb09fbe3050> 12
   <Atom object: id 1, type SC, of peptide TYR at 0x7fb09fbe30d0> 192
   2

Add atoms
---------

**Input**

.. code-block:: python
   :linenos:

   import openpd as pd

   peptide = pd.Peptide('TYR')
   peptide.addAtoms(pd.Atom('CA', 12), pd.Atom('CA', 12))

   for atom in peptide.atoms:
   print(atom, atom.mass)
   print(peptide.num_atoms)


**Output**:

.. parsed-literal::

   <Atom object: id 0, type CA, of peptide TYR at 0x7fb09fbc7dd0> 12
   <Atom object: id 1, type SC, of peptide TYR at 0x7fb09fbc78d0> 192
   <Atom object: id 2, type CA, of peptide TYR at 0x7fb09fbc79d0> 12
   <Atom object: id 3, type CA, of peptide TYR at 0x7fb09fbc7f50> 12
   4