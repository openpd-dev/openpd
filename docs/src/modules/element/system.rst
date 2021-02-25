============================
openpd.element.System class
============================

Overview
===========

``openpd.element.System`` is the ultima class for model representation. A ``System`` instance is consists of a series of ``Chain`` instances. 

Meanwhile, the ``System`` will also create a ``Topology`` instance during the instantiation and adding topology information when call ``System.addChains()`` method.

.. seealso::

   :doc:`topology` page

Class methods
==============

.. automodule:: openpd.element.system
   :members:
   :undoc-members:
   :show-inheritance:

.. note::
   
   The ``chain_id`` of added ``chain`` will be changed to follow the adding order, so do their affiliated ``peptide``. 

.. important::

   Read-only properties:

   - ``num_atoms``
   - ``atoms``
   - ``num_peptides``
   - ``peptides``
   - ``num_chains``
   - ``chains``

   Editable properties:

   - ``coordinate``

Example
==============

Instantiation
-------------

**Input**:

.. code-block:: python
   :linenos:

   import openpd as pd

   peptide1 = pd.Peptide('TYR')
   peptide2 = pd.Peptide('ASN')

   chain1 = pd.Chain()
   chain1.addPeptides(peptide1, peptide2)
   chain2 = pd.Chain()
   chain2.addPeptides(peptide2, peptide1)

   system = pd.System()
   system.addChains(chain1, chain2)

   for chain in system.chains:
      print(chain)

   for peptide in system.peptides:
      print(peptide)
      
   for atom in system.atoms:
      print(atom)
      
   print(system.topology)

**Output**:

.. parsed-literal::

   <Chain object: id 0, with 2 peptides, at 0x7fb09fbd2310>
   <Chain object: id 1, with 2 peptides, at 0x7fb09fbd23d0>
   <Peptide object: id 0, type TYR, of chain 0 of 0x7fb09fbd2450>
   <Peptide object: id 1, type ASN, of chain 0 of 0x7fb09fbd24d0>
   <Peptide object: id 2, type ASN, of chain 1 of 0x7fb09fbd2810>
   <Peptide object: id 3, type TYR, of chain 1 of 0x7fb09fbd2890>
   <Atom object: id 0, type CA, of peptide TYR at 0x7fb09fbd2590>
   <Atom object: id 1, type SC, of peptide TYR at 0x7fb09fbd2610>
   <Atom object: id 2, type CA, of peptide ASN at 0x7fb09fbd2710>
   <Atom object: id 3, type SC, of peptide ASN at 0x7fb09fbd2790>
   <Atom object: id 4, type CA, of peptide ASN at 0x7fb09fbd2950>
   <Atom object: id 5, type SC, of peptide ASN at 0x7fb09fbd29d0>
   <Atom object: id 6, type CA, of peptide TYR at 0x7fb09fbd2ad0>
   <Atom object: id 7, type SC, of peptide TYR at 0x7fb09fbd2b50>
   <Topology object: 8 atoms, 6 bonds, 4 angles, 2 torsions at 0x7fb09e385bd0>