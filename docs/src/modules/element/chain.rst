==========================
openpd.element.Chain class
==========================

Introduction
============

``openpd.element.Chain`` is designed to represent a peptide chain. It is consists of a series of ``Peptide`` instances.

Class methods
==============

.. automodule:: openpd.element.chain
   :members:
   :undoc-members:
   :show-inheritance:

.. note::
   
   The ``atom_id`` of atoms in the added ``peptide`` will be changed to follow the adding order. And the ``chain_id`` of added ``peptide`` will be set to the ``chain_id`` of current ``chain``.

.. important::

   Read-only properties:

   - ``num_atoms``
   - ``atoms``
   - ``num_peptides``
   - ``peptides``

   Editable properties:

   - ``chain_id``

Example 
========

Instantiation
---------------

**Input**:

.. code-block:: python 
   :linenos:

   import openpd as pd

   peptide1 = pd.Peptide('TYR')
   peptide2 = pd.Peptide('ASN')

   chain = pd.Chain()
   chain.addPeptides(peptide1, peptide2)

   for peptide in chain.peptides:
      print(peptide)
      
   for atom in chain.atoms:
      print(atom)

**Output**:

.. parsed-literal::

   <Peptide object: id 0, type TYR, of chain 0 of 0x7fb09fbdd790>
   <Peptide object: id 1, type ASN, of chain 0 of 0x7fb09fbdd6d0>
   <Atom object: id 0, type CA, of peptide TYR at 0x7fb09fbddb50>
   <Atom object: id 1, type SC, of peptide TYR at 0x7fb09fbddbd0>
   <Atom object: id 2, type CA, of peptide ASN at 0x7fb09fbddcd0>
   <Atom object: id 3, type SC, of peptide ASN at 0x7fb09fbddd50>
